---
name: cycling-analyzer
description: >
  Analysiert Radtraining-Einheiten aus Wahoo/Garmin FIT-Dateien (.fit, .fit.gz)
  und vergleicht sie mit dem Trainingsplan (Markdown). Gibt Soll/Ist-Analyse,
  Wochenübersicht, Empfehlungen für die nächste Einheit und optional einen
  Quarto/Markdown-Report aus. Immer verwenden wenn der Nutzer FIT-Dateien
  hochlädt, nach Trainingsauswertung fragt, seinen Trainingsplan auswerten
  möchte, Soll/Ist-Vergleich beim Radfahren braucht, oder Begriffe wie
  TSS, NP, IF, FTP, Powerzonen, Polarisierung, Trainingsstress,
  Wochenvolumen, CTL, ATL erwähnt.
---

# Cycling Analyzer Skill

Analysiert Radtraining-Einheiten aus FIT-Dateien und vergleicht sie mit
einem Trainingsplan in Markdown-Format.

## Workflow

### 1. FIT-Datei(en) einlesen

Nutze das Analyse-Skript für alle bereitgestellten FIT-Dateien:

```bash
pip install fitparse --break-system-packages -q
python scripts/analyze_fit.py <datei.fit.gz> [weitere Dateien...]
```

Das Skript gibt strukturiertes JSON zurück mit:
- `date`, `duration_hms`, `distance_km`, `total_ascent_m`
- `avg_power_w`, `normalized_power_w`, `ftp_w`, `intensity_factor`, `tss`
- `avg_hr`, `max_hr`, `avg_cadence`, `avg_speed_kmh`
- `power_zones` (Z1–Z6 mit Sekunden und Prozent)
- `hr_zones` (Z1–Z5 mit Sekunden und Prozent)
- `polarization` (low/mid/high %-Anteile)
- `workout_name` (geplante Einheit laut Gerät, falls vorhanden)

### 2. Trainingsplan lesen

Suche im Projektordner nach der Trainingsplan-Datei (typisch: `trainingsplan.md`,
`plan.md`, oder ähnlich). Lies die Datei und identifiziere:

- **Wochenstruktur**: Welche Einheiten sind für welchen Wochentag geplant?
- **Einheitstypen**: Z2-Grundlage, Intervall, Tempo, Erholung, Langer Ritt
- **Ziel-TSS**: Falls angegeben (Woche, Einheit)
- **Intensitätsvorgaben**: Powerzonen, HR-Zonen, RPE
- **FTP-Basis**: Falls im Plan vermerkt

**Wenn kein Plan im Projektordner gefunden wird**: Frage den Nutzer nach dem
Pfad oder fahre mit reiner Einzel-Analyse ohne Soll/Ist-Vergleich fort.

### 3. Soll/Ist-Vergleich

Ordne die analysierte Einheit dem Trainingsplan zu (nach Datum und Einheitstyp)
und erstelle den Vergleich:

| Kennzahl          | Soll (Plan)     | Ist (Einheit)   | Abweichung |
|-------------------|-----------------|-----------------|------------|
| TSS               | z.B. 80–100     | 112.2           | +12–32%    |
| Dauer             | z.B. 2:30       | 2:41:55         | +8%        |
| Intensitäts-Typ   | Z2-Grundlage    | Z2/Z3-gemischt  | ⚠          |
| Distanz           | ~70 km          | 65.3 km         | -7%        |

**Polarisierungscheck**: Für polarisiertes Training ist die Faustformel:
- Optimal: ~80% Zeit in Z1/Z2 (aerob niedrig), ~20% in Z4–Z6 (hochintensiv)
- Z3-Anteil ("Mittelmaß-Zone") > 30% gilt als suboptimal

### 4. Wochenübersicht (falls mehrere Dateien / Wochenkontext)

Wenn mehrere Einheiten vorliegen oder der Wochenkontext aus dem Plan
rekonstruiert werden kann:

- Gesammt-TSS der Woche vs. Ziel-TSS
- Verteilung der Trainingsbelastung über die Woche
- Kumulierter ATL-Schätzwert (Acute Training Load: 7-Tage-TSS-Durchschnitt)

### 5. Empfehlungen

Leite konkrete Empfehlungen ab:

