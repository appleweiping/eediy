from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence
from urllib.parse import unquote, urlsplit

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.course_data import ROLE_TEXT, catalogue_statistics, normalize_url
from scripts.course_guides import _external_links, load_course_guides
from scripts.track_guides import load_track_guides
from scripts.quality_common import (
    Issue,
    QualityError,
    atomic_write,
    display_path,
    emit_issues,
    ensure_within,
    exit_code,
    load_json,
    repo_path,
    sha256_text,
    stable_json,
    write_json_report,
)
from scripts.validate_courses import validate_file
from scripts.validate_routes import validate_route_files


GENERATED_MARKER = "<!-- generated-by: scripts/generate_course_pages.py"
GROUP_TITLES = {
    "foundations": ("数理与工程基础", "Mathematical and Engineering Foundations"),
    "core": ("电子工程核心", "Electrical Engineering Core"),
    "systems": ("数字、嵌入式与计算系统", "Digital, Embedded, and Computing Systems"),
    "waves": ("信号、通信与电磁", "Signals, Communications, and Electromagnetics"),
    "devices": ("器件、芯片与微纳", "Devices, Integrated Circuits, and Micro/Nano"),
    "energy": ("电能与可持续能源", "Electric Energy and Sustainability"),
    "practice": ("仪器、设计与跨学科实践", "Instrumentation, Design, and Practice"),
}
ROLE_LABELS = {
    "mainline": ("主课", "Main course"),
    "alternative": ("可替代", "Alternative"),
    "supplement": ("补充材料", "Supplement"),
}
LEVEL_LABELS = {
    "introductory": ("入门", "Introductory"),
    "intermediate": ("中级", "Intermediate"),
    "advanced": ("进阶", "Advanced"),
    "mixed": ("混合", "Mixed"),
    "unspecified": ("提供方未标准化（请按先修判断）", "Not standardized by provider (use prerequisites)"),
}
ACCESS_LABELS = {
    "open": ("无需注册公开访问", "Open access"),
    "open-registration": ("注册后访问", "Registration required"),
    "free-audit": ("可免费旁听", "Free audit"),
    "limited-free": ("部分免费", "Limited free access"),
    "paid": ("付费", "Paid"),
    "institutional": ("机构权限", "Institutional access"),
}
STATUS_LABELS = {
    "available": ("官方页已列出", "Listed by official page"),
    "degraded": ("部分受限", "Degraded"),
    "archived": ("归档", "Archived"),
    "unavailable": ("不可访问", "Unavailable"),
    "review-needed": ("链接或范围待确认", "Access or scope not confirmed"),
}
COVERAGE_LABELS = {
    0: ("本次未核到", "Not verified in this review"),
    1: ("部分或受限", "Partial or restricted"),
    2: ("可用材料集合", "Usable material set"),
}
PRACTICE_COVERAGE_LABELS = {
    0: ("未核到公开练习", "No public practice found"),
    1: ("部分开放或受限", "Partial or restricted"),
    2: ("有公开作业或实验", "Public assignments or labs"),
}
COVERAGE_NAMES = {
    "video": ("视频", "Video"),
    "notes": ("讲义与阅读", "Notes and readings"),
    "practice": ("练习与作业", "Practice and assignments"),
    "labs": ("实验", "Labs"),
    "exams": ("考试", "Exams"),
    "code": ("代码、数据与设计文件", "Code, data, and design files"),
}


def _yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _safe(value: Any) -> str:
    return html.escape(str(value), quote=False).replace("|", r"\|").replace("\n", " ")


def mainline_audit_annotations(
    value: Any,
    catalogue: Mapping[str, Any],
    *,
    source: str = "data/mainline_audit.json",
) -> tuple[dict[int, Mapping[str, Any]], list[Issue]]:
    records = value.get("audits") if isinstance(value, Mapping) else None
    if not isinstance(records, list):
        return {}, [
            Issue(
                "error",
                "generated.mainline_audit_shape",
                "mainline audit must contain an audits array",
                source,
            )
        ]
    courses_by_source = {
        course["source_id"]: course
        for course in catalogue.get("courses", [])
        if isinstance(course, Mapping)
    }
    expected = {
        course_id
        for course_id, course in courses_by_source.items()
        if course.get("role") == "mainline"
    }
    annotations: dict[int, Mapping[str, Any]] = {}
    issues: list[Issue] = []
    for index, record in enumerate(records):
        path = f"{source}:/audits/{index}"
        if not isinstance(record, Mapping):
            issues.append(
                Issue(
                    "error",
                    "generated.mainline_audit_item",
                    "audit record must be an object",
                    path,
                )
            )
            continue
        course_id = record.get("course_id")
        if not isinstance(course_id, int) or isinstance(course_id, bool):
            issues.append(
                Issue(
                    "error",
                    "generated.mainline_audit_course",
                    "audit course_id must be an integer",
                    path,
                )
            )
            continue
        if course_id in annotations:
            issues.append(
                Issue(
                    "error",
                    "generated.mainline_audit_duplicate",
                    f"duplicate audit for course_id {course_id}",
                    path,
                )
            )
            continue
        if course_id not in expected:
            issues.append(
                Issue(
                    "error",
                    "generated.mainline_audit_scope",
                    f"course_id {course_id} is not a canonical mainline course",
                    path,
                )
            )
        if record.get("status") not in {"pass", "review"}:
            issues.append(
                Issue(
                    "error",
                    "generated.mainline_audit_status",
                    f"unsupported audit status {record.get('status')!r}",
                    path,
                )
            )
        for key in ("limitation_zh", "limitation_en", "verified_at"):
            if not isinstance(record.get(key), str) or not record[key].strip():
                issues.append(
                    Issue(
                        "error",
                        "generated.mainline_audit_text",
                        f"{key} must be non-empty",
                        path,
                    )
                )
        annotations[course_id] = record
    missing = expected.difference(annotations)
    if missing:
        issues.append(
            Issue(
                "error",
                "generated.mainline_audit_missing",
                f"missing audits for mainline course_ids {sorted(missing)}",
                source,
            )
        )
    return annotations, issues


def _front_matter(
    title: str,
    description: str,
    page_type: str,
    extra: Mapping[str, Any] | None = None,
) -> str:
    lines = [
        "---",
        f"title: {_yaml_string(title)}",
        f"description: {_yaml_string(description)}",
        f"page_type: {page_type}",
    ]
    for key, value in (extra or {}).items():
        if isinstance(value, bool):
            rendered = "true" if value else "false"
        elif isinstance(value, (int, float)):
            rendered = str(value)
        else:
            rendered = _yaml_string(str(value))
        lines.append(f"{key}: {rendered}")
    return "\n".join([*lines, "---", ""]) + "\n"


def _marker(source_payload: Any) -> str:
    fingerprint = sha256_text(stable_json(source_payload))[:16]
    return f"{GENERATED_MARKER}; fingerprint: {fingerprint} -->\n\n"


def _course_href(course: Mapping[str, Any], language: str, *, from_route: bool = False) -> str:
    prefix = "../courses" if from_route else "."
    return f"{prefix}/{course['track']}/{course['slug']}.md"


def _course_sort_key(course: Mapping[str, Any]) -> tuple[int, int, int]:
    role_order = {"mainline": 0, "alternative": 1, "supplement": 2}
    tier_order = {"S": 0, "A": 1, "B": 2}
    return (
        role_order.get(str(course.get("role")), 9),
        tier_order.get(str(course.get("tier")), 9),
        int(course.get("source_id", 999999)),
    )


def _prerequisite_guidance(
    course: Mapping[str, Any],
    language: str,
) -> tuple[list[str], list[str]]:
    official_value = course.get("official_prerequisites")
    recommended_value = course.get("recommended_background")
    if isinstance(official_value, Mapping) and isinstance(
        official_value.get(language), list
    ) and isinstance(recommended_value, Mapping) and isinstance(
        recommended_value.get(language), list
    ):
        return (
            [str(item) for item in official_value[language] if str(item).strip()],
            [str(item) for item in recommended_value[language] if str(item).strip()],
        )

    # Backward-compatible split for fixtures and older catalogues. Canonical
    # builds always carry the two explicit fields above.
    legacy = [
        str(item)
        for item in course.get("prerequisites", {}).get(language, [])
        if str(item).strip()
    ]
    recommended_prefixes = (
        ("建议先完成方向基础：", "建议背景：")
        if language == "zh"
        else ("Recommended foundation:", "Recommended background:")
    )
    recommended = [
        item for item in legacy if item.startswith(recommended_prefixes)
    ]
    official = [
        item for item in legacy if not item.startswith(recommended_prefixes)
    ]
    return official, recommended


def _render_prerequisites(
    course: Mapping[str, Any],
    courses_by_source: Mapping[int, Mapping[str, Any]],
    language: str,
) -> str:
    official_items, recommended_items = _prerequisite_guidance(course, language)
    prerequisite_ids = list(course.get("prerequisite_course_ids", []))
    # course_data._course_prerequisite_sections deterministically appends exact
    # course-sequence requirements to the provider section. Replace those plain
    # entries with internal links without touching an adjacent provider note.
    provider_items = (
        official_items[: -len(prerequisite_ids)]
        if prerequisite_ids
        else official_items
    )
    official_lines = [f"- {_safe(item)}" for item in provider_items]
    for prerequisite_id in prerequisite_ids:
        prerequisite = courses_by_source[prerequisite_id]
        href = f"../{prerequisite['track']}/{prerequisite['slug']}.md"
        linked_title = (
            f"[《{_safe(prerequisite['title']['zh'])}》]({href})"
            if language == "zh"
            else f"[{_safe(prerequisite['title']['en'])}]({href})"
        )
        if language == "zh":
            official_lines.append(
                f"- 课程顺序要求：先完成{linked_title}"
                f"（{_safe(prerequisite['institution'])} "
                f"{_safe(prerequisite['course_code'])}）"
            )
        else:
            official_lines.append(
                f"- Course-sequence requirement: complete {linked_title} "
                f"({_safe(prerequisite['institution'])} "
                f"{_safe(prerequisite['course_code'])}) first"
            )
    if not official_lines:
        official_lines = [
            (
                "- 本次未核到提供方公布的硬性先修；开始前仍应复核课程主页。"
                if language == "zh"
                else (
                    "- No provider-published hard prerequisite was verified in this "
                    "review; recheck the course page before starting."
                )
            )
        ]
    recommended_lines = [f"- {_safe(item)}" for item in recommended_items]
    if not recommended_lines:
        recommended_lines = [
            (
                "- 本站未在提供方要求之外另设准备条件。"
                if language == "zh"
                else "- EEDIY adds no preparation requirement beyond the provider section."
            )
        ]
    official_heading = (
        "**官方先修（提供方）**"
        if language == "zh"
        else "**Official prerequisites (provider)**"
    )
    recommended_heading = (
        "**本站建议背景**"
        if language == "zh"
        else "**EEDIY recommended background**"
    )
    return (
        f"{official_heading}\n\n"
        + "\n".join(official_lines)
        + f"\n\n{recommended_heading}\n\n"
        + "\n".join(recommended_lines)
    )


