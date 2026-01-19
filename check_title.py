"""Check simple schemas for title differences."""
import yaml

with open(r'Expected results\EBACL_FPAD_20251110_OpenApi3.1_FPAD_API_Participant_4.1_v20251212.yaml', 'r', encoding='utf-8') as f:
    gold = yaml.safe_load(f)
with open(r'Roundtrip_Output\generated_oas_3.1.yaml', 'r', encoding='utf-8') as f:
    gen = yaml.safe_load(f)

for name in ['LEIType', 'Max500Text', 'FpadUniqueIdentifier']:
    print(f'=== {name} ===')
    print(f"Gold: {gold['components']['schemas'][name]}")
    print(f"Gen:  {gen['components']['schemas'][name]}")
    print()