**Für die nächste Einheit:**
- Was steht im Plan?
- Anpassung nötig aufgrund der heutigen Belastung?
- Regenerations-Warnung wenn TSS > 120 oder IF > 0.85 für die Einheit

**Intensitäts-Drift erkennen:**
- Wenn Z3-Anteil > 30%: "Sweetspot-Drift" – nächste Z2-Einheit strikt unter FTP
- Wenn Ø HR bei Z2 zu hoch: Ermüdungszeichen, Erholungseinheit empfehlen
- Wenn NP >> Avg Power (NP/AvgP > 1.15): Sehr variable Intensität

**Qualitätsaussagen:**
- Trainingseffizienz: TSS/h (typisch: Z2 ~50-60, Intervall ~80-100)
- Links/Rechts-Balance (falls vorhanden, aus `left_right_balance`)

### 6. Output-Format

#### Standard-Ausgabe (in der Konversation)

Strukturierter Bericht mit:
1. **Einheit-Zusammenfassung** (kompakte Tabelle)
2. **Soll/Ist-Vergleich** (nur wenn Trainingsplan vorhanden)
3. **Zonen-Analyse** (Power & HR als kompakte Tabelle)
4. **Empfehlung nächste Einheit** (1-3 konkrete Sätze)

#### Quarto/Markdown-Report (wenn explizit angefragt)

Erstelle eine `.qmd` oder `.md` Datei mit:
- YAML-Frontmatter (title, date, format: html/pdf)
- Alle Tabellen als Markdown-Tabellen
- Zonenverteilung als textuelle Beschreibung (keine Bibliotheken nötig)
- Abschnitte: Einheit | Soll/Ist | Zonen | Empfehlung | Nächste Woche

Speichere als `training-report-YYYY-MM-DD.qmd` im aktuellen Projektordner
oder `/mnt/user-data/outputs/`.

## Referenzwerte (Radsport)

### TSS-Kategorien
| TSS      | Erholung       | Nächste Einheit       |
|----------|----------------|----------------------|
| < 150    | Minimal (<24h) | Normal               |
| 150–300  | Normal (24h)   | Leichte Einheit ok   |
| 300–450  | Signifikant    | Z2 oder Pause        |
| > 450    | Sehr groß      | Mindestens 48h Pause |

### Intensity Factor (IF)
| IF       | Charakter                        |
|----------|----------------------------------|
| < 0.75   | Erholungsfahrt / leichtes Z2     |
| 0.75–0.85| Ausdauer Z2/Z3                   |
| 0.85–0.95| Tempofahrt / Schwellentraining   |
| > 0.95   | Kurzes Rennen / Maximalintervall |

### Power-Zonen (% FTP nach Coggan)
| Zone | % FTP    | Bezeichnung         |
|------|----------|---------------------|
| Z1   | < 55%    | Aktive Erholung     |
| Z2   | 56–75%   | Grundlagenausdauer  |
| Z3   | 76–90%   | Tempo               |
| Z4   | 91–105%  | Laktatschwelle      |
| Z5   | 106–120% | VO2max              |
| Z6   | > 120%   | Anaerob / Sprint    |

## Hinweise zur Trainingsplan-Interpretation

Typische Markdown-Formate für Trainingspläne:

```markdown
## Woche 3 – Aufbau

| Tag  | Einheit         | Dauer  | TSS  | Beschreibung         |
|------|-----------------|--------|------|----------------------|
| Mo   | Pause/Mobility  | –      | 0    |                      |
| Di   | Z2 Grundlage    | 2:00   | 70   | Strikt unter FTP     |
| Mi   | Intervalle      | 1:30   | 95   | 4×8 min @ 95–105%FTP |
```

Erkenne auch narrative Formate ohne Tabelle und extrahiere Einheitstyp,
Dauer, Intensitätsangaben.

## Fehlerbehandlung

- **Kein FTP in FIT-Datei**: Frage den Nutzer, nutze 250W als Fallback mit
  explizitem Hinweis
- **Keine Power-Daten**: Analysiere nur HR-Zonen und RPE-basiert
- **Plan nicht gefunden**: Reine Einzel-Analyse, TSS-Einordnung nach
  Referenztabelle, keine Soll/Ist-Spalte
- **Mehrere Sessions in einer Datei**: Jede Session einzeln auswerten