RESOURCE_KIND_LABELS = {
    "course": ("课程主页", "Course home"),
    "video": ("视频", "Videos"),
    "notes": ("讲义", "Notes"),
    "textbook": ("教材", "Textbook"),
    "assignments": ("作业", "Assignments"),
    "labs": ("实验", "Labs"),
    "projects": ("项目", "Projects"),
    "exams": ("考试", "Exams"),
    "code": ("代码", "Code"),
    "dataset": ("数据集", "Dataset"),
    "simulator": ("仿真器", "Simulator"),
    "community": ("社区", "Community"),
    "other": ("其他", "Other"),
}
EDITORIAL_STATUS_LABELS = {
    "catalogue": (
        "资料索引；不是完整课程替代",
        "Catalogue only; not a complete course substitute",
    ),
    "researched": ("公开材料导读", "Public-material guide"),
    "learner-reviewed": ("学习者复核", "Learner-reviewed"),
}
EDITORIAL_RELATIONSHIP_LABELS = {
    ("learner-reviewed", "exact-offering"): (
        "学习者复核（对应开课）",
        "Learner-reviewed (exact offering)",
    ),
    ("learner-reviewed", "same-course-other-run"): (
        "学习者复核（同课另一轮次）",
        "Learner-reviewed (another run of the same course)",
    ),
    ("researched", "successor-course"): (
        "公开材料导读；后继课程复盘仅作背景",
        "Public-material guide; successor-course report is contextual only",
    ),
}


def _review_relationship(guide: Mapping[str, Any] | None) -> str | None:
    if not guide:
        return None
    relationships = {
        str(review.get("relationship"))
        for review in guide.get("learner_reviews", [])
        if isinstance(review, Mapping) and review.get("relationship")
    }
    for relationship in (
        "exact-offering",
        "same-course-other-run",
        "successor-course",
    ):
        if relationship in relationships:
            return relationship
    return None


def _editorial_evidence_label(
    editorial_status: str,
    language: str,
    *,
    review_relationship: str | None = None,
) -> str:
    labels = EDITORIAL_RELATIONSHIP_LABELS.get(
        (editorial_status, review_relationship),
        EDITORIAL_STATUS_LABELS.get(
            editorial_status,
            EDITORIAL_STATUS_LABELS["catalogue"],
        ),
    )
    return labels[0 if language == "zh" else 1]


def _resource_access_summary(course: Mapping[str, Any], language: str) -> str:
    resources = [
        resource
        for resource in course.get("resources", [])
        if resource.get("status") != "unavailable"
    ]
    access_values = {
        str(resource.get("access"))
        for resource in resources
        if isinstance(resource, Mapping)
    }
    if language == "zh":
        if not access_values:
            return "本次未核到可用入口"
        if access_values == {"open"}:
            return "无需注册公开访问"
        if access_values <= {"open-registration"}:
            return "需注册；可用范围以平台为准"
        if access_values <= {"free-audit"}:
            return "可免费旁听；作业与证书范围另核"
        if access_values <= {"limited-free"}:
            return "仅部分内容免费"
        if access_values <= {"paid"}:
            return "需付费访问"
        if access_values <= {"institutional"}:
            return "需机构权限"
        if "open" in access_values and "institutional" in access_values:
            return "公开入口；部分材料需机构权限"
        if "open" in access_values and "paid" in access_values:
            return "公开入口；部分材料需付费"
        if "open" in access_values and access_values.intersection(
            {"open-registration", "free-audit", "limited-free"}
        ):
            return "公开入口；部分材料需注册或受限"
        return "混合访问条件；详见资源表"
    if not access_values:
        return "No usable entry verified"
    if access_values == {"open"}:
        return "Open without registration"
    if access_values <= {"open-registration"}:
        return "Registration required; scope varies by platform"
    if access_values <= {"free-audit"}:
        return "Free audit; assignment and certificate scope varies"
    if access_values <= {"limited-free"}:
        return "Only part of the material is free"
    if access_values <= {"paid"}:
        return "Paid access required"
    if access_values <= {"institutional"}:
        return "Institutional access required"
    if "open" in access_values and "institutional" in access_values:
        return "Open entry; some materials require institutional access"
    if "open" in access_values and "paid" in access_values:
        return "Open entry; some materials are paid"
    if "open" in access_values and access_values.intersection(
        {"open-registration", "free-audit", "limited-free"}
    ):
        return "Open entry; some materials require registration or are limited"
    return "Mixed access conditions; see the resource table"


def _course_metadata(
    course: Mapping[str, Any],
    language: str,
    *,
    reviewed_at: str,
    editorial_status: str,
    review_relationship: str | None = None,
) -> str:
    index = 0 if language == "zh" else 1
    separator = "：" if language == "zh" else ":"
    labels = (
        {
            "institution": "所属大学",
            "code": "课程编号",
            "official_prerequisites": "官方先修",
            "recommended_background": "本站建议背景",
            "resources": "访问条件",
            "reviewed": "资料状态",
        }
        if language == "zh"
        else {
            "institution": "University",
            "code": "Course code",
            "official_prerequisites": "Official prerequisites",
            "recommended_background": "EEDIY preparation",
            "resources": "Access",
            "reviewed": "Material status",
        }
    )
    official_items, recommended_items = _prerequisite_guidance(course, language)
    prerequisite_ids = list(course.get("prerequisite_course_ids", []))
    provider_items = (
        official_items[: -len(prerequisite_ids)]
        if prerequisite_ids and len(official_items) >= len(prerequisite_ids)
        else official_items
    )
    # The canonical provider note already names the formal requirement. The
    # trailing sequence entries exist to create internal links in catalogue
    # pages; repeating both forms in this compact metadata row obscures the
    # actual rule.
    official_display_items = provider_items or official_items
    official_prerequisites = [
        _safe(str(item)) for item in official_display_items if str(item).strip()
    ]
    official = (
        ("；" if language == "zh" else "; ").join(official_prerequisites)
        if official_prerequisites
        else (
            "本次未核到提供方公布的硬性先修；开始前请复核课程主页"
            if language == "zh"
            else "No provider-published hard prerequisite verified; recheck the course page"
        )
    )
    recommended = (
        ("；" if language == "zh" else "; ").join(
            _safe(str(item)) for item in recommended_items if str(item).strip()
        )
        if recommended_items
        else (
            "本站未另设准备条件"
            if language == "zh"
            else "No additional EEDIY preparation requirement"
        )
    )
    metadata_status_labels = (
        {
            "catalogue": "资料索引",
            "researched": "公开材料导读",
            "learner-reviewed": "含署名学习复盘",
        }
        if language == "zh"
        else {
            "catalogue": "resource catalogue",
            "researched": "public-material guide",
            "learner-reviewed": "includes an attributed learner report",
        }
    )
    relationship_labels = EDITORIAL_RELATIONSHIP_LABELS.get(
        (editorial_status, review_relationship)
    )
    status_note = (
        relationship_labels[0 if language == "zh" else 1]
        if relationship_labels
        else metadata_status_labels.get(
            editorial_status,
            metadata_status_labels["catalogue"],
        )
    )
    rows = [
        (labels["institution"], _safe(course["institution"])),
        (labels["code"], _safe(course["course_code"] or "—")),
        (labels["official_prerequisites"], official),
        (labels["recommended_background"], recommended),
        (
            labels["resources"],
            _resource_access_summary(course, language),
        ),
        (
            labels["reviewed"],
            (
                f"{reviewed_at}；{status_note}"
                if language == "zh"
                else f"{reviewed_at}; {status_note}"
            ),
        ),
    ]
    return "\n".join(
        f"- **{label}{separator}** {value}" for label, value in rows
    )


def _resource_label(resource: Mapping[str, Any], language: str) -> str:
    index = 0 if language == "zh" else 1
    resource_kind = str(resource["kind"])
    kind = RESOURCE_KIND_LABELS.get(resource_kind, ("资源", "Resource"))[index]
    title = _human_resource_title(resource, language)
    generic_by_kind = {
        "course": {"course home", "course homepage", "课程主页"},
        "assignments": {"assignments", "作业"},
        "labs": {"labs", "laboratory", "实验"},
        "notes": {"lecture notes", "notes", "讲义"},
        "video": {"videos", "video", "视频"},
        "exams": {"exams", "考试"},
        "code": {"code", "代码"},
    }
    aliases = {
        item.casefold() for item in generic_by_kind.get(resource_kind, set())
    }
    if title.casefold() in aliases:
        return kind
    if language == "zh" and title.startswith(kind):
        # Once the structural prefix is localized, repeating the kind produces
        # labels such as “作业 · 作业 3” or “实验 · 实验 2”. The localized title
        # already carries the type, so keep the more precise label by itself.
        return title
    # A syllabus or calendar may share the broad "course" kind with the
    # homepage. Preserve its precise provider title instead of presenting two
    # different destinations as identical course-home links.
    if resource_kind == "course":
        return title
    return f"{kind} · {title}"


RESOURCE_DISPLAY_PRIORITY = {
    "course": 0,
    "assignments": 1,
    "labs": 2,
    "projects": 3,
    "video": 4,
    "notes": 5,
    "exams": 6,
    "code": 7,
    "textbook": 8,
    "dataset": 9,
    "simulator": 10,
    "community": 11,
    "other": 12,
}
LOW_SIGNAL_COMPACT_RESOURCE_RE = re.compile(
    r"(?:\bmeet\s+(?:the\s+)?(?:team|tas|instructors?|staff)\b|"
    r"\bcourse\s+(?:team|staff)\b|/"
    r"(?:meet-the-(?:team|tas|instructors?|staff)|course-(?:team|staff))/?$|"
    r"\b(?:lecture|recitation)\s+video\s+transcript(?:\s+\(pdf\))?"
    r"\s+[—-]\s+\S+/[a-z0-9_-]{8,}(?:\s|$)|"
    r"\bwatch\s+now\b.*\bsee\.stanford\.edu/\d+\b)",
    re.IGNORECASE,
)
MACHINE_TITLE_SUFFIX_RE = re.compile(
    r"\s+[—-]\s+(?:[a-z0-9.-]+\.[a-z]{2,}/\S+|resource\s+[0-9a-f]{8})",
    re.IGNORECASE,
)
EEDIY_EXAMPLE_LINK_RE = re.compile(
    r"(?<!!)\[([^\]]+)\]\("
    r"(https://github\.com/appleweiping/eediy/tree/main/examples/[^)\s]+)"
    r"\)"
)


def _natural_text_key(value: str) -> tuple[tuple[int, int | str], ...]:
    parts = re.split(r"(\d+)", value.casefold())
    return tuple(
        (0, int(part)) if part.isdigit() else (1, part)
        for part in parts
        if part
    )


def _resource_display_key(
    indexed_resource: tuple[int, Mapping[str, Any]],
) -> tuple[Any, ...]:
    index, resource = indexed_resource
    title = resource.get("title", {})
    title_text = (
        " ".join(str(value) for value in title.values())
        if isinstance(title, Mapping)
        else str(title)
    )
    return (
        RESOURCE_DISPLAY_PRIORITY.get(str(resource["kind"]), 99),
        0 if resource["id"] == "primary" else 1,
        _natural_text_key(title_text),
        index,
    )


def _is_low_signal_compact_resource(resource: Mapping[str, Any]) -> bool:
    title = resource.get("title", {})
    title_text = (
        " ".join(str(value) for value in title.values())
        if isinstance(title, Mapping)
        else str(title)
    )
    return bool(
        LOW_SIGNAL_COMPACT_RESOURCE_RE.search(
            f"{title_text} {resource.get('url', '')}"
        )
    )


