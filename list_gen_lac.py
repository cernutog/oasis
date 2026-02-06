
import yaml

def list_gen_schemas():
    gen_path = r"Output OAS\generated_oas_3.1.yaml"
    with open(gen_path, 'r', encoding='utf-8') as f:
        spec = yaml.safe_load(f)
    schemas = spec.get('components', {}).get('schemas', {})
    
    print("All schema keys (sorted):")
    for k in sorted(schemas.keys()):
        if 'exceptionlac' in k.lower():
            print(f"- {k}")

if __name__ == "__main__":
    list_gen_schemas()
