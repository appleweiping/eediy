## ECE 4880、毫米波电路课与天线课是三条主线

[Cornell ECE 4880](110-ece-4880.md)从 link budget、noise、mixer、PLL 走到 receiver/transmitter 和 6 个 lab，适合 radio architecture；[官方课程归档](https://ocw.ece.cornell.edu/courses/ece-4880-radio-frequency-systems/)缺 Lecture 1–5，教材、Simulink 与台面也有访问成本。ECE 4880 是 RF-systems 分支首选，不是电路或天线分支的通用入口。[RF and Millimeter-Wave Circuit Design](111-rf-and-millimeter-wave-circuit-design.md)通过 19 个 assignment 和 5 个 design lab 深入 matching、amplification、mixing、oscillation 与 frequency synthesis，其 Qucs-S/Octave 路线仍是 discrete-device teaching flow，不能写成 PDK 级 IC design。

[Microwave Antennas](112-108105114.md)用 40 讲从 field integral、array 走到 aperture 与 reflector，适合 radiation/pattern 分支，却没有开放 lab 或 coding project。[MIT 6.661](113-6-661.md)用开放讲义和 13 套带解题连接 receiver、antenna 与 signal，适合主分支后的理论接口。共享基础之后选 system、circuit 或 antenna 之一；三条主线全修会重复大量 impedance、noise 与 field conversion。

选课可以由最终图表反推：希望交付 cascaded gain、noise figure 与 link budget，走 ECE 4880；希望交付 matching network、amplifier 或 oscillator 的 circuit result，走毫米波电路课；希望交付 pattern、polarization 与 aperture efficiency，走天线课。6.661 更适合解释这些图表背后的 receiver/antenna/signal 关系。这样每门课程承担一个输出，避免把所有材料堆进同一条“RF 大全”。

## 所有数字先绑定 reference plane、\(Z_0\) 与功率定义

[电磁学](../electromagnetics/index.md)提供 Maxwell、boundary、wave impedance、propagation 与 radiation，[电路分析](../circuits/index.md)提供 phasor、resonance、two-port 与 noise，[通信系统](../communications/index.md)提供 modulation、detection、SNR 与 link requirement。开始 CAD 之前，应能在明确 \(Z_0\) 下由 impedance 换算 S-parameter，沿 Smith chart 解释 matching path，并在 Friis cascade 中为每级写 gain、noise factor 与 reference plane。

available gain、transducer gain、mismatch loss 和 antenna realized gain 各有独立定义。对声明为无源的 two-port data 检查 reciprocity、passivity 或 energy balance；只有 active small-signal two-port 才讨论 stability。异常可能来自 active behavior、measurement noise、port order、normalization 或 reference-plane error。图中写清 dB/dBm/linear unit、frequency unit、port direction、polarization 与 coordinate system，否则一次“gain improvement”可能只来自定义变化。

reference plane 移动会把 fixture 的 phase 与 loss 并入或移出 DUT，\(Z_0\) 改变则会改变波量归一化与 S-parameter 数值。power wave、available power 和 delivered power 应沿着同一张端口图定义；天线 gain 还要区分 directivity、radiation efficiency 与 mismatch。每次换算都写出输入量和公式，读者才能判断差异来自器件、匹配还是坐标选择。

## 校外工作以 calibrated passive data 或明确的 simulation 为边界

ECE 4880 的题目与考试仍有价值，但开头 5 讲缺失，6 个 lab 需要 signal source、scope/spectrum 和 VNA 类能力。毫米波课的完整访问可能收费；提供方称多数 lab 使用 Qucs-S/Octave，但目前没有核到可长期匿名下载的 official starter package。天线课则是 lecture/assignment 主导。校外可使用 public S2P、circuit/EM simulation 和 dummy-load/cabled model，注明 frequency grid、port/calibration plane、substrate、loss、mesh、boundary、power 与 software release。

有 VNA 时，完成课程要求的 open/short/load/thru 或等价 calibration，把 reference plane 推至 fixture，再比较 raw 与 de-embedded result。缺少标准件时，不把响应称作精确器件参数。实体工作限于额定 passive 或 cabled dummy-load path；不进行未经许可的 radiation，不把廉价 SDR 当 calibrated spectrum analyzer，也不在 RF power 存在时改接线。公开 S-parameter 还需要 device、bias、temperature、fixture 与 de-embedding condition。

公开 Touchstone 文件也要在导入时核对 format、frequency unit、magnitude/angle 或 real/imaginary encoding，以及 port order。EM simulation 则额外报告 mesh refinement、radiation boundary、substrate stack 和 conductor loss；至少选择一个 passivity 或 energy-balance check。校准数据、fixture model 与 DUT data 分层存放，可避免 de-embedding 后的曲线无法追回原始参考面。

## 第一、二层证据：passive S-parameter 与 Friis active chain

第一层只讨论 **passive S-parameter**。在固定 \(Z_0\) 和 reference plane 下，用 matching network、filter 或 antenna port 的 S2P/EM data 报告 \(S_{11}\)、\(S_{21}\)、insertion loss、reciprocity、passivity 与 energy balance。[IBIS Touchstone 2.1 规范](https://ibis.org/touchstone_ver2.1/touchstone_ver2_1.pdf)定义的是线性网络容器，并非无源专用格式：它可以保存 active small-signal network parameter，两端口文件还可选带 noise parameter。这里选用的 passive S2P 数据集不能支持 active gain、noise figure 或 IIP3。

第二层才是 **active small-signal gain/noise chain**。对 LNA、mixer 与后级逐级写 \(S_{21}\) 或 transducer/available gain、active two-port stability、noise factor、mismatch 与 reference plane，再计算 cascaded gain 和 Friis noise figure；noise parameter、active device 或 behavioral model 必须明确。手里只有 passive S2P 时，最多计算 passive loss 对 system noise budget 的影响，不能把其中的 \(S_{21}\) 改名为 LNA gain。两层可共用 frequency band 与 port drawing，但输入模型和可得结论必须分开。

这两层的交界是第一只 active device 的输入参考面。放在 LNA 前的 filter 或 cable 既降低送入信号，也按其 physical temperature 损害 system noise figure；放在高增益 LNA 后的同样损耗影响不同。逐级表应同时列 linear gain/noise factor 与 dB 显示值，Friis calculation 使用 linear quantity，最终再转回 dB，避免把 dB 直接相加进错误的噪声公式。

## 第三、四层证据：two-tone IIP3 与 LO phase-noise PSD

第三层是 **linearity**。使用能处理 nonlinear behavior 的 active model 做 two-tone sweep，声明 tone spacing、input-power range、output fundamental 与 IM3 的 fit interval。two-tone 曲线只在 fundamental 与 IM3 分别接近一阶、三阶斜率的区间外推 IIP3；进入 compression 后继续拟合会扭曲结果。linear S-parameter simulation 没有 intermodulation mechanism，因此不能证明 blocker tolerance。

第四层是 **LO quality**。为 oscillator/PLL model 报告 phase-noise PSD 随 offset frequency 的曲线，声明 SSB convention、carrier frequency 与 integration band，再计算 RMS phase/time jitter，并说明其怎样进入 mixer reciprocal mixing 或 sampling aperture。IIP3 描述 amplitude nonlinearity，phase noise 描述随机相位扰动；两者不能由同一次 sweep 互相推出，transient 中整齐的一条 clock edge 也不能替代 PSD 与积分带宽。

最终 receive-chain 报告可以共享 band、link budget 和端口图，但四层各自给 input model、unit、simulation command 与结论边界；缺一层就不作对应声明。antenna 分支另加 impedance、efficiency、pattern、polarization 与 mesh convergence。合规台面也只比较额定范围内的 passive 或 cabled path，并带 calibration 与重复测量；其余结论明确限定为模型。

四层汇总表的每一行还应写清 source provenance：public S2P、linear active model、nonlinear device model 或 oscillator/PLL noise model。相同器件名并不保证这些模型来自同一 bias、temperature 或 process corner；跨层连接时要注明这种不一致。这样最终 link budget 会显示哪些数值是直接输入、哪些是计算结果、哪些仍待合规台面确认。
