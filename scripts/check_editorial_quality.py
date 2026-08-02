from __future__ import annotations

import argparse
import difflib
import re
import subprocess
import sys
import unicodedata
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence
from urllib.parse import urlsplit, urlunsplit

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.quality_common import (
    Issue,
    QualityError,
    REPO_ROOT,
    display_path,
    emit_issues,
    exit_code,
    load_json,
    markdown_headings,
    write_json_report,
)


ZH_DEPTH_MINIMUM = 320
EN_DEPTH_MINIMUM = 180
ZH_DEPTH_MAXIMUM = 1_400
EN_DEPTH_MAXIMUM = 900
NARRATIVE_LINK_MINIMUM = 3
NARRATIVE_LINK_MAXIMUM = 9
ZH_PROSE_PER_LINK_MINIMUM = 40
EN_PROSE_PER_LINK_MINIMUM = 20

ZH_PARAGRAPH_MINIMUM = 80
EN_PARAGRAPH_MINIMUM = 45
ZH_EXACT_PARAGRAPH_MINIMUM = 100
EN_EXACT_PARAGRAPH_MINIMUM = 60
FUZZY_PARAGRAPH_THRESHOLD = 0.88
FUZZY_PARAGRAPH_ERROR_COUNT = 2
ZH_SENTENCE_MINIMUM = 35
EN_SENTENCE_MINIMUM = 20
FUZZY_SENTENCE_THRESHOLD = 0.90
FUZZY_SENTENCE_ERROR_COUNT = 3
FUZZY_NGRAM_CANDIDATE_THRESHOLD = 0.40
INTRA_DOCUMENT_SENTENCE_REPEAT_ERROR_COUNT = 3

CONCRETE_ANCHOR_MINIMUM = 3
CONCRETE_ANCHOR_CATEGORY_MINIMUM = 2
GENERIC_WARNING_COUNT = 2
GENERIC_ERROR_COUNT = 4
GENERIC_ERROR_RATIO = 0.10

NUMBER_PARITY_WARNING_THRESHOLD = 0.85
TERM_PARITY_WARNING_THRESHOLD = 0.80
TERM_PARITY_ERROR_THRESHOLD = 0.65
LENGTH_RATIO_WARNING_MINIMUM = 0.35
LENGTH_RATIO_WARNING_MAXIMUM = 1.10
LENGTH_RATIO_ERROR_MINIMUM = 0.25
LENGTH_RATIO_ERROR_MAXIMUM = 1.25
# A single missing paragraph can erase a caveat, project boundary, or source
# note while leaving headings, URLs, and whole-document length ratios intact.
# Course-guide translations therefore keep a one-to-one substantive paragraph
# structure. Translators may still reshape sentences inside a paragraph.
PARAGRAPH_COUNT_DELTA_ERROR = 1
PARAGRAPH_ALIGNMENT_ZH_MINIMUM = 60
PARAGRAPH_LENGTH_RATIO_ERROR_MINIMUM = 0.45
PARAGRAPH_LENGTH_RATIO_ERROR_MAXIMUM = 1.75
SECTION_LENGTH_RATIO_ERROR_MINIMUM = 0.50
SECTION_LENGTH_RATIO_ERROR_MAXIMUM = 1.40

CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
LATIN_WORD_RE = re.compile(r"\b[A-Za-z][A-Za-z0-9'+.-]*\b")
RAW_HTTPS_RE = re.compile(r"""https://[^\s<>()"']+""", re.IGNORECASE)
MARKDOWN_LINK_RE = re.compile(
    r"(?<!!)\[([^\]]+)]\(\s*(https://[^)\s]+)(?:\s+[\"'][^\"']*[\"'])?\s*\)",
    re.IGNORECASE,
)
AUTOLINK_RE = re.compile(r"<(https://[^>\s]+)>", re.IGNORECASE)
HTML_TAG_RE = re.compile(r"<[^>]+>")
INLINE_MARKUP_RE = re.compile(r"[`*_~]")
LIST_MARKER_RE = re.compile(r"^\s*(?:[-+*]|\d+[.)])\s+")
FENCE_RE = re.compile(r"^\s*(```+|~~~+)")
TABLE_RE = re.compile(r"^\s*\|")

NUMBER_RE = re.compile(
    r"(?<![A-Za-z])\d+(?:\.\d+)?(?:\s*[–—-]\s*\d+(?:\.\d+)?)?%?"
)
PERCENT_RE = re.compile(
    r"(?<![\w.])(\d+(?:\.\d+)?)\s*(?:%|percent\b|per\s+cent\b)",
    re.IGNORECASE,
)
YEAR_RE = re.compile(r"(?<!\d)(?:19|20)\d{2}(?!\d)")
PROTECTED_TERM_RE = re.compile(r"\b[A-Za-z][A-Za-z0-9+.#]*(?:[-/][A-Za-z0-9+.#]+)*\b")

FIRST_HAND_ZH_RE = re.compile(
    r"(?:我|本人)(?:学过|学完|上过|做过|完成过|踩过|花了|使用过)"
)
FIRST_HAND_EN_RE = re.compile(
    r"\bI\s+(?:took|studied|completed|built|spent|used|learned)\b",
    re.IGNORECASE,
)

GENERIC_ZH_RE = re.compile(
    r"(?:"
    r"系统(?:性|地)?(?:学习|掌握|理解)?|"
    r"全面(?:地|覆盖|掌握|理解)?|"
    r"深入(?:地)?(?:理解|掌握|探索)|"
    r"(?:打下|奠定)(?:坚实|良好)?(?:的)?基础|"
    r"坚实(?:的)?基础|非常适合|值得推荐|不容错过|"
    r"优质课程|高质量课程|内容丰富|循序渐进|从零到一|轻松掌握|"
    r"提升[^。！？；]{0,12}能力|拓宽[^。！？；]{0,12}视野|"
    r"无论你是|相信(?:你|学习者)|总而言之|总的来说|"
    r"值得一提的是?|极大地|帮助你"
    r")"
)
GENERIC_EN_RE = re.compile(
    r"\b(?:"
    r"comprehensive|systematic(?:ally)?|in-depth|solid foundation|"
    r"well-structured|excellent|high-quality|ideal|perfect|well-suited|"
    r"valuable learning experience|help you|whether you are|overall|"
    r"it is worth noting|deep understanding|master(?:y)?|unlock|journey"
    r")\b",
    re.IGNORECASE,
)
# In the first editorial batches, dozens of literal translations used
# “repair probability / repair linear algebra” as a generic prerequisite
# instruction. The repetition read like machine-translated workflow jargon,
# not natural technical English. Keep this narrow corpus-level guard even
# though “repair” can be valid in other contexts; a course guide can always
# name the concrete action (review, revisit, debug, fix, or re-derive).
TRANSLATIONESE_EN_RE = re.compile(
    r"(?:\brepair(?:ing|ed)?\s+(?:linear algebra|calculus|probability|signals?|"
    r"prerequisites?|background|gaps?)\b|\brepair\s+around\b)",
    re.IGNORECASE,
)
FAKE_REVIEWER_RE = {
    "zh": re.compile(r"(?:我会|我将)(?:检查|找|寻找|核对|验收|评分)"),
    "en": re.compile(
        r"\bI(?:'ll| will| would)\s+(?:check|look for|verify|grade|assess)\b",
        re.IGNORECASE,
    ),
}
DEFENSIVE_NEGATION_ZH_RE = re.compile(r"(?:不是|不等于|而不是)")
DIRECTIVE_ZH_RE = re.compile(r"(?:必须|不要|应当)")
SEQUENCED_WORKFLOW_ZH_RE = re.compile(
    r"先[^。！？\n]{0,120}再[^。！？\n]{0,120}最后"
)
OPENING_DECISION_RE = {
    "zh": re.compile(
        r"(?:适合|不适合|值得|推荐|首选|优先|选|换成|改选|"
        r"如果|若|想要|需要|用作|定位|主线|替代|价值|结论)"
    ),
    "en": re.compile(
        r"\b(?:fit|fits|suit|suits|suited|best|worth|value|recommend|prefer|"
        r"choose|choosing|instead|alternative|if|want|need|should|use as|"
        r"main course|first course|verdict|right|complete|offers|both)\b",
        re.IGNORECASE,
    ),
}
COMPARISON_RE = re.compile(
    r"(?:相比|不同于|区别|不是.+而是|优先|再选|可选|"
    r"\bcompared\b|\bunlike\b|\brather than\b|\bversus\b|\bvs\.?\b|"
    r"\bchoose\b|\bprefer\b)",
    re.IGNORECASE,
)

