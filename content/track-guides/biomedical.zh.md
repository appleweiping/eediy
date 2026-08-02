## NPTEL 从电极和传感器讲起，分类器留在后面

[NPTEL Biomedical Instrumentation](139-102106669.md)的[官方课程页](https://nptel.ac.in/courses/102106669)把生理信号、电极与传感器接到放大、记录、安全和临床应用，适合建立第一条测量主线。公开 video sequence 与 12 周 syllabus 并非逐项完全对应，Week 11–12 的 laser、安全和监管主题也没有清晰映射；同时缺少公开项目、实验、代码和逐题答案。它能说明测量链由哪些部分组成，却不能替学习者提供一套可复现实验。

选择 ECG、EEG 或 PPG 中一种，画 physiology→electrode/sensor→front end→filter→ADC→stored record。每一段注明单位、动态范围、带宽、噪声来源、饱和方式与常见 artifact。ADC counts 到电压的 calibration、electrode impedance 和 isolation boundary 还不清楚时，“波形看起来很干净”没有可靠含义。

还要区分课程中用于说明原理的示意波形与带有采集条件、标注规则和缺失值说明的数据记录；二者承担的证据强度不同。

## 一段公开 ECG 同时考验仪器、DSP 和生理解释

[传感器与仪器](../sensors-instrumentation/index.md)提供 front end、calibration、uncertainty、CMRR 与 isolation；[数字信号处理](../dsp/index.md)提供 sampling、filter、spectrum、phase delay 与 validation；[物理基础](../physics/index.md)则负责 bioelectric、optical 或 acoustic interaction。拿一条许可明确的公开 ECG，读清 sampling rate、lead、unit、annotation 和 missing-data 说明，再标出 baseline wander、mains interference、motion artifact 与 clipping。

处理任务可以只做一件事，例如降低工频干扰且不过度移动 QRS timing。原始与处理后片段并排，幅度和延迟都有数字，并把异常定位到身体、电极、前端或算法。“更平滑”不构成 DSP 指标，设备输出也不构成诊断真值；无法用单位和耦合机制解释 artifact 时，扩大模型规模不会增加可信度。

若不同导联、受试者或设备的误差分布明显不同，结论应按这些来源分层呈现，不能只给一个总体平均值。

## HST.582J 的算法材料建立在可信测量链之后

[MIT HST.582J](140-hst-582j.md)的[公开课程档案](https://ocw.mit.edu/courses/hst-582j-biomedical-signal-and-image-processing-spring-2007)适合继续 ECG/EEG processing、statistical estimation、image reconstruction 或 segmentation。多数讲义、labs 与 MATLAB workflow 可用，但若干 MRI、surgical applications、Random Signals III 和总结讲次缺 notes，旧数据链接与 MATLAB 接口也需要迁移。移到 Python、MNE、NeuroKit2 或 WFDB 时，应保持同一数据、subject-level split 与 metric，并明确新实现并非 MIT 原 lab。

数据表在模型之前确定 record 列表、annotation provenance、baseline、denominator 与 non-diagnostic scope。同一人的相邻窗口不能随机分到 train/test 两边；annotation 缺少 clinical gold standard 时，sensitivity、specificity 或 segmentation error 的结论也随之降级。简单 baseline 排除受试者泄漏和采集设备差异后，更复杂的模型才有比较意义。

图像重建与分割还要注明像素间距、扫描协议和预处理；这些采集差异若与标签相关，模型可能只是在识别设备或医院，未必识别了目标生理结构。

## 人体、安全和隐私决定项目能走多远

默认使用去标识、许可清楚的公开数据或 synthetic signal，并注明 dataset version、checksum、sampling/units、license、exclusion 与 retention。未经伦理审批不自行采集人体信号；自制 mains-powered、非医疗隔离或 leakage current 不明的设备不能接到人体。低压 wearable 仍涉及 consent、privacy、skin contact、battery 与删除期限。

合适的收束是一份公开波形的 error/safety budget，或严格标为非诊断用途的 beat-quality、artifact-rejection、segmentation 研究。前者应解释饱和、断联或运动伪迹怎样穿过测量链；后者需给数据版本、代码环境、结果表与异常样本。课程材料不提供医疗器械认证、临床训练或诊断授权；真实人体采集、患者决策和器械验证需要伦理、临床与合格硬件共同支持。
