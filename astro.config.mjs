import { defineConfig } from 'astro/config';
export default defineConfig({ site: process.env.SITE_URL || 'https://biostack.vercel.app', base: process.env.BASE_PATH || '/', trailingSlash: 'ignore' });
