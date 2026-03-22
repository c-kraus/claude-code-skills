---
name: zotero-skill
description: |
  Interact with a local Zotero 7+ library via its local HTTP API (localhost:23119) and the Zotero Web API (api.zotero.org).
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

# Zotero API Skill

Access a running Zotero 7 installation via its local HTTP API and the Zotero Web API.

## Critical: API Key Security

**NEVER hardcode API keys or user IDs in code, files, or git repositories.**

- Store credentials exclusively as environment variables: `ZOTERO_API_KEY` and `ZOTERO_USER_ID`
- If the user provides credentials inline during a session, set them as shell variables for the session only — do not write them to any file
- Before committing anything, verify no API keys leaked into tracked files

## Architecture: Read Local, Write via Web API

The local Zotero API (`localhost:23119/api`) is **read-only** — all write operations (POST, PATCH, DELETE) return 400 or 501. The Zotero Web API (`api.zotero.org`) supports full CRUD. The Zotero Connector API (`localhost:23119/connector/`) supports item creation as a special case.

| Operation | Use | API |
|---|---|---|
| Search, read items | Local API | `localhost:23119/api` |
| List collections | Local API | `localhost:23119/api` |
| Export BibTeX | Local API | `localhost:23119/api` |
| Read annotations | Local API | `localhost:23119/api` |
| **Create items** | Connector API | `localhost:23119/connector/saveItems` |
| **Add items to collections** | Web API | `api.zotero.org` PATCH |
| **Update metadata** | Web API | `api.zotero.org` PATCH |
| **Delete items** | Web API | `api.zotero.org` DELETE |
| **Create collections** | Web API | `api.zotero.org` POST |

### Decision flow

1. For **read operations**: use local API (fast, no auth needed beyond the header)
2. For **write operations**: check if `ZOTERO_API_KEY` and `ZOTERO_USER_ID` are set
   - If yes → use Web API directly
   - If no → ask user for credentials (from zotero.org/settings/keys)
3. Exception: **creating items** can use the Connector API locally (see below)

---

## Setup: Determine Mode

```bash
python3 - << 'EOF'
import urllib.request, os, sys, json

# 1. Test local API (for reads)
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

# 2. Test Web API (needed for writes)
key = os.environ.get("ZOTERO_API_KEY", "")
uid = os.environ.get("ZOTERO_USER_ID", "")
web_ok = False
if key and uid:
    try:
        req = urllib.request.Request(
            f"https://api.zotero.org/users/{uid}/items?limit=1",
            headers={"Zotero-API-Key": key, "Zotero-API-Version": "3"}
        )
        with urllib.request.urlopen(req, timeout=5) as r:
            web_ok = True
    except Exception:
        pass

if local_ok:
    print("LOCAL: OK (reads)")
else:
    print("LOCAL: not available")

if web_ok:
    print(f"WEB:   OK (reads + writes, UID={uid})")
else:
    print("WEB:   not available — set ZOTERO_API_KEY and ZOTERO_USER_ID for write operations")
EOF
```

If the user needs write operations and Web API credentials aren't set, ask them to:
1. Go to https://www.zotero.org/settings/keys
2. Note their **User ID** (top right)
3. Create a new API key with library read/write access
4. Set: `export ZOTERO_API_KEY="..." ZOTERO_USER_ID="..."`

---

## Read Operations (Local API)

All read operations use the local API with header `Zotero-Allowed-Request: true` and `userID = 0`.

### Search (fulltext & metadata)

```bash
python3 -c "
import urllib.request, json
req = urllib.request.Request(
    'http://localhost:23119/api/users/0/items?q=SUCHBEGRIFF&limit=20&format=json',
    headers={'Zotero-Allowed-Request': 'true'}
)
with urllib.request.urlopen(req, timeout=10) as r:
    items = json.load(r)
for it in items:
    d = it.get('data', {})
    if d.get('itemType') == 'attachment': continue
    creators = ', '.join(c.get('lastName', c.get('name','?')) for c in d.get('creators', [])[:2])
    year = (d.get('date') or '')[:4]
    print(f\"[{d.get('itemType','?')}] {d.get('title','(no title)')} — {creators} ({year})\")
    print(f\"  Key: {d.get('key')}  DOI: {d.get('DOI','-')}\")
    print()
"
```

