from __future__ import annotations

import copy
import hashlib
import re
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence
from urllib.parse import urlsplit, urlunsplit

from scripts.quality_common import (
    Issue,
    QualityError,
    localized,
    localized_list,
    slugify,
)


SCHEMA_VERSION = "1.0.0"
ROLES = {"mainline", "alternative", "supplement"}
TIERS = {"S", "A", "B"}
LEVELS = {"introductory", "intermediate", "advanced", "unspecified"}
PRACTICE_MODALITIES = {"simulation-only", "low-energy", "supervised", "standard"}
COVERAGE_KEYS = ("video", "notes", "practice", "labs", "exams", "code")
RESOURCE_STATUSES = {
    "available",
    "degraded",
    "archived",
    "unavailable",
    "review-needed",
}
GENERATED_RESOURCE_ID_RE = re.compile(
    r"^(?:course|video|notes|assignments|labs|projects|exams|code|textbook)-[0-9a-f]{10}$"
)
RESOURCE_ACCESS = {
    "open",
    "open-registration",
    "free-audit",
    "limited-free",
    "paid",
    "institutional",
}
HIGH_VALUE_RESOURCE_KINDS = {
    "course",
    "video",
    "notes",
    "textbook",
    "assignments",
    "labs",
    "projects",
    "exams",
    "code",
    "dataset",
    "simulator",
}

# Candidate IDs intentionally describe the source research vocabulary. Every
# non-identical mapping is explicit so a new or mistyped track fails loudly.
TRACK_ALIASES = {
    "programming": "programming-tools",
    "circuits-laboratory": "electronics-laboratory",
    "analog-ic-design": "analog-ic",
    "fpga": "fpga-soc",
    "system-on-chip": "fpga-soc",
    "real-time-systems": "real-time-cps",
    "cyber-physical-systems": "real-time-cps",
    "signals": "signals-systems",
    "signal-processing": "dsp",
    "communication-systems": "communications",
    "information-theory": "information-theory-coding",
    "coding-theory": "information-theory-coding",
    "control": "control-systems",
    "rf-microwave": "rf-microwave-antennas",
    "antennas": "rf-microwave-antennas",
    "semiconductors": "semiconductor-devices",
    "analog-ic-design": "analog-ic",
    "vlsi": "vlsi-ic",
    "microfabrication": "fabrication-mems",
    "mems": "fabrication-mems",
    "photonics": "optics-photonics",
    "power-systems": "power-systems-machines",
    "electrical-machines": "power-systems-machines",
    "renewable-energy": "energy-storage-pv",
    "pcb-design": "pcb-eda",
    "instrumentation": "sensors-instrumentation",
    "sensors": "sensors-instrumentation",
    "biomedical-engineering": "biomedical",
    "capstone": "capstone-practice",
}

ROLE_TEXT = {
    "mainline": ("主线", "Mainline"),
    "alternative": ("替代", "Alternative"),
    "supplement": ("补充", "Supplement"),
}

TIER_TEXT = {
    "S": (
        "资源完整、教学设计清晰，适合作为该方向的优先选择。",
        "A particularly complete and well-structured option for this track.",
    ),
    "A": (
        "核心内容可靠，适合按自身背景作为主课或高质量替代。",
        "A reliable option that can serve as a main course or strong alternative.",
    ),
    "B": (
        "在特定主题上有明确价值，建议与更完整的主线资源配合。",
        "Useful for specific topics and best paired with a more complete mainline resource.",
    ),
}


SUPERVISED_TRACKS = {
    "energy-storage-pv",
    "fabrication-mems",
    "optics-photonics",
    "power-electronics",
    "power-systems-machines",
    "rf-microwave-antennas",
}

