"""Version update checks driven by a configurable remote manifest."""

from __future__ import annotations

import json
import re
import urllib.request
from dataclasses import dataclass
from typing import Callable


_VERSION_RE = re.compile(r"^[vV]?(\d+(?:\.\d+)*)$")


@dataclass(frozen=True)
class UpdateManifest:
    version: str
    download_url: str = ""
    announcement_url: str = ""
    release_manifest_url: str = ""
    release_index_url: str = ""
    release_notes: str = ""
    preferences_override: dict | None = None


@dataclass(frozen=True)
class ReleaseHistoryEntry:
    version: str
    title: str = ""
    date: str = ""
    release_notes: str = ""
    download_url: str = ""
    announcement_url: str = ""


@dataclass(frozen=True)
class UpdateCheckResult:
    checked: bool
    update_available: bool
    latest_version: str = ""
    download_url: str = ""
    announcement_url: str = ""
    release_manifest_url: str = ""
    release_index_url: str = ""
    release_notes: str = ""
    preferences_override: dict | None = None
    error: str = ""


ManifestFetcher = Callable[[str, float], str | bytes]


def _parse_version(version: str) -> tuple[int, ...]:
    text = str(version).strip()
    match = _VERSION_RE.match(text)
    if not match:
        raise ValueError(f"Invalid version value: {version!r}")
    return tuple(int(part) for part in match.group(1).split("."))


def is_newer_version(candidate: str, current: str) -> bool:
    """Return True when candidate is strictly newer than current."""

    candidate_parts = _parse_version(candidate)
    current_parts = _parse_version(current)
    width = max(len(candidate_parts), len(current_parts))
    candidate_parts = candidate_parts + (0,) * (width - len(candidate_parts))
    current_parts = current_parts + (0,) * (width - len(current_parts))
    return candidate_parts > current_parts


def parse_update_manifest(payload: str | bytes) -> UpdateManifest:
    if isinstance(payload, bytes):
        payload = payload.decode("utf-8")

    data = json.loads(payload)
    if not isinstance(data, dict):
        raise ValueError("Update manifest must be a JSON object.")

    version = str(data.get("version", "")).strip()
    if not version:
        raise ValueError("Update manifest must include a version.")

    _parse_version(version)
    download_url = str(data.get("download_url") or data.get("download_page") or "").strip()
    announcement_url = str(data.get("announcement_web_url") or data.get("announcement_url") or "").strip()
    release_manifest_url = str(data.get("release_manifest_url") or data.get("release_notes_url") or "").strip()
    release_index_url = str(data.get("release_index_url") or data.get("release_history_url") or "").strip()
    release_notes = str(data.get("release_notes") or "").strip()
    preferences_override = data.get("preferences_override")
    if preferences_override is not None and not isinstance(preferences_override, dict):
        raise ValueError("Update manifest preferences_override must be a JSON object.")
    return UpdateManifest(
        version=version,
        download_url=download_url,
        announcement_url=announcement_url,
        release_manifest_url=release_manifest_url,
        release_index_url=release_index_url,
        release_notes=release_notes,
        preferences_override=preferences_override,
    )


def _string_list_or_text(value) -> str:
    if isinstance(value, list):
        return "\n".join(str(item).strip() for item in value if str(item).strip())
    return str(value or "").strip()


def _release_entry_from_dict(data: dict) -> ReleaseHistoryEntry:
    version = str(data.get("version", "")).strip()
    if not version:
        raise ValueError("Release manifest entry must include a version.")
    _parse_version(version)
    return ReleaseHistoryEntry(
        version=version,
        title=str(data.get("title") or "").strip(),
        date=str(data.get("date") or "").strip(),
        release_notes=_string_list_or_text(data.get("release_notes") or data.get("notes")),
        download_url=str(data.get("download_url") or data.get("download_page") or "").strip(),
        announcement_url=str(data.get("announcement_web_url") or data.get("announcement_url") or "").strip(),
    )


def parse_release_manifest(payload: str | bytes) -> ReleaseHistoryEntry:
    if isinstance(payload, bytes):
        payload = payload.decode("utf-8")

    data = json.loads(payload)
    if not isinstance(data, dict):
        raise ValueError("Release manifest must be a JSON object.")
    return _release_entry_from_dict(data)


