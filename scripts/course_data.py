from __future__ import annotations

import copy
import hashlib
import re
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence
from urllib.parse import urlsplit, urlunsplit

from scripts.quality_common import (
    Issue,
    QualityError,
    localized,
    localized_list,
    slugify,
)


SCHEMA_VERSION = "1.0.0"
ROLES = {"mainline", "alternative", "supplement"}
TIERS = {"S", "A", "B"}
LEVELS = {"introductory", "intermediate", "advanced", "unspecified"}
COVERAGE_KEYS = ("video", "notes", "practice", "labs", "exams", "code")
RESOURCE_STATUSES = {
    "available",
    "degraded",
    "archived",
    "unavailable",
    "review-needed",
}
GENERATED_RESOURCE_ID_RE = re.compile(
    r"^(?:course|video|notes|assignments|labs|projects|exams|code|textbook)-[0-9a-f]{10}$"
)
RESOURCE_ACCESS = {
    "open",
    "open-registration",
    "free-audit",
    "limited-free",
    "paid",
    "institutional",
}
RESOURCE_ARTIFACT_SCOPES = {
    "content",
    "index",
    "outline",
    "landing",
    "syllabus",
}
HIGH_VALUE_RESOURCE_KINDS = {
    "course",
    "video",
    "notes",
    "textbook",
    "assignments",
    "labs",
    "projects",
    "exams",
    "code",
    "dataset",
    "simulator",
}

# Candidate IDs intentionally describe the source research vocabulary. Every
# non-identical mapping is explicit so a new or mistyped track fails loudly.
TRACK_ALIASES = {
    "programming": "programming-tools",
    "circuits-laboratory": "electronics-laboratory",
    "analog-ic-design": "analog-ic",
    "fpga": "fpga-soc",
    "system-on-chip": "fpga-soc",
    "real-time-systems": "real-time-cps",
    "cyber-physical-systems": "real-time-cps",
    "signals": "signals-systems",
    "signal-processing": "dsp",
    "communication-systems": "communications",
    "information-theory": "information-theory-coding",
    "coding-theory": "information-theory-coding",
    "control": "control-systems",
    "rf-microwave": "rf-microwave-antennas",
    "antennas": "rf-microwave-antennas",
    "semiconductors": "semiconductor-devices",
    "analog-ic-design": "analog-ic",
    "vlsi": "vlsi-ic",
    "microfabrication": "fabrication-mems",
    "mems": "fabrication-mems",
    "photonics": "optics-photonics",
    "power-systems": "power-systems-machines",
    "electrical-machines": "power-systems-machines",
    "renewable-energy": "energy-storage-pv",
    "pcb-design": "pcb-eda",
    "instrumentation": "sensors-instrumentation",
    "sensors": "sensors-instrumentation",
    "biomedical-engineering": "biomedical",
    "capstone": "capstone-practice",
}

ROLE_TEXT = {
    "mainline": ("主线", "Mainline"),
    "alternative": ("替代", "Alternative"),
    "supplement": ("补充", "Supplement"),
}

TIER_TEXT = {
    "S": (
        "资源完整、教学设计清晰，适合作为该方向的优先选择。",
        "A particularly complete and well-structured option for this track.",
    ),
    "A": (
        "核心内容可靠，适合按自身背景作为主课或高质量替代。",
        "A reliable option that can serve as a main course or strong alternative.",
    ),
    "B": (
        "在特定主题上有明确价值，建议与更完整的主线资源配合。",
        "Useful for specific topics and best paired with a more complete mainline resource.",
    ),
}


def _policy_for_url(url: str) -> dict[str, str]:
    host = urlsplit(url).hostname or ""
    host = host.lower().removeprefix("www.")
    path = urlsplit(url).path.lower()
    if host == "ocw.mit.edu":
        return {
            "access": "open",
            "license": "CC BY-NC-SA 4.0 for site materials; third-party exclusions may apply",
        }
    if host.endswith("nptel.ac.in"):
        return {"access": "open", "license": "NPTEL provider terms"}
    if host.endswith("coursera.org"):
        return {"access": "limited-free", "license": "Coursera Terms of Use"}
    if host.endswith("edx.org"):
        return {"access": "limited-free", "license": "edX Terms of Service"}
    if host.endswith("youtube.com") or host == "youtu.be":
        return {
            "access": "open",
            "license": "Creator copyright under YouTube Terms of Service",
        }
    if host.endswith("github.com") or host.endswith("gitlab.com"):
        return {
            "access": "open",
            "license": "Repository-specific license; inspect before reuse",
        }
    if "archive" in host or "/archive" in path:
        return {
            "access": "open",
            "license": "Original provider terms; archive host terms also apply",
        }
    return {
        "access": "open",
        "license": "Provider-specific terms; verify before reuse",
    }


