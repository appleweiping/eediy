from __future__ import annotations

import json
import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pytest

import scripts.check_external_links as external_links
from scripts.check_external_links import (
    LinkChecker,
    annotate_review_decisions,
    check_urls,
    classify_http_status,
    collect_external_urls,
    load_review_ledger,
    result_issues,
    review_approval_counts,
)


def _valid_ledger_payload(
    *,
    reviewed_at: str = "2026-07-30",
) -> dict[str, object]:
    return {
        "reviewed_at": reviewed_at,
        "reviewer": "independent review",
        "summary": {
            "reviewed": 1,
            "retain": 1,
            "replace": 0,
            "remove": 0,
        },
        "groups": [
            {
                "name": "Official course index",
                "decision": "retain",
                "automation_reason": "robots policy",
                "allowed_reason_codes": ["robots_denied"],
                "method": "Exact href on the official index.",
                "evidence": ["https://example.edu/index"],
                "urls": ["https://example.edu/course"],
            }
        ],
    }


def _write_ledger(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")


@pytest.mark.parametrize("status", [400, 401, 403, 429, 451, 500, 503])
def test_temporary_or_policy_statuses_require_review(status: int) -> None:
    assert classify_http_status(status)[0] == "review"


def test_only_permanent_missing_statuses_fail() -> None:
    assert classify_http_status(200)[0] == "ok"
    assert classify_http_status(404)[0] == "failed"
    assert classify_http_status(410)[0] == "failed"
    assert classify_http_status(418)[0] == "review"


@pytest.mark.parametrize(
    ("status", "reason_code"),
    [(403, "http_403"), (404, "http_missing"), (500, "http_server_error")],
)
def test_healthy_outcome_cannot_contradict_http_status(
    status: int,
    reason_code: str,
) -> None:
    issues = result_issues(
        [
            {
                "url": "https://example.edu/course",
                "outcome": "ok",
                "http_status": status,
                "reason": "forged healthy cache entry",
                "reason_code": reason_code,
            }
        ],
        allow_review=True,
    )

    assert len(issues) == 1
    assert issues[0].severity == "error"
    assert issues[0].code == "external.result_inconsistent"


def test_poisoned_cache_entry_is_discarded_and_rechecked_offline(
    tmp_path: Path,
) -> None:
    url = "https://example.edu/course"
    cache_path = tmp_path / "external-links.json"
    cache_path.write_text(
        json.dumps(
            {
                "version": external_links.CACHE_VERSION,
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "results": {
                    url: {
                        "url": url,
                        "outcome": "ok",
                        "http_status": 404,
                        "reason": "resource is missing",
                        "reason_code": "http_missing",
                        "final_url": url,
                        "checked_at": datetime.now(timezone.utc).isoformat(),
                        "elapsed_ms": 1,
                        "from_cache": False,
                    }
                },
            }
        ),
        encoding="utf-8",
    )

    results = check_urls([url], cache_path=cache_path, offline=True)

    assert results[0]["outcome"] == "review"
    assert results[0]["reason_code"] == "offline_cache_miss"
    assert results[0]["from_cache"] is False


def test_only_ledger_retained_review_is_allowed_as_warning() -> None:
    unapproved = {
        "url": "https://example.edu/",
        "outcome": "review",
        "reason": "robots policy blocks automated checking",
        "http_status": None,
        "review_adjudication": {
            "recorded": False,
            "decision": None,
            "approved": False,
        },
    }
    approved = {
        **unapproved,
        "review_adjudication": {
            "recorded": True,
            "decision": "retain",
            "approved": True,
            "allowed_reason_codes": ["robots_denied"],
        },
    }
    strict = result_issues([approved], allow_review=False)
    allowed = result_issues([approved], allow_review=True)
    still_blocked = result_issues([unapproved], allow_review=True)
    assert strict[0].severity == "error"
    assert allowed[0].severity == "warning"
    assert still_blocked[0].severity == "error"
    assert "not counted as healthy" in allowed[0].message
    assert "manual decision=retain" in allowed[0].message
    assert "manual decision=unrecorded" in still_blocked[0].message


@pytest.mark.parametrize("status", [404, 410])
def test_missing_evidence_url_is_a_release_error(status: int) -> None:
    evidence_url = "https://example.edu/index"
    results = annotate_review_decisions(
        [
            {
                "url": evidence_url,
                "outcome": "failed",
                "http_status": status,
                "reason": "resource is missing",
            }
        ],
        external_links.ReviewLedger(
            reviewer="independent review",
            reviewed_at="2026-07-30",
            evidence_groups={evidence_url: "Official index"},
        ),
        target_urls=[],
        evidence_urls=[evidence_url],
    )

    issues = result_issues(results, allow_review=True)

    assert len(issues) == 1
    assert issues[0].severity == "error"
    assert issues[0].code == "external.evidence_failed"


@pytest.mark.parametrize(
    ("status", "reason"),
    [
        (403, "client access policy"),
        (None, "robots policy blocks automated checking"),
    ],
)
def test_attested_evidence_access_review_is_warning_but_not_target_retain(
    status: int | None,
    reason: str,
) -> None:
    target_url = "https://example.edu/course"
    evidence_url = "https://example.edu/index"
    ledger = external_links.ReviewLedger(
        {
            target_url: {
                "recorded": True,
                "decision": "retain",
                "approved": True,
                "group": "Official index",
                "allowed_reason_codes": ["http_403"],
            }
        },
        reviewer="independent review",
        reviewed_at="2026-07-30",
        evidence_groups={evidence_url: "Official index"},
    )
    results = annotate_review_decisions(
        [
            {
                "url": target_url,
                "outcome": "review",
                "http_status": 403,
                "reason": "access policy",
            },
            {
                "url": evidence_url,
                "outcome": "review",
                "http_status": status,
                "reason": reason,
            },
        ],
        ledger,
        target_urls=[target_url],
        evidence_urls=[evidence_url],
    )

    issues = result_issues(results, allow_review=True)

    assert [issue.severity for issue in issues] == ["warning", "warning"]
    assert issues[1].code == "external.evidence_review"
    assert "does not count as a target retain" in issues[1].message
    assert review_approval_counts(results) == (1, 0)


def test_non_policy_evidence_review_remains_a_release_error() -> None:
    evidence_url = "https://example.edu/index"
    results = annotate_review_decisions(
        [
            {
                "url": evidence_url,
                "outcome": "review",
                "http_status": None,
                "reason": "TLS handshake failed",
            }
        ],
        external_links.ReviewLedger(
            reviewer="independent review",
            reviewed_at="2026-07-30",
            evidence_groups={evidence_url: "Official index"},
        ),
        target_urls=[],
        evidence_urls=[evidence_url],
    )

    issues = result_issues(results, allow_review=True)

    assert issues[0].severity == "error"
    assert issues[0].code == "external.evidence_review"
    assert review_approval_counts(results) == (0, 0)


def test_target_evidence_overlap_applies_both_policies() -> None:
    url = "https://example.edu/course"
    ledger = external_links.ReviewLedger(
        {
            url: {
                "recorded": True,
                "decision": "retain",
                "approved": True,
                "allowed_reason_codes": ["tls_error"],
            }
        },
        reviewer="independent review",
        reviewed_at="2026-07-29",
        evidence_groups={url: "Exact target"},
    )
    results = annotate_review_decisions(
        [
            {
                "url": url,
                "outcome": "review",
                "http_status": None,
                "reason": "SSLError: certificate chain unavailable",
                "reason_code": "tls_error",
            }
        ],
        ledger,
        target_urls=[url],
        evidence_urls=[url],
    )

    issues = result_issues(results, allow_review=True)

    assert results[0]["link_roles"] == ["target", "evidence"]
    assert [issue.code for issue in issues] == [
        "external.review",
        "external.evidence_review",
    ]
    assert [issue.severity for issue in issues] == ["warning", "error"]


def test_robots_word_in_dns_failure_cannot_spoof_evidence_policy() -> None:
    url = "https://robots.invalid/evidence"
    results = annotate_review_decisions(
        [
            {
                "url": url,
                "outcome": "review",
                "http_status": None,
                "reason": "DNS resolution failed for robots.invalid",
                "reason_code": "dns_resolution",
            }
        ],
        external_links.ReviewLedger(
            reviewer="independent review",
            reviewed_at="2026-07-29",
            evidence_groups={url: "Spoof attempt"},
        ),
        target_urls=[],
        evidence_urls=[url],
    )

    issues = result_issues(results, allow_review=True)

    assert len(issues) == 1
    assert issues[0].severity == "error"
    assert issues[0].code == "external.evidence_review"


def test_target_review_reason_must_match_ledger_allowlist() -> None:
    url = "https://example.edu/course"
    results = annotate_review_decisions(
        [
            {
                "url": url,
                "outcome": "review",
                "http_status": 403,
                "reason": "client access policy",
                "reason_code": "http_403",
            }
        ],
        {
            url: {
                "recorded": True,
                "decision": "retain",
                "approved": True,
                "allowed_reason_codes": ["robots_denied"],
            }
        },
        target_urls=[url],
    )

    issues = result_issues(results, allow_review=True)

    assert issues[0].severity == "error"
    assert review_approval_counts(results) == (0, 1)


def test_review_ledger_parses_grouped_decisions_and_canonicalizes_urls(
    tmp_path: Path,
) -> None:
    path = tmp_path / "reviews.json"
    path.write_text(
        json.dumps(
            {
                "reviewed_at": "2026-07-30",
                "reviewer": "independent review",
                "groups": [
                    {
                        "name": "Official course index",
                        "decision": "retain",
                        "automation_reason": "robots policy",
                        "allowed_reason_codes": ["robots_denied"],
                        "method": "Exact href on the official index.",
                        "evidence": ["https://example.edu/index"],
                        "urls": ["HTTPS://EXAMPLE.EDU/course#week-1"],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    reviews = load_review_ledger(path, today=date(2026, 7, 30))

    assert list(reviews) == ["https://example.edu/course"]
    assert reviews["https://example.edu/course"] == {
        "recorded": True,
        "decision": "retain",
        "approved": True,
        "group": "Official course index",
        "reviewed_at": "2026-07-30",
        "reviewer": "independent review",
        "automation_reason": "robots policy",
        "method": "Exact href on the official index.",
        "allowed_reason_codes": ["robots_denied"],
        "evidence": ["https://example.edu/index"],
    }


def test_review_ledger_rejects_invalid_decision(tmp_path: Path) -> None:
    path = tmp_path / "reviews.json"
    path.write_text(
        json.dumps(
            {
                "reviewed_at": "2026-07-30",
                "reviewer": "independent review",
                "groups": [
                    {
                        "name": "Ambiguous",
                        "decision": "maybe",
                        "automation_reason": "robots policy",
                        "allowed_reason_codes": ["robots_denied"],
                        "method": "Checked the official index.",
                        "evidence": ["https://example.edu/index"],
                        "urls": ["https://example.edu/course"],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(external_links.QualityError, match="invalid decision"):
        load_review_ledger(path, today=date(2026, 7, 30))


@pytest.mark.parametrize(
    ("missing_key", "message"),
    [
        ("reviewer", "reviewer must be a non-empty string"),
        ("reviewed_at", "reviewed_at must be an ISO date"),
    ],
)
def test_review_ledger_requires_reviewer_and_review_date(
    tmp_path: Path,
    missing_key: str,
    message: str,
) -> None:
    payload = _valid_ledger_payload()
    del payload[missing_key]
    path = tmp_path / "reviews.json"
    _write_ledger(path, payload)

    with pytest.raises(external_links.QualityError, match=message):
        load_review_ledger(path, today=date(2026, 7, 30))


@pytest.mark.parametrize("reviewed_at", ["2026-7-30", "20260730", "2026-02-30"])
def test_review_ledger_requires_strict_valid_iso_date(
    tmp_path: Path,
    reviewed_at: str,
) -> None:
    path = tmp_path / "reviews.json"
    _write_ledger(path, _valid_ledger_payload(reviewed_at=reviewed_at))

    with pytest.raises(external_links.QualityError, match="valid ISO date|ISO date"):
        load_review_ledger(path, today=date(2026, 7, 30))


def test_review_ledger_rejects_stale_and_future_dates(tmp_path: Path) -> None:
    path = tmp_path / "reviews.json"
    current = date(2026, 7, 30)

    _write_ledger(
        path,
        _valid_ledger_payload(reviewed_at=(current - timedelta(days=15)).isoformat()),
    )
    with pytest.raises(external_links.QualityError, match="stale"):
        load_review_ledger(path, today=current)

    # The maximum is inclusive and configurable.
    _write_ledger(
        path,
        _valid_ledger_payload(reviewed_at=(current - timedelta(days=15)).isoformat()),
    )
    assert len(load_review_ledger(path, today=current, max_age_days=15)) == 1

    _write_ledger(
        path,
        _valid_ledger_payload(reviewed_at=(current + timedelta(days=1)).isoformat()),
    )
    with pytest.raises(external_links.QualityError, match="future"):
        load_review_ledger(path, today=current, max_age_days=30)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("automation_reason", "", "automation_reason"),
        ("method", None, "method"),
        ("allowed_reason_codes", [], "allowed_reason_codes"),
        ("evidence", [], "at least one HTTPS evidence"),
    ],
)
def test_review_ledger_requires_group_method_reason_and_evidence(
    tmp_path: Path,
    field: str,
    value: object,
    message: str,
) -> None:
    payload = _valid_ledger_payload()
    groups = payload["groups"]
    assert isinstance(groups, list)
    groups[0][field] = value
    path = tmp_path / "reviews.json"
    _write_ledger(path, payload)

    with pytest.raises(external_links.QualityError, match=message):
        load_review_ledger(path, today=date(2026, 7, 30))


@pytest.mark.parametrize(
    "evidence",
    [
        "http://example.edu/index",
        "https://not a host/index",
        "https:///missing-host",
        "https://example.edu/%not-escaped",
        "https://user:secret@example.edu/index",
    ],
)
def test_review_ledger_rejects_non_https_or_malformed_evidence(
    tmp_path: Path,
    evidence: str,
) -> None:
    payload = _valid_ledger_payload()
    groups = payload["groups"]
    assert isinstance(groups, list)
    groups[0]["evidence"] = [evidence]
    path = tmp_path / "reviews.json"
    _write_ledger(path, payload)

    with pytest.raises(external_links.QualityError, match="evidence URL"):
        load_review_ledger(path, today=date(2026, 7, 30))


def test_review_ledger_canonicalizes_and_rejects_duplicate_evidence(
    tmp_path: Path,
) -> None:
    payload = _valid_ledger_payload()
    groups = payload["groups"]
    assert isinstance(groups, list)
    groups.append(
        {
            "name": "Duplicate official index",
            "decision": "remove",
            "automation_reason": "HTTP 403",
            "allowed_reason_codes": ["http_403"],
            "method": "Checked the same official index.",
            "evidence": ["HTTPS://EXAMPLE.EDU.:443/index#duplicate"],
            "urls": ["https://example.edu/other"],
        }
    )
    payload["summary"] = {
        "reviewed": 2,
        "retain": 1,
        "replace": 0,
        "remove": 1,
    }
    path = tmp_path / "reviews.json"
    _write_ledger(path, payload)

    with pytest.raises(external_links.QualityError, match="evidence URL more than once"):
        load_review_ledger(path, today=date(2026, 7, 30))


def test_review_ledger_idna_hosts_cannot_duplicate_evidence(tmp_path: Path) -> None:
    payload = _valid_ledger_payload()
    groups = payload["groups"]
    assert isinstance(groups, list)
    groups[0]["evidence"] = ["https://bücher.example/index"]
    groups.append(
        {
            "name": "Punycode duplicate",
            "decision": "retain",
            "automation_reason": "robots policy",
            "allowed_reason_codes": ["robots_denied"],
            "method": "Checked the same IDNA host.",
            "evidence": ["https://xn--bcher-kva.example/index"],
            "urls": ["https://example.edu/other"],
        }
    )
    payload["summary"] = {
        "reviewed": 2,
        "retain": 2,
        "replace": 0,
        "remove": 0,
    }
    path = tmp_path / "reviews.json"
    _write_ledger(path, payload)

    with pytest.raises(external_links.QualityError, match="evidence URL more than once"):
        load_review_ledger(path, today=date(2026, 7, 30))


@pytest.mark.parametrize("max_age", [float("nan"), float("inf"), float("-inf"), -1])
def test_review_ledger_rejects_invalid_max_age(
    tmp_path: Path,
    max_age: float,
) -> None:
    path = tmp_path / "reviews.json"
    _write_ledger(path, _valid_ledger_payload())

    with pytest.raises(external_links.QualityError, match="finite non-negative"):
        load_review_ledger(
            path,
            today=date(2026, 7, 30),
            max_age_days=max_age,
        )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("reviewed", 2),
        ("retain", 0),
        ("replace", 1),
        ("remove", True),
    ],
)
def test_review_ledger_summary_must_match_target_decisions(
    tmp_path: Path,
    field: str,
    value: object,
) -> None:
    payload = _valid_ledger_payload()
    summary = payload["summary"]
    assert isinstance(summary, dict)
    summary[field] = value
    path = tmp_path / "reviews.json"
    _write_ledger(path, payload)

    with pytest.raises(external_links.QualityError, match="summary"):
        load_review_ledger(path, today=date(2026, 7, 30))


def test_repository_review_ledger_has_38_current_retained_targets() -> None:
    ledger = load_review_ledger(
        Path("data/external_link_reviews.json"),
        today=date(2026, 7, 29),
    )

    assert len(ledger) == 38
    assert len(ledger.evidence_urls) == 13
    assert ledger.reviewed_at == "2026-07-29"
    assert all(review["decision"] == "retain" for review in ledger.values())


def test_historical_ledger_entry_does_not_block_a_now_healthy_url() -> None:
    url = "https://example.edu/course"
    results = annotate_review_decisions(
        [_ok_result(url)],
        {
            url: {
                "recorded": True,
                "decision": "remove",
                "approved": False,
                "group": "Historical review",
            }
        },
    )

    assert results[0]["review_adjudication"]["decision"] == "remove"
    assert review_approval_counts(results) == (0, 0)
    assert result_issues(results, allow_review=True) == []


def test_url_collection_deduplicates_fragments(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "index.md").write_text(
        "[One](https://example.edu/path#one)\n"
        "[Two](https://example.edu/path#two)\n",
        encoding="utf-8",
    )
    assert collect_external_urls(docs) == ["https://example.edu/path"]


def test_network_and_tls_errors_require_review() -> None:
    class NetworkError(Exception):
        pass

    class FakeRequests:
        RequestException = NetworkError

        @staticmethod
        def get(*args: object, **kwargs: object) -> object:
            raise NetworkError("robots timeout")

        @staticmethod
        def head(*args: object, **kwargs: object) -> object:
            raise NetworkError("TLS handshake failed")

    checker = LinkChecker(timeout=0.01, retries=0, resolve_dns=False)
    checker.requests = FakeRequests()
    result = checker.check("https://example.edu/course")
    assert result["outcome"] == "review"
    assert "TLS handshake failed" in result["reason"]
    assert checker.check("http://example.edu/course")["outcome"] == "failed"


@pytest.mark.parametrize(
    "url",
    [
        "http://example.edu/course",
        "https://student:secret@example.edu/course",
        "https://localhost/course",
        "https://lab.localhost/course",
        "https://127.0.0.1/course",
        "https://10.0.0.8/course",
        "https://169.254.1.2/course",
        "https://[::1]/course",
        "https://[fe80::1]/course",
    ],
)
def test_explicitly_unsafe_targets_fail_without_network(url: str) -> None:
    class NoNetworkRequests:
        class RequestException(Exception):
            pass

        @staticmethod
        def head(*args: object, **kwargs: object) -> object:
            raise AssertionError("unsafe target must not be requested")

        @staticmethod
        def get(*args: object, **kwargs: object) -> object:
            raise AssertionError("unsafe target must not be requested")

    checker = LinkChecker(
        timeout=0.01,
        retries=0,
        respect_robots=False,
        resolve_dns=False,
    )
    checker.requests = NoNetworkRequests()
    result = checker.check(url)
    assert result["outcome"] == "failed"
    assert result["http_status"] is None


def test_hostname_resolving_to_non_global_address_fails_without_network() -> None:
    class NoNetworkRequests:
        class RequestException(Exception):
            pass

        @staticmethod
        def head(*args: object, **kwargs: object) -> object:
            raise AssertionError("private DNS target must not be requested")

        @staticmethod
        def get(*args: object, **kwargs: object) -> object:
            raise AssertionError("private DNS target must not be requested")

    checker = LinkChecker(
        retries=0,
        respect_robots=False,
        resolver=lambda _hostname, _port: ["93.184.216.34", "192.168.1.9"],
    )
    checker.requests = NoNetworkRequests()
    result = checker.check("https://example.edu/course")
    assert result["outcome"] == "failed"
    assert "non-global" in result["reason"]
    assert "192.168.1.9" in result["reason"]


def test_dns_resolution_failure_requires_review_without_network() -> None:
    class NoNetworkRequests:
        class RequestException(Exception):
            pass

        @staticmethod
        def head(*args: object, **kwargs: object) -> object:
            raise AssertionError("unresolved target must not be requested")

        @staticmethod
        def get(*args: object, **kwargs: object) -> object:
            raise AssertionError("unresolved target must not be requested")

    def failed_resolver(_hostname: str, _port: int) -> list[str]:
        raise socket.gaierror("name not found")

    checker = LinkChecker(
        retries=0,
        respect_robots=False,
        resolver=failed_resolver,
    )
    checker.requests = NoNetworkRequests()
    result = checker.check("https://missing.example.edu/course")
    assert result["outcome"] == "review"
    assert "DNS resolution failed" in result["reason"]


def test_dns_target_validation_is_cached_per_host_and_port() -> None:
    calls = 0

    def resolver(_hostname: str, _port: int) -> list[str]:
        nonlocal calls
        calls += 1
        return ["93.184.216.34"]

    checker = LinkChecker(
        retries=0,
        respect_robots=False,
        resolver=resolver,
    )

    checker._validate_target("https://example.edu/one")
    checker._validate_target("https://example.edu/two")

    assert calls == 1


def test_unsafe_redirect_is_rejected_before_following() -> None:
    class FakeResponse:
        status_code = 302
        headers = {"Location": "https://127.0.0.1/admin"}

        @staticmethod
        def close() -> None:
            return None

    class FakeRequests:
        class RequestException(Exception):
            pass

        def __init__(self) -> None:
            self.calls: list[tuple[str, dict[str, object]]] = []

        def head(self, url: str, **kwargs: object) -> FakeResponse:
            self.calls.append((url, kwargs))
            return FakeResponse()

        @staticmethod
        def get(*args: object, **kwargs: object) -> object:
            raise AssertionError("GET fallback must not run")

    checker = LinkChecker(
        retries=0,
        respect_robots=False,
        resolve_dns=False,
    )
    fake_requests = FakeRequests()
    checker.requests = fake_requests
    result = checker.check("https://example.edu/course")
    assert result["outcome"] == "failed"
    assert "non-global IP" in result["reason"]
    assert [url for url, _kwargs in fake_requests.calls] == [
        "https://example.edu/course"
    ]
    assert fake_requests.calls[0][1]["allow_redirects"] is False


def test_redirect_dns_failure_requires_review_before_following() -> None:
    class FakeResponse:
        status_code = 302
        headers = {"Location": "https://missing.example.edu/course"}

        @staticmethod
        def close() -> None:
            return None

    class FakeRequests:
        class RequestException(Exception):
            pass

        def __init__(self) -> None:
            self.calls: list[str] = []

        def head(self, url: str, **kwargs: object) -> FakeResponse:
            assert kwargs["allow_redirects"] is False
            self.calls.append(url)
            return FakeResponse()

        @staticmethod
        def get(*args: object, **kwargs: object) -> object:
            raise AssertionError("GET fallback must not run")

    def resolver(hostname: str, _port: int) -> list[str]:
        if hostname == "missing.example.edu":
            raise socket.gaierror("name not found")
        return ["93.184.216.34"]

    checker = LinkChecker(
        retries=0,
        respect_robots=False,
        resolver=resolver,
    )
    fake_requests = FakeRequests()
    checker.requests = fake_requests
    result = checker.check("https://example.edu/course")
    assert result["outcome"] == "review"
    assert "DNS resolution failed" in result["reason"]
    assert fake_requests.calls == ["https://example.edu/course"]


def test_safe_redirects_are_followed_manually() -> None:
    class FakeResponse:
        def __init__(
            self,
            status_code: int,
            location: str | None = None,
        ) -> None:
            self.status_code = status_code
            self.headers = {"Location": location} if location else {}

        @staticmethod
        def close() -> None:
            return None

    class FakeRequests:
        class RequestException(Exception):
            pass

        def __init__(self) -> None:
            self.calls: list[tuple[str, bool]] = []

        def head(self, url: str, **kwargs: object) -> FakeResponse:
            self.calls.append((url, bool(kwargs["allow_redirects"])))
            if url == "https://example.edu/course":
                return FakeResponse(301, "/new-course")
            return FakeResponse(200)

        @staticmethod
        def get(*args: object, **kwargs: object) -> object:
            raise AssertionError("GET fallback must not run")

    resolved_hosts: list[str] = []

    def resolver(hostname: str, _port: int) -> list[str]:
        resolved_hosts.append(hostname)
        return ["93.184.216.34"]

    checker = LinkChecker(
        retries=0,
        respect_robots=False,
        resolver=resolver,
    )
    fake_requests = FakeRequests()
    checker.requests = fake_requests
    result = checker.check("https://example.edu/course")
    assert result["outcome"] == "ok"
    assert result["final_url"] == "https://example.edu/new-course"
    assert fake_requests.calls == [
        ("https://example.edu/course", False),
        ("https://example.edu/new-course", False),
    ]
    assert resolved_hosts == ["example.edu"]


@pytest.mark.parametrize(
    ("get_status", "expected_outcome"),
    [(200, "ok"), (404, "failed"), (410, "failed"), (503, "review")],
)
def test_head_missing_is_confirmed_by_get(
    get_status: int, expected_outcome: str
) -> None:
    class FakeResponse:
        def __init__(self, status_code: int) -> None:
            self.status_code = status_code
            self.url = "https://example.edu/course"

        @staticmethod
        def close() -> None:
            return None

    class FakeRequests:
        class RequestException(Exception):
            pass

        def __init__(self) -> None:
            self.get_calls = 0

        @staticmethod
        def head(*args: object, **kwargs: object) -> FakeResponse:
            return FakeResponse(404)

        def get(self, *args: object, **kwargs: object) -> FakeResponse:
            self.get_calls += 1
            return FakeResponse(get_status)

    checker = LinkChecker(
        timeout=0.01,
        retries=0,
        respect_robots=False,
        resolve_dns=False,
    )
    fake_requests = FakeRequests()
    checker.requests = fake_requests
    result = checker.check("https://example.edu/course")
    assert fake_requests.get_calls == 1
    assert result["outcome"] == expected_outcome


def test_same_origin_robots_fetch_is_single_flight_and_path_specific() -> None:
    class FakeResponse:
        status_code = 200
        text = "User-agent: *\nDisallow: /private\n"

        @staticmethod
        def close() -> None:
            return None

    class FakeRequests:
        class RequestException(Exception):
            pass

        def __init__(self) -> None:
            self.calls = 0
            self.lock = threading.Lock()

        def get(self, *args: object, **kwargs: object) -> FakeResponse:
            with self.lock:
                self.calls += 1
            time.sleep(0.05)
            return FakeResponse()

    checker = LinkChecker(timeout=1, retries=0, resolve_dns=False)
    fake_requests = FakeRequests()
    checker.requests = fake_requests
    urls = [
        "https://example.edu/public/one",
        "https://example.edu/public/two",
        "https://example.edu/private/one",
        "https://example.edu/private/two",
    ]
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(checker._robots_allows, urls))
    assert fake_requests.calls == 1
    assert [allowed for allowed, _ in results] == [True, True, False, False]


def _ok_result(url: str) -> dict[str, object]:
    return {
        "url": url,
        "outcome": "ok",
        "http_status": 200,
        "reason": "successful response",
        "final_url": url,
        "checked_at": "2026-07-29T00:00:00+00:00",
        "elapsed_ms": 1,
        "from_cache": False,
    }


def test_completed_batches_survive_interruption(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    cache_path = tmp_path / "external-links.json"
    first_url = "https://example.edu/a"
    interrupted_url = "https://example.edu/b"
    checkpoint_written = threading.Event()
    real_atomic_write = external_links.atomic_write

    def signaling_atomic_write(path: Path, content: str) -> None:
        real_atomic_write(path, content)
        payload = json.loads(content)
        if first_url in payload["results"]:
            checkpoint_written.set()

    class InterruptingChecker:
        def __init__(self, **kwargs: object) -> None:
            pass

        def check(self, url: str) -> dict[str, object]:
            if url == first_url:
                return _ok_result(url)
            assert checkpoint_written.wait(timeout=2)
            raise KeyboardInterrupt

    monkeypatch.setattr(external_links, "atomic_write", signaling_atomic_write)
    monkeypatch.setattr(external_links, "LinkChecker", InterruptingChecker)
    with pytest.raises(KeyboardInterrupt):
        check_urls(
            [first_url, interrupted_url],
            cache_path=cache_path,
            workers=1,
            retries=0,
            checkpoint_batch_size=1,
        )

    payload = json.loads(cache_path.read_text(encoding="utf-8"))
    assert payload["version"] == external_links.CACHE_VERSION
    assert list(payload["results"]) == [first_url]
    assert payload["results"][first_url]["outcome"] == "ok"


def test_one_future_exception_does_not_abort_other_urls(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    bad_url = "https://example.edu/bad"

    class IsolatingChecker:
        def __init__(self, **kwargs: object) -> None:
            pass

        @staticmethod
        def check(url: str) -> dict[str, object]:
            if url == bad_url:
                raise RuntimeError("isolated failure")
            return _ok_result(url)

    monkeypatch.setattr(external_links, "LinkChecker", IsolatingChecker)
    results = check_urls(
        ["https://example.edu/a", bad_url, "https://example.edu/c"],
        cache_path=tmp_path / "external-links.json",
        workers=3,
        retries=0,
    )
    by_url = {result["url"]: result for result in results}
    assert by_url["https://example.edu/a"]["outcome"] == "ok"
    assert by_url["https://example.edu/c"]["outcome"] == "ok"
    assert by_url[bad_url]["outcome"] == "review"
    assert "RuntimeError" in by_url[bad_url]["reason"]


def test_cli_payload_records_approved_and_unapproved_reviews(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    approved_url = "https://example.edu/approved"
    unapproved_url = "https://example.edu/unapproved"
    ledger_path = tmp_path / "reviews.json"
    output_path = tmp_path / "external-links.json"
    ledger_path.write_text(
        json.dumps(
            {
                "reviewed_at": "2026-07-30",
                "reviewer": "independent review",
                "groups": [
                    {
                        "name": "Official evidence",
                        "decision": "retain",
                        "automation_reason": "access policy",
                        "allowed_reason_codes": ["http_403"],
                        "method": "Confirmed on the primary page.",
                        "evidence": ["https://example.edu/index"],
                        "urls": [approved_url],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    def fake_check_urls(*args: object, **kwargs: object) -> list[dict[str, object]]:
        return [
            {
                "url": approved_url,
                "outcome": "review",
                "http_status": 403,
                "reason": "access policy",
                "final_url": approved_url,
                "checked_at": "2026-07-30T00:00:00+00:00",
                "elapsed_ms": 1,
                "from_cache": False,
            },
            {
                "url": unapproved_url,
                "outcome": "review",
                "http_status": None,
                "reason": "robots policy",
                "final_url": unapproved_url,
                "checked_at": "2026-07-30T00:00:00+00:00",
                "elapsed_ms": 1,
                "from_cache": False,
            },
            {
                "url": "https://example.edu/index",
                "outcome": "ok",
                "http_status": 200,
                "reason": "successful response",
                "final_url": "https://example.edu/index",
                "checked_at": "2026-07-30T00:00:00+00:00",
                "elapsed_ms": 1,
                "from_cache": False,
            },
        ]

    monkeypatch.setattr(
        external_links,
        "collect_external_urls",
        lambda *a, **k: [approved_url, unapproved_url],
    )
    monkeypatch.setattr(external_links, "check_urls", fake_check_urls)

    status = external_links.main(
        [
            "--allow-review",
            "--review-ledger",
            str(ledger_path),
            "--output",
            str(output_path),
            "--cache",
            str(tmp_path / "cache.json"),
        ]
    )

    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert status == 1
    assert payload["summary"]["review"] == 2
    assert payload["summary"]["review_approved"] == 1
    assert payload["summary"]["review_unapproved"] == 1
    assert payload["summary"]["target_total"] == 2
    assert payload["summary"]["target_review"] == 2
    assert payload["summary"]["evidence_total"] == 1
    assert payload["summary"]["evidence_ok"] == 1
    assert payload["summary"]["evidence_only"] == 1
    by_url = {result["url"]: result for result in payload["results"]}
    assert by_url[approved_url]["review_adjudication"]["decision"] == "retain"
    assert by_url[approved_url]["review_adjudication"]["method"] == (
        "Confirmed on the primary page."
    )
    assert by_url[unapproved_url]["review_adjudication"] == {
        "recorded": False,
        "decision": None,
        "approved": False,
    }
    assert by_url["https://example.edu/index"]["link_roles"] == ["evidence"]
    assert [issue["severity"] for issue in payload["issues"]] == [
        "warning",
        "error",
    ]