GENERIC_RESOURCE_TITLE_ZH = {
    "assignment": "作业",
    "assignments": "作业",
    "homework": "作业",
    "homework and labs": "作业与实验",
    "homework and exams": "作业与考试",
    "lab": "实验",
    "labs": "实验",
    "laboratory": "实验",
    "projects and labs": "项目与实验",
    "lab assignment logistics": "实验作业安排",
    "lab equipment handout": "实验设备说明",
    "lab kit": "实验套件",
    "lab practice and safety": "实验练习与安全说明",
    "lab videos": "实验视频",
    "lecture notes": "讲义",
    "lecture notes and handouts": "讲义与补充材料",
    "course notes": "课程讲义",
    "handwritten lecture notes": "手写讲义",
    "previous course notes": "往期课程讲义",
    "notes": "讲义",
    "exam": "考试",
    "exams": "考试",
    "exam materials": "考试材料",
    "midterm": "期中考试",
    "midterm exam": "期中考试",
    "midterm solutions": "期中考试解答",
    "final exam": "期末考试",
    "final exam solutions": "期末考试解答",
    "final project": "期末项目",
    "solution": "解答",
    "solutions": "解答",
    "syllabus": "课程大纲",
    "course syllabus": "课程大纲",
    "video": "视频",
    "videos": "视频",
    "video resources": "视频资源",
    "video lectures": "课程视频",
    "lecture video": "课程视频",
    "lecture videos": "课程视频",
    "related video lectures": "相关课程视频",
    "view video page": "视频页面",
    "problem solving help videos": "解题辅助视频",
    "resource index": "资源索引",
}
RESOURCE_FORMAT_SUFFIX_RE = re.compile(
    r"\s*(?P<format>\((?:PDF|HTML|ZIP|M)(?:\s*-\s*[^)]+)?\))\s*$",
    re.IGNORECASE,
)
RESOURCE_TERM_ZH = {
    "spring": "春季",
    "summer": "夏季",
    "fall": "秋季",
    "winter": "冬季",
}


def _zh_resource_format(value: str | None) -> str:
    if not value:
        return ""
    return f"（{value.strip()[1:-1]}）"


def _zh_resource_topic(value: str) -> str:
    """Preserve a provider topic while polishing only a trailing file marker."""

    topic = value.strip()
    exact = {
        "review for final exam": "期末考试复习",
    }.get(topic.casefold())
    if exact is not None:
        return exact
    topic = re.sub(
        r"\(Handwritten\s+Notes\)",
        "（手写讲义）",
        topic,
        flags=re.IGNORECASE,
    )
    suffix = RESOURCE_FORMAT_SUFFIX_RE.search(topic)
    if suffix is None:
        return topic
    return (
        topic[: suffix.start()].rstrip()
        + _zh_resource_format(suffix.group("format"))
    )


def _zh_resource_term(season: str, year: str) -> str:
    return f"{year} {RESOURCE_TERM_ZH[season.casefold()]}"


def _localize_generic_resource_title(title: str) -> str:
    """Localize only structural resource labels with unambiguous semantics.

    The provider's topic after a colon or dash remains verbatim. This keeps
    course codes, people, paper/book titles, and technical terms out of a
    speculative translation path while still making labels such as
    ``Homework 3`` or ``Lecture 8: PLL Design`` natural on the Chinese page.
    """

    stripped = title.strip()
    exact = GENERIC_RESOURCE_TITLE_ZH.get(stripped.casefold())
    if exact is not None:
        return exact

    match = re.fullmatch(
        r"(?P<number>\d+(?:\.\d+)*)\s+Topic\s+Videos?",
        stripped,
        flags=re.IGNORECASE,
    )
    if match:
        return f"{match.group('number')} 主题视频"

    match = re.fullmatch(
        r"(?:Lecture|Recitation)\s+video\s+transcript"
        r"(?P<format>\s+\((?:PDF|HTML)[^)]*\))?",
        stripped,
        flags=re.IGNORECASE,
    )
    if match:
        prefix = (
            "课程视频文字稿"
            if stripped.casefold().startswith("lecture")
            else "习题课视频文字稿"
        )
        return prefix + _zh_resource_format(match.group("format"))

    match = re.fullmatch(
        r"Assignment\s+resource:\s*(?P<topic>.+)",
        stripped,
        flags=re.IGNORECASE,
    )
    if match:
        return f"作业资源：{_zh_resource_topic(match.group('topic'))}"

    match = re.fullmatch(
        r"Lab\s+resource:\s*(?P<topic>.+)",
        stripped,
        flags=re.IGNORECASE,
    )
    if match:
        return f"实验资源：{_zh_resource_topic(match.group('topic'))}"

    if stripped.casefold() == (
        "laboratory assignments resource index "
        "(includes selected lab solutions)"
    ):
        return "实验作业资源索引（含部分实验解答）"
    if stripped.casefold() == (
        "restricted homework index (linked files require uiuc access)"
    ):
        return "受限作业索引（链接文件需要 UIUC 权限）"

    match = re.fullmatch(
        r"Homework\s+(?P<number>\d+)"
        r"(?:\s+(?P<detail>solutions?|code|additional exercise))?"
        r"(?P<format>\s+\((?:PDF|HTML|ZIP|M)[^)]*\))?",
        stripped,
        flags=re.IGNORECASE,
    )
    if match:
        detail = {
            "solution": "解答",
            "solutions": "解答",
            "code": "代码",
            "additional exercise": "附加题",
        }.get((match.group("detail") or "").casefold(), "")
        return (
            f"作业 {match.group('number')}"
            + (f" {detail}" if detail else "")
            + _zh_resource_format(match.group("format"))
        )

    match = re.fullmatch(
        r"Homework\s+(?P<number>\d+)\s*:\s*(?P<topic>.+)",
        stripped,
        flags=re.IGNORECASE,
    )
    if match:
        return (
            f"作业 {match.group('number')}："
            f"{_zh_resource_topic(match.group('topic'))}"
        )

    match = re.fullmatch(
        r"Assignments?\s+(?P<number>\d+)"
        r"(?P<format>\s+\((?:PDF|HTML|ZIP|M)[^)]*\))?",
        stripped,
        flags=re.IGNORECASE,
    )
    if match:
        return (
            f"作业 {match.group('number')}"
            + _zh_resource_format(match.group("format"))
        )

    match = re.fullmatch(
        r"Lab\s+(?P<number>\d+[A-Z]?)"
        r"(?:\s+(?P<detail>solutions?|background))?"
        r"(?P<format>\s+\((?:PDF|HTML|ZIP|M)[^)]*\))?",
        stripped,
        flags=re.IGNORECASE,
    )
    if match:
        detail = {
            "solution": "解答",
            "solutions": "解答",
            "background": "背景资料",
        }.get((match.group("detail") or "").casefold(), "")
        return (
            f"实验 {match.group('number')}"
            + (f" {detail}" if detail else "")
            + _zh_resource_format(match.group("format"))
        )

    match = re.fullmatch(
        r"Lab\s+(?P<number>\d+[A-Z]?)"
        r"(?:\s*[:\u2013\u2014-]\s*|\s+)(?P<topic>.+)",
        stripped,
        flags=re.IGNORECASE,
    )
    if match:
        topic = match.group("topic")
        if topic.casefold().startswith("handout: extra credit lab"):
            topic = re.sub(
                r"^Handout:\s*Extra\s+Credit\s+Lab",
                "讲义：加分实验",
                topic,
                count=1,
                flags=re.IGNORECASE,
            )
            return f"实验 {match.group('number')} {_zh_resource_topic(topic)}"
        return (
            f"实验 {match.group('number')}："
            f"{_zh_resource_topic(topic)}"
        )

    match = re.fullmatch(
        r"Lecture\s+(?P<number>\d+[A-Z]?)"
        r"(?P<format>\s+\((?:PDF|HTML)[^)]*\))?",
        stripped,
        flags=re.IGNORECASE,
    )
    if match:
        return (
            f"第 {match.group('number')} 讲"
            + _zh_resource_format(match.group("format"))
        )

    match = re.fullmatch(
        r"Lecture\s+(?P<number>\d+[A-Z]?)\s*:\s*(?P<topic>.+)",
        stripped,
        flags=re.IGNORECASE,
    )
    if match:
        return (
            f"第 {match.group('number')} 讲："
            f"{_zh_resource_topic(match.group('topic'))}"
        )

    exam_detail_zh = {
        "solution": "解答",
        "solutions": "解答",
        "review": "复习材料",
        "formula sheet": "公式表",
        "problem solving": "解题",
        "practice problems i": "练习题 I",
        "practice problems ii": "练习题 II",
        "practice solutions i": "练习题解答 I",
        "practice solutions ii": "练习题解答 II",
    }
    match = re.fullmatch(
        r"Exam\s+(?P<number>\d+)"
        r"(?:\s+(?P<detail>solutions?|review|formula sheet|problem solving|"
        r"practice problems [IVX]+|practice solutions [IVX]+))?"
        r"(?P<format>\s+\((?:PDF|HTML)[^)]*\))?",
        stripped,
        flags=re.IGNORECASE,
    )
    if match:
        detail = exam_detail_zh.get(
            (match.group("detail") or "").casefold(),
            "",
        )
        return (
            f"考试 {match.group('number')}"
            + (f" {detail}" if detail else "")
            + _zh_resource_format(match.group("format"))
        )

    match = re.fullmatch(
        r"Practice\s+Exam\s+(?P<number>\d+)"
        r"(?:\s+(?P<solution>solutions?))?"
        r"(?P<format>\s+\((?:PDF|HTML)[^)]*\))?",
        stripped,
        flags=re.IGNORECASE,
    )
    if match:
        return (
            f"模拟考试 {match.group('number')}"
            + (" 解答" if match.group("solution") else "")
            + _zh_resource_format(match.group("format"))
        )

    match = re.fullmatch(
        r"Practice\s+Quiz\s+(?P<number>\d+[A-Z]?)"
        r"(?:\s+(?P<solution>solutions?))?"
        r"(?P<format>\s+\((?:PDF|HTML)[^)]*\))?",
        stripped,
        flags=re.IGNORECASE,
    )
    if match:
        return (
            f"模拟测验 {match.group('number')}"
            + (" 解答" if match.group("solution") else "")
            + _zh_resource_format(match.group("format"))
        )

    match = re.fullmatch(
        r"Problem\s+sets?\s+(?P<number>\d+)"
        r"(?:\s+(?P<solution>solutions?))?"
        r"(?P<format>\s+\((?:PDF|HTML)[^)]*\))?",
        stripped,
        flags=re.IGNORECASE,
    )
    if match:
        return (
            f"习题 {match.group('number')}"
            + (" 解答" if match.group("solution") else "")
            + _zh_resource_format(match.group("format"))
        )

    match = re.fullmatch(
        r"Solutions?\s+to\s+problem\s+set\s+(?P<number>\d+)"
        r"(?P<format>\s+\((?:PDF|HTML)[^)]*\))?",
        stripped,
        flags=re.IGNORECASE,
    )
    if match:
        return (
            f"习题 {match.group('number')} 解答"
            + _zh_resource_format(match.group("format"))
        )

    match = re.fullmatch(
        r"(?P<year>\d{4})\s+Midterm(?:\s+Exam)?"
        r"(?:\s+(?:with\s+)?(?P<solution>solutions?))?"
        r"(?P<format>\s+\((?:PDF|HTML)[^)]*\))?",
        stripped,
        flags=re.IGNORECASE,
    )
    if match:
        return (
            f"{match.group('year')} 年期中考试"
            + ("（含解答）" if match.group("solution") else "")
            + _zh_resource_format(match.group("format"))
        )

    match = re.fullmatch(
        r"(?P<year>\d{4})\s+Midterm\s+Problems"
        r"(?P<format>\s+\((?:PDF|HTML)[^)]*\))?",
        stripped,
        flags=re.IGNORECASE,
    )
    if match:
        return (
            f"{match.group('year')} 年期中考试题"
            + _zh_resource_format(match.group("format"))
        )

    match = re.fullmatch(
        r"(?P<season>Spring|Summer|Fall|Winter)\s+(?P<year>\d{4})\s+"
        r"Midterm(?:\s+Exam)?(?:\s+(?P<number>\d+))?"
        r"(?:\s+(?P<solution>solutions?))?"
        r"(?P<format>\s+\((?:PDF|HTML)[^)]*\))?",
        stripped,
        flags=re.IGNORECASE,
    )
    if match:
        return (
            f"{_zh_resource_term(match.group('season'), match.group('year'))}"
            "期中考试"
            + (f" {match.group('number')}" if match.group("number") else "")
            + (" 解答" if match.group("solution") else "")
            + _zh_resource_format(match.group("format"))
        )

    match = re.fullmatch(
        r"Midterm(?:\s+Exam)?(?:\s+(?P<number>\d+))?"
        r"(?:\s+(?P<solution>solutions?))?"
        r"(?P<format>\s+\((?:PDF|HTML)[^)]*\))?",
        stripped,
        flags=re.IGNORECASE,
    )
    if match:
        number = match.group("number")
        if number and len(number) == 4:
            prefix = f"{number} 年期中考试"
        else:
            prefix = "期中考试" + (f" {number}" if number else "")
        return (
            prefix
            + (" 解答" if match.group("solution") else "")
            + _zh_resource_format(match.group("format"))
        )

    match = re.fullmatch(
        r"Practice\s+Final\s+Exam"
        r"(?:\s+(?P<solution>solutions?))?"
        r"(?P<format>\s+\((?:PDF|HTML)[^)]*\))?",
        stripped,
        flags=re.IGNORECASE,
    )
    if match:
        return (
            "期末模拟考试"
            + ("解答" if match.group("solution") else "")
            + _zh_resource_format(match.group("format"))
        )

    final_detail_zh = {
        "solution": "解答",
        "solutions": "解答",
        "formula sheet": "公式表",
        "practice problems": "练习题",
        "problem 4 solution": "第 4 题解答",
    }
    match = re.fullmatch(
        r"Final\s+Exam"
        r"(?:\s+\((?P<season>Spring|Summer|Fall|Winter)\s+"
        r"(?P<term_year>\d{4})\)|\s+(?P<plain_season>Spring|Summer|Fall|Winter)"
        r"\s+(?P<plain_year>\d{4}))?"
        r"(?:\s+(?P<detail>solutions?|formula sheet|practice problems|"
        r"problem 4 solution))?"
        r"(?P<format>\s+\((?:PDF|HTML)[^)]*\))?",
        stripped,
        flags=re.IGNORECASE,
    )
    if match:
        term = ""
        if match.group("season"):
            term = f"（{_zh_resource_term(match.group('season'), match.group('term_year'))}）"
        elif match.group("plain_season"):
            term = f"（{_zh_resource_term(match.group('plain_season'), match.group('plain_year'))}）"
        detail = final_detail_zh.get(
            (match.group("detail") or "").casefold(),
            "",
        )
        return (
            "期末考试"
            + term
            + detail
            + _zh_resource_format(match.group("format"))
        )

    match = re.fullmatch(
        r"Final\s+Exam\s+from\s+(?P<year>\d{4})"
        r"(?P<format>\s+\((?:PDF|HTML)[^)]*\))?",
        stripped,
        flags=re.IGNORECASE,
    )
    if match:
        return (
            f"{match.group('year')} 年期末考试"
            + _zh_resource_format(match.group("format"))
        )

    match = re.fullmatch(
        r"Final\s+Exam\s+Solutions?\s+"
        r"(?P<season>Spring|Summer|Fall|Winter)\s+(?P<year>\d{4})"
        r"(?P<format>\s+\((?:PDF|HTML)[^)]*\))?",
        stripped,
        flags=re.IGNORECASE,
    )
    if match:
        return (
            f"{_zh_resource_term(match.group('season'), match.group('year'))}"
            "期末考试解答"
            + _zh_resource_format(match.group("format"))
        )

    match = re.fullmatch(
        r"(?P<season>Spring|Summer|Fall|Winter)\s+(?P<year>\d{4})\s+"
        r"Solutions?\s+Final\s+Exam"
        r"(?P<format>\s+\((?:PDF|HTML)[^)]*\))?",
        stripped,
        flags=re.IGNORECASE,
    )
    if match:
        return (
            f"{_zh_resource_term(match.group('season'), match.group('year'))}"
            "期末考试解答"
            + _zh_resource_format(match.group("format"))
        )

    match = re.fullmatch(
        r"(?:(?P<season>Spring|Summer|Fall|Winter)\s+)?"
        r"(?P<year>\d{4})\s+Final\s+Exam"
        r"(?:\s+(?P<solution>solutions?))?"
        r"(?P<format>\s+\((?:PDF|HTML)[^)]*\))?",
        stripped,
        flags=re.IGNORECASE,
    )
    if match:
        prefix = (
            _zh_resource_term(match.group("season"), match.group("year"))
            if match.group("season")
            else f"{match.group('year')} 年"
        )
        return (
            f"{prefix}期末考试"
            + (" 解答" if match.group("solution") else "")
            + _zh_resource_format(match.group("format"))
        )

    match = re.fullmatch(
        r"Finals?\s+(?P<year>\d{4})",
        stripped,
        flags=re.IGNORECASE,
    )
    if match:
        return f"{match.group('year')} 年期末考试"

    match = re.fullmatch(
        r"Final\s+project\s+discussion\s*(?P<detail>\(.+\))?",
        stripped,
        flags=re.IGNORECASE,
    )
    if match:
        return "期末项目讨论" + (f" {match.group('detail')}" if match.group("detail") else "")

    match = re.fullmatch(
        r"(?P<season>Spring|Summer|Fall|Winter)\s+(?P<year>\d{4})\s+"
        r"lecture\s+directory\s+(?P<count>\(\d+\s+PDFs?\))",
        stripped,
        flags=re.IGNORECASE,
    )
    if match:
        return (
            f"{_zh_resource_term(match.group('season'), match.group('year'))}"
            f"讲义目录{_zh_resource_format(match.group('count'))}"
        )

    match = re.fullmatch(
        r"(?P<season>Spring|Summer|Fall|Winter)\s+(?P<year>\d{4})\s+"
        r"homework\s+directory\s+\(HW\s+(?P<range>.+?)\s+and\s+"
        r"partial\s+solutions\)",
        stripped,
        flags=re.IGNORECASE,
    )
    if match:
        return (
            f"{_zh_resource_term(match.group('season'), match.group('year'))}"
            f"作业目录（HW {match.group('range')}；含部分解答）"
        )

    match = re.fullmatch(
        r"(?P<season>Spring|Summer|Fall|Winter)\s+(?P<year>\d{4})\s+"
        r"problem\s+sets?\s+(?P<range>.+?)\s+with\s+solutions\s+"
        r"\(historical\s+companion\)",
        stripped,
        flags=re.IGNORECASE,
    )
    if match:
        return (
            f"{_zh_resource_term(match.group('season'), match.group('year'))}"
            f"习题 {match.group('range')}（含解答；历史配套）"
        )

    return stripped