Search parameters:
- `q=TEXT` — fulltext search (title, author, abstract)
- `qmode=titleCreatorYear` — search in title/author/year only
- `tag=TAGNAME` — filter by tag (combinable with `q`)
- `itemType=journalArticle` — filter by type: `journalArticle`, `book`, `bookSection`, `report`, `thesis`, `conferencePaper`, `webpage`
- `sort=dateAdded|dateModified|title|creator|date`
- `limit=N` — max 100

### Single item with abstract

```bash
python3 -c "
import urllib.request, json
req = urllib.request.Request(
    'http://localhost:23119/api/users/0/items/ITEMKEY?format=json',
    headers={'Zotero-Allowed-Request': 'true'}
)
with urllib.request.urlopen(req, timeout=10) as r:
    it = json.load(r)
d = it.get('data', it)
print('Title:   ', d.get('title'))
print('Authors: ', ', '.join(c.get('lastName','?') for c in d.get('creators',[])))
print('Year:    ', (d.get('date') or '')[:4])
print('Journal: ', d.get('publicationTitle', d.get('bookTitle','-')))
print('DOI:     ', d.get('DOI','-'))
print('URL:     ', d.get('url','-'))
print('Abstract:', (d.get('abstractNote') or '(no abstract)')[:600])
"
```

### List collections

```bash
python3 -c "
import urllib.request, json
req = urllib.request.Request(
    'http://localhost:23119/api/users/0/collections?format=json',
    headers={'Zotero-Allowed-Request': 'true'}
)
with urllib.request.urlopen(req, timeout=10) as r:
    colls = json.load(r)
for c in sorted(colls, key=lambda x: x['data'].get('name','')):
    d = c['data']
    n = c.get('meta',{}).get('numItems','?')
    parent = d.get('parentCollection', '')
    indent = '  ' if parent else ''
    print(f\"{indent}{d['name']} (key: {d['key']}, {n} Items)\")
"
```

### Items of a collection

```bash
python3 -c "
import urllib.request, json
req = urllib.request.Request(
    'http://localhost:23119/api/users/0/collections/COLLECTIONKEY/items/top?format=json&limit=100',
    headers={'Zotero-Allowed-Request': 'true'}
)
with urllib.request.urlopen(req, timeout=10) as r:
    items = json.load(r)
for it in items:
    d = it.get('data', {})
    creators = ', '.join(c.get('lastName','?') for c in d.get('creators',[])[:3])
    year = (d.get('date') or '')[:4]
    print(f\"- {d.get('title','?')} ({creators}, {year})  [Key: {d.get('key')}]\")
"
```

### BibTeX export

```bash
# Single item
curl -s -H "Zotero-Allowed-Request: true" \
  "http://localhost:23119/api/users/0/items/ITEMKEY?format=bibtex"

# Entire collection
curl -s -H "Zotero-Allowed-Request: true" \
  "http://localhost:23119/api/users/0/collections/COLLECTIONKEY/items?format=bibtex"
```

### Formatted citation

```bash
python3 -c "
import urllib.request, json
req = urllib.request.Request(
    'http://localhost:23119/api/users/0/items/ITEMKEY?format=json&include=bib&style=apa',
    headers={'Zotero-Allowed-Request': 'true'}
)
with urllib.request.urlopen(req, timeout=10) as r:
    it = json.load(r)
print(it.get('bib', '(no citation)'))
"
```

Common CSL styles: `apa`, `chicago-author-date`, `harvard-cite-them-right`, `ieee`, `din-1505-2`

### Annotations from PDF attachments

```bash
python3 -c "
import urllib.request, json

# 1. Find attachments of an item
req = urllib.request.Request(
    'http://localhost:23119/api/users/0/items/ITEMKEY/children?format=json',
    headers={'Zotero-Allowed-Request': 'true'}
)
with urllib.request.urlopen(req, timeout=10) as r:
    children = json.load(r)
for c in children:
    d = c.get('data',{})
    if d.get('itemType') == 'attachment':
        att_key = d.get('key')
        print(f\"Attachment: {d.get('title')} (key: {att_key}, type: {d.get('contentType')})\")

        # 2. Get annotations of this attachment
        req2 = urllib.request.Request(
            f'http://localhost:23119/api/users/0/items/{att_key}/children?format=json',
            headers={'Zotero-Allowed-Request': 'true'}
        )
        with urllib.request.urlopen(req2, timeout=10) as r2:
            annots = json.load(r2)
        for a in annots:
            ad = a.get('data',{})
            if ad.get('itemType') == 'annotation':
                print(f\"  [{ad.get('annotationType','?').upper()}] p. {ad.get('pageLabel','?')}\")
                if ad.get('annotationText'): print(f\"    Highlighted: {ad['annotationText']}\")
                if ad.get('annotationComment'): print(f\"    Comment: {ad['annotationComment']}\")
"
```

