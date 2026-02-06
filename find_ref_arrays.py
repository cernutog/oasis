
import yaml

def find_array_schemas():
    path = r"C:\Users\giuse\Downloads\EBACL_STEP2_20250507_Openapi3.1_CGS-DKK_API_Participants_2_0_v20251006.yaml"
    with open(path, 'r', encoding='utf-8') as f:
        spec = yaml.safe_load(f)
    
    schemas = spec.get('components', {}).get('schemas', {})
    array_schemas = {k: v for k, v in schemas.items() if v.get('type') == 'array'}
    
    print(f"Total Array Schemas: {len(array_schemas)}")
    for k in sorted(array_schemas.keys()):
        print(f"- {k}: {array_schemas[k].get('items', {}).get('$ref', 'Inline/Scalar')}")

if __name__ == "__main__":
    find_array_schemas()
