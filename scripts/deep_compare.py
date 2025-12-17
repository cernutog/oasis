import yaml
import sys
import json

def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def deep_compare_path():
    golden = load_yaml("last_good_generated_oas_3.1.yaml")
    current = load_yaml("API Templates/generated/generated_oas_3.1.yaml")
    
    # Pick first path
    path_url = list(golden["paths"].keys())[0]
    print(f"Comparing Path: {path_url}")
    
    g_op = golden["paths"][path_url]
    c_op = current["paths"][path_url]
    
    # Dump both to JSON strings and diff?
    # Or just print structure?
    
    print("\nGolden keys:", g_op.keys())
    print("Current keys:", c_op.keys())
    
    # Check method (e.g. post)
    method = list(g_op.keys())[0]
    print(f"\nComparing Method: {method}")
    
    g_m = g_op[method]
    c_m = c_op.get(method, {})
    
    print("Golden Method keys:", g_m.keys())
    print("Current Method keys:", c_m.keys())
    
    # Check Request Body
    if "requestBody" in g_m:
        print("\nRequest Body Comparison:")
        g_rb = json.dumps(g_m["requestBody"], sort_keys=True, indent=2)
        c_rb = json.dumps(c_m.get("requestBody", {}), sort_keys=True, indent=2)
        if g_rb == c_rb:
            print("MATCH")
        else:
            print("MISMATCH")
            print("Golden Length:", len(g_rb))
            print("Current Length:", len(c_rb))
            # print("Golden:", g_rb)
            # print("Current:", c_rb)
            
    # Check Responses
    if "responses" in g_m:
        print("\nResponses Comparison:")
        g_resp = json.dumps(g_m["responses"], sort_keys=True, indent=2)
        c_resp = json.dumps(c_m.get("responses", {}), sort_keys=True, indent=2)
        if g_resp == c_resp:
            print("MATCH")
        else:
            print("MISMATCH")
            print("Golden Length:", len(g_resp))
            print("Current Length:", len(c_resp))

if __name__ == "__main__":
    deep_compare_path()
