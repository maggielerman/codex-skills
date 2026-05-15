import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'Project Docs',
  description: 'Documentation site',
  themeConfig: {
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Getting Started', link: '/getting-started/' },
      { text: 'Features', link: '/features/' },
      { text: 'Development', link: '/development/' },
      { text: 'Database', link: '/database/' },
      { text: 'API', link: '/api/' },
      { text: 'Deployment', link: '/deployment/' },
      { text: 'Contributing', link: '/contributing/' },
    ],
    sidebar: {
      '/': [
        { text: 'Getting Started', link: '/getting-started/' },
        { text: 'Features', link: '/features/' },
        { text: 'Development', link: '/development/' },
        { text: 'Database', link: '/database/' },
        { text: 'API', link: '/api/' },
        { text: 'Deployment', link: '/deployment/' },
        { text: 'Contributing', link: '/contributing/' },
        { text: 'Projects', link: '/PROJECTS/' },
        { text: 'Historical', link: '/historical/' },
      ],
    },
    search: { provider: 'local' },
  },
})
