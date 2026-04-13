import os
import sys

import pandas as pd


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


from src.generator_pkg.response_builder import build_schema_from_flat_table


def test_build_schema_from_flat_table_preserves_duplicate_nested_names():
    df = pd.DataFrame(
        [
            {"Name": "values", "Type": "object", "Parent": "", "Mandatory": "M"},
            {
                "Name": "lspBicDefaultDayValues",
                "Type": "array",
                "Parent": "values",
                "Mandatory": "O",
                "Items Data Type": "object",
            },
            {
                "Name": "day",
                "Type": "schema",
                "Schema Name": "Day",
                "Parent": "lspBicDefaultDayValues",
                "Mandatory": "M",
            },
            {
                "Name": "defaultLACValues",
                "Type": "array",
                "Parent": "lspBicDefaultDayValues",
                "Mandatory": "M",
                "Items Data Type": "schema",
                "Schema Name": "DefaultLACValues1",
            },
            {
                "Name": "memberDefaultDayValues",
                "Type": "array",
                "Parent": "values",
                "Mandatory": "O",
                "Items Data Type": "object",
            },
            {
                "Name": "day",
                "Type": "schema",
                "Schema Name": "Day",
                "Parent": "memberDefaultDayValues",
                "Mandatory": "M",
            },
            {
                "Name": "defaultLACValues",
                "Type": "array",
                "Parent": "memberDefaultDayValues",
                "Mandatory": "M",
                "Items Data Type": "schema",
                "Schema Name": "DefaultLACValues2",
            },
        ]
    )

    schema = build_schema_from_flat_table(df, "3.0.0")

    lsp_items = schema["properties"]["lspBicDefaultDayValues"]["items"]
    member_items = schema["properties"]["memberDefaultDayValues"]["items"]

    assert lsp_items["type"] == "object"
    assert member_items["type"] == "object"

    assert lsp_items["properties"]["day"]["$ref"] == "#/components/schemas/Day"
    assert member_items["properties"]["day"]["$ref"] == "#/components/schemas/Day"

    assert (
        lsp_items["properties"]["defaultLACValues"]["items"]["$ref"]
        == "#/components/schemas/DefaultLACValues1"
    )
    assert (
        member_items["properties"]["defaultLACValues"]["items"]["$ref"]
        == "#/components/schemas/DefaultLACValues2"
    )

    assert lsp_items["required"] == ["day", "defaultLACValues"]
    assert member_items["required"] == ["day", "defaultLACValues"]
