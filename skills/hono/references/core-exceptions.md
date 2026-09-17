---
name: core-exceptions
description: HTTPException, global error handlers, and not-found responses
---

# Error Handling

## Throwing HTTPException

`HTTPException` (from `hono/http-exception`) is the idiomatic way to abort a request with an error response. Throw it from anywhere in a handler or middleware:

```ts
import { HTTPException } from 'hono/http-exception'

app.get('/private', async (c) => {
  if (!c.req.header('Authorization')) {
    throw new HTTPException(401, { message: 'Unauthorized' })
  }
  return c.text('ok')
})
```

### Constructor options

```ts
throw new HTTPException(status, {
  message, // string -> text/plain response body
  res,     // custom Response (status from constructor wins; res headers preserved)
  cause,   // arbitrary attached data, e.g. the original caught error
})
```

Custom response (e.g. JSON body, custom headers):

```ts
const res = new Response(JSON.stringify({ error: 'invalid_token' }), {
  headers: { 'WWW-Authenticate': 'error="invalid_token"' },
})
throw new HTTPException(401, { res })
```

Preserve the underlying cause:

```ts
app.post('/login', async (c) => {
  try {
    await authorize(c)
  } catch (cause) {
    throw new HTTPException(401, { message: 'login failed', cause })
  }
  return c.redirect('/')
})
```

## Global Error Handler

Uncaught errors (including `HTTPException`) flow to `app.onError(err, c)`. Return a `Response`:

```ts
import { HTTPException } from 'hono/http-exception'

app.onError((err, c) => {
  if (err instanceof HTTPException) {
    return err.getResponse() // builds a Response from status + message/res
  }
  console.error(err)
  return c.text('Internal Server Error', 500)
})
```

Return structured JSON for API consistency:

```ts
app.onError((err, c) => {
  const status = err instanceof HTTPException ? err.status : 500
  console.error(err)
  return c.json({ error: err.message, status }, status)
})
```

> `err.getResponse()` is not Context-aware — headers set on `c` before the throw won't be on that response. Re-apply them or build a fresh `Response` via `c.json()`/`c.text()` if you need context headers.

### Route-level priority

If both a parent app and a mounted subapp define `onError`, the route-level (inner) handler takes priority.

## Not Found

Customize 404 with `app.notFound()`:

```ts
app.notFound((c) => c.json({ error: 'Not Found' }, 404))
```

Call `c.notFound()` from a handler to trigger it explicitly:

```ts
app.get('/users/:id', async (c) => {
  const user = await findUser(c.req.param('id'))
  if (!user) return c.notFound()
  return c.json(user)
})
```

> `app.notFound()` only fires from the top-level app; a `notFound` set on a subapp won't run for unmatched routes in the parent.

## Inspecting Errors in Middleware

After `await next()`, check `c.error` to observe whether a handler threw — useful for logging/metrics without overriding the response:

```ts
app.use(async (c, next) => {
  await next()
  if (c.error) console.error('handler failed:', c.error)
})
```

## Recommended Patterns

- **Throw `HTTPException`** for expected HTTP errors (auth, validation, not-found) — it carries a status and a ready response.
- **Use `app.onError`** as a catch-all for unexpected errors; log and return a generic 500, and map `HTTPException` to its response.
- **Don't wrap `next()` in try/catch** — Hono already catches thrown errors and routes them to `onError`; `next()` won't throw.
- **Avoid RoR-style controllers** that take a bare `Context` — path params lose literal-type inference. Define handlers inline on routes, or use `createFactory().createHandlers(...)` to preserve types.

<!--
Source references:
- https://hono.dev/docs/api/exception
- https://hono.dev/docs/api/hono
- https://hono.dev/docs/guides/best-practices
-->
