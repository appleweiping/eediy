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


TEMPLATE_FIELDS = {
    "track",
    "title",
    "brief",
    "deliverables",
    "verification",
    "reproducibility",
    "safety_level",
    "safety_note",
}
LOCALIZED_TEXT_FIELDS = ("title", "brief", "safety_note")
LOCALIZED_LIST_MINIMUMS = {
    "deliverables": 4,
    "verification": 4,
    "reproducibility": 3,
}
SAFETY_LEVELS = {"simulation-only", "low-energy", "supervised", "standard"}
HIGH_RISK_TRACKS = {
    "fabrication-mems",
    "optics-photonics",
    "power-electronics",
    "power-systems-machines",
    "energy-storage-pv",
    "rf-microwave-antennas",
    "robotics",
    "capstone-practice",
}
LOW_ENERGY_TRACKS = {
    "ee-introduction",
    "circuits",
    "electronics-laboratory",
    "analog-electronics",
    "fpga-soc",
    "embedded-systems",
    "pcb-eda",
    "sensors-instrumentation",
}
FORMAT_FIELDS = {"course_title", "track_title"}


def _localized_text_issues(value: Any, *, path: str) -> list[Issue]:
    if not isinstance(value, Mapping):
        return [Issue("error", "project_template.localized", "must be an object", path)]
    issues: list[Issue] = []
    if set(value) != {"zh", "en"}:
        issues.append(
            Issue(
                "error",
                "project_template.languages",
                "localized text must contain exactly zh and en",
                path,
            )
        )
    for language in ("zh", "en"):
        text = value.get(language)
        if not isinstance(text, str) or not text.strip():
            issues.append(
                Issue(
                    "error",
                    "project_template.translation",
                    f"{language} translation must be non-empty",
                    path,
                )
            )
    return issues


def _localized_list_issues(value: Any, *, path: str, minimum: int) -> list[Issue]:
    if not isinstance(value, Mapping):
        return [Issue("error", "project_template.localized_list", "must be an object", path)]
    issues: list[Issue] = []
    if set(value) != {"zh", "en"}:
        issues.append(
            Issue(
                "error",
                "project_template.languages",
                "localized list must contain exactly zh and en",
                path,
            )
        )
    lengths: dict[str, int] = {}
    for language in ("zh", "en"):
        items = value.get(language)
        if not isinstance(items, list):
            issues.append(
                Issue(
                    "error",
                    "project_template.translation_list",
                    f"{language} must be a list",
                    path,
                )
            )
            continue
        lengths[language] = len(items)
        if len(items) < minimum:
            issues.append(
                Issue(
                    "error",
                    "project_template.evidence_count",
                    f"{language} requires at least {minimum} items; found {len(items)}",
                    path,
                )
            )
        if any(not isinstance(item, str) or not item.strip() for item in items):
            issues.append(
                Issue(
                    "error",
                    "project_template.empty_evidence",
                    f"{language} contains an empty item",
                    path,
                )
            )
    if lengths.get("zh") != lengths.get("en"):
        issues.append(
            Issue(
                "error",
                "project_template.cardinality",
                "zh and en evidence lists must have equal length",
                path,
            )
        )
    return issues


def _format_names(text: str) -> set[str]:
    return set(re.findall(r"\{([a-z_][a-z0-9_]*)\}", text))


