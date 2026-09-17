---
name: utilities
description: Misc Hono middleware (events, logging, UA blocking, authz, DI, WebSocket, SSG, Cap'n Web, example, alt router)
---

# Utilities

## Event Emitter

```bash
npm i @hono/event-emitter
```

Lightweight, edge-compatible event emitter. As Hono middleware it adds an `Emitter` to context under the `emitter` key; standalone use `createEmitter(handlers)`. Use `defineHandlers<AvailableEvents>()` for typed handlers.

```ts
import { emitter } from '@hono/event-emitter'
import { Hono } from 'hono'

const handlers = {
  'user:created': [(c, user) => { /* c is Context */ }],
  'user:deleted': [async (c, id) => {}],
}

const app = new Hono()
app.use(emitter(handlers))

app.post('/users', (c) => {
  // sync emit
  c.get('emitter').emit(c, 'user:created', user)
  // or async (concurrent default; { mode: 'sequencial' } to stop on first error)
  // await c.get('emitter').emitAsync(c, 'user:created', user)
  return c.json({ ok: true })
})
```

`on(key, handler)`/`off(key, handler?)` manage listeners; `emit` is sync, `emitAsync` returns a `Promise`. Not request-scoped — one `Emitter` is shared across requests, so only use named (non-anonymous) functions when subscribing inside middleware/handlers to avoid memory leaks. `defineHandler<AvailableEvents, 'user:created'>(fn)` types a single handler.

## Structured Logger

```bash
npm i @hono/structured-logger
```

Library-agnostic structured logging (pino, winston, console). Request-scoped logger on `c.var.logger` with response-time measurement and native `hono/request-id` integration.

```ts
import { Hono } from 'hono'
import { requestId } from 'hono/request-id'
import { structuredLogger, type StructuredLoggerEnv } from '@hono/structured-logger'
import pino from 'pino'

const rootLogger = pino()
const app = new Hono<StructuredLoggerEnv<pino.Logger>>()

app.use(requestId())
app.use(
  structuredLogger({
    createLogger: (c) => rootLogger.child({ requestId: c.var.requestId }),
    onResponse: (logger, c, elapsedMs) =>
      logger.info({ method: c.req.method, path: c.req.path, elapsedMs }, 'request completed'),
  })
)

app.get('/', (c) => { c.var.logger.info('handling'); return c.text('Hello!') })
```

Options: `createLogger(c)` (required), `contextKey` (default `'logger'`; use `StructuredLoggerEnv<L, 'log'>` + `contextKey: 'log'`), `skip(c)`, `onRequest`, `onResponse(logger, c, elapsedMs)` (required), `onError(logger, err, c, elapsedMs)`. `elapsedMs` uses `performance.now()` measured after `onRequest`. Avoid logging in both `onError` and `app.onError()` (duplicates; `HTTPException` never reaches `app.onError`). Works on all Hono runtimes.

## UA Blocker

```bash
npm i @hono/ua-blocker
```

Blocks requests by `User-Agent` and serves AI-bot robots.txt. `blocklist` is `string[]` or a `RegExp` matching uppercase UAs.

```ts
import { uaBlocker } from '@hono/ua-blocker'
import { aiBots, useAiRobotsTxt } from '@hono/ua-blocker/ai-bots'
import { Hono } from 'hono'

const app = new Hono()

app.use('*', uaBlocker({ blocklist: aiBots }))
app.use('/robots.txt', useAiRobotsTxt())
app.get('/', (c) => c.text('Hello World'))
```

Exports: `aiBots` (full AI-bot list from [ai.robots.txt](https://github.com/ai-robots-txt/ai.robots.txt)), `nonRespectingAiBots` (bots that ignore robots.txt), `AI_ROBOTS_TXT` (raw robots.txt content to extend), `useAiRobotsTxt()` (serves the file).

## Casbin

```bash
npm i @hono/casbin casbin
```

Enforces [Casbin](https://casbin.org) authorization policies. Requires model + policy files. Built-in `basicAuthorizer` (from `@hono/casbin/helper`, after `hono/basic-auth`) and `jwtAuthorizer` (after `hono/jwt`, defaults to the `sub` claim; pass a claim mapping).

```ts
import { Hono } from 'hono'
import { basicAuth } from 'hono/basic-auth'
import { newEnforcer } from 'casbin'
import { casbin } from '@hono/casbin'
import { basicAuthorizer } from '@hono/casbin/helper'

const app = new Hono()

app.use(
  '*',
  basicAuth(
    { username: 'alice', password: 'password' },
    { username: 'bob', password: 'password' }
  ),
  casbin({
    newEnforcer: newEnforcer('examples/model.conf', 'examples/policy.csv'),
    authorizer: basicAuthorizer,
  })
)

app.get('/dataset1/test', (c) => c.text('ok')) // alice + bob
app.post('/dataset1/test', (c) => c.text('ok')) // alice only
```

Custom authorizer: `authorizer: async (c, enforcer) => enforcer.enforce(user, path, method)`.

## tsyringe

```bash
npm i @hono/tsyringe tsyringe reflect-metadata
```

Dependency injection via [tsyringe](https://github.com/microsoft/tsyringe). Creates a request-scoped child container; resolve via `c.var.resolve(Token)`.

```ts
import 'reflect-metadata'
import { container, inject, injectable } from 'tsyringe'
import { tsyringe } from '@hono/tsyringe'
import { Hono } from 'hono'

@injectable()
class Hello {
  constructor(@inject('name') private name: string) {}
  greet() { return `Hello, ${this.name}!` }
}

const app = new Hono()

app.use(
  '*',
  tsyringe((container) => {
    container.register('name', { useValue: 'world' })
  })
)

app.get('/', (c) => c.text(c.var.resolve(Hello).greet()))
```

The callback receives the request-scoped `container` and can register factories using `c.req.param`/`c.var` (e.g. `container.register(Config, { useFactory: () => new Config(tenantName) })`). Register shared dependencies on the global `container` before the middleware; they are inherited.

## node-ws (Deprecated)

```bash
npm i @hono/node-ws @hono/node-server
```

> **Deprecated.** `@hono/node-server` v2 now provides built-in WebSocket support via its own `upgradeWebSocket`. Migrate to `@hono/node-server` (see its WebSocket docs).

Before (deprecated):

```ts
import { createNodeWebSocket } from '@hono/node-ws'
import { Hono } from 'hono'
import { serve } from '@hono/node-server'

const app = new Hono()
const { injectWebSocket, upgradeWebSocket } = createNodeWebSocket({ app })

app.get('/ws', upgradeWebSocket((c) => ({ /* websocket helpers */ })))
const server = serve(app)
injectWebSocket(server)
```

After (recommended):

```ts
import { serve, upgradeWebSocket } from '@hono/node-server'
import { WebSocketServer } from 'ws'
import { Hono } from 'hono'

const app = new Hono()
app.get('/ws', upgradeWebSocket((c) => ({ /* websocket helpers */ })))

const wss = new WebSocketServer({ noServer: true })
serve({ fetch: app.fetch, websocket: { server: wss } })
```

## SSG Plugins Essential

```bash
npm i @hono/ssg-plugins-essential
```

Standard plugins for [Hono SSG](https://hono.dev/docs/helpers/ssg) (`toSSG(app, fs, { plugins: [...] })`). Generates `sitemap.xml`, `robots.txt`, and `rss.xml`/`atom.xml` during static generation.

```ts
import { sitemapPlugin } from '@hono/ssg-plugins-essential/sitemap'
import { robotsTxtPlugin } from '@hono/ssg-plugins-essential/robots-txt'
import { rssPlugin } from '@hono/ssg-plugins-essential/rss'
import { toSSG } from 'hono/ssg'
import fs from 'fs/promises'

toSSG(app, fs, {
  plugins: [
    sitemapPlugin({ baseUrl: 'https://example.com', canonicalize: true }),
    robotsTxtPlugin({
      rules: [{ userAgent: '*', allow: ['/'], disallow: ['/private'] }],
      sitemapUrl: 'https://example.com/sitemap.xml',
      extraLines: ['# comment'],
    }),
    rssPlugin({
      baseUrl: 'https://example.com',
      feedTitle: 'My Blog',
      feedDescription: 'Latest updates',
      feedType: 'rss2',
    }),
  ],
})
```

## Cap'n Web

```bash
npm i @hono/capnweb capnweb hono
```

Enables [Cap'n Web](https://github.com/cloudflare/capnweb) RPC over WebSocket and HTTP. Define an API with `RpcTarget`, then return `newRpcResponse(c, server, { upgradeWebSocket })` from a route.

```ts
import { RpcTarget } from 'capnweb'
import { Hono } from 'hono'
import { upgradeWebSocket } from 'hono/cloudflare-workers'
import { newRpcResponse } from '@hono/capnweb'

export class MyApiServer extends RpcTarget {
  hello(name: string) { return `Hello, ${name}!` }
}

const app = new Hono()
app.all('/api', (c) => newRpcResponse(c, new MyApiServer(), { upgradeWebSocket }))
```

Runtime-specific `upgradeWebSocket` import: `hono/cloudflare-workers`, `hono/deno`, `hono/bun`, or `@hono/node-ws` on Node. Client: `newWebSocketRpcSession<Api>('ws://host/api')` (with `using` for cleanup) or `newHttpBatchRpcSession<Api>('http://host/api')`.

## Hello

```bash
npm i @hono/hello
```

Example/reference third-party middleware — adds an `X-Message` header to the response.

```ts
import { hello } from '@hono/hello'
import { Hono } from 'hono'

const app = new Hono()
app.use('*', hello('Hello!! Hono!!'))
app.get('/', (c) => c.text('foo'))
```

## Medley Router

```bash
npm i @hono/medley-router @medley/router
```

A proof-of-concept alternative router using [@medley/router](https://www.npmjs.com/package/@medley/router). Pass it as Hono's `router` option.

```ts
import { Hono } from 'hono'
import { MedleyRouter } from '@hono/medley-router'

const app = new Hono({ router: new MedleyRouter() })
app.get('/', (c) => c.text('Hello'))
```

<!--
Source references:
- https://github.com/honojs/middleware/tree/main/packages/event-emitter
- https://github.com/honojs/middleware/tree/main/packages/structured-logger
- https://github.com/honojs/middleware/tree/main/packages/ua-blocker
- https://github.com/honojs/middleware/tree/main/packages/casbin
- https://github.com/honojs/middleware/tree/main/packages/tsyringe
- https://github.com/honojs/middleware/tree/main/packages/node-ws
- https://github.com/honojs/middleware/tree/main/packages/ssg-plugins-essential
- https://github.com/honojs/middleware/tree/main/packages/capnweb
- https://github.com/honojs/middleware/tree/main/packages/hello
- https://github.com/honojs/middleware/tree/main/packages/medley-router
-->
