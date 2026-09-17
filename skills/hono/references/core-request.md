---
name: core-request
description: Reading the request via c.req — params, query, headers, cookies, and body parsing
---

# Request

`c.req` wraps the Web `Request`. Read path params, query, headers, and the body through it.

## Path Parameters

```ts
app.get('/entry/:id', (c) => c.text(c.req.param('id')))

app.get('/entry/:id/comment/:commentId', (c) => {
  const { id, commentId } = c.req.param() // all params at once
  return c.json({ id, commentId })
})
```

When a route is defined inline, `c.req.param('id')` is inferred as a literal type — no manual generics needed.

## Query Parameters

```ts
app.get('/search', (c) => c.text(c.req.query('q') ?? ''))

app.get('/search', (c) => {
  const { q, limit, offset } = c.req.query()
  return c.json({ q, limit, offset })
})
```

For repeated keys (`?tags=A&tags=B`) use `queries()`, which returns `string[]`:

```ts
app.get('/search', (c) => c.json(c.req.queries('tags')))
```

## Headers

```ts
app.get('/', (c) => c.text(c.req.header('User-Agent') ?? 'unknown'))
```

`c.req.header()` with no argument returns all headers as a record, but keys are **lowercased** — always fetch specific headers by name with `c.req.header('X-Foo')` rather than indexing the record with mixed-case keys.

## Body Parsing

| Method | Content type | Returns |
|--------|--------------|---------|
| `c.req.json()` | `application/json` | parsed JSON |
| `c.req.text()` | `text/plain` | `string` |
| `c.req.parseBody()` | form/multipart | `Record<string, string \| File>` |
| `c.req.formData()` | multipart | `FormData` |
| `c.req.arrayBuffer()` | any | `ArrayBuffer` |
| `c.req.blob()` | any | `Blob` |

```ts
app.post('/entry', async (c) => {
  const body = await c.req.json<{ title: string }>()
  return c.json({ got: body.title })
})
```

### parseBody specifics

A single file field returns `string | File`; multiple uploads use the `[]` postfix and return arrays:

```ts
const body = await c.req.parseBody()
const file = body['avatar']     // string | File
const files = body['photos[]']  // (string | File)[]
```

Handle multiple values with the same name via `{ all: true }`; structure dotted keys (`obj.key`) into nested objects via `{ dot: true }`:

```ts
const body = await c.req.parseBody({ all: true })
const nested = await c.req.parseBody({ dot: true })
// nested.obj.key1 === 'value1'
```

## Cookies

```ts
app.get('/', (c) => c.text(c.req.cookie('session') ?? 'none'))
app.get('/all', (c) => c.json(c.req.cookies()))
```

`c.req.cookie(name)` returns `string | undefined`; `c.req.cookies()` returns all cookies as a `Record<string, string>`.

## Request Metadata

```ts
app.get('/about/me', (c) => c.json({
  method: c.req.method, // 'GET'
  path:   c.req.path,   // '/about/me'
  url:    c.req.url,    // full URL string
}))
```

## Raw Request

`c.req.raw` exposes the underlying `Request` for platform-specific fields (e.g. Cloudflare's `cf`):

```ts
app.post('/', (c) => {
  const cf = c.req.raw.cf
  // ...
})
```

If a validator or body method already consumed the body, use `cloneRawRequest()` to re-read it:

```ts
import { cloneRawRequest } from 'hono/request'
import { validator } from 'hono/validator'

app.post('/forward', validator('json', (d) => d), async (c) => {
  const cloned = await cloneRawRequest(c.req)
  await cloned.json() // works even after validation
})
```

## Validated Data

After a validator runs, access parsed/validated input via `c.req.valid('target')`:

```ts
app.post('/posts', (c) => {
  const { title, body } = c.req.valid('form')
  // targets: 'form' | 'json' | 'query' | 'header' | 'cookie' | 'param'
})
```

<!--
Source references:
- https://hono.dev/docs/api/request
- https://hono.dev/docs/api/routing
-->