# Tooling is deliberately keyed by every canonical track. These are
# maintainer-suggested, mostly open-source verification paths, not inferred
# provider requirements. Keeping the mapping exhaustive makes a newly added
# track fail loudly instead of silently falling back to browser/PDF boilerplate.
TRACK_TOOLING = {
    "mathematics": {
        "software": (
            "Python 3、Jupyter、NumPy、SciPy、SymPy 与 Matplotlib",
            "Python 3, Jupyter, NumPy, SciPy, SymPy, and Matplotlib",
        ),
        "hardware": (
            "可运行 notebook 并保存结果的通用计算机；不假设专用实体硬件",
            "a general-purpose computer that can run notebooks and retain results; no dedicated physical hardware is assumed",
        ),
        "cost_class": "compute",
        "evidence": ("theory", "simulation"),
    },
    "probability-statistics": {
        "software": (
            "Python 3、Jupyter、NumPy、SciPy、pandas、statsmodels 与 Matplotlib",
            "Python 3, Jupyter, NumPy, SciPy, pandas, statsmodels, and Matplotlib",
        ),
        "hardware": (
            "可重复运行统计 notebook 并保留数据快照的通用计算机；不假设专用实体硬件",
            "a general-purpose computer that can rerun statistical notebooks and retain data snapshots; no dedicated physical hardware is assumed",
        ),
        "cost_class": "compute",
        "evidence": ("theory", "simulation"),
    },
    "physics": {
        "software": (
            "Python 3、Jupyter、SciPy、Matplotlib 与 VPython",
            "Python 3, Jupyter, SciPy, Matplotlib, and VPython",
        ),
        "hardware": (
            "课程实验手册明确列出的低压传感器、数据采集接口与基础测量器具",
            "low-voltage sensors, a data-acquisition interface, and basic measurement tools explicitly listed by the course lab manual",
        ),
        "cost_class": "bench",
        "evidence": ("theory", "simulation"),
    },
    "programming-tools": {
        "software": (
            "Python 3、Git、pytest、Jupyter 与 VSCodium 或同类编辑器",
            "Python 3, Git, pytest, Jupyter, and VSCodium or a comparable editor",
        ),
        "hardware": (
            "可运行测试、版本控制和 notebook 的通用计算机；不假设专用实体硬件",
            "a general-purpose computer that can run tests, version control, and notebooks; no dedicated physical hardware is assumed",
        ),
        "cost_class": "compute",
        "evidence": ("code",),
    },
    "ee-introduction": {
        "software": (
            "Qucs-S、ngspice、KiCad、Python 3 与 Jupyter",
            "Qucs-S, ngspice, KiCad, Python 3, and Jupyter",
        ),
        "hardware": (
            "限流低压电源、面包板、数字万用表及课程明确指定的入门开发板或元件",
            "a current-limited low-voltage supply, breadboard, digital multimeter, and any introductory board or components explicitly specified by the course",
        ),
        "cost_class": "bench",
        "evidence": ("design", "simulation"),
    },
    "circuits": {
        "software": (
            "Qucs-S、ngspice、Python 3 与 Jupyter",
            "Qucs-S, ngspice, Python 3, and Jupyter",
        ),
        "hardware": (
            "限流低压电源、面包板、数字万用表、示波器与函数发生器",
            "a current-limited low-voltage supply, breadboard, digital multimeter, oscilloscope, and function generator",
        ),
        "cost_class": "bench",
        "evidence": ("theory", "simulation"),
    },
    "electronics-laboratory": {
        "software": (
            "ngspice、sigrok/PulseView、Python 3 与 Jupyter",
            "ngspice, sigrok/PulseView, Python 3, and Jupyter",
        ),
        "hardware": (
            "限流台式电源、数字万用表、示波器、函数发生器、面包板与逻辑分析仪",
            "a current-limited bench supply, digital multimeter, oscilloscope, function generator, breadboard, and logic analyzer",
        ),
        "cost_class": "bench",
        "evidence": ("design",),
    },
    "analog-electronics": {
        "software": (
            "Qucs-S、ngspice、KiCad、Python 3 与 Jupyter",
            "Qucs-S, ngspice, KiCad, Python 3, and Jupyter",
        ),
        "hardware": (
            "限流低压电源、面包板、数字万用表、示波器、函数发生器与课程指定器件",
            "a current-limited low-voltage supply, breadboard, digital multimeter, oscilloscope, function generator, and course-specified devices",
        ),
        "cost_class": "bench",
        "evidence": ("design", "simulation"),
    },
    "signals-systems": {
        "software": (
            "Python 3、Jupyter、NumPy、SciPy 与 Matplotlib",
            "Python 3, Jupyter, NumPy, SciPy, and Matplotlib",
        ),
        "hardware": (
            "可运行数值实验并保存输入输出数据的通用计算机；不假设专用实体硬件",
            "a general-purpose computer that can run numerical experiments and retain input/output data; no dedicated physical hardware is assumed",
        ),
        "cost_class": "compute",
        "evidence": ("theory", "simulation"),
    },
    "digital-logic": {
        "software": (
            "Logisim Evolution、Icarus Verilog 或 Verilator，以及 GTKWave",
            "Logisim Evolution, Icarus Verilog or Verilator, and GTKWave",
        ),
        "hardware": (
            "课程明确指定的逻辑实验板、USB 编程器和逻辑分析仪",
            "a logic training board, USB programmer, and logic analyzer explicitly specified by the course",
        ),
        "cost_class": "bench",
        "evidence": ("design", "code", "simulation"),
    },
    "electromagnetics": {
        "software": (
            "openEMS、GNU Octave 或 Python 3，以及 ParaView",
            "openEMS, GNU Octave or Python 3, and ParaView",
        ),
        "hardware": (
            "可承担网格计算并保存场数据的计算机；实体场测量仅使用课程指定的合规设施",
            "a computer capable of mesh-based computation and field-data storage; use only course-specified compliant facilities for physical field measurements",
        ),
        "cost_class": "compute",
        "evidence": ("theory", "simulation"),
    },
    "computer-architecture": {
        "software": (
            "RISC-V GNU 或 LLVM 工具链、QEMU、Verilator 与 GTKWave",
            "a RISC-V GNU or LLVM toolchain, QEMU, Verilator, and GTKWave",
        ),
        "hardware": (
            "可运行仿真和交叉编译的通用计算机；仅在课程明确要求时使用指定 RISC-V 或 FPGA 板",
            "a general-purpose computer for simulation and cross-compilation; use a specified RISC-V or FPGA board only when the course explicitly calls for it",
        ),
        "cost_class": "compute",
        "evidence": ("design", "code", "simulation"),
    },
    "fpga-soc": {
        "software": (
            "Yosys、nextpnr、Verilator 与 GTKWave；仅在目标器件需要时安装提供方指定的厂商工具链并核对许可",
            "Yosys, nextpnr, Verilator, and GTKWave; install a provider-specified vendor toolchain only when the target device requires it and verify its license",
        ),
        "hardware": (
            "课程明确支持的 FPGA 开发板、USB/JTAG 编程器与逻辑分析仪",
            "a course-supported FPGA development board, USB/JTAG programmer, and logic analyzer",
        ),
        "cost_class": "bench",
        "evidence": ("design", "code", "simulation"),
    },
    "embedded-systems": {
        "software": (
            "GCC 或 LLVM、CMake、GDB、OpenOCD，以及 Renode 或 QEMU",
            "GCC or LLVM, CMake, GDB, OpenOCD, and Renode or QEMU",
        ),
        "hardware": (
            "课程明确支持的微控制器开发板、USB 调试器、限流低压电源与逻辑分析仪",
            "a course-supported microcontroller development board, USB debugger, current-limited low-voltage supply, and logic analyzer",
        ),
        "cost_class": "bench",
        "evidence": ("design", "code"),
    },
    "real-time-cps": {
        "software": (
            "Zephyr 或 FreeRTOS 源码、GCC 或 LLVM、CMake、GDB，以及 Renode 或 QEMU",
            "Zephyr or FreeRTOS source, GCC or LLVM, CMake, GDB, and Renode or QEMU",
        ),
        "hardware": (
            "课程支持的实时控制开发板、USB 调试器、逻辑分析仪及低压传感器/执行器",
            "a course-supported real-time control board, USB debugger, logic analyzer, and low-voltage sensors/actuators",
        ),
        "cost_class": "bench",
        "evidence": ("design", "code"),
    },
    "hardware-security": {
        "software": (
            "Verilator、Yosys、GTKWave、Python 3 与 Jupyter",
            "Verilator, Yosys, GTKWave, Python 3, and Jupyter",
        ),
        "hardware": (
            "课程明确支持的测试板、隔离/限流供电、逻辑分析仪；侧信道设备只在合规实验环境使用",
            "a course-supported test board, isolated/current-limited power, and logic analyzer; use side-channel equipment only in a compliant lab",
        ),
        "cost_class": "specialized",
        "evidence": ("design", "code"),
    },
    "dsp": {
        "software": (
            "Python 3、Jupyter、NumPy、SciPy、Matplotlib 与 GNU Octave",
            "Python 3, Jupyter, NumPy, SciPy, Matplotlib, and GNU Octave",
        ),
        "hardware": (
            "课程明确指定的音频接口、DSP/微控制器板或软件定义无线电；先用录制数据验证",
            "a course-specified audio interface, DSP/microcontroller board, or software-defined radio; validate with recorded data first",
        ),
        "cost_class": "bench",
        "evidence": ("simulation", "code"),
    },
    "communications": {
        "software": (
            "GNU Radio、Python 3、Jupyter、NumPy、SciPy 与 GNU Octave",
            "GNU Radio, Python 3, Jupyter, NumPy, SciPy, and GNU Octave",
        ),
        "hardware": (
            "课程明确支持的软件定义无线电、衰减器、屏蔽连接与合规天线/负载",
            "a course-supported software-defined radio, attenuators, shielded connections, and compliant antenna/load",
        ),
        "cost_class": "specialized",
        "evidence": ("theory", "simulation"),
    },
    "information-theory-coding": {
        "software": (
            "Python 3、Jupyter、NumPy、SciPy 与 SageMath",
            "Python 3, Jupyter, NumPy, SciPy, and SageMath",
        ),
        "hardware": (
            "可重复运行编码实验并保存随机种子和结果的通用计算机；不假设专用实体硬件",
            "a general-purpose computer that can rerun coding experiments and retain seeds and results; no dedicated physical hardware is assumed",
        ),
        "cost_class": "compute",
        "evidence": ("theory", "code"),
    },
    "control-systems": {
        "software": (
            "Python 3、Jupyter、python-control、SciPy 与 GNU Octave",
            "Python 3, Jupyter, python-control, SciPy, and GNU Octave",
        ),
        "hardware": (
            "课程明确支持的低压控制对象、传感器、执行器、实时控制板与紧急断电装置",
            "a course-supported low-voltage plant, sensors, actuators, real-time controller, and emergency shutdown",
        ),
        "cost_class": "bench",
        "evidence": ("theory", "simulation"),
    },
    "robotics": {
        "software": (
            "ROS 2、Gazebo、RViz 2、Python 或 C++，以及固定版本的容器环境",
            "ROS 2, Gazebo, RViz 2, Python or C++, and a version-pinned container environment",
        ),
        "hardware": (
            "课程明确支持的机器人平台、传感器、低压电源、急停与安全测试区域",
            "a course-supported robot platform, sensors, low-voltage power, emergency stop, and safe test area",
        ),
        "cost_class": "specialized",
        "evidence": ("design", "code", "simulation"),
    },
    "rf-microwave-antennas": {
        "software": (
            "openEMS、scikit-rf、GNU Octave 或 Python 3，以及 KiCad",
            "openEMS, scikit-rf, GNU Octave or Python 3, and KiCad",
        ),
        "hardware": (
            "合规实验室中的矢量网络分析仪、校准件、屏蔽互连、衰减器及课程指定夹具/天线",
            "a vector network analyzer, calibration kit, shielded interconnects, attenuators, and course-specified fixture/antenna in a compliant lab",
        ),
        "cost_class": "specialized",
        "evidence": ("theory", "simulation", "design"),
    },
    "semiconductor-devices": {
        "software": (
            "DEVSIM、Python 3、Jupyter、NumPy 与 ngspice",
            "DEVSIM, Python 3, Jupyter, NumPy, and ngspice",
        ),
        "hardware": (
            "可运行器件数值模型并保存网格/偏置数据的计算机；不假设晶圆或探针台",
            "a computer that can run numerical device models and retain mesh/bias data; no wafer or probe station is assumed",
        ),
        "cost_class": "compute",
        "evidence": ("theory", "simulation"),
    },
    "microelectronics": {
        "software": (
            "ngspice、Qucs-S、KiCad、Python 3 与 Jupyter",
            "ngspice, Qucs-S, KiCad, Python 3, and Jupyter",
        ),
        "hardware": (
            "课程指定器件、限流低压电源、面包板或测试 PCB、数字万用表与示波器",
            "course-specified devices, a current-limited low-voltage supply, breadboard or test PCB, digital multimeter, and oscilloscope",
        ),
        "cost_class": "bench",
        "evidence": ("design", "simulation"),
    },
    "analog-ic": {
        "software": (
            "xschem、ngspice、KLayout、Magic，以及教程明确支持的开放 PDK",
            "xschem, ngspice, KLayout, Magic, and an open PDK explicitly supported by the tutorial",
        ),
        "hardware": (
            "可运行 PDK、角落仿真和版图检查的计算机；不假设流片或实体芯片",
            "a computer that can run the PDK, corner simulations, and layout checks; no tape-out or physical chip is assumed",
        ),
        "cost_class": "compute",
        "evidence": ("design", "simulation"),
    },
    "vlsi-ic": {
        "software": (
            "Yosys、OpenROAD、OpenSTA、Verilator、GTKWave 与 KLayout",
            "Yosys, OpenROAD, OpenSTA, Verilator, GTKWave, and KLayout",
        ),
        "hardware": (
            "具备足够内存和存储运行综合、布局布线及回归测试的计算机；不假设流片",
            "a computer with enough memory and storage for synthesis, place-and-route, and regressions; no tape-out is assumed",
        ),
        "cost_class": "compute",
        "evidence": ("design", "code", "simulation"),
    },
    "fabrication-mems": {
        "software": (
            "KLayout、gdsfactory、Python 3 与 Jupyter",
            "KLayout, gdsfactory, Python 3, and Jupyter",
        ),
        "hardware": (
            "机构批准的洁净室、工艺设备、计量设备与个人防护用品；不得以家庭采购替代",
            "institution-approved cleanroom, process tools, metrology, and personal protective equipment; do not substitute home purchases",
        ),
        "cost_class": "specialized",
        "evidence": ("design",),
    },
    "optics-photonics": {
        "software": (
            "MEEP、MPB、Python 3、Jupyter 与 ParaView",
            "MEEP, MPB, Python 3, Jupyter, and ParaView",
        ),
        "hardware": (
            "合规光学实验室中的课程指定光源、光学件、探测器、遮光与激光安全防护",
            "course-specified sources, optics, detectors, beam containment, and laser safety controls in a compliant optics lab",
        ),
        "cost_class": "specialized",
        "evidence": ("theory", "simulation"),
    },
    "power-electronics": {
        "software": (
            "Qucs-S、ngspice、Python 3、Jupyter 与 GNU Octave",
            "Qucs-S, ngspice, Python 3, Jupyter, and GNU Octave",
        ),
        "hardware": (
            "合规实验室中的隔离/限流电源、差分探头、电子负载、示波器及课程指定功率级",
            "isolated/current-limited power, differential probes, electronic load, oscilloscope, and course-specified power stage in a compliant lab",
        ),
        "cost_class": "specialized",
        "evidence": ("design", "simulation"),
    },
    "power-systems-machines": {
        "software": (
            "pandapower、OpenDSS、Python 3、Jupyter 与 GNU Octave",
            "pandapower, OpenDSS, Python 3, Jupyter, and GNU Octave",
        ),
        "hardware": (
            "机构监督的三相/电机教学平台、隔离与保护装置、测量接口及紧急断电",
            "an institution-supervised three-phase/machine trainer, isolation and protection, measurement interface, and emergency shutdown",
        ),
        "cost_class": "specialized",
        "evidence": ("theory", "simulation"),
    },
    "energy-storage-pv": {
        "software": (
            "pvlib-python、PyBaMM、Python 3、Jupyter 与 pandas",
            "pvlib-python, PyBaMM, Python 3, Jupyter, and pandas",
        ),
        "hardware": (
            "课程指定且受保护的低压光伏/电池教学模块、温度与电流传感器、电子负载及防护容器",
            "course-specified protected low-voltage PV/battery training modules, temperature/current sensors, electronic load, and protective enclosure",
        ),
        "cost_class": "specialized",
        "evidence": ("theory", "simulation"),
    },
    "pcb-eda": {
        "software": (
            "KiCad（原理图、PCB 与 ngspice）、gerbv 与 Git",
            "KiCad (schematic, PCB, and ngspice), gerbv, and Git",
        ),
        "hardware": (
            "仅在设计检查通过后使用课程指定元件、打样 PCB、限流电源、数字万用表与示波器",
            "course-specified components, prototype PCB, current-limited supply, digital multimeter, and oscilloscope only after design checks pass",
        ),
        "cost_class": "bench",
        "evidence": ("design",),
    },
    "sensors-instrumentation": {
        "software": (
            "Python 3、Jupyter、sigrok/PulseView、KiCad 与 SciPy",
            "Python 3, Jupyter, sigrok/PulseView, KiCad, and SciPy",
        ),
        "hardware": (
            "课程指定传感器、校准参考、低压数据采集接口、数字万用表、示波器与逻辑分析仪",
            "course-specified sensors, calibration reference, low-voltage data-acquisition interface, digital multimeter, oscilloscope, and logic analyzer",
        ),
        "cost_class": "bench",
        "evidence": ("design",),
    },
    "biomedical": {
        "software": (
            "Python 3、Jupyter、MNE-Python、NeuroKit2 与 WFDB",
            "Python 3, Jupyter, MNE-Python, NeuroKit2, and WFDB",
        ),
        "hardware": (
            "优先使用去标识公开数据或信号模拟器；人体连接仅使用机构批准的隔离设备并完成伦理与安全审查",
            "prefer de-identified public data or a signal simulator; connect to people only with institution-approved isolated equipment and completed ethics/safety review",
        ),
        "cost_class": "biomedical",
        "evidence": ("theory", "code"),
    },
    "capstone-practice": {
        "software": (
            "Git、Markdown、自动测试，以及与项目相符的 KiCad、FreeCAD、Python 或 HDL 工具链",
            "Git, Markdown, automated tests, and a project-appropriate KiCad, FreeCAD, Python, or HDL toolchain",
        ),
        "hardware": (
            "经需求和风险评审后确定的原型元件、限流电源、测量设备、安全防护与备件",
            "prototype components, current-limited power, measurement equipment, safety controls, and spares selected after requirements and risk review",
        ),
        "cost_class": "bench",
        "evidence": ("design", "code"),
    },
}


