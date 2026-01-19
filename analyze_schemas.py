import sys
import yaml
import os
sys.path.insert(0, 'src')

from oas_importer.oas_parser import OASParser

source_file = r"C:\Users\giuse\.gemini\antigravity\scratch\OASIS\OAS Imports\EBACL_FPAD_20260116_OpenApi3.1_FPAD_API_Participant_5.0.7_v20260418.yaml"

# Find latest roundtrip directory
roundtrip_base = r"C:\Users\giuse\.gemini\antigravity\scratch\OASIS\Imported Templates\_roundtrip_history"
dirs = sorted([d for d in os.listdir(roundtrip_base) if d.startswith('202')])
latest_dir = dirs[-1]
generated_file = os.path.join(roundtrip_base, latest_dir, "generated_oas_3.1.yaml")

print(f"Using latest roundtrip: {latest_dir}\n")

source_oas = OASParser(source_file).oas
gen_oas = OASParser(generated_file).oas

src_schemas = source_oas.get('components', {}).get('schemas', {})
gen_schemas = gen_oas.get('components', {}).get('schemas', {})

def count_yaml_lines(obj):
    if not obj:
        return 0
    return len(yaml.dump(obj, default_flow_style=False, sort_keys=False).strip().split('\n'))

print("=== SCHEMAS LINE COUNT COMPARISON ===\n")
print(f"{'Schema Name':<50} | {'Source':<10} | {'Generated':<10} | {'Delta':<10}")
print("-" * 90)

schema_deltas = []
for schema_name in sorted(set(list(src_schemas.keys()) + list(gen_schemas.keys()))):
    src_lines = count_yaml_lines(src_schemas.get(schema_name, {}))
    gen_lines = count_yaml_lines(gen_schemas.get(schema_name, {}))
    delta = gen_lines - src_lines
    
    if delta != 0:
        schema_deltas.append((schema_name, src_lines, gen_lines, delta))

# Sort by absolute delta
schema_deltas.sort(key=lambda x: abs(x[3]), reverse=True)

# Show top 20 discrepancies
for schema_name, src, gen, delta in schema_deltas[:20]:
    delta_str = f"+{delta}" if delta > 0 else str(delta)
    display_name = schema_name if len(schema_name) <= 50 else schema_name[:47] + "..."
    print(f"{display_name:<50} | {src:<10} | {gen:<10} | {delta_str:<10}")

total_delta = sum([d for _,_,_,d in schema_deltas])
print(f"\n{'TOTAL DELTA':<50} | {'':<10} | {'':<10} | {total_delta:<10}")
print(f"\nTotal schemas with discrepancies: {len(schema_deltas)}")
