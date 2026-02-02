
import sys
import os
import pandas as pd

# Add src to sys.path for absolute imports to work correctly
sys.path.append(os.path.abspath("src"))

import excel_parser as parser
from generator import OASGenerator

def test_real_data():
    base_dir = "C:/EBA Clearing/APIs/Templates/FPAD VOP for Responding PSP"
    index_path = os.path.join(base_dir, "$index.xlsx")
    
    if not os.path.exists(index_path):
        print(f"Error: {index_path} not found.")
        return

    print(f"Loading Index: {index_path}")
    
    # 2. Parse Master Index (Following main.py logic)
    df_info = parser.load_excel_sheet(index_path, "General Description")
    info_data, inline_servers = parser.parse_info(df_info)

    df_paths = parser.load_excel_sheet(index_path, "Paths")
    paths_list = parser.parse_paths_index(df_paths)

    components_data = parser.parse_components(index_path)  # Global components (Schemas)
    
    # 3. Parse Operation Files
    files_in_dir = os.listdir(base_dir)
    operations_details = {}
    unique_files = set(op.get("file") for op in paths_list if op.get("file"))

    for raw_file_name in unique_files:
        full_path = parser.find_best_match_file(raw_file_name, base_dir, files_in_dir)
        if full_path:
            op_det = parser.parse_operation_file(full_path)
            if op_det:
                operations_details[raw_file_name] = op_det
    
    # 4. Generate
    gen = OASGenerator(version="3.0.0")
    gen.build_info(info_data)
    gen.build_paths(paths_list, operations_details)
    gen.build_components(components_data)
    
    yaml_out = gen.get_yaml()
    
    # Save for inspection
    with open("repro_real_data.yaml", "w", encoding="utf-8") as f:
        f.write(yaml_out)
        
    print("\nGeneration complete. Saved to repro_real_data.yaml")
    
    # Search for PartyType
    if "PartyType:" in yaml_out:
        print("\nFound PartyType in output.")
        lines = yaml_out.splitlines()
        found = False
        for i, line in enumerate(lines):
            if "  PartyType:" in line: # Usually indented under schemas
                found = True
                print(f"PartyType definition starts at line {i+1}:")
                # Print until next top-level component or next schema at same level
                limit = i + 30
                for j in range(i, min(limit, len(lines))):
                    print(lines[j])
                    if j > i and lines[j].startswith("    ") and not lines[j].startswith("      "):
                        # Stop if we hit another schema at the same indentation level
                         if ":" in lines[j] and not lines[j].strip().startswith("-"):
                             break
                break
        if not found:
             print("PartyType block not found (indented). Searching for literal 'PartyType:'...")
             for i, line in enumerate(lines):
                if "PartyType:" in line:
                    print(f"Found at line {i+1}: {line}")
    else:
        print("\nPartyType NOT found in output.")

if __name__ == "__main__":
    test_real_data()