def normalize_url(url: str) -> str:
    parsed = urlsplit(url.strip())
    scheme = parsed.scheme.lower()
    host = (parsed.hostname or "").lower()
    if host == "www.ocw.mit.edu":
        host = "ocw.mit.edu"
    if parsed.port and not (
        (scheme == "https" and parsed.port == 443) or (scheme == "http" and parsed.port == 80)
    ):
        host = f"{host}:{parsed.port}"
    archive_target = (
        re.match(r"^(?P<prefix>/web/[^/]+/)(?P<target>https?://.+)$", parsed.path)
        if host == "web.archive.org"
        else None
    )
    if archive_target:
        # A Wayback path embeds the original absolute URL. Collapsing repeated
        # slashes across the whole path would turn ``https://`` into
        # ``https:/`` and silently corrupt the snapshot target.
        path = (
            re.sub(r"/{2,}", "/", archive_target.group("prefix"))
            + archive_target.group("target")
        )
    else:
        path = re.sub(r"/{2,}", "/", parsed.path) or "/"
    if path != "/":
        path = path.rstrip("/")
    return urlunsplit((scheme, host, path, parsed.query, ""))


def normalize_track_id(candidate_track: str, taxonomy_ids: set[str]) -> str:
    normalized = TRACK_ALIASES.get(candidate_track, candidate_track)
    if normalized not in taxonomy_ids:
        raise QualityError(
            f"candidate track {candidate_track!r} is not present in the canonical taxonomy"
        )
    return normalized


def load_taxonomy(value: Any) -> tuple[list[dict[str, Any]], list[Issue]]:
    issues: list[Issue] = []
    if not isinstance(value, dict):
        return [], [Issue("error", "taxonomy.type", "track taxonomy must be an object")]
    groups = value.get("groups")
    tracks = value.get("tracks")
    if not isinstance(groups, list) or not isinstance(tracks, list):
        return [], [
            Issue("error", "taxonomy.shape", "track taxonomy requires groups[] and tracks[]")
        ]
    group_ids: set[str] = set()
    for index, group in enumerate(groups):
        path = f"data/tracks.json:groups[{index}]"
        if not isinstance(group, dict):
            issues.append(Issue("error", "taxonomy.group.type", "group must be an object", path))
            continue
        group_id = group.get("id")
        if not isinstance(group_id, str) or not group_id:
            issues.append(Issue("error", "taxonomy.group.id", "group id is required", path))
        elif group_id in group_ids:
            issues.append(Issue("error", "taxonomy.group.duplicate", group_id, path))
        else:
            group_ids.add(group_id)
        for key in ("title_zh", "title_en"):
            if not isinstance(group.get(key), str) or not group[key].strip():
                issues.append(Issue("error", "taxonomy.group.translation", f"{key} is required", path))

    track_ids: set[str] = set()
    orders: set[int] = set()
    for index, track in enumerate(tracks):
        path = f"data/tracks.json:tracks[{index}]"
        if not isinstance(track, dict):
            issues.append(Issue("error", "taxonomy.track.type", "track must be an object", path))
            continue
        track_id = track.get("id")
        if not isinstance(track_id, str) or not track_id:
            issues.append(Issue("error", "taxonomy.track.id", "track id is required", path))
        elif track_id in track_ids:
            issues.append(Issue("error", "taxonomy.track.duplicate", track_id, path))
        else:
            track_ids.add(track_id)
        if track.get("group") not in group_ids:
            issues.append(
                Issue(
                    "error",
                    "taxonomy.track.group",
                    f"unknown group {track.get('group')!r}",
                    path,
                )
            )
        order = track.get("order")
        if not isinstance(order, int) or order < 1:
            issues.append(Issue("error", "taxonomy.track.order", "positive order required", path))
        elif order in orders:
            issues.append(Issue("error", "taxonomy.track.order_duplicate", str(order), path))
        else:
            orders.add(order)
        for key in ("title_zh", "title_en", "summary_zh", "summary_en"):
            if not isinstance(track.get(key), str) or not track[key].strip():
                issues.append(Issue("error", "taxonomy.track.translation", f"{key} is required", path))
        if not isinstance(track.get("prerequisites"), list):
            issues.append(
                Issue("error", "taxonomy.track.prerequisites", "prerequisites must be a list", path)
            )
    for index, track in enumerate(tracks):
        for prerequisite in track.get("prerequisites", []):
            if prerequisite not in track_ids:
                issues.append(
                    Issue(
                        "error",
                        "taxonomy.track.prerequisite",
                        f"unknown prerequisite {prerequisite!r}",
                        f"data/tracks.json:tracks[{index}]",
                    )
                )
    issues.extend(_track_cycle_issues(tracks, "taxonomy.track.cycle"))
    return tracks, issues


