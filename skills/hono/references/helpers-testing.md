---
name: testing
description: Test Hono apps with testClient and app.request() — typed calls and raw requests
---

# Testing

Two approaches: `testClient()` for type-safe RPC-style calls, and `app.request()` for raw `Request`/`Response` testing.

## testClient() — Type-Safe

`testClient(app)` returns a typed client identical to `hc()`, so you get path and input autocompletion inside tests.

**Routes must be chained** for type inference to work — defining routes with separate `app.get(...)` calls after `new Hono()` loses the type chain:

```ts
// index.ts
import { Hono } from 'hono'
const app = new Hono().get('/search', (c) => {
  return c.json({ query: c.req.query('q'), results: ['r1', 'r2'] })
})
export default app
```

```ts
// index.test.ts
import { testClient } from 'hono/testing'
import { describe, it, expect } from 'vitest'
import app from './index'

describe('Search', () => {
  const client = testClient(app)

  it('returns results', async () => {
    const res = await client.search.$get({ query: { q: 'hono' } })
    expect(res.status).toBe(200)
    expect(await res.json()).toEqual({ query: 'hono', results: ['r1', 'r2'] })
  })
})
```

### Headers and Init

Pass headers or a `RequestInit` as the second argument:

```ts
const res = await client.search.$get(
  { query: { q: 'hono' } },
  {
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    init: { signal: controller.signal },
  }
)
```

## app.request() — Raw Requests

`app.request(path, init?, env?)` builds a `Request`, runs it through the app, and returns the `Response`. Useful for assertions on status, headers, and body without the type machinery:

```ts
import { describe, test, expect } from 'vitest'

describe('Posts API', () => {
  test('GET /posts', async () => {
    const res = await app.request('/posts')
    expect(res.status).toBe(200)
    expect(await res.text()).toBe('Many posts')
  })

  test('POST /posts', async () => {
    const res = await app.request('/posts', { method: 'POST' })
    expect(res.status).toBe(201)
    expect(res.headers.get('X-Custom')).toBe('Thank you')
    expect(await res.json()).toEqual({ message: 'Created' })
  })
})
```

### JSON and FormData Bodies

Always set `Content-Type` for JSON bodies (the validator won't parse otherwise):

```ts
const res = await app.request('/posts', {
  method: 'POST',
  body: JSON.stringify({ message: 'hi' }),
  headers: new Headers({ 'Content-Type': 'application/json' }),
})
```

FormData is detected automatically — no `Content-Type` needed:

```ts
const formData = new FormData()
formData.append('message', 'hi')
const res = await app.request('/posts', { method: 'POST', body: formData })
```

### Passing a Request Object

You can also construct a `Request` and pass it directly:

```ts
const req = new Request('http://localhost/posts', { method: 'POST' })
const res = await app.request(req)
```

## Mocking Env and Bindings

Pass a mock `env` (Cloudflare bindings, D1, KV, etc.) as the third argument to `app.request()`:

```ts
const MOCK_ENV = {
  API_HOST: 'example.com',
  DB: { prepare: () => ({ /* mocked D1 */ }) },
}

test('uses mocked D1', async () => {
  const res = await app.request('/posts', {}, MOCK_ENV)
  expect(res.status).toBe(200)
})
```

For Cloudflare Workers, pair with `@cloudflare/vitest-pool-workers` to get a realistic `env` and module isolation.

## Testing Error Responses

Test non-2xx paths by asserting the status and body:

```ts
test('returns 404 for missing post', async () => {
  const res = await app.request('/posts?id=999')
  expect(res.status).toBe(404)
  expect(await res.json()).toEqual({ error: 'not found' })
})
```

## Snapshotting Responses

```ts
test('matches snapshot', async () => {
  const res = await app.request('/posts')
  expect(await res.json()).toMatchSnapshot()
})
```

<!--
Source references:
- https://hono.dev/docs/helpers/testing
- https://hono.dev/docs/guides/testing
-->
