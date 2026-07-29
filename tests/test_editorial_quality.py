from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import scripts.check_editorial_quality as editorial
from scripts.check_editorial_quality import (
    GuideDocument,
    GuidePair,
    _bilingual_issues,
    _document_issues,
    _exact_paragraph_issues,
    _fuzzy_duplicate_issues,
    analyze_document,
    editorial_quality_issues,
    selected_course_ids,
)
from scripts.quality_common import Issue


def _guide_pair(
    course_id: int,
    *,
    root: Path,
    topic_zh: str = "阻尼电容网络",
    topic_en: str = "damped capacitor network",
) -> GuidePair:
    code = f"EE-{course_id}"
    title = f"Evidence Course {course_id}"
    urls = (
        f"https://example.edu/{course_id}/syllabus",
        f"https://example.edu/{course_id}/assignments",
        f"https://example.edu/{course_id}/archive",
    )
    zh_padding = " ".join(
        [
            (
                f"围绕{topic_zh}，记录模型假设、输入条件、原始输出、误差来源和复核依据，"
                "并把未通过的检查与下一次修改完整留在工程日志中。"
            )
            for _ in range(25)
        ]
    )
    en_padding = " ".join(
        [
            (
                f"For the {topic_en}, preserve model assumptions, input conditions, "
                "raw output, error sources, failed checks, review evidence, and the "
                "next engineering revision in a reproducible log."
            )
            for _ in range(22)
        ]
    )
    zh = f"""\
## 课程定位

官方 [Syllabus]({urls[0]}) 说明 {code} 的 2024 版本按 Lecture 1–4 组织，
并把 RLC 与 SPICE 模型放进同一条分析链。

## 课件与考核

官方 [Assignments]({urls[1]}) 列出 Problem Set 1–4、Quiz 1 与 Exam 1；
作业占 40%，公开 solutions 用于提交后的复核。

## 实验和项目

官方材料中的 Lab 1 与 Project 2 要求保存输入、测量和设计判断，不能只提交最后图表。

## 版本与建议

[Course archive]({urls[2]}) 保留 2024 工具版本与访问说明。EEDIY 建议另做一个
{topic_zh} notebook 作为数值补充；它不是官方项目或课程作业。

## 完成判断

{zh_padding}
"""
    en = f"""\
## Course Position

The official [syllabus]({urls[0]}) organizes the 2024 version of {code} as
Lectures 1–4 and connects the RLC and SPICE models in one analysis chain.

## Materials and Assessment

The official [assignments]({urls[1]}) list Problem Sets 1–4, Quiz 1, and Exam 1.
Homework is 40%, with public solutions reserved for post-submission review.

## Laboratory and Project

Official material for Lab 1 and Project 2 requires inputs, measurements, and
design decisions rather than only a final plot.

## Version and Advice

The [course archive]({urls[2]}) preserves the 2024 tool version and access note.
EEDIY suggests adding a {topic_en} notebook as a numerical supplement; it is
not an official project or course assignment.

## Completion

{en_padding}
"""
    metadata = {
        "source_id": course_id,
        "title": {"zh": title, "en": title},
        "institution": "Example University",
        "course_code": code,
        "slug": f"{course_id:03d}-evidence-course",
        "track": "calibration",
    }
    zh_document = GuideDocument(
        course_id,
        "zh",
        root / "content" / "course-guides" / f"{course_id:03d}.zh.md",
        zh,
        metadata,
        urls,
        "R0",
    )
    en_document = GuideDocument(
        course_id,
        "en",
        root / "content" / "course-guides" / f"{course_id:03d}.en.md",
        en,
        metadata,
        urls,
        "R0",
    )
    return GuidePair(course_id, zh_document, en_document)


def _codes(issues: list[Issue], severity: str | None = None) -> set[str]:
    return {
        issue.code
        for issue in issues
        if severity is None or issue.severity == severity
    }


def test_course_specific_pair_passes_all_hard_gates(tmp_path: Path) -> None:
    pair = _guide_pair(1, root=tmp_path)

    issues, statistics = editorial_quality_issues([pair])

    assert _codes(issues, "error") == set()
    assert statistics == {
        "guides_total": 1,
        "guides_checked": 1,
        "documents_analyzed": 2,
        "errors": 0,
        "warnings": 0,
    }