NUMBER_WORDS = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "ten": "10",
    "eleven": "11",
    "twelve": "12",
    "thirteen": "13",
    "fourteen": "14",
    "fifteen": "15",
    "sixteen": "16",
    "seventeen": "17",
    "eighteen": "18",
    "nineteen": "19",
    "twenty": "20",
}
NUMBER_WORD_RE = re.compile(
    r"\b(" + "|".join(sorted(NUMBER_WORDS, key=len, reverse=True)) + r")\b",
    re.IGNORECASE,
)

STRUCTURE_KIND = (
    r"lecture|lec|unit|module|chapter|session|week|recitation|tutorial|"
    r"讲|单元|章节|章|周|习题课|辅导课"
)
ASSESSMENT_KIND = (
    r"problem\s*sets?|psets?|homeworks?|assignments?|assessments?|"
    r"quizzes?|exams?|finals?|ps|hw|习题|作业|测验|考试|考核"
)
PRACTICE_KIND = (
    r"labs?|laborator(?:y|ies)|projects?|checkpoints?|design\s*reviews?|"
    r"实验|项目|检查点|设计评审"
)
NUMBERED_ARTIFACT_RE = re.compile(
    rf"\b(?P<kind>{STRUCTURE_KIND}|{ASSESSMENT_KIND}|{PRACTICE_KIND})"
    rf"\s*(?:#|no\.?)?\s*(?P<identifier>\d+(?:\.\d+)?"
    rf"(?:\s*[–—-]\s*\d+(?:\.\d+)?)?|[A-Z]{{2,}}\d*)",
    re.IGNORECASE,
)
COUNTED_ARTIFACT_RE = re.compile(
    rf"(?P<count>\d+|{'|'.join(NUMBER_WORDS)})\s*(?:份|次|套|个|组|条)?\s*"
    rf"(?P<kind>{STRUCTURE_KIND}|{ASSESSMENT_KIND}|{PRACTICE_KIND})\b",
    re.IGNORECASE,
)
ZH_NUMBERED_ARTIFACT_RE = re.compile(
    r"(?:第\s*)?(?P<identifier>[一二三四五六七八九十百\d]+"
    r"(?:\s*[–—-]\s*[一二三四五六七八九十百\d]+)?)\s*"
    r"(?P<kind>讲|单元|章|周|份作业|套题|次测验|次考试|个实验|个项目)"
)
RESOURCE_LABEL_RE = re.compile(
    rf"\b(?:{STRUCTURE_KIND}|{ASSESSMENT_KIND}|{PRACTICE_KIND}|"
    r"syllabus|calendar|notes?|videos?|solutions?|resource\s*index)\b",
    re.IGNORECASE,
)
LIMIT_RE = re.compile(
    r"(?:"
    r"版本|年代|过时|旧版|失效|重定向|限制|登录|付费|收费|"
    r"公开|未公开|不公开|没有(?:官方|公开)?(?:答案|解答|视频|代码|grader)|"
    r"答案|解答|反馈|访问|许可|地区|工具链|器件停产|"
    r"\bversion\b|\bdated\b|\blegacy\b|\boutdated\b|\bbroken\b|"
    r"\bunavailable\b|\baccess\b|\blogin\b|\bpaywall\b|\bpaid\b|"
    r"\bpublic\b|\bsolutions?\b|\bfeedback\b|\bgrader\b|"
    r"\blicen[cs]e\b|\bregion\b|\bmissing\b|\bredirect"
    r")",
    re.IGNORECASE,
)

SOURCE_CUE_ZH_RE = re.compile(
    r"(?:官方|提供方|课程主页|课程首页|课程页|课程网站|"
    r"syllabus|calendar|resource\s*index|官方仓库|官方说明|官方列出|"
    r"(?:MIT|Cornell|Stanford)\s*(?:报告|列出|说明|提供|写明))",
    re.IGNORECASE,
)
SOURCE_CUE_EN_RE = re.compile(
    r"(?:\bofficial\b|\bprovider\b|\bsyllabus\b|\bcourse\s+(?:home|page|site)\b|"
    r"\bcalendar\b|\bresource\s+index\b|\bofficial\s+repository\b|"
    r"\bMIT\s+(?:reports|lists|states|provides)\b)",
    re.IGNORECASE,
)
NEGATIVE_OFFICIAL_RE = re.compile(
    r"(?:不是|并非|而非|非)\s*官方|\b(?:not|non-)\s+official\b",
    re.IGNORECASE,
)
EDITORIAL_CUE_ZH_RE = re.compile(
    r"(?:EEDIY|编辑(?:据此)?|建议|优先|可选|应当|不应|不要|"
    r"可以|可先|不得|必须|适合|不适合|值得|首选|选择|改选|换成|"
    r"独立学习时|自学时|更实际的诊断|"
    r"更有效的读法|更好的学习顺序)"
)
EDITORIAL_CUE_EN_RE = re.compile(
    r"(?:\bEEDIY\b|\beditorial\b|\bmaintainer\b|\brecommend\b|\bshould\b|"
    r"\bprefer\b|\bchoose\b|\bfit(?:s|ted)?\b|\bsuit(?:s|ed)?\b|\bworth\b|"
    r"\bbest\b|\bdo not\b|\bshould not\b|"
    r"\bfor independent study\b|\ban independent learner\b)",
    re.IGNORECASE,
)
HIGH_RISK_FACT_RE = re.compile(
    rf"(?:"
    rf"\b(?:\d+|{'|'.join(NUMBER_WORDS)})\s*(?:份|次|套|个|组|条)?\s*"
    rf"(?:{STRUCTURE_KIND}|{ASSESSMENT_KIND}|{PRACTICE_KIND})\b|"
    r"\d+(?:\.\d+)?\s*(?:%|percent\b|per\s+cent\b)|"
    r"(?:官方|正式|课程|当前)?先修(?:是|为|要求|写成|列为)|"
    r"\bprerequisites?\b\s*(?:are|is|include|require|list)|"
    r"\d+(?:\.\d+)?\s*(?:hours?|小时|weeks?|周)\b|"
    r"(?:19|20)\d{2}[^。.!?；;]{0,32}"
    r"(?:版本|学期|课程(?:是|为|使用|没有|提供)|材料(?:是|为|使用|没有|提供)|"
    r"录制(?:于|自)|工具(?:是|为|使用)|version\s+(?:is|uses|has)|"
    r"term\s+(?:is|uses|has)|course\s+(?:is|uses|has)|"
    r"material\s+(?:is|uses|has)|recorded\s+in|tool\s+(?:is|uses|has))|"
    r"(?:没有|无|未|不)(?:公开|提供|列出)?"
    r"(?:答案|解答|视频|代码|实验|考试|grader)|"
    r"\b(?:no|not)\s+(?:official|public|complete)?\s*"
    r"(?:solutions?|videos?|code|labs?|exams?|grader)\b"
    r")",
    re.IGNORECASE,
)
SUPPLEMENT_TASK_RE = re.compile(
    r"(?:"
    r"(?:若需实践|独立学习者|外部学习者|自学者|EEDIY|维护者)"
    r"[^。！？；]{0,35}(?:可|可以|建议|另做|自建|补充)"
    r"[^。！？；]{0,35}(?:notebook|项目|实验|作业|模拟|实现|搭建|产物|报告)|"
    r"(?:自建|另做|补充任务)\s*[^。！？；]{0,36}"
    r"(?:notebook|项目|实验|作业|模拟|实现|搭建)|"
    r"\b(?:learner|independent study|EEDIY|maintainer)\b"
    r"[^.!?;]{0,40}\b(?:can|may|could|should|suggests?)\b"
    r"[^.!?;]{0,45}\b(?:create|add|build|design|simulate|implement)\b"
    r"[^.!?;]{0,45}\b(?:notebook|project|lab|assignment|exercise|artifact)\b|"
    r"\bmaintainer-suggested\b"
    r")",
    re.IGNORECASE,
)
SUPPLEMENT_BOUNDARY_RE = re.compile(
    r"(?:"
    r"EEDIY[^。！？；]{0,50}(?:补充|建议|替代)|"
    r"(?:不是|并非|而非|非)\s*(?:课程|MIT|提供方)?官方"
    r"[^。！？；]{0,20}(?:作业|实验|项目|任务|要求)?|"
    r"(?:课程|提供方)?没有官方(?:编程)?(?:作业|实验|项目|任务)|"
    r"\bEEDIY\s+(?:supplement|substitution|migration)\b|"
    r"\bmaintainer-suggested\b|"
    r"\bnot\s+an?\s+official\b|\bnot\s+official\b"
    r")",
    re.IGNORECASE,
)
NO_PUBLIC_COURSEWORK_RE = {
    "zh": re.compile(
        r"(?:没有|未|无|不)(?:公开|提供|列出)?"
        r"[^。！？；]{0,60}(?:assignments?|starter|rubric|staff feedback|"
        r"作业|实验|项目|考试|评分标准|教师反馈)",
        re.IGNORECASE,
    ),
    "en": re.compile(
        r"(?:"
        r"(?:no|not|without)\s+(?:current\s+|public\s+|official\s+|complete\s+)*"
        r"(?:assignments?|labs?|projects?|exams?|starter(?:\s+files?)?|rubrics?|"
        r"staff feedback)|"
        r"(?:assignments?|labs?|projects?|exams?|starter(?:\s+files?)?|rubrics?|"
        r"staff feedback)[^.!?;]{0,55}"
        r"(?:remain|are|is)\s+(?:outside|absent|unpublished|unavailable)"
        r")",
        re.IGNORECASE,
    ),
}
INDEPENDENT_PROJECT_MAP_RE = {
    "zh": re.compile(
        r"(?:独立(?:自学)?项目|独立练习|项目地图)"
        r"[^。！？；]{0,100}"
        r"(?:不是|并非|不属于|区别于)"
        r"[^。！？；]{0,45}"
        r"(?:官方|课程|作业|实验|submission|Illinois)",
        re.IGNORECASE,
    ),
    "en": re.compile(
        r"(?:independent (?:self-study )?(?:projects?|exercises?|project map)|"
        r"project map)"
        r"[^.!?;]{0,120}"
        r"(?:not|do not|does not)"
        r"[^.!?;]{0,55}"
        r"(?:official|coursework|submission|assignments?|labs?|recreate)",
        re.IGNORECASE,
    ),
}

