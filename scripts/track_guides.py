from __future__ import annotations

import difflib
import re
from collections import Counter
from functools import lru_cache
from math import ceil
from pathlib import Path
from typing import Any, Iterable, Mapping
from urllib.parse import urlsplit, urlunsplit

from scripts.quality_common import Issue, display_path, markdown_headings, repo_path


CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
LATIN_WORD_RE = re.compile(r"\b[A-Za-z][A-Za-z0-9'-]*\b")
INTERNAL_MARKDOWN_LINK_RE = re.compile(
    r"(?<!!)\[[^\]]+\]\(((?!https?://|mailto:|#)[^)\s]+\.md(?:#[^)\s]+)?)\)"
)
EXTERNAL_HTTPS_MARKDOWN_LINK_RE = re.compile(
    r"""(?ix)
    (?<!!)
    \[[^\]\r\n]+\]
    \(
        \s*<?
        (https://[^)\s>]+)
        >?
        (?:\s+(?:"[^"]*"|'[^']*'))?
        \s*
    \)
    """
)
TRACK_INDEX_LINK_RE = re.compile(r"^\.\./([a-z0-9]+(?:-[a-z0-9]+)*)/index\.md$")
PARAGRAPH_SPLIT_RE = re.compile(r"\n[ \t]*\n")
MARKDOWN_LINK_TARGET_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
H2_RE = re.compile(r"(?m)^##\s+[^\r\n]+\r?\n")
NUMBER_TOKEN_RE = re.compile(r"(?<![A-Za-z0-9])\d+(?:\.\d+)*(?:%|[A-Za-z])?")
WORD_TOKEN_RE = re.compile(
    r"(?<![A-Za-z0-9])"
    r"(?:[A-Za-z][A-Za-z0-9]*(?:[-+][A-Za-z0-9]+)*|"
    r"[A-Za-z0-9]+(?:[-+][A-Za-z0-9]+)+)"
    r"(?![A-Za-z0-9])"
)
PROTECTED_TECH_TERMS = {
    "adc",
    "alu",
    "amat",
    "awgn",
    "ber",
    "bjt",
    "bms",
    "bpsk",
    "cdc",
    "cmos",
    "cpi",
    "csi",
    "dac",
    "de1-soc",
    "dft",
    "dma",
    "dsp",
    "eda",
    "fdtd",
    "fft",
    "fir",
    "fpga",
    "fsm",
    "gdsfactory",
    "gpio",
    "hdl",
    "hls",
    "iir",
    "isa",
    "jupyter",
    "klayout",
    "labview",
    "lmi",
    "ltspice",
    "matlab",
    "mcu",
    "meep",
    "mems",
    "mimo",
    "mosfet",
    "mppt",
    "mspm0",
    "ngspice",
    "octave",
    "pdk",
    "pll",
    "pml",
    "psd",
    "pvt",
    "pybamm",
    "python",
    "python-control",
    "qucs-s",
    "rf",
    "risc-v",
    "rosette",
    "rtl",
    "rtos",
    "scikit-rf",
    "scipy",
    "sdr",
    "snr",
    "soc",
    "spice",
    "svd",
    "systemverilog",
    "tm4c123",
    "uart",
    "vhdl",
    "verilog",
    "vivado",
    "vm",
    "yosys",
}
PROTECTED_TECH_IGNORE = {
    "ee",
    "ic",
    "id",
    "ir",
    "mit",
    "pdf",
}
FORMULAIC_COPY = {
    "zh": (
        re.compile(r"掌握.+的核心概念、模型与分析方法"),
        re.compile(r"完成可复现、可检验的练习、实验或设计成果"),
        re.compile(r"建议按以下顺序推进"),
    ),
    "en": (
        re.compile(r"explain the core concepts, models, and methods of", re.IGNORECASE),
        re.compile(
            r"produce reproducible exercises, experiments, or designs with explicit checks",
            re.IGNORECASE,
        ),
        re.compile(r"proceed in the following order", re.IGNORECASE),
    ),
}
TRACK_GUIDE_SECTION_MAXIMUM = 5
TRACK_GUIDE_BRAND_MAXIMUM = 1
TRACK_GUIDE_CORPUS_STYLE_MAXIMUM = {
    "先字流程": 0.35,
    "防御性否定": 0.35,
    "命令词": 0.35,
    "统一保留动作": 0.35,
    "统一固定动作": 0.35,
    "站点自称": 0.10,
}
TRACK_GUIDE_CORPUS_STYLE_PATTERNS = {
    "先字流程": re.compile(r"(?<!优)先(?!修|后|前|验|导)"),
    "防御性否定": re.compile(r"(?:不是|不等于|而不是)"),
    "命令词": re.compile(r"(?:必须|不要|应当)"),
    "统一保留动作": re.compile(r"保留"),
    "统一固定动作": re.compile(r"(?:冻结|固定)"),
    "站点自称": re.compile(r"(?:\bEEDIY\b|本站|本页)", re.IGNORECASE),
}
TRACK_GUIDE_CORPUS_ENGLISH_STYLE_MAXIMUM = {
    "Bring … from": 0.30,
    "Without": 0.55,
    "failure / failed / failing": 0.60,
    "record / preserve / keep": 0.60,
}
TRACK_GUIDE_CORPUS_ENGLISH_STYLE_PATTERNS = {
    "Bring … from": re.compile(
        r"\bbring\b[^.!?\r\n]{0,240}\bfrom\b",
        re.IGNORECASE,
    ),
    "Without": re.compile(r"\bwithout\b", re.IGNORECASE),
    "failure / failed / failing": re.compile(
        r"\b(?:failure|failed|failing)\b",
        re.IGNORECASE,
    ),
    "record / preserve / keep": re.compile(
        r"\b(?:record|preserve|keep)\b",
        re.IGNORECASE,
    ),
}
TRACK_GUIDE_CORPUS_H2_VARIETY_MINIMUM = 3
TRACK_GUIDE_CORPUS_H2_SHARE_MAXIMUM = 0.70
INTERNAL_EDITORIAL_COPY = {
    "zh": (
        re.compile(r"\bR[0-3]\b", re.IGNORECASE),
        re.compile(r"(?:让|由).{0,10}(?:reviewer|审阅者|评审者)", re.IGNORECASE),
        re.compile(r"(?:访问|资源|证据).{0,8}(?:ledger|台账|账本)", re.IGNORECASE),
        re.compile(r"(?:完成|结课|退出).{0,6}(?:evidence|dossier|证据档案|证据包)", re.IGNORECASE),
        re.compile(r"(?:入门|先修|验收|结课|作为|用作).{0,8}\bgate\b", re.IGNORECASE),
        re.compile(r"(?:桌面|案头)(?:研究|审读|复核)"),
        re.compile(r"(?:维护者|编辑部)(?:协议|流程|队列|复核)"),
    ),
    "en": (
        re.compile(r"\bR[0-3]\b", re.IGNORECASE),
        re.compile(r"\b(?:reviewer|maintainer)\b", re.IGNORECASE),
        re.compile(
            r"\b(?:access|resource|evidence)\s+(?:ledger|dossier)\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\b(?:completion|exit)\s+(?:evidence|dossier|protocol)\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\b(?:entry|readiness|prerequisite|completion)\s+gate\b",
            re.IGNORECASE,
        ),
        re.compile(r"\bdesk[- ]research(?:ed)?\b", re.IGNORECASE),
        re.compile(r"\breview (?:queue|protocol)\b", re.IGNORECASE),
    ),
}
PROTOCOL_ENDING = {
    "zh": re.compile(
        r"(?:reviewer|审阅者|评审者|课程\s*ID|纠错协议|复核队列|维护者).{0,120}$",
        re.IGNORECASE | re.DOTALL,
    ),
    "en": re.compile(
        r"(?:reviewer|maintainer|course\s*ID|correction protocol|review queue).{0,120}$",
        re.IGNORECASE | re.DOTALL,
    ),
}
FUZZY_PARAGRAPH_THRESHOLD = 0.88
FUZZY_NGRAM_CANDIDATE_THRESHOLD = 0.55


