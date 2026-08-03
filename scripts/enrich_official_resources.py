"""Discover high-value learning resources linked by official course pages.

The crawler is intentionally conservative:

* candidate URLs are treated as seeds, never synthesized;
* only HTTPS resources found in fetched official HTML are retained;
* navigation, account, social, tracking, and presentation assets are excluded;
* requests are rate-limited per host and robots.txt is respected;
* output is de-duplicated and deterministically sorted.

Run from the repository root:

    python scripts/enrich_official_resources.py
    python scripts/enrich_official_resources.py --validate-only
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import time
from typing import Any, Iterable
from urllib.parse import (
    parse_qsl,
    unquote,
    urlencode,
    urljoin,
    urlsplit,
    urlunsplit,
)
from urllib.robotparser import RobotFileParser

import requests


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "course_candidates.json"
DEFAULT_OUTPUT = ROOT / "data" / "course_resources.json"
DEFAULT_CHECKPOINT = ROOT / "data" / ".course_resources.checkpoint.json"
VERIFIED_DATE = "2026-07-28"
SCHEMA_VERSION = "1.0"
PRECISION_FILTER_VERSION = 1
USER_AGENT = (
    "EEDIYResourceVerifier/1.0 "
    "(educational resource indexing; +https://github.com/appleweiping/eediy)"
)

KINDS = (
    "course",
    "video",
    "notes",
    "assignments",
    "labs",
    "projects",
    "exams",
    "code",
    "textbook",
)
ACCESS_VALUES = (
    "open",
    "open-registration",
    "free-audit",
    "limited-free",
    "paid",
    "institutional",
)
STATUS_VALUES = (
    "available",
    "degraded",
    "archived",
    "unavailable",
    "review-needed",
)
KIND_ORDER = {kind: index for index, kind in enumerate(KINDS)}

TRACKING_QUERY_KEYS = {
    "fbclid",
    "gclid",
    "mc_cid",
    "mc_eid",
    "ref",
    "source",
}
TRACKING_QUERY_PREFIXES = ("utm_",)

BLOCKED_EXTENSIONS = {
    ".7z",
    ".aac",
    ".avi",
    ".bmp",
    ".css",
    ".eot",
    ".flac",
    ".gif",
    ".ico",
    ".jpeg",
    ".jpg",
    ".js",
    ".m4a",
    ".mov",
    ".mp3",
    ".ogg",
    ".otf",
    ".png",
    ".svg",
    ".tif",
    ".tiff",
    ".ttf",
    ".wav",
    ".webm",
    ".webp",
    ".woff",
    ".woff2",
}

EXCLUDED_HOSTS = {
    "facebook.com",
    "www.facebook.com",
    "instagram.com",
    "www.instagram.com",
    "linkedin.com",
    "www.linkedin.com",
    "pinterest.com",
    "www.pinterest.com",
    "tiktok.com",
    "www.tiktok.com",
    "twitter.com",
    "www.twitter.com",
    "x.com",
    "www.x.com",
}

TRUSTED_RESOURCE_HOSTS = {
    "archive.org",
    "docs.google.com",
    "drive.google.com",
    "github.com",
    "gitlab.com",
    "vimeo.com",
    "www.youtube.com",
    "youtube.com",
    "youtu.be",
}

EXCLUDED_TEXT_RE = re.compile(
    r"\b("
    r"about|accessibility|account|admission|alumni|apply|blog|careers|cart|"
    r"catalog|cookie|copyright|donate|facebook|feedback|instagram|linkedin|"
    r"login|log in|newsletter|policy|privacy|register|registration|search|"
    r"share|sign in|sign up|store|support|terms|twitter"
    r")\b",
    re.IGNORECASE,
)
EXCLUDED_PATH_RE = re.compile(
    r"/("
    r"about|account|auth|cart|checkout|cookie|donate|login|oauth|privacy|"
    r"search|share|signin|signup|social|store|terms"
    r")(/|$)",
    re.IGNORECASE,
)
COURSE_DOWNLOAD_RE = re.compile(
    r"\b(download (the )?(entire |whole )?course|course download|zip course)\b",
    re.IGNORECASE,
)
GENERIC_OFFSITE_PATH_RE = re.compile(
    r"/("
    r"articles?|become|browse|career(?:s|-academy)?|categories|certificates?|"
    r"degrees?|professional-certificates?|research|search|specializations?"
    r")(/|$)|/(?:projects?)(?:/|$)|"
    r"/(?:courses?)(?:/|\?|$).*(?:[?&]query=)",
    re.IGNORECASE,
)
GENERIC_CHANNEL_PATH_RE = re.compile(
    r"^/(?:@[^/]+|channel/[^/]+|user/[^/]+|c/[^/]+)/?$",
    re.IGNORECASE,
)
PLATFORM_HOSTS = {
    "coursera.org",
    "www.coursera.org",
    "edx.org",
    "www.edx.org",
}
RELEVANCE_STOPWORDS = {
    "advanced",
    "analysis",
    "analog",
    "and",
    "applications",
    "basic",
    "course",
    "design",
    "digital",
    "electrical",
    "engineering",
    "for",
    "from",
    "fundamentals",
    "integrated",
    "introduction",
    "modern",
    "principles",
    "project",
    "projects",
    "science",
    "system",
    "systems",
    "the",
    "to",
    "using",
    "with",
}

KIND_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "exams",
        re.compile(
            r"\b(exams?|examinations?|midterms?|quizzes?|final exam|"
            r"practice tests?|sample tests?)\b|"
            r"(?:^|[/_.-])(?:qz|quiz|exam|midterm|final)[-_ ]?[0-9a-z]*"
            r"(?:$|[/_.-])",
            re.IGNORECASE,
        ),
    ),
    (
        "assignments",
        re.compile(
            r"\b(assignments?|homeworks?|problem sets?|problem sheets?|psets?|"
            r"worksheets?|exercises?|drills?|tutorial problems?)\b|"
            r"(?:^|[/_.-])(?:hw|pset|probset|assignment)[-_ ]?\d+",
            re.IGNORECASE,
        ),
    ),
    (
        "notes",
        re.compile(
            r"\b(lecture notes?|course notes?|class notes?|handouts?|slides?|"
            r"transcripts?|recitation notes?|tutorial notes?)\b|"
            r"(?:^|[/_.-])(?:lec|lecture|notes?)[-_ ]?\d+",
            re.IGNORECASE,
        ),
    ),
    (
        "labs",
        re.compile(
            r"\b(lab(?:orator(?:y|ies))?|experiment(?:s|al)?)\b|"
            r"(?:^|[/_.-])lab[-_ ]?\d+",
            re.IGNORECASE,
        ),
    ),
    (
        "projects",
        re.compile(
            r"\b(capstone|design project|final project|term project|projects?)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "code",
        re.compile(
            r"\b(source code|starter code|code repository|github|gitlab|"
            r"software|simulation files?|matlab|octave|python|jupyter|"
            r"notebooks?|datasets?|data files?|verilog|vhdl|spice|cad files?|"
            r"design files?)\b|(?:^|[/_.-])(?:src|source|code)(?:$|[/_.-])|"
            r"\.(?:ipynb|m|py|c|cc|cpp|h|v|sv|vhd|cir|spice|asc|kicad_[a-z]+|zip)"
            r"(?:$|[?#])",
            re.IGNORECASE,
        ),
    ),
    (
        "video",
        re.compile(
            r"\b(videos?|video lectures?|lecture recordings?|recordings?|"
            r"webcasts?|watch|playlist|youtube|vimeo)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "textbook",
        re.compile(
            r"\b(textbooks?|course texts?|open texts?|online books?|"
            r"e-?books?|book chapters?)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "notes",
        re.compile(
            r"\b(readings?|reading list|papers?|articles?|references?|"
            r"bibliograph(?:y|ies)|chapters?|learning modules?|course materials?)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "course",
        re.compile(
            r"\b(syllabus|course outline|course overview|course calendar|"
            r"schedule|learning objectives?|course information)\b",
            re.IGNORECASE,
        ),
    ),
)

COLLECTION_RE = re.compile(
    r"\b("
    r"assignments?|homeworks?|problem sets?|exams?|lecture notes?|handouts?|"
    r"projects?|labs?|laborator(?:y|ies)|readings?|video lectures?|"
    r"course materials?|resources?"
    r")\b",
    re.IGNORECASE,
)

GENERIC_MODULE_PATH_RE = re.compile(
    r"/(pages|lectures?|modules?|units?|sessions?|topics?|course-materials?|"
    r"materials?|content)(/|$)",
    re.IGNORECASE,
)
GENERIC_MODULE_TITLE_RE = re.compile(
    r"^(?:"
    r"(?:part|unit|module|week|session|topic|chapter|lesson)\s+[A-Z0-9IVX.-]+"
    r"|[0-9]+[.): -]"
    r")",
    re.IGNORECASE,
)
GENERIC_RESOURCE_TITLES = {
    "download",
    "file",
    "github",
    "html",
    "link",
    "m",
    "pdf",
    "resource",
    "video",
    "zip",
}


@dataclass(frozen=True)
class Anchor:
    href: str
    text: str
    title: str
    aria_label: str


class AnchorParser(HTMLParser):
    """Small dependency-free HTML anchor extractor."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.anchors: list[Anchor] = []
        self.base_href: str | None = None
        self._active: dict[str, Any] | None = None

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        values = {key.lower(): value or "" for key, value in attrs}
        if tag.lower() == "base" and values.get("href") and self.base_href is None:
            self.base_href = values["href"]
        if tag.lower() == "a":
            self._active = {
                "href": values.get("href", ""),
                "title": values.get("title", ""),
                "aria_label": values.get("aria-label", ""),
                "parts": [],
            }

    def handle_data(self, data: str) -> None:
        if self._active is not None:
            self._active["parts"].append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() != "a" or self._active is None:
            return
        self.anchors.append(
            Anchor(
                href=self._active["href"],
                text=clean_title(" ".join(self._active["parts"])),
                title=clean_title(self._active["title"]),
                aria_label=clean_title(self._active["aria_label"]),
            )
        )
        self._active = None


