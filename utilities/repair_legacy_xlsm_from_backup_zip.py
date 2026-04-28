from __future__ import annotations

import argparse
import shutil
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
from xml.etree import ElementTree as ET


CURRENT_SHEET_PREFIX = "xl/worksheets/"
WORKBOOK_RELS_PATH = "xl/_rels/workbook.xml.rels"
CONTENT_TYPES_PATH = "[Content_Types].xml"
CALCCHAIN_PATH = "xl/calcChain.xml"
STYLES_PATH = "xl/styles.xml"

PKG_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
CALCCHAIN_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/calcChain"


def read_zip_map(path: Path) -> dict[str, bytes]:
    with ZipFile(path, "r") as zf:
        return {info.filename: zf.read(info.filename) for info in zf.infolist()}


def remove_calcchain_relationships(xml_bytes: bytes) -> bytes:
    root = ET.fromstring(xml_bytes)
    removed = False
    for rel in list(root):
        if rel.attrib.get("Type") == CALCCHAIN_REL:
            root.remove(rel)
            removed = True
    if not removed:
        return xml_bytes
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def remove_calcchain_content_type(xml_bytes: bytes) -> bytes:
    root = ET.fromstring(xml_bytes)
    removed = False
    for child in list(root):
        if child.attrib.get("PartName") == "/xl/calcChain.xml":
            root.remove(child)
            removed = True
    if not removed:
        return xml_bytes
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def extract_backup_members(backup_zip: Path, temp_dir: Path) -> dict[str, Path]:
    extracted: dict[str, Path] = {}
    with ZipFile(backup_zip, "r") as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            name = Path(info.filename).name
            if not name.lower().endswith(".xlsm"):
                continue
            dest = temp_dir / name
            with zf.open(info, "r") as src, dest.open("wb") as dst:
                shutil.copyfileobj(src, dst)
            extracted[name] = dest
    return extracted


def repair_one(target_path: Path, source_path: Path, backup_path: Path) -> tuple[bool, str]:
    current_entries = read_zip_map(source_path)
    backup_entries = read_zip_map(backup_path)

    if "xl/vbaProject.bin" not in backup_entries:
        return False, "backup missing xl/vbaProject.bin"

    merged_entries = dict(backup_entries)
    replaced_sheets = 0
    for name, data in current_entries.items():
        if name.startswith(CURRENT_SHEET_PREFIX) and name.endswith(".xml"):
            merged_entries[name] = data
            replaced_sheets += 1

    if STYLES_PATH in current_entries:
        merged_entries[STYLES_PATH] = current_entries[STYLES_PATH]

    merged_entries.pop(CALCCHAIN_PATH, None)
    if WORKBOOK_RELS_PATH in merged_entries:
        merged_entries[WORKBOOK_RELS_PATH] = remove_calcchain_relationships(merged_entries[WORKBOOK_RELS_PATH])
    if CONTENT_TYPES_PATH in merged_entries:
        merged_entries[CONTENT_TYPES_PATH] = remove_calcchain_content_type(merged_entries[CONTENT_TYPES_PATH])

    tmp_path = target_path.with_suffix(target_path.suffix + ".repairing")
    backup_copy = target_path.with_suffix(target_path.suffix + ".bak-corrupted")

    with ZipFile(tmp_path, "w", compression=ZIP_DEFLATED) as zf:
        for name in sorted(merged_entries):
            zf.writestr(name, merged_entries[name])

    test_entries = read_zip_map(tmp_path)
    if "xl/vbaProject.bin" not in test_entries:
        tmp_path.unlink(missing_ok=True)
        return False, "repaired file missing xl/vbaProject.bin"
    if replaced_sheets == 0:
        tmp_path.unlink(missing_ok=True)
        return False, "no sheet xml found in corrupted source"

    if not backup_copy.exists():
        shutil.copy2(source_path, backup_copy)
    tmp_path.replace(target_path)
    return True, f"repaired with {replaced_sheets} sheet xml"


def main() -> int:
    parser = argparse.ArgumentParser(description="Repair corrupted legacy .xlsm files by restoring VBA/package parts from a backup zip.")
    parser.add_argument("backup_zip", type=Path, help="Zip file containing old .xlsm originals")
    parser.add_argument("legacy_dir", type=Path, help="Folder containing current legacy .xlsm files to repair")
    args = parser.parse_args()

    backup_zip = args.backup_zip.resolve()
    legacy_dir = args.legacy_dir.resolve()

    if not backup_zip.is_file():
        raise SystemExit(f"Backup zip not found: {backup_zip}")
    if not legacy_dir.is_dir():
        raise SystemExit(f"Legacy directory not found: {legacy_dir}")

    repaired = 0
    skipped = 0
    failed = 0

    with tempfile.TemporaryDirectory(prefix="oas_vba_repair_") as temp_name:
        temp_dir = Path(temp_name)
        backup_members = extract_backup_members(backup_zip, temp_dir)

        for target_path in sorted(legacy_dir.glob("*.xlsm")):
            backup_path = backup_members.get(target_path.name)
            if backup_path is None:
                print(f"SKIPPED|{target_path.name}|missing in backup zip")
                skipped += 1
                continue

            source_path = target_path.with_suffix(target_path.suffix + ".bak-corrupted")
            if not source_path.exists():
                print(f"SKIPPED|{target_path.name}|missing source {source_path.name}")
                skipped += 1
                continue

            ok, message = repair_one(target_path, source_path, backup_path)
            if ok:
                print(f"REPAIRED|{target_path.name}|{message}")
                repaired += 1
            else:
                print(f"FAILED|{target_path.name}|{message}")
                failed += 1

    print(f"REPAIRED_TOTAL={repaired}")
    print(f"SKIPPED_TOTAL={skipped}")
    print(f"FAILED_TOTAL={failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
