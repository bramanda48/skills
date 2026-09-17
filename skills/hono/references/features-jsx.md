---
name: jsx
description: Server-side JSX rendering with hono/jsx, components, context, streaming, and the html/css helpers
---

# JSX

`hono/jsx` lets you render HTML using JSX syntax on the server. Configure `tsconfig.json` to use the Hono JSX runtime:

```json
{
  "compilerOptions": {
    "jsx": "react-jsx",
    "jsxImportSource": "hono/jsx"
  }
}
```

Use `.tsx` for files containing JSX.

## Function Components and Props

Components are plain functions typed with `FC` or `PropsWithChildren`:

```tsx
import { Hono } from 'hono'
import type { FC, PropsWithChildren } from 'hono/jsx'

const app = new Hono()

const Layout: FC = (props) => (
  <html>
    <body>{props.children}</body>
  </html>
)

const Post: FC<{ title: string }> = ({ title, children }: PropsWithChildren<{ title: string }>) => (
  <Layout>
    <h1>{title}</h1>
    {children}
  </Layout>
)

app.get('/', (c) => {
  return c.html(<Post title="Hello">Hono!</Post>)
})
```

Render with `c.html(<Component />)`. Components can be `async` — `c.html()` awaits them automatically.

## The `html` Template Tag

For static or near-static markup, the `html` tagged literal from `hono/html` is faster than JSX and avoids escaping overhead. It returns an `HtmlEsclosedString` usable as a component or inside JSX:

```tsx
import { html, raw } from 'hono/html'

const Footer = () => html`<footer>Powered by Hono</footer>`

app.get('/:name', (c) => {
  const { name } = c.req.param()
  return c.html(
    html`<!doctype html>
      <h1>Hello! ${name}!</h1>
      <${Footer} />`
  )
})
```

Use `raw()` to insert a pre-escaped string without further escaping:

```tsx
return c.html(html`<p>I'm ${raw(name)}.</p>`)
```

## JSX Renderer Middleware

`jsxRenderer` from `hono/jsx-renderer` wraps a layout around `c.render()` calls, so you don't need `c.setRenderer()` in every route. It receives `{ children }` plus any props you pass to `c.render()`:

```tsx
import { jsxRenderer } from 'hono/jsx-renderer'

app.use(
  '/page/*',
  jsxRenderer(({ children }) => (
    <html>
      <body>
        <header>Menu</header>
        <div>{children}</div>
      </body>
    </html>
  ))
)

app.get('/page/about', (c) => c.render(<h1>About</h1>))
```

### Nested Layouts

Each renderer receives a `Layout` prop that renders the parent layout, enabling composition:

```tsx
const blog = new Hono()
blog.use(
  jsxRenderer(({ children, Layout }) => (
    <Layout>
      <nav>Blog Menu</nav>
      <div>{children}</div>
    </Layout>
  ))
)
app.route('/blog', blog)
```

### Accessing Context in Components

`useRequestContext()` returns the `Context` inside a component rendered by `jsxRenderer`:

```tsx
import { useRequestContext } from 'hono/jsx-renderer'

const UrlBadge = () => {
  const c = useRequestContext()
  return <b>{c.req.url}</b>
}
```

### Passing Props to the Renderer

Extend the `ContextRenderer` interface to type extra props passed to `c.render()`:

```tsx
declare module 'hono' {
  interface ContextRenderer {
    (content: string | Promise<string>, props: { title: string }): Response
  }
}

app.get('/page/favorites', (c) =>
  c.render(<ul><li>Eating sushi</li></ul>, { title: 'My favorites' })
)
```

### Streaming and SSG Options

`jsxRenderer` accepts `{ stream: true }` to stream with `Suspense`, `{ docType: false }` to omit the DOCTYPE, or a function `(c) => ({ ... })` for per-request options. Use `isSSGContext(c)` to disable streaming during static generation.

## Context (useContext)

Share data across the component tree without prop drilling:

```tsx
import { createContext, useContext } from 'hono/jsx'

const ThemeContext = createContext({ color: '#000' })

const Button = () => {
  const theme = useContext(ThemeContext)
  return <button style={theme}>Push!</button>
}

app.get('/', (c) =>
  c.html(
    <ThemeContext.Provider value={{ color: '#fff' }}>
      <Button />
    </ThemeContext.Provider>
  )
)
```

## Metadata Hoisting

`<title>`, `<meta>`, and `<link>` written inside any component are hoisted to `<head>`. Existing elements are not removed, so later ones are appended:

```tsx
app.get('/about', (c) =>
  c.render(
    <>
      <title>About Page</title>
      <meta name="description" content="About us" />
      about content
    </>
  )
)
```

## Streaming with Suspense and ErrorBoundary

Wrap async components in `Suspense` and stream the response with `renderToReadableStream`. The fallback renders first; the awaited content streams in once the promise resolves:

```tsx
import { renderToReadableStream, Suspense, ErrorBoundary } from 'hono/jsx/streaming'

const AsyncPost = async () => {
  const post = await fetchPost()
  return <div>{post.title}</div>
}

app.get('/', (c) => {
  const stream = renderToReadableStream(
    <html>
      <body>
        <ErrorBoundary fallback={<div>Out of service</div>}>
          <Suspense fallback={<div>Loading...</div>}>
            <AsyncPost />
          </Suspense>
        </ErrorBoundary>
      </body>
    </html>
  )
  return c.body(stream, {
    headers: { 'Content-Type': 'text/html; charset=UTF-8', 'Transfer-Encoding': 'chunked' },
  })
})
```

Use `StreamingContext` to inject a CSP `scriptNonce` onto the script tags `Suspense`/`ErrorBoundary` generate.

## CSS Helper (hono/css)

Write scoped CSS-in-JS. `css` returns a class name; `<Style />` emits the collected rules:

```tsx
import { css, Style } from 'hono/css'

app.get('/', (c) => {
  const headerClass = css`
    background: orange;
    color: white;
    &:hover { background: red; }
  `
  return c.html(
    <html>
      <head><Style /></head>
      <body><h1 class={headerClass}>Hello!</h1></body>
    </html>
  )
})
```

Compose with `cx`, animate with `keyframes`, and build a custom context with `createCssContext` for predictable class slugs. Never interpolate untrusted input directly — validate against an allowlist first.

## hono/jsx/dom (Client-Side)

`hono/jsx/dom` is a small client-side DOM renderer that lets the same JSX components hydrate and update in the browser without React. Use it when you need lightweight interactivity from server-rendered Hono components. It is a separate concern from server rendering — most Hono apps render JSX only on the server with `c.html()`.

<!--
Source references:
- https://hono.dev/docs/guides/jsx
- https://hono.dev/docs/middleware/builtin/jsx-renderer
- https://hono.dev/docs/guides/jsx-dom
- https://hono.dev/docs/helpers/html
- https://hono.dev/docs/helpers/css
-->