EVIDENCE_TEMPLATES = {
    "theory": (
        "理论推导档案：逐项列出假设、符号、推导、单位与边界条件，并用至少一种独立方法复核",
        "Theory dossier with explicit assumptions, notation, derivation, units, and boundary conditions, checked by at least one independent method",
    ),
    "simulation": (
        "仿真包：模型或网表、输入、求解器与版本、参数扫描脚本、基准对照、预期结果及一条重新运行命令",
        "Simulation package with model or netlist, inputs, solver and version, parameter-sweep script, benchmark comparison, expected results, and one rerun command",
    ),
    "code": (
        "代码仓库：固定依赖和工具链、最小运行命令、测试或波形/基准、预期输出与许可说明",
        "Code repository with pinned dependencies and toolchain, a minimal run command, tests or waveform/benchmark checks, expected output, and license notes",
    ),
    "experiment": (
        "实验包：原理图/装置设置、校准记录、原始数据、不确定度、安全检查、失败记录与从原始数据重建图表的步骤",
        "Experiment package with schematic/setup, calibration record, raw data, uncertainty, safety checks, failed runs, and steps to rebuild plots from raw data",
    ),
    "design": (
        "设计审查包：需求与约束、方案权衡、可编辑源文件、适用的 ERC/DRC/时序/稳定性检查、导出物与复现实验",
        "Design-review package with requirements and constraints, trade-offs, editable sources, applicable ERC/DRC/timing/stability checks, exports, and a reproduction test",
    ),
}


def _policy_for_url(url: str) -> dict[str, str]:
    host = urlsplit(url).hostname or ""
    host = host.lower().removeprefix("www.")
    path = urlsplit(url).path.lower()
    if host == "ocw.mit.edu":
        return {
            "access": "open",
            "license": "CC BY-NC-SA 4.0 for site materials; third-party exclusions may apply",
        }
    if host.endswith("nptel.ac.in"):
        return {"access": "open", "license": "NPTEL provider terms"}
    if host.endswith("coursera.org"):
        return {"access": "limited-free", "license": "Coursera Terms of Use"}
    if host.endswith("edx.org"):
        return {"access": "limited-free", "license": "edX Terms of Service"}
    if host.endswith("youtube.com") or host == "youtu.be":
        return {
            "access": "open",
            "license": "Creator copyright under YouTube Terms of Service",
        }
    if host.endswith("github.com") or host.endswith("gitlab.com"):
        return {
            "access": "open",
            "license": "Repository-specific license; inspect before reuse",
        }
    if "archive" in host or "/archive" in path:
        return {
            "access": "open",
            "license": "Original provider terms; archive host terms also apply",
        }
    return {
        "access": "open",
        "license": "Provider-specific terms; verify before reuse",
    }


def normalize_url(url: str) -> str:
    parsed = urlsplit(url.strip())
    scheme = parsed.scheme.lower()
    host = (parsed.hostname or "").lower()
    if parsed.port and not (
        (scheme == "https" and parsed.port == 443) or (scheme == "http" and parsed.port == 80)
    ):
        host = f"{host}:{parsed.port}"
    path = re.sub(r"/{2,}", "/", parsed.path) or "/"
    if path != "/":
        path = path.rstrip("/")
    return urlunsplit((scheme, host, path, parsed.query, ""))


def normalize_track_id(candidate_track: str, taxonomy_ids: set[str]) -> str:
    normalized = TRACK_ALIASES.get(candidate_track, candidate_track)
    if normalized not in taxonomy_ids:
        raise QualityError(
            f"candidate track {candidate_track!r} is not present in the canonical taxonomy"
        )
    return normalized


def load_taxonomy(value: Any) -> tuple[list[dict[str, Any]], list[Issue]]:
    issues: list[Issue] = []
    if not isinstance(value, dict):
        return [], [Issue("error", "taxonomy.type", "track taxonomy must be an object")]
    groups = value.get("groups")
    tracks = value.get("tracks")
    if not isinstance(groups, list) or not isinstance(tracks, list):
        return [], [
            Issue("error", "taxonomy.shape", "track taxonomy requires groups[] and tracks[]")
        ]
    group_ids: set[str] = set()
    for index, group in enumerate(groups):
        path = f"data/tracks.json:groups[{index}]"
        if not isinstance(group, dict):
            issues.append(Issue("error", "taxonomy.group.type", "group must be an object", path))
            continue
        group_id = group.get("id")
        if not isinstance(group_id, str) or not group_id:
            issues.append(Issue("error", "taxonomy.group.id", "group id is required", path))
        elif group_id in group_ids:
            issues.append(Issue("error", "taxonomy.group.duplicate", group_id, path))
        else:
            group_ids.add(group_id)
        for key in ("title_zh", "title_en"):
            if not isinstance(group.get(key), str) or not group[key].strip():
                issues.append(Issue("error", "taxonomy.group.translation", f"{key} is required", path))

    track_ids: set[str] = set()
    orders: set[int] = set()
    for index, track in enumerate(tracks):
        path = f"data/tracks.json:tracks[{index}]"
        if not isinstance(track, dict):
            issues.append(Issue("error", "taxonomy.track.type", "track must be an object", path))
            continue
        track_id = track.get("id")
        if not isinstance(track_id, str) or not track_id:
            issues.append(Issue("error", "taxonomy.track.id", "track id is required", path))
        elif track_id in track_ids:
            issues.append(Issue("error", "taxonomy.track.duplicate", track_id, path))
        else:
            track_ids.add(track_id)
        if track.get("group") not in group_ids:
            issues.append(
                Issue(
                    "error",
                    "taxonomy.track.group",
                    f"unknown group {track.get('group')!r}",
                    path,
                )
            )
        order = track.get("order")
        if not isinstance(order, int) or order < 1:
            issues.append(Issue("error", "taxonomy.track.order", "positive order required", path))
        elif order in orders:
            issues.append(Issue("error", "taxonomy.track.order_duplicate", str(order), path))
        else:
            orders.add(order)
        for key in ("title_zh", "title_en", "summary_zh", "summary_en"):
            if not isinstance(track.get(key), str) or not track[key].strip():
                issues.append(Issue("error", "taxonomy.track.translation", f"{key} is required", path))
        if not isinstance(track.get("prerequisites"), list):
            issues.append(
                Issue("error", "taxonomy.track.prerequisites", "prerequisites must be a list", path)
            )
    for index, track in enumerate(tracks):
        for prerequisite in track.get("prerequisites", []):
            if prerequisite not in track_ids:
                issues.append(
                    Issue(
                        "error",
                        "taxonomy.track.prerequisite",
                        f"unknown prerequisite {prerequisite!r}",
                        f"data/tracks.json:tracks[{index}]",
                    )
                )
    issues.extend(_track_cycle_issues(tracks, "taxonomy.track.cycle"))
    return tracks, issues


