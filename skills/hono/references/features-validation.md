---
name: validation
description: Validate request body, query, params, headers, and cookies with the validator() middleware
---

# Validation

Hono ships a thin `validator()` middleware for inspecting and transforming incoming request data. It runs before your handler, lets you return a custom error response on failure, and exposes the typed result via `c.req.valid()`.

## Manual Validator

`validator()` takes a target and a callback. Return the validated/transformed value from the callback; return a `Response` to short-circuit on error.

```ts
import { Hono } from 'hono'
import { validator } from 'hono/validator'

const app = new Hono()

app.post(
  '/posts',
  validator('form', (value, c) => {
    const body = value['body']
    if (!body || typeof body !== 'string') {
      return c.text('Invalid!', 400)
    }
    return { body }
  }),
  (c) => {
    const { body } = c.req.valid('form')
    return c.json({ message: 'Created!' }, 201)
  }
)
```

### Validation Targets

| Target | Access in callback | Retrieve in handler |
|--------|-------------------|---------------------|
| `json` | `value` is parsed JSON body | `c.req.valid('json')` |
| `form` | `value` is parsed form fields | `c.req.valid('form')` |
| `formData` | `value` is `FormData` | `c.req.valid('formData')` |
| `query` | `value` is query params | `c.req.valid('query')` |
| `param` | `value` is route params | `c.req.valid('param')` |
| `header` | `value` is headers (lowercase keys) | `c.req.valid('header')` |
| `cookie` | `value` is cookies | `c.req.valid('cookie')` |

## Multiple Validators

Stack validators to validate several request parts in one route:

```ts
app.post(
  '/posts/:id',
  validator('param', (value, c) => {
    if (!/^\d+$/.test(value.id)) return c.text('Invalid id', 400)
    return { id: Number(value.id) }
  }),
  validator('query', (value, c) => {
    return { page: value.page ? Number(value.page) : 1 }
  }),
  validator('json', (value, c) => {
    if (!value.title) return c.text('title required', 400)
    return { title: String(value.title) }
  }),
  (c) => {
    const { id } = c.req.valid('param')
    const { page } = c.req.valid('query')
    const { title } = c.req.valid('json')
    return c.json({ id, page, title })
  }
)
```

## Content-Type Requirement

When validating `json` or `form`, the request **must** carry a matching `Content-Type` header. Without it the body is not parsed and the callback receives `{}`. Set the header explicitly when testing via `app.request()`:

```ts
const res = await app.request('/posts', {
  method: 'POST',
  body: JSON.stringify({ title: 'Hi' }),
  headers: new Headers({ 'Content-Type': 'application/json' }),
})
```

## Header Keys Must Be Lowercase

Headers are accessed with lowercase keys. `value['Idempotency-Key']` returns `undefined`; use `value['idempotency-key']`.

## Using a Schema Library (Zod / Valibot / ArkType)

Hono's built-in `validator()` only hands you raw values. For real schema validation, use a third-party `@hono/*` validator package. These are **separate packages**, not part of `hono` core — see the hono-third-party skill for the full list.

The most common is `@hono/zod-validator`:

```ts
import { Hono } from 'hono'
import { zValidator } from '@hono/zod-validator'
import { z } from 'zod'

const app = new Hono()

app.post(
  '/posts',
  zValidator('form', z.object({ body: z.string() })),
  (c) => {
    const { body } = c.req.valid('form')
    return c.json({ body }, 201)
  }
)
```

For library-agnostic validation, `@hono/standard-validator` accepts any [Standard Schema](https://standardschema.dev/) compatible library (Zod, Valibot, ArkType):

```ts
import { sValidator } from '@hono/standard-validator'
import * as v from 'valibot'

app.post(
  '/author',
  sValidator('json', v.object({ name: v.string(), age: v.number() })),
  (c) => {
    const data = c.req.valid('json')
    return c.json({ message: `${data.name} is ${data.age}` })
  }
)
```

Using a schema validator is preferred over manual validation: the validated data is fully typed, error responses are consistent, and the types flow through to RPC clients.

## Error Response Hook

The validator callback receives `(value, c)`. Return any `Response` from the callback to reject the request before the handler runs. This gives you full control over the error shape — there is no built-in error format to configure.

<!--
Source references:
- https://hono.dev/docs/guides/validation
-->
