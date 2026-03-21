---
name: zotero
description: |
  Interact with a local Zotero 7+ library via its local HTTP API (localhost:23119).
  Use this skill whenever the user mentions Zotero, wants to search their research library,
  retrieve literature, find papers by topic/author/tag, fetch abstracts or metadata,
  list collections, export citations/BibTeX, or add items to Zotero.
  Trigger phrases include: "suche in Zotero", "welche Papers habe ich zu X",
  "hol mir die Quelle zu X aus Zotero", "exportiere als BibTeX", "Zotero-Bibliothek",
  "füge diesen Artikel zu Zotero hinzu", "meine Literatur zu X", "search my library",
  "find papers about X", "get citation for X", any mention of a DOI or paper title
  combined with reference management context.
  Always use this skill before asking the user to manually look up references.
---

# Zotero Local API Skill

Dieses Skill ermöglicht den Zugriff auf eine laufende Zotero 7-Installation über die lokale HTTP-API.

## Zugriffsmodi

Der Skill unterstützt zwei Modi — **lokal bevorzugt, Web als Fallback**:

| Modus | Basis-URL | Auth | Voraussetzung |
|---|---|---|---|
| **Lokal** (bevorzugt) | `http://localhost:23119/api` | Header `Zotero-Allowed-Request: true` | Zotero läuft, lokale API aktiviert |
| **Web API** (Fallback) | `https://api.zotero.org` | Header `Zotero-API-Key: KEY` | API-Key aus zotero.org/settings/keys |

Beim lokalen Modus ist `userID = 0` der Shortcut für die eigene Bibliothek. Bei der Web API ist die echte numerische User-ID nötig (steht auf zotero.org/settings/keys oben rechts unter "Your User ID").

---

## Workflow: Wie Claude die API nutzt

Claude führt API-Aufrufe mit dem `bash_tool` aus und interpretiert die JSON-Antworten.

### 1. Modus bestimmen (immer zuerst)

```bash
python3 - << 'EOF'
import urllib.request, sys

# Lokale API testen
try:
    req = urllib.request.Request(
        "http://localhost:23119/api/users/0/items?limit=1",
        headers={"Zotero-Allowed-Request": "true"}
    )
    with urllib.request.urlopen(req, timeout=2) as r:
        print("MODE=local")
        sys.exit(0)
except Exception:
    pass

# Web API testen (erfordert ZOTERO_API_KEY und ZOTERO_USER_ID in Env)
import os
key = os.environ.get("ZOTERO_API_KEY", "")
uid = os.environ.get("ZOTERO_USER_ID", "")
if key and uid:
    try:
        req = urllib.request.Request(
            f"https://api.zotero.org/users/{uid}/items?limit=1",
            headers={"Zotero-API-Key": key, "Zotero-API-Version": "3"}
        )
        with urllib.request.urlopen(req, timeout=5) as r:
            print(f"MODE=web UID={uid}")
            sys.exit(0)
    except Exception as e:
        print(f"FEHLER Web API: {e}")
else:
    print("FEHLER: Kein lokales Zotero und keine Web-API-Credentials (ZOTERO_API_KEY / ZOTERO_USER_ID)")
EOF
```

Wenn lokal nicht erreichbar und keine Env-Variablen gesetzt: User fragen, ob er den API-Key zur Hand hat, und ihn für die Session als Variable setzen lassen. **Niemals** API-Keys hardcoden.

### Hilfsfunktion für alle Aufrufe

Statt Modus jedes Mal neu zu prüfen, einmal bestimmen und dann konsistent nutzen:

```bash
# Setzt ZOTERO_BASE, ZOTERO_AUTH_HEADER, ZOTERO_USER
python3 - << 'EOF'
import urllib.request, os, sys

local_ok = False
try:
    req = urllib.request.Request(
        "http://localhost:23119/api/users/0/items?limit=1",
        headers={"Zotero-Allowed-Request": "true"}
    )
    with urllib.request.urlopen(req, timeout=2) as r:
        local_ok = True
except Exception:
    pass

if local_ok:
    print('export ZOTERO_BASE="http://localhost:23119/api"')
    print('export ZOTERO_USER="0"')
    print('export ZOTERO_AUTH_HEADER="Zotero-Allowed-Request: true"')
    print('echo "Modus: lokal"')
else:
    key = os.environ.get("ZOTERO_API_KEY","")
    uid = os.environ.get("ZOTERO_USER_ID","")
    if key and uid:
        print(f'export ZOTERO_BASE="https://api.zotero.org"')
        print(f'export ZOTERO_USER="{uid}"')
        print(f'export ZOTERO_AUTH_HEADER="Zotero-API-Key: {key}"')
        print('echo "Modus: Web API"')
    else:
        print('echo "FEHLER: Zotero nicht erreichbar"')
        sys.exit(1)
EOF
```

Danach in allen curl-Aufrufen `$ZOTERO_BASE`, `$ZOTERO_USER`, `$ZOTERO_AUTH_HEADER` verwenden.

---

