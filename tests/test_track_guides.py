from __future__ import annotations

import json
from pathlib import Path

from scripts.track_guides import (
    _corpus_style_issues,
    _validate_fragment,
    _validate_translation_details,
    load_track_guides,
)


ROOT = Path(__file__).resolve().parents[1]


def _fragment(language: str) -> str:
    if language == "zh":
        paragraph = (
            "这段方向导读比较具体课程、先修缺口、材料访问边界和能够带到下一门课的作品，"
            "帮助学习者根据实际项目选择课程，而不是并行收集一组作用相同的替代课。"
        )
        links = "[课程甲](001-course-a.md) 与 [先修方向](../foundation/index.md)"
    else:
        paragraph = (
            "This authored track guide compares specific courses, prerequisite gaps, "
            "material-access boundaries, and work that remains useful in the next subject, "
            "so a learner chooses from a real project instead of collecting alternatives. "
        )
        links = "[Course A](001-course-a.md) and [the prerequisite](../foundation/index.md)"
    primary_source = (
        "[课程主页](https://example.edu/course/)"
        if language == "zh"
        else "[course home](https://example.edu/course/)"
    )
    return (
        f"## Position\n\n{links}. {primary_source}. {paragraph * 5}\n\n"
        f"## Selection\n\n"
        f"{'选课时要说清每个替代项解决的具体缺口。' if language == 'zh' else 'Course selection should name the precise gap each alternative solves. '}"
        f"{paragraph * 6}\n\n"
        f"## What to carry forward\n\n"
        f"{'离开这一方向时，应留下能被下一门课直接复用的作品。' if language == 'zh' else 'Leave this track with work that the next subject can use directly. '}"
        f"{paragraph * 6}\n"
    )


def test_track_guide_loader_requires_bilingual_authored_fragments(
    tmp_path: Path,
) -> None:
    root = tmp_path / "track-guides"
    root.mkdir()
    (root / "circuits.zh.md").write_text(_fragment("zh"), encoding="utf-8")
    (root / "circuits.en.md").write_text(_fragment("en"), encoding="utf-8")
    for language in ("zh", "en"):
        foundation = (
            _fragment(language)
            .replace("001-course-a.md", "002-foundation.md")
            .replace("../foundation/index.md", "../circuits/index.md")
            .replace(
                "这段方向导读比较具体课程、先修缺口、材料访问边界和能够带到下一门课的作品，"
                "帮助学习者根据实际项目选择课程，而不是并行收集一组作用相同的替代课。",
                "基础方向稿围绕概念依赖、推导训练、错题复核和后续课程接口展开，"
                "读者应以诊断题暴露薄弱环节，并用能够复算的推导档案证明入口已经补齐。",
            )
            .replace(
                "This authored track guide compares specific courses, prerequisite gaps, "
                "material-access boundaries, and work that remains useful in the next subject, "
                "so a learner chooses from a real project instead of collecting alternatives. ",
                "This foundation guide follows conceptual dependencies, derivation practice, "
                "error review, and interfaces to later courses. A learner uses diagnostic "
                "problems to expose gaps and a reproducible derivation record to close them. ",
            )
        )
        (root / f"foundation.{language}.md").write_text(
            foundation,
            encoding="utf-8",
        )
    catalogue = {
        "courses": [
            {"track": "circuits", "slug": "001-course-a"},
            {"track": "foundation", "slug": "002-foundation"},
        ]
    }

    guides, issues = load_track_guides(catalogue, root)

    assert issues == []
    assert set(guides) == {"circuits", "foundation"}
    assert set(guides["circuits"]["bodies"]) == {"zh", "en"}


def test_track_guide_validator_rejects_short_unlinked_fragment(
    tmp_path: Path,
) -> None:
    path = tmp_path / "circuits.en.md"
    body = (
        "## One\n\n[Course home](https://example.edu/course). Short.\n\n"
        "## Two\n\nShort.\n\n## Three\n\nShort.\n"
    )

    issues = _validate_fragment(body, language="en", path=path)

    assert {issue.code for issue in issues} == {
        "track_guide.depth",
        "track_guide.course_links",
        "track_guide.section_depth",
    }


