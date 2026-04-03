"""Test if array examples are now correctly generated as arrays instead of scalars"""
import pandas as pd
import sys, os, warnings, tempfile, shutil, yaml
warnings.filterwarnings('ignore')
sys.path.insert(0, 'src')
from legacy_converter import LegacyConverter

LEGACY_DIR = r"C:\EBA Clearing\APIs\Templates\R2P API Participants\Legacy\2026Q4"
TEMP_OUT = os.path.join(tempfile.gettempdir(), "oasis_test_array_ex")
if os.path.exists(TEMP_OUT):
    shutil.rmtree(TEMP_OUT)
os.makedirs(TEMP_OUT)

print("Running conversion with array example fix...")
converter = LegacyConverter(LEGACY_DIR, TEMP_OUT, log_callback=lambda msg: None)
success = converter.convert(tracing_enabled=False)
print(f"Conversion success: {success}")

# Check a specific endpoint that has array fields in response
test_ep = "participantManagement_inquiryUnavailability.260331.xlsx"
test_path = os.path.join(TEMP_OUT, test_ep)
if os.path.exists(test_path):
    xl = pd.ExcelFile(test_path)
    if "200" in xl.sheet_names:
        df = pd.read_excel(xl, "200", dtype=str, header=None)
        # Find the examples row
        for idx, row in df.iterrows():
            if str(row.iloc[0]).strip() == "examples" and str(row.iloc[1]).strip() == "OK":
                example_val = str(row.iloc[13]).strip() if len(row) > 13 else ""
                print(f"\n=== {test_ep} / 200 OK example ===")
                print(example_val[:500])
                
                # Parse the YAML and check array fields
                try:
                    example_dict = yaml.safe_load(example_val)
                    if 'list' in example_dict:
                        list_obj = example_dict['list']
                        if isinstance(list_obj, dict):
                            for field, value in list_obj.items():
                                if field in ['solutionPurposeId', 'aosId']:
                                    print(f"  {field}: {type(value).__name__} = {value}")
                                    if field == 'solutionPurposeId' and isinstance(value, str):
                                        print("    ❌ ERROR: array field emitted as string!")
                                    elif field == 'solutionPurposeId' and isinstance(value, list):
                                        print("    ✅ FIXED: array field correctly emitted as list!")
                except Exception as e:
                    print(f"  YAML parse error: {e}")
                break
    xl.close()

# Cleanup
shutil.rmtree(TEMP_OUT, ignore_errors=True)
