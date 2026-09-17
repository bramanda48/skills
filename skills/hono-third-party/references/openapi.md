---
name: openapi
description: OpenAPI / Swagger tooling for Hono (Swagger UI, Swagger Editor, Zod OpenAPI)
---

# OpenAPI & Swagger

## Swagger UI

```bash
npm i @hono/swagger-ui
```

Serves [Swagger UI](https://swagger.io/tools/swagger-ui/) on a Hono route, pointing at an OpenAPI definition URL.

```ts
import { Hono } from 'hono'
import { swaggerUI } from '@hono/swagger-ui'

const app = new Hono()

app.get('/ui', swaggerUI({ url: '/doc' }))
```

Also exports a `SwaggerUI` component for `hono/html` layouts. Options: `version` (Swagger UI version, default `latest`), `manuallySwaggerUIHtml` (custom HTML; overrides other options), plus standard Swagger UI config (`url`, `urls`, `presets`, `plugins`). Pair with `@hono/zod-openapi`'s `app.doc('/doc', {...})` to generate the definition served at `url`.

## Swagger Editor

```bash
npm i @hono/swagger-editor
```

Serves [Swagger Editor](https://swagger.io/tools/swagger-editor/) on a Hono route.

```ts
import { Hono } from 'hono'
import { swaggerEditor } from '@hono/swagger-editor'

const app = new Hono()

app.get('/swagger-editor', swaggerEditor({ url: '/doc' }))
```

Supports almost all swagger-editor options (see swagger.io docs). The `url` points at the OpenAPI definition to edit.

## Zod OpenAPI

```bash
npm i hono zod @hono/zod-openapi
```

An extended `Hono` class (`OpenAPIHono`) that validates with Zod and generates OpenAPI/Swagger docs, based on [Zod to OpenAPI](https://github.com/asteasolutions/zod-to-openapi). Import `z` and `createRoute` from `@hono/zod-openapi`.

```ts
import { OpenAPIHono, createRoute, z } from '@hono/zod-openapi'
import { swaggerUI } from '@hono/swagger-ui'

const ParamsSchema = z.object({
  id: z.string().min(3).openapi({ param: { name: 'id', in: 'path' }, example: '1212121' }),
})
const UserSchema = z.object({
  id: z.string().openapi({ example: '123' }),
  name: z.string().openapi({ example: 'John Doe' }),
  age: z.number().openapi({ example: 42 }),
}).openapi('User') // registers as #/components/schemas/User

const route = createRoute({
  method: 'get',
  path: '/users/{id}',
  request: { params: ParamsSchema },
  responses: {
    200: { content: { 'application/json': { schema: UserSchema } }, description: 'Retrieve the user' },
  },
})

const app = new OpenAPIHono()

app.openapi(route, (c) => {
  const { id } = c.req.valid('param')
  return c.json({ id, age: 20, name: 'Ultra-man' }, 200) // status code required even for 200
})

app.doc('/doc', { openapi: '3.0.0', info: { version: '1.0.0', title: 'My API' } })       // v3.0
// app.doc31('/docs', { openapi: '3.1.0', info: { title: 'foo', version: '1' } })          // v3.1

app.get('/ui', swaggerUI({ url: '/doc' }))
```

Key APIs: `app.openapi(route, handler, hook?)` registers a route (validated data via `c.req.valid('json'/'param'/'query'/'header')`). `app.openAPIRegistry` accesses the registry (`registerComponent('schemas'/'securitySchemes', ...)`, `registerComponent` for `securitySchemes` to wire Bearer auth: `{ type: 'http', scheme: 'bearer' }` then `security: [{ Bearer: [] }]` on the route). `defaultHook` on the constructor centralizes validation-error formatting. `defineOpenAPIRoute`/`openapiRoutes([...])` register routes in batch with type safety; `addRoute` flag enables conditional routes. RPC mode: chain `.openapi()` calls and pass to `hc<typeof routes>`. Header keys in schemas must be lowercase. `hide: true` on a route excludes it from docs. Use `$(...)` to restore `OpenAPIHono` type after `use()`/`get()`; `HonoToOpenAPIHono<T>` is the type-level equivalent.

<!--
Source references:
- https://github.com/honojs/middleware/tree/main/packages/swagger-ui
- https://github.com/honojs/middleware/tree/main/packages/swagger-editor
- https://github.com/honojs/middleware/tree/main/packages/zod-openapi
-->
