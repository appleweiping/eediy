from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
GUIDE_ROOT = REPO_ROOT / "content" / "course-guides"
H2_RE = re.compile(r"^## (.+)$", re.MULTILINE)

# These limits are deliberately looser than the current corpus. They leave room
# for course-specific judgments and the occasional useful imperative, while
# preventing a return to 100% bespoke headings or a corpus dominated by the
# same command/contrast/count formulas.
MAX_UNIQUE_HEADING_SHARE = 0.85
MAX_IMPERATIVE_SHARE = {"en": 0.25, "zh": 0.20}
MAX_NEGATED_CONTRAST_SHARE = 0.12
MAX_COUNT_SLOGAN_SHARE = 0.12

IMPERATIVE_RE = {
    "en": re.compile(
        r"^(?:Use|Read|Treat|Follow|Pair|Draw|Keep|Fix|Reorder|Delay|Make|"
        r"Build|Trace|Separate|Move|Turn|Attach|Organize|Run|Test|Start|"
        r"Rebuild|Preserve|Pick|Check|Audit|Stop|Add|Control|Let|Solve|"
        r"Return|Compare|Choose|Decide|Find|Learn|Prefer|Finish|End|"
        r"Graduate|Leave|Supply|Describe|Review|Frame|Interleave|Confirm|"
        r"Compress|Change|Enter|Put|Omit)\b",
        re.IGNORECASE,
    ),
    "zh": re.compile(
        r"^(?:使用|阅读|把|用|让|先|从|选择|固定|保留|检查|建立|完成|"
        r"不要|别|按|将|重排|压缩|改|拿|做|每|同时)"
    ),
}
NEGATED_CONTRAST_RE = {
    "en": re.compile(
        r"\b(?:not|cannot|do not|without|rather than|instead of|isn't|aren't)\b",
        re.IGNORECASE,
    ),
    "zh": re.compile(
        r"(?:不能|无法|不应|不要|别|不是|不等于|而不是|不替代|不代表|不冒充|不必)"
    ),
}
COUNT_SLOGAN_RE = {
    "en": re.compile(
        r"\b(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|"
        r"eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|"
        r"eighteen|nineteen|twenty(?:-five)?|twenty-four|twenty-eight|"
        r"thirty-eight|thirty-nine|sixty-five|eighty-four)\s+"
        r"(?:lectures?|weeks?|units?|chapters?|handouts?|sessions?|modules?|"
        r"problem sets?|problem groups?|sets?|homeworks?|assignments?|quizzes?|"
        r"exams?|labs?|projects?|meetings?|lessons?|studios?|design reviews?)\b",
        re.IGNORECASE,
    ),
    "zh": re.compile(
        r"(?:\d+|一|二|三|四|五|六|七|八|九|十|十一|十二|十三|十四|"
        r"十五|十六|十七|十八|十九|二十|二十四|二十五|二十八|三十八|"
        r"三十九|六十五|八十四)\s*"
        r"(?:讲|周|单元|章|份\s*(?:作业|题|handout)|套\s*(?:题|作业)|"
        r"个\s*(?:lab|project|实验|项目)|次\s*(?:课|quiz|考试)|lecture|"
        r"week|unit|chapter|handout|module|lab|project)",
        re.IGNORECASE,
    ),
}

STABLE_HEADING_PAIRS = {
    "Course fit": "课程定位",
    "Course focus": "课程重点",
    "Course scope": "课程范围",
    "Course format": "课程形式",
    "Course approach": "课程方法",
    "Prerequisites": "先修要求",
    "Course structure": "课程结构",
    "Course materials": "课程材料",
    "Coursework": "课程任务",
    "Assignments and feedback": "作业与反馈",
    "Labs and feedback": "实验与反馈",
    "Labs and projects": "实验与项目",
    "Final project": "结课项目",
    "Study advice": "学习建议",
    "Study notes": "学习笔记",
    "Learning outcomes": "学习成果",
    "Access and version notes": "访问与版本说明",
    "Access and course scope": "访问与课程范围",
    "Tools and environment": "工具与环境",
    "Safety": "安全说明",
    "Evaluation criteria": "评价标准",
    "Performance evaluation": "性能评估",
    "Programming practice": "编程练习",
    "Integration testing": "集成测试",
    "Independent exercises": "独立练习",
    "Synthesis exercise": "综合练习",
    "Numerical exercise": "数值练习",
    "Modeling exercise": "建模练习",
    "Modeling workflow": "建模方法",
    "Computational exercise": "计算练习",
}


