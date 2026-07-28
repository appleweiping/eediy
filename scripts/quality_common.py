from __future__ import annotations

import fnmatch
import hashlib
import json
import os
import re
import sys
import tempfile
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping, Sequence
from urllib.parse import unquote, urlsplit


REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = REPO_ROOT / "docs"
DATA_ROOT = REPO_ROOT / "data"
BUILD_ROOT = REPO_ROOT / "build"

MARKDOWN_LINK_RE = re.compile(
    r"!?\[[^\]]*]\(\s*(?:<([^>]+)>|([^\s)]+))(?:\s+[\"'][^\"']*[\"'])?\s*\)"
)
REFERENCE_LINK_RE = re.compile(r"^\s{0,3}\[[^\]]+]:\s*(?:<([^>]+)>|(\S+))", re.MULTILINE)
HTML_LINK_RE = re.compile(r"\b(?:href|src)\s*=\s*[\"']([^\"']+)[\"']", re.IGNORECASE)
HTML_ID_RE = re.compile(r"\bid\s*=\s*[\"']([^\"']+)[\"']", re.IGNORECASE)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$", re.MULTILINE)
EXPLICIT_ANCHOR_RE = re.compile(r"\{\s*#([A-Za-z][\w:.-]*)\s*\}\s*$")
FENCE_RE = re.compile(r"^\s*(```+|~~~+)", re.MULTILINE)
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


@dataclass(frozen=True)
class Issue:
    severity: str
    code: str
    message: str
    path: str = ""
    line: int | None = None
    context: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class QualityError(RuntimeError):
    """Raised when a quality input cannot be parsed safely."""


def repo_path(value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else REPO_ROOT / path


def display_path(path: str | Path, root: Path = REPO_ROOT) -> str:
    candidate = Path(path)
    try:
        return candidate.resolve().relative_to(root.resolve()).as_posix()
    except (OSError, ValueError):
        return candidate.as_posix()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise QualityError(f"{display_path(path)} is not valid UTF-8") from exc


def load_json(path: Path) -> Any:
    try:
        return json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        raise QualityError(
            f"{display_path(path)}:{exc.lineno}:{exc.colno}: invalid JSON: {exc.msg}"
        ) from exc


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=False) + "\n"


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        newline="\n",
        dir=path.parent,
        delete=False,
    ) as handle:
        handle.write(content)
        temporary = Path(handle.name)
    os.replace(temporary, path)


