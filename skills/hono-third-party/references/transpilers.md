---
name: transpilers
description: Bundler/transpiler and compression helpers for Hono (esbuild, Bun transpiler, Bun compress)
---

# Transpilers & Compression

These middlewares transpile TypeScript/TSX served statically from disk. Mount the transpiler on a route matching the file extension (before `serveStatic`), and the script is transpiled to JavaScript on the fly. None include caching — pair with Hono's `hono/cache` or custom caching for production.

## esbuild Transpiler

```bash
# Cloudflare Workers/Pages (Wasm)
npm i @hono/esbuild-transpiler esbuild-wasm
# Node.js (native esbuild)
npm i @hono/node-server @hono/esbuild-transpiler esbuild
```

```ts
import { Hono } from 'hono'
import { serveStatic } from 'hono/cloudflare-workers'
import { esbuildTranspiler } from '@hono/esbuild-transpiler/wasm'
import wasm from '../node_modules/esbuild-wasm/esbuild.wasm'

const app = new Hono()

app.get('/static/:scriptName{.+.tsx?}', esbuildTranspiler({ wasmModule: wasm }))
app.get('/static/*', serveStatic({ root: './' }))
```

Import path differs by runtime: `/wasm` (Cloudflare, with `wasmModule`), root (Deno, passing `{ esbuild }` after `esbuild.initialize({ wasmURL, worker: false })`), or `/node` (Node.js, no options). Declare `*.wasm` modules in `global.d.ts`. Works on Cloudflare Workers, Deno/Deno Deploy, and Node.js. Note: incompatible with `@hono/vite-dev-server` (no Wasm support; use Vite's own transpilation).

## Bun Transpiler

```bash
npm i @hono/bun-transpiler
```

Bun-native transpilation of TypeScript/TSX. Works only on [Bun](https://bun.sh/).

```ts
import { Hono } from 'hono'
import { serveStatic } from 'hono/bun'
import { bunTranspiler } from '@hono/bun-transpiler'

const app = new Hono()

app.get('/static/:scriptName{.+.tsx?}', bunTranspiler())
app.get('/static/*', serveStatic({ root: './' }))
```

## Bun Compress (Deprecated)

```bash
npm i @hono/bun-compress
```

> **Deprecated.** Bun now supports `CompressionStream` natively. Use the built-in [`hono/compress`](https://hono.dev/docs/middleware/builtin/compress) middleware instead.

Migration — replace:

```ts
import { compress } from '@hono/bun-compress'
```

with:

```ts
import { compress } from 'hono/compress'
```

The API is identical; no other changes are needed.

<!--
Source references:
- https://github.com/honojs/middleware/tree/main/packages/esbuild-transpiler
- https://github.com/honojs/middleware/tree/main/packages/bun-transpiler
- https://github.com/honojs/middleware/tree/main/packages/bun-compress
-->
