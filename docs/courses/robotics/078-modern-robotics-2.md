---
title: "Modern Robotics, Course 2: Robot Kinematics"
description: "Northwestern University 的《Modern Robotics, Course 2: Robot Kinematics》用视频、讲义、练习、仿真和代码训练机器人运动学；平台高度建议按系列顺序学习，因为本课会使用 Course 1 的语言，完整访问也可能收费。"
page_type: course
course_id: "course-078"
editorial_status: "researched"
evidence_level: "R0"
reviewed_at: "2026-07-30"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 63591aa5124dcf7a -->

# Northwestern University Modern Robotics 2: Modern Robotics, Course 2: Robot Kinematics

## 课程简介

- **所属大学：** Northwestern University
- **课程编号：** Modern Robotics 2
- **官方先修：** Coursera 的 specialization 页面只说高度建议 Courses 1–6 按顺序学习，因为内容前后累积
- **本站建议背景：** 建议先掌握 Course 1 的 SE(3)、twist、adjoint 与矩阵指数/对数；课程系列可按顺序学习，但这不是平台声明的硬性先修
- **访问条件：** 公开入口；部分材料需注册或受限
- **资料状态：** 2026-07-30；公开材料导读

### 2R 手算基准把刚体语言接到机械臂

Coursera [Robot Kinematics](https://www.coursera.org/learn/modernrobotics-course2) 对应 *Modern Robotics* Chapters 4–7：forward kinematics、velocity kinematics/statics、inverse kinematics 与 closed chains。[教材主页](https://hades.mech.northwestern.edu/index.php/Modern_Robotics) 提供统一 preprint 与勘误。它适合已经掌握 Course 1 刚体运动语言的人；SE(3)、twist、adjoint 和 exp/log 若仍靠试转置，应回 Chapter 3 重新推导。

一台 2R planar arm 足以检查所需基础：手算 home configuration、space/body screw axes、FK、Jacobian 和 singular pose，再用 finite difference 检查 \(J\dot\theta\)。

### POE、Jacobian 与 IK 共用同一台 2R arm

Chapter 4 用 product of exponentials 写 space/body FK，两式在一致的 home pose 与 screw definition 下应给相同 \(T\)。Chapter 5 推导 Jacobian、wrench/torque、singularity 与 manipulability；非方 Jacobian 检查 rank/singular value，混合角速度与线速度时注明 scaling。

Chapter 6 的 numerical IK 要记录 initial guess、frame convention、angular/linear tolerance、iteration count 与 termination。测试 reachable、unreachable、near-singular、workspace boundary 和 multiple-solution targets。Chapter 7 则写 loop-closure constraint、passive coordinates 和 constraint Jacobian，用数值扰动验证允许方向的一阶残差。

IK 的测试表还要分开“收敛到不同合法解”和“算法失败”。对多组固定 initial guess 保存最终关节角、末端旋转/平移误差、最小 singular value 与停止原因；接近奇异点时观察 step 是否突然放大。若需要加入 damping 或 step limit，把原始失败与修改后的结果并列，不能只留下最后一个成功姿态。

### 官方函数的输入输出要能逐项解释

[ModernRobotics repository](https://github.com/NxRLab/ModernRobotics) 提供
`FKinSpace(M,Slist,thetalist) → T`、`JacobianSpace(Slist,thetalist) → J_s` 与
`IKinSpace(Slist,M,T,thetalist0,eomg,ev) → (thetalist, success)`；按
[library setup](https://hades.mech.northwestern.edu/index.php/Getting_Started_with_the_Modern_Robotics_Code_Library)
锁定语言、commit 和依赖。每类函数用 2R 手算、library output 与 small-\(\Delta t\) finite
difference 互查。差异出现时检查 axis、frame 与指数次序，不能只放宽 tolerance。

[官方 Course 2 assignments 与 resources](https://hades.mech.northwestern.edu/index.php/Coursera_Resources) 是 coursework 与版本入口。UR5 model 的 home pose、screw axes、joint order 和单位作为受版本控制的数据；固定随机关节角上的 space/body FK 一致后，再运行 IK。

模型加载后检查每个 rotation block、矩阵尺寸与 \(q=0\) 位姿。随机回归既覆盖一般姿态，也单列完全伸展、折叠和接近 joint boundary 的情况；对 Jacobian 每一列施加微小关节扰动，从末端 transform 的增量重建 twist。这个检查能抓住 axis direction、joint ordering 与 adjoint direction 的错误，即便动画看起来仍像机械臂运动。

### UR5 CSV 是数值结果的导出边界

[CoppeliaSim setup](https://hades.mech.northwestern.edu/index.php/Getting_Started_with_the_CoppeliaSim_Simulator) 提供 UR5 CSV scene。每个 waypoint 输出前计算 FK error、minimum singular value 与 joint jump，动画通过仍不代表满足真实 joint limit、collision、calibration 或 controller safety。

生成 trajectory 时，每个 waypoint 都独立求解并验证，相邻 IK 解的连接方式由这些结果决定。简单插值可能跨过 joint limit、碰撞区或 discontinuous branch；因此同时输出关节增量与末端误差，并把被拒绝 waypoint 留在 failure table。scene 只读取已验证的 CSV，不在可视化阶段静默修正数值。

课程记录分成 2R oracle、random regression、IK boundary matrix、closed-chain check 与 scene export 五个可独立命令，并记录 errata、library commit、scene 与 tolerance。没有实体 UR5 也能完成数值目标；simulator precision 不能换算成硬件 accuracy。

选一条成功目标和一条不可达目标，从 screw-axis 数据一路追到 FK、Jacobian、IK iteration 与
CSV 输出。用同一命令再算两条路径，并在返回值旁直接写 reachability、conditioning 或
iteration budget；一个含糊的 `False` 没有说明 IK 为什么停下。

## 课程资源

- [课程主页](https://www.coursera.org/learn/modernrobotics-course2)
- [代码 · Modern Robotics official software library](https://github.com/NxRLab/ModernRobotics)

## 资源汇总

本次核对的公开入口已全部列在上方；若你有完成记录、补充材料或失效链接，可通过页末反馈与纠错入口提交依据。
