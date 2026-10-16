export function GET({ site }) { const b = new URL(import.meta.env.BASE_URL, site).href.replace(/\/$/, ''); return new Response(`User-agent: *\nAllow: /\nSitemap: ${b}/sitemap.xml\n`); }
