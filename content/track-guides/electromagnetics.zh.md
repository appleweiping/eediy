## ECE 3030 用大量解题校正边界，6.013 用系统联系组织方程

[Cornell ECE 3030](107-ece-3030.md)的[官方档案](https://ocw.ece.cornell.edu/courses/ece-3030-electromagnetic-fields-and-waves-2)由 36 组 handout、12 套带解答 homework 和 4 份带解答 exam 组成。当前 Cornell 目录列出的先修是 PHYS 2213、MATH 2930 与 ECE 2100，而公开教学材料来自 Fall 2007；当前目录要求与旧档案不能写成同一学期。它适合能从文字补全推导、希望靠纸笔题纠正边界条件的人。[MIT 6.013](108-6-013.md)的[官方课程页](https://ocw.mit.edu/courses/6-013-electromagnetics-and-applications-spring-2009)用开放教材、例题、demonstration 与考试连接 electrostatics、magnetics、waves、transmission 和应用；syllabus 要求 18.01/18.02、8.01/8.02、6.002 与 6.00 背景，课程还会使用 Fourier 方法。它更容易展示场方程怎样进入器件与系统，但同样没有完整 lecture-video 序列。

两门课都可以作为第一条主线，按阅读习惯与应用兴趣择一，不必重复同一套 Maxwell 基础。[MIT 6.630](109-6-630.md)提供仿真视频、MATLAB 文件、题目和考试，但 reading/teaching index 不完整，更适合在主线后补 numerical field 或一个特定专题。

## 从通量和边界走到一个有解析极限的数值模型

[工程数学](../mathematics/index.md)需要提供 multivariable calculus、vector analysis、ODE、complex phasor 和 boundary-value language，[物理基础](../physics/index.md)需要提供 electrostatics、magnetic induction、material response 与 energy。对一个简单 vector field 计算 grad/div/curl，画方向、微元面积、法向量与通量；再用 Coulomb 与 Gauss 两种方法解决一个对称问题，并让同一个 \(e^{j\omega t}\) 约定贯穿 phase、Poynting power 和 material loss。

接着选择 coax/microstrip、rectangular waveguide、dielectric interface 或 electrostatic sensor，写 geometry、material、source、boundary conditions 与待求量。推导一个可解极限，再做 parameter sweep 与 mesh refinement，比较 field continuity、Poynting power、stored energy、reflection 或 propagation constant，并以 conservation 或 reciprocity 独立核对。坐标变换只剩公式替换时，缺的是向量几何；边界条件无法由 Maxwell equations 和 constitutive relation 推出时，缺的是物理。

每次换坐标系都画微元长度、面积和法向量，再根据对称性确定积分范围。介质界面则分别写切向与法向条件，指出自由电荷或表面电流是否存在。这个过程会在求解器之前暴露遗漏的尺度因子、法向方向和材料参数。

ECE 3030 是 2007 文字材料，6.013 demonstration 无法充当可复制 RF lab，6.630 的 MATLAB 界面也有年代。迁移到 Python、Julia 或新 MATLAB 时注明 equation、grid、boundary、solver tolerance 和 convergence；每张 field map 附 mesh、domain truncation、material parameter 与 energy/flux residual。漂亮颜色不能代替解析极限和网格收敛。

解析结果与数值结果不一致时，优先检查单位、源归一化、相位约定和人工边界位置。只有这些条件对齐后，网格或求解算法的差异才有可解释意义。

## 能量沿哪条路径离开模型，就决定下一分支

能量沿 transmission line 或 waveguide 传播时，继续 microwave；radiation、far field、matching 和 array 主导时，转 antenna/RF；material dispersion、device geometry 与 mode 主导时，转 photonics/device；目标是 baseband、channel 和 coding 时，在 field/RF front end 后接[通信系统](../communications/index.md)。选择理由应指出当前模型中哪一项近似开始失效。

默认项目范围是解析与仿真。低功率传输线、波导或天线实物需要重新核对法规、仪器和风险；个人学习不搭建市电、高压、强 RF 辐射或未知微波源。材料常数、频率区间、PEC、lossless medium、far-field 与 infinite-boundary 假设都要注明。最终解释应指出能量从哪里进入、在哪里储存或耗散、从哪个边界离开，并区分 Maxwell 方程的结论与数值近似造成的结果。
