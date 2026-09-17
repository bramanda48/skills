---
name: factory
description: Share middleware, handlers, and Env types across apps with createFactory and createMiddleware
---

# Factory and Route Helpers

## createFactory()

`createFactory()` centralizes your `Env` type and app options so middleware and apps share one definition. Pass `Env` as a generic to type `c.var`, `c.env`, and bindings in one place:

```ts
import { createFactory, createMiddleware } from 'hono/factory'

type Env = {
  Variables: { user: string }
  Bindings: { DB: D1Database }
}

const factory = createFactory<Env>()

const app = factory.createApp() // Env inferred — no need to repeat `new Hono<Env>()`

const authMiddleware = factory.createMiddleware(async (c, next) => {
  c.set('user', 'anthony') // c.var.user is typed
  await next()
})
```

### initApp Option

Run setup middleware on every app created by the factory — useful for injecting a DB client derived from a binding:

```ts
export default createFactory<{
  Bindings: { MY_DB: D1Database }
  Variables: { db: DrizzleD1Database }
}>({
  initApp: (app) => {
    app.use(async (c, next) => {
      c.set('db', drizzle(c.env.MY_DB))
      await next()
    })
  },
})
```

```ts
// another file
import factoryWithDB from './factory-with-db'

const app = factoryWithDB.createApp()
app.post('/posts', (c) => {
  c.var.db.insert() // typed
  return c.json({ ok: true })
})
```

### defaultAppOptions

```ts
const factory = createFactory({ defaultAppOptions: { strict: false } })
const app = factory.createApp() // strict: false applied
```

## createMiddleware()

Standalone shortcut for `factory.createMiddleware()`. Useful when you don't need a shared factory:

```ts
import { createMiddleware } from 'hono/factory'

const addHeader = createMiddleware(async (c, next) => {
  await next()
  c.res.headers.set('X-Message', 'Hello!')
})

app.use(addHeader)
```

### Parameterized Middleware

Wrap in a function to accept arguments:

```ts
const messageMiddleware = (message: string) =>
  createMiddleware(async (c, next) => {
    await next()
    c.res.headers.set('X-Message', message)
  })

app.use(messageMiddleware('Good evening!'))
```

## createHandlers()

Define a handler chain separately from the route, so handlers can be reused or tested in isolation:

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

## Mounting Sub-Apps with app.route

`app.route(path, subApp)` mounts a Hono instance at a prefix. Chain `.route()` calls and export the combined type for RPC:

```ts
const app = new Hono()
  .route('/authors', authorsApp)
  .route('/books', booksApp)

export type AppType = typeof app
```

## Route Helper — Inspection at Runtime

`hono/route` exposes functions for inspecting matched routes inside a handler or middleware. Useful for logging, debugging, and conditional middleware:

```ts
import { matchedRoutes, routePath, baseRoutePath, basePath } from 'hono/route'

app.get('/posts/:id', (c) => {
  routePath(c)      // '/posts/:id' — registered pattern
  matchedRoutes(c)  // [{ method, path, handler }, ...] including middleware
  return c.json({ path: routePath(c) })
})
```

### With Mounted Sub-Apps

```ts
const apiApp = new Hono()
apiApp.get('/posts/:id', (c) => ({
  routePath: routePath(c),       // '/posts/:id'
  baseRoutePath: baseRoutePath(c), // '/api'
  basePath: basePath(c),          // '/api' (with actual params)
}))
app.route('/api', apiApp)
```

Both `routePath()` and `baseRoutePath()` accept an index for `Array.prototype.at()`-style access: `routePath(c, 0)` is the first matched route, `routePath(c, -1)` the last.

<!--
Source references:
- https://hono.dev/docs/helpers/factory
- https://hono.dev/docs/helpers/route
-->
