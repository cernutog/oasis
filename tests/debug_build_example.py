"""
Debug the actual _build_body_example_dict call for retransmitOutFiles
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

# Get the Body structure for retransmitOutFiles
import pandas as pd
ep_filename = "retransmitOutFiles.210702.xlsm"
ep_path = INPUT_DIR / ep_filename

if ep_path.exists():
    xl = pd.ExcelFile(ep_path)
    children = converter._read_legacy_structure(xl, "Body")
    
    print(f"=== Building Body Example for {ep_filename} ===")
    
    # Test _build_body_example_dict
    result = converter._build_body_example_dict(children, ep_filename)
    
    print(f"Result: {result}")
    
    # Also test with debug prints
    print(f"\n=== Manual check of each field ===")
    for name, parent, desc, dtype, mandatory, v_rules, items_type in children:
        print(f"\nField: {name}")
        print(f"  dtype: {dtype}")
        dt = converter._resolve_leaf_dt(dtype, ep_filename)
        print(f"  resolved dt: {dt is not None}")
        if dt:
            examples = converter._get_example_values(dt)
            print(f"  examples: {examples}")
        else:
            print(f"  no dt resolved")
else:
    print(f"File not found: {ep_path}")
