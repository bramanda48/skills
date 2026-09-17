---
name: features-types
description: Typing Hono apps — Env generics for Bindings and Variables, typed context, and path-param inference
---

# Typing

Hono is written in TypeScript and infers types from route definitions. Path params, validated bodies, and context variables are typed without runtime overhead.

## The Env Generic

`Hono` accepts an `Env` generic with two fields: `Bindings` (platform env/KV/D1) and `Variables` (per-request values set via `c.set`). Both are optional; pass what you need.

```ts
import { Hono } from 'hono'

type Bindings = {
  TOKEN: string
  DB: D1Database
}

type Variables = {
  user: { id: string; name: string }
}

const app = new Hono<{ Bindings: Bindings; Variables: Variables }>()
```

### Typing c.env

`c.env` is typed from `Bindings`:

```ts
app.use('/auth/*', async (c, next) => {
  const token = c.env.TOKEN // string
  c.set('user', { id: '1', name: 'Alice' }) // typed as Variables['user']
  await next()
})

app.get('/me', (c) => c.json(c.get('user'))) // { id: string; name: string }
```

`c.set()`/`c.get()` are typed from `Variables`; `c.var` exposes the same values as properties (handy for non-scalar values).

## Path Parameter Inference

When a route is defined inline, path params become literal types — `c.req.param('id')` is `string` and the key is known:

```ts
app.get('/user/:name', (c) => {
  const name = c.req.param('name') // typed, key known
  return c.text(name)
})

app.get('/posts/:id/comment/:comment_id', (c) => {
  const { id, comment_id } = c.req.param() // both keys known
  return c.json({ id, comment_id })
})
```

This is why inline handlers are preferred over extracted "controller" functions that take a bare `Context` — the latter lose the route's param types. To pin types when the path is dynamic, pass the path as an explicit generic: `app.get<'/users/:id'>('/users/:id', handler)`.

## Typed Middleware

`createMiddleware` accepts the same `Env` generic so a middleware can declare the `Variables` it provides:

```ts
import { createMiddleware } from 'hono/factory'

const authMiddleware = createMiddleware<{
  Variables: { user: { id: string; name: string } }
}>(async (c, next) => {
  c.set('user', { id: '123', name: 'Alice' })
  await next()
})
```

### Chaining accumulates types

Each `.use()` returns a `Hono` with merged `Variables`, so downstream handlers see every variable type-safely without a combined `Env`:

```ts
const app = new Hono()
  .use(authMiddleware) // provides Variables.user
  .use(dbMiddleware)   // provides Variables.db
  .get('/', (c) => c.json({
    user: c.var.user, // typed
    db: c.var.db,     // typed
  }))
```

## Reusable Handlers with createHandlers

To extract handlers/middleware into arrays while preserving inference, use `createFactory().createHandlers(...)`:

```ts
import { createFactory } from 'hono/factory'
import { logger } from 'hono/logger'

const factory = createFactory()

const mw = factory.createMiddleware(async (c, next) => {
  c.set('foo', 'bar')
  await next()
})

const handlers = factory.createHandlers(logger(), mw, (c) => c.json(c.var.foo))
app.get('/api', ...handlers)
```

## Global Variable Typing (ContextVariableMap)

Augment `ContextVariableMap` to type a variable app-wide. **Caution:** this marks the variable as present in *every* handler, even ones where the setting middleware never runs — you get `string` typing on a value that is `undefined` at runtime. Only use it for variables set by app-wide middleware guaranteed to run.

```ts
declare module 'hono' {
  interface ContextVariableMap {
    result: string
  }
}

const mw = createMiddleware(async (c, next) => {
  c.set('result', 'value')
  await next()
})

app.get('/foo', mw, (c) => c.get('result')) // string (correct)
app.get('/bar', (c) => c.get('result'))      // string, but undefined at runtime!
```

Prefer the `Variables` generic on `Hono`/`createMiddleware` for anything scoped.

## Custom Context Renderer

Type a `c.render()` layout signature by augmenting `ContextRenderer`:

```ts
declare module 'hono' {
  interface ContextRenderer {
    (content: string | Promise<string>, head: { title: string }): Response | Promise<Response>
  }
}
```

<!--
Source references:
- https://hono.dev/docs/api/context
- https://hono.dev/docs/api/hono
- https://hono.dev/docs/api/routing
-->
