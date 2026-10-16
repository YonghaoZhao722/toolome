import tools from '../data/tools.json';
export const SITE = { name: 'BioStack', tagline: 'The directory of AI tools for biology', email: 'yonghao@mail.grokbot.com', repo: 'https://github.com/YonghaoZhao722/biostack' };
export const CATS = {
 'single-cell': ['Single-cell & foundation models','🧬'], 'spatial': ['Spatial omics','🗺️'], 'protein': ['Protein structure & design','🧪'],
 'genomics': ['Genomics & DNA models','🧾'], 'drug-discovery': ['Drug discovery & molecules','💊'], 'agents': ['Bio LLM agents & copilots','🤖'],
 'cloud-labs': ['Cloud labs & wet-lab services','🏭'], 'imaging': ['Imaging & pathology','🔬'], 'datasets': ['Datasets & benchmarks','📚'] };
export { tools };
export const base = import.meta.env.BASE_URL.replace(/\/$/, '');
export const u = (p) => base + p;
