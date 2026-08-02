from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.nav import Navigation
from mkdocs.structure.pages import Page


def _is_english_location(location: str) -> bool:
    normalized = location.lstrip("/")
    return normalized == "en" or normalized.startswith("en/")


def on_page_context(
    context: dict[str, Any],
    *,
    page: Page,
    config: MkDocsConfig,
    nav: Navigation,
) -> dict[str, Any]:
    """Render Material's built-in interface strings in the page language."""

    del nav
    source = page.file.src_uri.replace("\\", "/")
    config.theme["language"] = "en" if _is_english_location(source) else "zh"
    return context


def _scoped_search_index(
    payload: Mapping[str, Any],
    *,
    language: str,
) -> dict[str, Any]:
    docs = payload.get("docs")
    config = payload.get("config")
    if not isinstance(docs, list) or not isinstance(config, Mapping):
        raise ValueError("Material search index must contain config{} and docs[]")
    if language not in {"zh", "en"}:
        raise ValueError(f"unsupported search language: {language}")

    scoped_docs = []
    for document in docs:
        if not isinstance(document, Mapping):
            raise ValueError("every Material search document must be an object")
        location = document.get("location")
        if not isinstance(location, str):
            raise ValueError("every Material search document needs a string location")
        is_english = _is_english_location(location)
        if is_english == (language == "en"):
            scoped_docs.append(dict(document))

    scoped_config = dict(config)
    scoped_config["lang"] = [language]
    return {
        "config": scoped_config,
        "docs": scoped_docs,
    }


def on_post_build(*, config: MkDocsConfig) -> None:
    """Write language-scoped indexes before the built site is published."""

    search_root = Path(config.site_dir) / "search"
    source_path = search_root / "search_index.json"
    payload = json.loads(source_path.read_text(encoding="utf-8"))
    if not isinstance(payload, Mapping):
        raise ValueError("Material search index root must be an object")

    combined_docs = payload.get("docs")
    if not isinstance(combined_docs, list):
        raise ValueError("Material search index must contain docs[]")

    scoped = {
        language: _scoped_search_index(payload, language=language)
        for language in ("zh", "en")
    }
    if any(not value["docs"] for value in scoped.values()):
        raise ValueError("both Chinese and English search indexes must be non-empty")
    if sum(len(value["docs"]) for value in scoped.values()) != len(combined_docs):
        raise ValueError("language-scoped search indexes must partition the full index")

    for language, value in scoped.items():
        destination = search_root / f"search_index.{language}.json"
        destination.write_text(
            json.dumps(
                value,
                ensure_ascii=False,
                separators=(",", ":"),
            ),
            encoding="utf-8",
        )
