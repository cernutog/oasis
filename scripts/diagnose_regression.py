import yaml
import sys
import os

def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def compare_keys(name, d1, d2):
    k1 = set(d1.keys())
    k2 = set(d2.keys())
    
    missing_in_new = k1 - k2
    extra_in_new = k2 - k1
    
    if missing_in_new:
        print(f"\n[MISSING] {name} ({len(missing_in_new)}):")
        for k in sorted(missing_in_new):
            print(f"  - {k}")
            
    if extra_in_new:
        print(f"\n[ADDED] {name} ({len(extra_in_new)}):")
        for k in sorted(extra_in_new):
            print(f"  - {k}")
            
    return k1 & k2

def analyze():
    print("Loading Golden Master...")
    if not os.path.exists("last_good_generated_oas_3.1.yaml"):
        print("Error: last_good_generated_oas_3.1.yaml not found")
        return

    golden = load_yaml("last_good_generated_oas_3.1.yaml")
    
    print("Loading Current Output...")
    current_path = "API Templates/generated/generated_oas_3.1.yaml"
    if not os.path.exists(current_path):
        print(f"Error: {current_path} not found")
        return

    current = load_yaml(current_path)
    
    # 1. Compare Paths
    print("\n--- PATHS ANALYSIS ---")
    g_paths = golden.get("paths", {})
    c_paths = current.get("paths", {})
    common_paths = compare_keys("Paths", g_paths, c_paths)
    
    # Check for missing methods in common paths
    for p in common_paths:
        g_methods = set(g_paths[p].keys())
        c_methods = set(c_paths[p].keys())
        diff = g_methods - c_methods
        if diff:
            print(f"  [PARTIAL] Path {p} missing methods: {diff}")

    # 2. Compare Components
    print("\n--- COMPONENTS ANALYSIS ---")
    g_comps = golden.get("components", {})
    c_comps = current.get("components", {})
    
    # Schemas
    compare_keys("Schemas", g_comps.get("schemas", {}), c_comps.get("schemas", {}))
    
    # Responses
    compare_keys("Responses", g_comps.get("responses", {}), c_comps.get("responses", {}))
    
    # Parameters
    compare_keys("Parameters", g_comps.get("parameters", {}), c_comps.get("parameters", {}))

if __name__ == "__main__":
    analyze()
