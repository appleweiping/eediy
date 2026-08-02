---
title: 技术写作
description: 把电子工程中的问题、方法、数据和限制写成别人能够判断与复现的文档。
page_type: guide
comments: true
---

# 技术写作

一份技术文档最怕读者只能“相信作者说做过了”。问题是什么、采用了什么条件、数据支持哪一个结论、还有哪些事尚未证明，都应该能在文中找到。实验报告、设计说明和操作文档面对的读者不同，但都要让工程判断回到可追溯的事实上。

## 先决定读者看完要做什么

动笔前先写一句“读者将用这份文档来……”。如果答案是选择方案，正文应围绕需求、候选设计和 trade-off；如果是复现实验，应优先给设备、连接、版本、步骤、原始数据和异常处理；如果是维护系统，则要先给接口、正常状态、危险边界和诊断路径。把同一份长文同时当论文、使用手册和实验日志，通常会让三类读者都找不到入口。

IEEE Professional Communication Society 的[工程报告写作指南](https://procomm.ieee.org/communication-resources-for-engineers/written-reports/write-effective-reports/)把 methods、results 和 discussion 分开：方法说明做了什么，结果呈现得到什么，讨论解释这些结果意味着什么。即使只写课程项目，这个区分也很有用。不要在方法段提前宣布成功，也不要让结论引入正文从未出现的新数据。

标题和开头应具体到对象与范围。“低噪声放大器设计”信息太少；“5 V 供电、1 kHz–100 kHz 传感前端的噪声与带宽权衡”让读者立即知道边界。摘要或首段可用四句话完成：问题、方法、主要定量结果、最重要限制。写不出这四句，往往说明工程问题本身还没有收束。

## 让每个结论带着条件出现

一句可靠的工程陈述至少包含对象、条件、指标、数值/方向和取得方式。例如，“在 5 V 供电、10 kΩ 负载和 10× probe 下，prototype 的 \(-3\ \mathrm{dB}\) bandwidth 为……，由三次 frequency sweep 得到”，比“电路带宽很好”多出的不是文风，而是可检验性。

把 predicted、simulated 和 measured 明确分开。仿真结果要写 simulator、model 来源、版本、corner、initial condition 与求解设置；测量结果要写仪器、probe、calibration 状态、采样与处理；理论值要写假设和适用近似。三条曲线放在一张图里时，图例和正文都不能把它们统称为 “result”。

这份 IEEE 工程报告指南还体现了几条值得沿用的习惯：术语前后一致，变量首次出现即定义，图表按出现顺序编号，并在正文中说明读者应从图里看出什么。课程作业不必模仿整套出版格式，但不能让排版掩盖定义和条件。

## 图表必须交代量、单位和测量条件

一张图首先回答“横纵轴各是什么量”。轴名、单位、scale、采样间隔和数据处理不能藏在脚本里；多个 dataset 要有可区分的 line style/marker，不能只靠颜色。曲线很多时，宁可拆图，也不要让图例覆盖数据。示波器截图适合保留异常细节，但最终报告还应导出数据并重画带单位的坐标轴。

NIST 的[SI 文稿检查说明](https://www.nist.gov/pml/special-publication-811/nist-guide-si-check-list-reviewing-manuscripts)强调使用标准 quantity/unit symbols，并避免含混的非标准缩写。EE 中尤其要小心 `m`/`M`、`V`/`dBV`、Hz/rad·s\(^{-1}\)、RMS/peak/peak-to-peak，以及 dB 的 reference。表头和坐标轴给出单位，正文不要让一个裸数字独自承担量纲。

图题应写出读图所需的条件，而不是重复标题。例如频响图题可以给 supply、load、probe、sweep method 和 nominal/corner；波形图要说明 trigger、bandwidth limit、averaging 和时间零点；照片应标 test point 与信号方向。读者若必须回看三页才能知道蓝线是什么，这张图还没有完成沟通任务。

## 误差、异常和负结果应留在正文

测量值不是没有误差的真值。NIST [Technical Note 1297](https://www.nist.gov/pml/nist-technical-note-1297)给出评定和表达测量不确定度的方法，并区分从重复观察得到的分量与从仪器规格、校准等信息估计的分量。课程报告至少要说明重复次数与散布、仪器准确度/分辨率来源、处理步骤，以及结果的有效数字为何合理。

不要用误差棒装饰一张仍未定义 measurand 的图。先说明究竟测的是某个时刻的 voltage、稳态平均、拟合得到的 gain，还是频带内积分 noise；然后列出会改变它的主要因素。若无法形成完整 uncertainty budget，可以诚实报告已知上界、repeatability 和尚未量化项。

负结果是设计信息。振荡只在某条 probe ground lead 下出现，说明测量连接可能参与了系统；某个 corner 不收敛，可能是数值设置，也可能暴露模型边界；三块板只有两块通过，不能只展示最好的一块。正文应写观察、排查顺序和当前最有根据的解释，并把猜测标成猜测。

## 引用和版本要让结论回到原处

引用应落在它支持的陈述旁边。datasheet 要给 manufacturer、part number、revision 和相关 table/figure；标准或论文要给 edition/date/DOI；网页要尽量链接到机构或作者的一手页面。IEEE Author Center 当前公开的[参考文献样式指南](https://docs.google.com/document/d/1j1L96U2NagwWI9MEVDNVKt9pXxRzTH7h3krI3Mb6wZE/edit?usp=sharing)给出 datasheet、standards、reports、software 和 online sources 等常见类型的格式。格式可以由工具生成，但作者仍要确认链接指向的版本确实支持正文。

复现入口应短而明确：数据在哪里，使用哪个提交，执行什么命令，会产生哪张图。原生的原理图和 PCB 工程文件无论是文本还是二进制，都应保留；另行导出 PDF、网表、BOM 或制造文件，方便没有同一软件和许可证的读者检查。大型原始数据可以放外部存储，但文档中要给稳定标识、校验和或版本。

最直接的检验，是把文档交给不了解项目的人，请对方找出一个关键结论的条件、从原始数据重算一个指标，并指出 measured 与 simulated 的边界。三件事都能在不靠口头补充的情况下完成，文档才真正承担了工程沟通。