@dataclass(frozen=True)
class FetchResult:
    ok: bool
    requested_url: str
    final_url: str
    html: str
    status_code: int | None
    reason: str | None


class PoliteFetcher:
    """Rate-limited HTTP client with robots.txt caching and bounded retries."""

    def __init__(
        self,
        *,
        delay: float,
        timeout: float,
        retries: int,
        respect_robots: bool = True,
    ) -> None:
        self.delay = max(0.0, delay)
        self.timeout = max(1.0, timeout)
        self.retries = max(0, retries)
        self.respect_robots = respect_robots
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.5",
                "Accept-Language": "en-US,en;q=0.8",
            }
        )
        self._last_request: dict[str, float] = {}
        self._robots: dict[str, RobotFileParser | None] = {}
        self.attempted = 0
        self.succeeded = 0
        self.failed = 0

    @staticmethod
    def _origin(url: str) -> str:
        parts = urlsplit(url)
        return f"{parts.scheme.lower()}://{parts.netloc.lower()}"

    def _wait(self, url: str) -> None:
        origin = self._origin(url)
        elapsed = time.monotonic() - self._last_request.get(origin, 0.0)
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self._last_request[origin] = time.monotonic()

    def _request(self, url: str) -> requests.Response:
        self._wait(url)
        return self.session.get(
            url,
            timeout=(min(10.0, self.timeout), self.timeout),
            allow_redirects=True,
        )

    def _robots_parser(self, url: str) -> RobotFileParser | None:
        origin = self._origin(url)
        if origin in self._robots:
            return self._robots[origin]

        robots_url = f"{origin}/robots.txt"
        parser = RobotFileParser()
        parser.set_url(robots_url)
        try:
            response = self._request(robots_url)
            if response.status_code == 200:
                parser.parse(response.text.splitlines())
                self._robots[origin] = parser
            else:
                self._robots[origin] = None
        except requests.RequestException:
            self._robots[origin] = None
        return self._robots[origin]

    def allowed(self, url: str) -> bool:
        if not self.respect_robots:
            return True
        parser = self._robots_parser(url)
        return parser is None or parser.can_fetch(USER_AGENT, url)

    def fetch_html(self, url: str) -> FetchResult:
        self.attempted += 1
        if not self.allowed(url):
            self.failed += 1
            return FetchResult(
                False, url, url, "", None, "robots-denied"
            )

        for attempt in range(self.retries + 1):
            try:
                response = self._request(url)
            except requests.Timeout:
                reason = "timeout"
            except requests.RequestException:
                reason = "request-error"
            else:
                final_url = normalize_url(response.url)
                if not final_url:
                    reason = "non-https-redirect"
                elif response.status_code == 429 or response.status_code >= 500:
                    reason = f"http-{response.status_code}"
                elif not 200 <= response.status_code < 300:
                    self.failed += 1
                    return FetchResult(
                        False,
                        url,
                        final_url,
                        "",
                        response.status_code,
                        f"http-{response.status_code}",
                    )
                else:
                    content_type = response.headers.get("content-type", "").lower()
                    if "html" not in content_type and not response.text.lstrip().startswith(
                        ("<!doctype html", "<html")
                    ):
                        self.failed += 1
                        return FetchResult(
                            False,
                            url,
                            final_url,
                            "",
                            response.status_code,
                            "not-html",
                        )
                    self.succeeded += 1
                    return FetchResult(
                        True,
                        url,
                        final_url,
                        response.text[:4_000_000],
                        response.status_code,
                        None,
                    )

            if attempt < self.retries:
                time.sleep(min(4.0, 0.75 * (2**attempt)))

        self.failed += 1
        return FetchResult(False, url, url, "", None, reason)