def validate_candidates(
    value: Any,
    *,
    taxonomy_ids: set[str] | None = None,
) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(value, list):
        return [Issue("error", "candidate.type", "candidate catalogue must be a JSON array")]
    ids: set[int] = set()
    urls: dict[str, int] = {}
    required = {
        "id",
        "title",
        "institution",
        "code",
        "url",
        "track",
        "role",
        "tier",
        "tier_note",
        "resources",
        "risk",
        "verified_at",
    }
    for index, candidate in enumerate(value):
        path = f"data/course_candidates.json:[{index}]"
        if not isinstance(candidate, dict):
            issues.append(Issue("error", "candidate.item_type", "candidate must be an object", path))
            continue
        missing = sorted(required - candidate.keys())
        if missing:
            issues.append(
                Issue("error", "candidate.required", f"missing: {', '.join(missing)}", path)
            )
            continue
        candidate_id = candidate.get("id")
        if not isinstance(candidate_id, int) or candidate_id < 1:
            issues.append(Issue("error", "candidate.id", "id must be a positive integer", path))
        elif candidate_id in ids:
            issues.append(Issue("error", "candidate.id_duplicate", str(candidate_id), path))
        else:
            ids.add(candidate_id)
        for key in ("title", "institution", "track", "tier_note", "risk", "verified_at"):
            if not isinstance(candidate.get(key), str) or not candidate[key].strip():
                issues.append(Issue("error", "candidate.text", f"{key} must be non-empty", path))
        if candidate.get("role") not in ROLES:
            issues.append(Issue("error", "candidate.role", str(candidate.get("role")), path))
        if candidate.get("tier") not in TIERS:
            issues.append(Issue("error", "candidate.tier", str(candidate.get("tier")), path))
        if candidate.get("level", "unspecified") not in LEVELS:
            issues.append(
                Issue("error", "candidate.level", str(candidate.get("level")), path)
            )
        inherit_track_prerequisites = candidate.get(
            "inherit_track_prerequisites", True
        )
        if not isinstance(inherit_track_prerequisites, bool):
            issues.append(
                Issue(
                    "error",
                    "candidate.inherit_track_prerequisites",
                    "inherit_track_prerequisites must be a boolean",
                    path,
                )
            )
        recommended_background = candidate.get("recommended_background")
        if recommended_background is not None and (
            not isinstance(recommended_background, Mapping)
            or set(recommended_background) != {"zh", "en"}
            or any(
                not isinstance(recommended_background.get(language), str)
                or not recommended_background[language].strip()
                for language in ("zh", "en")
            )
        ):
            issues.append(
                Issue(
                    "error",
                    "candidate.recommended_background",
                    "recommended_background must contain non-empty zh and en text",
                    path,
                )
            )
        prerequisite_note = candidate.get("prerequisite_note")
        if prerequisite_note is not None and (
            not isinstance(prerequisite_note, Mapping)
            or set(prerequisite_note) != {"zh", "en"}
            or any(
                not isinstance(prerequisite_note.get(language), str)
                or not prerequisite_note[language].strip()
                for language in ("zh", "en")
            )
        ):
            issues.append(
                Issue(
                    "error",
                    "candidate.prerequisite_note",
                    "prerequisite_note must contain non-empty zh and en text",
                    path,
                )
            )
        workload = candidate.get("workload")
        if workload is not None:
            if not isinstance(workload, dict) or not workload:
                issues.append(
                    Issue(
                        "error",
                        "candidate.workload",
                        "workload must be a non-empty object",
                        path,
                    )
                )
            elif set(workload) - {"weeks", "hours_per_week"}:
                issues.append(
                    Issue(
                        "error",
                        "candidate.workload",
                        "workload supports only weeks and hours_per_week",
                        path,
                    )
                )
            else:
                weeks = workload.get("weeks")
                if weeks is not None and (
                    not isinstance(weeks, int)
                    or isinstance(weeks, bool)
                    or not 1 <= weeks <= 104
                ):
                    issues.append(
                        Issue(
                            "error",
                            "candidate.workload.weeks",
                            "weeks must be an integer from 1 to 104",
                            path,
                        )
                    )
                hours = workload.get("hours_per_week")
                if hours is not None:
                    if not isinstance(hours, dict) or set(hours) != {"min", "max"}:
                        issues.append(
                            Issue(
                                "error",
                                "candidate.workload.hours",
                                "hours_per_week must contain min and max",
                                path,
                            )
                        )
                    else:
                        minimum = hours.get("min")
                        maximum = hours.get("max")
                        if (
                            not isinstance(minimum, (int, float))
                            or isinstance(minimum, bool)
                            or not isinstance(maximum, (int, float))
                            or isinstance(maximum, bool)
                            or minimum <= 0
                            or maximum < minimum
                            or maximum > 80
                        ):
                            issues.append(
                                Issue(
                                    "error",
                                    "candidate.workload.hours",
                                    "hours range must satisfy 0 < min <= max <= 80",
                                    path,
                                )
                            )
        primary = candidate.get("url")
        alternatives = candidate.get("alternate_urls", [])
        if not isinstance(alternatives, list):
            issues.append(
                Issue("error", "candidate.alternate_urls", "alternate_urls must be a list", path)
            )
            alternatives = []
        for url in [primary, *alternatives]:
            if not isinstance(url, str) or not url.startswith("https://"):
                issues.append(
                    Issue("error", "candidate.url", f"HTTPS URL required, found {url!r}", path)
                )
                continue
            normalized = normalize_url(url)
            if normalized in urls and urls[normalized] != candidate_id:
                issues.append(
                    Issue(
                        "warning",
                        "candidate.url_duplicate",
                        f"also used by candidate {urls[normalized]}: {normalized}",
                        path,
                    )
                )
            else:
                urls[normalized] = candidate_id
        coverage = candidate.get("resources")
        if not isinstance(coverage, dict) or set(coverage) != set(COVERAGE_KEYS):
            issues.append(
                Issue(
                    "error",
                    "candidate.coverage_shape",
                    f"resources must contain exactly {', '.join(COVERAGE_KEYS)}",
                    path,
                )
            )
        else:
            for key, score in coverage.items():
                if not isinstance(score, int) or isinstance(score, bool) or not 0 <= score <= 2:
                    issues.append(
                        Issue(
                            "error",
                            "candidate.coverage_score",
                            f"{key} must be an integer from 0 to 2",
                            path,
                        )
                    )
        try:
            date.fromisoformat(str(candidate.get("verified_at")))
        except ValueError:
            issues.append(
                Issue("error", "candidate.verified_at", "verified_at must be YYYY-MM-DD", path)
            )
        raw_track = candidate.get("track")
        if isinstance(raw_track, str) and taxonomy_ids is not None:
            try:
                normalize_track_id(raw_track, taxonomy_ids)
            except QualityError as exc:
                issues.append(Issue("error", "candidate.track", str(exc), path))
    for index, candidate in enumerate(value):
        if not isinstance(candidate, dict):
            continue
        path = f"data/course_candidates.json:[{index}]"
        candidate_id = candidate.get("id")
        prerequisite_ids = candidate.get("prerequisite_course_ids", [])
        if not isinstance(prerequisite_ids, list):
            issues.append(
                Issue(
                    "error",
                    "candidate.prerequisite_course_ids",
                    "prerequisite_course_ids must be a list",
                    path,
                )
            )
            continue
        if any(
            prerequisite_id in prerequisite_ids[:prerequisite_index]
            for prerequisite_index, prerequisite_id in enumerate(prerequisite_ids)
        ):
            issues.append(
                Issue(
                    "error",
                    "candidate.prerequisite_course_ids_duplicate",
                    "prerequisite_course_ids must be unique",
                    path,
                )
            )
        for prerequisite_id in prerequisite_ids:
            if (
                not isinstance(prerequisite_id, int)
                or isinstance(prerequisite_id, bool)
                or prerequisite_id < 1
            ):
                issues.append(
                    Issue(
                        "error",
                        "candidate.prerequisite_course_id",
                        f"positive integer required, found {prerequisite_id!r}",
                        path,
                    )
                )
            elif prerequisite_id == candidate_id:
                issues.append(
                    Issue(
                        "error",
                        "candidate.prerequisite_course_self",
                        "a course cannot require itself",
                        path,
                    )
                )
            elif prerequisite_id not in ids:
                issues.append(
                    Issue(
                        "error",
                        "candidate.prerequisite_course_missing",
                        f"unknown prerequisite course id {prerequisite_id}",
                        path,
                    )
                )
    issues.extend(_candidate_prerequisite_cycle_issues(value))
    return issues


