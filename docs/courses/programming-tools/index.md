---
title: "编程与工程计算"
description: "Python、C、版本控制、可复现实验与数值工具，强调把分析变成可验证的软件。"
page_type: track
track_id: "track-programming-tools"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: cb1c5911d7db942d -->

# 编程与工程计算

## 方向定位

Python、C、版本控制、可复现实验与数值工具，强调把分析变成可验证的软件。

## 建议先修方向

- 无

## 6.100L、6.087 与 6.057 对应三种真实工程文件

[MIT 6.100L](015-6-100l.md)的[官方课程页](https://ocw.mit.edu/courses/6-100l-introduction-to-cs-and-programming-using-python-fall-2022/)适合第一次系统学习 Python：函数、数据结构、测试和调试能直接处理数值模型、CSV 与仪器数据；没有传统考试，但 Python 3 材料和编程练习足以形成连续反馈。[MIT 6.087](016-6-087.md)的[官方归档](https://ocw.mit.edu/courses/6-087-practical-programming-in-c-january-iap-2010/)转向编译、指针、数组布局、文件和系统接口，主要依靠讲义、练习、lab 与代码，旧 UNIX 命令需要写出现代等价做法。[MIT 6.057](017-6-057.md)只在后续确实出现 `.m` 文件、合法 MATLAB 环境或 toolbox 依赖时加入；其[官方 syllabus](https://ocw.mit.edu/courses/6-057-introduction-to-matlab-january-iap-2019/pages/syllabus/)不能替代许可证。GNU Octave 移植要注明语法、toolbox 和数值差异。

典型组合无须三门全修。[信号与系统](../signals-systems/index.md)可用 Python 建 reference model，再取 6.087 的数组、文件与性能题；[嵌入式系统](../embedded-systems/index.md)则需要认真完成 C 的编译、内存与 I/O。课程的价值最终落在真实文件上：Python notebook 或 package、可警告全开的 C build、以及确有需求才出现的 MATLAB/Octave artifact。选择标准是后续仓库实际包含的数据、binary 和脚本类型，而非语言名称的数量。

## 一个数值内核同时接受语言契约与诊断工具审问

选 FIR、校准曲线、寄存器转换或 CSV parser，用 Python 明确 dtype、shape、单位、缺失值、边界长度和异常行为，再由手算样例与单元测试给出 reference。C 版本显式选择整数宽度、signedness、buffer ownership、长度参数、overflow policy 与 return code。两边共享正常、空输入、最大/最小值、截断、非法字段和浮点边界向量；整数逐项一致，浮点 tolerance 必须能由算法和表示误差解释。

Python 端注明 interpreter 与依赖环境，C 端注明 compiler、language standard、warning 和 optimization flags；在严格 warning 下编译，再用 AddressSanitizer、UndefinedBehaviorSanitizer、静态分析与边界输入检查内存。benchmark 同时给数据规模、CPU、优化级别与 peak memory。串口、GPIO 或仪器输入应封装成 host-side byte stream，测试断开、timeout、半帧与重放；容器只能约束用户态依赖，不能证明 USB timing、driver 或实时延迟相同。删掉报错用例或放宽 tolerance 都不属于诊断。

## 二进制仪器日志把课程练习变成可审查的软件

定义含 sync word、timestamp、channel、fixed-point ADC value 与 CRC 的小格式。Python 生成合法和损坏样本、给出参考解析、单位换算与图；C 用 streaming buffer 处理 endian、split frame、bad CRC、counter wrap 和 overflow。至少十组固定文件覆盖噪声前缀、半帧、错误长度、错误 CRC、回绕及连续帧，两个实现输出同一组结构化结果。再故意加入一次 off-by-one、sign extension 或 scale 错误，用最小输入定位，并把该输入写入 regression。

仓库中的 format specification、vector checksum、build/test command、benchmark 原始结果与短分析应从干净目录一条命令重建。更换合法 channel count 或 sample rate 不应要求手工修改 parser 内部状态；损坏数据必须报告位置，不能静默生成貌似合理的工程量。这项工作比“会 Python 和 C”更精确：它说明同一份仪器字节在两种内存模型下仍遵守同一契约。

## 课程清单

| 课程 | 机构 | 角色 | 编辑证据 | 实践资源 |
|---|---|---|---|---|
| [Introduction to CS and Programming Using Python](015-6-100l.md) | MIT | 主课 | 公开材料导读 | 有公开作业或实验 |
| [Practical Programming in C](016-6-087.md) | MIT | 主课 | 公开材料导读 | 有公开作业或实验 |
| [Introduction to MATLAB](017-6-057.md) | MIT | 补充材料 | 公开材料导读 | 部分开放或受限 |
