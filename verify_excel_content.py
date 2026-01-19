import pandas as pd
import os
import yaml

# Find the index file
index_file = None
for f in os.listdir('Roundtrip_Templates'):
    if f.endswith('index.xlsx'):
        index_file = f
        break

if not index_file:
    print("Index file not found!")
    exit(1)

path = os.path.join('Roundtrip_Templates', index_file)
print(f"Reading {path}...")

# Hardcoded for debugging
filename = "search-account-insight-notifications.260118.xlsx"
file_path = os.path.join('Roundtrip_Templates', filename)

if True: # Skip index lookup
    if os.path.exists(file_path):

        print(f"Reading {file_path}...")
        # Inspect response 200 sheet
        try:
            # Read raw content
            resp_df = pd.read_excel(file_path, sheet_name='200', header=None) 
            
            print("Response Sheet Raw Head:")
            print(resp_df.head(10).to_string())
            
            # Find header row
            header_row_idx = None
            for idx, row in resp_df.iterrows():
                row_str = row.astype(str).tolist()
                if 'Name' in row_str and 'Example' in row_str:
                    header_row_idx = idx
                    print(f"Header found at row {idx}")
                    break
            
            if header_row_idx is not None:
                # Reload with header
                resp_df = pd.read_excel(file_path, sheet_name='200', header=header_row_idx)
                
                # Check for 'value' in Name column
                name_col = next((c for c in resp_df.columns if 'Name' in str(c)), None)
                ex_col = next((c for c in resp_df.columns if 'Example' in str(c)), None)
                
                if name_col:
                     print(f"Searching 'value' in col '{name_col}'")
                     value_rows = resp_df[resp_df[name_col] == 'value']
                     if not value_rows.empty:
                         print("\nRow 'value' FOUND:")
                         print(value_rows)
                         if ex_col:
                             val = value_rows[ex_col].values[0]
                             print("\nExample content:")
                             print(val)
                             print(f"Type: {type(val)}")
                         else:
                             print("Example column not found.")
                     else:
                         print("Row 'value' NOT FOUND.")
            else:
                print("Header row not found.")

            
        except Exception as e:
            print(f"Error reading sheet 200: {e}")
    else:
        print(f"File {file_path} does not exist!")
else:
    print("Path not found in index.")

