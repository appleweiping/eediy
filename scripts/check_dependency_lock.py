from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.quality_common import Issue, emit_issues, exit_code, repo_path


PIN_RE = re.compile(r"^([A-Za-z0-9][A-Za-z0-9_.-]*)==([^\s\\]+)")


def _normalized_name(value: str) -> str:
    return re.sub(r"[-_.]+", "-", value).lower()


def _direct_pins(paths: list[Path]) -> tuple[dict[str, str], list[Issue]]:
    pins: dict[str, str] = {}
    issues: list[Issue] = []
    for path in paths:
        for line_number, raw in enumerate(
            path.read_text(encoding="utf-8").splitlines(), 1
        ):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            match = PIN_RE.fullmatch(line)
            if not match:
                issues.append(
                    Issue(
                        "error",
                        "dependency.direct_not_exact",
                        "direct dependencies must use a plain exact name==version pin",
                        path.as_posix(),
                        line_number,
                    )
                )
                continue
            name = _normalized_name(match.group(1))
            version = match.group(2)
            previous = pins.get(name)
            if previous is not None and previous != version:
                issues.append(
                    Issue(
                        "error",
                        "dependency.direct_conflict",
                        f"{name} is pinned to both {previous} and {version}",
                        path.as_posix(),
                        line_number,
                    )
                )
            pins[name] = version
    return pins, issues


def dependency_lock_issues(
    direct_paths: list[Path],
    lock_path: Path,
) -> list[Issue]:
    direct, issues = _direct_pins(direct_paths)
    lines = lock_path.read_text(encoding="utf-8").splitlines()
    locked: dict[str, tuple[str, int, str]] = {}
    starts = [
        index
        for index, line in enumerate(lines)
        if line and not line[0].isspace() and PIN_RE.match(line)
    ]
    for position, start in enumerate(starts):
        match = PIN_RE.match(lines[start])
        assert match is not None
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        name = _normalized_name(match.group(1))
        version = match.group(2)
        block = "\n".join(lines[start:end])
        if name in locked:
            issues.append(
                Issue(
                    "error",
                    "dependency.lock_duplicate",
                    f"duplicate lock entry for {name}",
                    lock_path.as_posix(),
                    start + 1,
                )
            )
        locked[name] = (version, start + 1, block)
        if "--hash=sha256:" not in block:
            issues.append(
                Issue(
                    "error",
                    "dependency.lock_hash_missing",
                    f"lock entry for {name} has no SHA-256 distribution hash",
                    lock_path.as_posix(),
                    start + 1,
                )
            )

    for name, version in sorted(direct.items()):
        locked_entry = locked.get(name)
        if locked_entry is None:
            issues.append(
                Issue(
                    "error",
                    "dependency.lock_missing",
                    f"direct dependency {name}=={version} is missing from the lock",
                    lock_path.as_posix(),
                )
            )
            continue
        locked_version, line_number, _block = locked_entry
        if locked_version != version:
            issues.append(
                Issue(
                    "error",
                    "dependency.lock_drift",
                    f"{name} is {version} in direct inputs but {locked_version} in the lock",
                    lock_path.as_posix(),
                    line_number,
                )
            )
    return issues


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate exact direct pins against the hash-locked resolution."
    )
    parser.add_argument(
        "--direct",
        action="append",
        default=[],
        help="Direct requirements file; may be repeated.",
    )
    parser.add_argument("--lock", default="requirements.lock")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    direct = args.direct or ["requirements.txt", "requirements-dev.txt"]
    issues = dependency_lock_issues(
        [repo_path(path) for path in direct],
        repo_path(args.lock),
    )
    emit_issues(issues)
    print(
        f"Dependency lock: {len(direct)} direct input files, "
        f"{len(issues)} issue(s)"
    )
    return exit_code(issues)


if __name__ == "__main__":
    raise SystemExit(main())
