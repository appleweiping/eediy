## EE 140/240A 把同一组规格反复送进作业、实验和项目

模拟 IC 从晶体管级开始。[Berkeley 的正式课程目录](https://www2.eecs.berkeley.edu/Courses/ELENG140/)将 EE 105 列为 EE 140/240A 的先修；需要带入 MOS I–V、\(g_m\)、\(r_o\)、body effect、single-stage small-signal model，以及[模拟电子](../analog-electronics/index.md)中的反馈、频响、噪声与稳定性。[Berkeley EE 140/240A](141-ee-140-ee-240a.md)公开的 21 份 lecture PDF、10 份 homework、8 个 lab 和 mixed-signal final project 依次经过 bias、single stage、differential pair、feedback、noise、op-amp、oscillator 与 data converter。它的长处是规格在推导、testbench 与设计决定中反复出现。

[NPTEL Analog IC Design](036-108106105-noc26-ee66.md)提供 12 周的 MOS 小信号、current mirror、差分级、频率响应、反馈和 fully differential/CMFB 讲解，适合补 Berkeley 讲义中跳得太快的地方，却没有开放的版图验证链。沿 Berkeley 的题目顺序推进、在卡点调用对应 NPTEL 周次，比串行重修两门更节省时间。

这里的先修不只是会写几个小信号公式。面对一组增益、摆幅、负载和功耗要求，需要能判断各指标分别由偏置电流、器件尺寸、输出电阻还是补偿网络控制；否则后续实验容易退化成无方向的参数搜索。

## 公开 LTspice、台面测量和校园 Cadence 是三种不同条件

第一层是公开文件能重建的 LTspice 子集。[Lab 1](https://people.eecs.berkeley.edu/~pister/140sp23/labs/lab1.pdf)前半段使用手算与 LTspice；旧 [Lab 3 Part 1](https://people.eecs.berkeley.edu/~pister/140sp23/labs/lab3_1.pdf)配有可直接下载的 [`BJTopamp.asc`](https://people.eecs.berkeley.edu/~pister/140sp23/labs/BJTopamp.asc)，可以重跑 BJT op-amp 的 operating point 与 sweep。第二层是 breadboard、示波器读数、slew/compensation measurement 与 GSI initials；`.asc` 能打开并不完成这些现场环节。

第三层才是 Spring 2025 的校园 IC flow。[Lab 2](https://people.eecs.berkeley.edu/~pister/140sp25/labs/lab2.pdf)、Lab 4–8 和[设计项目](https://people.eecs.berkeley.edu/~pister/140sp25/labs/project.pdf)依赖校内 Virtuoso server、SKY130 PDK、libraries、DRC/LVS/PEX 与 instructor setup。缺少这些条件时，可以用 ngspice、Xschem、KLayout 或另一套合法工具做独立迁移，但项目说明需列 model deck、device mapping、corner、tool version，以及未复现的仿真、台面或校园条件。

这三层最好在目录和图表标题上也保持分开：公开网表的结果、面包板读数、校园版图验证各自回答不同问题，不能在一张性能汇总表里省略来源。教材、模型和服务器权限同样要逐项说明，购买一本书也不会自动获得工艺文件。

## 每一个性能结论都要匹配它所在的层

schematic simulation 只能支持 pre-layout gain、stability、noise 与 power；没有实体测量，simulated slew 或 noise 不能写成 bench result；没有 mismatch model，就没有 statistical-yield 结论；没有 extracted parasitic，schematic GBW 也不等同于 post-layout 结果。NPTEL 的 enrollment、graded assignment 和 certificate exam 会随 run 改变，公开视频本身不产生正式评分。

可以拿给定 supply、load、gain 与 bandwidth 的 differential pair 做交底：给出 bias、headroom、output swing、dominant pole，并画清 differential path 与 common-mode feedback 的职责。若 transistor-level node 仍只能靠 ideal-op-amp 规则解释，多级补偿暂时只会增加符号。收敛警告、缺失模型、启动状态和极端工作区也属于结论边界，仿真顺利退出不能自动覆盖它们。

结果表中的每一行还应能回到具体测量定义。例如相位裕度采用哪一个环路断点、噪声积分覆盖哪个频带、功耗是否包含偏置支路，都可能改变数字的含义。定义不一致时，两个“更好”的数字没有直接可比性。

## 一颗小放大器足以呈现取舍

选择 two-stage op-amp、OTA 或 fully differential gain stage，把 DC gain、GBW、phase margin、slew rate、output swing、input-referred noise、power、load 和 area proxy 写成规格表。手算 bias 与 compensation 后，为各项性能建立独立 testbench，再做 operating point、AC、transient、noise、PVT、load step，以及一次 startup 或 saturation case。一版因追求 GBW 而牺牲 phase margin、swing 或 power 的 sizing，往往比最终 nominal 图更能解释设计。

有可靠且获准使用的 open-PDK flow 时，才加入 schematic、layout、DRC/LVS 与 post-layout comparison；否则明确止于 pre-layout。更关键的判断是：load 或 bias current 改变后，能否由电流、跨导、极点和补偿电容预判 bandwidth、stability、swing 与 power 的方向。

规格之间发生冲突时，应回到电流路径和节点电容解释，无需继续添加扫描维度。一处清楚的取舍推导，往往比几十组尺寸组合更接近真实设计工作。

## 版图、数据转换器和 RF 改变的是不同问题

当偏置、环路稳定性与 PVT 行为已经可解释，下一步才分叉。parasitic、matching、floorplan 和 physical verification 主导时进入 layout；comparator、sampling、clocking 与 digital calibration 成为主角时转 mixed-signal/data converter；器件 \(f_T\)、matching network、noise figure 与 distributed effects 主导时才是 RFIC。

同一颗 op-amp 不会自动覆盖三条分支。结束主线时，应能指出设计最早受 headroom、noise、stability、speed、power 或 area 中哪一项限制，并说明下一门课会改变哪个模型或工具层。这个答案比把“做出版图”当成统一结课条件更可靠。

如果还无法分辨问题属于器件模型、反馈网络还是物理实现，继续留在小放大器上会更有效；分支课程并不会替基础设计自动补上因果解释。
