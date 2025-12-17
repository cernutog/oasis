
import pandas as pd
import os
from src.parser import find_best_match_file

# Simulate finding the file
target_name = "account_assessment_vop_bulk"
files = os.listdir("API Templates")
matched = find_best_match_file(target_name, "API Templates", files)
print(f"Matched File: {matched}")

if matched:
    sheet = "Body" # or whatever the schema definition sheet is. Usually 'Body' for request or '200' etc logic. 
    # But usually components are defined in 'Body' if it's the main request body, OR implicitly in responses.
    
    # Wait, where is VopBulkResponse defined? It might be a response schema.
    # Let's check '200' sheet of that file.
    
    
    # Dump 201 sheet of matched file
    try:
         df = pd.read_excel(matched, sheet_name="201")
         print(f"\n--- Sheet: 201 (First 20 rows) ---")
         print(df.head(20).to_string())
    except: pass

    # Also check the other file
    other_file = "API Templates/account_assessment_vop_bulk_{bulkId}.251111.xlsm"
    try:
         df = pd.read_excel(other_file, sheet_name="200") # check 200 here?
         print(f"\n--- Other File 200 Sheet ---")
         print(df.head(20).to_string())
    except:
         try:
             df = pd.read_excel(other_file, sheet_name="201") 
             print(f"\n--- Other File 201 Sheet ---")
             print(df.head(20).to_string())
         except: pass
