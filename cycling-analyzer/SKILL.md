---
name: cycling-analyzer
description: >
  Analysiert Radtraining-Einheiten über die intervals.icu API und vergleicht
  sie mit dem Trainingsplan (Markdown). Gibt Soll/Ist-Analyse, Wochenübersicht,
  Intervall-Qualität (Power-Decay, Drehmoment, Entkopplung) und Trendanalyse
  über mehrere Einheiten aus. Immer verwenden wenn der Nutzer nach
  Trainingsauswertung fragt, seinen Trainingsplan auswerten möchte,
  Soll/Ist-Vergleich beim Radfahren braucht, TSS/NP/IF/FTP-Werte analysieren
  will, Intervall-Qualität oder Kraftausdauer-Entwicklung bewerten möchte,
  oder Begriffe wie TSS, NP, IF, FTP, Powerzonen, Polarisierung, K3,
  Trainingsstress, CTL, ATL, Pw:Hr, VI, intervals.icu erwähnt.
---

# Cycling Analyzer Skill

Analysiert Radtraining-Einheiten über den **intervals.icu MCP-Server** und
vergleicht sie mit dem Trainingsplan. Datenquelle ist intervals.icu.

---

## 0. Credentials

Credentials sind dauerhaft gespeichert in:
`~/.claude/skills/cycling-analyzer/.icu_creds`

Lese die Datei mit dem Read-Tool und extrahiere `ATHLETE_ID` und `API_KEY`.
Diese Werte werden bei jedem MCP-Tool-Aufruf als `athlete_id` und `api_key`
übergeben.

Wenn die Datei nicht existiert: Nutzer einmalig nach Athlete-ID und API Key
fragen (intervals.icu/settings → "Developer Settings"), dann speichern:

```
ATHLETE_ID=iXXXXXX
API_KEY=xxxxxxxxxxxx
```

---

## 1. Daten abrufen via MCP-Tools

### Aktivitäten eines Zeitraums

`mcp__intervals-icu__get_activities` mit:
- `athlete_id`, `api_key`
- `start_date` / `end_date` (YYYY-MM-DD)
- `limit` — großzügig wählen (z.B. 20) bei Trendanalysen

→ Liefert pro Aktivität: ID, Name, Typ, Datum, Dauer, Distanz, avg/weighted
Power, TSS, IF, HR, Kadenz, CTL, ATL, L/R Balance, Decoupling, Polarization
Index.

### Intervall-Details einer Aktivität

Wenn Intervall-Analyse nötig (K3, Z5, Over-Under):
1. Erst `get_activities` → Activity-ID ermitteln
2. Dann `mcp__intervals-icu__get_activity_intervals` mit `activity_id` und `api_key`

→ Liefert alle WORK/REST-Segmente mit Power, HR, Kadenz, Drehmoment,
Entkopplung pro Intervall.

### Einzelne Aktivität (Detailansicht)

`mcp__intervals-icu__get_activity_details` mit `activity_id` und `api_key`

→ Liefert vollständige Metriken einer einzelnen Einheit.

### Wellness / CTL-ATL-Verlauf

`mcp__intervals-icu__get_wellness_data` mit `athlete_id`, `api_key`,
`start_date`, `end_date`

→ Liefert tägliche CTL (Fitness), ATL (Fatigue), Form (TSB), HRV, Schlaf,
Gewicht.

---

## 2. Trainingsplan lesen

Suche im Projektordner nach dem Trainingsplan (typisch `kw*_trainingspeaks.md`,
`grobplan.md`). Identifiziere:

- **Wochenstruktur**: Welche Einheit ist für welchen Tag geplant?
- **Einheitstypen**: Z2, K3, Z5, Over-Under, Aktivierung
- **Ziel-TSS**: Woche und Einheit
- **Intensitätsvorgaben**: Powerzonen, Watt-Ziele, Kadenz
- **FTP-Basis**: Im Plan vermerkt?

---

## 3. Soll/Ist-Vergleich (Einzel-Analyse)

Ordne die Einheit dem Plan zu und erstelle:

| Kennzahl | Soll (Plan) | Ist (intervals.icu) | Abweichung |
|---|---|---|---|
| TSS | z.B. 90 | 56 | −38% |
| Dauer | 1:15h | 0:47:32 | −37% |
| NP | ~265W | 233W | −12% |
| IF | ~0.96 | 0.85 | ⚠ |
| Typ | K3 Kraftausdauer | ✓ | ✓ |

**Intervall-Qualität** (wenn Intervall-Daten vorhanden):

| Kennzahl | Wert | Bewertung |
|---|---|---|
| Intervalle abgeschlossen | 2/3 | ⚠ |
| Power-Decay | −2.6% | ✓ gut |
| Avg Drehmoment | 43 Nm | ✓ K3-Level |
| Pw:Hr-Entkopplung | 2.1% | ✓ (<5%) |
| HR-Drift 1.→letztes Int. | +4 bpm | ✓ stabil |

**CTL/ATL-Kontext** (immer wenn verfügbar angeben):

| Kennzahl | Wert | Bedeutung |
|---|---|---|
| CTL (Fitness) | z.B. 34 | Langfristige Fitness |
| ATL (Fatigue) | z.B. 62 | Akute Ermüdung |
| ATL/CTL-Ratio | 1.8 | >2.0 = Überlastungsrisiko |

**Polarisierungscheck** (für Z2-Einheiten):
- Optimal: ~80% Zeit Z1/Z2, ~20% Z4–Z6
- Z3-Anteil > 30% = "Sweetspot-Drift"
- Polarization Index aus MCP direkt verfügbar — nutzen

**L/R Balance** (bei Außenfahrten):
- Normalbereich: 48–52% links
- Abweichung >3% konsistent = Asymmetrie-Hinweis

---

## 4. Wochenübersicht

Wenn mehrere Einheiten im Zeitraum vorliegen:

- Gesamt-TSS der Woche vs. Plan-Ziel
- CTL/ATL-Verlauf über die Woche
- Tagesverteilung der Belastung
- Hochintensive Einheiten: Qualität der Intervalle

---

## 5. Trendanalyse (≥ 3 gleiche Einheitstypen)

Wenn mehrere Einheiten desselben Typs vorliegen:

**Power-Decay-Trend**: Wird der Leistungsabfall über die Intervallserie kleiner?
→ Zeichen verbesserter Kraftausdauer.

**NP-Trend**: Steigt die Normalized Power bei gleichem IF?
→ Echte FTP-Entwicklung.

**Drehmoment-Trend** (K3): Bleibt `avg_torque_nm` konstant bei steigenden Watts?
→ Motorisches Muster verbessert sich.

**HR-Effizienz-Trend**: Fällt HR bei gleicher Leistung?
→ Aerobe Adaptation.

**CTL-Trend**: Steigt CTL über Wochen konsistent?
→ Positive Trainingsanpassung.

### Ausgabeformat Trendanalyse

Kompakte Tabelle: Datum | NP | Power-Decay | Drehmoment | HR | CTL — eine Zeile
pro Einheit. Dann Evidence-basierte Aussage:

> "3 von 4 K3-Einheiten zeigen Power-Decay < 5% bei Ø 43 Nm — stabile
> Kraftausdauer. NP-Trend: 225 → 231 → 233W. CTL: 28 → 32 → 35."

---

## 6. Stärken / Schwächen / Entwicklung

### Stärken (konsistente Positivbefunde)
Aerobe Effizienz (Pw:Hr), HR-Stabilität in Z2, Kadenz, niedrige Entkopplung,
L/R-Symmetrie, steigende CTL.

### Schwächen (wiederkehrende Muster)
Power-Decay im letzten Intervall, erhöhter VI, HR über Sollbereich bei Z2,
L/R-Asymmetrie, hohe ATL/CTL-Ratio.

**Immer Evidence-basiert formulieren:**
- ✗ "Du hast ein Kraftausdauerdefizit"
- ✓ "3 von 4 Z5-Einheiten zeigen Power-Decay > 8% im letzten Intervall —
  deutet auf muskuläre Limitierung hin"

---

## 7. Empfehlung nächste Einheit