def test_track_guide_loader_reports_missing_translation(tmp_path: Path) -> None:
    root = tmp_path / "track-guides"
    root.mkdir()
    (root / "circuits.zh.md").write_text(_fragment("zh"), encoding="utf-8")

    _, issues = load_track_guides(
        {"courses": [{"track": "circuits", "slug": "001-course-a"}]},
        root,
    )

    assert any(issue.code == "track_guide.file_read" for issue in issues)


def test_track_guide_translation_rejects_missing_caveat_paragraph() -> None:
    zh = _fragment("zh").replace(
        "\n\n## Selection",
        (
            "\n\n这一段单独说明原课程的实验需要校园仪器和现场反馈，"
            "校外自拟练习不能改名为原课程实验，也不能声称获得原校评分。"
            "\n\n## Selection"
        ),
    )

    issues = _validate_translation_details(
        "circuits",
        {"zh": zh, "en": _fragment("en")},
    )

    assert "track_guide.translation_paragraphs" in {
        issue.code for issue in issues
    }


def test_track_guide_translation_rejects_numeric_and_technical_mismatch() -> None:
    zh = _fragment("zh").replace(
        "[课程主页](https://example.edu/course/).",
        (
            "[课程主页](https://example.edu/course/)。"
            "同一 RISC-V 模块要在 FPGA 上用 Vivado 重放 6 个周期。"
        ),
    )
    en = _fragment("en").replace(
        "[course home](https://example.edu/course/).",
        (
            "[course home](https://example.edu/course/). "
            "Replay the same ARM module for 7 cycles on the FPGA in Vivado."
        ),
    )

    issues = _validate_translation_details(
        "computer-architecture",
        {"zh": zh, "en": en},
    )
    codes = {issue.code for issue in issues}

    assert "track_guide.translation_numbers" in codes
    assert "track_guide.translation_terms" in codes


def test_track_guide_loader_rejects_invalid_and_mismatched_links(
    tmp_path: Path,
) -> None:
    root = tmp_path / "track-guides"
    root.mkdir()
    zh = _fragment("zh").replace(
        "../foundation/index.md",
        "../unknown/index.md",
    )
    en = _fragment("en")
    (root / "circuits.zh.md").write_text(zh, encoding="utf-8")
    (root / "circuits.en.md").write_text(en, encoding="utf-8")
    (root / "foundation.zh.md").write_text(
        _fragment("zh").replace("001-course-a.md", "002-foundation.md"),
        encoding="utf-8",
    )
    (root / "foundation.en.md").write_text(
        _fragment("en").replace("001-course-a.md", "002-foundation.md"),
        encoding="utf-8",
    )
    catalogue = {
        "courses": [
            {"track": "circuits", "slug": "001-course-a"},
            {"track": "foundation", "slug": "002-foundation"},
        ]
    }

    _, issues = load_track_guides(catalogue, root)

    codes = {issue.code for issue in issues}
    assert "track_guide.link_target" in codes
    assert "track_guide.translation_links" in codes


def test_track_guide_validator_requires_direct_https_primary_source(
    tmp_path: Path,
) -> None:
    path = tmp_path / "circuits.en.md"
    body = _fragment("en").replace(
        "[course home](https://example.edu/course/)",
        "course home at https://example.edu/course/",
    )

    issues = _validate_fragment(body, language="en", path=path)

    assert "track_guide.primary_source_link" in {
        issue.code for issue in issues
    }


