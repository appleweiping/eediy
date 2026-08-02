## 电网课与电机课共享标幺制，但各有独立主线

[NPTEL Power System Analysis](118-117105140.md)的[官方页面](https://nptel.ac.in/courses/117105140)覆盖 per-unit、power flow、fault 与 stability，视频和作业开放，认证考试收费，也没有公开 code/lab 闭环。[MIT 6.691](119-6-691.md)的[官方 OCW 归档](https://ocw.mit.edu/courses/6-691-seminar-in-electric-power-systems-spring-2006/)更偏 operation、planning 与 market；7 套带解题、MATLAB 小程序和 project sample 很有价值，但规则与案例属于 2006 年。电网侧可据此形成“标幺换算—潮流残差—故障约束—稳定解释”的题目链，市场内容则另按历史案例阅读。

机器侧，[MIT 6.685](120-6-685.md)的[官方 syllabus](https://ocw.mit.edu/courses/6-685-electric-machines-fall-2013/pages/syllabus/)用讲义与 11 份 problem set 系统处理 electromechanical conversion 与 machine model，公开归档缺课程安排中的 3 小时 final。[Electrical Machines II](121-108105131.md)的[官方 NPTEL 页面](https://nptel.ac.in/courses/108105131)是视频型替代，却没有可复现实验和反馈链。6.685 的题更适合由 magnetic co-energy 推 torque，再落到 synchronous/induction machine equivalent model；NPTEL 则适合配合视频整理 rotating-field 与 performance equation。静态 power flow 不要求完整机器课，单机 dynamics 也不要求 market 课；只有并网机器问题才各选一门并在同一 base 上连接。

## 6.691 应作为 2006 年案例档案阅读

6.691 的 market rule、load data 与 blackout discussion 可以训练建模和论证，却不能直接支持 2026 年的运行结论。若讨论当前 ISO/RTO dispatch、reserve 或 transmission rule，应另取当下 ISO/RTO、regulator 或 utility 的一手数据，注明 time zone、base、revision 与 license，并与 2006 案例分栏。课程提供的小 MATLAB 程序可以解释当时的计算任务；迁移到 pandapower、OpenDSS、Python 或 GNU Octave 时，应说明 dataset、solver、tolerance 与 model 的对应关系。

同样，6.685 缺少的 final 不应由第三方答案拼成完整官方考试，NPTEL 开放作业也不意味着存在 anonymous grader。历史档案的价值来自可核的原题、原数据与原语境，包装成当前电网或当前产业流程反而会丢失可验证边界。对同一案例，可分别写“2006 课程结论”和“当前数据复核”，避免时间条件在段落中混合。

## 两母线潮流给同步机 swing equation 提供初值

[电路分析](../circuits/index.md)中的 three-phase complex power 与 network equation、[电磁场](../electromagnetics/index.md)中的 magnetic circuit、air-gap field、induction 与 torque，以及[工程数学](../mathematics/index.md)中的 nonlinear solve 与 differential equation 在这里相遇。为 two-bus case 选 \(S_\mathrm{base}\) 和各 voltage base，完成 per-unit conversion、power balance 与 Newton-Raphson mismatch；再把 operating point 转成简化 synchronous machine 的 rotor angle、mechanical power 与 swing-equation initial condition。传递时列出 bus voltage phasor、machine terminal power、internal emf 与 reactance，逐项说明从网络变量到机器变量的换算。用无扰动短仿真检查 rotor speed 保持同步、angle derivative 接近零、electric/mechanical power 差只对应设定损耗，这比直接施加 fault 更能暴露初值错误。

纸面与脚本共用一张 base/sign/convention 表，明确 line-to-line/phase、RMS/peak、generator/load sign、sequence component 与 torque direction。solver 报告 converged 后仍要检查 bus residual、generator reactive/voltage limit 与 Jacobian；动态开始时 electric power、mechanical power 和 speed 也要与稳态一致。故障前后若切换网络拓扑，还需分别给出 admittance matrix 和 clearing instant 的 state continuity。光滑的 rotor-angle curve 可能从错误初值出发，这些交叉量才是接口校验。

## 一个扰动同时经过网络约束、转矩与转角

电网分支建立小型 multi-bus case，声明 load、generation、line 与 voltage limit，使 power-flow residual 达到自定 tolerance，再施加 N-1、balanced/unbalanced fault 或 clearing-time sweep。机器分支把 synchronous 或 induction machine 接到 Thevenin source 与 mechanical load，计算 torque、flux、speed 与 loss，并运行 startup 或 load transient。两支合并时，把同一潮流工作点交给 machine model，画出网络事件怎样改变 electromagnetic torque 与 rotor state。

实体 three-phase supply、machine、transformer 与 fault rig 涉及市电、启动电流、旋转储能、裸露端子和机械卷入，只能在有保护与现场监督的实验室操作；校外默认用仿真或公开数据。报告应含数据来源、per-unit base、网络/机器图、方程、代码、solver version、原始结果与可手算小 case，并至少展示一个不收敛、reactive limit 越界、失步或 thermal constraint 超界的参数点。clearing-time sweep 还应在临界点附近加密，使“稳定/失步”判断不会只由粗网格决定。结论落在第一次越界及对应能量流，而非一条孤立的平滑电压或转速曲线。
