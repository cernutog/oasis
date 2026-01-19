"""Regenerate $index.xlsx with the fix applied."""
import os
import shutil
from src.oas_importer.oas_converter import OASToExcelConverter

# Source OAS
oas_path = 'Expected results/EBACL_FPAD_20251110_OpenApi3.1_FPAD_API_Participant_4.1_v20251212.yaml'

# Convert
c = OASToExcelConverter(oas_path)

# Generate to temp path first
temp_path = 'Imported Templates/temp_index.xlsx'
final_path = 'Imported Templates/$index.xlsx'

path = c.generate_index_file(temp_path)
print(f'Generated temp: {path}')

# Copy to final path (handles $ in filename better)
if os.path.exists(final_path):
    os.remove(final_path)
shutil.copy(temp_path, final_path)
os.remove(temp_path)
print(f'Moved to: {final_path}')
