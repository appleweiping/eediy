from __future__ import annotations

import json
import os
import shlex
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
RING_BUFFER = REPO_ROOT / "examples" / "ring-buffer"
SENSOR_SAMPLER = REPO_ROOT / "examples" / "sensor-sampler"

STRICT_C_FLAGS = (
    "-std=c11",
    "-Wall",
    "-Wextra",
    "-Wpedantic",
    "-Wconversion",
    "-Wshadow",
    "-Werror",
)

RING_BUFFER_OUTPUT = """\
ring-buffer check=empty-and-invalid result=PASS
ring-buffer check=exact-capacity-and-full result=PASS
ring-buffer check=fifo-wraparound result=PASS
ring-buffer check=repeated-boundary result=PASS
ring-buffer check=adc-dma-adapter result=PASS
ring-buffer check=adapter-arguments result=PASS
ring-buffer summary=PASS checks=6
"""

SENSOR_SAMPLER_OUTPUT = """\
scenario=default_safe event=state t_ms=0 validity=invalid value_milli=0 reason=not_ready state=idle
scenario=normal event=request t_ms=0 state=waiting deadline_ms=5
scenario=normal event=outcome t_ms=1 validity=valid value_milli=2500 reason=none state=idle
scenario=sensor_missing event=outcome t_ms=0 validity=invalid value_milli=0 reason=sensor_missing state=idle
scenario=bus_busy event=outcome t_ms=0 validity=invalid value_milli=0 reason=bus_busy state=idle
scenario=crc_error event=request t_ms=0 state=waiting deadline_ms=5
scenario=crc_error event=outcome t_ms=1 validity=invalid value_milli=0 reason=crc_error state=idle
scenario=buffer_full event=request t_ms=0 state=waiting deadline_ms=5
scenario=buffer_full event=outcome t_ms=1 validity=invalid value_milli=0 reason=buffer_full state=idle
scenario=delayed_interrupt event=request t_ms=0 state=waiting deadline_ms=5
scenario=delayed_interrupt event=outcome t_ms=5 validity=invalid value_milli=0 reason=delayed_interrupt state=idle
sensor-sampler summary=PASS scenarios=6
"""


def _compiler_candidates() -> list[list[str]]:
    candidates: list[list[str]] = []
    configured = os.environ.get("CC")
    if configured:
        candidates.append(shlex.split(configured, posix=os.name != "nt"))
    for name in ("gcc", "clang"):
        resolved = shutil.which(name)
        if resolved:
            candidates.append([resolved])
    if os.name == "nt":
        candidates.append(
            [r"D:\tuelearning\C\MSYS2\ucrt64\bin\gcc.exe"]
        )
    return candidates


