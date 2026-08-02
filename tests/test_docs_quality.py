from __future__ import annotations

import difflib
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path
from urllib.parse import urljoin

from mkdocs.commands.build import build
from mkdocs.config import load_config

from scripts.check_forbidden_terms import forbidden_issues
from scripts.check_markdown_links import markdown_link_issues
from scripts.check_navigation import navigation_issues
from scripts.check_translations import translation_issues
from scripts.quality_common import markdown_headings


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

GUIDE_TEMPLATE_HEADINGS = {
    "目的与学习成果",
    "最小环境",
    "学习顺序",
    "验证任务",
    "常见失败与排查",
    "可复现证据",
    "成本、许可与无障碍",
    "安全边界",
    "完成清单",
    "Purpose and learning outcomes",
    "Minimum environment",
    "Learning sequence",
    "Verification task",
    "Common failures and debugging",
    "Reproducible evidence",
    "Cost, licensing, and accessibility",
    "Safety boundary",
    "Completion checklist",
}
EXTERNAL_URL_RE = re.compile(r"https://[^)\s>]+")
PRACTICE_PARAGRAPH_MINIMUM = {"zh": 120, "en": 70}
PRACTICE_FUZZY_THRESHOLD = 0.90


def _write_pair(docs: Path, relative: str, zh: str, en: str) -> None:
    zh_path = docs / relative
    en_path = docs / "en" / relative
    zh_path.parent.mkdir(parents=True, exist_ok=True)
    en_path.parent.mkdir(parents=True, exist_ok=True)
    zh_path.write_text(zh, encoding="utf-8")
    en_path.write_text(en, encoding="utf-8")


def _practice_paragraphs(text: str, language: str) -> list[str]:
    if text.startswith("---"):
        _opening, _separator, text = text.partition("\n---\n")
    paragraphs: list[str] = []
    for block in re.split(r"\n[ \t]*\n", text):
        lines = [
            line.strip()
            for line in block.splitlines()
            if line.strip()
            and not line.lstrip().startswith(("#", "|", "```", "~~~", "<"))
        ]
        if not lines or all(re.match(r"^(?:[-*+]|\d+[.)])\s+", line) for line in lines):
            continue
        visible = " ".join(lines)
        visible = re.sub(r"!?\[([^\]]+)]\([^)]+\)", r"\1", visible)
        visible = re.sub(r"`([^`]+)`", r"\1", visible)
        visible = re.sub(r"[*_~]", "", visible)
        units = (
            len(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]", visible))
            if language == "zh"
            else len(re.findall(r"\b[A-Za-z][A-Za-z0-9'-]*\b", visible))
        )
        if units < PRACTICE_PARAGRAPH_MINIMUM[language]:
            continue
        normalized = unicodedata.normalize("NFKC", visible).casefold()
        normalized = re.sub(r"https://\S+", " URL ", normalized)
        normalized = re.sub(r"\b\d+(?:\.\d+)?\b", " NUMBER ", normalized)
        normalized = re.sub(r"[^\w\u3400-\u4dbf\u4e00-\u9fff]+", " ", normalized)
        paragraphs.append(re.sub(r"\s+", " ", normalized).strip())
    return paragraphs


