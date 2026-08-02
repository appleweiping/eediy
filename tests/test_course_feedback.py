from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from mkdocs.commands.build import build
from mkdocs.config import load_config
import yaml


ROOT = Path(__file__).resolve().parents[1]
COMMENTS_PARTIAL = ROOT / "overrides" / "partials" / "comments.html"
ISSUE_TEMPLATE_ROOT = ROOT / ".github" / "ISSUE_TEMPLATE"

ISSUE_TEMPLATES = (
    "content-error.yml",
    "broken-link.yml",
    "course-feedback.yml",
)


class _FeedbackHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.correction_href: str | None = None

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        values = dict(attrs)
        if tag == "a" and "template=content-error.yml" in (values.get("href") or ""):
            self.correction_href = values["href"]


def _comments_partial() -> str:
    return COMMENTS_PARTIAL.read_text(encoding="utf-8")


def test_feedback_uses_only_direct_github_issue_actions() -> None:
    partial = _comments_partial()

    assert "giscus" not in partial.lower()
    assert "/discussions" not in partial
    assert '<ul class="ee-course-feedback__actions">' in partial
    assert "<details" not in partial


def test_every_page_issue_link_preserves_shared_and_reported_context() -> None:
    partial = _comments_partial()
    issue_links = [
        line.strip()
        for line in partial.splitlines()
        if "<a href=" in line and "?template=" in line
    ]

    assert len(issue_links) == 3
    assert {
        href.split("template=", maxsplit=1)[1].split("&amp;", maxsplit=1)[0]
        for href in issue_links
    } == set(ISSUE_TEMPLATES)
    for href in issue_links:
        assert "page={{ canonical_page | urlencode }}" in href
        assert "reported_language={{ reported_language | urlencode }}" in href
    general_links = [
        href for href in issue_links if "template=course-feedback.yml" not in href
    ]
    assert all("page_id={{ page_id | urlencode }}" in href for href in general_links)
    course_feedback = next(
        href for href in issue_links if "template=course-feedback.yml" in href
    )
    assert "course_id={{ page_id | urlencode }}" in course_feedback


def test_course_track_route_and_practice_pages_receive_stable_feedback_ids() -> None:
    partial = _comments_partial()

    assert 'canonical_source.startswith("guides/")' in partial
    assert 'page_type = "guide" if is_practice_guide else page.meta.page_type' in partial
    assert 'page.meta.course_id | default("", true)' in partial
    assert 'page.meta.track_id | default("", true)' in partial
    assert 'page.meta.route_id | default("", true)' in partial
    assert 'metadata_id.startswith("course-")' in partial
    assert 'metadata_id.startswith("track-")' in partial
    assert 'metadata_id.startswith("route-")' in partial
    assert 'canonical_source[:-3].replace("/", "-")' in partial
    assert 'page_id = "guide-" ~ guide_slug' in partial
    assert "reported_path = page.url" in partial


def test_reader_entry_pages_enable_the_shared_feedback_footer() -> None:
    paths = (
        "index.md",
        "getting-started.md",
        "roadmap.md",
        "books.md",
        "math-foundations.md",
        "math-advanced.md",
        "postscript.md",
    )
    for relative in paths:
        for prefix in ("", "en/"):
            text = (ROOT / "docs" / prefix / relative).read_text(encoding="utf-8")
            assert "page_type: guide" in text, f"{prefix}{relative}"
            assert "comments: true" in text, f"{prefix}{relative}"


def test_comments_flag_is_authoritative_and_every_practice_guide_opts_in() -> None:
    partial = _comments_partial()
    assert "{% if page.meta and page.file and page.meta.comments %}" in partial

    for guide_root in (ROOT / "docs" / "guides", ROOT / "docs" / "en" / "guides"):
        for path in guide_root.glob("*.md"):
            text = path.read_text(encoding="utf-8")
            assert "page_type: guide" in text, path
            assert "comments: true" in text, path


def test_issue_forms_accept_the_reported_page_language_prefill() -> None:
    for filename in ISSUE_TEMPLATES:
        form = yaml.safe_load(
            (ISSUE_TEMPLATE_ROOT / filename).read_text(encoding="utf-8")
        )
        fields = {
            field.get("id"): field
            for field in form["body"]
            if isinstance(field, dict) and field.get("id")
        }

        assert "reported_language" in fields, filename
        language = fields["reported_language"]
        assert language["type"] == "input", filename
        assert language.get("validations", {}).get("required") is True, filename
        stable_id = "course_id" if filename == "course-feedback.yml" else "page_id"
        assert fields[stable_id].get("validations", {}).get("required") is True


