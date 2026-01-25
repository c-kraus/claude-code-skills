# MARP Syntax Guide für THWS (Prof. Kraus)

Dies ist die verbindliche Syntax-Referenz.

## 1. Global Header
Jede Datei muss mit diesem Block beginnen:

---
marp: true
theme: thws
paginate: true
header: '**Modul Name** <br> Prof. Dr. Christian Kraus'
math: mathjax
---

## 2. Slide Classes (Design)
Nutze diese Klassen, indem du `` unter den Trenner `---` schreibst.

| Klasse | Syntax | Beschreibung |
| :--- | :--- | :--- |
| **Titlepage** | `<!-- _class: titlepage -->` | Nur für die allererste Folie. Petrol Hintergrund. |
| **Structural** | `<!-- _class: structural -->` | Für Agenda, Lernziele, Kapitel-Trenner & Interaktionen. Petrol Hintergrund. |
| **Img Right** | `<!-- _class: img-right -->` | Standard für Content. Links Text, rechts Bild. |
| **Img Right (Small)** | `<!-- _class: img-right small-text -->` | Wie oben, aber kleinere Schrift für mehr Text. |
| **Fullscreen** | `    <!-- _class: fullscreen -->` | Vollbild-Foto mit Caption. |
| **Center** | `<!-- _class: center -->` | Zentrierter Text (für Zitate/Thesen). |
| **End** | `<!-- _class: end -->` | Inhalt am unteren Rand. |

## 3. Umgang mit Bildern
Bei der Klasse `img-right` muss das Bild im Markdown *nach* dem Text stehen.
Format: `![Beschreibung](URL)`
Nutze Unsplash Source URLs: `https://source.unsplash.com/featured/?begriff`

## 4. Typografie
- Nutze `# Headline` damit Überschriften automatisch skalieren.
- Zitate: `> Zitattext`
- Formeln: `$$a = b + c$$`