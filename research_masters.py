import pandas as pd
import os

master_index = r"Templates Master\$index.xlsx"
if os.path.exists(master_index):
    # Read without headers to see the layout
    df = pd.read_excel(master_index, sheet_name='Schemas', header=None)
    print("Schemas Layout (Row 1):", df.iloc[1].tolist())
    print("Schemas Layout (Row 2):", df.iloc[2].tolist())
    
    # Also check Paths in legacy again with more detail
    legacy_index = r"Templates Legacy\$index.xlsm"
    xl = pd.ExcelFile(legacy_index)
    df_paths = pd.read_excel(xl, "Paths", header=None)
    # Print row 0 and 1 to find headers
    print("Legacy Paths - Row 0:", df_paths.iloc[0].tolist())
    print("Legacy Paths - Row 1:", df_paths.iloc[1].tolist())
else:
    print("Master index not found at:", os.path.abspath(master_index))
