
import yaml

def check_schemas_section():
    path = r"C:\Users\giuse\Downloads\EBACL_STEP2_20250507_Openapi3.1_SCT_API_Participants_2_1_v20251006.yaml"
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        schemas_start = content.find('schemas:')
        if schemas_start != -1:
            # Print the next 10000 characters from 'schemas:'
            print(content[schemas_start:schemas_start+10000])
        else:
            print("'schemas:' section not found.")

if __name__ == "__main__":
    check_schemas_section()
