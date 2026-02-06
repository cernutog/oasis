
import pandas as pd
import os

def inspect_specific_schemas():
    path = "Templates Converted V3/$index.xlsx"
    if not os.path.exists(path):
        print("File not found.")
        return

    print(f"Loading {path}...")
    df = pd.read_excel(path, "Schemas", header=None)
    
    # Headers are likely row 0
    headers = df.iloc[0].to_list()
    print(f"Headers: {headers}")
    
    # Find rows for Alerts and AgendaDetails
    targets = ["Alerts", "alerts", "AgendaDetails", "Alerts.eventType"]
    
    for t in targets:
        # Search in column 0 (Name)
        # Note: Name is col 1 in Excel (0-indexed in pandas)
        # Parent is col 2 (1-indexed)
        matches = df[df[0] == t]
        if not matches.empty:
            print(f"\n--- Found {t} ---")
            for idx, row in matches.iterrows():
                # Extract key columns based on V3Writer mapping:
                # Name(0), Parent(1), Type(3), SchemaName(5)
                # (Indices shifted by -1 from Writer's 1-based indexing if read as header=None)
                # Writer: Name=1, Parent=2, Type=4, SchemaName=6
                # Pandas: Name=0, Parent=1, Type=3, Items=4, SchemaName=5
                print(f"Row {idx}: Name='{row[0]}', Parent='{row[1]}', Type='{row[3]}', ItemsRef='{row[4]}', SchemaRef='{row[5]}', Format='{row[6]}'")
        else:
            # Try searching just by name if it's a property (AgendaDetails.dailyThresholds)
            pass

    # Search for dailyThresholds property of AgendaDetails
    print("\n--- Searching for AgendaDetails properties ---")
    parent_matches = df[df[1] == "AgendaDetails"]
    if not parent_matches.empty:
        for idx, row in parent_matches.iterrows():
            print(f"Prop Row {idx}: Name='{row[0]}', Parent='{row[1]}', Type='{row[3]}', SchemaRef='{row[5]}'")

if __name__ == "__main__":
    inspect_specific_schemas()
