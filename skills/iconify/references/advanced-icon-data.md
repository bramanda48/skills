---
name: advanced-icon-data
description: IconifyJSON and IconifyIcon data structures, aliasing, types
---

# Icon Data Format & Types

Defined in `@iconify/types`. These shapes are the interchange format for icon data — used by the API, storage, `addIcon`/`addCollection`, and `@iconify/utils`.

## `IconifyIcon` (single icon)

```ts
interface IconifyIcon extends IconifyOptional {
  body: string  // SVG inner content (paths, etc.) — the only required field
}

interface IconifyOptional extends IconifyDimensions, IconifyTransformations {}

interface IconifyDimensions {
  left?: number   // default 0
  top?: number    // default 0
  width?: number  // default 16
  height?: number // default 16
}

interface IconifyTransformations {
  rotate?: 0 | 1 | 2 | 3  // 90° steps, additive (mod 4)
  hFlip?: boolean          // merged XOR
  vFlip?: boolean
}
```

```ts
const icon: IconifyIcon = {
  body: '<path fill="currentColor" d="M10 20v-6h4v6h5v-8h3L12 3L2 12h3v8h5Z"/>',
  width: 24,
  height: 24,
}
```

## `IconifyJSON` (icon set)

```ts
interface IconifyJSON extends IconifyJSONIconsData, IconifyMetaData {
  lastModified?: number  // unix seconds, for cache invalidation
  not_found?: string[]
}

interface IconifyJSONIconsData extends IconifyDimensions {
  prefix: string                  // required
  provider?: string
  icons: Record<string, ExtendedIconifyIcon>      // name → icon
  aliases?: Record<string, ExtendedIconifyAlias>  // name → alias
}

interface ExtendedIconifyIcon extends IconifyIcon {
  hidden?: boolean  // not shown in lists, but loadable
}

interface IconifyAlias extends IconifyOptional {
  parent: string  // the icon name this alias points to
}
```

The set root can hold any `IconifyOptional` field (dimensions, transformations) as **defaults for all icons** — per-icon values override.

## `IconifyMetaData`

```ts
interface IconifyMetaData {
  info?: IconifyInfo
  chars?: IconifyChars           // Record<hexCode, iconName> — font char map
  categories?: IconifyCategories // Record<category, string[]>
  themes?: LegacyIconifyThemes   // deprecated
  prefixes?: Record<string, string>
  suffixes?: Record<string, string>
}
```

## `IconifyInfo` (set metadata)

```ts
interface IconifyInfo {
  name: string
  author?: { name: string; url?: string }
  license?: { title: string; spdx?: string; url?: string }
  total?: number
  version?: string
  samples?: string[]
  height?: number | number[]
  displayHeight?: number  // 16–24
  category?: string
  tags?: string[]
  palette?: boolean  // true = coloured; false = monotone (uses currentColor)
  hidden?: boolean
}
```

## Aliasing

Aliases point to a parent icon and can override dimensions/transformations. Merging rules:

- `rotate`: **additive** (mod 4)
- `hFlip` / `vFlip`: **XOR**
- other fields: overwrite

```ts
const set: IconifyJSON = {
  prefix: 'mdi',
  icons: {
    home: { body: '<path d="..."/>', width: 24, height: 24 },
  },
  aliases: {
    'house': { parent: 'home' },                 // alias → home
    'home-flip': { parent: 'home', hFlip: true }, // alias with transform
  },
}
```

## `IconifyIconCustomisations`

The render-time customisations object (passed to `buildIcon`, used by components):

```ts
interface IconifyIconCustomisations extends IconifyTransformations {
  width?: string | number | null
  height?: string | number | null
  inline?: boolean
}
```

## Key Points

- `body` is the only required field on an icon — dimensions/transformations are optional with sensible defaults (16×16, no rotation/flip).
- Set-root dimensions become defaults for all icons in the set.
- `palette: false` (monotone) → icons use `currentColor` and can be recolored; `palette: true` → hardcoded colors.
- Alias merging: rotate additive, flip XOR — important when bundling derived icons.

<!--
Source references:
- sources/iconify/packages/types/types.d.ts
- sources/iconify/packages/types/README.md
- https://iconify.design/docs/types/
-->
