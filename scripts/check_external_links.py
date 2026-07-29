from __future__ import annotations

import argparse
import ipaddress
import json
import math
import re
import socket
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime, timedelta, timezone
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
DEFAULT_REVIEW_LEDGER = "data/external_link_reviews.json"
REVIEW_DECISIONS = frozenset({"retain", "replace", "remove"})
DEFAULT_REVIEW_MAX_AGE_DAYS = 14
ROBOTS_DENIED_REASON = "robots policy blocks automated checking"
EVIDENCE_REVIEW_REASON_CODES = frozenset({"http_403", "robots_denied"})
MANUAL_REVIEW_REASON_CODES = frozenset(
    {*EVIDENCE_REVIEW_REASON_CODES, "tls_error"}
)
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


class ReviewLedger(dict[str, dict[str, Any]]):
    """Validated target adjudications plus their independently checked evidence."""

    reviewer: str
    reviewed_at: str
    evidence_urls: tuple[str, ...]
    evidence_groups: dict[str, str]

    def __init__(
        self,
        reviews: Mapping[str, Mapping[str, Any]] | None = None,
        *,
        reviewer: str = "",
        reviewed_at: str = "",
        evidence_groups: Mapping[str, str] = (),
    ) -> None:
        source = reviews or {}
        super().__init__((url, dict(value)) for url, value in source.items())
        self.reviewer = reviewer
        self.reviewed_at = reviewed_at
        self.evidence_groups = dict(evidence_groups)
        self.evidence_urls = tuple(sorted(self.evidence_groups))


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
    scheme = parsed.scheme.lower()
    hostname = parsed.hostname
    netloc = parsed.netloc.lower()
    if hostname:
        normalized_host = hostname.rstrip(".").encode("idna").decode("ascii").lower()
        host = f"[{normalized_host}]" if ":" in normalized_host else normalized_host
        port = parsed.port
        if port is not None and not (scheme == "https" and port == 443):
            host = f"{host}:{port}"
        userinfo = ""
        if parsed.username is not None:
            userinfo = parsed.username
            if parsed.password is not None:
                userinfo += f":{parsed.password}"
            userinfo += "@"
        netloc = f"{userinfo}{host}"
    return urlunsplit(
        (
            scheme,
            netloc,
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


def http_reason_code(status: int) -> str:
    if 200 <= status < 300:
        return "http_ok"
    if 300 <= status < 400:
        return "http_redirect"
    if status in PERMANENT_MISSING_STATUSES:
        return "http_missing"
    if status == 403:
        return "http_403"
    if 400 <= status < 500:
        return "http_client_error"
    if 500 <= status < 600:
        return "http_server_error"
    return "http_unexpected"


def infer_reason_code(result: Mapping[str, Any]) -> str:
    """Infer a structured code for legacy cache entries and test fixtures."""

    status = result.get("http_status")
    if isinstance(status, int) and not isinstance(status, bool):
        return http_reason_code(status)
    reason = str(result.get("reason", ""))
    if reason == ROBOTS_DENIED_REASON:
        return "robots_denied"
    if reason.startswith("SSLError:"):
        return "tls_error"
    if reason.startswith("DNS resolution failed"):
        return "dns_resolution"
    if reason.startswith("checker task raised"):
        return "checker_exception"
    if reason == "not present in a fresh cache; network check required":
        return "offline_cache_miss"
    if result.get("outcome") == "failed":
        return "unsafe_target"
    return "network_error"


def reason_code_matches_result(result: Mapping[str, Any]) -> bool:
    """Reject a claimed policy code when the underlying result contradicts it."""

    code = result.get("reason_code")
    if not isinstance(code, str) or not code:
        return False
    if code.startswith("http_"):
        status = result.get("http_status")
        if not isinstance(status, int) or isinstance(status, bool):
            return False
        expected_outcome, _reason = classify_http_status(status)
        return (
            result.get("outcome") == expected_outcome
            and code == http_reason_code(status)
        )
    reason = str(result.get("reason", ""))
    if code == "robots_denied":
        return (
            result.get("outcome") == "review"
            and result.get("http_status") is None
            and reason == ROBOTS_DENIED_REASON
        )
    if code == "tls_error":
        return (
            result.get("outcome") == "review"
            and result.get("http_status") is None
            and reason.startswith("SSLError:")
        )
    if code == "dns_resolution":
        return (
            result.get("outcome") == "review"
            and result.get("http_status") is None
            and reason.startswith("DNS resolution failed")
        )
    if code == "checker_exception":
        return (
            result.get("outcome") == "review"
            and result.get("http_status") is None
            and reason.startswith("checker task raised")
        )
    if code == "offline_cache_miss":
        return (
            result.get("outcome") == "review"
            and result.get("http_status") is None
            and reason == "not present in a fresh cache; network check required"
        )
    if code == "unsafe_target":
        return result.get("outcome") == "failed" and result.get("http_status") is None
    if code == "missing_result":
        return (
            result.get("outcome") == "failed"
            and result.get("http_status") is None
            and reason == "link checker returned no result for requested URL"
        )
    if code == "invalid_result":
        return (
            result.get("outcome") == "failed"
            and result.get("http_status") is None
            and reason.startswith("inconsistent checker result")
        )
    if code == "redirect_error":
        return result.get("outcome") == "review" and result.get("http_status") is None
    if code == "network_error":
        return result.get("outcome") == "review" and result.get("http_status") is None
    return False


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


def _canonical_https_url(raw_url: Any, *, field: str) -> str:
    """Validate a public HTTPS URL structurally and return its canonical form."""

    if not isinstance(raw_url, str) or not raw_url or raw_url != raw_url.strip():
        raise QualityError(f"{field} must be a non-empty URL without outer whitespace")
    if any(character.isspace() or ord(character) < 32 for character in raw_url):
        raise QualityError(f"{field} contains whitespace or control characters")
    if "\\" in raw_url:
        raise QualityError(f"{field} contains an invalid backslash")
    if re.search(r"%(?![0-9A-Fa-f]{2})", raw_url):
        raise QualityError(f"{field} contains an invalid percent escape")

    try:
        parsed = urlsplit(raw_url)
        hostname = parsed.hostname
        # Accessing port is deliberately part of validation because urlsplit()
        # otherwise defers malformed-port errors.
        _port = parsed.port
    except (TypeError, ValueError) as exc:
        raise QualityError(f"{field} is malformed: {exc}") from exc
    if parsed.scheme.lower() != "https":
        raise QualityError(f"{field} must use HTTPS")
    if not hostname:
        raise QualityError(f"{field} must include a hostname")
    if parsed.username is not None or parsed.password is not None:
        raise QualityError(f"{field} must not include credentials")

    normalized_host = hostname.rstrip(".").lower()
    if not normalized_host:
        raise QualityError(f"{field} must include a hostname")
    try:
        address = ipaddress.ip_address(normalized_host)
    except ValueError:
        try:
            ascii_host = normalized_host.encode("idna").decode("ascii")
        except UnicodeError as exc:
            raise QualityError(f"{field} contains an invalid hostname") from exc
        labels = ascii_host.split(".")
        hostname_pattern = re.compile(
            r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?$"
        )
        if (
            len(ascii_host) > 253
            or any(not label or not hostname_pattern.fullmatch(label) for label in labels)
        ):
            raise QualityError(f"{field} contains an invalid hostname")
    else:
        if not _is_global_unicast(address):
            raise QualityError(f"{field} must point to a public Internet host")

    return canonical_url(raw_url)


def _required_text(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise QualityError(f"{field} must be a non-empty string")
    return value.strip()


def load_review_ledger(
    path: Path,
    *,
    max_age_days: float = DEFAULT_REVIEW_MAX_AGE_DAYS,
    today: date | None = None,
) -> ReviewLedger:
    """Load and fully validate grouped manual-review adjudications."""

    if not math.isfinite(max_age_days) or max_age_days < 0:
        raise QualityError(
            "external-link review max age must be a finite non-negative number"
        )
    if not path.exists():
        return ReviewLedger()
    try:
        payload = load_json(path)
    except (OSError, QualityError) as exc:
        raise QualityError(f"could not load external-link review ledger: {exc}") from exc
    if not isinstance(payload, Mapping):
        raise QualityError("external-link review ledger must be a JSON object")

    reviewer = _required_text(
        payload.get("reviewer"),
        field="external-link review ledger reviewer",
    )
    raw_reviewed_at = payload.get("reviewed_at")
    if not isinstance(raw_reviewed_at, str) or not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}", raw_reviewed_at
    ):
        raise QualityError(
            "external-link review ledger reviewed_at must be an ISO date "
            "in YYYY-MM-DD form"
        )
    try:
        reviewed_date = date.fromisoformat(raw_reviewed_at)
    except ValueError as exc:
        raise QualityError(
            "external-link review ledger reviewed_at must be a valid ISO date"
        ) from exc
    # Review dates are calendar dates entered by maintainers, so compare them
    # with the host's local release date rather than UTC (which can be the
    # preceding day in Asian release environments).
    current_date = today or datetime.now().astimezone().date()
    if reviewed_date > current_date:
        raise QualityError(
            "external-link review ledger reviewed_at cannot be in the future"
        )
    review_age = (current_date - reviewed_date).days
    if review_age > max_age_days:
        raise QualityError(
            "external-link review ledger is stale: "
            f"{review_age} days old (maximum {max_age_days:g})"
        )

    groups = payload.get("groups")
    if not isinstance(groups, list):
        raise QualityError("external-link review ledger must contain a groups list")

    reviews: dict[str, dict[str, Any]] = {}
    evidence_groups: dict[str, str] = {}
    group_names: set[str] = set()
    decision_counts = {decision: 0 for decision in REVIEW_DECISIONS}
    for index, group in enumerate(groups, start=1):
        if not isinstance(group, Mapping):
            raise QualityError(f"external-link review group {index} must be an object")
        name = _required_text(
            group.get("name"),
            field=f"external-link review group {index} name",
        )
        if name in group_names:
            raise QualityError(
                f"external-link review ledger records group name more than once: {name!r}"
            )
        group_names.add(name)
        decision = group.get("decision")
        if not isinstance(decision, str) or decision not in REVIEW_DECISIONS:
            allowed = ", ".join(sorted(REVIEW_DECISIONS))
            raise QualityError(
                f"external-link review group {name!r} has invalid decision "
                f"{decision!r}; expected one of: {allowed}"
            )
        automation_reason = _required_text(
            group.get("automation_reason"),
            field=f"external-link review group {name!r} automation_reason",
        )
        method = _required_text(
            group.get("method"),
            field=f"external-link review group {name!r} method",
        )
        raw_reason_codes = group.get("allowed_reason_codes")
        if (
            not isinstance(raw_reason_codes, list)
            or not raw_reason_codes
            or any(
                not isinstance(reason_code, str) or not reason_code
                for reason_code in raw_reason_codes
            )
            or len(set(raw_reason_codes)) != len(raw_reason_codes)
        ):
            raise QualityError(
                f"external-link review group {name!r} needs a non-empty, "
                "unique allowed_reason_codes list"
            )
        unsupported_reason_codes = set(raw_reason_codes) - MANUAL_REVIEW_REASON_CODES
        if unsupported_reason_codes:
            unsupported = ", ".join(sorted(unsupported_reason_codes))
            raise QualityError(
                f"external-link review group {name!r} uses unsupported manual-review "
                f"reason code(s): {unsupported}"
            )
        allowed_reason_codes = sorted(raw_reason_codes)
        urls = group.get("urls")
        if not isinstance(urls, list) or not urls:
            raise QualityError(
                f"external-link review group {name!r} needs a non-empty urls list"
            )

        raw_evidence = group.get("evidence")
        if not isinstance(raw_evidence, list) or not raw_evidence:
            raise QualityError(
                f"external-link review group {name!r} needs at least one "
                "HTTPS evidence URL"
            )
        evidence: list[str] = []
        for evidence_index, raw_url in enumerate(raw_evidence, start=1):
            evidence_url = _canonical_https_url(
                raw_url,
                field=(
                    f"external-link review group {name!r} evidence "
                    f"URL {evidence_index}"
                ),
            )
            if evidence_url in evidence_groups:
                raise QualityError(
                    "external-link review ledger records evidence URL more than once: "
                    f"{evidence_url} (groups {evidence_groups[evidence_url]!r} "
                    f"and {name!r})"
                )
            evidence_groups[evidence_url] = name
            evidence.append(evidence_url)

        adjudication: dict[str, Any] = {
            "recorded": True,
            "decision": decision,
            "approved": decision == "retain",
            "group": name,
            "reviewed_at": raw_reviewed_at,
            "reviewer": reviewer,
            "automation_reason": automation_reason,
            "method": method,
            "allowed_reason_codes": allowed_reason_codes,
            "evidence": evidence,
        }

        for target_index, raw_url in enumerate(urls, start=1):
            try:
                url = _canonical_https_url(
                    raw_url,
                    field=(
                        f"external-link review group {name!r} target "
                        f"URL {target_index}"
                    ),
                )
            except QualityError as exc:
                raise QualityError(
                    f"external-link review group {name!r} contains an invalid URL: "
                    f"{raw_url!r} ({exc})"
                ) from exc
            if url in reviews:
                raise QualityError(
                    f"external-link review ledger records URL more than once: {url}"
                )
            reviews[url] = dict(adjudication)
            decision_counts[decision] += 1

    summary = payload.get("summary")
    if summary is not None:
        if not isinstance(summary, Mapping):
            raise QualityError(
                "external-link review ledger summary must be a JSON object"
            )
        actual_summary = {
            "reviewed": len(reviews),
            **decision_counts,
        }
        for key, actual in actual_summary.items():
            value = summary.get(key)
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                raise QualityError(
                    "external-link review ledger summary "
                    f"{key} must be a non-negative integer"
                )
            if value != actual:
                raise QualityError(
                    "external-link review ledger summary is inconsistent: "
                    f"{key}={value}, expected {actual}"
                )

    return ReviewLedger(
        reviews,
        reviewer=reviewer,
        reviewed_at=raw_reviewed_at,
        evidence_groups=evidence_groups,
    )


def annotate_review_decisions(
    results: Iterable[Mapping[str, Any]],
    reviews: Mapping[str, Mapping[str, Any]],
    *,
    target_urls: Iterable[str] | None = None,
    evidence_urls: Iterable[str] | None = None,
) -> list[dict[str, Any]]:
    """Attach adjudications and distinguish content targets from evidence URLs."""

    source_results = [dict(result) for result in results]
    target_set = (
        {canonical_url(url) for url in target_urls}
        if target_urls is not None
        else {
            canonical_url(str(result["url"]))
            for result in source_results
            if isinstance(result.get("url"), str)
            and is_external_url(str(result["url"]))
        }
    )
    if evidence_urls is None and isinstance(reviews, ReviewLedger):
        evidence_urls = reviews.evidence_urls
    evidence_set = (
        {canonical_url(url) for url in evidence_urls}
        if evidence_urls is not None
        else set()
    )
    annotated: list[dict[str, Any]] = []
    for item in source_results:
        raw_url = item.get("url")
        adjudication: Mapping[str, Any] | None = None
        canonical = ""
        if isinstance(raw_url, str) and is_external_url(raw_url):
            canonical = canonical_url(raw_url)
            adjudication = reviews.get(canonical)
        roles: list[str] = []
        if canonical in target_set:
            roles.append("target")
        if canonical in evidence_set:
            roles.append("evidence")
        item["link_roles"] = roles
        if "target" in roles and adjudication is not None:
            review_record = dict(adjudication)
            if isinstance(review_record.get("evidence"), list):
                review_record["evidence"] = list(review_record["evidence"])
            item["review_adjudication"] = review_record
        elif "target" in roles and item.get("outcome") == "review":
            item["review_adjudication"] = {
                "recorded": False,
                "decision": None,
                "approved": False,
            }
        if "evidence" in roles:
            group = (
                reviews.evidence_groups.get(canonical)
                if isinstance(reviews, ReviewLedger)
                else None
            )
            evidence_record: dict[str, Any] = {
                "recorded": True,
                "manually_verified": True,
            }
            if group:
                evidence_record["group"] = group
            if isinstance(reviews, ReviewLedger):
                evidence_record["reviewer"] = reviews.reviewer
                evidence_record["reviewed_at"] = reviews.reviewed_at
            item["evidence_attestation"] = evidence_record
        annotated.append(item)
    return annotated


def _result_has_role(result: Mapping[str, Any], role: str) -> bool:
    roles = result.get("link_roles")
    if isinstance(roles, list):
        return role in roles
    # Reports created before role labelling contain content targets only.
    return role == "target"


def review_approval_counts(
    results: Iterable[Mapping[str, Any]],
) -> tuple[int, int]:
    approved = 0
    unapproved = 0
    for result in results:
        if result.get("outcome") != "review" or not _result_has_role(
            result, "target"
        ):
            continue
        adjudication = result.get("review_adjudication")
        decision = (
            adjudication.get("decision")
            if isinstance(adjudication, Mapping)
            else None
        )
        allowed_reason_codes = (
            adjudication.get("allowed_reason_codes")
            if isinstance(adjudication, Mapping)
            else None
        )
        reason_code = (
            str(result["reason_code"])
            if isinstance(result.get("reason_code"), str)
            else infer_reason_code(result)
        )
        if (
            decision == "retain"
            and isinstance(allowed_reason_codes, list)
            and reason_code in allowed_reason_codes
            and reason_code_matches_result(
                {**dict(result), "reason_code": reason_code}
            )
        ):
            approved += 1
        else:
            unapproved += 1
    return approved, unapproved


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
            "reason_code": "unsafe_target",
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
        reason_code: str,
    ) -> dict[str, Any]:
        return {
            "url": url,
            "outcome": "review",
            "reason_code": reason_code,
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
                reason_code="dns_resolution",
            )
        allowed, robots_reason = self._robots_allows(url)
        if not allowed:
            return self._review_result(
                url,
                checked_at=checked_at,
                started=started,
                reason=robots_reason,
                reason_code="robots_denied",
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
                    "reason_code": http_reason_code(status),
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
                    reason_code="dns_resolution",
                )
            except (self.requests.RequestException, RedirectError) as exc:
                last_error = f"{type(exc).__name__}: {exc}"
                last_error_code = (
                    "tls_error"
                    if type(exc).__name__ == "SSLError"
                    else "redirect_error"
                    if isinstance(exc, RedirectError)
                    else "network_error"
                )
                if attempt < self.retries:
                    time.sleep(min(2**attempt, 4))
        return self._review_result(
            url,
            checked_at=checked_at,
            started=started,
            reason=last_error or "network request failed",
            reason_code=last_error_code if last_error else "network_error",
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
            if not isinstance(cached.get("reason_code"), str):
                cached["reason_code"] = infer_reason_code(cached)
            if not reason_code_matches_result(cached):
                continue
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
        "reason_code": "checker_exception",
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
        if not isinstance(normalized.get("reason_code"), str):
            normalized["reason_code"] = infer_reason_code(normalized)
        if not reason_code_matches_result(normalized):
            normalized = {
                "url": url,
                "outcome": "failed",
                "reason_code": "invalid_result",
                "http_status": None,
                "reason": "inconsistent checker result was rejected",
                "final_url": url,
                "checked_at": datetime.now(timezone.utc).isoformat(),
                "elapsed_ms": 0,
                "from_cache": False,
            }
            cacheable = False
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
                    "reason_code": "offline_cache_miss",
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
        is_target = _result_has_role(result, "target")
        is_evidence = _result_has_role(result, "evidence")
        reason_code = (
            str(result["reason_code"])
            if isinstance(result.get("reason_code"), str)
            else infer_reason_code(result)
        )
        reason_code_valid = reason_code_matches_result(
            {**dict(result), "reason_code": reason_code}
        )
        if not reason_code_valid:
            issues.append(
                Issue(
                    "error",
                    "external.result_inconsistent",
                    "outcome, HTTP status, reason, and structured reason code "
                    "do not describe the same checker result",
                    str(result.get("url", "")),
                )
            )
            continue
        if outcome == "failed":
            evidence_only = is_evidence and not is_target
            issues.append(
                Issue(
                    "error",
                    "external.evidence_failed" if evidence_only else "external.failed",
                    (
                        "manual-review evidence is unavailable: "
                        if evidence_only
                        else ""
                    )
                    + f"{result.get('reason')} (HTTP {result.get('http_status')})",
                    str(result.get("url", "")),
                )
            )
        elif outcome == "review":
            classified = False
            if is_target:
                classified = True
                adjudication = result.get("review_adjudication")
                decision = (
                    adjudication.get("decision")
                    if isinstance(adjudication, Mapping)
                    else None
                )
                allowed_reason_codes = (
                    adjudication.get("allowed_reason_codes")
                    if isinstance(adjudication, Mapping)
                    else None
                )
                approved = (
                    decision == "retain"
                    and isinstance(allowed_reason_codes, list)
                    and reason_code in allowed_reason_codes
                    and reason_code_valid
                )
                decision_label = (
                    str(decision) if decision is not None else "unrecorded"
                )
                issues.append(
                    Issue(
                        "warning" if allow_review and approved else "error",
                        "external.review",
                        f"not counted as healthy; manual decision={decision_label}, "
                        f"reason_code={reason_code}: "
                        f"{result.get('reason')} "
                        f"(HTTP {result.get('http_status')})",
                        str(result.get("url", "")),
                    )
                )
            if is_evidence:
                classified = True
                attestation = result.get("evidence_attestation")
                manually_verified = (
                    isinstance(attestation, Mapping)
                    and attestation.get("recorded") is True
                    and attestation.get("manually_verified") is True
                )
                can_warn = (
                    allow_review
                    and manually_verified
                    and reason_code_valid
                    and reason_code in EVIDENCE_REVIEW_REASON_CODES
                )
                issues.append(
                    Issue(
                        "warning" if can_warn else "error",
                        "external.evidence_review",
                        "manually verified evidence URL; this does not count as "
                        f"a target retain decision; reason_code={reason_code}: "
                        f"{result.get('reason')} "
                        f"(HTTP {result.get('http_status')})",
                        str(result.get("url", "")),
                    )
                )
            if not classified:
                issues.append(
                    Issue(
                        "error",
                        "external.review",
                        f"unclassified manual-review result: {result.get('reason')} "
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
    parser.add_argument("--review-ledger", default=DEFAULT_REVIEW_LEDGER)
    parser.add_argument(
        "--review-max-age-days",
        type=float,
        default=DEFAULT_REVIEW_MAX_AGE_DAYS,
        help="Maximum age of the manual-review ledger (default: 14 days).",
    )
    parser.add_argument("--cache-ttl-hours", type=float, default=168)
    parser.add_argument("--workers", type=int, default=24)
    parser.add_argument("--timeout", type=float, default=8)
    parser.add_argument("--retries", type=int, default=1)
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--ignore-robots", action="store_true")
    parser.add_argument(
        "--allow-review",
        action="store_true",
        help=(
            "Downgrade ledger-approved retain decisions to warnings; "
            "unapproved manual-review results still fail."
        ),
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        review_ledger = load_review_ledger(
            repo_path(args.review_ledger),
            max_age_days=args.review_max_age_days,
        )
    except QualityError as exc:
        issues = [Issue("error", "external.review_ledger", str(exc))]
        emit_issues(issues)
        return 1
    root_markdown = sorted(repo_path(".").glob("*.md"))
    manifest_paths = [repo_path(path) for path in args.manifest]
    default_manifest = repo_path("data/external_resources.json")
    if default_manifest.exists() and default_manifest not in manifest_paths:
        manifest_paths.append(default_manifest)
    target_urls = collect_external_urls(
        repo_path(args.docs_root),
        catalogue_path=repo_path(args.catalogue),
        extra_markdown=root_markdown,
        manifest_paths=manifest_paths,
    )
    urls = sorted({*target_urls, *review_ledger.evidence_urls})
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
    returned_urls = {
        canonical_url(str(result["url"]))
        for result in results
        if isinstance(result, Mapping)
        and isinstance(result.get("url"), str)
        and is_external_url(str(result["url"]))
    }
    for missing_url in sorted(set(urls) - returned_urls):
        results.append(
            {
                "url": missing_url,
                "outcome": "failed",
                "reason_code": "missing_result",
                "http_status": None,
                "reason": "link checker returned no result for requested URL",
                "final_url": missing_url,
                "checked_at": datetime.now(timezone.utc).isoformat(),
                "elapsed_ms": 0,
                "from_cache": False,
            }
        )
    results = annotate_review_decisions(
        results,
        review_ledger,
        target_urls=target_urls,
        evidence_urls=review_ledger.evidence_urls,
    )
    issues = result_issues(results, allow_review=args.allow_review)
    counts = {
        outcome: sum(result["outcome"] == outcome for result in results)
        for outcome in ("ok", "review", "failed")
    }
    target_results = [
        result for result in results if _result_has_role(result, "target")
    ]
    evidence_results = [
        result for result in results if _result_has_role(result, "evidence")
    ]
    target_counts = {
        outcome: sum(result["outcome"] == outcome for result in target_results)
        for outcome in ("ok", "review", "failed")
    }
    evidence_counts = {
        outcome: sum(result["outcome"] == outcome for result in evidence_results)
        for outcome in ("ok", "review", "failed")
    }
    review_approved, review_unapproved = review_approval_counts(results)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total": len(results),
            **counts,
            "target_total": len(target_results),
            **{
                f"target_{outcome}": count
                for outcome, count in target_counts.items()
            },
            "evidence_total": len(evidence_results),
            **{
                f"evidence_{outcome}": count
                for outcome, count in evidence_counts.items()
            },
            "evidence_only": sum(
                _result_has_role(result, "evidence")
                and not _result_has_role(result, "target")
                for result in results
            ),
            "review_approved": review_approved,
            "review_unapproved": review_unapproved,
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
        f"External links: {len(results)} unique checked, {counts['ok']} healthy, "
        f"{counts['review']} review, {counts['failed']} failed; "
        f"targets: {len(target_results)} total, {target_counts['review']} review "
        f"({review_approved} approved, {review_unapproved} unapproved), "
        f"{target_counts['failed']} failed; evidence: {len(evidence_results)} total, "
        f"{evidence_counts['review']} review, {evidence_counts['failed']} failed"
    )
    return exit_code(issues)


if __name__ == "__main__":
    raise SystemExit(main())