def _machine_human_resource_title(
    resource: Mapping[str, Any],
    language: str,
) -> str:
    raw = str(resource["title"][language]).strip()
    if not MACHINE_TITLE_SUFFIX_RE.search(raw):
        return raw

    url = str(resource.get("url", ""))
    path = unquote(urlsplit(url).path)
    lowered = path.casefold()
    solution = bool(
        re.search(r"(?:^|[/_.-])(?:sol|soln|solution|solutions)(?:$|[/_.-])", lowered)
    )
    is_zh = language == "zh"

    homework = re.search(r"(?:hw|homework)[_-]?0*(\d+)", lowered)
    if homework:
        number = homework.group(1)
        if re.search(r"extra|additional", lowered):
            return f"作业 {number} 附加题" if is_zh else f"Homework {number} additional exercise"
        if solution:
            return f"作业 {number} 解答" if is_zh else f"Homework {number} solutions"
        return f"作业 {number}" if is_zh else f"Homework {number}"

    exam = re.search(r"(?:^|/)(?:exam|midterm)[_-]?0*(\d+)", lowered)
    if exam:
        number = exam.group(1)
        review = "review" in lowered
        if is_zh:
            return f"考试 {number}{' 复习材料' if review else ''}{'解答' if solution else ''}"
        return (
            f"Exam {number}"
            + (" review" if review else "")
            + (" solutions" if solution else "")
        )

    lecture = re.search(r"(?:lec|lecture)[_-]?0*(\d+)", lowered)
    if lecture:
        number = lecture.group(1)
        detail = ""
        if "five_eqn" in lowered:
            detail = " · five-equation summary"
        elif "photo" in lowered:
            detail = " · photolithography"
        if is_zh:
            translated_detail = {
                " · five-equation summary": " · 五方程小结",
                " · photolithography": " · 光刻补充",
            }.get(detail, "")
            return f"第 {number} 讲讲义{translated_detail}"
        return f"Lecture {number} notes{detail}"

    tutorial = re.search(r"ece4750[-_](t\d{2})[-_](.+?)(?:\.pdf)?$", lowered)
    if tutorial:
        code = tutorial.group(1).upper()
        topic = tutorial.group(2).replace("-", " ").replace("_", " ")
        replacements = {
            "proc": "processor",
            "uarch": "microarchitecture",
            "mem": "memory",
            "ap": "advanced processors",
            "ooo": "out-of-order execution",
        }
        words = [replacements.get(word, word) for word in topic.split()]
        readable = " ".join(words)
        return (
            f"{code} · {readable}"
            if not is_zh
            else f"{code} · {readable} 讲义"
        )

    if "/lectures/" in lowered and lowered.endswith(("/code", "/slides.pdf")):
        parts = [part for part in path.split("/") if part]
        topic = parts[-2].replace("-", " ").replace("_", " ")
        kind = "代码" if lowered.endswith("/code") and is_zh else (
            "code" if lowered.endswith("/code") else ("讲义" if is_zh else "slides")
        )
        return f"{topic} · {kind}"

    if "final" in lowered:
        return "期末考试解答" if is_zh and solution else (
            "期末考试" if is_zh else ("Final exam solutions" if solution else "Final exam")
        )
    if "midterm" in lowered:
        return "期中考试解答" if is_zh and solution else (
            "期中考试" if is_zh else ("Midterm solutions" if solution else "Midterm")
        )

    if lowered.endswith("/syllabus"):
        term = re.search(
            r"(?:^|[-_/])(spring|summer|fall|winter)-(\d{4})(?:[-_/]|$)",
            lowered,
        )
        if term:
            season, year = term.groups()
            if is_zh:
                season_zh = {
                    "spring": "春",
                    "summer": "夏",
                    "fall": "秋",
                    "winter": "冬",
                }[season]
                return f"{year} {season_zh}季课程大纲"
            return f"{season.title()} {year} syllabus"
        return "课程大纲" if is_zh else "Syllabus"

    # A human-readable base is preferable to leaking a crawler host, path, or
    # hash. The URL remains visible on hover and in the link destination.
    return MACHINE_TITLE_SUFFIX_RE.split(raw, maxsplit=1)[0].strip()


def _human_resource_title(
    resource: Mapping[str, Any],
    language: str,
) -> str:
    human = _machine_human_resource_title(resource, language)
    if language != "zh":
        return human
    return _localize_generic_resource_title(human)


