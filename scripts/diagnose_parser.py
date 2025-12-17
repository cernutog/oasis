import sys
import os
import pandas as pd

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import parser, generator

def debug_parser():
    file_name = "API Templates/account_assessment.251111.xlsm"
    print(f"Parsing {file_name}...")
    
    op_details = parser.parse_operation_file(file_name)
    
    if not op_details:
        print("Parser returned None/Empty")
        return
        
    print("Keys found:", op_details.keys())
    
    gen = generator.OASGenerator()
    
    if "body" in op_details:
        df = op_details["body"]
        print(f"\nBody DataFrame Shape: {df.shape if df is not None else 'None'}")
        if df is not None and not df.empty:
            print(df.head().to_string())
            print("\nColumns:", df.columns.tolist())
            
            print("\n--- Testing Generator _get_name ---")
            for idx, row in df.head().iterrows():
                name = gen._get_name(row)
                print(f"Row {idx}: Name='{name}' (Raw Name: {row.get('Name')}, Name.1: {row.get('Name.1')})")

if __name__ == "__main__":
    debug_parser()