PROTECTED_TERM_IGNORE = {
    "a",
    "an",
    "and",
    "course",
    "courses",
    "eediY".casefold(),
    "en",
    "http",
    "https",
    "lab",
    "labs",
    "lecture",
    "lectures",
    "mit",
    "no",
    "notes",
    "ocw",
    "pdf",
    "problem",
    "project",
    "projects",
    "ps",
    "r0",
    "or",
    "set",
    "the",
    "unit",
    "url",
    "zh",
}


@dataclass(frozen=True)
class GuideDocument:
    course_id: int
    language: str
    path: Path
    text: str
    metadata: Mapping[str, Any]
    primary_sources: tuple[str, ...]
    evidence_level: str


@dataclass(frozen=True)
class GuidePair:
    course_id: int
    zh: GuideDocument
    en: GuideDocument


@dataclass(frozen=True)
class Segment:
    text: str
    normalized: str
    line: int
    section: int
    units: int


@dataclass(frozen=True)
class ConcreteAnchor:
    category: str
    key: str
    line: int
    paragraph_index: int


@dataclass(frozen=True)
class BodyAnalysis:
    document: GuideDocument
    visible_units: int
    external_links: tuple[str, ...]
    heading_levels: tuple[int, ...]
    paragraphs: tuple[Segment, ...]
    eligible_paragraphs: tuple[Segment, ...]
    eligible_sentences: tuple[Segment, ...]
    anchors: tuple[ConcreteAnchor, ...]
    generic_sentences: tuple[Segment, ...]
    link_only_paragraphs: tuple[Segment, ...]


def _normalize_url(value: str) -> str:
    value = value.rstrip(".,;:!?，。；：！？")
    parsed = urlsplit(value)
    path = parsed.path.rstrip("/") or "/"
    return urlunsplit(
        (
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            path,
            parsed.query,
            "",
        )
    )


def _external_links(text: str) -> tuple[str, ...]:
    return tuple(sorted({_normalize_url(match.group(0)) for match in RAW_HTTPS_RE.finditer(text)}))


def _replace_links_with_labels(text: str) -> str:
    text = MARKDOWN_LINK_RE.sub(lambda match: match.group(1), text)
    text = AUTOLINK_RE.sub(" ", text)
    text = RAW_HTTPS_RE.sub(" ", text)
    return text


def _visible_text(text: str) -> str:
    text = _replace_links_with_labels(text)
    text = HTML_TAG_RE.sub(" ", text)
    text = INLINE_MARKUP_RE.sub("", text)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    return re.sub(r"\s+", " ", text).strip()


def _visible_units(text: str, language: str) -> int:
    visible = _visible_text(text)
    if language == "zh":
        return len(CJK_RE.findall(visible))
    return len(LATIN_WORD_RE.findall(visible))


def _metadata_values(document: GuideDocument) -> list[str]:
    values = [str(document.course_id), f"{document.course_id:03d}"]
    for key in ("title", "institution", "course_code", "slug", "track"):
        value = document.metadata.get(key)
        if isinstance(value, Mapping):
            values.extend(str(item) for item in value.values())
        elif isinstance(value, str):
            values.append(value)
    return sorted(
        {value.strip() for value in values if len(value.strip()) >= 2},
        key=len,
        reverse=True,
    )


def _normalize_for_duplication(text: str, document: GuideDocument) -> str:
    normalized = _replace_links_with_labels(text)
    for value in _metadata_values(document):
        normalized = re.sub(re.escape(value), " COURSE ", normalized, flags=re.IGNORECASE)
    normalized = NUMBER_WORD_RE.sub(
        lambda match: f" {NUMBER_WORDS[match.group(1).casefold()]} ",
        normalized,
    )
    normalized = NUMBER_RE.sub(" NUMBER ", normalized)
    normalized = unicodedata.normalize("NFKC", normalized).casefold()
    normalized = re.sub(
        r"[^\w\u3400-\u4dbf\u4e00-\u9fff]+",
        " ",
        normalized,
    )
    return re.sub(r"\s+", " ", normalized).strip()


def _raw_paragraphs(document: GuideDocument) -> list[tuple[str, int, int]]:
    paragraphs: list[tuple[str, int, int]] = []
    buffer: list[str] = []
    start_line = 1
    section = 0
    buffer_section = 0
    fence: str | None = None
    in_comment = False

    def flush() -> None:
        nonlocal buffer
        if buffer:
            paragraphs.append((" ".join(buffer).strip(), start_line, buffer_section))
            buffer = []

    for line_number, raw in enumerate(document.text.splitlines(), 1):
        stripped = raw.strip()
        fence_match = FENCE_RE.match(raw)
        if fence_match:
            flush()
            marker = fence_match.group(1)[0]
            fence = None if fence == marker else marker
            continue
        if fence is not None:
            continue
        if "<!--" in stripped:
            flush()
            in_comment = True
        if in_comment:
            if "-->" in stripped:
                in_comment = False
            continue
        if re.match(r"^##\s+", stripped):
            flush()
            section += 1
            continue
        if re.match(r"^#{1,6}\s+", stripped) or TABLE_RE.match(raw):
            flush()
            continue
        if not stripped or stripped in {"<details>", "</details>", "<summary>", "</summary>"}:
            flush()
            continue
        if not buffer:
            start_line = line_number
            buffer_section = section
        cleaned = LIST_MARKER_RE.sub("", stripped)
        cleaned = re.sub(r"^\s*>\s?", "", cleaned)
        buffer.append(cleaned)
    flush()
    return paragraphs


def _sentence_segments(
    paragraph: Segment,
    document: GuideDocument,
) -> list[Segment]:
    if document.language == "zh":
        pieces = re.split(r"(?<=[。！？；])", paragraph.text)
    else:
        pieces = re.split(r"(?<=[.!?;])\s+(?=[A-Z0-9\[])|\n+", paragraph.text)
    output: list[Segment] = []
    for piece in pieces:
        piece = piece.strip()
        if not piece:
            continue
        units = _visible_units(piece, document.language)
        minimum = ZH_SENTENCE_MINIMUM if document.language == "zh" else EN_SENTENCE_MINIMUM
        if units < minimum:
            continue
        output.append(
            Segment(
                piece,
                _normalize_for_duplication(piece, document),
                paragraph.line,
                paragraph.section,
                units,
            )
        )
    return output


def _artifact_category(kind: str) -> str:
    lowered = kind.casefold()
    if re.search(ASSESSMENT_KIND, lowered, re.IGNORECASE):
        return "assessment"
    if re.search(PRACTICE_KIND, lowered, re.IGNORECASE):
        return "practice"
    return "structure"


def _protected_terms(text: str) -> set[str]:
    output: set[str] = set()
    for match in PROTECTED_TERM_RE.finditer(_replace_links_with_labels(text)):
        value = match.group(0)
        parts = value.split("/") if "/" in value else [value]
        for part in parts:
            letters = "".join(character for character in part if character.isalpha())
            informative = (
                len(parts) > 1
                or any(character.isdigit() for character in part)
                or "-" in part
                or (len(letters) >= 2 and letters.upper() == letters)
            )
            folded = part.casefold()
            if informative and folded not in PROTECTED_TERM_IGNORE:
                output.add(folded)
    return output


