from __future__ import annotations

import argparse
import copy
import difflib
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.quality_common import (
    Issue,
    QualityError,
    atomic_write,
    emit_issues,
    exit_code,
    load_json,
    repo_path,
    stable_json,
)


EDITORIAL_FIELDS = {"source_id", "summary", "review_note"}
LOCALIZED_FIELDS = ("summary", "review_note")
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
RESOURCE_TERMS = {
    "zh": (
        "视频",
        "讲义",
        "练习",
        "习题",
        "作业",
        "实验",
        "考试",
        "代码",
        "教材",
        "项目",
        "材料",
        "课件",
        "笔记本",
        "演示",
        "模拟器",
        "仿真",
        "预印本",
        "专著",
        "录屏",
        "阅读",
        "答案",
        "资源",
        "工具链",
    ),
    "en": (
        "video",
        "note",
        "practice",
        "problem",
        "homework",
        "lab",
        "exam",
        "code",
        "text",
        "project",
        "material",
        "slide",
        "notebook",
        "demonstration",
        "simulator",
        "simulation",
        "preprint",
        "monograph",
        "recording",
        "reading",
        "solution",
        "resource",
        "assignment",
        "assessment",
        "feedback",
        "toolchain",
    ),
}


def _sentence_count(text: str, language: str) -> int:
    if language == "zh":
        return len(re.findall(r"[。！？](?:[”’」』】）》]*)", text))
    return len(re.findall(r"[.!?](?:[\"'’”)\]]*)?(?:\s|$)", text))


