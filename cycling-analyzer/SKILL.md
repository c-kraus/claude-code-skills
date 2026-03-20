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

Analysiert Radtraining-Einheiten über die **intervals.icu API** und vergleicht
sie mit dem Trainingsplan. Datenquelle ist intervals.icu (nicht mehr FIT-Dateien).

---

## 0. Credentials (einmalig pro Session)

Prüfe ob `/tmp/.icu_creds` existiert:

```bash
cat /tmp/.icu_creds 2>/dev/null
```

Wenn die Datei nicht existiert oder leer ist: **Frage den Nutzer einmalig**
nach Athlete-ID und API Key (zu finden unter intervals.icu/settings →
"Developer Settings"). Schreibe dann:

```bash
printf 'ATHLETE_ID=%s\nAPI_KEY=%s\n' "<id>" "<key>" > ~/.claude/skills/cycling-analyzer/.icu_creds
chmod 600 ~/.claude/skills/cycling-analyzer/.icu_creds
```

Die Datei ist dauerhaft gespeichert und in `.gitignore` eingetragen — wird
nie nochmals abgefragt.

---

## 1. Daten abrufen

Installiere das requests-Package falls nötig:

```bash
pip3 install requests --break-system-packages -q
```

### Einzelner Tag / aktuelle Einheit

```bash
python3 ~/.claude/skills/cycling-analyzer/scripts/fetch_intervals_icu.py \
  --creds-file /tmp/.icu_creds \
  --date YYYY-MM-DD \
  --with-intervals
```

### Letzte N Tage (Wochenübersicht)

```bash
python3 ~/.claude/skills/cycling-analyzer/scripts/fetch_intervals_icu.py \
  --creds-file /tmp/.icu_creds \
  --days 7
```

### Trendanalyse (mehrere Wochen, mit Intervall-Details)

```bash
python3 ~/.claude/skills/cycling-analyzer/scripts/fetch_intervals_icu.py \
  --creds-file /tmp/.icu_creds \
  --oldest YYYY-MM-DD --newest YYYY-MM-DD \
  --with-intervals
```

Das Skript gibt strukturiertes JSON zurück mit:
- `activities[]`: Liste der Radeinheiten im Zeitraum
- Pro Aktivität: `avg_power_w`, `normalized_power_w` (NP), `ftp_w`,
  `intensity_factor` (IF), `tss`, `variability_index` (VI), `avg_hr`,
  `max_hr`, `avg_cadence`, `left_right_balance`, `pw_hr`
- Bei `--with-intervals`: `intervals[]` (jedes WORK/REST-Segment) und
  `interval_summary` mit `power_decay_pct`, `avg_torque_nm`,
  `avg_decoupling_pct`, `hr_drift_pct`

---

## 2. Trainingsplan lesen

Suche im Projektordner nach dem Trainingsplan (typisch `kw*_trainingspeaks.md`,
`grobplan.md`, oder ähnlich). Identifiziere:

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

**Intervall-Qualität** (wenn `interval_summary` vorhanden):

| Kennzahl | Wert | Bewertung |
|---|---|---|
| Intervalle abgeschlossen | 2/3 | ⚠ |
| Power-Decay | −2.6% | ✓ gut |
| Avg Drehmoment | 43 Nm | ✓ K3-Level |
| Pw:Hr-Entkopplung | 2.1% | ✓ (<5%) |
| HR-Drift 1.→letztes Int. | +4 bpm | ✓ stabil |

**Polarisierungscheck** (für Z2-Einheiten):
- Optimal: ~80% Zeit Z1/Z2, ~20% Z4–Z6
- Z3-Anteil > 30% = "Sweetspot-Drift"

---

## 4. Wochenübersicht

Wenn mehrere Einheiten im Zeitraum vorliegen:

- Gesamt-TSS der Woche vs. Plan-Ziel
- Tagesverteilung der Belastung
- Hochintensive Einheiten: Qualität der Intervalle (Power-Decay, VI)

---

## 5. Trendanalyse (≥ 3 gleiche Einheitstypen)