## Kernoperationen

> Immer zuerst Modus bestimmen (s.o.) und `$ZOTERO_BASE`, `$ZOTERO_USER`, `$ZOTERO_AUTH_HEADER` exportieren.

### Suche (Volltext & Metadaten)

```bash
curl -s -H "$ZOTERO_AUTH_HEADER" \
  "$ZOTERO_BASE/users/$ZOTERO_USER/items?q=SUCHBEGRIFF&limit=20&format=json" \
  | python3 -c "
import sys, json
items = json.load(sys.stdin)
for it in items:
    d = it.get('data', {})
    if d.get('itemType') == 'attachment': continue
    creators = ', '.join(
        c.get('lastName', c.get('name','?'))
        for c in d.get('creators', [])[:2]
    )
    year = (d.get('date') or '')[:4]
    print(f\"[{d.get('itemType','?')}] {d.get('title','(kein Titel)')} — {creators} ({year})\")
    print(f\"  Key: {d.get('key')}  DOI: {d.get('DOI','-')}\")
    print()
"
```

Suchparameter:
- `q=TEXT` — Volltextsuche (Titel, Autor, Abstract)
- `qmode=titleCreatorYear` — nur in Titel/Autor/Jahr suchen
- `tag=TAGNAME` — nach Tag filtern (kombinierbar mit `q`)
- `itemType=journalArticle` — nach Typ filtern: `journalArticle`, `book`, `bookSection`, `report`, `thesis`, `conferencePaper`, `webpage`
- `sort=dateAdded|dateModified|title|creator|date`
- `limit=N` — max. 100

### Einzelnes Item abrufen (inkl. Abstract)

```bash
curl -s -H "$ZOTERO_AUTH_HEADER" \
  "$ZOTERO_BASE/users/$ZOTERO_USER/items/ITEMKEY?format=json" \
  | python3 -c "
import sys, json
it = json.load(sys.stdin)
d = it.get('data', it)
print('Titel:   ', d.get('title'))
print('Autoren: ', ', '.join(c.get('lastName','?') for c in d.get('creators',[])))
print('Jahr:    ', (d.get('date') or '')[:4])
print('Journal: ', d.get('publicationTitle', d.get('bookTitle','-')))
print('DOI:     ', d.get('DOI','-'))
print('URL:     ', d.get('url','-'))
print('Abstract:', (d.get('abstractNote') or '(kein Abstract)')[:600])
"
```

### Kollektionen auflisten

```bash
curl -s -H "$ZOTERO_AUTH_HEADER" \
  "$ZOTERO_BASE/users/$ZOTERO_USER/collections?format=json" \
  | python3 -c "
import sys, json
colls = json.load(sys.stdin)
for c in sorted(colls, key=lambda x: x['data'].get('name','')):
    d = c['data']
    n = c.get('meta',{}).get('numItems','?')
    parent = d.get('parentCollection', '')
    indent = '  ' if parent else ''
    print(f\"{indent}{d['name']} (key: {d['key']}, {n} Items)\")
"
```

### Items einer Kollektion abrufen

```bash
curl -s -H "$ZOTERO_AUTH_HEADER" \
  "$ZOTERO_BASE/users/$ZOTERO_USER/collections/COLLECTIONKEY/items/top?format=json&limit=100" \
  | python3 -c "
import sys, json
items = json.load(sys.stdin)
for it in items:
    d = it.get('data', {})
    creators = ', '.join(c.get('lastName','?') for c in d.get('creators',[])[:3])
    year = (d.get('date') or '')[:4]
    print(f\"- {d.get('title','?')} ({creators}, {year})  [Key: {d.get('key')}]\")
"
```

### BibTeX-Export

```bash
# Einzelnes Item
curl -s -H "$ZOTERO_AUTH_HEADER" \
  "$ZOTERO_BASE/users/$ZOTERO_USER/items/ITEMKEY?format=bibtex"

# Gesamte Kollektion
curl -s -H "$ZOTERO_AUTH_HEADER" \
  "$ZOTERO_BASE/users/$ZOTERO_USER/collections/COLLECTIONKEY/items?format=bibtex"

# Suchergebnis als BibTeX
curl -s -H "$ZOTERO_AUTH_HEADER" \
  "$ZOTERO_BASE/users/$ZOTERO_USER/items?q=SUCHBEGRIFF&format=bibtex&limit=20"
```

### Formatierte Zitation abrufen

```bash
# style = CSL-Bezeichner
curl -s -H "$ZOTERO_AUTH_HEADER" \
  "$ZOTERO_BASE/users/$ZOTERO_USER/items/ITEMKEY?format=json&include=bib&style=apa" \
  | python3 -c "
import sys, json
it = json.load(sys.stdin)
print(it.get('bib', '(keine Zitation)'))"
```

Häufige CSL-Styles: `apa`, `chicago-author-date`, `harvard-cite-them-right`, `ieee`, `din-1505-2`, `din-1505-2-alphanumeric`

### Neues Item anlegen