def _visible_length(text: str, language: str) -> int:
    without_urls = re.sub(r"https?://\S+", " ", text)
    if language == "zh":
        return len(CJK_RE.findall(without_urls))
    return len(LATIN_WORD_RE.findall(without_urls))


def _translation_visible_length(text: str, language: str) -> int:
    """Count embedded technical English in Chinese when comparing translations."""

    without_urls = re.sub(r"https?://\S+", " ", text)
    if language == "zh":
        return len(CJK_RE.findall(without_urls)) + len(
            LATIN_WORD_RE.findall(without_urls)
        )
    return len(LATIN_WORD_RE.findall(without_urls))


def _internal_targets(body: str) -> list[str]:
    return [target.split("#", 1)[0] for target in INTERNAL_MARKDOWN_LINK_RE.findall(body)]


def _normalize_https_target(target: str) -> str | None:
    """Canonicalize a direct HTTPS Markdown target for bilingual comparison."""

    try:
        parts = urlsplit(target)
        port = parts.port
    except ValueError:
        return None
    if parts.scheme.casefold() != "https" or not parts.hostname:
        return None

    hostname = parts.hostname.casefold()
    if ":" in hostname and not hostname.startswith("["):
        hostname = f"[{hostname}]"
    netloc = hostname
    if parts.username is not None:
        credentials = parts.username
        if parts.password is not None:
            credentials += f":{parts.password}"
        netloc = f"{credentials}@{netloc}"
    if port is not None and port != 443:
        netloc = f"{netloc}:{port}"

    path = parts.path or "/"
    if path != "/":
        path = path.rstrip("/")
    return urlunsplit(("https", netloc, path, parts.query, parts.fragment))


