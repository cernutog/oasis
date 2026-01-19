
import os
import sys
import openpyxl

# Add root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src import excel_parser as parser
from src.generator import OASGenerator
from src.oas_importer.oas_converter import OASToExcelConverter

def run_roundtrip_verification():
    print("=== STARTING FULL ROUND-TRIP VERIFICATION ===")
    
    # --- PHASE 1: GENERATION (Excel -> OAS) ---
    print("\n[Phase 1] Generating OAS from 'API Templates'...")
    templates_dir = 'API Templates'
    index_path = os.path.join(templates_dir, chr(36) + 'index.xlsm')
    
    if not os.path.exists(index_path):
        print(f"Error: Templates not found at {index_path}")
        return

    # Load and Parse
    try:
        print("Loading Excel templates...")
        df_paths = parser.load_excel_sheet(index_path, 'Paths')
        paths = parser.parse_paths_index(df_paths)
        
        # Load General Description (needed for valid OAS)
        df_info = parser.load_excel_sheet(index_path, 'General Description')
        info, servers = parser.parse_info(df_info)

        ops_details = {}
        for p in paths:
            filename = p.get('file')
            if filename:
                filepath = os.path.join(templates_dir, filename)
                if os.path.exists(filepath):
                    try:
                        ops_details[filename] = parser.parse_operation_file(filepath)
                    except:
                        pass
        
        # Build OAS
        print("Building OAS structure...")
        gen = OASGenerator('3.1.0')
        gen.build_info(info)
        
        # Tags & Servers
        if servers:
            gen.oas['servers'] = servers
            
        df_tags = parser.load_excel_sheet(index_path, 'Tags')
        if df_tags is not None:
            tags = parser.parse_tags(df_tags)
            if tags:
                gen.oas['tags'] = tags
                
        # Components (Schemas, Parameters, etc.)
        print("Parsing Components...")
        components = parser.parse_components(index_path)
        gen.build_components(components, source_file=index_path)
        
        gen.build_paths(paths, ops_details)
        
        yaml_content = gen.get_yaml()
        
        # Save to temp file
        temp_oas_file = "temp_verification_oas.yaml"
        with open(temp_oas_file, 'w', encoding='utf-8') as f:
            f.write(yaml_content)
            
        print(f"OAS generated and saved to: {temp_oas_file}")
        
    except Exception as e:
        print(f"Phase 1 Failed: {e}")
        import traceback
        traceback.print_exc()
        return

    # --- PHASE 2: IMPORT (OAS -> Excel) ---
    print("\n[Phase 2] Importing back to Excel...")
    output_dir = "Imported Templates"
    os.makedirs(output_dir, exist_ok=True)
    output_index_path = os.path.join(output_dir, chr(36) + "index.xlsx")
    
    try:
        if os.path.exists(output_index_path):
            os.remove(output_index_path)
            
        converter = OASToExcelConverter(temp_oas_file)
        converter.generate_index_file(output_index_path)
        print(f"Imported index saved to: {output_index_path}")
        
    except Exception as e:
        print(f"Phase 2 Failed: {e}")
        import traceback
        traceback.print_exc()
        return

    # --- PHASE 3: VERIFICATION ---
    print("\n[Phase 3] Verifying Content...")
    try:
        wb = openpyxl.load_workbook(output_index_path)
        ws = wb['Paths']
        
        target_path = "/v1/accounts/assessments/vop/bulk/{bulkId}"
        found = False
        
        for row in ws.iter_rows(min_row=3, values_only=True):
            path = row[1]
            if path == target_path:
                found = True
                ext_text = row[8]
                print(f"Found Target Path: {path}")
                
                if not ext_text:
                    print("FAILURE: Extension text is empty.")
                    # Debug
                    print(f"DEBUG: op.path={path}")
                    # Try manual extraction with lowercase
                    try:
                        debug_ext = converter.parser.get_raw_extensions(path, 'get')
                        print(f"DEBUG: Manual extract with 'get': len={len(debug_ext)}")
                        debug_ext_upper = converter.parser.get_raw_extensions(path, 'GET')
                        print(f"DEBUG: Manual extract with 'GET': len={len(debug_ext_upper)}")
                    except:
                        pass
                    return

                # 1. Content Completeness Check (7 status codes)
                status_codes = ['400', '401', '403', '404', '409', '429', '500']
                found_codes = []
                for code in status_codes:
                    if f"'{code}':" in ext_text or f"{code}:" in ext_text:
                        found_codes.append(code)
                
                print(f"Status codes found: {len(found_codes)}/7")
                if len(found_codes) == 7:
                    print("CHECK PASSED: All 7 status codes present.")
                else:
                    print(f"CHECK FAILED: Missing codes: {set(status_codes) - set(found_codes)}")

                # 2. Indentation Check
                lines = ext_text.split('\n')
                
                # Header line (should be column 0)
                if lines[0].strip().startswith('x-sandbox-rule-type') and not lines[0].startswith(' '):
                    print("CHECK PASSED: Header indentation is 0.")
                else:
                    print(f"CHECK FAILED: Header indentation invalid. Line: {repr(lines[0])}")

                # Content block header
                # Should be line 1 usually: x-sandbox-rule-content: |
                content_header = next((l for l in lines if 'x-sandbox-rule-content' in l), None)
                if content_header and not content_header.startswith(' '):
                    print("CHECK PASSED: Content header indentation is 0.")
                else:
                    print(f"CHECK FAILED: Content header invalid. Line: {repr(content_header)}")
                    
                # Content body (JS)
                # Should be 2 spaces indentation
                body_line = next((l for l in lines if 'var responseName' in l), None)
                if body_line:
                    indent = len(body_line) - len(body_line.lstrip())
                    if indent == 2:
                        print("CHECK PASSED: JS Body indentation is 2 spaces.")
                    else:
                        print(f"CHECK FAILED: JS Body indentation is {indent} (expected 2).")
                else:
                     print("WARNING: Could not find JS body line to check indent.")

                break
        
        if not found:
            print(f"FAILURE: Target path {target_path} not found in generated Excel.")
            
    except Exception as e:
        print(f"Phase 3 Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_roundtrip_verification()
