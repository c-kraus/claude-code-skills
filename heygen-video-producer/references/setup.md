# HeyGen MCP Server – Einrichtung (einmalig)

## Voraussetzungen

- **uv** installiert: `brew install uv` (macOS) oder [docs.astral.sh/uv](https://docs.astral.sh/uv/)
- Aktiver HeyGen-Account mit API-Zugang

## 1. API-Key beschaffen

1. HeyGen-Dashboard → **Settings → API**
2. API-Key kopieren

## 2. MCP-Server in Claude Code konfigurieren

Datei: `~/.claude/claude.json`

```json
{
  "mcpServers": {
    "HeyGen": {
      "command": "uvx",
      "args": ["heygen-mcp"],
      "env": {
        "HEYGEN_API_KEY": "dein-api-key-hier"
      }
    }
  }
}
```

Den Key direkt eintragen oder über eine Shell-Variable referenzieren:

```json
"HEYGEN_API_KEY": "${HEYGEN_API_KEY}"
```

(Dann muss `HEYGEN_API_KEY` in der Shell-Umgebung gesetzt sein, z. B. in `~/.zshenv`.)

## 3. Installation prüfen

Claude Code neu starten, dann:

```
/mcp
```

→ `HeyGen` sollte als verbundener Server erscheinen.

Funktionstest:

```
Wie viele HeyGen-Credits habe ich noch?
```

Claude ruft dann `mcp__HeyGen__get_remaining_credits` auf und gibt den Kontostand aus.

## Avatar-ID und Voice-ID ermitteln (optional)

Falls du andere Avatare oder Stimmen nutzen willst:

```
Zeig mir alle verfügbaren HeyGen-Avatargruppen.
```

→ `mcp__HeyGen__get_avatar_groups` mit `include_public: true`

```
Zeig mir alle verfügbaren Stimmen.
```

→ `mcp__HeyGen__get_voices`

Die IDs aus den Ergebnissen kannst du dann beim Aufruf des Skills überschreiben.

## Standardwerte des Skills

| Parameter | Wert |
|---|---|
| `avatar_id` | `1b929830392742439cfcd67fe7f7a79c` |
| `voice_id` | `578c2318ebde4d989005f2e439d2c2be` |

Diese Werte sind im Skill hardcoded und müssen nicht konfiguriert werden.
