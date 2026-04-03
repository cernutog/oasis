"""Test array examples on multiple endpoints"""
import pandas as pd
import sys, os, warnings, tempfile, shutil, yaml
warnings.filterwarnings('ignore')
sys.path.insert(0, 'src')
from legacy_converter import LegacyConverter

LEGACY_DIR = r"C:\EBA Clearing\APIs\Templates\R2P API Participants\Legacy\2026Q4"
TEMP_OUT = os.path.join(tempfile.gettempdir(), "oasis_test_array_ex2")
if os.path.exists(TEMP_OUT):
    shutil.rmtree(TEMP_OUT)
os.makedirs(TEMP_OUT)

print("Running conversion...")
converter = LegacyConverter(LEGACY_DIR, TEMP_OUT, log_callback=lambda msg: None)
success = converter.convert(tracing_enabled=False)
print(f"Conversion: {success}")

# Check endpoints with array fields
test_eps = [
    "participantManagement_inquiryUnavailability.260331.xlsx",
    "routingTable_updateRe.250624.xlsx", 
    "participantReOperation_reOperationDetails.250624.xlsx"
]

for ep in test_eps:
    ep_path = os.path.join(TEMP_OUT, ep)
    if not os.path.exists(ep_path):
        continue
        
    xl = pd.ExcelFile(ep_path)
    for sheet in ["200", "201", "Body"]:
        if sheet not in xl.sheet_names:
            continue
            
        df = pd.read_excel(xl, sheet, dtype=str, header=None)
        print(f"\n=== {ep} / {sheet} ===")
        
        # Find examples
        for idx, row in df.iterrows():
            if str(row.iloc[0]).strip() == "examples":
                example_type = str(row.iloc[1]).strip()
                example_val = str(row.iloc[13]).strip() if len(row) > 13 else ""
                if example_val and example_val.lower() != 'nan':
                    print(f"  Example: {example_type}")
                    try:
                        example_dict = yaml.safe_load(example_val)
                        # Check for array fields
                        def check_arrays(obj, path=""):
                            if isinstance(obj, dict):
                                for k, v in obj.items():
                                    new_path = f"{path}.{k}" if path else k
                                    if k in ['solutionPurposeId', 'aosId', 'list']:
                                        print(f"    {new_path}: {type(v).__name__} = {v}")
                                        if k in ['solutionPurposeId', 'aosId'] and isinstance(v, str):
                                            print(f"      ❌ ERROR: {k} should be array, got string")
                                        elif k in ['solutionPurposeId', 'aosId'] and isinstance(v, list):
                                            print(f"      ✅ FIXED: {k} correctly array")
                                    check_arrays(v, new_path)
                            elif isinstance(obj, list):
                                for i, item in enumerate(obj):
                                    check_arrays(item, f"{path}[{i}]")
                        check_arrays(example_dict)
                    except Exception as e:
                        print(f"    Parse error: {e}")
        break
    xl.close()

shutil.rmtree(TEMP_OUT, ignore_errors=True)
