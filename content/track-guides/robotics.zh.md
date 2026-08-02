## 6.4210 与 6.832 分别围绕 manipulation 和 underactuation

[MIT 6.4210](074-6-4210.md)的[官方 OCW 页面](https://ocw.mit.edu/courses/6-4210-robotic-manipulation-fall-2022/)用 Drake 把 geometry、kinematics、planning、perception 与 grasping 接到 10 份 problem set 和 final project，适合 desktop manipulation。课程任务会让同一个 object 在 frame、collision geometry、grasp candidate、planner 与 controller 之间移动，项目也自然要求这些接口互相一致。[MIT 6.832](075-6-832.md)的[官方 OCW 页面](https://ocw.mit.edu/courses/6-832-underactuated-robotics-spring-2022/)关注 dynamics、optimization 与 controller 怎样利用 natural dynamics，适合 swing-up、legged system 和 underactuated mechanism。两门各自完整，不能因课程号相近就排成前后学期；pick-and-place 选前者，energy shaping 或 dynamic motion 选后者。

6.4210 的问题集适合按 object pose、grasp feasibility、collision-free path 与 execution 分阶段组织，final project 再把这些结果接成 manipulation pipeline。6.832 则以 equation of motion、trajectory optimization、stability argument 和 simulation trace 为主，摆起或步态的成功依赖 dynamics。前者常见瓶颈在 geometry/perception interface，后者常见瓶颈在 model/controller interface；选课时应看自己愿意分析哪种接口。

## Modern Robotics 是唯一严格递进的六门序列

[Course 1](077-modern-robotics-1.md)与[Course 2](078-modern-robotics-2.md)建立 configuration、rigid motion、kinematics 与 Jacobian，[Course 3](079-modern-robotics-3.md)进入 dynamics，[Course 4](080-modern-robotics-4.md)处理 planning/control，[Course 5](081-modern-robotics-5.md)合并 manipulation 与 mobile robot；[Course 6](082-modern-robotics-6.md)的 mobile-manipulation capstone 假定前五门完成。[Coursera 第一门官方页](https://www.coursera.org/learn/modernrobotics-course1)可以核对当前平台入口；教材、[官方 wiki](https://hades.mech.northwestern.edu/index.php/Modern_Robotics)与[官方代码库](https://github.com/NxRLab/ModernRobotics)公开，graded/peer work、trial 和 price 则可能变化。

这条路线适合希望一套 notation 从 SE(3) 贯穿到 youBot capstone 的人，不必再把 6.4210 或 6.832 全部叠加。[MASLab](061-6-186.md)只作为 2005 年 whole-robot competition 的方法参考，旧 OrcPad、Java/CVS、kit 与赛场不再构成可复刻课程环境。

六门的依赖可以用同一个 library example 检查：Course 1/2 产出 frame 与 kinematic model，Course 3 为同一结构增加 inertia 与 force，Course 4 提供 path/controller，Course 5 增加 manipulation/mobile subsystem，Course 6 才把它们放到完整任务。若 capstone 中某个 Jacobian 或 odometry 接口解释不清，应回到产生该对象的课程，而非从 Course 6 的 scene 反向猜定义。

## frame、Jacobian、dynamics 和 collision 各有独立数值检查

[控制系统](../control-systems/index.md)中的 state、stability、feedback 与 actuator limit，[物理](../physics/index.md)中的 rigid body、energy、friction 与 contact，以及[编程工具](../programming-tools/index.md)中的 linear algebra、unit test、profiling 与 replay，在机器人里落实为可执行检查。为 2R arm 实现 forward kinematics 与 Jacobian，明确 space/body frame、unit 和 joint order，用 finite difference 检查至少一列，并验证 twist/wrench transform 的 power pairing。identity transform、zero motion、small step 和 known singular configuration 都应有确定结果。

再为 pendulum 写 mass matrix、gravity term 与 feedback simulation，用 energy change 与 limiting pose 检查符号。collision checker 用已知相交/分离 geometry 校准，random planner 固定 seed。frame 不能靠动画猜，Jacobian sign 不能只靠 library 输出，planning success 也不能脱离 collision tolerance；增加 robot description 的复杂度不会消除这些基础错误。

数值检查之间还要保持坐标约定一致。forward kinematics 输出的 end-effector pose、collision geometry 的 transform、controller 读取的 state 与 log 中的 joint order 必须来自同一模型。可挑一个非零姿态，把 position、velocity、kinetic energy 和 actuator effort 分别手算或用第二实现核对。若某项只有动画能说明，就缺少可自动回归的量。

## 活教材、付费作业与旧平台必须分别注明版本

6.4210 的 Fall 2022 prompt、Drake/pydrake note 和 repository 会继续演化，复做时注明 prompt year、commit、Python 与 solver；部分 graded assignment 和 feedback 未开放。6.832 当前 notes、Drake example 与 Colab 很强，同样没有完整作业反馈。Modern Robotics 公开书、wiki 与 library，Coursera 的 grader/peer review 属于平台注册层；旧说明中的 V-REP 是 CoppeliaSim 的旧名称，scene、CSV 与 library version 应一起说明。

现代 simulator 或 robot 可以重做 MASLab 的工程问题，却不能被称为原平台。simulation success 也不证明真实 collision geometry、friction、latency 与 actuator saturation。实体机器人需要 emergency stop、speed/current limit、隔离 collision area、现场 supervision 与 battery procedure；条件不足时项目停在 simulation。

版本说明应覆盖 robot description、mesh、physics engine、time step、solver、controller frequency 与 random seed。模型文件和可视化 mesh 也要区分，后者过于粗糙或坐标原点不同会污染碰撞结论。更换 Drake、CoppeliaSim 或 library release 后，先运行固定的 kinematics、collision 和 dynamics small case，再判断高层任务的变化来自算法还是环境升级。

## 最有价值的接口案例是 planner 成功而 controller 执行不成

选择 desktop pick-and-place、underactuated swing-up、mobile navigation 或 youBot mobile manipulation，开头声明 robot model、environment、frame、joint/actuator limit、planner-controller interface 与 success metric。为 kinematics、dynamics、collision、planner、controller 和 state update 分别写 deterministic test，再运行多个 initial condition、obstacle 或 parameter perturbation，报告 success rate、tracking error、minimum clearance、control effort 与 runtime，并注明 seed 与 raw log。

重点分析一条 collision-free plan 为何在 tracking 中因 saturation、contact 或 model mismatch 不能完成：定位到具体 waypoint、state 或 interface，修改后加入 replay regression。项目应包含 model、source、scene、environment version、log、replay command 与 safety limit。替换 initial condition 或 obstacle 后，脚本应自动指出问题落在 kinematics、collision、planning 还是 control；video 只作为时间索引，不能承担诊断。

planner-controller handoff 应显式给 trajectory timestamp、state convention、interpolation 和 actuator bound。若 planner 只输出 geometric waypoint，controller 仍需决定速度与加速度；这一步可能让原本无碰的路径在动态执行时越过限制。报告把 planned clearance 与 executed clearance、commanded effort 与 saturated effort 并排画出，接口问题便能从“机器人没抓到”缩小为可重放的时间区间。
