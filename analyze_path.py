"""Analyze a specific path difference."""
import yaml

with open(r'Expected results\EBACL_FPAD_20251110_OpenApi3.1_FPAD_API_Participant_4.1_v20251212.yaml', 'r', encoding='utf-8') as f:
    gold = yaml.safe_load(f)
with open(r'Roundtrip_Output\generated_oas_3.1.yaml', 'r', encoding='utf-8') as f:
    gen = yaml.safe_load(f)

# Pick a path with +9 diff
path = '/v1/accounts/assessments/vop'
print(f'=== PATH: {path} ===')
print()

gold_path = gold['paths'][path]
gen_path = gen['paths'][path]

# Compare each method
for method in set(gold_path.keys()) | set(gen_path.keys()):
    if method.startswith('x-'):
        continue
    gold_method = gold_path.get(method, {})
    gen_method = gen_path.get(method, {})
    
    gold_lines = yaml.dump(gold_method, default_flow_style=False).count('\n')
    gen_lines = yaml.dump(gen_method, default_flow_style=False).count('\n')
    diff = gen_lines - gold_lines
    
    print(f'{method.upper()}: gold={gold_lines}, gen={gen_lines}, diff={diff:+d}')
    
    if diff != 0:
        # Find what's different
        for key in set(gold_method.keys()) | set(gen_method.keys()):
            gold_val = yaml.dump(gold_method.get(key), default_flow_style=False).count('\n') if key in gold_method else 0
            gen_val = yaml.dump(gen_method.get(key), default_flow_style=False).count('\n') if key in gen_method else 0
            if gold_val != gen_val:
                print(f'  {key}: gold={gold_val}, gen={gen_val}, diff={gen_val-gold_val:+d}')
