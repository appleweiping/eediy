## Colorado 四门课先按官方考核链理解

[ECEA 5315 官方页面](https://www.colorado.edu/ecee/academics/online-programs/ms-ece-coursera/curriculum/computer-engineering-embedded-systems/ecea-5315-concept-and-practices)把 quizzes 记 10%、programming assignments 30%、peer reviews 30%、final 30%。因此 [Real-Time Embedded Systems 1](063-real-time-embedded-systems-1.md) 中的 thread、timing 和 deadline measurement 同时经由代码、互评和考试评估。[ECEA 5316 官方页面](https://www.colorado.edu/ecee/academics/online-programs/ms-ece-coursera/curriculum/computer-engineering-embedded-systems/ecea-5316-theory-and-analysis)与[ECEA 5317 官方页面](https://www.colorado.edu/ecee/academics/online-programs/ms-ece-coursera/curriculum/computer-engineering-embedded-systems/ecea-5317-mission-critical-sw)都把 quizzes 记 10%、programming 与 peer review 合计 60%、final 30%；前者对应 [Theory and Analysis](064-real-time-embedded-systems-2.md) 的 schedulability，后者对应 [Mission-Critical Systems Design](065-real-time-embedded-systems-3.md) 的 ECC、flash、redundancy 与 FMEA。官方页没有再拆开那 60%，这里也不自拟比例。

[ECEA 5318 官方页面](https://www.colorado.edu/ecee/academics/online-programs/ms-ece-coursera/curriculum/computer-engineering-embedded-systems/ecea-5318-real-time-embedded)指定 camera visual-synchronome [Project](066-real-time-embedded-systems-4.md)，不是自由选题 capstone：5 次 peer review 合计 50%，3 次 quiz 合计 15%，1 Hz/10 Hz programming 与 final 的两次 rate test 合计 35%。前两门构成实时专项；后两门只在 reliability 或指定 camera capstone 确实需要时加入。若目标是 task model 与 scheduling analysis，学到 5316 即可。platform assignment、grader、peer review、starter 与 hardware 的完整访问可能收费，匿名产品页不能替代注册后的 assessment chain。

这些比例也决定校外能够复习什么：programming 检查可运行实现，peer review 检查设计说明与同伴可读性，quiz/final 检查个人在限时条件下的分析。只下载 lecture 或复刻一段 thread code，覆盖不了原课的多种评测。学习日志应把“看过的公开材料”“自己完成的独立练习”和“平台注册后获得的评分”分栏，课程完成度才不会被混写。

## EECS 149 解释模型组合，Colorado 把时间约束做实

[Berkeley EECS 149](060-eecs-149.md)用开放教材连接 model of computation、embedded implementation、sensing/actuation、networking 与 feedback，适合理解“software timing 怎样改变 physical system”。录播、lab hardware 和 toolchain 有年代，校外学习更值得跟随教材中的 model relationship，而不是复刻旧平台。Colorado 5315/5316 随后把 thread、period、deadline、priority、blocking 与 schedulability 放进可评测的 programming 和 analysis；5317 再增加 reliability，5318 则固定到 camera rate pipeline。两套材料的交点是系统时间语义，角色并不相同。

[嵌入式系统](../embedded-systems/index.md)应已覆盖 C、interrupt、timer、concurrency、memory-mapped I/O 与硬件观测；[信号与系统](../signals-systems/index.md)则提供 discrete time、sampling、state、stability 和 feedback。实时专项不是“代码跑得快”，而是 release、response、deadline 与 physical sample age 之间存在可检查关系。

EECS 149 的模型组合还要求说明事件由谁产生、在哪个时间语义下消费，以及 software actor 与 physical plant 怎样交换状态。Colorado 的调度题则把这种语义压缩成可计算的 task set：periodic/sporadic release、priority、execution budget 和 shared-resource blocking 都进入 response-time reasoning。两边放在一起时，模型负责说明“时间为何重要”，调度分析负责回答“当前配置是否满足时间约束”。

## 周期任务从 absolute release time 与完整 timestamp 开始

建立两个不同 period 的 task，逐项定义 release、start、finish、deadline、priority、shared resource 与 overrun policy。使用 monotonic clock 和 absolute release time，避免 relative sleep 把 execution time 逐周期积成 drift。timestamp trace 应能定位一次 preemption、blocking、priority inversion 或 cache/page fault 对 response time 的影响。mean latency、99.9 percentile 与 maximum observed value 回答不同问题，普通 Linux 上的观测最大值更不等于 WCET proof。

纸面用 utilization、response-time analysis 或 schedule table 预测方向，再比较 idle 与 controlled-load 测量。日志若只有 finish time，没有 release 和 deadline，就分不清 late dispatch、execution overrun 与 missing sample。测试结果还要说明 observation duration、sample count、lost record 与 clock-synchronization error；“没有 miss”只有在负载范围和 instrumentation overhead 都明确时才有意义。

一条 trace 可以按 job identifier 连接 release、dispatch、preemption、resume 与 completion，再由 deadline 减 completion 得到 slack。shared resource 访问区间应在同一时间轴显示，priority inversion 才能从调度现象与锁持有者对应起来。若分析采用 WCET estimate，测量最大执行时间只能作为输入或质询，不能自动把 estimate 变成证明；两者的来源和适用机器配置需要并列说明。

## tracing 开销、kernel 配置和 actuator safety 必须同页出现

自建环境注明 kernel、architecture、compiler、scheduler policy、priority、CPU affinity、clock source、frequency scaling、background load 与 logging method。比较 tracing 开启/关闭时的 latency distribution，估算 observer intrusion。container 能稳定 user-space package，却复制不了 interrupt latency、driver 和 CPU power state；通用 Linux 的数据只代表一个配置和观测窗口，不能宣称 hard-real-time guarantee。

连接 actuator 前，在 plant simulation 或 low-energy hardware-in-the-loop 中测试 timeout、watchdog 与 safe state。实体系统需要 mechanical limit、speed/current bound、manual stop，以及 communication loss 后的 default action；课堂 FMEA 和 redundancy exercise 不构成 safety certification。实时分析与安全措施可以互相提供输入，但不能互相替代。

tracing 本身也要作为 workload 看待：buffer flush、console output 与 timestamp call 都可能延长 critical path。可分别采用内存缓冲和批量导出，观察 distribution 是否移动，并将差异写作 measurement perturbation。actuator 侧则把 stale sample、late command 和 command loss 分成不同状态；safe state 的触发条件、复位方式与物理限位应在控制逻辑之外另有说明。

## 非 CU 项目：制造一次 deadline miss 并追到 plant output

**以下 `sense → estimate/process → control → actuate` pipeline 是本站用于连接 scheduling 与 control 的练习，不是 5315–5318 的 official assignment，也不能替代 programming、peer review 或 final。** 为简化 plant 建 periodic pipeline，task table 给 period、deadline、priority、shared resource 与 WCET estimate；runtime data 同时包含 release/start/finish、latency/jitter、miss count、state estimate 与 control output。建立 controlled-load baseline 后，逐次注入 execution overrun、priority inversion、message delay 或 sensor dropout。

用时间线说明调度事件怎样传播到 sample age、estimation error、control saturation 或 plant state，并在修复后加入 replay test。若同时学习 Mission-Critical Systems Design，再分别写 severity、occurrence、detection 与 mitigation，避免用单一 risk score 隐藏假设。最后改变一个 task period 或 workload，先由分析预测 miss 与 control performance 的变化方向，再重跑。结果应包含 task model、analysis、timestamp trace、raw distribution、build command、fallback behavior 与定位过程；它是独立练习，不冒充 Colorado 指定 camera project。

项目判读以两条时间线对齐为中心：上半部分画 job release、blocking 与 completion，下半部分画 sample age、controller output 和 plant state。注入点与物理偏差出现的间隔可以区分 scheduling delay、estimator lag 与 plant inertia。修复也应对应明确机制，例如缩短 critical section、调整优先级或改变 sampling policy；只降低绘图频率而让 miss 消失，说明测量负担改变了，并未回答原来的系统问题。