Wenn mehrere Einheiten desselben Typs vorliegen (z.B. alle K3-Sessions der
letzten 8 Wochen), berechne Trends **auf Basis tatsächlicher Evidenz**:

### Was zu analysieren ist

**Power-Decay-Trend**: Wird der Leistungsabfall über die Intervallserie
kleiner? → Zeichen verbesserter Kraftausdauer.

**NP-Trend**: Steigt die Normalized Power bei gleichem IF? → Echte FTP-Entwicklung.

**Drehmoment-Trend** (K3): Bleibt `avg_torque_nm` konstant bei steigenden Watts?
→ Motorisches Muster verbessert sich.

**HR-Effizienz-Trend**: Fällt HR bei gleicher Leistung? → Aerobe Adaptation.

**Entkopplungs-Trend**: Nimmt `avg_decoupling_pct` ab? → Bessere Ausdauer.

### Ausgabeformat Trendanalyse

Zeige eine kompakte Tabelle mit Datum, NP, Power-Decay, Drehmoment, HR — eine
Zeile pro Einheit. Dann formuliere den Trend als Evidence-basierte Aussage:

> "3 von 4 K3-Einheiten zeigen Power-Decay < 5% bei Ø 43 Nm — das deutet auf
> stabile Kraftausdauer hin. NP-Trend: 225 → 231 → 233W über 6 Wochen."

---

## 6. Stärken / Schwächen / Entwicklung

Am Ende jeder Analyse (besonders bei mehreren Einheiten):

### Stärken (konsistente Positivbefunde)
Was zeigen die Daten wiederholt positiv: aerobe Effizienz (Pw:Hr),
HR-Stabilität in Z2, konsistente Kadenz, niedrige Entkopplung.

### Schwächen (wiederkehrende Muster)
Wiederkehrende Auffälligkeiten: Power-Decay im letzten Intervall, erhöhter VI,
HR über Sollbereich bei Z2, Asymmetrie Links/Rechts (falls Daten vorhanden).

**Wichtig: Immer Evidence-basiert formulieren:**
- ✗ "Du hast ein Kraftausdauerdefizit"
- ✓ "3 von 4 Z5-Einheiten zeigen Power-Decay > 8% im letzten Intervall bei
  HR < 88% HFmax — das deutet auf muskuläre Limitierung hin"

### Entwicklung (Trend über Zeit)
Nur wenn ≥ 3 vergleichbare Einheiten vorliegen. Trenne klar:
- **Gesicherte Evidenz**: Zahlen aus der API
- **Interpretation**: Physiologische Schlussfolgerung daraus

---

## 7. Empfehlung nächste Einheit

- Was steht im Plan?
- Anpassung nötig aufgrund der heutigen Belastung (TSS, HR-Trend)?
- Regenerations-Warnung wenn TSS > 120 oder IF > 0.85 für eine Einzeleinheit

---

## Referenzwerte

### TSS-Kategorien
| TSS | Erholung | Nächste Einheit |
|---|---|---|
| < 150 | Minimal (<24h) | Normal |
| 150–300 | Normal (24h) | Leichte Einheit ok |
| 300–450 | Signifikant | Z2 oder Pause |
| > 450 | Sehr groß | Min. 48h Pause |

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
| < 1.05 | Sehr gleichmäßig (Flachstrecke, Z2) |
| 1.05–1.10 | Normal für Training mit Terrain |
| > 1.10 | Hohes Intensitätsgefälle (Intervalle/Berge) |

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

## Fehlerbehandlung

- **401 / Authentifizierung**: Credentials ungültig — neu abfragen, Creds-Datei löschen
- **Keine Aktivitäten im Zeitraum**: Explizit melden, anderen Zeitraum vorschlagen
- **Kein FTP in Daten**: Nutzer nach aktuellem FTP fragen, 275W als Fallback (mit Hinweis)
- **Keine Intervall-Daten**: `--with-intervals` nur bei Einheiten mit erkannten Intervallen sinnvoll — bei reinen Z2-Einheiten weglassen
- **Rechts-Links-Balance fehlt**: Explizit als "Keine Pedaldaten verfügbar" kennzeichnen
