# BioStack — AI tools for biology

A curated, hand-verified directory of AI tools for single-cell, spatial omics, protein design, genomics, drug discovery, bio agents, cloud labs, imaging and datasets.

- Data: `src/data/tools.json` (regenerate/verify with `python3 scripts/verify.py`, which curls every URL and GitHub repo and drops dead ones)
- Stack: Astro static site (`npm run build` → `dist/`), deploys free on Vercel (framework preset: Astro) or GitHub Pages (`SITE_URL=https://yonghaozhao722.github.io BASE_PATH=/biostack npm run build`)
- Generated: `sitemap.xml`, `robots.txt`, `llms.txt`, per-tool JSON-LD `SoftwareApplication`
- Submit a tool: open a GitHub issue

Requires Node 22+. See `OPERATIONS.md` for the daily/weekly routine.