def clean_title(value: str) -> str:
    value = (value or "").replace("Â\u00a0", " ").replace("Â ", " ")
    if re.search(r"(?:Ã.|Â|â[\x80-\xBF])", value or ""):
        try:
            repaired = value.encode("latin-1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass
        else:
            if "\ufffd" not in repaired:
                value = repaired
    value = re.sub(r"\s+", " ", value or "").strip()
    value = re.sub(
        r"\s*(?:opens? in (?:a )?new (?:window|tab)|external link)\s*$",
        "",
        value,
        flags=re.IGNORECASE,
    ).strip(" \t\r\n|·•")
    return value[:180]


def is_generic_resource_title(title: str) -> bool:
    normalized = re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()
    return normalized in GENERIC_RESOURCE_TITLES


def _resource_format_hint(title: str, url: str) -> str | None:
    explicit_hint = re.search(
        r"\((PDF|HTML|ZIP|M|PY|IPYNB)\)\s*$",
        title,
        re.IGNORECASE,
    )
    if explicit_hint:
        return explicit_hint.group(1).upper()
    normalized = re.sub(r"[^a-z0-9]+", "", title.lower())
    if normalized in {"pdf", "html", "zip", "m"}:
        return normalized.upper()
    suffix = Path(urlsplit(url).path).suffix.lower().lstrip(".")
    if suffix in {"pdf", "html", "htm", "zip", "m", "py", "ipynb"}:
        return "HTML" if suffix in {"html", "htm"} else suffix.upper()
    return None


def _number_label(value: str) -> str:
    match = re.fullmatch(r"(\d+)([a-z]?)", value, re.IGNORECASE)
    if not match:
        return value.upper()
    return f"{match.group(1)}{match.group(2).upper()}"


def readable_title_from_url(kind: str, title: str, url: str) -> str:
    """Turn a generic file-type anchor into a factual URL-derived label."""

    raw_slug = unquote(Path(urlsplit(url).path.rstrip("/")).name)
    raw_slug = re.sub(r"\.(?:pdf|html?|zip|m|py|ipynb)$", "", raw_slug, flags=re.I)
    lowered = raw_slug.lower()
    solution = bool(re.search(r"(?:^|[_-])(?:sol|solution|solutions)(?:$|[_-])", lowered))

    label: str | None = None
    quiz = re.search(
        r"(?:pract|prct|practice)[_-]*(?:qz|quiz)[_-]*(\d+[a-z]?)",
        lowered,
    )
    if quiz:
        label = f"Practice Quiz {_number_label(quiz.group(1))}"
    else:
        patterns = (
            (r"(?:^|[_-])(?:qz|quiz)[_-]*(\d+[a-z]?)", "Quiz"),
            (r"(?:^|[_-])(?:midterm|mid)[_-]*(\d+[a-z]?)", "Midterm"),
            (r"(?:^|[_-])(?:exam|ex)[_-]*(\d+[a-z]?)", "Exam"),
            (r"(?:^|[_-])(?:lec|lecture)[_-]*(\d+[a-z]?)", "Lecture"),
            (r"(?:^|[_-])(?:hw|homework)[_-]*(\d+[a-z]?)", "Homework"),
            (r"(?:^|[_-])(?:pset|probset)[_-]*(\d+[a-z]?)", "Problem Set"),
            (r"(?:^|[_-])(?:lab)[_-]*(\d+[a-z]?)", "Lab"),
            (r"(?:^|[_-])(?:project|proj)[_-]*(\d+[a-z]?)", "Project"),
        )
        for pattern, prefix in patterns:
            match = re.search(pattern, lowered)
            if match:
                label = f"{prefix} {_number_label(match.group(1))}"
                break
    if label is None and re.search(r"(?:^|[_-])final(?:$|[_-])", lowered):
        label = "Final Exam" if kind == "exams" else "Final"
    if label is not None and solution and "Solution" not in label:
        label += " Solution"

    if label is None:
        cleaned_slug = re.sub(r"[_-]+", " ", raw_slug).strip()
        cleaned_slug = re.sub(r"\s+", " ", cleaned_slug)
        kind_label = {
            "course": "Course resource",
            "video": "Video resource",
            "notes": "Notes resource",
            "assignments": "Assignment resource",
            "labs": "Lab resource",
            "projects": "Project resource",
            "exams": "Exam resource",
            "code": "Code resource",
            "textbook": "Textbook resource",
        }.get(kind, "Learning resource")
        label = f"{kind_label}: {cleaned_slug or 'linked material'}"

    format_hint = _resource_format_hint(title, url)
    if format_hint:
        label += f" ({format_hint})"
    return clean_title(label)


def normalize_resource_title_and_kind(resource: dict[str, Any]) -> None:
    """Apply direct URL kind evidence and repair generic anchor labels."""

    title = clean_title(str(resource.get("title", "")))
    resource["title"] = title
    generated_fallback = bool(
        re.match(
            r"^(?:course|video|notes|assignment|lab|project|exam|code|"
            r"textbook|learning) resource:",
            title,
            re.IGNORECASE,
        )
    )
    if not is_generic_resource_title(title) and not generated_fallback:
        return
    direct_kind = classify_resource("", str(resource.get("url", "")))
    source_kind = classify_resource("", str(resource.get("source_url", "")))
    kind = direct_kind or source_kind or str(resource.get("kind", "notes"))
    if kind not in KINDS:
        kind = "notes"
    resource["kind"] = kind
    resource["title"] = readable_title_from_url(
        kind, title, str(resource.get("url", ""))
    )


def ensure_unique_course_titles(
    resources: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows = [dict(resource) for resource in resources]
    groups: dict[tuple[int, str], list[dict[str, Any]]] = defaultdict(list)
    for resource in rows:
        groups[(resource["course_id"], resource["title"].casefold())].append(resource)
    for duplicates in groups.values():
        if len(duplicates) < 2:
            continue
        for resource in sorted(duplicates, key=lambda item: item["url"]):
            parts = urlsplit(resource["url"])
            host = (parts.hostname or "resource").lower().removeprefix("www.")
            slug = Path(parts.path.rstrip("/")).name
            suffix = host if not slug else f"{host}/{slug}"
            resource["title"] = clean_title(f"{resource['title']} — {suffix}")
    used_by_course: dict[int, set[str]] = defaultdict(set)
    for resource in sorted(
        rows,
        key=lambda item: (
            item["course_id"],
            item["title"].casefold(),
            item["url"],
        ),
    ):
        used = used_by_course[resource["course_id"]]
        key = resource["title"].casefold()
        if key in used:
            digest = hashlib.sha256(resource["url"].encode("utf-8")).hexdigest()[:8]
            resource["title"] = clean_title(
                f"{resource['title']} — resource {digest}"
            )
            key = resource["title"].casefold()
        used.add(key)
    return sorted(
        rows,
        key=lambda item: (
            item["course_id"],
            KIND_ORDER[item["kind"]],
            item["title"].casefold(),
            item["url"],
        ),
    )


def title_quality_counts(
    resources: Iterable[dict[str, Any]],
) -> dict[str, int]:
    rows = list(resources)
    generic_count = sum(
        is_generic_resource_title(str(resource.get("title", "")))
        for resource in rows
    )
    title_counts = Counter(
        (
            resource.get("course_id"),
            str(resource.get("title", "")).casefold(),
        )
        for resource in rows
    )
    duplicate_count = sum(count - 1 for count in title_counts.values() if count > 1)
    return {
        "generic_title_count": generic_count,
        "duplicate_title_count": duplicate_count,
    }


def ensure_evidenced_candidate_seeds(
    resources: Iterable[dict[str, Any]],
    candidates: list[dict[str, Any]],
    failures: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Retain every seed that was itself fetched or explicitly failed."""

    rows = [dict(resource) for resource in resources]
    existing = {
        (resource["course_id"], resource["url"]) for resource in rows
    }
    evidenced_sources = {
        (resource["course_id"], resource["source_url"]) for resource in rows
    }
    failed_sources = {
        (failure["course_id"], failure["source_url"]) for failure in failures
    }
    for candidate in candidates:
        for raw_seed in [
            candidate["url"],
            *candidate.get("alternate_urls", []),
        ]:
            seed = normalize_url(raw_seed)
            if not seed or (candidate["id"], seed) in existing:
                continue
            key = (candidate["id"], seed)
            if key not in evidenced_sources and key not in failed_sources:
                continue
            resource = make_resource(
                course_id=candidate["id"],
                kind="course",
                title=f"{candidate['title']} — official course overview",
                url=seed,
                source_url=seed,
                source_fetched=key not in failed_sources,
            )
            if resource is not None:
                rows.append(resource)
                existing.add(key)
    return rows


def normalize_url(raw_url: str, base_url: str | None = None) -> str | None:
    """Return a canonical HTTPS URL or ``None`` when the URL is unsuitable."""

    if not raw_url:
        return None
    raw_url = raw_url.strip()
    if raw_url.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return None
    if raw_url.startswith("//"):
        raw_url = f"https:{raw_url}"
    elif base_url:
        raw_url = urljoin(base_url, raw_url)

    try:
        parts = urlsplit(raw_url)
    except ValueError:
        return None
    if parts.scheme.lower() != "https" or not parts.netloc:
        return None

    host = parts.hostname.lower() if parts.hostname else ""
    if host in EXCLUDED_HOSTS:
        return None
    path = re.sub(r"/{2,}", "/", parts.path or "/")
    if path != "/":
        path = path.rstrip("/")
    if EXCLUDED_PATH_RE.search(path):
        return None
    extension = Path(path.lower()).suffix
    if extension in BLOCKED_EXTENSIONS:
        return None

    filtered_query = []
    for key, value in parse_qsl(parts.query, keep_blank_values=True):
        lowered = key.lower()
        if lowered in TRACKING_QUERY_KEYS or lowered.startswith(
            TRACKING_QUERY_PREFIXES
        ):
            continue
        filtered_query.append((key, value))
    query = urlencode(filtered_query, doseq=True)

    netloc = parts.netloc.lower()
    if netloc.endswith(":443"):
        netloc = netloc[:-4]
    return urlunsplit(("https", netloc, path, query, ""))


def anchor_title(anchor: Anchor, url: str) -> str:
    title = anchor.text or anchor.title or anchor.aria_label
    if title:
        return clean_title(title)
    path_name = Path(urlsplit(url).path.rstrip("/")).name
    return clean_title(re.sub(r"[-_]+", " ", path_name))


EXACT_LAB_TOKEN_RE = re.compile(
    r"(?:^|[\s/_.-])labs?(?:$|[\s/_.-])",
    re.IGNORECASE,
)
EXACT_PROJECT_TOKEN_RE = re.compile(
    r"(?:^|[\s/_.-])projects?(?:$|[\s/_.-])",
    re.IGNORECASE,
)


def _classification_haystack(title: str, url: str) -> str:
    parts = urlsplit(url)
    path = unquote(parts.path)
    lowered_path = path.lower()
    if "/resources/" in lowered_path:
        relevant_path = path[lowered_path.index("/resources/") + len("/resources/") :]
    elif "/pages/" in lowered_path:
        relevant_path = path[lowered_path.index("/pages/") + len("/pages/") :]
    else:
        segments = [segment for segment in path.split("/") if segment]
        relevant_path = "/".join(segments[-2:])
    host_hint = ""
    host = (parts.hostname or "").lower()
    if host in {"github.com", "gitlab.com"}:
        host_hint = " code repository"
    elif host in {
        "youtube.com",
        "www.youtube.com",
        "youtu.be",
        "vimeo.com",
    }:
        host_hint = " video"
    haystack = f"{title} {relevant_path} {parts.query}{host_hint}"
    # Course sites commonly join semantic path labels with "-", "_", or "/"
    # (for example, ``pages/lecture-notes``).  Preserve the original text for
    # slug-token patterns and add a word-separated view for phrase patterns.
    return f"{haystack} {re.sub(r'[-_/]+', ' ', haystack)}"


def explicit_collection_kind(title: str, url: str) -> str | None:
    """Return exact labs/projects collection evidence, if unambiguous."""

    haystack = _classification_haystack(title, url)
    # An exam or assignment token names a more specific artifact than the
    # surrounding lab/project collection and therefore keeps precedence.
    if any(pattern.search(haystack) for _kind, pattern in KIND_PATTERNS[:2]):
        return None
    if EXACT_LAB_TOKEN_RE.search(haystack):
        return "labs"
    if EXACT_PROJECT_TOKEN_RE.search(haystack):
        return "projects"
    return None


def classify_resource(title: str, url: str) -> str | None:
    haystack = _classification_haystack(title, url)
    for kind, pattern in KIND_PATTERNS[:2]:
        if pattern.search(haystack):
            return kind
    collection_kind = explicit_collection_kind(title, url)
    if collection_kind:
        return collection_kind
    for kind, pattern in KIND_PATTERNS[2:]:
        if pattern.search(haystack):
            return kind
    return None


def course_path_prefix(seed_url: str) -> str:
    path = urlsplit(seed_url).path
    if path.endswith("/"):
        return path
    if not Path(path).suffix:
        return path + "/"
    return path.rsplit("/", 1)[0] + "/"


def same_course_scope(url: str, seed_url: str) -> bool:
    target = urlsplit(url)
    seed = urlsplit(seed_url)
    if target.hostname != seed.hostname:
        return False
    prefix = course_path_prefix(seed_url)
    return len(prefix) > 1 and target.path.startswith(prefix)


def exact_or_course_subtree(url: str, seed_url: str) -> bool:
    """Return whether a URL is the seed or below its explicit course directory."""

    target = urlsplit(url)
    seed = urlsplit(seed_url)
    if target.hostname != seed.hostname:
        return False
    target_path = target.path.rstrip("/") or "/"
    seed_path = seed.path.rstrip("/") or "/"
    if target_path == seed_path:
        return True
    # A seed ending in a document is a landing page, not authority over the
    # faculty member's entire directory.
    if Path(seed_path).suffix:
        return False
    return target_path.startswith(seed_path + "/")


def candidate_relevance_terms(
    candidate: dict[str, Any], *, include_url_slug: bool = True
) -> dict[str, set[str]]:
    def words(value: str) -> list[str]:
        return re.findall(r"[a-z0-9]+", value.lower())

    title_words = [
        word
        for word in words(str(candidate.get("title", "")))
        if len(word) >= 4 and word not in RELEVANCE_STOPWORDS
    ]
    code = "".join(words(str(candidate.get("code", ""))))
    slug_terms: set[str] = set()
    if include_url_slug:
        for raw_seed in [
            candidate.get("url", ""),
            *candidate.get("alternate_urls", []),
        ]:
            seed = normalize_url(str(raw_seed))
            if not seed:
                continue
            segment = Path(urlsplit(seed).path).name
            for word in words(segment):
                if len(word) >= 5 and word not in RELEVANCE_STOPWORDS:
                    slug_terms.add(word)
    phrases = {
        "".join(words(str(candidate.get("title", "")))),
        code,
    }
    phrases = {phrase for phrase in phrases if len(phrase) >= 4}
    return {
        "tokens": set(title_words) | slug_terms,
        "phrases": phrases,
    }


def relevance_match(
    candidate: dict[str, Any], *values: str, include_url_slug: bool = True
) -> bool:
    terms = candidate_relevance_terms(
        candidate, include_url_slug=include_url_slug
    )
    haystack = " ".join(values).lower()
    compact = "".join(re.findall(r"[a-z0-9]+", haystack))
    if any(phrase in compact for phrase in terms["phrases"]):
        return True
    haystack_tokens = set(re.findall(r"[a-z0-9]+", haystack))
    matched = terms["tokens"] & haystack_tokens
    if len(matched) >= 2:
        return True
    return any(len(token) >= 8 for token in matched)


def seed_is_course_specific(candidate: dict[str, Any], seed_url: str) -> bool:
    return relevance_match(
        candidate,
        urlsplit(seed_url).path,
        include_url_slug=False,
    )


def is_generic_home_channel_or_repo(url: str) -> bool:
    parts = urlsplit(url)
    host = (parts.hostname or "").lower()
    path = parts.path.rstrip("/") or "/"
    if path == "/":
        return True
    if host in {"youtube.com", "www.youtube.com", "youtu.be"}:
        return bool(GENERIC_CHANNEL_PATH_RE.match(path))
    if host in {"github.com", "gitlab.com"}:
        segments = [segment for segment in path.split("/") if segment]
        return len(segments) < 2
    return False


def resource_relevance(
    resource: dict[str, Any], candidate: dict[str, Any]
) -> tuple[bool, str]:
    """Apply course-scope precision rules to one discovered resource."""

    url = resource["url"]
    source_url = resource["source_url"]
    title = resource["title"]
    seeds = [
        seed
        for raw_seed in [candidate["url"], *candidate.get("alternate_urls", [])]
        if (seed := normalize_url(raw_seed))
    ]
    if any(url == seed for seed in seeds):
        resource["kind"] = "course"
        resource["title"] = clean_title(
            f"{candidate['title']} — official course overview"
        )
        return True, "candidate-seed"

    direct_kind = classify_resource(title, url)
    matching_seed = next(
        (seed for seed in seeds if exact_or_course_subtree(url, seed)), None
    )
    source_seed = next(
        (seed for seed in seeds if exact_or_course_subtree(source_url, seed)), None
    )

    if direct_kind is None and matching_seed is not None and looks_like_generic_module(
        title, url, matching_seed
    ):
        direct_kind = "notes"
    if direct_kind is None:
        return False, "no-direct-kind-evidence"
    resource["kind"] = direct_kind

    host = (urlsplit(url).hostname or "").lower()
    source_host = (urlsplit(source_url).hostname or "").lower()
    platform_source = source_host in PLATFORM_HOSTS
    relevant = relevance_match(candidate, title, url)

    if re.search(r"(?:^|[/_.-])(?:undefined|null)(?:[/_.-]|$)", url, re.IGNORECASE):
        return False, "placeholder-url"
    if (
        host != source_host
        and title.strip().lower() in {"video", "watch", "watch now", "link"}
        and not relevant
    ):
        return False, "generic-external-title"
    query_keys = {
        key.lower() for key, _value in parse_qsl(urlsplit(url).query)
    }
    if host in PLATFORM_HOSTS and query_keys & {
        "query",
        "q",
        "search",
        "productdifficultylevel",
    }:
        return False, "platform-search-query"
    if (
        GENERIC_OFFSITE_PATH_RE.search(
            f"{urlsplit(url).path}?{urlsplit(url).query}"
        )
        and matching_seed is None
    ):
        return False, "generic-navigation-path"
    if is_generic_home_channel_or_repo(url) and not relevant:
        return False, "generic-home-channel-or-repo"

    # Product-platform HTML is navigation-heavy. Only a link still carrying the
    # course slug/code/topic may leave the exact product subtree.
    if platform_source and matching_seed is None and not relevant:
        return False, "platform-unrelated"

    # Same-host links outside a course directory are often global research,
    # faculty, certificate, or catalogue navigation.
    if host == source_host and matching_seed is None and not relevant:
        return False, "same-host-outside-course"

    if source_seed is None and matching_seed is None and not relevant:
        return False, "outside-course-provenance"

    # A broad faculty/shop landing page is evidence only for links that identify
    # the selected course. It is not authority over every publication or channel.
    if (
        source_seed is not None
        and not seed_is_course_specific(candidate, source_seed)
        and matching_seed is None
        and not relevant
    ):
        return False, "generic-seed-unrelated"

    # Repositories are easy to over-collect from global navigation. Require a
    # course-relevant repository name/title unless the repository is itself a seed.
    if host in {"github.com", "gitlab.com"} and matching_seed is None and not relevant:
        return False, "generic-repository"
    return True, "kept"


def filter_course_resources(
    resources: Iterable[dict[str, Any]], candidate: dict[str, Any]
) -> tuple[list[dict[str, Any]], Counter[str]]:
    kept: list[dict[str, Any]] = []
    reasons: Counter[str] = Counter()
    for original in resources:
        resource = dict(original)
        normalize_resource_title_and_kind(resource)
        allowed, reason = resource_relevance(resource, candidate)
        if allowed:
            kept.append(resource)
        else:
            reasons[reason] += 1
    return kept, reasons


def filter_checkpoint_resources(
    checkpoint: dict[str, Any], candidates: list[dict[str, Any]]
) -> dict[str, Any]:
    existing = checkpoint.get("precision_filter", {})
    if (
        isinstance(existing, dict)
        and existing.get("version") == PRECISION_FILTER_VERSION
    ):
        return existing
    by_id = {candidate["id"]: candidate for candidate in candidates}
    totals: Counter[str] = Counter()
    before_total = 0
    after_total = 0
    for course_id, resources in checkpoint.get("course_resources", {}).items():
        candidate = by_id.get(int(course_id))
        if candidate is None or not isinstance(resources, list):
            continue
        filtered, reasons = filter_course_resources(resources, candidate)
        before_total += len(resources)
        after_total += len(filtered)
        totals.update(reasons)
        checkpoint["course_resources"][course_id] = filtered
    precision_filter = {
        "version": PRECISION_FILTER_VERSION,
        "before_resources": before_total,
        "after_resources": after_total,
        "removed_resources": before_total - after_total,
        "removed_by_reason": dict(sorted(totals.items())),
    }
    checkpoint["precision_filter"] = precision_filter
    return precision_filter


def build_review_candidates(
    resources: Iterable[dict[str, Any]],
    candidates: list[dict[str, Any]],
    *,
    limit: int = 120,
) -> dict[str, Any]:
    """Return a bounded, deterministic queue for manual precision review."""

    by_id = {candidate["id"]: candidate for candidate in candidates}
    flagged: list[dict[str, Any]] = []
    for resource in resources:
        candidate = by_id[resource["course_id"]]
        seeds = {
            seed
            for raw_seed in [candidate["url"], *candidate.get("alternate_urls", [])]
            if (seed := normalize_url(raw_seed))
        }
        if resource["url"] in seeds:
            continue
        reasons: list[str] = []
        if resource["status"] == "review-needed":
            reasons.append("review-needed-status")
        if not relevance_match(candidate, resource["title"], resource["url"]):
            target_host = (urlsplit(resource["url"]).hostname or "").lower()
            source_host = (urlsplit(resource["source_url"]).hostname or "").lower()
            if target_host != source_host:
                reasons.append("external-link-relies-on-course-page-provenance")
            elif len(resource["title"].split()) <= 2:
                reasons.append("short-title-without-course-token")
        if not reasons:
            continue
        flagged.append(
            {
                "course_id": resource["course_id"],
                "title": resource["title"],
                "url": resource["url"],
                "source_url": resource["source_url"],
                "reason": ", ".join(reasons),
            }
        )
    flagged.sort(
        key=lambda item: (
            item["course_id"],
            item["reason"],
            item["title"].casefold(),
            item["url"],
        )
    )
    return {
        "total_flagged": len(flagged),
        "shown": min(len(flagged), limit),
        "items": flagged[:limit],
    }


def build_domain_samples(
    resources: Iterable[dict[str, Any]],
    candidates: list[dict[str, Any]],
    *,
    courses_per_domain: int = 3,
    resources_per_course: int = 6,
) -> list[dict[str, Any]]:
    """Build deterministic pseudo-random samples for every provider domain."""

    resources_by_course: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for resource in resources:
        resources_by_course[resource["course_id"]].append(resource)
    candidates_by_host: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for candidate in candidates:
        host = (urlsplit(candidate["url"]).hostname or "").lower()
        candidates_by_host[host].append(candidate)

    samples: list[dict[str, Any]] = []
    for host in sorted(candidates_by_host):
        ranked = sorted(
            candidates_by_host[host],
            key=lambda candidate: hashlib.sha256(
                f"{host}:{candidate['id']}".encode("utf-8")
            ).hexdigest(),
        )
        course_samples = []
        for candidate in ranked[:courses_per_domain]:
            rows = sorted(
                resources_by_course.get(candidate["id"], []),
                key=lambda item: (
                    KIND_ORDER[item["kind"]],
                    item["title"].casefold(),
                    item["url"],
                ),
            )
            course_samples.append(
                {
                    "course_id": candidate["id"],
                    "course_title": candidate["title"],
                    "resource_count": len(rows),
                    "by_kind": dict(
                        sorted(Counter(row["kind"] for row in rows).items())
                    ),
                    "sample_resources": [
                        {
                            "kind": row["kind"],
                            "title": row["title"],
                            "url": row["url"],
                        }
                        for row in rows[:resources_per_course]
                    ],
                }
            )
        samples.append(
            {
                "domain": host,
                "available_courses": len(candidates_by_host[host]),
                "sampled_courses": course_samples,
            }
        )
    return samples


def hard_blacklist_reason(
    resource: dict[str, Any], candidate: dict[str, Any]
) -> str | None:
    """Return a known navigation-junk reason, independent of ranking."""

    parts = urlsplit(resource["url"])
    host = (parts.hostname or "").lower()
    path_query = f"{parts.path}?{parts.query}"
    seeds = [
        seed
        for raw_seed in [candidate["url"], *candidate.get("alternate_urls", [])]
        if (seed := normalize_url(raw_seed))
    ]
    in_course_subtree = any(
        exact_or_course_subtree(resource["url"], seed) for seed in seeds
    )
    if host in {"coursera.org", "www.coursera.org"} and re.search(
        r"^/(?:articles?|certificates?|professional-certificates?|"
        r"specializations?|projects?|search|browse)(?:/|$)|"
        r"(?:[?&](?:query|q|productDifficultyLevel)=)",
        path_query,
        re.IGNORECASE,
    ):
        return "coursera-global-navigation"
    if re.search(r"/research/projects?(?:/|$)", parts.path, re.IGNORECASE):
        return "global-research-projects"
    if (
        re.search(r"^/projects?(?:/|$)", parts.path, re.IGNORECASE)
        and not in_course_subtree
    ):
        return "generic-projects"
    if host in {"edx.org", "www.edx.org"} and not in_course_subtree:
        if not relevance_match(candidate, resource["title"], resource["url"]):
            return "edx-unrelated-product"
    if candidate["id"] == 38 and not relevance_match(
        candidate, resource["title"], resource["url"]
    ):
        if resource["url"] not in seeds:
            return "generic-faculty-publication"
    return None


def precision_blacklist_matches(
    resources: Iterable[dict[str, Any]], candidates: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    by_id = {candidate["id"]: candidate for candidate in candidates}
    matches: list[dict[str, Any]] = []
    for resource in resources:
        candidate = by_id[resource["course_id"]]
        reason = hard_blacklist_reason(resource, candidate)
        if reason:
            matches.append(
                {
                    "course_id": resource["course_id"],
                    "title": resource["title"],
                    "url": resource["url"],
                    "reason": reason,
                }
            )
    return sorted(
        matches,
        key=lambda item: (
            item["course_id"],
            item["reason"],
            item["title"].casefold(),
            item["url"],
        ),
    )


def looks_like_generic_module(title: str, url: str, seed_url: str) -> bool:
    """Recognize substantive unit pages when a page omits resource keywords."""

    if not same_course_scope(url, seed_url):
        return False
    path = urlsplit(url).path
    seed_path = urlsplit(seed_url).path.rstrip("/") + "/"
    if path.rstrip("/") == seed_path.rstrip("/"):
        return False
    if not GENERIC_MODULE_PATH_RE.search(path):
        return False
    if len(title) < 4 or title.lower() in {
        "home",
        "next",
        "previous",
        "read more",
        "learn more",
        "course home",
    }:
        return False
    return bool(GENERIC_MODULE_TITLE_RE.search(title)) or len(title) >= 4


def is_collection_page(title: str, url: str, seed_url: str) -> bool:
    if not same_course_scope(url, seed_url):
        return False
    suffix = Path(urlsplit(url).path.rstrip("/")).suffix.lower()
    if suffix and suffix not in {".html", ".htm"}:
        return False
    combined = f"{title} {urlsplit(url).path}"
    return bool(COLLECTION_RE.search(combined))


def infer_access(url: str, source_url: str) -> str | None:
    host = (urlsplit(url).hostname or "").lower()
    source_host = (urlsplit(source_url).hostname or "").lower()
    path_and_query = f"{urlsplit(url).path} {urlsplit(url).query}".lower()

    if "coursera.org" in host:
        return "open-registration"
    if host.endswith("edx.org"):
        return "free-audit"
    if any(token in path_and_query for token in ("purchase", "checkout", "buy-now")):
        return "paid"
    if host == source_host or host in TRUSTED_RESOURCE_HOSTS:
        return "open"
    if host.endswith(
        (
            ".edu",
            ".edu.cn",
            ".edu.au",
            ".ac.in",
            ".ac.uk",
            ".ac.jp",
            ".org",
        )
    ):
        return "open"
    # A link leaving the official/trusted educational host may still be useful,
    # but its access model cannot be inferred from an anchor alone. Omitting it
    # is safer than inventing "limited-free" or "open-registration" evidence.
    return None


def resource_status(url: str, source_url: str, source_fetched: bool) -> str:
    if not source_fetched:
        return "review-needed"
    host = (urlsplit(url).hostname or "").lower()
    path = urlsplit(url).path.lower()
    if "archive" in host or "/archive" in path:
        return "archived"
    source_host = (urlsplit(source_url).hostname or "").lower()
    if host == source_host or host in TRUSTED_RESOURCE_HOSTS:
        return "available"
    if host.endswith(
        (
            ".edu",
            ".edu.cn",
            ".edu.au",
            ".ac.in",
            ".ac.uk",
            ".ac.jp",
        )
    ):
        return "available"
    return "review-needed"


def make_resource(
    *,
    course_id: int,
    kind: str,
    title: str,
    url: str,
    source_url: str,
    source_fetched: bool,
) -> dict[str, Any] | None:
    access = infer_access(url, source_url)
    if access is None:
        return None
    return {
        "course_id": course_id,
        "kind": kind,
        "title": clean_title(title),
        "url": url,
        "access": access,
        "status": resource_status(url, source_url, source_fetched),
        "last_verified": VERIFIED_DATE,
        "source_url": source_url,
    }


def parse_anchors(html: str, base_url: str) -> list[Anchor]:
    parser = AnchorParser()
    try:
        parser.feed(html)
    except Exception:
        # HTML in the wild is frequently malformed. HTMLParser usually recovers;
        # retain links parsed before an exceptional malformed construct.
        pass
    base_parts = urlsplit(base_url)
    join_path = base_parts.path
    if join_path != "/" and not join_path.endswith("/") and not Path(join_path).suffix:
        join_path += "/"
    join_base = urlunsplit(
        (
            base_parts.scheme,
            base_parts.netloc,
            join_path,
            base_parts.query,
            "",
        )
    )
    effective_base = (
        urljoin(join_base, parser.base_href) if parser.base_href else join_base
    )
    if normalize_url(effective_base) is None:
        effective_base = join_base
    normalized: list[Anchor] = []
    for anchor in parser.anchors:
        url = normalize_url(anchor.href, effective_base)
        if not url:
            continue
        normalized.append(
            Anchor(
                href=url,
                text=anchor.text,
                title=anchor.title,
                aria_label=anchor.aria_label,
            )
        )
    return normalized


def reject_anchor(title: str, url: str) -> bool:
    if not title or len(title) > 180:
        return True
    if EXCLUDED_TEXT_RE.search(title):
        return True
    if COURSE_DOWNLOAD_RE.search(f"{title} {url}"):
        return True
    if title.lower() in {
        "click here",
        "download",
        "here",
        "link",
        "more",
        "next",
        "previous",
        "read more",
    }:
        return True
    return False


def extract_resources_from_html(
    *,
    course_id: int,
    html: str,
    page_url: str,
    seed_url: str,
    fallback_kind: str | None = None,
) -> tuple[list[dict[str, Any]], list[tuple[str, str, str]]]:
    resources: list[dict[str, Any]] = []
    collections: list[tuple[str, str, str]] = []
    for anchor in parse_anchors(html, page_url):
        url = anchor.href
        title = anchor_title(anchor, url)
        if reject_anchor(title, url):
            continue

        kind = classify_resource(title, url)
        if kind is None and looks_like_generic_module(title, url, seed_url):
            kind = "notes"
        if kind is None and fallback_kind is not None:
            suffix = Path(urlsplit(url).path).suffix.lower()
            if same_course_scope(url, seed_url) or suffix in {
                ".pdf",
                ".doc",
                ".docx",
                ".ppt",
                ".pptx",
                ".tex",
                ".zip",
                ".ipynb",
                ".m",
                ".py",
                ".c",
                ".cpp",
                ".v",
                ".sv",
                ".vhd",
            }:
                kind = fallback_kind
        if kind is None:
            continue

        resource = make_resource(
            course_id=course_id,
            kind=kind,
            title=title,
            url=url,
            source_url=page_url,
            source_fetched=True,
        )
        if resource is None:
            continue
        resources.append(resource)
        if is_collection_page(title, url, seed_url):
            collections.append((url, title, kind))
    return resources, collections


def de_duplicate_and_limit(
    resources: Iterable[dict[str, Any]], max_per_course: int
) -> list[dict[str, Any]]:
    """De-duplicate by course and URL, then cap with balanced kind coverage."""

    by_course_and_url: dict[tuple[int, str], dict[str, Any]] = {}
    for resource in resources:
        key = (resource["course_id"], resource["url"])
        current = by_course_and_url.get(key)
        if current is None:
            by_course_and_url[key] = resource
            continue
        # Prefer an available record, then a specific resource type over a
        # generic course/module record, then the lexicographically stable source.
        candidate_score = (
            resource["status"] == "available",
            resource["kind"] != "course",
            -KIND_ORDER[resource["kind"]],
        )
        current_score = (
            current["status"] == "available",
            current["kind"] != "course",
            -KIND_ORDER[current["kind"]],
        )
        if candidate_score > current_score or (
            candidate_score == current_score
            and resource["source_url"] < current["source_url"]
        ):
            by_course_and_url[key] = resource

    grouped: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for resource in by_course_and_url.values():
        grouped[resource["course_id"]].append(resource)

    selected: list[dict[str, Any]] = []
    for course_id in sorted(grouped):
        per_kind: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for resource in grouped[course_id]:
            per_kind[resource["kind"]].append(resource)
        for bucket in per_kind.values():
            bucket.sort(
                key=lambda item: (
                    item["status"] != "available",
                    item["title"].casefold(),
                    item["url"],
                )
            )

        course_selected: list[dict[str, Any]] = []
        # A round-robin cap prevents a 50-lecture collection from hiding a
        # course's assignments, exams, code, or laboratory links.
        while len(course_selected) < max_per_course and any(per_kind.values()):
            progressed = False
            for kind in KINDS:
                if per_kind[kind] and len(course_selected) < max_per_course:
                    course_selected.append(per_kind[kind].pop(0))
                    progressed = True
            if not progressed:
                break
        selected.extend(course_selected)

    return sorted(
        selected,
        key=lambda item: (
            item["course_id"],
            KIND_ORDER[item["kind"]],
            item["title"].casefold(),
            item["url"],
        ),
    )


def load_candidates(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError("candidate file must contain a JSON array")
    ids = [item.get("id") for item in data]
    if any(not isinstance(course_id, int) for course_id in ids):
        raise ValueError("every candidate must have an integer id")
    if len(ids) != len(set(ids)):
        raise ValueError("candidate ids must be unique")
    for item in data:
        if normalize_url(item.get("url", "")) is None:
            raise ValueError(f"candidate {item['id']} has a non-HTTPS primary URL")
        alternates = item.get("alternate_urls", [])
        if not isinstance(alternates, list):
            raise ValueError(f"candidate {item['id']} alternate_urls must be an array")
        for alternate in alternates:
            if normalize_url(alternate) is None:
                raise ValueError(
                    f"candidate {item['id']} has a non-HTTPS alternate URL"
                )
    return sorted(data, key=lambda item: item["id"])


def build_stats(
    *,
    candidates: list[dict[str, Any]],
    resources: list[dict[str, Any]],
    failures: list[dict[str, Any]],
    fetcher: PoliteFetcher | None = None,
    fetch_counts: dict[str, int] | None = None,
) -> dict[str, Any]:
    available_landings = {
        item["course_id"]
        for item in resources
        if item["status"] == "available"
        and item["kind"] == "course"
        and item["url"] == item["source_url"]
    }
    extracted_courses = {
        item["course_id"] for item in resources if item["url"] != item["source_url"]
    }
    if fetch_counts is None:
        if fetcher is None:
            raise ValueError("fetcher or fetch_counts is required")
        fetch_counts = {
            "attempted": fetcher.attempted,
            "succeeded": fetcher.succeeded,
            "failed": fetcher.failed,
        }
    return {
        "candidate_courses": len(candidates),
        "courses_with_any_resource": len({item["course_id"] for item in resources}),
        "courses_with_available_landing": len(available_landings),
        "courses_with_extracted_resources": len(extracted_courses),
        "total_resources": len(resources),
        "available_resources": sum(
            item["status"] == "available" for item in resources
        ),
        "review_needed_resources": sum(
            item["status"] == "review-needed" for item in resources
        ),
        "by_kind": dict(
            sorted(Counter(item["kind"] for item in resources).items())
        ),
        "by_access": dict(
            sorted(Counter(item["access"] for item in resources).items())
        ),
        "fetches": fetch_counts,
        "failed_sources": len(failures),
    }


def crawl(
    candidates: list[dict[str, Any]],
    *,
    delay: float,
    timeout: float,
    retries: int,
    max_collection_pages: int,
    max_resources_per_course: int,
    respect_robots: bool,
    checkpoint_path: Path | None,
    resume: bool,
    retry_failed_courses: bool,
) -> dict[str, Any]:
    fetcher = PoliteFetcher(
        delay=delay,
        timeout=timeout,
        retries=retries,
        respect_robots=respect_robots,
    )
    checkpoint: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "last_verified": VERIFIED_DATE,
        "completed_course_ids": [],
        "course_resources": {},
        "course_failures": {},
        "fetches": {"attempted": 0, "succeeded": 0, "failed": 0},
        "precision_filter": {
            "version": PRECISION_FILTER_VERSION,
            "before_resources": 0,
            "after_resources": 0,
            "removed_resources": 0,
            "removed_by_reason": {},
        },
    }
    if resume and checkpoint_path is not None and checkpoint_path.exists():
        with checkpoint_path.open(encoding="utf-8") as handle:
            loaded = json.load(handle)
        migrate_checkpoint_kinds(loaded)
        filter_checkpoint_resources(loaded, candidates)
        validate_checkpoint(
            loaded, candidate_ids={item["id"] for item in candidates}
        )
        checkpoint = loaded
        if retry_failed_courses:
            retry_ids = {
                int(course_id)
                for course_id, course_failures in checkpoint[
                    "course_failures"
                ].items()
                if course_failures
            }
            checkpoint["completed_course_ids"] = [
                course_id
                for course_id in checkpoint["completed_course_ids"]
                if course_id not in retry_ids
            ]
            for course_id in retry_ids:
                checkpoint["course_resources"].pop(str(course_id), None)
                checkpoint["course_failures"].pop(str(course_id), None)

    completed_course_ids = set(checkpoint["completed_course_ids"])
    all_resources = [
        resource
        for course_id in sorted(
            checkpoint["course_resources"], key=lambda value: int(value)
        )
        for resource in checkpoint["course_resources"][course_id]
    ]
    failures = [
        failure
        for course_id in sorted(
            checkpoint["course_failures"], key=lambda value: int(value)
        )
        for failure in checkpoint["course_failures"][course_id]
    ]
    fetcher.attempted = checkpoint["fetches"]["attempted"]
    fetcher.succeeded = checkpoint["fetches"]["succeeded"]
    fetcher.failed = checkpoint["fetches"]["failed"]

    for index, course in enumerate(candidates, start=1):
        course_id = course["id"]
        if course_id in completed_course_ids:
            print(
                f"[{index:03d}/{len(candidates):03d}] "
                f"{course_id}: {course['title']} (checkpoint)",
                flush=True,
            )
            continue
        seeds = [course["url"], *course.get("alternate_urls", [])]
        visited_collections: set[str] = set()
        course_resources: list[dict[str, Any]] = []
        course_failures: list[dict[str, Any]] = []

        print(
            f"[{index:03d}/{len(candidates):03d}] "
            f"{course_id}: {course['title']}",
            flush=True,
        )
        for raw_seed in seeds:
            seed_url = normalize_url(raw_seed)
            assert seed_url is not None
            result = fetcher.fetch_html(seed_url)
            landing_url = result.final_url if result.ok else seed_url
            landing = make_resource(
                course_id=course_id,
                kind="course",
                title=f"{course['title']} — official course overview",
                url=landing_url,
                source_url=seed_url,
                source_fetched=result.ok,
            )
            if landing is not None:
                course_resources.append(landing)
            if not result.ok:
                course_failures.append(
                    {
                        "course_id": course_id,
                        "source_url": seed_url,
                        "reason": result.reason,
                    }
                )
                continue

            extracted, collections = extract_resources_from_html(
                course_id=course_id,
                html=result.html,
                page_url=result.final_url,
                seed_url=result.final_url,
            )
            course_resources.extend(extracted)

            queue: list[tuple[str, str, str]] = []
            for item in sorted(
                set(collections), key=lambda value: (value[0], value[1], value[2])
            ):
                if item[0] != result.final_url:
                    queue.append(item)

            for collection_url, _title, fallback_kind in queue[
                :max_collection_pages
            ]:
                if collection_url in visited_collections:
                    continue
                visited_collections.add(collection_url)
                collection_result = fetcher.fetch_html(collection_url)
                if not collection_result.ok:
                    course_failures.append(
                        {
                            "course_id": course_id,
                            "source_url": collection_url,
                            "reason": collection_result.reason,
                        }
                    )
                    continue
                detail_resources, _ = extract_resources_from_html(
                    course_id=course_id,
                    html=collection_result.html,
                    page_url=collection_result.final_url,
                    seed_url=result.final_url,
                    fallback_kind=fallback_kind,
                )
                course_resources.extend(detail_resources)

        precision_before = len(course_resources)
        course_resources, precision_reasons = filter_course_resources(
            course_resources, course
        )
        precision = checkpoint.setdefault(
            "precision_filter",
            {
                "version": PRECISION_FILTER_VERSION,
                "before_resources": 0,
                "after_resources": 0,
                "removed_resources": 0,
                "removed_by_reason": {},
            },
        )
        precision["before_resources"] += precision_before
        precision["after_resources"] += len(course_resources)
        removed_by_reason = Counter(precision.get("removed_by_reason", {}))
        removed_by_reason.update(precision_reasons)
        precision["removed_by_reason"] = dict(sorted(removed_by_reason.items()))
        precision["removed_resources"] = (
            precision["before_resources"] - precision["after_resources"]
        )

        finalized_course_resources = de_duplicate_and_limit(
            course_resources, max_per_course=max_resources_per_course
        )
        all_resources.extend(finalized_course_resources)
        failures.extend(course_failures)

        completed_course_ids.add(course_id)
        checkpoint["completed_course_ids"] = sorted(completed_course_ids)
        checkpoint["course_resources"][str(course_id)] = (
            finalized_course_resources
        )
        checkpoint["course_failures"][str(course_id)] = course_failures
        checkpoint["fetches"] = {
            "attempted": fetcher.attempted,
            "succeeded": fetcher.succeeded,
            "failed": fetcher.failed,
        }
        if checkpoint_path is not None:
            write_json_atomic(checkpoint_path, checkpoint)

    all_resources = ensure_evidenced_candidate_seeds(
        all_resources, candidates, failures
    )
    resources = ensure_unique_course_titles(
        de_duplicate_and_limit(
            all_resources, max_per_course=max_resources_per_course
        )
    )
    blacklist_matches = precision_blacklist_matches(resources, candidates)
    if blacklist_matches:
        preview = "; ".join(
            f"{item['course_id']}:{item['url']}" for item in blacklist_matches[:5]
        )
        raise ValueError(
            f"precision blacklist matched {len(blacklist_matches)} resources: "
            f"{preview}"
        )
    failures.sort(
        key=lambda item: (
            item["course_id"],
            item["source_url"],
            item["reason"] or "",
        )
    )
    payload = {
        "schema_version": SCHEMA_VERSION,
        "last_verified": VERIFIED_DATE,
        "verification_semantics": (
            "available means the resource was discoverable on a successfully "
            "fetched official source page on the verification date; "
            "review-needed means the seed could not be fetched or an extracted "
            "link leaves the official or trusted educational host."
        ),
        "stats": build_stats(
            candidates=candidates,
            resources=resources,
            failures=failures,
            fetcher=fetcher,
        ),
        "precision_audit": {
            "filter": checkpoint.get("precision_filter", {}),
            "hard_blacklist_matches": 0,
            "title_quality": title_quality_counts(resources),
            "domain_samples": build_domain_samples(resources, candidates),
            "manual_review": build_review_candidates(resources, candidates),
        },
        "resources": resources,
        "failures": failures,
    }
    validate_payload(
        payload,
        candidate_ids={item["id"] for item in candidates},
        candidates=candidates,
    )
    return payload


def validate_payload(
    payload: dict[str, Any],
    *,
    candidate_ids: set[int] | None = None,
    candidates: list[dict[str, Any]] | None = None,
) -> None:
    if payload.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("unsupported resource schema version")
    if payload.get("last_verified") != VERIFIED_DATE:
        raise ValueError("unexpected verification date")
    resources = payload.get("resources")
    if not isinstance(resources, list):
        raise ValueError("resources must be an array")

    required = {
        "course_id",
        "kind",
        "title",
        "url",
        "access",
        "status",
        "last_verified",
        "source_url",
    }
    seen: set[tuple[int, str]] = set()
    previous_sort_key: tuple[Any, ...] | None = None
    for index, resource in enumerate(resources):
        if set(resource) != required:
            raise ValueError(f"resource {index} fields do not match the schema")
        course_id = resource["course_id"]
        if not isinstance(course_id, int):
            raise ValueError(f"resource {index} has a non-integer course_id")
        if candidate_ids is not None and course_id not in candidate_ids:
            raise ValueError(f"resource {index} references an unknown course")
        if resource["kind"] not in KINDS:
            raise ValueError(f"resource {index} has an invalid kind")
        collection_kind = explicit_collection_kind(
            str(resource.get("title", "")),
            str(resource.get("url", "")),
        )
        # Canonical candidate seeds remain course overviews even when the
        # course name/slug itself contains "lab" or "project".
        if (
            collection_kind
            and resource["kind"] != "course"
            and resource["kind"] != collection_kind
        ):
            raise ValueError(
                f"resource {index} violates exact collection kind invariant: "
                f"{resource['kind']} -> {collection_kind}"
            )
        if resource["access"] not in ACCESS_VALUES:
            raise ValueError(f"resource {index} has an invalid access value")
        if resource["status"] not in STATUS_VALUES:
            raise ValueError(f"resource {index} has an invalid status")
        if resource["last_verified"] != VERIFIED_DATE:
            raise ValueError(f"resource {index} has an invalid verification date")
        if not isinstance(resource["title"], str) or not resource["title"].strip():
            raise ValueError(f"resource {index} has an empty title")
        for field in ("url", "source_url"):
            if normalize_url(resource[field]) != resource[field]:
                raise ValueError(
                    f"resource {index} {field} is not canonical HTTPS"
                )
        key = (course_id, resource["url"])
        if key in seen:
            raise ValueError(f"duplicate course resource: {key}")
        seen.add(key)
        sort_key = (
            course_id,
            KIND_ORDER[resource["kind"]],
            resource["title"].casefold(),
            resource["url"],
        )
        if previous_sort_key is not None and sort_key < previous_sort_key:
            raise ValueError("resources are not stably sorted")
        previous_sort_key = sort_key

    failures = payload.get("failures")
    if not isinstance(failures, list):
        raise ValueError("failures must be an array")
    for failure in failures:
        if set(failure) != {"course_id", "source_url", "reason"}:
            raise ValueError("failure fields do not match the schema")
        if normalize_url(failure["source_url"]) != failure["source_url"]:
            raise ValueError("failure source URL is not canonical HTTPS")

    stats = payload.get("stats")
    if not isinstance(stats, dict):
        raise ValueError("stats must be an object")
    if stats.get("total_resources") != len(resources):
        raise ValueError("resource count does not match stats")
    if stats.get("failed_sources") != len(failures):
        raise ValueError("failure count does not match stats")
    title_counts = title_quality_counts(resources)
    if any(title_counts.values()):
        raise ValueError(f"resource title quality failed: {title_counts}")
    recorded_title_counts = (
        payload.get("precision_audit", {}).get("title_quality")
    )
    if recorded_title_counts != title_counts:
        raise ValueError("recorded title quality counts are stale")
    if candidates is not None:
        by_id = {candidate["id"]: candidate for candidate in candidates}
        for index, resource in enumerate(resources):
            candidate = by_id.get(resource["course_id"])
            if candidate is None:
                raise ValueError(f"resource {index} references an unknown course")
            reviewed = dict(resource)
            allowed, reason = resource_relevance(reviewed, candidate)
            if not allowed:
                raise ValueError(
                    f"resource {index} fails precision filter: {reason}"
                )
            if reviewed["kind"] != resource["kind"]:
                raise ValueError(
                    f"resource {index} kind is stale: "
                    f"{resource['kind']} -> {reviewed['kind']}"
                )
        blacklist_matches = precision_blacklist_matches(resources, candidates)
        if blacklist_matches:
            raise ValueError(
                f"hard precision blacklist matched {len(blacklist_matches)} resources"
            )


def validate_checkpoint(
    checkpoint: dict[str, Any], *, candidate_ids: set[int]
) -> None:
    if checkpoint.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("checkpoint schema version does not match")
    if checkpoint.get("last_verified") != VERIFIED_DATE:
        raise ValueError("checkpoint verification date does not match")
    completed = checkpoint.get("completed_course_ids")
    resources = checkpoint.get("course_resources")
    failures = checkpoint.get("course_failures")
    fetches = checkpoint.get("fetches")
    if not isinstance(completed, list) or completed != sorted(set(completed)):
        raise ValueError("checkpoint completed ids are invalid")
    if any(
        not isinstance(course_id, int) or course_id not in candidate_ids
        for course_id in completed
    ):
        raise ValueError("checkpoint references an unknown candidate")
    if not isinstance(resources, dict) or not isinstance(failures, dict):
        raise ValueError("checkpoint course payloads must be objects")
    expected_keys = {str(course_id) for course_id in completed}
    if set(resources) != expected_keys or set(failures) != expected_keys:
        raise ValueError("checkpoint course payloads are incomplete")
    for course_id in completed:
        for resource in resources[str(course_id)]:
            if resource.get("course_id") != course_id:
                raise ValueError("checkpoint resource course id mismatch")
            if resource.get("access") not in ACCESS_VALUES:
                raise ValueError("checkpoint resource access is invalid")
            if resource.get("status") not in STATUS_VALUES:
                raise ValueError("checkpoint resource status is invalid")
    if not isinstance(fetches, dict) or set(fetches) != {
        "attempted",
        "succeeded",
        "failed",
    }:
        raise ValueError("checkpoint fetch stats are invalid")
    if any(not isinstance(value, int) or value < 0 for value in fetches.values()):
        raise ValueError("checkpoint fetch counts must be non-negative integers")


def refilter_existing_payload(
    payload: dict[str, Any],
    candidates: list[dict[str, Any]],
    *,
    max_resources_per_course: int,
) -> dict[str, Any]:
    """Re-apply current precision and kind rules without network requests."""

    by_id = {candidate["id"]: candidate for candidate in candidates}
    original_resources = payload.get("resources", [])
    if not isinstance(original_resources, list):
        raise ValueError("existing payload resources must be an array")
    failures = payload.get("failures", [])
    if not isinstance(failures, list):
        raise ValueError("existing payload failures must be an array")
    filtered: list[dict[str, Any]] = []
    removed_reasons: Counter[str] = Counter()
    for original in original_resources:
        if not isinstance(original, dict):
            continue
        resource = dict(original)
        normalize_resource_title_and_kind(resource)
        candidate = by_id.get(resource.get("course_id"))
        if candidate is None:
            removed_reasons["unknown-course"] += 1
            continue
        allowed, reason = resource_relevance(resource, candidate)
        if allowed:
            filtered.append(resource)
        else:
            removed_reasons[reason] += 1
    filtered = ensure_evidenced_candidate_seeds(
        filtered, candidates, failures
    )
    resources = ensure_unique_course_titles(
        de_duplicate_and_limit(filtered, max_resources_per_course)
    )
    blacklist_matches = precision_blacklist_matches(resources, candidates)
    if blacklist_matches:
        raise ValueError(
            f"hard precision blacklist matched {len(blacklist_matches)} resources"
        )

    fetch_counts = payload.get("stats", {}).get("fetches")
    if not isinstance(fetch_counts, dict):
        raise ValueError("existing payload fetch stats are missing")
    payload["stats"] = build_stats(
        candidates=candidates,
        resources=resources,
        failures=failures,
        fetch_counts={
            key: int(fetch_counts.get(key, 0))
            for key in ("attempted", "succeeded", "failed")
        },
    )
    precision_filter = dict(
        payload.get("precision_audit", {}).get("filter", {})
    )
    precision_filter["final_resources_after_balanced_cap"] = len(resources)
    precision_filter["refilter_input_resources"] = len(original_resources)
    precision_filter["refilter_output_resources"] = len(resources)
    precision_filter["refilter_removed_by_reason"] = dict(
        sorted(removed_reasons.items())
    )
    payload["precision_audit"] = {
        "filter": precision_filter,
        "hard_blacklist_matches": 0,
        "title_quality": title_quality_counts(resources),
        "domain_samples": build_domain_samples(resources, candidates),
        "manual_review": build_review_candidates(resources, candidates),
    }
    payload["resources"] = resources
    validate_payload(
        payload,
        candidate_ids=set(by_id),
        candidates=candidates,
    )
    return payload


def migrate_checkpoint_kinds(checkpoint: dict[str, Any]) -> None:
    """Upgrade in-flight checkpoints without repeating verified requests."""

    replacements = {"syllabus": "course", "reading": "notes"}
    course_resources = checkpoint.get("course_resources", {})
    if not isinstance(course_resources, dict):
        return
    for resources in course_resources.values():
        if not isinstance(resources, list):
            continue
        for resource in resources:
            if isinstance(resource, dict) and resource.get("kind") in replacements:
                resource["kind"] = replacements[resource["kind"]]
            if isinstance(resource, dict):
                for field in ("url", "source_url"):
                    canonical = normalize_url(str(resource.get(field, "")))
                    if canonical:
                        resource[field] = canonical
                if resource.get("status") == "available":
                    host = (urlsplit(str(resource.get("url", ""))).hostname or "").lower()
                    path = urlsplit(str(resource.get("url", ""))).path.lower()
                    if "archive" in host or "/archive" in path:
                        resource["status"] = "archived"
    course_failures = checkpoint.get("course_failures", {})
    if isinstance(course_failures, dict):
        for failures in course_failures.values():
            if not isinstance(failures, list):
                continue
            for failure in failures:
                if not isinstance(failure, dict):
                    continue
                canonical = normalize_url(str(failure.get("source_url", "")))
                if canonical:
                    failure["source_url"] = canonical


def write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(rendered, encoding="utf-8", newline="\n")
    temporary.replace(path)


def write_payload(path: Path, payload: dict[str, Any]) -> None:
    write_json_atomic(path, payload)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT)
    parser.add_argument(
        "--taxonomy",
        type=Path,
        default=ROOT / "data" / "tracks.json",
        help="taxonomy used by catalogue merge mode",
    )
    parser.add_argument(
        "--catalogue",
        type=Path,
        default=ROOT / "data" / "courses.json",
        help="canonical catalogue used by merge mode",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.35,
        help="minimum seconds between requests to the same host",
    )
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--max-collection-pages", type=int, default=8)
    parser.add_argument("--max-resources-per-course", type=int, default=80)
    parser.add_argument(
        "--ignore-robots",
        action="store_true",
        help="disable robots.txt checks (not recommended)",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="validate the existing output without using the network",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="resume completed courses from the checkpoint file",
    )
    parser.add_argument(
        "--keep-checkpoint",
        action="store_true",
        help="retain the checkpoint after a successful final write",
    )
    parser.add_argument(
        "--retry-failed-courses",
        action="store_true",
        help=(
            "when resuming, re-run only checkpointed courses with at least "
            "one failed seed or collection page"
        ),
    )
    merge_group = parser.add_mutually_exclusive_group()
    merge_group.add_argument(
        "--merge-catalogue",
        action="store_true",
        help=(
            "merge the existing manifest into the canonical catalogue while "
            "preserving reviewed overlays"
        ),
    )
    merge_group.add_argument(
        "--check-merge",
        action="store_true",
        help="check that the canonical catalogue matches a deterministic merge",
    )
    merge_group.add_argument(
        "--refilter-output",
        action="store_true",
        help=(
            "re-apply current relevance, kind, title, and blacklist rules to "
            "the existing manifest without using the network"
        ),
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    candidates = load_candidates(args.input)
    if args.refilter_output:
        with args.output.open(encoding="utf-8") as handle:
            payload = json.load(handle)
        payload = refilter_existing_payload(
            payload,
            candidates,
            max_resources_per_course=max(1, args.max_resources_per_course),
        )
        write_payload(args.output, payload)
        print(json.dumps(payload["stats"], ensure_ascii=False, indent=2))
        return 0
    if args.merge_catalogue or args.check_merge:
        with args.output.open(encoding="utf-8") as handle:
            payload = json.load(handle)
        validate_payload(
            payload,
            candidate_ids={item["id"] for item in candidates},
            candidates=candidates,
        )
        from scripts.compile_courses import main as compile_courses_main

        compile_args = [
            "--candidates",
            str(args.input),
            "--taxonomy",
            str(args.taxonomy),
            "--output",
            str(args.catalogue),
            "--resources",
            str(args.output),
        ]
        if args.check_merge:
            compile_args.append("--check")
        return compile_courses_main(compile_args)
    if args.validate_only:
        with args.output.open(encoding="utf-8") as handle:
            payload = json.load(handle)
        validate_payload(
            payload,
            candidate_ids={item["id"] for item in candidates},
            candidates=candidates,
        )
        print(
            f"validated {len(payload['resources'])} resources "
            f"for {payload['stats']['courses_with_any_resource']} courses"
        )
        return 0

    payload = crawl(
        candidates,
        delay=args.delay,
        timeout=args.timeout,
        retries=args.retries,
        max_collection_pages=max(0, args.max_collection_pages),
        max_resources_per_course=max(1, args.max_resources_per_course),
        respect_robots=not args.ignore_robots,
        checkpoint_path=args.checkpoint,
        resume=args.resume,
        retry_failed_courses=args.retry_failed_courses,
    )
    write_payload(args.output, payload)
    if not args.keep_checkpoint and args.checkpoint.exists():
        args.checkpoint.unlink()
    print(json.dumps(payload["stats"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