def test_translation_and_internal_link_checks(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    _write_pair(docs, "index.md", ZH_PAGE, EN_PAGE)
    _write_pair(docs, "child.md", ZH_CHILD, EN_CHILD)
    translation_findings, statistics = translation_issues(docs)
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
    translation_findings, _ = translation_issues(docs)
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


def test_editorial_notes_state_the_learner_evidence_gap_honestly() -> None:
    root = Path(__file__).resolve().parents[1]
    zh = (root / "docs" / "postscript.md").read_text(encoding="utf-8")
    en = (root / "docs" / "en" / "postscript.md").read_text(encoding="utf-8")
    guide_data = json.loads(
        (root / "data" / "course_guides.json").read_text(encoding="utf-8")
    )
    reviewed_guides = [
        guide for guide in guide_data["guides"] if guide.get("learner_reviews")
    ]

    assert "title: 编辑说明" in zh
    assert "# 编辑说明" in zh
    assert "title: Editorial Notes" in en
    assert "# Editorial Notes" in en
    assert [guide["course_id"] for guide in reviewed_guides] == [21, 42]
    guide_by_course = {guide["course_id"]: guide for guide in reviewed_guides}
    assert guide_by_course[21]["editorial_status"] == "learner-reviewed"
    assert guide_by_course[21]["learner_reviews"][0]["relationship"] == (
        "same-course-other-run"
    )
    assert guide_by_course[42]["editorial_status"] == "researched"
    assert guide_by_course[42]["learner_reviews"][0]["relationship"] == (
        "successor-course"
    )
    assert "有一份公开署名复盘达到 `learner-reviewed` 门槛" in zh
    assert "只有 6.002 导读标为 `learner-reviewed`" in zh
    assert "Spring 2007 的实体 labs" in zh
    assert "Spring 2006 labs" in zh
    assert "one public, attributable account meets the site's" in en
    assert "Only the 6.002 guide is therefore labeled `learner-reviewed`" in en
    assert "Spring 2007 physical labs" in en
    assert "Spring 2006 labs" in en


def test_support_pages_keep_actionable_editorial_corrections() -> None:
    root = Path(__file__).resolve().parents[1]

    zh_books = (root / "docs" / "books.md").read_text(encoding="utf-8")
    en_books = (root / "docs" / "en" / "books.md").read_text(encoding="utf-8")
    assert "**18.03/6.003 + 18.06**" in zh_books
    assert "**18.03/6.003 plus 18.06**" in en_books
    assert "VMLS/概率基础 → DSP Guide" not in zh_books
    assert "VMLS/probability foundations → DSP Guide" not in en_books
    assert "四周后" not in zh_books
    assert "four weeks" not in en_books.casefold()

    zh_projects = (root / "docs" / "guides" / "projects.md").read_text(
        encoding="utf-8"
    )
    en_projects = (root / "docs" / "en" / "guides" / "projects.md").read_text(
        encoding="utf-8"
    )
    assert "一个两周的低压小系统" not in zh_projects
    assert "a two-week low-voltage system" not in en_projects.casefold()

    zh_tools = (root / "docs" / "guides" / "tools.md").read_text(
        encoding="utf-8"
    )
    en_tools = (root / "docs" / "en" / "guides" / "tools.md").read_text(
        encoding="utf-8"
    )
    zh_writing = (root / "docs" / "guides" / "technical-writing.md").read_text(
        encoding="utf-8"
    )
    en_writing = (
        root / "docs" / "en" / "guides" / "technical-writing.md"
    ).read_text(encoding="utf-8")
    assert "二进制工程文件之外" not in zh_tools
    assert "alongside a binary pcb project" not in en_tools.casefold()
    assert "二进制 schematic/PCB 文件" not in zh_writing
    assert "native binary schematic or pcb files" not in en_writing.casefold()


def test_curated_resource_pages_publish_review_dates_and_example_links() -> None:
    root = Path(__file__).resolve().parents[1]
    reviewed_pairs = (
        ("docs/books.md", "docs/en/books.md", "2026-08-02"),
        ("docs/math-foundations.md", "docs/en/math-foundations.md", "2026-07-31"),
        ("docs/math-advanced.md", "docs/en/math-advanced.md", "2026-07-31"),
        ("docs/guides/tools.md", "docs/en/guides/tools.md", "2026-07-31"),
    )
    for zh_relative, en_relative, reviewed_at in reviewed_pairs:
        zh = (root / zh_relative).read_text(encoding="utf-8")
        en = (root / en_relative).read_text(encoding="utf-8")
        assert f"last_reviewed: {reviewed_at}" in zh
        assert f"last_reviewed: {reviewed_at}" in en

    starter_url = (
        "https://github.com/appleweiping/eediy/tree/main/examples/rc-lowpass"
    )
    for relative in (
        "docs/guides/version-control.md",
        "docs/en/guides/version-control.md",
        "docs/guides/instrumentation-measurement.md",
        "docs/en/guides/instrumentation-measurement.md",
    ):
        assert starter_url in (root / relative).read_text(encoding="utf-8")


def test_project_guide_indexes_every_release_checked_executable_starter() -> None:
    root = Path(__file__).resolve().parents[1]
    pages = (
        (root / "docs" / "guides" / "projects.md").read_text(encoding="utf-8"),
        (root / "docs" / "en" / "guides" / "projects.md").read_text(
            encoding="utf-8"
        ),
    )
    starters = (
        "rc-lowpass",
        "ring-buffer",
        "sensor-sampler",
        "sync-fifo",
        "tmp117-kicad",
    )
    commands = (
        "python examples/rc-lowpass/run.py",
        "cmake --workflow --preset host-sanitized",
        "python examples/sync-fifo/run_checks.py --require-tools all",
        "python examples/tmp117-kicad/export.py --require-kicad",
    )

    for page in pages:
        for starter in starters:
            assert (
                "https://github.com/appleweiping/eediy/tree/main/examples/"
                f"{starter}"
            ) in page
        for command in commands:
            assert command in page


def test_course_starter_mentions_stay_editorial_instead_of_becoming_readmes() -> None:
    root = Path(__file__).resolve().parents[1]
    course_starters = {
        "016": "ring-buffer",
        "021": "rc-lowpass",
        "037": "sync-fifo",
        "055": "tmp117-kicad",
        "057": "sensor-sampler",
    }
    command_or_matrix = re.compile(
        r"(?:`|cmake|run_checks|--require|asan|ubsan|ctest|symbiyosys|"
        r"iverilog|verilator|sha256sums)",
        re.IGNORECASE,
    )

    for course_id, starter in course_starters.items():
        for language in ("zh", "en"):
            text = (
                root / "content" / "course-guides" / f"{course_id}.{language}.md"
            ).read_text(encoding="utf-8")
            paragraphs = [
                paragraph
                for paragraph in re.split(r"\n\s*\n", text)
                if f"/examples/{starter}" in paragraph
            ]
            assert len(paragraphs) == 1, (course_id, language, starter)
            paragraph = paragraphs[0]
            prose = re.sub(r"\]\([^)]+\)", "]", paragraph)
            sentence_count = len(
                re.findall(r"(?:[.!?。！？])(?:\s|$)", prose)
            )
            assert sentence_count <= 2, (
                course_id,
                language,
                "starter context belongs in at most two editorial sentences",
            )
            assert command_or_matrix.search(paragraph) is None, (
                course_id,
                language,
                "commands and tool-result matrices belong in the starter README",
            )


def test_contribution_pages_offer_direct_action_paths() -> None:
    root = Path(__file__).resolve().parents[1]
    pages = (
        (root / "docs" / "contributing.md").read_text(encoding="utf-8"),
        (root / "docs" / "en" / "contributing.md").read_text(encoding="utf-8"),
    )
    required = (
        "https://github.com/appleweiping/eediy/issues/new?template=broken-link.yml",
        "https://github.com/appleweiping/eediy/issues/new?template=content-error.yml",
        "https://github.com/appleweiping/eediy/issues/new?template=course.yml",
        "https://github.com/appleweiping/eediy/discussions",
        "https://github.com/appleweiping/eediy/compare",
        "https://github.com/appleweiping/eediy/blob/main/CONTRIBUTING.md",
        "https://github.com/appleweiping/eediy/blob/main/data/course_candidates.json",
    )
    for page in pages:
        for url in required:
            assert url in page
        assert "python -m mkdocs serve" in page
        assert "python scripts/run_quality.py" in page


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


def test_published_license_pages_include_pinned_third_party_notices() -> None:
    root = Path(__file__).resolve().parents[1]
    required = (
        "Copyright © <2021> <copyright Yinmin Zhong>",
        "Copyright (c) 2016-2025 Martin Donath <martin.donath@squidfunk.com>",
        "Material for MkDocs 9.7.7",
    )

    for relative in (
        "THIRD_PARTY_NOTICES.md",
        "docs/about/license.md",
        "docs/en/about/license.md",
    ):
        text = (root / relative).read_text(encoding="utf-8")
        for notice in required:
            assert notice in text, f"{relative} is missing {notice}"


def test_practice_guides_are_authored_articles_with_primary_links() -> None:
    root = Path(__file__).resolve().parents[1]
    zh_root = root / "docs" / "guides"
    en_root = root / "docs" / "en" / "guides"
    guide_names = {
        path.name for path in zh_root.glob("*.md") if path.name != "index.md"
    }

    assert guide_names == {
        path.name for path in en_root.glob("*.md") if path.name != "index.md"
    }
    for name in sorted(guide_names):
        zh = (zh_root / name).read_text(encoding="utf-8")
        en = (en_root / name).read_text(encoding="utf-8")
        zh_headings = markdown_headings(zh)
        en_headings = markdown_headings(en)
        zh_h2 = [title for level, title, _line in zh_headings if level == 2]
        en_h2 = [title for level, title, _line in en_headings if level == 2]

        assert 3 <= len(zh_h2) <= 7, f"{name} has {len(zh_h2)} Chinese H2s"
        assert len(zh_h2) == len(en_h2), f"{name} has mismatched bilingual sections"
        assert sum(title in GUIDE_TEMPLATE_HEADINGS for title in zh_h2) < 3
        assert sum(title in GUIDE_TEMPLATE_HEADINGS for title in en_h2) < 3

        zh_urls = set(EXTERNAL_URL_RE.findall(zh))
        en_urls = set(EXTERNAL_URL_RE.findall(en))
        assert len(zh_urls) >= 3, f"{name} needs at least three direct HTTPS sources"
        assert zh_urls == en_urls, f"{name} must cite the same sources in both languages"
        assert '<div class="ee-language"' not in zh
        assert '<div class="ee-language"' not in en
        zh_visible = EXTERNAL_URL_RE.sub("", zh)
        en_visible = EXTERNAL_URL_RE.sub("", en)
        assert len(re.findall(r"\bEEDIY\b", zh_visible, re.IGNORECASE)) <= 1
        assert len(re.findall(r"\bEEDIY\b", en_visible, re.IGNORECASE)) <= 1


def test_pages_use_the_header_language_menu_instead_of_inline_switch_links() -> None:
    root = Path(__file__).resolve().parents[1]
    inline_switch = re.compile(
        r"(?m)^\[(?:English(?: version)?|中文|简体中文)\]\([^)]+\)\s*$"
    )
    offenders = [
        path.relative_to(root).as_posix()
        for path in sorted((root / "docs").rglob("*.md"))
        if inline_switch.search(path.read_text(encoding="utf-8"))
    ]

    assert not offenders, (
        "language switching belongs in Material's header menu, not the article "
        f"body: {offenders}"
    )


def test_search_results_are_scoped_to_the_current_language_tree() -> None:
    root = Path(__file__).resolve().parents[1]
    javascript = (
        root / "docs" / "assets" / "javascripts" / "extra.js"
    ).read_text(encoding="utf-8")
    main_template = (root / "overrides" / "main.html").read_text(
        encoding="utf-8"
    )
    config = (root / "mkdocs.yml").read_text(encoding="utf-8")

    assert "setupLanguageScopedSearch" in javascript
    assert '"[data-md-component=\'search-result\']"' in javascript
    assert '".md-search-result__list"' in javascript
    assert 'resultList.querySelectorAll(":scope > li")' not in javascript
    assert "item.remove()" not in javascript
    assert "search_index.en.json" in main_template
    assert "search_index.zh.json" in main_template
    assert r"/\/search\/search_index\.json$/" in main_template
    assert "XMLHttpRequest.prototype.open" in main_template
    assert "originalXhrOpen.call" in main_template
    assert "scripts/mkdocs_hooks.py" in config


def test_external_resources_keep_native_link_navigation_semantics() -> None:
    root = Path(__file__).resolve().parents[1]
    javascript = (
        root / "docs" / "assets" / "javascripts" / "extra.js"
    ).read_text(encoding="utf-8")

    assert "setupExternalResourceLinks" not in javascript
    assert 'anchor.target = "_blank"' not in javascript


def test_csdiy_navigation_affordances_are_enabled_and_localized() -> None:
    root = Path(__file__).resolve().parents[1]
    config = (root / "mkdocs.yml").read_text(encoding="utf-8")
    javascript = (
        root / "docs" / "assets" / "javascripts" / "extra.js"
    ).read_text(encoding="utf-8")

    assert "  - git-revision-date:" in config
    assert "  - open-in-new-tab:" in config
    assert "permalink_title: 永久链接" in config
    assert "setupLocalizedPermalinks" in javascript
    assert '"Permanent link"' in javascript
    assert '"永久链接"' in javascript
    assert 'document.querySelectorAll("a.headerlink")' in javascript


def test_practice_guides_do_not_reuse_or_lightly_rewrite_long_paragraphs() -> None:
    root = Path(__file__).resolve().parents[1]
    for language, guide_root in (
        ("zh", root / "docs" / "guides"),
        ("en", root / "docs" / "en" / "guides"),
    ):
        by_name = {
            path.name: _practice_paragraphs(
                path.read_text(encoding="utf-8"),
                language,
            )
            for path in sorted(guide_root.glob("*.md"))
            if path.name != "index.md"
        }
        exact: dict[str, list[str]] = defaultdict(list)
        for name, paragraphs in by_name.items():
            for paragraph in paragraphs:
                exact[paragraph].append(name)
        repeated = {
            paragraph: sorted(set(names))
            for paragraph, names in exact.items()
            if len(set(names)) > 1
        }
        assert not repeated, f"{language} practice guides reuse long paragraphs: {repeated}"

        names = sorted(by_name)
        fuzzy: list[tuple[str, str, float]] = []
        for left_index, left_name in enumerate(names):
            for right_name in names[left_index + 1 :]:
                for left in by_name[left_name]:
                    for right in by_name[right_name]:
                        shorter, longer = sorted((len(left), len(right)))
                        if shorter / max(longer, 1) < 0.72:
                            continue
                        matcher = difflib.SequenceMatcher(None, left, right, autojunk=False)
                        if matcher.quick_ratio() < PRACTICE_FUZZY_THRESHOLD:
                            continue
                        ratio = matcher.ratio()
                        if ratio >= PRACTICE_FUZZY_THRESHOLD:
                            fuzzy.append((left_name, right_name, round(ratio, 3)))
        assert not fuzzy, f"{language} practice guides contain fuzzy template reuse: {fuzzy}"


def test_hreflang_targets_preserve_site_subpath_and_deep_counterpart(
    tmp_path: Path,
) -> None:
    root = Path(__file__).resolve().parents[1]
    docs = tmp_path / "docs"
    _write_pair(docs, "index.md", ZH_PAGE, EN_PAGE)
    _write_pair(docs, "courses/demo.md", ZH_CHILD, EN_CHILD)
    site = tmp_path / "site"
    config_path = tmp_path / "mkdocs.yml"
    custom_dir = (root / "overrides").as_posix()
    hook_path = (root / "scripts" / "mkdocs_hooks.py").as_posix()
    config_path.write_text(
        "site_name: Alternate metadata test\n"
        "site_url: https://appleweiping.github.io/eediy/\n"
        "docs_dir: docs\n"
        "site_dir: site\n"
        "hooks:\n"
        f"  - {hook_path}\n"
        "theme:\n"
        "  name: material\n"
        f"  custom_dir: {custom_dir}\n"
        "  palette:\n"
        "    - scheme: default\n"
        "      primary: light blue\n"
        "      accent: deep purple\n"
        "      toggle:\n"
        "        icon: material/weather-sunny\n"
        "        name: switch\n"
        "    - scheme: slate\n"
        "      primary: cyan\n"
        "      accent: deep purple\n"
        "      toggle:\n"
        "        icon: material/weather-night\n"
        "        name: switch\n"
        "extra:\n"
        "  alternate: true\n"
        "nav:\n"
        "  - 中文:\n"
        "      - 首页: index.md\n"
        "      - 深层页: courses/demo.md\n"
        "  - English:\n"
        "      - Home: en/index.md\n"
        "      - Deep page: en/courses/demo.md\n",
        encoding="utf-8",
    )

    build(load_config(config_file=str(config_path)))

    expected_by_page = {
        site / "index.html": {
            "zh-Hans": "https://appleweiping.github.io/eediy/",
            "en": "https://appleweiping.github.io/eediy/en/",
        },
        site / "en" / "index.html": {
            "zh-Hans": "https://appleweiping.github.io/eediy/",
            "en": "https://appleweiping.github.io/eediy/en/",
        },
        site / "courses" / "demo" / "index.html": {
            "zh-Hans": "https://appleweiping.github.io/eediy/courses/demo/",
            "en": "https://appleweiping.github.io/eediy/en/courses/demo/",
        },
        site / "en" / "courses" / "demo" / "index.html": {
            "zh-Hans": "https://appleweiping.github.io/eediy/courses/demo/",
            "en": "https://appleweiping.github.io/eediy/en/courses/demo/",
        },
    }
    pattern = re.compile(
        r'<link rel="alternate" href="([^"]+)" hreflang="([^"]+)">'
    )
    for page, expected in expected_by_page.items():
        rendered = page.read_text(encoding="utf-8")
        targets = {language: href for href, language in pattern.findall(rendered)}
        assert targets == expected

    relation_pattern = re.compile(
        r'<link rel="(prev|next)" href="([^"]+)">'
    )
    expected_relations = {
        site / "index.html": {
            "next": "https://appleweiping.github.io/eediy/courses/demo/",
        },
        site / "courses" / "demo" / "index.html": {
            "prev": "https://appleweiping.github.io/eediy/",
        },
        site / "en" / "index.html": {
            "next": "https://appleweiping.github.io/eediy/en/courses/demo/",
        },
        site / "en" / "courses" / "demo" / "index.html": {
            "prev": "https://appleweiping.github.io/eediy/en/",
        },
    }
    canonical_by_page = {
        site / "index.html": "https://appleweiping.github.io/eediy/",
        site / "courses" / "demo" / "index.html": (
            "https://appleweiping.github.io/eediy/courses/demo/"
        ),
        site / "en" / "index.html": "https://appleweiping.github.io/eediy/en/",
        site / "en" / "courses" / "demo" / "index.html": (
            "https://appleweiping.github.io/eediy/en/courses/demo/"
        ),
    }
    for page, expected in expected_relations.items():
        rendered = page.read_text(encoding="utf-8")
        relations = {
            relation: urljoin(canonical_by_page[page], href)
            for relation, href in relation_pattern.findall(rendered)
        }
        assert relations == expected

    header_logo_pattern = re.compile(
        r'<a href="([^"]+)"[^>]*class="md-header__button md-logo"'
    )
    expected_header_homes = {
        site / "index.html": "https://appleweiping.github.io/eediy/",
        site / "courses" / "demo" / "index.html": (
            "https://appleweiping.github.io/eediy/"
        ),
        site / "en" / "index.html": "https://appleweiping.github.io/eediy/en/",
        site / "en" / "courses" / "demo" / "index.html": (
            "https://appleweiping.github.io/eediy/en/"
        ),
    }
    for page, expected in expected_header_homes.items():
        rendered = page.read_text(encoding="utf-8")
        match = header_logo_pattern.search(rendered)
        assert match is not None
        assert urljoin(canonical_by_page[page], match.group(1)) == expected

    chinese_html = (site / "courses" / "demo" / "index.html").read_text(
        encoding="utf-8"
    )
    english_html = (
        site / "en" / "courses" / "demo" / "index.html"
    ).read_text(encoding="utf-8")
    assert '<html lang="zh"' in chinese_html
    assert '<html lang="en"' in english_html
    assert 'placeholder="搜索"' in chinese_html
    assert 'placeholder="Search"' in english_html
    assert 'aria-label="切换至深色"' in chinese_html
    assert 'aria-label="Switch to dark"' in english_html
    assert "Switch to dark /" not in english_html
    assert "search_index.zh.json" in chinese_html
    assert "search_index.en.json" in english_html

    combined_index = json.loads(
        (site / "search" / "search_index.json").read_text(encoding="utf-8")
    )
    zh_index = json.loads(
        (site / "search" / "search_index.zh.json").read_text(encoding="utf-8")
    )
    en_index = json.loads(
        (site / "search" / "search_index.en.json").read_text(encoding="utf-8")
    )
    assert zh_index["config"]["lang"] == ["zh"]
    assert en_index["config"]["lang"] == ["en"]
    assert all(
        not document["location"].lstrip("/").startswith("en/")
        for document in zh_index["docs"]
    )
    assert all(
        document["location"].lstrip("/").startswith("en/")
        for document in en_index["docs"]
    )
    assert (
        len(zh_index["docs"]) + len(en_index["docs"])
        == len(combined_index["docs"])
    )

    chinese_navigation = (site / "index.html").read_text(encoding="utf-8")
    english_navigation = (site / "en" / "index.html").read_text(encoding="utf-8")
    assert "深层页" in chinese_navigation
    assert "Deep page" not in chinese_navigation
    assert "Deep page" in english_navigation
    assert "深层页" not in english_navigation
