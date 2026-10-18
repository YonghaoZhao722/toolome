import tools from '../data/tools.json';
import cfg from '../../site.config.json';
// Optional: env GOOGLE_SITE_VERIFICATION overrides site.config.json
export const GSV = process.env.GOOGLE_SITE_VERIFICATION || cfg.googleSiteVerification || '';
export const SITE = { name: 'Toolome', tagline: 'The directory of AI tools for biology', repo: 'https://github.com/YonghaoZhao722/toolome' };
export const CATS = {
 'single-cell': ['Single-cell & foundation models','🧬'], 'spatial': ['Spatial omics','🗺️'], 'protein': ['Protein structure & design','🧪'],
 'genomics': ['Genomics & DNA models','🧾'], 'drug-discovery': ['Drug discovery & molecules','💊'], 'agents': ['Bio LLM agents & copilots','🤖'],
 'cloud-labs': ['Cloud labs & wet-lab services','🏭'], 'imaging': ['Imaging & pathology','🔬'], 'datasets': ['Datasets & benchmarks','📚'],
 'sequencing': ['Sequencing & variant calling','🧷'], 'proteomics': ['Proteomics & metabolomics','⚖️'], 'crispr': ['CRISPR & gene editing','✂️'],
 'rna': ['RNA structure & design','🌀'], 'microbiome': ['Microbiome & metagenomics','🦠'], 'clinical': ['Clinical & biomedical LLMs','🩺'], 'platforms': ['R&D & bioinformatics platforms','🧰'] };
export { tools };
export const base = import.meta.env.BASE_URL.replace(/\/$/, '');
export const u = (p) => base + p;
export const INTRO = {
 'single-cell':'Foundation models and toolkits for single-cell RNA-seq and multi-omics: cell annotation, integration, embeddings and perturbation prediction.',
 'spatial':'Tools for spatial transcriptomics and proteomics: deconvolution, domain detection, alignment, histology-to-expression prediction and spatial data frameworks.',
 'protein':'Structure prediction, protein language models and generative protein/binder design.',
 'genomics':'DNA language models, sequence-to-function models, variant calling and splicing prediction.',
 'drug-discovery':'Molecular property prediction, docking, generative chemistry and cheminformatics libraries.',
 'agents':'LLM agents and research copilots for biology and literature work.',
 'cloud-labs':'Cloud labs, protein testing and wet-lab services you can order programmatically.',
 'imaging':'Cell segmentation, microscopy analysis and computational pathology models.',
 'datasets':'Reference datasets, atlases and benchmarks for AI in biology.',
 'sequencing':'Basecallers, long-read and short-read variant callers, polishing and modified-base detection.',
 'proteomics':'Mass-spec proteomics and metabolomics: DIA search, spectrum and retention-time prediction, de novo peptide sequencing and metabolite annotation.',
 'crispr':'CRISPR guide and pegRNA design, editing-outcome analysis and AI-designed gene editors.',
 'rna':'RNA secondary and 3D structure prediction, RNA foundation models and RNA design.',
 'microbiome':'Metagenomic profiling, binning, MAG quality, taxonomy and virus/plasmid detection.',
 'clinical':'Medical and biomedical language and vision-language models.',
 'platforms':'Hosted R&D, computational-chemistry and bioinformatics workflow platforms that bundle many tools behind one interface.' };
export const PAIRS = [['scgpt','geneformer'],['alphafold-server-alphafold-3','boltz'],['rfdiffusion','bindcraft'],['enformer','borzoi'],['cellpose','stardist'],['chai-1','boltz'],['alphafold-server-alphafold-3','chai-1'],['protenix','boltz'],['openfold3','boltz'],['alphafold2','openfold'],['alphafold2','colabfold'],['alphafold2','rosettafold'],['esm-2-esmfold','prottrans'],['esm3','esm-2-esmfold'],['saprot','esm-2-esmfold'],['rfdiffusion','rfdiffusion2'],['rfdiffusion2','rfdiffusion3'],['ablang2','antiberty'],['scgpt','uce-universal-cell-embeddings'],['geneformer','transcriptformer'],['scvi-tools','harmony'],['scanpy','seurat'],['tangram','cell2location'],['cell2location','rctd-spacexr'],['stagate','graphst'],['bayesspace','spagcn'],['evo-2','evo'],['hyenadna','caduceus'],['dnabert-2','nucleotide-transformer'],['cellpose','cellsam'],['diffdock','autodock-vina'],['chemprop','deepchem'],['deepvariant','clair3'],['dorado','bonito'],['metaphlan','kraken2'],['semibin','vamb'],['viennarna','eternafold'],['casanovo','instanovo'],['alphadia','dia-nn'],['rhofold','rna-fm']];
export const bySlug = Object.fromEntries(tools.map(t=>[t.slug,t]));
export const pairSlug = ([a,b]) => `${bySlug[a].slug}-vs-${bySlug[b].slug}`;

