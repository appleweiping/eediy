---
title: "控制系统"
description: "状态空间、稳定性、频域设计、估计与最优控制，强调仿真、实验和模型失配。"
page_type: track
track_id: "track-control-systems"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: c8774cf2a6a801cf -->

# 控制系统

## 方向定位

状态空间、稳定性、频域设计、估计与最优控制，强调仿真、实验和模型失配。

!!! warning "开始前请确认这些课程的材料限制"
    - [Feedback Systems: An Introduction for Scientists and Engineers](073-cds-101-cds-110.md)：入口是作者维护的第二版教材配套站，提供开放文本、实例、习题和更新后的 Python 图源，但不是当前完整课程运行页；教师习题手册仍受限。

## 建议先修方向

- [信号与系统](../signals-systems/index.md)
- [工程数学](../mathematics/index.md)

## 开放教材、实验档案和状态空间课并不互相替代

[Feedback Systems companion](073-cds-101-cds-110.md)及其[开放教材站](https://fbswiki.org/wiki/index.php/Feedback_Systems:_An_Introduction_for_Scientists_and_Engineers)把 modeling、analysis、design 与 robustness 连在一条线里；它是 companion 和 archive，校外学习不会产生 CDS 101/110 的在课评分。[MIT 6.302](067-6-302.md)的[官方档案](https://ocw.mit.edu/courses/6-302-feedback-systems-spring-2007)用 Bode、root locus、compensation 和 motor/thermal/op-amp lab 训练经典频域判断。官方 syllabus 假设已学 linear systems、电路、物理与数学，并有先前 circuit laboratory 经验，不能当成微积分后的零基础入口。[Stanford EE 263 archive](068-ee-263.md)则从线性代数进入 state space。

第一遍默认选 [MIT 6.302](067-6-302.md)，因为它把经典反馈判断落实到电子与机电实验；缺少安全实验台条件时，改用 Feedback Systems 的开放教材与 companion 作为无实验替代。需要 formal controllability、observability、realization、estimation、robust stability 和 robust performance 时，再加入 [MIT 6.241J](069-6-241j.md)或 2008 EE 263。四门课处理的入口和证据不同，不必按编号全部串起来。

选择后应让同一个对象至少穿过建模、分析和设计三部分。不断更换只展示某种方法优点的例子，会掩盖坐标、线性化和性能指标之间的接口。

## 一只二阶对象要同时经得住物理、极点和实验解释

[信号与系统](../signals-systems/index.md)提供 poles/zeros、convolution、frequency response、sampling 与 stability，[工程数学](../mathematics/index.md)提供 ODE、eigenvalue、quadratic form、optimization 和 probability。选择 motor、thermal process 或 mass-spring-damper，由物理量建立 state model，求 equilibrium、linearization 与 transfer function，并以单位、能量和极限情形检查。

对相同 poles/eigenvalues 区分 internal、input-output 与 asymptotic stability，再预测 step response 和 Bode 特征。随后设计 classical 或 state-feedback controller，比较两组 specification，并同时看 stability margin、transient、control effort、saturation 与 sample-time sensitivity。“仿真没有发散”无法构成稳定性证明；state、input、output 和 disturbance 单位不一致时，控制器曲线再漂亮也建立在错误对象上。

还应手算一次质量、阻尼、延迟或采样周期改变后的趋势。若变化方向只能从软件图上事后读取，就很难判断仿真是在验证模型，还是模型正在迎合仿真结果。

## 高级课程应回答基线控制器怎样失效

[MIT 6.243J](070-6-243j.md)处理 nonlinear stability、Lyapunov、backstepping 和 adaptive control；[6.245](071-6-245.md)处理 MIMO、\(H_\infty\)、\(\mu\) 与 LMI；[6.231](072-6-231.md)处理 stochastic decision 和 dynamic programming。摆类系统的线性控制只在小区域有效时，6.243J 有具体入口；多输入对象在 uncertainty 下无法同时满足 stability/performance 时，才需要 6.245；状态包含随机资源或调度决定时，再使用 6.231。

对同一二阶或低阶对象分别注入 parameter error、delay、noise 或 disturbance，选一个 nominal 成功而 perturbed 失效的案例。误差拆成 model、discretization、measurement 与 controller 四类，说明未覆盖的 operating region。新方法若不能指出修正了哪条名义假设，增加数学复杂度只会遮住基线问题。

## 年份决定哪些作业、软件和结论可以放在一起

6.302 缺主教材讲义，1985 录像来自另一时期，不能直接当作 2007 课堂；motor、thermal、op-amp lab 也需要重新选择安全低压 BOM。这里的 EE 263 是 2008 Linear Dynamical Systems 档案；Fall 2025 起同号课已改为 Matrix Methods/SVD，当前 Julia 作业不能与旧 MATLAB 材料混成一个学期。6.241J 没有视频且答案不全，6.243J 没有 video/lab 闭环，6.245 的 MATLAB/LMI 流程有年代，6.231 页面列出的 6 个 related videos 并非本课录像。

最后交付一个版本化的低阶模型、一组 nominal run 和一组 perturbed run，注明 solver、tolerance、discretization 与移植中的不等价功能。能解释扰动结果的术语决定下一门课：非线性 region of attraction 进入 6.243J，多变量 uncertainty bound 进入 6.245，随机 policy 或资源决定进入 6.231。若三者都不是解释所必需，当前 baseline model 和 controller 还值得再迭代一轮。

## 课程清单

| 课程 | 机构 | 角色 | 编辑证据 | 实践资源 |
|---|---|---|---|---|
| [Introduction to Linear Dynamical Systems (2008 Archive)](068-ee-263.md) | Stanford University | 主课 | 公开材料导读 | 有公开作业或实验 |
| [Feedback Systems: An Introduction for Scientists and Engineers](073-cds-101-cds-110.md) | Caltech | 主课 — 材料限制待确认 | 公开材料导读 | 部分开放或受限 |
| [Feedback Systems](067-6-302.md) | MIT | 主课 | 公开材料导读 | 有公开作业或实验 |
| [Dynamic Systems and Control](069-6-241j.md) | MIT | 可替代 | 公开材料导读 | 部分开放或受限 |
| [Dynamics of Nonlinear Systems](070-6-243j.md) | MIT | 补充材料 | 公开材料导读 | 部分开放或受限 |
| [Dynamic Programming and Stochastic Control](072-6-231.md) | MIT | 补充材料 | 公开材料导读 | 部分开放或受限 |
| [Multivariable Control Systems](071-6-245.md) | MIT | 补充材料 | 公开材料导读 | 部分开放或受限 |
