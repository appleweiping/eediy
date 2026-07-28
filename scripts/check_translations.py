from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.quality_common import (
    FENCE_RE,
    Issue,
    QualityError,
    emit_issues,
    exit_code,
    markdown_files,
    markdown_headings,
    repo_path,
    split_front_matter,
    strip_code_blocks,
    write_json_report,
)


CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
LATIN_WORD_RE = re.compile(r"\b[A-Za-z]{3,}\b")


def counterpart(path: Path, docs_root: Path) -> Path:
    relative = path.relative_to(docs_root)
    if relative.parts and relative.parts[0] == "en":
        return docs_root.joinpath(*relative.parts[1:])
    return docs_root / "en" / relative


def translation_pairs(docs_root: Path) -> tuple[list[tuple[Path, Path]], list[Issue]]:
    issues: list[Issue] = []
    files = markdown_files(docs_root)
    file_set = {path.resolve() for path in files}
    pairs: list[tuple[Path, Path]] = []
    for zh_path in files:
        relative = zh_path.relative_to(docs_root)
        if relative.parts and relative.parts[0] == "en":
            continue
        en_path = counterpart(zh_path, docs_root)
        if en_path.resolve() not in file_set:
            issues.append(
                Issue(
                    "error",
                    "translation.missing_en",
                    "English counterpart is missing",
                    relative.as_posix(),
                )
            )
        else:
            pairs.append((zh_path, en_path))
    for en_path in files:
        relative = en_path.relative_to(docs_root)
        if not relative.parts or relative.parts[0] != "en":
            continue
        zh_path = counterpart(en_path, docs_root)
        if zh_path.resolve() not in file_set:
            issues.append(
                Issue(
                    "error",
                    "translation.missing_zh",
                    "Chinese counterpart is missing",
                    relative.as_posix(),
                )
            )
    return pairs, issues


def _body_language_issues(body: str, language: str, path: str) -> list[Issue]:
    visible = strip_code_blocks(body)
    # Remove tags and URLs before a light language sanity check. Technical names
    # may remain in either language, so this deliberately avoids ratio matching.
    visible = re.sub(r"<[^>]+>", " ", visible)
    visible = re.sub(r"https?://\S+", " ", visible)
    issues: list[Issue] = []
    if len(visible.strip()) < 80:
        issues.append(
            Issue("error", "translation.too_short", "page body is too short to be useful", path)
        )
    if language == "zh" and not CJK_RE.search(visible):
        issues.append(
            Issue(
                "error",
                "translation.zh_language",
                "Chinese page contains no Chinese text",
                path,
            )
        )
    if language == "en" and len(LATIN_WORD_RE.findall(visible)) < 12:
        issues.append(
            Issue(
                "error",
                "translation.en_language",
                "English page contains too little English prose",
                path,
            )
        )
    return issues


def _is_learning_guide(relative: Path) -> bool:
    return (
        relative.as_posix() in {"getting-started.md", "roadmap.md"}
        or (relative.parts and relative.parts[0] == "guides")
    )


def _is_substantive_pair(zh_body: str, en_body: str) -> bool:
    zh_visible = re.sub(r"<[^>]+>", " ", strip_code_blocks(zh_body))
    en_visible = re.sub(r"<[^>]+>", " ", strip_code_blocks(en_body))
    zh_length = len(re.sub(r"\s+", "", zh_visible))
    en_words = len(LATIN_WORD_RE.findall(en_visible))
    return zh_length >= 500 and en_words >= 120


