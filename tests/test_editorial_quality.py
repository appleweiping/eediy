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
    zh_padding = "\n\n".join(
        [
            f"围绕{topic_zh}，先固定电源、源阻抗、负载与元件公差，再从微分方程推导"
            "传递函数。SPICE 的 DC operating point、AC response 与 transient response "
            "分别回答偏置、频域和时域问题；极点位置、阻尼比、谐振峰与 settling "
            "必须能从手算和仿真两边解释。若手算与波形不一致，应回到同一张电路图检查"
            "参考方向、初始条件、负载模型"
            "和 solver 设置。每次只改变一个参数，观察 pole 与 step response 怎样移动；"
            "这样可以区分代数符号错误、模型遗漏和数值设置，而不是靠反复调参碰到一条"
            "看似正确的曲线。",
            "收尾时重新做一题尚未看解答的 assignment，再用公开 solution 定位推导中"
            "最早的分歧。随后在固定条件下比较手算 Bode 特征、SPICE sweep 和 transient "
            f"结果，并说明{topic_zh}在哪个参数范围内满足设计目标、在哪个边界首先失效。"
            "这份比较比堆叠截图更能体现课程里的模型判断。",
        ]
    )
    en_padding = "\n\n".join(
        [
            f"For the {topic_en}, fix the supply, source impedance, load, and "
            "component tolerances before deriving the transfer function from the "
            "differential equation. SPICE DC operating point, AC response, and "
            "transient response answer different questions. Pole locations, damping "
            "ratio, resonant peak, and settling should agree with both the derivation "
            "and the simulation. When the calculation and waveform disagree, return "
            "to the same schematic "
            "and inspect reference directions, initial conditions, the load model, and "
            "solver settings. Change one parameter at a time and predict how the poles "
            "and step response should move. This separates an algebra error, an omitted "
            "model effect, and a numerical setting from blind parameter tuning.",
            "To finish, attempt an unseen assignment problem before opening its public "
            "solution and locate the earliest divergence in the derivation. Under fixed "
            "conditions, compare the hand-derived Bode features, SPICE sweep, and "
            f"transient result. Explain where the {topic_en} meets the design target "
            "and which parameter boundary causes the first failure; that comparison "
            "demonstrates model judgment better than a stack of screenshots.",
        ]
    )
    zh = f"""\
## 课程定位

若想把 RLC 手算和 SPICE 验证放在同一门课里，这门课适合作为首选。官方
[Syllabus]({urls[0]}) 说明 {code} 的 2024 版本按 Lecture 1–4 组织，
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

This course is a good first choice if you want RLC derivations and SPICE
verification in one sequence. The official [syllabus]({urls[0]}) organizes the
2024 version of {code} as
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
            "deriving the transfer function",
            "repair linear algebra first, then derive the transfer function",
            1,
        ),
    )

    issues = _document_issues(analyze_document(unnatural))

    assert "editorial.translationese" in _codes(issues, "error")


def test_repeated_sentence_tripwire_ignores_code_tables_and_two_uses(
    tmp_path: Path,
) -> None:
    pair = _guide_pair(1, root=tmp_path)
    sentence = (
        "This deliberately repeated narrative sentence describes the same circuit "
        "assumption, simulation result, boundary condition, and engineering decision "
        "without adding any new course-specific evidence or technical explanation for "
        "the learner."
    )
    twice = replace(pair.en, text=pair.en.text + f"\n\n{sentence} {sentence}\n")
    padding_loop = replace(
        pair.en,
        text=pair.en.text + f"\n\n{sentence} {sentence} {sentence}\n",
    )
    code_and_table = replace(
        pair.en,
        text=(
            pair.en.text
            + f"\n\n```text\n{sentence}\n{sentence}\n{sentence}\n```\n\n"
            "| Expression | Meaning |\n"
            "| --- | --- |\n"
            f"| {sentence} | model |\n"
            f"| {sentence} | model |\n"
            f"| {sentence} | model |\n"
        ),
    )

    assert "editorial.repeated_sentence" not in _codes(
        _document_issues(analyze_document(twice)),
        "error",
    )
    assert "editorial.repeated_sentence" in _codes(
        _document_issues(analyze_document(padding_loop)),
        "error",
    )
    assert "editorial.repeated_sentence" not in _codes(
        _document_issues(analyze_document(code_and_table)),
        "error",
    )


def test_template_voice_and_delayed_course_judgment_are_blocked(
    tmp_path: Path,
) -> None:
    text = """\