def validate_candidates(
    value: Any,
    *,
    minimum_courses: int = 125,
    minimum_tracks: int = 24,
    taxonomy_ids: set[str] | None = None,
) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(value, list):
        return [Issue("error", "candidate.type", "candidate catalogue must be a JSON array")]
    if len(value) < minimum_courses:
        issues.append(
            Issue(
                "error",
                "candidate.course_count",
                f"expected at least {minimum_courses} candidates, found {len(value)}",
                "data/course_candidates.json",
            )
        )
    ids: set[int] = set()
    urls: dict[str, int] = {}
    normalized_tracks: list[str] = []
    required = {
        "id",
        "title",
        "institution",
        "code",
        "url",
        "track",
        "role",
        "tier",
        "tier_note",
        "resources",
        "risk",
        "verified_at",
    }
    for index, candidate in enumerate(value):
        path = f"data/course_candidates.json:[{index}]"
        if not isinstance(candidate, dict):
            issues.append(Issue("error", "candidate.item_type", "candidate must be an object", path))
            continue
        missing = sorted(required - candidate.keys())
        if missing:
            issues.append(
                Issue("error", "candidate.required", f"missing: {', '.join(missing)}", path)
            )
            continue
        candidate_id = candidate.get("id")
        if not isinstance(candidate_id, int) or candidate_id < 1:
            issues.append(Issue("error", "candidate.id", "id must be a positive integer", path))
        elif candidate_id in ids:
            issues.append(Issue("error", "candidate.id_duplicate", str(candidate_id), path))
        else:
            ids.add(candidate_id)
        for key in ("title", "institution", "track", "tier_note", "risk", "verified_at"):
            if not isinstance(candidate.get(key), str) or not candidate[key].strip():
                issues.append(Issue("error", "candidate.text", f"{key} must be non-empty", path))
        if candidate.get("role") not in ROLES:
            issues.append(Issue("error", "candidate.role", str(candidate.get("role")), path))
        if candidate.get("tier") not in TIERS:
            issues.append(Issue("error", "candidate.tier", str(candidate.get("tier")), path))
        if candidate.get("level", "unspecified") not in LEVELS:
            issues.append(
                Issue("error", "candidate.level", str(candidate.get("level")), path)
            )
        practice_modality = candidate.get("practice_modality")
        if (
            practice_modality is not None
            and practice_modality not in PRACTICE_MODALITIES
        ):
            issues.append(
                Issue(
                    "error",
                    "candidate.practice_modality",
                    f"unsupported practice modality {practice_modality!r}",
                    path,
                )
            )
        recommended_background = candidate.get("recommended_background")
        if recommended_background is not None and (
            not isinstance(recommended_background, Mapping)
            or set(recommended_background) != {"zh", "en"}
            or any(
                not isinstance(recommended_background.get(language), str)
                or not recommended_background[language].strip()
                for language in ("zh", "en")
            )
        ):
            issues.append(
                Issue(
                    "error",
                    "candidate.recommended_background",
                    "recommended_background must contain non-empty zh and en text",
                    path,
                )
            )
        workload = candidate.get("workload")
        if workload is not None:
            if not isinstance(workload, dict) or not workload:
                issues.append(
                    Issue(
                        "error",
                        "candidate.workload",
                        "workload must be a non-empty object",
                        path,
                    )
                )
            elif set(workload) - {"weeks", "hours_per_week"}:
                issues.append(
                    Issue(
                        "error",
                        "candidate.workload",
                        "workload supports only weeks and hours_per_week",
                        path,
                    )
                )
            else:
                weeks = workload.get("weeks")
                if weeks is not None and (
                    not isinstance(weeks, int)
                    or isinstance(weeks, bool)
                    or not 1 <= weeks <= 104
                ):
                    issues.append(
                        Issue(
                            "error",
                            "candidate.workload.weeks",
                            "weeks must be an integer from 1 to 104",
                            path,
                        )
                    )
                hours = workload.get("hours_per_week")
                if hours is not None:
                    if not isinstance(hours, dict) or set(hours) != {"min", "max"}:
                        issues.append(
                            Issue(
                                "error",
                                "candidate.workload.hours",
                                "hours_per_week must contain min and max",
                                path,
                            )
                        )
                    else:
                        minimum = hours.get("min")
                        maximum = hours.get("max")
                        if (
                            not isinstance(minimum, (int, float))
                            or isinstance(minimum, bool)
                            or not isinstance(maximum, (int, float))
                            or isinstance(maximum, bool)
                            or minimum <= 0
                            or maximum < minimum
                            or maximum > 80
                        ):
                            issues.append(
                                Issue(
                                    "error",
                                    "candidate.workload.hours",
                                    "hours range must satisfy 0 < min <= max <= 80",
                                    path,
                                )
                            )
        primary = candidate.get("url")
        alternatives = candidate.get("alternate_urls", [])
        if not isinstance(alternatives, list):
            issues.append(
                Issue("error", "candidate.alternate_urls", "alternate_urls must be a list", path)
            )
            alternatives = []
        for url in [primary, *alternatives]:
            if not isinstance(url, str) or not url.startswith("https://"):
                issues.append(
                    Issue("error", "candidate.url", f"HTTPS URL required, found {url!r}", path)
                )
                continue
            normalized = normalize_url(url)
            if normalized in urls and urls[normalized] != candidate_id:
                issues.append(
                    Issue(
                        "warning",
                        "candidate.url_duplicate",
                        f"also used by candidate {urls[normalized]}: {normalized}",
                        path,
                    )
                )
            else:
                urls[normalized] = candidate_id
        coverage = candidate.get("resources")
        if not isinstance(coverage, dict) or set(coverage) != set(COVERAGE_KEYS):
            issues.append(
                Issue(
                    "error",
                    "candidate.coverage_shape",
                    f"resources must contain exactly {', '.join(COVERAGE_KEYS)}",
                    path,
                )
            )
        else:
            for key, score in coverage.items():
                if not isinstance(score, int) or isinstance(score, bool) or not 0 <= score <= 2:
                    issues.append(
                        Issue(
                            "error",
                            "candidate.coverage_score",
                            f"{key} must be an integer from 0 to 2",
                            path,
                        )
                    )
        try:
            date.fromisoformat(str(candidate.get("verified_at")))
        except ValueError:
            issues.append(
                Issue("error", "candidate.verified_at", "verified_at must be YYYY-MM-DD", path)
            )
        raw_track = candidate.get("track")
        if isinstance(raw_track, str):
            if taxonomy_ids is None:
                normalized_tracks.append(TRACK_ALIASES.get(raw_track, raw_track))
            else:
                try:
                    normalized_tracks.append(normalize_track_id(raw_track, taxonomy_ids))
                except QualityError as exc:
                    issues.append(Issue("error", "candidate.track", str(exc), path))
    for index, candidate in enumerate(value):
        if not isinstance(candidate, dict):
            continue
        path = f"data/course_candidates.json:[{index}]"
        candidate_id = candidate.get("id")
        prerequisite_ids = candidate.get("prerequisite_course_ids", [])
        if not isinstance(prerequisite_ids, list):
            issues.append(
                Issue(
                    "error",
                    "candidate.prerequisite_course_ids",
                    "prerequisite_course_ids must be a list",
                    path,
                )
            )
            continue
        if any(
            prerequisite_id in prerequisite_ids[:prerequisite_index]
            for prerequisite_index, prerequisite_id in enumerate(prerequisite_ids)
        ):
            issues.append(
                Issue(
                    "error",
                    "candidate.prerequisite_course_ids_duplicate",
                    "prerequisite_course_ids must be unique",
                    path,
                )
            )
        for prerequisite_id in prerequisite_ids:
            if (
                not isinstance(prerequisite_id, int)
                or isinstance(prerequisite_id, bool)
                or prerequisite_id < 1
            ):
                issues.append(
                    Issue(
                        "error",
                        "candidate.prerequisite_course_id",
                        f"positive integer required, found {prerequisite_id!r}",
                        path,
                    )
                )
            elif prerequisite_id == candidate_id:
                issues.append(
                    Issue(
                        "error",
                        "candidate.prerequisite_course_self",
                        "a course cannot require itself",
                        path,
                    )
                )
            elif prerequisite_id not in ids:
                issues.append(
                    Issue(
                        "error",
                        "candidate.prerequisite_course_missing",
                        f"unknown prerequisite course id {prerequisite_id}",
                        path,
                    )
                )
    distinct_tracks = len(set(normalized_tracks))
    issues.extend(_candidate_prerequisite_cycle_issues(value))
    if distinct_tracks < minimum_tracks:
        issues.append(
            Issue(
                "error",
                "candidate.track_count",
                f"expected at least {minimum_tracks} used tracks, found {distinct_tracks}",
                "data/course_candidates.json",
            )
        )
    return issues


