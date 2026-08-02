## 三个公开档案，对应三种项目工作室

[Cornell ECE 4760 / 5730](057-ece-4760-ece-5730.md)围绕 embedded product 展开；[当前课程站](https://ece4760.github.io/)使用 RP2350/Pico 2，labs、demo 与多年学生项目网页把实现、测量和展示放在同一节奏里。[Cornell ECE 3400](062-ece-3400.md)的[公开档案](https://ocw.ece.cornell.edu/courses/ece-3400-ece-practice-and-design)以 maze robot 连接机械、电路、感知和软件，但讲义、考核与部分链接不全。[MIT 6.270](076-6-270.md)的[2005 课程页](https://ocw.mit.edu/courses/6-270-autonomous-robot-design-competition-january-iap-2005)公开 Assignments 1–7、团队过程和竞赛作品，controller 与 sensors 已是历史硬件。

这三门课各自代表一种项目工作室。MCU 产品适合沿 ECE 4760 的 lab—project 节奏；移动机器人可借 ECE 3400 的子系统接口；短周期竞赛则从 6.270 的策略、分工和现场约束入手。选择其中一个真实问题环境，比拼接三套器材清单更接近课程本意。

## ECE 4760 的价值在连续的小型实现

ECE 4760 当前页面能看到 RP2350/Pico 2 的 labs、C 示例、视频演示和学生项目档案。阅读重点在观察每个项目怎样从定时、外设和通信走向可测输出，而非复刻某届作品。自己的题目应在最早阶段打通 sensor→state transition→observable output，并把输入范围、单位、更新率、异常状态和一项外部测量写清。

[电子实验](../electronics-laboratory/index.md)负责限流供电、测量与接线，[编程与工具](../programming-tools/index.md)负责可重建的 build、test 和版本历史，[嵌入式系统](../embedded-systems/index.md)负责 interrupt、timer、driver 与 concurrency。若程序只在开发者电脑上靠手工步骤运行，主要问题属于构建环境；若同一现象无法区分软件状态和电气输入，就把观测点移到接口两端，无需增加云服务或视觉模型。

## ECE 3400 与 6.270 关注的是物理集成和团队节拍

Maze robot 把电机、供电、传感、定位和策略放在同一有限空间里。适合按物理耦合安排集成：电源和急停可用后接单个驱动，再让一个传感通道控制一个动作，最后才加入地图或规划。团队不应按“机械、电路、软件”各自做到最后才总装；围绕能运行的子系统切片分工，接口争议会更早暴露。

6.270 的公开 assignments 可以研究短周期里怎样压缩决策与测试，但 2005 controller、sensor 与比赛场地不再是采购建议。它的竞赛成绩、现场指导和团队反馈也不能由校外复现。若项目需要策略比较，可以在同一仿真或安全场地上跑确定起始条件，说明随机性、碰撞规则和计分方式；不同硬件、地图与软件版本的成绩缺少无条件排名的共同基准。

## 年代、替换件和能量边界都属于设计

RP2350/Pico 2、ECE 3400 robot kit 和 6.270 controller 分属不同年代与开放程度。BOM 需要 revision、datasheet、voltage/current、mechanical interface、compiler/SDK、license、spare 与替代测试。换传感器、驱动器或板卡时，电气、时序和机械接口都可能变化；用小夹具比较关键行为，再决定迁移范围。

实体工作保持低压、限流。motor、battery/charger、moving mechanism、laser/IR 和 high-current driver 各自需要能量上限、夹伤/起火/眼睛风险与 emergency stop。无法安全测试的动作应改成假负载、台架或仿真。校外同伴可以讨论设计和观看 demo，却不能提供 Cornell/MIT credit、竞赛成绩或合格的现场安全监督。

安全条件应直接影响项目范围，而不只是写在报告末尾。

## 作品的去向由最难解释的接口决定

一个可交接的项目应从干净环境完成 build/flash，并能找到 source、schematic/pin map、BOM、接口说明、测试输入、原始 trace、demo 与简短 postmortem。这里没有统一要求做 PCB、云端或复杂机构；课程特有的出口可以是一项 RP2350 外设测量、一段 maze-robot 集成结果，或一个带明确规则的竞赛策略比较。

从 postmortem 中挑一个输入、输出与失效证据仍不完整的接口，把它写成下一门课的第一个问题。timer、driver、memory 或 concurrency trace 交给嵌入式；calibration residual 交给仪器或 DSP；estimation/dynamics mismatch 交给 robotics/control；反复出现的供电或 signal-integrity fault 则回电子实验与硬件设计。交接沿用同一条 trace 和 subsystem，不再把作品改名成更大的通用“毕业设计”。
