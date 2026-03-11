"""
Debug the detailed flow inside _build_body_example_dict
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
    
    print(f"=== Detailed debug of _build_body_example_dict ===")
    
    # Manually simulate the logic step by step
    # Build parent → children mapping
    node_parent = {}
    node_dtype = {}
    ordered_names = []
    
    for name, parent, desc, dtype, mandatory, v_rules, items_type in children:
        node_parent[name] = parent or ""
        node_dtype[name] = dtype or "string"
        ordered_names.append(name)
        print(f"Field: {name:20s} | dtype: {dtype:15s} | parent: {parent or 'ROOT':10s}")
    
    # Test get_rotated_value for each field
    print(f"\n=== Testing get_rotated_value for each field ===")
    type_counters = {}
    
    for name in ordered_names:
        dtype = node_dtype[name]
        dt = converter._resolve_leaf_dt(dtype, ep_filename)
        
        print(f"\nField: {name}")
        print(f"  dtype: {dtype}")
        print(f"  resolved dt: {dt is not None}")
        
        if dt:
            examples = converter._get_example_values(dt)
            print(f"  examples: {examples}")
            
            if examples:
                low = dtype.lower() if dtype else "string"
                count = type_counters.get(low, 0)
                idx = count % len(examples)
                type_counters[low] = count + 1
                raw = examples[idx]
                print(f"  selected example [{idx}]: '{raw}'")
                
                # Coerce based on DataType.type
                if dt.type.lower() in ("integer", "int"):
                    try:
                        result = int(raw)
                        print(f"  coerced to int: {result}")
                    except (ValueError, TypeError):
                        result = raw
                elif dt.type.lower() in ("number", "float", "double", "decimal"):
                    try:
                        result = float(raw)
                        print(f"  coerced to float: {result}")
                    except (ValueError, TypeError):
                        result = raw
                elif dt.type.lower() == "boolean":
                    result = raw.lower() in ("true", "yes", "1")
                    print(f"  coerced to boolean: {result}")
                else:
                    result = raw
                    print(f"  kept as string: '{result}'")
            else:
                result = converter._generate_synthetic_value(dtype.lower())
                print(f"  no examples, synthetic: {result}")
        else:
            result = converter._generate_synthetic_value(dtype.lower())
            print(f"  no dt, synthetic: {result}")
            
        print(f"  final result: {result}")
else:
    print(f"File not found: {ep_path}")
