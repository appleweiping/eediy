from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from typing import Any, Mapping

from scripts.course_data import normalize_url
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
PARAGRAPH_SPLIT_RE = re.compile(r"\n[ \t]*\n")
MARKDOWN_LINK_TARGET_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
FIRST_HAND_ZH_RE = re.compile(
    r"(?:我|本人)(?:学过|学完|上过|做过|完成过|踩过|花了|使用过)"
)
FIRST_HAND_EN_RE = re.compile(
    r"\bI\s+(?:took|studied|completed|built|spent|used|learned)\b",
    re.IGNORECASE,
)
VALID_STATUSES = {"catalogue", "researched", "learner-reviewed"}
VALID_EVIDENCE_LEVELS = {"R0", "R1", "R2", "R3", "R4"}
LEARNER_REVIEW_EVIDENCE_LEVELS = {"R2", "R3", "R4"}
LEARNER_REVIEW_RELATIONSHIPS = {
    "exact-offering",
    "same-course-other-run",
    "successor-course",
}
QUALIFYING_LEARNER_REVIEW_RELATIONSHIPS = {
    "exact-offering",
    "same-course-other-run",
}
EVIDENCE_LEVEL_RANK = {
    level: rank for rank, level in enumerate(("R0", "R1", "R2", "R3", "R4"))
}
GUIDE_SECTION_MINIMUM = 2
GUIDE_SECTION_MAXIMUM = 5
GUIDE_LENGTH_BOUNDS = {
    "zh": (320, 1400),
    "en": (180, 900),
}
BRAND_MENTION_MAXIMUM = 2
PROTOCOL_TONE_MAXIMUM = {
    "zh": 6,
    "en": 9,
}
PROTOCOL_TONE_PATTERNS = {
    "zh": (
        re.compile(pattern, re.IGNORECASE)
        for pattern in (
            r"保留",
            r"记录",
            r"复核",
            r"声称",
            r"最终报告",
            r"\bartifacts?\b",
            r"\bunknown\b",
            r"\bsign-off\b",
        )
    ),
    "en": (
        re.compile(pattern, re.IGNORECASE)
        for pattern in (
            r"\bpreserv(?:e|es|ed|ing)\b",
            r"\brecord(?:s|ed|ing)?\b",
            r"\breview(?:s|ed|ing)?\b",
            r"\bclaim(?:s|ed|ing)?\b",
            r"\bfinal report\b",
            r"\bartifacts?\b",
            r"\bunknown\b",
            r"\bsign-off\b",
        )
    ),
}
PROTOCOL_TONE_PATTERNS = {
    language: tuple(patterns)
    for language, patterns in PROTOCOL_TONE_PATTERNS.items()
}
INTERNAL_REVIEW_LANGUAGE = {
    "zh": re.compile(
        r"(?:\bR0\b|维护者|桌面(?:证据|审读|考察|研究)|"
        r"资料考察\s*[（(]?\s*R0|"
        r"\b(?:access|resource|evidence|gap)\s+ledger\b|"
        r"\b(?:completion|evidence)\s+dossier\b|"
        r"\breviewed_on\b)",
        re.IGNORECASE,
    ),
    "en": re.compile(
        r"(?:\bR0\b|desk[- ]research(?:ed)?|maintainer|"
        r"\b(?:access|resource|evidence|gap)\s+ledger\b|"
        r"\b(?:completion|evidence)\s+dossier\b|"
        r"\breviewed_on\b)",
        re.IGNORECASE,
    ),
}
ENDING_PROTOCOL = {
    "zh": re.compile(
        r"(?:纠错|修正建议|课程\s*ID|course\s*ID|审稿人|审核者|"
        r"提交反馈|资料考察\s*[（(]?\s*R0|\bR0\b)",
        re.IGNORECASE,
    ),
    "en": re.compile(
        r"(?:corrections?\s+(?:should|must)|course\s*ID|"
        r"reviewer|submit\s+(?:a\s+)?correction|\bR0\b|desk[- ]review)",
        re.IGNORECASE,
    ),
}
SINGULAR_RANGE_LABEL_EN_RE = re.compile(
    r"\b(?:Week|Module|Lecture|Handout)\s+\d+\s*[–-]\s*\d+\b"
)


def _external_links(text: str) -> list[str]:
    return MARKDOWN_LINK_RE.findall(text) + HTML_LINK_RE.findall(text)


