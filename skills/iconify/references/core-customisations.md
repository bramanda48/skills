---
name: core-customisations
description: Icon customisations — dimensions, flip, rotate, inline mode
---

# Icon Customisations

Shared across all Iconify components. These are **SVG-level** transformations (they mutate the viewBox and bounding box), not CSS transforms.

## Dimensions

Default: `height: "1em"`, `width` auto-calculated from the icon's aspect ratio. Icon scales with `font-size`.

```html
<!-- Scale via font-size (default 1em) -->
<iconify-icon icon="mdi:home" style="font-size: 48px"></iconify-icon>

<!-- Explicit dimensions -->
<iconify-icon icon="mdi:home" height="24"></iconify-icon>
<iconify-icon icon="mdi:home" height="24px"></iconify-icon>
<iconify-icon icon="mdi:home" height="2em"></iconify-icon>

<!-- "auto" = use original viewBox dimensions -->
<iconify-icon icon="mdi:home" height="auto"></iconify-icon>

<!-- "unset"/"none" = no dimension attrs; control via CSS -->
<iconify-icon icon="mdi:home" height="unset" style="width: 48px; height: 48px"></iconify-icon>
```

If only one dimension is set, the other is calculated from the aspect ratio. For non-square icons, set both to avoid distortion.

## Flip

```html
<!-- flip attribute (comma-separated) -->
<iconify-icon icon="bi:check2-circle" flip="horizontal"></iconify-icon>
<iconify-icon icon="bi:check2-circle" flip="vertical"></iconify-icon>
<iconify-icon icon="bi:check2-circle" flip="horizontal,vertical"></iconify-icon>

<!-- hFlip / vFlip boolean attributes -->
<iconify-icon icon="bi:check2-circle" h-flip></iconify-icon>
<iconify-icon icon="bi:check2-circle" v-flip></iconify-icon>
```

## Rotate

```html
<!-- degrees -->
<iconify-icon icon="bi:check2-circle" rotate="90deg"></iconify-icon>
<iconify-icon icon="bi:check2-circle" rotate="180deg"></iconify-icon>
<iconify-icon icon="bi:check2-circle" rotate="270deg"></iconify-icon>

<!-- or numeric: 1=90deg, 2=180deg, 3=270deg -->
<iconify-icon icon="bi:check2-circle" rotate="2"></iconify-icon>
```

Flip is applied first, then rotation. The bounding box updates correctly (e.g. a 24×16 icon rotated 90deg becomes 16×24) — unlike CSS `transform`, which keeps the box and may cause overlap.

## Inline Mode

```html
<iconify-icon inline icon="line-md:image-twotone"></iconify-icon>
```

`inline` sets `vertical-align: -0.125em` on the inner SVG, aligning the icon baseline with text (like emoji/icon-font behavior). It does **not** change `display`.

## `buildIcon()` Customisations Object

When calling `buildIcon(icon, customisations)` directly:

```ts
interface IconifyIconCustomisations {
  inline?: boolean
  width?: string | number | null   // "auto", "unset", "none", or value
  height?: string | number | null
  hFlip?: boolean
  vFlip?: boolean
  rotate?: number                   // 0, 1, 2, 3 (90° increments)
}
```

## Key Points

- Flip/rotate are SVG-level: they update viewBox + bounding box, unlike CSS `transform`.
- Default size is `1em` — scale via `font-size`, not just width/height.
- Set both width and height for non-square icons to avoid distortion.
- `inline` only affects vertical alignment, not display.

<!--
Source references:
- https://iconify.design/docs/iconify-icon/transform.html
- https://iconify.design/docs/iconify-icon/dimensions.html
- https://iconify.design/docs/iconify-icon/inline.html
- https://iconify.design/docs/iconify-icon/build-icon.html
- sources/iconify/packages/utils/src/customisations/
-->
