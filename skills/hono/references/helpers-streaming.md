---
name: streaming
description: Stream responses, Server-Sent Events, and WebSockets with the streaming and websocket helpers
---

# Streaming and WebSockets

## stream()

`stream()` returns a streaming `Response`. The callback receives a `stream` object with `write`, `pipe`, `sleep`, `onAbort`, and `shutdown`:

```ts
import { Hono } from 'hono'
import { stream } from 'hono/streaming'

const app = new Hono()

app.get('/stream', (c) =>
  stream(c, async (stream) => {
    stream.onAbort(() => console.log('Aborted!'))
    await stream.write(new Uint8Array([0x48, 0x65, 0x6c, 0x6c, 0x6f]))
    await stream.pipe(anotherReadableStream)
  })
)
```

## streamText()

Like `stream()` but sets `Content-Type: text/plain`, `Transfer-Encoding: chunked`, and `X-Content-Type-Options: nosniff`. Adds a `writeln()` helper and `sleep()`:

```ts
import { streamText } from 'hono/streaming'

app.get('/streamText', (c) =>
  streamText(c, async (stream) => {
    await stream.writeln('Hello')
    await stream.sleep(1000)
    await stream.write('Hono!')
  })
)
```

On Cloudflare Workers/Wrangler, set `Content-Encoding: Identity` if streaming misbehaves.

## streamSSE()

Stream Server-Sent Events. Each `writeSSE()` call emits one event; loop while `!stream.aborted` for a live feed:

```ts
import { streamSSE } from 'hono/streaming'

let id = 0
app.get('/sse', (c) =>
  streamSSE(c, async (stream) => {
    while (!stream.aborted) {
      await stream.writeSSE({
        data: new Date().toISOString(),
        event: 'time-update',
        id: String(id++),
      })
      await stream.sleep(1000)
    }
  })
)
```

## Error Handling

The third argument is an error handler. Errors thrown inside the callback do **not** trigger `app.onError()` — the response has already started streaming and cannot be overwritten:

```ts
app.get('/stream', (c) =>
  stream(
    c,
    async (stream) => {
      await stream.write('data')
    },
    (err, stream) => {
      stream.writeln('An error occurred!')
      console.error(err)
    }
  )
)
```

## Backpressure and Cancellation

`stream.write()` awaits when the client can't keep up (backpressure). `stream.aborted` becomes `true` when the client disconnects. Register `stream.onAbort()` to clean up resources (timers, DB connections).

## WebSocket Helper

`upgradeWebSocket()` returns a handler that upgrades an HTTP request to a WebSocket connection. The import path is runtime-specific:

```ts
import { upgradeWebSocket } from 'hono/cloudflare-workers' // Cloudflare Workers
// import { upgradeWebSocket } from 'hono/deno'             // Deno
// import { upgradeWebSocket, websocket } from 'hono/bun'    // Bun (also export { websocket })
// import { serve, upgradeWebSocket } from '@hono/node-server' // Node.js (needs ws)
```

### Handler with Events

```ts
app.get(
  '/ws',
  upgradeWebSocket((c) => ({
    onOpen(event, ws) {
      ws.send('Connected!')
    },
    onMessage(event, ws) {
      console.log(`Message: ${event.data}`)
      ws.send('Hello from server!')
    },
    onClose() {
      console.log('Connection closed')
    },
    onError(error) {
      console.error(error)
    },
  }))
)
```

Available events: `onOpen` (not on Cloudflare Workers), `onMessage`, `onClose`, `onError`. The `ws` object exposes `.send()` and `.close()`.

### Bun Setup

Export both `fetch` and `websocket` from the entry module:

```ts
export default {
  fetch: app.fetch,
  websocket,
}
```

### Node.js Setup

Install `ws` (and `@types/ws`). Create a `WebSocketServer({ noServer: true })` and pass it to `serve()`:

```ts
import { serve, upgradeWebSocket } from '@hono/node-server'
import { WebSocketServer } from 'ws'

const wss = new WebSocketServer({ noServer: true })
serve({
  fetch: app.fetch,
  websocket: { server: wss },
})
```

### RPC Mode for WebSockets

Export the route type and the client gets a `$ws()` method returning a native `WebSocket`:

```ts
// server
export type WebSocketApp = typeof app

// client
const client = hc<WebSocketApp>('http://localhost:8787')
const socket = client.ws.$ws()
socket.addEventListener('open', () => socket.send('hi'))
```

### Middleware Caveat

`upgradeWebSocket()` modifies headers internally. Middleware that also modifies headers (e.g. CORS) on the same route can cause "can't modify immutable headers" errors. Keep WebSocket routes separate from header-rewriting middleware, or apply headers carefully.

<!--
Source references:
- https://hono.dev/docs/helpers/streaming
- https://hono.dev/docs/helpers/websocket
-->
