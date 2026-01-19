
import os
import yaml
import difflib

source_path = r"C:\Users\giuse\.gemini\antigravity\scratch\OASIS\OAS Imports\EBACL_FPAD_20260116_OpenApi3.1_FPAD_API_Participant_5.0.7_v20260418.yaml"
gen_path = r"C:\Users\giuse\.gemini\antigravity\scratch\OASIS\Imported Templates\_roundtrip_history\20260119_040439\generated_oas_3.1.yaml"

schemas_to_check = [
    "InsightNotificationSearchFilter",
    "TransactionInvestigationReportFilter"
]

def load_schema(path, schema_name):
    if not os.path.exists(path):
        return f"File not found: {path}"
    with open(path, 'r', encoding='utf-8') as f:
        oas = yaml.safe_load(f)
    return oas.get('components', {}).get('schemas', {}).get(schema_name)

print(f"Comparing schemas between:\nSource: {os.path.basename(source_path)}\nGen:    {os.path.basename(gen_path)}\n")

for name in schemas_to_check:
    print(f"\n--- {name} ---")
    s_obj = load_schema(source_path, name)
    g_obj = load_schema(gen_path, name)
    
    s_yaml = yaml.dump(s_obj, sort_keys=False) if s_obj else "MISSING"
    g_yaml = yaml.dump(g_obj, sort_keys=False) if g_obj else "MISSING"
    
    print("SOURCE:")
    print(s_yaml)
    print("\nGENERATED:")
    print(g_yaml)
    
    print("\nDIFF:")
    diff = difflib.unified_diff(s_yaml.splitlines(), g_yaml.splitlines(), lineterm='')
    for line in diff:
        print(line)
