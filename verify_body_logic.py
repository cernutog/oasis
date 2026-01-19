import pandas as pd
import json
from src.generator import OASGenerator
from src.generator_pkg.row_helpers import (
    get_col_value, get_type, get_name, get_parent, get_description, get_schema_name, parse_example_string
)
from src.generator_pkg import response_builder

# Verify that generator can handle implicit vs explicit body rows
# Explicit: has a row for 'application/json' (content type)
# Implicit: no content type row, just fields

def test_body_logic():
    print("Testing Generator functionality for Body...")
    
    # 1. Explicit DataFrame (Current generated format)
    data_explicit = [
        {'Section': 'content', 'Name': 'application/json', 'Type': 'object', 'Parent': None},
        {'Section': None, 'Name': 'field1', 'Type': 'string', 'Parent': 'application/json'},
        {'Section': None, 'Name': 'field2', 'Type': 'integer', 'Parent': 'application/json'}
    ]
    df_explicit = pd.DataFrame(data_explicit)
    
    # 2. Implicit DataFrame (Old template format)
    data_implicit = [
        {'Section': None, 'Name': 'field1', 'Type': 'string', 'Parent': None},
        {'Section': None, 'Name': 'field2', 'Type': 'integer', 'Parent': None}
    ]
    df_implicit = pd.DataFrame(data_implicit)
    
    gen = OASGenerator()
    
    print("\n--- Processing Explicit ---")
    body_explicit = gen._build_request_body(df_explicit)
    print(json.dumps(body_explicit, indent=2))
    
    print("\n--- Processing Implicit ---")
    body_implicit = gen._build_request_body(df_implicit)
    print(json.dumps(body_implicit, indent=2))
    
    # Compare
    is_match = body_explicit == body_implicit
    print(f"\nMatch: {is_match}")
    
    if is_match:
        print("Success: Generator handles both formats identically.")
    else:
        print("Difference detected.")

if __name__ == '__main__':
    test_body_logic()
