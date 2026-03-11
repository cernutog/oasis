import sys
import shutil
from pathlib import Path

from src.legacy_converter import LegacyConverter


def verify_legacy_tracing_merge_column() -> int:
    legacy_root = Path(__file__).parent / "Templates Legacy"
    if not legacy_root.exists():
        print("SKIP: Templates Legacy not found")
        return 0

    out_dir = Path(__file__).parent / "tmp" / "_verify_tracing_merge"
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.parent.mkdir(parents=True, exist_ok=True)

    logs = []

    def _log(msg: str):
        logs.append(str(msg))

    converter = LegacyConverter(
        str(legacy_root),
        str(out_dir),
        log_callback=_log,
        include_descriptions_in_collision=False,
        include_examples_in_collision=False,
    )
    ok = converter.convert(tracing_enabled=True)
    if not ok:
        print("FAIL: conversion failed")
        return 2

    text = "\n".join(logs)
    if "| SCHEMA NAME" not in text:
        print("FAIL: tracing table header missing")
        return 1
    if "| MERGE" not in text:
        print("FAIL: MERGE column missing in tracing table")
        return 1

    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(verify_legacy_tracing_merge_column())
