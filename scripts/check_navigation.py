from __future__ import annotations

import argparse
import sys
from collections import Counter, deque
from pathlib import Path
from typing import Any, Iterable, Mapping

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.doc_links import markdown_neighbors, resolve_internal_target
from scripts.quality_common import (
    Issue,
    QualityError,
    emit_issues,
    exit_code,
    iter_markdown_links,
    markdown_files,
    matches_any,
    repo_path,
    write_json_report,
)


def _load_yaml(path: Path) -> Mapping[str, Any]:
    try:
        import yaml
    except ImportError as exc:
        raise QualityError("PyYAML is required; install requirements-dev.txt") from exc
    class MkDocsLoader(yaml.SafeLoader):
        pass

    def construct_env(loader: Any, node: Any) -> Any:
        import os

        if isinstance(node, yaml.SequenceNode):
            values = loader.construct_sequence(node)
            if not values:
                return None
            for name in values[:-1]:
                if isinstance(name, str) and name in os.environ:
                    return os.environ[name]
            return values[-1]
        name = loader.construct_scalar(node)
        return os.environ.get(name, "")

    MkDocsLoader.add_constructor("!ENV", construct_env)
    try:
        value = yaml.load(path.read_text(encoding="utf-8"), Loader=MkDocsLoader)
    except Exception as exc:
        raise QualityError(f"invalid YAML in {path.as_posix()}: {exc}") from exc
    if not isinstance(value, Mapping):
        raise QualityError("mkdocs.yml must contain a mapping")
    return value


def nav_targets(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from nav_targets(item)
    elif isinstance(value, Mapping):
        for item in value.values():
            yield from nav_targets(item)


def _excluded_patterns(config: Mapping[str, Any]) -> list[str]:
    raw = config.get("exclude_docs", "")
    if isinstance(raw, str):
        return [line.strip() for line in raw.splitlines() if line.strip()]
    if isinstance(raw, list):
        return [str(item) for item in raw]
    return []


def navigation_issues(
    config_path: Path,
    *,
    check_reachability: bool = True,
) -> tuple[list[Issue], dict[str, Any]]:
    issues: list[Issue] = []
    try:
        config = _load_yaml(config_path)
    except (OSError, UnicodeDecodeError, QualityError) as exc:
        return [Issue("error", "nav.config", str(exc), config_path.as_posix())], {}
    docs_root = (
        config_path.parent / str(config.get("docs_dir", "docs"))
    ).resolve()
    directory_urls = bool(config.get("use_directory_urls", True))
    nav = config.get("nav")
    if not isinstance(nav, list) or not nav:
        return [Issue("error", "nav.missing", "mkdocs nav must be a non-empty list")], {}
    raw_targets = list(nav_targets(nav))
    path_targets = [
        target
        for target in raw_targets
        if not target.startswith(("http://", "https://"))
    ]
    duplicates = [
        target for target, count in Counter(path_targets).items() if count > 1
    ]
    for target in duplicates:
        issues.append(
            Issue("error", "nav.duplicate", f"navigation target appears more than once: {target}")
        )
    seeds: set[Path] = set()
    synthetic_source = docs_root / "index.md"
    for target in path_targets:
        resolved = resolve_internal_target(
            synthetic_source,
            "/" + target.lstrip("/"),
            docs_root,
            directory_urls=directory_urls,
        )
        if resolved.kind != "internal" or resolved.path is None:
            issues.append(
                Issue(
                    "error",
                    "nav.target",
                    f"{resolved.message or 'invalid target'}: {target}",
                    config_path.name,
                )
            )
        elif resolved.path.suffix.lower() != ".md":
            issues.append(
                Issue("error", "nav.not_markdown", f"nav target is not Markdown: {target}")
            )
        else:
            seeds.add(resolved.path.resolve())
    all_docs = {path.resolve() for path in markdown_files(docs_root)}
    reachable = set(seeds)
    if check_reachability:
        queue = deque(seeds)
        while queue:
            page = queue.popleft()
            try:
                text = page.read_text(encoding="utf-8")
            except OSError:
                continue
            neighbors = markdown_neighbors(
                page,
                (target for target, _ in iter_markdown_links(text)),
                docs_root,
                directory_urls=directory_urls,
            )
            for neighbor in neighbors:
                if neighbor not in reachable:
                    reachable.add(neighbor)
                    queue.append(neighbor)
        excluded = _excluded_patterns(config)
        for orphan in sorted(all_docs - reachable):
            relative = orphan.relative_to(docs_root).as_posix()
            if matches_any(relative, excluded):
                continue
            issues.append(
                Issue(
                    "error",
                    "nav.orphan",
                    "page is not reachable from any navigation entry",
                    relative,
                )
            )
    statistics = {
        "nav_targets": len(path_targets),
        "markdown_pages": len(all_docs),
        "reachable_pages": len(reachable),
        "reachability_percent": (
            round(len(reachable) * 100 / len(all_docs), 2) if all_docs else 100.0
        ),
    }
    return list(dict.fromkeys(issues)), statistics


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate MkDocs navigation targets, duplicates, and graph reachability."
    )
    parser.add_argument("--config", default="mkdocs.yml")
    parser.add_argument("--no-reachability", action="store_true")
    parser.add_argument("--json-report")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    issues, statistics = navigation_issues(
        repo_path(args.config), check_reachability=not args.no_reachability
    )
    emit_issues(issues)
    print(
        f"Navigation: {statistics.get('nav_targets', 0)} targets, "
        f"{statistics.get('reachability_percent', 0):.2f}% reachable"
    )
    write_json_report(
        repo_path(args.json_report) if args.json_report else None,
        {
            "ok": exit_code(issues) == 0,
            "statistics": statistics,
            "issues": [issue.to_dict() for issue in issues],
        },
    )
    return exit_code(issues)


if __name__ == "__main__":
    raise SystemExit(main())