@pytest.fixture(scope="module")
def c_compiler() -> list[str]:
    for command in _compiler_candidates():
        if not command:
            continue
        executable = Path(command[0])
        if not executable.exists() and shutil.which(command[0]) is None:
            continue
        probe = subprocess.run(
            [*command, "--version"],
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        if probe.returncode == 0:
            return command
    pytest.fail(
        "The executable C examples require GCC or Clang; no compiler was found."
    )


def _compile(
    compiler: list[str],
    output: Path,
    include_dir: Path,
    sources: tuple[Path, ...],
    *,
    definitions: tuple[str, ...] = (),
) -> subprocess.CompletedProcess[str]:
    command = [
        *compiler,
        *STRICT_C_FLAGS,
        *(f"-D{definition}" for definition in definitions),
        "-I",
        str(include_dir),
        *(str(source) for source in sources),
        "-o",
        str(output),
    ]
    return subprocess.run(
        command,
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def _run(executable: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(executable)],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def test_ring_buffer_contract_executes_with_strict_warnings(
    tmp_path: Path,
    c_compiler: list[str],
) -> None:
    executable_name = (
        "ring-buffer-tests.exe" if os.name == "nt" else "ring-buffer-tests"
    )
    executable = tmp_path / executable_name
    compiled = _compile(
        c_compiler,
        executable,
        RING_BUFFER / "include",
        (
            RING_BUFFER / "src" / "ring_buffer.c",
            RING_BUFFER / "src" / "adc_dma_adapter.c",
            RING_BUFFER / "tests" / "test_ring_buffer.c",
        ),
    )
    assert compiled.returncode == 0, compiled.stdout + compiled.stderr

    completed = _run(executable)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert completed.stderr == ""
    assert completed.stdout == RING_BUFFER_OUTPUT


def test_ring_buffer_deliberate_fault_really_exits_nonzero(
    tmp_path: Path,
    c_compiler: list[str],
) -> None:
    executable_name = (
        "ring-buffer-fault.exe" if os.name == "nt" else "ring-buffer-fault"
    )
    executable = tmp_path / executable_name
    compiled = _compile(
        c_compiler,
        executable,
        RING_BUFFER / "include",
        (
            RING_BUFFER / "src" / "ring_buffer.c",
            RING_BUFFER / "tests" / "fault_probe.c",
        ),
        definitions=("RING_BUFFER_DELIBERATE_FULL_FAULT=1",),
    )
    assert compiled.returncode == 0, compiled.stdout + compiled.stderr

    completed = _run(executable)
    assert completed.returncode == 7
    assert completed.stderr == ""
    assert (
        completed.stdout
        == "deliberate-fault: accepted sample 999 while full\n"
    )


def test_sensor_sampler_executes_all_fault_injections(
    tmp_path: Path,
    c_compiler: list[str],
) -> None:
    executable_name = (
        "sensor-sampler-tests.exe" if os.name == "nt" else "sensor-sampler-tests"
    )
    executable = tmp_path / executable_name
    compiled = _compile(
        c_compiler,
        executable,
        SENSOR_SAMPLER / "include",
        (
            SENSOR_SAMPLER / "src" / "sampler.c",
            SENSOR_SAMPLER / "tests" / "test_sensor_sampler.c",
        ),
    )
    assert compiled.returncode == 0, compiled.stdout + compiled.stderr

    completed = _run(executable)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert completed.stderr == ""
    assert completed.stdout == SENSOR_SAMPLER_OUTPUT


@pytest.mark.parametrize("example", (RING_BUFFER, SENSOR_SAMPLER))
def test_cmake_presets_run_real_sanitized_workflows(example: Path) -> None:
    cmake = (example / "CMakeLists.txt").read_text(encoding="utf-8")
    presets = json.loads(
        (example / "CMakePresets.json").read_text(encoding="utf-8")
    )

    assert "C_EXTENSIONS OFF" in cmake
    assert "-fsanitize=address,undefined" in cmake
    assert "-fno-omit-frame-pointer" in cmake
    assert "-Werror" in cmake
    assert "include(CTest)" in cmake

    configure = {
        preset["name"]: preset for preset in presets["configurePresets"]
    }
    assert configure["host-sanitized"]["cacheVariables"] == {
        "ENABLE_SANITIZERS": "ON"
    }
    workflows = {
        preset["name"]: preset for preset in presets["workflowPresets"]
    }
    assert workflows["host-sanitized"]["steps"] == [
        {"type": "configure", "name": "host-sanitized"},
        {"type": "build", "name": "host-sanitized"},
        {"type": "test", "name": "host-sanitized"},
    ]


def test_ring_buffer_negative_test_checks_exit_and_observation() -> None:
    harness = (
        RING_BUFFER / "cmake" / "ExpectFailure.cmake"
    ).read_text(encoding="utf-8")
    normal_source = (
        RING_BUFFER / "src" / "ring_buffer.c"
    ).read_text(encoding="utf-8")

    assert "probe_result EQUAL 7" in harness
    assert "accepted sample 999 while full" in harness
    assert "RING_BUFFER_DELIBERATE_FULL_FAULT" in normal_source
    assert "malloc(" not in normal_source
    assert "calloc(" not in normal_source
    assert "realloc(" not in normal_source


def test_c_examples_are_linked_from_bilingual_guides() -> None:
    expected = {
        "docs/guides/c-cmake.md": (
            "https://github.com/appleweiping/eediy/tree/main/examples/ring-buffer"
        ),
        "docs/en/guides/c-cmake.md": (
            "https://github.com/appleweiping/eediy/tree/main/examples/ring-buffer"
        ),
        "docs/guides/embedded-toolchains.md": (
            "https://github.com/appleweiping/eediy/tree/main/examples/sensor-sampler"
        ),
        "docs/en/guides/embedded-toolchains.md": (
            "https://github.com/appleweiping/eediy/tree/main/examples/sensor-sampler"
        ),
    }
    for relative_path, starter_url in expected.items():
        guide = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
        assert starter_url in guide
        assert "cmake --workflow --preset host-sanitized" in guide


@pytest.mark.parametrize(
    ("readme", "expected_output"),
    (
        (RING_BUFFER / "README.md", RING_BUFFER_OUTPUT),
        (SENSOR_SAMPLER / "README.md", SENSOR_SAMPLER_OUTPUT),
    ),
)
def test_readmes_preserve_observed_host_output(
    readme: Path,
    expected_output: str,
) -> None:
    text = readme.read_text(encoding="utf-8")
    assert expected_output.rstrip() in text
