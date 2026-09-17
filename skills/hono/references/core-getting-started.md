---
name: core-getting-started
description: Installing, scaffolding, and the Hono mental model — Web Standards, zero-dep, multi-runtime
---

# Getting Started

Hono is a small, ultrafast web framework built on Web Standards with zero runtime dependencies. The same application code runs on Cloudflare Workers, Deno, Bun, Node.js, AWS Lambda, Vercel, and Netlify — only the entry-point wiring differs.

## Scaffolding

Use `create-hono` to pull a starter template:

```sh
npm create hono@latest my-app
```

Pick a template for your target runtime (`cloudflare-workers`, `bun`, `deno`, `nodejs`, `vercel`, `aws-lambda`, `nextjs`, etc.). For non-interactive scaffolding, forward flags after `--` (npm requires the `--`):

```sh
npm create hono@latest my-app -- --template cloudflare-workers --pm pnpm --install
```

Useful flags: `--template <name>` (skip the prompt), `--install` (auto-install deps), `--pm <npm|pnpm|yarn>`, `--offline` (use local cache).

Then start the dev server:

```sh
cd my-app && npm run dev
```

## Minimal Application

```ts
import { Hono } from 'hono'

const app = new Hono()

app.get('/', (c) => c.text('Hello Hono!'))
app.get('/api/hello', (c) => c.json({ ok: true, message: 'Hello!' }))
app.post('/posts', (c) => c.text('Created!', 201))
app.delete('/posts/:id', (c) => c.text(`${c.req.param('id')} deleted!`))

export default app
```

`export default app` works for Cloudflare Workers and Bun. For other runtimes, wire `app.fetch` into the platform's entry point — the route code above stays unchanged.

## Runtime Entry Points

Application code is runtime-agnostic; only the entry differs:

```ts
// Cloudflare Workers (module syntax)
export default {
  fetch(request: Request, env: Env, ctx: ExecutionContext) {
    return app.fetch(request, env, ctx)
  },
}
```

```ts
// Bun
export default {
  port: 3000,
  fetch: app.fetch,
}
```

```ts
// Node.js — use @hono/node-server
import { serve } from '@hono/node-server'
serve({ fetch: app.fetch, port: 3000 })
```

Adapters for platform-specific features (WebSocket, static files) live under `hono/<runtime>` (e.g. `hono/cloudflare-workers`).

## Mental Model

- **Web Standards**: Hono uses `Request`/`Response`, `Headers`, `fetch` — no custom abstractions to learn.
- **Zero dependencies**: middleware and adapters are bundled only when imported, so the core stays tiny.
- **Context-centric**: every handler receives `c: Context` — read the request via `c.req`, shape the response via `c.text()`/`c.json()`/`c.html()`, pass values between middleware via `c.set()`/`c.get()`.
- **Handler vs Middleware**: a handler returns a `Response` (only one runs). Middleware calls `await next()` to continue the chain, or returns a `Response` to short-circuit.

## Presets

Hono ships size-optimized presets imported via subpaths — `hono/tiny` (smallest, under 14KB minified) and `hono/quick` (balanced). Reach for them when bundle size is critical (edge/CDN). The `router` constructor option selects the router implementation (`RegExpRouter` for raw speed, `LinearRouter` for fast cold-start, `PatternRouter` for minimal size) — see the advanced-internals reference for router selection and preset internals.

<!--
Source references:
- https://hono.dev/docs/getting-started/basic
- https://hono.dev/docs/guides/create-hono
- https://hono.dev/docs/concepts/motivation
- https://hono.dev/docs/concepts/philosophy
-->