def _visible_length(text: str, language: str) -> int:
    without_urls = re.sub(r"https://\S+", " ", text)
    if language == "zh":
        return len(CJK_RE.findall(without_urls))
    return len(LATIN_WORD_RE.findall(without_urls))


def _last_prose_block(text: str) -> str:
    blocks = [
        block.strip()
        for block in re.split(r"\n[ \t]*\n", text.strip())
        if block.strip()
    ]
    for block in reversed(blocks):
        if block.startswith(("#", "```", "~~~", "|")):
            continue
        return block
    return ""


def _normalized_long_paragraphs(body: str) -> list[str]:
    paragraphs: list[str] = []
    for raw in PARAGRAPH_SPLIT_RE.split(body):
        paragraph = raw.strip()
        if (
            not paragraph
            or paragraph.startswith("#")
            or paragraph.startswith("|")
            or paragraph.startswith(("```", "~~~"))
        ):
            continue
        paragraph = MARKDOWN_LINK_TARGET_RE.sub(r"\1", paragraph)
        paragraph = re.sub(r"[*_`~]", "", paragraph)
        paragraph = re.sub(r"\s+", " ", paragraph).strip().casefold()
        if len(paragraph) >= 180:
            paragraphs.append(paragraph)
    return paragraphs


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


def _learner_review_issues(
    record: Mapping[str, Any],
    *,
    source: str,
) -> list[Issue]:
    issues: list[Issue] = []
    status = record.get("editorial_status")
    record_level = record.get("evidence_level")
    reviews = record.get("learner_reviews")
    if not isinstance(reviews, list):
        return [
            Issue(
                "error",
                "guide.learner_reviews",
                "learner_reviews must be an array",
                source,
            )
        ]
    qualifying_reviews = [
        review
        for review in reviews
        if isinstance(review, Mapping)
        and review.get("relationship")
        in QUALIFYING_LEARNER_REVIEW_RELATIONSHIPS
    ]
    if status == "learner-reviewed" and not qualifying_reviews:
        issues.append(
            Issue(
                "error",
                "guide.review_missing",
                "learner-reviewed status requires an attributed report for the "
                "exact offering or another run of the same course",
                source,
            )
        )
    contextual_only = bool(reviews) and all(
        isinstance(review, Mapping)
        and review.get("relationship") == "successor-course"
        for review in reviews
    )
    if reviews and status != "learner-reviewed" and not (
        status == "researched" and contextual_only
    ):
        issues.append(
            Issue(
                "error",
                "guide.review_state",
                "attributed learner reports require learner-reviewed status unless "
                "every report is explicitly contextual successor-course evidence",
                source,
            )
        )
    if qualifying_reviews and record_level not in LEARNER_REVIEW_EVIDENCE_LEVELS:
        issues.append(
            Issue(
                "error",
                "guide.review_level",
                "attributed learner reports require R2, R3, or R4 record evidence",
                source,
            )
        )

    reviewed_at: date | None = None
    try:
        reviewed_at = date.fromisoformat(str(record.get("reviewed_at")))
    except ValueError:
        pass

    required_text_fields = ("coverage", "environment", "friction")
    required_fields = (
        "author",
        "url",
        "evidence_kind",
        "evidence_level",
        "relationship",
        "published_at",
        "completion_period",
        *required_text_fields,
    )
    for index, review in enumerate(reviews):
        review_source = f"{source}/learner_reviews/{index}"
        if not isinstance(review, Mapping):
            issues.append(
                Issue(
                    "error",
                    "guide.review_shape",
                    "learner review must be an object",
                    review_source,
                )
            )
            continue
        missing = [
            field
            for field in required_fields
            if field not in review
        ]
        if missing:
            issues.append(
                Issue(
                    "error",
                    "guide.review_shape",
                    "learner review is missing: " + ", ".join(missing),
                    review_source,
                )
            )
        for field in ("author", "completion_period"):
            value = review.get(field)
            if not isinstance(value, str) or not value.strip():
                issues.append(
                    Issue(
                        "error",
                        "guide.review_text",
                        f"{field} must be a nonempty string",
                        review_source,
                    )
                )
        url = review.get("url")
        if (
            not isinstance(url, str)
            or not re.fullmatch(r"https://\S+", url)
        ):
            issues.append(
                Issue(
                    "error",
                    "guide.review_url",
                    "learner report URL must use HTTPS",
                    review_source,
                )
            )
        if review.get("evidence_kind") != "first-person-report":
            issues.append(
                Issue(
                    "error",
                    "guide.review_kind",
                    "learner report evidence_kind must be first-person-report",
                    review_source,
                )
            )
        relationship = review.get("relationship")
        if relationship not in LEARNER_REVIEW_RELATIONSHIPS:
            issues.append(
                Issue(
                    "error",
                    "guide.review_relationship",
                    "relationship must be exact-offering, same-course-other-run, "
                    "or successor-course",
                    review_source,
                )
            )
        review_level = review.get("evidence_level")
        if review_level not in LEARNER_REVIEW_EVIDENCE_LEVELS:
            issues.append(
                Issue(
                    "error",
                    "guide.review_item_level",
                    "learner report evidence_level must be R2, R3, or R4",
                    review_source,
                )
            )
        elif (
            relationship in QUALIFYING_LEARNER_REVIEW_RELATIONSHIPS
            and record_level in EVIDENCE_LEVEL_RANK
            and EVIDENCE_LEVEL_RANK[review_level]
            > EVIDENCE_LEVEL_RANK[record_level]
        ):
            issues.append(
                Issue(
                    "error",
                    "guide.review_item_level",
                    "learner report evidence cannot exceed the record evidence level",
                    review_source,
                )
            )
        published_at: date | None = None
        try:
            published_at = date.fromisoformat(str(review.get("published_at")))
        except ValueError:
            issues.append(
                Issue(
                    "error",
                    "guide.review_date",
                    "published_at must be a valid ISO date",
                    review_source,
                )
            )
        if (
            published_at is not None
            and reviewed_at is not None
            and published_at > reviewed_at
        ):
            issues.append(
                Issue(
                    "error",
                    "guide.review_date",
                    "published_at cannot be later than reviewed_at",
                    review_source,
                )
            )
        for field in required_text_fields:
            bilingual = review.get(field)
            if not isinstance(bilingual, Mapping):
                issues.append(
                    Issue(
                        "error",
                        "guide.review_bilingual",
                        f"{field} must contain zh and en text",
                        review_source,
                    )
                )
                continue
            for language in ("zh", "en"):
                text = bilingual.get(language)
                if not isinstance(text, str) or not text.strip():
                    issues.append(
                        Issue(
                            "error",
                            "guide.review_bilingual",
                            f"{field}.{language} must be nonempty",
                            review_source,
                        )
                    )
        artifacts = review.get("artifacts", [])
        if not isinstance(artifacts, list):
            issues.append(
                Issue(
                    "error",
                    "guide.review_artifacts",
                    "artifacts must be an array",
                    review_source,
                )
            )
        elif (
            any(
                not isinstance(url, str)
                or not re.fullmatch(r"https://\S+", url)
                for url in artifacts
            )
            or len(artifacts) != len(set(artifacts))
        ):
            issues.append(
                Issue(
                    "error",
                    "guide.review_artifacts",
                    "artifacts must be unique HTTPS URLs",
                    review_source,
                )
            )
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
    first_content_line = next(
        (line.strip() for line in body.splitlines() if line.strip()),
        "",
    )
    if not first_content_line.startswith("## "):
        issues.append(
            Issue(
                "error",
                "guide.opening_h2",
                "course-guide fragments must begin with the H2 that will be "
                "folded into the generated course overview",
                relative,
            )
        )
    if any(level == 1 for level, _, _ in headings):
        issues.append(
            Issue(
                "error",
                "guide.h1",
                "course-guide fragments must not contain an H1",
                relative,
            )
        )
    singular_range = (
        SINGULAR_RANGE_LABEL_EN_RE.search(body)
        if language == "en"
        else None
    )
    if singular_range:
        issues.append(
            Issue(
                "error",
                "guide.range_label_agreement",
                (
                    f"multi-item range {singular_range.group(0)!r} uses a singular "
                    "label; write Weeks, Modules, Lectures, or Handouts before a "
                    "numeric range"
                ),
                relative,
            )
        )
    h2_count = sum(level == 2 for level, _, _ in headings)
    if h2_count < GUIDE_SECTION_MINIMUM:
        issues.append(
            Issue(
                "error",
                "guide.sections",
                (
                    "researched course guides require at least "
                    f"{GUIDE_SECTION_MINIMUM} H2 sections"
                ),
                relative,
            )
        )
    if h2_count > GUIDE_SECTION_MAXIMUM:
        issues.append(
            Issue(
                "error",
                "guide.section_sprawl",
                (
                    f"guide has {h2_count} H2 sections; consolidate to at most "
                    f"{GUIDE_SECTION_MAXIMUM} course-specific sections"
                ),
                relative,
            )
        )
    minimum, maximum = GUIDE_LENGTH_BOUNDS[language]
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
    if length > maximum:
        issues.append(
            Issue(
                "error",
                "guide.sprawl",
                (
                    f"guide has {length} visible "
                    f"{'CJK characters' if language == 'zh' else 'words'}; "
                    f"maximum is {maximum}. Keep the course judgment, distinctive "
                    "work, access limits, and one concrete learning exit; move the "
                    "remaining official links to the generated resource index"
                ),
                relative,
            )
        )
    links = _external_links(body)
    if not 3 <= len(links) <= 9:
        issues.append(
            Issue(
                "error",
                "guide.narrative_links",
                f"guide narrative requires 3–9 curated HTTPS links, found {len(links)}",
                relative,
            )
        )
    normalized_links = [normalize_url(url) for url in links]
    if len(normalized_links) != len(set(normalized_links)):
        issues.append(
            Issue(
                "error",
                "guide.duplicate_link",
                "guide narrative repeats an HTTPS destination; link it once and "
                "use the surrounding prose to explain why it matters",
                relative,
            )
        )
    review_match = INTERNAL_REVIEW_LANGUAGE[language].search(body)
    if review_match:
        issues.append(
            Issue(
                "error",
                "guide.internal_review_language",
                (
                    "learner-facing prose contains internal review or maintenance "
                    f"language: {review_match.group(0)!r}; keep evidence level and "
                    "review workflow in structured metadata"
                ),
                relative,
            )
        )
    brand_mentions = len(re.findall(r"\bEEDIY\b", body, flags=re.IGNORECASE))
    if brand_mentions > BRAND_MENTION_MAXIMUM:
        issues.append(
            Issue(
                "error",
                "guide.brand_overuse",
                (
                    f"learner-facing prose mentions EEDIY {brand_mentions} times; "
                    f"maximum is {BRAND_MENTION_MAXIMUM}"
                ),
                relative,
            )
        )
    protocol_tone_count = sum(
        len(pattern.findall(body))
        for pattern in PROTOCOL_TONE_PATTERNS[language]
    )
    protocol_tone_maximum = PROTOCOL_TONE_MAXIMUM[language]
    if protocol_tone_count > protocol_tone_maximum:
        issues.append(
            Issue(
                "error",
                "guide.protocol_tone_density",
                (
                    "learner-facing prose overuses archive/review/proof-of-work "
                    f"vocabulary ({protocol_tone_count} matches; maximum "
                    f"{protocol_tone_maximum}). Rewrite around the course's actual "
                    "choices, difficult ideas, and debugging moves instead of a "
                    "generic acceptance protocol"
                ),
                relative,
            )
        )
    ending = _last_prose_block(body)
    ending_match = ENDING_PROTOCOL[language].search(ending)
    if ending_match:
        issues.append(
            Issue(
                "error",
                "guide.protocol_ending",
                (
                    "guide ends with a correction or review protocol instead of "
                    f"course-specific learning advice: {ending_match.group(0)!r}"
                ),
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
    seen_paragraphs: dict[tuple[str, str], Path] = {}
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
            learner_reviews = []
        issues.extend(_learner_review_issues(record, source=record_path))
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
            for paragraph in _normalized_long_paragraphs(body):
                key = (language, paragraph)
                previous = seen_paragraphs.get(key)
                if previous is not None and previous != path:
                    issues.append(
                        Issue(
                            "error",
                            "guide.duplicate_paragraph",
                            (
                                "long learner-facing paragraph duplicates "
                                f"{display_path(previous)}"
                            ),
                            display_path(path),
                        )
                    )
                else:
                    seen_paragraphs[key] = path
        if heading_levels.get("zh") != heading_levels.get("en"):
            issues.append(
                Issue(
                    "error",
                    "guide.translation_structure",
                    "Chinese and English guide heading levels differ",
                    record_path,
                )
            )
        for review_index, review in enumerate(learner_reviews):
            if not isinstance(review, Mapping):
                continue
            review_url = review.get("url")
            if not isinstance(review_url, str):
                continue
            normalized_review_url = normalize_url(review_url)
            for language, body in bodies.items():
                body_links = {
                    normalize_url(url) for url in _external_links(body)
                }
                if normalized_review_url not in body_links:
                    issues.append(
                        Issue(
                            "error",
                            "guide.review_citation",
                            (
                                f"{language} guide must cite learner review "
                                f"{review_index + 1} in its narrative"
                            ),
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