def _canonical_track(track: Mapping[str, Any]) -> dict[str, Any]:
    title_zh = str(track["title_zh"])
    title_en = str(track["title_en"])
    return {
        "id": track["id"],
        "group": track["group"],
        "order": track["order"],
        "title": localized(title_zh, title_en),
        "summary": localized(str(track["summary_zh"]), str(track["summary_en"])),
        "outcomes": localized_list(
            [
                f"掌握{title_zh}的核心概念、模型与分析方法",
                "完成可复现、可检验的练习、实验或设计成果",
            ],
            [
                f"Explain the core concepts, models, and methods of {title_en}",
                "Produce reproducible exercises, experiments, or designs with explicit checks",
            ],
        ),
        "prerequisite_tracks": list(track.get("prerequisites", [])),
    }


def _course_summary(
    candidate: Mapping[str, Any], track: Mapping[str, Any]
) -> dict[str, str]:
    institution = str(candidate["institution"])
    title = str(candidate["title"])
    track_zh = str(track["title_zh"])
    track_en = str(track["title_en"])
    return localized(
        f"{institution} 提供的《{title}》，纳入{track_zh}路线；页面按资源完整度、实践条件和复核风险给出选课建议。",
        f"{title} from {institution}, placed in the {track_en} pathway with explicit resource coverage, practice constraints, and review notes.",
    )


def _course_prerequisites(
    candidate: Mapping[str, Any],
    track: Mapping[str, Any],
    track_by_id: Mapping[str, Any],
    candidate_by_id: Mapping[int, Mapping[str, Any]],
) -> dict[str, list[str]]:
    track_prerequisites = [
        track_by_id[track_id]
        for track_id in track.get("prerequisites", [])
        if track_id in track_by_id
    ]
    course_prerequisites = [
        candidate_by_id[course_id]
        for course_id in candidate.get("prerequisite_course_ids", [])
        if course_id in candidate_by_id
    ]
    recommended_background = candidate.get("recommended_background")
    recommended_zh = (
        [f"建议背景：{recommended_background['zh']}"]
        if isinstance(recommended_background, Mapping)
        else []
    )
    recommended_en = (
        [f"Recommended background: {recommended_background['en']}"]
        if isinstance(recommended_background, Mapping)
        else []
    )
    return localized_list(
        [
            *[f"建议先完成方向基础：{item['title_zh']}" for item in track_prerequisites],
            *recommended_zh,
            *[
                f"课程顺序要求：先完成《{item['title']}》（{item['institution']} {item['code']}）"
                for item in course_prerequisites
            ],
        ],
        [
            *[f"Recommended foundation: {item['title_en']}" for item in track_prerequisites],
            *recommended_en,
            *[
                f"Course-sequence requirement: complete {item['title']} "
                f"({item['institution']} {item['code']}) first"
                for item in course_prerequisites
            ],
        ],
    )


def _course_outcomes(
    candidate: Mapping[str, Any], track: Mapping[str, Any]
) -> dict[str, list[str]]:
    coverage = candidate["resources"]
    title_zh = str(track["title_zh"])
    title_en = str(track["title_en"])
    zh = [f"解释{title_zh}中的核心模型，并说明主要假设与适用边界"]
    en = [
        f"Explain the core models in {title_en}, including their assumptions and limits"
    ]
    if coverage["practice"] or coverage["exams"]:
        zh.append("独立完成代表性推导与题目，并用量纲、极限情形或数值结果交叉检查")
        en.append(
            "Solve representative derivations and problems, checking units, limiting cases, or numerical results"
        )
    if coverage["labs"] or coverage["code"]:
        zh.append("完成可复现实验或实现，保留原始数据、参数、版本和验证记录")
        en.append(
            "Complete a reproducible experiment or implementation with raw data, parameters, versions, and verification"
        )
    return localized_list(zh, en)


def _study_plan(candidate: Mapping[str, Any]) -> dict[str, Any]:
    coverage = candidate["resources"]
    role = str(candidate["role"])
    estimated_weeks = {
        "mainline": 10,
        "alternative": 8,
        "supplement": 5,
    }[role]
    hours_per_week = {
        "mainline": 8,
        "alternative": 6,
        "supplement": 4,
    }[role]
    if coverage["labs"] or coverage["code"]:
        estimated_weeks += 2
    if coverage["labs"] == 2 or coverage["code"] == 2:
        hours_per_week += 2
    if coverage["practice"] == 2 or coverage["exams"] == 2:
        estimated_weeks += 1
        hours_per_week += 1
    published = candidate.get("workload", {})
    published_weeks = published.get("weeks") if isinstance(published, Mapping) else None
    published_hours = (
        published.get("hours_per_week") if isinstance(published, Mapping) else None
    )
    if isinstance(published_weeks, int):
        estimated_weeks = published_weeks
    if isinstance(published_hours, Mapping):
        minimum = float(published_hours["min"])
        maximum = float(published_hours["max"])
        midpoint = round((minimum + maximum) / 2, 1)
        hours_per_week = int(midpoint) if midpoint.is_integer() else midpoint
    if isinstance(published_weeks, int) and isinstance(published_hours, Mapping):
        minimum = published_hours["min"]
        maximum = published_hours["max"]
        if minimum == maximum:
            note = localized(
                f"提供方公布 {published_weeks} 周、每周 {minimum} 小时。先试学两周并记录授课、练习、实验和复盘时间，若实际偏差超过 25%，据实调整剩余计划。",
                f"The provider publishes {published_weeks} weeks at {minimum} hours per week. Pilot two weeks while logging instruction, practice, lab, and review time, then adjust the remaining plan when actual effort differs by more than 25%.",
            )
        else:
            note = localized(
                f"提供方公布 {published_weeks} 周、每周 {minimum}–{maximum} 小时；上方每周工时采用区间中点便于规划。先试学两周并记录授课、练习、实验和复盘时间，若实际偏差超过 25%，据实调整剩余计划。",
                f"The provider publishes {published_weeks} weeks at {minimum}–{maximum} hours per week; the midpoint is shown above for planning. Pilot two weeks while logging instruction, practice, lab, and review time, then adjust the remaining plan when actual effort differs by more than 25%.",
            )
    elif isinstance(published_weeks, int):
        note = localized(
            f"提供方公布 {published_weeks} 周；上方每周工时是维护者规划估计，依据课程角色与公开练习、实验密度生成，不是提供方承诺。先试学两周，若实际偏差超过 25%，据实调整。",
            f"The provider publishes {published_weeks} weeks; the weekly effort above is a maintainer planning estimate derived from course role and public practice/lab density, not a provider promise. Pilot two weeks and adjust when actual effort differs by more than 25%.",
        )
    else:
        note = localized(
            "这是维护者规划估计，依据课程角色与公开练习、实验密度生成，不是提供方工时承诺。先试学两周，分别记录授课、练习、实验和复盘时间；若实际偏差超过 25%，据实调整剩余计划。",
            "This maintainer planning estimate is derived from course role and the density of public practice and labs; it is not a provider workload promise. Pilot two weeks while logging instruction, practice, lab, and review time, then adjust the remaining plan when actual effort differs by more than 25%.",
        )
    return {
        "estimated_weeks": estimated_weeks,
        "hours_per_week": hours_per_week,
        "note": note,
    }


def _practice_modality(
    candidate: Mapping[str, Any], canonical_track: str
) -> str:
    explicit = candidate.get("practice_modality")
    if explicit in PRACTICE_MODALITIES:
        return str(explicit)
    coverage = candidate["resources"]
    profile = TRACK_TOOLING[canonical_track]
    if profile["cost_class"] == "compute":
        return "simulation-only"
    if coverage["labs"]:
        return (
            "supervised"
            if canonical_track in SUPERVISED_TRACKS
            else "low-energy"
        )
    if coverage["code"]:
        return "simulation-only"
    return "standard"