---

## Write Operations (Web API)

All write operations require `ZOTERO_API_KEY` and `ZOTERO_USER_ID` environment variables.

### Add items to a collection

This is the most common write operation. PATCH each item to append the collection key to its `collections` array:

```bash
python3 -c "
import urllib.request, json, os

key = os.environ['ZOTERO_API_KEY']
uid = os.environ['ZOTERO_USER_ID']
collection_key = 'COLLECTIONKEY'
item_keys = ['KEY1', 'KEY2', 'KEY3']

for item_key in item_keys:
    # Get current item (need version and existing collections)
    req = urllib.request.Request(
        f'https://api.zotero.org/users/{uid}/items/{item_key}?format=json',
        headers={'Zotero-API-Key': key, 'Zotero-API-Version': '3'}
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        item = json.load(r)
    version = item['version']
    current_colls = item['data'].get('collections', [])

    if collection_key in current_colls:
        print(f'{item_key}: already in collection')
        continue

    # PATCH to add collection
    new_colls = current_colls + [collection_key]
    data = json.dumps({'collections': new_colls}).encode('utf-8')
    req = urllib.request.Request(
        f'https://api.zotero.org/users/{uid}/items/{item_key}',
        data=data,
        headers={
            'Zotero-API-Key': key,
            'Zotero-API-Version': '3',
            'Content-Type': 'application/json',
            'If-Unmodified-Since-Version': str(version)
        },
        method='PATCH'
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        title = item['data'].get('title', '?')[:50]
        print(f'{item_key}: OK — {title}')
"
```

### Create a collection

```bash
python3 -c "
import urllib.request, json, os

key = os.environ['ZOTERO_API_KEY']
uid = os.environ['ZOTERO_USER_ID']

data = json.dumps([{'name': 'COLLECTION NAME'}]).encode('utf-8')
req = urllib.request.Request(
    f'https://api.zotero.org/users/{uid}/collections',
    data=data,
    headers={
        'Zotero-API-Key': key,
        'Zotero-API-Version': '3',
        'Content-Type': 'application/json'
    },
    method='POST'
)
with urllib.request.urlopen(req, timeout=10) as r:
    result = json.load(r)
    for k, v in result.get('success', {}).items():
        print(f'Created: key={v}')
"
```

### Update item metadata

```bash
python3 -c "
import urllib.request, json, os

key = os.environ['ZOTERO_API_KEY']
uid = os.environ['ZOTERO_USER_ID']
item_key = 'ITEMKEY'

# Get current version first
req = urllib.request.Request(
    f'https://api.zotero.org/users/{uid}/items/{item_key}?format=json',
    headers={'Zotero-API-Key': key, 'Zotero-API-Version': '3'}
)
with urllib.request.urlopen(req, timeout=10) as r:
    item = json.load(r)
version = item['version']

# PATCH with changes
data = json.dumps({'tags': [{'tag': 'NEW-TAG'}]}).encode('utf-8')
req = urllib.request.Request(
    f'https://api.zotero.org/users/{uid}/items/{item_key}',
    data=data,
    headers={
        'Zotero-API-Key': key,
        'Zotero-API-Version': '3',
        'Content-Type': 'application/json',
        'If-Unmodified-Since-Version': str(version)
    },
    method='PATCH'
)
with urllib.request.urlopen(req, timeout=10) as r:
    print(f'Updated: {r.status}')
"
```

### Delete items