def test_track_guide_loader_rejects_mismatched_external_sources(
    tmp_path: Path,
) -> None:
    root = tmp_path / "track-guides"
    root.mkdir()
    for language in ("zh", "en"):
        body = _fragment(language).replace(
            "../foundation/index.md",
            "002-course-b.md",
        )
        if language == "en":
            body = body.replace(
                "https://example.edu/course/",
                "https://example.edu/different-course/",
            )
        (root / f"circuits.{language}.md").write_text(body, encoding="utf-8")
    catalogue = {
        "courses": [
            {"track": "circuits", "slug": "001-course-a"},
            {"track": "circuits", "slug": "002-course-b"},
        ]
    }

    _, issues = load_track_guides(catalogue, root)

    mismatch = [
        issue
        for issue in issues
        if issue.code == "track_guide.translation_external_links"
    ]
    assert len(mismatch) == 1
    assert "https://example.edu/course" in (mismatch[0].context or "")
    assert "https://example.edu/different-course" in (
        mismatch[0].context or ""
    )


def test_track_guide_loader_normalizes_external_sources_before_comparison(
    tmp_path: Path,
) -> None:
    root = tmp_path / "track-guides"
    root.mkdir()
    zh = (
        _fragment("zh")
        .replace("../foundation/index.md", "002-course-b.md")
        .replace(
            "https://example.edu/course/",
            "https://EXAMPLE.EDU:443/course/",
        )
    )
    en = (
        _fragment("en")
        .replace("../foundation/index.md", "002-course-b.md")
        .replace("https://example.edu/course/", "https://example.edu/course")
    )
    (root / "circuits.zh.md").write_text(zh, encoding="utf-8")
    (root / "circuits.en.md").write_text(en, encoding="utf-8")
    catalogue = {
        "courses": [
            {"track": "circuits", "slug": "001-course-a"},
            {"track": "circuits", "slug": "002-course-b"},
        ]
    }

    _, issues = load_track_guides(catalogue, root)

    assert not any(
        issue.code == "track_guide.translation_external_links"
        for issue in issues
    )


def test_track_guide_loader_rejects_reused_editorial_paragraph(
    tmp_path: Path,
) -> None:
    root = tmp_path / "track-guides"
    root.mkdir()
    for track, slug in (("circuits", "001-course-a"), ("signals", "002-course-b")):
        for language in ("zh", "en"):
            body = _fragment(language).replace("001-course-a.md", f"{slug}.md")
            (root / f"{track}.{language}.md").write_text(body, encoding="utf-8")
    catalogue = {
        "courses": [
            {"track": "circuits", "slug": "001-course-a"},
            {"track": "signals", "slug": "002-course-b"},
            {"track": "foundation", "slug": "003-foundation"},
        ]
    }

    _, issues = load_track_guides(catalogue, root)

    assert any(issue.code == "track_guide.duplicate_paragraph" for issue in issues)


def test_track_guide_loader_rejects_lightly_rewritten_template(
    tmp_path: Path,
) -> None:
    root = tmp_path / "track-guides"
    root.mkdir()
    for language in ("zh", "en"):
        first = _fragment(language)
        second = (
            first.replace("001-course-a.md", "002-course-b.md")
            .replace("这段方向导读", "这份方向导读")
            .replace("This authored track guide", "This edited track guide")
        )
        (root / f"circuits.{language}.md").write_text(first, encoding="utf-8")
        (root / f"signals.{language}.md").write_text(second, encoding="utf-8")
    catalogue = {
        "courses": [
            {"track": "circuits", "slug": "001-course-a"},
            {"track": "signals", "slug": "002-course-b"},
            {"track": "foundation", "slug": "003-foundation"},
        ]
    }

    _, issues = load_track_guides(catalogue, root)

    assert any(issue.code == "track_guide.fuzzy_paragraph" for issue in issues)


def test_track_guide_validator_rejects_catalogue_boilerplate(tmp_path: Path) -> None:
    path = tmp_path / "circuits.zh.md"
    body = _fragment("zh") + "\n掌握电路的核心概念、模型与分析方法。\n"

    issues = _validate_fragment(body, language="zh", path=path)

    assert "track_guide.formulaic_copy" in {issue.code for issue in issues}