def translation_issues(
    docs_root: Path,
    *,
    minimum_substantive_guides: int = 16,
) -> tuple[list[Issue], dict[str, Any]]:
    pairs, issues = translation_pairs(docs_root)
    substantive_guides: list[str] = []
    for zh_path, en_path in pairs:
        zh_relative = zh_path.relative_to(docs_root).as_posix()
        en_relative = en_path.relative_to(docs_root).as_posix()
        try:
            zh_meta, zh_body = split_front_matter(zh_path.read_text(encoding="utf-8"))
            en_meta, en_body = split_front_matter(en_path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, QualityError) as exc:
            issues.append(Issue("error", "translation.parse", str(exc), zh_relative))
            continue
        for path, metadata in ((zh_relative, zh_meta), (en_relative, en_meta)):
            for key in ("title", "description"):
                if not isinstance(metadata.get(key), str) or not metadata[key].strip():
                    issues.append(
                        Issue(
                            "error",
                            "translation.front_matter",
                            f"front matter requires non-empty {key}",
                            path,
                        )
                    )
        zh_heading_levels = [level for level, _, _ in markdown_headings(zh_body)]
        en_heading_levels = [level for level, _, _ in markdown_headings(en_body)]
        if zh_heading_levels != en_heading_levels:
            issues.append(
                Issue(
                    "error",
                    "translation.heading_structure",
                    f"heading levels differ: zh={zh_heading_levels}, en={en_heading_levels}",
                    zh_relative,
                )
            )
        zh_fences = len(FENCE_RE.findall(zh_body))
        en_fences = len(FENCE_RE.findall(en_body))
        if zh_fences != en_fences:
            issues.append(
                Issue(
                    "error",
                    "translation.code_structure",
                    f"code-fence counts differ: zh={zh_fences}, en={en_fences}",
                    zh_relative,
                )
            )
        normalized_zh = re.sub(r"\s+", " ", strip_code_blocks(zh_body)).strip()
        normalized_en = re.sub(r"\s+", " ", strip_code_blocks(en_body)).strip()
        if len(normalized_zh) > 200 and normalized_zh == normalized_en:
            issues.append(
                Issue(
                    "error",
                    "translation.identical",
                    "counterpart pages are identical and appear untranslated",
                    zh_relative,
                )
            )
        issues.extend(_body_language_issues(zh_body, "zh", zh_relative))
        issues.extend(_body_language_issues(en_body, "en", en_relative))
        if _is_learning_guide(zh_path.relative_to(docs_root)) and _is_substantive_pair(
            zh_body, en_body
        ):
            substantive_guides.append(zh_relative)
    zh_count = len(
        [
            path
            for path in markdown_files(docs_root)
            if path.relative_to(docs_root).parts[0] != "en"
        ]
    )
    en_count = len(markdown_files(docs_root)) - zh_count
    statistics = {
        "zh_pages": zh_count,
        "en_pages": en_count,
        "paired_pages": len(pairs),
        "pair_coverage_percent": (
            round(len(pairs) * 100 / max(zh_count, en_count), 2)
            if max(zh_count, en_count)
            else 100.0
        ),
        "substantive_guide_pairs": len(substantive_guides),
        "substantive_guides": sorted(substantive_guides),
    }
    if len(substantive_guides) < minimum_substantive_guides:
        issues.append(
            Issue(
                "error",
                "translation.guide_count",
                f"expected at least {minimum_substantive_guides} substantive bilingual guide "
                f"pairs, found {len(substantive_guides)}",
                docs_root.as_posix(),
            )
        )
    return list(dict.fromkeys(issues)), statistics


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Require complete, structurally aligned Chinese and English documentation."
    )
    parser.add_argument("--docs-root", default="docs")
    parser.add_argument("--json-report")
    parser.add_argument("--minimum-substantive-guides", type=int, default=16)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    issues, statistics = translation_issues(
        repo_path(args.docs_root),
        minimum_substantive_guides=args.minimum_substantive_guides,
    )
    emit_issues(issues)
    print(
        f"Translations: {statistics['paired_pages']} pairs, "
        f"{statistics['pair_coverage_percent']:.2f}% coverage"
    )
    write_json_report(
        repo_path(args.json_report) if args.json_report else None,
        {
            "ok": exit_code(issues) == 0,
            "statistics": statistics,
            "issues": [issue.to_dict() for issue in issues],
        },
    )
    return exit_code(issues)


if __name__ == "__main__":
    raise SystemExit(main())
