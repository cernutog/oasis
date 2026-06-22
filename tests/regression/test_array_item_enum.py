import os
import sys

import pandas as pd


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


from src.generator_pkg.schema_builder import map_type_to_schema
from src.generator_pkg.yaml_output import QuotedString


def test_array_allowed_values_are_applied_to_items_enum():
    row = pd.Series(
        {
            "Name": "labels",
            "Type": "array",
            "Items Data Type \n(Array only)": "string",
            "Allowed value": "LTG001, LTG037",
        }
    )

    schema = map_type_to_schema(row, version="3.1.0")

    assert "enum" not in schema
    assert schema["type"] == "array"
    assert schema["items"] == {"type": "string", "enum": ["LTG001", "LTG037"]}


def test_array_string_allowed_values_preserve_numeric_tokens_as_strings():
    row = pd.Series(
        {
            "Name": "codes",
            "Type": "array",
            "Items Data Type \n(Array only)": "string",
            "Allowed value": "001, 002",
        }
    )

    schema = map_type_to_schema(row, version="3.1.0")

    assert "enum" not in schema
    assert schema["items"]["type"] == "string"
    assert schema["items"]["enum"] == [QuotedString("001"), QuotedString("002")]


def test_array_integer_allowed_values_are_cast_on_items_enum():
    row = pd.Series(
        {
            "Name": "scores",
            "Type": "array",
            "Items Data Type \n(Array only)": "integer",
            "Allowed value": "1, 2",
        }
    )

    schema = map_type_to_schema(row, version="3.1.0")

    assert "enum" not in schema
    assert schema["items"] == {"type": "integer", "enum": [1, 2]}