export const licText = (t) => !t.licenseNote ? t.license : (['Custom','Mixed','NOASSERTION'].includes(t.license) ? t.licenseNote : `${t.license} (${t.licenseNote})`);
export const starsOf = (t) => t.github && t.specs?.stars!=null ? t.specs.stars : -1;
export const catsOf = (t) => [t.category, ...(t.alsoIn||[])];
export const inCat = (t,c) => catsOf(t).includes(c);
export const dt = (t) => t.released||t.firstReleased||'';
export const byNewest = (l) => [...l].sort((a,b)=> (dt(a)&&dt(b))? dt(b).localeCompare(dt(a))||a.name.toLowerCase().localeCompare(b.name.toLowerCase()) : dt(a)?-1 : dt(b)?1 : a.name.toLowerCase().localeCompare(b.name.toLowerCase()));

export const SHORT = {'single-cell':'single-cell','spatial':'spatial omics','protein':'protein design','genomics':'genomics','drug-discovery':'drug discovery','agents':'agents','cloud-labs':'cloud labs','imaging':'imaging','datasets':'datasets','sequencing':'sequencing','proteomics':'proteomics/metabolomics','crispr':'CRISPR','rna':'RNA','microbiome':'microbiome','clinical':'clinical LLMs','platforms':'R&D platforms'};
export const catList = () => { const n=Object.keys(CATS).map(k=>SHORT[k]||k); return n.slice(0,-1).join(', ')+' and '+n.at(-1); };
export const PAIR_BLURB = {
 'scgpt-geneformer':'Two single-cell foundation models: generative pretraining vs rank-based gene embeddings.',
 'alphafold-server-alphafold-3-boltz':'Hosted AlphaFold 3 vs an open-source biomolecular structure model.',
 'rfdiffusion-bindcraft':'Diffusion-based backbone design vs AlphaFold-guided binder hallucination.',
 'enformer-borzoi':'Sequence-to-function models predicting gene expression from DNA.',
 'cellpose-stardist':'Two widely used deep-learning cell segmentation tools.',
 'chai-1-boltz':'Two open AlphaFold 3-class structure prediction models.',
 'alphafold-server-alphafold-3-chai-1':'Hosted AlphaFold 3 vs an open multimodal structure prediction model.',
 'protenix-boltz':'A trainable PyTorch AlphaFold 3 reproduction vs open biomolecular interaction models.',
 'openfold3-boltz':'An open AlphaFold3-style preview model vs open biomolecular interaction models.',
 'alphafold2-openfold':'DeepMind’s AlphaFold2 vs its trainable PyTorch reproduction.',
 'alphafold2-colabfold':'AlphaFold2 vs the MMseqs2 + AlphaFold Colab workflow built on it.',
 'alphafold2-rosettafold':'Two protein structure predictors: AlphaFold2 and the Baker lab’s three-track network.',
 'esm-2-esmfold-prottrans':'Two families of protein language models used for embeddings.',
 'esm3-esm-2-esmfold':'Multimodal generative ESM3 vs the earlier ESM-2 / ESMFold models.',
 'saprot-esm-2-esmfold':'A structure-aware protein language model vs sequence-only ESM-2.',
 'rfdiffusion-rfdiffusion2':'Backbone and binder diffusion vs atom-level enzyme active-site scaffolding.',
 'rfdiffusion2-rfdiffusion3':'Two Baker lab diffusion design models: enzyme scaffolding vs all-atom binder and enzyme design.',
 'ablang2-antiberty':'Two antibody language models: paired-chain vs BERT-style on OAS sequences.',
 'scgpt-uce-universal-cell-embeddings':'Two single-cell foundation models: generative pretraining vs cross-species universal embeddings.',
 'geneformer-transcriptformer':'Two single-cell transformers: human transcriptomes vs cross-species generative training.',
 'scvi-tools-harmony':'Two approaches to single-cell integration: deep generative models vs fast batch correction.',
 'scanpy-seurat':'The main single-cell analysis toolkits for Python and R.',
 'tangram-cell2location':'Two methods for mapping cell types onto spatial transcriptomics data.',
 'cell2location-rctd-spacexr':'Two cell type deconvolution methods for spatial transcriptomics.',
 'stagate-graphst':'Two graph neural network methods for spatial domain identification.',
 'bayesspace-spagcn':'Bayesian clustering vs graph convolution for spatial domains.',
 'evo-2-evo':'Evo 2 vs the original Evo genomic foundation model.',
 'hyenadna-caduceus':'Two long-range DNA language models at single-nucleotide resolution.',
 'dnabert-2-nucleotide-transformer':'Two multi-species DNA foundation models.',
 'cellpose-cellsam':'Two generalist cell segmentation models.',
 'diffdock-autodock-vina':'A diffusion docking model vs a classical docking engine.',
 'chemprop-deepchem':'A molecular property prediction library vs a broad deep learning toolkit for chemistry.',
 'deepvariant-clair3':'Two deep learning small-variant callers for short and long reads.',
 'dorado-bonito':'Oxford Nanopore’s production basecaller vs its research basecaller.',
 'metaphlan-kraken2':'Marker-gene profiling vs k-mer classification for metagenomes.',
 'semibin-vamb':'Two deep learning metagenomic binners.',
 'viennarna-eternafold':'Two RNA secondary structure packages: ViennaRNA vs Eterna-trained EternaFold.',
 'casanovo-instanovo':'Two transformer models for de novo peptide sequencing.',
 'alphadia-dia-nn':'Two DIA proteomics search engines.',
 'rhofold-rna-fm':'RNA 3D structure prediction vs an RNA foundation model.'};
