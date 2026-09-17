---
name: advanced-api-providers
description: Custom API providers, caching, and @iconify/utils helpers
---

# API Providers & Utilities

## Custom API Providers

By default, icons load from the public Iconify API. Register a custom provider to self-host or route through a private endpoint.

```ts
import { addAPIProvider } from 'iconify-icon'

addAPIProvider('local', {
  resources: ['https://my-icon-api.com'],
  // optional:
  index: 0,              // host rotation index
  start: 1,              // max simultaneous requests per host
  limit: 0,              // cooldown after failures (0 = no limit)
  rotate: 50,            // rotate after 50 requests
  timeout: 1000,         // abort after 1s (retries next host)
  type: 'json',          // response type
})
```

Then reference icons by `@local:prefix:name`:

```html
<iconify-icon icon="@local:custom:home"></iconify-icon>
```

The `resources` array supports redundancy — failed hosts rotate to the next. Config keys map to `PartialIconifyAPIConfig`.

## Global Config (CDN / no bundler)

```html
<script>
  window.IconifyProviders = {
    local: { resources: ['https://my-icon-api.com'] },
  }
</script>
```

Auto-processed at component init.

## Caching

The web component caches loaded icons in an in-memory store. `loadIcons()` batches requests and avoids re-fetching cached data.

> Historical note: `enableCache()` / `disableCache()` / `setAPIConfig()` / `getAPIConfig()` existed for localStorage/sessionStorage-based caching but are no longer operative as of 2025 — caching is now internal. `disableCache` may still be imported in some demo code but has no effect.

## `@iconify/utils` Public API

Helper library for building custom icon tooling. Key exports grouped by category:

### Customisations

- `mergeCustomisations(customisations, defaults)` — merge customisation objects
- `flipFromString(customisations, str)` — parse `"horizontal,vertical"` → booleans
- `rotateFromString(str)` — parse `"90deg"` → number

### Icon names

- `stringToIcon(str, validate?, allowSimple?)` — parse `provider:prefix:name`
- `validateIconName(name)` — validate

### Icon data

- `mergeIconData(icon, defaultData)` — merge icon + defaults
- `makeIconSquare(icon)` — force equal width/height

### Icon-set operations

- `parseIconSet(data, callback)` — iterate all icons (sync)
- `parseIconSetAsync(data, callback)` — async variant
- `validateIconSet(data)` / `quicklyValidateIconSet(data)`
- `getIcons(set, names)` — extract subset
- `getIconData(set, name)` — resolve icon (following aliases)
- `expandIconSet(data)` — expand aliases into full icons
- `minifyIconSet(data)` — minify for transport
- `convertIconSetInfo(data)` — normalize metadata

### SVG build/parse

- `iconToSVG(icon, customisations)` — render icon → `{ attributes, body }`
- `iconToHTML(body, attrs)` — wrap in `<svg>` string
- `svgToURL(svg)` / `svgToData(svg)` — encode for CSS
- `encodeSvgForCss(svg)` — encode for `url(data:...)`
- `calculateSize(size, ratio)` — resolve `"auto"`/`"1em"`/numbers
- `replaceIDs(html)` — dedupe SVG IDs (avoid collisions)
- `trimSVG(svg)` / `prettifySVG(svg)` — format SVG
- `getSVGViewBox(svg)` — parse viewBox

### CSS

- `getIconCSS(icon, selector?, isMask?)` — generate CSS for an icon
- `getIconContentCSS(icon)` — generate `content` CSS
- `getIconsCSS(set, names)` / `getIconsContentCSS(set, names)`

### Colours

- `stringToColor(str)` / `colorToString(color)` — parse/serialize
- `compareColors(a, b)` — equality

### Loader (for build tools / custom resolvers)

- `getCustomIcon(name, customLoaders?)` — resolve via custom loader
- `searchForIcon(...)` / `loadIcon(...)` — find/load icons
- `mergeIconProps(...)` — merge icon + customisation props
- Types: `CustomIconLoader`, `ExternalPkgName`, `UniversalIconLoader`

## Key Points

- Custom providers are referenced as `@provider:prefix:name`.
- `resources` array gives redundancy — failed hosts rotate automatically.
- `@iconify/utils` is the toolkit for building icon pipelines (validators, minifiers, SVG renderers, CSS generators).
- `getIconData` follows alias chains — use it when resolving icons from a set.

<!--
Source references:
- https://iconify.design/docs/api/providers.html
- https://iconify.design/docs/libraries/utils/
- sources/iconify/packages/utils/src/index.ts
- sources/iconify/iconify-icon/icon/src/functions.ts
-->
