from pathlib import Path
import json, subprocess
from datetime import datetime, timezone
r=Path('.')
s=json.loads((r/'SECTION3_CONTINUATION_STATE.json').read_text(encoding='utf-8-sig'))
commit=subprocess.check_output(['git','-c','safe.directory='+str(r.resolve()).replace('\\','/'),'rev-parse','HEAD'],text=True).strip()
s.update(verified_code_commit=commit,verified_module_count=709,verified_axiom_audit_count=610,latest_full_build_utc='2026-10-06T17:32:15.0923380Z',pending_full_build_axiom_audit_count=None,pending_snapshot_status='Sixth full snapshot verified; 709 modules / 610 ordered audits / 136 certificate batches. Pending independently checked eta, moment power bounds and physical age mixture remain scratch. Section 3 incomplete.')
(r/'SECTION3_CONTINUATION_STATE.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
report=r/'docs/R077_完整研究记录.md'
t=report.read_text(encoding='utf-8-sig').replace('截至 12:38 UTC 的状态以末节为准','最新状态以末节为准')
t+='''\n## 17:33 UTC：第六次完整核验\n\n完整构建在 2026-10-06T17:32:15.0923380Z 成功结束：709 模块、610 条按顺序一一匹配的 kernel 公理输出、136 证书批次；verify_snapshot.py 的源码/构建/公理核对全部通过，零错误。仅 propext、Classical.choice、Quot.sound。代码提交 COMMIT。继续同轮 R077，实际墙钟已超过 7 小时 25 分钟；本轮未结束。\n\n本次新增可靠结论：实际尺寸出生级数的双边尺度估计及全尺寸双常数幂律，逐点 δ=logρ/(logm−logρ)；实际有限均匀根半径尾收敛到半径出生级数，临界累积尾双边 r^{−(logm−logρ)/logℓ}，点概率是相邻尾差且总和为一；低阶根簇矩在临界点两侧收敛到同一个有限正值；任意有限字任意切割的循环置换保持实际不动点、响应、实相似和三个增长商；tie/gem 两规则的全部 Classical 图条件。新增实际均匀根 age 法则、有限簇指示函数极限、独立 spine/初始内部顶点/Bernoulli 配置空间和 prefix 对应也纳入此次完整检查。\n\n证明要点：尺寸结论来自已证同一实际质量极限的平滑正密度 LLT 和全阶点尾界；半径下界由第二代内部边仅该粗边开通事件及胞腔等距性给出，其根贡献通过有限出生部分和下界到极限，未误当成单层出生；上界来自胞腔直径及边界质量。\n\n完整快照之外：η 的任意固定距离窗口双常数估计及其指数 5 个模块、近临界实际根簇矩幂发散/对数发散 5 个模块、实际 age 混合无限图空间 4 个模块和端点嵌入 1 个模块均已单独通过，但尚未迁移；diamond 几何第一模块单独通过，其余仍在核验。主控半径点指数条件值与通用非存在分析仍为未验草稿，归档中明确放在 working-drafts。\n\n精确缺口：无限均匀根图尺寸/半径律与热力学出生级数的识别、几乎处处局部有限性；矩指数 γ/Δ 及共同 gap 分类；diamond 实际半径尖峰与点指数不存在；半径点指数若存在的值；Wheatstone 第三响应的强双常数幂界；tie/gem 小数表与电阻例证；最终物理 critical-exponent universality class 充要及反例推论。Section 3 未完成。其他对话的 Section 4/5 状态应以项目根目录总索引各自记录为准，本轮不修改其代码。\n\n下一步：完成上述最短证明链，保持三 agent 并行写证明、最多两个 Lean 进程核验，分别通过后再做下一次全闭包核验。没有新的证明失败或撤回；不能把已证热力学极限等同于尚缺识别的无限图定理。\n'''.replace('COMMIT',commit)
report.write_text(t,encoding='utf-8')
p=r/'docs/SECTION3_COVERAGE.md';t=p.read_text(encoding='utf-8-sig');lines=t.splitlines()
for i,line in enumerate(lines):
 if line.startswith('| `def:physical-observables`: infinite volume'):
  lines[i]='| `def:physical-observables`: infinite volume | Partial | Actual direct-limit graph, finite-component indicator convergence, uniform-root age law, product Bernoulli sampled towers and prefix laws are kernel checked; physical size-law identification and almost-sure local finiteness remain |'
 elif line.startswith('| `thm:critical-exponents-dimensions`: β;'):
  lines[i]='| `thm:critical-exponents-dimensions`: β; `thm:delta-eta-dimensions` | Thermodynamic β and δ proved; η individually checked | Actual escaping-mass β is in the 639-module snapshot; actual root-size double power bounds and δ value are in the 709-module snapshot. η final five modules are individually checked scratch. Infinite rooted graph identification remains separate |'
 elif line.startswith('| `prop:annealed-moments`: remaining cases'):
  lines[i]='| `prop:annealed-moments`: remaining cases | In progress | Finite positive two-sided critical continuity below threshold is in the 709-module snapshot. Actual near-critical power/log bounds have passed individually in scratch; logarithmic moment and ratio exponents, common-gap classification and physical graph identification remain |'
 elif line.startswith('| `prop:annealed-radius-tail`'):
  lines[i]='| `prop:annealed-radius-tail` | Cumulative law proved | Actual thermodynamic radius tail, critical double power bounds, actual point law and total mass one are in the 709-module snapshot. Conditional point exponent value, diamond nonexistence and infinite rooted graph identification remain |'
 elif line.startswith('| `lem:transposition-invariance`: two-factor step'):
  lines[i]='| `lem:transposition-invariance`: finite words | `Rule.cyclic_block_word_real_similarity`, `cyclic_block_word_three_growth_values` | Arbitrary word cut, actual mapped fixed point, response, real similarity and three growth fractions included in the 709-module snapshot; factors terminal-symmetric, scale and original interior fixed point, reverse admissibility derived |'
t='\n'.join(lines)+'\n\nSixth full snapshot, 2026-10-06T17:32:15.0923380Z: **709 modules / 610 ordered kernel outputs / 136 certificate batches**, zero errors, only standard logical axioms. This supersedes earlier pending statuses for critical size summation, cumulative radius laws, moment continuity and arbitrary cyclic cuts. The remaining gaps in the updated table remain open.\n'
p.write_text(t,encoding='utf-8')
p=r/'README.md';t=p.read_text(encoding='utf-8-sig');t+='\nCurrent Section 3 checkpoint (R077, 2026-10-06 17:32 UTC): 709 modules / 610 ordered axiom outputs / 136 certificate batches, full verification zero errors. Actual thermodynamic beta, delta and cumulative radius power laws are proved; eta and near-critical strong moment laws are individually checked candidates. Physical infinite-root identification, the remaining point-radius conclusions and final classification are still open. See docs/SECTION3_COVERAGE.md for the current scope; older open-item lists above are historical where superseded.\n';p.write_text(t,encoding='utf-8')
print(commit)
