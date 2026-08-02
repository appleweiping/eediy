---
title: "电力电子"
description: "变换器拓扑、磁性元件、调制与闭环控制；高压和大功率实验默认仿真或受监督。"
page_type: track
track_id: "track-power-electronics"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 12b0e0c2bfdcfca9 -->

# 电力电子

## 方向定位

变换器拓扑、磁性元件、调制与闭环控制；高压和大功率实验默认仿真或受监督。

## 建议先修方向

- [电路分析](../circuits/index.md)
- [控制系统](../control-systems/index.md)
- [电子实验与测量](../electronics-laboratory/index.md)

## 6.622 是一条完整设计叙事，Coursera 是三段式序列

[MIT 6.622](114-6-622.md)的[官方 OCW 页面](https://ocw.mit.edu/courses/6-622-power-electronics-spring-2023/)把 switching conversion、magnetics、semiconductor loss、modeling 与 feedback control 放在同一门课里，公开视频、手写讲义、习题、考试和 design project 足够支撑一次完整学习。Coursera 路线按依赖拆开：[Introduction to Power Electronics](115-power-electronics-1.md)的[官方页](https://www.coursera.org/learn/power-electronics)由仿真建立 switching state 与 steady-state quantity，[Converter Circuits](116-power-electronics-2.md)进入非隔离/隔离 topology，[Converter Control](117-power-electronics-3.md)才完成 small-signal model 与 loop design。三门顺序有实质依赖，不能只挑标题熟悉的一门。

这两条是替代路线，无须合并成四门必修。愿意做较重纸笔题、希望一次贯穿设计链，可选 6.622；需要短模块与持续 simulation feedback，可完成 Coursera 序列。完成 6.622 后只需抽取一个 LTspice 或 control exercise 校准工具。只做 Coursera 第一门则应诚实停在 steady-state conversion，尚未覆盖 magnetics、device stress 与 closed-loop boundary。选定路线后，把每周的 topology、magnetics、loss 与 control 题都落到同一组 converter specification 上，课程各单元才会汇合成设计。

## 一只 buck 在三个模型里回答三个问题

在理想 buck 上画导通/关断电流路径，由[电路分析](../circuits/index.md)的电感伏秒与电容电荷平衡推出 conversion ratio、ripple 与 CCM/DCM boundary。解析式用于 steady-state ratio、stress 和数量级；averaged model 在 operating point 附近给出 control-to-output pole/zero，服务于[控制系统](../control-systems/index.md)的 crossover 与 phase margin；switched model 才能显示 ripple、dead time、parasitic 与 startup。三者在共同有效频段应有一致趋势，不要求逐点波形重合。

仿真注明 device model、temperature、step size、startup condition、steady-state window 与 disturbance time，并比较 nominal 和至少两个 corner。运行模型前纸算 inductor slope、output ripple 与 duty，偏差才容易分成符号、参数与 solver 设置。还要在 switching period、control bandwidth 和 line/load transient 三种时间尺度上各选观察窗，避免把 ripple 当控制振荡，或把启动过程误读成稳态。line/load step 后若 duty saturation、magnetic saturation 或 oscillation 出现，应沿 energy path 和 control path 解释，不能只调 compensation 直到曲线顺眼。

## 台面波形只在隔离低压平台上增加一层证据

[电子实验](../electronics-laboratory/index.md)中的限流、隔离、差分测量与紧急断电必须在 schematic 阶段出现。实体延伸默认限制为隔离、current-bounded low voltage；不直连市电，不自行测试未知高能 transformer，也不用普通接地 probe 跨 high-side switch。semiconductor voltage/current/SOA/junction temperature、magnetic saturation/temperature rise、PCB spacing 与停机后储能要分别核算。6.622 公开设计材料不提供校外高功率设施，Coursera grader 与 feedback 也可能依赖付费账户。

没有相应台面时，报告在 simulation 层结束，并逐项说明 thermal、EMI 与 physical parasitic 尚未验证。低压实物若存在，则给 current limit、isolation、probe connection、startup current 与 stop condition；还要把 input/output power 的测量带宽、探头误差和稳态窗口写清。一条漂亮 switching waveform 本身不能证明安全或效率。

## 用 line/load step 判决两个 topology

给出 input range、output/load、ripple、efficiency、transient、switching frequency、size proxy 与 allowable temperature rise，在 buck、boost、flyback 或另一边界明确的候选中至少比较两个。逐一列 switching state、CCM/DCM range、device stress、magnetic value 与 loss model，再解释为什么留下其中一个。controller 同时报告 crossover、phase margin、control saturation 和 line/load transient；在三个工作角落上指出第一项越界约束。

项目包含 analytic derivation、averaged 与 switched source、model version、corner sweep 和原始 trace。一次不满足规格的运行要能追到 inductor saturation、duty limit、loop dynamics 或 thermal assumption，并导致具体设计修改。两种 topology 使用同一输入范围、负载阶跃、器件温度和损耗定义，比较才有意义。结论最终回答：哪一个输入/负载角落最早触及哪项约束，哪个模型提前给出了迹象，以及仍有哪些量只有真实硬件才能回答。

## 课程清单

| 课程 | 机构 | 角色 | 编辑证据 | 实践资源 |
|---|---|---|---|---|
| [Power Electronics](114-6-622.md) | MIT | 主课 | 公开材料导读 | 有公开作业或实验 |
| [Introduction to Power Electronics](115-power-electronics-1.md) | University of Colorado Boulder | 可替代 | 公开材料导读 | 部分开放或受限 |
| [Converter Circuits](116-power-electronics-2.md) | University of Colorado Boulder | 可替代 | 公开材料导读 | 部分开放或受限 |
| [Converter Control](117-power-electronics-3.md) | University of Colorado Boulder | 可替代 | 公开材料导读 | 部分开放或受限 |