```bash
python3 -c "
import urllib.request, json, os

key = os.environ['ZOTERO_API_KEY']
uid = os.environ['ZOTERO_USER_ID']
item_key = 'ITEMKEY'

# Get version first
req = urllib.request.Request(
    f'https://api.zotero.org/users/{uid}/items/{item_key}?format=json',
    headers={'Zotero-API-Key': key, 'Zotero-API-Version': '3'}
)
with urllib.request.urlopen(req, timeout=10) as r:
    item = json.load(r)
version = item['version']

# DELETE
req = urllib.request.Request(
    f'https://api.zotero.org/users/{uid}/items/{item_key}',
    headers={
        'Zotero-API-Key': key,
        'Zotero-API-Version': '3',
        'If-Unmodified-Since-Version': str(version)
    },
    method='DELETE'
)
with urllib.request.urlopen(req, timeout=10) as r:
    print(f'Deleted: {r.status}')
"
```

### Create items via Web API

```bash
python3 -c "
import urllib.request, json, os

key = os.environ['ZOTERO_API_KEY']
uid = os.environ['ZOTERO_USER_ID']

items = [{
    'itemType': 'journalArticle',
    'title': 'TITLE',
    'creators': [{'creatorType': 'author', 'firstName': 'FIRST', 'lastName': 'LAST'}],
    'date': 'YEAR',
    'DOI': 'DOI',
    'publicationTitle': 'JOURNAL',
    'collections': ['OPTIONAL_COLLECTION_KEY']
}]

data = json.dumps(items).encode('utf-8')
req = urllib.request.Request(
    f'https://api.zotero.org/users/{uid}/items',
    data=data,
    headers={
        'Zotero-API-Key': key,
        'Zotero-API-Version': '3',
        'Content-Type': 'application/json'
    },
    method='POST'
)
with urllib.request.urlopen(req, timeout=10) as r:
    result = json.load(r)
    for k, v in result.get('success', {}).items():
        print(f'Created: key={v}')
    for k, v in result.get('failed', {}).items():
        print(f'Failed: {json.dumps(v)}')
"
```

Note: when creating via Web API, you can include `collections: ['KEY']` directly in the item data to place it in a collection immediately.

---

## Connector API (Local Item Creation)

When the Web API is not available but Zotero is running locally, items can be created via the Connector API. This endpoint saves items to **the currently selected collection** in the Zotero UI.

### Select a collection first (macOS)

```bash
open "zotero://select/library/collections/COLLECTIONKEY"
sleep 1
```

### Verify selected collection

```bash
python3 -c "
import urllib.request, json
req = urllib.request.Request(
    'http://localhost:23119/connector/getSelectedCollection',
    data=b'{}',
    headers={'Zotero-Allowed-Request': 'true', 'Content-Type': 'application/json'},
    method='POST'
)
with urllib.request.urlopen(req, timeout=5) as r:
    result = json.load(r)
print(f'Selected: id={result.get(\"id\")}, name={result.get(\"name\")}')
print('Available targets:')
for t in result.get('targets', []):
    indent = '  ' * t.get('level', 0)
    print(f'  {indent}{t.get(\"name\")} (id={t.get(\"id\")})')
"
```

### Create items via connector/saveItems

```bash
python3 -c "
import urllib.request, json

item = {
    'itemType': 'journalArticle',
    'title': 'TITLE',
    'creators': [{'firstName': 'FIRST', 'lastName': 'LAST', 'creatorType': 'author'}],
    'date': 'YEAR',
    'DOI': 'DOI',
    'publicationTitle': 'JOURNAL',
    'url': '',
    'tags': []
}

payload = json.dumps({
    'items': [item],
    'uri': 'http://zotero-import'
}).encode('utf-8')

req = urllib.request.Request(
    'http://localhost:23119/connector/saveItems',
    data=payload,
    headers={
        'Zotero-Allowed-Request': 'true',
        'Content-Type': 'application/json'
    },
    method='POST'
)
with urllib.request.urlopen(req, timeout=10) as r:
    print(f'Status: {r.status}')
"
```

Items created this way land in the currently selected collection. After creation, use the Web API to move them to a different collection if needed.

---

## Better BibTeX JSON-RPC

If Better BibTeX is installed, a JSON-RPC endpoint is available at `localhost:23119/better-bibtex/json-rpc`. This is useful for searching by citekey and exporting formatted citations.

### Available methods

