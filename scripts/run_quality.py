from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.quality_common import REPO_ROOT


@dataclass(frozen=True)
class Command:
    label: str
    arguments: tuple[str, ...]


def commands(*, include_external: bool, include_build: bool) -> list[Command]:
    python = sys.executable
    output = [
        Command("dependency consistency", (python, "-m", "pip", "check")),
        Command(
            "dependency lock",
            (python, "scripts/check_dependency_lock.py"),
        ),
        Command(
            "official resource evidence",
            (python, "scripts/enrich_official_resources.py", "--validate-only"),
        ),
        Command("canonical drift", (python, "scripts/compile_courses.py", "--check")),
        Command(
            "suggested project drift",
            (python, "scripts/apply_project_templates.py", "--check"),
        ),
        Command(
            "editorial drift",
            (python, "scripts/apply_course_editorial.py", "--check"),
        ),
        Command("course data", (python, "scripts/validate_courses.py")),
        Command(
            "mainline audit",
            (python, "scripts/validate_mainline_audit.py"),
        ),
        Command(
            "researched course guides",
            (
                python,
                "scripts/check_course_guides.py",
                "--minimum-guides",
                "60",
                "--require-track-coverage",
                "--require-mainline-coverage",
            ),
        ),
        Command(
            "editorial anti-template gate",
            (
                python,
                "scripts/check_editorial_quality.py",
                "--warnings-as-errors",
                "--json-report",
                "build/editorial-quality.json",
            ),
        ),
        Command("learning routes", (python, "scripts/validate_routes.py")),
        Command("generated pages", (python, "scripts/generate_course_pages.py", "--check")),
        Command("generated navigation", (python, "scripts/sync_navigation.py", "--check")),
        Command("forbidden text", (python, "scripts/check_forbidden_terms.py")),
        Command("translations", (python, "scripts/check_translations.py")),
        Command("navigation", (python, "scripts/check_navigation.py")),
        Command("Markdown links", (python, "scripts/check_markdown_links.py")),
        Command("unit tests", (python, "-m", "pytest", "-q")),
    ]
    if include_external:
        output.append(
            Command(
                "external links",
                (
                    python,
                    "scripts/check_external_links.py",
                    "--allow-review",
                ),
            )
        )
    output.append(Command("quality report", (python, "scripts/quality_report.py")))
    if include_build:
        output.append(
            Command(
                "strict site build",
                (python, "-m", "mkdocs", "build", "--strict"),
            )
        )
    return output


def run_commands(items: Sequence[Command]) -> int:
    failures: list[str] = []
    for command in items:
        print(f"\n== {command.label} ==")
        completed = subprocess.run(command.arguments, cwd=REPO_ROOT, check=False)
        if completed.returncode:
            failures.append(f"{command.label} ({completed.returncode})")
    if failures:
        print("\nQuality gate failed: " + ", ".join(failures), file=sys.stderr)
        return 1
    print("\nAll quality gates passed.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the complete local quality gate.")
    parser.add_argument("--external", action="store_true")
    parser.add_argument("--skip-build", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return run_commands(
        commands(
            include_external=args.external,
            include_build=not args.skip_build,
        )
    )


if __name__ == "__main__":
    raise SystemExit(main())