```bash
curl -s -X POST \
  -H "$ZOTERO_AUTH_HEADER" \
  -H "Content-Type: application/json" \
  "$ZOTERO_BASE/users/$ZOTERO_USER/items" \
  -d '[{
    "itemType": "journalArticle",
    "title": "TITEL",
    "creators": [{"creatorType": "author", "firstName": "VORNAME", "lastName": "NACHNAME"}],
    "date": "JAHR",
    "DOI": "DOI",
    "publicationTitle": "ZEITSCHRIFT",
    "abstractNote": "ABSTRACT"
  }]' | python3 -c "
import sys, json
r = json.load(sys.stdin)
success = r.get('success', {})
failed = r.get('failed', {})
if success:
    for k, v in success.items():
        print(f'Angelegt: Key={v}')
if failed:
    print('Fehler:', json.dumps(failed, indent=2))
"
```

Itemtypen: `journalArticle`, `book`, `bookSection`, `thesis`, `report`, `conferencePaper`, `webpage`, `preprint`

### Item-Metadaten aktualisieren (PATCH)

```bash
curl -s -X PATCH \
  -H "$ZOTERO_AUTH_HEADER" \
  -H "Content-Type: application/json" \
  -H "If-Unmodified-Since-Version: VERSION" \
  "$ZOTERO_BASE/users/$ZOTERO_USER/items/ITEMKEY" \
  -d '{"tags": [{"tag": "NEUER-TAG"}]}'
```

Version des Items vorher abrufen: aus `it['version']` im JSON-Abruf.

### Annotationen aus PDF-Attachments

```bash
# 1. Attachments eines Items finden
curl -s -H "$ZOTERO_AUTH_HEADER" \
  "$ZOTERO_BASE/users/$ZOTERO_USER/items/ITEMKEY/children?format=json" \
  | python3 -c "
import sys, json
for c in json.load(sys.stdin):
    d = c.get('data',{})
    if d.get('itemType') == 'attachment':
        print(f\"Attachment: {d.get('title')} (key: {d.get('key')}, type: {d.get('contentType')})\")
"

# 2. Annotationen des Attachments
curl -s -H "$ZOTERO_AUTH_HEADER" \
  "$ZOTERO_BASE/users/$ZOTERO_USER/items/ATTACHMENTKEY/children?format=json" \
  | python3 -c "
import sys, json
for a in json.load(sys.stdin):
    d = a.get('data',{})
    if d.get('itemType') == 'annotation':
        print(f\"[{d.get('annotationType','?').upper()}] S. {d.get('pageLabel','?')}\")
        if d.get('annotationText'): print(f\"  Markiert: {d['annotationText']}\")
        if d.get('annotationComment'): print(f\"  Kommentar: {d['annotationComment']}\")
        print()
"
```

---

## Ausgabekonventionen

- Bei Suchergebnissen: kompakte Liste (Titel, Autoren, Jahr, Key, DOI)
- Bei Einzelabruf: vollständige Metadaten inkl. Abstract
- Bei BibTeX: rohen BibTeX-Block ausgeben, ready-to-use
- Bei Zitationen: formatierter String, bereit zum Einfügen
- Keys immer mitausgeben, damit der User sie für Folgeabfragen nutzen kann
- Bei mehr als 10 Treffern: Top-10 zeigen und Möglichkeit zur Verfeinerung anbieten

## Fehlerbehandlung

| Fehlerbild | Ursache | Empfehlung |
|---|---|---|
| Connection refused | Zotero läuft nicht | Zotero starten |
| "Request not allowed" | Header fehlt | `Zotero-Allowed-Request: true` setzen |
| 404 / "No endpoint found" | Falscher URL-Pfad | `users/0` statt nur `items` prüfen |
| Leeres Array `[]` | Keine Treffer | Suchbegriff anpassen, ggf. Kollektion prüfen |
| 403 | API-Key-Problem (Web API) | Lokale API braucht keinen Key |

---

## Referenz: Nützliche Endpunkte

```
# Persönliche Bibliothek
GET  /users/0/items                        Alle Items (lokal: 0, Web: echte UID)
GET  /users/0/items/top                    Nur Top-Level (keine Attachments)
GET  /users/0/items?q=TEXT                 Volltextsuche
GET  /users/0/items?tag=TAG                Nach Tag filtern
GET  /users/0/items/KEY                    Einzelnes Item
GET  /users/0/items/KEY/children           Attachments & Annotationen
GET  /users/0/collections                  Alle Kollektionen
GET  /users/0/collections/KEY/items/top    Items einer Kollektion
GET  /users/0/tags                         Alle Tags
POST /users/0/items                        Neues Item anlegen
PATCH /users/0/items/KEY                   Metadaten aktualisieren

# Gruppenlibraries
GET  /groups/GROUPID/items                 Items einer Gruppe
```

Formate: `?format=json` (default) | `?format=bibtex` | `?format=ris` | `?format=atom`

Web API: User-ID unter https://www.zotero.org/settings/keys (oben rechts "Your User ID")
