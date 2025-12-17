import yaml

def verify_content():
    try:
        with open("API Templates/generated/generated_oas_3.1.yaml", "r") as f:
            oas = yaml.safe_load(f)
            
        paths = oas.get("paths", {})
        print(f"Total Paths: {len(paths)}")
        
        ops_count = 0
        req_body_count = 0
        resp_content_count = 0
        extensions_count = 0
        
        for p, methods in paths.items():
            for m, op in methods.items():
                ops_count += 1
                if "requestBody" in op:
                    req_body_count += 1
                
                if "responses" in op:
                    for r, r_obj in op["responses"].items():
                        if "content" in r_obj:
                            resp_content_count += 1
                            
                # Check extensions
                for k in op.keys():
                    if k.startswith("x-"):
                        extensions_count += 1
        
        schemas = oas.get("components", {}).get("schemas", {})
        print(f"Total Schemas: {len(schemas)}")
                        
        print(f"Total Operations: {ops_count}")
        print(f"Operations with requestBody: {req_body_count}")
        print(f"Responses with content: {resp_content_count}")
        print(f"Total Extensions (x-*) found: {extensions_count}")
        
        # Dump first op
        if paths:
            first_path = list(paths.keys())[0]
            first_method = list(paths[first_path].keys())[0]
            op = paths[first_path][first_method]
            print(f"\n--- First Operation: {first_path} {first_method} ---")
            print(yaml.dump(op))
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_content()
