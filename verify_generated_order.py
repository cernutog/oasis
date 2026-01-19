import yaml
import os

files = ['Roundtrip_Output/generated_oas_3.1.yaml', 'Roundtrip_Output/generated_oas_3.0.yaml']

for f_path in files:
    if not os.path.exists(f_path):
        print(f"Skipping {f_path} (not found)")
        continue

    print(f"Checking {f_path}...")
    with open(f_path, 'r', encoding='utf-8') as f:
        oas = yaml.safe_load(f)
    
    schema = oas['components']['schemas'].get('InvestigationTransactionData', {})
    
    example_data = None
    if 'examples' in schema and schema['examples']:
        print("  Found 'examples' (array)")
        example_data = schema['examples'][0]
    elif 'example' in schema:
        print("  Found 'example' (singular)")
        example_data = schema['example']
    else:
        print("  NO EXAMPLE FOUND!")
        continue

    # Identify keys order from the file content directly because yaml.safe_load might reshuffle dict keys in older python versions,
    # though 3.7+ preserves insertion order.
    # To be absolutely sure about the FILE content order, we can grep the file or rely on Python 3.7+ dict order.
    # Since we are in Python 3.13 environment, dict order is preserved.
    
    if isinstance(example_data, dict):
        keys = list(example_data.keys())
        print(f"  First 5 keys: {keys[:5]}")
        
        expected_start = ['serviceType', 'instructingAgentBic', 'instructedAgentBic']
        if keys[:3] == expected_start:
             print("  SUCCESS: Order matches Gold OAS.")
        else:
             print("  FAILURE: Order does NOT match Gold OAS.")
    else:
        print(f"  Example data is not a dict: {type(example_data)}")
