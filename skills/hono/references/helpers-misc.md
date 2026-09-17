---
name: misc
description: Quick reference for Accepts, Adapter, ConnInfo, Proxy, JWT, and Dev helpers
---

# Miscellaneous Helpers

## Accepts

`accepts()` negotiates an `Accept-*` header against the values your app supports and returns the best match (or the default).

```ts
import { accepts } from 'hono/accepts'

app.get('/', (c) => {
  const lang = accepts(c, {
    header: 'Accept-Language',
    supports: ['en', 'ja', 'zh'],
    default: 'en',
  })
  return c.json({ lang })
})
```

Valid headers: `Accept`, `Accept-Charset`, `Accept-Encoding`, `Accept-Language`, `Accept-Patch`, `Accept-Post`, `Accept-Ranges`. An optional `match` function overrides the default negotiation algorithm.

## Adapter (env, getRuntimeKey)

`env()` reads environment variables across runtimes (Cloudflare `wrangler.toml`, `process.env`, `Deno.env`, etc.) so you don't branch on platform manually:

```ts
import { env, getRuntimeKey } from 'hono/adapter'

app.get('/env', (c) => {
  const { NAME } = env<{ NAME: string }>(c) // works on Workers, Node, Bun, Deno
  return c.text(NAME)
})

app.get('/whoami', (c) => {
  const key = getRuntimeKey() // 'workerd' | 'deno' | 'bun' | 'node' | 'edge-light' | 'fastly' | 'other'
  return c.text(key)
})
```

Pin a runtime explicitly with the second argument: `env<{ X: string }>(c, 'workerd')`.

## ConnInfo

`getConnInfo(c)` returns the remote client's address and transport info. The import path is runtime-specific:

```ts
import { getConnInfo } from 'hono/cloudflare-workers'
// 'hono/deno', 'hono/bun', 'hono/vercel', '@hono/node-server/conninfo', etc.

app.get('/', (c) => {
  const info = getConnInfo(c)
  return c.text(`Your remote address is ${info.remote.address}`)
})
```

`ConnInfo.remote` is a `NetAddrInfo` with `address`, `addressType` (`'IPv4' | 'IPv6' | undefined`), `port`, and `transport` (`'tcp' | 'udp'`). Not all fields are populated on every runtime.

## Proxy

`proxy()` is a `fetch()` wrapper for reverse-proxying. It returns a `Response` ready to return from a handler and rewrites `Accept-Encoding` to what the current runtime supports. Hop-by-hop `Connection` headers are stripped by default to prevent injection.

```ts
import { proxy } from 'hono/proxy'

app.get('/proxy/:path', (c) => {
  return proxy(`http://origin-server/${c.req.param('path')}`)
})
```

Forward and override headers — set a value to `undefined` to drop it:

```ts
app.all('/proxy/:path', (c) => {
  return proxy(`http://origin/${c.req.param('path')}`, {
    ...c.req, // forward method/body
    headers: {
      ...c.req.header(),
      'X-Forwarded-For': '127.0.0.1',
      'X-Forwarded-Host': c.req.header('host'),
      Authorization: undefined, // strip the auth header
    },
  })
})
```

Use `customFetch` to override the global `fetch` (e.g. for service bindings) and `strictConnectionProcessing: true` for strict RFC 9110 connection-header handling in trusted environments.

## JWT Utility (sign / verify / decode)

Low-level JWT functions from `hono/jwt` — distinct from the `jwt()` middleware, which is the higher-level guard. Use these when you need manual control.

```ts
import { sign, verify, decode } from 'hono/jwt'

const secret = 'mySecretKey'

const token = await sign(
  { sub: 'user123', role: 'admin', exp: Math.floor(Date.now() / 1000) + 300 },
  secret
)

const payload = await verify(token, secret, 'HS256')

const { header, payload: decoded } = decode(token) // no signature check
```

`verify` validates `exp`, `nbf`, `iat`, `iss` (via `issuer` option), and `aud` (via `aud` option) claims when present. Supported algorithms: `HS256/384/512`, `RS256/384/512`, `PS256/384/512`, `ES256/384/512`, `EdDSA`. `decode()` does not verify — use it only for inspection or debugging.

## Dev

```ts
import { getRouterName, showRoutes } from 'hono/dev'

console.log(getRouterName(app)) // e.g. 'HonoRouter' or 'RegExpRouter'

showRoutes(app, { verbose: true, colorize: true })
// GET   /v1/posts
// GET   /v1/posts/:id
// POST  /v1/posts
```

`showRoutes` prints a route table at startup; `getRouterName` returns the active router implementation. Both are dev-only helpers — don't ship them in production hot paths.

<!--
Source references:
- https://hono.dev/docs/helpers/accepts
- https://hono.dev/docs/helpers/adapter
- https://hono.dev/docs/helpers/conninfo
- https://hono.dev/docs/helpers/proxy
- https://hono.dev/docs/helpers/jwt
- https://hono.dev/docs/helpers/dev
-->
