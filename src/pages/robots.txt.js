export function GET({ site }) { const b = new URL(import.meta.env.BASE_URL, site).href.replace(/\/$/, '');
 const bots=['*','GPTBot','OAI-SearchBot','ChatGPT-User','PerplexityBot','ClaudeBot','Claude-Web','anthropic-ai','Google-Extended','Googlebot','Bingbot','CCBot','Applebot-Extended'];
 return new Response(bots.map(x=>`User-agent: ${x}\nAllow: /\n`).join('\n')+`\nSitemap: ${b}/sitemap.xml\n`); }
