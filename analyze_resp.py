"""Analyze response differences in a specific operation."""
import yaml

with open(r'Expected results\EBACL_FPAD_20251110_OpenApi3.1_FPAD_API_Participant_4.1_v20251212.yaml', 'r', encoding='utf-8') as f:
    gold = yaml.safe_load(f)
with open(r'Roundtrip_Output\generated_oas_3.1.yaml', 'r', encoding='utf-8') as f:
    gen = yaml.safe_load(f)

path = '/v1/accounts/assessments/vop'
method = 'post'

gold_responses = gold['paths'][path][method]['responses']
gen_responses = gen['paths'][path][method]['responses']

print('Response code differences:')
for code in sorted(set(gold_responses.keys()) | set(gen_responses.keys())):
    gold_val = yaml.dump(gold_responses.get(code, {}), default_flow_style=False).count('\n')
    gen_val = yaml.dump(gen_responses.get(code, {}), default_flow_style=False).count('\n')
    diff = gen_val - gold_val
    if diff != 0:
        print(f'  {code}: gold={gold_val}, gen={gen_val}, diff={diff:+d}')
        # Show what's different
        gold_resp = gold_responses.get(code, {})
        gen_resp = gen_responses.get(code, {})
        # If it's a $ref, just show it
        if '$ref' in gold_resp or '$ref' in gen_resp:
            print(f'    Gold: {gold_resp}')
            print(f'    Gen:  {gen_resp}')
        else:
            for key in set(gold_resp.keys()) | set(gen_resp.keys()):
                g = yaml.dump(gold_resp.get(key), default_flow_style=False).count('\n') if key in gold_resp else 0
                n = yaml.dump(gen_resp.get(key), default_flow_style=False).count('\n') if key in gen_resp else 0
                if g != n:
                    print(f'    {key}: gold={g}, gen={n}')