def _anchors_for_paragraph(
    paragraph: Segment,
    paragraph_index: int,
) -> list[ConcreteAnchor]:
    anchors: dict[tuple[str, str], ConcreteAnchor] = {}

    def add(category: str, key: str) -> None:
        normalized = re.sub(r"\s+", " ", unicodedata.normalize("NFKC", key).casefold()).strip()
        if normalized:
            anchors[(category, normalized)] = ConcreteAnchor(
                category,
                normalized,
                paragraph.line,
                paragraph_index,
            )

    for match in NUMBERED_ARTIFACT_RE.finditer(paragraph.text):
        add(_artifact_category(match.group("kind")), match.group(0))
    for match in COUNTED_ARTIFACT_RE.finditer(paragraph.text):
        add(_artifact_category(match.group("kind")), match.group(0))
    for match in ZH_NUMBERED_ARTIFACT_RE.finditer(paragraph.text):
        add(_artifact_category(match.group("kind")), match.group(0))
    for match in MARKDOWN_LINK_RE.finditer(paragraph.text):
        label = match.group(1)
        resource = RESOURCE_LABEL_RE.search(label)
        if resource:
            add(_artifact_category(resource.group(0)), f"{label} {match.group(2)}")
    for term in _protected_terms(paragraph.text):
        add("topic-tool", term)
    if LIMIT_RE.search(paragraph.text):
        match = LIMIT_RE.search(paragraph.text)
        assert match is not None
        add("version-access-feedback", match.group(0))
    return sorted(anchors.values(), key=lambda item: (item.category, item.key))


def _has_concrete_context(text: str) -> bool:
    if NUMBER_RE.search(text) or RAW_HTTPS_RE.search(text) or COMPARISON_RE.search(text):
        return True
    placeholder = Segment(text, "", 1, 0, 0)
    anchors = _anchors_for_paragraph(placeholder, 0)
    return any(anchor.category != "version-access-feedback" for anchor in anchors)


def analyze_document(document: GuideDocument) -> BodyAnalysis:
    paragraphs: list[Segment] = []
    anchors: list[ConcreteAnchor] = []
    sentences: list[Segment] = []
    link_only: list[Segment] = []
    paragraph_minimum = (
        ZH_PARAGRAPH_MINIMUM if document.language == "zh" else EN_PARAGRAPH_MINIMUM
    )
    link_only_limit = 20 if document.language == "zh" else 10

    for index, (raw, line, section) in enumerate(_raw_paragraphs(document)):
        units = _visible_units(raw, document.language)
        segment = Segment(
            raw,
            _normalize_for_duplication(raw, document),
            line,
            section,
            units,
        )
        paragraphs.append(segment)
        anchors.extend(_anchors_for_paragraph(segment, index))
        sentences.extend(_sentence_segments(segment, document))
        if RAW_HTTPS_RE.search(raw) and units <= link_only_limit:
            link_only.append(segment)

    eligible_paragraphs = tuple(
        paragraph for paragraph in paragraphs if paragraph.units >= paragraph_minimum
    )
    generic_pattern = GENERIC_ZH_RE if document.language == "zh" else GENERIC_EN_RE
    generic_sentences = tuple(
        sentence
        for sentence in sentences
        if generic_pattern.search(sentence.text) and not _has_concrete_context(sentence.text)
    )
    unique_anchors = {
        (anchor.category, anchor.key): anchor
        for anchor in anchors
    }
    return BodyAnalysis(
        document=document,
        visible_units=_visible_units(document.text, document.language),
        external_links=_external_links(document.text),
        heading_levels=tuple(
            level for level, _, _ in markdown_headings(document.text)
        ),
        paragraphs=tuple(paragraphs),
        eligible_paragraphs=eligible_paragraphs,
        eligible_sentences=tuple(sentences),
        anchors=tuple(
            sorted(
                unique_anchors.values(),
                key=lambda item: (item.category, item.key, item.line),
            )
        ),
        generic_sentences=generic_sentences,
        link_only_paragraphs=tuple(link_only),
    )


def _source_cue(text: str, document: GuideDocument) -> bool:
    without_negative = NEGATIVE_OFFICIAL_RE.sub(" ", text)
    pattern = SOURCE_CUE_ZH_RE if document.language == "zh" else SOURCE_CUE_EN_RE
    if pattern.search(without_negative):
        return True
    links = set(_external_links(text))
    sources = {_normalize_url(url) for url in document.primary_sources}
    if links & sources:
        return True
    link_hosts = {urlsplit(url).netloc.casefold() for url in links}
    source_hosts = {urlsplit(url).netloc.casefold() for url in sources}
    return bool(link_hosts & source_hosts)


def _source_window(
    analysis: BodyAnalysis,
    paragraph_index: int,
) -> bool:
    paragraph = analysis.paragraphs[paragraph_index]
    # A numbered diagnostic list may sit between a source sentence and the
    # prose that interprets it. Four prose blocks keeps the cue local while
    # avoiding a false failure caused only by Markdown list segmentation.
    for candidate_index in range(
        max(0, paragraph_index - 4),
        min(len(analysis.paragraphs), paragraph_index + 5),
    ):
        candidate = analysis.paragraphs[candidate_index]
        if candidate.section != paragraph.section:
            continue
        if _source_cue(candidate.text, analysis.document):
            return True
    return False


def _repeated_sentence_issues(analysis: BodyAnalysis) -> list[Issue]:
    """Catch sentence-loop padding inside one guide.

    Fenced code and Markdown tables never enter ``eligible_sentences``. Skip
    common display-math forms as an additional guard so repeated equations are
    not mistaken for repeated prose.
    """

    buckets: dict[str, list[Segment]] = {}
    for sentence in analysis.eligible_sentences:
        stripped = sentence.text.lstrip()
        if stripped.startswith(("$$", r"\[", r"\begin{")):
            continue
        if not sentence.normalized:
            continue
        buckets.setdefault(sentence.normalized, []).append(sentence)

    issues: list[Issue] = []
    for entries in buckets.values():
        if len(entries) < INTRA_DOCUMENT_SENTENCE_REPEAT_ERROR_COUNT:
            continue
        first = entries[0]
        issues.append(
            Issue(
                "error",
                "editorial.repeated_sentence",
                f"the same normalized narrative sentence appears {len(entries)} "
                "times in one guide; replace sentence-loop padding with distinct "
                "course-specific analysis",
                display_path(analysis.document.path),
                first.line,
                first.text[:220],
            )
        )
    return issues


