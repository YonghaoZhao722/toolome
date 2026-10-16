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
 'rna': ['RNA structure & design','🌀'], 'microbiome': ['Microbiome & metagenomics','🦠'], 'clinical': ['Clinical & biomedical LLMs','🩺'] };
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
 'clinical':'Medical and biomedical language and vision-language models.' };
export const PAIRS = [['scgpt','geneformer'],['alphafold-server-alphafold-3','boltz'],['rfdiffusion','bindcraft'],['enformer','borzoi'],['cellpose','stardist'],['chai-1','boltz']];
export const bySlug = Object.fromEntries(tools.map(t=>[t.slug,t]));
export const pairSlug = ([a,b]) => `${bySlug[a].slug}-vs-${bySlug[b].slug}`;

export const dt = (t) => t.released||t.firstReleased||'';
export const byNewest = (l) => [...l].sort((a,b)=> (dt(a)&&dt(b))? dt(b).localeCompare(dt(a))||a.name.toLowerCase().localeCompare(b.name.toLowerCase()) : dt(a)?-1 : dt(b)?1 : a.name.toLowerCase().localeCompare(b.name.toLowerCase()));

export const SHORT = {'single-cell':'single-cell','spatial':'spatial omics','protein':'protein design','genomics':'genomics','drug-discovery':'drug discovery','agents':'agents','cloud-labs':'cloud labs','imaging':'imaging','datasets':'datasets','sequencing':'sequencing','proteomics':'proteomics/metabolomics','crispr':'CRISPR','rna':'RNA','microbiome':'microbiome','clinical':'clinical LLMs'};
export const catList = () => { const n=Object.keys(CATS).map(k=>SHORT[k]||k); return n.slice(0,-1).join(', ')+' and '+n.at(-1); };
