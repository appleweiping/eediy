from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Mapping

from scripts.quality_common import (
    Issue,
    QualityError,
    display_path,
    load_json,
    markdown_headings,
    repo_path,
)


MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\((https://[^)\s]+)\)")
HTML_LINK_RE = re.compile(r"""href=["'](https://[^"']+)["']""")
LATIN_WORD_RE = re.compile(r"\b[A-Za-z][A-Za-z0-9'-]*\b")
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
FIRST_HAND_ZH_RE = re.compile(
    r"(?:我|本人)(?:学过|学完|上过|做过|完成过|踩过|花了|使用过)"
)
FIRST_HAND_EN_RE = re.compile(
    r"\bI\s+(?:took|studied|completed|built|spent|used|learned)\b",
    re.IGNORECASE,
)
VALID_STATUSES = {"catalogue", "researched", "learner-reviewed"}
VALID_EVIDENCE_LEVELS = {"R0", "R1", "R2", "R3", "R4"}


def _external_links(text: str) -> list[str]:
    return MARKDOWN_LINK_RE.findall(text) + HTML_LINK_RE.findall(text)


def _visible_length(text: str, language: str) -> int:
    without_urls = re.sub(r"https://\S+", " ", text)
    if language == "zh":
        return len(CJK_RE.findall(without_urls))
    return len(LATIN_WORD_RE.findall(without_urls))


def _schema_issues(value: Any, schema: Any, source: str) -> list[Issue]:
    try:
        from jsonschema import Draft202012Validator, FormatChecker
    except ImportError:
        return [
            Issue(
                "error",
                "guide.schema_dependency",
                "jsonschema is required; install the development dependencies",
                source,
            )
        ]
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    issues: list[Issue] = []
    for error in sorted(validator.iter_errors(value), key=lambda item: list(item.path)):
        pointer = "/".join(str(part) for part in error.absolute_path)
        path = f"{source}:/{pointer}" if pointer else source
        issues.append(Issue("error", "guide.schema", error.message, path))
    return issues


def _validate_body(
    body: str,
    *,
    language: str,
    path: Path,
    evidence_level: str,
) -> list[Issue]:
    relative = display_path(path)
    issues: list[Issue] = []
    if body.startswith("---"):
        issues.append(
            Issue(
                "error",
                "guide.front_matter",
                "course-guide fragments must not contain front matter",
                relative,
            )
        )
    headings = markdown_headings(body)
    if any(level == 1 for level, _, _ in headings):
        issues.append(
            Issue(
                "error",
                "guide.h1",
                "course-guide fragments must not contain an H1",
                relative,
            )
        )
    h2_count = sum(level == 2 for level, _, _ in headings)
    if h2_count < 3:
        issues.append(
            Issue(
                "error",
                "guide.sections",
                "researched course guides require at least three H2 sections",
                relative,
            )
        )
    minimum = 1000 if language == "zh" else 550
    length = _visible_length(body, language)
    if length < minimum:
        issues.append(
            Issue(
                "error",
                "guide.depth",
                f"guide has {length} visible {'CJK characters' if language == 'zh' else 'words'}; "
                f"minimum is {minimum}",
                relative,
            )
        )
    links = _external_links(body)
    if not 3 <= len(links) <= 7:
        issues.append(
            Issue(
                "error",
                "guide.narrative_links",
                f"guide narrative requires 3–7 curated HTTPS links, found {len(links)}",
                relative,
            )
        )
    if evidence_level == "R0":
        first_hand = (
            FIRST_HAND_ZH_RE.search(body)
            if language == "zh"
            else FIRST_HAND_EN_RE.search(body)
        )
        if first_hand:
            issues.append(
                Issue(
                    "error",
                    "guide.unsourced_first_hand",
                    "R0 desk research must not claim first-hand learning experience",
                    relative,
                )
            )
    return issues


def load_course_guides(
    manifest_path: Path,
    catalogue: Mapping[str, Any],
    schema_path: Path | None = None,
) -> tuple[dict[int, dict[str, Any]], list[Issue]]:
    try:
        value = load_json(manifest_path)
    except (OSError, QualityError) as exc:
        return {}, [
            Issue("error", "guide.manifest_load", str(exc), display_path(manifest_path))
        ]
    schema_path = schema_path or repo_path("data/course-guide.schema.json")
    try:
        schema = load_json(schema_path)
    except (OSError, QualityError) as exc:
        return {}, [
            Issue("error", "guide.schema_load", str(exc), display_path(schema_path))
        ]
    schema_issues = _schema_issues(value, schema, display_path(manifest_path))
    if schema_issues:
        return {}, schema_issues
    records = value.get("guides") if isinstance(value, Mapping) else None
    if not isinstance(records, list):
        return {}, [
            Issue(
                "error",
                "guide.manifest_shape",
                "course-guide manifest must contain a guides array",
                display_path(manifest_path),
            )
        ]

    known_ids = {
        int(course["source_id"])
        for course in catalogue.get("courses", [])
        if isinstance(course, Mapping) and isinstance(course.get("source_id"), int)
    }
    guides: dict[int, dict[str, Any]] = {}
    issues: list[Issue] = []
    for index, record in enumerate(records):
        record_path = f"{display_path(manifest_path)}:/guides/{index}"
        if not isinstance(record, Mapping):
            issues.append(
                Issue("error", "guide.record", "guide record must be an object", record_path)
            )
            continue
        course_id = record.get("course_id")
        if not isinstance(course_id, int) or isinstance(course_id, bool):
            issues.append(
                Issue(
                    "error",
                    "guide.course_id",
                    "course_id must be an integer",
                    record_path,
                )
            )
            continue
        if course_id in guides:
            issues.append(
                Issue(
                    "error",
                    "guide.duplicate",
                    f"duplicate guide for course_id {course_id}",
                    record_path,
                )
            )
            continue
        if course_id not in known_ids:
            issues.append(
                Issue(
                    "error",
                    "guide.unknown_course",
                    f"course_id {course_id} does not exist in the catalogue",
                    record_path,
                )
            )
        status = record.get("editorial_status")
        evidence_level = record.get("evidence_level")
        if status not in VALID_STATUSES:
            issues.append(
                Issue(
                    "error",
                    "guide.status",
                    f"unsupported editorial_status {status!r}",
                    record_path,
                )
            )
        if evidence_level not in VALID_EVIDENCE_LEVELS:
            issues.append(
                Issue(
                    "error",
                    "guide.evidence_level",
                    f"unsupported evidence_level {evidence_level!r}",
                    record_path,
                )
            )
        learner_reviews = record.get("learner_reviews", [])
        if not isinstance(learner_reviews, list):
            issues.append(
                Issue(
                    "error",
                    "guide.learner_reviews",
                    "learner_reviews must be an array",
                    record_path,
                )
            )
            learner_reviews = []
        if evidence_level in {"R0", "R1"} and learner_reviews:
            issues.append(
                Issue(
                    "error",
                    "guide.review_level",
                    "R0/R1 records cannot contain learner reviews",
                    record_path,
                )
            )
        if status == "learner-reviewed" and evidence_level not in {"R2", "R3", "R4"}:
            issues.append(
                Issue(
                    "error",
                    "guide.review_status",
                    "learner-reviewed status requires R2, R3, or R4 evidence",
                    record_path,
                )
            )

        files = record.get("files")
        bodies: dict[str, str] = {}
        heading_levels: dict[str, list[int]] = {}
        if not isinstance(files, Mapping):
            issues.append(
                Issue(
                    "error",
                    "guide.files",
                    "guide record requires bilingual files",
                    record_path,
                )
            )
            files = {}
        for language in ("zh", "en"):
            file_value = files.get(language)
            if not isinstance(file_value, str) or not file_value.strip():
                issues.append(
                    Issue(
                        "error",
                        "guide.file",
                        f"missing {language} guide file",
                        record_path,
                    )
                )
                continue
            path = repo_path(file_value)
            expected_root = repo_path("content/course-guides")
            try:
                path.resolve().relative_to(expected_root.resolve())
            except ValueError:
                issues.append(
                    Issue(
                        "error",
                        "guide.file_scope",
                        "guide files must stay under content/course-guides",
                        file_value,
                    )
                )
                continue
            try:
                body = path.read_text(encoding="utf-8").strip() + "\n"
            except (OSError, UnicodeDecodeError) as exc:
                issues.append(
                    Issue("error", "guide.file_read", str(exc), display_path(path))
                )
                continue
            bodies[language] = body
            heading_levels[language] = [
                level for level, _, _ in markdown_headings(body)
            ]
            issues.extend(
                _validate_body(
                    body,
                    language=language,
                    path=path,
                    evidence_level=str(evidence_level),
                )
            )
        if heading_levels.get("zh") != heading_levels.get("en"):
            issues.append(
                Issue(
                    "error",
                    "guide.translation_structure",
                    "Chinese and English guide heading levels differ",
                    record_path,
                )
            )

        primary_sources = record.get("primary_sources")
        if (
            not isinstance(primary_sources, list)
            or len(primary_sources) < 2
            or any(
                not isinstance(url, str) or not url.startswith("https://")
                for url in primary_sources
            )
        ):
            issues.append(
                Issue(
                    "error",
                    "guide.primary_sources",
                    "guide requires at least two HTTPS primary sources",
                    record_path,
                )
            )

        hydrated = dict(record)
        hydrated["bodies"] = bodies
        guides[course_id] = hydrated
    return guides, issues