def _tooling(
    candidate: Mapping[str, Any], canonical_track: str
) -> dict[str, Any]:
    coverage = candidate["resources"]
    if canonical_track not in TRACK_TOOLING:
        raise QualityError(
            f"canonical track {canonical_track!r} has no tooling profile"
        )
    profile = TRACK_TOOLING[canonical_track]
    software_zh, software_en = profile["software"]
    hardware_zh, hardware_en = profile["hardware"]
    software = [
        f"维护者建议的开源/免费验证路径：{software_zh}",
    ]
    software_en_items = [
        f"Maintainer-suggested open-source/free verification path: {software_en}",
    ]
    if coverage["code"]:
        software.append(
            "资源清单包含公开代码覆盖；复现时固定解释器、依赖、工具链、数据集和 PDK（如适用）版本"
        )
        software_en_items.append(
            "The resource inventory lists public code coverage; pin interpreter, dependencies, toolchain, datasets, and PDK versions where applicable"
        )
    else:
        software.append(
            "资源清单未标注公开代码覆盖；上述工具仅用于维护者建议的独立验证，不代表提供方要求"
        )
        software_en_items.append(
            "The resource inventory does not list public code coverage; the tools above are only a maintainer-suggested independent check, not a provider requirement"
        )

    cost_class = profile["cost_class"]
    practice_modality = _practice_modality(candidate, canonical_track)
    if practice_modality == "simulation-only" and cost_class != "compute":
        lab_context_zh = (
            "资源清单包含实验覆盖；本课程的维护者路径明确将其限定为计算或仿真实验。"
            if coverage["labs"]
            else "资源清单未标注公开实体实验覆盖；维护者路径限定为计算或仿真。"
        )
        lab_context_en = (
            "The resource inventory lists lab coverage, but this course's maintainer path explicitly limits it to computational or simulation work."
            if coverage["labs"]
            else "The resource inventory does not list public physical-lab coverage; the maintainer path is limited to computation or simulation."
        )
        hardware = [
            f"{lab_context_zh}只假设一台能运行上述软件并保存结果的通用计算机；不采购或连接{hardware_zh}",
        ]
        hardware_en_items = [
            f"{lab_context_en} It assumes only a general-purpose computer able to run the software above and retain results; do not purchase or connect {hardware_en}",
        ]
        cost_note = localized(
            "当前维护者路径只使用计算与仿真，不设专用硬件采购；建议软件优先采用开源/免费工具。这不是提供方要求，平台访问、商业软件或云算力费用仍随提供方、地区与方案而变。",
            "The current maintainer path uses computation and simulation only, with no dedicated hardware purchase, and prefers open-source/free tools. This is not a provider requirement; platform, commercial-software, or cloud-compute costs still vary by provider, region, and plan.",
        )
    elif cost_class == "compute":
        lab_context_zh = (
            "资源清单包含实验覆盖；维护者路径将其按计算/仿真实验处理，除非提供方实验手册另有明确说明。"
            if coverage["labs"]
            else "资源清单未标注公开实体实验覆盖；维护者路径默认采用计算/仿真。"
        )
        lab_context_en = (
            "The resource inventory lists lab coverage; the maintainer path treats it as computational/simulation work unless the provider lab manual explicitly says otherwise."
            if coverage["labs"]
            else "The resource inventory does not list public physical-lab coverage; the maintainer path defaults to computation/simulation."
        )
        hardware = [
            f"{lab_context_zh}只假设{hardware_zh}。提供方如另列设备或算力要求，以其课程页面为准",
        ]
        hardware_en_items = [
            f"{lab_context_en} It assumes only {hardware_en}. If the provider lists different equipment or compute requirements, follow its course page",
        ]
        cost_note = localized(
            "建议软件栈可开源或免费使用；这只是维护者规划，不是提供方要求。商业许可证、云计算、存储和机构资源如被提供方指定，其费用随方案、地区与机构而变，本文不设固定价格。",
            "The suggested software stack is available open source or free; this is maintainer planning, not a provider requirement. If the provider specifies commercial licenses, cloud compute, storage, or institutional resources, costs vary by plan, region, and institution, so no fixed price is asserted here.",
        )
    elif cost_class == "biomedical":
        if coverage["labs"]:
            hardware = [
                "资源清单包含实验覆盖；维护者路径仍优先使用去标识公开数据或信号模拟器。任何人体连接只能在合规机构中使用获批隔离设备，并先完成伦理与安全审查；仅在提供方实验手册明确要求后核对规格、许可与安全条件",
            ]
            hardware_en_items = [
                "The resource inventory lists lab coverage, but the maintainer path still prioritizes de-identified public data or a signal simulator. Any connection to a person must occur only in a compliant institution with approved isolated equipment and completed ethics and safety review; verify ratings, authorization, and safety conditions only when the provider lab manual explicitly requires it",
            ]
        else:
            hardware = [
                "资源清单未标注公开人体实验覆盖；默认仅使用去标识公开数据或信号模拟器，不采购或自行连接人体设备。任何人体测量只能在合规机构中使用获批隔离设备，并先完成伦理与安全审查；如自行扩展，先核对提供方范围并重新评估安全",
            ]
            hardware_en_items = [
                "The resource inventory does not list public human-subject lab coverage; default to de-identified public data or a signal simulator, with no equipment purchase or independent connection to a person. Any human measurement must occur only in a compliant institution with approved isolated equipment and completed ethics and safety review; before extending the course, verify provider scope and reassess safety",
            ]
        cost_note = localized(
            "软件与去标识数据路径优先采用开源/免费资源；这不是提供方设备要求。隔离设备、伦理审批、数据访问与机构监督不可用家庭采购替代，具体费用随提供方、地区和机构而变。",
            "Prefer open-source/free software and de-identified data; this is not a provider equipment requirement. Home purchases cannot substitute for isolation, ethics approval, data access, or institutional supervision, and any costs vary by provider, region, and institution.",
        )
    elif coverage["labs"]:
        facility_prefix_zh = (
            "资源清单包含实验覆盖；只在合规机构内借用或共享"
            if cost_class == "specialized"
            else "资源清单包含实验覆盖；优先借用或共享"
        )
        facility_prefix_en = (
            "The resource inventory lists lab coverage; use compliant institutional access to the following borrowed or shared equipment:"
            if cost_class == "specialized"
            else "The resource inventory lists lab coverage; prefer borrowing or sharing the following equipment:"
        )
        hardware = [
            f"{facility_prefix_zh}{hardware_zh}。仅在提供方实验手册明确要求后核对规格、许可与安全条件",
        ]
        hardware_en_items = [
            f"{facility_prefix_en} {hardware_en}. Verify ratings, authorization, and safety conditions only after the provider lab manual explicitly calls for them",
        ]
        if cost_class == "specialized":
            cost_note = localized(
                "仿真软件路径优先采用开源/免费工具；这不是提供方设备要求。专用仪器或场地应通过合规机构共享，不建议个人采购；访问、耗材和许可费用随提供方、地区与机构而变。",
                "Prefer open-source/free simulation tools; this is not a provider equipment requirement. Access specialized instruments or facilities through a compliant institution rather than personal purchase; access, consumable, and license costs vary by provider, region, and institution.",
            )
        else:
            cost_note = localized(
                "建议软件栈可开源或免费使用；这不是提供方要求或物料清单。开发板、元件、打样和仪器的实际清单与费用以提供方实验手册、地区和当地可得性为准，采购前优先借用、共享或仿真。",
                "The suggested software stack is available open source or free; this is not a provider requirement or bill of materials. The actual boards, components, fabrication, and instruments—and their costs—depend on the provider lab manual, region, and local availability; prefer simulation, borrowing, or sharing before purchase.",
            )
    else:
        hardware = [
            f"资源清单未标注公开实验覆盖；默认只做仿真，不采购{hardware_zh}。如自行扩展，先核对提供方范围并重新评估安全",
        ]
        hardware_en_items = [
            f"The resource inventory does not list public lab coverage; default to simulation and do not purchase {hardware_en}. If extending the course independently, first verify provider scope and reassess safety",
        ]
        cost_note = localized(
            "当前维护者路径不设专用硬件采购，建议软件优先采用开源/免费工具；这不是提供方要求。若提供方另列商业软件、元件、设备或机构访问，费用随提供方、地区和机构而变。",
            "The current maintainer path assumes no dedicated hardware purchase and prefers open-source/free software; this is not a provider requirement. If the provider separately lists commercial software, components, equipment, or institutional access, costs vary by provider, region, and institution.",
        )
    return {
        "software": localized_list(software, software_en_items),
        "hardware": localized_list(hardware, hardware_en_items),
        "cost_note": cost_note,
    }


def _safety(candidate: Mapping[str, Any], canonical_track: str) -> dict[str, Any]:
    coverage = candidate["resources"]
    practice_modality = _practice_modality(candidate, canonical_track)
    if practice_modality == "simulation-only":
        level = "simulation-only"
        zh = "默认实践范围仅限软件、计算或仿真；不得因资源清单中的“实验”标签自行连接实体设备，任何硬件扩展都必须重新核对提供方范围并进行风险评估。"
        en = (
            "The default practice scope is software, computation, or simulation only; a lab label in the resource inventory does not authorize connecting physical equipment, and any hardware extension requires provider-scope verification and a new risk assessment."
        )
    elif practice_modality == "supervised":
        level = "supervised"
        zh = (
            "实体实践可能涉及高能量、强场、射频、激光、化学品或加工设备；只能在合规场所由合格人员监督。"
        )
        en = (
            "Physical work may involve high energy, strong fields, RF, lasers, chemicals, or fabrication equipment; use a compliant facility with qualified supervision."
        )
    elif practice_modality == "low-energy":
        level = "low-energy"
        zh = (
            "仅开展隔离、限流、低能量实验；通电前检查额定值、接地、短路风险和紧急断电方式。"
        )
        en = (
            "Keep work isolated, current-limited, and low energy; verify ratings, grounding, short-circuit risk, and emergency shutdown before power-up."
        )
    else:
        level = "standard"
        zh = "课程记录未要求实体实验；遵守一般用电、人体工学、数据和设备使用规范。"
        en = (
            "No physical lab is recorded; follow ordinary electrical, ergonomic, data, and equipment-use precautions."
        )
    return {"level": level, "note": localized(zh, en)}


def _completion_evidence(
    candidate: Mapping[str, Any], canonical_track: str
) -> dict[str, list[str]]:
    coverage = candidate["resources"]
    if canonical_track not in TRACK_TOOLING:
        raise QualityError(
            f"canonical track {canonical_track!r} has no evidence profile"
        )
    evidence_modes = list(TRACK_TOOLING[canonical_track]["evidence"])
    if coverage["code"] and "code" not in evidence_modes:
        evidence_modes.append("code")
    if coverage["labs"]:
        modality = _practice_modality(candidate, canonical_track)
        if modality in {"low-energy", "supervised"}:
            if "experiment" not in evidence_modes:
                evidence_modes.append("experiment")
        elif "simulation" not in evidence_modes:
            evidence_modes.append("simulation")
    zh = [
        "按周学习日志：投入时间、问题、错误订正、决策、下一步，并链接本周可复现产物",
    ]
    en = [
        "Weekly learning log with time, questions, corrected errors, decisions, next steps, and links to that week's reproducible artifacts",
    ]
    for mode in evidence_modes:
        template_zh, template_en = EVIDENCE_TEMPLATES[mode]
        zh.append(template_zh)
        en.append(template_en)
    return localized_list(zh, en)


