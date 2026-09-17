export interface VendorSkillMeta {
  official?: boolean
  source: string
  skillsPath?: string // Optional custom path to skills directory (default: 'skills')
  skills: Record<string, string> // sourceSkillName -> outputSkillName
}

/**
 * Repositories to clone as submodules and generate skills from source
 */
export const submodules = {
  'vue': 'https://github.com/vuejs/docs',
  'nuxt': 'https://github.com/nuxt/nuxt',
  'vite': 'https://github.com/vitejs/vite',
  'pinia': 'https://github.com/vuejs/pinia',
  'vitest': 'https://github.com/vitest-dev/vitest',
  'vitepress': 'https://github.com/vuejs/vitepress',
  'iconify': 'https://github.com/iconify/iconify',
  'hono': 'https://github.com/honojs/hono',
  'hono-third-party': 'https://github.com/honojs/middleware',
}

/**
 * Already generated skills, sync with their `skills/` directory
 */
export const vendors: Record<string, VendorSkillMeta> = {
  'antislop': {
    official: true,
    source: 'https://github.com/miqdadbadjuber/anti-slop',
    skills: {
      'antislop': 'antislop',
      'antislop-ui': 'antislop-ui',
      'antislop-layoutmobile': 'antislop-layoutmobile',
      'antislop-human': 'antislop-human',
      'antislop-copywriting': 'antislop-copywriting',
      'antislop-code': 'antislop-code',
    },
  },
  'vueuse': {
    official: true,
    source: 'https://github.com/vueuse/vueuse',
    skills: {
      'vueuse-functions': 'vueuse-functions',
    },
  },
  'tsdown': {
    official: true,
    source: 'https://github.com/rolldown/tsdown',
    skills: {
      tsdown: 'tsdown',
    },
  },
  'vuejs-ai': {
    source: 'https://github.com/vuejs-ai/skills',
    skills: {
      'vue-best-practices': 'vue-best-practices',
      'vue-router-best-practices': 'vue-router-best-practices',
      'vue-testing-best-practices': 'vue-testing-best-practices',
    },
  },
  'turborepo': {
    official: true,
    source: 'https://github.com/vercel/turborepo',
    skills: {
      turborepo: 'turborepo',
    },
  },
  'cloudflare': {
    official: true,
    source: 'https://github.com/cloudflare/skills',
    skills: {
      'cloudflare': 'cloudflare',
      'agents-sdk': 'cloudflare-agents-sdk',
      'workers-best-practices': 'cloudflare-workers-best-practices',
      'wrangler': 'cloudflare-wrangler',
    },
  },
}

/**
 * Hand-written skills with Anthony Fu's preferences/tastes/recommendations
 */
export const manual = [
  'conventional-commits',
  'github-cli',
  'os-awareness',
  'shadcn-vue',
]
