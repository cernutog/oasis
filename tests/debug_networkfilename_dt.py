"""
Check if NetworkFileName DataType has example values
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

# Check NetworkFileName DataType
dt_name = "NetworkFileName"
if dt_name in converter.global_schemas:
    dt = converter.global_schemas[dt_name]
    print(f"\n=== DataType: {dt_name} ===")
    print(f"Type: {dt.type}")
    print(f"Format: {dt.format}")
    print(f"Example: '{dt.example}'")
    print(f"Allowed values: '{dt.allowed_values}'")
    print(f"Min: '{dt.min_val}'")
    print(f"Max: '{dt.max_val}'")
    print(f"Regex: '{dt.regex}'")
else:
    print(f"DataType '{dt_name}' not found in global schemas")
