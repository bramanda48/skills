---
name: iconify
description: Iconify icon framework — web component, customisations, color modes, offline usage, data format, API providers, and Tailwind. Use when rendering icons via `iconify-icon`, `@iconify-icon/react|solid`, bundling icon data offline, or using `@iconify/utils`.
metadata:
  author: Anthony Fu
  version: "2026.9.17"
  source: Generated from https://github.com/iconify/iconify, scripts located at https://github.com/antfu/skills
---

# Iconify

> Based on iconify-icon web component v3.0.2. Iconify is the most versatile icon framework: 200+ icon sets, 250,000+ icons, loaded on demand from an API or bundled offline.

Iconify renders icons by name, fetching data from the Iconify API at runtime (no bundling needed) or from locally-bundled icon data. The recommended approach is the `iconify-icon` web component, which uses Shadow DOM and works across all frameworks.

## Core

| Topic | Description | Reference |
|-------|-------------|-----------|
| Overview & Naming | Ecosystem, `provider:prefix:name` format, component taxonomy | [core-overview](references/core-overview.md) |
| Web Component | `<iconify-icon>` attributes, methods, SSR/Nuxt config | [core-web-component](references/core-web-component.md) |
| Customisations | Dimensions, flip, rotate, inline mode, `buildIcon()` | [core-customisations](references/core-customisations.md) |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| Color & Modes | `svg`/`style`/`bg`/`mask` modes, `currentColor`, palette vs monotone | [features-color-modes](references/features-color-modes.md) |
| Framework Components | Legacy `@iconify/{react,vue,svelte}` native components | [features-framework-components](references/features-framework-components.md) |
| CSS & Tailwind | CSS icons, Tailwind v3/v4 plugins, class patterns | [features-css-tailwind](references/features-css-tailwind.md) |

## Advanced

| Topic | Description | Reference |
|-------|-------------|-----------|
| Icon Data Format | `IconifyIcon`, `IconifyJSON`, aliasing, `@iconify/types` | [advanced-icon-data](references/advanced-icon-data.md) |
| API Providers & Utils | Custom API providers, caching, `@iconify/utils` helpers | [advanced-api-providers](references/advanced-api-providers.md) |

## Offline Usage

| Topic | Description | Reference |
|-------|-------------|-----------|
| Offline / Bundling | `addIcon`/`addCollection`, `@iconify/json`, per-set packages, preload | [offline-usage](references/offline-usage.md) |

## Quick Reference

### Install

```bash
npm i iconify-icon              # web component (universal)
npm i @iconify-icon/react       # React wrapper
npm i @iconify-icon/solid       # SolidJS wrapper
npm i @iconify/json             # all icon data (offline)
npm i @iconify-json/mdi         # one set (tree-shakeable, offline)
```

### Render an icon

```html
<!-- Web component (import once to register) -->
<script type="module">
  import 'iconify-icon'
</script>
<iconify-icon icon="mdi:home" style="font-size: 24px; color: #08f"></iconify-icon>
```

```tsx
// React
import { Icon } from '@iconify-icon/react'
<Icon icon="mdi:home" width={24} />
```

### Bundle icons offline

```ts
import { addCollection } from 'iconify-icon'
import mdi from '@iconify/json/json/mdi.json'
addCollection(mdi) // now <iconify-icon icon="mdi:home"> resolves locally
```
