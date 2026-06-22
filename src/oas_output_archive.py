from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
import shutil


OAS_OUTPUT_EXTENSIONS = {".yaml", ".yml", ".json"}
ARCHIVE_FOLDER_NAME = "Archive"
SOURCE_MAP_FOLDER_NAME = ".oasis_excel_maps"


def list_existing_oas_files(output_dir) -> list[Path]:
    """Return current OAS files directly inside the output folder."""
    folder = Path(output_dir)
    if not folder.exists() or not folder.is_dir():
        return []
    return sorted(
        (
            path
            for path in folder.iterdir()
            if path.is_file() and path.suffix.lower() in OAS_OUTPUT_EXTENSIONS
        ),
        key=lambda path: path.name.lower(),
    )


def filter_previous_oas_files(files, expected_filenames, today: date | None = None) -> list[Path]:
    """Return files that do not belong to the current generation day and output set."""
    current_day = today or date.today()
    expected = {str(name).lower() for name in expected_filenames}
    previous: list[Path] = []

    for path in sorted((Path(item) for item in files), key=lambda item: item.name.lower()):
        modified_day = datetime.fromtimestamp(path.stat().st_mtime).date()
        if path.name.lower() not in expected or modified_day != current_day:
            previous.append(path)

    return previous


def build_expected_oas_filenames(
    filename_pattern,
    api_version,
    release,
    gen_30=True,
    gen_31=True,
    gen_swift=False,
    today: date | None = None,
) -> set[str]:
    """Build the OAS filenames expected for one generation run."""
    current_day = today or date.today()
    current_date = current_day.strftime("%Y%m%d")
    pattern = str(filename_pattern or "").strip()
    if not pattern:
        names = set()
        if gen_30:
            names.add("generated_oas_3.0.yaml")
        if gen_31:
            names.add("generated_oas_3.1.yaml")
        if gen_swift:
            names.add("generated_oas_3.0_SWIFT.yaml")
            names.add("generated_oas_3.1_SWIFT.yaml")
        return names

    def render(oas_version, customization=""):
        customization_value = f"{customization}_" if customization else ""
        return (
            pattern.replace("<current_date>", current_date)
            .replace("<oas_version>", oas_version)
            .replace("<customization>", customization_value)
            .replace("<api_version>", str(api_version or ""))
            .replace("<release>", str(release or ""))
            .strip()
        )

    names = set()
    if gen_30:
        names.add(render("3.0"))
    if gen_31:
        names.add(render("3.1"))
    if gen_swift:
        names.add(render("3.0", "SWIFT"))
        names.add(render("3.1", "SWIFT"))
    return names


def archive_existing_oas_files(files, output_dir) -> list[tuple[Path, Path]]:
    """Move OAS files and their source maps under Archive/YYYYMMDD."""
    folder = Path(output_dir)
    moved: list[tuple[Path, Path]] = []

    for source in sorted((Path(path) for path in files), key=lambda path: path.name.lower()):
        if not source.exists() or not source.is_file():
            continue

        archive_day = datetime.fromtimestamp(source.stat().st_mtime).strftime("%Y%m%d")
        archive_folder = folder / ARCHIVE_FOLDER_NAME / archive_day
        archive_folder.mkdir(parents=True, exist_ok=True)

        destination = _unique_destination(archive_folder / source.name)
        source_map = folder / SOURCE_MAP_FOLDER_NAME / f"{source.name}.map.json"
        map_destination = archive_folder / SOURCE_MAP_FOLDER_NAME / f"{destination.name}.map.json"

        shutil.move(str(source), str(destination))
        moved.append((source, destination))

        if source_map.exists() and source_map.is_file():
            map_destination.parent.mkdir(parents=True, exist_ok=True)
            map_destination = _unique_destination(map_destination)
            shutil.move(str(source_map), str(map_destination))

    return moved


def describe_archive_destinations(moved_files) -> list[str]:
    """Return the actual archive folders used by archived OAS files."""
    folders = {Path(destination).parent for _, destination in moved_files}
    return [str(folder) for folder in sorted(folders, key=lambda path: str(path).lower())]


def delete_existing_oas_files(files, output_dir) -> list[Path]:
    """Delete current OAS files and their source maps."""
    folder = Path(output_dir)
    deleted: list[Path] = []

    for source in sorted((Path(path) for path in files), key=lambda path: path.name.lower()):
        if not source.exists() or not source.is_file():
            continue

        source_map = folder / SOURCE_MAP_FOLDER_NAME / f"{source.name}.map.json"
        source.unlink()
        deleted.append(source)

        if source_map.exists() and source_map.is_file():
            source_map.unlink()

    return deleted


def _unique_destination(destination: Path) -> Path:
    if not destination.exists():
        return destination

    counter = 1
    while True:
        candidate = destination.with_name(f"{destination.stem}_{counter}{destination.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1
