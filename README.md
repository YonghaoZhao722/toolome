# Toolome — AI tools for biology

A curated, hand-verified directory of AI tools for single-cell, spatial omics, protein design, genomics, drug discovery, bio agents, cloud labs, imaging, datasets, sequencing, proteomics/metabolomics, CRISPR, RNA, microbiome and clinical LLMs.

- Data: `src/data/tools.json` (regenerate/verify with `python3 scripts/verify.py`, which curls every URL and GitHub repo and drops dead ones)
- Stack: Astro static site (`npm run build` → `dist/`), deploys free on Vercel (framework preset: Astro) or GitHub Pages via `scripts/deploy-pages.sh` (custom domain https://toolome.bio)
- Generated: `sitemap.xml`, `robots.txt`, `llms.txt`, per-tool JSON-LD `SoftwareApplication`
- Submit a tool: open a GitHub issue

Requires Node 22+. See `OPERATIONS.md` for the daily/weekly routine.

## Deploy & config
`scripts/deploy-pages.sh` builds and publishes to the `gh-pages` branch. Optional settings in `site.config.json` (or env vars):
- `googleSiteVerification` (`GOOGLE_SITE_VERIFICATION`): adds the Search Console `google-site-verification` meta tag.
- `customDomain` (`CUSTOM_DOMAIN`): writes `CNAME` and builds at the domain root. Also set the domain in repo Settings → Pages and add DNS records.