def test_exact_duplicate_normalizes_course_metadata_and_numbers(
    tmp_path: Path,
) -> None:
    first = _guide_pair(1, root=tmp_path)
    second = _guide_pair(2, root=tmp_path)
    analyses = [
        analyze_document(first.zh),
        analyze_document(second.zh),
    ]

    issues = _exact_paragraph_issues(analyses, {2})

    assert "editorial.duplicate_paragraph" in _codes(issues, "error")
    assert all(issue.path.endswith("002.zh.md") for issue in issues)
    assert any("001.zh.md" in issue.message for issue in issues)


def test_two_fuzzy_paragraphs_block_but_one_only_warns(tmp_path: Path) -> None:
    metadata = {
        "title": {"zh": "甲", "en": "Alpha"},
        "institution": "Example",
        "course_code": "EE-A",
    }
    base_one = (
        "这段课程说明逐项核对输入模型、边界条件、原始测量、误差传播、版本记录和复核"
        "结果，并要求学习者说明每一次失败怎样改变下一次实验设计，还要保存参数选择、"
        "复现实验命令、审阅结论和下一轮验证计划。"
    )
    base_two = (
        "第二段课程说明把讲义推导、独立作业、数值仿真、实体测量和报告审阅连接起来，"
        "同时保留工具版本、参数选择、未通过测试与重新运行步骤，并解释模型假设、"
        "测量不确定度、边界条件和工程结论怎样互相约束。"
    )
    near_one = base_one.replace("输入模型", "输入假设")
    near_two = base_two.replace("实体测量", "台架测量")

    def document(course_id: int, text: str) -> GuideDocument:
        return GuideDocument(
            course_id,
            "zh",
            tmp_path / f"{course_id:03d}.zh.md",
            text,
            metadata,
            (),
            "R0",
        )

    first = analyze_document(document(1, f"{base_one}\n\n{base_two}\n"))
    one_match = analyze_document(document(2, f"{near_one}\n"))
    two_matches = analyze_document(document(3, f"{near_one}\n\n{near_two}\n"))

    warning_issues = _fuzzy_duplicate_issues([first, one_match], {2})
    error_issues = _fuzzy_duplicate_issues([first, two_matches], {3})

    assert "editorial.fuzzy_paragraph" in _codes(warning_issues, "warning")
    assert "editorial.fuzzy_paragraphs" not in _codes(warning_issues, "error")
    assert "editorial.fuzzy_paragraphs" in _codes(error_issues, "error")


def test_fuzzy_prefilter_keeps_lightly_edited_english_template(
    tmp_path: Path,
) -> None:
    metadata = {
        "title": {"zh": "甲", "en": "Alpha"},
        "institution": "Example",
        "course_code": "EE-A",
    }
    original = (
        "For every laboratory, record the input model, boundary conditions, raw "
        "measurements, uncertainty calculation, software version, failed tests, "
        "and rerun command. Explain how each failure changed the next experiment, "
        "then preserve the parameter choices, plots, reviewer notes, and final "
        "verification result so another learner can reproduce the work."
    )
    edited = (
        "For every assignment, record the input assumption, boundary conditions, "
        "raw measurements, uncertainty calculation, tool version, failed tests, "
        "and rerun command. Explain how each failure changed the next experiment, "
        "then preserve the parameter choices, plots, reviewer notes, and final "
        "verification result so another learner can reproduce the work."
    )

    def document(course_id: int, text: str) -> GuideDocument:
        return GuideDocument(
            course_id,
            "en",
            tmp_path / f"{course_id:03d}.en.md",
            text,
            metadata,
            (),
            "R0",
        )

    issues = _fuzzy_duplicate_issues(
        [
            analyze_document(document(1, original)),
            analyze_document(document(2, edited)),
        ],
        {2},
    )

    assert "editorial.fuzzy_paragraph" in _codes(issues, "warning")


