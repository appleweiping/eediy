## 6.071J、Real Analog 和 6.091 需要不同的工作台

[MIT 6.071J](024-6-071j.md)的[官方档案](https://ocw.mit.edu/courses/6-071j-introduction-to-electronics-signals-and-measurement-spring-2006)把电子学、信号与测量放进 25 次实验及配套作业、测验，适合已有通用示波器、函数发生器和数据采集条件，并愿意迁移旧 LabVIEW 流程的人；公开答案链不完整。[Real Analog](027-real-analog.md)把讲义、练习与实验接得更紧，[官方器材页](https://digilent.com/shop/coursework-learning-resources)围绕 Analog Discovery 2/3，价格和地区供应会直接影响路线。[MIT 6.091](025-6-091.md)是短而密的焊接、晶体管、数字芯片和电机接口训练，却不提供一学期的连续反馈。

通常在 6.071J 与 Real Analog 中选一门贯穿全程，再从 6.091 取一个正好补缺的短实验。通用台式仪器充足时，6.071J 的测量范围更广；已有指定 Digilent 设备时，Real Analog 的校外闭环更直接；只有少量台面时间时，6.091 适合建立基本操作，但不能代替完整电路与误差分析。

## 第一次实验发生在上电之前

拿到原理图后，用[电路分析](../circuits/index.md)标出地参考、测试点与电流路径，算 DC operating point、波形范围和元件耗散，并写下需要立即断电的异常读数。DMM 电流档可能把节点短接，普通示波器地夹不能随意接到浮动电路，探头电容也会改变高阻节点；这些判断来自电路结构和仪器输入，而非照抄接线图。

KCL/KVL、受控源、一阶暂态、正弦稳态和基本运放还不稳时，台面实验会被接线错误淹没；分析没有问题但不会设置限流、探头倍率、触发和采样率时，可以从 6.091 最小仪器练习起步。实验的第一项结果应是带单位和容差的预测，让测量有机会反驳它，目标不宜预设成“得到教材波形”。

## 迁移旧实验时，仪器输入和误差也一起改变

6.071J 的 LabVIEW virtual instrument、旧 DAQ 和部分器件需要替换；Real Analog 从 Analog Discovery 移到台式示波器与信号源后，input impedance、range、sampling 和 data export 都会变化；6.091 中的 555、TTL 与老式 ADC/DAC 也要重新核对 pinout 和 rating。替代器件与仪器应围绕 measurand、stimulus、bandwidth、accuracy 和 decision rule 比较，相似屏幕截图不能证明实验等价。

实体实验只在隔离、低压、限流环境中进行，断电改线，不接市电、人体或来历不明的电源。公开 demonstration 可以说明现象，但缺 BOM、校准、原始数据和异常记录时仍只是演示。迁移说明注明原实验年份、替换件、仪器型号与无法复现的现场指导，避免把现代工具的便利误写成原课条件。

## 一个小系统要经得住多次重新测量

选择含 sensor input、gain/filter 和 output load 的低压系统。schematic、BOM、rating check、仪器设置、calibration、手算预测、raw data 与重建图表的脚本要能对应同一测试点。专门测一次 probe loading 或元件公差，再加入 open circuit、wrong value 或 bias fault；调试说明按实际观测、最小假设、单一变量和新读数展开。

uncertainty budget 区分 resolution、repeatability 与 systematic effect，再让另一位学习者只按文字步骤复测一个指标。记录对方第一个需要猜的 ground、range、test point 或 shutdown condition，修改步骤直到该猜测消失。剩余偏差若属于 sensor transfer/noise，就把 raw trace 与 calibration 带到测量仪器；若属于 event timing 或 peripheral state，就把同一条 trace 带到嵌入式。真正的交接是可复测的测量，不是尝试过多少个实验。
