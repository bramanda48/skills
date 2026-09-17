---
name: features-css-tailwind
description: CSS icons and Tailwind CSS plugin integration
---

# CSS Icons & Tailwind

Two CSS-based approaches that render icons without a JS component: the `components-css` packages (background/mask) and the Tailwind CSS plugins.

## CSS Icon Components (`components-css`)

Render icons as `<span>` elements using `background-image` or `mask-image`, with the Iconify API as a fallback for Safari (which has buggy mask/bg support). Available for React, Vue, and Svelte.

```tsx
import { Icon } from '@iconify/css/react'
<Icon icon="mdi:home" />
```

> This is an experimental track separate from the main `iconify-icon` web component. For most use cases, prefer the web component with `mode="style"`/`"bg"`/`"mask"` instead — see [features-color-modes](features-color-modes.md).

## Tailwind CSS Plugin

Render icons purely with CSS classes — no JS component, icons become part of the stylesheet.

### Tailwind v4 (`@iconify/tailwind4`)

CSS-based config:

```css
@import "tailwindcss";
@plugin "@iconify/tailwind4";
```

### Tailwind v3 (`@iconify/tailwind`)

```js
// tailwind.config.js
import { addIconSelectors, addDynamicIconSelectors } from '@iconify/tailwind'

export default {
  plugins: [
    addIconSelectors(['mdi', 'lucide']),  // static selectors for named sets
    addDynamicIconSelectors(),             // any icon, on demand
  ],
}
```

### Class patterns

| Pattern | Example | Behavior |
|---------|---------|----------|
| Dynamic selector | `icon-[mdi-light--home]` | Any icon; `--` separates prefix and name |
| Clean selector | `iconify mdi-light--home` | Uses `iconify` + `prefix--name` |
| Colored icon | `iconify-color mdi-light--home` | Preserves palette colors |

```html
<!-- dynamic -->
<span class="icon-[mdi-light--home]"></span>

<!-- clean -->
<span class="iconify mdi-light--home"></span>
```

## Key Points

- CSS-based rendering trades runtime JS for stylesheet size — best when you have a fixed icon set.
- Tailwind dynamic selectors (`addDynamicIconSelectors`) support any icon on demand; static selectors (`addIconSelectors`) are smaller for known sets.
- The `components-css` packages are experimental — prefer the web component's `mode` attribute for CSS rendering in app code.
- Tailwind class name separator is `--` (prefix`--`name), while the component icon-name separator is `:`.

<!--
Source references:
- https://iconify.design/docs/usage/css/
- https://iconify.design/docs/usage/css/tailwind/
- sources/iconify/README.md
- sources/iconify/components-css/
-->
