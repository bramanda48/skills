---
name: core-overview
description: Iconify ecosystem, naming format, and component taxonomy
---

# Iconify Overview

Iconify is a unified icon framework: 200+ icon sets, 250,000+ icons, loaded on demand from an API or bundled offline.

## Icon Naming Format

Format: `[@provider:]prefix:name` — parts separated by `:` (the provider is optional, prefixed with `@`).

| Part | Required | Example | Notes |
|------|----------|---------|-------|
| `provider` | No | `@custom` | Defaults to the public Iconify API (empty). Custom providers start with `@`. |
| `prefix` | Yes | `mdi`, `bi`, `mdi-light` | Icon-set identifier. Hyphens allowed. |
| `name` | Yes | `home`, `arrow-left` | Icon within the set. |

```html
<!-- public API, prefix 'mdi', name 'home' -->
<iconify-icon icon="mdi:home"></iconify-icon>

<!-- custom provider, prefix 'md', name 'test' -->
<iconify-icon icon="@custom:md:test"></iconify-icon>
```

## Two Delivery Modes

1. **On-demand (API):** Components fetch icon data at render time from the Iconify API. No bundling of icon data; works with any of 300k+ icons.
2. **Offline/bundled:** Bundle icon data locally via `@iconify/json` (all sets) or `@iconify-json/{prefix}` (one set). No API call — see [offline-usage](offline-usage.md).

## Component Taxonomy

| Package | Type | Status |
|---------|------|--------|
| `iconify-icon` | Web component (`<iconify-icon>`) | **Recommended modern default** — works everywhere via Shadow DOM |
| `@iconify-icon/react` | React wrapper for the web component | Current |
| `@iconify-icon/solid` | SolidJS wrapper for the web component | Current |
| `@iconify/react`, `@iconify/vue`, `@iconify/svelte` | Legacy native framework components | Deprecated-but-supported; prefer web component |
| `components-css/*` | CSS background/mask rendering | Experimental; API fallback for Safari |

> Prefer the `iconify-icon` web component (with framework wrappers where needed) over the legacy `@iconify/{react,vue,svelte}` native components. The native components are being phased out. The web component avoids framework-specific quirks, works better with SSR (Shadow DOM → no hydration mismatch), and interoperates across frameworks.

## Monorepo Packages (`@iconify/*`)

| Package | Purpose |
|---------|---------|
| `@iconify/types` | TypeScript type definitions (icon + icon-set shapes) |
| `@iconify/utils` | Helpers: SVG build/parse, icon-set ops, loader, colours, customisations |
| `@iconify/core` | Shared impl for native components (will be deprecated → `@iconify/component-utils`) |
| `@iconify/fetch` | `fetch` wrapper with redundancy/multi-host (replaces `@iconify/api-redundancy`) |
| `@iconify/component-utils` | Modern shared impl for components (replaces `@iconify/core`) |

Related external repos: `iconify/icon-sets` (data), `iconify/tools` (parsers), `iconify/iconify-tailwind` (Tailwind plugin).

<!--
Source references:
- https://iconify.design/docs/icon-components/
- https://iconify.design/docs/iconify-icon/
- https://iconify.design/docs/api/providers.html
- sources/iconify/README.md
-->