def _eediy_example_links(body: str) -> list[tuple[str, str]]:
    links: list[tuple[str, str]] = []
    seen: set[str] = set()
    for label, url in EEDIY_EXAMPLE_LINK_RE.findall(body):
        normalized = normalize_url(url)
        if normalized in seen:
            continue
        links.append((label, url))
        seen.add(normalized)
    return links


def _curated_resources(
    course: Mapping[str, Any],
    *,
    limit: int = 6,
    exclude_urls: Iterable[str] = (),
) -> list[Mapping[str, Any]]:
    ordered = sorted(
        enumerate(course["resources"]),
        key=_resource_display_key,
    )
    excluded = {normalize_url(url) for url in exclude_urls}
    selected: list[Mapping[str, Any]] = []
    used_kinds: set[str] = set()
    used_urls: set[str] = set()
    for _, resource in ordered:
        if _is_low_signal_compact_resource(resource):
            continue
        kind = str(resource["kind"])
        url = str(resource["url"])
        if normalize_url(url) in excluded:
            continue
        if url in used_urls:
            continue
        if kind in used_kinds and kind not in {"course", "other"}:
            continue
        selected.append(resource)
        used_kinds.add(kind)
        used_urls.add(url)
        if len(selected) == limit:
            break
    return selected


def _render_resource_index(
    course: Mapping[str, Any],
    language: str,
    *,
    show_coverage: bool = True,
    resources: Sequence[Mapping[str, Any]] | None = None,
) -> str:
    visible_resources = [
        resource
        for _, resource in sorted(
            enumerate(course["resources"] if resources is None else resources),
            key=_resource_display_key,
        )
    ]
    if not visible_resources:
        return ""
    index = 0 if language == "zh" else 1
    if language == "zh":
        summary = f"展开更多官方资源（{len(visible_resources)} 项）"
        labels = {
            "resource": "资源",
            "access": "访问",
            "status": "状态",
            "verified": "复核日期",
            "coverage": "材料覆盖",
            "type": "类型",
            "level": "公开状态",
            "coverage_note": (
                "“可用材料集合”只表示在下方所列访问条件下，提供方给出了一组足以"
                "沿课程推进的该类材料；不保证逐学期、逐文件齐全，也不默认包含题解、"
                "评分、starter code 或反馈机制。正文记录的访问限制与缺口优先于摘要。"
            ),
            "notice": (
                "其余条目保留访问状态与复核日期；材料权利归原提供方，实际可用性"
                "可能随账号、地区或课程改版变化。"
            ),
        }
    else:
        resource_count = len(visible_resources)
        resource_noun = "item" if resource_count == 1 else "items"
        summary = f"Show more official resources ({resource_count} {resource_noun})"
        labels = {
            "resource": "Resource",
            "access": "Access",
            "status": "Status",
            "verified": "Verified",
            "coverage": "Material coverage",
            "type": "Type",
            "level": "Public status",
            "coverage_note": (
                "“Usable material set” means the provider exposes a course-level set that can "
                "support study under the access conditions listed below. It does not promise "
                "every term or file, and it does not imply solutions, grading, starter code, "
                "or feedback. The guide's documented limits take precedence over the summary."
            ),
            "notice": (
                "These remaining entries retain access status and review dates. Rights stay "
                "with the original providers, and actual access may change with account, "
                "region, or course redesign."
            ),
        }
    resource_rows = []
    for resource in visible_resources:
        access = ACCESS_LABELS[str(resource["access"])][index]
        status = STATUS_LABELS[str(resource["status"])][index]
        resource_rows.append(
            f"| [{_safe(_human_resource_title(resource, language))}]({resource['url']}) "
            f"| {_safe(access)} | {_safe(status)} | {resource['last_verified']} |"
        )
    coverage_block = ""
    if show_coverage:
        coverage_rows = "\n".join(
            f"| {COVERAGE_NAMES[key][index]} | "
            f"{COVERAGE_LABELS[int(course['resource_coverage'][key])][index]} |"
            for key in COVERAGE_NAMES
        )
        coverage_block = (
            f"**{labels['coverage']}**\n\n"
            f"| {labels['type']} | {labels['level']} |\n|---|---|\n"
            f"{coverage_rows}\n\n"
            f"> {_safe(labels['coverage_note'])}\n\n"
        )
    return (
        '<details markdown="1">\n'
        f"<summary>{summary}</summary>\n\n"
        + coverage_block
        + f"**{labels['resource']}**\n\n"
        f"| {labels['resource']} | {labels['access']} | {labels['status']} | "
        f"{labels['verified']} |\n|---|---|---|---|\n"
        + "\n".join(resource_rows)
        + f"\n\n> {_safe(labels['notice'])}\n\n"
        "</details>"
    )


def _render_selected_resources(
    course: Mapping[str, Any],
    language: str,
    *,
    narrative_urls: Iterable[str],
    eediy_examples: Sequence[tuple[str, str]] = (),
) -> str:
    cited = {normalize_url(url) for url in narrative_urls}
    selected: list[Mapping[str, Any]] = [
        resource
        for resource in course["resources"]
        if normalize_url(str(resource["url"])) in cited
        and not _is_low_signal_compact_resource(resource)
    ][:5]
    selected_urls = {normalize_url(str(resource["url"])) for resource in selected}
    for resource in _curated_resources(course, limit=5):
        if len(selected) >= 5:
            break
        normalized = normalize_url(str(resource["url"]))
        if normalized in selected_urls:
            continue
        selected.append(resource)
        selected_urls.add(normalized)
    remaining = [
        resource
        for resource in course["resources"]
        if normalize_url(str(resource["url"])) not in selected_urls
        and not _is_low_signal_compact_resource(resource)
    ]
    lines = [
        f"- [{_safe(_resource_label(resource, language))}]({resource['url']})"
        for resource in selected
    ]
    if not lines:
        lines.append(
            "核心入口已在正文中列出。"
            if language == "zh"
            else "The core entry points are linked in the guide above."
        )
    summary_heading = "资源汇总" if language == "zh" else "Resource Summary"
    resource_index = _render_resource_index(
        course,
        language,
        show_coverage=False,
        resources=remaining,
    )
    lines.extend(["", f"## {summary_heading}", ""])
    lines.extend(
        f"- [{_safe(label)}]({url})"
        for label, url in eediy_examples
    )
    if resource_index:
        if eediy_examples:
            lines.append("")
        lines.append(resource_index)
    else:
        if not eediy_examples:
            lines.append(
                (
                    "本次核对的公开入口已全部列在上方；若你有完成记录、补充材料或"
                    "失效链接，可通过页末反馈与纠错入口提交依据。"
                    if language == "zh"
                    else (
                        "Every public entry point verified in this review is listed above. "
                        "Use the feedback and corrections links below to submit a completion "
                        "record, another resource, or a broken-link report."
                    )
                )
            )
    return "\n".join(lines)


def _mainline_audit_notice(
    audit: Mapping[str, Any] | None,
    language: str,
) -> str:
    if not audit or audit.get("status") != "review":
        return ""
    if language == "zh":
        return (
            '\n!!! warning "开始前请确认材料限制"\n'
            f"    {_safe(audit['limitation_zh'])} "
            f"最近核对：{_safe(audit['verified_at'])}。\n"
        )
    return (
        '\n!!! warning "Check the material limits before starting"\n'
        f"    {_safe(audit['limitation_en'])} "
        f"Last checked: {_safe(audit['verified_at'])}.\n"
    )


def _nest_first_guide_section_under_overview(body: str) -> str:
    lines = body.strip().splitlines()
    if not lines or not lines[0].startswith("## "):
        raise ValueError("authored guide body must begin with an H2")
    for index, line in enumerate(lines):
        heading = re.match(r"^(#{2,5})(\s+.+)$", line)
        if heading:
            lines[index] = "#" + line
    return "\n".join(lines)


def render_course_page(
    course: Mapping[str, Any],
    track: Mapping[str, Any],
    language: str,
    courses_by_source: Mapping[int, Mapping[str, Any]],
    audit: Mapping[str, Any] | None = None,
    guide: Mapping[str, Any] | None = None,
) -> str:
    title = str(course["title"][language])
    institution = str(course["institution"])
    course_code = str(course["course_code"])
    display_prefix = (
        institution
        if course_code.casefold() in title.casefold()
        else f"{institution} {course_code}"
    )
    display_title = f"{display_prefix}: {title}"
    summary = str(course["summary"][language])
    status = str(guide["editorial_status"]) if guide else "catalogue"
    evidence_level = str(guide["evidence_level"]) if guide else "R0"
    reviewed_at = str(guide["reviewed_at"]) if guide else str(course["last_reviewed"])
    review_relationship = _review_relationship(guide)
    metadata = _course_metadata(
        course,
        language,
        reviewed_at=reviewed_at,
        editorial_status=status,
        review_relationship=review_relationship,
    )
    marker_payload = {
        "course": course,
        "guide": guide if guide else None,
        "language": language,
    }
    front_matter_extra = {
        "course_id": course["id"],
        "editorial_status": status,
        "evidence_level": evidence_level,
        "reviewed_at": reviewed_at,
        "comments": True,
    }
    if review_relationship:
        front_matter_extra["review_relationship"] = review_relationship
    prefix = (
        _front_matter(
            title,
            summary,
            "course",
            front_matter_extra,
        )
        + _marker(marker_payload)
        + f"# {_safe(display_title)}\n\n"
        + ("## 课程简介\n\n" if language == "zh" else "## Course Overview\n\n")
        + metadata
        # End the metadata list before the authored guide begins. A single
        # newline makes CommonMark treat the opening guide paragraph as a
        # continuation of the final list item, collapsing the page hierarchy.
        + "\n\n"
    )
    resource_index_heading = "课程资源" if language == "zh" else "Course Resources"
    resource_summary_heading = "资源汇总" if language == "zh" else "Resource Summary"
    if guide:
        source_body = str(guide.get("bodies", {}).get(language, "")).strip()
        body = _nest_first_guide_section_under_overview(source_body)
        narrative_urls = _external_links(source_body)
        eediy_examples = _eediy_example_links(source_body)
        page = (
            prefix
            + body
            + _mainline_audit_notice(audit, language)
        )
        if guide.get("resource_index_mode", "structured") == "inline-only":
            contextual_note = (
                "本页已在正文中按版本与访问条件放置核心资料链接。为避免把前序课程、"
                "历史 syllabus 或受限材料脱离上下文误列为本课资源，这里不重复生成"
                "通用资源清单。"
                if language == "zh"
                else (
                    "The guide above links each core resource where its version and "
                    "access conditions are explained. To avoid relabeling a sequence "
                    "course, archived syllabus, or restricted item out of context, "
                    "this page does not repeat a generic resource list."
                )
            )
            return (
                page.rstrip()
                + f"\n\n## {resource_index_heading}\n\n"
                + contextual_note
                + f"\n\n## {resource_summary_heading}\n\n"
                + (
                    "本页没有脱离上下文重复列出资源；正文中的链接及其版本说明构成"
                    "本次核对的完整汇总。"
                    if language == "zh"
                    else (
                        "This page does not repeat resources outside their version context. "
                        "The links and version notes in the overview are the complete verified "
                        "summary for this review."
                    )
                )
                + "\n"
            )
        return (
            page
            + f"\n\n## {resource_index_heading}\n\n"
            + _render_selected_resources(
                course,
                language,
                narrative_urls=narrative_urls,
                eediy_examples=eediy_examples,
            )
            + "\n"
        )

    prerequisites = _render_prerequisites(course, courses_by_source, language)
    if language == "zh":
        body = (
            f"{_safe(summary)}\n\n"
            "**开始前先核对**\n\n"
            f"{prerequisites}\n\n"
            "### 已知边界\n\n"
            f"{_safe(course['review_note']['zh'])}\n\n"
            "这条记录没有把维护者自拟项目、统一工时或通用验收条件包装成课程事实。"
            "若你完成过这门课，可通过页末反馈入口提交作业结构、实际耗时、失效链接和"
            "踩坑证据。\n\n"
        )
        resource_intro = (
            "先从下面几个入口判断课程是否适合自己。核验清单只列出本次实际检查的"
            "官方索引页与代表性文件，不冒充课程官网的逐项镜像；清单中没有某类材料，"
            "只表示本次未核到，不能反推提供方一定没有。"
        )
    else:
        body = (
            f"{_safe(summary)}\n\n"
            "**Check before starting**\n\n"
            f"{prerequisites}\n\n"
            "### Known Boundaries\n\n"
            f"{_safe(course['review_note']['en'])}\n\n"
            "This catalogue record does not present a maintainer-invented project, uniform "
            "workload, or generic acceptance test as a course fact. If you completed the "
            "course, use the feedback links below to report assignment structure, actual effort, "
            "broken access, and concrete pitfalls.\n\n"
        )
        resource_intro = (
            "Use these entry points to decide whether the course fits. The verified list contains "
            "the official index pages and representative files checked in this review; it is not "
            "a file-by-file mirror of the provider site. If a resource type is absent from the "
            "list, this review did not verify it; absence is not proof that the provider has none."
        )
    return (
        prefix
        + body
        + _mainline_audit_notice(audit, language)
        + f"## {resource_index_heading}\n\n"
        + resource_intro
        + "\n\n"
        + _render_selected_resources(
            course,
            language,
            narrative_urls=(),
        )
        + "\n"
    )


