"""
Test resolving NetworkFileName DataType in retransmitOutFiles context
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

# Try to resolve NetworkFileName in the context of retransmitOutFiles
ep_filename = "retransmitOutFiles.210702.xlsm"
print(f"\n=== Resolving NetworkFileName in context of {ep_filename} ===")

out_name, dt = converter._resolve_data_type("NetworkFileName", ep_filename)
if out_name and dt:
    print(f"Resolved to: {out_name}")
    print(f"Type: {dt.type}")
    print(f"Format: {dt.format}")
    print(f"Example: '{dt.example}'")
    print(f"Regex: '{dt.regex}'")
    print(f"PatternEba: '{dt.pattern_eba}'")
    print(f"Source file: {dt.source_file}")
else:
    print("Failed to resolve NetworkFileName")
    
    # Check what's in raw_data_types for this file
    print(f"\n=== Raw data types in {ep_filename} ===")
    file_key = ep_filename
    if file_key in converter.raw_data_types:
        for name, dt in converter.raw_data_types[file_key].items():
            if "network" in name.lower() or "filename" in name.lower():
                print(f"  {name}: type={dt.type}, example='{dt.example}', regex='{dt.regex}', pattern_eba='{dt.pattern_eba}'")
    else:
        print(f"No raw data types found for {file_key}")
