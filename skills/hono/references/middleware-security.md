---
name: middleware-security
description: Security-focused built-in middleware — auth, CSRF, secure headers, IP restriction
---

# Security Middleware

Built-in middleware for authentication, CSRF protection, and security headers. All import from `hono/*` subpaths — no extra packages needed.

## Basic Auth

```ts
import { basicAuth } from 'hono/basic-auth'
```

Protect a path with username/password. Works on any runtime without extra setup.

```ts
app.use(
  '/auth/*',
  basicAuth({
    username: 'hono',
    password: 'acoolproject',
  })
)
```

Use `verifyUser` for dynamic credential checks (e.g. against a database). Pass multiple user objects as extra arguments for multi-user support.

Key options: `username`/`password` (required), `verifyUser: (username, password, c) => boolean | Promise<boolean>`, `realm`, `onAuthSuccess: (c, username) => void | Promise<void>` (set context variables after auth).

## Bearer Auth

```ts
import { bearerAuth } from 'hono/bearer-auth'
```

Verify an API token from the `Authorization: Bearer <token>` header.

```ts
const token = 'honoiscool'
app.use('/api/*', bearerAuth({ token }))
```

Pass `token: string[]` to accept multiple tokens. Use `verifyToken: (token, c) => boolean | Promise<boolean>` for database-backed validation. The token must match `/[A-Za-z0-9._~+/-]+=*/` (covers Base64 and JWT strings).

Key options: `token: string | string[]` (required), `verifyToken`, `realm`, `prefix` (default `'Bearer'`), `headerName` (default `'Authorization'`).

## JWT Auth

```ts
import { jwt } from 'hono/jwt'
import type { JwtVariables } from 'hono/jwt'
```

Verify a JWT from the `Authorization` header. The decoded payload is available via `c.get('jwtPayload')`.

```ts
const app = new Hono<{ Variables: JwtVariables }>()

app.use(
  '/auth/*',
  jwt({ secret: 'it-is-very-secret', alg: 'HS256' })
)

app.get('/auth/page', (c) => {
  return c.json(c.get('jwtPayload'))
})
```

To use a runtime env secret (e.g. `c.env.JWT_SECRET`), inline the middleware so it reads the binding per request:

```ts
app.use('/auth/*', (c, next) => {
  return jwt({ secret: c.env.JWT_SECRET, alg: 'HS256' })(c, next)
})
```

Key options: `secret` (required), `alg` (required — `HS256`|`HS384`|`HS512`|`RS256`|`RS384`|`RS512`|`PS256`|`PS384`|`PS512`|`ES256`|`ES384`|`ES512`|`EdDSA`), `cookie` (read token from a cookie instead), `headerName` (default `'Authorization'`), `verification: { iss, aud, nbf, iat, exp }`.

## JWK Auth

```ts
import { jwk } from 'hono/jwk'
```

Verify JWTs using JWK (JSON Web Key) — fetches keys from a `jwks_uri` endpoint. Rejects symmetric algorithms (`HS256` etc.) and requires a `kid` header.

```ts
app.use(
  '/auth/*',
  jwk({
    jwks_uri: 'https://your-auth-server/.well-known/jwks.json',
    alg: ['RS256'],
  })
)
```

`jwks_uri` accepts a function `(c) => string` for dynamic endpoints. Set `allow_anon: true` for optional auth — check `c.get('jwtPayload')` for `null` in handlers. Use the exported `verifyWithJwks()` to verify tokens outside of middleware.

Key options: `alg: AsymmetricAlgorithm[]` (required), `keys` or `jwks_uri`, `allow_anon` (default `false`), `cookie`, `headerName`, `verification: { iss, aud, nbf, iat, exp }`.

## CSRF Protection

```ts
import { csrf } from 'hono/csrf'
```

Protect against CSRF by validating the `Origin` and `Sec-Fetch-Site` headers. Only validates unsafe methods (not GET/HEAD/OPTIONS) with form-encodable content types.

```ts
app.use(csrf({ origin: ['https://myapp.example.com'] }))
```

For dynamic origin validation, pass a function — always anchor the regex to `$` to prevent prefix-match bypasses:

```ts
app.use(csrf({
  origin: (origin) => /https:\/\/(\w+\.)?myapp\.example\.com$/.test(origin),
}))
```

Key options: `origin: string | string[] | (origin, c) => boolean` (default: same-origin only), `secFetchSite: string | string[] | (secFetchSite, c) => boolean` (default: `'same-origin'` only).

## Secure Headers

```ts
import { secureHeaders } from 'hono/secure-headers'
```

Sets security headers (HSTS, X-Frame-Options, CSP, etc.) with sensible defaults. Inspired by Helmet.

```ts
app.use(secureHeaders())
```

Disable specific headers or override values:

```ts
app.use(secureHeaders({
  xFrameOptions: 'DENY',
  xXssProtection: false,
  strictTransportSecurity: 'max-age=63072000; includeSubDomains; preload',
}))
```

Set CSP with the `contentSecurityPolicy` object, and use the exported `NONCE` value in `scriptSrc` to generate per-request nonces accessible via `c.get('secureHeadersNonce')`. Order matters: `secureHeaders()` before `poweredBy()` removes `X-Powered-By`; the reverse order adds it back.

Key options: each header is a `string` (override), `false` (disable), or omitted (default). Notable: `contentSecurityPolicy`, `contentSecurityPolicyReportOnly`, `permissionsPolicy`, `strictTransportSecurity`, `xFrameOptions`, `crossOriginResourcePolicy`, `crossOriginOpenerPolicy`, `referrerPolicy`.

## IP Restriction

```ts
import { ipRestriction } from 'hono/ip-restriction'
```

Allow or deny requests based on the client IP. Requires a runtime-specific `getConnInfo` helper (e.g. `hono/bun`, `hono/deno`, `hono/cloudflare-workers`).

```ts
import { getConnInfo } from 'hono/bun'

app.use(
  '*',
  ipRestriction(getConnInfo, {
    allowList: ['127.0.0.1', '::1'],
    denyList: [],
  })
)
```

Rules support CIDR notation (`192.168.2.0/24`) and `*` (all). Pass a third argument to customize the 403 response:

```ts
app.use('*', ipRestriction(
  getConnInfo,
  { denyList: ['192.168.2.0/24'] },
  async (remote, c) => c.text(`Blocking ${remote.addr}`, 403)
))
```

Key options: `allowList: string[]`, `denyList: string[]`, custom error handler as third argument.

<!--
Source references:
- https://hono.dev/docs/middleware/builtin/basic-auth
- https://hono.dev/docs/middleware/builtin/bearer-auth
- https://hono.dev/docs/middleware/builtin/jwt
- https://hono.dev/docs/middleware/builtin/jwk
- https://hono.dev/docs/middleware/builtin/csrf
- https://hono.dev/docs/middleware/builtin/secure-headers
- https://hono.dev/docs/middleware/builtin/ip-restriction
-->
