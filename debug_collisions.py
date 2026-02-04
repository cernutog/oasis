
from src.legacy_converter import LegacyConverter
import os
import pprint

def check_collisions():
    base = r"c:\Users\giuse\.gemini\antigravity\scratch\OASIS"
    c = LegacyConverter(
        legacy_dir=os.path.join(base, "Templates Legacy"),
        output_dir=os.path.join(base, "Output OAS"),
        master_dir=os.path.join(base, "Templates Master")
    )
    
    print("1. Collecting definitions...")
    print("1. Tracing usages (triggering inline extraction)...")
    index_path = os.path.join(base, "Templates Legacy", "$index.xlsm")
    # We must collect static types first
    c._preload_master_schemas()
    c._collect_all_local_definitions(index_path)
    # Then trace
    c._trace_all_usages(index_path)
    
    target = "SearchCriteria"
    print(f"2. Inspecting '{target}' across files...")
    
    variations = []
    
    for filename, defs in c.local_file_definitions.items():
        if target in defs:
            # defs[target] = (name, parent, type, attrs)
            d = defs[target]
            attrs = d[3]
            props = list(attrs.get('properties', {}).keys())
            fingerprint = tuple(sorted(props))
            
            print(f"File: {filename}")
            print(f"  Props ({len(props)}): {props}")
            variations.append((filename, fingerprint))
            
    # Check distinct fingerprints
    unique_fps = set(v[1] for v in variations)
    print(f"\nTotal files with '{target}': {len(variations)}")
    print(f"Unique variations found: {len(unique_fps)}")
    
    if len(unique_fps) > 1:
        print("DIFFERENCES FOUND! These should generate numbered schemas.")
    else:
        print("ALL IDENTICAL. Merging is correct behavior.")

if __name__ == "__main__":
    check_collisions()
