
import yaml

def check_gold_example():
    path = r"OAS Imports\EBACL_FPAD_20260116_OpenApi3.1_FPAD_API_Participant_5.0.7_v20260418.yaml"
    try:
        with open(path, 'r', encoding='utf-8') as f:
            oas = yaml.safe_load(f)
            
        target_path = '/v1/insight-notifications/accounts/search'
        if target_path in oas['paths']:
            post = oas['paths'][target_path]['post']
            resp = post['responses']['200']
            content = resp['content']['application/json']
            
            print(f"Has 'example'? {'example' in content}")
            print(f"Has 'examples'? {'examples' in content}")
            
            if 'example' in content:
                ex = content['example']
                print(f"Singular example type: {type(ex)}")
                if isinstance(ex, dict):
                     print(f"Singular example keys: {list(ex.keys())}")
            
            if 'examples' in content:
                exs = content['examples']
                print(f"Plural examples keys: {list(exs.keys())}")
                if 'OK' in exs:
                    ok_ex = exs['OK']
                    print(f"OK example type: {type(ok_ex)}")
                    if isinstance(ok_ex, dict):
                         print(f"OK example keys: {list(ok_ex.keys())}")
                         if 'value' in ok_ex:
                             val = ok_ex['value']
                             print("Found 'value' key!")
                             
                             # Search for labels
                             found_labels = False
                             def find_labels(obj, path=""):
                                 nonlocal found_labels
                                 if isinstance(obj, dict):
                                     for k, v in obj.items():
                                         if k == 'labels':
                                             print(f"Found labels in Gold at {path}.{k}: {v}")
                                             found_labels = True
                                         find_labels(v, f"{path}.{k}")
                                 elif isinstance(obj, list):
                                     for i, item in enumerate(obj):
                                         find_labels(item, f"{path}[{i}]")
                             
                             find_labels(val)
                             if not found_labels:
                                 print("Labels NOT found in Gold example value.")

                         else:
                             print("NO 'value' key found.")
                
        else:
            print("Path not found")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_gold_example()
