---
name: hono
description: Hono — a small, simple, ultrafast web framework built on Web Standards. Use when building HTTP APIs, edge functions, or server apps with Hono, including routing, middleware, context, JSX, RPC, validation, and multi-runtime deployment.
metadata:
  author: Anthony Fu
  version: "2026.9.17"
  source: Generated from https://github.com/honojs/hono, scripts located at https://github.com/antfu/skills
---

Hono is a small, simple, and ultrafast web framework built on Web Standards. It works on any JavaScript runtime — Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, AWS Lambda, Lambda@Edge, and Node.js — with the same code. It is zero-dependency, has first-class TypeScript support, and ships built-in middleware, helpers, and a type-safe RPC client.

> The skill is based on Hono v4.13.8, generated at 2026-09-17.

## Core

| Topic | Description | Reference |
|-------|-------------|-----------|
| Getting Started | Installing, scaffolding, and the Hono mental model — Web Standards, zero-dep, multi-runtime | [core-getting-started](references/core-getting-started.md) |
| Routing | Route registration, path params, wildcards, regex, grouping, ordering, and mounting | [core-routing](references/core-routing.md) |
| Context | The Context object — responses, headers, status, variables, env bindings, and execution context | [core-context](references/core-context.md) |
| Request | Reading the request via `c.req` — params, query, headers, cookies, and body parsing | [core-request](references/core-request.md) |
| Middleware | Writing and composing middleware, execution order, path scoping, and short-circuiting | [core-middleware](references/core-middleware.md) |
| Exceptions & Errors | `HTTPException`, global error handlers, and not-found responses | [core-exceptions](references/core-exceptions.md) |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| Validation | Validate request body, query, params, headers, and cookies with the `validator()` middleware | [features-validation](references/features-validation.md) |
| JSX | Server-side JSX rendering with `hono/jsx`, components, context, streaming, and the `html`/`css` helpers | [features-jsx](references/features-jsx.md) |
| RPC | Type-safe RPC with `hc()` — share route types between server and client | [features-rpc](references/features-rpc.md) |
| TypeScript | Typing Hono apps — `Env` generics for Bindings and Variables, typed context, and path-param inference | [features-types](references/features-types.md) |

## Helpers

| Topic | Description | Reference |
|-------|-------------|-----------|
| Streaming | Stream responses, Server-Sent Events, and WebSockets with the streaming and websocket helpers | [helpers-streaming](references/helpers-streaming.md) |
| Cookie | Get, set, delete, and sign cookies with the `hono/cookie` helper | [helpers-cookie](references/helpers-cookie.md) |
| SSG | Generate static files from Hono routes with `toSSG` and plugins | [helpers-ssg](references/helpers-ssg.md) |
| Testing | Test Hono apps with `testClient` and `app.request()` — typed calls and raw requests | [helpers-testing](references/helpers-testing.md) |
| Factory | Share middleware, handlers, and Env types across apps with `createFactory` and `createMiddleware` | [helpers-factory](references/helpers-factory.md) |
| Misc Helpers | Quick reference for Accepts, Adapter, ConnInfo, Proxy, JWT, and Dev helpers | [helpers-misc](references/helpers-misc.md) |

## Built-in Middleware

| Topic | Description | Reference |
|-------|-------------|-----------|
| Security Middleware | Security-focused built-in middleware — auth, CSRF, secure headers, IP restriction | [middleware-security](references/middleware-security.md) |
| Common Middleware | Common utility built-in middleware — CORS, logger, cache, compress, timing, and more | [middleware-common](references/middleware-common.md) |

## Advanced

| Topic | Description | Reference |
|-------|-------------|-----------|
| Adapters & Runtimes | Multi-runtime deployment model — the same Hono app runs on every JS runtime via adapters | [adapters](references/adapters.md) |
| Routers & Presets | Router internals, how `SmartRouter` picks, and when to use each preset | [advanced-internals](references/advanced-internals.md) |

## Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Best Practices | Project structure, error handling, testing, performance, and TypeScript discipline for Hono apps | [best-practices](references/best-practices.md) |
