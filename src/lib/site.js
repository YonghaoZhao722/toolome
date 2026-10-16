import tools from '../data/tools.json';
import cfg from '../../site.config.json';
// Optional: env GOOGLE_SITE_VERIFICATION overrides site.config.json
export const GSV = process.env.GOOGLE_SITE_VERIFICATION || cfg.googleSiteVerification || '';
export const SITE = { name: 'Toolome', tagline: 'The directory of AI tools for biology', repo: 'https://github.com/YonghaoZhao722/toolome' };
export const CATS = {
 'single-cell': ['Single-cell & foundation models','🧬'], 'spatial': ['Spatial omics','🗺️'], 'protein': ['Protein structure & design','🧪'],
 'genomics': ['Genomics & DNA models','🧾'], 'drug-discovery': ['Drug discovery & molecules','💊'], 'agents': ['Bio LLM agents & copilots','🤖'],
 'cloud-labs': ['Cloud labs & wet-lab services','🏭'], 'imaging': ['Imaging & pathology','🔬'], 'datasets': ['Datasets & benchmarks','📚'] };
export { tools };
export const base = import.meta.env.BASE_URL.replace(/\/$/, '');
export const u = (p) => base + p;
export const INTRO = {
 'single-cell':'Foundation models and toolkits for single-cell RNA-seq and multi-omics: cell annotation, integration, embeddings and perturbation prediction.',
 'spatial':'Tools for spatial transcriptomics and proteomics: deconvolution, domain detection, alignment and spatial data frameworks.',
 'protein':'Structure prediction, protein language models and generative protein/binder design.',
 'genomics':'DNA language models, sequence-to-function models, variant calling and splicing prediction.',
 'drug-discovery':'Molecular property prediction, docking, generative chemistry and cheminformatics libraries.',
 'agents':'LLM agents and research copilots for biology and literature work.',
 'cloud-labs':'Cloud labs, protein testing and wet-lab services you can order programmatically.',
 'imaging':'Cell segmentation, microscopy analysis and computational pathology models.',
 'datasets':'Reference datasets, atlases and benchmarks for AI in biology.' };
export const PAIRS = [['scgpt','geneformer'],['alphafold-server-alphafold-3','boltz'],['rfdiffusion','bindcraft'],['enformer','borzoi'],['cellpose','stardist'],['chai-1','boltz']];
export const bySlug = Object.fromEntries(tools.map(t=>[t.slug,t]));
export const pairSlug = ([a,b]) => `${bySlug[a].slug}-vs-${bySlug[b].slug}`;
