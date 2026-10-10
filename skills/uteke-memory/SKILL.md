---
name: uteke-memory
description: "Persistent memory engine via uteke MCP tools — use when the user asks to remember, save, or store something to memory, or to recall/search past memories. Auto-use on 'simpan ke memory', 'ingat ini', 'recall', 'what did we decide about X'."
---

# Uteke Memory

Persistent local-first memory via uteke MCP tools (`mcp__uteke_*`). MCP tools are the default interface; do not shell out to `uteke.exe` unless MCP is unavailable.

## When to Use (MANDATORY triggers)

| User says | Action |
|---|---|
| "simpan/ingetin/catat ke memory", "remember this" | `uteke_remember` with the content |
| "recall/cari di memory", "apa yang kita bahas soal X" | `uteke_recall` first, answer from results |
| Before starting work on a project | `uteke_recall` for project context |
| Big decision made in conversation | proactively `uteke_remember` it (decisions, preferences, gotchas) |

Do NOT wait for an explicit "uteke" keyword — the user says "memory", it means uteke.

## Tool Routes

| Need | Tool |
|---|---|
| Store | `uteke_remember` — content, tags, type (fact/decision/procedure/preference), importance |
| Semantic + keyword search | `uteke_recall` — query, limit |
| Exact keyword | `uteke_search` — FTS5 |
| Fetch full record | `uteke_get` — by id |
| Update | `uteke_update` — partial fields |
| Supersede | `uteke_supersede` — mark old memory replaced by newer (decisions that pivot) |
| Pin | `uteke_pin` / `uteke_unpin` |
| Delete | `uteke_forget` |
| Stats / health | `uteke_stats`, `uteke_verify` |
| Docs/wiki | `uteke_doc_*` |
| Graph | `uteke_graph`, `uteke_graph_add_edge` |
| Rooms | `uteke_room_*` |

## Project-Aware Memory (MANDATORY)

- Always tag project-specific memories with `project:<name>` (lowercase, repo folder name).
- Always scope recall: `tags=["project:<name>"]`.
- No specific project in conversation → no `project:` tag.

## Rules

1. One fact per memory; concise self-contained sentence.
2. Decisions: type `decision`, include why + date context.
3. Contradicting a prior memory → `uteke_supersede` the old one, don't leave both active.
4. Durable facts (user prefs, architecture, install locations) → remember proactively, mention briefly.
5. Never store secrets (API keys, passwords, tokens).