def _external_https_targets(body: str) -> set[str]:
    return {
        normalized
        for target in EXTERNAL_HTTPS_MARKDOWN_LINK_RE.findall(body)
        if (normalized := _normalize_https_target(target)) is not None
    }


def _normalized_paragraphs(body: str) -> Iterable[str]:
    for raw in PARAGRAPH_SPLIT_RE.split(body):
        paragraph = raw.strip()
        if (
            not paragraph
            or paragraph.startswith("#")
            or paragraph.startswith("|")
            or paragraph.startswith("```")
        ):
            continue
        paragraph = MARKDOWN_LINK_TARGET_RE.sub(r"\1", paragraph)
        paragraph = re.sub(r"[*_`~]", "", paragraph)
        paragraph = re.sub(r"\s+", " ", paragraph).strip().casefold()
        if len(paragraph) >= 180:
            yield paragraph


def _plain_paragraph(raw: str) -> str:
    paragraph = MARKDOWN_LINK_TARGET_RE.sub(r"\1", raw)
    paragraph = re.sub(r"<https?://[^>]+>", " ", paragraph)
    paragraph = re.sub(r"https?://\S+", " ", paragraph)
    paragraph = re.sub(r"[*_`~]", "", paragraph)
    return re.sub(r"\s+", " ", paragraph).strip()


def _substantive_paragraphs(section: str, language: str) -> list[str]:
    """Return prose paragraphs that carry bilingual editorial meaning."""

    paragraphs: list[str] = []
    for raw in PARAGRAPH_SPLIT_RE.split(section):
        candidate = raw.strip()
        if (
            not candidate
            or candidate.startswith("#")
            or candidate.startswith("|")
            or candidate.startswith("```")
        ):
            continue
        plain = _plain_paragraph(candidate)
        minimum = 18 if language == "zh" else 12
        if _visible_length(plain, language) >= minimum:
            paragraphs.append(plain)
    return paragraphs


def _numeric_tokens(paragraph: str) -> set[str]:
    return {
        token.casefold()
        for token in NUMBER_TOKEN_RE.findall(paragraph)
    }


def _is_protected_technical_token(token: str) -> bool:
    normalized = token.casefold()
    if normalized in PROTECTED_TECH_TERMS:
        return True
    if (
        any(character.isdigit() for character in token)
        and any(character.isupper() for character in token)
    ):
        return True
    uppercase_count = sum(character.isupper() for character in token)
    if uppercase_count >= 2:
        return True
    return bool(
        re.search(r"[A-Z][a-z]+[A-Z]", token)
        or re.search(r"[a-z][A-Z]", token)
    )


