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
