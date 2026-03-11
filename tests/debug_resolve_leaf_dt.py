"""
Debug _resolve_leaf_dt behavior for NetworkFileName
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

# Load global schemas
converter._collect_all_data_types()
converter._perform_naming_and_usage_pass()

# Test _resolve_leaf_dt
ep_filename = "retransmitOutFiles.210702.xlsm"
dtype = "NetworkFileName"

print(f"=== Testing _resolve_leaf_dt for '{dtype}' ===")
leaf_dt = converter._resolve_leaf_dt(dtype, ep_filename)
print(f"_resolve_leaf_dt result: {leaf_dt}")

# Also test _resolve_data_type
out_name, resolved_dt = converter._resolve_data_type(dtype, ep_filename)
print(f"_resolve_data_type result: name='{out_name}', dt={resolved_dt}")
if resolved_dt:
    print(f"  - Type: {resolved_dt.type}")
    print(f"  - Example: '{resolved_dt.example}'")
    print(f"  - Source: {resolved_dt.source_file}")