def _normalize_technical_token(token: str) -> str:
    normalized = token.casefold().replace("–", "-").replace("—", "-")
    if normalized == "op-amps":
        return "op-amp"
    if normalized.endswith("s") and (
        normalized[:-1] in PROTECTED_TECH_TERMS
        or sum(character.isupper() for character in token) >= 2
    ):
        return normalized[:-1]
    return normalized


def _technical_tokens(paragraph: str) -> set[str]:
    return {
        normalized
        for token in WORD_TOKEN_RE.findall(paragraph)
        if _is_protected_technical_token(token)
        and (
            normalized := _normalize_technical_token(token)
        ) not in PROTECTED_TECH_IGNORE
    }


def _validate_translation_details(
    track_id: str,
    bodies: Mapping[str, str],
) -> list[Issue]:
    """Check aligned bilingual prose, numbers, and protected technical terms."""

    if set(bodies) != {"zh", "en"}:
        return []
    zh_sections = _h2_sections(bodies["zh"])
    en_sections = _h2_sections(bodies["en"])
    if len(zh_sections) != len(en_sections):
        return []

    issues: list[Issue] = []
    for section_index, (zh_section, en_section) in enumerate(
        zip(zh_sections, en_sections, strict=True),
        start=1,
    ):
        zh_paragraphs = _substantive_paragraphs(zh_section, "zh")
        en_paragraphs = _substantive_paragraphs(en_section, "en")
        if len(zh_paragraphs) != len(en_paragraphs):
            issues.append(
                Issue(
                    "error",
                    "track_guide.translation_paragraphs",
                    (
                        f"H2 section {section_index} has "
                        f"{len(zh_paragraphs)} substantive Chinese paragraph(s) "
                        f"and {len(en_paragraphs)} English paragraph(s); "
                        "each editorial paragraph requires one counterpart"
                    ),
                    track_id,
                )
            )
            continue

        for paragraph_index, (zh_paragraph, en_paragraph) in enumerate(
            zip(zh_paragraphs, en_paragraphs, strict=True),
            start=1,
        ):
            ratio = _translation_visible_length(en_paragraph, "en") / max(
                _translation_visible_length(zh_paragraph, "zh"),
                1,
            )
            if not 0.25 <= ratio <= 1.25:
                issues.append(
                    Issue(
                        "error",
                        "track_guide.translation_paragraph_length",
                        (
                            f"H2 section {section_index}, paragraph "
                            f"{paragraph_index} has English/Chinese visible-length "
                            f"ratio {ratio:.2f}; expected 0.25–1.25"
                        ),
                        track_id,
                    )
                )

            zh_numbers = _numeric_tokens(zh_paragraph)
            en_numbers = _numeric_tokens(en_paragraph)
            if zh_numbers != en_numbers:
                issues.append(
                    Issue(
                        "error",
                        "track_guide.translation_numbers",
                        (
                            f"H2 section {section_index}, paragraph "
                            f"{paragraph_index} changes numeric claims"
                        ),
                        track_id,
                        context=(
                            f"zh={sorted(zh_numbers) or 'none'}; "
                            f"en={sorted(en_numbers) or 'none'}"
                        ),
                    )
                )

            zh_terms = _technical_tokens(zh_paragraph)
            en_terms = _technical_tokens(en_paragraph)
            missing_en = sorted(zh_terms - en_terms)
            missing_zh = sorted(en_terms - zh_terms)
            if missing_en or missing_zh:
                issues.append(
                    Issue(
                        "error",
                        "track_guide.translation_terms",
                        (
                            f"H2 section {section_index}, paragraph "
                            f"{paragraph_index} changes protected technical terms"
                        ),
                        track_id,
                        context=(
                            f"missing-en={missing_en or 'none'}; "
                            f"missing-zh={missing_zh or 'none'}"
                        ),
                    )
                )
    return issues


