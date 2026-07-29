from __future__ import annotations

from pathlib import Path

from scripts.check_forbidden_terms import forbidden_issues
from scripts.check_markdown_links import markdown_link_issues
from scripts.check_navigation import navigation_issues
from scripts.check_translations import translation_issues


ZH_PAGE = """---
title: 示例
description: 一份用于检查的中文示例页面，包含足够说明文字。
---

# 示例

这是一份用于结构检查的中文页面。它解释目标、步骤、证据与结果，并链接到[下一页](child.md#结果)。

## 方法

记录输入、过程与验证结论，使结果可以由另一位学习者复核。
"""

EN_PAGE = """---
title: Example
description: An English example page with enough explanatory context for checks.
---

# Example

This page explains the goal, steps, evidence, and result for structural validation. It links to the [next page](child.md#result).

## Method

Record inputs, process, and verification conclusions so another learner can reproduce the result independently.
"""

ZH_CHILD = """---
title: 结果
description: 中文结果页面，记录验证结果和复现条件。
---

# 结果

这里记录足够详细的中文结果、限制、参数和复现条件，帮助学习者独立检查。记录还应说明输入数据、工具版本、失败尝试、误差来源和验收标准，并给出下一位学习者能够直接执行的复现步骤。
"""

EN_CHILD = """---
title: Result
description: English result page documenting verification and reproduction conditions.
---

# Result

This English result page documents enough parameters, limitations, verification evidence, and reproduction conditions for an independent check.
"""


def _write_pair(docs: Path, relative: str, zh: str, en: str) -> None:
    zh_path = docs / relative
    en_path = docs / "en" / relative
    zh_path.parent.mkdir(parents=True, exist_ok=True)
    en_path.parent.mkdir(parents=True, exist_ok=True)
    zh_path.write_text(zh, encoding="utf-8")
    en_path.write_text(en, encoding="utf-8")


def test_translation_and_internal_link_checks(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    _write_pair(docs, "index.md", ZH_PAGE, EN_PAGE)
    _write_pair(docs, "child.md", ZH_CHILD, EN_CHILD)
    translation_findings, statistics = translation_issues(
        docs, minimum_substantive_guides=0
    )
    link_findings, _ = markdown_link_issues(docs)
    assert translation_findings == []
    assert statistics["pair_coverage_percent"] == 100.0
    assert link_findings == []


def test_missing_translation_and_anchor_are_errors(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "index.md").write_text(
        ZH_PAGE.replace("child.md#结果", "index.md#不存在"),
        encoding="utf-8",
    )
    translation_findings, _ = translation_issues(
        docs, minimum_substantive_guides=0
    )
    link_findings, _ = markdown_link_issues(docs)
    assert any(issue.code == "translation.missing_en" for issue in translation_findings)
    assert any(issue.code == "link.anchor_missing" for issue in link_findings)


def test_navigation_uses_reachability_not_sidebar_enumeration(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    _write_pair(docs, "index.md", ZH_PAGE, EN_PAGE)
    _write_pair(docs, "child.md", ZH_CHILD, EN_CHILD)
    config = tmp_path / "mkdocs.yml"
    config.write_text(
        "docs_dir: docs\n"
        "use_directory_urls: true\n"
        "nav:\n"
        "  - 中文:\n"
        "      - 首页: index.md\n"
        "  - English:\n"
        "      - Home: en/index.md\n",
        encoding="utf-8",
    )
    issues, statistics = navigation_issues(config)
    assert issues == []
    assert statistics["reachability_percent"] == 100.0


def test_navigation_requires_direct_enumeration_when_enabled(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    _write_pair(docs, "index.md", ZH_PAGE, EN_PAGE)
    _write_pair(docs, "child.md", ZH_CHILD, EN_CHILD)
    config = tmp_path / "mkdocs.yml"
    config.write_text(
        "docs_dir: docs\n"
        "use_directory_urls: true\n"
        "extra:\n"
        "  navigation_requires_all_docs: true\n"
        "nav:\n"
        "  - 中文:\n"
        "      - 首页: index.md\n"
        "  - English:\n"
        "      - Home: en/index.md\n",
        encoding="utf-8",
    )
    issues, statistics = navigation_issues(config)
    missing = [issue.path for issue in issues if issue.code == "nav.direct_missing"]
    assert missing == ["child.md", "en/child.md"]
    assert statistics["directly_listed_pages"] == 2
    assert statistics["direct_coverage_percent"] == 50.0
    assert statistics["reachability_percent"] == 100.0


def test_navigation_direct_enumeration_passes_at_full_coverage(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    _write_pair(docs, "index.md", ZH_PAGE, EN_PAGE)
    _write_pair(docs, "child.md", ZH_CHILD, EN_CHILD)
    config = tmp_path / "mkdocs.yml"
    config.write_text(
        "docs_dir: docs\n"
        "extra:\n"
        "  navigation_requires_all_docs: true\n"
        "nav:\n"
        "  - 中文:\n"
        "      - 首页: index.md\n"
        "      - 子页: child.md\n"
        "  - English:\n"
        "      - Home: en/index.md\n"
        "      - Child: en/child.md\n",
        encoding="utf-8",
    )
    issues, statistics = navigation_issues(config)
    assert issues == []
    assert statistics["direct_coverage_percent"] == 100.0


def test_forbidden_scanner_reports_custom_pattern(tmp_path: Path) -> None:
    path = tmp_path / "page.md"
    path.write_text("A deliberately unfinished marker appears here.", encoding="utf-8")
    issues = forbidden_issues(
        tmp_path,
        denied_terms=(("unfinished", "unfinished marker"),),
    )
    assert len(issues) == 1
    assert issues[0].line == 1


def test_forbidden_scanner_allows_honest_upstream_attribution(
    tmp_path: Path,
) -> None:
    path = tmp_path / "NOTICE.md"
    path.write_text(
        "Template lineage: CSDIY / PKUFlyingPig/cs-self-learning.\n",
        encoding="utf-8",
    )

    assert forbidden_issues(tmp_path) == []


def test_forbidden_scanner_prunes_generated_directories(tmp_path: Path) -> None:
    generated = tmp_path / "build" / "nested"
    generated.mkdir(parents=True)
    (generated / "page.md").write_text("unfinished marker", encoding="utf-8")

    assert (
        forbidden_issues(
            tmp_path,
            denied_terms=(("unfinished", "unfinished marker"),),
        )
        == []
    )