def test_generic_ratio_requires_unsupported_sentences(tmp_path: Path) -> None:
    generic = (
        "这是一门非常适合所有学习者的优质课程，可以帮助你形成全面而深入的理解，"
        "并为未来学习奠定坚实基础。"
    )
    neutral = (
        "记录假设来源、输入状态、输出证据、失败原因和复核结论，并保留修改前后的差异。"
    )
    text = "## 说明\n\n" + "".join([generic] * 4 + [neutral] * 36)
    document = GuideDocument(
        1,
        "zh",
        tmp_path / "generic.zh.md",
        text,
        {"title": {"zh": "测试"}, "course_code": "EE-1"},
        (),
        "R0",
    )

    analysis = analyze_document(document)
    issues = _document_issues(analysis)

    assert len(analysis.generic_sentences) == 4
    assert "editorial.generic_claims" in _codes(issues, "error")

    anchored = replace(
        document,
        text="## 说明\n\n"
        + (
            generic.rstrip("。")
            + "，并由 Lecture 1 与 Problem Set 1 的具体结果提供证据。"
        )
        * 4,
    )
    assert analyze_document(anchored).generic_sentences == ()


def test_translationese_repair_is_blocked_in_english_guides(
    tmp_path: Path,
) -> None:
    pair = _guide_pair(1, root=tmp_path)
    unnatural = replace(
        pair.en,
        text=pair.en.text.replace(
            "preserve model assumptions",
            "repair linear algebra first, then preserve model assumptions",
            1,
        ),
    )

    issues = _document_issues(analyze_document(unnatural))

    assert "editorial.translationese" in _codes(issues, "error")


def test_anchor_source_and_supplement_boundaries_are_actionable(
    tmp_path: Path,
) -> None:
    pair = _guide_pair(1, root=tmp_path)
    valid_analysis = analyze_document(pair.zh)
    valid_codes = _codes(_document_issues(valid_analysis), "error")
    assert "editorial.specificity" not in valid_codes
    assert "editorial.real_coursework" not in valid_codes
    assert "editorial.untraced_fact" not in valid_codes
    assert "editorial.supplement_boundary" not in valid_codes

    untraced = replace(
        pair.zh,
        text=pair.zh.text
        + "\n## 未溯源评分\n\nHomework 占 25%，Final 占 75%。\n",
    )
    untraced_issues = _document_issues(analyze_document(untraced))
    assert "editorial.untraced_fact" in _codes(untraced_issues, "error")

    supplement = replace(
        pair.zh,
        text=pair.zh.text.replace(
            "EEDIY 建议另做一个\n"
            "阻尼电容网络 notebook 作为数值补充；它不是官方项目或课程作业。",
            "独立学习者可以创建一个阻尼电容网络 notebook 项目并作为课程实验提交。",
        ),
    )
    supplement_issues = _document_issues(analyze_document(supplement))
    assert "editorial.supplement_boundary" in _codes(supplement_issues, "error")


def test_bilingual_parity_checks_links_years_percentages_and_numbers(
    tmp_path: Path,
) -> None:
    pair = _guide_pair(1, root=tmp_path)
    broken_en = replace(
        pair.en,
        text=pair.en.text.replace(
            "https://example.edu/1/archive",
            "https://example.edu/1/different-archive",
        )
        .replace("2024 tool version", "2025 tool version")
        .replace("Homework is 40%", "Homework is 35%"),
    )
    broken_pair = GuidePair(pair.course_id, pair.zh, broken_en)

    issues = _bilingual_issues(
        broken_pair,
        analyze_document(broken_pair.zh),
        analyze_document(broken_pair.en),
    )

    codes = _codes(issues, "error")
    assert "editorial.translation_links" in codes
    assert "editorial.translation_years" in codes
    assert "editorial.translation_percentages" in codes
    assert "editorial.translation_numbers" in _codes(issues, "warning")


