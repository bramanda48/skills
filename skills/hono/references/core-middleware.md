---
name: core-middleware
description: Writing and composing middleware, execution order, path scoping, and short-circuiting
---

# Middleware

Middleware wraps handlers in an "onion": it runs before `await next()` (downstream) and after (upstream). A **handler** returns a `Response` and only one runs; **middleware** calls `await next()` to continue, or returns a `Response` to short-circuit.

## Registering Middleware

```ts
import { Hono } from 'hono'
import { logger } from 'hono/logger'
import { cors } from 'hono/cors'
import { basicAuth } from 'hono/basic-auth'

const app = new Hono()

app.use(logger())                              // all methods, all paths
app.use('/posts/*', cors())                    // path-scoped
app.post('/posts/*', basicAuth({               // method + path
  username: 'u',
  password: 'p',
}))
```

`app.use([path], ...mw)` applies to every method; `app.METHOD(path, ...mw)` scopes to a method. Multiple middleware and a handler can be passed positionally.

## Execution Order

Order follows registration — first registered runs first on the way down, last on the way up:

```ts
app.use(async (c, next) => { console.log('1 start'); await next(); console.log('1 end') })
app.use(async (c, next) => { console.log('2 start'); await next(); console.log('2 end') })
app.get('/', (c) => { console.log('handler'); return c.text('Hello!') })
```

Output:

```
1 start -> 2 start -> handler -> 2 end -> 1 end
```

Hono catches thrown errors and routes them to `app.onError()` (or a 500), so `next()` never throws — no try/catch is needed around it.

## Custom Middleware

Inline:

```ts
// Log + add a header after the handler runs
app.use(async (c, next) => {
  console.log(`[${c.req.method}] ${c.req.url}`)
  await next()
  c.header('x-message', 'from middleware')
})
```

For reusable, type-safe middleware, use `createMiddleware()` from `hono/factory`:

```ts
import { createMiddleware } from 'hono/factory'

const logger = createMiddleware(async (c, next) => {
  console.log(`[${c.req.method}] ${c.req.url}`)
  await next()
})
```

## Short-Circuiting

Return a `Response` instead of calling `next()` to stop the chain early (e.g. auth failure):

```ts
app.use('/admin/*', async (c, next) => {
  if (!isAuthorized(c)) return c.text('Forbidden', 403)
  await next()
})
```

## Modifying the Response After next

Mutate `c.res` after `await next()` to rewrite headers or replace the body:

```ts
app.use(async (c, next) => {
  const start = performance.now()
  await next()
  c.res.headers.set('X-Response-Time', `${performance.now() - start}`)
})

// Replace the response entirely:
const replace = createMiddleware(async (c, next) => {
  await next()
  c.res = new Response('New Response')
})
```

## Extending Context with Variables

Set typed values for downstream handlers via `c.set()`; declare them with the `Variables` generic on `createMiddleware`:

```ts
const echoMiddleware = createMiddleware<{
  Variables: { echo: (s: string) => string }
}>(async (c, next) => {
  c.set('echo', (s) => s)
  await next()
})

app.get('/echo', echoMiddleware, (c) => c.text(c.var.echo('Hello!')))
```

### Chained Type Accumulation

`.use()` returns a new `Hono` with merged `Variables` types, so chaining accumulates types without a combined `Env` upfront:

```ts
const app = new Hono()
  .use(authMiddleware) // provides Variables.user
  .use(dbMiddleware)   // provides Variables.db
  .get('/', (c) => c.json({ user: c.var.user, db: c.var.db })) // both typed
```

## Accessing Context Inside Middleware Args

To read `c.env` when constructing middleware options, inline the call so `c` is in scope:

```ts
app.use('*', async (c, next) => {
  const mw = cors({ origin: c.env.CORS_ORIGIN })
  return mw(c, next)
})
```

## Built-in & Third-party

Built-ins (no external deps) are imported via subpaths: `logger` (`hono/logger`), `cors` (`hono/cors`), `basicAuth`/`bearerAuth`/`jwt` (`hono/basic-auth`, `hono/bearer-auth`, `hono/jwt`), `etag`, `compress`, `prettyJson`, `secureHeaders`, `cache`, `poweredBy`. Third-party packages add GraphQL Server, Sentry, Firebase Auth, etc.

<!--
Source references:
- https://hono.dev/docs/concepts/middleware
- https://hono.dev/docs/guides/middleware
- https://hono.dev/docs/api/hono
-->
