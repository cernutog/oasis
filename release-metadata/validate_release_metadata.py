import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlparse


def load_json(path):
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        raise ValueError(f"Missing file: {path}")
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}")


def manifest_path(root, latest):
    url = str(latest.get("release_manifest_url") or "").strip()
    if url:
        parsed = urlparse(url)
        candidate = Path(parsed.path).name
        if candidate:
            return root / "releases" / candidate

    version = str(latest.get("version") or "").strip()
    if not version:
        raise ValueError("oasis-version.json is missing version")
    return root / "releases" / f"v{version}.json"


def require_text(data, key, label):
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} is missing required text field '{key}'")
    return value.strip()


def optional_text(data, key, label):
    value = data.get(key)
    if value is None:
        return ""
    if not isinstance(value, str):
        raise ValueError(f"{label} field '{key}' must be text when present")
    return value.strip()


def release_notes_present(data, label):
    notes = data.get("release_notes")
    if isinstance(notes, str) and notes.strip():
        return
    if isinstance(notes, list) and notes:
        return
    raise ValueError(f"{label} is missing release_notes")


def validate_root(root):
    root = Path(root)
    latest_path = root / "oasis-version.json"
    latest = load_json(latest_path)
    release_path = manifest_path(root, latest)
    release = load_json(release_path)

    latest_version = require_text(latest, "version", str(latest_path))
    release_version = require_text(release, "version", str(release_path))
    if latest_version != release_version:
        raise ValueError(
            f"Version mismatch: {latest_path} has {latest_version}, "
            f"{release_path} has {release_version}"
        )

    latest_download = require_text(latest, "download_url", str(latest_path))
    release_download = optional_text(release, "download_url", str(release_path))
    if release_download and latest_download != release_download:
        raise ValueError(
            f"download_url mismatch between {latest_path} and {release_path}"
        )

    release_notes_present(latest, str(latest_path))
    release_notes_present(release, str(release_path))

    latest_announcement = optional_text(latest, "announcement_url", str(latest_path))
    release_announcement = optional_text(release, "announcement_url", str(release_path))
    if latest_announcement != release_announcement:
        raise ValueError(
            "announcement_url mismatch: latest update dialog reads "
            f"{latest_path}, release details read {release_path}"
        )

    print(f"OK: {root} latest release metadata is coherent for {latest_version}")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Validate OASIS latest release metadata coherence."
    )
    parser.add_argument(
        "roots",
        nargs="+",
        help="Release metadata roots containing oasis-version.json and releases/.",
    )
    args = parser.parse_args(argv)

    failures = []
    for root in args.roots:
        try:
            validate_root(root)
        except ValueError as exc:
            failures.append(str(exc))

    if failures:
        for failure in failures:
            print(f"ERROR: {failure}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
