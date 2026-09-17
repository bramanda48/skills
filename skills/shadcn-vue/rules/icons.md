# Icons

**Default icon framework is Iconify** via `@iconify/vue`. Render icons by name string with the `<Icon>` component — e.g. `<Icon icon="lucide:search" />`. Never import from per-library Vue packages (`@lucide/vue`, `@tabler/icons-vue`, etc.) in code you write.

> Iconify is string-first (`prefix:name`), so the icon name is data, not a component import. This keeps icon choice decoupled from the bundler and lets you swap sets without touching imports.

---

## Icons in Button use data-icon attribute

Add `data-icon="inline-start"` (prefix) or `data-icon="inline-end"` (suffix) to the `<Icon>`. No sizing classes on the icon. The `<Icon>` renders its SVG as a direct child of the Button, so the Button's `data-icon` CSS handles spacing.

**Incorrect:**

```html
<Button>
  <Icon icon="lucide:search" class="mr-2 size-4" />
  Search
</Button>
```

**Correct:**

```html
<Button>
  <Icon icon="lucide:search" data-icon="inline-start" />
  Search
</Button>

<Button>
  Next
  <Icon icon="lucide:arrow-right" data-icon="inline-end" />
</Button>
```

---

## No sizing classes on icons inside components

Components handle icon sizing via CSS. Don't add `size-4`, `w-4 h-4`, or other sizing classes to icons inside `Button`, `DropdownMenuItem`, `Alert`, `Sidebar*`, or other shadcn components. Unless the user explicitly asks for custom icon sizes.

**Incorrect:**

```html
<Button>
  <Icon icon="lucide:search" class="size-4" data-icon="inline-start" />
  Search
</Button>

<DropdownMenuItem>
  <Icon icon="lucide:settings" class="mr-2 size-4" />
  Settings
</DropdownMenuItem>
```

**Correct:**

```html
<Button>
  <Icon icon="lucide:search" data-icon="inline-start" />
  Search
</Button>

<DropdownMenuItem>
  <Icon icon="lucide:settings" />
  Settings
</DropdownMenuItem>
```

This rule applies only to icons rendered **inside** a shadcn component. For standalone `<Icon>` (not wrapped by a shadcn component), provide explicit sizing (`size-4`, `w-5 h-5`, etc.) — the default is `1em` and depends on context font-size, which is often too large or inconsistent.

```html
<!-- Standalone icon: size it explicitly -->
<Icon icon="lucide:search" class="size-4" />
```

---

## Pass icon names as strings, not component objects

With Iconify, the icon is a string (`lucide:check`), not an imported component. Pass the string through a prop and render `<Icon>` in the template. Don't build a component-key lookup map, and don't pass a non-existent component object.

**Incorrect:**

```vue
<script setup lang="ts">
import { CheckIcon, AlertIcon } from "@lucide/vue"

const iconMap = {
  check: CheckIcon,
  alert: AlertIcon,
}

defineProps<{ icon: string }>()
</script>

<template>
  <component :is="iconMap[icon]" />
</template>
```

**Correct:**

```vue
<script setup lang="ts">
import { Icon } from "@iconify/vue"

defineProps<{ icon: string }>() // e.g. "lucide:check"
</script>

<template>
  <Icon :icon="icon" />
</template>

<!-- Usage -->
<StatusBadge icon="lucide:check" />
```

---

## Swap CLI component icon imports to Iconify

The shadcn-vue CLI only supports `lucide`, `tabler`, `hugeicons`, `phosphor`, and `remixicon` as `iconLibrary` — there is no `iconify` option. Components added via `npx shadcn-vue@latest add` will import from the project's configured `iconLibrary` (e.g. `@lucide/vue`). After adding, rewrite those imports and usages to Iconify.

1. Remove the per-library import: `import { SearchIcon } from "@lucide/vue"`.
2. Add the Iconify import: `import { Icon } from "@iconify/vue"`.
3. Replace the component usage with `<Icon icon="<prefix>:<name>" />`, mapping the icon name to the Iconify set (e.g. `lucide` → `lucide:`, `tabler` → `tabler:`).

**Before (CLI-generated):**

```vue
<script setup lang="ts">
import { SearchIcon } from "@lucide/vue"
</script>

<template>
  <Button>
    <SearchIcon data-icon="inline-start" />
    Search
  </Button>
</template>
```

**After (Iconify):**

```vue
<script setup lang="ts">
import { Icon } from "@iconify/vue"
</script>

<template>
  <Button>
    <Icon icon="lucide:search" data-icon="inline-start" />
    Search
  </Button>
</template>
```

> This is part of [workflow step 7](../SKILL.md#workflow) — always review added component files and normalize their icons to Iconify before moving on.

---

## Offline bundling (no API calls)

By default `<Icon>` fetches icon data from the Iconify API at runtime. For offline/production reliability, bundle the icon sets you use via `@iconify-json/<set>` and register them with `addCollection`. Bundled sets resolve locally — no network calls.

```ts
// main.ts (or app entry) — register once
import { addCollection } from '@iconify/vue'
import { icons as lucide } from '@iconify-json/lucide';

addCollection(lucide) // <Icon icon="lucide:home" /> now resolves locally
```

```bash
# Install per-set icon data (tree-shakeable, offline)
pnpm add @iconify-json/lucide
pnpm add @iconify-json/tabler   # add more sets as needed
```

Only bundle sets you actually use. Prefer `lucide` as the default set (closest parity with shadcn-vue's default `lucide` `iconLibrary`).
