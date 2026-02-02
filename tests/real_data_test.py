
import sys
import os
import json
import pandas as pd
from src.generator import OASGenerator
from src.excel_parser import ExcelParser

def test_real_data():
    index_path = "C:/EBA Clearing/APIs/Templates/FPAD VOP for Responding PSP/$index.xlsx"
    template_dir = "C:/EBA Clearing/APIs/Templates/FPAD VOP for Responding PSP"
    
    print(f"Loading Index: {index_path}")
    parser = ExcelParser(index_path, template_dir)
    
    # 1. Parse Index
    info_data = parser.parse_info()
    paths_list = parser.parse_paths()
    
    # 2. Parse Operations
    ops_details = {}
    for op in paths_list:
        file_ref = op.get("file")
        if file_ref:
            print(f"Parsing Operation File: {file_ref}")
            ops_details[file_ref] = parser.parse_operation_file(file_ref)
            
    # 3. Parse Global Components (Schemas)
    global_components = parser.parse_global_components()
    
    # 4. Generate
    gen = OASGenerator(version="3.0.0") # User preference says True for both 3.0 and 3.1
    gen.build_info(info_data)
    gen.build_paths(paths_list, ops_details)
    gen.build_components(global_components)
    
    yaml_out = gen.get_yaml()
    
    # Save for inspection
    with open("repro_real_data.yaml", "w", encoding="utf-8") as f:
        f.write(yaml_out)
        
    print("\nGeneration complete. Saved to repro_real_data.yaml")
    
    # Search for PartyType
    if "PartyType:" in yaml_out:
        print("\nFound PartyType in output.")
        # Find the block for PartyType and see if properties is there
        lines = yaml_out.splitlines()
        for i, line in enumerate(lines):
            if "PartyType:" in line:
                print(f"PartyType definition starts at line {i+1}:")
                for j in range(i, min(i+20, len(lines))):
                    print(lines[j])
                break
    else:
        print("\nPartyType NOT found in output.")

if __name__ == "__main__":
    test_real_data()