def _canonical_track(track: Mapping[str, Any]) -> dict[str, Any]:
    title_zh = str(track["title_zh"])
    title_en = str(track["title_en"])
    return {
        "id": track["id"],
        "group": track["group"],
        "order": track["order"],
        "title": localized(title_zh, title_en),
        "summary": localized(str(track["summary_zh"]), str(track["summary_en"])),
        "outcomes": localized_list(
            [
                f"掌握{title_zh}的核心概念、模型与分析方法",
                "完成可复现、可检验的练习、实验或设计成果",
            ],
            [
                f"Explain the core concepts, models, and methods of {title_en}",
                "Produce reproducible exercises, experiments, or designs with explicit checks",
            ],
        ),
        "prerequisite_tracks": list(track.get("prerequisites", [])),
    }


def _course_summary(
    candidate: Mapping[str, Any], track: Mapping[str, Any]
) -> dict[str, str]:
    institution = str(candidate["institution"])
    title = str(candidate["title"])
    track_zh = str(track["title_zh"])
    track_en = str(track["title_en"])
    return localized(
        f"{institution} 提供的《{title}》，纳入{track_zh}路线；页面按资源完整度、实践条件和复核风险给出选课建议。",
        f"{title} from {institution}, placed in the {track_en} pathway with explicit resource coverage, practice constraints, and review notes.",
    )


def _course_prerequisite_sections(
    candidate: Mapping[str, Any],
    track: Mapping[str, Any],
    track_by_id: Mapping[str, Any],
    candidate_by_id: Mapping[int, Mapping[str, Any]],
) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    track_prerequisites = (
        [
            track_by_id[track_id]
            for track_id in track.get("prerequisites", [])
            if track_id in track_by_id
        ]
        if candidate.get("inherit_track_prerequisites", True)
        else []
    )
    course_prerequisites = [
        candidate_by_id[course_id]
        for course_id in candidate.get("prerequisite_course_ids", [])
        if course_id in candidate_by_id
    ]
    recommended_background = candidate.get("recommended_background")
    recommended_zh = (
        [str(recommended_background["zh"])]
        if isinstance(recommended_background, Mapping)
        else []
    )
    recommended_en = (
        [str(recommended_background["en"])]
        if isinstance(recommended_background, Mapping)
        else []
    )
    prerequisite_note = candidate.get("prerequisite_note")
    prerequisite_note_zh = (
        [str(prerequisite_note["zh"])]
        if isinstance(prerequisite_note, Mapping)
        else []
    )
    prerequisite_note_en = (
        [str(prerequisite_note["en"])]
        if isinstance(prerequisite_note, Mapping)
        else []
    )
    recommended = localized_list(
        [
            *[str(item["title_zh"]) for item in track_prerequisites],
            *recommended_zh,
        ],
        [
            *[str(item["title_en"]) for item in track_prerequisites],
            *recommended_en,
        ],
    )
    official = localized_list(
        [
            *prerequisite_note_zh,
            *[
                f"先完成《{item['title']}》（{item['institution']} {item['code']}）"
                for item in course_prerequisites
            ],
        ],
        [
            *prerequisite_note_en,
            *[
                f"Complete {item['title']} "
                f"({item['institution']} {item['code']}) first"
                for item in course_prerequisites
            ],
        ],
    )
    return official, recommended