def validate_editorial(
    value: Any,
    candidates: Sequence[Mapping[str, Any]],
    *,
    source: str = "data/course_editorial.json",
) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(value, list):
        return [Issue("error", "editorial.type", "editorial data must be a JSON array", source)]

    candidate_by_id = {
        int(candidate["id"]): candidate
        for candidate in candidates
        if isinstance(candidate, Mapping) and isinstance(candidate.get("id"), int)
    }
    expected_ids = set(candidate_by_id)
    seen_ids: set[int] = set()
    summaries: dict[str, dict[str, int]] = {"zh": {}, "en": {}}

    for index, item in enumerate(value):
        path = f"{source}:[{index}]"
        if not isinstance(item, Mapping):
            issues.append(Issue("error", "editorial.item", "entry must be an object", path))
            continue
        keys = set(item)
        if keys != EDITORIAL_FIELDS:
            missing = sorted(EDITORIAL_FIELDS - keys)
            extra = sorted(keys - EDITORIAL_FIELDS)
            details = []
            if missing:
                details.append(f"missing {', '.join(missing)}")
            if extra:
                details.append(f"unexpected {', '.join(extra)}")
            issues.append(
                Issue("error", "editorial.fields", "; ".join(details), path)
            )

        source_id = item.get("source_id")
        if not isinstance(source_id, int) or isinstance(source_id, bool):
            issues.append(
                Issue("error", "editorial.source_id", "source_id must be an integer", path)
            )
            candidate = None
        else:
            if source_id in seen_ids:
                issues.append(
                    Issue(
                        "error",
                        "editorial.duplicate_id",
                        f"duplicate source_id {source_id}",
                        path,
                    )
                )
            seen_ids.add(source_id)
            candidate = candidate_by_id.get(source_id)
            if candidate is None:
                issues.append(
                    Issue(
                        "error",
                        "editorial.unknown_id",
                        f"source_id {source_id} is not present in candidates",
                        path,
                    )
                )

        for field in LOCALIZED_FIELDS:
            localized = item.get(field)
            if not isinstance(localized, Mapping) or set(localized) != {"zh", "en"}:
                issues.append(
                    Issue(
                        "error",
                        "editorial.localized_shape",
                        f"{field} must contain exactly zh and en",
                        path,
                    )
                )
                continue
            zh = localized.get("zh")
            en = localized.get("en")
            if not isinstance(zh, str) or not zh.strip():
                issues.append(
                    Issue("error", "editorial.empty", f"{field}.zh must be non-empty", path)
                )
                continue
            if not isinstance(en, str) or not en.strip():
                issues.append(
                    Issue("error", "editorial.empty", f"{field}.en must be non-empty", path)
                )
                continue
            if zh.strip().casefold() == en.strip().casefold():
                issues.append(
                    Issue(
                        "error",
                        "editorial.identical_translation",
                        f"{field} cannot use identical Chinese and English text",
                        path,
                    )
                )
            if field == "review_note" and not CJK_RE.search(zh):
                issues.append(
                    Issue(
                        "error",
                        "editorial.review_note_chinese",
                        "review_note.zh must contain Chinese text",
                        path,
                    )
                )
            if field == "summary":
                for language, text in (("zh", zh.strip()), ("en", en.strip())):
                    if _sentence_count(text, language) > 2:
                        issues.append(
                            Issue(
                                "error",
                                "editorial.summary_sentence_count",
                                f"summary.{language} must use no more than two sentences",
                                path,
                            )
                        )
                    previous = summaries[language].get(text.casefold())
                    if previous is not None:
                        issues.append(
                            Issue(
                                "error",
                                "editorial.duplicate_summary",
                                f"summary.{language} duplicates source_id {previous}",
                                path,
                            )
                        )
                    elif isinstance(source_id, int):
                        summaries[language][text.casefold()] = source_id

        summary = item.get("summary")
        review_note = item.get("review_note")
        if candidate is not None and isinstance(summary, Mapping):
            title = str(candidate.get("title", "")).strip()
            institution = str(candidate.get("institution", "")).strip()
            for language in ("zh", "en"):
                text = summary.get(language)
                if not isinstance(text, str):
                    continue
                missing_evidence = [
                    label
                    for label, evidence in (("course title", title), ("institution", institution))
                    if evidence and evidence.casefold() not in text.casefold()
                ]
                if missing_evidence:
                    issues.append(
                        Issue(
                            "error",
                            "editorial.summary_evidence",
                            f"summary.{language} must name the {', '.join(missing_evidence)}",
                            path,
                        )
                    )
                if not any(term in text.casefold() for term in RESOURCE_TERMS[language]):
                    issues.append(
                        Issue(
                            "error",
                            "editorial.summary_resource_form",
                            f"summary.{language} must name at least one verifiable resource form",
                            path,
                        )
                    )
        if candidate is not None and isinstance(review_note, Mapping):
            english = review_note.get("en")
            risk = str(candidate.get("risk", "")).strip()
            if isinstance(english, str) and english.strip() != risk:
                issues.append(
                    Issue(
                        "error",
                        "editorial.review_note_fidelity",
                        "review_note.en must preserve the reviewed candidate risk exactly",
                        path,
                    )
                )

    missing_ids = sorted(expected_ids - seen_ids)
    extra_ids = sorted(seen_ids - expected_ids)
    if missing_ids:
        issues.append(
            Issue(
                "error",
                "editorial.coverage_missing",
                f"missing source IDs: {', '.join(map(str, missing_ids))}",
                source,
            )
        )
    if extra_ids:
        issues.append(
            Issue(
                "error",
                "editorial.coverage_extra",
                f"unexpected source IDs: {', '.join(map(str, extra_ids))}",
                source,
            )
        )
    if len(value) != len(expected_ids):
        issues.append(
            Issue(
                "error",
                "editorial.coverage_count",
                f"expected {len(expected_ids)} entries, found {len(value)}",
                source,
            )
        )
    return issues


