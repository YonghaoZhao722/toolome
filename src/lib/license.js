// Commercial-use class, derived at build time from license + licenseNote + pricing (never hand-edited; ambiguous -> 'unknown').
const PERMISSIVE = /^(MIT|Apache-2\.0|BSD-[23]-Clause(-Clear)?|GPL-[23]\.0|AGPL-3\.0|LGPL-[23]\.[01]|MPL-2\.0|CC-BY-4\.0|CC0-1\.0)$/;
const NC = /\bnc\b|-nc-|non-?commercial|academic|polyform|commons clause|commercial restrictions|research license/i;
const PAIDP = ['Paid','Contact','Freemium'];
export const licenseUse = (t) => {
  const L = t.license||'', n = t.licenseNote||'', p = t.pricing||'', all = L+' '+n;
  if (!L || L==='NOASSERTION' || /not released|see (model|dataset) card|see illumina/i.test(n)) return 'unknown';
  const ncSig = NC.test(all) || p==='Open source (non-commercial)' || p==='Free (research)';
  if (ncSig) {
    // permissive code, non-commercial weights/services only -> mixed
    if (PERMISSIVE.test(L) && (/weights|web services|virtues/i.test(n) || n==='client') && !/^weights$/i.test(n) && !NC.test(L)) return 'mixed';
    if (L==='Mixed' && /\bMIT\b/.test(n) && NC.test(n)) return 'mixed';
    if (L==='Mixed' && !n) return 'unknown';
    return 'non-commercial';
  }
  if (/^(Commercial|Proprietary)$/.test(L)) return PAIDP.includes(p) ? 'commercial' : 'unknown';
  if (PERMISSIVE.test(L)) {
    if (/separate terms|llama|gemma|health ai|follow each base/i.test(n)) return 'unknown';
    return 'commercial';
  }
  if (L==='Mixed' && n.split(/[;\/]/).every(x=>/MIT|LGPL|CC-BY-4\.0/.test(x))) return 'commercial';
  if (L==='Custom' && /bsd-style|permissive|incl\. commercial|openmdw/i.test(n)) return 'commercial';
  return 'unknown';
};
export const LICUSE = { commercial:'Commercial OK', 'non-commercial':'Non-commercial', mixed:'Mixed terms', unknown:'License unclear' };
export const licUseLabel = (t) => { const c=licenseUse(t); return c==='commercial'&&PAIDP.includes(t.pricing)&&/^(Commercial|Proprietary)$/.test(t.license)?'Commercial license':LICUSE[c]; };
