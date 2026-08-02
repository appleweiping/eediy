## 6.003 的题目链先建立系统观，EE 261 再把 Fourier 做深

[MIT 6.003](083-6-003.md)在[官方 OCW 归档](https://ocw.mit.edu/courses/6-003-signals-and-systems-fall-2011/)中用连续/离散 LTI、卷积、变换、采样和反馈组成完整的习题与考试体系，适合第一次学习；它没有 programming 或 hardware lab。[Stanford EE 261](097-ee-261.md)的[官方 Stanford Engineering Everywhere 页面](https://see.stanford.edu/Course/EE261)有 30 个视频、讲义、9 套带解作业和考试，Fourier transform 的深度更适合通信、成像和频谱方向。通常先完成 6.003，再按需要取 EE 261 的 Fourier 单元，不必重复两个完整学期。

[MIT RES.6-007](084-res-6-007.md)讲解和例题密集却没有考试；[ECE 3250](086-ece-3250.md)提供数学专著、11 份作业与 2 套无解考试；[ECE 2200](085-ece-2200.md)有 10 套带解作业、4 套带解考试和 5 份 lab prompt，却没有配套讲义。它们分别适合补解释、补严格文字或补题。[MIT 6.011](098-6-011.md)再用开放教材与考试把信号、通信和控制接起来，应放在基础之后。

## 一只 RC 在微分方程、卷积与极点中只能有一段物理历史

以 RC low-pass 为对象，从[电路分析](../circuits/index.md)的 KCL 与初值写 differential equation，再由 impulse response 写 convolution，最后用 transfer function 解释 pole、DC gain、time constant 与 -3 dB point。[工程数学](../mathematics/index.md)中的复指数、积分和线性微分方程在这里不是独立章节，而是三种表示间的翻译工具。对 step、impulse 和 sinusoid 输入分别给出预测，检查单位、因果性、稳定性与 \(t=0^+\) 的连续/跳变条件；三种推法若给出不同初始行为，应回到 initial condition 和 unilateral/bilateral transform 的选择。

离散部分再从定义计算一组短序列 convolution，明确 index origin、support 与 boundary。极点不能只被当作多项式根，它还应解释自然响应；频响幅度也不能脱离 phase、delay 与 transient。输入变成随机过程、correlation 或 PSD 时，需要[概率与统计](../probability-statistics/index.md)给出统计含义，而不是在信号课里临时记一组公式。

## 两根正弦与四种窗口设置足以暴露采样误读

构造 \(x(t)=\sin(2\pi 300t)+0.5\sin(2\pi 1300t)\)，分别用 8 kHz 和 2 kHz 采样；运行代码之前先画离散频率并预测 1300 Hz 在低采样率下的 alias 位置。随后比较 64、256、1024 点以及 rectangular/Hann window，明确 time array、raw samples、FFT normalization 与 frequency axis，解释 bin spacing、main-lobe width、leakage 和 amplitude bias。再设计简单 FIR 或一阶 IIR，仅保留目标分量，并用 difference equation、impulse response 与 frequency response 同时解释 delay、transient 和 steady state。

6.003 与 EE 261 没有统一的现代 Python lab，EE 261 的小型 MATLAB 工具也较旧；NumPy/SciPy notebook 应标明是独立计算练习。ECE 2200 的 lab prompt 可以提供问题，但软件 trace 不等于实体测量。若项目换成 audio、sensor 或 baseband data，要注明来源、checksum、sampling rate、单位与 acquisition 条件，并保留一个可手算片段。课程的落点是让同一极点、采样率或窗口选择同时约束公式、代码和两域图像。

同一 notebook 输出一张参数—预测表：采样率变化对应 alias 位置，窗口长度对应 bin spacing，window type 对应 main-lobe 与 leakage，pole 移动对应 transient 与 bandwidth。先填写预测，再逐项回填运行结果；任何不一致都要追回 normalization、index、initial condition 或 pole placement，而不是在图画完后另找一段公式解释。
