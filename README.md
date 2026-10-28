# Toolome — AI tools for biology

A curated, hand-verified directory of AI tools for single-cell, spatial omics, protein design, genomics, drug discovery, bio agents, cloud labs, imaging, datasets, sequencing, proteomics/metabolomics, CRISPR, RNA, microbiome and clinical LLMs.

- Data: `src/data/tools.json` (edit by hand; check with `npm run check`. Never regenerate it from a script. `scripts/verify.py` is deprecated and only calls the read-only audit)
- Stack: Astro static site (`npm run build` → `dist/`), deployed on GitHub Pages (gh-pages branch, custom domain https://toolome.bio). Pushing to main does NOT deploy: run `scripts/deploy-pages.sh` manually after pushing
- Generated: `sitemap.xml`, `robots.txt`, `llms.txt`, per-tool JSON-LD `SoftwareApplication`
- Submit a tool: open a GitHub issue

## About: non-commercial, open data

- The site code and the full dataset are public in this repository. The dataset is `src/data/tools.json`.
- No ads, no analytics or tracking scripts, no affiliate links, and no paid or sponsored listings. No account is needed to browse. Nothing on the site is sold.
- Inclusion is editorial, not paid. A tool is listed only if its core method uses machine learning (or it is a dataset/benchmark built for ML), it is influential (notable lab or venue, or meaningful adoption), and its facts are confirmed from primary sources: license via the GitHub API, venue and year via Crossref/arXiv. Full rules: [`INCLUSION.md`](INCLUSION.md).
- Links are checked daily by an automated job.
- Submit a tool or a correction by opening a [GitHub issue](https://github.com/YonghaoZhao722/toolome/issues).

Requires Node 22+. See `OPERATIONS.md` for the daily/weekly routine.

## Deploy & config
`scripts/deploy-pages.sh` builds and publishes to the `gh-pages` branch. Optional settings in `site.config.json` (or env vars):
- `googleSiteVerification` (`GOOGLE_SITE_VERIFICATION`): adds the Search Console `google-site-verification` meta tag.
- `customDomain` (`CUSTOM_DOMAIN`): writes `CNAME` and builds at the domain root. Also set the domain in repo Settings → Pages and add DNS records.
