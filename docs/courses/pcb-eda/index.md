---
title: "PCB、EDA 与硬件验证"
description: "原理图、版图、制造文件、BOM、调试与设计评审，让电路从仿真走到可制造、可测试硬件。"
page_type: track
track_id: "track-pcb-eda"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 352f461aea0f7ebe -->

# PCB、EDA 与硬件验证

## 方向定位

原理图、版图、制造文件、BOM、调试与设计评审，让电路从仿真走到可制造、可测试硬件。

## 建议先修方向

- [电路分析](../circuits/index.md)
- [电子实验与测量](../electronics-laboratory/index.md)

## 八个 MIT 实验足够带出第一块板

[MIT IAP PCB 2026](055-iap-pcb-2026.md)的[官方课程站](https://pcb.mit.edu/)围绕 8 个 KiCad/Altium 实验展开，从 schematic capture、layout、review、制造输出一直走到 bring-up；讲义、代码和课程流程采用开放许可，但 Panopto、板厂与 BOM 的实际成本仍需当期确认。[WPI Essentials of PCB Design](056-essentials-of-pcb-design.md)的[官方站点](https://pcb.wpi.edu/)公开 slides、starter/sample board 与 KiCad/GitHub 资源，录屏则需要 WPI 账户。第一次做板可完整跟 MIT 的实验节奏，再用 WPI 样板核对目录、library 与提交文件；没有必要同时复刻两套板。只想学会读原理图或审查制造包，也可以在数字评审结束，不必为了“做完课程”仓促下单。

## 原理图、布局与制造包是三次不同的评审

原理图评审从一张 interface table 开始。为低压 sensor/MCU board 的每个连接写 supply/current、logic level、connector pinout、source/load、bandwidth 和 test point，并从 datasheet 分开摘出 absolute maximum、recommended operating condition 与 footprint。这里会直接用到[电路分析](../circuits/index.md)中的电源、回流、接口阻抗、filtering 与 decoupling：最坏 rail current 要能算出，高速或脉冲电流的 return path 要能画出，pull-up、bulk capacitor 和 local bypass 解决的时间尺度也要讲清。MIT lab 中的 ERC 通过只说明连接规则没有被触发，不说明接口选择正确。

布局评审关注 placement、decoupling loop、return path、connector/ESD、电源铜宽、test point 与装配方向。自建及第三方 symbol、footprint、3D model 要注明来源和许可，每个 land pattern 对照 datasheet 检查 pin numbering、courtyard、paste 与 mask。制造评审则面对机器真正读取的 Gerber、drill 和 placement 文件：stack-up、minimum trace/space、drill、copper weight、controlled impedance 与 panel 条件来自某次具体报价，不能永久沿用课程默认值。用独立 viewer 打开导出文件，逐层核对 board outline、孔、阻焊和极性；生产输入以这些导出层为准。WPI sample board 可在这一轮充当第二份文件组织样例，尤其适合核对 library path 与 fabrication note 是否随项目移动。

## Bring-up 的起点是限流电源与静态检查

项目目录至少包含 requirements、block diagram、interface/power budget、可编辑 schematic/PCB、ERC/DRC 输出、规则来源、BOM/替代料、Gerber、钻孔、坐标文件与 fabrication README。KiCad、ngspice、gerbv 和 Git 的版本应可见；BOM 同时考虑地区供货、替代件、EOL 与装配方向。若课程录屏或 Altium 专有步骤无法访问，就说明采用了哪一种功能等价的 KiCad 操作，不能把迁移后的过程写成原 lab。

实体板只在隔离、限流低压条件下继续。[电子实验](../electronics-laboratory/index.md)中的断电连续性、短路、极性与探头接法检查完成后，按 rail 上电，观察 quiescent current 与关键节点，再运行功能测试和 open/short 等受控异常。电池、马达、继电器或外部高能端口需要额外保护。把第一次未通过的检查留在 bring-up log 中，记录它对应的 schematic node、layout location、制造文件或装配方向，以及修订后重测结果；板厂输入和台面证据由此闭合在同一次具体返工上。

## 课程清单

| 课程 | 机构 | 角色 | 编辑证据 | 实践资源 |
|---|---|---|---|---|
| [The Art and Science of PCB Design](055-iap-pcb-2026.md) | MIT | 主课 | 公开材料导读 | 部分开放或受限 |
| [Essentials of PCB Design](056-essentials-of-pcb-design.md) | Worcester Polytechnic Institute | 补充材料 | 公开材料导读 | 有公开作业或实验 |
