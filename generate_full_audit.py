
import yaml
import os

def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def generate_report():
    ref_path = r"C:\Users\giuse\Downloads\EBACL_STEP2_20250507_Openapi3.1_CGS-DKK_API_Participants_2_0_v20251006.yaml"
    gen_path = r"Output OAS\generated_oas_3.1.yaml"
    report_path = "full_parity_audit_report.md"

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
    
    # Pre-process for matching
    ref_keys_lower = {k.lower(): k for k in ref_schemas.keys()}
    gen_keys_lower = {k.lower(): k for k in gen_schemas.keys()}
    
    import datetime
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"# Full Parity Audit Report (Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n\n")
        f.write(f"**Reference File:** `{os.path.basename(ref_path)}`\n")
        f.write(f"**Generated File:** `{os.path.basename(gen_path)}`\n\n")
        
        f.write("## Executive Summary\n\n")
        f.write(f"- Total Reference Schemas: {len(ref_schemas)}\n")
        f.write(f"- Total Generated Schemas: {len(gen_schemas)}\n")
        
        # 1. Missing Schemas
        missing = [k for k in ref_schemas.keys() if k.lower() not in gen_keys_lower]
        # Ignore technical native types
        missing = [m for m in missing if m.lower() not in ["boolean", "number", "string", "integer", "object"]]
        
        f.write(f"- Missing Schemas in Gen (non-native): {len(missing)}\n")
        
        extra_schemas = [k for k in gen_schemas.keys() if k.lower() not in ref_keys_lower]
        # Ignore technical native types
        extra_schemas = [m for m in extra_schemas if m.lower() not in ["boolean", "number", "string", "integer", "object", "array"]]
        
        f.write(f"- Extra Schemas in Gen: {len(extra_schemas)}\n")
        
        # 2. Detailed Schema Parity
        f.write("\n## Schema Property Comparison\n\n")
        f.write("| Reference Schema | Generated Schema | Match Status | Details |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        
        matched_count = 0
        mismatch_count = 0
        
        # Iterate over all reference schemas (excluding technical ones)
        for ref_k in sorted(ref_schemas.keys()):
            if ref_k.lower() in ["boolean", "number", "string", "integer", "object", "array"]: continue
            
            lk = ref_k.lower()
            if lk not in gen_keys_lower:
                f.write(f"| {ref_k} | - | ❌ Missing | Not found in generated OAS |\n")
                mismatch_count += 1
                continue
            
            gen_k = gen_keys_lower[lk]
            ref_obj = ref_schemas[ref_k]
            gen_obj = gen_schemas[gen_k]
            
            ref_props = ref_obj.get('properties', {})
            gen_props = gen_obj.get('properties', {})
            
            # Case-sensitive property check
            ref_p_set = set(ref_props.keys())
            gen_p_set = set(gen_props.keys())
            
            missing_props = ref_p_set - gen_p_set
            extra_props = gen_p_set - ref_p_set
            
            # Type check for matched properties
            type_mismatches = []
            for common_p in (ref_p_set & gen_p_set):
                ref_node = ref_props[common_p]
                gen_node = gen_props[common_p]
                
                ref_t = ref_node.get('type') or ref_node.get('$ref', 'Complex')
                gen_t = gen_node.get('type') or gen_node.get('$ref', 'Complex')
                
                # Normalize ref path for comparison if it exists
                if isinstance(ref_t, str) and '#/components/schemas/' in ref_t:
                    ref_t = ref_t.split('/')[-1]
                if isinstance(gen_t, str) and '#/components/schemas/' in gen_t:
                    gen_t = gen_t.split('/')[-1]
                
                if str(ref_t).lower() != str(gen_t).lower():
                    type_mismatches.append(f"`{common_p}`: {ref_t} vs {gen_t}")

            if not missing_props and not extra_props and not type_mismatches:
                f.write(f"| {ref_k} | {gen_k} | ✅ Exact | Full property set match |\n")
                matched_count += 1
            else:
                details = []
                if missing_props: details.append(f"Missing: {list(missing_props)}")
                if extra_props: details.append(f"Extra: {list(extra_props)}")
                if type_mismatches: details.append(f"Types: {type_mismatches}")
                
                status = "⚠️ Partial" if not missing_props else "❌ Mismatch"
                f.write(f"| {ref_k} | {gen_k} | {status} | {'; '.join(details)} |\n")
                mismatch_count += 1

        # 3. Extra Schemas Details
        if extra_schemas:
            f.write("\n## Extra Schemas in Generated OAS\n\n")
            f.write("The following schemas are in the generated OAS but NOT in the reference. These might be redundant variants or incorrectly hoisted properties.\n\n")
            for ex in sorted(extra_schemas):
                f.write(f"- {ex}\n")

        f.write(f"\n\n**Final Statistics:** {matched_count} Exact Matches, {mismatch_count} Discrepancies (including missing ref schemas).\n")

    print(f"Report generated at: {report_path}")

if __name__ == "__main__":
    generate_report()
