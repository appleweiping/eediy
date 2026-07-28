from __future__ import annotations

import json
import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

import scripts.check_external_links as external_links
from scripts.check_external_links import (
    LinkChecker,
    check_urls,
    classify_http_status,
    collect_external_urls,
    result_issues,
)


@pytest.mark.parametrize("status", [400, 401, 403, 429, 451, 500, 503])
def test_temporary_or_policy_statuses_require_review(status: int) -> None:
    assert classify_http_status(status)[0] == "review"


def test_only_permanent_missing_statuses_fail() -> None:
    assert classify_http_status(200)[0] == "ok"
    assert classify_http_status(404)[0] == "failed"
    assert classify_http_status(410)[0] == "failed"
    assert classify_http_status(418)[0] == "review"


def test_manual_review_is_visible_even_when_allowed() -> None:
    result = {
        "url": "https://example.edu/",
        "outcome": "review",
        "reason": "robots policy blocks automated checking",
        "http_status": None,
    }
    strict = result_issues([result], allow_review=False)
    allowed = result_issues([result], allow_review=True)
    assert strict[0].severity == "error"
    assert allowed[0].severity == "warning"
    assert "not counted as healthy" in allowed[0].message


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
