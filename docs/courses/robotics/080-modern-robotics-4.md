---
title: "Modern Robotics, Course 4: Robot Motion Planning and Control"
description: "Northwestern University 的《Modern Robotics, Course 4: Robot Motion Planning and Control》聚焦机器人运动规划与控制；实践资源完整，平台高度建议按顺序学完前面的建模、运动学与动力学材料，完整访问可能收费。"
page_type: course
course_id: "course-080"
editorial_status: "researched"
evidence_level: "R0"
reviewed_at: "2026-07-30"
comments: true
---

<!-- generated-by: scripts/generate_course_pages.py; fingerprint: 691c69d967cdbf2a -->

# Northwestern University Modern Robotics 4: Modern Robotics, Course 4: Robot Motion Planning and Control

## 课程简介

- **所属大学：** Northwestern University
- **课程编号：** Modern Robotics 4
- **官方先修：** Coursera 的 specialization 页面只说高度建议 Courses 1–6 按顺序学习，因为内容前后累积
- **本站建议背景：** 建议先完成 Course 1–3 或具备同等的 SE(3)、运动学、动力学与轨迹基础；这是本站按内容给出的学习顺序
- **访问条件：** 公开入口；部分材料需注册或受限
- **资料状态：** 2026-07-30；公开材料导读

### A*、RRT/PRM 与 tracking 在 Course 4 才真正接起来

Coursera [Robot Motion Planning and Control](https://www.coursera.org/learn/modernrobotics-course4) 对应 *Modern Robotics* Chapters 10–11。规划从 C-space obstacle、A* 进入 RRT/PRM、potential field 与 optimization；控制从 error dynamics 进入 velocity、torque/force 和 hybrid motion-force control。它适合已经掌握前三门的 SE(3)、kinematics、dynamics 与 trajectory、想把 planner 接到 controller 的学习者。

接口要提前固定：planner 输出 path，trajectory generator 赋时间，controller 追踪 reference。三层各自可重放，才能定位“未到终点”来自哪里。

### 两个 planning project 各有明确契约

[A* project](https://hades.mech.northwestern.edu/index.php/A%2A_Graph_Search_Project) 读取 `nodes.csv`、`edges.csv`，输出 `path.csv` 和 scene 截图。小图上的 parent、cost-to-come、heuristic 与 tie 手算提供基准，测试再覆盖 start=goal、unreachable、duplicate edge 和 malformed input。输出同时包含 total cost、expanded nodes 与明确 failure state；heuristic 的 admissibility/consistency 需结合题设 cost 论证。

[Sampling-Based Planning](https://hades.mech.northwestern.edu/index.php/Sampling-Based_Planning) 在 \([-0.5,0.5]^2\) 圆障碍环境实现 RRT 或 PRM，并自写 segment-circle collision checker。固定 map、radius、step、goal bias、maximum iterations 与 seed，对 narrow passage、isolated region 和 grazing edge 报告 success rate、path length、node count 与 runtime。平滑后逐段重做 collision check。

A* 与 sampling planner 共用同一套输入解析、collision query 和 path validator。A* 的 heuristic 设为 0 时应退化为 Dijkstra；PRM 的 query stage 则复用已经验证的 A*。为每个失败明确区分 invalid map、start/goal collision、no path 与 timeout，空路径不能同时表达四种状态。随机 planner 对一组固定 seeds 汇总分布，不能挑最短的一次。

### Controller 从已知误差开始验证

Chapter 11 用可解析 error system 核对符号，然后进入 body/space error、feedforward、P/PI/PID、computed torque 与 force control。用相同 initial error/reference 比较 feedforward-only、low-gain feedback、disturbance 与 saturation，画 6D pose error、command peak、saturation time 和 steady-state offset。

控制实验还需固定 sampling interval 与 actuator limit。reference 突变、模型偏差和外部 wrench 分别测试，integral term 要显示 anti-windup 前后差异。若 tracking error 下降而 command 长期饱和，不能只看末端 pose 宣布成功；应检查 trajectory duration 是否超出系统带宽。

[教材主页](https://hades.mech.northwestern.edu/index.php/Modern_Robotics) 给章节与勘误，[MR repository](https://github.com/NxRLab/ModernRobotics) 提供教学实现。代码需自行处理 no-path、input validation、tolerance、speed/torque limit 和 anti-windup；提高 gain 不能修复 frame、reference discontinuity 或病态 Jacobian。

### 分开交付，再做集成

[Coursera Resources](https://hades.mech.northwestern.edu/index.php/Coursera_Resources) 把两项 project 归在 Course 4；[CoppeliaSim setup](https://hades.mech.northwestern.edu/index.php/Getting_Started_with_the_CoppeliaSim_Simulator) 提供 scene/CSV 边界。目录保留固定输入、原始输出、seed、README、截图/视频与 1 条重跑命令。

planner benchmark、无障碍环境中的 controller reference tracking 和集成失败 run 分别保留。结果应能区分 path discontinuity、时间尺度、IK conditioning 与 control bandwidth；模拟结果只证明算法实验，不提供实体 collision 或 motor safety 认证。

集成接口至少写 waypoint frame、timestamp、velocity continuity、clearance 和失败码。对 reference 做一次离线 validation，再让 controller 回放；若失败，从已保存的 path 与 control log 分别复现。最终报告并列 planning success distribution 与 tracking-error distribution，避免用一段最佳视频掩盖其中一层的不稳定。

## 课程资源

- [课程主页](https://www.coursera.org/learn/modernrobotics-course4)
- [代码 · Modern Robotics official software library](https://github.com/NxRLab/ModernRobotics)

## 资源汇总

本次核对的公开入口已全部列在上方；若你有完成记录、补充材料或失效链接，可通过页末反馈与纠错入口提交依据。