def _near_duplicate_ratio(left: str, right: str) -> float:
    total = len(left) + len(right)
    if not total:
        return 0.0
    if 2.0 * min(len(left), len(right)) / total < FUZZY_PARAGRAPH_THRESHOLD:
        return 0.0
    left_ngrams = _character_ngrams(left)
    right_ngrams = _character_ngrams(right)
    ngram_total = len(left_ngrams) + len(right_ngrams)
    if (
        ngram_total
        and 2.0 * len(left_ngrams & right_ngrams) / ngram_total
        < FUZZY_NGRAM_CANDIDATE_THRESHOLD
    ):
        return 0.0
    left_counts = _character_counts(left)
    right_counts = _character_counts(right)
    shared = sum(
        min(count, right_counts.get(character, 0))
        for character, count in left_counts.items()
    )
    if 2.0 * shared / total < FUZZY_PARAGRAPH_THRESHOLD:
        return 0.0
    return difflib.SequenceMatcher(
        None,
        left,
        right,
        autojunk=False,
    ).ratio()


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


def _h2_sections(body: str) -> list[str]:
    matches = list(H2_RE.finditer(body))
    return [
        body[match.end() : matches[index + 1].start() if index + 1 < len(matches) else len(body)]
        for index, match in enumerate(matches)
    ]


def _validate_fragment(body: str, *, language: str, path: Path) -> list[Issue]:
    source = display_path(path)
    issues: list[Issue] = []
    if body.startswith("---"):
        issues.append(
            Issue(
                "error",
                "track_guide.front_matter",
                "track-guide fragments must not contain front matter",
                source,
            )
        )
    headings = markdown_headings(body)
    if any(level == 1 for level, _, _ in headings):
        issues.append(
            Issue(
                "error",
                "track_guide.h1",
                "track-guide fragments must not contain an H1",
                source,
            )
        )
    h2_count = sum(level == 2 for level, _, _ in headings)
    if h2_count < 3:
        issues.append(
            Issue(
                "error",
                "track_guide.sections",
                "an authored track guide requires at least three H2 sections",
                source,
            )
        )
    if h2_count > TRACK_GUIDE_SECTION_MAXIMUM:
        issues.append(
            Issue(
                "error",
                "track_guide.section_sprawl",
                (
                    f"track guide has {h2_count} H2 sections; "
                    f"maximum is {TRACK_GUIDE_SECTION_MAXIMUM}"
                ),
                source,
            )
        )
    section_minimum = 100 if language == "zh" else 55
    shallow_sections = [
        index + 1
        for index, section in enumerate(_h2_sections(body))
        if _visible_length(section, language) < section_minimum
    ]
    if shallow_sections:
        unit = "CJK characters" if language == "zh" else "words"
        issues.append(
            Issue(
                "error",
                "track_guide.section_depth",
                (
                    f"H2 section(s) {shallow_sections} have fewer than "
                    f"{section_minimum} visible {unit}"
                ),
                source,
            )
        )
    minimum = 550 if language == "zh" else 300
    length = _visible_length(body, language)
    if length < minimum:
        unit = "CJK characters" if language == "zh" else "words"
        issues.append(
            Issue(
                "error",
                "track_guide.depth",
                f"track guide has {length} visible {unit}; minimum is {minimum}",
                source,
            )
        )
    links = _internal_targets(body)
    if len(set(links)) < 2:
        issues.append(
            Issue(
                "error",
                "track_guide.course_links",
                "an authored track guide must compare at least two distinct linked course or prerequisite pages",
                source,
            )
        )
    if not _external_https_targets(body):
        issues.append(
            Issue(
                "error",
                "track_guide.primary_source_link",
                (
                    "an authored track guide requires at least one direct HTTPS "
                    "Markdown link to a primary course or project source"
                ),
                source,
            )
        )
    for pattern in FORMULAIC_COPY[language]:
        if pattern.search(body):
            issues.append(
                Issue(
                    "error",
                    "track_guide.formulaic_copy",
                    "track guide retains generated catalogue boilerplate instead of track-specific editorial judgment",
                    source,
                )
            )
            break
    for pattern in INTERNAL_EDITORIAL_COPY[language]:
        if pattern.search(body):
            issues.append(
                Issue(
                    "error",
                    "track_guide.internal_editorial_voice",
                    (
                        "track guide exposes editorial workflow language instead "
                        "of speaking naturally to a learner"
                    ),
                    source,
                )
            )
            break
    brand_mentions = len(re.findall(r"\bEEDIY\b", body, re.IGNORECASE))
    if brand_mentions > TRACK_GUIDE_BRAND_MAXIMUM:
        issues.append(
            Issue(
                "error",
                "track_guide.brand_overuse",
                (
                    f"track guide mentions EEDIY {brand_mentions} times; "
                    f"maximum is {TRACK_GUIDE_BRAND_MAXIMUM}"
                ),
                source,
            )
        )
    if PROTOCOL_ENDING[language].search(body[-500:]):
        issues.append(
            Issue(
                "error",
                "track_guide.protocol_ending",
                "track guide ends with a maintenance or review protocol",
                source,
            )
        )
    return issues


