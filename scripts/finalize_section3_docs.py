from pathlib import Path
from datetime import datetime,timezone,timedelta
import json,subprocess,re
r=Path(__file__).resolve().parents[1]
a=json.loads((r/'docs/source-audit.json').read_text(encoding='utf-8-sig'))
b=json.loads((r/'docs/build-metadata.json').read_text(encoding='utf-8-sig'))
integrity=json.loads((r/'docs/section3-final-integrity.json').read_text(encoding='utf-8'))
assert a['ok'] and a['module_count']==863 and a['kernel_axiom_output_count']==956
assert b['module_count']==863 and integrity['module_count']==863
commit=subprocess.check_output(['git','-c','safe.directory='+str(r).replace('\\','/'),'rev-parse','HEAD'],cwd=r,text=True).strip()
now=datetime.now(timezone.utc)
p=r/'SECTION3_CONTINUATION_STATE.json';s=json.loads(p.read_text(encoding='utf-8-sig'))
elapsed=(now-datetime.fromisoformat(s['start_utc'].replace('Z','+00:00'))).total_seconds()
s.update(round_status='complete',status='section3_complete',verified_code_commit=commit,verified_module_count=863,verified_axiom_audit_count=956,latest_full_build_utc=b['completed_at_utc'],end_utc=now.isoformat(),end_shanghai=now.astimezone(timezone(timedelta(hours=8))).isoformat(),wall_clock_seconds=elapsed,pending_full_build_module_count=None,pending_full_build_axiom_audit_count=None,pending_final_additions=None,pending_snapshot_status=None)
p.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
status=f'''## Acceptance status

**Section 3 accepted.** The complete canonical import closure passed at
{b['completed_at_utc']}: **863 modules / 956 ordered kernel axiom outputs /
136 finite-certificate batches**. Independent source/build verification has
zero errors; observed axioms are only propext, Classical.choice and Quot.sound.
Code commit: `{commit}`. Post-build source/object hashes, recursive project
dependency fingerprints and the Lean binary hash are sealed in
`section3-final-integrity.json`.

The scope is the original manuscript's **12 independent theorem/lemma/
proposition/corollary statements, five definitions and three examples**,
including the four additional exponents later moved to an appendix. All
Tie/Gem numerical claims, the additional gamma/alpha intervals, electrical
examples and actual Hausdorff classification wrappers are now in this build.
The focused entry is `Universality.Section3`. Proof-display boundaries below
remain explicit; completion concerns the stated conclusions and examples.

'''
p=r/'docs/SECTION3_COVERAGE.md';text=p.read_text(encoding='utf-8-sig')
text=re.sub(r'\n\nLatest verified checkpoint:[^\n]*\n','\n',text)
text=text.replace('# Final coverage map — integrated build pending','# Section 3 — verified final coverage')
text=text[:text.index('## Acceptance status')]+status+text[text.index('## Scope, definitions and conditions'):]
for old,new in [
('integrated pending full verification','verified in the final full build'),
('integrated pending full audit','verified in the final full audit'),
('newly integrated','included in the verified final build'),
('integrated candidate','verified formal library'),
('pending the integrated\nfull audit','included in the final full audit'),
('after the current freeze','completed in the final integration')]:text=text.replace(old,new)
# Keep detailed mappings, replace stale acceptance commentary with the actual
# result rather than counting scratch checks as an integrated proof.
lines=[]
for line in text.splitlines():
    if line.startswith('| ex:tie-gem-similarity, tab:tie-gem-detail'):
        line='| ex:tie-gem-similarity, tab:tie-gem-detail, and the three approximate eigenvalues | Eight canonical Examples/Matrix modules through TieGemCommonSpectrum certify critical points, thermal response, the actual Perron interval (5.708705,5.708725), and a common actual full-spectrum third eigenvalue in (1.42005,1.42015). All included in the final full audit. |'
    if 'two further four-decimal' in line:continue
    lines.append(line)
