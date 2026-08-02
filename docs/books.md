---
title: EE 好书推荐
description: 按电子工程方向整理的教材与长期参考书，标明适用阶段、使用方式和合法获取入口。
page_type: guide
comments: true
last_reviewed: 2026-08-02
---


# EE 好书推荐

这不是“买齐就会”的书单。电子工程里，电路、场、器件、信号和控制使用不同的直觉；一本书很少能同时讲清理论、设计和实验。下面每一项都回答三个问题：它最擅长补哪块、什么时候读、从哪里合法获取。开放教材直接链接全文；商业教材只链接作者或出版社页面，不提供来路不明的 PDF。

刚开始时不要并行啃五本书。选一本主教材，配一门有作业或实验的[公开课](courses/index.md)，遇到明确问题再查第二本。书上的推导最终要落到计算、仿真或测量，否则很容易形成“看懂了”的错觉。

## 电路入门与电子学工作台

- **[Lessons in Electric Circuits / All About Circuits](https://www.allaboutcircuits.com/textbook/)**（开放在线教材）
  从直流、交流一路讲到半导体、数字电路、仪表和安全，检索方便，例子多。它很适合第一次补齐术语，或在搭电路前查一个具体概念；数学深度有限，学完节点法、暂态和频率响应后，应转入一门正规的电路课程。

- **[The Art of Electronics, 3rd ed.](https://www.book2look.com/book/9780521809269)**（Cambridge 出版社预览；纸书付费）
  这本书关心“真实元件接起来会怎样”，强项是器件选择、噪声、精密电路、接口和大量工程经验。它不是最温和的第一本电路理论教材：最好先学过线性电路，并在需要设计或排故时按主题查阅，而不是从头背到尾。

- **[Learning the Art of Electronics, 2nd ed.](https://www.cambridge.org/core/books/learning-the-art-of-electronics/9B9FA2FE6B1802BD4627B1F9825E8F0A)**（出版社页；付费）
  如果你真正缺的是实验训练，选这本配套实验书比只读《The Art of Electronics》更合适。新版实验覆盖模拟电路、FPGA 和 ARM 微控制器；开始前先核对仪器、器件和安全条件，不能把实验步骤当作无设备的纸面练习。

- **[Foundations of Analog and Digital Electronic Circuits](https://shop.elsevier.com/books/foundations-of-analog-and-digital-electronic-circuits/agarwal/978-0-08-050681-4)**（出版社页；付费，官方伴随材料部分开放）
  Agarwal 与 Lang 从 circuit abstraction、阻性网络和网络定理走到 MOSFET、小信号模型、暂态、正弦稳态与运放，正好构成一条完整的本科电路分析主线，也是 MIT 6.002 使用的教材。它把模拟与数字放进同一种抽象语言，强项是模型之间的衔接；若目标是大量传统网络定理题或三相电路，还要另配对应课程。读每章时应同时做 6.002 的题目，而不是只读概念。

## 仪器、探测与测量不确定度

- **[XYZs of Oscilloscopes Primer](https://www.tek.com/en/documents/primer/xyzs-oscilloscopes-primer)**（厂商开放入门手册）
  从波形、示波器结构、带宽、采样、触发和基本测量讲起，适合第一次接触示波器前建立词汇与控制面板概念。它是 Tektronix 编写的厂商手册，不是独立计量教材；型号选择和产品功能要与实际设备手册交叉核对。阅读后应能解释带宽与上升时间、采样率与记录长度的区别，并在已知低压信号上预先写出量程和时间基准。

- **[ABCs of Probes Primer](https://www.tek.com/en/documents/whitepaper/abcs-probes-primer)**（厂商开放探头手册）
  探头不是一根透明导线。这份手册把输入阻抗、尖端电容、带宽、上升时间、接地引线电感、差分/电流探头和安全额定值放进同一条测量链。它最适合配合一个低压、隔离且参数已知的 RC 或脉冲源阅读：先预测探头负载，再比较不同接地长度或衰减档的结果。任何高压、浮地或功率测量仍必须按设备类别、额定值和合格监督执行。

- **[JCGM 100:2008 — Guide to the Expression of Uncertainty in Measurement](https://www.bipm.org/en/committees/jc/jcgm/publications)**（BIPM/JCGM 官方开放标准指南）
  GUM 不是仪器操作手册，而是回答“这个测量结果到底说明了多少”的长期参考：被测量定义、输入量、标准不确定度、相关性、合成不确定度与报告方式。第一次阅读不必追完全部附录；先为一次电压或截止频率测量列出模型与不确定度来源，并区分分辨率、准确度、重复性和校准信息。它不能替代具体仪器手册，也不应被简化成给所有误差随意相加。

## 数学、概率与优化

- **[Introduction to Applied Linear Algebra: Vectors, Matrices, and Least Squares](https://stanford.edu/~boyd/vmls/)**（作者授权开放全文）
  以最小二乘、数据拟合和工程应用组织线性代数，配有视频、额外习题以及 Python/Julia 伴随材料。适合信号、控制和估计之前建立“矩阵在解决什么问题”的直觉；若后续要读严格的谱理论或证明，仍需补一门更理论化的线性代数。

- **[Introduction to Probability, Statistics, and Random Processes](https://www.probabilitycourse.com/)**（开放全文）
  面向本科高年级与研究生初段，概率、统计、随机过程和随机信号在同一套符号下展开，并有短视频、计算器和 Python 仿真章节。它是进入通信、噪声和估计的好主线；不要跳过条件概率和多元随机变量直接读随机过程。

- **[Convex Optimization](https://web.stanford.edu/~boyd/cvxbook/)**（作者授权开放全文）
  适合已经掌握多元微积分、线性代数，并开始接触控制、信号恢复、通信资源分配或电路优化的人。先读凸集、凸函数、对偶与 KKT 条件，再把书中方法用于一个可复算的小问题；它不是“优化算法速查表”，也不适合作为零基础数学入门。

## 信号、DSP 与反馈控制

- **[Signals and Systems, 2nd ed.](https://www.pearson.com/en-gb/subject-catalog/p/signals-and-systems-pearson-new-international-edition/P200000005151)**（出版社页；付费）
  Oppenheim、Willsky 与 Nawab 把连续时间和离散时间系统并行展开，从 LTI、卷积和 Fourier 表示走到采样、Laplace、Z 变换与反馈，是本科信号与系统的标准主教材。它比 DSP Guide 数学要求高，也更适合为通信、控制和数字信号处理打共同基础。不要只背变换表：每个系统同时画时域、频域和极零点表示，并用至少一道题检查因果、稳定和收敛域。

- **[The Scientist and Engineer's Guide to Digital Signal Processing](https://www.dspguide.com/)**（作者开放全文）
  用大量图和工程语言解释采样、卷积、频谱、数字滤波与 FFT，适合先建立直觉或在项目里快速定位方法。它有意降低数学门槛；如果目标是通信、估计或研究级 DSP，应再配一门严格处理复指数、DTFT、Z 变换和随机信号的课程。

- **[Feedback Systems: An Introduction for Scientists and Engineers, 2nd ed.](https://fbswiki.org/wiki/index.php/Feedback_Systems:_An_Introduction_for_Scientists_and_Engineers)**（出版社授权开放全文）
  Åström 与 Murray 把建模、时域响应、频域设计、鲁棒性和系统架构串在一起，官网还有章节 PDF、例题、FAQ、勘误和 Python 图形源码。先用低阶对象做完一次建模—分析—控制器—仿真的闭环，再读鲁棒性能；只会套 PID 公式并不等于学会反馈。

## 数字逻辑与计算机体系结构

- **[The Elements of Computing Systems / Nand2Tetris](https://www.nand2tetris.org/)**（图书付费；课程、软件与项目开放）
  从 NAND 门、HDL 和 CPU 一直搭到汇编器、编译器与操作系统，最大的价值是连续的项目链。它能回答“抽象层怎样接起来”，但不会深入 FPGA 时序收敛、CDC、总线协议或物理实现；完成硬件半程后，应转入[数字逻辑](courses/digital-logic/index.md)或 [FPGA/SoC](courses/fpga-soc/index.md)课程。

- **[Digital Design and Computer Architecture: RISC-V Edition](https://shop.elsevier.com/books/digital-design-and-computer-architecture-risc-v-edition/harris/978-0-12-820064-3)**（出版社页；付费，伴随资源部分开放）
  把组合/时序逻辑、SystemVerilog/VHDL、RISC-V 指令集、单周期/多周期/流水线处理器和存储层次放在一条线上。适合已经会基本编程、希望从 RTL 走到处理器的人；配套站提供 HDL、实验和讲义，读书时应真正跑仿真并查看波形。

## 嵌入式系统

- **[Making Embedded Systems, 2nd ed.](https://www.oreilly.com/library/view/making-embedded-systems/9781098151539/)**（出版社页；付费或订阅）
  重点不是某块开发板的寄存器，而是资源受限系统中的架构、状态机、中断、并发、错误处理、调试和功耗。它更适合已经写过 C、能让一块板子跑起来的人；边读边把一个轮询式小项目改造成可观测、可测试的结构，收获会比摘录设计模式大得多。

## 半导体器件与集成电路

- **[Fundamentals of Microelectronics, 3rd ed.](https://bcs.wiley.com/he-bcs/Books?action=index&bcsId=12028&itemId=1119694396)**（出版社官方伴随页；正文付费）
  Razavi 从半导体基础、二极管和双极/MOS 器件进入单级放大器、差分级、频率响应、反馈、振荡器和功率放大器，填补“学过器件，但还不会完整分析微电子电路”的本科主线。官方伴随页按章列出公式、图、实验、视频与部分题目资源，实际访问权限需逐项核对。它与后面的《Design of Analog CMOS Integrated Circuits》不是并行起步书：先用本书完成电路分析和 SPICE 复核，再进入设计权衡。

- **[Modern Semiconductor Devices for Integrated Circuits](https://www.chu.berkeley.edu/modern-semiconductor-devices-for-integrated-circuits-chenming-calvin-hu-2010/)**（作者页；章节开放）
  Chenming Hu 用紧凑篇幅讲清 PN 结、MOS 电容、MOSFET、缩放与器件限制。它适合有基础电磁学和固体物理后进入微电子，不适合只靠背能带图：每章至少把器件方程、工作区和一条可测 I–V/C–V 曲线对应起来。

- **[Design of Analog CMOS Integrated Circuits, 2nd ed.](https://www.mheducation.com/highered/product/design-of-analog-cmos-integrated-circuits-razavi.html)**（出版社页；付费）
  Razavi 的主线是从 MOS 器件直觉进入单级放大器、差分对、电流镜、频率响应、噪声、反馈、运放与 PLL。适合完成微电子电路基础后作为模拟 IC 主教材；只看公式不够，最好为每一章建立可运行的 SPICE 测试平台，并检查偏置、摆幅、增益带宽和工艺角。

- **[CMOS VLSI Design: A Circuits and Systems Perspective, 4th ed.](https://www.pearson.com/en-us/subject-catalog/p/cmos-vlsi-design-a-circuits-and-systems-perspective/P200000003427/9780137981076)**（出版社页；付费）
  从 CMOS 门延伸到延迟、功耗、互连、数据通路、存储阵列和片上系统，适合作为数字 VLSI 的第二步。它不能代替 HDL/综合实验；选择章节时应让逻辑努力、延迟估算或功耗模型与一次真实综合/布局结果互相校正。

## 通信与信息论

- **[Fundamentals of Wireless Communication](https://web.stanford.edu/~dntse/wireless_book.html)**（出版社许可的作者版全文）
  Tse 与 Viswanath 以信道、检测、容量、多用户与 MIMO 为主线，把概率、信息论和系统设计联系起来。它是研究生层次的无线通信教材，不是第一门通信课；在进入衰落和 MIMO 前，应先稳住随机变量、线性系统、基带表示和 AWGN 检测。

- **[Information Theory, Inference, and Learning Algorithms](https://www.inference.org.uk/mackay/itila/)**（作者开放全文）
  MacKay 把编码、贝叶斯推断和学习算法放在同一视角下，例子鲜活、跨度很大。适合已经学过概率、想理解“信息量、推断和编码为何相连”的读者；若只需要一门标准通信信息论，先沿熵—典型集—信道容量—编码定理读主线，不必一次追完神经网络和统计物理支线。

## 电磁场、微波与光子学

- **[Electromagnetic Field Theory: A Problem-Solving Approach](https://ocw.mit.edu/courses/res-6-002-electromagnetic-field-theory-a-problem-solving-approach-spring-2008/pages/textbook-contents/)**（MIT OpenCourseWare 开放全文）
  从矢量分析、电静力和边界值问题走到电磁感应、波、传输线、波导与辐射，章节习题和部分答案也在同页。它适合愿意动手算边界条件的人；学习时画清几何、法向和介质区域，比孤立背 Maxwell 方程更重要。

- **[Microwave Engineering, 4th ed.](https://bcs.wiley.com/he-bcs/Books?action=index&bcsId=6874&itemId=0470631554)**（出版社伴随页；正文付费）
  Pozar 是从电磁场进入微波网络、匹配、耦合器、滤波器与有源电路的经典主线。开始前应会传输线、复功率和 S 参数；Smith 圆图和匹配网络必须配合计算或仿真使用，不能只把图形步骤抄一遍。

- **[RP Photonics Encyclopedia](https://www.rp-photonics.com/encyclopedia.html)**（开放在线参考）
  覆盖激光、光纤、非线性光学、光通信、光电器件与测量，适合查概念、公式边界和进一步文献。它是作者持续维护的百科，不是一门按周推进的课程；用它解决一个明确问题，再回到系统教材或论文建立完整推导。

## 电力电子、电机与电力系统

- **[Fundamentals of Power Electronics, 3rd ed.](https://link.springer.com/book/10.1007/978-3-030-43881-4)**（出版社页；付费）
  适合高年级本科到研究生初段，主线是变换器稳态、开关器件、磁性元件、控制与设计权衡。先在低压隔离环境中用仿真验证伏秒/安秒平衡和小信号模型；书里的拓扑分析不构成直接操作市电或高能储能系统的许可。

- **[Electric Machines and Drives: A First Course](https://bcs.wiley.com/he-bcs/Books?action=contents&bcsId=7010&itemId=1118074815)**（出版社伴随页；正文付费）
  以机电能量转换、磁路、直流/交流电机、空间矢量和驱动控制建立第一条电机主线。适合已经学过三相电路和基础控制的人；至少配一套额定值受控的仿真或教学平台，把转矩—转速曲线、损耗和控制器限制对应起来。

- **[Electric Power Systems: A First Course](https://bcs.wiley.com/he-bcs/Books?action=index&bcsId=7091&itemId=1118074793)**（出版社伴随页；正文付费）
  面向第一次接触电力系统的读者，重点是三相系统、变压器、输电、潮流、故障和稳定性的系统视角。它与电力电子不是替代关系：前者解释电网中的功率和约束，后者解释变换器。任何涉及市电、并网或高压的实践都应在合格实验室和监督下进行。

## 机器人与机电系统

- **[Modern Robotics: Mechanics, Planning, and Control](https://hades.mech.northwestern.edu/index.php/Modern_Robotics)**（作者站提供开放预印本、视频、练习与代码）
  从刚体运动、运动学和动力学走到轨迹、规划、控制、抓取与移动机器人，符号统一，配套 Python/MATLAB/Mathematica 代码。它适合学过线性代数、微积分和基础力学后系统进入机器人；若目标是做出实机，还要并行补电机驱动、传感器、实时软件和安全停机。

## 怎么从书单真正开始

如果还没有明确方向，从 **All About Circuits + 一门电路公开课** 起步；想做数字硬件，就走 **Nand2Tetris → Digital Design and Computer Architecture**；想进信号或控制，先用 **18.03/6.003 + 18.06** 接稳微分方程、LTI 系统和线性代数，再进入 DSP Guide 或 Feedback Systems。只有当问题开始涉及噪声、估计、随机输入或通信时，才把概率接进主线。想进芯片，则先把 **电路 + 器件** 接稳，再分到 Razavi 或 Weste/Harris。

选择后只做一件小事：把准备读的章节、配套题目和一个验证任务写下来。例如“读 Feedback Systems 第 2 章，复算两个一阶对象，为其中一个画闭环响应并解释稳态误差”。完成一个代表性的“章节—习题—验证”闭环后，若仍只能复述句子、不能独立建模或复现实验，就缩小范围、补先修或换一门有反馈的课程，不要继续加书。

书籍的版次、售价、地区可用性和配套资源会变化。购买前以作者/出版社页面为准；发现链接失效、版本变化或更合适的合法入口，可以在本页下方留言，或按[贡献指南](contributing.md)提交修正。
