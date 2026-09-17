---
name: cookie
description: Get, set, delete, and sign cookies with the hono/cookie helper
---

# Cookie Helper

Read, write, and remove cookies. Signed cookies use HMAC-SHA256 via the WebCrypto API, so they are async.

```ts
import { Hono } from 'hono'
import { getCookie, setCookie, deleteCookie, getSignedCookie, setSignedCookie } from 'hono/cookie'
```

## Regular Cookies

```ts
app.get('/cookie', (c) => {
  setCookie(c, 'user', 'anthony')
  const user = getCookie(c, 'user')          // string | undefined
  const all = getCookie(c)                    // Record<string, string>
  const deleted = deleteCookie(c, 'user')     // returns the deleted value
  return c.text(`user is ${user}`)
})
```

## Signed Cookies

`getSignedCookie` returns `false` if the signature fails verification, `undefined` if the cookie is absent or not a signed format. Both are falsy, so `if (!value)` covers both.

```ts
app.get('/signed', async (c) => {
  const secret = 'a-long-enough-secret-string'

  await setSignedCookie(c, 'session', 'secret-value', secret)
  const value = await getSignedCookie(c, secret, 'session') // string | false | undefined

  const all = await getSignedCookie(c, secret) // Record<string, string | false>
  return c.text(`session: ${value}`)
})
```

## Options

`setCookie` / `setSignedCookie` accept an options object:

| Option | Type | Notes |
|--------|------|-------|
| `path` | `string` | Default `/` |
| `domain` | `string` | |
| `secure` | `boolean` | HTTPS only |
| `httpOnly` | `boolean` | Not accessible via JS |
| `sameSite` | `'Strict' \| 'Lax' \| 'None'` | |
| `expires` | `Date` | Absolute expiry |
| `maxAge` | `number` | Seconds; must be ≤ 400 days |
| `priority` | `'Low' \| 'Medium' \| 'High'` | |
| `prefix` | `'secure' \| 'host'` | Cookie-name prefix |
| `partitioned` | `boolean` | CHIPS |

```ts
setCookie(c, 'token', 'abc', {
  path: '/',
  secure: true,
  httpOnly: true,
  sameSite: 'Strict',
  maxAge: 3600,
  expires: new Date(Date.UTC(2030, 0, 1)),
})
```

`deleteCookie` accepts a subset: `{ path, secure, domain }`.

## __Secure- and __Host- Prefixes

Pass `'secure'` or `'host'` to validate or set a prefixed cookie:

```ts
getCookie(c, 'token', 'host')
await getSignedCookie(c, secret, 'token', 'secure')
setCookie(c, 'token', 'val', { prefix: 'host' })
```

The helper enforces RFC6265bis rules and throws if a prefixed cookie is used without `secure`, a `__Host-` cookie has a non-`/` path or a set domain, or `maxAge`/`expires` exceeds 400 days.

## Generating Cookie Strings

`generateCookie` and `generateSignedCookie` produce a cookie string without setting it on the response — useful when you need to set headers manually or batch multiple `Set-Cookie` values:

```ts
import { generateCookie, generateSignedCookie } from 'hono/cookie'

const cookie = generateCookie('token', 'val', { secure: true, httpOnly: true })
// 'token=val; Path=/; Secure; HttpOnly'

const signed = await generateSignedCookie('token', 'val', 'secret', { secure: true })
c.header('Set-Cookie', cookie, { append: true })
c.header('Set-Cookie', signed, { append: true })
```

<!--
Source references:
- https://hono.dev/docs/helpers/cookie
-->
