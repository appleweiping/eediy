---
title: EE 进阶数学
description: 从复变量、应用矩阵方法、严格概率和近似方法中选择真正服务于信号、控制、电磁与数值建模的课程。
page_type: guide
comments: true
last_reviewed: 2026-07-31
---


# EE 进阶数学

“进阶数学”不是本科数学之后必须依次完成的第二套基础课。对多数 EE 学生，先修一门完整的复分析、严格概率和应用矩阵课程，再回头学专业课，反而会把定理的使用场景抽空。更实际的顺序是先在[数学基础](math-foundations.md)中建立微积分、线性代数、微分方程和工程概率，再让一门专业课中的具体困难决定下一门数学课。

本页只推荐目录中已有充分公开材料的课程，也会直说它们不适合什么。出现“复平面上的解析结构”“大矩阵的条件性”“概率极限为何成立”或“估算比精算更重要”时，下面四门课各有清楚的分工，但不要求全部完成。

## 18.04：当复平面本身成为问题时再学

[MIT 18.04 Complex Variables with Applications](courses/mathematics/005-18-04.md) 是这里最像传统数学课的一门。[Spring 2018 课程](https://ocw.mit.edu/courses/18-04-complex-variables-with-applications-spring-2018/)由 Jeremy Orloff 主讲，公开的 [37 组 lecture notes](https://ocw.mit.edu/courses/18-04-complex-variables-with-applications-spring-2018/pages/lecture-notes/) 从解析函数与 Cauchy–Riemann 方程，走到 Cauchy 定理、Taylor/Laurent 展开、留数、调和函数、保角映射、幅角原理和 Laplace 变换。九套 problem sets 都有解答，另有 recitation、两次期中和一次期末；缺少的是授课视频，而不是课程骨架。

它适合已经完成 18.02 与 18.03、并在[信号与系统](courses/signals-systems/index.md)、频率域电路或[电磁场](courses/electromagnetics/index.md)里遇到真实复变量问题的人。留数可以处理某些逆变换和频域积分，解析函数把极点、零点与有效区域放进同一幅图，保角映射则能把部分二维势场边界化成较容易的几何。但这些用途都依赖条件：复对数要说明 branch，Laurent 级数要说明环域，围道积分要说明奇点与方向，二维场解还要保留材料和边界假设。

若目前只是计算一阶、二阶系统的 Laplace 变换，18.03SC 与信号课程已经够用；若只是用相量算交流电路，也不需要先学 Cauchy 定理。18.04 的价值出现在“为什么可以这样变形、积分、延拓”已经影响结论时。先修中的多变量积分和常微分方程若不稳，强行从留数开始只会把缺口藏在技巧下面。

## 18.065：矩阵成为计算瓶颈之后接 18.06

[MIT 18.065 Matrix Methods in Data Analysis, Signal Processing, and Machine Learning](courses/mathematics/009-18-065.md) 不是另一本线性代数入门，也不是机器学习模型名录。Gilbert Strang 的 [Spring 2018 课程](https://ocw.mit.edu/courses/18-065-matrix-methods-in-data-analysis-signal-processing-and-machine-learning-spring-2018/) 以 18.06 为先修，从四个基本子空间、LU/QR/SVD、最小二乘、PCA 和低秩近似继续到随机矩阵、矩阵微分、优化、稀疏性、matrix completion 与 SGD。对阵列处理、系统辨识、控制、反问题和大规模信号数据，这条线比再学一遍手算消元有用得多。

选它之前，应能解释投影、特征值、奇异值与秩，而不只是调用库函数。课程公开了完整视频和汇总的 [assignments](https://ocw.mit.edu/courses/18-065-matrix-methods-in-data-analysis-signal-processing-and-machine-learning-spring-2018/pages/assignments/)，但指定教材 *Linear Algebra and Learning from Data* 不是开放教材，作业也没有公开解答。原课没有考试，以 final project 替代最后三次作业；公开页并没有提供完整的项目评分说明或校外反馈。因此它更适合能够自己建立小规模基准、数值实验和反例的学习者，而不适合依赖逐题答案完成第一次线性代数学习。

在 EE 里，18.065 最值得围绕同一个矩阵反复比较：节点或状态方程是否病态，正规方程、QR 与 SVD 对残差和扰动的反应有何不同，低秩截断节省了什么又丢失了什么。控制方向可把这些问题接到[线性系统与控制](courses/control-systems/index.md)，信号方向可接到[数字信号处理](courses/dsp/index.md)。如果连列空间和正交投影都说不清，应回到 18.06SC；课程号更大不会自动补齐这些概念。

## 6.436J：只有当概率证明本身是工作时才值得进入

[MIT 6.436J Fundamentals of Probability](courses/probability-statistics/008-6-436j.md) 是研究生概率论，而不是 18.05 的加速版。它的 [lecture notes](https://ocw.mit.edu/courses/6-436j-fundamentals-of-probability-fall-2018/pages/lecture-notes/) 从概率测度、可测性和抽象积分开始，继续到条件期望、不同收敛方式、变换、LLN/CLT 与离散和连续时间 Markov 过程。官方形式先修是 18.02 与 elementary probability，实际还需要能够读写证明、处理集合与极限，并愿意为一个定理的假设花时间。

这门课适合准备研究型通信、信息论、随机过程、统计学习或随机控制的人：当“能算一个密度”已经不够，必须知道条件期望相对于哪个 \(\sigma\)-代数、为何可以交换极限与积分、某种收敛能否推出另一种收敛时，严格语言会直接改变推导。若目标只是噪声功率、常见随机变量和有限状态 Markov 链，[6.041SC](courses/probability-statistics/007-6-041sc.md) 的工程主线更完整、更容易获得答案反馈。

公开版的限制也比课程难度更关键。[Assignments](https://ocw.mit.edu/courses/6-436j-fundamentals-of-probability-fall-2018/pages/assignments/) 有十二套题，第十二套为 optional，但 OCW 没有公开原课解答；midterm 与 final 同样只有题面。没有能核对证明的人时，先修 6.041SC 并补实分析通常比直接进入 6.436J 更稳妥。[Cornell ECE 3100](courses/probability-statistics/087-ece-3100.md) 可以在前一门工程概率之后提供随机信号语境的题目，但它也缺少讲义和多数答案，不能补上 6.436J 的反馈缺口。

## 6.055J：应该穿插的近似方法，而不是最后一门数学课

[MIT 6.055J The Art of Approximation in Science and Engineering](courses/mathematics/018-6-055j.md) 训练的是另一种深度。Sanjoy Mahajan 的 [开放书稿](https://ocw.mit.edu/courses/6-055j-the-art-of-approximation-in-science-and-engineering-spring-2008/pages/readings/) 依次使用量纲分析、极限情形、尺度律、逐次近似、平衡和对称；六套正式 [assignments](https://ocw.mit.edu/courses/6-055j-the-art-of-approximation-in-science-and-engineering-spring-2008/pages/assignments/) 均有完整解答。原课没有传统考试，重心一直在作业与低成本实验。

这门课不要求等到复分析或严格概率之后。学过单变量微积分和基础物理就可以穿插，每周拿当前专业课的一项量做估算：RC settling time 的数量级、导线温升由什么尺度主导、天线尺寸怎样随频率变化、采样率提高后数据与功耗怎样增长。精确模型之前先判断变量、单位、极端情形和忽略项，往往能在仿真前发现错误。

近似方法也不能越界。量纲分析不能给出所有无量纲常数，尺度律会忽略几何转变、材料变化和边界效应，逐次近似只有在被忽略项确实较小时才有效。6.055J 适合让电路、器件、控制和电磁中的计算更有判断力，却不能替代任何一门给出完整系统理论的专业课。

## 按专业问题组合课程

- **信号、DSP 与通信：** 先完成 18.03SC 和一门完整的[信号与系统](courses/signals-systems/index.md)。需要处理围道、解析性或更细的极点结构时加入 18.04；矩阵维度、最小二乘或低秩结构成为问题时加入 18.065；只有研究工作需要测度化概率与收敛论证时，才在 6.041SC 之后进入 6.436J。普通滤波器设计不需要同时开三门进阶数学。
- **控制与机器人：** 状态空间的第一层仍是 18.06SC 与 18.03SC。多变量估计、系统辨识、模型降阶和优化更直接地受益于 18.065；随机控制的严格理论才需要 6.436J。若基准模型本身的单位、平衡点或参数都不可靠，应先修模型，而不是增加抽象层。
- **电磁、射频与光子：** 18.02SC 的向量分析是不可跳过的底座。18.04 对二维势场、解析函数和部分频域方法有用，6.055J 对尺度、边界层和数量级很有用；三维复杂几何最终还会走向数值离散。数学结果不会自动验证材料模型、激励、边界或端口定义，实体实验也仍须遵守场地、功率、辐射与高压安全要求。
- **电路、器件与测量：** 频率域解析或某些逆变换真正需要复平面时选 18.04；参数提取、过定约束或高维测量出现病态时选 18.065；实验不确定性通常先由 18.05 处理，而不是直接上 6.436J。6.055J 则适合贯穿始终，用来判断某个二阶效应是否值得纳入模型。

判断是否选课时，可以直接看正在卡住的那一行数学：branch cut 与围道指向 18.04，singular-value decay 与 conditioning 指向 18.065，almost sure convergence 与 conditional expectation 的定义指向 6.436J，主导尺度与小参数指向 6.055J。若问题说不出这么具体，通常还没有到需要整门进阶课的时候。

## 数值方法要在专业模型里学习

当前目录没有把一门“通用数值方法”包装成所有方向的统一答案，因为不同 EE 问题关心的误差并不相同。常微分方程要比较步长、稳定区间与解析极限；最小二乘要看条件数、残差以及 QR/SVD 与正规方程的差异；电磁离散要做网格加密并检查通量或能量守恒；Monte Carlo 则要区分采样误差与模型误差。[数值计算与模型验证](guides/numerical-computing.md)给出这些共同习惯，具体算法仍应跟随专业课。

这也是进阶数学真正回到 EE 的地方。18.04 提供解析基准和奇点结构，18.065 解释数值线性代数为何稳定或失稳，6.436J说明随机极限需要哪些条件，6.055J则在开算之前判断答案应落在哪个量级。仿真曲线只有在模型、参数、离散方式和误差来源都能说明时才有意义；尤其在电磁与高功率系统中，仿真不是实体安全结论。

选完一门课后，应尽快回到[全局路线](roadmap.md)中的专业主线。判断这门进阶数学是否有用，要看原先说不清的工程结论是否因此有了条件、推导和适用范围。
