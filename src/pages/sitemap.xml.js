import LM from '../data/lastmod.json';
import { tools, CATS, PAIRS, pairSlug, bySlug } from '../lib/site.js';
export function GET({ site }) {
  // lastmod = last real data change per tool (scripts/data_dates.py, from git history), not link-check or deploy dates
  const lm = t => LM[t.slug] || t.added;
  const b = new URL(import.meta.env.BASE_URL, site).href.replace(/\/$/, '');
  const mx = a => a.filter(Boolean).sort().at(-1);
  const all = mx(tools.map(lm));
  const cat = c => mx(tools.filter(t => t.category === c || (t.alsoIn||[]).includes(c)).map(lm)) || all;
  const p = [['/', all], ['/submit/', all], ['/compare/', all], ['/licenses/', all], ['/about/', '2026-10-26'], ...Object.keys(CATS).map(c => [`/category/${c}/`, cat(c)]), ...tools.map(t => [`/tools/${t.slug}/`, lm(t)]), ...PAIRS.map(x => [`/compare/${pairSlug(x)}/`, mx(x.slice(0,2).map(s => bySlug[s] && lm(bySlug[s]))) || all])];
  return new Response(`<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${p.map(([x, d]) => `<url><loc>${b}${x}</loc>${d ? `<lastmod>${d}</lastmod>` : ''}</url>`).join('')}</urlset>`, { headers: { 'Content-Type': 'application/xml' } });
}
