from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.quality_common import Issue, emit_issues, exit_code, line_for_offset, repo_path


TEXT_SUFFIXES = {
    ".css",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".md",
    ".py",
    ".svg",
    ".toml",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}
SKIP_PARTS = {
    ".git",
    ".cache",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "site",
}


def default_denied_terms() -> tuple[tuple[str, str], ...]:
    # Sensitive comparison names are assembled so the checker does not itself
    # publish those names in repository text.
    return (
        ("reference-brand-a", "".join(("cs", "diy"))),
        ("reference-repository", "".join(("cs-self", "-learning"))),
        ("reference-account", "".join(("PKU", "FlyingPig"))),
        ("copy-claim", "".join(("\u4eff", "\u5236"))),
        ("unfinished-marker-a", "".join(("TO", "DO"))),
        ("unfinished-marker-b", "".join(("T", "BD"))),
        ("unfinished-marker-c", "".join(("FIX", "ME"))),
        ("unfinished-zh", "".join(("\u5f85", "\u8865\u5145"))),
        ("unfinished-zh-later", "".join(("\u7a0d\u540e", "\u8865\u5145"))),
        ("unfinished-en", " ".join(("coming", "soon"))),
        ("placeholder", " ".join(("lorem", "ipsum"))),
    )


SECRET_PATTERNS = (
    ("private-key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b")),
    ("api-key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
)


def iter_text_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in SKIP_PARTS for part in path.parts):
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in {
            "CODEOWNERS",
            "LICENSE",
        }:
            yield path


def forbidden_issues(
    root: Path,
    *,
    denied_terms: Sequence[tuple[str, str]] | None = None,
) -> list[Issue]:
    denied_terms = denied_terms or default_denied_terms()
    issues: list[Issue] = []
    for path in iter_text_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            issues.append(
                Issue(
                    "error",
                    "text.encoding",
                    "managed text file is not valid UTF-8",
                    path.relative_to(root).as_posix(),
                )
            )
            continue
        relative = path.relative_to(root).as_posix()
        lowered = text.casefold()
        for label, term in denied_terms:
            offset = lowered.find(term.casefold())
            if offset >= 0:
                issues.append(
                    Issue(
                        "error",
                        f"text.{label}",
                        "forbidden or unfinished term found",
                        relative,
                        line_for_offset(text, offset),
                    )
                )
        for label, pattern in SECRET_PATTERNS:
            for match in pattern.finditer(text):
                issues.append(
                    Issue(
                        "error",
                        f"secret.{label}",
                        "credential-like text must not be committed",
                        relative,
                        line_for_offset(text, match.start()),
                    )
                )
    return issues


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Reject prohibited references, unfinished placeholders, and credential patterns."
    )
    parser.add_argument("--root", default=".")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = repo_path(args.root)
    issues = forbidden_issues(root)
    emit_issues(issues)
    print(f"Forbidden-text scan: {len(issues)} issue(s)")
    return exit_code(issues)


if __name__ == "__main__":
    raise SystemExit(main())