export const pairBlurb = p => PAIR_BLURB[p.join('-')] || '';
export const pairsFor = slug => PAIRS.filter(p=>p.includes(slug));
export const pairsForCat = cat => PAIRS.filter(p=>p.some(s=>bySlug[s].category===cat));
export const SPEC_FIELDS = {
 'protein':[['task','Task'],['modalities','Modalities'],['msa','MSA required'],['weights','Open weights'],['gpu','GPU need']],
 'single-cell':[['corpus','Pretraining corpus'],['architecture','Architecture'],['tasks','Tasks'],['species','Species']],
 'genomics':[['context','Input length / context'],['resolution','Resolution'],['species','Species'],['tasks','Tasks']],
 'imaging':[['dims','2D / 3D'],['modality','Modality'],['segType','Segmentation type']],
 'spatial':[['platforms','Platforms supported'],['resolution','Resolution'],['tasks','Tasks']],
 'agents':[['backbone','Model backbone'],['actions','Tools / actions'],['wetlab','Wet-lab integration']],
 'datasets':[['size','Size'],['modality','Modality'],['access','Access']],
 'drug-discovery':[['task','Task'],['representation','Molecular representation'],['weights','Open weights']],
 'cloud-labs':[['services','Services'],['ordering','Ordering (API / web)'],['turnaround','Turnaround']],
 'sequencing':[['platform','Sequencing platform'],['task','Task'],['variants','Variant types']],
 'proteomics':[['acquisition','Acquisition (DDA / DIA)'],['task','Task'],['input','Input']],
 'crispr':[['system','Editing system'],['task','Task'],['organism','Organisms']],
 'rna':[['task','Task'],['level','Structure level (2D / 3D)'],['input','Input']],
 'microbiome':[['input','Input'],['task','Task'],['database','Reference database']],
 'clinical':[['modality','Modality'],['baseModel','Base model'],['params','Parameters']],
 'platforms':[['focus','Focus'],['access','Access (web / API / SDK)'],['compute','Compute']] };
export const COMMON_FIELDS = [['license','License'],['pricing','Pricing'],['date','Released'],['paper','Paper'],['github','GitHub'],['stars','GitHub stars'],['interface','Interface']];
export const specRows = (t) => {
  const s=t.specs||{};
  const c={license:licText(t),pricing:t.pricing,date:t.released||t.firstReleased||'',paper:t.paper||'',github:t.github||'',stars:s.stars!=null?s.stars.toLocaleString('en-US'):'',interface:s.interface||''};
  return [...(SPEC_FIELDS[t.category]||[]).map(([k,l])=>[l,s[k]||'']), ...COMMON_FIELDS.map(([k,l])=>[l,c[k]])];
};
export const cmpData = () => ({ fields:SPEC_FIELDS, common:COMMON_FIELDS, cats:Object.fromEntries(Object.entries(CATS).map(([k,v])=>[k,v[0]])),
  tools:Object.fromEntries(tools.map(t=>[t.slug,{n:t.name,c:t.category,cs:catsOf(t),d:t.description,s:t.specs||{},l:licText(t),p:t.pricing,r:t.released||t.firstReleased||'',pa:t.paper||'',g:t.github||'',src:t.specsSources||[],rows:specRows(t),u:t.url,pp:t.paper||''}])) });

export { licenseUse, LICUSE, licUseLabel, licClass, LICCLS, licBadge, licAllows, licParts, copyleftKind, licAnswer } from './license.js';
