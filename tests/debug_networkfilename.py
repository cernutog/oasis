"""
Debug script to inspect the legacy Body sheet structure for retransmitOutFiles
and see why networkFileName is missing from the generated example.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from src.legacy_converter import LegacyConverter

INPUT_DIR = ROOT / "Templates Legacy"
MASTER_DIR = ROOT / "Templates Master"

def log(msg):
    print(msg)

converter = LegacyConverter(
    input_dir=str(INPUT_DIR),
    output_dir=str(ROOT / "tests" / "_debug_out"),
    master_dir=str(MASTER_DIR),
    log_callback=log,
)

# Load global schemas first
converter._collect_all_data_types()
converter._perform_naming_and_usage_pass()

# Read the legacy structure for retransmitOutFiles Body sheet
legacy_path = INPUT_DIR / "retransmitOutFiles.210702.xlsm"
if legacy_path.exists():
    print(f"\n=== Legacy Body structure for {legacy_path.name} ===")
    children = converter._read_legacy_structure(legacy_path, "Body")
    for i, (name, parent, desc, dtype, mandatory, v_rules, items_type) in enumerate(children, 1):
        print(f"{i:2d}. {name:20s} | parent: {parent or 'ROOT':10s} | type: {dtype:10s} | mandatory: {mandatory or 'O':1s} | items: {items_type or '-':10s}")
else:
    print(f"File not found: {legacy_path}")
