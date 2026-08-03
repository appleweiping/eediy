from __future__ import annotations

import argparse
import ipaddress
import json
import socket
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.robotparser import RobotFileParser

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.quality_common import (
    Issue,
    QualityError,
    atomic_write,
    emit_issues,
    exit_code,
    is_external_url,
    iter_markdown_links,
    load_json,
    markdown_files,
    repo_path,
    stable_json,
)


USER_AGENT = "EEDIY-LinkChecker/1.0"
CACHE_VERSION = 3
PERMANENT_MISSING_STATUSES = frozenset({404, 410})
REDIRECT_STATUSES = frozenset({301, 302, 303, 307, 308})
MAX_REDIRECTS = 10

Resolver = Callable[[str, int], Iterable[str]]


class UnsafeTargetError(ValueError):
    """The URL explicitly points at a target the checker must never contact."""


class TargetResolutionError(RuntimeError):
    """The target could not be resolved and therefore needs manual review."""


class RedirectError(RuntimeError):
    """The redirect chain is malformed or exceeds the checker policy."""


def _system_resolver(hostname: str, port: int) -> Iterable[str]:
    return {
        str(sockaddr[0])
        for _family, _socktype, _proto, _canonname, sockaddr in socket.getaddrinfo(
            hostname,
            port,
            type=socket.SOCK_STREAM,
        )
    }


