---
name: validators-popular
description: Schema-library validators for Hono (Zod, Valibot, TypeBox, ArkType, Ajv)
---

# Schema-Library Validators

Each package wraps Hono core's `validator()` with the shared contract `validator(target, schema, hook?)`, where `target` is a `ValidationTargets` key (`'json'`, `'form'`, `'query'`, `'header'`, `'param'`). Access validated data in the handler via `c.req.valid('json')` (or the matching target). Pass a `hook` as the third argument to customize the failure response. See the hono skill's `features-validation` for the underlying contract.

## Zod Validator

```bash
npm i @hono/zod-validator
```

```ts
import * as z from 'zod'
import { zValidator } from '@hono/zod-validator'

const schema = z.object({ name: z.string(), age: z.number() })

app.post('/author', zValidator('json', schema), (c) => {
  const data = c.req.valid('json')
  return c.json({ message: `${data.name} is ${data.age}` })
})
```

Hook (custom failure response) and a custom `validationFunction` (defaults to `schema.safeParseAsync`, e.g. to use `.passthrough()`):

```ts
app.post(
  '/post',
  zValidator('json', schema, (result, c) => {
    if (!result.success) return c.text('Invalid!', 400)
  }),
  (c) => c.json(c.req.valid('json'))
)

zValidator('json', schema, undefined, {
  validationFunction: async (schema, value) =>
    schema.passthrough().safeParseAsync(value),
})
```

Use Zod for the widest ecosystem familiarity; pick the hook to throw an `HTTPException` instead of returning directly.

## Valibot Validator

```bash
npm i @hono/valibot-validator
```

```ts
import * as v from 'valibot'
import { vValidator } from '@hono/valibot-validator'

const schema = v.object({ name: v.string(), age: v.number() })

app.post('/author', vValidator('json', schema), (c) => {
  const data = c.req.valid('json')
  return c.json({ message: `${data.name} is ${data.age}` })
})
```

Hook signature matches Zod: `vValidator('json', schema, (result, c) => { if (!result.success) return c.text('Invalid!', 400) })`. Choose Valibot for its modular/tree-shakable build size.

## TypeBox Validator

```bash
npm i @hono/typebox-validator
```

```ts
import { tbValidator } from '@hono/typebox-validator'
import Type from 'typebox'

const User = Type.Object({ name: Type.String(), age: Type.Number() })

app.post('/user', tbValidator('json', User), (c) => {
  const user = c.req.valid('json')
  return c.json({ message: `${user.name} is ${user.age}` })
})
```

Also accepts a raw JSON Schema object instead of a TypeBox schema, so you can reuse shared JSON Schema definitions. Hook signature: `tbValidator('json', User, (result, c) => { if (!result.success) return c.text('Invalid!', 400) })`. Choose TypeBox when you need JSON Schema as the source of truth.

## ArkType Validator

```bash
npm i @hono/arktype-validator
```

```ts
import { type } from 'arktype'
import { arktypeValidator } from '@hono/arktype-validator'

const schema = type({ name: 'string', age: 'number' })

app.post('/author', arktypeValidator('json', schema), (c) => {
  const data = c.req.valid('json')
  return c.json({ message: `${data.name} is ${data.age}` })
})
```

Hook signature: `arktypeValidator('json', schema, (result, c) => { if (!result.success) return c.text('Invalid!', 400) })`. Choose ArkType for its concise string-based DSL and fast runtime.

## Ajv Validator

```bash
npm i @hono/ajv-validator
```

```ts
import { type JSONSchemaType } from 'ajv'
import { ajvValidator } from '@hono/ajv-validator'

const schema: JSONSchemaType<{ name: string; age: number }> = {
  type: 'object',
  properties: { name: { type: 'string' }, age: { type: 'number' } },
  required: ['name', 'age'],
  additionalProperties: false,
}

app.post('/user', ajvValidator('json', schema), (c) => {
  const user = c.req.valid('json')
  return c.json({ message: `${user.name} is ${user.age}` })
})
```

Hook signature matches the others: `ajvValidator('json', schema, (result, c) => { if (!result.success) return c.text('Invalid!', 400) })`. Choose Ajv when validating against externally-supplied JSON Schemas (draft-07/2019-09/2020-12) or sharing schemas across services.

<!--
Source references:
- https://github.com/honojs/middleware/tree/main/packages/zod-validator
- https://github.com/honojs/middleware/tree/main/packages/valibot-validator
- https://github.com/honojs/middleware/tree/main/packages/typebox-validator
- https://github.com/honojs/middleware/tree/main/packages/arktype-validator
- https://github.com/honojs/middleware/tree/main/packages/ajv-validator
-->
