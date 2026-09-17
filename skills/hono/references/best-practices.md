---
name: best-practices
description: Project structure, error handling, testing, performance, and TypeScript discipline for Hono apps
---

# Best Practices

Patterns for structuring, testing, and optimizing Hono applications.

## Project Structure & Route Organization

### Write handlers inline — avoid "controllers"

Path parameters are inferred only when the handler is defined directly on the route. Extracting handlers into separate functions breaks type inference for params.

```ts
// Correct — `id` is inferred as a string literal type
app.get('/books/:id', (c) => {
  const id = c.req.param('id')
  return c.json(`get ${id}`)
})
```

### Compose larger apps with `app.route()`

Split routes into separate files, each exporting its own `Hono` instance, then mount them.

```ts
// books.ts
import { Hono } from 'hono'
const app = new Hono()
app.get('/', (c) => c.json('list books'))
app.get('/:id', (c) => c.json(`get ${c.req.param('id')}`))
export default app

// index.ts
import { Hono } from 'hono'
import books from './books'

const app = new Hono()
app.route('/books', books)
export default app
```

### Use `createFactory` for reusable handlers/middleware

When you need to extract handlers, use `hono/factory` so types stay correct:

```ts
import { createFactory } from 'hono/factory'

const factory = createFactory()
const handlers = factory.createHandlers(
  logger(),
  (c) => c.json(c.get('foo'))
)
app.get('/api', ...handlers)
```

### RPC with larger apps

Chain `.get()/.post()` calls and export the type for typed client inference:

```ts
// authors.ts
const app = new Hono()
  .get('/', (c) => c.json('list authors'))
  .get('/:id', (c) => c.json(`get ${c.req.param('id')}`))

export default app
export type AppType = typeof app

// client.ts
import { hc } from 'hono/client'
import type { AppType } from './authors'
const client = hc<AppType>('http://localhost')
```

## Error Handling

### `app.onError()` — global error handler

Hono catches thrown errors and passes them to `onError` (or returns a 500). `next()` never throws, so no try/catch is needed around it.

```ts
app.onError((err, c) => {
  console.error(err)
  return c.text('Internal Server Error', 500)
})
```

### `HTTPException` — structured error responses

Throw `HTTPException` with a status code and message or custom response. Handle it centrally in `onError`:

```ts
import { HTTPException } from 'hono/http-exception'

app.post('/login', async (c) => {
  if (!authorized) {
    throw new HTTPException(401, { message: 'Unauthorized' })
  }
  return c.redirect('/')
})

app.onError((err, c) => {
  if (err instanceof HTTPException) {
    return err.getResponse()
  }
  console.error(err)
  return c.text('Internal Server Error', 500)
})
```

For non-text responses, use `res` option: `throw new HTTPException(401, { res: new Response(...) })`. Attach metadata with `cause`. Note: `getResponse()` is not context-aware — reapply any headers set on `c` to a new `Response`.

## Testing

Use `app.request()` to make in-process requests and assert on the `Response`. No HTTP server needed.

```ts
describe('Example', () => {
  test('GET /posts', async () => {
    const res = await app.request('/posts')
    expect(res.status).toBe(200)
    expect(await res.text()).toBe('Many posts')
  })

  test('POST /posts with JSON', async () => {
    const res = await app.request('/posts', {
      method: 'POST',
      body: JSON.stringify({ message: 'hello' }),
      headers: new Headers({ 'Content-Type': 'application/json' }),
    })
    expect(res.status).toBe(201)
  })
})
```

Pass mock bindings/env as the third argument: `app.request('/posts', {}, MOCK_ENV)`.

## Performance

### Choose the right router

- **`hono` (default)** — SmartRouter with RegExpRouter + TrieRouter. Best for long-running servers (Node.js, Bun, Deno, persistent isolates). Registration is slower but request dispatch is fastest.
- **`hono/quick`** — SmartRouter with LinearRouter + TrieRouter. Best when the app initializes on every request.
- **`hono/tiny`** — PatternRouter only. Under 14KB, for resource-constrained edge environments.

RegExpRouter is the fastest router in the JS world because it compiles all routes into one large regex and matches in a single pass. SmartRouter auto-selects the fastest router at startup.

### Use streaming responses for large data

```ts
import { streamText } from 'hono/streaming'

app.get('/stream', (c) =>
  streamText(c, async (stream) => {
    for (let i = 0; i < 100; i++) {
      await stream.writeln(`line ${i}`)
      await stream.sleep(100)
    }
  })
)
```

Note: streaming callbacks do not trigger `onError` — handle errors inside the callback.

### Cache responses

Use the `cache` middleware on runtimes that support the Cache API (Cloudflare Workers, Deno):

```ts
app.get('*', cache({ cacheName: 'my-app', cacheControl: 'max-age=3600' }))
```

## TypeScript Discipline

### Type `Bindings` and `Variables`

Pass type definitions as generics to `Hono` for full type safety:

```ts
type Bindings = {
  DB: D1Database
  API_KEY: string
}

type Variables = {
  user: User
}

const app = new Hono<{ Bindings: Bindings; Variables: Variables }>()

app.get('/', (c) => {
  // c.env.DB is typed as D1Database
  // c.get('user') is typed as User
})
```

For middleware-specific variables, import the provided `*Variables` types (e.g. `JwtVariables`, `TimingVariables`, `RequestIdVariables`, `SecureHeadersVariables`) and add them to the `Variables` generic.

## Security Checklist

- Use `secureHeaders()` for baseline security headers (HSTS, CSP, X-Frame-Options).
- Use `csrf()` for form-based CSRF protection on unsafe methods.
- Use `basicAuth`, `bearerAuth`, or `jwt`/`jwk` for authentication.
- Use `bodyLimit()` to cap request body sizes and prevent abuse.
- Use `ipRestriction()` for IP-based access control (requires `getConnInfo`).
- Use `timeout()` to prevent long-running requests from hanging.
- Type all `Bindings` to avoid accidentally exposing or mishandling secrets.

<!--
Source references:
- https://hono.dev/docs/guides/best-practices
- https://hono.dev/docs/guides/testing
- https://hono.dev/docs/concepts/developer-experience
- https://hono.dev/docs/concepts/benchmarks
-->
