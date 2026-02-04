
import yaml
import pandas as pd
import os
import re
import argparse

def normalize_name(name):
    """
    Removes numeric suffixes for comparison.
    Handles both standard suffixes (e.g., Schema1) 
    and OperationId suffixes in hoisted names (e.g., op1Request).
    """
    if not isinstance(name, str): return name
    # 1. Remove trailing digits: Schema1 -> Schema
    name = re.sub(r'\d+$', '', name)
    # 2. Remove digits before Request/Response: op1Request -> opRequest
    name = re.sub(r'(\d+)(Request|Response)$', r'\2', name)
    return name

def run_audit():
    parser = argparse.ArgumentParser(description="Audit generated schemas against legacy YAML.")
    parser.add_argument("--oas", required=True, help="Path to generated OAS YAML")
    parser.add_argument("--index", required=True, help="Path to converted $index.xlsx")
    parser.add_argument("--legacy", required=True, help="Path to legacy YAML")
    parser.add_argument("--report", help="Path to write report (optional)")
    args = parser.parse_args()

    print(f"--- SCHEMA AUDIT ---")
    print(f"YAML: {args.legacy}")
    print(f"Index: {args.index}")

    # 1. Load YAML Schemas
    with open(args.legacy, 'r', encoding='utf-8') as f:
        spec = yaml.safe_load(f)
    yaml_schemas = set(spec.get('components', {}).get('schemas', {}).keys())
    print(f"Total schemas in YAML: {len(yaml_schemas)}")

    # 2. Load Excel Schemas (from the converted index)
    df_excel = pd.read_excel(args.index, sheet_name="Schemas")
    excel_schemas = set(df_excel['Name'].dropna().astype(str).unique())
    print(f"Total schemas in Excel Index: {len(excel_schemas)}")

    # 3. Categorize
    standard_excel = {s for s in excel_schemas if not s.endswith(('Request', 'Response'))}
    hoisted_excel = {s for s in excel_schemas if s.endswith(('Request', 'Response'))}

    print(f"  - Standard converted: {len(standard_excel)}")
    print(f"  - Hoisted structures: {len(hoisted_excel)}")

    # 4. Compare (Case-Insensitive & Normalized)
    yaml_schemas_map = {normalize_name(s.lower()): s for s in yaml_schemas}
    excel_schemas_map = {normalize_name(s.lower()): s for s in excel_schemas}

    # Native types we intentionally removed from Schemas
    native_types = {'boolean', 'number', 'integer', 'string', 'object', 'array'}

    missing_in_excel = []
    for norm_low, orig_yaml in yaml_schemas_map.items():
        if norm_low in native_types: continue
        if norm_low not in excel_schemas_map:
            missing_in_excel.append(orig_yaml)

    print(f"\nActually missing concepts (Normalized) ({len(missing_in_excel)}):")
    for m in sorted(missing_in_excel):
        print(f"  [MISSING] {m}")

    extra_in_excel = []
    for norm_low, orig_excel in excel_schemas_map.items():
        if norm_low not in yaml_schemas_map:
            if not orig_excel.endswith(('Request', 'Response')):
                extra_in_excel.append(orig_excel)

    print(f"\nExtra schemas in Excel index ({len(extra_in_excel)}):")
    for e in sorted(extra_in_excel):
        print(f"  [EXTRA  ] {e}")

    print("\n--- Summary ---")
    print(f"Missing concepts: {len(missing_in_excel)}")
    
    if args.report:
        with open(args.report, 'w', encoding='utf-8') as f:
            f.write(f"# Schema Audit Report\n\n")
            f.write(f"- YAML: `{args.legacy}`\n")
            f.write(f"- Index: `{args.index}`\n\n")
            f.write(f"## Missing Concepts ({len(missing_in_excel)})\n")
            for m in sorted(missing_in_excel):
                f.write(f"- [ ] {m}\n")
            f.write(f"\n## Extra Concepts ({len(extra_in_excel)})\n")
            for e in sorted(extra_in_excel):
                f.write(f"- {e}\n")

if __name__ == "__main__":
    run_audit()