def apply_editorial(
    catalogue: Mapping[str, Any],
    editorial: Sequence[Mapping[str, Any]],
    candidates: Sequence[Mapping[str, Any]],
) -> tuple[dict[str, Any] | None, list[Issue]]:
    issues = validate_editorial(editorial, candidates)
    if any(issue.severity == "error" for issue in issues):
        return None, issues

    result = copy.deepcopy(dict(catalogue))
    courses = result.get("courses")
    if not isinstance(courses, list):
        return None, issues + [
            Issue(
                "error",
                "editorial.catalogue_shape",
                "canonical catalogue must contain courses[]",
                "data/courses.json",
            )
        ]

    course_by_id: dict[int, dict[str, Any]] = {}
    for index, course in enumerate(courses):
        if not isinstance(course, dict) or not isinstance(course.get("source_id"), int):
            issues.append(
                Issue(
                    "error",
                    "editorial.catalogue_course",
                    "each canonical course needs an integer source_id",
                    f"data/courses.json:courses[{index}]",
                )
            )
            continue
        source_id = int(course["source_id"])
        if source_id in course_by_id:
            issues.append(
                Issue(
                    "error",
                    "editorial.catalogue_duplicate",
                    f"duplicate canonical source_id {source_id}",
                    f"data/courses.json:courses[{index}]",
                )
            )
        course_by_id[source_id] = course

    editorial_ids = {int(item["source_id"]) for item in editorial}
    catalogue_ids = set(course_by_id)
    if editorial_ids != catalogue_ids:
        issues.append(
            Issue(
                "error",
                "editorial.catalogue_coverage",
                "editorial and canonical source IDs must match exactly",
                "data/courses.json",
            )
        )
    if any(issue.severity == "error" for issue in issues):
        return None, issues

    for item in sorted(editorial, key=lambda entry: int(entry["source_id"])):
        course = course_by_id[int(item["source_id"])]
        course["summary"] = copy.deepcopy(item["summary"])
        course["review_note"] = copy.deepcopy(item["review_note"])
    return result, issues


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Apply the reviewed bilingual editorial layer to the canonical course catalogue."
    )
    parser.add_argument("--catalogue", default="data/courses.json")
    parser.add_argument("--editorial", default="data/course_editorial.json")
    parser.add_argument("--candidates", default="data/course_candidates.json")
    parser.add_argument(
        "--output",
        default=None,
        help="Output path; defaults to the canonical catalogue path.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail when the output differs from the deterministic editorial result.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    catalogue_path = repo_path(args.catalogue)
    editorial_path = repo_path(args.editorial)
    candidates_path = repo_path(args.candidates)
    output_path = repo_path(args.output) if args.output else catalogue_path
    issues: list[Issue] = []
    try:
        catalogue = load_json(catalogue_path)
        editorial = load_json(editorial_path)
        candidates = load_json(candidates_path)
    except (OSError, QualityError) as exc:
        issues.append(Issue("error", "editorial.input", str(exc)))
        emit_issues(issues)
        return exit_code(issues)
    if not isinstance(catalogue, Mapping) or not isinstance(candidates, list):
        issues.append(
            Issue(
                "error",
                "editorial.input_shape",
                "catalogue must be an object and candidates must be an array",
            )
        )
        emit_issues(issues)
        return exit_code(issues)

    result, apply_issues = apply_editorial(catalogue, editorial, candidates)
    issues.extend(apply_issues)
    if result is None:
        emit_issues(issues)
        return exit_code(issues)
    expected = stable_json(result)
    if args.check:
        if not output_path.exists():
            issues.append(
                Issue(
                    "error",
                    "editorial.output_missing",
                    f"run scripts/apply_course_editorial.py to create {args.output or args.catalogue}",
                    output_path.as_posix(),
                )
            )
        else:
            current = output_path.read_text(encoding="utf-8")
            if current != expected:
                diff = "".join(
                    difflib.unified_diff(
                        current.splitlines(keepends=True),
                        expected.splitlines(keepends=True),
                        fromfile=output_path.as_posix(),
                        tofile=f"{output_path.as_posix()} (expected)",
                        n=2,
                    )
                )
                issues.append(
                    Issue(
                        "error",
                        "editorial.drift",
                        "canonical catalogue does not contain the reviewed editorial layer",
                        output_path.as_posix(),
                        context="\n".join(diff.splitlines()[:30]),
                    )
                )
    else:
        atomic_write(output_path, expected)
        print(f"Applied {len(editorial)} editorial entries to {output_path.as_posix()}")
    emit_issues(issues)
    return exit_code(issues)


if __name__ == "__main__":
    raise SystemExit(main())
