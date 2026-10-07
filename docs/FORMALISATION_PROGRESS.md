# Lean formalisation 进展总览

更新：2026-10-07（上海时间）。整理读取 Codex 对话 **universality class 2、universality class 3、universality class 4**，核对各自覆盖范围、构建记录和源码/编译产物哈希；Section 5 的最终公理依赖审计已重新从源运行通过。这不表示重新编译了各节所有数值证明。

**目前已验收的是 Section 2 的具名数学结论、原 Section 3 的全部已列明结论与例子（包括后来移入附录的另四指数），Section 4 在两个明确外部数学输入下的全部已陈述结论，以及 Section 5 的全部已陈述结果。Section 5 仅超越性使用已接受的 GS 接口，四指数猜想保留为显式假设。全文尚未作为一个统一构建完成验收。**

## 1. 按章节看现在完成了什么

| 部分 | 已有结果 | 形式化证据与准确边界 |
| --- | --- | --- |
| Section 2：渗流、random EIGS 与质量矩阵 | 有限配置与可靠性、临界点、条件替代的全层联合律、几何递归、三态矩阵及谱结构、pivotal 响应等具名结论 | R072 验收闭包为 **259 模块、142 项指定公理输出**。当时随机律以任意有限深度表达，几何极限是兼容实现下的逐点结论；R075 又构造了相容的无限历史概率空间。不能把早期摘要误读成任意随机图的任意度量缩放极限定理。见 [R072](R072_完整研究记录.md)、[R075](R075_完整研究记录.md)。 |
| Section 3：四指数与分类 | 实际观测量定义下的 β、crossing ν、点概率 δ、平均连通性 η 的存在性、公式、唯一性，以及四指数相等当且仅当三个临界维数相等 | R077 完整闭包为 **863 模块、956 项指定公理输出、136 个有限证书批次**。原稿 **12 个独立定理性环境、5 个定义、3 个例子**已逐条对应。环境维数已接到实际紧致极限度量空间的 Hausdorff 维数，并非仅给对数商命名。见 [统一入口](../Universality/Section3.lean)、[完整覆盖表](SECTION3_COVERAGE.md)。 |
| 原 Section 3、现附录：另外四指数 | 实际有限簇矩及 γ、相邻矩比及 Δ、真实簇数密度 κ 的正则性和 raw α 判据、实际环境半径尾律和条件点指数；包括 diamond 半径点指数不存在及 α 例子 | 全部包含在 R077 验收中。这里完成的是论文中有适用条件的结论与非存在例证，**不等于八个指数对所有模型都无条件存在**。η 使用固定环境距离窗口的平均连通性；半径累计尾与原逐点指数严格区分。 |
| Section 3：乘法维数不能分类 | 任意有限替代字的循环不变性、真实 classical 规则上的非交换障碍、任意乘法观测不能分类，以及同 Hausdorff 维数但不同物理指数类的例子 | 已接实际有限图和物理指数类。Tie/Gem 的真实三态谱、电阻 4/3、相关四位小数均有内核证书。不是把浮点实验或抽象玩具矩阵当成实际图的证明。 |
| Section 4：六指数定理与公度性 | 实际增长倍率的代数性、秩判据、迭代与尺度对齐、完整不动点商的结构和次数、不可约判据、任意族共同整数本原底数、尺度对数秩、pivotal 超越性，以及 Wheatstone/diamond 整类推论 | R080 最终闭包 **647 模块、5740 个项目数学内核声明**。已连接实际 Hausdorff 维数及实际四指数普适类。使用两个经用户授权的外部数学公理接口：六指数定理、Gelfond–Schneider。详见 [冻结覆盖表](https://github.com/Nero-17/LEAN-Formalisation-IGS-Bernoulli-percolation-universality-class/blob/919e8735cc28374000c6ca9554ebb0a6887e751f/docs/SECTION4_COVERAGE.md)。 |
| Section 5：同类不公度反例及移位例 | 四份精确整数证书、三个实际 classical 图、尺度对数独立、无限同类且两两不公度族、实际物理指数和 Hausdorff 维数、三个维数全超越而有理相关的移位例，以及 Discussion 的条件性四指数结论 | R079 最终 **906 模块**闭包完成；最终依赖审计覆盖 **905 个项目来源模块、8543 个内核声明**，本次重跑通过。无遗留的具体证书前提。GS 是唯一非基础数学公理；四指数猜想是定理参数。见 [冻结发布说明](https://github.com/Nero-17/LEAN-Formalisation-IGS-Bernoulli-percolation-universality-class/blob/3e77e78297089288cbe216a2bd629b3b7c838bd9/docs/SECTION5_PUBLICATION.md)。 |

各闭包大量重叠，不能把 259、863、647、906 相加作为独立模块总数。956 是选定的公理打印输出数，5740 是对项目数学内核声明的审计数，Section 5 的 8543 则包含 private/generated 内核声明；这些统计口径不同，都不能当作独立定理数。

## 2. 三个对话各自交付的位置

| 对话 | 最终交付 | GitHub 位置 |
| --- | --- | --- |
| universality class 2 | R077；最终证明提交 `5b80bbe96fd5d55e4ce2ee03e3576665d5e37eb6`，文档封存提交 `7d3f92416baeaa3c26e50b06830457926e9c6c5b` | 本次将这一完整历史合入 **main**，保留原来的全部 supplementary 材料。最终验收时间为 **2026-10-07 04:05:04（上海）**。 |
| universality class 3 | R078 算术基础、R080 完整接口；最终证明提交 `803c9497e6c25e92a08b15bdd4bf2bc95d760256`，文档封存提交 `919e8735cc28374000c6ca9554ebb0a6887e751f` | 已在 **codex/section4-independent**，对应 [Draft PR #1](https://github.com/Nero-17/LEAN-Formalisation-IGS-Bernoulli-percolation-universality-class/pull/1)。最终验收时间为 **2026-10-07 02:40:51（上海）**。本次保留该独立已验收分支，没有宣称完成跨分支联合构建。 |
| universality class 4 | R079；发布提交 `3e77e78297089288cbe216a2bd629b3b7c838bd9` | **codex/section5-complete**，对应 [Draft PR #2](https://github.com/Nero-17/LEAN-Formalisation-IGS-Bernoulli-percolation-universality-class/pull/2)。原最终构建于 **2026-10-07 08:10:13（上海）**完成；本次重新运行最终依赖审计于 **08:51:53**完成。原冻结依赖保留，没有覆盖 main 的最终 Section 3。 |

Section 4 的统一入口为 [`Universality.Arithmetic.Section4Complete`](https://github.com/Nero-17/LEAN-Formalisation-IGS-Bernoulli-percolation-universality-class/blob/919e8735cc28374000c6ca9554ebb0a6887e751f/Universality/Arithmetic/Section4Complete.lean)。同分支仍保留纯算术、几何及三观测量的较小入口。

Section 5 统一入口为 [Universality.Section5](https://github.com/Nero-17/LEAN-Formalisation-IGS-Bernoulli-percolation-universality-class/blob/3e77e78297089288cbe216a2bd629b3b7c838bd9/Universality/Section5.lean)。首次构建前需按 [恢复说明](https://github.com/Nero-17/LEAN-Formalisation-IGS-Bernoulli-percolation-universality-class/blob/3e77e78297089288cbe216a2bd629b3b7c838bd9/RESTORE_GENERATED_DATA.md) 重建 44 份纯数据文件（453,477,561 字节）；原始 JSON、全部证明源码、恢复脚本及哈希清单均在分支中。恢复不替代 Lean 验证。

单轮权威归档仍使用原文件：

- [R077：Section 3 完整报告、源码和核验证据](https://drive.google.com/file/d/1hA3QlcBJyTtAD7cL4DDHOOX784uF9-ni/view)。
- [R080：Section 4 完整报告、源码和核验证据](https://drive.google.com/file/d/1Ml3UCXhF0uWYmOvFYurKq9q2Ey8Aca-K/view)。
- [R079：Section 5 完整报告、源码和核验证据](https://drive.google.com/file/d/1fgiilwUMoIPasJk-qis5UOF43flUgKzm/view)。

本总览不替代这些逐轮记录，也不另建同轮的 Drive 报告。

## 3. “完成”的数学范围与信任边界

1. **Section 3 的 main 闭包不引入数学公理或占位证明。** 最终日志中的依赖只包含 `propext`、`Classical.choice`、`Quot.sound`；正式源没有 `sorry`、`admit`、`native_decide`。具体图的计算由产生证明项的策略交给 Lean 内核检查。
2. **Section 4 有两个明确的外部数学输入。** [`Universality.External.six_exponentials`](https://github.com/Nero-17/LEAN-Formalisation-IGS-Bernoulli-percolation-universality-class/blob/919e8735cc28374000c6ca9554ebb0a6887e751f/Universality/Arithmetic/SixExponentials.lean) 和 [`Universality.External.gelfond_schneider_real`](https://github.com/Nero-17/LEAN-Formalisation-IGS-Bernoulli-percolation-universality-class/blob/919e8735cc28374000c6ca9554ebb0a6887e751f/Universality/Arithmetic/GelfondSchneider.lean) 是已知定理的显式公理接口，其自身证明未在本库形式化；下游证明经内核检查并显示这些依赖。不能将这部分表述为“完全没有新增公理”。
3. **Section 4 开篇的公度猜想没有被作为定理或公理加入。** 形式化正面判据不是全 HL 的无条件公度定理，也没有解决 generalized DHL 的原全局研究问题。
4. **采用精确的论文观测约定。** 四指数结论适用于已定义的 classical 规则及相应 annealed / uniform-root、crossing、平均窗口观测量；不能自动改称 quenched 或任意逐点 η。α 和逐点半径指数保留各自条件及不成立的情形。
5. **完成的是陈述，不要求照抄原证明。** κ 正则性采用另一条已验证证明；原证明中可选的解析线性化、周期振幅及共振展示式未逐式形式化。实际累计顶点质量证明了所需 L² 极限，不声称额外的全序列几乎处处收敛。Lean 的代数编号与论文相差一层，LLT 密度及同一历史极限的归一化转换已显式证明。
6. **构建范围可复现但仍有工程边界。** 两边固定 Lean 4.32.1 / mathlib `520045ab14e26149ee970e2e617ca04b09bde5d6`，使用已有固定依赖环境的直接 Lean 编译和公理审计；尚未声称在全新机器完成 `lake build`，也未进行所有章节合并后的统一验收。

## 4. 本次实际做了哪些核查和发布

- 阅读两个对话的最终回复及前序范围说明，核对冻结稿的 coverage，而非只根据“完成”两个字下结论。
- Section 3 的 **863 对**源码/`.olean` 与最终完整性清单一致；Section 4 的 **647 对**与最终构建清单一致。核对记录见 [formalisation-progress-verification.json](formalisation-progress-verification.json)。这是构建后的完整性复核，不是重新运行一次 Lean。
- Section 3 最终源码此前尚未在远端 main。本次整合其完整提交历史，保留原 supplementary 目录，并补入原始 [构建日志](../build-evidence/section3-continuation-build.log)，供 [快照验证脚本](../scripts/verify_snapshot.py) 使用。
- 原始编译源混用 LF/CRLF；本次按已认证字节保存 Lean 文件及日志，使用 `.gitattributes` 防止 Git 的换行转换使原构建哈希失效。没有修改已验收的数学证明。
- 保留 Section 4 已上传的独立分支和 PR，主入口给出固定提交链接；仓库仍为 **private**。没有修改两个源对话的工作区或 Overleaf。

## 5. 接下来真正需要的工作

1. 将 Section 4 与最终 R077 依赖合到同一工作树，处理重叠模块和不同审计入口，然后重新做联合构建；目前不能把两个独立通过的构建直接称作一个共同通过的构建。
2. Section 5 已独立交付并核对；下一步将其固定依赖与最终 Section 3/4 对齐，恢复大型纯数据输入后做联合验收。不能直接把各节分别通过当作合并版本通过。
3. 将冻结稿 label 映射复核到最终投稿稿，防止定理移动、编号变化或定义修改造成“旧陈述已证，新陈述未检查”。
4. 做一次干净环境的构建复现，并为投稿材料给出简明的 Lean 覆盖范围及 Section 4 外部输入说明。

这些是全项目整合与交付任务；不是将 R077、R080、R079 已明确验收的数学结论重新改成未完成。

## 6. Section 5 本次发布复核（2026-10-07）

- 原 R079 ZIP 的 1208 个清单文件全部哈希匹配；44 份纯数据模块与其精确恢复清单一致。906 个闭包源码均有归属：862 个按认证字节存入 Git，44 个通过已验证的确定性恢复配方表示。
- 完整最终依赖快照与历史成功回执一致；重新运行 Section5FinalKernelAudit.lean，退出 0，8543 个内核声明的依赖均通过政策检查；10 个 GS 依赖端点是明确的超越性结论。该重跑使用已认证编译对象，没有伪装成所有数值证书的重新编译。
- 具体无限族共享真实四指数 β=13/70、ν=10/7、δ=219/13、η_av=−3/50，尺度为 (19·661^k)^100。移位例的维数与原族不同，不能把它误报成共享超越维数的同类不公度反例。
- 所有上传的证明源码保持原验收字节；原工作区未改动。因已有目录正在进行 Section 4 合并，发布在独立副本进行，原合并没有被中止或覆盖。

本次 [精确核查记录](https://github.com/Nero-17/LEAN-Formalisation-IGS-Bernoulli-percolation-universality-class/blob/3e77e78297089288cbe216a2bd629b3b7c838bd9/docs/section5-publication-review.json) 与 [原始审计输出](https://github.com/Nero-17/LEAN-Formalisation-IGS-Bernoulli-percolation-universality-class/blob/3e77e78297089288cbe216a2bd629b3b7c838bd9/docs/section5-publication-review.axioms.log) 已上传。源码在 PR #2，main 更新本总览和 README；跨章节合并仍明确列为后续工作。
