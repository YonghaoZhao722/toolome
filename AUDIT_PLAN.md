# Toolome 全站逻辑问题检查计划

目标：系统性找出"数据前后不一致 / 页面显示不合逻辑"的问题（例如：给了 GitHub 链接却没有 GitHub stars），并让这类问题以后**自动被拦截**，而不是靠人眼发现。

> 本计划只描述"如何检查"。执行阶段再按优先级逐项修复，每类修复单独提交。

---

## 0. 现状摸底（2026-10-16 跑出来的基线数据）

对 `src/data/tools.json`（209 个工具）做了一次快速统计，已经能确认以下问题：

| # | 问题 | 数量 | 例子 |
|---|------|------|------|
| 1 | 有 `github` 但没有 `specs.stars` | 13 | pie, openfold3, tahoe-x1, rfdiffusion3, nucleotide-transformer-v3-ntv3, rnapro, stack, genbio-pathfm, eva, esmfold2-esmc-biohub, opendde, nesso-1, instanovo-fm（基本都是 45eeb3f 那批 gap-fill 新加的） |
| 2 | 完全没有 `specs`（详情页 Specs 表全是 "—"） | 14 | futurehouse-platform, consensus, ginkgo-bioworks, casp, spliceai2, biomistral, kosmos, atlas-2, gpt-rosalind, instanovo-fm … |
| 3 | 没有任何日期（`released`/`firstReleased` 都缺） | 25 | rdkit, alphafold-db, uniprot, cellprofiler, benchling, opentrons … |
| 4 | 两个工具共用同一个 GitHub 仓库 | 2 对 | esm3 & esmfold2-esmc-biohub → `Biohub/esm`；nucleotide-transformer & ntv3 → `instadeepai/nucleotide-transformer`（stars 会重复、需确认是否合理） |
| 5 | license 写法不统一 | 多处 | `Open` / `Custom` / `Mixed` / `Apache-2.0 (code); …` 等 25+ 种写法，无法做筛选或一致性判断 |
| 6 | 冗余字段 `specsSource`（单数）与 `specsSources`（复数）并存 | 182 | 页面只用复数版本，单数是历史遗留 |

**根因级问题（比单条数据错误更严重）：**

- **R1. stars 是手填的，没有任何脚本去拉取/刷新。** 新加工具时只要忘了填就会出现"有链接无 stars"；老工具的 stars 也会随时间过期，`specsChecked` 日期并不代表 stars 是最新的。
- **R2. `scripts/verify.py` 会毁掉数据。** README 和 OPERATIONS.md 都说"用 `verify.py` 重新生成/校验"，但它是从 `scripts/candidates.py`（只有 101 条）**整体重写** `tools.json`：会丢掉 108 个工具，以及所有 `specs`、`firstReleased`、`notability`、`released/source`，并把 `added` 全部改成写死的 `2026-10-15`。按文档的每日流程执行一次就会出大事故。
- **R3. 没有任何构建期校验。** `npm run build` 只要 JSON 能解析就会通过，字段缺失/矛盾不会报错。

---

## 1. 检查分层

问题分四层，从便宜到昂贵依次做：

| 层 | 检查什么 | 方式 | 是否需要网络 |
|----|---------|------|-------------|
| L1 数据一致性 | `tools.json` 内部字段之间的逻辑矛盾 | 新脚本 `scripts/audit.py`，纯本地 | 否 |
| L2 外部事实核对 | 数据和真实世界是否一致（stars、archived、license、链接存活、日期） | `scripts/audit.py --online`，调 GitHub API / curl | 是 |
| L3 渲染结果检查 | 构建出来的 HTML 是否符合预期（字段显示、链接、JSON-LD、sitemap） | 对 `dist/` 做静态分析 + Playwright 抽查 | 否 |
| L4 人工语义审查 | 分类是否正确、描述是否准确、是否值得收录 | 按类别抽样人工过 | 是 |

---

## 2. L1 数据一致性规则（`scripts/audit.py`）

每条规则有编号、严重级别（ERROR 会让检查失败，WARN 只提示），输出 `slug + 规则 + 说明`，最后汇总计数。

### 2.1 字段依赖类（"有 A 就必须有 B"）
- **D1** `github` 非空 → `specs.stars` 必须是正整数（**用户提出的问题**）。ERROR
- **D2** `specs.stars` 存在 → `github` 必须非空（反向检查，防止 stars 来源不明）。ERROR
- **D3** `released` 存在 → `source` 必须存在；`firstReleased` 存在 → `dateSource` 必须存在。ERROR
- **D4** `specs` 存在 → `specsSources` 非空，且 `specsChecked` 存在。ERROR
- **D5** 每个 category 在 `SPEC_FIELDS` 里定义的字段，至少填了一半；全空则 WARN（对应"Specs 表一整列都是 —"）。
- **D6** `pricing` 是 `Open source*` → 应该有 `github`（或其它公开代码地址）；没有则 WARN（"说是开源却找不到代码"）。
- **D7** 没有 `specs` 的工具 → WARN，列入补全清单。
- **D8** 没有任何日期 → WARN（首页"按最新排序"会把它们排到最后，且详情页没有日期行）。

