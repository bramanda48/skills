---
name: servers
description: GraphQL, tRPC, and Model Context Protocol (MCP) servers built on Hono
---

# Servers

## GraphQL Server

```bash
npm i @hono/graphql-server
```

Hosts a [GraphQL.js](https://www.npmjs.com/package/graphql) endpoint with an optional GraphiQL UI. Depends on `graphql`.

```ts
import { Hono } from 'hono'
import { type RootResolver, graphqlServer } from '@hono/graphql-server'
import { buildSchema } from 'graphql'

const app = new Hono()

const schema = buildSchema(`
type Query {
  hello: String
}
`)

const rootResolver: RootResolver = (c) => ({
  hello: () => 'Hello Hono!',
})

app.use(
  '/graphql',
  graphqlServer({ schema, rootResolver, graphiql: true })
)
```

`graphqlServer({ schema, rootResolver, graphiql? })` — set `graphiql: true` to present the GraphiQL UI in a browser. The `rootResolver` receives the Hono `Context` `c` so it can access request/env data.

## tRPC Server

```bash
npm i @hono/trpc-server
```

Adapts a [tRPC](https://trpc.io) router as Hono middleware, so the same code runs on Cloudflare Workers, Deno, Bun, and Node.

```ts
import { Hono } from 'hono'
import { trpcServer } from '@hono/trpc-server'
import { appRouter } from './router'

const app = new Hono()

app.use(
  '/trpc/*',
  trpcServer({ router: appRouter })
)
```

Pass `createContext: (_opts, c) => ({ ... })` to build the tRPC context from the Hono `Context` (e.g. `c.env.DB`, `c.req.header('X-VAR2')`). Pass `endpoint: '/api/trpc'` and mount at `/api/trpc/*` for custom prefixes. For large RPC apps, register routes on small `OpenAPIHono`/`Hono` instances and mount with `.route()` to keep `hc<>` type-checking fast. The client uses `createTRPCProxyClient<AppRouter>` with `httpBatchLink({ url })`.

## MCP (Model Context Protocol)

```bash
npm i @hono/mcp
```

Connects Hono to an [MCP](https://modelcontextprotocol.io) server over HTTP Streaming Transport (`StreamableHTTPTransport`).

```ts
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js'
import { StreamableHTTPTransport } from '@hono/mcp'
import { Hono } from 'hono'

const app = new Hono()
const mcpServer = new McpServer({ name: 'my-mcp-server', version: '1.0.0' })
const transport = new StreamableHTTPTransport()

app.all('/mcp', async (c) => {
  if (!mcpServer.isConnected()) await mcpServer.connect(transport)
  return transport.handleRequest(c)
})
```

`StreamableHTTPTransport` accepts the MCP SDK's `StreamableHTTPServerTransportOptions` plus `strictAcceptHeader` (default `false`; when `true`, requires both `application/json` and `text/event-stream` in `Accept`) and `onsessiondisconnected` (callback with the session ID on SSE-stream disconnect). MCP Auth via `simpleMcpAuthRouter({ issuer, resourceServerUrl })`.

<!--
Source references:
- https://github.com/honojs/middleware/tree/main/packages/graphql-server
- https://github.com/honojs/middleware/tree/main/packages/trpc-server
- https://github.com/honojs/middleware/tree/main/packages/mcp
-->
