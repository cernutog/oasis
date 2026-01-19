"""Regenerate all imported templates with the fixed converter."""
import os
import shutil
from src.oas_importer.oas_converter import OASToExcelConverter

# Source OAS
oas_path = 'Expected results/EBACL_FPAD_20251110_OpenApi3.1_FPAD_API_Participant_4.1_v20251212.yaml'
output_dir = 'Imported Templates'

# Backup existing files
backup_dir = 'Imported Templates_backup'
if os.path.exists(backup_dir):
    shutil.rmtree(backup_dir)
shutil.copytree(output_dir, backup_dir)
print(f"Backed up to: {backup_dir}")

# Remove old generated files (except generated folder)
for f in os.listdir(output_dir):
    fp = os.path.join(output_dir, f)
    if os.path.isfile(fp) and f.endswith('.xlsx'):
        os.remove(fp)
        print(f"Removed: {f}")

# Convert
c = OASToExcelConverter(oas_path)

# Generate index file
temp_path = os.path.join(output_dir, 'temp_index.xlsx')
final_path = os.path.join(output_dir, '$index.xlsx')
c.generate_index_file(temp_path)
if os.path.exists(final_path):
    os.remove(final_path)
shutil.move(temp_path, final_path)
print(f"Generated: $index.xlsx")

# Generate all endpoint files
endpoints = c.generate_all_endpoint_files(output_dir)
print(f"Generated {len(endpoints)} endpoint files")
for ep in endpoints:
    print(f"  - {os.path.basename(ep)}")

print("\nDone!")
