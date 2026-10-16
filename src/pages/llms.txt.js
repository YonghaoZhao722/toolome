import { tools, CATS } from '../lib/site.js';
export function GET({ site }) {
  const b = new URL(import.meta.env.BASE_URL, site).href.replace(/\/$/, '');
  let s = `# BioStack\n\n> Curated, hand-verified directory of AI tools for biology (${tools.length} tools). Each tool page lists URL, GitHub, paper, license and pricing.\n\n`;
  for (const [k, [n]] of Object.entries(CATS)) { s += `## ${n}\n\n`; for (const t of tools.filter(t => t.category === k)) s += `- [${t.name}](${b}/tools/${t.slug}/): ${t.description}\n`; s += '\n'; }
  return new Response(s);
}