def render_track_page(
    track: Mapping[str, Any],
    courses: Sequence[Mapping[str, Any]],
    tracks_by_id: Mapping[str, Mapping[str, Any]],
    language: str,
    audits_by_course: Mapping[int, Mapping[str, Any]] | None = None,
    guide: Mapping[str, Any] | None = None,
    course_guides: Mapping[int, Mapping[str, Any]] | None = None,
) -> str:
    title = str(track["title"][language])
    summary = str(track["summary"][language])
    ordered = sorted(courses, key=_course_sort_key)
    prerequisites = [
        tracks_by_id[track_id]
        for track_id in track.get("prerequisite_tracks", [])
        if track_id in tracks_by_id
    ]
    if language == "zh":
        labels = {
            "position": "方向定位",
            "prereq": "建议先修方向",
            "sequence": "建议顺序",
            "courses": "课程清单",
            "course": "课程",
            "institution": "机构",
            "role": "角色",
            "evidence": "编辑证据",
            "practice": "实践资源",
            "selection": "如何选课",
            "exit": "方向验收",
        }
        selection = [
            "第一次系统学习优先从材料范围已核清的主线开始；带“范围待复核”标记的课程先读清限制，同一阶段通常不必并行完成多个替代课程。",
            "先打开作业、实验和课程说明，再根据自己的先修、访问条件与反馈方式选择；不要只看学校或课程名。",
            "补充课程只用于填补某个主题、工具或实践缺口。",
        ]
    else:
        labels = {
            "position": "Track position",
            "prereq": "Recommended prerequisite tracks",
            "sequence": "Suggested order",
            "courses": "Courses",
            "course": "Course",
            "institution": "Institution",
            "role": "Role",
            "evidence": "Editorial evidence",
            "practice": "Practice coverage",
            "selection": "How to choose",
            "exit": "Track completion",
        }
        selection = [
            "For a first systematic pass, start with a mainline whose material scope is clear. Read the limitation on any course marked “Scope needs review,” and rarely take parallel alternatives.",
            "Open the assignments, laboratories, and course description before choosing; fit depends on prerequisites, access, and feedback, not the institution or course title alone.",
            "Use supplements only to close a specific topic, tool, or practice gap.",
        ]
    prereq_items = (
        "\n".join(
            f"- [{_safe(item['title'][language])}](../{item['id']}/index.md)"
            for item in prerequisites
        )
        if prerequisites
        else ("- 无" if language == "zh" else "- None")
    )
    audits_by_course = audits_by_course or {}
    course_guides = course_guides or {}

    def audit_suffix(course: Mapping[str, Any]) -> str:
        audit = audits_by_course.get(int(course["source_id"]))
        if not audit or audit.get("status") != "review":
            return ""
        return " — 材料限制待确认" if language == "zh" else " — Check material limits"

    mainline = [course for course in ordered if course["role"] == "mainline"]
    sequence_courses = mainline or ordered[:3]
    sequence = "\n".join(
        f"{index}. [{_safe(course['title'][language])}]({course['slug']}.md)"
        f"{audit_suffix(course)}"
        for index, course in enumerate(sequence_courses, 1)
    )
    course_rows: list[str] = []
    for course in ordered:
        practice_score = max(
            int(course["resource_coverage"]["practice"]),
            int(course["resource_coverage"]["labs"]),
            int(course["resource_coverage"]["code"]),
        )
        course_guide = course_guides.get(int(course["source_id"]), {})
        editorial_status = str(course_guide.get("editorial_status", "catalogue"))
        evidence_label = _editorial_evidence_label(
            editorial_status,
            language,
            review_relationship=_review_relationship(course_guide),
        )
        course_rows.append(
            f"| [{_safe(course['title'][language])}]({course['slug']}.md) "
            f"| {_safe(course['institution'])} "
            f"| {ROLE_LABELS[course['role']][0 if language == 'zh' else 1]}"
            f"{audit_suffix(course)} "
            f"| {_safe(evidence_label)} "
            f"| {PRACTICE_COVERAGE_LABELS[practice_score][0 if language == 'zh' else 1]} |"
        )
    exit_items = track["outcomes"][language]
    review_records = [
        (course, audits_by_course[int(course["source_id"])])
        for course in ordered
        if int(course["source_id"]) in audits_by_course
        and audits_by_course[int(course["source_id"])].get("status") == "review"
    ]
    if review_records:
        review_title = (
            "开始前请确认这些课程的材料限制"
            if language == "zh"
            else "Check these course materials before starting"
        )
        limitation_key = "limitation_zh" if language == "zh" else "limitation_en"
        review_lines = []
        for course, audit in review_records:
            separator = "：" if language == "zh" else ": "
            review_lines.append(
                f"    - [{_safe(course['title'][language])}]({course['slug']}.md)"
                f"{separator}{_safe(audit[limitation_key])}"
            )
        review_notice = (
            f'!!! warning "{review_title}"\n'
            + "\n".join(review_lines)
            + "\n\n"
        )
    else:
        review_notice = ""
    marker_payload = {
        "track": track,
        "courses": [course["id"] for course in ordered],
        "guide": guide,
    }
    if guide:
        guide_body = str(guide.get("bodies", {}).get(language, "")).strip()
        return (
            _front_matter(
                title,
                summary,
                "track",
                {
                    "track_id": f"track-{track['id']}",
                    "comments": True,
                },
            )
            + _marker(marker_payload)
            + f"# {_safe(title)}\n\n"
            + f"## {labels['position']}\n\n{_safe(summary)}\n\n"
            + review_notice
            + f"## {labels['prereq']}\n\n{prereq_items}\n\n"
            + guide_body
            + "\n\n"
            + f"## {labels['courses']}\n\n"
            + f"| {labels['course']} | {labels['institution']} | {labels['role']} | "
            + f"{labels['evidence']} | "
            + f"{labels['practice']} |\n"
            + "|---|---|---|---|---|\n"
            + "\n".join(course_rows)
            + "\n"
        )
    return (
        _front_matter(
            title,
            summary,
            "track",
            {
                "track_id": f"track-{track['id']}",
                "comments": True,
            },
        )
        + _marker(marker_payload)
        + f"# {_safe(title)}\n\n"
        + f"## {labels['position']}\n\n{_safe(summary)}\n\n"
        + review_notice
        + f"## {labels['prereq']}\n\n{prereq_items}\n\n"
        + f"## {labels['sequence']}\n\n{sequence}\n\n"
        + f"## {labels['courses']}\n\n"
        + f"| {labels['course']} | {labels['institution']} | {labels['role']} | "
        + f"{labels['evidence']} | "
        + f"{labels['practice']} |\n"
        + "|---|---|---|---|---|\n"
        + "\n".join(course_rows)
        + "\n\n"
        + f"## {labels['selection']}\n\n"
        + "\n".join(f"- {_safe(item)}" for item in selection)
        + "\n\n"
        + f"## {labels['exit']}\n\n"
        + "\n".join(f"- {_safe(item)}" for item in exit_items)
        + "\n"
    )


def render_catalogue_index(
    tracks: Sequence[Mapping[str, Any]],
    courses: Sequence[Mapping[str, Any]],
    language: str,
) -> str:
    used = Counter(str(course["track"]) for course in courses)
    used_tracks = [track for track in tracks if used[track["id"]]]
    if language == "zh":
        title = "课程导航"
        description = "按方向整理的电子工程公开课导航，直接说明作业、实验、访问条件和已知缺口。"
        intro = (
            "目录按方向组织课程。每篇课程页都先回答几个实际问题："
            "从哪里开始，公开了哪些作业或实验，缺了什么，以及校外学习者能否真正做下去。"
        )
        usage_title = "先选方向，再选一门课"
        usage = [
            "如果目标还不明确，先看学习路线；已经知道要学什么，可以直接进入相应方向。",
            "同一主题通常只选一门主课。先打开它的第一份作业或实验，再根据先修、访问条件和设备要求决定。",
            "页面若只有公开材料整理、尚无完整学习复盘，会直接说明；这类判断不能冒充上过课后的体验。",
        ]
        headers = ("方向", "课程数", "主线")
    else:
        title = "Course Catalogue"
        description = (
            "A bilingual catalogue of public electrical-engineering courses, with the links and practical limits needed to choose one."
        )
        intro = (
            "The catalogue organizes courses by track. Each page answers practical questions first: "
            "where to begin, which assignments or labs are public, what is missing, and whether "
            "an independent learner can realistically continue."
        )
        usage_title = "Choose a track, then one course"
        usage = [
            "If your goal is still vague, start with the learning routes. If you already know the subject, open its track directly.",
            "Usually choose one main course per subject. Open its first assignment or lab before committing, then check prerequisites, access, and equipment.",
            "A page based only on public materials says so plainly. It must not sound like experience from someone who completed the course.",
        ]
        headers = ("Track", "Courses", "Mainline")
    grouped: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for track in used_tracks:
        grouped[str(track["group"])].append(track)
    group_chunks: list[str] = []
    for group, group_tracks in grouped.items():
        group_title = GROUP_TITLES.get(group, (group, group))[0 if language == "zh" else 1]
        rows = []
        for track in sorted(group_tracks, key=lambda item: item["order"]):
            track_courses = [course for course in courses if course["track"] == track["id"]]
            rows.append(
                f"| [{_safe(track['title'][language])}]({track['id']}/index.md) "
                f"| {len(track_courses)} "
                f"| {sum(course['role'] == 'mainline' for course in track_courses)} |"
            )
        group_chunks.append(
            f"### {_safe(group_title)}\n\n"
            f"| {headers[0]} | {headers[1]} | {headers[2]} |\n"
            "|---|---:|---:|\n"
            + "\n".join(rows)
        )
    return (
        _front_matter(title, description, "catalogue")
        + _marker({"tracks": tracks, "courses": [course["id"] for course in courses]})
        + f"# {title}\n\n"
        + ("[学习路线](../routes/index.md)" if language == "zh" else "[Learning routes](../routes/index.md)")
        + f"\n\n{intro}\n\n"
        + f"## {usage_title}\n\n"
        + "\n".join(f"{index}. {_safe(item)}" for index, item in enumerate(usage, 1))
        + "\n\n## "
        + ("方向索引" if language == "zh" else "Track index")
        + "\n\n"
        + "\n\n".join(group_chunks)
        + "\n"
    )


