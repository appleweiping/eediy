from __future__ import annotations

from pathlib import Path

from scripts.check_dependency_lock import dependency_lock_issues


def test_dependency_lock_accepts_matching_hashed_pin(tmp_path: Path) -> None:
    direct = tmp_path / "requirements.txt"
    lock = tmp_path / "requirements.lock"
    direct.write_text("Example_Package==1.2.3\n", encoding="utf-8")
    lock.write_text(
        "example-package==1.2.3 \\\n"
        "    --hash=sha256:abc123\n",
        encoding="utf-8",
    )

    assert dependency_lock_issues([direct], lock) == []


def test_dependency_lock_detects_direct_version_drift(tmp_path: Path) -> None:
    direct = tmp_path / "requirements.txt"
    lock = tmp_path / "requirements.lock"
    direct.write_text("example-package==2.0.0\n", encoding="utf-8")
    lock.write_text(
        "example-package==1.2.3 \\\n"
        "    --hash=sha256:abc123\n",
        encoding="utf-8",
    )

    issues = dependency_lock_issues([direct], lock)

    assert any(issue.code == "dependency.lock_drift" for issue in issues)


def test_dependency_lock_requires_exact_direct_pin_and_hash(tmp_path: Path) -> None:
    direct = tmp_path / "requirements.txt"
    lock = tmp_path / "requirements.lock"
    direct.write_text("example-package>=1\n", encoding="utf-8")
    lock.write_text("example-package==1.2.3\n", encoding="utf-8")

    issues = dependency_lock_issues([direct], lock)

    assert any(issue.code == "dependency.direct_not_exact" for issue in issues)
    assert any(issue.code == "dependency.lock_hash_missing" for issue in issues)
