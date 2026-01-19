"""Analyze line differences between gold master and generated OAS."""
import yaml

# Load both files
with open(r'Expected results\EBACL_FPAD_20251110_OpenApi3.1_FPAD_API_Participant_4.1_v20251212.yaml', 'r', encoding='utf-8') as f:
    gold = yaml.safe_load(f)
with open(r'Roundtrip_Output\generated_oas_3.1.yaml', 'r', encoding='utf-8') as f:
    gen = yaml.safe_load(f)

# Count lines per section by re-dumping each section
def count_section_lines(data, key):
    if key not in data:
        return 0
    section_yaml = yaml.dump({key: data[key]}, default_flow_style=False, allow_unicode=True)
    return section_yaml.count('\n')

print('Section line counts:')
print(f'{"Section":<25} {"Gold":>8} {"Gen":>8} {"Diff":>8}')
print('-' * 50)

sections = ['openapi', 'info', 'servers', 'tags', 'security', 'paths', 'components']
for section in sections:
    gold_lines = count_section_lines(gold, section)
    gen_lines = count_section_lines(gen, section)
    diff = gen_lines - gold_lines
    print(f'{section:<25} {gold_lines:>8} {gen_lines:>8} {diff:>+8}')

# Deep dive into components
print('\nComponents breakdown:')
for comp in ['parameters', 'headers', 'schemas', 'responses']:
    gold_comp = gold.get('components', {}).get(comp, {})
    gen_comp = gen.get('components', {}).get(comp, {})
    gold_lines = yaml.dump(gold_comp, default_flow_style=False, allow_unicode=True).count('\n')
    gen_lines = yaml.dump(gen_comp, default_flow_style=False, allow_unicode=True).count('\n')
    diff = gen_lines - gold_lines
    print(f'  {comp:<23} {gold_lines:>8} {gen_lines:>8} {diff:>+8}')
