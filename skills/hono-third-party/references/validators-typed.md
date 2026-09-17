---
name: validators-typed
description: Type-inference, decorator, and standard-schema validators for Hono (Typia, class-validator, Effect, Conform, Standard, TypeDriver)
---

# Type-Inference & Standard-Schema Validators

These validators use the same shared contract as the schema-library validators: `validator(target, schema, hook?)`, with validated data accessed via `c.req.valid('json')` (or the matching target). See the hono skill's `features-validation` for the underlying contract. The `hook` is the optional third argument `(result, c) => Response | void` for custom failure handling.

## Typia Validator

```bash
npm i @hono/typia-validator
```

```ts
import typia, { tags } from 'typia'
import { typiaValidator } from '@hono/typia-validator'

interface Author {
  name: string
  age: number & tags.Type<'uint32'> & tags.Minimum<20> & tags.ExclusiveMaximum<100>
}

const validate = typia.createValidate<Author>()

app.post('/author', typiaValidator('json', validate), (c) => {
  const data = c.req.valid('json')
  return c.json({ message: `${data.name} is ${data.age}` })
})
```

The HTTP module (`@hono/typia-validator/http`) adds query and header validation with automatic type parsing via `typia.http.createValidateQuery<T>()` and `typia.http.createValidateHeaders<T>()`. Note its parsing differs from Hono's native parsers. Choose Typia for zero-runtime-overhead validation compiled from TypeScript types (requires `typia`'s transform).

## Class-Validator

```bash
npm i @hono/class-validator
```

```ts
import { classValidator } from '@hono/class-validator'
import { IsInt, IsString } from 'class-validator'

class CreateUserDto {
  @IsString() name!: string
  @IsInt() age!: number
}

app.post('/user', classValidator('json', CreateUserDto), (c) => {
  const user = c.req.valid('json')
  return c.json({ message: `${user.name} is ${user.age}` })
})
```

Hook: `classValidator('json', CreateUserDto, (result, c) => { if (!result.success) return c.text('Invalid!', 400) })`. Choose class-validator when migrating a NestJS/typestack codebase that already defines DTOs with decorators.

## Effect Validator

```bash
npm i @hono/effect-validator
```

```ts
import { Schema as S } from '@effect/schema'
import { effectValidator } from '@hono/effect-validator'

const User = S.Struct({ name: S.String, age: S.Number })

app.post('/user', effectValidator('json', User), (c) => {
  const user = c.req.valid('json')
  return c.json({ message: `${user.name} is ${user.age}` })
})
```

API: `effectValidator(target, schema)`. Choose Effect Schema when you want bidirectional decode/encode transforms and integration with the Effect ecosystem (annotations, dependency tracking).

## Conform Validator

```bash
npm i @hono/conform-validator
```

Validates form submissions via [Conform](https://conform.guide) and integrates with Hono RPC. Pass a function that parses `FormData` into a Conform `SubmissionResult`:

```ts
import * as z from 'zod'
import { parseWithZod } from '@conform-to/zod'
import { conformValidator } from '@hono/conform-validator'

const schema = z.object({ name: z.string(), age: z.string() })

app.post(
  '/author',
  conformValidator((formData) => parseWithZod(formData, { schema }), (submission, c) => {
    if (submission.status !== 'success') return c.json({ message: 'Bad Request' }, 400)
  }),
  (c) => {
    const submission = c.req.valid('form')
    const data = submission.value
    return c.json({ message: `${data.name} is ${data.age}` })
  }
)
```

The second argument is the hook receiving the `SubmissionResult`; `parseWithYup` and `parseWithValibot` work the same way. Choose Conform for progressive form validation that shares schema logic with the client.

## Standard Validator

```bash
npm i @hono/standard-validator
```

Accepts any schema implementing the [Standard Schema Spec](https://github.com/standard-schema/standard-schema) — Zod, Valibot, ArkType, and others:

```ts
import * as z from 'zod'
import { sValidator } from '@hono/standard-validator'

const schema = z.object({ name: z.string(), age: z.number() })

app.post('/author', sValidator('json', schema), (c) => {
  const data = c.req.valid('json')
  return c.json({ message: `${data.name} is ${data.age}` })
})
```

For header validation, define keys in lowercase (Hono lowercases headers internally). `flattenErrors(result.error)` inside a hook groups flat error arrays into `{ fieldErrors, formErrors }` for form display. Choose this when you want a single validator middleware that is library-agnostic and follows the standard-schema contract.

## TypeDriver Validator

```bash
npm i @hono/typedriver-validator
```

Accepts a TypeScript DSL string, a JSON Schema object, or a Standard Schema (e.g. Zod) — unified integration for TypeScript, JSON Schema, and Standard Schema:

```ts
import { tdValidator } from '@hono/typedriver-validator'

// TypeScript DSL (library-free)
app.post(
  '/user',
  tdValidator('json', `{ name: string, age: number }`),
  (c) => {
    const user = c.req.valid('json')
    return c.json({ message: `${user.name} is ${user.age}` })
  }
)
```

Options object (4th argument): `{ format: 'json-schema' | 'standard-schema', locale: 'en_US' | 'ja_JP' | <BCP 47 with underscore> }` controls error reporting format and language. Hook: `tdValidator('json', schemaString, (result, c) => { if (!result.success) return c.text('Invalid!', 400) })`. Choose TypeDriver when one middleware must handle TypeScript, JSON Schema, and standard-schema inputs interchangeably.

<!--
Source references:
- https://github.com/honojs/middleware/tree/main/packages/typia-validator
- https://github.com/honojs/middleware/tree/main/packages/class-validator
- https://github.com/honojs/middleware/tree/main/packages/effect-validator
- https://github.com/honojs/middleware/tree/main/packages/conform-validator
- https://github.com/honojs/middleware/tree/main/packages/standard-validator
- https://github.com/honojs/middleware/tree/main/packages/typedriver-validator
-->