def _document_issues(analysis: BodyAnalysis) -> list[Issue]:
    document = analysis.document
    relative = display_path(document.path)
    issues: list[Issue] = []
    depth_minimum = ZH_DEPTH_MINIMUM if document.language == "zh" else EN_DEPTH_MINIMUM
    depth_maximum = ZH_DEPTH_MAXIMUM if document.language == "zh" else EN_DEPTH_MAXIMUM
    unit_label = "CJK characters" if document.language == "zh" else "English words"
    if analysis.visible_units < depth_minimum:
        issues.append(
            Issue(
                "error",
                "editorial.depth",
                f"researched guide has {analysis.visible_units} visible {unit_label}; "
                f"minimum is {depth_minimum}",
                relative,
            )
        )
    if analysis.visible_units > depth_maximum:
        issues.append(
            Issue(
                "error",
                "editorial.sprawl",
                f"researched guide has {analysis.visible_units} visible {unit_label}; "
                f"maximum is {depth_maximum}. Move exhaustive schedules, general "
                "safety rules, and tool-migration procedures to companion guides.",
                relative,
            )
        )
    issues.extend(_repeated_sentence_issues(analysis))

    if analysis.paragraphs:
        opening = analysis.paragraphs[0]
        opening_limit = 160 if document.language == "zh" else 90
        first_h2 = next(
            (
                title
                for level, title, _ in markdown_headings(document.text)
                if level == 2
            ),
            "",
        )
        opening_text = f"{first_h2} {opening.text}"
        opening_excerpt = (
            "".join(CJK_RE.findall(opening_text))[:opening_limit]
            if document.language == "zh"
            else " ".join(LATIN_WORD_RE.findall(opening_text)[:opening_limit])
        )
        if not OPENING_DECISION_RE[document.language].search(opening_excerpt):
            issues.append(
                Issue(
                    "error",
                    "editorial.late_judgment",
                    "the opening paragraph must quickly tell the learner who this "
                    "course fits, why it is worth taking, or when to choose an "
                    "alternative",
                    relative,
                    opening.line,
                    opening.text[:220],
                )
            )

    link_count = len(analysis.external_links)
    if not NARRATIVE_LINK_MINIMUM <= link_count <= NARRATIVE_LINK_MAXIMUM:
        issues.append(
            Issue(
                "error",
                "editorial.narrative_links",
                f"narrative requires {NARRATIVE_LINK_MINIMUM}–"
                f"{NARRATIVE_LINK_MAXIMUM} unique HTTPS links; found {link_count}",
                relative,
            )
        )
    if link_count:
        density = analysis.visible_units / link_count
        density_minimum = (
            ZH_PROSE_PER_LINK_MINIMUM
            if document.language == "zh"
            else EN_PROSE_PER_LINK_MINIMUM
        )
        if density < density_minimum:
            issues.append(
                Issue(
                    "error",
                    "editorial.link_density",
                    f"only {density:.1f} visible {unit_label} per narrative link; "
                    f"minimum is {density_minimum}",
                    relative,
                )
            )
    link_only_count = len(analysis.link_only_paragraphs)
    paragraph_share = link_only_count / max(1, len(analysis.paragraphs))
    if link_only_count > 2 or paragraph_share > 0.20:
        first = analysis.link_only_paragraphs[0] if analysis.link_only_paragraphs else None
        issues.append(
            Issue(
                "error",
                "editorial.link_wall",
                f"{link_only_count} link-only paragraphs occupy {paragraph_share:.0%} "
                "of prose; explain why each narrative link matters",
                relative,
                first.line if first else None,
                first.text[:180] if first else "",
            )
        )

    fake_reviewer = FAKE_REVIEWER_RE[document.language].search(document.text)
    if fake_reviewer:
        issues.append(
            Issue(
                "error",
                "editorial.fake_reviewer_voice",
                "an uncredited guide must not speak as an imagined grader or "
                "reviewer; state the observable course artifact directly",
                relative,
                document.text.count("\n", 0, fake_reviewer.start()) + 1,
                fake_reviewer.group(0),
            )
        )
    if document.language == "zh":
        defensive_count = len(DEFENSIVE_NEGATION_ZH_RE.findall(document.text))
        if defensive_count > 2:
            issues.append(
                Issue(
                    "error",
                    "editorial.defensive_voice",
                    f"guide uses {defensive_count} defensive negations "
                    "(不是/不等于/而不是); maximum is 2",
                    relative,
                )
            )
        directive_count = len(DIRECTIVE_ZH_RE.findall(document.text))
        if directive_count > 5:
            issues.append(
                Issue(
                    "error",
                    "editorial.command_voice",
                    f"guide uses {directive_count} directive terms "
                    "(必须/不要/应当); maximum is 5",
                    relative,
                )
            )
        workflow_count = len(SEQUENCED_WORKFLOW_ZH_RE.findall(document.text))
        if workflow_count > 1:
            issues.append(
                Issue(
                    "error",
                    "editorial.workflow_template",
                    f"guide contains {workflow_count} separate 先—再 workflows; "
                    "maximum is 1 unless the provider defines that sequence",
                    relative,
                )
            )

    anchor_categories = {anchor.category for anchor in analysis.anchors}
    if (
        len(analysis.anchors) < CONCRETE_ANCHOR_MINIMUM
        or len(anchor_categories) < CONCRETE_ANCHOR_CATEGORY_MINIMUM
    ):
        issues.append(
            Issue(
                "error",
                "editorial.specificity",
                f"found {len(analysis.anchors)} distinct courseware anchors across "
                f"{len(anchor_categories)} categories; require at least "
                f"{CONCRETE_ANCHOR_MINIMUM} anchors across "
                f"{CONCRETE_ANCHOR_CATEGORY_MINIMUM} categories",
                relative,
                context="categories: " + ", ".join(sorted(anchor_categories)),
            )
        )
    official_artifact = any(
        anchor.category in {"assessment", "practice"}
        and _source_window(analysis, anchor.paragraph_index)
        for anchor in analysis.anchors
    )
    catalogue_only_map = (
        bool(NO_PUBLIC_COURSEWORK_RE[document.language].search(document.text))
        and bool(INDEPENDENT_PROJECT_MAP_RE[document.language].search(document.text))
        and _source_cue(document.text, document)
    )
    if not official_artifact and not catalogue_only_map:
        issues.append(
            Issue(
                "error",
                "editorial.real_coursework",
                "no assignment, lab, project, or exam anchor is tied to an "
                "official cue or primary-source link, and the guide is not an "
                "explicit catalogue-only independent-project map",
                relative,
            )
        )
    if "version-access-feedback" not in anchor_categories:
        issues.append(
            Issue(
                "error",
                "editorial.missing_limit",
                "guide needs a concrete version, access, solution, grader, or "
                "feedback limitation",
                relative,
            )
        )

    generic_count = len(analysis.generic_sentences)
    generic_ratio = generic_count / max(1, len(analysis.eligible_sentences))
    if generic_count >= GENERIC_ERROR_COUNT and generic_ratio >= GENERIC_ERROR_RATIO:
        first = analysis.generic_sentences[0]
        issues.append(
            Issue(
                "error",
                "editorial.generic_claims",
                f"{generic_count} unsupported generic claims occupy "
                f"{generic_ratio:.0%} of eligible sentences; attach concrete "
                "courseware evidence or remove the claims",
                relative,
                first.line,
                first.text[:220],
            )
        )
    elif generic_count >= GENERIC_WARNING_COUNT:
        first = analysis.generic_sentences[0]
        issues.append(
            Issue(
                "warning",
                "editorial.generic_claims",
                f"{generic_count} generic claims lack a number, technical term, "
                "courseware anchor, source link, or explicit comparison",
                relative,
                first.line,
                first.text[:220],
            )
        )

    if document.language == "en":
        translationese = TRANSLATIONESE_EN_RE.search(document.text)
        if translationese:
            issues.append(
                Issue(
                    "error",
                    "editorial.translationese",
                    "generic 'repair' phrasing is blocked in English course guides; "
                    "name the concrete action with natural technical prose",
                    relative,
                    document.text.count("\n", 0, translationese.start()) + 1,
                    translationese.group(0),
                )
            )

    if document.evidence_level == "R0":
        first_hand = (
            FIRST_HAND_ZH_RE.search(document.text)
            if document.language == "zh"
            else FIRST_HAND_EN_RE.search(document.text)
        )
        if first_hand:
            issues.append(
                Issue(
                    "error",
                    "editorial.unsourced_first_hand",
                    "R0 desk research must not claim first-hand completion or experience",
                    relative,
                    document.text.count("\n", 0, first_hand.start()) + 1,
                    first_hand.group(0),
                )
            )

    editorial_pattern = (
        EDITORIAL_CUE_ZH_RE if document.language == "zh" else EDITORIAL_CUE_EN_RE
    )
    if not _source_cue(document.text, document):
        issues.append(
            Issue(
                "error",
                "editorial.fact_boundary",
                "guide has no natural-language official/provider fact cue",
                relative,
            )
        )
    if not editorial_pattern.search(document.text):
        issues.append(
            Issue(
                "error",
                "editorial.advice_boundary",
                "guide has no explicit EEDIY/editorial recommendation cue",
                relative,
            )
        )

    for index, paragraph in enumerate(analysis.paragraphs):
        if HIGH_RISK_FACT_RE.search(paragraph.text) and not _source_window(analysis, index):
            issues.append(
                Issue(
                    "error",
                    "editorial.untraced_fact",
                    "assignment count, grading, prerequisite, workload, availability, "
                    "or version fact lacks an adjacent official cue or primary source",
                    relative,
                    paragraph.line,
                    paragraph.text[:220],
                )
            )
        if SUPPLEMENT_TASK_RE.search(paragraph.text):
            neighbor_text = " ".join(
                analysis.paragraphs[candidate].text
                for candidate in range(
                    max(0, index - 1),
                    min(len(analysis.paragraphs), index + 2),
                )
                if analysis.paragraphs[candidate].section == paragraph.section
            )
            if not SUPPLEMENT_BOUNDARY_RE.search(neighbor_text):
                issues.append(
                    Issue(
                        "error",
                        "editorial.supplement_boundary",
                        "a suggested notebook, exercise, lab, or project must be "
                        "labelled as an EEDIY/editorial supplement and not official work",
                        relative,
                        paragraph.line,
                        paragraph.text[:220],
                    )
                )
    return issues


