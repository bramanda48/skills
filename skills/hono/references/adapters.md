---
name: adapters
description: Multi-runtime deployment model — the same Hono app runs on every JS runtime via adapters
---

# Adapters

Hono runs on any JavaScript runtime using only Web Standard APIs. The same application code works everywhere — only the entry-point/serve code differs per runtime.

## Adapter Helper

```ts
import { env, getRuntimeKey } from 'hono/adapter'
```

### `env(c)`

Retrieve environment variables across runtimes in a unified way. On Node.js/Bun reads `process.env`, on Cloudflare reads `wrangler.toml` bindings, on Deno reads `Deno.env`.

```ts
app.get('/env', (c) => {
  const { NAME } = env<{ NAME: string }>(c)
  return c.text(NAME)
})
```

Pass a runtime key as the second argument to force a specific runtime: `env(c, 'workerd')`.

### `getRuntimeKey()`

Returns the current runtime identifier. Keys: `'workerd'` (Cloudflare Workers), `'deno'`, `'bun'`, `'node'`, `'edge-light'` (Vercel Edge), `'fastly'`, or `'other'`.

```ts
app.get('/', (c) => {
  if (getRuntimeKey() === 'workerd') {
    return c.text('Running on Cloudflare')
  }
  return c.text('Other runtime')
})
```

## Cloudflare Workers

Export `app` as the default export. Bindings (KV, R2, D1, secrets) are typed via `Hono<{ Bindings }>` and accessed via `c.env`.

```ts
type Bindings = {
  MY_BUCKET: R2Bucket
  USERNAME: string
}

const app = new Hono<{ Bindings: Bindings }>()

app.get('/', (c) => c.text('Hello Cloudflare Workers!'))

export default app
```

For scheduled events or other handlers, export an object: `export default { fetch: app.fetch, scheduled: async (batch, env) => {} }`.

## Deno

Use `Deno.serve()` with `app.fetch`.

```ts
import { Hono } from 'hono'

const app = new Hono()
app.get('/', (c) => c.text('Hello Deno!'))

Deno.serve(app.fetch)
```

Specify port: `Deno.serve({ port: 8787 }, app.fetch)`.

## Bun

Export `app` as default, or export an object with `port` and `fetch`.

```ts
import { Hono } from 'hono'

const app = new Hono()
app.get('/', (c) => c.text('Hello Bun!'))

export default {
  port: 3000,
  fetch: app.fetch,
}
```

## Node.js

Use `@hono/node-server` (requires Node.js 18.14.1+, 19.7.0+, or 20+).

```ts
import { serve } from '@hono/node-server'
import { Hono } from 'hono'

const app = new Hono()
app.get('/', (c) => c.text('Hello Node.js!'))

serve(app)
```

Specify port: `serve({ fetch: app.fetch, port: 8787 })`. Access raw Node APIs via `c.env.incoming` / `c.env.outgoing` (type with `HttpBindings` from `@hono/node-server`).

## AWS Lambda

Use `handle` from `hono/aws-lambda`. Exports a Lambda handler.

```ts
import { Hono } from 'hono'
import { handle } from 'hono/aws-lambda'

const app = new Hono()
app.get('/', (c) => c.text('Hello Hono!'))

export const handler = handle(app)
```

Access Lambda event/context via typed bindings: `type Bindings = { event: LambdaEvent; lambdaContext: LambdaContext }`. For streaming responses, use `streamHandle(app)` instead and set `invokeMode: RESPONSE_STREAM` on the function URL.

## Vercel

Export `app` as default. Zero-config deployment.

```ts
import { Hono } from 'hono'

const app = new Hono()
app.get('/', (c) => c.text('Hello Hono!'))

export default app
```

## Netlify

For Netlify Edge Functions, use `handle` from `jsr:@hono/hono/netlify`.

```ts
import { Hono } from 'jsr:@hono/hono'
import { handle } from 'jsr:@hono/hono/netlify'

const app = new Hono()
app.get('/', (c) => c.text('Hello Hono!'))

export default handle(app)
```

Access Netlify's `Context` via `c.env.context` (geo, cookies, etc.).

## Lambda@Edge

Use `handle` from `hono/lambda-edge`.

```ts
import { Hono } from 'hono'
import { handle } from 'hono/lambda-edge'

const app = new Hono()
app.get('/', (c) => c.text('Hello Hono on Lambda@Edge!'))

export const handler = handle(app)
```

For continuing request processing after middleware (e.g. Basic Auth), use `c.env.callback(null, c.env.request)` in a handler. Typed bindings: `Callback` and `CloudFrontRequest`.

## Service Worker

Use `handle` or `fire` from `hono/service-worker`. Runs the Hono app as a browser `FetchEvent` handler.

```ts
declare const self: ServiceWorkerGlobalScope

import { Hono } from 'hono'
import { fire } from 'hono/service-worker'

const app = new Hono().basePath('/sw')
app.get('/', (c) => c.text('Hello World'))

fire(app)
```

`fire(app)` is shorthand for `self.addEventListener('fetch', handle(app))`.

## Fastly Compute

Use `fire` from `@fastly/hono-fastly-compute`.

```ts
import { Hono } from 'hono'
import { fire } from '@fastly/hono-fastly-compute'

const app = new Hono()
app.get('/', (c) => c.text('Hello Fastly!'))

fire(app)
```

For bindings (KV Stores, Config Stores, etc.), use `buildFire` instead and type with `typeof fire.Bindings`. Use `Hono` from `'hono'` (not `'hono/quick'`) since `fire` builds router data at init.

<!--
Source references:
- https://hono.dev/docs/concepts/stacks
- https://hono.dev/docs/helpers/adapter
- https://hono.dev/docs/getting-started/cloudflare-workers
- https://hono.dev/docs/getting-started/deno
- https://hono.dev/docs/getting-started/bun
- https://hono.dev/docs/getting-started/nodejs
- https://hono.dev/docs/getting-started/aws-lambda
- https://hono.dev/docs/getting-started/vercel
- https://hono.dev/docs/getting-started/netlify
- https://hono.dev/docs/getting-started/lambda-edge
- https://hono.dev/docs/getting-started/service-worker
- https://hono.dev/docs/getting-started/fastly
-->