def validate_project_templates(
    templates_value: Any,
    taxonomy_value: Any,
    *,
    templates_source: str = "data/project_templates.json",
    taxonomy_source: str = "data/tracks.json",
) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(taxonomy_value, Mapping) or not isinstance(
        taxonomy_value.get("tracks"), list
    ):
        return [
            Issue(
                "error",
                "project_template.taxonomy",
                "taxonomy must contain tracks[]",
                taxonomy_source,
            )
        ]
    taxonomy_tracks = taxonomy_value["tracks"]
    taxonomy_ids = {
        str(track.get("id"))
        for track in taxonomy_tracks
        if isinstance(track, Mapping) and track.get("id")
    }
    if not isinstance(templates_value, Mapping):
        return [
            Issue(
                "error",
                "project_template.root",
                "template file must be an object",
                templates_source,
            )
        ]
    if templates_value.get("schema_version") != "1.0.0":
        issues.append(
            Issue(
                "error",
                "project_template.schema_version",
                "schema_version must be 1.0.0",
                templates_source,
            )
        )
    templates = templates_value.get("templates")
    if not isinstance(templates, list):
        return issues + [
            Issue(
                "error",
                "project_template.shape",
                "template file must contain templates[]",
                templates_source,
            )
        ]
    seen_tracks: set[str] = set()
    content_fingerprints: dict[tuple[str, str], str] = {}
    for index, template in enumerate(templates):
        path = f"{templates_source}:templates/{index}"
        if not isinstance(template, Mapping):
            issues.append(
                Issue("error", "project_template.item", "template must be an object", path)
            )
            continue
        fields = set(template)
        if fields != TEMPLATE_FIELDS:
            missing = sorted(TEMPLATE_FIELDS - fields)
            extra = sorted(fields - TEMPLATE_FIELDS)
            detail = []
            if missing:
                detail.append(f"missing {', '.join(missing)}")
            if extra:
                detail.append(f"unexpected {', '.join(extra)}")
            issues.append(
                Issue(
                    "error",
                    "project_template.fields",
                    "; ".join(detail),
                    path,
                )
            )
        track = template.get("track")
        if not isinstance(track, str) or track not in taxonomy_ids:
            issues.append(
                Issue(
                    "error",
                    "project_template.track",
                    f"unknown canonical track {track!r}",
                    path,
                )
            )
        elif track in seen_tracks:
            issues.append(
                Issue(
                    "error",
                    "project_template.track_duplicate",
                    f"duplicate template for {track}",
                    path,
                )
            )
        else:
            seen_tracks.add(track)
        for field in LOCALIZED_TEXT_FIELDS:
            issues.extend(
                _localized_text_issues(template.get(field), path=f"{path}/{field}")
            )
        for field, minimum in LOCALIZED_LIST_MINIMUMS.items():
            issues.extend(
                _localized_list_issues(
                    template.get(field),
                    path=f"{path}/{field}",
                    minimum=minimum,
                )
            )
        title = template.get("title")
        brief = template.get("brief")
        if isinstance(title, Mapping) and isinstance(brief, Mapping):
            for language in ("zh", "en"):
                title_text = str(title.get(language, ""))
                brief_text = str(brief.get(language, ""))
                if "course_title" not in _format_names(title_text):
                    issues.append(
                        Issue(
                            "error",
                            "project_template.course_context",
                            f"{language} title must contain {{course_title}}",
                            f"{path}/title",
                        )
                    )
                if not {"course_title", "track_title"} <= _format_names(brief_text):
                    issues.append(
                        Issue(
                            "error",
                            "project_template.track_context",
                            f"{language} brief must contain course and track placeholders",
                            f"{path}/brief",
                        )
                    )
                unknown_fields = (
                    _format_names(title_text) | _format_names(brief_text)
                ) - FORMAT_FIELDS
                if unknown_fields:
                    issues.append(
                        Issue(
                            "error",
                            "project_template.placeholder",
                            f"unknown placeholders: {', '.join(sorted(unknown_fields))}",
                            path,
                        )
                    )
            zh_brief = str(brief.get("zh", ""))
            en_brief = str(brief.get("en", "")).casefold()
            if "维护者" not in zh_brief or "不是课程官方作业" not in zh_brief:
                issues.append(
                    Issue(
                        "error",
                        "project_template.origin_disclosure",
                        "Chinese brief must disclose maintainer suggestion and non-official status",
                        f"{path}/brief",
                    )
                )
            if (
                "maintainer-suggested" not in en_brief
                or "not an official course assignment" not in en_brief
            ):
                issues.append(
                    Issue(
                        "error",
                        "project_template.origin_disclosure",
                        "English brief must disclose maintainer suggestion and non-official status",
                        f"{path}/brief",
                    )
                )
            fingerprint = (zh_brief, str(brief.get("en", "")))
            previous = content_fingerprints.get(fingerprint)
            if previous is not None:
                issues.append(
                    Issue(
                        "error",
                        "project_template.generic_duplicate",
                        f"brief duplicates track {previous}",
                        f"{path}/brief",
                    )
                )
            elif isinstance(track, str):
                content_fingerprints[fingerprint] = track
        safety_level = template.get("safety_level")
        if safety_level not in SAFETY_LEVELS:
            issues.append(
                Issue(
                    "error",
                    "project_template.safety_level",
                    f"unsupported safety level {safety_level!r}",
                    path,
                )
            )
        if track in HIGH_RISK_TRACKS and safety_level not in {
            "simulation-only",
            "supervised",
        }:
            issues.append(
                Issue(
                    "error",
                    "project_template.high_risk",
                    "high-risk track must be simulation-only or supervised",
                    path,
                )
            )
        safety_note = template.get("safety_note")
        if track in LOW_ENERGY_TRACKS and isinstance(safety_note, Mapping):
            zh_note = str(safety_note.get("zh", ""))
            en_note = str(safety_note.get("en", "")).casefold()
            if not all(token in zh_note for token in ("限流", "额定值", "断电")):
                issues.append(
                    Issue(
                        "error",
                        "project_template.low_energy_safety",
                        "Chinese low-energy note must require current limiting, rating checks, and unpowered wiring",
                        f"{path}/safety_note",
                    )
                )
            if not all(
                token in en_note
                for token in ("current-limit", "rating", "power removed")
            ):
                issues.append(
                    Issue(
                        "error",
                        "project_template.low_energy_safety",
                        "English low-energy note must require current limiting, rating checks, and unpowered wiring",
                        f"{path}/safety_note",
                    )
                )
        if track == "biomedical" and isinstance(safety_note, Mapping):
            combined = " ".join(str(value) for value in safety_note.values()).casefold()
            for token in ("公开", "合成", "public", "synthetic", "人体", "human"):
                if token.casefold() not in combined:
                    issues.append(
                        Issue(
                            "error",
                            "project_template.biomedical_safety",
                            f"biomedical safety note must include {token!r}",
                            f"{path}/safety_note",
                        )
                    )
        english_evidence = " ".join(
            str(item)
            for field in ("deliverables", "verification", "reproducibility")
            for item in (
                template.get(field, {}).get("en", [])
                if isinstance(template.get(field), Mapping)
                else []
            )
        ).casefold()
        for token in ("source", "raw", "report"):
            if token not in english_evidence:
                issues.append(
                    Issue(
                        "error",
                        "project_template.evidence",
                        f"English evidence must explicitly include {token!r}",
                        path,
                    )
                )
        if not any(
            token in english_evidence
            for token in ("pin ", "pinned", "version", "environment")
        ):
            issues.append(
                Issue(
                    "error",
                    "project_template.environment",
                    "English evidence must pin or record the execution environment",
                    path,
                )
            )
        verification_en = " ".join(
            str(item)
            for item in (
                template.get("verification", {}).get("en", [])
                if isinstance(template.get("verification"), Mapping)
                else []
            )
        )
        if not re.search(r"\d|%|threshold|tolerance|margin", verification_en):
            issues.append(
                Issue(
                    "error",
                    "project_template.quantification",
                    "verification must contain a measurable threshold or margin",
                    f"{path}/verification",
                )
            )
    missing_tracks = sorted(taxonomy_ids - seen_tracks)
    extra_tracks = sorted(seen_tracks - taxonomy_ids)
    if missing_tracks:
        issues.append(
            Issue(
                "error",
                "project_template.missing_tracks",
                f"missing templates for: {', '.join(missing_tracks)}",
                templates_source,
            )
        )
    if extra_tracks:
        issues.append(
            Issue(
                "error",
                "project_template.extra_tracks",
                f"unknown templates for: {', '.join(extra_tracks)}",
                templates_source,
            )
        )
    if len(templates) != len(taxonomy_ids):
        issues.append(
            Issue(
                "error",
                "project_template.count",
                f"expected exactly {len(taxonomy_ids)} templates, found {len(templates)}",
                templates_source,
            )
        )
    return list(dict.fromkeys(issues))