### 2.2 字段互斥 / 矛盾类
- **C1** `pricing` 与 `license` 矛盾：`Open source` 配 `Commercial/Proprietary`；`Paid/Contact` 配 MIT/Apache/BSD 等（需人工判断是否是"开源 SDK + 商业平台"这类合理情况，可加白名单）。WARN
- **C2** license 含 `NC`（non-commercial）但 pricing 是不带 "(non-commercial)" 的 `Open source`。ERROR
- **C3** `specs.weights` 写 "Yes (MIT)" 之类，但括号里的许可证和 `license` 字段不一致。WARN
- **C4** `released` 与 `firstReleased` 同时存在且不一致。WARN
- **C5** `url` 本身就是 GitHub 仓库地址，但 `github` 字段为空或指向另一个仓库。ERROR
- **C6** `specs.interface` 写 "Web" 但 pricing 是 `Open source` 且无 `url` 网站 等不可能组合（规则可以随审查补充）。

### 2.3 格式 / 取值类
- **F1** `github` 必须匹配 `^https://github\.com/[^/]+/[^/]+$`（不能带 `/tree/...`、`.git`、结尾斜杠）。
- **F2** 所有日期是 `YYYY-MM-DD`，且不晚于今天、不早于 1990。
- **F3** `category` 必须在 `CATS` 里；`pricing` 必须在固定枚举里。
- **F4** `license` 规范化：主许可证用 SPDX ID，补充说明另放字段（例如 `licenseNote`），否则 WARN。先出清单，再决定是否改 schema。
- **F5** `tags` 非空、小写、无重复、无空字符串。
- **F6** `slug` 由 `name` 推导规则一致、唯一（现在有 `esm3--evolutionaryscale` 这种双横线 slug，虽然唯一但不美观；改 slug 会改 URL，需要加重定向，单独评估）。
- **F7** `description` 长度区间（如 40–200 字符），不以句号外的标点结尾，不与 name 完全重复。

### 2.4 重复 / 引用类
- **U1** `github` 归一化（小写、去尾斜杠）后重复 → WARN，人工确认是"同仓库多模型"还是重复收录。确认合理的加入白名单。
- **U2** `url` 或 `paper` 重复。WARN
- **U3** `name` 大小写/空格归一化后重复。ERROR
- **U4** `site.js` 里的 `PAIRS` 引用的 slug 必须都存在，且一对的两个工具属于同一 category（compare 页依赖这一点）。ERROR
- **U5** `PAIR_BLURB` 的 key 必须和 `PAIRS` 一一对应。WARN

### 2.5 代码侧逻辑（读代码确认，不是数据规则）
- **K1** `SpecTable.astro` 单工具模式下会隐藏 License/Pricing/Released/Paper/GitHub，但保留 "GitHub stars"：当 stars 缺失时详情页就会出现"上面有 GitHub 链接，下面 stars 是 —"——这正是用户看到的现象。D1 修复后自然消失，但也要确认显示逻辑本身合理（例如没有 github 的工具是否应该干脆不显示 stars 行，而不是显示 "—"）。
- **K2** `compare/index.astro` 的 `rowsOf` 与 `site.js` 的 `specRows` 是两份重复实现，需对比确认两边的字段和格式化完全一致（任何一边改了另一边就会不一致）。
- **K3** `Card.astro` 和 `byNewest` 对 "released 优先于 firstReleased" 的处理是否处处一致（详情页、卡片、排序、llms.txt、JSON-LD）。
- **K4** 详情页 JSON-LD 的 `isAccessibleForFree` 由 pricing 推导：`Freemium`、`Free (research)` 的语义是否正确。
- **K5** 详情页 "Related" 区块直接取 `slice(0,3)`，没有排序，结果依赖 JSON 顺序——确认是否是期望行为。

---

## 3. L2 外部事实核对（`scripts/audit.py --online`）

用 `gh api`（已认证，限额 5000/小时，够用）批量拉取每个 `github` 仓库：

