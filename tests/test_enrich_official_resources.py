from __future__ import annotations

import json
from pathlib import Path
import unittest

from scripts.enrich_official_resources import (
    Anchor,
    clean_title,
    classify_resource,
    de_duplicate_and_limit,
    extract_resources_from_html,
    migrate_checkpoint_kinds,
    normalize_url,
    normalize_resource_title_and_kind,
    parse_anchors,
    resource_relevance,
    resource_status,
    title_quality_counts,
)


class NormalizeUrlTests(unittest.TestCase):
    def test_repairs_common_utf8_mojibake(self) -> None:
        self.assertEqual(
            clean_title("Studentsâ Learning"),
            "Students’ Learning",
        )
        self.assertEqual(clean_title("HomeworkÂ 4Â Code"), "Homework 4 Code")

    def test_requires_https_and_removes_tracking(self) -> None:
        self.assertEqual(
            normalize_url(
                "https://Example.EDU/course/?utm_source=news&id=2#week-1"
            ),
            "https://example.edu/course?id=2",
        )
        self.assertIsNone(normalize_url("http://example.edu/course/"))
        self.assertIsNone(normalize_url("mailto:teacher@example.edu"))

    def test_preserves_wayback_embedded_https_target(self) -> None:
        url = (
            "https://web.archive.org/web/20241219154359/"
            "https://cs61c.org/fa24/"
        )
        self.assertEqual(
            normalize_url(url),
            (
                "https://web.archive.org/web/20241219154359/"
                "https://cs61c.org/fa24"
            ),
        )

    def test_excludes_images_and_social_hosts(self) -> None:
        self.assertIsNone(normalize_url("https://example.edu/figure.svg"))
        self.assertIsNone(normalize_url("https://twitter.com/example"))

    def test_relative_base_keeps_course_directory_scope(self) -> None:
        anchors = parse_anchors(
            '<base href="./"><a href="homework.html">Homework</a>',
            "https://example.edu/class/ee100",
        )
        self.assertEqual(
            anchors[0].href,
            "https://example.edu/class/ee100/homework.html",
        )

    def test_archive_status_is_explicit(self) -> None:
        self.assertEqual(
            resource_status(
                "https://onlinecourses-archive.example.edu/course/notes",
                "https://onlinecourses-archive.example.edu/course",
                True,
            ),
            "archived",
        )


class ClassificationTests(unittest.TestCase):
    def test_classifies_core_resource_kinds(self) -> None:
        cases = {
            "Lecture videos": "video",
            "Lecture notes and handouts": "notes",
            "Course syllabus": "course",
            "Homework 4": "assignments",
            "Final project": "projects",
            "Practice exam": "exams",
            "Starter MATLAB code": "code",
            "Open textbook": "textbook",
            "Required readings": "notes",
        }
        for title, expected in cases.items():
            with self.subTest(title=title):
                self.assertEqual(
                    classify_resource(title, "https://example.edu/course/"),
                    expected,
                )

    def test_does_not_classify_navigation(self) -> None:
        self.assertIsNone(
            classify_resource("University admissions", "https://example.edu/")
        )
        self.assertIsNone(
            classify_resource(
                "Worked example: Atwood machine",
                "https://example.edu/week-1/worked-example-atwood-machine",
            )
        )

    def test_exact_collection_tokens_override_generic_notes(self) -> None:
        cases = (
            (
                "Labs",
                "https://ocw.mit.edu/courses/example/pages/labs",
                "labs",
            ),
            (
                "Projects",
                "https://ocw.mit.edu/courses/example/pages/projects",
                "projects",
            ),
            (
                "Labs — Homework 1",
                "https://ocw.mit.edu/courses/example/pages/labs/hw01",
                "assignments",
            ),
            (
                "Projects — Final Exam",
                "https://ocw.mit.edu/courses/example/pages/projects/final",
                "exams",
            ),
        )
        for title, url, expected in cases:
            with self.subTest(title=title):
                self.assertEqual(classify_resource(title, url), expected)

    def test_specific_titles_do_not_get_overridden_by_incidental_tokens(self) -> None:
        cases = (
            (
                "Final Project",
                "https://example.edu/files/ece3400_finalproject.pdf",
                "projects",
            ),
            (
                "Calendar",
                "https://example.edu/course/pages/calendar",
                "course",
            ),
            (
                "Experiments with Photons",
                "https://example.edu/course/resources/lecnotes2",
                "notes",
            ),
        )
        for title, url, expected in cases:
            with self.subTest(title=title):
                self.assertEqual(classify_resource(title, url), expected)

    def test_host_semantics_outrank_incidental_technology_and_project_words(
        self,
    ) -> None:
        cases = (
            (
                "Introduction to FPGA and Verilog",
                "https://youtu.be/yvqkg44_DQA",
                "video",
            ),
            (
                "Final project discussion",
                "https://www.youtube.com/watch?v=example",
                "video",
            ),
            (
                "Real-Time Project for Embedded Systems",
                "https://www.coursera.org/learn/real-time-project-embedded-systems",
                "course",
            ),
            (
                "Buy at MIT Press",
                (
                    "https://mitpress.mit.edu/9780262542364/"
                    "introduction-to-computation-and-programming-using-python"
                ),
                "textbook",
            ),
        )
        for title, url, expected in cases:
            with self.subTest(title=title):
                self.assertEqual(classify_resource(title, url), expected)

    def test_code_requires_artifact_or_tutorial_evidence_not_a_bare_tool_word(
        self,
    ) -> None:
        cases = (
            (
                "Least squares and least norm solutions using Matlab",
                "https://see.stanford.edu/materials/lsoeldsee263/Additional4-ls_ln_matlab.pdf",
                "notes",
            ),
            (
                "Python Tutorial",
                "https://example.edu/course/pages/python-tutorial",
                "notes",
            ),
            (
                "Starter files",
                "https://example.edu/course/ps0_code.zip",
                "code",
            ),
        )
        for title, url, expected in cases:
            with self.subTest(title=title):
                self.assertEqual(classify_resource(title, url), expected)


