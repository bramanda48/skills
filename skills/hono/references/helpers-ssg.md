---
name: ssg
description: Generate static files from Hono routes with toSSG and plugins
---

# Static Site Generation (SSG)

`toSSG()` renders every registered route to static files at build time. Each route's `Content-Type` determines the file extension.

## Basic Usage

```ts
import { Hono } from 'hono'
import { toSSG } from 'hono/ssg'
import fs from 'node:fs/promises'

const app = new Hono()
app.get('/', (c) => c.html('Hello, World!'))
app.get('/about', (c) => c.html('<h1>About</h1>'))

await toSSG(app, fs)
// -> ./static/index.html, ./static/about.html
```

The second argument is a `FileSystemModule` — `node:fs/promises` on Node.js. Deno and Bun ship their own `toSSG` that omit the fs argument:

```ts
import { toSSG } from 'hono/deno' // or 'hono/bun'
toSSG(app)
```

## Route-to-File Mapping

| Route | File |
|-------|------|
| `/` | `./static/index.html` |
| `/about` | `./static/about.html` |
| `/about/` | `./static/about/index.html` |

Paths ending with `/` always save to `index.<ext>` regardless of `Content-Type`.

## Options

```ts
interface ToSSGOptions {
  dir?: string            // output dir, default './static'
  concurrency?: number   // parallel files, default 2
  extensionMap?: Record<string, string> // Content-Type → extension
  plugins?: SSGPlugin[]   // see Plugins below
}
```

Override extensions when your routes return non-standard `Content-Type`:

```ts
import { toSSG, defaultExtensionMap } from 'hono/ssg'

toSSG(app, fs, {
  dir: './public',
  extensionMap: { 'application/x-html': 'html', ...defaultExtensionMap },
})
```

## Result

```ts
interface ToSSGResult {
  success: boolean
  files: string[]
  error?: Error
}
```

## Built-in Middleware

### ssgParams — Prerender Dynamic Routes

Like Next.js `generateStaticParams`. Return an array of param objects to generate a file per value:

```ts
import { ssgParams } from 'hono/ssg'

app.get(
  '/shops/:id',
  ssgParams(async () => {
    const shops = await getShops()
    return shops.map((s) => ({ id: s.id }))
  }),
  async (c) => {
    const shop = await getShop(c.req.param('id'))
    return c.render(<h1>{shop.name}</h1>)
  }
)
```

### isSSGContext — Branch on Build vs. Runtime

```ts
import { isSSGContext } from 'hono/ssg'

app.get('/page', (c) => {
  if (isSSGContext(c)) return c.text('static content')
  return c.text('dynamic content')
})
```

### disableSSG / onlySSG

```ts
import { disableSSG, onlySSG } from 'hono/ssg'

app.get('/api', disableSSG(), (c) => c.text('not generated'))    // skipped by toSSG
app.get('/page', onlySSG(), (c) => c.html('static-only'))        // becomes 404 after build
```

`isSSGContext` is useful with `jsxRenderer` to disable `<Suspense>` streaming during SSG:

```ts
app.use('*', jsxRenderer(({ children }) => <div>{children}</div>, (c) => ({
  stream: !isSSGContext(c),
})))
```

## Plugins

Plugins hook into the generation lifecycle. `defaultPlugin` (skips non-200 responses) is applied automatically **only when no plugins are specified**. If you pass custom plugins, include it explicitly:

```ts
import { toSSG, defaultPlugin, redirectPlugin } from 'hono/ssg'

toSSG(app, fs, {
  plugins: [redirectPlugin(), defaultPlugin()], // redirect BEFORE default
})
```

`redirectPlugin()` generates an HTML meta-refresh page for redirect (301/302/etc.) routes.

### Hook Types

```ts
type BeforeRequestHook = (req: Request) => Request | false  // false = skip route
type AfterResponseHook = (res: Response) => Response | false // false = skip file
type AfterGenerateHook  = (result: ToSSGResult) => void | Promise<void>
```

### Custom Plugin Examples

Filter to GET requests only:

```ts
const getOnly: SSGPlugin = {
  beforeRequestHook: (req) => (req.method === 'GET' ? req : false),
}
```

Generate a sitemap after all files are written:

```ts
import path from 'node:path'
import { DEFAULT_OUTPUT_DIR } from 'hono/ssg'

const sitemapPlugin = (baseURL: string): SSGPlugin => ({
  afterGenerateHook: (result, fsModule, options) => {
    const dir = options?.dir ?? DEFAULT_OUTPUT_DIR
    const urls = result.files.map((f) => new URL(f, baseURL).toString())
    const xml = `<?xml version="1.0"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map((u) => `<url><loc>${u}</loc></url>`).join('\n')}
</urlset>`
    return fsModule.writeFile(path.join(dir, 'sitemap.xml'), xml)
  },
})

toSSG(app, fs, { plugins: [defaultPlugin(), sitemapPlugin('https://example.com')] })
```

## Vite Integration

Use `@hono/vite-ssg` to integrate SSG into a Vite build pipeline: https://github.com/honojs/vite-plugins/tree/main/packages/ssg

<!--
Source references:
- https://hono.dev/docs/helpers/ssg
-->
