---
name: features-color-modes
description: Color handling and rendering modes (svg, style, bg, mask)
---

# Color & Rendering Modes

## Rendering Modes (`mode` attribute)

| Mode | Element | Technique | Palette support |
|------|---------|-----------|----------------|
| `"svg"` (default) | `<svg>` | Direct SVG render | All icons |
| `"style"` | `<span>`/`<svg>` | Auto-selects `bg` or `mask` | Auto |
| `"bg"` | `<span>` | `background-image: url(data:svg)` | Icons with palette only |
| `"mask"` | `<span>` | `mask-image: url(...)` + `background-color: currentColor` | Monotone icons only |

Auto-detection: `svg` unless the icon body contains an `<a` (animation) tag → `bg`/`mask`. `mask` chosen when `currentColor` is present, else `bg`. **Safari forces `svg`** (buggy mask/bg support).

### SVG mode output

```html
<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24">
  <path fill="currentColor" d="M10 20v-6h4v6h5v-8h3L12 3L2 12h3v8h5Z"/>
</svg>
```

### Mask mode output

```html
<span style="
  --svg: url('data:image/svg+xml,...');
  background-color: currentColor;
  -webkit-mask-image: var(--svg);
  mask-image: var(--svg);
  mask-repeat: no-repeat;
  mask-size: 100% 100%;
  width: 1em; height: 1em;
"/>
```

## Color Handling

- **Monotone icons** use `currentColor` in the SVG path. Color inherits from CSS `color` on the element or a parent.
- **Palette icons** (emoji, some brand icons) have hardcoded colors and **cannot** be recolored.

```html
<!-- Via CSS color on parent -->
<div style="color: #08f">
  <iconify-icon inline icon="bi:bell-fill"></iconify-icon>
</div>

<!-- Via inline style -->
<iconify-icon inline style="color: red" icon="bx:bx-home"></iconify-icon>

<!-- Via CSS class -->
<iconify-icon inline class="red-icon" icon="bx:bx-home"></iconify-icon>
```

```css
.red-icon { color: #e00; }
```

> **RGBA/HSLA warning:** Semi-transparent colors overlay both layers of multi-layer icons. Use solid colors + CSS `opacity` instead.

## Key Points

- `palette: true` in icon-set metadata = coloured (ignores `color`); `false` = monotone (uses `currentColor`).
- Default `mode` is `svg` — only switch to `style`/`bg`/`mask` for animated icons or CSS-based rendering.
- Safari always falls back to `svg` regardless of `mode`.
- Color is controlled via CSS `color`, not a component attribute.

<!--
Source references:
- https://iconify.design/docs/iconify-icon/modes.html
- https://iconify.design/docs/iconify-icon/color.html
- sources/iconify/packages/types/types.d.ts
- sources/iconify/iconify-icon/icon/src/attributes/mode.ts
-->