def _exact_paragraph_issues(
    analyses: Sequence[BodyAnalysis],
    selected_ids: set[int],
) -> list[Issue]:
    buckets: dict[tuple[str, str], list[tuple[BodyAnalysis, Segment]]] = {}
    for analysis in analyses:
        exact_minimum = (
            ZH_EXACT_PARAGRAPH_MINIMUM
            if analysis.document.language == "zh"
            else EN_EXACT_PARAGRAPH_MINIMUM
        )
        for paragraph in analysis.eligible_paragraphs:
            if paragraph.units < exact_minimum:
                continue
            buckets.setdefault(
                (analysis.document.language, paragraph.normalized),
                [],
            ).append((analysis, paragraph))

    issues: list[Issue] = []
    for entries in buckets.values():
        course_ids = {analysis.document.course_id for analysis, _ in entries}
        if len(course_ids) < 2 or not course_ids & selected_ids:
            continue
        ordered = sorted(
            entries,
            key=lambda item: (
                item[0].document.course_id,
                item[0].document.path.as_posix(),
                item[1].line,
            ),
        )
        left = next(
            (item for item in ordered if item[0].document.course_id in selected_ids),
            ordered[0],
        )
        right = next(
            item
            for item in ordered
            if item[0].document.course_id != left[0].document.course_id
        )
        issues.append(
            Issue(
                "error",
                "editorial.duplicate_paragraph",
                "long normalized paragraph duplicates "
                f"{display_path(right[0].document.path)}:{right[1].line}; "
                "rewrite around this course's actual artifacts and constraints",
                display_path(left[0].document.path),
                left[1].line,
                left[1].text[:220],
            )
        )
    return issues


def _best_fuzzy_matches(
    left: Sequence[Segment],
    right: Sequence[Segment],
    threshold: float,
) -> list[tuple[float, Segment, Segment]]:
    candidates: list[tuple[float, Segment, Segment]] = []
    for left_segment in left:
        for right_segment in right:
            if left_segment.normalized == right_segment.normalized:
                continue
            left_text = left_segment.normalized
            right_text = right_segment.normalized
            total_length = len(left_text) + len(right_text)
            if total_length == 0:
                continue
            # SequenceMatcher.real_quick_ratio() is exactly this length bound.
            # Computing it directly avoids constructing a matcher for almost
            # every dissimilar pair in the corpus.
            if (2.0 * min(len(left_text), len(right_text)) / total_length) < threshold:
                continue
            # High SequenceMatcher scores in editorial prose also retain many
            # contiguous character trigrams. A deliberately low Dice cutoff
            # removes unrelated prose before the expensive quadratic matcher
            # while keeping reordered or lightly edited template candidates.
            left_ngrams = _character_ngrams(left_text)
            right_ngrams = _character_ngrams(right_text)
            ngram_total = len(left_ngrams) + len(right_ngrams)
            if (
                ngram_total
                and 2.0 * len(left_ngrams & right_ngrams) / ngram_total
                < FUZZY_NGRAM_CANDIDATE_THRESHOLD
            ):
                continue
            # SequenceMatcher.quick_ratio() is a multiset-character upper
            # bound. Cache each segment's histogram because the same segment is
            # compared against many courses. This preserves the bound while
            # avoiding repeated O(n) setup inside difflib.
            left_counts = _character_counts(left_text)
            right_counts = _character_counts(right_text)
            shared = sum(
                min(count, right_counts.get(character, 0))
                for character, count in left_counts.items()
            )
            if (2.0 * shared / total_length) < threshold:
                continue
            matcher = difflib.SequenceMatcher(
                None,
                left_text,
                right_text,
                autojunk=False,
            )
            ratio = matcher.ratio()
            if ratio >= threshold:
                candidates.append((ratio, left_segment, right_segment))
    candidates.sort(
        key=lambda item: (-item[0], item[1].line, item[2].line)
    )
    chosen: list[tuple[float, Segment, Segment]] = []
    used_left: set[int] = set()
    used_right: set[int] = set()
    for candidate in candidates:
        _, left_segment, right_segment = candidate
        left_key = id(left_segment)
        right_key = id(right_segment)
        if left_key in used_left or right_key in used_right:
            continue
        chosen.append(candidate)
        used_left.add(left_key)
        used_right.add(right_key)
    return chosen


@lru_cache(maxsize=None)
def _character_counts(text: str) -> Counter[str]:
    return Counter(text)


@lru_cache(maxsize=None)
def _character_ngrams(text: str, width: int = 3) -> frozenset[str]:
    if len(text) <= width:
        return frozenset({text})
    return frozenset(
        text[index : index + width]
        for index in range(len(text) - width + 1)
    )


def _fuzzy_duplicate_issues(
    analyses: Sequence[BodyAnalysis],
    selected_ids: set[int],
) -> list[Issue]:
    issues: list[Issue] = []
    by_language: dict[str, list[BodyAnalysis]] = {"zh": [], "en": []}
    for analysis in analyses:
        by_language[analysis.document.language].append(analysis)

    for language in ("zh", "en"):
        items = sorted(
            by_language[language],
            key=lambda item: item.document.course_id,
        )
        for left_index, left in enumerate(items):
            for right in items[left_index + 1 :]:
                pair_ids = {left.document.course_id, right.document.course_id}
                if not pair_ids & selected_ids:
                    continue
                reporter, counterpart = (
                    (left, right)
                    if left.document.course_id in selected_ids
                    else (right, left)
                )
                paragraph_matches = _best_fuzzy_matches(
                    reporter.eligible_paragraphs,
                    counterpart.eligible_paragraphs,
                    FUZZY_PARAGRAPH_THRESHOLD,
                )
                if len(paragraph_matches) >= FUZZY_PARAGRAPH_ERROR_COUNT:
                    first = paragraph_matches[0]
                    issues.append(
                        Issue(
                            "error",
                            "editorial.fuzzy_paragraphs",
                            f"{len(paragraph_matches)} near-duplicate paragraphs "
                            f"(similarity ≥ {FUZZY_PARAGRAPH_THRESHOLD:.2f}) match "
                            f"{display_path(counterpart.document.path)}; two or more "
                            "indicate template reuse",
                            display_path(reporter.document.path),
                            first[1].line,
                            f"{first[0]:.3f}: {first[1].text[:190]}",
                        )
                    )
                elif paragraph_matches:
                    first = paragraph_matches[0]
                    issues.append(
                        Issue(
                            "warning",
                            "editorial.fuzzy_paragraph",
                            f"near-duplicate paragraph has similarity {first[0]:.3f} "
                            f"with {display_path(counterpart.document.path)}:"
                            f"{first[2].line}",
                            display_path(reporter.document.path),
                            first[1].line,
                            first[1].text[:220],
                        )
                    )

                sentence_matches = _best_fuzzy_matches(
                    reporter.eligible_sentences,
                    counterpart.eligible_sentences,
                    FUZZY_SENTENCE_THRESHOLD,
                )
                if len(sentence_matches) >= FUZZY_SENTENCE_ERROR_COUNT:
                    first = sentence_matches[0]
                    issues.append(
                        Issue(
                            "error",
                            "editorial.fuzzy_sentences",
                            f"{len(sentence_matches)} near-duplicate sentences "
                            f"(similarity ≥ {FUZZY_SENTENCE_THRESHOLD:.2f}) match "
                            f"{display_path(counterpart.document.path)}; three or more "
                            "indicate swap-test failure",
                            display_path(reporter.document.path),
                            first[1].line,
                            f"{first[0]:.3f}: {first[1].text[:190]}",
                        )
                    )
    return issues


def _number_tokens(text: str) -> set[str]:
    expanded = NUMBER_WORD_RE.sub(
        lambda match: NUMBER_WORDS[match.group(1).casefold()],
        text,
    )
    return {
        re.sub(r"\s+", "", match.group(0)).replace("—", "-").replace("–", "-")
        for match in NUMBER_RE.finditer(expanded)
    }


def _percent_tokens(text: str) -> set[str]:
    expanded = NUMBER_WORD_RE.sub(
        lambda match: NUMBER_WORDS[match.group(1).casefold()],
        text,
    )
    return {f"{match.group(1)}%" for match in PERCENT_RE.finditer(expanded)}


def _course_code_present(document: GuideDocument) -> bool:
    value = document.metadata.get("course_code")
    return isinstance(value, str) and bool(
        re.search(re.escape(value), document.text, re.IGNORECASE)
    )


def _section_units(analysis: BodyAnalysis) -> dict[int, int]:
    output: dict[int, int] = {}
    for paragraph in analysis.paragraphs:
        output[paragraph.section] = output.get(paragraph.section, 0) + paragraph.units
    return output


