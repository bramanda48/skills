---
name: rpc
description: Type-safe RPC with hc() — share route types between server and client
---

# RPC

Hono's RPC feature lets a client share your server's API spec through types alone. The client gets full autocompletion for paths, methods, inputs, and response shapes — no code generation step required.

## Server Setup

Assign the chained route to a variable and export its `typeof` as `AppType`. Response types are inferred from `c.json()` return values, and input types from any `validator()` or `zValidator()` middleware:

```ts
import { Hono } from 'hono'
import { zValidator } from '@hono/zod-validator'
import { z } from 'zod'

const route = app.post(
  '/posts',
  zValidator('form', z.object({ title: z.string(), body: z.string() })),
  (c) => {
    return c.json({ ok: true, message: 'Created!' }, 201)
  }
)

export type AppType = typeof route
```

For type inference to work in monorepos, set `"strict": true` in both client and server `tsconfig.json`.

## Client Usage

```ts
import { hc } from 'hono/client'
import type { AppType } from './server'

const client = hc<AppType>('http://localhost:8787/')

const res = await client.posts.$post({
  form: { title: 'Hello', body: 'Hono is cool' },
})

if (res.ok) {
  const data = await res.json() // { ok: boolean, message: string } — fully typed
}
```

The response is a standard fetch `Response`; call `.json()` to get typed data. Method calls are prefixed with `$` (`$get`, `$post`) to avoid clashing with reserved names.

## Path Parameters

Access dynamic segments via bracket notation. Params and query values are always **strings**, even if the server coerces them to numbers via the validator:

```ts
const res = await client.posts[':id'].$get({
  param: { id: '123' },
  query: { page: '1' },
})
```

Multiple params stack: `client.posts[':postId'][':authorId'].$get({ param: { postId: '1', authorId: '2' } })`.

## Status-Code-Typed Responses

Explicitly pass a status code to `c.json()` to make it a discriminable branch on the client:

```ts
// server
.get('/posts', async (c) => {
  const post = await getPost(c.req.query('id')!)
  if (!post) return c.json({ error: 'not found' }, 404)
  return c.json({ post }, 200)
})
```

```ts
// client
const res = await client.posts.$get({ query: { id: '1' } })

if (res.status === 404) {
  const data: { error: string } = await res.json()
}
if (res.ok) {
  const data: { post: Post } = await res.json()
}

type AllResponses = InferResponseType<typeof client.posts.$get>     // { post } | { error }
type OkOnly      = InferResponseType<typeof client.posts.$get, 200> // { post }
```

Avoid `c.notFound()` for typed routes — it returns `unknown` to the client. Use `c.json(..., 404)` instead, or augment the `NotFoundResponse` interface.

## Nesting Apps with app.route

Chain `.route()` calls and export the final type so all sub-routes are included:

```ts
const app = new Hono()
  .route('/authors', authorsApp)
  .route('/books', booksApp)

export type AppType = typeof app
```

Each sub-app should chain its handlers (`.get('/').post('/')`) so types propagate upward.

## Headers, Init, and Cookies

Per-request headers go in the second argument:

```ts
await client.search.$get({}, { headers: { 'X-Custom': 'value' } })
```

Shared defaults go on the client constructor. Use `credentials: 'include'` for cookies:

```ts
const client = hc<AppType>('/', {
  headers: { Authorization: 'Bearer TOKEN' },
  init: { credentials: 'include' },
})
```

Pass a `RequestInit` via `init` (e.g. an `AbortSignal`). `init` takes the highest priority and can override other options.

## $url() and $path()

Get a `URL` or path string for a route (requires an absolute base URL for `$url`):

```ts
const url = client.api.posts[':id'].$url({ param: { id: '1' } }) // URL
const path = client.api.posts.$path({ query: { page: '1' } })     // "/api/posts?page=1"
```

## Custom fetch and Query Serialization

Override `fetch` (useful for Cloudflare Service Bindings) or customize array serialization:

```ts
const client = hc<AppType>('http://localhost', {
  fetch: c.env.AUTH.fetch.bind(c.env.AUTH),
  buildSearchParams: (query) => {
    const sp = new URLSearchParams()
    for (const [k, v] of Object.entries(query)) {
      if (Array.isArray(v)) v.forEach((item) => sp.append(`${k}[]`, item))
      else sp.set(k, v as string)
    }
    return sp
  },
})
```

## Inferring Types and Parsing

```ts
import type { InferRequestType, InferResponseType } from 'hono/client'
import { parseResponse, DetailedError } from 'hono/client'

type ReqType = InferRequestType<typeof client.todo.$post>['form']
type ResType = InferResponseType<typeof client.todo.$post>

const result = await parseResponse(client.hello.$get()).catch(
  (e: DetailedError) => console.error(e)
)
```

`parseResponse` throws on non-ok responses and auto-parses based on `Content-Type`.

## Global Error Responses

RPC doesn't infer types from `app.onError()` or global middleware. Merge them with `ApplyGlobalResponse`:

```ts
import type { ApplyGlobalResponse } from 'hono/client'

type AppWithErrors = ApplyGlobalResponse<typeof app, {
  401: { json: { error: string } }
  500: { json: { error: string } }
}>
```

## Performance Tips for Large Apps

- **Compile first**: build a pre-typed client with `hc<typeof app>('')`, export its type, and use a typed `hcWithType()` wrapper so `tsserver` skips re-instantiating every route on each keystroke.
- **Match Hono versions** across backend and frontend, or you'll hit "type instantiation excessively deep" errors.
- **Use project references** so the frontend can import `AppType` from the backend.
- **Split apps**: create a separate client per sub-app (`hc<typeof authorsApp>('/authors')`).
- **Avoid `.then()` chains** in handlers — they break response inference. Use `async`/`await` or annotate the `.then()` return with `TypedResponse`.

<!--
Source references:
- https://hono.dev/docs/guides/rpc
-->
