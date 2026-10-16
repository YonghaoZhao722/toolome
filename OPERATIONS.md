# BioStack operations

Rule: nothing goes out (newsletter, sponsor email, social post) without explicit owner approval.

## Daily (~15 min, automatable)
1. **New releases**: scan bioRxiv/arXiv (q-bio, cs.LG+bio), GitHub trending, X and Hugging Face for new bio-AI tools. Add 1–3 to `src/data/tools.json` with fresh `added` dates (update the `NEW` list in `src/pages/index.astro`). Never add a tool whose URL can't be verified. Never list work under anonymous review.
2. **Link check**: `python3 scripts/verify.py` (curls every URL + GitHub repo, drops dead entries; review the DROP/WARN lines before committing).
3. **One SEO improvement**: e.g. a richer description on one tool page, a category intro paragraph, a comparison page ("Tangram vs cell2location"), internal links, or a fix flagged in Google Search Console.
4. `npm run build` must pass → commit → push (Vercel auto-deploys).

## Weekly report (Mondays)
Tools added/removed, broken links, traffic (Vercel Analytics / Search Console clicks & impressions, top queries), newsletter subscribers, sponsor pipeline status, next week's SEO focus.

## Newsletter workflow (The BioStack Weekly)
1. Draft Sunday: 5–8 new tools, 1 deep-dive, sponsor block (or "Your tool here").
2. **Send draft to owner for approval. Do not send without explicit approval.**
3. After approval: send via Resend (not yet wired; signup form posts to placeholder `/api/subscribe`).

## Sponsor pricing (DRAFT)
Top banner $150/week · Newsletter slot $100/issue. Revisit once traffic > 5k visits/month.

## Sponsor outreach candidates (no emails sent)
| # | Company | Website | Why |
|---|---|---|---|
| 1 | Adaptyv Bio | https://www.adaptyvbio.com | Protein-testing cloud lab; runs design competitions |
| 2 | Tamarind Bio | https://www.tamarind.bio | No-code protein/molecular ML platform |
| 3 | LatchBio | https://latch.bio | Bioinformatics cloud workflows |
| 4 | Rowan | https://www.rowansci.com | Cloud computational chemistry |
| 5 | EvolutionaryScale | https://www.evolutionaryscale.ai | ESM3 API/Forge |
| 6 | Chai Discovery | https://www.chaidiscovery.com | Structure prediction models |
| 7 | Benchling | https://www.benchling.com | R&D cloud / ELN |
| 8 | Emerald Cloud Lab | https://www.emeraldcloudlab.com | Cloud lab |
| 9 | Twist Bioscience | https://www.twistbioscience.com | DNA synthesis for design-test loops |
| 10 | 10x Genomics | https://www.10xgenomics.com | Single-cell & spatial platforms |
| 11 | Vizgen | https://www.vizgen.com | MERFISH spatial platform |
| 12 | Profluent | https://www.profluent.bio | Protein design AI |
| 13 | Cradle | https://www.cradle.bio | Protein engineering SaaS |
| 14 | Owkin | https://www.owkin.com | AI for pathology / biotech |
| 15 | Modal | https://modal.com | Serverless GPUs used by bio-ML teams |
| 16 | Lambda | https://lambda.ai | GPU cloud |
| 17 | Basecamp Research | https://www.basecamp-research.com | Biodiversity data + protein AI |
| 18 | Plasmidsaurus | https://www.plasmidsaurus.com | Sequencing service popular with designers |
| 19 | Latent Labs | https://www.latentlabs.com | Generative protein design |
| 20 | Synthace | https://www.synthace.com | Lab experiment automation |
