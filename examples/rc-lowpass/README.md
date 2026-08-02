# RC low-pass: one model, three evidence classes / RC 低通：一个模型，三类证据

This starter is deliberately small, but it is not a screenshot demo. It
contains a deterministic analytical reference, a checksum-verified
standard-library analysis, an independent ngspice deck, predeclared
acceptance limits, and failing-input tests.

这个 starter 的范围很小，但不是“跑出一张图”的演示。仓库里同时保留了可确定生成的
解析参考、带校验和的标准库分析、独立的 ngspice 网表、事先写定的验收界限，以及针对
坏输入的自动测试。

## Evidence boundary / 证据边界

| Class | What exists here | What may be claimed |
| --- | --- | --- |
| `analytic_reference` / 解析参考 | `generate_reference.py` evaluates the ideal first-order equations / 由解析式直接生成 | The scripts recover \(\tau\) and \(f_c\) for the stated ideal model; this response alone cannot identify \(R\) and \(C\) separately / 脚本能恢复已声明理想模型的 \(\tau\) 与 \(f_c\)，但仅凭该响应不能分别辨识 \(R\) 与 \(C\) |
| `simulation` / 数值仿真 | `rc_lowpass.cir` asks ngspice to solve the same ideal circuit / ngspice 求解同一理想电路 | A solver result for this netlist and its settings / 只对该网表及设置成立的求解结果 |
| `measurement` / 实测 | **None / 没有** | No breadboard, oscilloscope, component, or safety claim / 不声称搭过电路、接过示波器或验证过器件与安全性 |

Do not rename a generated or ngspice file to `raw-measurement.csv`. A real
measurement needs a new run record with instrument model, channel, probe
ratio, range, sample rate, calibration basis, wiring, trigger definition,
UTC time, and an immutable raw-file checksum.

不要把解析文件或 ngspice 输出改名成 `raw-measurement.csv`。真实测量必须另建 run
record，至少记录仪器型号、通道、探头倍率、量程、采样率、校准依据、接线、触发定义、
UTC 时间和不可变原始文件的校验和。

## Circuit and predictions / 电路与预期

The modeled network is a 1 V source driving a \(1\ \mathrm{k\Omega}\) series
resistor, with a \(1\ \mathrm{\mu F}\) capacitor from the output node to
ground. The step occurs at \(t_0=2\ \mathrm{ms}\). For this ideal unloaded
network,

\[
\tau=RC=1\ \mathrm{ms},\qquad
f_c=\frac{1}{2\pi RC}=159.154943\ \mathrm{Hz}.
\]

After the input event, \(v_\mathrm{out}\) reaches \(1-1/e\) of its final
change one time constant later. The event is intentionally delayed:
\(t_0=2\ \mathrm{ms}\), so the absolute crossing is near \(3\ \mathrm{ms}\)
while the time constant remains \(3-2=1\ \mathrm{ms}\). Reporting 3 ms as
\(\tau\) is a failed analysis.

理想、空载的一阶网络满足上式。输入事件被故意延迟到 \(t_0=2\ \mathrm{ms}\)：
输出在绝对时间约 3 ms 达到 63.2%，但时间常数必须相对触发点计算，即
\(3-2=1\ \mathrm{ms}\)。把 3 ms 报成 \(\tau\) 就是失败。

## Offline rebuild / 离线重建

From the repository root, run:

```console
python examples/rc-lowpass/run.py
```

No network access or third-party Python package is used. The command creates
the disposable `examples/rc-lowpass/build/` directory and performs this chain:

1. generate `analytic_step.csv` and `analytic_ac.csv` from fixed equations;
2. write `manifest.json` with units, parameters, row counts, data class, and
   SHA-256 checksums;
3. refuse analysis if either CSV no longer matches the manifest;
4. calculate \(t_0\), the interpolated 63.2% crossing, \(\tau\), half-power
   cutoff, and cutoff phase;
5. compare the result with `expected/acceptance.json`.

这条命令不访问网络，也不依赖第三方 Python 包。它生成可删除的 `build/` 目录，
写入带单位与 SHA-256 的 provenance manifest，先校验输入，再计算阶跃和 AC 指标，
最后按 `expected/acceptance.json` 中预先写定的容差验收。

A passing console summary is approximately:

```text
data_kind=analytic_reference
measurement_claim=false
trigger_time_s=0.002
threshold_crossing_time_s=0.003
tau_63_2_s=0.001
cutoff_hz=159.16
phase_at_cutoff_deg=-45.00
verification=PASS
```

The committed acceptance file is authoritative; the rounded text above is
only a reading aid. `build/summary.json` preserves the unrounded values,
method names, cross-check, and limitations.

