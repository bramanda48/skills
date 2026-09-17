---
name: middleware-common
description: Common utility built-in middleware — CORS, logger, cache, compress, timing, and more
---

# Common Middleware

Built-in utility middleware for cross-cutting concerns. All import from `hono/*` subpaths — no extra packages needed.

## CORS

```ts
import { cors } from 'hono/cors'
```

Enable cross-origin requests. Must be registered before routes.

```ts
app.use('/api/*', cors({
  origin: ['https://example.com', 'https://example.org'],
  allowHeaders: ['X-Custom-Header'],
  allowMethods: ['POST', 'GET', 'OPTIONS'],
  exposeHeaders: ['Content-Length'],
  maxAge: 600,
  credentials: true,
}))
```

`origin`, `allowMethods` accept a function for dynamic per-request decisions. For environment-based config, inline the middleware to read `c.env`:

```ts
app.use('*', async (c, next) => {
  return cors({ origin: c.env.CORS_ORIGIN })(c, next)
})
```

Key options: `origin` (default `*`), `allowMethods`, `allowHeaders`, `exposeHeaders`, `maxAge`, `credentials`.

## Logger

```ts
import { logger } from 'hono/logger'
```

Logs incoming requests and outgoing responses with method, path, status, and elapsed time. Status codes are color-coded (disable with `NO_COLOR` env var).

```ts
app.use(logger())
```

Pass a custom `PrintFunc` for tailored output: `app.use(logger((str, ...rest) => console.log(str, ...rest)))`.

## Pretty JSON

```ts
import { prettyJSON } from 'hono/pretty-json'
```

Pretty-prints JSON responses when `?pretty` is in the query string.

```ts
app.use(prettyJSON())
```

Key options: `space: number` (default `2`), `query: string` (default `'pretty'`), `force: boolean` (always prettify, default `false`).

## Request ID

```ts
import { requestId } from 'hono/request-id'
import type { RequestIdVariables } from 'hono/request-id'
```

Generates a unique ID per request, accessible via `c.get('requestId')`. If the `X-Request-Id` header is present, it uses that value instead.

```ts
const app = new Hono<{ Variables: RequestIdVariables }>()
app.use('*', requestId())

app.get('/', (c) => c.text(`Request id: ${c.get('requestId')}`))
```

Key options: `headerName` (default `'X-Request-Id'`, set to `''` to disable passthrough), `limitLength` (default `255`), `generator: (c) => string` (default `crypto.randomUUID()`). Use `generator` to capture platform-specific IDs (e.g. AWS Lambda context).

## ETag

```ts
import { etag } from 'hono/etag'
```

Adds `ETag` headers and returns `304 Not Modified` for matching conditional requests.

```ts
app.use('/etag/*', etag())
```

Key options: `weak: boolean` (weak validation, default `false`), `retainedHeaders: string[]` (extend `RETAINED_304_HEADERS` for custom 304 headers), `generateDigest: (body: Uint8Array) => ArrayBuffer` (default SHA-1).

## Cache

```ts
import { cache } from 'hono/cache'
```

Caches responses using the Web Cache API. Supports Cloudflare Workers (custom domains) and Deno 1.26+.

```ts
// Cloudflare Workers
app.get('*', cache({
  cacheName: 'my-app',
  cacheControl: 'max-age=3600',
}))

// Deno — must set wait: true
app.get('*', cache({
  cacheName: 'my-app',
  cacheControl: 'max-age=3600',
  wait: true,
}))
```

Key options: `cacheName` (required, accepts `(c) => string`), `cacheControl`, `wait` (required `true` on Deno), `vary`, `keyGenerator`, `cacheableStatusCodes` (default `[200]`), `maxQueryBodySize` (default 64 KiB for QUERY requests).

## Compress

```ts
import { compress } from 'hono/compress'
```

Compresses response body based on `Accept-Encoding`. Not needed on Cloudflare Workers or Deno Deploy (they auto-compress).

```ts
app.use(compress())
```

Key options: `encoding: 'gzip' | 'deflate'`, `threshold: number` (default `1024` bytes), `contentTypeFilter: RegExp | (type) => boolean` (use exported `COMPRESSIBLE_CONTENT_TYPE_REGEX` to extend defaults).

## Server-Timing

```ts
import { timing, setMetric, startTime, endTime, wrapTime } from 'hono/timing'
import type { TimingVariables } from 'hono/timing'
```

Adds `Server-Timing` response headers with performance metrics.

```ts
const app = new Hono<{ Variables: TimingVariables }>()
app.use(timing())

app.get('/', async (c) => {
  setMetric(c, 'region', 'europe-west3')
  setMetric(c, 'custom', 23.8, 'My custom Metric')
  startTime(c, 'db')
  const data = await db.findMany()
  endTime(c, 'db')
  return c.json({ data })
})
```

Key options: `total` (default `true`), `enabled: boolean | (c) => boolean`, `crossOrigin` (default `false`). Use `wrapTime(c, 'db', promise)` as a shorthand for start/end.

## Language

```ts
import { languageDetector } from 'hono/language'
```

Detects the user's preferred locale from query string, cookie, header, or path. Detected language is available via `c.get('language')`.

```ts
app.use(languageDetector({
  supportedLanguages: ['en', 'ar', 'ja'],
  fallbackLanguage: 'en',
}))
```

