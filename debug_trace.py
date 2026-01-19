"""Debug script to trace where description is lost."""
import os
import pandas as pd
from src import excel_parser as parser
from src.generator import OASGenerator
from src.generator_pkg import schema_builder

# Load data
index_path = os.path.join('Imported Templates', '$index.xlsx')
components_data = parser.parse_components(index_path)
df_schemas = components_data['schemas']

print("Columns in schemas DataFrame:", df_schemas.columns.tolist())
print()

# Find debtorBic rows
rows = df_schemas[df_schemas['Name'] == 'debtorBic']
print(f"Found {len(rows)} 'debtorBic' rows:")
for idx, row in rows.iterrows():
    parent = row.get('Parent', 'N/A')
    desc_raw = row.get('Description', 'N/A')
    print(f"  Row {idx}: Parent={parent}")
    print(f"    Description in DF: {str(desc_raw)[:50] if pd.notna(desc_raw) else 'NaN/None'}")
    
    # Test get_description helper
    desc_helper = schema_builder.get_description(row)
    print(f"    get_description(): {str(desc_helper)[:50] if pd.notna(desc_helper) else 'NaN/None'}")
    print()

# Now test with the exact flow from _build_schema_group
print("\n--- Testing _build_schema_group flow ---")
gen = OASGenerator(version='3.1.0')

# Simulate what _build_schema_group does
for idx, row in df_schemas.iterrows():
    name = gen._get_name(row)
    if name != 'debtorBic':
        continue
    
    parent = gen._get_parent(row)
    if parent != 'InvestigationTransactionData':
        continue
        
    print(f"Processing row {idx}: name={name}, parent={parent}")
    
    # What _build_schema_group does:
    desc_from_generator = gen._get_description(row)
    print(f"  gen._get_description(): {str(desc_from_generator)[:50] if pd.notna(desc_from_generator) else 'NaN/None'}")
    
    # What map_type_to_schema receives
    schema_obj = gen._map_type_to_schema(row, is_node=True)
    print(f"  _map_type_to_schema result: {schema_obj}")
    break