- Was steht im Plan?
- CTL/ATL-Ratio beachten: bei ATL/CTL > 2.0 Warnung ausgeben
- Regenerations-Warnung wenn TSS > 120 oder IF > 0.85

---

## Referenzwerte

### TSS-Kategorien
| TSS | Erholung | Nächste Einheit |
|---|---|---|
| < 150 | Minimal (<24h) | Normal |
| 150–300 | Normal (24h) | Leichte Einheit ok |
| 300–450 | Signifikant | Z2 oder Pause |
| > 450 | Sehr groß | Min. 48h Pause |

### ATL/CTL-Ratio (Fatigue/Fitness)
| Ratio | Zustand |
|---|---|
| < 1.0 | Frisch / Taper |
| 1.0–1.5 | Normales Training |
| 1.5–2.0 | Hohe Belastung — beobachten |
| > 2.0 | Überlastungsrisiko — Warnung |

### Intensity Factor (IF)
| IF | Charakter |
|---|---|
| < 0.75 | Erholungsfahrt / leichtes Z2 |
| 0.75–0.85 | Ausdauer Z2/Z3 |
| 0.85–0.95 | Tempofahrt / Schwellentraining |
| > 0.95 | Kurzes Rennen / Maximalintervall |

### Variability Index (VI = NP/AvgPower)
| VI | Charakter |
|---|---|
| < 1.05 | Sehr gleichmäßig |
| 1.05–1.10 | Normal für Terrain |
| > 1.10 | Hohes Intensitätsgefälle |

### Power-Zonen (% FTP nach Coggan)
| Zone | % FTP | Bezeichnung |
|---|---|---|
| Z1 | < 55% | Aktive Erholung |
| Z2 | 56–75% | Grundlagenausdauer |
| Z3 | 76–90% | Tempo |
| Z4 | 91–105% | Laktatschwelle |
| Z5 | 106–120% | VO2max |
| Z6 | > 120% | Anaerob / Sprint |

### Drehmoment-Referenz (K3 Kraftausdauer)
| Kadenz | Watt | Nm | Charakter |
|---|---|---|---|
| 90 rpm | 265W | ~28 Nm | Normal |
| 60 rpm | 265W | ~42 Nm | K3-Level |
| 50 rpm | 265W | ~50 Nm | Maximaler K3-Reiz |

---

## Workout-Events in intervals.icu erstellen

Verwende `mcp__intervals-icu__add_or_update_event` zum Anlegen von Trainingsevents.

### Sprint-Schritte (ALL OUT / HT-Sprints)

**Niemals `maxeffort: true` verwenden** — Wahoo und Zwift lehnen das ab:
- Wahoo: "each interval must have a valid targets array"
- Zwift: "Element 'MaxEffort' must have no element [children]"

**Korrekt für All-Out-Sprints:** Absoluten Wattwert **900W** verwenden:
```json
{"duration": 12, "power": {"value": 900, "units": "w"}, "text": "Sprint ALL OUT"}
```

Grund: 900W ist hoch genug dass der Athlet im ERG-Modus (Zwift/Wahoo) aus dem
Modus herausgedrückt wird und frei sprintet — genau das gewünschte Verhalten
für 10–15'' All-Out-Sprints.

### Verschachtelte Steps

Nur eine Ebene Verschachtelung erlaubt. `reps` innerhalb von `reps` führt zu
"Nested steps not supported". Mehrere separate Repeat-Blöcke hintereinander
(z.B. 3× Set als drei einzelne `reps`-Blöcke) funktioniert.

---

## Fehlerbehandlung

- **403 Forbidden**: athlete_id oder api_key falsch — Creds-Datei prüfen
- **Keine Aktivitäten**: Zeitraum anpassen, anderen Datumsbereich vorschlagen
- **Kein FTP**: Nutzer fragen, 275W als Fallback (mit Hinweis)
- **Keine Intervall-Daten**: Nur bei Einheiten mit erkannten Intervallen
  `get_activity_intervals` aufrufen — bei reinen Z2 weglassen
- **L/R Balance fehlt**: Als "Keine Pedaldaten / Zwift-Session" kennzeichnen
