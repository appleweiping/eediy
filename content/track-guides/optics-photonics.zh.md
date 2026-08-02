## 2.71 与 NPTEL 分别用推导和演示建立经典光学

[MIT 2.71](134-2-71.md)以 10 组讲义、6 份 problem set 与多套考试建立 geometrical optics、wave optics、diffraction 和 imaging；Problem Set 1–4 有解、5–6 无解，也没有完整 video 或 physical-lab sequence。[NPTEL Introduction to Photonics](132-108106135.md)用 34 个主题、4 个 tutorial 与 10 个实验演示提供更连续的视频路线，覆盖器件现象更广，却没有公开作业答案。偏好由方程和考试题搭骨架可选 2.71；希望从现象、器件与演示进入可选 NPTEL。两门不必从头重复：2.71 学习者挑器件演示，NPTEL 学习者补几道 diffraction 与 imaging 推导即可。两条路径最后都应完成一份有尺度、有坐标系的 ray diagram 和一份可核归一化的 diffraction calculation，避免只熟悉其中一种语言。

经典底座最终要能处理 aperture、Fourier plane、sampling 与 waveguide boundary。对 slab waveguide，由 boundary condition 推出 mode equation，预测 mode count、cutoff、effective index 与 confinement 随 geometry 的变化；solver 只用于数值对照，并以 power integral 检查 normalization。做 imaging 时则从 aperture 与 detector sampling 预测 resolution 和 aliasing，而不是只调出清晰图片。

## ECE 5330 的核心是载流子怎样变成光功率

[Cornell ECE 5330](131-ece-5330.md)沿 semiconductor optoelectronics 进入 LED、laser、detector 与 modulator。[官方 OCW 页面](https://ocw.ece.cornell.edu/courses/ece-5330-semiconductor-optoelectronics/)公开讲义和部分作业反馈，是可以持续自学的第一条器件分支。这里会使用[电磁场](../electromagnetics/index.md)的 mode、polarization 与 Poynting flow，也会使用[半导体器件](../semiconductor-devices/index.md)的 band、carrier statistics、junction、recombination 与 noise。density of states、occupation、spontaneous/stimulated emission 和 recombination 要分别说明，它们随后进入 responsivity、gain、threshold 或 modulation bandwidth。

课程后段作业依赖未公开的 `ece533solver`。MEEP、MPB、Python/Jupyter、gdsfactory 或 ParaView 可以实现开放的等价模型，但应称为独立实现，并写明 mesh、boundary、dispersion、normalization、solver version 与 convergence。开源软件补上计算能力，并未补回课程私有工具和评分反馈。做 LED 或 detector 题时，可把 carrier rate equation、optical power 与 terminal current 放到同一张量纲表；做 laser 题时，再加入 threshold gain、cavity loss 与 confinement factor。这样能看出作业中的材料参数究竟改变了哪一个可测输出。

## ECE 5310 是独立的研究生量子分支

[Cornell ECE 5310](130-ece-5310.md)的[官方课程归档](https://ocw.ece.cornell.edu/courses/ece-5310-quantum-optics-for-photonics/)沿 density matrix、operator 与 open system 进入 quantum optics，含讲义、作业和部分考试反馈；没有视频，final 也没有解答。它不是普通光学的必修终点。选择之前，[物理基础](../physics/index.md)中的 quantum mechanics、basis change、operator、density matrix 与 simple time evolution 应能独立使用；classical interference formula 不能替代 quantum-state evolution。

当问题真正涉及 photon statistics、coherence、open-system dynamics 或 measurement back-action，ECE 5310 才比继续加深 classical field model 更合适。若对象仍是 waveguide cutoff、detector responsivity 或 laser threshold，应停留在相应经典或 semiconductor branch，把模型做深。可用 two-level system 的 population 与 coherence 演化作入口：同一组初态分别用 matrix equation 和数值积分求解，再检查 trace、positivity 与长时间极限。

## Phot1x 是逐期购买的完整工程链，不是常驻公开主线

[UBC Phot1x](133-phot1x.md)只能按高成本、逐期开售的 catalogue 评估。当前[官方 edX 页面](https://www.edx.org/learn/engineering/university-of-british-columbia-silicon-photonics-design-fabrication-and-data-ana)要求在报名当期重查 price、cohort、region、fabrication window，以及 PDK、solver、layout 和 measurement data 的真实可见范围；匿名页没有可下载的上述文件，也不能承诺导出或长期访问。官方 FAQ 说明课程 cohort 共用一次 fabrication，由 UBC 完成 measurement 并向参与者提供数据；默认不会邮寄实体 chip。个人若另购自己的 chip，才可能增加 fabrication、shipping 与 tax。只有 live run、预算、地区和账户内材料都满足时，才把它当 paid cohort；旧 syllabus 与外围工具生态不能被包装成当前 Phot1x 课程包。

[MIT 3.46](135-3-46.md)只在 material selection 已经限制 device performance 时加入，其 paid text 与无解 design problem 也构成访问边界。laser、fiber end、biased detector 与 invisible source 需要合规 laboratory、enclosure、interlock 和训练；lecture demonstration 不构成家庭 bench experiment。默认项目停在 simulation，除非真实设施、仪器和程序都已具备。

## 一个器件必须同时通过 mode、material 与 measurement budget

选择 waveguide、ring resonator、photodetector、LED/laser 或 simple imaging system，明确 wavelength、material、geometry、port、loss、bandwidth、noise 与 fabrication tolerance。核心结果至少由两种独立方法交叉，例如 analytic slab mode 对 mode solver、transfer matrix 对 frequency-domain simulation，或 responsivity/noise 手算对 datasheet。扫描关键尺寸、refractive index、loss 或 temperature，给出 convergence 与第一个规格边界。

把 source power、coupling loss、connector loss、polarization mismatch、detector floor/bandwidth、averaging time 与 expected observable 放进同一 measurement budget，才能判断“看不见信号”来自器件还是测量链。没有 fabrication 和 instrument data 时，结论只说明模型在给定假设下满足规格；field plot 不能替代 energy conservation、mesh convergence 与 tolerance analysis。最终结果以参数表、convergence plot 和第一次触及规格的 tolerance corner 收束，使读者能区分设计余量来自器件物理、测量预算还是网格设置。
