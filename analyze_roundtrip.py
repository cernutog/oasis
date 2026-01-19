import sys
import os

# Add src to path
sys.path.insert(0, 'src')

from oas_importer.oas_comparator import OASComparator

# Files from latest roundtrip (from screenshot)
source_file = r"C:\Users\giuse\.gemini\antigravity\scratch\OASIS\OAS Imports\EBACL_FPAD_20260116_OpenApi3.1_FPAD_API_Participant_5.0_v20260418.yaml"
generated_file = r"C:\Users\giuse\.gemini\antigravity\scratch\OASIS\Imported Templates\_roundtrip_history\20260118_182323\generated_oas_3.1.yaml"

print("=== ROUNDTRIP ANALYSIS ===\n")
print(f"Source: {os.path.basename(source_file)}")
print(f"Generated: {os.path.basename(generated_file)}")

# Check files exist
if not os.path.exists(source_file):
    print(f"\nERROR: Source file not found")
    # Try to find it
    import glob
    matches = glob.glob(r"C:\Users\giuse\.gemini\antigravity\scratch\OASIS\**\*EBACL_FPAD*.yaml", recursive=True)
    if matches:
        print(f"Found potential source files:")
        for m in matches:
            print(f"  {m}")
        source_file = matches[0]
        print(f"\nUsing: {source_file}")
    else:
        sys.exit(1)

if not os.path.exists(generated_file):
    print(f"\nERROR: Generated file not found: {generated_file}")
    sys.exit(1)

# Create comparator
comp = OASComparator(source_file, generated_file)

# Get detailed breakdown
breakdown = comp.get_detailed_structure_breakdown()

print("\n\n=== COMPONENTS BREAKDOWN ===")
print(f"{'Subsection':<30} | {'Source':<10} | {'Generated':<10} | {'Delta':<10}")
print("-" * 70)

total_comp_delta = 0
for subsection, (src, gen, delta) in sorted(breakdown['components'].items()):
    delta_str = f"+{delta}" if delta > 0 else str(delta)
    print(f"{subsection:<30} | {src:<10} | {gen:<10} | {delta_str:<10}")
    total_comp_delta += delta

print(f"\n{'TOTAL COMPONENTS':<30} | {'':<10} | {'':<10} | {total_comp_delta:<10}")

print("\n\n=== PATHS BREAKDOWN (Top Discrepancies) ===")
print(f"{'Path':<60} | {'Source':<10} | {'Generated':<10} | {'Delta':<10}")
print("-" * 100)

total_paths_delta = 0
for i, (path_name, src, gen, delta) in enumerate(breakdown['paths'][:20], 1):
    delta_str = f"+{delta}" if delta > 0 else str(delta)
    display_path = path_name if len(path_name) <= 60 else path_name[:57] + "..."
    print(f"{display_path:<60} | {src:<10} | {gen:<10} | {delta_str:<10}")
    total_paths_delta += delta

print(f"\n{'TOTAL TOP 20 PATHS':<60} | {'':<10} | {'':<10} | {total_paths_delta:<10}")

# Get line comparison
line_comp = comp.get_line_comparison()
if 'Total Lines' in line_comp:
    src_lines, gen_lines = line_comp['Total Lines']
    print(f"\n\n=== TOTAL FILE LINE COUNT ===")
    print(f"Source Lines: {src_lines}")
    print(f"Generated Lines: {gen_lines}")
    print(f"Delta: {gen_lines - src_lines}")