def _course_prerequisites(
    candidate: Mapping[str, Any],
    track: Mapping[str, Any],
    track_by_id: Mapping[str, Any],
    candidate_by_id: Mapping[int, Mapping[str, Any]],
) -> dict[str, list[str]]:
    official, recommended = _course_prerequisite_sections(
        candidate,
        track,
        track_by_id,
        candidate_by_id,
    )
    return localized_list(
        [*recommended["zh"], *official["zh"]],
        [*recommended["en"], *official["en"]],
    )


def _resource_from_url(
    url: str, *, resource_id: str, verified_at: str, alternate: bool
) -> dict[str, Any]:
    policy = _policy_for_url(url)
    archived = "archive" in (urlsplit(url).hostname or "").lower() or "/archive" in urlsplit(
        url
    ).path.lower()
    title = (
        localized("备用课程入口", "Alternate course entry")
        if alternate
        else localized("课程主页", "Course home")
    )
    return {
        "id": resource_id,
        "kind": "course",
        "title": title,
        "url": normalize_url(url),
        "access": policy["access"],
        "license": policy["license"],
        "status": "archived" if archived else "available",
        "last_verified": verified_at,
        "note": localized(
            "访问条件与许可按提供方当前页面记录；转载或改编前应再次核对。",
            "Access and licensing follow the provider page; re-check before redistribution or adaptation.",
        ),
    }


def resource_from_manifest(record: Mapping[str, Any]) -> dict[str, Any]:
    url = normalize_url(str(record["url"]))
    kind = str(record["kind"])
    raw_title = record.get("title")
    if isinstance(raw_title, Mapping):
        title = localized(str(raw_title.get("zh", "")), str(raw_title.get("en", "")))
    else:
        title_text = str(raw_title).strip()
        title = localized(title_text, title_text)
    policy = _policy_for_url(url)
    identifier = f"{slugify(kind)}-{hashlib.sha256(url.encode('utf-8')).hexdigest()[:10]}"
    resource = {
        "id": identifier,
        "kind": kind,
        "title": title,
        "url": url,
        "access": str(record["access"]),
        "license": str(record.get("license") or policy["license"]),
        "status": str(record["status"]),
        "last_verified": str(record["last_verified"]),
        "note": localized(
            "资源由独立证据清单核对；许可按提供方或仓库记录，权利不明确时不得转载。",
            "Checked through the evidence manifest; licensing follows the provider or repository, and unclear rights prohibit redistribution.",
        ),
    }
    if record.get("artifact_scope") is not None:
        resource["artifact_scope"] = str(record["artifact_scope"])
    return resource


def validate_resource_manifest(
    value: Any,
    *,
    candidate_ids: set[int],
    source: str = "data/course_resources.json",
) -> tuple[list[Mapping[str, Any]], list[Issue]]:
    if isinstance(value, Mapping):
        records = value.get("resources")
    else:
        records = value
    if not isinstance(records, list):
        return [], [
            Issue("error", "resource_manifest.shape", "manifest must be an array or contain resources[]", source)
        ]
    issues: list[Issue] = []
    valid: list[Mapping[str, Any]] = []
    required = {"course_id", "kind", "title", "url", "access", "status", "last_verified"}
    seen: set[tuple[int, str]] = set()
    for index, record in enumerate(records):
        path = f"{source}:[{index}]"
        if not isinstance(record, Mapping):
            issues.append(Issue("error", "resource_manifest.item", "record must be an object", path))
            continue
        missing = required - record.keys()
        if missing:
            issues.append(
                Issue(
                    "error",
                    "resource_manifest.required",
                    f"missing: {', '.join(sorted(missing))}",
                    path,
                )
            )
            continue
        course_id = record.get("course_id")
        if course_id not in candidate_ids:
            issues.append(
                Issue(
                    "error",
                    "resource_manifest.course",
                    f"unknown course_id {course_id!r}",
                    path,
                )
            )
        if record.get("kind") not in HIGH_VALUE_RESOURCE_KINDS | {"community", "other"}:
            issues.append(
                Issue(
                    "error",
                    "resource_manifest.kind",
                    f"unsupported kind {record.get('kind')!r}",
                    path,
                )
            )
        if record.get("access") not in RESOURCE_ACCESS:
            issues.append(
                Issue(
                    "error",
                    "resource_manifest.access",
                    f"unsupported access {record.get('access')!r}",
                    path,
                )
            )
        if record.get("status") not in RESOURCE_STATUSES:
            issues.append(
                Issue(
                    "error",
                    "resource_manifest.status",
                    f"unsupported status {record.get('status')!r}",
                    path,
                )
            )
        artifact_scope = record.get("artifact_scope")
        if (
            artifact_scope is not None
            and artifact_scope not in RESOURCE_ARTIFACT_SCOPES
        ):
            issues.append(
                Issue(
                    "error",
                    "resource_manifest.artifact_scope",
                    f"unsupported artifact_scope {artifact_scope!r}",
                    path,
                )
            )
        url = record.get("url")
        if not isinstance(url, str) or not url.startswith("https://"):
            issues.append(Issue("error", "resource_manifest.url", "HTTPS URL required", path))
        elif isinstance(course_id, int):
            key = (course_id, normalize_url(url))
            if key in seen:
                issues.append(
                    Issue("error", "resource_manifest.duplicate", f"duplicate URL {url}", path)
                )
            seen.add(key)
        if parse_iso_date(record.get("last_verified")) is None:
            issues.append(
                Issue("error", "resource_manifest.date", "last_verified must be YYYY-MM-DD", path)
            )
        if not any(issue.path == path and issue.severity == "error" for issue in issues):
            valid.append(record)
    return valid, issues


