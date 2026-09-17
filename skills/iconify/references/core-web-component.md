---
name: core-web-component
description: The iconify-icon web component — attributes, methods, SSR
---

# `iconify-icon` Web Component

The modern recommended way to render icons. A custom element (`<iconify-icon>`) that renders icons in Shadow DOM. Works in React, Vue, Svelte, Lit, Ember, and plain HTML.

## Installation & Registration

```ts
// Bundler (import once, registers the custom element)
import 'iconify-icon'

// CDN (no bundler)
// <script src="https://code.iconify.design/iconify-icon/3.0.0/iconify-icon.min.js"></script>
```

Framework wrappers (fix `class`/`className`, object icons, TS types):

```ts
// React
import { Icon } from '@iconify-icon/react'

// SolidJS
import { Icon } from '@iconify-icon/solid'
```

> Vue, Svelte, Lit, Ember work with `<iconify-icon>` directly. React works directly too, but must use `class` instead of `className` — the wrapper fixes this.

### Nuxt 3 SSR config

Declare `iconify-icon` as a custom element, otherwise dev mode warns:

```ts
export default defineNuxtConfig({
  vue: {
    compilerOptions: {
      isCustomElement: (tag: string) => tag === 'iconify-icon',
    },
  },
})
```

Not needed with `@vitejs/plugin-vue`.

## Usage

```html
<iconify-icon icon="mdi:home"></iconify-icon>
```

## Attributes / Properties

All attributes are observed — setting them re-renders. String attributes; some have typed property accessors.

| Attribute | Type | Default | Notes |
|-----------|------|---------|-------|
| `icon` | `string \| IconifyIcon` | required | Name, or JSON-stringified icon object; object via property setter |
| `mode` | `'svg' \| 'style' \| 'bg' \| 'mask'` | `'svg'` | See [features-color-modes](features-color-modes.md). Auto-detects animated icons; Safari forces `svg` |
| `inline` | `boolean` | `false` | Adds `vertical-align: -0.125em` for text baseline alignment |
| `width` | `string \| number` | derived | `"auto"` = viewBox dims; `"none"`/`"unset"` = remove (let CSS control) |
| `height` | `string \| number` | derived | Default scales with `font-size` (`1em`) |
| `flip` | `string` | — | `"horizontal"`, `"vertical"`, or `"horizontal,vertical"` |
| `rotate` | `string \| number` | `0` | `"90deg"`/`"180deg"`/`"270deg"` or `1`/`2`/`3` |
| `noobserver` | `boolean` | `false` | Disable visibility-based lazy rendering (v2.1+) |

```html
<iconify-icon icon="mdi:alert" style="color: #ba3329; font-size: 48px" width="36" height="36"></iconify-icon>
```

## Methods

Exported functions (also as static methods on the element class and instance methods on element nodes):

| Function | Signature | Returns |
|----------|-----------|---------|
| `loadIcon` | `(icon: string \| IconifyIconName) => Promise<IconifyIcon>` | Fetch one icon from API |
| `loadIcons` | `(icons, callback?) => Unsubscribe` | Bulk load; callback receives `{ loaded, missing, pending }` |
| `iconLoaded` | `(name: string) => boolean` | Is icon data in storage? |
| `getIcon` | `(name: string) => IconifyIcon \| null` | Retrieve icon data from storage |
| `listIcons` | `(provider?, prefix?) => string[]` | List loaded icons |
| `addIcon` | `(name, data: IconifyIcon) => boolean` | Add one icon — see [offline-usage](offline-usage.md) |
| `addCollection` | `(data: IconifyJSON, provider?) => boolean` | Add full icon set |
| `addAPIProvider` | `(provider, config) => void` | Custom API endpoint — see [advanced-api-providers](advanced-api-providers.md) |
| `setCustomIconLoader` | `(loader, prefix, provider?) => void` | Custom sync/async icon loader |
| `buildIcon` | `(icon, customisations?) => { attributes, body }` | Generate SVG from icon data |
| `calculateSize` | `(size, ratio?) => string` | Resolve dimension keywords |
| `restartAnimation` | `() => void` | Re-trigger SVG animations (instance method) |

```js
import { loadIcon, addIcon } from 'iconify-icon'
await loadIcon('mdi:home')
```

## Events

No public DOM events. Loading is handled via `loadIcons()` callback or polling `iconLoaded()`.

## SSR / Shadow DOM

- Content renders in Shadow DOM → server HTML is just `<iconify-icon>`, same on client → **no hydration mismatch**.
- Document styles don't leak into Shadow DOM; icon hidden until JS loads.
- Visibility observer (v2.0+) renders icons only when visible (`IntersectionObserver`); opt out with `noobserver`.

<!--
Source references:
- https://iconify.design/docs/iconify-icon/
- https://iconify.design/docs/iconify-icon/attributes.html
- sources/iconify/iconify-icon/icon/README.md
- sources/iconify/iconify-icon/icon/src/component.ts
- sources/iconify/iconify-icon/react/readme.md
-->
