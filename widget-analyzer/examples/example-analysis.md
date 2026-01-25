# Beispiel Widget-Analyse: Kapitel "Buchführung und Jahresabschluss"

## Zusammenfassung
- Kapitel: "Buchführung und Jahresabschluss" (Kapitel 3)
- Analysierte Abschnitte: 5
- Identifizierte Widget-Potenziale: 4
- Empfohlene Umsetzungen: 2 (High Priority)

## Widget-Vorschläge

### Widget Proposal 1: Buchungssatz-Generator

**Location:** Abschnitt 3.2 "Vom Geschäftsvorfall zum Buchungssatz"
**Category:** Prozesse/Abläufe
**Priority:** High

**Didactic Rationale:**
Die Transformation eines Geschäftsvorfalls in einen Buchungssatz folgt einem klaren, aber für Anfänger oft abstrakten Prozess. Ein interaktives Widget, das diesen Prozess Schritt für Schritt visualisiert, hilft Studierenden, die Logik der doppelten Buchführung zu verstehen und den Zusammenhang zwischen realwirtschaftlichen Vorgängen und ihrer buchhalterischen Abbildung zu verinnerlichen.

**Widget Description:**
Ein mehrstufiges Widget, das einen beispielhaften Geschäftsvorfall (z.B. "Kauf von Büromaterial auf Ziel für 500 €") durch alle Analyseschritte führt:
1. Identifikation der betroffenen Bilanzpositionen
2. Bestimmung von Soll und Haben
3. Konstruktion des fertigen Buchungssatzes
4. Auswirkung auf die Bilanz

Jeder Schritt wird visuell hervorgehoben, mit Erklärungen versehen und kann vom Nutzer in eigenem Tempo durchlaufen werden.

**Technical Specifications:**
- Widget Type: Step-by-step Animation mit Navigation
- Data/Parameters: 3-4 vordefinierte Geschäftsvorfälle zur Auswahl
- Interactivity: 
  - Vor/Zurück-Buttons zwischen Schritten
  - Dropdown zur Auswahl verschiedener Geschäftsvorfälle
  - Highlighting der aktuellen Analyseebene
  - "Lösung anzeigen" Button für Selbstkontrolle
- Visual Elements:
  - Animierte Bilanz (T-Konten)
  - Farbcodierung: Aktiva (blau), Passiva (grün), Aufwand (rot), Ertrag (grün)
  - Pfeile zeigen Buchungsbewegungen
