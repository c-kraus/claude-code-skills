---
name: academic-research
description: |
  Multi-source academic literature search across SSRN, OpenAlex, CrossRef, and Semantic Scholar.
  Orchestrates Jina MCP (for SSRN working papers and web content) and Academix MCP (for published journals,
  citations, and BibTeX) into a unified research workflow. Optimized for IFRS, Finance, Accounting, Ethics,
  and interdisciplinary fields where SSRN pre-prints and published journal articles both matter.
  Use this skill whenever the user wants to find academic papers, search for literature on a topic,
  build a bibliography, do a literature review, find working papers, search SSRN, look up citations,
  or gather sources for a lecture, paper, or seminar.
  Trigger phrases include: "suche Paper zu", "find literature on", "Literaturrecherche",
  "search SSRN for", "find working papers about", "literature review on",
  "welche Studien gibt es zu", "find me papers about", "Quellen zu", "research on",
  "bibliography for", "who has published on", "citation network for",
  any mention of SSRN, OpenAlex, CrossRef, Semantic Scholar, or academic search in general.
  Also trigger when the user provides a research topic and seems to want sources, even if they
  don't explicitly say "search" — e.g., "I need sources on algorithmic fairness" or
  "was gibt es Aktuelles zu IFRS 17".
---

# Academic Research Skill

Orchestrate multi-source academic literature search using two MCP servers: **Jina** (SSRN, web, arXiv) and **Academix** (OpenAlex, CrossRef, Semantic Scholar). The combination covers both pre-publication working papers and published journal articles.

## Critical: API Key Security

**NEVER hardcode API keys in files or git repositories.** All credentials go into environment variables only.

## MCP Server Requirements

This skill requires two MCP servers. Check availability before starting:

### Check if MCP servers are configured

```bash
claude mcp list 2>/dev/null
```

If the servers aren't listed, guide the user through setup (see Setup section below).

### When to use which source

| Source | Best for | Via |
|---|---|---|
| **SSRN** | Working papers, pre-publications, regulatory commentary, IFRS/finance drafts | Jina MCP |
| **arXiv** | CS, ML, NLP, quantitative finance pre-prints | Jina MCP |
| **Web** | Blog posts, news, regulatory agency pages, grey literature | Jina MCP |
| **OpenAlex** | Published journal articles, citation counts, broad coverage (100k+ venues) | Academix MCP |
| **CrossRef** | DOI resolution, publisher metadata, exact bibliographic data | Academix MCP |
| **Semantic Scholar** | AI-powered related paper recommendations, citation networks | Academix MCP |

### Field-specific guidance

**IFRS / Accounting / Finance:**
Start with SSRN — it's where IASB comments, Deloitte analyses, and pre-publication drafts land first. Then complement with OpenAlex for published versions in *Journal of Accounting Research*, *Contemporary Accounting Research*, *Accounting Review*.

**Ethics / Business Ethics:**
SSRN has strong coverage via the Philosophy Research Network and Business Ethics eJournal. OpenAlex covers *Journal of Business Ethics*, *Business & Society*, *Ethics*.

**CS / AI / NLP:**
Start with arXiv via Jina, then Semantic Scholar for citation networks and related papers.

**Interdisciplinary topics:**
Run parallel searches across SSRN (working papers) and OpenAlex (published journals) to get both cutting-edge and peer-reviewed coverage.

---

## Research Workflows

### Standard literature search

For a given topic, run searches in parallel across sources, then deduplicate and present results:

**Step 1: Search across sources**

Use the MCP tools in parallel:

```
# Via Jina MCP — search SSRN for working papers
Tool: search_ssrn
Input: {"query": "IFRS 17 insurance contracts implementation challenges"}

# Via Academix MCP — search published literature
Tool: academic_search_papers
Input: {"query": "IFRS 17 insurance contracts implementation", "limit": 20}
```

**Step 2: Deduplicate**

Papers often appear in both SSRN (as working papers) and published journals. Check by title similarity and DOI overlap. Prefer the published version when both exist, but note the SSRN version if it has a more recent revision.

**Step 3: Get full metadata for promising results**

```
# Via Academix — get detailed metadata
Tool: academic_get_paper_details
Input: {"paper_id": "DOI or OpenAlex ID"}

# Via Jina — read the actual paper page for abstract/content
Tool: read_url
Input: {"url": "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=XXXXX"}
```