def _render_text(
    value: Mapping[str, Any],
    *,
    course_title: Mapping[str, str],
    track_title: Mapping[str, str],
) -> dict[str, str]:
    return {
        language: str(value[language]).format(
            course_title=course_title[language],
            track_title=track_title[language],
        )
        for language in ("zh", "en")
    }


def _render_list(
    value: Mapping[str, Any],
    *,
    course_title: Mapping[str, str],
    track_title: Mapping[str, str],
) -> dict[str, list[str]]:
    return {
        language: [
            str(item).format(
                course_title=course_title[language],
                track_title=track_title[language],
            )
            for item in value[language]
        ]
        for language in ("zh", "en")
    }


def build_suggested_project(
    course: Mapping[str, Any],
    template: Mapping[str, Any],
    taxonomy_track: Mapping[str, Any],
) -> dict[str, Any]:
    raw_course_title = course.get("title")
    if not isinstance(raw_course_title, Mapping):
        raise QualityError(f"course {course.get('id')!r} has no localized title")
    course_title = {
        "zh": str(raw_course_title.get("zh", "")).strip(),
        "en": str(raw_course_title.get("en", "")).strip(),
    }
    if not all(course_title.values()):
        raise QualityError(f"course {course.get('id')!r} has an empty title translation")
    institution = str(course.get("institution", "")).strip()
    course_code = str(course.get("course_code", "")).strip()
    qualifier = " ".join(value for value in (institution, course_code) if value)
    course_context = {
        language: (
            f"{course_title[language]} · {qualifier}"
            if qualifier
            else course_title[language]
        )
        for language in ("zh", "en")
    }
    track_title = {
        "zh": str(taxonomy_track.get("title_zh", "")).strip(),
        "en": str(taxonomy_track.get("title_en", "")).strip(),
    }
    if not all(track_title.values()):
        raise QualityError(f"track {taxonomy_track.get('id')!r} has an empty title translation")
    return {
        "title": _render_text(
            template["title"],
            course_title=course_context,
            track_title=track_title,
        ),
        "brief": _render_text(
            template["brief"],
            course_title=course_context,
            track_title=track_title,
        ),
        "origin": "suggested",
        "deliverables": _render_list(
            template["deliverables"],
            course_title=course_context,
            track_title=track_title,
        ),
        "verification": _render_list(
            template["verification"],
            course_title=course_context,
            track_title=track_title,
        ),
        "reproducibility": _render_list(
            template["reproducibility"],
            course_title=course_context,
            track_title=track_title,
        ),
        "safety_level": str(template["safety_level"]),
        "safety_note": _render_text(
            template["safety_note"],
            course_title=course_context,
            track_title=track_title,
        ),
    }


