import pandas as pd
import json
from src.generator_pkg.response_builder import build_examples_from_rows
from src.generator_pkg.row_helpers import get_name, get_parent, get_col_value, get_type

# Verify Generator logic for Array Examples
# Hypothesis: Repeated keys (Name) with same Parent will overwrite each other,
# unless explicit indexing (Parent[0]) is used.

def test_array_example_logic():
    print("Testing Generator Array Example Logic...")
    
    # Check implicitly repeated rows (Current Generation)
    # parent 'riskInfoArray' is repeated
    data_implicit = [
        {'Section': 'examples', 'Name': 'riskInfoArray', 'Parent': 'OK', 'Type': 'array', 'Example': None},
        # Item 1
        {'Section': 'examples', 'Name': 'modelName', 'Parent': 'riskInfoArray', 'Type': 'string', 'Example': 'Model1'},
        # Item 2
        {'Section': 'examples', 'Name': 'modelName', 'Parent': 'riskInfoArray', 'Type': 'string', 'Example': 'Model2'},
    ]
    df_implicit = pd.DataFrame(data_implicit)
    
    print("\n--- Processing Implicit (Repeated Keys) ---")
    try:
        ex_implicit = build_examples_from_rows(df_implicit)
        print(json.dumps(ex_implicit, indent=2))
        
        # Check if we lost Model1
        risk = ex_implicit.get('riskInfoArray')
        if isinstance(risk, list):
            # It might be list of 1 object?
            print(f"Result Type: {type(risk)}")
            print(f"Content: {risk}")
    except Exception as e:
        print(f"Error: {e}")

    # Check Explicit Indexing (Reference Style)
    data_explicit = [
        {'Section': 'examples', 'Name': 'riskInfoArray', 'Parent': 'OK', 'Type': 'array', 'Example': None},
        # Item 1 - Parent riskInfoArray[0]
        {'Section': 'examples', 'Name': 'modelName', 'Parent': 'riskInfoArray[0]', 'Type': 'string', 'Example': 'Model1'},
        # Item 2 - Parent riskInfoArray[1]
        {'Section': 'examples', 'Name': 'modelName', 'Parent': 'riskInfoArray[1]', 'Type': 'string', 'Example': 'Model2'},
    ]
    df_explicit = pd.DataFrame(data_explicit)
    
    print("\n--- Processing Explicit (Indexed Parent) ---")
    try:
        ex_explicit = build_examples_from_rows(df_explicit)
        print(json.dumps(ex_explicit, indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    test_array_example_logic()