def _resource_from_url(
    url: str, *, resource_id: str, verified_at: str, alternate: bool
) -> dict[str, Any]:
    policy = _policy_for_url(url)
    archived = "archive" in (urlsplit(url).hostname or "").lower() or "/archive" in urlsplit(
        url
    ).path.lower()
    title = (
        localized("备用课程入口", "Alternate course entry")
        if alternate
        else localized("课程主页", "Course home")
    )
    return {
        "id": resource_id,
        "kind": "course",
        "title": title,
        "url": normalize_url(url),
        "access": policy["access"],
        "license": policy["license"],
        "status": "archived" if archived else "available",
        "last_verified": verified_at,
        "note": localized(
            "访问条件与许可按提供方当前页面记录；转载或改编前应再次核对。",
            "Access and licensing follow the provider page; re-check before redistribution or adaptation.",
        ),
    }


def resource_from_manifest(record: Mapping[str, Any]) -> dict[str, Any]:
    url = normalize_url(str(record["url"]))
    kind = str(record["kind"])
    raw_title = record.get("title")
    if isinstance(raw_title, Mapping):
        title = localized(str(raw_title.get("zh", "")), str(raw_title.get("en", "")))
    else:
        title_text = str(raw_title).strip()
        title = localized(title_text, title_text)
    policy = _policy_for_url(url)
    identifier = f"{slugify(kind)}-{hashlib.sha256(url.encode('utf-8')).hexdigest()[:10]}"
    return {
        "id": identifier,
        "kind": kind,
        "title": title,
        "url": url,
        "access": str(record["access"]),
        "license": str(record.get("license") or policy["license"]),
        "status": str(record["status"]),
        "last_verified": str(record["last_verified"]),
        "note": localized(
            "资源由独立证据清单核对；许可按提供方或仓库记录，权利不明确时不得转载。",
            "Checked through the evidence manifest; licensing follows the provider or repository, and unclear rights prohibit redistribution.",
        ),
    }


def validate_resource_manifest(
    value: Any,
    *,
    candidate_ids: set[int],
    source: str = "data/course_resources.json",
) -> tuple[list[Mapping[str, Any]], list[Issue]]:
    if isinstance(value, Mapping):
        records = value.get("resources")
    else:
        records = value
    if not isinstance(records, list):
        return [], [
            Issue("error", "resource_manifest.shape", "manifest must be an array or contain resources[]", source)
        ]
    issues: list[Issue] = []
    valid: list[Mapping[str, Any]] = []
    required = {"course_id", "kind", "title", "url", "access", "status", "last_verified"}
    seen: set[tuple[int, str]] = set()
    for index, record in enumerate(records):
        path = f"{source}:[{index}]"
        if not isinstance(record, Mapping):
            issues.append(Issue("error", "resource_manifest.item", "record must be an object", path))
            continue
        missing = required - record.keys()
        if missing:
            issues.append(
                Issue(
                    "error",
                    "resource_manifest.required",
                    f"missing: {', '.join(sorted(missing))}",
                    path,
                )
            )
            continue
        course_id = record.get("course_id")
        if course_id not in candidate_ids:
            issues.append(
                Issue(
                    "error",
                    "resource_manifest.course",
                    f"unknown course_id {course_id!r}",
                    path,
                )
            )
        if record.get("kind") not in HIGH_VALUE_RESOURCE_KINDS | {"community", "other"}:
            issues.append(
                Issue(
                    "error",
                    "resource_manifest.kind",
                    f"unsupported kind {record.get('kind')!r}",
                    path,
                )
            )
        if record.get("access") not in RESOURCE_ACCESS:
            issues.append(
                Issue(
                    "error",
                    "resource_manifest.access",
                    f"unsupported access {record.get('access')!r}",
                    path,
                )
            )
        if record.get("status") not in RESOURCE_STATUSES:
            issues.append(
                Issue(
                    "error",
                    "resource_manifest.status",
                    f"unsupported status {record.get('status')!r}",
                    path,
                )
            )
        url = record.get("url")
        if not isinstance(url, str) or not url.startswith("https://"):
            issues.append(Issue("error", "resource_manifest.url", "HTTPS URL required", path))
        elif isinstance(course_id, int):
            key = (course_id, normalize_url(url))
            if key in seen:
                issues.append(
                    Issue("error", "resource_manifest.duplicate", f"duplicate URL {url}", path)
                )
            seen.add(key)
        if parse_iso_date(record.get("last_verified")) is None:
            issues.append(
                Issue("error", "resource_manifest.date", "last_verified must be YYYY-MM-DD", path)
            )
        if not any(issue.path == path and issue.severity == "error" for issue in issues):
            valid.append(record)
    return valid, issues


def _canonical_course(
    candidate: Mapping[str, Any],
    *,
    canonical_track: str,
    taxonomy_track: Mapping[str, Any],
    taxonomy_by_id: Mapping[str, Any],
    candidate_by_id: Mapping[int, Mapping[str, Any]],
) -> dict[str, Any]:
    source_id = int(candidate["id"])
    course_slug = slugify(
        str(candidate.get("code") or candidate["title"]), fallback=f"course-{source_id:03d}"
    )
    resources = [
        _resource_from_url(
            str(candidate["url"]),
            resource_id="primary",
            verified_at=str(candidate["verified_at"]),
            alternate=False,
        )
    ]
    for index, url in enumerate(candidate.get("alternate_urls", []), start=1):
        resources.append(
            _resource_from_url(
                str(url),
                resource_id=f"alternate-{index}",
                verified_at=str(candidate["verified_at"]),
                alternate=True,
            )
        )
    tier_zh, tier_en = TIER_TEXT[str(candidate["tier"])]
    role_zh, role_en = ROLE_TEXT[str(candidate["role"])]
    tier_note = str(candidate["tier_note"]).strip()
    selection_suffix = "" if tier_note == candidate["tier"] else f"（审阅记录：{tier_note}）"
    selection_suffix_en = "" if tier_note == candidate["tier"] else f" Review note: {tier_note}"
    risk = str(candidate["risk"]).strip()
    return {
        "id": f"course-{source_id:03d}",
        "source_id": source_id,
        "slug": f"{source_id:03d}-{course_slug}",
        "track": canonical_track,
        "title": localized(str(candidate["title"]), str(candidate["title"])),
        "summary": _course_summary(candidate, taxonomy_track),
        "institution": str(candidate["institution"]).strip(),
        "course_code": str(candidate.get("code", "")).strip(),
        "role": candidate["role"],
        "tier": candidate["tier"],
        "level": str(candidate.get("level", "unspecified")),
        "languages": ["en"],
        "study_plan": _study_plan(candidate),
        "tooling": _tooling(candidate, canonical_track),
        "safety": _safety(candidate, canonical_track),
        "prerequisite_course_ids": list(candidate.get("prerequisite_course_ids", [])),
        "prerequisites": _course_prerequisites(
            candidate,
            taxonomy_track,
            taxonomy_by_id,
            candidate_by_id,
        ),
        "outcomes": _course_outcomes(candidate, taxonomy_track),
        "completion_evidence": _completion_evidence(candidate, canonical_track),
        "selection_note": localized(
            f"{role_zh}课程，{tier_zh}{selection_suffix}",
            f"{role_en} course. {tier_en}{selection_suffix_en}",
        ),
        "review_note": localized(f"复核注意：{risk}", risk),
        "resource_coverage": {key: int(candidate["resources"][key]) for key in COVERAGE_KEYS},
        "resources": resources,
        "projects": [],
        "last_reviewed": str(candidate["verified_at"]),
    }


def _deep_overlay(base: Any, overlay: Any) -> Any:
    if isinstance(base, dict) and isinstance(overlay, dict):
        merged = copy.deepcopy(base)
        for key, value in overlay.items():
            if key in merged:
                merged[key] = _deep_overlay(merged[key], value)
        return merged
    return copy.deepcopy(overlay)


def _merge_resources(
    generated: Sequence[Mapping[str, Any]],
    existing: Sequence[Mapping[str, Any]],
    *,
    authoritative_urls: set[str] | None = None,
) -> list[dict[str, Any]]:
    authoritative_urls = authoritative_urls or set()
    status_priority = {
        "available": 0,
        "archived": 1,
        "degraded": 2,
        "review-needed": 3,
        "unavailable": 4,
    }
    by_url = {
        normalize_url(str(resource.get("url", ""))): resource
        for resource in existing
        if isinstance(resource, Mapping) and resource.get("url")
    }
    generated_urls: set[str] = set()
    output: list[dict[str, Any]] = []
    for resource in generated:
        key = normalize_url(str(resource["url"]))
        generated_urls.add(key)
        if key in by_url:
            existing_resource = by_url[key]
            merged = _deep_overlay(resource, existing_resource)
            if key in authoritative_urls:
                # Fresh manifest evidence is authoritative for metadata. A
                # conservative human status may remain only when it is worse
                # than the new observation; an old "available" must never mask
                # a newly observed review-needed/degraded/unavailable state.
                existing_status = str(existing_resource.get("status", ""))
                generated_status = str(resource.get("status", ""))
                for field, value in resource.items():
                    merged[field] = copy.deepcopy(value)
                if status_priority.get(existing_status, -1) > status_priority.get(
                    generated_status, -1
                ):
                    merged["status"] = existing_status
            output.append(merged)
        else:
            output.append(copy.deepcopy(dict(resource)))
    for resource in existing:
        if not isinstance(resource, Mapping) or not resource.get("url"):
            continue
        key = normalize_url(str(resource["url"]))
        resource_id = str(resource.get("id", ""))
        if (
            key not in generated_urls
            and resource_id != "primary"
            and not resource_id.startswith("alternate-")
            and not GENERATED_RESOURCE_ID_RE.fullmatch(resource_id)
        ):
            output.append(copy.deepcopy(dict(resource)))
    return output


