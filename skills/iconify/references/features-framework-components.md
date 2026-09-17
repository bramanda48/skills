---
name: features-framework-components
description: Legacy native framework components — React, Vue, Svelte
---

# Framework Components (Legacy)

The `@iconify/react`, `@iconify/vue`, `@iconify/svelte` packages are native framework components. They are **deprecated-but-supported** — prefer the `iconify-icon` web component (see [core-web-component](core-web-component.md)). Documented here for existing codebases.

## Imports

```ts
// React — named exports: Icon, InlineIcon
import { Icon, InlineIcon } from '@iconify/react'

// Vue 3 — named export Icon (Vue 2: @iconify/vue2)
import { Icon } from '@iconify/vue'

// Svelte — default export
import Icon from '@iconify/svelte'
```

## Props

All three accept the same customisation props (mirror `IconifyIconCustomisations`):

| Prop | Type | Notes |
|------|------|-------|
| `icon` | `string \| IconifyIcon` | required; string = API name, object = data |
| `width` | `string \| number` | default `1em`; `"auto"` = viewBox |
| `height` | `string \| number` | default derived from ratio |
| `color` | `string` | sets `currentColor` (monotone only) |
| `inline` | `boolean` | `vertical-align: -0.125em` |
| `flip` | `string` | `"horizontal"` / `"vertical"` / `"horizontal,vertical"` |
| `rotate` | `string \| number` | `"90deg"` or `1`/`2`/`3` |
| `mode` | `'svg' \| 'bg' \| 'mask' \| 'style'` | render mode |
| `ssr` | `boolean` | server-side render |
| `onLoad` | `() => void` | callback on first render / after API fetch (never for object icons) |

### Flip prop differences per framework

| Framework | Horizontal flip | Vertical flip |
|-----------|----------------|---------------|
| React / Svelte | `hFlip: boolean` | `vFlip: boolean` |
| Vue | `horizontalFlip` / `h-flip` | `verticalFlip` / `v-flip` |

> Vue avoids `hFlip`/`vFlip` because the `v-` prefix clashes with Vue directives.

```tsx
// React
import { Icon } from '@iconify/react'
<Icon icon="mdi:home" width="24" color="#08f" hFlip />
```

```vue
<!-- Vue -->
<script setup>
import { Icon } from '@iconify/vue'
</script>
<template>
  <Icon icon="mdi:home" width="24" color="#08f" horizontal-flip />
</template>
```

## Extra Props

- Any extra props/attributes pass through to the `<svg>` (React: `onClick`, etc.).
- `InlineIcon` (React) = `Icon` with `inline` preset.
- Svelte does **not** forward events — wrap in a `<button>` if you need click handling.
- Svelte scoped styles need `:global(svg)` to target the icon's SVG.

## Offline Entry Points

Each legacy package ships an `/offline` entry that never hits the API (see [offline-usage](offline-usage.md)).

## Key Points

- Prefer migrating to `iconify-icon` (web component) — it has better SSR, no framework quirks, and cross-framework interop.
- The `color` prop only affects monotone icons; palette icons ignore it.
- `onLoad` is a callback prop, not a DOM event.

<!--
Source references:
- sources/iconify/components/react/readme.md
- sources/iconify/components/vue/README.md
- sources/iconify/components/svelte/README.md
- sources/iconify/components/vue/src/props.ts
-->
