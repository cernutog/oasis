"""
Debug why get_rotated_value returns synthetic value instead of example
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

# Resolve NetworkFileName
ep_filename = "retransmitOutFiles.210702.xlsm"
out_name, dt = converter._resolve_data_type("NetworkFileName", ep_filename)

if dt:
    print(f"=== Testing get_rotated_value logic ===")
    examples = converter._get_example_values(dt)
    print(f"Examples available: {examples}")
    
    # Simulate the logic from get_rotated_value
    dtype = "string"
    low = dtype.lower()
    
    if examples:
        count = 0  # First usage
        idx = count % len(examples)
        print(f"Would select example at index {idx}: '{examples[idx]}'")
        raw = examples[idx]
        print(f"Raw value: '{raw}'")
        
        # Coerce based on DataType.type
        if dt.type.lower() in ("integer", "int"):
            try:
                result = int(raw)
                print(f"Coerced to int: {result}")
            except (ValueError, TypeError):
                print("Failed to coerce to int, keeping raw")
                result = raw
        elif dt.type.lower() in ("number", "float", "double", "decimal"):
            try:
                result = float(raw)
                print(f"Coerced to float: {result}")
            except (ValueError, TypeError):
                print("Failed to coerce to float, keeping raw")
                result = raw
        elif dt.type.lower() == "boolean":
            result = raw.lower() in ("true", "yes", "1")
            print(f"Coerced to boolean: {result}")
        else:
            result = raw
            print(f"Keeping as string: '{result}'")
    else:
        result = converter._generate_synthetic_value(low)
        print(f"No examples, using synthetic: {result}")
else:
    print("Failed to resolve NetworkFileName")
