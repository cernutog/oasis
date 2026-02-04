
import yaml

def check_reference_yaml():
    path = r"C:\Users\giuse\Downloads\EBACL_STEP2_20250507_Openapi3.1_SCT_API_Participants_2_1_v20251006.yaml"
    with open(path, 'r', encoding='utf-8') as f:
        # Read the first 500 lines to see schemas and properties
        for i in range(500):
            line = f.readline()
            if not line: break
            print(line.rstrip())

if __name__ == "__main__":
    check_reference_yaml()
