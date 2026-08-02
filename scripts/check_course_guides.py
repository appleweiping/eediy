from __future__ import annotations

import argparse
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median, pstdev
from typing import Any, Mapping
from urllib.parse import urlsplit

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.course_guides import (
    _external_links,
    _last_prose_block,
    _visible_length,
    load_course_guides,
)
from scripts.quality_common import (
    Issue,
    QualityError,
    emit_issues,
    exit_code,
    load_json,
    repo_path,
    markdown_headings,
    write_json_report,
)

DEEP_EDITORIAL_STATUSES = frozenset({"researched", "learner-reviewed"})
DEEP_MATERIAL_COVERAGE_FIELDS = (
    "video",
    "notes",
    "practice",
    "labs",
    "exams",
    "code",
)
PUBLIC_RESOURCE_ACCESS = frozenset(
    {"open", "open-registration", "free-audit", "limited-free"}
)
COVERAGE_RESOURCE_KINDS = {
    "video": frozenset({"video"}),
    "notes": frozenset({"notes", "textbook"}),
    "practice": frozenset({"assignments", "projects"}),
    "labs": frozenset({"labs", "projects", "simulator"}),
    "exams": frozenset({"exams"}),
    "code": frozenset({"code", "dataset", "simulator"}),
}
NON_CONTENT_ARTIFACT_SCOPES = frozenset(
    {"index", "outline", "landing", "syllabus"}
)
CORPUS_MEDIAN_ZH_MINIMUM = 400
CORPUS_MEDIAN_ZH_MAXIMUM = 850
CORPUS_P90_ZH_MAXIMUM = 1_200
CORPUS_LENGTH_CV_MINIMUM = 0.20
CORPUS_H2_MODE_SHARE_MAXIMUM = 0.70
CORPUS_DOMAIN_MEDIAN_MINIMUM = 2
CORPUS_TEMPLATE_PAGE_SHARE_MAXIMUM = {
    "中文先字流程": 0.25,
    "中文防御性否定": 0.25,
    "中文命令词": 0.25,
    "站点自称": 0.10,
    "统一入场诊断": 0.12,
    "统一结题收口": 0.10,
    "审核协议词": 0.15,
    "想象中的复核者": 0.05,
    "English protocol voice": 0.15,
}
CORPUS_HEADING_PAGE_SHARE_MAXIMUM = {
    "first H2 starts with 结论": 0.10,
    "an H2 starts with 用": 0.25,
}
CORPUS_PROTOCOL_ENDING_SHARE_MAXIMUM = 0.20
CORPUS_GOVERNANCE_ENDING_SHARE_MAXIMUM = 0.08
CORPUS_NORMATIVE_ENDING_SHARE_MAXIMUM = 0.25
PROTOCOL_ENDING_ZH_RE = re.compile(r"(?:记录|报告|交付|成果|产物)")
GOVERNANCE_ENDING_ZH_RE = re.compile(
    r"(?:证据(?:链|包)?|审计|验收|交付物|可追溯|冻结|声称|可复现|重跑|"
    r"留痕|记录包|成果包|完成标准|完成证据|学习闭环|课程闭环|评分闭环|真实闭环)"
)
NORMATIVE_ENDING_ZH_RE = re.compile(
    r"(?:必须|应当|应该|应能|应先|应写|应说明|应明确|应保留|应记录|"
    r"应完成|应使用|应把|应与|应从|应由|应只|应避免|应分别|应留|"
    r"应继续|应按|需要|不得|不应|结课时|学完时|结束时|完成标准|完成意味着)"
)
WORKFLOW_FIRST_ZH_RE = re.compile(r"(?<!优)先(?!修|后|前|验|导)")
TEMPLATE_PATTERNS_ZH = {
    "中文先字流程": WORKFLOW_FIRST_ZH_RE,
    "中文防御性否定": re.compile(r"(?:不是|不等于|而不是)"),
    "中文命令词": re.compile(r"(?:必须|不要|应当)"),
    "站点自称": re.compile(r"(?:\bEEDIY\b|本站|本页)", flags=re.IGNORECASE),
    "统一入场诊断": re.compile(
        r"(?:入场|开始前|先修诊断|准备检查|进入前|开课前)"
    ),
    "统一结题收口": re.compile(
        r"(?:课程出口|学习出口|结题|最终产物|成果包|退出条件|完成标准|结束时)"
    ),
    "审核协议词": re.compile(
        r"(?:冻结|(?:^|\W)gate(?:$|\W)|闸门|验收|版本签名|迁移矩阵|四栏|三栏)",
        flags=re.IGNORECASE,
    ),
    "想象中的复核者": re.compile(
        r"(?:另一(?:位|个)?(?:读者|人)|他人复现|新接手者|别人复现|独立复现)"
    ),
}
TEMPLATE_PATTERNS_EN = {
    "English protocol voice": re.compile(
        r"(?:entry (?:test|check|gate)|exit (?:condition|gate)|"
        r"(?:completion|final) package|another (?:reader|person|learner)|"
        r"EEDIY (?:supplement|exercise)|release gate|freeze gates?|"
        r"must be able to reproduce)",
        flags=re.IGNORECASE,
    ),
}


