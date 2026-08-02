## 6.002 是一条重主线，Linear Circuits 1–2 是两段式替代

[MIT 6.002](021-6-002.md)把节点分析、动态网络、小信号电子学、作业、实验与考试放在同一门课里；[官方 2007 档案](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007)材料很全，但不同年份的实验与课堂页不能拼成一个虚构学期。[Linear Circuits 1](022-linear-circuits-1.md)和 [Linear Circuits 2](023-linear-circuits-2.md)分别处理 DC/暂态与 AC，[第一段官方页](https://www.coursera.org/learn/linear-circuits-dcanalysis)显示的是平台课程，反馈、付费和开放范围可能变化；两段合起来才是一条替代主线。

[Cornell ECE 2100](028-ece-2100.md)公开的 prelab 与实验说明适合给上述任一路线增加台面练习，但它缺连续讲义、解答和同学期考试，无法单独承担理论。更合理的组合是 6.002，或 Georgia Tech 两段课，再配一个对应 Cornell 实验。四门全修会重复节点方程，却不会自动改善对探头、地参考与元件公差的判断。

## 让同一个网络依次经过纸面、网表和测量

本方向依赖[工程数学](../mathematics/index.md)中的小型线性系统、复数极坐标和一阶初值问题，也依赖[物理基础](../physics/index.md)中的电荷、能量、功率与 passive sign convention。选择一个含电阻、储能元件及受控源或运放的低压网络，统一节点名和 reference direction，求 DC operating point、暂态初终值与 time constant、AC transfer function 和 power balance。

网表运行前写下 \(t=0^+\)、\(t\to\infty\)、\(\omega\to0\) 与 \(\omega\to\infty\) 的极限和符号预期；随后用 ngspice、LTspice 或 Qucs-S 计算，再在安全条件下测 DC 点和频率响应。KCL/KVL residual、参数扫描和 probe-loading 估计可以区分方程符号、模型、元件公差与仪器误差。代数无法闭合时回数学，电压、电流和功率方向互相冲突时回物理；软件不负责替学习者选择节点、初值与单位。

没有示波器或信号源时，工作止于 simulation/prelab。实体实验使用隔离、限流、低压供电，并注明探头、地参考、量程和元件公差。软件波形与实测曲线即使相似，也只有在激励、负载、带宽和不确定度一致时才可比较。

## 档案缺口和下一分支都应从这个网络读出来

6.002 的 2007 教学页与更早实验不逐项对应，Lecture 24 还有缺页；Linear Circuits 的平台演示没有可移植的 BOM、完整仪器设置和原始数据；ECE 2100 也不公开现场指导与全部反馈。说明中注明采用的年份、仿真器版本、模型来源及没有执行的台面环节，避免把几套材料包装成一门“完整版”课程。

结束时限时完成一份未见过的综合题，再用简短说明和 discrepancy table 重建主要曲线，表中明确 frequency、load 与 uncertainty。表里第一个解释不了的现象决定后续：晶体管工作点、反馈或噪声进入[模拟电子](../analog-electronics/index.md)；离散时间、频谱或滤波进入信号与系统；transmission line、field boundary 或 radiation 进入电磁场。下一方向继续使用这只网络及其 conservation、initial condition、impedance 与 frequency-response 检查，不另换一个失去上下文的例子。
