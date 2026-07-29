from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
COMMENTS_PARTIAL = ROOT / "overrides" / "partials" / "comments.html"
EXTRA_JAVASCRIPT = ROOT / "docs" / "assets" / "javascripts" / "extra.js"
ISSUE_TEMPLATE_ROOT = ROOT / ".github" / "ISSUE_TEMPLATE"

ISSUE_TEMPLATES = (
    "content-error.yml",
    "broken-link.yml",
    "course-feedback.yml",
)


def _comments_partial() -> str:
    return COMMENTS_PARTIAL.read_text(encoding="utf-8")


def test_giscus_uses_stable_repository_category_and_course_mapping() -> None:
    partial = _comments_partial()

    expected_attributes = {
        "data-repo": "appleweiping/eediy",
        "data-repo-id": "R_kgDOTmjk4g",
        "data-category": "Announcements",
        "data-category-id": "DIC_kwDOTmjk4s4DCMDn",
        "data-mapping": "specific",
        "data-term": "{{ course_id }}",
        "data-strict": "1",
    }
    for attribute, value in expected_attributes.items():
        assert f'{attribute}="{value}"' in partial


def test_giscus_repository_restricts_embedding_to_the_canonical_site() -> None:
    config_path = ROOT / "giscus.json"
    assert config_path.is_file(), "giscus.json must restrict allowed embedding origins"

    config = json.loads(config_path.read_text(encoding="utf-8"))
    assert config.get("origins") == ["https://appleweiping.github.io"]
    assert not config.get("originsRegex")


def test_every_course_issue_link_preserves_shared_and_reported_context() -> None:
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
        assert "course_id={{ course_id | urlencode }}" in href
        assert "page={{ canonical_page | urlencode }}" in href
        assert "reported_language={{ reported_language | urlencode }}" in href


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


def test_course_discussion_has_a_visible_github_fallback() -> None:
    partial = _comments_partial()
    discussion = partial.split(
        '<section class="ee-course-discussion"',
        maxsplit=1,
    )[1].split("</section>", maxsplit=1)[0]

    fallback_links = [
        line.strip()
        for line in discussion.splitlines()
        if "<a href=" in line and "/discussions" in line
    ]
    assert fallback_links, "course discussion must link directly to GitHub Discussions"
    assert all("discussions_q={{ course_id | urlencode }}" in link for link in fallback_links)


def test_material_palette_changes_are_forwarded_to_giscus() -> None:
    javascript = EXTRA_JAVASCRIPT.read_text(encoding="utf-8")

    assert "MutationObserver" in javascript
    assert "postMessage" in javascript
    assert "setConfig" in javascript
    assert "theme" in javascript
    assert "https://giscus.app" in javascript
