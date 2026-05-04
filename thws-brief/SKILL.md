---
name: thws-brief
description: >
  Erstellt THWS-Briefe im Corporate-Design als PDF mit der brief-typst Quarto-Extension.
  Verwende diesen Skill immer wenn der User einen Brief schreiben, verfassen, erstellen oder
  umwandeln möchte – egal ob er einen Empfänger nennt, einen Entwurf beschreibt, eine
  Markdown-Datei hat oder einfach sagt "schreib mir einen Brief an...". Auch bei Anfragen
  wie "kannst du das als Brief aufsetzen", "formuliere ein Anschreiben" oder "ich brauche
  ein Schreiben an X" soll dieser Skill aktiv werden.
---

# THWS-Brief Skill

Dieser Skill erstellt offizielle Briefe von Prof. Dr. Christian Kraus (THWS) im
Corporate-Design. Das Ergebnis ist eine `.qmd`-Datei plus ein fertig gerendertes PDF.

## Verzeichnisse

- **Briefe-Ordner**: `/Users/christiankraus/Library/Mobile Documents/com~apple~CloudDocs/01_THWS/04_Administrative_Dokumente/`
- **PDF-Archiv**: Unterordner `pdf_archiv/` im Briefe-Ordner
- **Quarto-Extension**: `_extensions/brief/` (bereits vorhanden, nie anfassen)

Das `quarto render` muss **immer aus dem Briefe-Ordner heraus** ausgeführt werden, damit
die Extension gefunden wird.

## Schritt 1: Informationen sammeln

Ermittle folgende Angaben — frag nach, was fehlt, aber halte die Rückfragen knapp:

| Feld | Erklärung | Fallback |
|------|-----------|---------|
| **Empfänger** | Name, Org, Adresse | Pflicht |
| **Intern/Extern** | Intern = "im Hause", kein Straße/PLZ | fragen |
| **Betreff** | Kurzer Betreff | aus Inhalt ableiten |
| **Sprache** | "de" oder "en" | aus Empfänger/Inhalt ableiten |
| **Anrede** | z.B. "Sehr geehrte Frau Dr. Müller," | aus Kontext generieren |
| **Inhalt** | Brieftext | Pflicht |
| **Datum** | Spezifisches Datum oder "today" | "today" |

**Wenn eine MD-Datei gegeben ist**: Extrahiere Empfänger, Betreff und Inhalt aus der Datei.
Fehlende Felder nachfragen oder intelligent ergänzen.

**Wenn nur eine grobe Beschreibung gegeben ist**: Formuliere einen professionellen Brieftext
passend zum akademischen Kontext (THWS-Professor). Stil: sachlich, höflich, klar.

## Schritt 2: QMD-Datei erstellen

**Dateiname**: `YYYY-MM-DD_EmpfaengerNachname_Betreff-Slug.qmd`
(Beispiel: `2026-04-11_Mueller_Pruefungsanmeldung.qmd`)

Speichere die Datei direkt im Briefe-Ordner.

### YAML-Template

```yaml
---
recipient-org: "[Organisation oder leer lassen]"
recipient-name: "[Vollständiger Name]"
recipient-street: "[Straße oder leer für interne Briefe]"
recipient-zip-city: "[PLZ Ort oder leer]"
recipient-country: "[Land ODER **im Hause** für interne Briefe]"

lang: "[de|en]"

location: "Schweinfurt"
date: "today"
subject: "[Betreff]"
salutation: "[Anrede mit Komma, z.B. Sehr geehrte Frau Dr. Müller,]"

format:
  brief-typst
---

[Brieftext in normalem Markdown, Absätze durch Leerzeilen getrennt]
```

### Wichtige Regeln für das YAML

- `recipient-country: "**im Hause**"` für interne THWS-Briefe (fett im PDF)
- Leere Felder als `""` schreiben, nicht weglassen
- `date: "today"` generiert automatisch das aktuelle Datum
- Für spezifische Daten: `date: "2026-03-15"` (ISO-Format)
- Kein `title:` im YAML — das Template braucht es nicht
- `lang: "de"` → Betreff-Präfix "Betr.:", Grußformel "Mit freundlichen Grüßen"
- `lang: "en"` → Betreff-Präfix "Re:", Grußformel "Best Regards"

### Brieftext-Hinweise

- Kein Markdown-Heading (`#`) im Body — die Anrede kommt aus dem YAML
- Absätze einfach durch Leerzeilen trennen
- Listen und **Fettschrift** sind möglich
- Die Grußformel ("Mit freundlichen Grüßen" / "Best Regards") wird automatisch ergänzt
- Die Unterschriftenzeile ("Prof. Dr. Christian Kraus") wird automatisch ergänzt

## Schritt 3: Rendern

```bash
cd "/Users/christiankraus/Library/Mobile Documents/com~apple~CloudDocs/01_THWS/04_Administrative_Dokumente" && quarto render DATEINAME.qmd
```

Prüfe ob das Rendering erfolgreich war (Exit-Code 0, PDF vorhanden).

## Schritt 4: PDF ins Archiv verschieben

Das PDF landet zunächst neben der QMD-Datei. Verschiebe es ins `pdf_archiv/`:

```bash
mv "/Users/christiankraus/Library/Mobile Documents/com~apple~CloudDocs/01_THWS/04_Administrative_Dokumente/DATEINAME.pdf" \
   "/Users/christiankraus/Library/Mobile Documents/com~apple~CloudDocs/01_THWS/04_Administrative_Dokumente/pdf_archiv/DATEINAME.pdf"
```

## Schritt 5: Symlink anbieten

Frage den User nach dem Verschieben kurz:

> "Das PDF liegt jetzt im Archiv unter `pdf_archiv/DATEINAME.pdf`. Soll ich in einem
> anderen Ordner (z.B. einem projektspezifischen Ordner) noch einen Symlink darauf anlegen?"

Wenn ja: `ln -s [absoluter Pfad zum PDF] [Zielordner/DATEINAME.pdf]`

## Häufige Empfänger-Muster

| Situation | recipient-country |
|-----------|------------------|
| THWS-Kollege | `"**im Hause**"` |
| Deutsches Unternehmen | `"Deutschland"` oder leer |
| Internationaler Empfänger | Landesname auf Englisch |
| Behörde ohne Ausland | `""` |

## Qualitätsprüfung vor dem Rendern

Bevor du `quarto render` ausführst, prüfe kurz:
- Sind alle Pflichtfelder gesetzt (recipient-name, subject, salutation)?
- Ist `format: brief-typst` korrekt eingerückt (2 Spaces)?
- Enthält der Brieftext mindestens einen Absatz?
- Ist das Datum-Format korrekt (ISO oder "today")?