def compile_catalogue(
    candidates: Sequence[Mapping[str, Any]],
    taxonomy_tracks: Sequence[Mapping[str, Any]],
    existing: Mapping[str, Any] | None = None,
    resource_records: Sequence[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    taxonomy_by_id = {str(track["id"]): track for track in taxonomy_tracks}
    taxonomy_ids = set(taxonomy_by_id)
    existing = existing or {}
    existing_tracks = {
        track.get("id"): track
        for track in existing.get("tracks", [])
        if isinstance(track, Mapping) and track.get("id")
    }
    tracks: list[dict[str, Any]] = []
    for taxonomy_track in sorted(taxonomy_tracks, key=lambda item: (item["order"], item["id"])):
        generated = _canonical_track(taxonomy_track)
        merged = _deep_overlay(generated, existing_tracks.get(generated["id"], {}))
        # Taxonomy semantics are authoritative.
        for key in ("id", "group", "order", "prerequisite_tracks"):
            merged[key] = copy.deepcopy(generated[key])
        tracks.append(merged)

    existing_courses = {
        course.get("source_id"): course
        for course in existing.get("courses", [])
        if isinstance(course, Mapping) and isinstance(course.get("source_id"), int)
    }
    resources_by_course: dict[int, list[Mapping[str, Any]]] = defaultdict(list)
    for record in resource_records:
        if isinstance(record.get("course_id"), int):
            resources_by_course[int(record["course_id"])].append(record)
    candidate_by_id = {
        int(candidate["id"]): candidate
        for candidate in candidates
        if isinstance(candidate, Mapping) and isinstance(candidate.get("id"), int)
    }
    courses: list[dict[str, Any]] = []
    for candidate in sorted(candidates, key=lambda item: int(item["id"])):
        canonical_track = normalize_track_id(str(candidate["track"]), taxonomy_ids)
        generated = _canonical_course(
            candidate,
            canonical_track=canonical_track,
            taxonomy_track=taxonomy_by_id[canonical_track],
            taxonomy_by_id=taxonomy_by_id,
            candidate_by_id=candidate_by_id,
        )
        candidate_resource_records = sorted(
            resources_by_course.get(int(candidate["id"]), []),
            key=lambda item: (
                str(item.get("kind")),
                normalize_url(str(item.get("url", ""))),
            ),
        )
        manifest_by_url = {
            normalize_url(str(record["url"])): record
            for record in candidate_resource_records
        }
        authoritative_urls: set[str] = set()
        for index, generated_resource in enumerate(generated["resources"]):
            key = normalize_url(str(generated_resource["url"]))
            record = manifest_by_url.get(key)
            if record is None:
                continue
            manifested = resource_from_manifest(record)
            # Candidate identity remains authoritative for primary/alternate
            # entries. The evidence manifest refreshes only current access and
            # verification metadata; it must not rename a corrected candidate
            # from an older crawl title.
            refreshed = copy.deepcopy(generated_resource)
            for field in (
                "access",
                "license",
                "status",
                "last_verified",
                "note",
            ):
                refreshed[field] = copy.deepcopy(manifested[field])
            generated["resources"][index] = refreshed
            authoritative_urls.add(key)
        known_urls = {normalize_url(resource["url"]) for resource in generated["resources"]}
        enriched = []
        for record in candidate_resource_records:
            resource = resource_from_manifest(record)
            if resource["url"] not in known_urls:
                source_url = normalize_url(str(record.get("source_url", "")))
                if resource["status"] == "unavailable":
                    # Keep confirmed failures in the evidence manifest, but do
                    # not turn a known-dead supplemental URL into learner-facing
                    # navigation.
                    continue
                if (
                    resource["kind"] == "course"
                    and resource["status"] == "review-needed"
                    and source_url == resource["url"]
                ):
                    # A failed seed that is no longer a candidate primary or
                    # alternate is superseded evidence, not a useful public
                    # learning link. Keep it in the crawl manifest for audit,
                    # but do not expose it in the learner-facing catalogue.
                    continue
                enriched.append(resource)
                known_urls.add(resource["url"])
                authoritative_urls.add(resource["url"])
        generated["resources"].extend(enriched)
        existing_course = existing_courses.get(int(candidate["id"]), {})
        merged = _deep_overlay(generated, existing_course)
        # Research evidence is authoritative; human enrichment remains everywhere else.
        for key in (
            "id",
            "source_id",
            "slug",
            "track",
            "title",
            "institution",
            "course_code",
            "role",
            "tier",
            "level",
            "study_plan",
            "tooling",
            "safety",
            "prerequisite_course_ids",
            "prerequisites",
            "outcomes",
            "completion_evidence",
            "selection_note",
            "resource_coverage",
            "last_reviewed",
        ):
            merged[key] = copy.deepcopy(generated[key])
        merged["resources"] = _merge_resources(
            generated["resources"],
            existing_course.get("resources", []),
            authoritative_urls=authoritative_urls,
        )
        courses.append(merged)
    updated_dates = [str(candidate["verified_at"]) for candidate in candidates]
    updated_at = max(updated_dates) if updated_dates else date.today().isoformat()
    return {
        "schema_version": SCHEMA_VERSION,
        "updated_at": updated_at,
        "tracks": tracks,
        "courses": courses,
    }


def _track_cycle_issues(
    tracks: Sequence[Mapping[str, Any]], code: str = "track.cycle"
) -> list[Issue]:
    graph = {
        str(track.get("id")): list(
            track.get("prerequisite_tracks", track.get("prerequisites", []))
        )
        for track in tracks
        if track.get("id")
    }
    visiting: set[str] = set()
    visited: set[str] = set()
    stack: list[str] = []
    issues: list[Issue] = []

    def visit(node: str) -> None:
        if node in visited:
            return
        if node in visiting:
            start = stack.index(node)
            cycle = stack[start:] + [node]
            issues.append(Issue("error", code, " -> ".join(cycle)))
            return
        visiting.add(node)
        stack.append(node)
        for dependency in graph.get(node, []):
            if dependency in graph:
                visit(dependency)
        stack.pop()
        visiting.remove(node)
        visited.add(node)

    for track_id in graph:
        visit(track_id)
    return issues


def _candidate_prerequisite_cycle_issues(
    candidates: Sequence[Mapping[str, Any]],
) -> list[Issue]:
    graph = {
        int(candidate["id"]): [
            prerequisite
            for prerequisite in candidate.get("prerequisite_course_ids", [])
            if isinstance(prerequisite, int) and not isinstance(prerequisite, bool)
        ]
        for candidate in candidates
        if isinstance(candidate, Mapping)
        and isinstance(candidate.get("id"), int)
        and not isinstance(candidate.get("id"), bool)
    }
    visiting: set[int] = set()
    visited: set[int] = set()
    stack: list[int] = []
    issues: list[Issue] = []

    def visit(node: int) -> None:
        if node in visited:
            return
        if node in visiting:
            start = stack.index(node)
            cycle = stack[start:] + [node]
            issues.append(
                Issue(
                    "error",
                    "candidate.prerequisite_course_cycle",
                    " -> ".join(str(course_id) for course_id in cycle),
                    "data/course_candidates.json",
                )
            )
            return
        visiting.add(node)
        stack.append(node)
        for dependency in graph.get(node, []):
            if dependency in graph:
                visit(dependency)
        stack.pop()
        visiting.remove(node)
        visited.add(node)

    for course_id in graph:
        visit(course_id)
    return list(dict.fromkeys(issues))


def catalogue_statistics(catalogue: Mapping[str, Any]) -> dict[str, Any]:
    courses = catalogue.get("courses", [])
    tracks = catalogue.get("tracks", [])
    used = Counter(course.get("track") for course in courses)
    resource_total = sum(len(course.get("resources", [])) for course in courses)
    complete_resources = sum(
        1
        for course in courses
        for resource in course.get("resources", [])
        if all(
            resource.get(key)
            for key in ("last_verified", "access", "license", "status")
        )
    )
    high_value_urls = {
        normalize_url(str(resource["url"]))
        for course in courses
        for resource in course.get("resources", [])
        if resource.get("kind") in HIGH_VALUE_RESOURCE_KINDS
        and resource.get("status") in {"available", "degraded", "archived"}
        and resource.get("url")
    }
    project_courses = sum(bool(course.get("projects")) for course in courses)
    return {
        "courses": len(courses),
        "tracks_defined": len(tracks),
        "tracks_used": len(used),
        "courses_by_track": dict(sorted(used.items())),
        "courses_by_tier": dict(sorted(Counter(course.get("tier") for course in courses).items())),
        "courses_by_role": dict(sorted(Counter(course.get("role") for course in courses).items())),
        "resources": resource_total,
        "unique_high_value_resources": len(high_value_urls),
        "courses_with_projects": project_courses,
        "resources_with_required_metadata": complete_resources,
        "resource_metadata_percent": (
            round(complete_resources * 100 / resource_total, 2) if resource_total else 0.0
        ),
    }


def parse_iso_date(value: Any) -> date | None:
    if not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None
