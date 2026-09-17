---
name: core-context
description: The Context object — responses, headers, status, variables, env bindings, and execution context
---

# Context

A `Context` (`c`) is created per request and lives until the response is returned. Read the request via `c.req`, shape the response via `c.body()`/`c.text()`/`c.json()`/`c.html()`, and pass values between middleware via `c.set()`/`c.get()`.

## Status & Headers

```ts
app.post('/posts', (c) => {
  c.status(201)
  c.header('X-Message', 'created')
  return c.text('Created!')
})

// Or pass status + headers inline to any response helper:
app.get('/welcome', (c) =>
  c.body('Thank you', 201, { 'X-Message': 'Hello!', 'Content-Type': 'text/plain' })
)
```

`c.body()` is the lowest-level helper; prefer `c.text()` / `c.html()` / `c.json()` for common content types. Each response helper accepts an optional `(body, status, headers)` signature.

## Response Helpers

```ts
app.get('/text', (c) => c.text('Hello!'))                // text/plain
app.get('/json', (c) => c.json({ message: 'Hello!' }))   // application/json
app.get('/html', (c) => c.html('<h1>Hello!</h1>'))      // text/html
app.get('/raw', () => new Response('Good morning!'))    // raw Response also works
```

### Redirect

Default status is `302`:

```ts
app.get('/redirect', (c) => c.redirect('/'))
app.get('/permanent', (c) => c.redirect('/', 301))
```

### Not Found

```ts
app.get('/missing', (c) => c.notFound())
```

Customize the 404 body globally with `app.notFound()` (see core-exceptions).

### Streaming

For chunked/streamed responses, use the `hono/streaming` helpers rather than buffering a full body:

```ts
import { stream, streamSSE } from 'hono/streaming'

app.get('/stream', (c) =>
  stream(c, async (s) => {
    s.write('chunk 1\n')
    await s.sleep(100)
    s.write('chunk 2\n')
  })
)
```

## Accessing the Response

After `await next()`, mutate the outgoing `Response` via `c.res`:

```ts
app.use('/', async (c, next) => {
  await next()
  c.res.headers.append('X-Debug', 'debug')
})
```

## Variables: set() / get() / var

Per-request key-value storage for passing values between middleware and handlers. Values survive only within the same request.

```ts
const app = new Hono<{ Variables: { message: string } }>()

app.use(async (c, next) => {
  c.set('message', 'Hono is cool')
  await next()
})

app.get('/', (c) => c.text(`The message is ${c.get('message')}`))
```

Access a variable's value as a property via `c.var` (useful for non-scalar values like functions):

```ts
import { createMiddleware } from 'hono/factory'

const echoMiddleware = createMiddleware<{
  Variables: { echo: (s: string) => string }
}>(async (c, next) => {
  c.set('echo', (s) => s)
  await next()
})

app.get('/echo', echoMiddleware, (c) => c.text(c.var.echo('Hello!')))
```

## env (Bindings)

Platform bindings (env vars, secrets, KV namespaces, D1, R2) are available as `c.env`. Type them via the `Bindings` generic:

```ts
const app = new Hono<{ Bindings: { MY_KV: KVNamespace; TOKEN: string } }>()

app.get('/', async (c) => {
  await c.env.MY_KV.put('key', 'value') // typed
  return c.text(c.env.TOKEN)
})
```

## executionCtx (Cloudflare Workers)

Access `ExecutionContext` for `waitUntil` and `exports`:

```ts
app.get('/foo', async (c) => {
  c.executionCtx.waitUntil(c.env.KV.put(key, data))
  return c.text('ok')
})
```

For `FetchEvent` (Service Worker syntax, legacy), use `c.event` — prefer the module-syntax `executionCtx` instead.

## error

If a handler throws, the error lands on `c.error` for inspection in post-`next()` middleware:

```ts
app.use(async (c, next) => {
  await next()
  if (c.error) {
    // log, report, etc.
  }
})
```

## Rendering Layouts

`c.setRenderer()` in middleware defines a layout wrapper; handlers call `c.render(content)` to produce wrapped HTML:

```ts
app.use(async (c, next) => {
  c.setRenderer((content) => c.html(`<html><body><p>${content}</p></body></html>`))
  await next()
})

app.get('/', (c) => c.render('Hello!'))
```

Customize the renderer signature via module augmentation for type-safe extra args:

```ts
declare module 'hono' {
  interface ContextRenderer {
    (content: string | Promise<string>, head: { title: string }): Response | Promise<Response>
  }
}
```

## ContextVariableMap (global typing)

Augment `ContextVariableMap` to type a variable app-wide. **Caution:** this types the variable in *every* handler, even those where the setting middleware never runs — `c.get('result')` will be typed as `string` but be `undefined` at runtime. Prefer the `Variables` generic on `Hono`/`createMiddleware` unless the middleware is guaranteed global.

```ts
declare module 'hono' {
  interface ContextVariableMap {
    result: string
  }
}
```

<!--
Source references:
- https://hono.dev/docs/api/context
-->
