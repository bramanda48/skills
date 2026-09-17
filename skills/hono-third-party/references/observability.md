---
name: observability
description: Metrics, tracing, and error reporting middleware for Hono (OpenTelemetry, Prometheus, Sentry)
---

# Observability

## OpenTelemetry

```bash
npm i @hono/otel
```

Instruments the full request-response lifecycle with [OpenTelemetry](https://opentelemetry.io/) traces and (on Node) metrics.

```ts
import { NodeSDK } from '@opentelemetry/sdk-node'
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http'
import { httpInstrumentationMiddleware } from '@hono/otel'
import { Hono } from 'hono'

const sdk = new NodeSDK({ traceExporter: new OTLPTraceExporter() })
sdk.start()

const app = new Hono()
app.use(
  httpInstrumentationMiddleware({
    serviceName: 'my-service',
    serviceVersion: '1.0.0',
    captureRequestHeaders: ['user-agent', 'service-name'],
    captureResponseHeaders: [],
  })
)
```

Configuration options on `HttpInstrumentationConfig`: `serviceName`/`serviceVersion` (Resource attributes — no defaults), `captureRequestHeaders`/`captureResponseHeaders` (arrays of header names; captured as `http.request.header.*` span attributes), `tracerProvider`/`meterProvider`/`tracer` (custom SDK components), `getTime`, and `spanNameFactory: (c: HonoContext) => string`. On Cloudflare Workers use `@microlabs/otel-cf-workers`'s `instrument(app, config)` wrapping the app instead (metrics support is limited there). Limitation: instruments the entire request lifecycle, not individual middleware.

## Prometheus

```bash
npm i @hono/prometheus prom-client
```

Adds RED metrics (Rate, Errors, Duration) and exposes them at `/metrics` for scraping.

```ts
import { prometheus } from '@hono/prometheus'
import { Hono } from 'hono'

const app = new Hono()

const { printMetrics, registerMetrics } = prometheus()
app.use('*', registerMetrics)
app.get('/metrics', printMetrics)
```

Options on `prometheus(options)`: `prefix` (string), `registry` (a prom-client `Registry` — pass a shared one to expose custom metrics on the same endpoint), `collectDefaultMetrics` (boolean or prom-client options), and `metricOptions` with `disabled` and `customLabels: Record<string, (c) => string>` (functions run after middleware; e.g. `content_type: (c) => c.res.headers.get('content-type')`). Register custom metrics on the shared registry, then increment them anywhere in app code.

## Sentry

```bash
npm i @hono/sentry
```

Captures exceptions and sends them to a Sentry DSN via [toucan-js](https://github.com/robertcepa/toucan-js). On Cloudflare Workers, set a `SENTRY_DSN` binding; elsewhere pass `{ dsn }`.

```ts
import { Hono } from 'hono'
import { sentry } from '@hono/sentry'

const app = new Hono()

app.use('*', sentry())
app.get('/', (c) => c.text('foo'))

app.onError((e, c) => {
  c.get('sentry').captureException(e)
  return c.text('Internal Server Error', 500)
})
```

Retrieve the `Sentry` instance via `c.get('sentry')` to add context (`setContext`, `captureException`). Options are `Omit<ToucanOptions, 'request' | 'context'>`. For Deno, import from `npm:@hono/sentry`. Note: Sentry now ships an official Hono SDK; new projects should prefer that for first-party support.

<!--
Source references:
- https://github.com/honojs/middleware/tree/main/packages/otel
- https://github.com/honojs/middleware/tree/main/packages/prometheus
- https://github.com/honojs/middleware/tree/main/packages/sentry
-->
