---
title: "Modern Robotics, Course 1: Foundations of Robot Motion"
description: "Northwestern University 的《Modern Robotics, Course 1: Foundations of Robot Motion》以开放预印本、软件库和 CoppeliaSim 练习建立机器人运动基础；自学材料强，但平台免费体验不完整。"
page_type: course
course_id: "course-077"
editorial_status: "researched"
evidence_level: "R0"
reviewed_at: "2026-07-31"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 26056af865fefd32 -->

# Northwestern University Modern Robotics 1: Modern Robotics, Course 1: Foundations of Robot Motion

## 课程简介

- **所属大学：** Northwestern University
- **课程编号：** Modern Robotics 1
- **官方先修：** Modern Robotics Course 1 假定熟悉叉积、特征值、矩阵求逆、正定性、受力图，并能使用一种矩阵计算语言
- **本站建议背景：** 本站未另设准备条件
- **访问条件：** 公开入口；部分材料需注册或受限
- **资料状态：** 2026-07-31；公开材料导读

### Chapter 2–3 先固定自由度与刚体变换

Coursera [Foundations of Robot Motion](https://www.coursera.org/learn/modernrobotics-course1) 是 6 门 specialization 的入口，适合愿意把机器人学坐标约定学扎实的人。它只覆盖 *Modern Robotics* Chapter 2 Configuration Space 与 Chapter 3 Rigid-Body Motions，却奠定后续所有 frame、twist 和 wrench 约定。[教材主页](https://hades.mech.northwestern.edu/index.php/Modern_Robotics) 提供 December 2019 updated first-edition preprint；它与 2019 年第 3 次印刷内容一致、页码排版不同。截至 2026-07-31，平台页列出 5 个模块、21 项作业（assignments），并估计 2 周、每周 10 小时；线代薄弱者通常需要更多时间。

这门课默认学习者熟悉 cross product、eigenvalue、matrix inverse、positive definiteness、free-body diagram，并会使用一种矩阵语言。这些工具尚不熟时，补强线代能节省大量排查 frame 错误的时间。

### Human-arm DOF 讨论先把 configuration 说清

[官方 Course 1 resources](https://hades.mech.northwestern.edu/index.php/Coursera_Resources)
在六门课中只为 Course 1 单列 human-arm degrees-of-freedom discussion prompt。它的输入是
关节、刚体、接触与独立约束的建模选择，输出应是一套能解释 configuration、C-space、task
space 与 workspace 的自由度计算，而不是按 motor 数量猜答案。Chapter 2 再把 Grübler
formula、topology、holonomic/nonholonomic constraint 和 Pfaffian form 接到平面闭链、空间
刚体与轮式底盘。

Chapter 3 引入 SO(3)/so(3)、SE(3)/se(3)、rotation/transform、angular velocity、twist、screw axis、exp/log、adjoint 与 wrench。在 space/body frame 之间切换 pose、twist 和 wrench 时，坐标约定必须一致；power \(F^TV\) 则提供一个很漂亮的不变量检查。

这一章最值得单独留一页 convention sheet，列清 \(R_{sb}\)、\(T_{sb}\)、space/body twist 与 wrench 的下标、作用方向和乘法顺序。结果相反时，单位轴与纯平移反例通常能迅速定位 active/passive、left/right multiplication 或 frame label；后续运动学、动力学和控制都会反复复用这些约定。

### `MatrixExp6` 与 `MatrixLog6` 把约定变成可测接口

[ModernRobotics repository](https://github.com/NxRLab/ModernRobotics) 提供 Python、MATLAB、
Mathematica 教学实现，并明确以可读性而非 production robustness 为目标。
[Library guide](https://hades.mech.northwestern.edu/index.php/Getting_Started_with_the_Modern_Robotics_Code_Library)
可以带你跑通 `MatrixExp6`。把 `VecTose3(Sθ)` 的 \(4\times4\) se(3) matrix 作为输入，
`MatrixExp6` 输出 \(T\in SE(3)\)；`MatrixLog6(T)` 再返回 se(3)。round trip 应比较最终
transform，同时检查 rotation orthogonality、determinant、inverse 与纯平移/纯旋转边界。

库函数最适合和手算小例对照。对 SO(3)/SE(3)，orthogonality、determinant、inverse 与 exp/log round trip 能抓住大多数 convention error；轴角表示不唯一时，应比较最终 transform，而非逐元素硬比。

[CoppeliaSim setup](https://hades.mech.northwestern.edu/index.php/Getting_Started_with_the_CoppeliaSim_Simulator) 提供 UR5 与 youBot 的 CSV scenes。前 3 个 pose 用来核对 frame、平移单位、旋转方向和列顺序，随后尝试纯旋转、纯平移与 screw motion。模拟器能显示运动，却无法替矩阵约定作证。

Coursera graded test 与 peer assignment 的访问可能付费，公开 preprint、代码与 simulator setup 则足够重建 Chapter 2–3 的核心例子。这门短课的核心价值是从开头钉牢整套机器人学符号，动画只承担末端显示。

## 课程资源

- [课程主页](https://www.coursera.org/learn/modernrobotics-course1)
- [代码 · Modern Robotics official software library](https://github.com/NxRLab/ModernRobotics)
- [代码 · Modern Robotics 代码库入门指南](https://hades.mech.northwestern.edu/index.php/Getting_Started_with_the_Modern_Robotics_Code_Library)
- [其他 · Modern Robotics 六门课程共享资源索引](https://hades.mech.northwestern.edu/index.php/Coursera_Resources)
- [仿真器 · Modern Robotics CoppeliaSim 入门指南](https://hades.mech.northwestern.edu/index.php/Getting_Started_with_the_CoppeliaSim_Simulator)

## 资源汇总

<details markdown="1">
<summary>展开更多官方资源（1 项）</summary>

**资源**

| 资源 | 访问 | 状态 | 复核日期 |
|---|---|---|---|
| [《Modern Robotics》教材主页与公开预印本入口](https://hades.mech.northwestern.edu/index.php/Modern_Robotics) | 无需注册公开访问 | 官方页已列出 | 2026-07-31 |

> 其余条目保留访问状态与复核日期；材料权利归原提供方，实际可用性可能随账号、地区或课程改版变化。

</details>