def test_page_feedback_actions_are_visible_without_a_collapsed_panel() -> None:
    partial = _comments_partial()

    assert "Feedback and corrections" in partial
    assert "反馈与纠错" in partial
    assert "Found a factual error or stale link?" in partial
    assert "发现事实错误或失效链接" in partial
    assert "canonical URL, reported URL, and language" in partial
    assert "规范 URL" in partial
    assert "Cite verifiable evidence" in partial
    assert "请附可核验依据" in partial


def test_course_feedback_exposes_honest_review_provenance() -> None:
    partial = _comments_partial()

    assert 'page.meta.editorial_status == "learner-reviewed"' in partial
    assert 'page.meta.review_relationship == "exact-offering"' in partial
    assert 'page.meta.review_relationship == "same-course-other-run"' in partial
    assert 'page.meta.review_relationship == "successor-course"' in partial
    assert "page.meta.reviewed_at" in partial
    assert "EEDIY editorial review" in partial
    assert "EEDIY 编辑审读" in partial
    assert "this is not a claim that an editor completed the course" in partial
    assert "不声称编辑者完整修读过本课程" in partial
    assert "another run of the same course" in partial
    assert "同一课程另一轮次的署名学习复盘" in partial
    assert "successor-course report for context" in partial
    assert "后继课程复盘作为背景" in partial


def test_rendered_guide_ids_and_report_urls_use_canonical_page_paths(
    tmp_path: Path,
) -> None:
    docs = tmp_path / "docs"
    (docs / "guides").mkdir(parents=True)
    (docs / "en" / "guides").mkdir(parents=True)
    page = (
        "---\n"
        'title: "Test"\n'
        "page_type: guide\n"
        "comments: true\n"
        "---\n\n"
        "# Test\n\n"
        "Body.\n"
    )
    for relative in (
        "index.md",
        "guides/index.md",
        "en/index.md",
        "en/guides/index.md",
    ):
        (docs / relative).write_text(page, encoding="utf-8")

    site = tmp_path / "site"
    config = tmp_path / "mkdocs.yml"
    custom_dir = (ROOT / "overrides").as_posix()
    config.write_text(
        "site_name: Feedback rendering test\n"
        "site_url: https://appleweiping.github.io/eediy/\n"
        "repo_url: https://github.com/appleweiping/eediy\n"
        "docs_dir: docs\n"
        "site_dir: site\n"
        "theme:\n"
        "  name: material\n"
        f"  custom_dir: {custom_dir}\n"
        "nav:\n"
        "  - Home: index.md\n"
        "  - Guides: guides/index.md\n"
        "  - English home: en/index.md\n"
        "  - English guides: en/guides/index.md\n",
        encoding="utf-8",
    )
    build(load_config(config_file=str(config)))

    expected = {
        site / "index.html": (
            "guide-index",
            "https://appleweiping.github.io/eediy/",
            "https://appleweiping.github.io/eediy/",
        ),
        site / "guides" / "index.html": (
            "guide-guides-index",
            "https://appleweiping.github.io/eediy/guides/",
            "https://appleweiping.github.io/eediy/guides/",
        ),
        site / "en" / "index.html": (
            "guide-index",
            "https://appleweiping.github.io/eediy/",
            "https://appleweiping.github.io/eediy/en/",
        ),
        site / "en" / "guides" / "index.html": (
            "guide-guides-index",
            "https://appleweiping.github.io/eediy/guides/",
            "https://appleweiping.github.io/eediy/en/guides/",
        ),
    }
    for rendered_path, (page_id, canonical_page, reported_page) in expected.items():
        parser = _FeedbackHTMLParser()
        parser.feed(rendered_path.read_text(encoding="utf-8"))
        assert parser.correction_href is not None

        query = parse_qs(urlparse(parser.correction_href).query)
        assert query["page_id"] == [page_id]
        assert query["page"] == [canonical_page]
        assert query["reported_page"] == [reported_page]
