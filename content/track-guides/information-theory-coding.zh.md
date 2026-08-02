## EE 276 与 6.441 是两种不同密度的证明档案

[Stanford EE 276](102-ee-276.md)适合承担第一次完整学习。课程的[官方页面](https://web.stanford.edu/class/ee276/)把 entropy、typical set、source coding、channel capacity、rate-distortion 和多用户入口串在一起；公开归档里可核到旧版 18 讲 notes、当前 8 份带解作业与 2 场考试，但当前学期只核到 1 份公开 slide。使用时应按材料年份阅读，不能把旧讲义逐讲改称现行课堂。[MIT 6.441](103-6-441.md)的[官方 OCW 归档](https://ocw.mit.edu/courses/6-441-information-theory-spring-2010/)有 23 讲更密的材料与 9 份题，证明和 multiuser channel 更深入，却没有公开解答。多数学习者可以用 EE 276 的题目—解答—考试链建立基础，遇到 converse、rate region 或 multiuser 问题时，再读 6.441 对应章节。若目标其实是同步、检测、波形或 modem 实现，应先完成[通信系统](../communications/index.md)；信息论讨论可达极限，并不替代物理链路。

## 一道题要同时经得起定义、证明和边界分布

这里的先修，是能用[概率与统计](../probability-statistics/index.md)的语言逐步论证；一张结业单本身无法提供这种能力。对一个联合分布，计算 entropy、conditional entropy 与 mutual information，逐行标出条件信息、logarithm base 及 bit/nat 单位；再用 Markov chain 写出 data-processing inequality 的适用方向。处理 BSC 或 BEC 时，把 input distribution、block length、error criterion、achievability 与 converse 的量词写全，并用均匀分布、退化分布和零/一 crossover probability 检查边界。把 capacity 当成设备铭牌上的恒定 bit rate，会把 channel alphabet、input cost 与 decoding error 的定义问题误判为代数问题。

EE 276 的带解作业适合这样使用：闭卷写出第一稿，只定位解答中最早分歧的一步，随后重新推导整题；两场考试则按公开时限完成，区分定义遗漏、证明技巧和时间分配。6.441 的 9 份题没有官方答案，核对只能依赖定义、第二种推导、极端分布或逐步同伴讨论。两门课都没有编程 lab，数值代码可以检验直觉，却不能被写成课程作业或校内成绩。这个方向最重要的阅读习惯，是对每一个等号追问独立性、凸性、极限交换或典型性条件究竟在哪里使用。

## 一个短码长实验把渐近定理拉回有限数据

选 BSC、BEC 或简单 input-constrained channel，先完整写出一个 source-coding 论证、一个 channel-coding bound 和一个 data-processing 推论，统一随机变量、分布、block length、极限次序与错误定义。随后实现可重复的 finite-block experiment：在至少三组 block length 与三组 channel parameter 下，比较经验错误率、有限长 bound 和 asymptotic capacity；随机试验给出次数与置信区间，代码还应包含可手算的小规模枚举。短码长偏离渐近预测正是实验的核心现象，应完整保留并解释。

输入约束改变后，mutual information 的数值不能脱离优化分布直接横比；经验曲线接近 capacity 也不能证明某个 decoder 最优。结尾选出偏离渐近预测最大的一组 block length/channel parameter，逐项核对 decoder、有限长 bound、置信区间与输入约束，并明确偏差由哪一个未满足的假设解释。这样定理允许的结论、程序估计的量和仍未覆盖的有限长行为会落在同一张图上。