def test_track_guide_validator_rejects_internal_review_voice_and_protocol_end(
    tmp_path: Path,
) -> None:
    path = tmp_path / "circuits.en.md"
    body = _fragment("en") + "\nA reviewer should approve the completion evidence.\n"

    issues = _validate_fragment(body, language="en", path=path)
    codes = {issue.code for issue in issues}

    assert "track_guide.internal_editorial_voice" in codes
    assert "track_guide.protocol_ending" in codes


def test_track_guide_validator_rejects_section_sprawl_and_brand_overuse(
    tmp_path: Path,
) -> None:
    path = tmp_path / "circuits.en.md"
    body = (
        _fragment("en")
        + "\n## Extra one\n\n"
        + ("A course-specific comparison with [Course A](001-course-a.md). " * 20)
        + "\n\n## Extra two\n\n"
        + ("EEDIY should stay out of the learner's way. " * 20)
        + "\n\n## Extra three\n\n"
        + ("EEDIY is repeated here only to exercise the quality rule. " * 20)
    )

    issues = _validate_fragment(body, language="en", path=path)
    codes = {issue.code for issue in issues}

    assert "track_guide.section_sprawl" in codes
    assert "track_guide.brand_overuse" in codes


def test_track_guide_corpus_gate_rejects_one_procedural_voice() -> None:
    body = (
        "先固定环境。这不是普通课程，学习者必须保留失败记录，"
        "不要省略步骤；EEDIY 会在最后冻结版本。"
    )
    guides = {
        f"track-{index:02d}": {
            "bodies": {
                "zh": body
                + "\n"
                + "\n".join(
                    f"## 区段 {section}"
                    for section in range(3 + (index % 3))
                ),
                "en": "placeholder",
            }
        }
        for index in range(35)
    }

    issues = _corpus_style_issues(guides)

    assert {issue.code for issue in issues} == {
        "track_guide.corpus_template_vocabulary"
    }
    assert len(issues) == 6


def test_track_guide_corpus_gate_rejects_isomorphic_h2_structure() -> None:
    body = "\n\n".join(
        f"## Section {index}\n\nTrack-specific discussion."
        for index in range(4)
    )
    guides = {
        f"track-{index:02d}": {"bodies": {"zh": body, "en": body}}
        for index in range(35)
    }

    issues = _corpus_style_issues(guides)
    by_code = {issue.code: issue for issue in issues}

    assert set(by_code) == {
        "track_guide.corpus_structure_variety",
        "track_guide.corpus_structure_dominance",
    }
    assert "[4:35]" in by_code[
        "track_guide.corpus_structure_variety"
    ].message
    assert "35/35 guides (100.0%)" in by_code[
        "track_guide.corpus_structure_dominance"
    ].message


def test_track_guide_corpus_gate_rejects_saturated_english_qa_vocabulary() -> None:
    guides = {}
    for index in range(35):
        h2_count = 3 + (index % 3)
        headings = "\n\n".join(
            f"## Section {section}\n\nTrack-specific discussion."
            for section in range(h2_count)
        )
        english = (
            headings
            + "\n\nBring every prerequisite from an earlier course. "
            "Without a failure, preserve the record."
        )
        guides[f"track-{index:02d}"] = {
            "bodies": {"zh": headings, "en": english}
        }

    issues = _corpus_style_issues(guides)

    vocabulary_issues = [
        issue
        for issue in issues
        if issue.code == "track_guide.corpus_template_vocabulary"
    ]
    assert len(vocabulary_issues) == 4
    assert {
        issue.message.split("' appears", 1)[0].strip("'")
        for issue in vocabulary_issues
    } == {
        "Bring … from",
        "Without",
        "failure / failed / failing",
        "record / preserve / keep",
    }


def test_production_track_guides_cover_every_populated_track_without_issues() -> None:
    catalogue = json.loads(
        (ROOT / "data" / "courses.json").read_text(encoding="utf-8")
    )
    expected = {course["track"] for course in catalogue["courses"]}

    guides, issues = load_track_guides(
        catalogue,
        ROOT / "content" / "track-guides",
    )

    assert issues == []
    assert set(guides) == expected