**Step 4: Export BibTeX**

```
# Via Academix — batch BibTeX export
Tool: academic_get_bibtex
Input: {"paper_ids": ["doi1", "doi2", "doi3"]}
```

### Citation network exploration

When the user has a seed paper and wants to find related work:

```
# Forward citations (who cites this paper?)
Tool: academic_get_citations
Input: {"paper_id": "10.xxxx/yyyy"}

# AI-powered related papers (thematically similar)
Tool: academic_get_related_papers
Input: {"paper_id": "10.xxxx/yyyy"}

# Full citation network for visualization
Tool: academic_get_citation_network
Input: {"paper_id": "10.xxxx/yyyy"}
```

### Author search

```
# Find all papers by an author
Tool: academic_search_author
Input: {"author_name": "Barth, Mary E."}
```

### Deep web research with Jina

For topics where academic databases aren't enough (regulatory developments, industry reports):

```
# Web search for recent regulatory content
Tool: search_web
Input: {"query": "EFRAG sustainability reporting standards ESRS 2025 update"}

# Read specific pages
Tool: read_url
Input: {"url": "https://www.efrag.org/..."}
```

---

## Output Conventions

### Search results presentation

Present results in a structured table:

```markdown
| # | Title | Authors | Year | Source | DOI/URL |
|---|-------|---------|------|--------|---------|
| 1 | ... | ... | 2024 | SSRN | https://ssrn.com/abstract=... |
| 2 | ... | ... | 2023 | J. of Accounting Research | 10.xxxx/... |
```

Group by source type: **Working Papers** first, then **Published Articles**, then **Grey Literature**.

### BibTeX output

When the user wants citations, always export via `academic_get_bibtex` for published papers. For SSRN-only papers, construct BibTeX manually:

```bibtex
@techreport{AuthorYear,
  author    = {Last, First and Last2, First2},
  title     = {Paper Title},
  year      = {2024},
  type      = {Working Paper},
  institution = {SSRN},
  url       = {https://ssrn.com/abstract=XXXXXXX},
  note      = {SSRN Working Paper}
}
```

### Integration with Zotero

After finding papers, offer to add them to Zotero using the zotero-skill. The workflow is:
1. Search and identify papers (this skill)
2. Export BibTeX or collect metadata
3. Add to Zotero collection (zotero-skill, via Web API)

---

## Available MCP Tools Reference

### Jina MCP Tools

| Tool | Description | Key Parameters |
|---|---|---|
| `search_ssrn` | Search SSRN working papers | `query` |
| `search_arxiv` | Search arXiv pre-prints | `query` |
| `search_web` | General web search | `query` |
| `search_bibtex` | Search for BibTeX citations | `query` |
| `search_images` | Search images | `query` |
| `read_url` | Extract clean content from URLs | `url` |
| `capture_screenshot_url` | Screenshot a webpage | `url` |
| `extract_pdf` | Extract content from PDF URL | `url` |
| `sort_by_relevance` | Re-rank results by relevance | `query`, `documents` |
| `deduplicate_strings` | Deduplicate text list | `strings` |
| `expand_query` | Expand a search query for better recall | `query` |
| `parallel_search_ssrn` | Parallel SSRN search | `queries` |
| `parallel_search_arxiv` | Parallel arXiv search | `queries` |
| `parallel_search_web` | Parallel web search | `queries` |
| `parallel_read_url` | Parallel URL reading | `urls` |

**Performance tip:** Use `expand_query` before searching to generate better query variants. Use `sort_by_relevance` after collecting results from multiple sources to rank them.

**Token savings:** When configuring the Jina MCP, exclude unused tools:
```
https://mcp.jina.ai/v1?exclude_tags=parallel
```

### Academix MCP Tools

| Tool | Description | Key Parameters |
|---|---|---|
| `academic_search_papers` | Search by keywords, title, author, DOI, date, venue | `query`, `limit`, `sort` |
| `academic_get_paper_details` | Full metadata for a paper | `paper_id` (DOI, OpenAlex ID, etc.) |
| `academic_get_bibtex` | Export BibTeX (batch) | `paper_ids` |
| `academic_get_citations` | Papers citing a given paper | `paper_id` |
| `academic_search_author` | Find papers by author | `author_name` |
| `academic_get_related_papers` | AI-powered recommendations | `paper_id` |
| `academic_get_citation_network` | Citation graph (nodes/edges) | `paper_id` |
| `academic_cache_stats` | Cache performance metrics | — |

