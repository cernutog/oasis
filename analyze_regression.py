import sys
sys.path.insert(0, 'src')

from oas_importer.oas_comparator import OASComparator
import os

source_file = r"C:\Users\giuse\.gemini\antigravity\scratch\OASIS\OAS Imports\EBACL_FPAD_20260116_OpenApi3.1_FPAD_API_Participant_5.0.7_v20260418.yaml"

# Find latest roundtrip
dirs = sorted([d for d in os.listdir(r'C:\Users\giuse\.gemini\antigravity\scratch\OASIS\Imported Templates\_roundtrip_history') if d.startswith('2026')])
latest = dirs[-1]
gen_file = rf'C:\Users\giuse\.gemini\antigravity\scratch\OASIS\Imported Templates\_roundtrip_history\{latest}\generated_oas_3.1.yaml'

print(f'Latest roundtrip: {latest}\n')

comp = OASComparator(source_file, gen_file)
bd = comp.get_detailed_structure_breakdown()

# Check schemas detail
if 'schemas_detail' in bd:
    print("=== TOP 15 SCHEMA CHANGES (worst first) ===\n")
    schemas = bd['schemas_detail']
    sorted_schemas = sorted(schemas.items(), key=lambda x: x[1][2])  # Sort by delta
    
    for name, (src_lines, gen_lines, delta) in sorted_schemas[:15]:
        print(f"{name:50s} {src_lines:4d} → {gen_lines:4d}  ({delta:+4d})")
    
    print(f"\n{'='*70}")
    print(f"Total schemas delta from breakdown: {sum(d for _,(_,_,d) in schemas.items())}")

# Check if Paths were modified
print("\n=== PATHS BREAKDOWN ===")
if 'paths_detail' in bd:
    paths = bd['paths_detail']
    print(f"Total paths with discrepancies: {len(paths)}")
    print("\nTop 10 path changes:")
    for path, (src, gen, delta) in sorted(paths.items(), key=lambda x: abs(x[1][2]), reverse=True)[:10]:
        print(f"  {path}: {src} → {gen} ({delta:+d})")