def render_route_index(
    routes: Sequence[Mapping[str, Any]],
    courses_by_source: Mapping[int, Mapping[str, Any]],
    language: str,
) -> str:
    if language == "zh":
        title = "学习路线"
        description = "按目标组织的电子工程自学路线：告诉你先学什么、哪些课二选一，以及做到什么可以继续。"
        intro = "路线帮你控制范围和顺序，不是另一份必须逐门打卡的培养方案。先选一条主路线，只补自己真正缺的先修。"
        headers = ("路线", "适合人群", "阶段", "独立课程")
        shared_notes_heading = "使用路线前"
        shared_notes = [
            "同一知识缺口选一套主材料即可；已经具备相应能力时，直接从阶段检查开始。",
            "阶段末的题目或项目用来判断知识是否接得起来，不用为了凑数量重复做同类作业。",
            "市电、高压、射频辐射、激光、化学品或加工设备只在合规设施和合格人员现场监督下操作；条件不足时改用解析、仿真或公开数据。",
        ]
    else:
        title = "Learning Routes"
        description = (
            "Goal-oriented electrical-engineering paths that show what comes first, which courses are alternatives, and when to move on."
        )
        intro = (
            "Routes control scope and sequence; they are not rigid degree plans. Choose one main route, "
            "then fill only the prerequisite gaps you actually have."
        )
        headers = ("Route", "Audience", "Stages", "Unique courses")
        shared_notes_heading = "Before using a route"
        shared_notes = [
            "Use one main source for a given knowledge gap. If the ability is already secure, begin with the stage check.",
            "The problem or project at the end of a stage tests whether the ideas connect; there is no need to repeat similar work merely to increase the count.",
            "Operate mains, high voltage, RF emitters, lasers, chemicals, or fabrication equipment only in a compliant facility with qualified on-site supervision; otherwise use analysis, simulation, or public data.",
        ]
    rows = []
    for route in routes:
        ids = {
            course_id
            for stage in route["stages"]
            for course_id in stage["course_ids"]
            if course_id in courses_by_source
        }
        rows.append(
            f"| [{_safe(route[f'title_{language}'])}]({route['id']}.md) "
            f"| {_safe(route[f'audience_{language}'])} "
            f"| {len(route['stages'])} | {len(ids)} |"
        )
    return (
        _front_matter(title, description, "routes")
        + _marker({"routes": routes})
        + f"# {title}\n\n"
        + ("[课程导航](../courses/index.md)" if language == "zh" else "[Course catalogue](../courses/index.md)")
        + f"\n\n{_safe(intro)}\n\n"
        + f"| {headers[0]} | {headers[1]} | {headers[2]} | {headers[3]} |\n"
        + "|---|---|---:|---:|\n"
        + "\n".join(rows)
        + f"\n\n## {shared_notes_heading}\n\n"
        + "\n".join(f"- {_safe(note)}" for note in shared_notes)
        + "\n"
    )


def render_route_page(
    route: Mapping[str, Any],
    courses_by_source: Mapping[int, Mapping[str, Any]],
    language: str,
    audits_by_course: Mapping[int, Mapping[str, Any]] | None = None,
    researched_course_ids: set[int] | None = None,
) -> str:
    audits_by_course = audits_by_course or {}
    deep_course_ids = researched_course_ids
    title = str(route[f"title_{language}"])
    audience = str(route[f"audience_{language}"])
    outcome = str(route[f"outcome_{language}"])
    if language == "zh":
        labels = {
            "audience": "适合人群",
            "outcome": "学完能做什么",
            "stages": "怎么走",
            "exit": "做到这里再往下",
            "selection": "为什么这样排",
            "required": "必学",
            "elective": "选 {count} 门",
            "elective_single": "本阶段选修",
            "optional": "按需补充",
            "complete_path": "完整路线",
            "path_course": "路线内课程",
            "in_order": "按列出顺序学习",
            "path_stop": "这条分支做到哪里",
            "optional_path": "可选有序扩展",
            "extension_course": "扩展内课程",
            "extension_stop": "扩展做到哪里",
            "audit_review": "材料限制待确认",
        }
    else:
        labels = {
            "audience": "Audience",
            "outcome": "What you should be able to do",
            "stages": "How to proceed",
            "exit": "Move on when",
            "selection": "Why these courses",
            "required": "Required",
            "elective": "Choose {count}",
            "elective_single": "Stage elective",
            "optional": "Use if needed",
            "complete_path": "Complete path",
            "path_course": "Course in this path",
            "in_order": "take these in the listed order",
            "path_stop": "This branch is done when",
            "optional_path": "Optional ordered extension",
            "extension_course": "Course in this extension",
            "extension_stop": "This extension is done when",
            "audit_review": "Check material limits",
        }

    def material_limit(
        course: Mapping[str, Any],
    ) -> Mapping[str, Any] | None:
        course_id = int(course["source_id"])
        audit = audits_by_course.get(course_id)
        if audit and audit.get("status") == "review":
            return audit
        if deep_course_ids is None or course_id in deep_course_ids:
            return None
        review_note = course.get("review_note")
        if not isinstance(review_note, Mapping):
            return None
        limitation_zh = review_note.get("zh")
        limitation_en = review_note.get("en")
        verified_at = course.get("last_reviewed")
        if not all(
            isinstance(value, str) and value.strip()
            for value in (limitation_zh, limitation_en, verified_at)
        ):
            return None
        return {
            "limitation_zh": limitation_zh,
            "limitation_en": limitation_en,
            "verified_at": verified_at,
        }

    def audit_suffix(course: Mapping[str, Any]) -> str:
        if material_limit(course) is None:
            return ""
        return f"; **{labels['audit_review']}**"

    review_records: list[tuple[Mapping[str, Any], Mapping[str, Any]]] = []
    seen_review_ids: set[int] = set()
    for stage in route["stages"]:
        for course_id in stage["course_ids"]:
            if course_id in seen_review_ids:
                continue
            course = courses_by_source[course_id]
            audit = material_limit(course)
            if audit is None:
                continue
            seen_review_ids.add(course_id)
            review_records.append((course, audit))
    audit_notice = ""
    if review_records:
        if language == "zh":
            audit_lines = [
                f"    - [{_safe(course['title']['zh'])}]"
                f"({_course_href(course, 'zh', from_route=True)})："
                f"{_safe(audit['limitation_zh'])} 最近核对：{_safe(audit['verified_at'])}。"
                for course, audit in review_records
            ]
            audit_notice = (
                '!!! warning "开始前请确认这些课程的材料限制"\n'
                + "\n".join(audit_lines)
                + "\n\n"
            )
        else:
            audit_lines = [
                f"    - [{_safe(course['title']['en'])}]"
                f"({_course_href(course, 'en', from_route=True)}): "
                f"{_safe(audit['limitation_en'])} "
                f"Last checked: {_safe(audit['verified_at'])}."
                for course, audit in review_records
            ]
            audit_notice = (
                '!!! warning "Check these course materials before starting"\n'
                + "\n".join(audit_lines)
                + "\n\n"
            )
    stage_chunks: list[str] = []
    for stage in route["stages"]:
        required_ids = set(stage["required_course_ids"])
        path_options = stage.get("path_options", [])
        extension_paths = stage.get("extension_paths", [])
        path_course_ids = {
            course_id
            for option in path_options
            for course_id in option["course_ids"]
        }
        extension_course_ids = {
            course_id
            for option in extension_paths
            for course_id in option["course_ids"]
        }
        elective_count = int(stage["elective_count"])
        remaining_candidates = [
            course_id
            for course_id in stage["course_ids"]
            if course_id not in required_ids
            and course_id not in path_course_ids
            and course_id not in extension_course_ids
        ]
        elective_candidates = list(
            stage.get(
                "elective_course_ids",
                remaining_candidates if elective_count else [],
            )
        )
        elective_ids = set(elective_candidates)
        optional_candidates = [
            course_id for course_id in remaining_candidates if course_id not in elective_ids
        ]
        if path_options:
            course_sections: list[str] = []
            for course_id in stage["course_ids"]:
                if course_id not in required_ids:
                    continue
                course = courses_by_source[course_id]
                course_sections.append(
                    f"- [{_safe(course['title'][language])}]"
                    f"({_course_href(course, language, from_route=True)})"
                    f" — **{labels['required']}**; {_safe(course['institution'])}"
                    f"{audit_suffix(course)}"
                )
            for option in path_options:
                option_lines = []
                for index, course_id in enumerate(option["course_ids"], 1):
                    course = courses_by_source[course_id]
                    option_lines.append(
                        f"{index}. [{_safe(course['title'][language])}]"
                        f"({_course_href(course, language, from_route=True)})"
                        f" — **{labels['path_course']}**; {_safe(course['institution'])}"
                        f"{audit_suffix(course)}"
                    )
                course_sections.append(
                    f"**{labels['complete_path']} — "
                    f"{_safe(option[f'label_{language}'])}"
                    f"（{labels['in_order']}）**"
                    if language == "zh"
                    else f"**{labels['complete_path']} — "
                    f"{_safe(option[f'label_{language}'])} "
                    f"({labels['in_order']})**"
                )
                course_sections.append("\n".join(option_lines))
                option_stop = option.get(f"stop_when_{language}")
                if option_stop:
                    course_sections.append(
                        f"**{labels['path_stop']}{'：' if language == 'zh' else ':'}** "
                        f"{_safe(option_stop)}"
                    )
            for course_id in optional_candidates:
                course = courses_by_source[course_id]
                course_sections.append(
                    f"- [{_safe(course['title'][language])}]"
                    f"({_course_href(course, language, from_route=True)})"
                    f" — **{labels['optional']}**; {_safe(course['institution'])}"
                    f"{audit_suffix(course)}"
                )
            course_content = "\n\n".join(course_sections)
        else:
            course_lines = []
            for course_id in stage["course_ids"]:
                course = courses_by_source[course_id]
                requirement = (
                    labels["required"]
                    if course_id in required_ids
                    else (
                        labels["elective_single"]
                        if len(elective_candidates) == 1
                        else labels["elective"].format(count=elective_count)
                    )
                    if course_id in elective_ids
                    else labels["optional"]
                )
                course_lines.append(
                    f"- [{_safe(course['title'][language])}]"
                    f"({_course_href(course, language, from_route=True)})"
                    f" — **{requirement}**; {_safe(course['institution'])}"
                    f"{audit_suffix(course)}"
                )
            course_content = "\n".join(course_lines)
        extension_sections: list[str] = []
        for option in extension_paths:
            option_lines = []
            for index, course_id in enumerate(option["course_ids"], 1):
                course = courses_by_source[course_id]
                option_lines.append(
                    f"{index}. [{_safe(course['title'][language])}]"
                    f"({_course_href(course, language, from_route=True)})"
                    f" — **{labels['extension_course']}**; {_safe(course['institution'])}"
                    f"{audit_suffix(course)}"
                )
            extension_sections.append(
                f"**{labels['optional_path']} — "
                f"{_safe(option[f'label_{language}'])}"
                f"（{labels['in_order']}）**"
                if language == "zh"
                else f"**{labels['optional_path']} — "
                f"{_safe(option[f'label_{language}'])} "
                f"({labels['in_order']})**"
            )
            extension_sections.append("\n".join(option_lines))
            option_stop = option.get(f"stop_when_{language}")
            if option_stop:
                extension_sections.append(
                    f"**{labels['extension_stop']}{'：' if language == 'zh' else ':'}** "
                    f"{_safe(option_stop)}"
                )
        if extension_sections:
            course_content = "\n\n".join(
                part for part in (course_content, *extension_sections) if part
            )
        selection_rule = stage[f"selection_{language}"]
        stage_chunks.append(
            f"### {_safe(stage[f'name_{language}'])}\n\n"
            + f"**{labels['selection']}{'：' if language == 'zh' else ':'}** "
            + f"{_safe(selection_rule)}\n\n"
            + course_content
            + f"\n\n**{labels['exit']}{'：' if language == 'zh' else ':'}** "
            + f"{_safe(stage[f'exit_{language}'])}"
        )
    guidance_chunks: list[str] = []
    for section in route["guidance_sections"]:
        items = [
            _safe(item)
            for item in section[f"items_{language}"]
        ]
        if section["style"] == "prose":
            body = "\n\n".join(items)
        else:
            body = "\n".join(f"- {item}" for item in items)
        guidance_chunks.append(
            f"## {_safe(section[f'title_{language}'])}\n\n{body}"
        )
    return (
        _front_matter(
            title,
            outcome,
            "route",
            {
                "route_id": f"route-{route['id']}",
                "comments": True,
            },
        )
        + _marker(route)
        + f"# {_safe(title)}\n\n"
        + f"## {labels['audience']}\n\n{_safe(audience)}\n\n"
        + f"## {labels['outcome']}\n\n{_safe(outcome)}\n\n"
        + "\n\n".join(guidance_chunks)
        + "\n\n"
        + audit_notice
        + f"## {labels['stages']}\n\n"
        + "\n\n".join(stage_chunks)
        + "\n"
    )


