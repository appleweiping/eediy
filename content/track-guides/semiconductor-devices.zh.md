## Cornell 提供材料全景，6.701 提供 state-to-current 叙事

[Cornell ECE 4070](124-ece-4070.md)的[官方课程页](https://ocw.ece.cornell.edu/courses/ece-4070-course-details)用 32 份 handout 从自由电子、晶格与能带推进到统计、phonon、transport、heterojunction、低维结构、optics 与 thermoelectrics；11 份带解作业和大部分带解考试，使纸笔反馈相当完整。课程没有录像，适合愿意沿讲义推导并需要宽 solid-state 视野的人。[MIT 6.701](125-6-701.md)的[官方 OCW 归档](https://ocw.mit.edu/courses/6-701-introduction-to-nanoelectronics-spring-2010/)从 particle in a box、molecule 与 nanostructure 进入 band、Landauer transport 和 ballistic MOSFET，开放教材形成连续的 quantum-state-to-current 路线；12 次作业、3 份考试和 2 项 MATLAB 题没有完整官方答案或可运行源码。材料跨度选 Cornell，量子输运过渡选 6.701，再从另一门抽取 phonon 或 transport 章节即可。

两门可以共享一张概念索引，但题目链不混用：Cornell 的 solved work 适合核查 band、statistics 与 scattering 推导，6.701 的开放教材则让同一个 state-count argument 延伸到 terminal current。引用解答时注明课程来源，避免把 Cornell 的反馈误写成 6.701 MATLAB 任务的官方答案。

## DOS、occupation 与 transmission 分别控制态数、载流子和电流

[物理](../physics/index.md)中的 wavefunction、eigenvalue、lattice 与 thermal statistics，[工程数学](../mathematics/index.md)中的 linear algebra、differential equation 与 Fourier representation，以及[电路分析](../circuits/index.md)中的 terminal voltage、charge、current 与 small-signal quantity，在这一页承担不同角色。6.701 正式先修为 6.007 或 6.003，因此还应从[EE 导论](../ee-introduction/index.md)或[信号与系统](../signals-systems/index.md)具备 field、energy 或 system representation。

从归一化的一维无限深势阱开始，推导 1D/2D/3D density of states 随能量的形式，并由 \(E(k)\) 曲率解释 effective mass。DOS 与 Fermi occupation 相乘才得到 carrier density；current 还需要 contact chemical potential、scattering 或 transmission。每一步写明单位、degeneracy、temperature 和 boundary。三条曲线即使外观相似，也不能把 available-state density、occupied population 和 conductance 互换。

可把同一 parabolic band 放在三张纵轴不同的图上：每单位能量的 state 数、积分后的 carrier concentration、以及给定 contact/transmission 下的 current。温度或 chemical potential 改变时，DOS 本身、occupation window 与 terminal current 的变化来源分别标注。这样既能检查单位，也能看出某个参数究竟作用在 band structure、statistics 还是 transport。

## 一维链的数值实现先核 state count，再接 Landauer current

建立 finite-difference quantum well 或 nearest-neighbor tight-binding chain。在 closed boundary 下求 eigenvalue/eigenvector，用解析无限深势阱或已知 dispersion 检查 energy、normalization 与 orthogonality；构造 DOS 后，以 energy integral 核对 state-count sum。继续到 transport 时接两个 contact，计算 transmission 与 Landauer current，并检查 zero-bias net current 以及交换左右 contact 后的 symmetry。

至少比较三组 grid spacing 或 chain length，再改变 well width、temperature 或 chemical potential，运行前由 band 与 occupation 预测方向。原始 eigenvalue、wavefunction、DOS、transmission 和 current array 应能重建图表。boundary 太近、energy grid 太粗或 contact coupling 设置错误时，指出 state count、convergence 或 current conservation 中哪一项先被破坏；最终 I-V 必须能逐层追回 Hamiltonian、boundary、DOS 与 occupation。

energy grid 的检查不能只看曲线平滑，还要比较 integrated DOS 和 current integral 的变化；spatial grid 则比较低阶 eigenvalue 与 wavefunction node。接入 contact 后，谱峰展宽、transmission peak 与 current window 应在同一能量轴对齐。若左右 chemical potential 相等，正反传播贡献必须抵消；交换 contact 后的对称关系可暴露 sign convention 或 self-energy 接法问题。

## MATLAB 题面停在模型层，cleanroom 更不属于校外延伸

ECE 4070 的公开强项是 handout—assignment—exam，没有 video、lab 或 code；6.701 描述 MATLAB simulation 任务，却没有官方可运行实现。自写 solver 要给 spatial grid、Hamiltonian discretization、boundary condition、contact/self-energy model、broadening 与 convergence tolerance，并将个人实现与课程材料清楚分开。历史课程中的 process scale、material parameter 与 device case 也不能直接写成当前产业节点数据。

公开访问不授权 cleanroom processing、chemical etch、implant、vacuum、高场 breakdown 或 nanofabrication。这些活动涉及化学品、辐射、高压和机构设施。缺少 device sample、probe station、calibration 与 raw I-V/C-V 时，曲线只能称数值模型结果。好的半导体项目并不需要假装制造过器件；它需要让态数、电流守恒、数值收敛与可核的课程材料彼此一致。

报告标题和图注应使用 model、simulation 或 public-data comparison 等准确措辞，并注明参数来自课程例题、文献还是自定扫描。这样读者可以复算数值结论，也能清楚看见 fabrication、contact resistance 与 measurement uncertainty 仍在项目范围之外。
