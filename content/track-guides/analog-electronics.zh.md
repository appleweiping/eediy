## 6.101 的六次实验和七周项目才是主线

[MIT 6.101](026-6-101.md)以设计课组织模拟电子，而非器件名词表。[课程主页](https://ocw.mit.edu/courses/6-101-introductory-analog-electronics-laboratory-spring-2007)里的六次实验从二极管、晶体管和运放逐步走到反馈、频率响应与仪器使用，最后七周留给一个完整项目。它公开了题面和相当多的教学材料，但部分阅读付费，BOM、器件与台面条件也停在 2007 年。选它意味着接受“按原问题重做、按今天的器件迁移”，并不意味着照着旧料号采购。

工作台条件较弱时，[NPTEL Analog Circuits](034-108101094.md)的[官方课程页](https://nptel.ac.in/courses/108101094)提供更连续的视频周次与题目；[IC、MOSFET、Op-Amp 及应用](035-108108111.md)则从工艺、器件一路讲到运放应用。二者适合补 6.101 中跳得太快的一章，却没有六次实验和七周项目那样的反馈链。通常是一门项目主线配一套讲解材料，无需把三门相近的基础内容同时重修。

对校外学习者而言，是否能取得仪器、器件和原始题面，比课程编号的先后更值得优先确认。

## 一次工作点检查，比一叠波特图更能说明问题

把[电路分析](../circuits/index.md)和[电子实验](../electronics-laboratory/index.md)放在同一个共源或共射级上。由偏置判断器件区域，求 \(g_m\)、\(r_o\)、中频增益、输入/输出电阻、headroom 和主导极点；再把电源、限流、探头地与信号源的连接画在原理图旁。SPICE 扫描之后测 DC 点、线性摆幅和频率响应，分别估计模型、器件离散性与 probe loading 对偏差的贡献。

只会套理想运放规则时，可以用有限 GBW、slew rate、offset、output range 与容性负载做一组短实验。关键并非曲线是否平滑，而是能否在上电或运行仿真之前指出最早受限的是工作区、输出电流、摆幅还是极点。实体实验限定在隔离、低压、限流条件；没有台面仪器时，结论清楚标为 simulation-only。

## 6.301 公开的 25 组 recitation 适合作为专题库

能独立完成单级放大器后，可从 [MIT 6.301](032-6-301.md)挑多级放大与反馈设计。官方 syllabus 要求 6.012，并假定已经掌握 6.003 中的 Bode、Laplace、transfer function 与 complex impedance。现存公开 recitation 编号为 1–26、缺 17；此外还有 9 份无解 assignment、Lab 1、Lab 2、Design Problem 与历史考试，但主课堂讲义和视频没有形成连续开放主线，因此更适合作为高级专题练习库。[6.331](033-6-331.md)也应按具体高级电路问题查阅；课程编号更高，不代表整门接在 6.101 后面就更有效。

沿 6.101 做项目时，可以把 6.301 的一组反馈或补偿题嵌入相同电路。这样，同一份工作点、负载与频率规格会同时接受手算、仿真和台面检验。若换用现代器件，要逐项比较 pinout、供电、功耗、带宽、稳定负载与模型来源；报告注明仿真器版本、温度和 model corner，不能用“功能相近”代替迁移依据。

## 一颗低频前端能把边界讲清

低频 sensor front end 或两级放大器足以作为收束。规格表写 source impedance、signal range、supply、load、gain、bandwidth、noise、offset、swing 与 power；两种 topology 用相同的偏置和误差预算比较，再分别跑 operating point、AC、transient、load 与 temperature sweep。有安全台面时增加原始测量，否则停在 schematic simulation。

收束时只把 load、supply 或 temperature 中一项推到规格外，找出最先被破坏的约束。若解释仍落在偏置、反馈符号或探头连接，就继续修同一个前端；若剩余不确定性已经是 PVT、mismatch、寄生、面积或片上功耗，则把原规格表和 schematic 带入[模拟集成电路](../analog-ic/index.md)。没有授权 PDK 时，这次交接仍止于 schematic/pre-layout，不能据此声称 fabricated-silicon 性能。
