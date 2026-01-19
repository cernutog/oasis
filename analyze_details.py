"""Analyze specific differences between gold master and generated OAS."""
import yaml

with open(r'Expected results\EBACL_FPAD_20251110_OpenApi3.1_FPAD_API_Participant_4.1_v20251212.yaml', 'r', encoding='utf-8') as f:
    gold = yaml.safe_load(f)
with open(r'Roundtrip_Output\generated_oas_3.1.yaml', 'r', encoding='utf-8') as f:
    gen = yaml.safe_load(f)

# 1. Security difference (-1)
print('=== SECURITY (-1 line) ===')
print(f'Gold: {gold.get("security")}')
print(f'Gen:  {gen.get("security")}')

# 2. Responses comparison (-12)
print('\n=== RESPONSES (-12 lines) ===')
gold_resp = gold.get('components', {}).get('responses', {})
gen_resp = gen.get('components', {}).get('responses', {})
print(f'Gold response count: {len(gold_resp)}')
print(f'Gen response count: {len(gen_resp)}')

# Which are different?
for name in gold_resp.keys():
    if name in gen_resp:
        gold_lines = yaml.dump(gold_resp[name], default_flow_style=False).count('\n')
        gen_lines = yaml.dump(gen_resp[name], default_flow_style=False).count('\n')
        if gold_lines != gen_lines:
            print(f'  {name}: gold={gold_lines}, gen={gen_lines}, diff={gen_lines-gold_lines:+d}')

# 3. Paths (+16)
print('\n=== PATHS (+16 lines) ===')
# Compare operation counts
gold_paths = gold.get('paths', {})
gen_paths = gen.get('paths', {})
print(f'Gold path count: {len(gold_paths)}')
print(f'Gen path count: {len(gen_paths)}')

# 4. Schemas (+35)
print('\n=== SCHEMAS (+35 lines) - top differences ===')
gold_schemas = gold.get('components', {}).get('schemas', {})
gen_schemas = gen.get('components', {}).get('schemas', {})
diffs = []
for name in set(gold_schemas.keys()) | set(gen_schemas.keys()):
    gold_lines = yaml.dump(gold_schemas.get(name, {}), default_flow_style=False).count('\n') if name in gold_schemas else 0
    gen_lines = yaml.dump(gen_schemas.get(name, {}), default_flow_style=False).count('\n') if name in gen_schemas else 0
    diff = gen_lines - gold_lines
    if diff != 0:
        diffs.append((name, gold_lines, gen_lines, diff))
diffs.sort(key=lambda x: abs(x[3]), reverse=True)
for name, g, n, d in diffs[:5]:
    print(f'  {name}: gold={g}, gen={n}, diff={d:+d}')