def _bilingual_issues(
    pair: GuidePair,
    zh: BodyAnalysis,
    en: BodyAnalysis,
) -> list[Issue]:
    issues: list[Issue] = []
    pair_path = f"course_id {pair.course_id}"
    if zh.heading_levels != en.heading_levels:
        issues.append(
            Issue(
                "error",
                "editorial.translation_structure",
                f"Chinese heading levels {list(zh.heading_levels)} differ from "
                f"English {list(en.heading_levels)}",
                pair_path,
            )
        )
    if set(zh.external_links) != set(en.external_links):
        only_zh = sorted(set(zh.external_links) - set(en.external_links))
        only_en = sorted(set(en.external_links) - set(zh.external_links))
        issues.append(
            Issue(
                "error",
                "editorial.translation_links",
                "Chinese and English narrative URL sets differ",
                pair_path,
                context=f"only zh={only_zh}; only en={only_en}",
            )
        )

    zh_years = set(YEAR_RE.findall(zh.document.text))
    en_years = set(YEAR_RE.findall(en.document.text))
    if zh_years != en_years:
        issues.append(
            Issue(
                "error",
                "editorial.translation_years",
                f"year facts differ: zh={sorted(zh_years)}, en={sorted(en_years)}",
                pair_path,
            )
        )
    zh_percents = _percent_tokens(zh.document.text)
    en_percents = _percent_tokens(en.document.text)
    if zh_percents != en_percents:
        issues.append(
            Issue(
                "error",
                "editorial.translation_percentages",
                f"percentage facts differ: zh={sorted(zh_percents)}, "
                f"en={sorted(en_percents)}",
                pair_path,
            )
        )
    if _course_code_present(zh.document) != _course_code_present(en.document):
        issues.append(
            Issue(
                "error",
                "editorial.translation_course_code",
                "course code appears in only one language",
                pair_path,
            )
        )

    zh_numbers = _number_tokens(zh.document.text)
    en_numbers = _number_tokens(en.document.text)
    number_union = zh_numbers | en_numbers
    number_jaccard = (
        len(zh_numbers & en_numbers) / len(number_union)
        if number_union
        else 1.0
    )
    if number_jaccard < NUMBER_PARITY_WARNING_THRESHOLD:
        issues.append(
            Issue(
                "warning",
                "editorial.translation_numbers",
                f"numeric-token Jaccard is {number_jaccard:.3f}; expected at least "
                f"{NUMBER_PARITY_WARNING_THRESHOLD:.2f}",
                pair_path,
                context=(
                    f"only zh={sorted(zh_numbers - en_numbers)}; "
                    f"only en={sorted(en_numbers - zh_numbers)}"
                ),
            )
        )

    zh_terms = _protected_terms(zh.document.text)
    en_folded = unicodedata.normalize("NFKC", en.document.text).casefold()
    present_terms = {
        term
        for term in zh_terms
        if re.search(rf"(?<![\w]){re.escape(term)}(?![\w])", en_folded)
    }
    term_ratio = len(present_terms) / len(zh_terms) if zh_terms else 1.0
    if term_ratio < TERM_PARITY_ERROR_THRESHOLD:
        severity = "error"
    elif term_ratio < TERM_PARITY_WARNING_THRESHOLD:
        severity = "warning"
    else:
        severity = ""
    if severity:
        issues.append(
            Issue(
                severity,
                "editorial.translation_terms",
                f"only {term_ratio:.1%} of Chinese code/acronym/tool tokens appear "
                "in English",
                pair_path,
                context="missing: " + ", ".join(sorted(zh_terms - present_terms)),
            )
        )

    length_ratio = en.visible_units / max(1, zh.visible_units)
    if (
        length_ratio < LENGTH_RATIO_ERROR_MINIMUM
        or length_ratio > LENGTH_RATIO_ERROR_MAXIMUM
    ):
        severity = "error"
    elif (
        length_ratio < LENGTH_RATIO_WARNING_MINIMUM
        or length_ratio > LENGTH_RATIO_WARNING_MAXIMUM
    ):
        severity = "warning"
    else:
        severity = ""
    if severity:
        issues.append(
            Issue(
                severity,
                "editorial.translation_length",
                f"English-word / Chinese-CJK length ratio is {length_ratio:.3f}; "
                f"expected {LENGTH_RATIO_WARNING_MINIMUM:.2f}–"
                f"{LENGTH_RATIO_WARNING_MAXIMUM:.2f}",
                pair_path,
            )
        )

    paragraph_delta = len(en.paragraphs) - len(zh.paragraphs)
    if abs(paragraph_delta) >= PARAGRAPH_COUNT_DELTA_ERROR:
        issues.append(
            Issue(
                "error",
                "editorial.translation_paragraphs",
                "Chinese and English differ by "
                f"{abs(paragraph_delta)} substantive paragraph(s); "
                f"zh={len(zh.paragraphs)}, en={len(en.paragraphs)}",
                pair_path,
            )
        )
    elif len(zh.paragraphs) == len(en.paragraphs):
        for paragraph_index, (zh_paragraph, en_paragraph) in enumerate(
            zip(zh.paragraphs, en.paragraphs, strict=True),
            1,
        ):
            if (
                zh_paragraph.section != en_paragraph.section
                or zh_paragraph.units < PARAGRAPH_ALIGNMENT_ZH_MINIMUM
            ):
                continue
            paragraph_ratio = en_paragraph.units / max(1, zh_paragraph.units)
            if (
                paragraph_ratio < PARAGRAPH_LENGTH_RATIO_ERROR_MINIMUM
                or paragraph_ratio > PARAGRAPH_LENGTH_RATIO_ERROR_MAXIMUM
            ):
                issues.append(
                    Issue(
                        "error",
                        "editorial.translation_paragraph_length",
                        f"aligned substantive paragraph {paragraph_index} has "
                        f"English-word / Chinese-CJK ratio {paragraph_ratio:.3f}; "
                        f"expected {PARAGRAPH_LENGTH_RATIO_ERROR_MINIMUM:.2f}–"
                        f"{PARAGRAPH_LENGTH_RATIO_ERROR_MAXIMUM:.2f}",
                        pair_path,
                        zh_paragraph.line,
                        (
                            f"zh line {zh_paragraph.line}: {zh_paragraph.text[:120]}; "
                            f"en line {en_paragraph.line}: {en_paragraph.text[:120]}"
                        ),
                    )
                )

    zh_sections = _section_units(zh)
    en_sections = _section_units(en)
    zh_section_paragraphs = Counter(
        paragraph.section for paragraph in zh.paragraphs
    )
    en_section_paragraphs = Counter(
        paragraph.section for paragraph in en.paragraphs
    )
    section_count = max(
        max(zh_sections, default=0),
        max(en_sections, default=0),
    )
    for section in range(1, section_count + 1):
        if not zh_sections.get(section) or not en_sections.get(section):
            issues.append(
                Issue(
                    "error",
                    "editorial.translation_empty_section",
                    f"H2 section {section} is empty in one language",
                    pair_path,
                    context=(
                        f"zh units={zh_sections.get(section, 0)}, "
                        f"en units={en_sections.get(section, 0)}"
                    ),
                )
            )
            continue
        section_ratio = en_sections[section] / zh_sections[section]
        if (
            (
                section_ratio < SECTION_LENGTH_RATIO_ERROR_MINIMUM
                or section_ratio > SECTION_LENGTH_RATIO_ERROR_MAXIMUM
            )
            and zh_section_paragraphs[section]
            != en_section_paragraphs[section]
        ):
            issues.append(
                Issue(
                    "error",
                    "editorial.translation_section_length",
                    f"H2 section {section} has English-word / Chinese-CJK ratio "
                    f"{section_ratio:.3f}; expected "
                    f"{SECTION_LENGTH_RATIO_ERROR_MINIMUM:.2f}–"
                    f"{SECTION_LENGTH_RATIO_ERROR_MAXIMUM:.2f}",
                    pair_path,
                    context=(
                        f"zh units={zh_sections[section]}, "
                        f"en units={en_sections[section]}; "
                        f"zh paragraphs={zh_section_paragraphs[section]}, "
                        f"en paragraphs={en_section_paragraphs[section]}"
                    ),
                )
            )
    return issues


def editorial_quality_issues(
    pairs: Sequence[GuidePair],
    *,
    selected_ids: Iterable[int] | None = None,
) -> tuple[list[Issue], dict[str, Any]]:
    ordered_pairs = sorted(pairs, key=lambda item: item.course_id)
    selected = (
        {pair.course_id for pair in ordered_pairs}
        if selected_ids is None
        else set(selected_ids)
    )
    analyses_by_key: dict[tuple[int, str], BodyAnalysis] = {}
    for pair in ordered_pairs:
        analyses_by_key[(pair.course_id, "zh")] = analyze_document(pair.zh)
        analyses_by_key[(pair.course_id, "en")] = analyze_document(pair.en)

    issues: list[Issue] = []
    for pair in ordered_pairs:
        if pair.course_id not in selected:
            continue
        zh = analyses_by_key[(pair.course_id, "zh")]
        en = analyses_by_key[(pair.course_id, "en")]
        issues.extend(_document_issues(zh))
        issues.extend(_document_issues(en))
        issues.extend(_bilingual_issues(pair, zh, en))

    all_analyses = [
        analyses_by_key[key]
        for key in sorted(analyses_by_key)
    ]
    issues.extend(_exact_paragraph_issues(all_analyses, selected))
    issues.extend(_fuzzy_duplicate_issues(all_analyses, selected))
    issues.sort(
        key=lambda item: (
            item.severity,
            item.code,
            item.path,
            item.line if item.line is not None else -1,
            item.message,
        )
    )
    statistics = {
        "guides_total": len(ordered_pairs),
        "guides_checked": len(selected & {pair.course_id for pair in ordered_pairs}),
        "documents_analyzed": len(all_analyses),
        "errors": sum(issue.severity == "error" for issue in issues),
        "warnings": sum(issue.severity == "warning" for issue in issues),
    }
    return issues, statistics