| Method | Required params | Description |
|---|---|---|
| `item.search` | `terms` (string) | Search by author/title |
| `item.export` | `citekeys`, `translator` | Export items in various formats |
| `item.bibliography` | `citekeys` | Get formatted bibliography |
| `item.citationkey` | `item_keys` (Zotero keys) | Get BBT citekeys for Zotero keys |
| `item.collections` | `citekeys` | Get collections of items |
| `item.notes` | `citekeys` | Get notes |
| `item.attachments` | `citekey` | Get attachments |
| `autoexport.add` | `collection`, `translator`, `path` | Set up auto-export |
| `user.groups` | — | List libraries |

BBT does **not** have collection management methods. You cannot create, rename, or add items to collections via BBT.

### Example: search by author

```bash
python3 -c "
import urllib.request, json
payload = json.dumps({
    'jsonrpc': '2.0',
    'method': 'item.search',
    'params': ['Bennett'],
    'id': 1
}).encode('utf-8')
req = urllib.request.Request(
    'http://localhost:23119/better-bibtex/json-rpc',
    data=payload,
    headers={'Content-Type': 'application/json', 'Zotero-Allowed-Request': 'true'}
)
with urllib.request.urlopen(req, timeout=5) as r:
    result = json.load(r)
for item in result.get('result', []):
    print(f\"{item.get('citation-key','?')}: {item.get('title','?')}\")
"
```

---

## Output Conventions

- Search results: compact list (title, authors, year, key, DOI)
- Single item: full metadata including abstract
- BibTeX: raw BibTeX block, ready to use
- Citations: formatted string, ready to paste
- Always include item keys so the user can use them in follow-up queries
- For more than 10 results: show top 10 and offer to refine

## Error Handling

| Error | Cause | Fix |
|---|---|---|
| Connection refused | Zotero not running | Start Zotero |
| "Request not allowed" | Header missing | Add `Zotero-Allowed-Request: true` |
| 404 / "No endpoint found" | Wrong URL path | Check `users/0` prefix |
| Empty array `[]` | No results | Adjust search terms |
| 403 | API key issue (Web API) | Check `ZOTERO_API_KEY` |
| 400 "Endpoint does not support method" | Local API write attempt | Switch to Web API |
| 501 Not Implemented | Local API PATCH/DELETE | Switch to Web API |
| UnicodeEncodeError in search | Non-ASCII in URL | URL-encode the query string |

## Known Dead Ends (Don't Waste Time on These)

- **Local API writes**: POST/PATCH/DELETE to `localhost:23119/api/users/0/...` will always fail. Don't retry.
- **AppleScript UI automation**: Requires explicit Accessibility permissions for the terminal app. Won't work out of the box.
- **BBT collection management**: No methods exist for creating or managing collections via Better BibTeX JSON-RPC.
- **connector/import for BibTeX**: The `/connector/import` endpoint is unreliable for BibTeX payloads (returns 400 with varying formats). Use `connector/saveItems` with structured item data instead.

## Quick Reference: Endpoints

```
# Local API (read-only)
GET  /api/users/0/items                        All items
GET  /api/users/0/items/top                    Top-level only
GET  /api/users/0/items?q=TEXT                 Fulltext search
GET  /api/users/0/items?tag=TAG                Filter by tag
GET  /api/users/0/items/KEY                    Single item
GET  /api/users/0/items/KEY/children           Attachments & annotations
GET  /api/users/0/collections                  All collections
GET  /api/users/0/collections/KEY/items/top    Items in a collection
GET  /api/users/0/tags                         All tags

# Connector API (item creation only)
POST /connector/getSelectedCollection          Get selected collection
POST /connector/saveItems                      Create items (into selected collection)

# Better BibTeX (search & export)
POST /better-bibtex/json-rpc                   JSON-RPC (see methods table above)

# Web API (full CRUD — needs ZOTERO_API_KEY)
GET    /users/UID/items/KEY                    Read item
POST   /users/UID/items                        Create items
PATCH  /users/UID/items/KEY                    Update item (needs If-Unmodified-Since-Version)
DELETE /users/UID/items/KEY                    Delete item (needs If-Unmodified-Since-Version)
POST   /users/UID/collections                  Create collection
GET    /users/UID/collections                  List collections

# URL scheme (macOS)
zotero://select/library/collections/KEY        Select collection in Zotero UI
```

Formats: `?format=json` (default) | `?format=bibtex` | `?format=ris` | `?format=atom`

Web API credentials: https://www.zotero.org/settings/keys (User ID top right, create API key with read/write access)