def test_bilingual_parity_blocks_missing_substantive_paragraphs(
    tmp_path: Path,
) -> None:
    pair = _guide_pair(1, root=tmp_path)
    extra = (
        "这一段新增方法要求保存每一层模型的输入输出、失败数据、误差界和复核记录，"
        "以便另一名学习者能逐项重放判断过程，并确认结论没有依赖被省略的假设。"
    )
    broken_zh = replace(
        pair.zh,
        text=pair.zh.text.replace(
            "## 完成判断",
            f"{extra}\n\n{extra}\n\n## 完成判断",
        ),
    )
    broken_pair = GuidePair(pair.course_id, broken_zh, pair.en)

    issues = _bilingual_issues(
        broken_pair,
        analyze_document(broken_pair.zh),
        analyze_document(broken_pair.en),
    )

    codes = _codes(issues, "error")
    assert "editorial.translation_paragraphs" in codes
    assert "editorial.translation_section_length" in codes


def test_protected_term_parity_splits_slash_compounds() -> None:
    terms = editorial._protected_terms(
        "PMF/PDF、KVL/KCL、Hertzian/wire/loop 与 read/write"
    )

    assert {"pmf", "kvl", "kcl", "hertzian", "wire", "loop", "read", "write"} <= terms
    assert "pdf" not in terms


def test_changed_files_selects_pair_but_compares_against_full_corpus(
    tmp_path: Path,
) -> None:
    first = _guide_pair(1, root=tmp_path)
    second = _guide_pair(2, root=tmp_path)
    manifest = tmp_path / "data" / "course_guides.json"
    catalogue = tmp_path / "data" / "courses.json"

    selected, selection_issues = selected_course_ids(
        [first, second],
        ["content/course-guides/002.en.md", "README.md"],
        manifest_path=manifest,
        catalogue_path=catalogue,
        repo_root=tmp_path,
    )
    quality_issues, statistics = editorial_quality_issues(
        [first, second],
        selected_ids=selected,
    )

    assert selection_issues == []
    assert selected == {2}
    assert statistics["guides_checked"] == 1
    duplicate = [
        issue
        for issue in quality_issues
        if issue.code == "editorial.duplicate_paragraph"
    ]
    assert duplicate
    assert all(issue.path.endswith("002.zh.md") or issue.path.endswith("002.en.md") for issue in duplicate)


def test_changed_unmanaged_guide_is_an_error(tmp_path: Path) -> None:
    pair = _guide_pair(1, root=tmp_path)

    selected, issues = selected_course_ids(
        [pair],
        ["content/course-guides/999.zh.md"],
        manifest_path=tmp_path / "data/course_guides.json",
        catalogue_path=tmp_path / "data/courses.json",
        repo_root=tmp_path,
    )

    assert selected == set()
    assert _codes(issues, "error") == {"editorial.changed_unmanaged"}


def test_cli_can_treat_warnings_as_errors(
    tmp_path: Path,
    monkeypatch,
) -> None:
    warning = Issue("warning", "editorial.test_warning", "nonblocking")
    monkeypatch.setattr(editorial, "load_guide_pairs", lambda *args, **kwargs: ([], []))
    monkeypatch.setattr(
        editorial,
        "selected_course_ids",
        lambda *args, **kwargs: (set(), []),
    )
    monkeypatch.setattr(
        editorial,
        "editorial_quality_issues",
        lambda *args, **kwargs: (
            [warning],
            {
                "guides_total": 0,
                "guides_checked": 0,
                "documents_analyzed": 0,
                "errors": 0,
                "warnings": 1,
            },
        ),
    )

    base_args = [
        "--manifest",
        str(tmp_path / "manifest.json"),
        "--catalogue",
        str(tmp_path / "catalogue.json"),
    ]

    assert editorial.main(base_args) == 0
    assert editorial.main([*base_args, "--warnings-as-errors"]) == 1


def test_workflow_runs_changed_and_full_editorial_modes() -> None:
    root = Path(__file__).resolve().parents[1]
    workflow = (root / ".github" / "workflows" / "quality.yml").read_text(
        encoding="utf-8"
    )

    assert "scripts/check_editorial_quality.py" in workflow
    assert '--changed-from "${{ github.event.pull_request.base.sha }}"' in workflow
    assert "--warnings-as-errors" in workflow
    assert "if: github.event_name == 'pull_request'" in workflow
    assert "if: github.event_name != 'pull_request'" in workflow
    assert "build/editorial-quality.json" in workflow
