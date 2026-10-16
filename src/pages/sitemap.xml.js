import { tools, CATS, PAIRS, pairSlug } from '../lib/site.js';
export function GET({ site }) {
  const b = new URL(import.meta.env.BASE_URL, site).href.replace(/\/$/, '');
  const p = ['/', '/submit/', ...Object.keys(CATS).map(c => `/category/${c}/`), ...tools.map(t => `/tools/${t.slug}/`), ...PAIRS.map(x => `/compare/${pairSlug(x)}/`)];
  return new Response(`<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${p.map(x => `<url><loc>${b}${x}</loc></url>`).join('')}</urlset>`);
}
