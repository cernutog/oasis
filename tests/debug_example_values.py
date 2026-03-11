"""
Debug why _get_example_values returns empty list for NetworkFileName
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

# Resolve NetworkFileName in context
ep_filename = "retransmitOutFiles.210702.xlsm"
out_name, dt = converter._resolve_data_type("NetworkFileName", ep_filename)

if dt:
    print(f"=== DataType: {out_name} ===")
    print(f"Type: {dt.type}")
    print(f"Example raw: '{dt.example}'")
    
    # Test _get_example_values
    examples = converter._get_example_values(dt)
    print(f"_get_example_values result: {examples}")
    
    # Test manual split
    if dt.example:
        manual = [p.strip() for p in dt.example.split(";") if p.strip()]
        print(f"Manual split: {manual}")
else:
    print("Failed to resolve NetworkFileName")
