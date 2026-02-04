
import yaml

def find_specific_schema(schema_name):
    path = r"C:\Users\giuse\Downloads\EBACL_STEP2_20250507_Openapi3.1_SCT_API_Participants_2_1_v20251006.yaml"
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        target = f"{schema_name}:"
        idx = content.find(target)
        if idx != -1:
            print(f"--- {schema_name} ---")
            print(content[idx:idx+1000])
        else:
            print(f"Schema '{schema_name}' NOT found.")

if __name__ == "__main__":
    find_specific_schema('rejectParticipantOperationRequest')
    find_specific_schema('commandRef') # Let's see if it's a property anywhere
    find_specific_schema('operationRef')