## 材料清点

官方页面列出了讲义和作业文件，这一段只复述页面栏目与文件名称。

## 统一流程

我会检查五项完成证据。先下载讲义，再填写表格，最后归档。先运行脚本，再截图，最后提交。
这个结果不是课程项目，也不等于完成课程，而不是官方评分。

## 命令

学习者必须记录版本，不要跳步，应当复核；必须保存日志，不要省略，应当提交。

[课程](https://example.edu/course) [作业](https://example.edu/work)
[考试](https://example.edu/exam)
"""
    document = GuideDocument(
        1,
        "zh",
        tmp_path / "templated.zh.md",
        text,
        {"title": {"zh": "测试"}, "course_code": "EE-1"},
        (
            "https://example.edu/course",
            "https://example.edu/work",
            "https://example.edu/exam",
        ),
        "R0",
    )

    codes = _codes(_document_issues(analyze_document(document)), "error")

    assert {
        "editorial.late_judgment",
        "editorial.fake_reviewer_voice",
        "editorial.defensive_voice",
        "editorial.command_voice",
        "editorial.workflow_template",
    } <= codes


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


def test_catalogue_only_course_can_use_an_explicit_independent_project_map(
    tmp_path: Path,
) -> None:
    text = """\
## 这是一张课程地图，不是公开课程包

想把 timing、control 与 FPGA implementation 接成系统的人，可以把这门课用作
主题地图。官方 [院系页](https://example.edu/department)、
[课程目录](https://example.edu/catalogue) 和
[学期记录](https://example.edu/term) 只确认主题与课程身份，没有公开现行
assignments、starter、rubric 或 staff feedback。

## 独立项目的边界

下面是独立项目地图，不是学校官方作业或实验。学习者自行定义一个 FSM、一个
arithmetic datapath 和一个 bus peripheral，并用 assertion 与 timing report 判断结果。
这组练习只映射公开主题，不冒充原课提交物。

## 版本与取舍

官方页面说明当前工具环境；编辑建议在已有 RTL 与 testbench 经验后再选这条路线。
如果需要真实公开 assignment、grader 与课堂反馈，应改选材料完整的课程。
"""
    document = GuideDocument(
        43,
        "zh",
        tmp_path / "043.zh.md",
        text,
        {"title": {"zh": "目录课程"}, "course_code": "ECE 385"},
        (
            "https://example.edu/department",
            "https://example.edu/catalogue",
            "https://example.edu/term",
        ),
        "R0",
    )

    codes = _codes(_document_issues(analyze_document(document)), "error")

    assert "editorial.real_coursework" not in codes


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


def test_bilingual_parity_blocks_one_missing_substantive_paragraph(
    tmp_path: Path,
) -> None:
    pair = _guide_pair(1, root=tmp_path)
    extra = (
        "这一段补充一个独立的课程限制、项目边界和复核条件，长度足以成为实质段落，"
        "却没有出现在英文版本中；标题和链接仍然完全一致，因此不能只靠页面结构判断翻译完整。"
    )
    broken_zh = replace(
        pair.zh,
        text=pair.zh.text.replace(
            "## 完成判断",
            f"{extra}\n\n## 完成判断",
        ),
    )
    broken_pair = GuidePair(pair.course_id, broken_zh, pair.en)

    issues = _bilingual_issues(
        broken_pair,
        analyze_document(broken_pair.zh),
        analyze_document(broken_pair.en),
    )

    assert "editorial.translation_paragraphs" in _codes(issues, "error")


def test_bilingual_parity_blocks_severely_truncated_aligned_paragraph(
    tmp_path: Path,
) -> None:
    pair = _guide_pair(1, root=tmp_path)
    original = pair.en.text
    start = original.index("For the damped capacitor network")
    end = original.index("\n", start)
    truncated = original[:start] + "A short summary." + original[end:]
    broken_pair = GuidePair(
        pair.course_id,
        pair.zh,
        replace(pair.en, text=truncated),
    )

    issues = _bilingual_issues(
        broken_pair,
        analyze_document(broken_pair.zh),
        analyze_document(broken_pair.en),
    )

    assert "editorial.translation_paragraph_length" in _codes(issues, "error")


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