def build_expected_pages(
    catalogue: Mapping[str, Any],
    routes_data: Mapping[str, Any],
    docs_root: Path,
    mainline_audit: Mapping[str, Any] | None = None,
    course_guides: Mapping[int, Mapping[str, Any]] | None = None,
    track_guides: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[Path, str]:
    tracks = sorted(catalogue["tracks"], key=lambda item: (item["order"], item["id"]))
    tracks_by_id = {track["id"]: track for track in tracks}
    courses = list(catalogue["courses"])
    courses_by_track: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for course in courses:
        courses_by_track[course["track"]].append(course)
    courses_by_source = {course["source_id"]: course for course in courses}
    audits_by_course, _ = (
        mainline_audit_annotations(mainline_audit, catalogue)
        if mainline_audit is not None
        else ({}, [])
    )
    course_guides = course_guides or {}
    track_guides = track_guides or {}
    researched_course_ids = {
        course_id
        for course_id, guide in course_guides.items()
        if guide.get("editorial_status") in {"researched", "learner-reviewed"}
    }
    pages: dict[Path, str] = {}
    for language in ("zh", "en"):
        language_root = docs_root if language == "zh" else docs_root / "en"
        course_root = language_root / "courses"
        pages[course_root / "index.md"] = render_catalogue_index(tracks, courses, language)
        for track in tracks:
            track_courses = courses_by_track.get(track["id"], [])
            if not track_courses:
                continue
            pages[course_root / track["id"] / "index.md"] = render_track_page(
                track,
                track_courses,
                tracks_by_id,
                language,
                audits_by_course,
                track_guides.get(str(track["id"])),
                course_guides,
            )
            for course in track_courses:
                pages[course_root / track["id"] / f"{course['slug']}.md"] = render_course_page(
                    course,
                    track,
                    language,
                    courses_by_source,
                    audits_by_course.get(int(course["source_id"])),
                    course_guides.get(int(course["source_id"])),
                )
        route_root = language_root / "routes"
        routes = routes_data["routes"]
        pages[route_root / "index.md"] = render_route_index(routes, courses_by_source, language)
        for route in routes:
            pages[route_root / f"{route['id']}.md"] = render_route_page(
                route,
                courses_by_source,
                language,
                audits_by_course,
                researched_course_ids,
            )
    return pages


def render_nav_fragment(
    catalogue: Mapping[str, Any],
    routes_data: Mapping[str, Any],
) -> str:
    tracks = {track["id"]: track for track in catalogue["tracks"]}
    used = sorted(
        {course["track"] for course in catalogue["courses"]},
        key=lambda track_id: (tracks[track_id]["order"], track_id),
    )
    lines = [
        "# Generated navigation fragment for review; merge its two roots into mkdocs.yml.",
        "zh:",
        "  - 课程导航: courses/index.md",
        "  - 方向:",
    ]
    for track_id in used:
        lines.append(f"      - {_safe(tracks[track_id]['title']['zh'])}: courses/{track_id}/index.md")
    lines.extend(["  - 学习路线: routes/index.md", "en:", "  - Course Catalogue: en/courses/index.md", "  - Tracks:"])
    for track_id in used:
        lines.append(
            f"      - {_safe(tracks[track_id]['title']['en'])}: en/courses/{track_id}/index.md"
        )
    lines.append("  - Learning Routes: en/routes/index.md")
    return "\n".join(lines) + "\n"


def generated_page_issues(expected: Mapping[Path, str], docs_root: Path) -> list[Issue]:
    issues: list[Issue] = []
    expected_resolved = {path.resolve() for path in expected}
    for path, content in expected.items():
        relative = display_path(path)
        if not path.exists():
            issues.append(Issue("error", "generated.missing", "generated page is missing", relative))
            continue
        current = path.read_text(encoding="utf-8")
        if current != content:
            code = "generated.protected_collision" if GENERATED_MARKER not in current else "generated.drift"
            issues.append(
                Issue(
                    "error",
                    code,
                    "page differs from deterministic generator output",
                    relative,
                )
            )
    managed_roots = [
        docs_root / "courses",
        docs_root / "en" / "courses",
        docs_root / "routes",
        docs_root / "en" / "routes",
    ]
    for root in managed_roots:
        if not root.exists():
            continue
        ensure_within(root, docs_root)
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if path.resolve() in expected_resolved:
                continue
            if (
                path.suffix.lower() == ".md"
                and GENERATED_MARKER in path.read_text(encoding="utf-8")
            ):
                issues.append(
                    Issue(
                        "error",
                        "generated.stale",
                        "stale generated page is no longer in the catalogue",
                        display_path(path),
                    )
                )
                continue
            issues.append(
                Issue(
                    "error",
                    "generated.unexpected_file",
                    "unexpected file exists in a generator-managed directory",
                    display_path(path),
                )
            )
    return issues


def write_pages(expected: Mapping[Path, str], docs_root: Path) -> list[Issue]:
    issues: list[Issue] = []
    expected_resolved = {path.resolve() for path in expected}
    for path, content in expected.items():
        ensure_within(path, docs_root)
        if path.exists():
            current = path.read_text(encoding="utf-8")
            if current != content and GENERATED_MARKER not in current:
                issues.append(
                    Issue(
                        "error",
                        "generated.protected_collision",
                        "refusing to overwrite a hand-authored page",
                        display_path(path),
                    )
                )
                continue
        atomic_write(path, content)
    for root in (
        docs_root / "courses",
        docs_root / "en" / "courses",
        docs_root / "routes",
        docs_root / "en" / "routes",
    ):
        if not root.exists():
            continue
        ensure_within(root, docs_root)
        for path in sorted(root.rglob("*.md"), reverse=True):
            if path.resolve() in expected_resolved:
                continue
            if GENERATED_MARKER in path.read_text(encoding="utf-8"):
                path.unlink()
        for directory in sorted(
            (item for item in root.rglob("*") if item.is_dir()),
            key=lambda item: len(item.parts),
            reverse=True,
        ):
            if not any(directory.iterdir()):
                directory.rmdir()
    return issues


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate deterministic bilingual course, track, and route pages."
    )
    parser.add_argument("--catalogue", default="data/courses.json")
    parser.add_argument("--schema", default="data/course.schema.json")
    parser.add_argument("--routes", default="data/routes.json")
    parser.add_argument("--route-schema", default="data/route.schema.json")
    parser.add_argument("--mainline-audit", default="data/mainline_audit.json")
    parser.add_argument("--course-guides", default="data/course_guides.json")
    parser.add_argument("--track-guides-root", default="content/track-guides")
    parser.add_argument("--docs-root", default="docs")
    parser.add_argument("--nav-fragment", default="build/generated_nav.yml")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json-report")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    catalogue_path = repo_path(args.catalogue)
    routes_path = repo_path(args.routes)
    catalogue, issues = validate_file(
        catalogue_path,
        repo_path(args.schema),
    )
    routes_data, route_validation, _ = validate_route_files(
        routes_path,
        catalogue_path,
        repo_path(args.route_schema),
    )
    issues.extend(route_validation)
    try:
        mainline_audit = load_json(repo_path(args.mainline_audit))
    except (OSError, QualityError) as exc:
        mainline_audit = None
        issues.append(
            Issue(
                "error",
                "generated.mainline_audit_load",
                str(exc),
                args.mainline_audit,
            )
        )
    if catalogue is not None and mainline_audit is not None:
        _, audit_issues = mainline_audit_annotations(
            mainline_audit,
            catalogue,
            source=args.mainline_audit,
        )
        issues.extend(audit_issues)
    if catalogue is None or routes_data is None or any(
        issue.severity == "error" for issue in issues
    ):
        emit_issues(issues)
        return exit_code(issues)
    course_guides, guide_issues = load_course_guides(
        repo_path(args.course_guides),
        catalogue,
    )
    issues.extend(guide_issues)
    track_guides, track_guide_issues = load_track_guides(
        catalogue,
        repo_path(args.track_guides_root),
    )
    issues.extend(track_guide_issues)
    if any(issue.severity == "error" for issue in issues):
        emit_issues(issues)
        return exit_code(issues)
    docs_root = repo_path(args.docs_root)
    expected = build_expected_pages(
        catalogue,
        routes_data,
        docs_root,
        mainline_audit=mainline_audit,
        course_guides=course_guides,
        track_guides=track_guides,
    )
    nav_path = repo_path(args.nav_fragment)
    nav_content = render_nav_fragment(catalogue, routes_data)
    if args.check:
        issues.extend(generated_page_issues(expected, docs_root))
        if nav_path.exists() and nav_path.read_text(encoding="utf-8") != nav_content:
            issues.append(
                Issue("error", "generated.nav_drift", "generated nav fragment is stale", args.nav_fragment)
            )
    else:
        issues.extend(write_pages(expected, docs_root))
        atomic_write(nav_path, nav_content)
        if not any(issue.severity == "error" for issue in issues):
            print(f"Wrote {len(expected)} bilingual course, track, and route pages")
    emit_issues(issues)
    write_json_report(
        repo_path(args.json_report) if args.json_report else None,
        {
            "ok": exit_code(issues) == 0,
            "expected_pages": len(expected),
            "issues": [issue.to_dict() for issue in issues],
        },
    )
    return exit_code(issues)


if __name__ == "__main__":
    raise SystemExit(main())
