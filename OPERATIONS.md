# Toolome operations

Rule: nothing goes out (newsletter, outreach email, social post) without explicit owner approval.

## Daily (~15 min, automatable)
1. **New releases**: scan bioRxiv/arXiv (q-bio, cs.LG+bio), GitHub trending, X and Hugging Face for new bio-AI tools. Add 1–3 to `src/data/tools.json` with fresh `added` dates (set `released` + `source` for new releases; the home page shows the last 14 days automatically). Never add a tool whose URL can't be verified. Never list work under anonymous review.
2. **Audit**: `npm run check` (L1 data rules → build → L3 dist checks; must pass with 0 ERROR). Weekly or after adding tools: `python3 scripts/audit.py --online --fix-stars --fix-archived` to refresh GitHub stars/`starsChecked` and the `archived` flag (drives the "Archived repo" badge) and flag archived/moved/404 repos and license mismatches (report only), plus `--links` for a link-liveness report in `audit-report.json`. Never use a script that regenerates `tools.json`.
3. **One SEO improvement**: e.g. a richer description on one tool page, a category intro paragraph, a comparison page ("Tangram vs cell2location"), internal links, or a fix flagged in Google Search Console.
4. `npm run check` must pass → commit → push (Vercel auto-deploys).

## Weekly report (Mondays)
Tools added/removed, broken links, traffic (Vercel Analytics / Search Console clicks & impressions, top queries), newsletter subscribers, next week's SEO focus.

## Newsletter workflow (The Toolome Weekly)
1. Draft Sunday: 5–8 new tools, 1 deep-dive.
2. **Send draft to owner for approval. Do not send without explicit approval.**
3. After approval: send via Resend (not yet wired; signup form posts to placeholder `/api/subscribe`).

