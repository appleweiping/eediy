---
title: 项目实践
description: 从规格、模型、实现和测量出发，做一个能解释差异的电子工程项目。
page_type: guide
comments: true
---

# 项目实践

一块板子能点亮、一段 RTL 能上板，都还不等于项目已经回答了工程问题。更关键的是：你能否事先作出预测，做出实现，再说明预测为什么成立、又在哪里失效。对 EE 学习者而言，一个范围收得住的低压小系统，只要规格清楚、测量可靠，往往比功能很多却无法解释的“综合项目”更有价值。

## 仓库里可以直接运行的起点

下面 5 个 starter 都提交了源码与故障用例，发布检查会在真实工具链中重建它们。表中的 Python 命令从仓库根目录运行；两个 CMake workflow 在各自 starter 目录运行。它们是 EEDIY 的独立练习，不是所映射大学课程的官方作业。

| 起点 | 运行命令 | 这一步真正检查什么 |
|---|---|---|
| [RC 低通：解析与 ngspice](https://github.com/appleweiping/eediy/tree/main/examples/rc-lowpass) | `python examples/rc-lowpass/run.py` | 解析阶跃与频响基线、参数和生成数据校验和；完整发布门禁另跑 ngspice 网表并比较 \(\tau\) 与截止频率 |
| [固定容量 ring buffer](https://github.com/appleweiping/eediy/tree/main/examples/ring-buffer) | `cmake --workflow --preset host-sanitized` | 空、满、回绕、ADC/DMA adapter 与故障版本；ASan/UBSan 必须真实执行 |
| [带超时的 sensor sampler](https://github.com/appleweiping/eediy/tree/main/examples/sensor-sampler) | `cmake --workflow --preset host-sanitized` | 正常采样、超时、延迟中断、总线错误与取消路径，输出逐行可判定 |
| [同步 FIFO 仿真、形式验证与综合](https://github.com/appleweiping/eediy/tree/main/examples/sync-fifo) | `python examples/sync-fifo/run_checks.py --require-tools all` | Icarus/Verilator 仿真、SymbiYosys 反例与 Yosys 综合；故障实现必须失败 |
| [TMP117 两层 KiCad 板](https://github.com/appleweiping/eediy/tree/main/examples/tmp117-kicad) | `python examples/tmp117-kicad/export.py --require-kicad` | ERC、DRC、引脚一致性和制造文件导出；不含实板测量 |

如果某条命令缺工具就跳过，结果不能写成通过；发布环境使用上表的严格参数，缺依赖直接失败。第一次阅读时先看各目录 README 的“它没有证明什么”，再把 starter 改造成自己的课程项目。

## 什么时候值得从习题升级成项目

当一道题只有唯一输入和标准答案时，先把题做好；当它开始出现接口、容差、噪声、时序、功耗或成本之间的取舍时，才值得做成项目。适合开题的问题通常能写成一句带条件的问句，例如：“在 5 V 供电和指定传感器源阻抗下，能否把 10–40 °C 映射到 ADC 的有效输入范围，同时让带内噪声和建立时间满足给定上限？”

这个问句已经限定了输入、环境、输出和主要矛盾。相反，“做一个智能温度计”仍然太大，因为显示、联网、外壳和算法都可能掩盖模拟前端是否真正工作。第一次项目最好只保留一个主要未知量：是模型不准、实现不稳，还是测量方法改变了被测对象。若同时有五个未知接口，调试只会退化成换零件。

## 先写一条可能失败的规格

规格必须允许结果判定为“不通过”。NASA [Systems Engineering Handbook 的 Appendix C](https://www.nasa.gov/reference/system-engineering-handbook-appendix/)强调区分强制要求、事实和目标；[Appendix D 需求验证矩阵](https://www.nasa.gov/reference/appendix-d-requirements-verification-matrix/)要求每条 “shall” 预先对应分析、检查、演示或测试方法。学生项目不需要照搬航天文档，但这两个原则非常实用。

开工前用一页写清：

- 工作范围：允许的输入、供电、负载、时钟、温度或数据分布；
- 可测指标：增益误差、带宽、噪声、延迟、吞吐、功耗、资源占用等，带单位和容差；
- 明确非目标：例如不做隔离、不接市电、不追求量产 EMI 合规；
- 测量方法：测试点、仪器带宽与输入阻抗、采样方式、重复次数和通过条件；
- 失效状态：饱和、振荡、溢出、丢样、时序违例或过热时，系统应怎样进入安全状态。

如果一项指标只能写成“效果好”或“运行稳定”，它还不是规格。若阈值暂时不知道，可以先写成待探索参数，并安排一次小实验得到数量级；不要在项目结束后根据最好看的结果倒写目标。

## 让模型、实现和测量互相找错

第一版模型只需足够回答设计选择。模拟电路可以从工作点、增益、极点和噪声预算开始；数字电路可以从状态转移、吞吐、最坏延迟和资源估算开始；信号处理可以先给出采样、频谱和误差传播。模型中每个参数都应有来源：datasheet 条件、手算假设、课程模型或已测数据。

实现时先做能暴露核心风险的最小版本。模拟前端先验证 bias、headroom 和单级频响，再接 ADC；FPGA 先让 reference model 与 self-checking testbench 对上，再上板；控制系统先确认传感器符号、采样周期和 actuator limit，再闭环。一次只改变一个可解释因素，并保留失败结果，因为“改了三个值以后好了”无法建立因果关系。

测量也不是中立观察。Tektronix 的[探头基础说明](https://www.tek.com/en/documents/whitepaper/abcs-probes-primer)把探头、示波器和信号源视为同一测量系统，并说明输入电阻、电容、带宽和接地会改变波形。记录探头倍率、带宽限制、耦合、采样率、负载和测试点；换探头后结果变化，首先应怀疑测量负载，而不是立即修改电路。

最后比较 prediction、simulation 和 measurement。偏差应落到具体原因：模型遗漏、器件离散、数值设置、实现错误、仪器限制或环境变化。NIST 的[测量不确定度指南](https://www.nist.gov/pml/nist-technical-note-1297)区分统计得到的分量与由规格、校准等信息估计的分量；学生项目至少应报告重复测量的散布、仪器分辨率/准确度来源，以及哪些误差仍未量化。

## 一个有分量的 EE 小项目长什么样

以低压 sensor front end 为例：先给出传感器范围和源阻抗，选择保护、增益、filter 与 ADC interface；手算 headroom、noise、settling 和 alias 风险；用 SPICE 扫 supply、component tolerance 与 load；再在面包板或 PCB 上测 DC transfer、frequency response、noise floor 和 step response。最关键的成果不是一张漂亮频响图，而是能指出哪一段由 op-amp GBW 限制、哪一段受 probe/ADC loading 影响，以及误差预算中哪一项占主导。

同样的方法可以迁移到数字或信号项目。UART receiver 要有波特率偏差、metastability 与 framing-error 条件；FIR accelerator 要比较 fixed-point 量化、吞吐、latency 与资源；motor control 的软件仿真要区分 plant model、sensor noise、saturation 和 sample delay。若涉及真实电机、高能电池、市电或其他危险源，先缩到隔离的低能量仿真/台架，并遵守[实验安全指南](safety.md)；项目价值不来自把自己置于更高风险。

## 怎样判断项目真的有效

项目可以停在“回答了原问题”的时刻，而不是功能再也加不动的时候。有效的结果应满足三点：换一组处于规格范围内的输入仍能预测方向；从原始数据可以重算主要指标；出现偏差时能定位到模型、实现或测量中的一层。若只有最终视频、截图或自动生成报告，这三件事都无法判断。

留下足够让未来的自己重跑的材料：当前规格与非目标、带版本的 schematic/RTL/code、模型和参数来源、BOM 或依赖、原始数据、生成图表的命令、仪器设置，以及没有通过的条件。最后用两段话回答：“哪个工程判断被数据支持？”和“在什么边界外，这个结论不再成立？”能回答这两问，项目才真正把课程知识变成了工程能力。
