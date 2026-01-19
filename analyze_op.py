"""Analyze specific path difference in detail."""
import yaml

with open(r'Expected results\EBACL_FPAD_20251110_OpenApi3.1_FPAD_API_Participant_4.1_v20251212.yaml', 'r', encoding='utf-8') as f:
    gold = yaml.safe_load(f)
with open(r'Roundtrip_Output\generated_oas_3.1.yaml', 'r', encoding='utf-8') as f:
    gen = yaml.safe_load(f)

path = '/v1/accounts/assessments'
method = 'post'

gold_op = gold['paths'][path][method]
gen_op = gen['paths'][path][method]

# Compare each top level key
for key in set(gold_op.keys()) | set(gen_op.keys()):
    gold_yaml = yaml.dump(gold_op.get(key), default_flow_style=False)
    gen_yaml = yaml.dump(gen_op.get(key), default_flow_style=False)
    gold_lines = gold_yaml.count('\n')
    gen_lines = gen_yaml.count('\n')
    diff = gen_lines - gold_lines
    if diff != 0:
        print(f'{key}: gold={gold_lines}, gen={gen_lines}, diff={diff:+d}')
        
        # If it's description, show both
        if key == 'description':
            print(f'  GOLD: {repr(gold_op.get(key)[:100])}...')
            print(f'  GEN:  {repr(gen_op.get(key)[:100])}...')
