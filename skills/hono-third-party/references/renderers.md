---
name: renderers
description: SSR and UI-renderer integrations for Hono (React Renderer, React Compat, Qwik City, Inertia)
---

# Renderers

## React Renderer

```bash
npm i @hono/react-renderer react react-dom hono
npm i -D @types/react @types/react-dom
```

Adds a React-based renderer to Hono. Set `jsx: "react-jsx"` and `jsxImportSource: "react"` in `tsconfig.json`; with Vite add `react`/`react-dom` to `ssr.external`.

```tsx
import { Hono } from 'hono'
import { reactRenderer } from '@hono/react-renderer'

const app = new Hono()

app.get(
  '*',
  reactRenderer(({ children }) => (
    <html>
      <body>
        <div>{children}</div>
      </body>
    </html>
  ))
)

app.get('/', (c) => c.render(<p>Welcome!</p>))
```

Extend `Props` via module augmentation (`declare module '@hono/react-renderer' { interface Props { title: string } }`) and pass values as the second argument to `c.render(node, props)`. Use `useRequestContext()` inside a component to read the Hono `Context`. Options: `docType` (boolean or custom DOCTYPE string) and `stream: true` to enable streaming responses (works with `<Suspense>`; not available under Vite/Vitest).

## React Compat

```bash
npm i react@npm:@hono/react-compat react-dom@npm:@hono/react-compat
```

An alias package that replaces `react` and `react-dom` with the React-compatibility API provided by Hono's `hono/jsx`. After this aliased install, `@hono/react-compat` is loaded wherever `react` is specified in `jsxImportSource` or an `import`. Useful when a codebase imports `react` but you want to run on `hono/jsx` primitives.

## Qwik City

```bash
npm i @hono/qwik-city
```

Mounts a Qwik City SSR renderer. Pass the Qwik City plan and your SSR `render` entry.

```ts
import { qwikMiddleware } from '@hono/qwik-city'
import qwikCityPlan from '@qwik-city-plan'
import render from './entry.ssr'
import { Hono } from 'hono'

const app = new Hono()
app.all('*', qwikMiddleware({ render, qwikCityPlan }))
```

## Inertia

```bash
npm i @hono/inertia
```

Implements the full [Inertia.js](https://inertiajs.com) protocol on Hono — render React, Vue, or Svelte straight from routes, skipping the REST/router/data-fetch layer. Define a `rootView` (returns the HTML shell that boots the SPA) and pass it to the middleware. Use `serializePage(page)` to embed the page object inside the `<script>` tag the client adapter reads on boot.

```ts
import { Hono } from 'hono'
import { inertia } from '@hono/inertia'
import { serializePage, type RootView } from '@hono/inertia'

const rootView: RootView = (page) => `<!DOCTYPE html>
<html>
  <head><title>App</title></head>
  <body>
    <script data-page="app" type="application/json">${serializePage(page)}</script>
    <div id="app"></div>
  </body>
</html>`

const app = new Hono()
app.use(inertia({ version: '1', rootView }))

app.get('/', (c) => c.render('Home', { message: 'Hello, Inertia' }))
app.get('/posts/:id', (c) => c.render('Posts/Show', { id: c.req.param('id') }))
```

Options: `version` (asset version; stale `X-Inertia-Version` triggers `409` + `X-Inertia-Location`), `rootView`. Helpers: `defer(() => fetch())` (deferred props), `merge`/`prepend`/`deepMerge(data, { matchOn })` (merge props), `scroll({ data, currentPage, lastPage, pageName, matchOn })` (infinite scroll). The bundled Vite plugin `inertiaPages()` (from `@hono/inertia/vite`) generates a `pages.gen.ts` that constrains `c.render`'s component name and types `PageProps<'Route'>`. `c.render` resolves the page URL from `c.req.url` (GET) or the `Referer` header (non-GET); pass `{ url }` as the third argument to override. `PUT`/`PATCH`/`DELETE` redirects are rewritten `302`→`303` automatically. Same route returns JSON when the request accepts `application/json`.

<!--
Source references:
- https://github.com/honojs/middleware/tree/main/packages/react-renderer
- https://github.com/honojs/middleware/tree/main/packages/react-compat
- https://github.com/honojs/middleware/tree/main/packages/qwik-city
- https://github.com/honojs/middleware/tree/main/packages/inertia
-->