def apply_project_templates(
    catalogue_value: Any,
    templates_value: Any,
    taxonomy_value: Any,
) -> tuple[dict[str, Any] | None, list[Issue]]:
    issues = validate_project_templates(templates_value, taxonomy_value)
    if any(issue.severity == "error" for issue in issues):
        return None, issues
    if not isinstance(catalogue_value, Mapping) or not isinstance(
        catalogue_value.get("courses"), list
    ):
        return None, issues + [
            Issue(
                "error",
                "project_apply.catalogue",
                "catalogue must be an object containing courses[]",
                "data/courses.json",
            )
        ]
    taxonomy_tracks = {
        str(track["id"]): track
        for track in taxonomy_value["tracks"]
        if isinstance(track, Mapping) and track.get("id")
    }
    template_by_track = {
        str(template["track"]): template
        for template in templates_value["templates"]
        if isinstance(template, Mapping)
    }
    result = copy.deepcopy(dict(catalogue_value))
    courses = result["courses"]
    course_ids: set[str] = set()
    for index, course in enumerate(courses):
        path = f"data/courses.json:courses/{index}"
        if not isinstance(course, dict):
            issues.append(
                Issue("error", "project_apply.course", "course must be an object", path)
            )
            continue
        course_id = course.get("id")
        if not isinstance(course_id, str) or not course_id:
            issues.append(
                Issue("error", "project_apply.course_id", "course id is required", path)
            )
            continue
        if course_id in course_ids:
            issues.append(
                Issue(
                    "error",
                    "project_apply.course_duplicate",
                    f"duplicate course id {course_id}",
                    path,
                )
            )
            continue
        course_ids.add(course_id)
        track = course.get("track")
        if track not in template_by_track or track not in taxonomy_tracks:
            issues.append(
                Issue(
                    "error",
                    "project_apply.track",
                    f"no project template for course track {track!r}",
                    path,
                )
            )
            continue
        try:
            project = build_suggested_project(
                course,
                template_by_track[str(track)],
                taxonomy_tracks[str(track)],
            )
        except (KeyError, TypeError, ValueError, QualityError) as exc:
            issues.append(
                Issue("error", "project_apply.render", str(exc), path)
            )
            continue
        course["projects"] = [project]
    if any(issue.severity == "error" for issue in issues):
        return None, issues
    generated_count = sum(
        1
        for course in courses
        if isinstance(course, Mapping)
        and len(course.get("projects", [])) == 1
        and course["projects"][0].get("origin") == "suggested"
    )
    if generated_count != len(courses):
        issues.append(
            Issue(
                "error",
                "project_apply.coverage",
                f"expected one suggested project for every course; generated {generated_count}/{len(courses)}",
                "data/courses.json",
            )
        )
        return None, issues
    return result, issues


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Apply reviewed, track-specific suggested projects to every canonical course."
    )
    parser.add_argument("--catalogue", default="data/courses.json")
    parser.add_argument("--templates", default="data/project_templates.json")
    parser.add_argument("--taxonomy", default="data/tracks.json")
    parser.add_argument(
        "--output",
        default="data/courses.json",
        help="Output catalogue; defaults to updating the canonical file atomically.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail when output differs from deterministic project application; do not write.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    catalogue_path = repo_path(args.catalogue)
    templates_path = repo_path(args.templates)
    taxonomy_path = repo_path(args.taxonomy)
    output_path = repo_path(args.output)
    try:
        catalogue_value = load_json(catalogue_path)
        templates_value = load_json(templates_path)
        taxonomy_value = load_json(taxonomy_path)
    except (OSError, QualityError) as exc:
        issues = [Issue("error", "project_apply.input", str(exc))]
        emit_issues(issues)
        return exit_code(issues)
    result, issues = apply_project_templates(
        catalogue_value,
        templates_value,
        taxonomy_value,
    )
    if result is None:
        emit_issues(issues)
        return exit_code(issues)
    expected = stable_json(result)
    if args.check:
        if not output_path.exists():
            issues.append(
                Issue(
                    "error",
                    "project_apply.missing",
                    f"run scripts/apply_project_templates.py to create {args.output}",
                    args.output,
                )
            )
        else:
            current = output_path.read_text(encoding="utf-8")
            if current != expected:
                diff = "".join(
                    difflib.unified_diff(
                        current.splitlines(keepends=True),
                        expected.splitlines(keepends=True),
                        fromfile=args.output,
                        tofile=f"{args.output} (expected)",
                        n=2,
                    )
                )
                preview = "\n".join(diff.splitlines()[:30])
                issues.append(
                    Issue(
                        "error",
                        "project_apply.drift",
                        "suggested projects are stale; run scripts/apply_project_templates.py",
                        args.output,
                        context=preview,
                    )
                )
    else:
        atomic_write(output_path, expected)
        print(
            f"Wrote {args.output}: {len(result['courses'])}/{len(result['courses'])} "
            "courses with one maintainer-suggested project"
        )
    emit_issues(issues)
    return exit_code(issues)


if __name__ == "__main__":
    raise SystemExit(main())
