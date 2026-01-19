from src.oas_importer.oas_converter import OASToExcelConverter
import os

OAS_FILE = 'Expected results/EBACL_FPAD_20251110_OpenApi3.1_FPAD_API_Participant_4.1_v20251212.yaml'
OUTPUT_DIR = 'Imported Templates'

print(f"Initializing Converter with {OAS_FILE}...")
converter = OASToExcelConverter(OAS_FILE)

print("Generating Endpoint Files...")
files = converter.generate_all_endpoint_files(OUTPUT_DIR)
for f in files:
    print(f"Generated: {f}")

print("Generating Index File...")
converter.generate_index_file(os.path.join(OUTPUT_DIR, '$index.xlsx'))
print("Done.")
