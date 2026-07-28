from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote, urlsplit

from scripts.quality_common import ensure_within


IGNORED_SCHEMES = {"mailto", "tel"}
UNSAFE_SCHEMES = {"javascript", "data", "vbscript", "file"}


@lru_cache(maxsize=4096)
def _directory_names(path: str, modified_ns: int) -> frozenset[str]:
    del modified_ns
    with os.scandir(path) as entries:
        return frozenset(entry.name for entry in entries)


@dataclass(frozen=True)
class ResolvedTarget:
    kind: str
    path: Path | None = None
    fragment: str = ""
    message: str = ""


def _candidate_paths(path: Path, *, directory_urls: bool = True) -> list[Path]:
    candidates = [path]
    suffix = path.suffix.lower()
    if suffix in {".htm", ".html"}:
        candidates.append(path.with_suffix(".md"))
        candidates.append(path.with_suffix("") / "index.md")
    elif not suffix:
        candidates.append(path.with_suffix(".md"))
        if directory_urls:
            candidates.append(path / "index.md")
    elif suffix == "/":
        candidates.append(path / "index.md")
    if path.is_dir():
        candidates.append(path / "index.md")
    return list(dict.fromkeys(candidates))


def _case_exact(candidate: Path, docs_root: Path) -> bool:
    try:
        root = Path(os.path.abspath(docs_root))
        relative = Path(os.path.abspath(candidate)).relative_to(root)
    except (OSError, ValueError):
        return False
    current = root
    for part in relative.parts:
        try:
            names = _directory_names(
                os.fspath(current),
                current.stat().st_mtime_ns,
            )
        except OSError:
            return False
        if part not in names:
            return False
        current /= part
    return True


def resolve_internal_target(
    source: Path,
    target: str,
    docs_root: Path,
    *,
    directory_urls: bool = True,
) -> ResolvedTarget:
    target = target.strip()
    if not target:
        return ResolvedTarget("invalid", message="empty link target")
    parsed = urlsplit(target)
    scheme = parsed.scheme.lower()
    if scheme in {"http", "https"}:
        return ResolvedTarget("external")
    if scheme in IGNORED_SCHEMES:
        return ResolvedTarget("ignored")
    if scheme in UNSAFE_SCHEMES:
        return ResolvedTarget("unsafe", message=f"unsafe URL scheme: {scheme}")
    if scheme:
        return ResolvedTarget("invalid", message=f"unsupported URL scheme: {scheme}")
    raw_path = unquote(parsed.path)
    fragment = unquote(parsed.fragment)
    if "\\" in raw_path:
        return ResolvedTarget("invalid", message="use forward slashes in documentation links")
    if raw_path.startswith("/"):
        candidate = docs_root / raw_path.lstrip("/")
    elif raw_path:
        candidate = source.parent / raw_path
    else:
        candidate = source
    try:
        ensure_within(candidate, docs_root)
    except Exception:
        return ResolvedTarget("outside", message="link escapes docs_dir")
    for possible in _candidate_paths(candidate, directory_urls=directory_urls):
        if possible.is_file():
            if not _case_exact(possible, docs_root):
                return ResolvedTarget(
                    "case_mismatch",
                    path=possible,
                    fragment=fragment,
                    message="link path case does not match the file on disk",
                )
            return ResolvedTarget("internal", possible, fragment)
    return ResolvedTarget("missing", candidate, fragment, "target does not exist")


def markdown_neighbors(
    source: Path,
    targets: Iterable[str],
    docs_root: Path,
    *,
    directory_urls: bool = True,
) -> set[Path]:
    output: set[Path] = set()
    for target in targets:
        resolved = resolve_internal_target(
            source, target, docs_root, directory_urls=directory_urls
        )
        if (
            resolved.kind == "internal"
            and resolved.path is not None
            and resolved.path.suffix.lower() == ".md"
        ):
            output.add(resolved.path.resolve())
    return output
