from pathlib import Path
import json,subprocess
r=Path('.')
a=json.loads((r/'docs/source-audit.json').read_text(encoding='utf-8-sig'))
b=json.loads((r/'docs/build-metadata.json').read_text(encoding='utf-8-sig'))
assert a['ok'] and a['module_count']==799 and a['kernel_axiom_output_count']==800
assert b['module_count']==799
commit=subprocess.check_output(['git','-c','safe.directory='+str(r.resolve()).replace('\\','/'),'rev-parse','HEAD'],text=True).strip()
p=r/'SECTION3_CONTINUATION_STATE.json';s=json.loads(p.read_text(encoding='utf-8-sig'))
s.update(verified_code_commit=commit,verified_module_count=799,verified_axiom_audit_count=800,latest_full_build_utc=b['completed_at_utc'],pending_full_build_module_count=None,pending_full_build_axiom_audit_count=None,pending_snapshot_status='Eighth full snapshot verified: 799 modules / 800 ordered audits / 136 certificate batches. Section 3 incomplete: full local weak law, actual critical radius identification, physical cluster-number size-sum/response integration, manuscript-normalized density and tie/gem numerical/electrical illustrations remain outside this snapshot.')
p.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
t='''
## 第八次完整核验：真实尖峰、共同gap、局部有限性与强响应

完整构建于 DATE 成功结束；799正式模块、800条有序匹配的kernel公理输出、136证书批次，独立源码/构建/公理核对零错误。仅propext、Classical.choice、Quot.sound。代码提交COMMIT。R077仍从2026-10-06T10:07:41Z连续进行，未结束；墙钟为开始至本检查点的实际时间差，未累计agent-hours。

新增已证明：真实diamond有限开闭事件、独立三层配置权及条件子胞腔质量给出实际精确半径点概率的dyadic尖峰下界，结合累积尾上界推出点半径对数指数不存在。包括指定粗边开通、选定16子胞腔cross其余240个failed的实际事件、隔离连通簇、每个被计根的精确半径、子胞腔质量增长、generation重关联和根概率规范化；没有预设尖峰。真实物理有限簇矩的γ、逐阶Δ、最终共同gap、全部正阶右侧gap相同当且仅当m≤ρ²亦已证；左侧保留有限阶阈值，固定正次临界充分高阶矩=∞，未把无穷矩toReal当作有限矩。

实际无限图每层嵌入保持环境距离。真实有限地址计数得端点存活概率≤2(d_R/m)^n，经iid尾移位和可数层/顶点交得到almost surely每个顶点最终进入某层内部；内部邻域冻结推出完整年龄混合律下几乎处处每个顶点邻域有限，对所有配置成立。实际顶点集无限且可数，有限球/有限集合/邻接进入充分晚层也已核验。不能将这些接口自动等同整个rooted-ball local weak law；最终球概率识别在下一批。

Wheatstone第三响应双侧强比较已证明：|κ‴(p)|≈|p−1/2|^{log5/log(13/8)−3}。精确规范化系数在中心为1，局部偏差以指数控制；加可控幂次/指数修正后由紧致退出区间的正上下界推出。没有假设周期振幅非零。此处κ仍用已经识别的有限图簇数密度极限，size-sum桥另行核验。任意有限字循环及Tie/Gem实际四指数同类wrapper也已整合。Diamond四指数公式接到真实HasCriticalExponents，0.1647、1.6353、18.8585、0.2014由平方根有理夹逼与有限对数级数误差界得到kernel区间证书，非浮点证据。

交叉审查发现原稿κ=Σn_s与有限图簇数密度极限尚需显式桥，现已另行单独check0四模块：有限簇尾计数≤1/N、统一尾界交换极限与和、κ=Σ physicalFiniteClusterProbability/s、真实κ的C^j及raw α判据。全p∈[0,1]有效，不要求有限簇质量和为1，覆盖超临界；尚未计入799。通用有限年龄事件分解/几何尾/概率极限/真实sample law混合4模块也单独通过，供实际球与半径specialization使用。

精确范围：当前稿把另四指数移至附录，本轮仍完成原先Section3全部数学目标。κ正则性正式命题已有替代证明，原证明的解析线性化/周期及共振展示式未逐条形式化。Lean generation0=paper depth1，LLT密度应精确换为w_paper(x)=ρw_Lean(ρx)，同一随机极限换为W/ρ；幂律常数可以吸收shift，密度本身不能仅说常数吸收。该wrapper在后续草稿。R080现已完成实际环境Hausdorff识别；已只读核对其clean提交919e8735cc28374000c6ca9554ebb0a6887e751f并冻结22个新几何模块，139模块依赖闭包中的其余117个与本库源码相同。计划本库重新编译并接入真实dimH分类式，尚未计入799；未修改其他对话源码。

单独核验补充（尚未计入799）：完整均匀根local weak law、临界实际无限图半径尾/点律、临界真实簇几乎处处有限、实际半径尾幂律及diamond点指数不存在wrapper，10模块全部check0。仍需整合这些模块；κ桥与三个α例子整合；LLT精确paper归一；Tie/Gem质量谱/临界/热小数及电阻乘法与4/3例证。Section3未完成。三agent继续并行，最多两个Lean核验进程。无新增已证结果撤回。后续单验草稿在ZIP working-drafts，完整审计范围以source-audit及本节为准。
'''.replace('DATE',b['completed_at_utc']).replace('COMMIT',commit)
p=r/'docs/R077_完整研究记录.md';p.write_text(p.read_text(encoding='utf-8-sig')+t,encoding='utf-8')
p=r/'docs/SECTION3_COVERAGE.md';p.write_text(p.read_text(encoding='utf-8-sig')+'\n## Eighth full snapshot\n\n799 modules / 800 ordered kernel outputs / 136 certificate batches; zero audit errors. Added actual diamond spikes/nonexistence, physical common-gap classification, full mixture a.s. local finiteness, infinite countable vertices, strong two-sided Wheatstone response, cyclic physical classes and rigorous diamond decimal intervals. Still pending: full local weak law, critical actual radius identification/wrappers, physical cluster-number size-sum/response integration, exact manuscript LLT density rescaling, Tie/Gem decimal/electrical illustrations.\n',encoding='utf-8')
print(json.dumps({'commit':commit,'completed':b['completed_at_utc']},ensure_ascii=False))