- **G1 stars**：拿到真实 `stargazers_count`。缺失的直接填；已有的与当前值偏差 >20% 或 >500 时更新。同时写入 `specs.starsChecked` 日期，表明 stars 的取数时间。
- **G2 仓库状态**：`archived`、`disabled`、重定向（`html_url` 和记录不同 → 仓库改名/迁移，更新链接）、404。
- **G3 license**：GitHub 识别出的 `license.spdx_id` 与我们的 `license` 字段对比，不一致的列清单人工判断（GitHub 只看代码，模型权重许可证可能另算）。
- **G4 活跃度**：`pushed_at` 超过 2 年 → WARN，考虑在页面标注 "unmaintained" 或降低排序。
- **G5 链接存活**：沿用 `verify.py` 的 curl 逻辑检查 `url`、`paper`、`source`、`dateSource`、`specsSources`，但**只报告不删除**，结果写到报告文件里，由人决定。
- **G6 日期**：对没有日期的 25 个工具，沿用 `backfill_dates.py` 的 GitHub created_at / Crossref / arXiv / bioRxiv 逻辑补全；数据库/平台类（UniProt、PDB、Benchling 等）没有明确"发布日期"的，确定一个统一处理方式（例如允许为空并在页面上不显示日期，而不是硬填）。

输出：`audit-report.json`（加入 `.gitignore`，不提交）+ 终端摘要。

---

## 4. L3 渲染结果检查

`npm run build` 之后对 `dist/` 做检查：

- **H1** 每个工具页：如果 HTML 中有 GitHub 链接行，Specs 表的 "GitHub stars" 单元格不能是 "—"（L1-D1 的端到端版本，防止数据对了但模板没渲染出来）。
- **H2** 页面数量：`dist/tools/*/index.html` 数量 = 工具数；每个 category 页面里卡片数 = 该类工具数；首页总数显示与数据一致。
- **H3** 内部链接全部可解析（所有 `href` 指向 `dist/` 中存在的文件），无 `undefined`、`null`、`NaN`、`[object Object]` 字样出现在任何 HTML/TXT 中。
- **H4** `sitemap.xml` 包含所有工具页、类别页、compare 页，且无多余 URL；`llms.txt` / `llms-full.txt` 工具数与数据一致。
- **H5** JSON-LD 可解析，`license`、`codeRepository` 与页面表格一致。
- **H6** Compare 页（静态 pair 页 + `/compare/?c=…&t=…` 动态页）：用 Playwright 打开 3–5 个组合，确认表格行数、stars 格式、来源链接正确，非法参数（不同类别、不存在的 slug、超过 4 个）有合理提示。
- **H7** 移动端宽度（375px）截图抽查详情页和 compare 页，确认表格不溢出。

---

## 5. L4 人工语义审查（抽样）

自动化抓不到的问题，按类别分批人工过（每批一个 category，约 10–20 个工具）：

- 分类是否正确（参考 8375db4：Atlas 2 原本分错类）。
- description 是否准确、是否夸大、是否和同类重复。
- 是否值得收录（参考 4c33e53/5449963 的 notability 标准），已归档 / 被取代的工具是否需要标注或移除。
- Specs 字段的取值是否真实来自 `specsSources`（随机抽 2–3 条点开核对）。
- 同仓库多条目（U1）是否应该合并。

结果记录为每类一个 checklist，修复和数据改动按类提交，提交信息沿用现有的 `Audit: …` 前缀。

---

## 6. 执行顺序

1. **先修 R2**：把 `verify.py` 改为"读取现有 `tools.json` → 只检查不重写"（或直接停用并更新 README / OPERATIONS.md），防止有人按文档执行时丢数据。优先级最高。
2. **写 `scripts/audit.py`**（L1 全部规则），跑出完整问题清单，确认误报，为合理例外建立白名单（`scripts/audit_allow.json`）。
3. **加 `--online` 模式**（L2），先修 D1：给那 13 个工具补 stars，并顺手刷新全部 stars。
4. **按清单修数据**：ERROR 全修；WARN 按影响排序（缺 specs → 缺日期 → license 规范化 → 其它）。
5. **加 L3 构建后检查**（`scripts/check_dist.py`），在 `package.json` 增加 `"check": "python3 scripts/audit.py && astro build && python3 scripts/check_dist.py"`。
6. **把 `npm run check` 写进 OPERATIONS.md 的每日流程**，替代原来的 `verify.py` 步骤；可选：加一个 GitHub Actions workflow 在 PR 上跑 L1+L3，每周定时跑 L2 刷新 stars。
7. **L4 人工审查**按类别分批进行，可与 1–6 并行。

## 7. 完成标准

- `python3 scripts/audit.py` 0 个 ERROR，WARN 均已修复或在白名单中有理由。
- 所有带 `github` 的工具都有 stars，且 `starsChecked` 不超过 30 天。
- `npm run check` 通过，并已写入日常流程；新增工具时漏填字段会被自动拦下。
- `verify.py` 不再有覆盖数据的风险。
