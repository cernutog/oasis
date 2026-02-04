
import yaml
import os

def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def audit_parity():
    ref_path = r"C:\Users\giuse\Downloads\EBACL_STEP2_20250507_Openapi3.1_SCT_API_Participants_2_1_v20251006.yaml"
    gen_path = r"Output OAS\generated_oas_3.1.yaml"
    
    if not os.path.exists(ref_path):
        print(f"FAIL: Reference not found at {ref_path}")
        return
    if not os.path.exists(gen_path):
        print(f"FAIL: Generated OAS not found at {gen_path}")
        return

    ref_spec = load_yaml(ref_path)
    gen_spec = load_yaml(gen_path)
    
    ref_schemas = ref_spec.get('components', {}).get('schemas', {})
    gen_schemas = gen_spec.get('components', {}).get('schemas', {})
    
    print(f"Reference Schemas: {len(ref_schemas)}")
    print(f"Generated Schemas: {len(gen_schemas)}")
    
    # Mapping for case-insensitive comparison
    ref_keys_lower = {k.lower(): k for k in ref_schemas.keys()}
    gen_keys_lower = {k.lower(): k for k in gen_schemas.keys()}
    
    missing_in_gen = []
    parity_errors = []
    
    # Filter out native types from reference (Booleane, Number, String are often technical aliases in legacy)
    filtered_ref_keys = [k for k in ref_schemas.keys() if k.lower() not in ["boolean", "number", "string", "integer", "object"]]
    
    for ref_k in filtered_ref_keys:
        lk = ref_k.lower()
        if lk not in gen_keys_lower:
            missing_in_gen.append(ref_k)
            continue
        
        gen_k = gen_keys_lower[lk]
        ref_obj = ref_schemas[ref_k]
        gen_obj = gen_schemas[gen_k]
        
        # Audit Properties
        ref_props = ref_obj.get('properties', {})
        gen_props = gen_obj.get('properties', {})
        
        ref_p_keys_lower = {k.lower(): k for k in ref_props.keys()}
        gen_p_keys_lower = {k.lower(): k for k in gen_props.keys()}
        
        missing_p = []
        for rpk_lower, rpk_original in ref_p_keys_lower.items():
            if rpk_lower not in gen_p_keys_lower:
                missing_p.append(rpk_original)
        
        extra_p = []
        for gpk_lower, gpk_original in gen_p_keys_lower.items():
            if gpk_lower not in ref_p_keys_lower:
                extra_p.append(gpk_original)
        
        if missing_p or extra_p:
            parity_errors.append({
                "schema": ref_k,
                "gen_name": gen_k,
                "missing": missing_p,
                "extra": extra_p
            })

            
    print("\n--- AUDIT RESULTS ---")
    if missing_in_gen:
        print(f"Missing Schemas in Generated ({len(missing_in_gen)}):")
        for m in missing_in_gen: print(f"  - {m}")
    else:
        print("PASS: All non-native reference schemas found (case-insensitive).")
        
    if parity_errors:
        print(f"\nProperty Parity Issues ({len(parity_errors)} schemas):")
        for err in parity_errors[:10]: # Limit output
            print(f"  Schema: {err['schema']} (vs {err['gen_name']})")
            if err['missing']: print(f"    Missing props: {err['missing']}")
            if err['extra']: print(f"    Extra props: {err['extra']}")
        if len(parity_errors) > 10:
            print(f"  ... and {len(parity_errors)-10} more.")
    else:
        print("PASS: All matching schemas have identical property sets.")

if __name__ == "__main__":
    audit_parity()