def _guide_paths(language: str) -> list[Path]:
    return sorted(GUIDE_ROOT.glob(f"[0-9][0-9][0-9].{language}.md"))


def _headings(path: Path) -> list[str]:
    return H2_RE.findall(path.read_text(encoding="utf-8"))


def _corpus_headings(language: str) -> list[str]:
    return [
        heading
        for path in _guide_paths(language)
        for heading in _headings(path)
    ]


def _share(headings: list[str], pattern: re.Pattern[str]) -> float:
    return sum(bool(pattern.search(heading)) for heading in headings) / len(headings)


def test_heading_structure_and_stable_labels_are_bilingual() -> None:
    reverse_pairs = {zh: en for en, zh in STABLE_HEADING_PAIRS.items()}
    en_paths = _guide_paths("en")
    zh_paths = _guide_paths("zh")

    assert [path.stem.removesuffix(".en") for path in en_paths] == [
        path.stem.removesuffix(".zh") for path in zh_paths
    ]
    for en_path, zh_path in zip(en_paths, zh_paths, strict=True):
        en_headings = _headings(en_path)
        zh_headings = _headings(zh_path)
        assert len(en_headings) == len(zh_headings), en_path.name
        assert len(en_headings) == len(set(en_headings)), (
            en_path.name,
            "a course page must not repeat an H2 label",
        )
        assert len(zh_headings) == len(set(zh_headings)), (
            zh_path.name,
            "a course page must not repeat an H2 label",
        )
        for index, (en_heading, zh_heading) in enumerate(
            zip(en_headings, zh_headings, strict=True),
            start=1,
        ):
            if en_heading in STABLE_HEADING_PAIRS:
                assert zh_heading == STABLE_HEADING_PAIRS[en_heading], (
                    en_path.name,
                    index,
                    en_heading,
                    zh_heading,
                )
            if zh_heading in reverse_pairs:
                assert en_heading == reverse_pairs[zh_heading], (
                    zh_path.name,
                    index,
                    en_heading,
                    zh_heading,
                )


def test_heading_voice_keeps_reusable_sections_without_becoming_a_template() -> None:
    for language in ("en", "zh"):
        headings = _corpus_headings(language)
        assert headings
        unique_share = len(set(headings)) / len(headings)
        assert unique_share <= MAX_UNIQUE_HEADING_SHARE, (
            language,
            f"{unique_share:.1%} of H2 headings are unique; stable editorial "
            f"sections must keep the share at or below "
            f"{MAX_UNIQUE_HEADING_SHARE:.0%}",
        )


def test_heading_voice_limits_command_contrast_and_count_formulas() -> None:
    for language in ("en", "zh"):
        headings = _corpus_headings(language)
        imperative_share = _share(headings, IMPERATIVE_RE[language])
        negated_share = _share(headings, NEGATED_CONTRAST_RE[language])
        count_share = _share(headings, COUNT_SLOGAN_RE[language])

        assert imperative_share <= MAX_IMPERATIVE_SHARE[language], (
            language,
            f"imperative H2 share {imperative_share:.1%} exceeds "
            f"{MAX_IMPERATIVE_SHARE[language]:.0%}",
        )
        assert negated_share <= MAX_NEGATED_CONTRAST_SHARE, (
            language,
            f"negated-contrast H2 share {negated_share:.1%} exceeds "
            f"{MAX_NEGATED_CONTRAST_SHARE:.0%}",
        )
        assert count_share <= MAX_COUNT_SLOGAN_SHARE, (
            language,
            f"count-led H2 share {count_share:.1%} exceeds "
            f"{MAX_COUNT_SLOGAN_SHARE:.0%}",
        )