def _percentile(values: list[int], quantile: float) -> int:
    ordered = sorted(values)
    if not ordered:
        return 0
    index = max(0, math.ceil(quantile * len(ordered)) - 1)
    return ordered[index]


def _is_deep_guide(guide: Mapping[str, Any] | Any) -> bool:
    return (
        isinstance(guide, Mapping)
        and guide.get("editorial_status") in DEEP_EDITORIAL_STATUSES
    )


def _public_resource_records(course: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    resources = course.get("resources")
    if not isinstance(resources, list):
        return []
    return [
        resource
        for resource in resources
        if isinstance(resource, Mapping)
        and resource.get("access") in PUBLIC_RESOURCE_ACCESS
        and resource.get("status") == "available"
    ]


def _score_two_fields_without_public_content(
    coverage: Mapping[str, Any],
    resources: list[Mapping[str, Any]],
) -> tuple[str, ...]:
    """Return score-2 fields without matching, reachable substantive content.

    Historical resource records predate ``artifact_scope``. A missing scope is
    accepted only for a substantive kind such as an assignment PDF, lab,
    lecture, or repository. Course landing pages never corroborate a usable
    material set, and an explicit index/outline/landing/syllabus scope never
    does.
    """

    unsupported: list[str] = []
    for field, kinds in COVERAGE_RESOURCE_KINDS.items():
        if coverage.get(field) != 2:
            continue
        matched = False
        for resource in resources:
            if resource.get("kind") not in kinds:
                continue
            scope = resource.get("artifact_scope")
            if scope in NON_CONTENT_ARTIFACT_SCOPES:
                continue
            if scope is None or scope == "content":
                matched = True
                break
        if not matched:
            unsupported.append(field)
    return tuple(unsupported)


def deep_coursework_issues(
    catalogue: Mapping[str, Any],
    guides: Mapping[int, Mapping[str, Any]],
    *,
    source: str = "data/course_guides.json",
) -> list[Issue]:
    """Reject deep status when structured evidence has no usable public material.

    A coverage score of 2 represents a coherent reviewed set. Every field
    carrying that score needs a matching, publicly reachable, available
    resource that exposes substantive content. A score of 1 remains the honest
    label for a partial, version-mismatched, or access-restricted set whose
    existence may be documented by a provider landing page or syllabus.
    Indexes, outlines, landing pages, syllabi, paid/institutional resources,
    degraded/archived records, and suggested projects cannot substantiate a
    score of 2.
    """

    courses_by_id = {
        int(course["source_id"]): course
        for course in catalogue.get("courses", [])
        if isinstance(course, Mapping)
        and isinstance(course.get("source_id"), int)
        and not isinstance(course.get("source_id"), bool)
    }
    issues: list[Issue] = []
    for course_id, guide in sorted(guides.items()):
        if not _is_deep_guide(guide):
            continue
        course = courses_by_id.get(course_id)
        coverage = course.get("resource_coverage") if isinstance(course, Mapping) else None
        if not isinstance(coverage, Mapping):
            continue
        values = [coverage.get(field) for field in DEEP_MATERIAL_COVERAGE_FIELDS]
        if not all(
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            for value in values
        ):
            continue
        unsupported_fields = _score_two_fields_without_public_content(
            coverage,
            _public_resource_records(course),
        )
        if not unsupported_fields:
            continue
        issues.append(
            Issue(
                "error",
                "guide.deep_without_public_coursework",
                "every coverage score of 2 requires a matching, publicly "
                "reachable, available, content-scoped structured resource; "
                "degraded/archived, restricted/paid, index, outline, landing, "
                "or syllabus records do not count. Downgrade unsupported "
                "fields to the honest partial/restricted score of 1. "
                f"Unsupported fields: {', '.join(unsupported_fields)}",
                source,
                context=f"{course_id:03d}",
            )
        )
    return issues


def corpus_style_issues(
    catalogue: Mapping[str, Any],
    guides: Mapping[int, Mapping[str, Any]],
    *,
    source: str = "data/course_guides.json",
) -> tuple[list[Issue], dict[str, Any]]:
    zh_documents: list[tuple[int, str]] = []
    en_documents: dict[int, str] = {}
    for course_id, guide in guides.items():
        bodies = guide.get("bodies") if isinstance(guide, Mapping) else None
        body = bodies.get("zh") if isinstance(bodies, Mapping) else None
        if isinstance(body, str) and body.strip():
            zh_documents.append((course_id, body))
        en_body = bodies.get("en") if isinstance(bodies, Mapping) else None
        if isinstance(en_body, str) and en_body.strip():
            en_documents[course_id] = en_body

    lengths = [_visible_length(body, "zh") for _, body in zh_documents]
    h2_counts = [
        sum(level == 2 for level, _, _ in markdown_headings(body))
        for _, body in zh_documents
    ]
    domain_counts: list[int] = []
    template_counts = Counter()
    template_ids: dict[str, list[int]] = defaultdict(list)
    heading_pattern_counts = Counter()
    heading_pattern_ids: dict[str, list[int]] = defaultdict(list)
    protocol_ending_ids: list[int] = []
    governance_ending_ids: list[int] = []
    normative_ending_ids: list[int] = []
    for course_id, body in zh_documents:
        urls = list(dict.fromkeys(_external_links(body)))
        domains = {
            urlsplit(url).netloc.casefold().removeprefix("www.")
            for url in urls
            if urlsplit(url).netloc
        }
        domain_counts.append(len(domains))
        for label, pattern in TEMPLATE_PATTERNS_ZH.items():
            if pattern.search(body):
                template_counts[label] += 1
                template_ids[label].append(course_id)
        h2_titles = [
            title.strip()
            for level, title, _ in markdown_headings(body)
            if level == 2
        ]
        if h2_titles and h2_titles[0].startswith("结论"):
            label = "first H2 starts with 结论"
            heading_pattern_counts[label] += 1
            heading_pattern_ids[label].append(course_id)
        if any(title.startswith("用") for title in h2_titles):
            label = "an H2 starts with 用"
            heading_pattern_counts[label] += 1
            heading_pattern_ids[label].append(course_id)
        last_prose_block = _last_prose_block(body)
        if PROTOCOL_ENDING_ZH_RE.search(last_prose_block):
            protocol_ending_ids.append(course_id)
        if GOVERNANCE_ENDING_ZH_RE.search(last_prose_block):
            governance_ending_ids.append(course_id)
        if NORMATIVE_ENDING_ZH_RE.search(last_prose_block):
            normative_ending_ids.append(course_id)
        en_body = en_documents.get(course_id, "")
        for label, pattern in TEMPLATE_PATTERNS_EN.items():
            if pattern.search(en_body):
                template_counts[label] += 1
                template_ids[label].append(course_id)

    document_count = len(zh_documents)
    median_length = float(median(lengths)) if lengths else 0.0
    p90_length = _percentile(lengths, 0.90)
    mean_length = sum(lengths) / len(lengths) if lengths else 0.0
    length_cv = pstdev(lengths) / mean_length if len(lengths) > 1 and mean_length else 0.0
    h2_mode_share = (
        max(Counter(h2_counts).values()) / len(h2_counts) if h2_counts else 0.0
    )
    median_domains = float(median(domain_counts)) if domain_counts else 0.0
    template_shares = {
        key: template_counts[key] / document_count if document_count else 0.0
        for key in CORPUS_TEMPLATE_PAGE_SHARE_MAXIMUM
    }
    heading_pattern_shares = {
        key: heading_pattern_counts[key] / document_count if document_count else 0.0
        for key in CORPUS_HEADING_PAGE_SHARE_MAXIMUM
    }
    protocol_ending_share = (
        len(protocol_ending_ids) / document_count if document_count else 0.0
    )
    governance_ending_share = (
        len(governance_ending_ids) / document_count if document_count else 0.0
    )
    normative_ending_share = (
        len(normative_ending_ids) / document_count if document_count else 0.0
    )
    statistics: dict[str, Any] = {
        "guide_zh_median_cjk": round(median_length, 1),
        "guide_zh_p90_cjk": p90_length,
        "guide_zh_length_cv": round(length_cv, 3),
        "guide_h2_mode_share": round(h2_mode_share, 3),
        "guide_median_unique_domains": round(median_domains, 1),
        "guide_template_page_shares": {
            key: round(value, 3) for key, value in template_shares.items()
        },
        "guide_template_page_ids": {
            key: sorted(template_ids[key])
            for key in CORPUS_TEMPLATE_PAGE_SHARE_MAXIMUM
        },
        "guide_heading_pattern_page_shares": {
            key: round(value, 3)
            for key, value in heading_pattern_shares.items()
        },
        "guide_heading_pattern_page_ids": {
            key: sorted(heading_pattern_ids[key])
            for key in CORPUS_HEADING_PAGE_SHARE_MAXIMUM
        },
        "guide_protocol_ending_share": round(protocol_ending_share, 3),
        "guide_protocol_ending_ids": sorted(protocol_ending_ids),
        "guide_governance_ending_share": round(governance_ending_share, 3),
        "guide_governance_ending_ids": sorted(governance_ending_ids),
        "guide_normative_ending_share": round(normative_ending_share, 3),
        "guide_normative_ending_ids": sorted(normative_ending_ids),
    }

    # Corpus ratios become meaningful once there is more than one authored
    # guide. They are deliberately independent of the catalogue's current
    # size so adding or removing a legitimate course cannot switch the gate on
    # or off.
    if document_count < 2:
        return [], statistics

    issues: list[Issue] = []
    if not CORPUS_MEDIAN_ZH_MINIMUM <= median_length <= CORPUS_MEDIAN_ZH_MAXIMUM:
        issues.append(
            Issue(
                "error",
                "guide.corpus_median_length",
                f"Chinese guide median is {median_length:.0f} CJK; expected "
                f"{CORPUS_MEDIAN_ZH_MINIMUM}–{CORPUS_MEDIAN_ZH_MAXIMUM}",
                source,
            )
        )
    if p90_length > CORPUS_P90_ZH_MAXIMUM:
        issues.append(
            Issue(
                "error",
                "guide.corpus_p90_length",
                f"Chinese guide p90 is {p90_length} CJK; maximum is "
                f"{CORPUS_P90_ZH_MAXIMUM}",
                source,
            )
        )
    if length_cv < CORPUS_LENGTH_CV_MINIMUM:
        issues.append(
            Issue(
                "error",
                "guide.corpus_length_rhythm",
                f"Chinese guide length CV is {length_cv:.3f}; minimum is "
                f"{CORPUS_LENGTH_CV_MINIMUM:.2f}. Short courses should stay short "
                "and only unusually complex courses should run long.",
                source,
            )
        )
    if h2_mode_share > CORPUS_H2_MODE_SHARE_MAXIMUM:
        issues.append(
            Issue(
                "error",
                "guide.corpus_heading_rhythm",
                f"one H2 count is used by {h2_mode_share:.1%} of guides; maximum "
                f"is {CORPUS_H2_MODE_SHARE_MAXIMUM:.0%}",
                source,
            )
        )
    if median_domains < CORPUS_DOMAIN_MEDIAN_MINIMUM:
        issues.append(
            Issue(
                "error",
                "guide.corpus_domain_diversity",
                f"median narrative domain count is {median_domains:.1f}; minimum "
                f"is {CORPUS_DOMAIN_MEDIAN_MINIMUM}",
                source,
            )
        )
    for label, maximum in CORPUS_TEMPLATE_PAGE_SHARE_MAXIMUM.items():
        share = template_shares[label]
        if share > maximum:
            issues.append(
                Issue(
                    "error",
                    "guide.corpus_template_vocabulary",
                    f"{label!r} appears in {share:.1%} of the guide corpus; maximum "
                    f"is {maximum:.0%}",
                    source,
                    context=label,
                )
            )
    for label, maximum in CORPUS_HEADING_PAGE_SHARE_MAXIMUM.items():
        share = heading_pattern_shares[label]
        if share > maximum:
            issues.append(
                Issue(
                    "error",
                    "guide.corpus_heading_template",
                    f"{label!r} appears in {share:.1%} of the guide corpus; maximum "
                    f"is {maximum:.0%}",
                    source,
                    context=label,
                )
            )
    if protocol_ending_share > CORPUS_PROTOCOL_ENDING_SHARE_MAXIMUM:
        issues.append(
            Issue(
                "error",
                "guide.corpus_protocol_endings",
                "too many guides end in report/record/deliverable language "
                f"({protocol_ending_share:.1%}; maximum "
                f"{CORPUS_PROTOCOL_ENDING_SHARE_MAXIMUM:.0%}); end with a "
                "course-specific judgment, difficult idea, or next-course choice",
                source,
                context=", ".join(f"{course_id:03d}" for course_id in protocol_ending_ids),
            )
        )
    if governance_ending_share > CORPUS_GOVERNANCE_ENDING_SHARE_MAXIMUM:
        issues.append(
            Issue(
                "error",
                "guide.corpus_governance_endings",
                "too many guides end in audit/evidence/acceptance language "
                f"({governance_ending_share:.1%}; maximum "
                f"{CORPUS_GOVERNANCE_ENDING_SHARE_MAXIMUM:.0%}); name the "
                "course-specific decision, failure, or tradeoff instead",
                source,
                context=", ".join(
                    f"{course_id:03d}" for course_id in governance_ending_ids
                ),
            )
        )
    if normative_ending_share > CORPUS_NORMATIVE_ENDING_SHARE_MAXIMUM:
        issues.append(
            Issue(
                "error",
                "guide.corpus_normative_endings",
                "too many guides end as requirements or completion rules "
                f"({normative_ending_share:.1%}; maximum "
                f"{CORPUS_NORMATIVE_ENDING_SHARE_MAXIMUM:.0%}); prefer a "
                "course-specific judgment or next choice",
                source,
                context=", ".join(
                    f"{course_id:03d}" for course_id in normative_ending_ids
                ),
            )
        )
    return issues, statistics


def track_coverage_issues(
    catalogue: Mapping[str, Any],
    guides: Mapping[int, Mapping[str, Any]],
    *,
    source: str = "data/course_guides.json",
) -> tuple[list[Issue], dict[str, int]]:
    courses = [
        course
        for course in catalogue.get("courses", [])
        if isinstance(course, Mapping)
        and isinstance(course.get("source_id"), int)
        and isinstance(course.get("track"), str)
    ]
    populated_tracks = {str(course["track"]) for course in courses}
    course_tracks = {
        int(course["source_id"]): str(course["track"]) for course in courses
    }
    deep_guide_ids = {
        course_id for course_id, guide in guides.items() if _is_deep_guide(guide)
    }
    covered_tracks = {
        course_tracks[course_id]
        for course_id in deep_guide_ids
        if course_id in course_tracks
    }
    missing = sorted(populated_tracks - covered_tracks)
    issues = []
    if missing:
        issues.append(
            Issue(
                "error",
                "guide.track_coverage",
                f"{len(missing)} populated track(s) lack a deep guide",
                source,
                context=", ".join(missing),
            )
        )
    return issues, {
        "tracks_populated": len(populated_tracks),
        "tracks_deep_covered": len(covered_tracks),
    }


def mainline_guide_coverage_issues(
    mainline_audit: Mapping[str, Any] | None,
    guides: Mapping[int, Mapping[str, Any]],
    *,
    source: str = "data/course_guides.json",
    audit_source: str = "data/mainline_audit.json",
) -> tuple[list[Issue], dict[str, int]]:
    records = (
        mainline_audit.get("audits")
        if isinstance(mainline_audit, Mapping)
        else None
    )
    if not isinstance(records, list):
        return [
            Issue(
                "error",
                "guide.mainline_audit_shape",
                "mainline audit must contain an audits array",
                audit_source,
            )
        ], {
            "mainlines_audited": 0,
            "mainlines_deep_covered": 0,
        }

    audited_ids = {
        int(record["course_id"])
        for record in records
        if isinstance(record, Mapping)
        and isinstance(record.get("course_id"), int)
        and not isinstance(record.get("course_id"), bool)
    }
    if not audited_ids:
        return [
            Issue(
                "error",
                "guide.mainline_audit_empty",
                "mainline audit contains no valid course IDs",
                audit_source,
            )
        ], {
            "mainlines_audited": 0,
            "mainlines_deep_covered": 0,
        }

    deep_guide_ids = {
        course_id for course_id, guide in guides.items() if _is_deep_guide(guide)
    }
    covered_ids = audited_ids & deep_guide_ids
    missing = sorted(audited_ids - covered_ids)
    issues: list[Issue] = []
    if missing:
        issues.append(
            Issue(
                "error",
                "guide.mainline_coverage",
                f"{len(missing)} audited mainline course(s) lack a deep guide",
                source,
                context=", ".join(f"{course_id:03d}" for course_id in missing),
            )
        )
    return issues, {
        "mainlines_audited": len(audited_ids),
        "mainlines_deep_covered": len(covered_ids),
    }


def release_gate_issues(
    catalogue: Mapping[str, Any],
    guides: Mapping[int, Mapping[str, Any]],
    *,
    mainline_audit: Mapping[str, Any] | None = None,
    require_track_coverage: bool = True,
    require_mainline_coverage: bool = True,
    source: str = "data/course_guides.json",
    audit_source: str = "data/mainline_audit.json",
) -> tuple[list[Issue], dict[str, int]]:
    issues = deep_coursework_issues(catalogue, guides, source=source)
    authored_count = len(guides)
    deep_count = sum(_is_deep_guide(guide) for guide in guides.values())
    catalogue_count = sum(
        isinstance(guide, Mapping) and guide.get("editorial_status") == "catalogue"
        for guide in guides.values()
    )
    coverage_issues, coverage = track_coverage_issues(
        catalogue,
        guides,
        source=source,
    )
    if require_track_coverage:
        issues.extend(coverage_issues)
    mainline_issues, mainline_coverage = mainline_guide_coverage_issues(
        mainline_audit,
        guides,
        source=source,
        audit_source=audit_source,
    )
    if require_mainline_coverage:
        issues.extend(mainline_issues)
    return issues, {
        "authored_guides": authored_count,
        "deep_guides": deep_count,
        "catalogue_guides": catalogue_count,
        **coverage,
        **mainline_coverage,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Validate authored bilingual course records, deep-guide coverage, "
            "and evidence boundaries."
        )
    )
    parser.add_argument("--catalogue", default="data/courses.json")
    parser.add_argument("--manifest", default="data/course_guides.json")
    parser.add_argument("--mainline-audit", default="data/mainline_audit.json")
    parser.add_argument("--schema", default="data/course-guide.schema.json")
    coverage = parser.add_mutually_exclusive_group()
    coverage.add_argument(
        "--require-track-coverage",
        dest="require_track_coverage",
        action="store_true",
        help="require at least one deep guide in every populated track (default)",
    )
    coverage.add_argument(
        "--allow-partial-track-coverage",
        dest="require_track_coverage",
        action="store_false",
        help="development-only escape hatch for deliberately partial fixtures",
    )
    parser.set_defaults(require_track_coverage=True)
    mainline_coverage = parser.add_mutually_exclusive_group()
    mainline_coverage.add_argument(
        "--require-mainline-coverage",
        dest="require_mainline_coverage",
        action="store_true",
        help="require a deep guide for every independently audited mainline course (default)",
    )
    mainline_coverage.add_argument(
        "--allow-partial-mainline-coverage",
        dest="require_mainline_coverage",
        action="store_false",
        help="development-only escape hatch for deliberately partial fixtures",
    )
    parser.set_defaults(require_mainline_coverage=True)
    parser.add_argument("--json-report")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        catalogue = load_json(repo_path(args.catalogue))
    except (OSError, QualityError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    mainline_audit: Mapping[str, Any] | None = None
    if args.require_mainline_coverage:
        try:
            mainline_audit = load_json(repo_path(args.mainline_audit))
        except (OSError, QualityError) as exc:
            print(str(exc), file=sys.stderr)
            return 1
    guides, issues = load_course_guides(
        repo_path(args.manifest),
        catalogue,
        repo_path(args.schema),
    )
    release_issues, statistics = release_gate_issues(
        catalogue,
        guides,
        mainline_audit=mainline_audit,
        require_track_coverage=args.require_track_coverage,
        require_mainline_coverage=args.require_mainline_coverage,
        source=args.manifest,
        audit_source=args.mainline_audit,
    )
    style_issues, style_statistics = corpus_style_issues(
        catalogue,
        guides,
        source=args.manifest,
    )
    issues.extend(release_issues)
    issues.extend(style_issues)
    statistics = {**statistics, **style_statistics}
    emit_issues(issues)
    print(
        f"Course records: {statistics['authored_guides']} authored bilingual; "
        f"{statistics['deep_guides']} deep; "
        f"{statistics['catalogue_guides']} catalogue; "
        f"deep coverage in {statistics['tracks_deep_covered']}/"
        f"{statistics['tracks_populated']} populated tracks and "
        f"{statistics['mainlines_deep_covered']}/"
        f"{statistics['mainlines_audited']} audited mainlines; "
        f"median {statistics['guide_zh_median_cjk']:.0f} CJK; "
        f"p90 {statistics['guide_zh_p90_cjk']} CJK"
    )
    write_json_report(
        repo_path(args.json_report) if args.json_report else None,
        {
            "ok": exit_code(issues) == 0,
            **statistics,
            "issues": [issue.to_dict() for issue in issues],
        },
    )
    return exit_code(issues)


if __name__ == "__main__":
    raise SystemExit(main())
