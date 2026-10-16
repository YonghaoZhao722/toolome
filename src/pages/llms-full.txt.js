import { tools, CATS, PAIRS, pairSlug } from '../lib/site.js';
export function GET({ site }) {
  const b = new URL(import.meta.env.BASE_URL, site).href.replace(/\/$/, '');
  let s = `# Toolome — full tool data\n\n> Curated, hand-verified directory of AI tools for biology. ${tools.length} tools. Source: ${b}/\n\n`;
  for (const [k, [n]] of Object.entries(CATS)) { s += `## ${n}\n\n`;
    for (const t of tools.filter(t => t.category === k)) { s += `### ${t.name}\n\n${t.description}\n\n- Page: ${b}/tools/${t.slug}/\n- Website: ${t.url}\n`;
      if (t.github) s += `- GitHub: ${t.github}\n`; if (t.paper) s += `- Paper: ${t.paper}\n`;
      s += `- License: ${t.license}\n- Pricing: ${t.pricing}\n- Tags: ${t.tags.join(', ')}\n`;
      if (t.released) s += `- Released: ${t.released} (${t.source})\n`; s += `- Last checked: ${t.lastChecked}\n\n`; } }
  s += `## Comparisons\n\n` + PAIRS.map(p => `- ${b}/compare/${pairSlug(p)}/`).join('\n') + '\n';
  return new Response(s, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
}