---

## Setup Instructions

### 1. Jina MCP (remote, no local setup)

Get a free API key at https://jina.ai/api-dashboard/, then:

```bash
# Set environment variable (add to ~/.zshrc for persistence)
export JINA_API_KEY="jina_..."

# Add to Claude Code
claude mcp add-json jina '{"type":"streamable-http","url":"https://mcp.jina.ai/v1?exclude_tags=parallel","headers":{"Authorization":"Bearer '${JINA_API_KEY}'"}}'
```

Note: We exclude parallel tools by default to save context tokens. Add them back if needed for batch operations.

### 2. Academix MCP (local server)

```bash
# Install
uv tool install academix

# Set environment variables (add to ~/.zshrc)
export ACADEMIX_EMAIL="your.email@example.com"  # unlocks higher rate limits
# export SEMANTIC_SCHOLAR_API_KEY="..."  # optional, for higher S2 limits

# Add to Claude Code
claude mcp add-json academix '{"type":"stdio","command":"uvx","args":["academix"],"env":{"ACADEMIX_EMAIL":"'${ACADEMIX_EMAIL}'"}}'
```

### 3. Verify

```bash
claude mcp list
# Should show: jina, academix
```

### Fallback: Without MCP servers

If MCP servers aren't available, the skill can fall back to direct API calls:

**OpenAlex** (no key required, email recommended for rate limits):
```bash
curl -s "https://api.openalex.org/works?search=QUERY&per_page=10&mailto=EMAIL" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for w in data.get('results', []):
    title = w.get('title', '?')
    year = w.get('publication_year', '?')
    doi = w.get('doi', '-')
    print(f'{title} ({year}) — {doi}')
"
```

**CrossRef** (no key required):
```bash
curl -s "https://api.crossref.org/works?query=QUERY&rows=10" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for item in data.get('message', {}).get('items', []):
    title = item.get('title', ['?'])[0]
    year = str(item.get('published-print', item.get('published-online', {})).get('date-parts', [['']])[0][0])
    doi = item.get('DOI', '-')
    print(f'{title} ({year}) — {doi}')
"
```

**SSRN** (via Jina read_url or direct scraping):
```bash
# Read SSRN search results page
python3 -c "
import urllib.request, json
url = 'https://api.ssrn.com/content/v1/bindings/search?terms=QUERY&sort=Relevance&limit=10'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.load(r)
        for p in data.get('papers', []):
            print(f\"{p.get('title','?')} — {p.get('authors','?')} ({p.get('publicDate','?')[:4]})\")
            print(f\"  https://ssrn.com/abstract={p.get('id','')}\")
except Exception as e:
    print(f'SSRN API error: {e} — use Jina read_url as fallback')
"
```

## Error Handling

| Error | Cause | Fix |
|---|---|---|
| "MCP server not found" | Server not configured | Run setup commands above |
| Rate limit on OpenAlex | No email set | Set `ACADEMIX_EMAIL` |
| Rate limit on Semantic Scholar | No API key | Set `SEMANTIC_SCHOLAR_API_KEY` (optional) |
| SSRN search returns empty | Query too specific | Broaden terms, try `expand_query` |
| Jina auth error | Invalid/expired key | Refresh at jina.ai/api-dashboard |
| "Tool not available" | Wrong MCP config | Check `claude mcp list`, reconfigure |

## Known Limitations

- **SSRN full-text**: Many SSRN papers are behind download walls. `read_url` gets the abstract page but not always the full PDF. Use `extract_pdf` if a direct PDF URL is available.
- **OpenAlex coverage**: Strong for STEM and major social science journals. Weaker for niche regional journals and very recent publications (indexing lag of days to weeks).
- **Semantic Scholar**: Excellent for CS/ML citation networks, but sparser for accounting/finance. Use OpenAlex citations as primary for those fields.
- **DBLP**: Not included — it's CS-only and not relevant for IFRS/Finance/Ethics. Academix uses it internally for BibTeX quality but it's not exposed as a search source.
