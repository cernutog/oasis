import yaml
import sys

def inspect_golden():
    try:
        with open("last_good_generated_oas_3.1.yaml", 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            
        schemas = data.get("components", {}).get("schemas", {})
        targets = ["dateTime", "identification", "name"]
        
        for t in targets:
            if t in schemas:
                print(f"\nSchema: {t}")
                print(yaml.dump(schemas[t], sort_keys=False))
            else:
                print(f"\nSchema: {t} NOT FOUND")
                
    except Exception as e:
        print(e)

if __name__ == "__main__":
    inspect_golden()
