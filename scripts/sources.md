# Harvest sources (machine-readable curated lists)

Picked for maintenance (pushed 2025–2026) and stars; parsed from README Markdown via GitHub API.
Each entry lists repo links (`github.com/owner/repo`) with a description line and section header.

| Source | Stars | Last push | Scope |
|---|---|---|---|
| seandavi/awesome-single-cell | 3.9k | 2026-10 | single-cell tools |
| danielecook/Awesome-Bioinformatics | 4.3k | 2026-09 | general bioinformatics |
| Peldom/papers_for_protein_design_using_DL | 2.0k | 2026-08 | protein design |
| OmicsML/awesome-foundation-model-single-cell-papers | 0.6k | 2026-10 | single-cell FMs |
| davidliwei/awesome-CRISPR | 0.6k | 2026-07 | CRISPR tools |
| apeterswu/Awesome-Bio-Foundation-Models | 0.3k | 2025-05 | DNA/RNA/protein FMs |
| FreedomIntelligence/Awesome-AI4Med | 2.9k | 2026-08 | medical AI / clinical LLMs |
| aristoteleo/awesome-bioagent-papers | 0.1k | 2026-02 | bio agents |
| wrab12/awesome-spatial-transcriptomics | 48 | 2026-10 | spatial omics |
| crazyhottommy/awesome-long-reads | 24 | 2025-03 | long-read sequencing |
| AspirinCode/awesome-AI4MolConformation-MD | 0.3k | 2026-10 | molecular modeling / drug discovery |

AI/ML requirement: harvest_jev.py asks Jev a separate AI/ML question per candidate and drops non-AI tools (see INCLUSION.md).

Not used: bio.tools/ELIXIR (very broad, mostly non-AI, weak notability signal); OmicsTools / BioAI Nav (no public machine-readable API found);
HF collections (model cards lack consistent repo/paper metadata). Enrichment: GitHub GraphQL (stars, license, created, releases),
Crossref/arXiv (paper venue/year; title must contain the tool name), Jev (category + include).
