
import sys
import os
sys.path.append(os.getcwd())

from src.generator import OASGenerator
import pandas as pd

# Monkey patch to add debug prints
original_build_inline = OASGenerator._build_inline_alternative

def debug_build_inline(self, nodes, alt_node, children_map=None, parent_type=None):
    alt_name = alt_node.get("name", "UNKNOWN")
    alt_idx = alt_node.get("idx", "NO_IDX")
    
    if "name[" in alt_name:
        print(f"\n=== Building inline alternative: {alt_name} (idx={alt_idx}) ===")
        print(f"  alt_node keys: {list(alt_node.keys())}")
        print(f"  children_map provided: {children_map is not None}")
        
        if children_map and alt_idx != "NO_IDX":
            children = children_map.get(alt_idx, [])
            print(f"  Children found for idx {alt_idx}: {len(children)}")
            for c in children:
                print(f"    - {c['name']} (idx {c.get('idx', 'NO_IDX')})")
        else:
            print(f"  Cannot lookup children (no map or no idx)")
    
    result = original_build_inline(self, nodes, alt_node, children_map, parent_type)
    
    if "name[" in alt_name:
        print(f"  Result schema keys: {list(result.keys())}")
        if "properties" in result:
            print(f"  Properties: {list(result['properties'].keys())}")
    
    return result

OASGenerator._build_inline_alternative = debug_build_inline

# Now run the generation
base_dir = "C:/EBA Clearing/APIs/Templates/FPAD VOP for Responding PSP"
index_path = os.path.join(base_dir, "$index.xlsx")

df = pd.read_excel(index_path, sheet_name="Schemas")
gen = OASGenerator(version="3.0.0")

# Filter for PartyTypeExtended group
group_df = df[df.apply(lambda row: row.astype(str).str.contains("PartyTypeExtended|name\\[").any(), axis=1)]

print("Building schemas for PartyTypeExtended group...")
schemas = gen._build_schema_group(group_df)

print("\n\n=== FINAL PartyTypeExtended.name ===")
if "PartyTypeExtended" in schemas:
    name_prop = schemas["PartyTypeExtended"].get("properties", {}).get("name", {})
    print(f"Type: {name_prop.get('type', 'N/A')}")
    if "oneOf" in name_prop:
        print(f"OneOf alternatives: {len(name_prop['oneOf'])}")
        for i, alt in enumerate(name_prop['oneOf']):
            print(f"  [{i}]: {alt}")
