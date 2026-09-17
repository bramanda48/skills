---
name: auth
description: Authentication and session middleware for Hono (Auth.js, Clerk, Firebase, OIDC, OAuth providers, Stytch, Cloudflare Access, sessions)
---

# Authentication & Session Middleware

## Auth.js

```bash
npm i @hono/auth-js @auth/core
```

Injects an [Auth.js](https://authjs.dev) session into request context. Requires `AUTH_SECRET` (and optionally `AUTH_URL`) environment variables.

```ts
import { Hono } from 'hono'
import { authHandler, initAuthConfig, verifyAuth } from '@hono/auth-js'
import GitHub from '@auth/core/providers/github'

const app = new Hono()

app.use(
  '*',
  initAuthConfig((c) => ({
    secret: c.env.AUTH_SECRET,
    providers: [GitHub({ clientId: c.env.GITHUB_ID, clientSecret: c.env.GITHUB_SECRET })],
  }))
)
app.use('/api/auth/*', authHandler())     // Auth.js routes (signin/callback/signout)
app.use('/api/*', verifyAuth())          // guards API routes

app.get('/api/protected', (c) => c.json(c.get('authUser')))
```

React helpers (`SessionProvider`, `useSession`) from `@hono/auth-js/react` read the session at `/api/auth/session` by default; override the base path via `authConfigManager.setConfig({ basePath: '/custom' })`.

## Clerk Auth

```bash
npm i @hono/clerk-auth
```

Injects the active [Clerk](https://clerk.com) session. Requires `CLERK_SECRET_KEY` and `CLERK_PUBLISHABLE_KEY` env vars.

```ts
import { clerkMiddleware, getAuth } from '@hono/clerk-auth'
import { Hono } from 'hono'

const app = new Hono()

app.use('*', clerkMiddleware())
app.get('/', (c) => {
  const { userId } = getAuth(c)
  if (!userId) return c.json({ message: 'Not logged in' })
  return c.json({ message: 'Logged in', userId })
})
```

Access the backend API client via `c.get('clerk')` (e.g. `await clerkClient.users.getUser(id)`). Pass `{ acceptsToken: 'api_key' }` to `getAuth` to verify API keys instead of session tokens.

## Firebase Auth

```bash
npm i @hono/firebase-auth
```

Verifies Firebase ID tokens (JWT) on Cloudflare Workers (officially; may work elsewhere). Requires `projectId` in config; defaults to `WorkersKVStoreSingle` for JWK caching (needs `PUBLIC_JWK_CACHE_KEY` + `PUBLIC_JWK_CACHE_KV` bindings).

```ts
import { Hono } from 'hono'
import { type VerifyFirebaseAuthConfig, type VerifyFirebaseAuthEnv, verifyFirebaseAuth, getFirebaseToken } from '@hono/firebase-auth'

const config: VerifyFirebaseAuthConfig = { projectId: 'your-project-id' }

const app = new Hono<{ Bindings: VerifyFirebaseAuthEnv }>()

app.use('*', verifyFirebaseAuth(config))
app.get('/hello', (c) => c.json(getFirebaseToken(c)))
```

`verifySessionCookieFirebaseAuth(config)` validates session cookies instead (requires `redirects.signIn` and Admin SDK credentials via `SERVICE_ACCOUNT_JSON`). Config options: `authorizationHeaderKey`, `keyStore`/`keyStoreInitializer`, `disableErrorLog`, `firebaseEmulatorHost`. Pair with `hono/csrf` and `hono/secure-headers` for cookie security (CSRF/XSS/MitM).

## OIDC Auth

```bash
npm i @hono/oidc-auth
```

Storage-less OpenID Connect login sessions backed by [oauth4webapi](https://www.npmjs.com/package/oauth4webapi). Session cookie is a signed JWT verified at the edge; refresh tokens are used implicitly after the refresh interval (default 15 min). Requires `OIDC_AUTH_SECRET` (>= 32 chars), `OIDC_ISSUER`, `OIDC_CLIENT_ID`, `OIDC_CLIENT_SECRET` (env or via `initOidcAuthMiddleware(config)`).

```ts
import { Hono } from 'hono'
import { oidcAuthMiddleware, getAuth, revokeSession, processOAuthCallback } from '@hono/oidc-auth'

const app = new Hono()

app.get('/logout', async (c) => { await revokeSession(c); return c.text('Logged out') })
app.get('/callback', async (c) => processOAuthCallback(c))
app.use('*', oidcAuthMiddleware())
app.get('/', async (c) => {
  const auth = await getAuth(c)
  return c.text(`Hello <${auth?.email}>!`)
})
```

For client secrets incompatible with `client_secret_basic` encoding (e.g. Google's `GOCSPX-`), call `setClientAuth(c, oauth2.ClientSecretPost(secret))` on every request before `getAuth`. Hook `oidcAuthRefreshErrorHook` (set via `c.set`) observes/handles refresh failures; `oidcClaimsHook` customizes claims. Tested IdPs: Auth0, AWS Cognito, GitLab, Google, Slack.

## OAuth Providers

```bash
npm i @hono/oauth-providers
```

Social-login OAuth2 flows for Google, Facebook, GitHub, LinkedIn, X (Twitter), Discord, Twitch, MS Entra, and OpenStreetMap. Import per-provider: `import { googleAuth } from '@hono/oauth-providers/google'`. The route the middleware is mounted on becomes the default `redirect_uri`.

```ts
import { Hono } from 'hono'
import { googleAuth } from '@hono/oauth-providers/google'

const app = new Hono()

app.use('/google', googleAuth({
  client_id: process.env.GOOGLE_ID,
  client_secret: process.env.GOOGLE_SECRET,
  scope: ['openid', 'email', 'profile'],
}))

app.get('/google', (c) => {
  const token = c.get('token')            // { token, expires_in }
  const grantedScopes = c.get('granted-scopes')
  const user = c.get('user-google')       // provider-specific user object
  return c.json({ token, user })
})
```

Most providers expose `refreshToken(client_id, client_secret, refresh_token)` and `revokeToken(...)` helpers (signatures vary by provider). GitHub supports both `oauthApp: true` (OAuth App, with scopes + refresh token) and GitHub App modes. MS Entra requires `tenant_id`; Twitch requires `redirect_uri`. Pass a custom `redirect_uri` when behind a reverse proxy.

## Stytch Auth

```bash
npm i @hono/stytch-auth stytch
```

Validates sessions created by [Stytch](https://stytch.com) Frontend SDKs for both Consumer and B2B auth. Requires `STYTCH_PROJECT_ID` and `STYTCH_PROJECT_SECRET` env vars. Reads JWTs from the `stytch_session_jwt` cookie by default.

```ts
import { Hono } from 'hono'
import { Consumer } from '@hono/stytch-auth'

const app = new Hono()

// Local (JWT-only, fastest) or Remote (calls Stytch, returns user data)
app.use('*', Consumer.authenticateSessionLocal())
app.get('/', (c) => {
  const session = Consumer.getStytchSession(c)
  return c.json({ message: `Hello ${session.user_id}!` })
})
```

`B2B` namespace mirrors the Consumer API (`authenticateSessionLocal`, `authenticateSessionRemote`, `authenticateOAuthToken`, `getStytchSession`/`getStytchMember`/`getStytchOrganization`). `getOAuthData(c)` returns `{ claims, token }`. Options: `getCredential(c)` (custom cookie/header extraction), `maxTokenAgeSeconds`, `onError(c, error)`. Raw Stytch client via `Consumer.getClient(c)` / `B2B.getClient(c)`.

## Cloudflare Access

```bash
npm i @hono/cloudflare-access
```

Validates that requests arrive through [Cloudflare Access](https://www.cloudflare.com/zero-trust/products/access/) by verifying the Access JWT; user details are available in context.

```ts
import { cloudflareAccess, type CloudflareAccessVariables } from '@hono/cloudflare-access'
import { Hono } from 'hono'

const app = new Hono<{ Variables: CloudflareAccessVariables }>()

app.use('*', cloudflareAccess('my-access-team-name', 'my-application-aud-tag'))
app.get('/', (c) => {
  const payload = c.get('accessPayload')
  return c.text(payload.email ? `Hello, ${payload.email}` : 'Hello')
})
```

First arg is the Access Team (org) name; second is the Application Audience (AUD) tag — a string or array (accept either to serve multiple Access apps). The AUD tag is optional for backwards compatibility but strongly recommended in production to prevent cross-application token reuse.

## Session

```bash
npm i @hono/session
```

Encrypted-cookie session middleware using [`jose`](https://github.com/panva/jose) for JWE. Requires `AUTH_SECRET` env (32-byte hex or an `EncryptionKey`). `Session<Data>` exposes `get(refresh?)`, `update(data)`, `delete()`.

```ts
import { useSession } from '@hono/session'
import { Hono } from 'hono'

const app = new Hono()

app.use(useSession()).get('/', async (c) => {
  const data = await c.var.session.get()
  return c.json(data)
})
```

With server-side session storage (e.g. Cloudflare KV, Unstorage):

```ts
import { useSession, useSessionStorage, type SessionEnv } from '@hono/session'

const app = new Hono<SessionEnv>()

app.use(
  useSessionStorage({
    async get(sid) { /* return stored data */ },
    set(sid, value) {},
    delete(sid) {},
  }),
  useSession()
)
```

Options: `generateId`, `secret`, `duration` (`{ absolute, inactivity? }` in seconds), and custom `get/set/deleteCookie` adapters. `session.get(refreshFn)` calls `refreshFn(expiredData)` if the session is stale; returning `null` destroys the session.

<!--
Source references:
- https://github.com/honojs/middleware/tree/main/packages/auth-js
- https://github.com/honojs/middleware/tree/main/packages/clerk-auth
- https://github.com/honojs/middleware/tree/main/packages/firebase-auth
- https://github.com/honojs/middleware/tree/main/packages/oidc-auth
- https://github.com/honojs/middleware/tree/main/packages/oauth-providers
- https://github.com/honojs/middleware/tree/main/packages/stytch-auth
- https://github.com/honojs/middleware/tree/main/packages/cloudflare-access
- https://github.com/honojs/middleware/tree/main/packages/session
-->