def _corpus_style_issues(
    guides: Mapping[str, Mapping[str, Any]],
    *,
    source: str = "content/track-guides",
) -> list[Issue]:
    # A corpus ratio is meaningful only when the sample can represent one hit
    # at the strictest allowed share. Derive that sample from the style limits,
    # rather than from the current taxonomy or a catalogue-size target.
    strictest_share = min(
        *TRACK_GUIDE_CORPUS_STYLE_MAXIMUM.values(),
        *TRACK_GUIDE_CORPUS_ENGLISH_STYLE_MAXIMUM.values(),
    )
    comparison_sample = ceil(1 / strictest_share)
    if len(guides) < comparison_sample:
        return []
    zh_bodies = {
        track_id: str(guide.get("bodies", {}).get("zh", ""))
        for track_id, guide in guides.items()
    }
    en_bodies = {
        track_id: str(guide.get("bodies", {}).get("en", ""))
        for track_id, guide in guides.items()
    }
    issues: list[Issue] = []
    for label, maximum in TRACK_GUIDE_CORPUS_STYLE_MAXIMUM.items():
        pattern = TRACK_GUIDE_CORPUS_STYLE_PATTERNS[label]
        matches = sorted(
            track_id for track_id, body in zh_bodies.items() if pattern.search(body)
        )
        share = len(matches) / len(zh_bodies)
        if share > maximum:
            issues.append(
                Issue(
                    "error",
                    "track_guide.corpus_template_vocabulary",
                    (
                        f"{label!r} appears in {len(matches)}/{len(zh_bodies)} "
                        f"Chinese track guides ({share:.1%}); maximum is "
                        f"{maximum:.0%}"
                    ),
                    source,
                    context=", ".join(matches),
                )
            )
    for label, maximum in TRACK_GUIDE_CORPUS_ENGLISH_STYLE_MAXIMUM.items():
        pattern = TRACK_GUIDE_CORPUS_ENGLISH_STYLE_PATTERNS[label]
        matches = sorted(
            track_id for track_id, body in en_bodies.items() if pattern.search(body)
        )
        share = len(matches) / len(en_bodies)
        if share > maximum:
            issues.append(
                Issue(
                    "error",
                    "track_guide.corpus_template_vocabulary",
                    (
                        f"{label!r} appears in {len(matches)}/{len(en_bodies)} "
                        f"English track guides ({share:.1%}); maximum is "
                        f"{maximum:.0%}"
                    ),
                    source,
                    context=", ".join(matches),
                )
            )

    h2_distribution = Counter(
        sum(level == 2 for level, _, _ in markdown_headings(body))
        for body in zh_bodies.values()
    )
    distribution = ", ".join(
        f"{h2_count}:{count}"
        for h2_count, count in sorted(h2_distribution.items())
    )
    if len(h2_distribution) < TRACK_GUIDE_CORPUS_H2_VARIETY_MINIMUM:
        issues.append(
            Issue(
                "error",
                "track_guide.corpus_structure_variety",
                (
                    f"H2-count distribution [{distribution}] has "
                    f"{len(h2_distribution)} distinct value(s); minimum is "
                    f"{TRACK_GUIDE_CORPUS_H2_VARIETY_MINIMUM}"
                ),
                source,
            )
        )
    dominant_h2_count, dominant_count = max(
        h2_distribution.items(),
        key=lambda item: (item[1], -item[0]),
    )
    dominant_share = dominant_count / len(zh_bodies)
    if dominant_share > TRACK_GUIDE_CORPUS_H2_SHARE_MAXIMUM:
        issues.append(
            Issue(
                "error",
                "track_guide.corpus_structure_dominance",
                (
                    f"H2-count distribution [{distribution}]; count "
                    f"{dominant_h2_count} appears in "
                    f"{dominant_count}/{len(zh_bodies)} guides "
                    f"({dominant_share:.1%}); maximum is "
                    f"{TRACK_GUIDE_CORPUS_H2_SHARE_MAXIMUM:.0%}"
                ),
                source,
            )
        )
    return issues