class ExtractionTests(unittest.TestCase):
    def test_extracts_only_real_https_learning_links(self) -> None:
        html = """
        <html><body>
          <a href="/course/notes/week-1.pdf">Lecture notes 1</a>
          <a href="/course/hw/hw1.pdf?utm_campaign=test">Homework 1</a>
          <a href="/course/images/diagram.png">Lecture diagram</a>
          <a href="http://example.edu/course/exam.pdf">Exam</a>
          <a href="/privacy/">Privacy policy</a>
        </body></html>
        """
        resources, _ = extract_resources_from_html(
            course_id=9,
            html=html,
            page_url="https://example.edu/course/",
            seed_url="https://example.edu/course/",
        )
        self.assertEqual(
            [item["kind"] for item in resources],
            ["notes", "assignments"],
        )
        self.assertEqual(
            resources[1]["url"],
            "https://example.edu/course/hw/hw1.pdf",
        )

    def test_deduplicates_and_balances_kinds(self) -> None:
        resources = []
        for index in range(5):
            resources.append(
                {
                    "course_id": 1,
                    "kind": "notes",
                    "title": f"Note {index}",
                    "url": f"https://example.edu/n{index}",
                    "access": "open",
                    "status": "available",
                    "last_verified": "2026-07-28",
                    "source_url": "https://example.edu/course/",
                }
            )
        resources.append(
            {
                "course_id": 1,
                "kind": "exams",
                "title": "Exam",
                "url": "https://example.edu/exam",
                "access": "open",
                "status": "available",
                "last_verified": "2026-07-28",
                "source_url": "https://example.edu/course/",
            }
        )
        selected = de_duplicate_and_limit(resources, max_per_course=2)
        self.assertEqual({item["kind"] for item in selected}, {"notes", "exams"})

    def test_migrates_in_flight_checkpoint_kinds(self) -> None:
        checkpoint = {
            "course_resources": {
                "1": [
                    {"kind": "syllabus"},
                    {"kind": "reading"},
                    {"kind": "exams"},
                ]
            }
        }
        migrate_checkpoint_kinds(checkpoint)
        self.assertEqual(
            [item["kind"] for item in checkpoint["course_resources"]["1"]],
            ["course", "notes", "exams"],
        )


class PrecisionRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        root = Path(__file__).resolve().parents[1]
        candidates = json.loads(
            (root / "data" / "course_candidates.json").read_text(encoding="utf-8")
        )
        cls.candidates = {candidate["id"]: candidate for candidate in candidates}

    def resource(
        self, course_id: int, title: str, url: str, source_url: str
    ) -> dict[str, object]:
        return {
            "course_id": course_id,
            "kind": "labs",
            "title": title,
            "url": url,
            "access": "open",
            "status": "available",
            "last_verified": "2026-07-28",
            "source_url": source_url,
        }

    def assert_rejected(
        self, course_id: int, title: str, url: str, source_url: str
    ) -> None:
        allowed, _ = resource_relevance(
            self.resource(course_id, title, url, source_url),
            self.candidates[course_id],
        )
        self.assertFalse(allowed)

    def test_product_platform_navigation_is_rejected(self) -> None:
        cases = [
            (
                82,
                "Project Management Certificate",
                "https://www.coursera.org/articles/project-management",
            ),
            (
                91,
                "Digital Marketing Certificate",
                "https://www.coursera.org/articles/digital-marketing",
            ),
            (
                111,
                "Software Developer Career Guide",
                "https://www.coursera.org/articles/software-developer",
            ),
            (
                122,
                "Python for Beginners",
                "https://www.edx.org/learn/python",
            ),
            (
                122,
                "Project Management",
                "https://www.edx.org/projects",
            ),
        ]
        for course_id, title, url in cases:
            with self.subTest(course_id=course_id, title=title):
                self.assert_rejected(
                    course_id,
                    title,
                    url,
                    self.candidates[course_id]["url"],
                )

    def test_other_platform_course_product_is_not_a_course_resource(self) -> None:
        source = self.candidates[63]["url"]
        resource = self.resource(
            63,
            "Introduction to Embedded Systems Software and Development Environments",
            "https://www.coursera.org/learn/introduction-embedded-systems",
            source,
        )
        allowed, reason = resource_relevance(resource, self.candidates[63])
        self.assertFalse(allowed)
        self.assertEqual(reason, "off-course-platform-course")

    def test_publisher_product_is_paid_textbook_not_code(self) -> None:
        source = (
            "https://ocw.mit.edu/courses/"
            "6-100l-introduction-to-cs-and-programming-using-python-fall-2022/"
            "pages/readings"
        )
        resource = self.resource(
            15,
            "Buy at MIT Press",
            (
                "https://mitpress.mit.edu/9780262542364/"
                "introduction-to-computation-and-programming-using-python"
            ),
            source,
        )
        resource["kind"] = "code"
        normalize_resource_title_and_kind(resource)
        allowed, _ = resource_relevance(resource, self.candidates[15])
        self.assertTrue(allowed)
        self.assertEqual(resource["kind"], "textbook")
        self.assertEqual(resource["access"], "paid")

    def test_restricted_direct_file_is_not_advertised_as_public_material(self) -> None:
        source = "https://courses.physics.illinois.edu/ece310/su2026/homework.html"
        resource = self.resource(
            94,
            "Homework 1",
            "https://courses.physics.illinois.edu/ece310/su2026/secure/hw01.pdf",
            source,
        )
        allowed, reason = resource_relevance(resource, self.candidates[94])
        self.assertFalse(allowed)
        self.assertEqual(reason, "restricted-direct-resource")

    def test_auth_gated_video_is_not_advertised_as_public_material(self) -> None:
        source = "https://courses.physics.illinois.edu/ece311/su2025/lab.html"
        resource = self.resource(
            95,
            "Lab 1 walkthrough",
            "https://mediaspace.illinois.edu/media/t/1_1xw6bgin",
            source,
        )
        allowed, reason = resource_relevance(resource, self.candidates[95])
        self.assertFalse(allowed)
        self.assertEqual(reason, "auth-gated-resource")

    def test_restricted_resource_normalizes_access_and_status_conservatively(
        self,
    ) -> None:
        cases = (
            (
                105,
                "Midterm solution",
                "https://web.stanford.edu/class/ee359/restricted/mt20_soln.pdf",
            ),
            (
                95,
                "Lab 1 walkthrough",
                "https://mediaspace.illinois.edu/media/t/1_1xw6bgin",
            ),
            (
                48,
                "GDB reference card",
                "https://inst.eecs.berkeley.edu/%7Ecs61c/resources/gdb5-refcard.pdf",
            ),
        )
        for course_id, title, url in cases:
            with self.subTest(course_id=course_id, url=url):
                resource = self.resource(
                    course_id,
                    title,
                    url,
                    self.candidates[course_id]["url"],
                )
                normalize_resource_title_and_kind(resource)
                self.assertEqual(resource["access"], "institutional")
                self.assertEqual(resource["status"], "degraded")

    def test_global_research_channels_and_repositories_are_rejected(self) -> None:
        self.assert_rejected(
            44,
            "Research Projects",
            "https://www2.eecs.berkeley.edu/Research/Projects",
            self.candidates[44]["url"],
        )
        self.assert_rejected(
            27,
            "GitHub",
            "https://github.com/digilent",
            self.candidates[27]["url"],
        )
        self.assert_rejected(
            27,
            "Digilent videos",
            "https://www.youtube.com/@digilent",
            self.candidates[27]["url"],
        )

    def test_generic_faculty_publications_require_course_match(self) -> None:
        source = self.candidates[38]["url"]
        self.assert_rejected(
            38,
            "BurstLink Video",
            "https://people.inf.ethz.ch/omutlu/pub/burstlink.pdf",
            source,
        )
        self.assert_rejected(
            38,
            "TCP Video",
            "https://www.youtube.com/watch?v=unrelated",
            source,
        )
        allowed, _ = resource_relevance(
            self.resource(
                38,
                "Digital Design and Computer Architecture video playlist",
                "https://www.youtube.com/playlist?list=course",
                source,
            ),
            self.candidates[38],
        )
        self.assertTrue(allowed)

    def test_same_course_modules_are_notes_not_parent_collection_kind(self) -> None:
        source = self.candidates[19]["url"]
        resource = self.resource(
            19,
            "Circuit Abstractions",
            (
                "https://ocw.mit.edu/courses/"
                "6-01sc-introduction-to-electrical-engineering-and-computer-"
                "science-i-spring-2011/pages/circuit-abstractions"
            ),
            source,
        )
        resource["kind"] = "exams"
        allowed, _ = resource_relevance(resource, self.candidates[19])
        self.assertTrue(allowed)
        self.assertEqual(resource["kind"], "notes")

    def test_same_course_projects_use_projects_kind(self) -> None:
        source = self.candidates[19]["url"]
        resource = self.resource(
            19,
            "Projects",
            (
                "https://ocw.mit.edu/courses/"
                "6-01sc-introduction-to-electrical-engineering-and-computer-"
                "science-i-spring-2011/pages/projects"
            ),
            source,
        )
        resource["kind"] = "labs"
        allowed, _ = resource_relevance(resource, self.candidates[19])
        self.assertTrue(allowed)
        self.assertEqual(resource["kind"], "projects")

    def test_placeholder_and_generic_external_resources_are_rejected(self) -> None:
        self.assert_rejected(
            128,
            "Syllabus",
            "https://archive.nptel.ac.in/content/syllabus_pdf/undefined.pdf",
            self.candidates[128]["url"],
        )
        self.assert_rejected(
            94,
            "video",
            "https://www.youtube.com/watch?v=generic",
            "https://courses.physics.illinois.edu/ece310/su2026/homework.html",
        )

    def test_generic_pdf_titles_use_direct_url_kind_tokens(self) -> None:
        cases = [
            (
                11,
                (
                    "https://ocw.mit.edu/courses/8-02x-physics-ii-electricity-"
                    "magnetism-with-an-experimental-focus-spring-2005/"
                    "resources/05_prct_qz3b_sol"
                ),
                "https://ocw.mit.edu/courses/example/pages/exams",
                "exams",
                "Practice Quiz 3B Solution (PDF)",
            ),
            (
                16,
                (
                    "https://ocw.mit.edu/courses/6-087-practical-programming-"
                    "in-c-january-iap-2010/resources/mit6_087iap10_lec01"
                ),
                "https://ocw.mit.edu/courses/example/pages/lecture-notes",
                "notes",
                "Lecture 01 (PDF)",
            ),
            (
                18,
                (
                    "https://ocw.mit.edu/courses/6-055j-the-art-of-"
                    "approximation/resources/hw01"
                ),
                "https://ocw.mit.edu/courses/example/pages/assignments",
                "assignments",
                "Homework 01 (PDF)",
            ),
            (
                11,
                (
                    "https://ocw.mit.edu/courses/8-02x-physics-ii-electricity-"
                    "magnetism-with-an-experimental-focus-spring-2005/"
                    "resources/2_06_2002_edited"
                ),
                "https://ocw.mit.edu/courses/example/pages/lecture-notes",
                "notes",
                "Notes resource: 2 06 2002 edited (PDF)",
            ),
        ]
        for course_id, url, source_url, expected_kind, expected_title in cases:
            with self.subTest(course_id=course_id):
                resource = self.resource(course_id, "PDF", url, source_url)
                normalize_resource_title_and_kind(resource)
                self.assertEqual(resource["kind"], expected_kind)
                self.assertEqual(resource["title"], expected_title)

    def test_title_quality_gate_counts_generic_and_duplicate_titles(self) -> None:
        first = self.resource(
            18,
            "PDF",
            "https://example.edu/hw01",
            self.candidates[18]["url"],
        )
        second = dict(first)
        second["url"] = "https://example.edu/hw02"
        self.assertEqual(
            title_quality_counts([first, second]),
            {"generic_title_count": 2, "duplicate_title_count": 1},
        )

    def test_generated_fallback_title_is_reclassified_idempotently(self) -> None:
        resource = self.resource(
            11,
            "Lab resource: 2 06 2002 edited (PDF)",
            (
                "https://ocw.mit.edu/courses/8-02x-physics-ii-electricity-"
                "magnetism-with-an-experimental-focus-spring-2005/"
                "resources/2_06_2002_edited"
            ),
            "https://ocw.mit.edu/courses/example/pages/lecture-notes",
        )
        resource["kind"] = "labs"
        normalize_resource_title_and_kind(resource)
        self.assertEqual(resource["kind"], "notes")
        self.assertEqual(
            resource["title"],
            "Notes resource: 2 06 2002 edited (PDF)",
        )


if __name__ == "__main__":
    unittest.main()
