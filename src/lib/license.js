// Commercial-use class, derived at build time from license + licenseNote + pricing (never hand-edited; ambiguous -> 'unknown').
const PERMISSIVE = /^(MIT|Apache-2\.0|BSD-[23]-Clause(-Clear)?|GPL-[23]\.0|AGPL-3\.0|LGPL-[23]\.[01]|MPL-2\.0|CC-BY-4\.0|CC0-1\.0)$/;
const NC = /\bnc\b|-nc-|non-?commercial|academic|polyform|commons clause|commercial restrictions|research license/i;
const PAIDP = ['Paid','Contact','Freemium'];
export const licenseUse = (t) => {
  const L = t.license||'', n = t.licenseNote||'', p = t.pricing||'', all = L+' '+n;
  if (!L || L==='NOASSERTION' || /not released|see (model|dataset) card|see illumina|terms unclear|out of scope/i.test(n)) return 'unknown';
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

// Finer classes for display/filter: permissive | copyleft | proprietary | non-commercial | mixed | unknown
const STRONG = /^(A?GPL-[23]\.0)$/, WEAK = /^(LGPL-[23]\.[01]|MPL-2\.0)$/;
export const copyleftKind = (t) => STRONG.test(t.license) ? (t.license.startsWith('AGPL')?'agpl':'strong') : WEAK.test(t.license) || (t.license==='Mixed' && /LGPL|MPL/.test(t.licenseNote||'')) ? 'weak' : '';
export const licClass = (t) => {
  const c = licenseUse(t);
  if (c !== 'commercial') return c;
  if (/^(Commercial|Proprietary)$/.test(t.license)) return 'proprietary';
  return copyleftKind(t) ? 'copyleft' : 'permissive';
};
export const LICCLS = [
  ['permissive','Permissive','Permissive (commercial OK)'],
  ['copyleft','Copyleft','Copyleft (commercial OK, share-alike)'],
  ['proprietary','Proprietary','Proprietary (paid or negotiated license)'],
  ['non-commercial','Non-commercial','Non-commercial'],
  ['mixed','Mixed','Mixed (code vs weights differ)'],
  ['unknown','Unknown','Unknown'] ];
export const licBadge = (t) => { const k=licClass(t); if (k==='copyleft') return copyleftKind(t)==='weak' ? 'Weak copyleft (commercial OK, share-alike)' : 'Copyleft (commercial OK, share-alike)'; return LICCLS.find(x=>x[0]===k)[2]; };
export const licAllows = (t) => ({
  permissive: 'Closed-source commercial use allowed; keep the license and copyright notices.',
  copyleft: {agpl:'Commercial use allowed; derived code, including code run as a network service, must be released under the same license.', strong:'Commercial use allowed; derived code you distribute must be released under the same license.', weak:'Commercial use allowed; changes to the licensed files themselves must be released; your own code linking to it can stay closed.'}[copyleftKind(t)],
  proprietary: 'Commercial use under a paid or negotiated license from the vendor.',
  'non-commercial': 'No commercial use.',
  mixed: licParts(t).code ? `Code (${licParts(t).code}) allows commercial use; the weights or hosted service do not.` : 'Components are under different terms; some do not allow commercial use.',
  unknown: 'Unclear; check the source before any commercial use.' })[licClass(t)];
const SPDX = /^(MIT|Apache-2\.0|BSD-[23]-Clause(-Clear)?|A?GPL-[23]\.0|LGPL-[23]\.[01]|MPL-2\.0|CC-BY-4\.0|CC0-1\.0|CC-BY-NC(-SA|-ND)?-4\.0|PolyForm-Strict-1\.0)$/;
// Code vs weights, only when the data states them.
export const licParts = (t) => {
  const n = t.licenseNote||'', segs = n.split(';').map(s=>s.trim()).filter(Boolean);
  let code = SPDX.test(t.license) ? t.license : '', weights = '';
  if (t.license==='Mixed') for (const s of segs) { if (/\(code\)|code\)/i.test(s)) code = s.replace(/\s*\((Census )?code\)/i,''); if (/weights|model\)/i.test(s)) weights = weights ? weights+'; '+s : s; }
  else { const w = segs.filter(s=>/weights|checkpoints|parameters/i.test(s)&&!/not released|full code|^README/i.test(s));
    if (w.length && w.every(x=>/^(\S+ )?weights$/i.test(x))) code = '';
    if (w.length) weights = w.map(x=>/^(\S+ )?weights$/i.test(x) ? t.license+' ('+x+')' : x).join('; '); }
  if (!weights) { const m = /\(([^)]+)\)/.exec(String(t.specs?.weights||'')); if (m && SPDX.test(m[1].replace(/ /g,'-').replace('Apache-2-0','Apache-2.0').replace('Apache-2.0','Apache-2.0'))) weights = m[1]; }
  return { code, weights };
};
