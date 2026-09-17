---
name: advanced-internals
description: Router internals, how SmartRouter picks, and when to use each preset
---

# Router Internals & Presets

Hono has five routers, each optimized for a different tradeoff. The default `Hono` class uses SmartRouter with RegExpRouter + TrieRouter.

## RegExpRouter

The fastest router in the JavaScript world. It compiles all registered routes into one large regular expression and matches in a single pass — faster than tree-based (radix/trie) algorithms in most cases.

```ts
import { RegExpRouter } from 'hono/router'
```

Tradeoff: doesn't support all routing patterns (e.g. some complex wildcard/regex combos). Usually paired with TrieRouter via SmartRouter so unsupported patterns fall back.

## SmartRouter

Selects the fastest router at startup by benchmarking the registered routes against its candidates. This is what the default `Hono` class uses internally.

```ts
// Inside Hono core:
new SmartRouter({
  routers: [new RegExpRouter(), new TrieRouter()],
})
```

When the application starts, SmartRouter runs a quick benchmark and picks the winner. If RegExpRouter can't handle the route set, SmartRouter falls back to TrieRouter automatically.

## TrieRouter

Uses a Trie-tree algorithm. Supports all routing patterns (params, wildcards, regex). Slower than RegExpRouter but much faster than Express-style linear routers.

```ts
import { TrieRouter } from 'hono/router'
```

Use when you need full pattern support and can't rely on RegExpRouter's fallback.

## LinearRouter

Optimized for startup speed — route registration is significantly faster than RegExpRouter because it doesn't compile strings. Adds routes linearly and matches with linear loops.

```ts
import { LinearRouter } from 'hono/router'
```

Best for environments that re-initialize the app on every request (where boot time dominates). Used in the `hono/quick` preset.

## PatternRouter

The smallest router. Simply adds and matches patterns with minimal logic. An app using only PatternRouter is under 14KB minified.

```ts
import { PatternRouter } from 'hono/router'
```

Use when bundle size is the primary constraint (resource-limited edge environments). Used in the `hono/tiny` preset.

## Choosing a Router

| Router | Fastest at | Supports all patterns | Startup cost | Bundle size |
|--------|-----------|----------------------|--------------|-------------|
| RegExpRouter | Dispatch | No (most patterns) | Higher (compiles) | Medium |
| SmartRouter | Auto-picks best | Yes (via fallback) | Higher | Medium |
| TrieRouter | Dispatch | Yes | Medium | Medium |
| LinearRouter | Startup | Yes | Lowest | Small |
| PatternRouter | — | Yes | Low | Smallest |

## Presets

Presets bundle a router choice with the `Hono` class so you don't specify the router manually. The `Hono` class is identical across presets — only the default router differs.

### `hono` (default)

```ts
import { Hono } from 'hono'
```

SmartRouter with `[RegExpRouter, TrieRouter]`. Recommended for most cases: long-running servers (Node.js, Bun, Deno) and persistent isolates (Cloudflare Workers, Deno Deploy). Registration is slower but dispatch is fastest once booted.

### `hono/quick`

```ts
import { Hono } from 'hono/quick'
```

SmartRouter with `[LinearRouter, TrieRouter]`. Designed for environments where the app initializes per request (serverless cold starts). Fast startup at the cost of slightly slower dispatch.

### `hono/tiny`

```ts
import { Hono } from 'hono/tiny'
```

PatternRouter only. Under 14KB minified. For resource-constrained environments where bundle size matters most. Supports all patterns but is the slowest at dispatch.

### When to use which

| Preset | Use when |
|--------|----------|
| `hono` | Long-running servers, persistent isolates — most use cases |
| `hono/quick` | App re-initializes on every request (cold-start heavy) |
| `hono/tiny` | Extreme bundle-size constraints on edge |

<!--
Source references:
- https://hono.dev/docs/concepts/routers
- https://hono.dev/docs/api/presets
-->
