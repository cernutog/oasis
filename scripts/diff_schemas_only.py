import yaml
import json
from deepdiff import DeepDiff

GOLDEN = "Expected results/EBACL_FPAD_20251110_OpenApi3.1_FPAD_API_Participant_4.1_v20251212.yaml"
GENERATED = "API Templates/generated/generated_oas_3.1.yaml"

def compare_schemas():
    with open(GOLDEN, 'r', encoding='utf-8') as f:
        golden = yaml.safe_load(f).get("components", {}).get("schemas", {})
    
    with open(GENERATED, 'r', encoding='utf-8') as f:
        gen = yaml.safe_load(f).get("components", {}).get("schemas", {})

    print(f"Golden Schemas: {len(golden)}")
    print(f"Generated Schemas: {len(gen)}")

    # Check for missing keys
    missing = set(golden.keys()) - set(gen.keys())
    if missing:
        print(f"MISSING SCHEMAS: {missing}")
    
    # Check for extra keys
    extra = set(gen.keys()) - set(golden.keys())
    if extra:
        print(f"EXTRA SCHEMAS: {extra}")

    # Deep Diff
    diff = DeepDiff(golden, gen, ignore_order=True)
    if not diff:
        print("SUCCESS: Schemas are IDENTICAL content-wise.")
    else:
        print("DIFFERENCES FOUND:")
        if 'dictionary_item_removed' in diff:
            print("\nREMVOED (In Golden, Missing in Gen):")
            print(diff['dictionary_item_removed'])
        
        if 'dictionary_item_added' in diff:
             print("\nADDED (In Gen, Missing in Golden):")
             # Limit output
             print(str(diff['dictionary_item_added'])[:500])

if __name__ == "__main__":
    compare_schemas()