def parse_release_index(payload: str | bytes) -> list[ReleaseHistoryEntry | str]:
    if isinstance(payload, bytes):
        payload = payload.decode("utf-8")

    data = json.loads(payload)
    if not isinstance(data, dict):
        raise ValueError("Release index must be a JSON object.")

    releases = data.get("releases", [])
    if not isinstance(releases, list):
        raise ValueError("Release index releases must be a JSON array.")

    entries: list[ReleaseHistoryEntry | str] = []
    for item in releases:
        if isinstance(item, dict):
            manifest_url = str(item.get("manifest_url") or item.get("url") or "").strip()
            entries.append(manifest_url if manifest_url else _release_entry_from_dict(item))
        else:
            raise ValueError("Release index entries must be JSON objects.")
    return entries


def fetch_update_manifest(manifest_url: str, timeout: float = 5.0) -> bytes:
    request = urllib.request.Request(
        manifest_url,
        headers={"User-Agent": "OASIS-Update-Check"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def _is_version_in_range(version: str, current_version: str, latest_version: str) -> bool:
    return is_newer_version(version, current_version) and not is_newer_version(version, latest_version)


def load_update_release_index(
    release_index_url: str = "",
    release_manifest_url: str = "",
    current_version: str = "",
    latest_version: str = "",
    timeout: float = 5.0,
    fetcher: ManifestFetcher | None = None,
) -> list[ReleaseHistoryEntry]:
    """Load release details newer than current_version, up to latest_version."""

    fetch = fetcher if fetcher else fetch_update_manifest
    latest = latest_version or "999999"
    entries: list[ReleaseHistoryEntry] = []

    if release_index_url:
        index_payload = fetch(release_index_url, timeout)
        for item in parse_release_index(index_payload):
            entry = parse_release_manifest(fetch(item, timeout)) if isinstance(item, str) else item
            if _is_version_in_range(entry.version, current_version, latest):
                entries.append(entry)
    elif release_manifest_url:
        entry = parse_release_manifest(fetch(release_manifest_url, timeout))
        if _is_version_in_range(entry.version, current_version, latest):
            entries.append(entry)

    return sorted(entries, key=lambda entry: _parse_version(entry.version))


def parse_release_history(payload: str | bytes) -> list[ReleaseHistoryEntry | str]:
    """Backward-compatible alias for pre-index metadata."""

    return parse_release_index(payload)


def load_update_release_history(
    release_history_url: str = "",
    release_manifest_url: str = "",
    current_version: str = "",
    latest_version: str = "",
    timeout: float = 5.0,
    fetcher: ManifestFetcher | None = None,
) -> list[ReleaseHistoryEntry]:
    """Backward-compatible alias for pre-index metadata."""

    return load_update_release_index(
        release_index_url=release_history_url,
        release_manifest_url=release_manifest_url,
        current_version=current_version,
        latest_version=latest_version,
        timeout=timeout,
        fetcher=fetcher,
    )


def check_for_update(
    manifest_url: str,
    current_version: str,
    timeout: float = 5.0,
    fetcher: ManifestFetcher | None = None,
) -> UpdateCheckResult:
    """Check a manifest URL and return a non-raising result for the UI."""

    url = str(manifest_url or "").strip()
    if not url:
        return UpdateCheckResult(checked=False, update_available=False)

    try:
        payload = fetcher(url, timeout) if fetcher else fetch_update_manifest(url, timeout)
        manifest = parse_update_manifest(payload)
        update_available = is_newer_version(manifest.version, current_version)
        return UpdateCheckResult(
            checked=True,
            update_available=update_available,
            latest_version=manifest.version,
            download_url=manifest.download_url,
            announcement_url=manifest.announcement_url,
            release_manifest_url=manifest.release_manifest_url,
            release_index_url=manifest.release_index_url,
            release_notes=manifest.release_notes,
            preferences_override=manifest.preferences_override,
        )
    except Exception as exc:
        return UpdateCheckResult(
            checked=True,
            update_available=False,
            error=str(exc),
        )
