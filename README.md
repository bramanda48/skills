# My Collection Skills

A curated collection of [Agent Skills](https://agentskills.io/home) based on [Anthony Fu's skills collection](https://github.com/antfu/skills), extended with additional skills reflecting [BRAM](https://github.com/bramanda48)'s preferences, experience, and best practices for web development.

> [!IMPORTANT]
> This is a proof-of-concept project for generating agent skills from source documentation and keeping them in sync.
> I haven't fully tested how well the skills perform in practice, so feedback and contributions are greatly welcome.

## Installation

```bash
bun x skills add bramanda48/skills --skill='*'
```

or to install all of them globally:

```bash
bun x skills add bramanda48/skills --skill='*' -g
```

Learn more about the CLI usage at [skills](https://github.com/vercel-labs/skills).

## Skills

This collection is aim to be a one-stop collection. It includes skills from different sources with different scopes.

### Hand-maintained Skills

> Opinionated

Manually maintained by me with his preferred tools, setup conventions, and best practices.

| Skill | Description |
|-------|-------------|
| [os-awareness](skills/os-awareness) | Detect the user's OS and use the correct CLI tools, shell commands, and path conventions for that platform |
| [conventional-commits](skills/conventional-commits) | Format commit messages using the Conventional Commits specification for automated changelogs and semantic versioning |
| [shadcn-vue](skills/shadcn-vue) | Manage shadcn-vue components and projects — adding, searching, fixing, debugging, styling, and composing UI |

### Skills Generated from Official Documentation

> Unopinionated but with tilted focus (e.g. TypeScript, ESM, Composition API, and other modern stacks)

Generated from official documentation and fine-tuned by Anthony.

| Skill | Description | Source |
|-------|-------------|--------|
| [vue](skills/vue) | Vue.js core - reactivity, components, composition API | [vuejs/docs](https://github.com/vuejs/docs) |
| [nuxt](skills/nuxt) | Nuxt framework - file-based routing, server routes, modules | [nuxt/nuxt](https://github.com/nuxt/nuxt) |
| [pinia](skills/pinia) | Pinia - intuitive, type-safe state management for Vue | [vuejs/pinia](https://github.com/vuejs/pinia) |
| [vite](skills/vite) | Vite build tool - config, plugins, SSR, library mode | [vitejs/vite](https://github.com/vitejs/vite) |
| [vitepress](skills/vitepress) | VitePress - static site generator powered by Vite | [vuejs/vitepress](https://github.com/vuejs/vitepress) |
| [vitest](skills/vitest) | Vitest - unit testing framework powered by Vite | [vitest-dev/vitest](https://github.com/vitest-dev/vitest) |
| [iconify](skills/iconify) | Iconify icon framework — web component, customisations, color modes, offline usage, Tailwind | [iconify/iconify](https://github.com/iconify/iconify) |
| [hono](skills/hono) | Hono — small, ultrafast web framework on Web Standards for HTTP APIs, edge functions, and multi-runtime apps | [honojs/hono](https://github.com/honojs/hono) |
| [hono-third-party](skills/hono-third-party) | Third-party @hono/* middleware — validators, auth, observability, renderers, OpenAPI tooling | [honojs/middleware](https://github.com/honojs/middleware) |

### Vendored Skills

Synced from external repositories that maintain their own skills.

| Skill | Description | Source |
|-------|-------------|--------|
| [antislop](skills/antislop) (Official) | Anti Slop core — rules for AI coding agents to stop generic AI slop | [miqdadbadjuber/anti-slop](https://github.com/miqdadbadjuber/anti-slop) |
| [antislop-ui](skills/antislop-ui) (Official) | UI/visual — color, layout, components, motion for interfaces | [miqdadbadjuber/anti-slop](https://github.com/miqdadbadjuber/anti-slop) |
| [antislop-copywriting](skills/antislop-copywriting) (Official) | Copy & text — headlines, tone, CTAs, anti-AI-writing patterns | [miqdadbadjuber/anti-slop](https://github.com/miqdadbadjuber/anti-slop) |
| [antislop-human](skills/antislop-human) (Official) | Human & accessibility — contrast, keyboard, focus, states | [miqdadbadjuber/anti-slop](https://github.com/miqdadbadjuber/anti-slop) |
| [antislop-layoutmobile](skills/antislop-layoutmobile) (Official) | Mobile/responsive — grids, overflow, tap targets across screen sizes | [miqdadbadjuber/anti-slop](https://github.com/miqdadbadjuber/anti-slop) |
| [antislop-code](skills/antislop-code) (Official) | Code comments — remove AI-slop comments, keep valuable ones, never touch code | [miqdadbadjuber/anti-slop](https://github.com/miqdadbadjuber/anti-slop) |
| [tsdown](skills/tsdown) (Official) | tsdown - TypeScript library bundler powered by Rolldown | [rolldown/tsdown](https://github.com/rolldown/tsdown) |
| [turborepo](skills/turborepo) (Official) | Turborepo - high-performance build system for monorepos | [vercel/turborepo](https://github.com/vercel/turborepo) |
| [vueuse-functions](skills/vueuse-functions) (Official) | VueUse - 200+ Vue composition utilities | [vueuse/skills](https://github.com/vueuse/skills) |
| [vue-best-practices](skills/vue-best-practices) | Vue 3 + TypeScript best practices | [vuejs-ai/skills](https://github.com/vuejs-ai/skills) |
| [vue-router-best-practices](skills/vue-router-best-practices) | Vue Router best practices | [vuejs-ai/skills](https://github.com/vuejs-ai/skills) |
| [vue-testing-best-practices](skills/vue-testing-best-practices) | Vue testing best practices | [vuejs-ai/skills](https://github.com/vuejs-ai/skills) |
| [cloudflare](skills/cloudflare) (Official) | Discover and choose Cloudflare products for apps, APIs, AI agents, storage, networking, and security | [cloudflare/skills](https://github.com/cloudflare/skills) |
| [cloudflare-agents-sdk](skills/cloudflare-agents-sdk) (Official) | Build, debug, or review Cloudflare Agents SDK applications using the agents package | [cloudflare/skills](https://github.com/cloudflare/skills) |
| [cloudflare-workers-best-practices](skills/cloudflare-workers-best-practices) (Official) | Cloudflare Workers best practices for production applications | [cloudflare/skills](https://github.com/cloudflare/skills) |
| [cloudflare-wrangler](skills/cloudflare-wrangler) (Official) | Run or troubleshoot Wrangler CLI commands and configure Worker projects | [cloudflare/skills](https://github.com/cloudflare/skills) |

## Generate Your Own Skills

Fork this project to create your own customized skill collection.

1. Fork or clone this repository
2. Install dependencies: `bun install`
3. Update `meta.ts` with your own projects and skill sources
4. Run `bun run start cleanup` to remove existing submodules and skills
5. Run `bun run start init` to clone the submodules
6. Run `bun run start sync` to sync vendored skills
7. Ask your agent to `Generate skills for \<project\>` (recommended one at a time to manage token usage)

See [AGENTS.md](AGENTS.md) for detailed generation guidelines.

## License

Skills and the scripts in this repository are [MIT](LICENSE.md) licensed.

Vendored skills from external repositories retain their original licenses - see each skill directory for details.
