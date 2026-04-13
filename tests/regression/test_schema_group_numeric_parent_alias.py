import os
import sys

import pandas as pd


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


from src.generator import OASGenerator


def test_build_schema_group_preserves_children_when_parent_uses_numeric_alias():
    df = pd.DataFrame(
        [
            {
                "Name": "MemberDefaultDayValues",
                "Parent": "",
                "Type": "array",
                "Items Data Type \n(Array only)": "object",
            },
            {
                "Name": "day",
                "Parent": "MemberDefaultDayValues1",
                "Type": "schema",
                "Schema Name\n(if Type = schema)": "Day",
                "Mandatory": "M",
            },
            {
                "Name": "defaultLACValues",
                "Parent": "MemberDefaultDayValues1",
                "Type": "schema",
                "Schema Name\n(if Type = schema)": "DefaultLACValues1",
                "Mandatory": "M",
            },
        ]
    )

    generator = OASGenerator(version="3.1.0")
    schemas = generator._build_schema_group(df)

    member_default_day_values = schemas["MemberDefaultDayValues"]
    items = member_default_day_values["items"]

    assert member_default_day_values["type"] == "array"
    assert items["type"] == "object"
    assert items["properties"]["day"]["$ref"] == "#/components/schemas/Day"
    assert (
        items["properties"]["defaultLACValues"]["$ref"]
        == "#/components/schemas/DefaultLACValues1"
    )
    assert items["required"] == ["day", "defaultLACValues"]