def _canonical_course(
    candidate: Mapping[str, Any],
    *,
    canonical_track: str,
    taxonomy_track: Mapping[str, Any],
    taxonomy_by_id: Mapping[str, Any],
    candidate_by_id: Mapping[int, Mapping[str, Any]],
) -> dict[str, Any]:
    source_id = int(candidate["id"])
    course_slug = slugify(
        str(candidate.get("code") or candidate["title"]), fallback=f"course-{source_id:03d}"
    )
    resources = [
        _resource_from_url(
            str(candidate["url"]),
            resource_id="primary",
            verified_at=str(candidate["verified_at"]),
            alternate=False,
        )
    ]
    for index, url in enumerate(candidate.get("alternate_urls", []), start=1):
        resources.append(
            _resource_from_url(
                str(url),
                resource_id=f"alternate-{index}",
                verified_at=str(candidate["verified_at"]),
                alternate=True,
            )
        )
    tier_zh, tier_en = TIER_TEXT[str(candidate["tier"])]
    role_zh, role_en = ROLE_TEXT[str(candidate["role"])]
    tier_note = str(candidate["tier_note"]).strip()
    selection_suffix = "" if tier_note == candidate["tier"] else f"（审阅记录：{tier_note}）"
    selection_suffix_en = "" if tier_note == candidate["tier"] else f" Review note: {tier_note}"
    risk = str(candidate["risk"]).strip()
    official_prerequisites, recommended_background = _course_prerequisite_sections(
        candidate,
        taxonomy_track,
        taxonomy_by_id,
        candidate_by_id,
    )
    return {
        "id": f"course-{source_id:03d}",
        "source_id": source_id,
        "slug": f"{source_id:03d}-{course_slug}",
        "track": canonical_track,
        "title": localized(str(candidate["title"]), str(candidate["title"])),
        "summary": _course_summary(candidate, taxonomy_track),
        "institution": str(candidate["institution"]).strip(),
        "course_code": str(candidate.get("code", "")).strip(),
        "role": candidate["role"],
        "tier": candidate["tier"],
        "level": str(candidate.get("level", "unspecified")),
        "languages": ["en"],
        "prerequisite_course_ids": list(candidate.get("prerequisite_course_ids", [])),
        "prerequisites": localized_list(
            [
                *recommended_background["zh"],
                *official_prerequisites["zh"],
            ],
            [
                *recommended_background["en"],
                *official_prerequisites["en"],
            ],
        ),
        "official_prerequisites": official_prerequisites,
        "recommended_background": recommended_background,
        "selection_note": localized(
            f"{role_zh}课程，{tier_zh}{selection_suffix}",
            f"{role_en} course. {tier_en}{selection_suffix_en}",
        ),
        "review_note": localized(f"复核注意：{risk}", risk),
        "resource_coverage": {key: int(candidate["resources"][key]) for key in COVERAGE_KEYS},
        "resources": resources,
        "last_reviewed": str(candidate["verified_at"]),
    }


def _deep_overlay(base: Any, overlay: Any) -> Any:
    if isinstance(base, dict) and isinstance(overlay, dict):
        merged = copy.deepcopy(base)
        for key, value in overlay.items():
            if key in merged:
                merged[key] = _deep_overlay(merged[key], value)
        return merged
    return copy.deepcopy(overlay)


