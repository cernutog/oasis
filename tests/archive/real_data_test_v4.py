
import sys
import os
import pandas as pd

# Add project ROOT to sys.path
sys.path.append(os.getcwd())

from src import excel_parser as parser
from src.generator import OASGenerator

def test_node_linking():
    base_dir = "C:/EBA Clearing/APIs/Templates/FPAD VOP for Responding PSP"
    index_path = os.path.join(base_dir, "$index.xlsx")
    
    # 2. Parse Global Components (Schemas)
    # We want to see how _build_schema_group behaves
    df = pd.read_excel(index_path, sheet_name="Schemas")
    
    gen = OASGenerator(version="3.0.0")
    
    # Simulate build_components but with instrumentation
    # Actually, let's just use the real build_components and then inspect gen.oas
    components_data = parser.parse_components(index_path)
    gen.build_components(components_data)
    
    oas = gen.oas
    schemas = oas.get("components", {}).get("schemas", {})
    
    pt = schemas.get("PartyType", {})
    pte = schemas.get("PartyTypeExtended", {})
    
    print("\n--- PartyType Properties ---")
    print(list(pt.get("properties", {}).keys()))
    
    print("\n--- PartyType Identification ---")
    print(pt.get("properties", {}).get("identification", {}))
    
    print("\n--- PartyTypeExtended Properties ---")
    print(list(pte.get("properties", {}).keys()))
    
    print("\n--- PartyTypeExtended Identification ---")
    print(pte.get("properties", {}).get("identification", {}))

if __name__ == "__main__":
    test_node_linking()
