---
name: offline-usage
description: Bundling icons locally without the API
---

# Offline Usage

Bundle icon data locally to avoid API calls. Use when you know the icons ahead of time, want offline support, or need predictable bundling.

## Data Packages

| Package | Contents |
|---------|----------|
| `@iconify/json` | Full icon data (all 300k+ icons). Large. |
| `@iconify-json/{prefix}` | One icon set per package (e.g. `@iconify-json/mdi`). Tree-shakeable. |
| `@iconify-icons/{prefix}` | ESM, one icon per file. |
| `@iconify/icons-{prefix}` | CJS variant — needed for Next.js / older bundlers. |

## Register Icons at Runtime

```ts
import { addIcon, addCollection } from 'iconify-icon'
import mdi from '@iconify/json/json/mdi.json'

// Add a full icon set
addCollection(mdi)

// Add a single icon
addIcon('mdi:custom', {
  body: '<path fill="currentColor" d="M10 20v-6h4v6h5v-8h3L12 3L2 12h3v8h5Z"/>',
  width: 24,
  height: 24,
})
```

After registration, `<iconify-icon icon="mdi:home">` resolves locally without an API call.

### `addCollection` prefix behavior

| `provider` arg | Storage key |
|----------------|-------------|
| omitted / `true` | uses `data.prefix + ':'` (default) |
| string | overrides the prefix |
| `false` | stores without a prefix (plain names) |

## Per-Set Packages (Tree-Shakeable)

```ts
// Import only the icons you need
import { home, account } from '@iconify-icons/mdi'

addIcon('mdi:home', home)
addIcon('mdi:account', account)
```

## Global Preload (CDN / no bundler)

```html
<script>
  window.IconifyPreload = [{ prefix: 'mdi', icons: { /* ... */ } }]
  // or an array of IconifyJSON sets
</script>
```

Auto-processed at component init — registers all sets before first render.

## Offline Component Variants (legacy native components)

The legacy `@iconify/{vue,react,svelte}` packages ship `/offline` entry points that never hit the API:

```ts
// Vue
import { Icon, addIcon, addCollection } from '@iconify/vue/dist/offline'

// React
import { Icon, addIcon, addCollection } from '@iconify/react/dist/offline'

// Svelte (default export)
import Icon, { addIcon, addCollection } from '@iconify/svelte/dist/OfflineIcon.svelte'
```

> The `/offline` stubs are TS-export shims that re-export from the main package; they exist because TypeScript doesn't support conditional exports cleanly. Functionally identical to calling `addIcon`/`addCollection` from the main entry.

## Key Points

- Object icons (passed via the `icon` property) never trigger an API call or `onLoad`.
- String icon names trigger an API fetch **only if** the prefix exists and data is missing from storage.
- For the web component, `addIcon`/`addCollection` are the only offline API — import them from `iconify-icon` (or `@iconify-icon/react`/`@iconify-icon/solid`).
- Prefer `@iconify-json/{prefix}` over the full `@iconify/json` for tree-shaking.

<!--
Source references:
- https://iconify.design/docs/icon-components/offline.html
- sources/iconify/components/vue/src/offline.ts
- sources/iconify/components/vue/offline/readme.md
- sources/iconify/iconify-icon/icon/src/functions.ts
- sources/iconify/iconify-icon/react/readme.md
-->