def _merge_resources(
    generated: Sequence[Mapping[str, Any]],
    existing: Sequence[Mapping[str, Any]],
    *,
    authoritative_urls: set[str] | None = None,
) -> list[dict[str, Any]]:
    authoritative_urls = authoritative_urls or set()
    status_priority = {
        "available": 0,
        "archived": 1,
        "degraded": 2,
        "review-needed": 3,
        "unavailable": 4,
    }
    by_url = {
        normalize_url(str(resource.get("url", ""))): resource
        for resource in existing
        if isinstance(resource, Mapping) and resource.get("url")
    }
    generated_urls: set[str] = set()
    output: list[dict[str, Any]] = []
    for resource in generated:
        key = normalize_url(str(resource["url"]))
        generated_urls.add(key)
        if key in by_url:
            existing_resource = by_url[key]
            merged = _deep_overlay(resource, existing_resource)
            if key in authoritative_urls:
                # Fresh manifest evidence is authoritative for metadata. A
                # conservative human status may remain only when it is worse
                # than the new observation; an old "available" must never mask
                # a newly observed review-needed/degraded/unavailable state.
                existing_status = str(existing_resource.get("status", ""))
                generated_status = str(resource.get("status", ""))
                for field, value in resource.items():
                    merged[field] = copy.deepcopy(value)
                if status_priority.get(existing_status, -1) > status_priority.get(
                    generated_status, -1
                ):
                    merged["status"] = existing_status
            output.append(merged)
        else:
            output.append(copy.deepcopy(dict(resource)))
    for resource in existing:
        if not isinstance(resource, Mapping) or not resource.get("url"):
            continue
        key = normalize_url(str(resource["url"]))
        resource_id = str(resource.get("id", ""))
        if (
            key not in generated_urls
            and resource_id != "primary"
            and not resource_id.startswith("alternate-")
            and not GENERATED_RESOURCE_ID_RE.fullmatch(resource_id)
        ):
            output.append(copy.deepcopy(dict(resource)))
    return output


