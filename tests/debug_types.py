"""
Debug the exact types of values returned by _build_body_example_dict
"""
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from src.legacy_converter import LegacyConverter
import yaml

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
    
    print(f"=== Debug types in _build_body_example_dict result ===")
    
    # Get the result
    result = converter._build_body_example_dict(children, ep_filename)
    
    print(f"Result dict: {result}")
    print(f"Result type: {type(result)}")
    
    for key, value in result.items():
        print(f"\n{key}:")
        print(f"  Value: {value}")
        print(f"  Type: {type(value)}")
        print(f"  Repr: {repr(value)}")
        
        # Test YAML serialization of just this value
        single_dict = {key: value}
        yaml_str = yaml.dump(single_dict, default_flow_style=False, allow_unicode=True, sort_keys=False)
        print(f"  YAML: {yaml_str.strip()}")
else:
    print(f"File not found: {ep_path}")
