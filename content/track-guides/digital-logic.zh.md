## 三条主线用三种项目回答“数字系统是什么”

[MIT 6.004](037-6-004.md)从组合逻辑走到处理器结构；[官方 2017 档案](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017)提供 21 个教学单元及视频、annotated slides 和 worksheet，syllabus 虽列 7 个 lab，公开导航却没有实验文件。[官方 2009 档案](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2009/)另有 8 个公开 lab、tutorial problem 与历史 quiz/exam，工具链也属于旧版本。适合用 2017 讲授配 2009 练习，但每项成果都要保留年份，不能写成 MIT 曾经开设的一门合成版本。[ETH DDCA](038-ddca.md)把 2025 视频、讲义、习题和代码放在同一版本，[公开视频索引](https://people.inf.ethz.ch/omutlu/lecture-videos.html)适合配 SystemVerilog、Vivado 与 Basys 3 实际综合。[Nand2Tetris I](039-nand2tetris-i.md)用自带 HDL simulator 和 6 个累积项目从 NAND 搭到计算机，硬件门槛最低，却不训练 FPGA timing constraints 与 board I/O。

三条路线各自完整：6.004 给处理器全景，DDCA 给现代 HDL/FPGA 工具，Nand2Tetris 给逐层接口。通常选一条做完项目。[Cornell ECE 2300](041-ece-2300.md)只有公开讲义，没有 homework、lab 和 exam，可作为某个概念的第二种讲法，不能替代项目主线。选课时比较愿意完成哪一种处理器或 FPGA 工作，学校和视频数量只作背景。

材料的开放边界也会改变作品形式：有完整实验包可以沿原题推进，只有讲义时就只能把自建模块明确写成独立练习，不能补写不存在的课程考核。

## 一页 ISA、一个 testbench 和首次错误周期构成核心练习

[编程与工具](../programming-tools/index.md)应能支持版本控制、脚本、位运算和命令行测试；[电路分析](../circuits/index.md)提供电压逻辑、组合延迟、时钟与储能。由 truth table 化简组合逻辑并穷举输入，再把文字 specification 画成带明确 reset 的 FSM，最后为 registered datapath 写 self-checking testbench，覆盖正常、边界与非法输入。setup/hold、clock-to-Q 和 metastability 说不清时，需要补时序物理；只能靠 GUI 手点波形时，需要补测试自动化。

随后从一页 ISA 实现 ALU、registered state、controller/FSM、memory interface 与一段程序。reference model、edge-case table 和最小反例与 HDL 同仓库；选择一条 instruction，逐层写 encoding、control、datapath value、cycle boundary 与 visible result，再改一个 control bit 并预测首次错误周期。6.004 的两个年份不能拼成同一学期成绩；DDCA 项目注明 Vivado、target part、board files、constraints 和 warning policy；没有 Basys 3 时止于 pre-board；Nand2Tetris 许可要求项目答案保持私有，公开作品只展示自写测试和非答案说明。

## 综合报告决定下一步是体系结构、验证还是 FPGA

仿真通过不代表 synthesis timing 收敛，LED 亮起也不替代 reference model。对同一设计报告 utilization、critical path、clock period、cycle count、CPI 与 memory behavior；有板卡时让 bitstream 对应 source commit，并用确定输入演示。新增 instruction 应只触及定义清楚的 decode、control 与 datapath 边界，旧测试负责暴露遗漏。

用一条新增 instruction 做交接测试：它的 specification、state transition、reference result、首次错误周期、synthesis timing 与 source commit 必须互相对上。architectural result 还不稳定时，问题仍属于数字逻辑；这条链闭合后，pipeline/cache 性能进入[计算机体系结构](../computer-architecture/index.md)，property/coverage 进入数字验证，CDC、板级接口或 constraint 进入 FPGA/SoC implementation。下一分支继续沿用同一条 instruction 和测试，不另换一个演示。