def _is_global_unicast(address: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    if isinstance(address, ipaddress.IPv6Address) and address.ipv4_mapped is not None:
        return _is_global_unicast(address.ipv4_mapped)
    return bool(
        address.is_global
        and not address.is_loopback
        and not address.is_private
        and not address.is_link_local
        and not address.is_multicast
        and not address.is_reserved
        and not address.is_unspecified
    )


def canonical_url(url: str) -> str:
    parsed = urlsplit(url.strip())
    return urlunsplit(
        (
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            parsed.path or "/",
            parsed.query,
            "",
        )
    )


def classify_http_status(status: int) -> tuple[str, str]:
    if 200 <= status < 300:
        return "ok", "successful response"
    if 300 <= status < 400:
        return "review", "redirect did not resolve to a successful response"
    if status in PERMANENT_MISSING_STATUSES:
        return "failed", "resource is missing"
    if 500 <= status < 600:
        return "review", "provider server error may be temporary"
    if 400 <= status < 500:
        return "review", "client, access-policy, or rate-limit response requires review"
    return "review", "unexpected HTTP status"


def _urls_from_json(value: Any) -> Iterable[str]:
    if isinstance(value, Mapping):
        for key, item in value.items():
            if key in {"url", "alternate_urls", "urls", "homepage"}:
                if isinstance(item, str) and is_external_url(item):
                    yield item
                elif isinstance(item, list):
                    for nested in item:
                        if isinstance(nested, str) and is_external_url(nested):
                            yield nested
                        else:
                            yield from _urls_from_json(nested)
            else:
                yield from _urls_from_json(item)
    elif isinstance(value, list):
        for item in value:
            yield from _urls_from_json(item)


def collect_external_urls(
    docs_root: Path,
    *,
    catalogue_path: Path | None = None,
    extra_markdown: Iterable[Path] = (),
    manifest_paths: Iterable[Path] = (),
) -> list[str]:
    urls: set[str] = set()
    for path in [*markdown_files(docs_root), *extra_markdown]:
        if not path.exists():
            continue
        for target, _ in iter_markdown_links(path.read_text(encoding="utf-8")):
            if is_external_url(target):
                urls.add(canonical_url(target))
    json_paths = [path for path in [catalogue_path, *manifest_paths] if path and path.exists()]
    for path in json_paths:
        try:
            value = load_json(path)
        except (OSError, QualityError):
            continue
        urls.update(canonical_url(url) for url in _urls_from_json(value))
    return sorted(urls)


class LinkChecker:
    def __init__(
        self,
        *,
        timeout: float = 8.0,
        retries: int = 1,
        respect_robots: bool = True,
        resolver: Resolver | None = None,
        resolve_dns: bool = True,
    ) -> None:
        try:
            import requests
        except ImportError as exc:
            raise QualityError("requests is required; install requirements-dev.txt") from exc
        self.requests = requests
        self.timeout = timeout
        self.retries = retries
        self.respect_robots = respect_robots
        self.resolver = resolver or _system_resolver
        # Disabling DNS resolution exists for deterministic unit tests only.
        # Production callers retain the secure default above.
        self.resolve_dns = resolve_dns
        self._robots: dict[str, tuple[RobotFileParser | None, str]] = {}
        self._robots_inflight: dict[str, threading.Event] = {}
        self._robots_lock = threading.Lock()
        self._target_policies: dict[tuple[str, int], tuple[str, str]] = {}
        self._target_inflight: dict[tuple[str, int], threading.Event] = {}
        self._target_lock = threading.Lock()
        self._request_local = threading.local()

    @staticmethod
    def _unsafe_result(
        url: str,
        *,
        checked_at: str,
        started: float,
        reason: str,
    ) -> dict[str, Any]:
        return {
            "url": url,
            "outcome": "failed",
            "http_status": None,
            "reason": reason,
            "final_url": url,
            "checked_at": checked_at,
            "elapsed_ms": round((time.monotonic() - started) * 1000),
            "from_cache": False,
        }

    @staticmethod
    def _review_result(
        url: str,
        *,
        checked_at: str,
        started: float,
        reason: str,
    ) -> dict[str, Any]:
        return {
            "url": url,
            "outcome": "review",
            "http_status": None,
            "reason": reason,
            "final_url": url,
            "checked_at": checked_at,
            "elapsed_ms": round((time.monotonic() - started) * 1000),
            "from_cache": False,
        }

    def _validate_target(self, url: str) -> str:
        try:
            parsed = urlsplit(url.strip())
            scheme = parsed.scheme.lower()
            hostname = parsed.hostname
            port = parsed.port or 443
            has_credentials = parsed.username is not None or parsed.password is not None
        except (TypeError, ValueError) as exc:
            raise UnsafeTargetError(f"malformed URL is not allowed: {exc}") from exc

        if scheme != "https":
            raise UnsafeTargetError("only HTTPS targets are allowed")
        if has_credentials:
            raise UnsafeTargetError("URLs containing credentials are not allowed")
        if not hostname:
            raise UnsafeTargetError("URL has no hostname")

        normalized_host = hostname.rstrip(".").lower()
        if normalized_host == "localhost" or normalized_host.endswith(".localhost"):
            raise UnsafeTargetError("localhost targets are not allowed")

        try:
            literal_address = ipaddress.ip_address(normalized_host)
        except ValueError:
            literal_address = None
        if literal_address is not None:
            if not _is_global_unicast(literal_address):
                raise UnsafeTargetError(
                    f"non-global IP target is not allowed: {literal_address}"
                )
            return canonical_url(url)

        if not self.resolve_dns:
            return canonical_url(url)

        self._validate_resolved_target(normalized_host, port)
        return canonical_url(url)

    @staticmethod
    def _apply_target_policy(policy: tuple[str, str]) -> None:
        outcome, reason = policy
        if outcome == "unsafe":
            raise UnsafeTargetError(reason)
        if outcome == "review":
            raise TargetResolutionError(reason)

    def _validate_resolved_target(self, hostname: str, port: int) -> None:
        key = (hostname, port)
        with self._target_lock:
            cached = self._target_policies.get(key)
            if cached is not None:
                self._apply_target_policy(cached)
                return
            inflight = self._target_inflight.get(key)
            if inflight is None:
                inflight = threading.Event()
                self._target_inflight[key] = inflight
                owns_resolution = True
            else:
                owns_resolution = False

        if not owns_resolution:
            inflight.wait()
            with self._target_lock:
                cached = self._target_policies.get(
                    key,
                    (
                        "review",
                        f"DNS validation did not complete for {hostname}",
                    ),
                )
            self._apply_target_policy(cached)
            return

        policy: tuple[str, str]
        try:
            resolved = tuple(self.resolver(hostname, port))
        except Exception as exc:
            policy = (
                "review",
                f"DNS resolution failed for {hostname}: "
                f"{type(exc).__name__}: {exc}",
            )
        else:
            policy = ("ok", "")
            if not resolved:
                policy = (
                    "review",
                    f"DNS resolution returned no addresses for {hostname}",
                )
            else:
                for value in resolved:
                    try:
                        address = ipaddress.ip_address(value)
                    except ValueError:
                        policy = (
                            "review",
                            "DNS resolution returned an invalid address for "
                            f"{hostname}: {value}",
                        )
                        break
                    if not _is_global_unicast(address):
                        policy = (
                            "unsafe",
                            f"DNS for {hostname} resolved to a non-global "
                            f"address: {address}",
                        )
                        break
        finally:
            with self._target_lock:
                self._target_policies[key] = policy
                event = self._target_inflight.pop(key)
                event.set()
        self._apply_target_policy(policy)

    def _request_with_safe_redirects(
        self,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> tuple[Any, str]:
        current_url = self._validate_target(url)
        request_client = getattr(self._request_local, "client", None)
        if request_client is None:
            session_factory = getattr(self.requests, "Session", None)
            request_client = session_factory() if session_factory else self.requests
            self._request_local.client = request_client
        request = request_client.head if method == "HEAD" else request_client.get
        for redirect_count in range(MAX_REDIRECTS + 1):
            response = request(
                current_url,
                allow_redirects=False,
                **kwargs,
            )
            if int(response.status_code) not in REDIRECT_STATUSES:
                return response, current_url

            location = response.headers.get("Location")
            if not location:
                return response, current_url
            try:
                redirect_url = urljoin(current_url, str(location))
                # Validate the destination before requests gets any opportunity
                # to contact it. This also resolves hostnames on every hop.
                next_url = self._validate_target(redirect_url)
            except Exception:
                response.close()
                raise
            response.close()
            if redirect_count >= MAX_REDIRECTS:
                raise RedirectError(
                    f"redirect limit exceeded ({MAX_REDIRECTS} redirects)"
                )
            current_url = next_url

        raise RedirectError(f"redirect limit exceeded ({MAX_REDIRECTS} redirects)")

    def _robots_policy(self, origin: str) -> tuple[RobotFileParser | None, str]:
        with self._robots_lock:
            cached = self._robots.get(origin)
            if cached is not None:
                return cached
            inflight = self._robots_inflight.get(origin)
            if inflight is None:
                inflight = threading.Event()
                self._robots_inflight[origin] = inflight
                owns_request = True
            else:
                owns_request = False

        if not owns_request:
            inflight.wait()
            with self._robots_lock:
                return self._robots.get(
                    origin, (None, "robots file unavailable after concurrent check")
                )

        robots_url = f"{origin}/robots.txt"
        result: tuple[RobotFileParser | None, str] = (
            None,
            "robots file unavailable",
        )
        try:
            response, _final_url = self._request_with_safe_redirects(
                "GET",
                robots_url,
                headers={"User-Agent": USER_AGENT},
                timeout=self.timeout,
            )
            if response.status_code == 200:
                parser = RobotFileParser()
                parser.set_url(robots_url)
                parser.parse(response.text.splitlines())
                result = (parser, "robots file loaded")
            response.close()
        except (
            self.requests.RequestException,
            UnsafeTargetError,
            TargetResolutionError,
            RedirectError,
        ):
            pass
        except Exception:
            result = (None, "robots file could not be parsed")
        finally:
            with self._robots_lock:
                self._robots[origin] = result
                event = self._robots_inflight.pop(origin)
                event.set()
        return result

    def _robots_allows(self, url: str) -> tuple[bool, str]:
        if not self.respect_robots:
            return True, "robots check disabled"
        parsed = urlsplit(url)
        origin = f"{parsed.scheme.lower()}://{parsed.netloc.lower()}"
        parser, reason = self._robots_policy(origin)
        if parser is None:
            return True, reason
        allowed = parser.can_fetch(USER_AGENT, url)
        return (
            allowed,
            "robots allowed" if allowed else "robots policy blocks automated checking",
        )

    def check(self, url: str) -> dict[str, Any]:
        checked_at = datetime.now(timezone.utc).isoformat()
        started = time.monotonic()
        try:
            self._validate_target(url)
        except UnsafeTargetError as exc:
            return self._unsafe_result(
                url,
                checked_at=checked_at,
                started=started,
                reason=str(exc),
            )
        except TargetResolutionError as exc:
            return self._review_result(
                url,
                checked_at=checked_at,
                started=started,
                reason=str(exc),
            )
        allowed, robots_reason = self._robots_allows(url)
        if not allowed:
            return self._review_result(
                url,
                checked_at=checked_at,
                started=started,
                reason=robots_reason,
            )
        last_error = ""
        for attempt in range(self.retries + 1):
            try:
                response, final_url = self._request_with_safe_redirects(
                    "HEAD",
                    url,
                    headers={"User-Agent": USER_AGENT},
                    timeout=self.timeout,
                )
                # A missing response to HEAD is not conclusive: some providers do
                # not implement HEAD correctly. Confirm permanent-missing statuses
                # with the same bounded GET fallback used for HEAD policy errors.
                if response.status_code in {
                    400,
                    403,
                    405,
                    *PERMANENT_MISSING_STATUSES,
                }:
                    response.close()
                    response, final_url = self._request_with_safe_redirects(
                        "GET",
                        url,
                        headers={
                            "User-Agent": USER_AGENT,
                            "Range": "bytes=0-2047",
                        },
                        timeout=self.timeout,
                        stream=True,
                    )
                status = int(response.status_code)
                response.close()
                outcome, reason = classify_http_status(status)
                return {
                    "url": url,
                    "outcome": outcome,
                    "http_status": status,
                    "reason": reason,
                    "final_url": final_url,
                    "checked_at": checked_at,
                    "elapsed_ms": round((time.monotonic() - started) * 1000),
                    "from_cache": False,
                }
            except UnsafeTargetError as exc:
                return self._unsafe_result(
                    url,
                    checked_at=checked_at,
                    started=started,
                    reason=str(exc),
                )
            except TargetResolutionError as exc:
                return self._review_result(
                    url,
                    checked_at=checked_at,
                    started=started,
                    reason=str(exc),
                )
            except (self.requests.RequestException, RedirectError) as exc:
                last_error = f"{type(exc).__name__}: {exc}"
                if attempt < self.retries:
                    time.sleep(min(2**attempt, 4))
        return self._review_result(
            url,
            checked_at=checked_at,
            started=started,
            reason=last_error or "network request failed",
        )


def _load_cache(path: Path, ttl: timedelta) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    try:
        payload = load_json(path)
    except (OSError, QualityError):
        return {}
    if not isinstance(payload, Mapping) or payload.get("version") != CACHE_VERSION:
        return {}
    cached_results = payload.get("results", {})
    if not isinstance(cached_results, Mapping):
        return {}
    now = datetime.now(timezone.utc)
    output: dict[str, dict[str, Any]] = {}
    for url, result in cached_results.items():
        if not isinstance(result, Mapping):
            continue
        try:
            checked = datetime.fromisoformat(str(result["checked_at"]))
            if checked.tzinfo is None:
                checked = checked.replace(tzinfo=timezone.utc)
        except (KeyError, ValueError):
            continue
        if now - checked <= ttl:
            cached = dict(result)
            cached["from_cache"] = True
            output[str(url)] = cached
    return output


def _write_cache(path: Path, results: Mapping[str, Mapping[str, Any]]) -> None:
    cache_payload = {
        "version": CACHE_VERSION,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "results": {url: dict(results[url]) for url in sorted(results)},
    }
    atomic_write(path, stable_json(cache_payload))


def _checker_exception_result(url: str, exc: Exception) -> dict[str, Any]:
    return {
        "url": url,
        "outcome": "review",
        "http_status": None,
        "reason": f"checker task raised {type(exc).__name__}: {exc}",
        "final_url": url,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "elapsed_ms": 0,
        "from_cache": False,
    }


def check_urls(
    urls: Iterable[str],
    *,
    cache_path: Path,
    cache_ttl_hours: float = 168,
    workers: int = 24,
    timeout: float = 8,
    retries: int = 1,
    offline: bool = False,
    respect_robots: bool = True,
    checkpoint_batch_size: int = 25,
    checkpoint_interval_seconds: float = 5,
) -> list[dict[str, Any]]:
    unique = sorted(set(urls))
    cached = _load_cache(cache_path, timedelta(hours=cache_ttl_hours))
    results: dict[str, dict[str, Any]] = {
        url: cached[url] for url in unique if url in cached
    }
    cache_results: dict[str, dict[str, Any]] = dict(cached)
    dirty_results = 0
    last_checkpoint = time.monotonic()

    def checkpoint(*, force: bool = False) -> None:
        nonlocal dirty_results, last_checkpoint
        batch_ready = dirty_results >= max(1, checkpoint_batch_size)
        interval_ready = (
            dirty_results > 0
            and time.monotonic() - last_checkpoint
            >= max(0, checkpoint_interval_seconds)
        )
        if not force and not batch_ready and not interval_ready:
            return
        _write_cache(cache_path, cache_results)
        dirty_results = 0
        last_checkpoint = time.monotonic()

    def record(
        url: str, result: Mapping[str, Any], *, cacheable: bool = True
    ) -> None:
        nonlocal dirty_results
        normalized = dict(result)
        normalized["url"] = url
        results[url] = normalized
        if cacheable:
            cache_results[url] = normalized
            dirty_results += 1
            checkpoint()

    def completed_result(future: Any, url: str) -> tuple[dict[str, Any], bool]:
        try:
            result = future.result()
            if not isinstance(result, Mapping):
                raise TypeError("checker task did not return a mapping")
            return dict(result), True
        except Exception as exc:
            return _checker_exception_result(url, exc), False

    pending = [url for url in unique if url not in results]
    if offline:
        now = datetime.now(timezone.utc).isoformat()
        for url in pending:
            record(
                url,
                {
                    "url": url,
                    "outcome": "review",
                    "http_status": None,
                    "reason": "not present in a fresh cache; network check required",
                    "final_url": url,
                    "checked_at": now,
                    "elapsed_ms": 0,
                    "from_cache": False,
                },
                cacheable=False,
            )
    elif pending:
        checker = LinkChecker(
            timeout=timeout, retries=retries, respect_robots=respect_robots
        )
        executor = ThreadPoolExecutor(max_workers=max(1, workers))
        futures = {executor.submit(checker.check, url): url for url in pending}
        try:
            for future in as_completed(futures):
                url = futures[future]
                result, cacheable = completed_result(future, url)
                record(url, result, cacheable=cacheable)
        except BaseException:
            # Capture work that finished before an interrupt but was not yet yielded
            # by as_completed, then persist it before propagating the interrupt.
            for future, url in futures.items():
                if url in results or not future.done() or future.cancelled():
                    continue
                exception = future.exception()
                if exception is None:
                    result, cacheable = completed_result(future, url)
                    record(url, result, cacheable=cacheable)
                elif isinstance(exception, Exception):
                    record(
                        url,
                        _checker_exception_result(url, exception),
                        cacheable=False,
                    )
            checkpoint(force=True)
            for future in futures:
                future.cancel()
            executor.shutdown(wait=False, cancel_futures=True)
            raise
        else:
            executor.shutdown(wait=True)
    checkpoint(force=True)
    return [results[url] for url in unique]


def result_issues(
    results: Iterable[Mapping[str, Any]],
    *,
    allow_review: bool = False,
) -> list[Issue]:
    issues: list[Issue] = []
    for result in results:
        outcome = result.get("outcome")
        if outcome == "failed":
            issues.append(
                Issue(
                    "error",
                    "external.failed",
                    f"{result.get('reason')} (HTTP {result.get('http_status')})",
                    str(result.get("url", "")),
                )
            )
        elif outcome == "review":
            issues.append(
                Issue(
                    "warning" if allow_review else "error",
                    "external.review",
                    f"not counted as healthy: {result.get('reason')} "
                    f"(HTTP {result.get('http_status')})",
                    str(result.get("url", "")),
                )
            )
    return issues


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check external resources with cache, robots handling, and explicit review states."
    )
    parser.add_argument("--docs-root", default="docs")
    parser.add_argument("--catalogue", default="data/courses.json")
    parser.add_argument("--manifest", action="append", default=[])
    parser.add_argument("--cache", default=".cache/external-links.json")
    parser.add_argument("--output", default="build/external-links.json")
    parser.add_argument("--cache-ttl-hours", type=float, default=168)
    parser.add_argument("--workers", type=int, default=24)
    parser.add_argument("--timeout", type=float, default=8)
    parser.add_argument("--retries", type=int, default=1)
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--ignore-robots", action="store_true")
    parser.add_argument(
        "--allow-review",
        action="store_true",
        help="Keep manual-review results visible but do not fail only because of them.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root_markdown = sorted(repo_path(".").glob("*.md"))
    manifest_paths = [repo_path(path) for path in args.manifest]
    default_manifest = repo_path("data/external_resources.json")
    if default_manifest.exists() and default_manifest not in manifest_paths:
        manifest_paths.append(default_manifest)
    urls = collect_external_urls(
        repo_path(args.docs_root),
        catalogue_path=repo_path(args.catalogue),
        extra_markdown=root_markdown,
        manifest_paths=manifest_paths,
    )
    try:
        results = check_urls(
            urls,
            cache_path=repo_path(args.cache),
            cache_ttl_hours=args.cache_ttl_hours,
            workers=args.workers,
            timeout=args.timeout,
            retries=args.retries,
            offline=args.offline,
            respect_robots=not args.ignore_robots,
        )
    except QualityError as exc:
        issues = [Issue("error", "external.dependency", str(exc))]
        emit_issues(issues)
        return 1
    issues = result_issues(results, allow_review=args.allow_review)
    counts = {
        outcome: sum(result["outcome"] == outcome for result in results)
        for outcome in ("ok", "review", "failed")
    }
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total": len(results),
            **counts,
            "healthy_percent": round(counts["ok"] * 100 / len(results), 2)
            if results
            else 100.0,
        },
        "results": results,
        "issues": [issue.to_dict() for issue in issues],
    }
    atomic_write(repo_path(args.output), stable_json(payload))
    emit_issues(issues)
    print(
        f"External links: {len(results)} total, {counts['ok']} healthy, "
        f"{counts['review']} manual review, {counts['failed']} failed"
    )
    return exit_code(issues)


if __name__ == "__main__":
    raise SystemExit(main())
