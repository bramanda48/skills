---
name: core-routing
description: Route registration, path params, wildcards, regex, grouping, ordering, and mounting
---

# Routing

## HTTP Method Helpers

```ts
import { Hono } from 'hono'
const app = new Hono()

app.get('/', (c) => c.text('GET'))
app.post('/', (c) => c.text('POST'))
app.put('/', (c) => c.text('PUT'))
app.delete('/', (c) => c.text('DELETE'))
app.patch('/', (c) => c.text('PATCH'))
app.options('/', (c) => c.text('OPTIONS'))

// Match any method
app.all('/hello', (c) => c.text('Any method'))

// Custom / multiple methods, multiple paths
app.on('PURGE', '/cache', (c) => c.text('purged'))
app.on(['PUT', 'DELETE'], '/post', (c) => c.text('put or delete'))
app.on('GET', ['/hello', '/ja/hello', '/en/hello'], (c) => c.text('hello'))
```

Hono auto-converts HEAD requests to GET and strips the body — do not register dedicated `app.head()` handlers; they will never run. Use middleware to add HEAD-specific headers if needed.

## Chained Registration

Chain methods on one path:

```ts
app
  .get('/endpoint', (c) => c.text('GET'))
  .post((c) => c.text('POST'))
  .delete((c) => c.text('DELETE'))
```

## Path Parameters

```ts
app.get('/user/:name', (c) => c.text(c.req.param('name')))

app.get('/posts/:id/comment/:comment_id', (c) => {
  const { id, comment_id } = c.req.param()
  return c.text(`${id} / ${comment_id}`)
})
```

When a route is defined inline, `c.req.param('name')` is inferred as a literal type — no manual generics needed.

### Optional Parameters

`?` makes a segment optional:

```ts
// matches /api/animal and /api/animal/dog
app.get('/api/animal/:type?', (c) => c.text(c.req.param('type') ?? 'all'))
```

### Regex Parameters

```ts
app.get('/post/:date{[0-9]+}/:title{[a-z]+}', (c) => {
  const { date, title } = c.req.param()
  return c.json({ date, title })
})
```

To include slashes in a regex capture, use `{.+}`:

```ts
app.get('/posts/:filename{.+\.png}', (c) => c.text(c.req.param('filename')))
```

## Wildcards

```ts
app.get('/wild/*/card', (c) => c.text('matched'))
```

`*` matches a single path segment; `{.+}` or named regex captures span segments.

## Nested Routes & Grouping

Compose larger apps by building a `Hono` subgroup and mounting it with `app.route(path, subapp)`:

```ts
const book = new Hono()
book.get('/', (c) => c.text('List'))                  // GET /book
book.get('/:id', (c) => c.text(c.req.param('id')))   // GET /book/:id
book.post('/', (c) => c.text('Created', 201))        // POST /book

const app = new Hono()
app.route('/book', book)
```

For multi-file apps, export a subapp from each module and mount:

```ts
// index.ts
import authors from './authors'
import books from './books'
const app = new Hono()
app.route('/authors', authors)
app.route('/books', books)
export default app
```

`basePath()` prefixes a subapp without remounting:

```ts
const api = new Hono().basePath('/api')
api.get('/book', (c) => c.text('List')) // GET /api/book
```

To merge multiple subapps at `/` without remounting each, mount each at `/`:

```ts
app.route('/', book) // book's own /book path is preserved
app.route('/', user)
```

## Route Ordering

Handlers and middleware run in **registration order**; the first matching handler stops the chain:

```ts
app.get('/book/a', (c) => c.text('a'))          // GET /book/a -> "a"
app.get('/book/:slug', (c) => c.text('common')) // GET /book/b -> "common"
```

A `*` catch-all registered **before** a specific route swallows it:

```ts
app.get('*', (c) => c.text('common')) // GET /foo -> "common"; /foo below never runs
app.get('/foo', (c) => c.text('foo'))
```

Use a `*` fallback **after** specific routes:

```ts
app.get('/bar', (c) => c.text('bar'))
app.get('*', (c) => c.text('fallback')) // GET /anything-else -> "fallback"
```

Register shared middleware before handlers:

```ts
app.use(logger())
app.get('/foo', (c) => c.text('foo'))
```

### Grouping order matters

`app.route()` copies the subapp's routes into the parent at call time. Mount inner subapps before outer ones, or the outer mount copies an empty route set:

```ts
// Correct: define innermost first, then mount outward
three.get('/hi', (c) => c.text('hi'))
two.route('/three', three)
app.route('/two', two) // GET /two/three/hi -> 200

// Wrong: app mounts two while two is still empty
app.route('/two', two) // GET /two/three/hi -> 404
two.route('/three', three)
```

## Strict Mode

By default `/hello` and `/hello/` are distinct. Disable with `{ strict: false }`:

```ts
const app = new Hono({ strict: false })
```

## Mounting External Apps

`app.mount()` integrates non-Hono handlers (e.g. itty-router) under a path:

```ts
app.mount('/itty', ittyRouter.handle)
```

By default the mount path is stripped from the incoming `Request`; pass `replaceRequest: false` to forward the original request unchanged.

<!--
Source references:
- https://hono.dev/docs/api/routing
- https://hono.dev/docs/api/hono
-->
