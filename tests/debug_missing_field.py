"""
Debug why networkFileName is completely missing from _build_body_example_dict result
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
    
    print(f"=== Debug why networkFileName is missing ===")
    
    # Print all children structure
    print(f"\nAll children from _read_legacy_structure:")
    for i, child in enumerate(children, 1):
        name, parent, desc, dtype, mandatory, v_rules, items_type = child
        print(f"  {i}. {name:20s} | parent: {parent or 'ROOT':10s} | dtype: {dtype:15s} | mandatory: {mandatory or 'O':1s}")
    
    # Test _build_body_example_dict step by step
    print(f"\n=== Testing _build_body_example_dict step by step ===")
    
    # Build parent → children mapping
    node_parent = {}
    node_dtype = {}
    ordered_names = []
    
    for name, parent, desc, dtype, mandatory, v_rules, items_type in children:
        node_parent[name] = parent or ""
        node_dtype[name] = dtype or "string"
        ordered_names.append(name)
    
    print(f"Ordered names: {ordered_names}")
    
    # Test building result manually
    result = {}
    type_counters = {}
    
    for name in ordered_names:
        dtype = node_dtype[name]
        dt = converter._resolve_leaf_dt(dtype, ep_filename)
        
        print(f"\nProcessing field: {name}")
        print(f"  dtype: {dtype}")
        print(f"  dt resolved: {dt is not None}")
        
        if dt:
            examples = converter._get_example_values(dt)
            print(f"  examples: {examples}")
            
            if examples:
                low = dtype.lower() if dtype else "string"
                count = type_counters.get(low, 0)
                idx = count % len(examples)
                type_counters[low] = count + 1
                raw = examples[idx]
                print(f"  selected: '{raw}'")
                result[name] = raw
            else:
                synthetic = converter._generate_synthetic_value(dtype.lower())
                print(f"  synthetic: {synthetic}")
                result[name] = synthetic
        else:
            synthetic = converter._generate_synthetic_value(dtype.lower())
            print(f"  no dt, synthetic: {synthetic}")
            result[name] = synthetic
    
    print(f"\nFinal result: {result}")
    
    # Compare with actual _build_body_example_dict
    actual_result = converter._build_body_example_dict(children, ep_filename)
    print(f"\nActual _build_body_example_dict result: {actual_result}")
    
    print(f"\nResults match: {result == actual_result}")
else:
    print(f"File not found: {ep_path}")
