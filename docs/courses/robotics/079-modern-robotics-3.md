---
title: "Modern Robotics, Course 3: Robot Dynamics"
description: "Northwestern University 的《Modern Robotics, Course 3: Robot Dynamics》把系列推进到机器人动力学；视频、讲义、练习、仿真和代码齐全，平台高度建议先按顺序掌握前面的刚体运动与运动学，完整访问可能收费。"
page_type: course
course_id: "course-079"
editorial_status: "researched"
evidence_level: "R0"
reviewed_at: "2026-07-30"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 8d4a151e719bea96 -->

# Northwestern University Modern Robotics 3: Modern Robotics, Course 3: Robot Dynamics

## 课程简介

- **所属大学：** Northwestern University
- **课程编号：** Modern Robotics 3
- **官方先修：** Coursera 的 specialization 页面只说高度建议 Courses 1–6 按顺序学习，因为内容前后累积
- **本站建议背景：** 建议先完成 Course 1–2 或具备同等的刚体运动与运动学基础；这是本站按内容给出的学习顺序
- **访问条件：** 公开入口；部分材料需注册或受限
- **资料状态：** 2026-07-30；公开材料导读

### 课程定位

Coursera [Robot Dynamics](https://www.coursera.org/learn/modernrobotics-course3) 对应 *Modern Robotics* Chapters 8–9。4 个 module 约为 7、7、5、4 小时：前半推 Lagrange、mass matrix 与 Newton–Euler，继而做 forward/task-space/constrained dynamics、gearing、friction 和 1 个带同伴互评的 project；后半处理 point/via-point trajectory 与受 dynamics/actuator limit 约束的 time-optimal scaling。它适合已经能把 Course 2 的 kinematics 写成稳定代码、准备进入动力学与轨迹约束的人。

课程假定已完成 Course 1–2。一台 2R arm 可以检查所需基础：写 kinetic/potential energy，检查 mass matrix 对称正定，并从 \(q,\dot q,\tau\) 求一次 \(\ddot q\)。

### Dynamics 接口必须在同一模型上 round-trip

官方库的核心接口是
`InverseDynamics(q,dq,ddq,g,Ftip,Mlist,Glist,Slist) → tau` 与
`ForwardDynamics(q,dq,tau,g,Ftip,Mlist,Glist,Slist) → ddq`。同一模型先由前者求
\(\tau\)，再送入后者检查是否恢复 \(\ddot q\)。另测静止重力补偿、zero-gravity energy、
tip wrench、friction/gearing 符号。模型文件单列 mass、COM、inertia、link transform、
screw axis、gravity、joint order 和单位，并验证质量为正、惯量物理可行。

测试误差要随尺度解释：round-trip 同时报告 absolute 与 relative residual；在零速度时检查 Coriolis 项，在静态姿态把 gravity torque 与有限差分 potential gradient 对照；施加 tip wrench 时检查虚功关系。若改变 integration step 后能量漂移不收敛，优先怀疑符号、frame 或模型参数，而非归咎模拟器。

[ModernRobotics repository](https://github.com/NxRLab/ModernRobotics) 的实现强调教学可读性。为每个函数加 shape、finite-value、energy 与 round-trip assertion；单摆或 1-DOF inertia 手算提供基准，多连杆用于扩大覆盖。

### Chapter 9 的输出是 path 与 time scaling 两组数组

joint、screw 和 Cartesian trajectory 使用同一起终 pose 与 duration，分别画 \(q,\dot q,\ddot q,\tau\)。via-point 检查位置/速度连续；time scaling 明确 velocity、acceleration 和 torque limit 的来源。画面平滑无法证明 command 连续或满足 limit。

对三种 path 统一采样并保存原始 arrays，比较末端几何、关节峰值与所需 torque。受力矩约束的 time scaling 还要显示 path coordinate、允许 acceleration interval 和 switching points；某个离散点可行不能推出整段可行。若缩短 duration 触发 limit，就保留首次违反的位置及对应关节。

[教材主页](https://hades.mech.northwestern.edu/index.php/Modern_Robotics) 提供 preprint、errata 与 UR5 参数，[Coursera Resources](https://hades.mech.northwestern.edu/index.php/Coursera_Resources) 汇总 6 门资源。锁定书版本、MR commit 和语言，避免混入另一套 spatial-vector convention。

### CoppeliaSim 只重放已经检查过的 state sequence

[CoppeliaSim instructions](https://hades.mech.northwestern.edu/index.php/Getting_Started_with_the_CoppeliaSim_Simulator) 提供 dynamic scene 与 trajectory CSV。固定 scene/engine、integrator、step、initial state 和 seed；若 arm 数值发散，分别检查 model、step、joint order 与 scene physics。无重力无输入时，energy drift 随 step 缩小而下降，才支持离散化解释。

模拟器异常时，用纯数值程序重放同一 joint sequence。离线正确而 scene 错，检查列顺序、joint direction、physics mode 与 time step；两处都错，再查 dynamics 和 controller。每次运行保存 exact initial state、input、duration 与终止原因，让动画可以从数组重建。

课程记录包括 Chapters 8/9 习题、inverse/forward tests、dynamics project、3 类 trajectory、raw arrays、图与动画。Coursera peer/graded access 可能付费；公开代码和 scene 可复建。真实机器人还需重新辨识 friction、gearing、current 与 collision limits。

最有价值的是一张误差表：手算小系统、MR function、numerical integration 与 CoppeliaSim 各自偏差多少，哪一项随步长下降，哪一项来自参数或 convention。它把“能播放”提升为可检查的动力学实现。

## 课程资源

- [课程主页](https://www.coursera.org/learn/modernrobotics-course3)
- [代码 · Modern Robotics official software library](https://github.com/NxRLab/ModernRobotics)

## 资源汇总

本次核对的公开入口已全部列在上方；若你有完成记录、补充材料或失效链接，可通过页末反馈与纠错入口提交依据。
