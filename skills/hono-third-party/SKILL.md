---
name: hono-third-party
description: Third-party middleware for Hono published under the @hono scope — validators, auth, observability, servers, renderers, OpenAPI tooling, transpilers, and utilities. Use when integrating @hono/* packages into a Hono app.
metadata:
  author: BRAM
  version: "2026.9.17"
  source: Generated from https://github.com/honojs/middleware, scripts located at https://github.com/bramanda48/skills
---

Third-party middleware for Hono is maintained in the `github.com/honojs/middleware` monorepo and published to npm under the `@hono` scope (e.g. `@hono/zod-validator`). Each package wraps or extends Hono with a specific integration — schema validators, authentication providers, observability, GraphQL/tRPC servers, SSR renderers, OpenAPI tooling, and more. Install with `npm i @hono/<name>` and import from `@hono/<name>`.

> The skill is based on the `honojs/middleware` monorepo, generated at 2026-09-17.

## Validators

| Topic | Description | Reference |
|-------|-------------|-----------|
| Popular Validators | Schema-library validators — Zod, Valibot, TypeBox, ArkType, Ajv | [validators-popular](references/validators-popular.md) |
| Typed Validators | Type-inference, decorator, and standard-schema validators — Typia, class-validator, Effect, Conform, Standard, TypeDriver | [validators-typed](references/validators-typed.md) |

## Auth

| Topic | Description | Reference |
|-------|-------------|-----------|
| Authentication | Auth and session middleware — Auth.js, Clerk, Firebase, OIDC, OAuth providers, Stytch, Cloudflare Access, sessions | [auth](references/auth.md) |

## Observability

| Topic | Description | Reference |
|-------|-------------|-----------|
| Observability | Metrics, tracing, and error reporting — OpenTelemetry, Prometheus, Sentry | [observability](references/observability.md) |

## Servers

| Topic | Description | Reference |
|-------|-------------|-----------|
| Servers | GraphQL, tRPC, and Model Context Protocol (MCP) servers built on Hono | [servers](references/servers.md) |

## Renderers

| Topic | Description | Reference |
|-------|-------------|-----------|
| Renderers | SSR and UI-renderer integrations — React Renderer, React Compat, Qwik City, Inertia | [renderers](references/renderers.md) |

## OpenAPI

| Topic | Description | Reference |
|-------|-------------|-----------|
| OpenAPI | Swagger UI, Swagger Editor, and Zod OpenAPI tooling | [openapi](references/openapi.md) |

## Transpilers

| Topic | Description | Reference |
|-------|-------------|-----------|
| Transpilers | Bundler/transpiler and compression helpers — esbuild, Bun transpiler, Bun compress | [transpilers](references/transpilers.md) |

## Utilities

| Topic | Description | Reference |
|-------|-------------|-----------|
| Utilities | Misc middleware — events, logging, UA blocking, authz, DI, WebSocket, SSG, Cap'n Web, example, alt router | [utilities](references/utilities.md) |