提交到仓库的 acceptance 文件才是验收依据；上面的数字经过舍入，只供快速阅读。
未舍入结果、方法、交叉核对与局限保存在 `build/summary.json`。

## Independent ngspice path / 独立 ngspice 路径

If ngspice is installed, first run the Python command above to create
`build/`, then:

```console
cd examples/rc-lowpass
ngspice -o build/ngspice.log rc_lowpass.cir
```

The deck uses the documented `meas` and `wrdata` forms in the official
[ngspice user manual](https://ngspice.sourceforge.io/docs/ngspice-manual.pdf).
It runs `.op`, transient, and AC analyses, prints `t0`, `t63`,
`tau63=t63-t0`, and `f3db`, then writes numeric solver output to
`build/ngspice_step.dat` and `build/ngspice_ac.dat`. These files are
**simulation**, not analytical reference and not measurement. A small
control-block header fixes `wr_singlescale`, vector names, and numeric
precision so the verifier can reject column-shape drift. A small
difference from the equations is expected from the finite 100 ns source rise,
transient step, AC grid, and numerical tolerances; a large discrepancy calls
for inspecting the deck and solver log, not widening the analytical
acceptance after the fact.

After ngspice exits, verify the generated columns and numerical results:

```console
python verify_ngspice.py
```

CI installs ngspice, records `ngspice --version`, runs this exact control-mode
command, rejects solver errors or failed measurements, and checks the
independently parsed \(\tau\) and cutoff frequency. The Python-only unit test
still remains usable on machines without ngspice.

网表按官方手册中的 `meas` 与 `wrdata` 形式运行 `.op`、transient 和 AC，打印
`t0`、`t63`、扣除延迟后的 `tau63` 与 `f3db`，并把数值输出写到 `build/`。
这些文件属于**仿真**，既不是解析参考，也不是实测。100 ns 上升沿、瞬态步长、
AC 网格和求解容差会带来小差异。控制块同时固定 `wr_singlescale`、列名与数值精度，
让校验器能拒绝输出列结构漂移；若数值差异很大，应先查网表和日志，不能事后放宽解析验收标准。

上面的 `-o build/ngspice.log` 会把求解日志写到校验器实际读取的位置。ngspice
退出后运行 `python verify_ngspice.py`，可检查输出列、solver 错误、
measurement failure，以及独立解析得到的 \(\tau\) 与截止频率。CI 会安装 ngspice、
记录版本并实际走完这条控制模式命令；没有 ngspice 的机器仍可单独运行 Python 测试。

## Tests and deliberate failures / 测试与故障注入

From the repository root:

```console
python -m pytest tests/test_rc_lowpass_example.py -q
```

The tests rebuild twice under the same recorded Python version, require
byte-identical generated inputs, verify the delayed-trigger calculation, tamper
with a CSV and require checksum rejection, remove stale solver output on a new
run, and parse active netlist lines to check component topology, parameter
values, control-block balance, and analysis order. They do not replace an
execution test with an installed ngspice whose version is recorded.

测试会在同一个已记录的 Python 版本下重建两次并要求解析输入逐字节一致；它还会核对
非零触发延迟，篡改一份 CSV 并要求校验和拒绝继续，确认新运行会移除旧 solver 输出，
再解析网表中的有效行，核对元件拓扑、参数值、控制块配对和分析顺序。它不能替代安装
ngspice、记录其版本并实跑网表。

## Limits and extension path / 局限与扩展

This model omits resistor and capacitor tolerance, ESR, leakage, source and
load impedance, breadboard parasitics, probe loading, noise, quantization,
temperature, and uncertainty propagation. It supports a software and modeling
exercise only. It is not evidence that a physical circuit meets a rating or
that a setup is safe.

模型没有电阻/电容容差、ESR、漏电、源/负载阻抗、面包板寄生、探头负载、噪声、
量化、温度或不确定度传播，因此只能支持软件与建模练习，不能证明实物满足额定值，
也不能证明实验条件安全。

For a measured extension, keep the generated reference unchanged. Add a
separate immutable raw-data directory and run manifest, write an importer that
maps documented instrument columns into SI units, and define a tolerance from
sample interval, instrument accuracy, component tolerance, and model
discrepancy before viewing the answer. Preserve both results so “model versus
measurement” remains a comparison rather than a relabeling.

扩展到实测时，不要覆盖这份解析参考。另建只读 raw-data 目录和 run manifest，
用导入脚本把已记录的仪器列映射到 SI 单位，并在看答案前根据采样间隔、仪器精度、
元件容差和模型偏差确定容差。解析、仿真与实测应并列保存，不能靠改标签混成一类。
