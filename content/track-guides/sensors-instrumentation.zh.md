## 课程 136 讲仪器，课程 137 解释传感机理

[NPTEL Electrical Measurement and Electronic Instruments](136-108105153.md)的[官方课程页](https://nptel.ac.in/courses/108105153)用 84 个以上 video 与 demonstration 覆盖 meter、bridge、oscilloscope、transducer 与 electronic instrument，适合建立测量理论地图；公开层没有可复现家庭实验、代码或答案反馈。[Sensor Technologies](137-108106193.md)的[官方课程页](https://nptel.ac.in/courses/108106193)用 8 周连接 sensor physics、fabrication 与 circuit，没有开放 build-and-test loop，适合在选定 thermistor、strain、capacitive 或 optical mechanism 后补器件理解。

两门课都应按 lecture/demonstration 资源阅读。课程展示没有公开 calibration reference、BOM、raw data 和逐步反馈，因此不能写成校外学习者亲自完成的实验。136 解决“仪表怎样表示和加载被测量”，137 解决“材料或结构怎样把 measurand 变成 electrical quantity”，角色互补而非前后证书序列。

阅读 demonstration 时，可分别摘出被测量、reference、excitation、instrument range 和显示结果，再注明哪些 calibration step 未公开。课程 137 的 sensor mechanism 则整理成 transfer relation、temperature dependence 与主要 noise/source-of-drift。两张表相接后，器件物理与仪器读数才不会混成一份名词清单。

## 课程 138 是一条具体、可能付费的 PSoC 传感链

[Sensors and Sensor Circuit Design](138-ecea-5340.md)在[官方 Coursera 页面](https://www.coursera.org/learn/sensors-circuit-interface)中包含 5 个 module、5 项 assignment、thermistor lab 与 course project；[Colorado 官方媒体页](https://www.colorado.edu/ecee/media/2412)用于核对课程材料来源。完整实践依赖 PSoC 5LP、LCD、配套器件、oscilloscope 与 Windows toolchain，平台内容与评分访问也可能收费。只有 hardware 和 registered course access 都真实存在时，才把 138 作为原课程项目路线。

缺少 PSoC 或平台权限时，可以课程 136 为测量主线、从 137 选相应 sensor physics，并独立实现一条低压链；这种实现不冒充 138 的 assignment、grader 或 project。三门全学会重复大量 sensor taxonomy，并不会自动提升 calibration、uncertainty 和 fault detection。

PSoC 路线的价值在于 analog front end、ADC、firmware display 与课程作业处于同一平台。移植路线要把这些接口重新定义：输入范围如何映射 ADC code，采样定时如何触发，LCD 或 host 输出如何表示 invalid state。课程素材可提供任务边界，新的 driver 与 board support package 仍属于独立实现。

## 从 measurand 到 ADC 的每一级都有单位、噪声与余量

为 thermistor、strain gauge 或 capacitive sensor 画 `measurand → transduction → excitation/bridge → gain/filter → ADC`。逐段写 unit、range、source impedance、noise、saturation、power 与 bandwidth。[模拟电子](../analog-electronics/index.md)中的 instrumentation amplifier、common-mode、output swing 与 noise，[信号与系统](../signals-systems/index.md)中的 sampling、settling 与 frequency response，以及[电子实验](../electronics-laboratory/index.md)中的 reference、probe loading 与 grounding，要落在同一张表。

从最小待分辨变化向后换算 sensor output、front-end voltage 与 ADC code，再把 reference error、offset、gain error、quantization 与 noise 折回 measurand unit。resolution、accuracy、repeatability、hysteresis 和 sensitivity 分别列出。数字平均无法恢复 front-end clipping，也不能修复 amplifier common-mode 超界或 sensor self-heating；如果信号只依赖显示小数位才可见，链路余量已经不足。

error budget 应同时有 typical 与 worst-case 两列。offset 和 gain error 可通过 calibration 估计，quantization 由 ADC step 决定，random noise 需要由带宽与 sample statistics 描述；hysteresis 和 drift 则不能被单次静态拟合吸收。把各项折回同一 measurand 单位后，才知道增加 amplifier gain、提高 ADC bits 或改善 reference 中哪一项真正有效。

## Thermistor lab 要同时经历升温、降温和 held-out data

为低压 thermistor divider 设 temperature range、response time、allowable self-heating、sample rate 与 target error。由 datasheet model 和实际 resistance 预测 divider voltage，选择 excitation 与 reference resistor，使全温区保有 ADC headroom。实验注明 reference thermometer specification、supply、ADC reference、environment settling time 与 connection drawing；至少采集 5 个 temperature point，并在升温和降温方向各重复多次。

把数据划为 calibration 与 untouched test，比较 Steinhart-Hart、lookup table 或 simple polynomial 中至少两种方法。结果报告 residual、repeatability、hysteresis、settling 和 uncertainty，而不只给 \(R^2\)。改变 excitation 或 sample interval，检查 self-heating 与 dynamic lag 是否按预测移动。若使用 public/synthetic data，要明确它不能证明真实 ageing、contact thermal resistance、sensor accuracy 或 front-end noise。

升温和降温数据应在相同温度轴上分别显示，避免平均后抹掉 hysteresis。每个温度平台的稳定判据可以由 reference thermometer 变化率和等待时间共同定义，原始 timestamp 用于重算 settling。held-out set 只在模型选定后评估；若看到 test residual 后又调整 polynomial order，该数据已不再承担独立检验。

## 平台迁移与工业回路分别受版本和安全边界约束

PSoC 5LP、LCD、器件和 Windows IDE 是课程 138 的具体平台。迁移到其他 MCU 时，重新确定 ADC reference、input range、timing、driver 与 test；只换 pin 不构成功能等价。项目材料应包含 schematic、firmware/notebook、raw/calibration/test split、instrument range 与 calibration state、environment、software version 和 residual。正常测试之后再注入 open circuit、short、ADC saturation、overrange 或 drift，系统需要输出明确 fault state，不能继续显示貌似可信的数值。

实体练习限于 isolated、current-bounded low voltage。未知 industrial transducer、4–20 mA loop、mains-referenced instrument 与 body-contact measurement 可能引入 external supply、ground potential 和 isolation risk，应在相应设施处理。替换 data-acquisition tool 后，额定值和安全连接要求保持原样；课程名称只说明教学主题，跨越这些边界仍需相应设施与授权。

fault injection 也要在低能量边界内实现，例如由可控 resistor 或 software stub 模拟 open/short，而非直接破坏未知设备。fault state 应与正常量程外读数区分，并在 raw code、engineering unit 和 user display 三层保持一致。恢复正常输入后，系统是否自动复位、需要人工确认或维持 latched alarm，也应由需求明确。