For path-based detection (`/en/about`), set `order: ['path', 'cookie', 'querystring', 'header']` and `lookupFromPathIndex: 0`. `fallbackLanguage` must be in `supportedLanguages`. Use `convertDetectedLanguage` to normalize codes (e.g. `en-US` to `en`). Disable cookie caching with `caches: false`.

Key options: `supportedLanguages` (required), `fallbackLanguage` (required), `order` (default `['querystring', 'cookie', 'header']`), `lookupQueryString` (default `'lang'`), `lookupCookie` (default `'language'`), `lookupFromHeaderKey` (default `'accept-language'`), `caches` (default `['cookie']`), `debug`.

## Trailing Slash

```ts
import { appendTrailingSlash, trimTrailingSlash } from 'hono/trailing-slash'
```

`appendTrailingSlash` redirects `/about/me` to `/about/me/`; `trimTrailingSlash` does the reverse. Only applies to GET requests that would 404.

```ts
const app = new Hono({ strict: true })
app.use(trimTrailingSlash())
```

Key options: `alwaysRedirect: boolean` (redirect before handlers — needed for wildcard routes), `skip: (path) => boolean` (e.g. skip paths with file extensions).

## Method Override

```ts
import { methodOverride } from 'hono/method-override'
```

Lets HTML forms use methods like DELETE/PATCH by reading an override value from a form field, header, or query.

```ts
app.use('/posts', methodOverride({ app }))

app.delete('/posts', (c) => {
  // Triggered by <form method="POST"><input name="_method" value="DELETE">
})
```

Key options: `app: Hono` (required), `form` (default `'_method'`), `header` (header name), `query` (query param key).

## Method Not Allowed

```ts
import { methodNotAllowed } from 'hono/method-not-allowed'
```

Returns `405 Method Not Allowed` with an `Allow` header when the path matches a route but the method doesn't. Without this, Hono returns 404.

```ts
app.use(methodNotAllowed({ app }))
```

Key options: `app: Hono` (required), `onMethodNotAllowed: (c, allowedMethods) => Response` (customize the 405 response).

## Body Limit

```ts
import { bodyLimit } from 'hono/body-limit'
```

Limits request body size. Checks `Content-Length` first; streams the body and errors if the limit is exceeded.

```ts
app.post('/upload', bodyLimit({
  maxSize: 50 * 1024,
  onError: (c) => c.text('overflow :(', 413),
}), async (c) => {
  const body = await c.req.parseBody()
  return c.text('pass :)')
})
```

Key options: `maxSize: number` (required, default `100 * 1024` = 100KB), `onError`. On Bun, also set `maxRequestBodySize` in `Bun.serve` if you exceed its 128MiB default.

## Timeout

```ts
import { timeout } from 'hono/timeout'
import { HTTPException } from 'hono/http-exception'
```

Rejects requests that exceed a duration (in milliseconds). Cannot be used with streaming responses — use `stream.close` + `setTimeout` instead.

```ts
app.use('/api', timeout(5000))

app.use('/api/long-process', timeout(60000, (c) =>
  new HTTPException(408, { message: 'Request timeout. Please try again.' })
))
```

## Context Storage

```ts
import { contextStorage, getContext, tryGetContext } from 'hono/context-storage'
```

Stores the Hono `Context` in `AsyncLocalStorage` so it's accessible outside the handler chain. Requires `AsyncLocalStorage` support (on Cloudflare Workers, add `nodejs_compat` flag).

```ts
app.use(contextStorage())

const getMessage = () => getContext().var.message

app.use(async (c, next) => {
  c.set('message', 'Hello!')
  await next()
})

app.get('/', (c) => c.text(getMessage()))
```

`tryGetContext()` returns `undefined` instead of throwing when no context is active.

## Combine

```ts
import { some, every, except } from 'hono/combine'
```

Compose multiple middleware into one. `some` runs the first that passes, `every` runs all (stops on first failure), `except` runs middleware only when a path condition is not met.

```ts
import { some, every } from 'hono/combine'
import { bearerAuth } from 'hono/bearer-auth'
import { ipRestriction } from 'hono/ip-restriction'

app.use('*', some(
  every(
    ipRestriction(getConnInfo, { allowList: ['192.168.0.2'] }),
    bearerAuth({ token }),
  ),
  rateLimit(),
))
```

`except('/api/public/*', bearerAuth({ token }))` skips auth for public paths.

<!--
Source references:
- https://hono.dev/docs/middleware/builtin/cors
- https://hono.dev/docs/middleware/builtin/logger
- https://hono.dev/docs/middleware/builtin/pretty-json
- https://hono.dev/docs/middleware/builtin/request-id
- https://hono.dev/docs/middleware/builtin/etag
- https://hono.dev/docs/middleware/builtin/cache
- https://hono.dev/docs/middleware/builtin/compress
- https://hono.dev/docs/middleware/builtin/timing
- https://hono.dev/docs/middleware/builtin/language
- https://hono.dev/docs/middleware/builtin/trailing-slash
- https://hono.dev/docs/middleware/builtin/method-override
- https://hono.dev/docs/middleware/builtin/method-not-allowed
- https://hono.dev/docs/middleware/builtin/body-limit
- https://hono.dev/docs/middleware/builtin/timeout
- https://hono.dev/docs/middleware/builtin/context-storage
- https://hono.dev/docs/middleware/builtin/combine
-->
