
import pandas as pd

def debug_parent_linking():
    xl = pd.ExcelFile("Output Legacy/$index.xlsx")
    df = xl.parse("Schemas")
    df.columns = df.columns.str.strip()
    
    name_col = "Name"
    parent_col = "Parent"
    
    # Simulate last_seen logic
    last_seen = {}
    
    for idx, row in df.iterrows():
        name = str(row[name_col]).strip() if pd.notna(row[name_col]) else ""
        parent = str(row[parent_col]).strip() if pd.notna(row[parent_col]) else ""
        
        if not name:
            continue
        
        # Determine parent_idx
        parent_idx = last_seen.get(parent) if parent else None
        
        # Check if it's an Operations child
        if parent.lower() == "operations":
            ops_root_idx = last_seen.get("Operations")
            print(f"Row {idx}: {name} with Parent='{parent}' -> parent_idx={parent_idx} (Operations root at idx {ops_root_idx})")
        
        # Update last_seen
        last_seen[name] = idx

if __name__ == "__main__":
    debug_parent_linking()
