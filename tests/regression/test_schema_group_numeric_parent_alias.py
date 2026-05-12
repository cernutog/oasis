import os
import sys

import pandas as pd


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


from src.generator import OASGenerator


def test_build_schema_group_reports_blocking_issue_when_parent_uses_numeric_alias():
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

    logs = []
    generator = OASGenerator(version="3.1.0", log_callback=logs.append)
    schemas = generator._build_schema_group(df)

    assert schemas["MemberDefaultDayValues"]["type"] == "array"
    assert "day" in schemas
    assert "defaultLACValues" in schemas
    assert logs == []
    assert generator.get_schema_parent_issues() == [
        {
            "severity": "WARNING",
            "schema": "MemberDefaultDayValues",
            "field": "day",
            "parent": "MemberDefaultDayValues1",
            "status": "blocking",
        },
        {
            "severity": "WARNING",
            "schema": "MemberDefaultDayValues",
            "field": "defaultLACValues",
            "parent": "MemberDefaultDayValues1",
            "status": "blocking",
        },
    ]


def test_build_schema_group_logs_unresolved_parent_when_alias_fallback_fails():
    df = pd.DataFrame(
        [
            {
                "Name": "ProductList6",
                "Parent": "",
                "Type": "array",
                "Items Data Type \n(Array only)": "object",
            },
            {
                "Name": "solutionProposed",
                "Parent": "ProductList14",
                "Type": "schema",
                "Schema Name\n(if Type = schema)": "SolutionProposed",
                "Mandatory": "M",
            },
        ]
    )

    logs = []
    generator = OASGenerator(version="3.1.0", log_callback=logs.append)
    schemas = generator._build_schema_group(df)

    assert "solutionProposed" in schemas
    assert logs == []
    assert generator.get_schema_parent_issues() == [
        {
            "severity": "WARNING",
            "schema": "ProductList6",
            "field": "solutionProposed",
            "parent": "ProductList14",
            "status": "blocking",
        }
    ]


def test_build_schema_group_parent_diagnostics_use_nearest_schema_root():
    df = pd.DataFrame(
        [
            {
                "Name": "AcceptanceCd",
                "Parent": "",
                "Type": "string",
            },
            {
                "Name": "ProductList",
                "Parent": "",
                "Type": "array",
                "Items Data Type \n(Array only)": "object",
            },
            {
                "Name": "prySndgNetAd",
                "Parent": "ProductList13",
                "Type": "schema",
                "Schema Name\n(if Type = schema)": "PrySndgNetAd",
            },
        ]
    )

    logs = []
    generator = OASGenerator(version="3.1.0", log_callback=logs.append)
    generator._build_schema_group(df)

    assert logs == []
    assert generator.get_schema_parent_issues() == [
        {
            "severity": "WARNING",
            "schema": "ProductList",
            "field": "prySndgNetAd",
            "parent": "ProductList13",
            "status": "blocking",
        }
    ]