text='\n'.join(lines)+'\n'
if '## Final acceptance checklist' in text:
    text=text[:text.index('## Final acceptance checklist')]+'''## Final acceptance evidence

All canonical modules are reachable from Audit.lean. The full Lean build,
ordered axiom output, source SHA256 verification, and post-build source/object/
dependency integrity check passed. The final archive is the existing R077 ZIP,
not a new checkpoint file. The project progress index uses its existing ID.

DiamondSusceptibilityNumerical certifies gamma+ in [2.94115,2.94125] and the
actual infinite subcritical susceptibility. WheatstoneAlphaNumerical certifies
raw alpha in [-1.31505,-1.31495]. These canonical modules are included in 863.
'''
text=text.replace('the checked Tie/Gem and two additional\n   numerical scratch modules are excluded from the current full target until\n   migrated and integrated.','all Tie/Gem and additional numerical modules are included in the final full build.')
p.write_text(text,encoding='utf-8')
p=r/'README.md';text=p.read_text(encoding='utf-8-sig')
text=re.sub(r'\n\nLatest verified checkpoint:[^\n]*\n','\n',text)
readstatus=f'''## Current verification status

**The original Section 3 is formalized and verified**, including its additional
four-exponent material later moved to an appendix. The complete build passed
**863 modules / 956 ordered kernel axiom outputs / 136 certificate batches**
at {b['completed_at_utc']}. Source/build verification reports zero errors and
only the standard logical axioms. Code commit: `{commit}`.

Start with [Universality/Section3.lean](Universality/Section3.lean), the complete
[statement coverage map](docs/SECTION3_COVERAGE.md), or the single continuous
[R077 report](docs/R077_完整研究记录.md). Post-build source/object/dependency
fingerprints are in `docs/section3-final-integrity.json`. Historical Section 2
and earlier Section 3 evidence remains in the R071/R072/R074/R075 reports.

'''
text=text[:text.index('## Current verification status')]+readstatus+text[text.index('## Section 3 scope'):]
text=text.replace('have passed individual checks and are now in the integrated build.','are all included in the successful complete build, with the numerical examples.')
text=text.replace('are recompiled here.','have been recompiled and verified here.')
p.write_text(text,encoding='utf-8')
t=f'''
## 最终验收：原 Section 3 完成

本轮开始2026-10-06 10:07:41 UTC；数学、代码及核验工作封存于{now.isoformat()}，实际墙钟{elapsed/3600:.3f}小时（{elapsed:.0f}秒）。此后仅执行本轮同一归档和项目索引的交付保存与回读，不另开研究轮次。没有累计agent-hours。本轮由主控和三个子agent并行完成，核验时最多两个Lean进程；未修改Overleaf或另外Section4/5的工作区。

最终完整构建于{b['completed_at_utc']}通过：863正式模块、956条有序匹配kernel公理输出、136证书批次。verify_snapshot零错误；全正式源无占位、无新增数学公理、无native计算捷径。全部打印公理仅propext、Classical.choice、Quot.sound。代码提交{commit}。随后独立封存每个模块源码/olean SHA256、递归项目依赖指纹与实际Lean二进制SHA，记录于docs/section3-final-integrity.json；该封存是构建后完整性核查，未伪装成另一轮编译。

统一入口Universality/Section3.lean。原稿12个独立定理性环境、5个定义、3个例子均覆盖；别名标签未重复计数。完整逐条数学条件及Lean声明见docs/SECTION3_COVERAGE.md，原稿为docs/section3-20261006.tex，冻结来源提交fccfba64fd345f8b0cbaafd94abec48420c0c6fa。原稿后来移入附录的另四指数仍在本轮验收范围。

最后11个新增正式模块包括Tie/Gem数值8模块、其余数值2模块及统一入口。Tie/Gem临界概率与热乘子四位小数已由有理区间认证，真实质量Perron根严格在(5.708705,5.708725)，第三根严格在(1.42005,1.42015)且属于两张实际完整三态质量矩阵的复谱；不是独立玩具矩阵或仅trace差的猜测。Diamond γ+在[2.94115,2.94125]，其任意0<p<pc实际有限簇susceptibility=∞；Wheatstone原始α在[-1.31505,-1.31495]。所有数值区间使用kernel证明，不依赖浮点实验。

本轮最终可靠结论包括：实际质量L²及光滑正密度LLT；真实均匀根随机图、局部弱极限与局部有限性；四实际物理指数及分类；实际矩与共同gap全部原稿条件结论；真实κ的正则性及三个α例子；实际环境半径累计律、条件点指数值和diamond点指数不存在；任意字循环实相似、实际不交换障碍及任意乘法观测不能分类；真实Hausdorff识别与分类wrapper；实际电阻乘法、Tie/Gem例证及全部文中数值说明。一般原逐点半径或原始α不存在统一公式的数学限制保留，没有把论文的条件结论升级成无条件全域指数存在。

范围边界：采用等价的形式证明，不逐行翻译原证明。κ proof的解析线性化/周期振幅/共振展示式未独立形式化，但全部正式正则性和rawα命题已由替代证明完成；顶点质量不声称原文未要求的全序列a.s.收敛；local weak使用有限根球同构事件刻画；端点κ用区间内解析/真实解析延拓。电阻仅在连通网络有物理解读。已明确区分actual compact generation Hausdorff维数与仅命名对数商。完整限制见coverage和独立审阅文档，无剩余本轮定理或代码义务。

构建使用固定Lean4.32.1/mathlib520045ab14e26149ee970e2e617ca04b09bde5d6依赖环境的直接Lean核验，复用此前已核验未改动模块并记录新增重编；没有宣称在全新机器完成portable lake build。原文所需有限图证书由Lean内核decide/norm_num等验证；Python浮点仅用作候选设计，没有成为证明前提。

单轮权威归档继续使用Drive文件1hA3QlcBJyTtAD7cL4DDHOOX784uF9-ni；项目最新进展继续使用1MHo2w0gzfnT3z3j1MjfAB0QFwvA3BeBW，保留R080/R079/R078独立成果。下一步是用户审阅/跨章节整合；Section3本身已完成。本轮形式化没有解决generalized DHL尺度公度必要性的原研究问题，也不将其他对话的Section5状态混作本轮结果。
'''
p=r/'docs/R077_完整研究记录.md';report=p.read_text(encoding='utf-8-sig')
report=report.replace('开始：2026-10-06 10:07:41 UTC / 18:07:41 中国标准时间。进行中。',f'开始：2026-10-06 10:07:41 UTC / 18:07:41 中国标准时间。核验与记录封存：{now.isoformat()}；实际墙钟{elapsed/3600:.3f}小时。本轮已完成。')
report=report.replace('本报告按时间记录核验节点；最新状态以末节为准，早期“尚未完成”条目可能已被后续证明取代。本轮仍在持续，没有重置开始时间。','本报告保留逐步核验历史；最终验收见末节。早期“尚未完成”条目为当时状态，已被后续证明取代。原始开始时间和轮号未重置。')
report=report.replace('\n\n来源对话：','\n\n最终结果：原Section3全部定理性陈述、定义和例子已形式化；863模块/956公理审计通过，零错误，仅标准逻辑公理。统一入口Universality/Section3.lean；完整范围及限制见docs/SECTION3_COVERAGE.md。\n\n来源对话：',1)
p.write_text(report+t,encoding='utf-8')
print(json.dumps({'commit':commit,'modules':863,'audits':956,'end_utc':now.isoformat(),'wall_clock_hours':elapsed/3600}))
