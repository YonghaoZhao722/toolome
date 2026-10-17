# Toolome inclusion rules

1. **AI/ML required.** The tool's core method must use machine learning: deep learning, neural networks, foundation models, LLMs,
   or trained/learned models (incl. classical ML classifiers such as random forests or gradient boosting), or it is a dataset/benchmark
   built for training or evaluating ML models. Classical bioinformatics is excluded: aligners, assemblers, quantifiers, file/format
   utilities, purely statistical/Bayesian methods without learned predictors, graph/diffusion embeddings, matrix factorization,
   workflow engines, visualization and databases.
   - Not AI: samtools, STAR, kallisto, Nextflow, MMseqs2, Scanorama, PHATE.
   - AI: scGen, SpaGCN, LigandMPNN, ProtTrans, CellBender.
   Platforms, cloud labs and agents qualify when the product centers on AI models or agents.
2. **Influential.** Notable lab/company, strong peer-reviewed venue, or meaningful adoption (stars/downloads), or widely discussed.
3. **Verified.** Every fact from a primary source: repo/license via GitHub API, venue/year via Crossref/arXiv (leave unlabeled if
   unconfirmable), first public date = earliest of preprint, paper or repo creation.
4. **No duplicates** (check names, aliases, repo URLs). New versions of listed tools are updates, not new entries.
5. **Copy:** never write "free" (say "no signup"); concise, accurate descriptions.
6. **Cap:** at most 10 tools per category per first-release year.
7. Judgment calls go to Jev (scripts/jev.py) with full context; Jev is a second opinion, confirmed against sources.
