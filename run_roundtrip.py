from src.oas_importer.oas_converter import OASToExcelConverter
from src.main import generate_oas
import shutil
import os

gold = r'OAS Imports\EBACL_FPAD_20260116_OpenApi3.1_FPAD_API_Participant_5.0.7_v20260418.yaml'

tpl_dir = 'Roundtrip_Templates'
out_dir = 'Roundtrip_Output'

# Clean and recreate directories
for d in [tpl_dir, out_dir]:
    if os.path.exists(d):
        shutil.rmtree(d)
    os.makedirs(d)

converter = OASToExcelConverter(gold)
converter.generate_index_file(os.path.join(tpl_dir, '$index.xlsx'))
converter.generate_all_endpoint_files(tpl_dir)

generate_oas(tpl_dir, gen_30=True, gen_31=True, gen_swift=False, output_dir=out_dir, log_callback=lambda x: None)

gold_lines = len(open(gold, 'r', encoding='utf-8').readlines())
gen_lines = len(open(os.path.join(out_dir, 'generated_oas_3.1.yaml'), 'r', encoding='utf-8').readlines())
print(f'Gold: {gold_lines}, Gen: {gen_lines}, Diff: {gen_lines - gold_lines:+d}')