def compile_catalogue(
    candidates: Sequence[Mapping[str, Any]],
    taxonomy_tracks: Sequence[Mapping[str, Any]],
    existing: Mapping[str, Any] | None = None,
    resource_records: Sequence[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    taxonomy_by_id = {str(track["id"]): track for track in taxonomy_tracks}
    taxonomy_ids = set(taxonomy_by_id)
    existing = existing or {}
    existing_tracks = {
        track.get("id"): track
        for track in existing.get("tracks", [])
        if isinstance(track, Mapping) and track.get("id")
    }
    tracks: list[dict[str, Any]] = []
    for taxonomy_track in sorted(taxonomy_tracks, key=lambda item: (item["order"], item["id"])):
        generated = _canonical_track(taxonomy_track)
        merged = _deep_overlay(generated, existing_tracks.get(generated["id"], {}))
        # Taxonomy semantics are authoritative.
        for key in ("id", "group", "order", "prerequisite_tracks"):
            merged[key] = copy.deepcopy(generated[key])
        tracks.append(merged)

    existing_courses = {
        course.get("source_id"): course
        for course in existing.get("courses", [])
        if isinstance(course, Mapping) and isinstance(course.get("source_id"), int)
    }
    resources_by_course: dict[int, list[Mapping[str, Any]]] = defaultdict(list)
    for record in resource_records:
        if isinstance(record.get("course_id"), int):
            resources_by_course[int(record["course_id"])].append(record)
    candidate_by_id = {
        int(candidate["id"]): candidate
        for candidate in candidates
        if isinstance(candidate, Mapping) and isinstance(candidate.get("id"), int)
    }
    courses: list[dict[str, Any]] = []
    for candidate in sorted(candidates, key=lambda item: int(item["id"])):
        canonical_track = normalize_track_id(str(candidate["track"]), taxonomy_ids)
        generated = _canonical_course(
            candidate,
            canonical_track=canonical_track,
            taxonomy_track=taxonomy_by_id[canonical_track],
            taxonomy_by_id=taxonomy_by_id,
            candidate_by_id=candidate_by_id,
        )
        candidate_resource_records = sorted(
            resources_by_course.get(int(candidate["id"]), []),
            key=lambda item: (
                str(item.get("kind")),
                normalize_url(str(item.get("url", ""))),
            ),
        )
        manifest_by_url = {
            normalize_url(str(record["url"])): record
            for record in candidate_resource_records
        }
        authoritative_urls: set[str] = set()
        for index, generated_resource in enumerate(generated["resources"]):
            key = normalize_url(str(generated_resource["url"]))
            record = manifest_by_url.get(key)
            if record is None:
                continue
            manifested = resource_from_manifest(record)
            # Candidate identity remains authoritative for primary/alternate
            # entries. The evidence manifest refreshes only current access and
            # verification metadata; it must not rename a corrected candidate
            # from an older crawl title.
            refreshed = copy.deepcopy(generated_resource)
            for field in (
                "access",
                "license",
                "status",
                "last_verified",
                "note",
                "artifact_scope",
            ):
                if field in manifested:
                    refreshed[field] = copy.deepcopy(manifested[field])
            generated["resources"][index] = refreshed
            authoritative_urls.add(key)
        known_urls = {normalize_url(resource["url"]) for resource in generated["resources"]}
        enriched = []
        for record in candidate_resource_records:
            resource = resource_from_manifest(record)
            if resource["url"] not in known_urls:
                source_url = normalize_url(str(record.get("source_url", "")))
                if resource["status"] == "unavailable":
                    # Keep confirmed failures in the evidence manifest, but do
                    # not turn a known-dead supplemental URL into learner-facing
                    # navigation.
                    continue
                if (
                    resource["kind"] == "course"
                    and resource["status"] in {"review-needed", "archived"}
                    and source_url == resource["url"]
                ):
                    # A failed or archived seed that is no longer a candidate
                    # primary or alternate is superseded evidence, not a useful
                    # public learning link. Keep it in the crawl manifest for
                    # audit, but do not expose it in the learner-facing
                    # catalogue. A deliberately retained archive can still be
                    # added as an override whose source_url names the current
                    # official evidence page.
                    continue
                enriched.append(resource)
                known_urls.add(resource["url"])
                authoritative_urls.add(resource["url"])
        generated["resources"].extend(enriched)
        existing_course = existing_courses.get(int(candidate["id"]), {})
        merged = _deep_overlay(generated, existing_course)
        # Research evidence is authoritative; human enrichment remains everywhere else.
        for key in (
            "id",
            "source_id",
            "slug",
            "track",
            "title",
            "institution",
            "course_code",
            "role",
            "tier",
            "level",
            "prerequisite_course_ids",
            "prerequisites",
            "official_prerequisites",
            "recommended_background",
            "selection_note",
            "resource_coverage",
            "last_reviewed",
        ):
            merged[key] = copy.deepcopy(generated[key])
        merged["resources"] = _merge_resources(
            generated["resources"],
            existing_course.get("resources", []),
            authoritative_urls=authoritative_urls,
        )
        courses.append(merged)
    updated_dates = [str(candidate["verified_at"]) for candidate in candidates]
    updated_at = max(updated_dates) if updated_dates else date.today().isoformat()
    return {
        "schema_version": SCHEMA_VERSION,
        "updated_at": updated_at,
        "tracks": tracks,
        "courses": courses,
    }


def _track_cycle_issues(
    tracks: Sequence[Mapping[str, Any]], code: str = "track.cycle"
) -> list[Issue]:
    graph = {
        str(track.get("id")): list(
            track.get("prerequisite_tracks", track.get("prerequisites", []))
        )
        for track in tracks
        if track.get("id")
    }
    visiting: set[str] = set()
    visited: set[str] = set()
    stack: list[str] = []
    issues: list[Issue] = []

    def visit(node: str) -> None:
        if node in visited:
            return
        if node in visiting:
            start = stack.index(node)
            cycle = stack[start:] + [node]
            issues.append(Issue("error", code, " -> ".join(cycle)))
            return
        visiting.add(node)
        stack.append(node)
        for dependency in graph.get(node, []):
            if dependency in graph:
                visit(dependency)
        stack.pop()
        visiting.remove(node)
        visited.add(node)

    for track_id in graph:
        visit(track_id)
    return issues


def _candidate_prerequisite_cycle_issues(
    candidates: Sequence[Mapping[str, Any]],
) -> list[Issue]:
    graph = {
        int(candidate["id"]): [
            prerequisite
            for prerequisite in candidate.get("prerequisite_course_ids", [])
            if isinstance(prerequisite, int) and not isinstance(prerequisite, bool)
        ]
        for candidate in candidates
        if isinstance(candidate, Mapping)
        and isinstance(candidate.get("id"), int)
        and not isinstance(candidate.get("id"), bool)
    }
    visiting: set[int] = set()
    visited: set[int] = set()
    stack: list[int] = []
    issues: list[Issue] = []

    def visit(node: int) -> None:
        if node in visited:
            return
        if node in visiting:
            start = stack.index(node)
            cycle = stack[start:] + [node]
            issues.append(
                Issue(
                    "error",
                    "candidate.prerequisite_course_cycle",
                    " -> ".join(str(course_id) for course_id in cycle),
                    "data/course_candidates.json",
                )
            )
            return
        visiting.add(node)
        stack.append(node)
        for dependency in graph.get(node, []):
            if dependency in graph:
                visit(dependency)
        stack.pop()
        visiting.remove(node)
        visited.add(node)

    for course_id in graph:
        visit(course_id)
    return list(dict.fromkeys(issues))


def catalogue_statistics(catalogue: Mapping[str, Any]) -> dict[str, Any]:
    courses = catalogue.get("courses", [])
    tracks = catalogue.get("tracks", [])
    used = Counter(course.get("track") for course in courses)
    resource_total = sum(len(course.get("resources", [])) for course in courses)
    complete_resources = sum(
        1
        for course in courses
        for resource in course.get("resources", [])
        if all(
            resource.get(key)
            for key in ("last_verified", "access", "license", "status")
        )
    )
    return {
        "courses": len(courses),
        "tracks_defined": len(tracks),
        "tracks_used": len(used),
        "courses_by_track": dict(sorted(used.items())),
        "courses_by_tier": dict(sorted(Counter(course.get("tier") for course in courses).items())),
        "courses_by_role": dict(sorted(Counter(course.get("role") for course in courses).items())),
        "resources": resource_total,
        "resources_with_required_metadata": complete_resources,
        "resource_metadata_percent": (
            round(complete_resources * 100 / resource_total, 2) if resource_total else 0.0
        ),
    }


def parse_iso_date(value: Any) -> date | None:
    if not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None
