---
title: "物理基础"
description: "力学、电磁学、波动与量子基础，面向机器人、场与波、器件和光电方向。"
page_type: track
track_id: "track-physics"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 2d48d9c45c435964 -->

# 物理基础

## 方向定位

力学、电磁学、波动与量子基础，面向机器人、场与波、器件和光电方向。

## 建议先修方向

- [工程数学](../mathematics/index.md)

## 8.01SC 用受力与守恒训练建模动作

[8.01SC](010-8-01sc.md)的[官方 OCW 页面](https://ocw.mit.edu/courses/8-01sc-classical-mechanics-fall-2016/)不只是高中力学复习。课程用 problem set、worked example 与在线教材反复要求从受力、约束、动量、能量和角动量建立模型，这套动作会在机器人、机电系统与控制中重复出现。学习时选一类对象贯穿数周，例如 spring–mass、pendulum 或 rotating body；每题先画坐标、力和约束，再写守恒或运动方程，最后用单位、极端位置与能量方向质询答案。8.01SC 的公开考试档案不完整，因此应额外做限时题或与同伴逐步核对，而不是用播放进度代替反馈。

## 8.02X 与 8.03SC 把 lumped circuit 推向 field 和 mode

[8.02X](011-8-02x.md)的[官方课程归档](https://ocw.mit.edu/courses/8-02x-physics-ii-electricity-magnetism-with-an-experimental-focus-spring-2005/)把 charge、potential、field、magnetism 与 circuit 接起来，并有明确实验取向；它是电路直觉走向 Maxwell equation 的桥。[8.03SC](012-8-03sc.md)则用 vibration、coupled mode 与 wave propagation，把 signal、acoustics、electromagnetics 和 optics 放进共同图像。对低压 RC/RLC，8.02X 负责由 field/charge 解释元件关系，8.03SC 负责 resonance、normal mode、dispersion 与 boundary。课程号相邻不表示必须连续完整播放：做电路和电磁可优先 8.02X，需要 transmission 与 mode 时再深入 8.03SC。

[工程数学](../mathematics/index.md)要与对象同步。8.01SC 可并行单变量微积分；8.02X 前应能处理 vector、integral 与基本 differential equation；8.03SC 前应会解二阶线性方程并理解 complex exponential。历史实验涉及高压电容、强磁场或特殊装置时，只使用官方数据、低能量替代或仿真；课程 safety 文件与现场设施不能被一段 PDF 替代。

## 8.04 与 8.05 是一条正式的两学期量子序列

[8.04](013-8-04.md)适合 semiconductor、nanoelectronics 或 photonics 已经提出 quantum state、potential well、tunneling 与 measurement language 的路线；经典电路、嵌入式和控制无需为了“物理完整”强行加入。[8.05](014-8-05.md)不是补充包，而是 MIT 正式第二门量子力学课。其[官方 syllabus](https://ocw.mit.edu/courses/8-05-quantum-physics-ii-fall-2013/pages/syllabus/)要求 8.04 成绩达到 C 或以上，再系统处理 quantum dynamics、two-state systems、angular momentum/spin、radial equation、operator method 与 identical particles。

选择量子分支前，应能把一维势阱写成本征值问题，解释 normalization、expectation value 与 measurement probability，并在某个极限连接经典图像。本站的 [8.04](013-8-04.md)采用 Spring 2016：10 套 problem set 没有链接本版解答，考试也没有完整答案链；另一个 [Spring 2013 官方归档](https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2013/pages/assignments/)为 10 套题全部提供解答，可作为标明年份的平行反馈，不能冒充 2016 answer key。8.05 的练习与考试反馈同样不完整，独立推导与限时练习不可省略。当前问题若仍是 motor torque、RC response 或 classical wave，继续把主线对象做深，比提前记 bra-ket notation 更有效。

## 一组 residual 把“定律正确”改写为“模型何时适用”

选择安全的 spring–mass、低压 RC/RLC、coupled pendulum 或 one-dimensional wave model。由明确的 physical assumption 推出 equation 与 boundary condition，形成解析或数值预测，再在多个 operating point 上与公开数据、仿真或真实低能量测量比较。原始数据、calibration、uncertainty 与 residual plot 应让读者区分 parameter-estimation、numerical、measurement 与 model discrepancy。

结论应落在 residual 首次出现系统偏离的位置：指出失效的是 linearity、lumped approximation、loss model、boundary condition 还是 classical scale，并写出下一模型必须增加的状态或相互作用。读者若能从这处偏离追回原始数据、方程与假设，再用修正后的模型解释同一组 operating point，这个物理项目就已经给后续 EE 课程留下了可复用的模型边界。

## 课程清单

| 课程 | 机构 | 角色 | 编辑证据 | 实践资源 |
|---|---|---|---|---|
| [Classical Mechanics](010-8-01sc.md) | MIT | 主课 | 公开材料导读 | 有公开作业或实验 |
| [Physics III: Vibrations and Waves](012-8-03sc.md) | MIT | 主课 | 公开材料导读 | 部分开放或受限 |
| [Physics II: Electricity and Magnetism with an Experimental Focus](011-8-02x.md) | MIT | 主课 | 公开材料导读 | 有公开作业或实验 |
| [Quantum Physics I](013-8-04.md) | MIT | 可替代 | 公开材料导读 | 部分开放或受限 |
| [Quantum Physics II](014-8-05.md) | MIT | 补充材料 | 公开材料导读 | 部分开放或受限 |
