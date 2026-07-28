---
title: "光电、光子与 MEMS"
description: "完成一个有模式/器件仿真、工艺约束、版图和性能预算的光子或 MEMS 设计。"
page_type: route
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 3209ba8462e4a8ed -->

# 光电、光子与 MEMS

[English](../en/routes/photonics-mems.md) · [← 学习路线](index.md)

## 适合人群

希望从电磁与量子基础进入光电器件、集成光子和微机电系统的学习者

## 最终验收

完成一个有模式/器件仿真、工艺约束、版图和性能预算的光子或 MEMS 设计。

!!! warning "路线中的主线审计复核项"
    - [Silicon Photonics Design, Fabrication and Data Analysis](../courses/optics-photonics/133-phot1x.md)：课程按期开放，商业工具许可、地区注册、流片日期和付费条件会变化；只返回测量数据，不邮寄芯片，必须在每次开课前人工复核。 最近审计：2026-07-29。

## 阶段安排

### 物理与场

**选课要求：** 完成全部 4 门必修；其余 1 门仅在需要补缺时选学。

- [Physics II: Electricity and Magnetism with an Experimental Focus](../courses/physics/011-8-02x.md) — **必修**; MIT; 主线; A
- [Physics III: Vibrations and Waves](../courses/physics/012-8-03sc.md) — **必修**; MIT; 主线; S
- [Quantum Physics I](../courses/physics/013-8-04.md) — **可选补充**; MIT; 替代; A
- [Electromagnetic Fields and Waves](../courses/electromagnetics/107-ece-3030.md) — **必修**; Cornell University; 主线; S
- [Physics of Semiconductors and Nanostructures](../courses/semiconductor-devices/124-ece-4070.md) — **必修**; Cornell University; 主线; A

**阶段退出条件：** 求解一个波导或谐振腔的模式，并用独立数值方法复核；前三个本征频率与解析或收敛基准偏差低于 2%，归一化场能量误差低于 1%。

### 器件与工艺

**选课要求：** 完成全部 2 门必修，并从 2 门选修候选中选择 1 门。

- [Micro/Nano Processing Technology](../courses/fabrication-mems/126-6-152j.md) — **必修**; MIT; 主线; S
- [Design and Fabrication of Microelectromechanical Devices](../courses/fabrication-mems/129-6-777j.md) — **选修候选**; MIT; 主线; A
- [Quantum Optics for Photonics](../courses/optics-photonics/130-ece-5310.md) — **选修候选**; Cornell University; 替代; A
- [Semiconductor Optoelectronics](../courses/optics-photonics/131-ece-5330.md) — **必修**; Cornell University; 主线; A

**阶段退出条件：** 设计一个光电、波导或 MEMS 器件并绑定可制造工艺，扫描至少 3 个关键尺寸；报告灵敏度、容差窗口和最坏角落性能，版图通过所采用的规则检查。

### 光子系统

**选课要求：** 完成全部 1 门必修，并从 2 门选修候选中选择 1 门。其余 1 门为可选补充，不计入本阶段选修数。

- [Introduction to Photonics](../courses/optics-photonics/132-108106135.md) — **必修**; IIT Madras / NPTEL; 主线; S
- [Silicon Photonics Design, Fabrication and Data Analysis](../courses/optics-photonics/133-phot1x.md) — **可选补充**; University of British Columbia; 主线; A; **审计复核中**
- [Optics](../courses/optics-photonics/134-2-71.md) — **选修候选**; MIT; 替代; S
- [Photonic Materials and Devices](../courses/optics-photonics/135-3-46.md) — **选修候选**; MIT; 补充; B

**阶段退出条件：** 完成片上或自由空间光链路预算，验证插入损耗、带宽、串扰和每比特能耗；对尺寸与材料偏差运行不少于 200 次蒙特卡洛试验并报告规格良率。

## 执行规则

- 按每个阶段的选课要求完成全部必修与指定数量的选修；若提供完整路径选项，只选择一条并按序完成其中全部课程；可选补充只用于填补明确缺口。
- 阶段内至少完成一个可复现产物，并把失败记录纳入复盘。
- 涉及市电、高压、射频辐射、激光、化学品或加工设备时，必须遵守本地法规并由合格人员监督。
