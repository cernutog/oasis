import yaml

GOLDEN_PATH = "Expected results/EBACL_FPAD_20251110_OpenApi3.1_FPAD_API_Participant_4.1_v20251212.yaml"
def check_keys():
    with open(GOLDEN_PATH, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    schemas = data.get("components", {}).get("schemas", {})
    
    print(f"Total Schemas: {len(schemas)}")
    if "identification" in schemas:
        print("YES: 'identification' is a Root Schema.")
    else:
        print("NO: 'identification' is NOT a Root Schema.")
        
    if "DateTime" in schemas:
        print("YES: 'DateTime' is a Root Schema.")
    else:
        print("NO: 'DateTime' is NOT a Root Schema.")

    if "name" in schemas:
        print("YES: 'name' is a Root Schema.")
    else:
        print("NO: 'name' is NOT a Root Schema.")

if __name__ == "__main__":
    check_keys()
