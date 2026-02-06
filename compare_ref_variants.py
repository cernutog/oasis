
import yaml

def compare_base_vs_variant():
    ref_path = r"C:\Users\giuse\Downloads\EBACL_STEP2_20250507_Openapi3.1_CGS-DKK_API_Participants_2_0_v20251006.yaml"
    pairs = [
        ("Boolean", "Boolean1"),
        ("DailyThresholds", "DailyThresholds1"),
        ("DefaultDailyThresholds", "DefaultDailyThresholds1"),
        ("ExceptionLacValues", "ExceptionLacValues1"),
        ("LacAgenda", "LacAgenda1"),
        ("LacDefaultAgenda", "LacDefaultAgenda1"),
        ("Number", "Number1"),
        ("SenderBIC", "SenderBIC1")
    ]
    
    with open(ref_path, 'r', encoding='utf-8') as f:
        spec = yaml.safe_load(f)
        
    schemas = spec.get('components', {}).get('schemas', {})
    for base, variant in pairs:
        print(f"=== {base} vs {variant} ===")
        if base in schemas:
            print(f"[{base}]:\n{yaml.dump(schemas[base])}")
        else:
            print(f"[{base}]: NOT FOUND")
            
        if variant in schemas:
            print(f"[{variant}]:\n{yaml.dump(schemas[variant])}")
        else:
            print(f"[{variant}]: NOT FOUND")
        print("-" * 20)

if __name__ == "__main__":
    compare_base_vs_variant()