- THWS Branding: 
  - THWS Farbschema (#003366, #00A3E0)
  - Logo subtil in Ecke

**Integration Details:**
- File name: `widgets/kapitel-03/widget-buchungssatz-generator.html`
- Placement: Nach dem erklärenden Absatz zu "Analyseschritten", vor den Übungsaufgaben
- Context text: "Das folgende interaktive Widget führt Sie Schritt für Schritt durch die Erstellung eines Buchungssatzes. Wählen Sie einen Geschäftsvorfall und klicken Sie sich durch die einzelnen Analysephasen:"

**iframe Code:**
```html
<iframe src="widgets/kapitel-03/widget-buchungssatz-generator.html" 
        width="100%" 
        height="600px" 
        frameborder="0"
        title="Interaktiver Buchungssatz-Generator">
</iframe>
```

**Fallback Content:**
Für die PDF-Version: Vier statische Diagramme, die die Schritte für einen exemplarischen Geschäftsvorfall zeigen.

---

### Widget Proposal 2: Bilanz-Zusammenhang Explorer

**Location:** Abschnitt 3.4 "Bilanzgleichung und ihre Dynamik"
**Category:** Zusammenhänge/Abhängigkeiten
**Priority:** High

**Didactic Rationale:**
Die fundamentale Bilanzgleichung (Aktiva = Passiva) und wie einzelne Geschäftsvorfälle diese Balance beeinflussen, ist ein zentrales aber oft schwer greifbares Konzept. Ein interaktives Widget, das die simultanen Auswirkungen auf beide Bilanzseiten visualisiert, macht diese Abhängigkeiten konkret erfahrbar.

**Widget Description:**
Eine vereinfachte, interaktive Bilanz mit 4-6 Hauptpositionen je Seite. Nutzer können verschiedene Geschäftsvorfälle auslösen (z.B. "Warenverkauf", "Kreditaufnahme", "Investition") und sehen in Echtzeit, wie sich beide Seiten der Bilanz verändern, um das Gleichgewicht zu wahren.

**Technical Specifications:**
- Widget Type: Interactive Balance Sheet mit Live-Updates
- Data/Parameters: 
  - 8-10 vordefinierte Geschäftsvorfälle
  - Anfangsbilanzdaten
- Interactivity:
  - Button/Dropdown zur Auswahl von Geschäftsvorfällen
  - Animierte Balkenveränderungen
  - Gleichgewichts-Indikator (zeigt Balance)
  - Hover über Positionen für Details
  - "Reset" Button zur Ausgangsposition
- Visual Elements:
  - Zwei Balkendiagramme (Aktiva links, Passiva rechts)
  - Verbindungslinien zeigen betroffene Positionen
  - Zahlenwerte ändern sich animiert
  - Gleichgewichts-Symbol in der Mitte
- THWS Branding: THWS-Farbpalette, dezentes Logo

**Integration Details:**
- File name: `widgets/kapitel-03/widget-bilanz-zusammenhang.html`
- Placement: Direkt nach der Einführung der Bilanzgleichung
- Context text: "Erkunden Sie, wie verschiedene Geschäftsvorfälle die Bilanz beeinflussen. Das Widget zeigt Ihnen, wie jede Transaktion das Gleichgewicht zwischen Aktiva und Passiva wahrt:"

**iframe Code:**
```html
<iframe src="widgets/kapitel-03/widget-bilanz-zusammenhang.html" 
        width="100%" 
        height="500px" 
        frameborder="0"
        title="Bilanz-Zusammenhang Explorer">
</iframe>
```

**Fallback Content:**
Statisches Diagramm mit drei Beispieltransaktionen und deren Bilanzauswirkungen.

---

### Widget Proposal 3: Abschreibungs-Rechner

**Location:** Abschnitt 3.6 "Abschreibungsmethoden"
**Category:** Parametervariationen
**Priority:** Medium

**Didactic Rationale:**
Die unterschiedlichen Abschreibungsmethoden (linear vs. degressiv) führen zu verschiedenen Jahreswerten. Ein Vergleichs-Widget macht die mathematischen Unterschiede und ihre praktischen Konsequenzen sichtbar und ermöglicht das Experimentieren mit verschiedenen Parametern.

**Widget Description:**
Interaktiver Rechner, bei dem Nutzer Anschaffungskosten, Nutzungsdauer und Abschreibungsmethode wählen können. Das Widget zeigt parallel zwei Diagramme: lineare und degressive Abschreibung, jeweils mit Jahreswerten und Restwert-Kurven.

**Technical Specifications:**
- Widget Type: Parameter-Slider + Vergleichs-Charts
- Data/Parameters:
  - Input: Anschaffungskosten (Slider: 10.000-500.000 €)
  - Input: Nutzungsdauer (Slider: 3-20 Jahre)
  - Input: Degressiver Satz (Dropdown: 20%, 25%, 30%)
- Interactivity:
  - Live-Update bei Parameteränderung
  - Tooltip zeigt Jahreswerte beim Hover
  - Toggle zwischen Tabellen- und Grafikansicht
- Visual Elements:
  - Zwei Line-Charts (linear/degressiv)
  - Tabelle mit Jahreswerten
  - Farbcodierung zur Unterscheidung
- THWS Branding: THWS-Farben, Logo

**Integration Details:**
- File name: `widgets/kapitel-03/widget-abschreibung-rechner.html`
- Placement: Nach der theoretischen Erklärung der Methoden, vor Rechenbeispielen
- Context text: "Experimentieren Sie mit verschiedenen Parametern und vergleichen Sie die Auswirkungen der linearen und degressiven Abschreibung:"

**iframe Code:**
```html
<iframe src="widgets/kapitel-03/widget-abschreibung-rechner.html" 
        width="100%" 
        height="550px" 
        frameborder="0"
        title="Abschreibungs-Rechner">
</iframe>
```

**Fallback Content:**
Vergleichstabelle mit Beispielrechnung für ein konkretes Szenario.

---

### Widget Proposal 4: GuV-Struktur Navigator

**Location:** Abschnitt 3.7 "Gewinn- und Verlustrechnung"
**Category:** Zusammenhänge/Abhängigkeiten
**Priority:** Low

**Didactic Rationale:**
Die Struktur der GuV mit ihren verschiedenen Ergebnisstufen (Betriebsergebnis, EBIT, EBT, Jahresüberschuss) ist hierarchisch aufgebaut. Ein interaktives Widget könnte diese Struktur explorierbar machen, wird aber als weniger kritisch eingeschätzt, da die hierarchische Darstellung auch gut textuell/tabellarisch funktioniert.

**Widget Description:**
Interaktive Baumstruktur der GuV, bei der Nutzer einzelne Positionen aufklappen können, um Unterpositionen zu sehen. Jede Ebene zeigt die Berechnung der jeweiligen Ergebnisstufe.

**Technical Specifications:**
- Widget Type: Collapsible Tree Diagram
- Data/Parameters: Beispiel-GuV-Daten
- Interactivity: Click to expand/collapse, Hover for definitions
- Visual Elements: Tree structure, connecting lines, value boxes
- THWS Branding: THWS-Farben

**Integration Details:**
- File name: `widgets/kapitel-03/widget-guv-navigator.html`
- Placement: Bei Einführung der GuV-Struktur
- Context text: "Die folgende interaktive Darstellung zeigt den Aufbau der GuV. Klicken Sie auf einzelne Positionen, um Details zu sehen:"

**iframe Code:**
```html
<iframe src="widgets/kapitel-03/widget-guv-navigator.html" 
        width="100%" 
        height="450px" 
        frameborder="0"
        title="GuV-Struktur Navigator">
</iframe>
```

**Fallback Content:**
Klassische hierarchische Darstellung als Textgliederung mit Einrückungen.

## Implementierungs-Roadmap

### Phase 1: Sofortige Umsetzung (High Priority)
1. **Buchungssatz-Generator** - Höchster didaktischer Mehrwert, zentral für Verständnis
2. **Bilanz-Zusammenhang Explorer** - Fundamentales Konzept, schwer textuell zu vermitteln

### Phase 2: Ergänzende Widgets (Medium Priority)
3. **Abschreibungs-Rechner** - Nützlich für Parameterverständnis, weniger kritisch

### Phase 3: Optional (Low Priority)
4. **GuV-Struktur Navigator** - Nice-to-have, aber gut durch statische Darstellung ersetzbar

## Technische Hinweise

- Alle Widgets sollten responsive sein (funktionieren auf Tablet/Desktop)
- JavaScript sollte vanilla JS sein (keine Framework-Dependencies für einfachere Wartung)
- Farbpalette einheitlich nutzen: THWS-Blau (#003366) für Primärelemente, Hellblau (#00A3E0) für Akzente
- Accessibility: Alle interaktiven Elemente brauchen keyboard navigation
- Performance: Widgets sollten auch auf älteren Rechnern flüssig laufen (Zielgruppe: Studenten-Laptops)
- Browser-Kompatibilität: Chrome, Firefox, Safari (keine IE-Unterstützung nötig)
