from __future__ import annotations

import argparse
import html
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.course_data import ROLE_TEXT, catalogue_statistics
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
    "systems": ("数字、系统与智能硬件", "Digital, Systems, and Intelligent Hardware"),
    "waves": ("信号、通信与电磁", "Signals, Communications, and Electromagnetics"),
    "devices": ("器件、芯片与微纳", "Devices, Integrated Circuits, and Micro/Nano"),
    "energy": ("电能与可持续能源", "Electric Energy and Sustainability"),
    "practice": ("仪器、设计与跨学科实践", "Instrumentation, Design, and Practice"),
}
ROLE_LABELS = {
    "mainline": ("主线", "Mainline"),
    "alternative": ("替代", "Alternative"),
    "supplement": ("补充", "Supplement"),
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
    "review-needed": ("待人工复核", "Manual review needed"),
}
SAFETY_LABELS = {
    "simulation-only": ("仅仿真", "Simulation only"),
    "low-energy": ("低能量实验", "Low energy"),
    "supervised": ("需合格监督", "Qualified supervision required"),
    "standard": ("一般学习活动", "Standard study"),
}
COVERAGE_LABELS = {
    0: ("无公开材料", "No public material"),
    1: ("部分", "Partial"),
    2: ("完整", "Complete"),
}
COVERAGE_NAMES = {
    "video": ("视频", "Video"),
    "notes": ("讲义", "Notes"),
    "practice": ("练习", "Practice"),
    "labs": ("实验", "Labs"),
    "exams": ("考试", "Exams"),
    "code": ("代码", "Code"),
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


def _front_matter(title: str, description: str, page_type: str) -> str:
    return (
        "---\n"
        f"title: {_yaml_string(title)}\n"
        f"description: {_yaml_string(description)}\n"
        f"page_type: {page_type}\n"
        "---\n\n"
    )


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


def _list_or_default(items: Sequence[str], language: str) -> str:
    if items:
        return "\n".join(f"- {_safe(item)}" for item in items)
    return "- 无硬性先修；建议先阅读课程主页的正式要求。" if language == "zh" else (
        "- No hard prerequisite is recorded; check the provider page before starting."
    )


def _render_prerequisites(
    course: Mapping[str, Any],
    courses_by_source: Mapping[int, Mapping[str, Any]],
    language: str,
) -> str:
    items = list(course["prerequisites"][language])
    prerequisite_ids = list(course.get("prerequisite_course_ids", []))
    # course_data._course_prerequisites deterministically appends the exact
    # course-sequence requirements after the broader recommended background.
    background_items = (
        items[: -len(prerequisite_ids)] if prerequisite_ids else items
    )
    lines = [f"- {_safe(item)}" for item in background_items]
    for prerequisite_id in prerequisite_ids:
        prerequisite = courses_by_source[prerequisite_id]
        href = f"../{prerequisite['track']}/{prerequisite['slug']}.md"
        linked_title = (
            f"[《{_safe(prerequisite['title']['zh'])}》]({href})"
            if language == "zh"
            else f"[{_safe(prerequisite['title']['en'])}]({href})"
        )
        if language == "zh":
            lines.append(
                f"- 课程顺序要求：先完成{linked_title}"
                f"（{_safe(prerequisite['institution'])} "
                f"{_safe(prerequisite['course_code'])}）"
            )
        else:
            lines.append(
                f"- Course-sequence requirement: complete {linked_title} "
                f"({_safe(prerequisite['institution'])} "
                f"{_safe(prerequisite['course_code'])}) first"
            )
    if lines:
        return "\n".join(lines)
    return (
        "- 无硬性先修；建议先阅读课程主页的正式要求。"
        if language == "zh"
        else "- No hard prerequisite is recorded; check the provider page before starting."
    )


def _render_projects(course: Mapping[str, Any], language: str) -> str:
    projects = course.get("projects", [])
    if projects:
        chunks: list[str] = []
        for project in projects:
            title = project["title"][language]
            brief = project["brief"][language]
            deliverables = project["deliverables"][language]
            verification = project["verification"][language]
            reproducibility = project["reproducibility"][language]
            deliverable_label = "交付物" if language == "zh" else "Deliverables"
            verification_label = "验收" if language == "zh" else "Verification"
            reproducibility_label = "复现要求" if language == "zh" else "Reproducibility"
            origin_label = "来源" if language == "zh" else "Origin"
            origin_value = (
                ("课程官方项目" if language == "zh" else "Official course project")
                if project["origin"] == "official"
                else ("维护者建议项目" if language == "zh" else "Maintainer-suggested project")
            )
            safety_label = "安全边界" if language == "zh" else "Safety boundary"
            safety_level = SAFETY_LABELS[project["safety_level"]][
                0 if language == "zh" else 1
            ]
            label_separator = "：" if language == "zh" else ":"
            chunks.append(
                f"### {_safe(title)}\n\n"
                f"{_safe(brief)}\n\n"
                f"**{origin_label}{label_separator}** {_safe(origin_value)}\n\n"
                f"**{deliverable_label}**\n\n"
                + "\n".join(f"- {_safe(item)}" for item in deliverables)
                + f"\n\n**{verification_label}**\n\n"
                + "\n".join(f"- {_safe(item)}" for item in verification)
                + f"\n\n**{reproducibility_label}**\n\n"
                + "\n".join(f"- {_safe(item)}" for item in reproducibility)
                + f"\n\n**{safety_label}{label_separator}** {_safe(safety_level)} — "
                + _safe(project["safety_note"][language])
            )
        return "\n\n".join(chunks)
    coverage = course["resource_coverage"]
    if language == "zh":
        steps = [
            "选取一组代表性题目，保留完整推导、单位检查与错误订正。",
            "用独立方法复核至少一个关键结论，例如数值计算、极限情形或仿真。",
        ]
        if coverage["labs"]:
            steps.append("复现实验并保存电路、仪器设置、原始数据、不确定度和安全检查。")
        if coverage["code"]:
            steps.append("固定依赖与随机种子，提供一条命令重现结果，并加入自动化断言。")
        if not coverage["labs"] and not coverage["code"]:
            steps.append("自行设计一个小型仿真或测量任务，弥补课程公开实践材料的缺口。")
    else:
        steps = [
            "Solve a representative problem set with full derivations, unit checks, and corrected errors.",
            "Verify at least one central result independently using numerics, a limiting case, or simulation.",
        ]
        if coverage["labs"]:
            steps.append(
                "Reproduce a lab while preserving schematics, instrument settings, raw data, uncertainty, and safety checks."
            )
        if coverage["code"]:
            steps.append(
                "Pin dependencies and random seeds, provide one-command reproduction, and add automated assertions."
            )
        if not coverage["labs"] and not coverage["code"]:
            steps.append(
                "Design a small simulation or measurement task to close the public-practice gap."
            )
    return "\n".join(f"{index}. {_safe(step)}" for index, step in enumerate(steps, 1))


def render_course_page(
    course: Mapping[str, Any],
    track: Mapping[str, Any],
    language: str,
    courses_by_source: Mapping[int, Mapping[str, Any]],
    audit: Mapping[str, Any] | None = None,
) -> str:
    other = "en" if language == "zh" else "zh"
    title = str(course["title"][language])
    summary = str(course["summary"][language])
    track_title = str(track["title"][language])
    role = ROLE_LABELS[str(course["role"])][0 if language == "zh" else 1]
    level = LEVEL_LABELS[str(course["level"])][0 if language == "zh" else 1]
    language_link = (
        f"[English](../../en/courses/{course['track']}/{course['slug']}.md)"
        if language == "zh"
        else f"[中文](../../../courses/{course['track']}/{course['slug']}.md)"
    )
    if language == "zh":
        labels = {
            "position": "课程定位",
            "why": "为什么选择这门课",
            "before": "学习前准备",
            "outcomes": "可验证的学习成果",
            "workload": "工时与节奏",
            "tooling": "软件、硬件与成本",
            "software": "软件",
            "hardware": "硬件",
            "cost": "成本说明",
            "safety": "安全等级",
            "coverage": "公开资源完整度",
            "resources": "资源与访问条件",
            "practice": "实践闭环",
            "risk": "风险、缺口与边界",
            "evidence": "完成证据",
            "institution": "机构",
            "code": "课程编号",
            "track": "方向",
            "tier": "评级",
            "role": "角色",
            "level": "难度",
            "reviewed": "最近复核",
            "kind": "资源",
            "access": "访问",
            "license": "许可",
            "status": "状态",
            "verified": "复核日期",
            "attribute": "属性",
            "value": "值",
            "resource_type": "资源类型",
            "completeness": "完整度",
        }
        notice = (
            "“官方页已列出”表示核验日从成功访问的官方来源页发现该链接，不保证目标文件"
            "在所有地区或账号状态下都能直接打开。访问不代表获得再分发权；下载、改编或"
            "公开发布前，应重新核对提供方页面、目标链接及其中第三方材料的许可。"
        )
    else:
        labels = {
            "position": "Course position",
            "why": "Why choose this course",
            "before": "Before you start",
            "outcomes": "Verifiable learning outcomes",
            "workload": "Workload and pacing",
            "tooling": "Software, hardware, and cost",
            "software": "Software",
            "hardware": "Hardware",
            "cost": "Cost note",
            "safety": "Safety level",
            "coverage": "Public resource coverage",
            "resources": "Resources and access",
            "practice": "Practice loop",
            "risk": "Risks, gaps, and boundaries",
            "evidence": "Completion evidence",
            "institution": "Institution",
            "code": "Course code",
            "track": "Track",
            "tier": "Tier",
            "role": "Role",
            "level": "Level",
            "reviewed": "Last reviewed",
            "kind": "Resource",
            "access": "Access",
            "license": "License",
            "status": "Status",
            "verified": "Verified",
            "attribute": "Attribute",
            "value": "Value",
            "resource_type": "Resource type",
            "completeness": "Completeness",
        }
        notice = (
            "“Listed by official page” means the link was discovered on a successfully fetched "
            "official source on the verification date; it does not guarantee that every region "
            "or account can open the target directly. Access does not grant redistribution rights. "
            "Re-check the provider page, target link, and third-party notices before downloading, "
            "adapting, or publishing material."
        )
    audit_notice = ""
    if audit and audit.get("status") == "review":
        if language == "zh":
            audit_notice = (
                '!!! warning "主线审计复核中"\n'
                f"    这门主线课程仍需人工复核：{_safe(audit['limitation_zh'])} "
                f"最近审计：{_safe(audit['verified_at'])}。\n\n"
            )
        else:
            audit_notice = (
                '!!! warning "Mainline audit review"\n'
                "    This mainline course still requires manual review: "
                f"{_safe(audit['limitation_en'])} "
                f"Last audited: {_safe(audit['verified_at'])}.\n\n"
            )
    metadata_rows = [
        (labels["institution"], course["institution"]),
        (labels["code"], course["course_code"] or "—"),
        (labels["track"], f"[{_safe(track_title)}](index.md)"),
        (labels["tier"], course["tier"]),
        (labels["role"], role),
        (labels["level"], level),
        (labels["reviewed"], course["last_reviewed"]),
    ]
    metadata_table = (
        f"| {labels['attribute']} | {labels['value']} |\n|---|---|\n"
        + "\n".join(
            f"| **{_safe(key)}** | "
            f"{_safe(value) if not str(value).startswith('[') else value} |"
            for key, value in metadata_rows
        )
    )
    coverage_rows = "\n".join(
        f"| {COVERAGE_NAMES[key][0 if language == 'zh' else 1]} | "
        f"{COVERAGE_LABELS[int(course['resource_coverage'][key])][0 if language == 'zh' else 1]} |"
        for key in COVERAGE_NAMES
    )
    resource_rows: list[str] = []
    for resource in course["resources"]:
        access = ACCESS_LABELS[str(resource["access"])][0 if language == "zh" else 1]
        status = STATUS_LABELS[str(resource["status"])][0 if language == "zh" else 1]
        resource_rows.append(
            f"| [{_safe(resource['title'][language])}]({resource['url']}) "
            f"| {_safe(access)} | {_safe(resource['license'])} | {_safe(status)} "
            f"| {resource['last_verified']} |"
        )
    prerequisites = _render_prerequisites(course, courses_by_source, language)
    outcomes = _list_or_default(course["outcomes"][language], language)
    study_plan = course["study_plan"]
    if study_plan["estimated_weeks"] is None or study_plan["hours_per_week"] is None:
        workload_value = "暂无可信估计" if language == "zh" else "No credible estimate yet"
    else:
        workload_value = (
            f"{study_plan['estimated_weeks']} 周，每周 {study_plan['hours_per_week']} 小时"
            if language == "zh"
            else f"{study_plan['estimated_weeks']} weeks at {study_plan['hours_per_week']} hours/week"
        )
    software = _list_or_default(course["tooling"]["software"][language], language)
    hardware = _list_or_default(course["tooling"]["hardware"][language], language)
    safety_level = SAFETY_LABELS[course["safety"]["level"]][
        0 if language == "zh" else 1
    ]
    sentence_stop = "。" if language == "zh" else "."
    evidence = course["completion_evidence"][language]
    content = (
        _front_matter(title, summary, "course")
        + _marker(course)
        + f"# {_safe(title)}\n\n"
        + f"{language_link} · [← {_safe(track_title)}](index.md)\n\n"
        + f"> {_safe(summary)}\n\n"
        + audit_notice
        + f"## {labels['position']}\n\n{metadata_table}\n\n"
        + f"## {labels['why']}\n\n{_safe(course['selection_note'][language])}\n\n"
        + f"## {labels['before']}\n\n{prerequisites}\n\n"
        + f"## {labels['outcomes']}\n\n{outcomes}\n\n"
        + f"## {labels['workload']}\n\n"
        + f"**{_safe(workload_value)}{sentence_stop}** {_safe(study_plan['note'][language])}\n\n"
        + f"## {labels['tooling']}\n\n"
        + f"### {labels['software']}\n\n{software}\n\n"
        + f"### {labels['hardware']}\n\n{hardware}\n\n"
        + f"### {labels['cost']}\n\n{_safe(course['tooling']['cost_note'][language])}\n\n"
        + f"## {labels['safety']}\n\n"
        + f"**{_safe(safety_level)}{sentence_stop}** {_safe(course['safety']['note'][language])}\n\n"
        + f"## {labels['coverage']}\n\n"
        + f"| {labels['resource_type']} | {labels['completeness']} |\n|---|---|\n"
        + coverage_rows
        + "\n\n"
        + f"## {labels['resources']}\n\n"
        + f"| {labels['kind']} | {labels['access']} | {labels['license']} | "
        + f"{labels['status']} | {labels['verified']} |\n"
        + "|---|---|---|---|---|\n"
        + "\n".join(resource_rows)
        + f"\n\n> {_safe(notice)}\n\n"
        + f"## {labels['practice']}\n\n{_render_projects(course, language)}\n\n"
        + f"## {labels['risk']}\n\n{_safe(course['review_note'][language])}\n\n"
        + f"## {labels['evidence']}\n\n"
        + "\n".join(f"- {_safe(item)}" for item in evidence)
        + "\n"
    )
    return content


def render_track_page(
    track: Mapping[str, Any],
    courses: Sequence[Mapping[str, Any]],
    tracks_by_id: Mapping[str, Mapping[str, Any]],
    language: str,
    audits_by_course: Mapping[int, Mapping[str, Any]] | None = None,
) -> str:
    title = str(track["title"][language])
    summary = str(track["summary"][language])
    other_link = (
        f"[English](../../en/courses/{track['id']}/index.md)"
        if language == "zh"
        else f"[中文](../../../courses/{track['id']}/index.md)"
    )
    ordered = sorted(courses, key=_course_sort_key)
    prerequisites = [
        tracks_by_id[track_id]
        for track_id in track.get("prerequisite_tracks", [])
        if track_id in tracks_by_id
    ]
    if language == "zh":
        labels = {
            "catalogue": "课程总览",
            "position": "方向定位",
            "prereq": "建议先修方向",
            "sequence": "建议顺序",
            "courses": "课程清单",
            "course": "课程",
            "institution": "机构",
            "role": "角色",
            "tier": "评级",
            "practice": "实践资源",
            "selection": "如何选课",
            "exit": "方向验收",
        }
        selection = [
            "第一次系统学习优先选择审计通过的主线课程；标为“审计复核中”的记录须先阅读限制，且同一阶段通常不需要并行完成多个替代课程。",
            "评级衡量公开材料完整度和自学可执行性，不代表学校、教师或学术声望排序。",
            "补充课程只用于填补某个主题、工具或实践缺口。",
        ]
    else:
        labels = {
            "catalogue": "Course catalogue",
            "position": "Track position",
            "prereq": "Recommended prerequisite tracks",
            "sequence": "Suggested order",
            "courses": "Courses",
            "course": "Course",
            "institution": "Institution",
            "role": "Role",
            "tier": "Tier",
            "practice": "Practice coverage",
            "selection": "How to choose",
            "exit": "Track completion",
        }
        selection = [
            "For a first systematic pass, start with audit-passed mainline courses; read the limitation before using a record marked “Audit review,” and rarely take parallel alternatives.",
            "Tiers measure public-resource completeness and self-study executability, not institutional or instructor prestige.",
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

    def audit_suffix(course: Mapping[str, Any]) -> str:
        audit = audits_by_course.get(int(course["source_id"]))
        if not audit or audit.get("status") != "review":
            return ""
        return " — 审计复核中" if language == "zh" else " — Audit review"

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
        course_rows.append(
            f"| [{_safe(course['title'][language])}]({course['slug']}.md) "
            f"| {_safe(course['institution'])} "
            f"| {ROLE_LABELS[course['role']][0 if language == 'zh' else 1]}"
            f"{audit_suffix(course)} "
            f"| {course['tier']} "
            f"| {COVERAGE_LABELS[practice_score][0 if language == 'zh' else 1]} |"
        )
    exit_items = track["outcomes"][language]
    review_records = [
        (course, audits_by_course[int(course["source_id"])])
        for course in ordered
        if int(course["source_id"]) in audits_by_course
        and audits_by_course[int(course["source_id"])].get("status") == "review"
    ]
    if review_records:
        review_title = "主线审计复核中" if language == "zh" else "Mainline audit review"
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
    return (
        _front_matter(title, summary, "track")
        + _marker({"track": track, "courses": [course["id"] for course in ordered]})
        + f"# {_safe(title)}\n\n"
        + f"{other_link} · [← {labels['catalogue']}](../index.md)\n\n"
        + f"## {labels['position']}\n\n{_safe(summary)}\n\n"
        + review_notice
        + f"## {labels['prereq']}\n\n{prereq_items}\n\n"
        + f"## {labels['sequence']}\n\n{sequence}\n\n"
        + f"## {labels['courses']}\n\n"
        + f"| {labels['course']} | {labels['institution']} | {labels['role']} | "
        + f"{labels['tier']} | {labels['practice']} |\n"
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
    other_link = (
        "[English](../en/courses/index.md)"
        if language == "zh"
        else "[中文](../../courses/index.md)"
    )
    stats = catalogue_statistics({"tracks": tracks, "courses": courses})
    if language == "zh":
        title = "课程导航"
        description = "按方向、角色、资源完整度和实践条件筛选的电子工程公开课程目录。"
        intro = (
            f"当前目录收录 **{stats['courses']}** 门经过结构化复核的课程，覆盖 "
            f"**{stats['tracks_used']}** 个有课程方向。每个资源都记录访问条件、许可、"
            "状态和最近复核日期。"
        )
        usage_title = "使用方法"
        usage = [
            "先从学习路线确定目标和阶段，再进入对应方向选择一门主线课程。",
            "打开课程页检查先修、实践资源、访问条件和风险；不要只按评级选课。",
            "以页面列出的完成证据为退出标准，再进入下一阶段。",
        ]
        headers = ("方向", "课程数", "S 级", "主线")
    else:
        title = "Course Catalogue"
        description = (
            "Open electrical-engineering courses screened by track, role, resource completeness, and practice conditions."
        )
        intro = (
            f"The catalogue contains **{stats['courses']}** structurally reviewed courses across "
            f"**{stats['tracks_used']}** populated tracks. Every resource records access, license, "
            "status, and its latest verification date."
        )
        usage_title = "How to use the catalogue"
        usage = [
            "Choose a goal and stage from the learning routes, then select one mainline course in the matching track.",
            "Inspect prerequisites, practice material, access, and risks on the course page; do not choose by tier alone.",
            "Meet the page's completion-evidence standard before advancing.",
        ]
        headers = ("Track", "Courses", "S tier", "Mainline")
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
                f"| {sum(course['tier'] == 'S' for course in track_courses)} "
                f"| {sum(course['role'] == 'mainline' for course in track_courses)} |"
            )
        group_chunks.append(
            f"### {_safe(group_title)}\n\n"
            f"| {headers[0]} | {headers[1]} | {headers[2]} | {headers[3]} |\n"
            "|---|---:|---:|---:|\n"
            + "\n".join(rows)
        )
    return (
        _front_matter(title, description, "catalogue")
        + _marker({"tracks": tracks, "courses": [course["id"] for course in courses]})
        + f"# {title}\n\n"
        + f"{other_link} · "
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
    other_link = (
        "[English](../en/routes/index.md)"
        if language == "zh"
        else "[中文](../../routes/index.md)"
    )
    if language == "zh":
        title = "学习路线"
        description = "按目标组织的分阶段电子工程自学路线，每个阶段指向经过复核的课程和明确验收结果。"
        intro = "路线用于控制范围和顺序，不是必须逐门完成的固定培养方案。先选择一条主路线，再按先修缺口补课。"
        headers = ("路线", "适合人群", "阶段", "独立课程")
    else:
        title = "Learning Routes"
        description = (
            "Goal-oriented, staged electrical-engineering pathways with reviewed courses and explicit outcomes."
        )
        intro = (
            "Routes control scope and sequence; they are not rigid degree plans. Choose one main route, "
            "then fill only the prerequisite gaps you actually have."
        )
        headers = ("Route", "Audience", "Stages", "Unique courses")
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
        + f"{other_link} · "
        + ("[课程导航](../courses/index.md)" if language == "zh" else "[Course catalogue](../courses/index.md)")
        + f"\n\n{_safe(intro)}\n\n"
        + f"| {headers[0]} | {headers[1]} | {headers[2]} | {headers[3]} |\n"
        + "|---|---|---:|---:|\n"
        + "\n".join(rows)
        + "\n"
    )


def render_route_page(
    route: Mapping[str, Any],
    courses_by_source: Mapping[int, Mapping[str, Any]],
    language: str,
    audits_by_course: Mapping[int, Mapping[str, Any]] | None = None,
) -> str:
    audits_by_course = audits_by_course or {}
    title = str(route[f"title_{language}"])
    audience = str(route[f"audience_{language}"])
    outcome = str(route[f"outcome_{language}"])
    other_link = (
        f"[English](../en/routes/{route['id']}.md)"
        if language == "zh"
        else f"[中文](../../routes/{route['id']}.md)"
    )
    if language == "zh":
        labels = {
            "routes": "学习路线",
            "audience": "适合人群",
            "outcome": "最终验收",
            "stages": "阶段安排",
            "rule": "执行规则",
            "exit": "阶段退出条件",
            "selection": "选课要求",
            "required": "必修",
            "elective": "选修候选",
            "optional": "可选补充",
            "complete_path": "完整路径选项",
            "path_course": "路径内课程",
            "in_order": "按序完成",
            "audit_review": "审计复核中",
        }
        rules = [
            "按每个阶段的选课要求完成全部必修与指定数量的选修；若提供完整路径选项，只选择一条并按序完成其中全部课程；可选补充只用于填补明确缺口。",
            "阶段内至少完成一个可复现产物，并把失败记录纳入复盘。",
            "涉及市电、高压、射频辐射、激光、化学品或加工设备时，必须遵守本地法规并由合格人员监督。",
        ]
    else:
        labels = {
            "routes": "Learning routes",
            "audience": "Audience",
            "outcome": "Final outcome",
            "stages": "Stages",
            "rule": "Execution rules",
            "exit": "Stage exit criterion",
            "selection": "Selection rule",
            "required": "Required",
            "elective": "Elective option",
            "optional": "Optional supplement",
            "complete_path": "Complete path option",
            "path_course": "Course in selected path",
            "in_order": "complete in the listed order",
            "audit_review": "Audit review",
        }
        rules = [
            "Follow each stage's selection rule: complete every required course and the stated number of electives; when complete path options are provided, choose one and finish every course in its listed order; use optional supplements only to close a specific gap.",
            "Produce at least one reproducible artifact per stage and include failed attempts in the retrospective.",
            "Work involving mains voltage, high voltage, RF exposure, lasers, chemicals, or fabrication equipment requires local-law compliance and qualified supervision.",
        ]

    def audit_suffix(course: Mapping[str, Any]) -> str:
        audit = audits_by_course.get(int(course["source_id"]))
        if not audit or audit.get("status") != "review":
            return ""
        return f"; **{labels['audit_review']}**"

    review_records: list[tuple[Mapping[str, Any], Mapping[str, Any]]] = []
    seen_review_ids: set[int] = set()
    for stage in route["stages"]:
        for course_id in stage["course_ids"]:
            if course_id in seen_review_ids:
                continue
            audit = audits_by_course.get(course_id)
            if not audit or audit.get("status") != "review":
                continue
            seen_review_ids.add(course_id)
            review_records.append((courses_by_source[course_id], audit))
    audit_notice = ""
    if review_records:
        if language == "zh":
            audit_lines = [
                f"    - [{_safe(course['title']['zh'])}]"
                f"({_course_href(course, 'zh', from_route=True)})："
                f"{_safe(audit['limitation_zh'])} 最近审计：{_safe(audit['verified_at'])}。"
                for course, audit in review_records
            ]
            audit_notice = (
                '!!! warning "路线中的主线审计复核项"\n'
                + "\n".join(audit_lines)
                + "\n\n"
            )
        else:
            audit_lines = [
                f"    - [{_safe(course['title']['en'])}]"
                f"({_course_href(course, 'en', from_route=True)}): "
                f"{_safe(audit['limitation_en'])} "
                f"Last audited: {_safe(audit['verified_at'])}."
                for course, audit in review_records
            ]
            audit_notice = (
                '!!! warning "Mainline audit review in this route"\n'
                + "\n".join(audit_lines)
                + "\n\n"
            )
    stage_chunks: list[str] = []
    for stage in route["stages"]:
        required_ids = set(stage["required_course_ids"])
        path_options = stage.get("path_options", [])
        path_course_ids = {
            course_id
            for option in path_options
            for course_id in option["course_ids"]
        }
        elective_count = int(stage["elective_count"])
        remaining_candidates = [
            course_id
            for course_id in stage["course_ids"]
            if course_id not in required_ids and course_id not in path_course_ids
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
                role = ROLE_LABELS[course["role"]][0 if language == "zh" else 1]
                course_sections.append(
                    f"- [{_safe(course['title'][language])}]"
                    f"({_course_href(course, language, from_route=True)})"
                    f" — **{labels['required']}**; {_safe(course['institution'])}; "
                    f"{role}; {course['tier']}{audit_suffix(course)}"
                )
            for option in path_options:
                option_lines = []
                for index, course_id in enumerate(option["course_ids"], 1):
                    course = courses_by_source[course_id]
                    role = ROLE_LABELS[course["role"]][0 if language == "zh" else 1]
                    option_lines.append(
                        f"{index}. [{_safe(course['title'][language])}]"
                        f"({_course_href(course, language, from_route=True)})"
                        f" — **{labels['path_course']}**; {_safe(course['institution'])}; "
                        f"{role}; {course['tier']}{audit_suffix(course)}"
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
            for course_id in optional_candidates:
                course = courses_by_source[course_id]
                role = ROLE_LABELS[course["role"]][0 if language == "zh" else 1]
                course_sections.append(
                    f"- [{_safe(course['title'][language])}]"
                    f"({_course_href(course, language, from_route=True)})"
                    f" — **{labels['optional']}**; {_safe(course['institution'])}; "
                    f"{role}; {course['tier']}{audit_suffix(course)}"
                )
            if language == "zh":
                required_clause = (
                    f"完成全部 {len(required_ids)} 门必修；" if required_ids else ""
                )
                selection_rule = (
                    f"{required_clause}从以下 {len(path_options)} 条完整路径中选择 1 条，"
                    "并按列出顺序完成所选路径的全部课程。"
                )
            else:
                required_noun = "course" if len(required_ids) == 1 else "courses"
                required_clause = (
                    f"Complete all {len(required_ids)} required {required_noun}; "
                    if required_ids
                    else ""
                )
                selection_rule = (
                    f"{required_clause}choose 1 of the {len(path_options)} complete paths below "
                    "and finish every course in the selected path in the listed order."
                )
            course_content = "\n\n".join(course_sections)
        else:
            course_lines = []
            for course_id in stage["course_ids"]:
                course = courses_by_source[course_id]
                role = ROLE_LABELS[course["role"]][0 if language == "zh" else 1]
                requirement = (
                    labels["required"]
                    if course_id in required_ids
                    else labels["elective"]
                    if course_id in elective_ids
                    else labels["optional"]
                )
                course_lines.append(
                    f"- [{_safe(course['title'][language])}]"
                    f"({_course_href(course, language, from_route=True)})"
                    f" — **{requirement}**; {_safe(course['institution'])}; {role}; "
                    f"{course['tier']}{audit_suffix(course)}"
                )
            if language == "zh":
                if elective_count:
                    elective_clause = (
                        "并完成该门选修候选。"
                        if elective_count == len(elective_candidates) == 1
                        else (
                            f"并完成全部 {len(elective_candidates)} 门选修候选。"
                            if elective_count == len(elective_candidates)
                            else f"并从 {len(elective_candidates)} 门选修候选中选择 "
                            f"{elective_count} 门。"
                        )
                    )
                    selection_rule = (
                        f"完成全部 {len(required_ids)} 门必修，{elective_clause}"
                        + (
                            f"其余 {len(optional_candidates)} 门为可选补充，不计入本阶段选修数。"
                            if optional_candidates
                            else ""
                        )
                    )
                else:
                    selection_rule = (
                        f"完成全部 {len(required_ids)} 门必修；其余 {len(optional_candidates)} 门仅在需要补缺时选学。"
                        if optional_candidates
                        else f"完成全部 {len(required_ids)} 门必修。"
                    )
            else:
                required_noun = "course" if len(required_ids) == 1 else "courses"
                elective_noun = "option" if len(elective_candidates) == 1 else "options"
                if elective_count:
                    elective_clause = (
                        "complete the elective option."
                        if elective_count == len(elective_candidates) == 1
                        else (
                            f"complete all {len(elective_candidates)} elective options."
                            if elective_count == len(elective_candidates)
                            else f"choose {elective_count} of {len(elective_candidates)} "
                            f"elective {elective_noun}."
                        )
                    )
                    optional_clause = ""
                    if len(optional_candidates) == 1:
                        optional_clause = (
                            " The other course is an optional supplement and does not "
                            "count toward the elective requirement."
                        )
                    elif optional_candidates:
                        optional_clause = (
                            f" The other {len(optional_candidates)} courses are optional "
                            "supplements and do not count toward the elective requirement."
                        )
                    selection_rule = (
                        f"Complete all {len(required_ids)} required {required_noun} and "
                        f"{elective_clause}{optional_clause}"
                    )
                else:
                    selection_rule = (
                        f"Complete all {len(required_ids)} required {required_noun}; use the other "
                        f"{len(optional_candidates)} "
                        f"{'option' if len(optional_candidates) == 1 else 'options'} "
                        "only to close a specific gap."
                        if optional_candidates
                        else f"Complete all {len(required_ids)} required {required_noun}."
                    )
            course_content = "\n".join(course_lines)
        stage_chunks.append(
            f"### {_safe(stage[f'name_{language}'])}\n\n"
            + f"**{labels['selection']}{'：' if language == 'zh' else ':'}** "
            + f"{_safe(selection_rule)}\n\n"
            + course_content
            + f"\n\n**{labels['exit']}{'：' if language == 'zh' else ':'}** "
            + f"{_safe(stage[f'exit_{language}'])}"
        )
    return (
        _front_matter(title, outcome, "route")
        + _marker(route)
        + f"# {_safe(title)}\n\n"
        + f"{other_link} · [← {labels['routes']}](index.md)\n\n"
        + f"## {labels['audience']}\n\n{_safe(audience)}\n\n"
        + f"## {labels['outcome']}\n\n{_safe(outcome)}\n\n"
        + audit_notice
        + f"## {labels['stages']}\n\n"
        + "\n\n".join(stage_chunks)
        + f"\n\n## {labels['rule']}\n\n"
        + "\n".join(f"- {_safe(rule)}" for rule in rules)
        + "\n"
    )


def build_expected_pages(
    catalogue: Mapping[str, Any],
    routes_data: Mapping[str, Any],
    docs_root: Path,
    mainline_audit: Mapping[str, Any] | None = None,
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
            )
            for course in track_courses:
                pages[course_root / track["id"] / f"{course['slug']}.md"] = render_course_page(
                    course,
                    track,
                    language,
                    courses_by_source,
                    audits_by_course.get(int(course["source_id"])),
                )
        route_root = language_root / "routes"
        routes = routes_data["routes"]
        pages[route_root / "index.md"] = render_route_index(routes, courses_by_source, language)
        for route in routes:
            pages[route_root / f"{route['id']}.md"] = render_route_page(
                route, courses_by_source, language, audits_by_course
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
    parser.add_argument("--docs-root", default="docs")
    parser.add_argument("--nav-fragment", default="build/generated_nav.yml")
    parser.add_argument("--minimum-courses", type=int, default=125)
    parser.add_argument("--minimum-used-tracks", type=int, default=24)
    parser.add_argument("--minimum-routes", type=int, default=10)
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
        minimum_courses=args.minimum_courses,
        minimum_used_tracks=args.minimum_used_tracks,
    )
    routes_data, route_validation, _ = validate_route_files(
        routes_path,
        catalogue_path,
        repo_path(args.route_schema),
        minimum_routes=args.minimum_routes,
        minimum_unique_courses=100,
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
    docs_root = repo_path(args.docs_root)
    expected = build_expected_pages(
        catalogue,
        routes_data,
        docs_root,
        mainline_audit=mainline_audit,
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
