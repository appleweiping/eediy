from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.doc_links import resolve_internal_target
from scripts.quality_common import (
    Issue,
    emit_issues,
    exit_code,
    is_external_url,
    iter_markdown_links,
    markdown_files,
    markdown_anchors,
    repo_path,
    write_json_report,
)


def markdown_link_issues(
    docs_root: Path,
    *,
    directory_urls: bool = True,
) -> tuple[list[Issue], dict[str, Any]]:
    issues: list[Issue] = []
    counts: Counter[str] = Counter()
    external_urls: set[str] = set()
    anchors_by_path: dict[Path, set[str]] = {}
    for path in markdown_files(docs_root):
        text = path.read_text(encoding="utf-8")
        anchors_by_path[path.resolve()] = markdown_anchors(text)
    for path in markdown_files(docs_root):
        relative = path.relative_to(docs_root).as_posix()
        text = path.read_text(encoding="utf-8")
        for target, line in iter_markdown_links(text):
            counts["total"] += 1
            if is_external_url(target):
                counts["external"] += 1
                external_urls.add(target)
                continue
            resolved = resolve_internal_target(
                path, target, docs_root, directory_urls=directory_urls
            )
            counts[resolved.kind] += 1
            if resolved.kind in {"ignored", "external"}:
                continue
            if resolved.kind != "internal":
                issues.append(
                    Issue(
                        "error",
                        f"link.{resolved.kind}",
                        f"{resolved.message}: {target}",
                        relative,
                        line,
                    )
                )
                continue
            if (
                resolved.fragment
                and resolved.path is not None
                and resolved.path.suffix.lower() == ".md"
                and resolved.fragment not in anchors_by_path.get(resolved.path.resolve(), set())
            ):
                issues.append(
                    Issue(
                        "error",
                        "link.anchor_missing",
                        f"anchor #{resolved.fragment} does not exist in "
                        f"{resolved.path.relative_to(docs_root).as_posix()}",
                        relative,
                        line,
                    )
                )
    statistics = {
        "markdown_files": len(markdown_files(docs_root)),
        "links_total": counts["total"],
        "links_internal": counts["internal"],
        "links_external": counts["external"],
        "unique_external_urls": len(external_urls),
        "external_urls": sorted(external_urls),
    }
    return list(dict.fromkeys(issues)), statistics


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate relative documentation links, assets, and heading anchors."
    )
    parser.add_argument("--docs-root", default="docs")
    parser.add_argument("--no-directory-urls", action="store_true")
    parser.add_argument("--json-report")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    issues, statistics = markdown_link_issues(
        repo_path(args.docs_root), directory_urls=not args.no_directory_urls
    )
    emit_issues(issues)
    print(
        f"Markdown links: {statistics['links_total']} checked, "
        f"{statistics['links_internal']} internal, {statistics['links_external']} external"
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