def _validate_link_targets(
    *,
    body: str,
    track_id: str,
    language: str,
    course_slugs: Mapping[str, set[str]],
    path: Path,
) -> list[Issue]:
    issues: list[Issue] = []
    for target in sorted(set(_internal_targets(body))):
        valid = False
        if "/" not in target and target.endswith(".md"):
            valid = target.removesuffix(".md") in course_slugs.get(track_id, set())
        else:
            match = TRACK_INDEX_LINK_RE.fullmatch(target)
            valid = bool(match and match.group(1) in course_slugs)
        if not valid:
            issues.append(
                Issue(
                    "error",
                    "track_guide.link_target",
                    (
                        f"{language} track guide links to {target!r}, which is neither "
                        "a course in this track nor another populated track index"
                    ),
                    display_path(path),
                )
            )
    return issues


def load_track_guides(
    catalogue: Mapping[str, Any],
    root: Path | None = None,
) -> tuple[dict[str, dict[str, Any]], list[Issue]]:
    root = root or repo_path("content/track-guides")
    populated = {
        str(course["track"])
        for course in catalogue.get("courses", [])
        if isinstance(course, Mapping) and isinstance(course.get("track"), str)
    }
    course_slugs: dict[str, set[str]] = {track_id: set() for track_id in populated}
    for course in catalogue.get("courses", []):
        if not isinstance(course, Mapping):
            continue
        track_id = course.get("track")
        slug = course.get("slug")
        if isinstance(track_id, str) and isinstance(slug, str):
            course_slugs.setdefault(track_id, set()).add(slug)
    guides: dict[str, dict[str, Any]] = {}
    issues: list[Issue] = []
    expected_paths: set[Path] = set()
    seen_paragraphs: dict[tuple[str, str], Path] = {}
    prior_paragraphs: dict[str, list[tuple[str, Path]]] = {"zh": [], "en": []}
    for track_id in sorted(populated):
        bodies: dict[str, str] = {}
        heading_levels: dict[str, list[int]] = {}
        for language in ("zh", "en"):
            path = root / f"{track_id}.{language}.md"
            expected_paths.add(path.resolve())
            try:
                body = path.read_text(encoding="utf-8").strip() + "\n"
            except (OSError, UnicodeDecodeError) as exc:
                issues.append(
                    Issue(
                        "error",
                        "track_guide.file_read",
                        str(exc),
                        display_path(path),
                    )
                )
                continue
            bodies[language] = body
            heading_levels[language] = [
                level for level, _, _ in markdown_headings(body)
            ]
            issues.extend(
                _validate_fragment(body, language=language, path=path)
            )
            issues.extend(
                _validate_link_targets(
                    body=body,
                    track_id=track_id,
                    language=language,
                    course_slugs=course_slugs,
                    path=path,
                )
            )
            for paragraph in _normalized_paragraphs(body):
                key = (language, paragraph)
                previous = seen_paragraphs.get(key)
                if previous is not None:
                    issues.append(
                        Issue(
                            "error",
                            "track_guide.duplicate_paragraph",
                            (
                                "long editorial paragraph duplicates "
                                f"{display_path(previous)}"
                            ),
                            display_path(path),
                        )
                    )
                else:
                    seen_paragraphs[key] = path
                    fuzzy_match = next(
                        (
                            (ratio, other_path)
                            for other, other_path in prior_paragraphs[language]
                            if other_path != path
                            and (
                                ratio := _near_duplicate_ratio(
                                    paragraph,
                                    other,
                                )
                            )
                            >= FUZZY_PARAGRAPH_THRESHOLD
                        ),
                        None,
                    )
                    if fuzzy_match is not None:
                        ratio, other_path = fuzzy_match
                        issues.append(
                            Issue(
                                "error",
                                "track_guide.fuzzy_paragraph",
                                (
                                    "editorial paragraph is "
                                    f"{ratio:.3f} similar to "
                                    f"{display_path(other_path)}; rewrite it "
                                    "around this track's own choices and constraints"
                                ),
                                display_path(path),
                            )
                        )
                    prior_paragraphs[language].append((paragraph, path))
        if heading_levels.get("zh") != heading_levels.get("en"):
            issues.append(
                Issue(
                    "error",
                    "track_guide.translation_structure",
                    "Chinese and English track-guide heading levels differ",
                    track_id,
                )
            )
        if set(bodies) == {"zh", "en"}:
            issues.extend(_validate_translation_details(track_id, bodies))
            zh_targets = set(_internal_targets(bodies["zh"]))
            en_targets = set(_internal_targets(bodies["en"]))
            if zh_targets != en_targets:
                issues.append(
                    Issue(
                        "error",
                        "track_guide.translation_links",
                        "Chinese and English track guides must link to the same course and prerequisite pages",
                        track_id,
                    )
                )
            zh_external_targets = _external_https_targets(bodies["zh"])
            en_external_targets = _external_https_targets(bodies["en"])
            if zh_external_targets != en_external_targets:
                zh_only = sorted(zh_external_targets - en_external_targets)
                en_only = sorted(en_external_targets - zh_external_targets)
                issues.append(
                    Issue(
                        "error",
                        "track_guide.translation_external_links",
                        (
                            "Chinese and English track guides must use the same "
                            "normalized direct HTTPS Markdown targets"
                        ),
                        track_id,
                        context=(
                            f"zh-only={zh_only or 'none'}; "
                            f"en-only={en_only or 'none'}"
                        ),
                    )
                )
            zh_length = _translation_visible_length(bodies["zh"], "zh")
            en_length = _translation_visible_length(bodies["en"], "en")
            ratio = en_length / max(zh_length, 1)
            if not 0.40 <= ratio <= 0.85:
                issues.append(
                    Issue(
                        "error",
                        "track_guide.translation_length",
                        (
                            "English/Chinese visible-length ratio "
                            f"{ratio:.2f} is outside the 0.40–0.85 parity band"
                        ),
                        track_id,
                    )
                )
            zh_sections = _h2_sections(bodies["zh"])
            en_sections = _h2_sections(bodies["en"])
            if len(zh_sections) == len(en_sections):
                bad_sections = []
                for index, (zh_section, en_section) in enumerate(
                    zip(zh_sections, en_sections, strict=True),
                    start=1,
                ):
                    section_ratio = _translation_visible_length(
                        en_section, "en"
                    ) / max(
                        _translation_visible_length(zh_section, "zh"),
                        1,
                    )
                    if not 0.35 <= section_ratio <= 0.95:
                        bad_sections.append(f"{index}:{section_ratio:.2f}")
                if bad_sections:
                    issues.append(
                        Issue(
                            "error",
                            "track_guide.translation_section_length",
                            (
                                "English/Chinese H2 section ratios outside the "
                                "0.35–0.95 parity band: "
                                + ", ".join(bad_sections)
                            ),
                            track_id,
                        )
                    )
        guides[track_id] = {"bodies": bodies}

    if root.exists():
        for path in root.glob("*.md"):
            if path.resolve() not in expected_paths:
                issues.append(
                    Issue(
                        "error",
                        "track_guide.unexpected",
                        "track-guide file does not map to a populated bilingual track",
                        display_path(path),
                    )
                )
    issues.extend(_corpus_style_issues(guides, source=display_path(root)))
    return guides, issues
