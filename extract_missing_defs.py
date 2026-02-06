
import yaml

def extract_missing_defs():
    ref_path = r"C:\Users\giuse\Downloads\EBACL_STEP2_20250507_Openapi3.1_CGS-DKK_API_Participants_2_0_v20251006.yaml"
    missing = [
        "Boolean1", "DailyThresholds1", "DefaultDailyThresholds1", 
        "ExceptionLacValues1", "LacAgenda1", "LacDefaultAgenda1", 
        "Number1", "SenderBIC1", "liquidityManagementRequest", "liquidityManagementResponse"
    ]
    
    with open(ref_path, 'r', encoding='utf-8') as f:
        spec = yaml.safe_load(f)
        
    schemas = spec.get('components', {}).get('schemas', {})
    for m in missing:
        if m in schemas:
            print(f"--- {m} ---")
            print(yaml.dump(schemas[m]))
        else:
            print(f"--- {m} NOT IN COMPONENTS/SCHEMAS ---")

if __name__ == "__main__":
    extract_missing_defs()
