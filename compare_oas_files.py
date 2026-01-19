"""Compare Generated OAS vs Reference OAS semantically."""
import yaml
import sys
import json

REF_FILE = 'Expected results/EBACL_FPAD_20251110_OpenApi3.1_FPAD_API_Participant_4.1_v20251212.yaml'
GEN_FILE = 'Imported Templates/generated/generated_oas_3.1.yaml'

def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def diff_obj(ref, gen, path=""):
    """Recursive diff."""
    if type(ref) != type(gen):
        return [f"{path}: Type mismatch {type(ref)} vs {type(gen)}"]
    
    diffs = []
    if isinstance(ref, dict):
        ref_keys = set(ref.keys())
        gen_keys = set(gen.keys())
        common = ref_keys & gen_keys
        missing = ref_keys - gen_keys
        extra = gen_keys - ref_keys
        
        for k in missing:
            diffs.append(f"{path}.{k}: MISSING in Gen")
        for k in extra:
            # diffs.append(f"{path}.{k}: EXTRA in Gen") # Ignore extra for now? or report?
            pass # Report at top level only
            
        for k in common:
            diffs.extend(diff_obj(ref[k], gen[k], f"{path}.{k}"))
            
    elif isinstance(ref, list):
        if len(ref) != len(gen):
            diffs.append(f"{path}: List length mismatch {len(ref)} vs {len(gen)}")
        else:
            for i, (r, g) in enumerate(zip(sorted(ref, key=str) if all(isinstance(x, (str,int)) for x in ref) else ref, 
                                          sorted(gen, key=str) if all(isinstance(x, (str,int)) for x in gen) else gen)):
                diffs.extend(diff_obj(r, g, f"{path}[{i}]"))
    else:
        if ref != gen:
            # Ignore whitespace in description?
            if isinstance(ref, str) and isinstance(gen, str):
                if ref.strip() == gen.strip(): return []
            diffs.append(f"{path}: Value mismatch '{ref}' vs '{gen}'")
            
    return diffs

def compare_dicts(ref, gen, context=""):
    """Compare content of two dicts (paths or components)."""
    ref_keys = set(ref.keys())
    gen_keys = set(gen.keys())
    
    common = ref_keys & gen_keys
    missing_in_gen = ref_keys - gen_keys
    extra_in_gen = gen_keys - ref_keys
    
    print(f"\n[{context}] Comparison:")
    print(f"  Total Ref: {len(ref_keys)}")
    print(f"  Total Gen: {len(gen_keys)}")
    print(f"  Common: {len(common)}")
    
    if missing_in_gen:
        print(f"  MISSING in GEN ({len(missing_in_gen)}): {sorted(list(missing_in_gen))}")
    if extra_in_gen:
        print(f"  EXTRA in GEN ({len(extra_in_gen)}): {sorted(list(extra_in_gen))}")
        
    # Deep compare common items
    diffs_found = 0
    for key in common:
        d = diff_obj(ref[key], gen[key], key)
        if d:
            print(f"  DIFF in '{key}':")
            for msg in d[:5]:
                print(f"    {msg}")
            if len(d) > 5: print("    ...")
            diffs_found += 1
            if diffs_found > 10:
                print("    ... (Stopping diff detail)")
                break


def main():
    print(f"Loading Ref: {REF_FILE}")
    ref_oas = load_yaml(REF_FILE)
    print(f"Loading Gen: {GEN_FILE}")
    gen_oas = load_yaml(GEN_FILE)
    
    # 1. Compare Info (Basic)
    print("\n=== INFO ===")
    print(f"Ref Version: {ref_oas.get('info', {}).get('version')}")
    print(f"Gen Version: {gen_oas.get('info', {}).get('version')}")

    # 2. Compare Components
    print("\n=== COMPONENTS ===")
    ref_comps = ref_oas.get('components', {})
    gen_comps = gen_oas.get('components', {})
    
    for section in ['schemas', 'responses', 'parameters', 'headers']:
        compare_dicts(ref_comps.get(section, {}), gen_comps.get(section, {}), f"Components/{section}")

    # 3. Compare Paths
    print("\n=== PATHS ===")
    compare_dicts(ref_oas.get('paths', {}), gen_oas.get('paths', {}), "Paths")

if __name__ == "__main__":
    main()
