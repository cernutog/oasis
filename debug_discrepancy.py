
import yaml
import json
import logging

# Configure logging to avoid encoding errors on Windows console
logging.basicConfig(level=logging.INFO, format='%(message)s')

def deep_compare(schema_name):
    ref_path = r"C:\Users\giuse\Downloads\EBACL_STEP2_20250507_Openapi3.1_CGS-DKK_API_Participants_2_0_v20251006.yaml"
    gen_path = r"Output V3 OAS\generated_oas_3.1.yaml"

    try:
        with open(ref_path, 'r', encoding='utf-8') as f:
            ref_spec = yaml.safe_load(f)
        with open(gen_path, 'r', encoding='utf-8') as f:
            gen_spec = yaml.safe_load(f)
    except FileNotFoundError as e:
        print(f"Error loading files: {e}")
        return

    ref_s = ref_spec.get('components', {}).get('schemas', {}).get(schema_name)
    gen_s = gen_spec.get('components', {}).get('schemas', {}).get(schema_name)

    print(f"\n======== Comparison for {schema_name} ========")
    
    if not ref_s:
        print(f"MISSING IN REFERENCE: {schema_name}")
    if not gen_s:
        print(f"MISSING IN GENERATED: {schema_name}")
        
    if ref_s and gen_s:
        # Normalize for comparison (ignore order)
        ref_json = json.dumps(ref_s, sort_keys=True, default=str)
        gen_json = json.dumps(gen_s, sort_keys=True, default=str)
        
        if ref_json == gen_json:
            print("STATUS: EXACT MATCH")
        else:
            print("STATUS: DISCREPANCY")
            print("--- REFERENCE ---")
            print(json.dumps(ref_s, indent=2, sort_keys=True))
            print("\n--- GENERATED ---")
            print(json.dumps(gen_s, indent=2, sort_keys=True))

if __name__ == "__main__":
    targets = ["Alerts", "alerts", "AgendaDetails", "Commands"]
    for t in targets:
        deep_compare(t)
