import pandas as pd
from pathlib import Path
import os
import shutil
from src.legacy_converter import LegacyConverter

def setup_mock_project():
    p = Path("tests/repro_array")
    if p.exists(): shutil.rmtree(p)
    p.mkdir(parents=True)
    
    # Global index
    idx_path = p / "$index.xlsx"
    paths_df = pd.DataFrame([
        ["Excel File", "OperationID"],
        ["endpoint_A.xlsx", "testOp"]
    ])
    
    # Global Data Type sheet
    data_types_df = pd.DataFrame([
        ["Name", "Type", "Items Data Type (Array only)"],
        ["array", "array", "object"],
        ["object", "object", ""],
        ["MyArray", "array", "BIC8"],
        ["BIC8", "string", ""]
    ])
    
    with pd.ExcelWriter(idx_path) as writer:
        paths_df.to_excel(writer, sheet_name="Paths", index=False)
        data_types_df.to_excel(writer, sheet_name="Data Type", index=False)
        pd.DataFrame([["Title", "Value"]]).to_excel(writer, sheet_name="General Description", index=False)
        pd.DataFrame([["Name", "Description"]]).to_excel(writer, sheet_name="Tags", index=False)
        pd.DataFrame([["Schema Name", "Type"]]).to_excel(writer, sheet_name="Schemas", index=False)

    # endpoint_A.xlsx setup
    ep_name = "endpoint_A.xlsx"
    ep_path = p / ep_name
    body_df = pd.DataFrame([
        ["Element", "Parent", "Data Type"],
        ["root", "", "object"],
        ["configuredS2Dp", "root", "array"],
        ["s2dpBIC", "configuredS2Dp", "BIC8"],
        ["customList", "root", "MyArray"]
    ])
    
    with pd.ExcelWriter(ep_path) as writer:
        body_df.to_excel(writer, sheet_name="Body", index=False)
        pd.DataFrame([["Name", "Type"]]).to_excel(writer, sheet_name="Data Type", index=False)
        pd.DataFrame([["Name", "In"]]).to_excel(writer, sheet_name="Parameters", index=False)
        pd.DataFrame([["Element", "Type"]]).to_excel(writer, sheet_name="200", index=False)

def test_array_conversion():
    setup_mock_project()
    input_dir = "tests/repro_array"
    output_dir = "tests/Converted Templates"
    if Path(output_dir).exists(): shutil.rmtree(output_dir)
    
    print(f"Running conversion from {input_dir} to {output_dir} (Internal master resolution)...")
    # We do NOT pass master_dir, it should be found automatically in CWD/Templates Master
    converter = LegacyConverter(input_dir, output_dir)
    success = converter.convert(tracing_enabled=False)
    
    if not success:
        print("FAIL: Conversion failed (likely could not find master_dir internally)")
        return

    # Verify Schema Sheet
    schemas_path = Path(output_dir) / "$index.xlsx"
    df_schemas = pd.read_excel(schemas_path, sheet_name="Schemas", header=None)
    
    print("\n--- SCHEMAS SHEET CHECK ---")
    all_data = df_schemas.values.tolist()
    schema_names = [str(r[0]) for r in all_data if r[0] and str(r[0]) != "Schema Name"]
    
    if "array" in [s.lower() for s in schema_names] or "object" in [s.lower() for s in schema_names]:
        print("FAIL: Literal primitive schemas (array/object) should have been suppressed!")
    else:
        print("PASS: Literal primitive schemas suppressed.")
        
    row_ma = next((r for r in all_data if r[0] == "MyArray"), None)
    if row_ma and str(row_ma[3]).lower() == "array" and str(row_ma[4]).lower() == "bic8":
        print("PASS: MyArray schema preserved and items resolved correctly (BIC8).")
    else:
        print(f"FAIL: MyArray resolution incorrect or missing. Found: {row_ma}")

    # Verify Endpoint Body Sheet
    ep_out_path = Path(output_dir) / "endpoint_A.xlsx"
    df_body = pd.read_excel(ep_out_path, sheet_name="Body", header=None)
    body_data = df_body.values.tolist()
    
    row_s2dp = next((r for r in body_data if r[1] == "configuredS2Dp"), None)
    if row_s2dp and str(row_s2dp[4]).lower() == "array" and str(row_s2dp[5]).lower() == "object":
        print("PASS: configuredS2Dp resolved correctly to primitive array of object.")
    else:
        print(f"FAIL: configuredS2Dp resolution incorrect. Found: {row_s2dp[4] if row_s2dp else 'None'}")

    row_custom = next((r for r in body_data if r[1] == "customList"), None)
    if row_custom and str(row_custom[4]).lower() == "schema" and str(row_custom[6]) == "MyArray":
        print("PASS: customList kept as schema reference (MyArray).")
    else:
        print("FAIL: customList resolution incorrect.")

if __name__ == "__main__":
    test_array_conversion()
