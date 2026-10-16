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
export const PAIRS = [['scgpt','geneformer'],['alphafold-server-alphafold-3','boltz'],['rfdiffusion','bindcraft'],['enformer','borzoi'],['cellpose','stardist'],['chai-1','boltz']];
export const bySlug = Object.fromEntries(tools.map(t=>[t.slug,t]));
export const pairSlug = ([a,b]) => `${bySlug[a].slug}-vs-${bySlug[b].slug}`;

export const licText = (t) => !t.licenseNote ? t.license : (['Custom','Mixed','NOASSERTION'].includes(t.license) ? t.licenseNote : `${t.license} (${t.licenseNote})`);
export const starsOf = (t) => t.github && t.specs?.stars!=null ? t.specs.stars : -1;
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
 'chai-1-boltz':'Two open AlphaFold 3-class structure prediction models.'};
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
  tools:Object.fromEntries(tools.map(t=>[t.slug,{n:t.name,c:t.category,d:t.description,s:t.specs||{},l:licText(t),p:t.pricing,r:t.released||t.firstReleased||'',pa:t.paper||'',g:t.github||'',src:t.specsSources||[],rows:specRows(t),u:t.url,pp:t.paper||''}])) });