def load_guide_pairs(
    manifest_path: Path,
    catalogue_path: Path,
    *,
    repo_root: Path = REPO_ROOT,
) -> tuple[list[GuidePair], list[Issue]]:
    try:
        manifest = load_json(manifest_path)
        catalogue = load_json(catalogue_path)
    except (OSError, QualityError) as exc:
        return [], [
            Issue(
                "error",
                "editorial.input",
                str(exc),
                display_path(manifest_path, repo_root),
            )
        ]
    records = manifest.get("guides") if isinstance(manifest, Mapping) else None
    courses = catalogue.get("courses") if isinstance(catalogue, Mapping) else None
    if not isinstance(records, list) or not isinstance(courses, list):
        return [], [
            Issue(
                "error",
                "editorial.input_shape",
                "manifest requires guides[] and catalogue requires courses[]",
                display_path(manifest_path, repo_root),
            )
        ]
    courses_by_id = {
        int(course["source_id"]): course
        for course in courses
        if isinstance(course, Mapping)
        and isinstance(course.get("source_id"), int)
        and not isinstance(course.get("source_id"), bool)
    }
    issues: list[Issue] = []
    pairs: list[GuidePair] = []
    seen: set[int] = set()
    for index, record in enumerate(records):
        record_path = f"{display_path(manifest_path, repo_root)}:/guides/{index}"
        if not isinstance(record, Mapping) or not isinstance(record.get("course_id"), int):
            issues.append(
                Issue(
                    "error",
                    "editorial.manifest_record",
                    "guide record requires an integer course_id",
                    record_path,
                )
            )
            continue
        course_id = int(record["course_id"])
        if course_id in seen:
            issues.append(
                Issue(
                    "error",
                    "editorial.duplicate_course",
                    f"duplicate course_id {course_id}",
                    record_path,
                )
            )
            continue
        seen.add(course_id)
        metadata = courses_by_id.get(course_id)
        if metadata is None:
            issues.append(
                Issue(
                    "error",
                    "editorial.unknown_course",
                    f"course_id {course_id} is absent from the catalogue",
                    record_path,
                )
            )
            continue
        files = record.get("files")
        sources = record.get("primary_sources")
        if not isinstance(files, Mapping) or not isinstance(sources, list):
            issues.append(
                Issue(
                    "error",
                    "editorial.manifest_record",
                    "guide record requires files{} and primary_sources[]",
                    record_path,
                )
            )
            continue
        documents: dict[str, GuideDocument] = {}
        for language in ("zh", "en"):
            value = files.get(language)
            if not isinstance(value, str):
                issues.append(
                    Issue(
                        "error",
                        "editorial.guide_file",
                        f"missing {language} guide path",
                        record_path,
                    )
                )
                continue
            path = Path(value)
            if not path.is_absolute():
                path = repo_root / path
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as exc:
                issues.append(
                    Issue(
                        "error",
                        "editorial.guide_read",
                        str(exc),
                        display_path(path, repo_root),
                    )
                )
                continue
            documents[language] = GuideDocument(
                course_id=course_id,
                language=language,
                path=path,
                text=text,
                metadata=metadata,
                primary_sources=tuple(
                    source for source in sources if isinstance(source, str)
                ),
                evidence_level=str(record.get("evidence_level", "")),
            )
        if set(documents) == {"zh", "en"}:
            pairs.append(GuidePair(course_id, documents["zh"], documents["en"]))
    return sorted(pairs, key=lambda item: item.course_id), issues


def _changed_paths_from_git(reference: str, repo_root: Path) -> tuple[list[str], list[Issue]]:
    completed = subprocess.run(
        [
            "git",
            "diff",
            "--name-only",
            "--diff-filter=ACMR",
            f"{reference}...HEAD",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if completed.returncode:
        return [], [
            Issue(
                "error",
                "editorial.git_diff",
                completed.stderr.strip() or f"git diff exited {completed.returncode}",
            )
        ]
    return sorted(
        {
            line.strip().replace("\\", "/")
            for line in completed.stdout.splitlines()
            if line.strip()
        }
    ), []


def selected_course_ids(
    pairs: Sequence[GuidePair],
    changed_files: Sequence[str] | None,
    *,
    manifest_path: Path,
    catalogue_path: Path,
    repo_root: Path = REPO_ROOT,
) -> tuple[set[int], list[Issue]]:
    if changed_files is None:
        return {pair.course_id for pair in pairs}, []
    normalized: set[str] = set()
    for value in changed_files:
        path = Path(value)
        if path.is_absolute():
            try:
                value = path.resolve().relative_to(repo_root.resolve()).as_posix()
            except ValueError:
                value = path.as_posix()
        normalized.add(value.replace("\\", "/").lstrip("./"))

    manifest_relative = display_path(manifest_path, repo_root)
    catalogue_relative = display_path(catalogue_path, repo_root)
    if manifest_relative in normalized or catalogue_relative in normalized:
        return {pair.course_id for pair in pairs}, []

    by_file: dict[str, int] = {}
    for pair in pairs:
        for document in (pair.zh, pair.en):
            by_file[display_path(document.path, repo_root)] = pair.course_id
    selected = {by_file[path] for path in normalized if path in by_file}
    unmanaged = sorted(
        path
        for path in normalized
        if path.startswith("content/course-guides/") and path not in by_file
    )
    issues = [
        Issue(
            "error",
            "editorial.changed_unmanaged",
            "changed course-guide file is not referenced by the manifest",
            path,
        )
        for path in unmanaged
    ]
    return selected, issues


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Block template reuse and evidence-boundary regressions in researched "
            "bilingual course guides."
        )
    )
    parser.add_argument("--manifest", default="data/course_guides.json")
    parser.add_argument("--catalogue", default="data/courses.json")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--changed-files",
        nargs="+",
        metavar="PATH",
        help=(
            "check guide pairs touched by these paths while comparing them with "
            "the complete corpus"
        ),
    )
    mode.add_argument(
        "--changed-from",
        metavar="GIT_REF",
        help="derive changed files from GIT_REF...HEAD",
    )
    parser.add_argument("--json-report")
    parser.add_argument(
        "--warnings-as-errors",
        action="store_true",
        help="fail when any editorial warning remains",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    manifest_path = Path(args.manifest)
    catalogue_path = Path(args.catalogue)
    if not manifest_path.is_absolute():
        manifest_path = REPO_ROOT / manifest_path
    if not catalogue_path.is_absolute():
        catalogue_path = REPO_ROOT / catalogue_path

    pairs, input_issues = load_guide_pairs(manifest_path, catalogue_path)
    changed_files = args.changed_files
    selection_issues: list[Issue] = []
    if args.changed_from:
        changed_files, selection_issues = _changed_paths_from_git(
            args.changed_from,
            REPO_ROOT,
        )
    selected, selected_issues = selected_course_ids(
        pairs,
        changed_files,
        manifest_path=manifest_path,
        catalogue_path=catalogue_path,
    )
    selection_issues.extend(selected_issues)
    quality_issues, statistics = editorial_quality_issues(
        pairs,
        selected_ids=selected,
    )
    issues = [*input_issues, *selection_issues, *quality_issues]
    emit_issues(issues)
    print(
        "Editorial quality: "
        f"{statistics['guides_checked']}/{statistics['guides_total']} guide pairs checked; "
        f"{sum(issue.severity == 'error' for issue in issues)} errors, "
        f"{sum(issue.severity == 'warning' for issue in issues)} warnings"
    )
    report_path = Path(args.json_report) if args.json_report else None
    if report_path is not None and not report_path.is_absolute():
        report_path = REPO_ROOT / report_path
    blocking_issues = (
        issues
        if args.warnings_as_errors
        else [issue for issue in issues if issue.severity == "error"]
    )
    write_json_report(
        report_path,
        {
            "ok": not blocking_issues,
            "mode": "changed-files" if changed_files is not None else "full",
            "selected_course_ids": sorted(selected),
            "statistics": {
                **statistics,
                "errors": sum(issue.severity == "error" for issue in issues),
                "warnings": sum(issue.severity == "warning" for issue in issues),
            },
            "issues": [issue.to_dict() for issue in issues],
        },
    )
    return 1 if blocking_issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