def sha256_text(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def slugify(value: str, fallback: str = "item") -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", normalized.lower()).strip("-")
    return slug or fallback


def localized(zh: str, en: str) -> dict[str, str]:
    return {"zh": zh.strip(), "en": en.strip()}


def localized_list(zh: Sequence[str], en: Sequence[str]) -> dict[str, list[str]]:
    return {
        "zh": [item.strip() for item in zh if item.strip()],
        "en": [item.strip() for item in en if item.strip()],
    }


def strip_code_blocks(markdown: str) -> str:
    output: list[str] = []
    fence: str | None = None
    for line in markdown.splitlines(keepends=True):
        match = re.match(r"^\s*(```+|~~~+)", line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker[0]
            elif marker[0] == fence:
                fence = None
            output.append("\n")
        elif fence is None:
            output.append(line)
        else:
            output.append("\n")
    return "".join(output)


def iter_markdown_links(markdown: str) -> Iterator[tuple[str, int]]:
    visible = strip_code_blocks(markdown)
    matches: list[tuple[int, str]] = []
    for pattern in (MARKDOWN_LINK_RE, REFERENCE_LINK_RE):
        for match in pattern.finditer(visible):
            target = next((group for group in match.groups() if group is not None), "")
            matches.append((match.start(), target))
    for match in HTML_LINK_RE.finditer(visible):
        matches.append((match.start(), match.group(1)))
    for offset, target in sorted(matches):
        yield target.strip(), visible.count("\n", 0, offset) + 1


def is_external_url(target: str) -> bool:
    return urlsplit(target).scheme.lower() in {"http", "https"}


def split_front_matter(markdown: str) -> tuple[dict[str, Any], str]:
    if not markdown.startswith("---\n"):
        return {}, markdown
    end = markdown.find("\n---\n", 4)
    if end < 0:
        raise QualityError("unterminated YAML front matter")
    raw = markdown[4:end]
    try:
        import yaml

        value = yaml.safe_load(raw) or {}
    except Exception as exc:  # pragma: no cover - dependency-specific error shape
        raise QualityError(f"invalid YAML front matter: {exc}") from exc
    if not isinstance(value, dict):
        raise QualityError("YAML front matter must be a mapping")
    return value, markdown[end + 5 :]


def markdown_headings(markdown: str) -> list[tuple[int, str, str]]:
    visible = strip_code_blocks(markdown)
    anchors_seen: dict[str, int] = {}
    headings: list[tuple[int, str, str]] = []
    for match in HEADING_RE.finditer(visible):
        level = len(match.group(1))
        raw = match.group(2).strip()
        explicit = EXPLICIT_ANCHOR_RE.search(raw)
        if explicit:
            anchor = explicit.group(1)
            title = raw[: explicit.start()].rstrip()
        else:
            title = re.sub(r"[`*_~]", "", raw)
            anchor = heading_slug(title)
        count = anchors_seen.get(anchor, 0)
        anchors_seen[anchor] = count + 1
        if count:
            anchor = f"{anchor}_{count}"
        headings.append((level, title, anchor))
    return headings


def markdown_anchors(markdown: str) -> set[str]:
    visible = strip_code_blocks(markdown)
    anchors = {anchor for _, _, anchor in markdown_headings(visible)}
    anchors.update(match.group(1) for match in HTML_ID_RE.finditer(visible))
    return anchors


def heading_slug(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).strip().lower()
    value = re.sub(r"[^\w\u4e00-\u9fff -]", "", value, flags=re.UNICODE)
    value = re.sub(r"[\s-]+", "-", value).strip("-")
    return value


def markdown_files(docs_root: Path = DOCS_ROOT) -> list[Path]:
    if not docs_root.exists():
        return []
    return sorted(path for path in docs_root.rglob("*.md") if path.is_file())


def line_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def matches_any(path: str, patterns: Iterable[str]) -> bool:
    normalized = path.replace("\\", "/")
    return any(fnmatch.fnmatch(normalized, pattern) for pattern in patterns)


def emit_issues(issues: Sequence[Issue], *, stream: Any = sys.stderr) -> None:
    for issue in sorted(
        issues,
        key=lambda item: (
            item.severity,
            item.code,
            item.path,
            item.line if item.line is not None else -1,
            item.message,
        ),
    ):
        location = issue.path
        if issue.line is not None:
            location = f"{location}:{issue.line}" if location else f"line {issue.line}"
        prefix = f"{location}: " if location else ""
        print(f"{prefix}{issue.severity.upper()} [{issue.code}] {issue.message}", file=stream)
        if os.environ.get("GITHUB_ACTIONS") == "true":
            command = "warning" if issue.severity == "warning" else "error"
            properties = []
            if issue.path:
                properties.append(f"file={issue.path}")
            if issue.line is not None:
                properties.append(f"line={issue.line}")
            prop_text = ",".join(properties)
            print(f"::{command} {prop_text}::{issue.code}: {issue.message}", file=stream)


def exit_code(issues: Sequence[Issue], *, warnings_as_errors: bool = False) -> int:
    failing = {"error"}
    if warnings_as_errors:
        failing.add("warning")
    return 1 if any(issue.severity in failing for issue in issues) else 0


def write_json_report(path: Path | None, payload: Mapping[str, Any]) -> None:
    if path is not None:
        atomic_write(path, stable_json(payload))


def ensure_within(path: Path, parent: Path) -> Path:
    resolved = path.resolve()
    root = parent.resolve()
    if resolved != root and root not in resolved.parents:
        raise QualityError(f"refusing path outside {display_path(parent)}: {resolved}")
    return resolved


def url_without_fragment(target: str) -> tuple[str, str]:
    parsed = urlsplit(target)
    base = parsed._replace(fragment="").geturl()
    return unquote(base), unquote(parsed.fragment)
