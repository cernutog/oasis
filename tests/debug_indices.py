
import sys
import os
import pandas as pd

# Add project ROOT to sys.path
sys.path.append(os.getcwd())

from src import excel_parser as parser
from src.generator import OASGenerator

def test_debug_indices():
    base_dir = "C:/EBA Clearing/APIs/Templates/FPAD VOP for Responding PSP"
    index_path = os.path.join(base_dir, "$index.xlsx")
    
    df = pd.read_excel(index_path, sheet_name="Schemas")
    
    gen = OASGenerator(version="3.0.0")
    
    # We want to see how _build_schema_group behaves for indices 34, 35, 36
    # I'll manually run the logic of build_components but with prints
    
    # 1. Build nodes & Map (Replicating generator.py logic)
    nodes = {}
    last_seen = {}
    
    for idx, row in df.iterrows():
        name = gen._get_name(row)
        if pd.isna(name): continue
        name = str(name).strip()
        if not name: continue
        
        raw_parent = gen._get_parent(row)
        parent = str(raw_parent).strip() if pd.notna(raw_parent) and str(raw_parent).strip() else None
        
        parent_idx = last_seen.get(parent) if parent else None
        
        node = {
            "idx": idx,
            "name": name,
            "parent": parent,
            "parent_idx": parent_idx,
            "type": str(gen._get_type(row)).strip().lower() if pd.notna(gen._get_type(row)) else "",
            "schema_obj": gen._map_type_to_schema(row, is_node=True)
        }
        nodes[idx] = node
        last_seen[name] = idx
        
        if "PartyTypeExtended" in name or "name[" in name or "firstName" in name:
            print(f"Row {idx}: Name='{name}', Parent='{parent}', ParentIdx={parent_idx}")

    # Build children map
    children_map = {}
    for idx, node in nodes.items():
        p_idx = node.get("parent_idx")
        if p_idx is not None:
            if p_idx not in children_map:
                children_map[p_idx] = []
            children_map[p_idx].append(node)
            
    print("\n--- Children of 34 (name) ---")
    if 34 in children_map:
        for c in children_map[34]:
            print(f"  {c['name']} (idx {c['idx']}, type {c['type']})")
    else:
        print("  NONE")

    print("\n--- Children of 35 (name[0]) ---")
    if 35 in children_map:
        for c in children_map[35]:
            print(f"  {c['name']} (idx {c['idx']}, type {c['type']})")
    else:
        print("  NONE")

if __name__ == "__main__":
    test_debug_indices()
