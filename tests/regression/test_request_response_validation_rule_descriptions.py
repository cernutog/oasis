import os
import sys

import pandas as pd
import pytest


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


from src.legacy_converter import DataType, LegacyConverter
from src.generator import OASGenerator


def test_build_children_rows_adds_validation_rules_for_request_usage():
    converter = LegacyConverter(input_dir=".", output_dir=".")
    children = [
        (
            "lacDefaultAgenda",
            "",
            "The following section is repeated as many times as the LACs are.",
            "string",
            "M",
            "It must be present one occurrence/lac (errorCode XA07)",
            "",
        )
    ]

    request_rows, _, _ = converter._build_children_rows(
        "DefaultDailyThresholds",
        children,
        usage_ctx="getDefaultAgenda (Body)",
    )
    response_rows, _, _ = converter._build_children_rows(
        "DefaultDailyThresholds",
        children,
        usage_ctx="getDefaultAgenda (200)",
    )

    request_desc = request_rows[0][2]
    response_desc = response_rows[0][2]

    assert "**Validation Rule(s)**" in request_desc
    assert "one occurrence/lac" in request_desc
    assert "**Validation Rule(s)**" in response_desc
    assert "one occurrence/lac" in response_desc


def test_request_rows_expand_parent_locally_when_nested_children_need_overrides():
    converter = LegacyConverter(input_dir=".", output_dir=".")
    converter.global_schemas["SettlementBIC"] = DataType(
        name="SettlementBIC",
        type="object",
        source_file="$global",
    )
    converter.output_names[("$global", "SettlementBIC")] = "SettlementBIC"
    children = [
        ("settlementBIC", "", "", "SettlementBIC", "M", "", ""),
        (
            "settlementBICCode",
            "settlementBIC",
            "The CGS Settlement BIC",
            "Bic11Only",
            "M",
            "It must be present in Routing Repositories (errorCode PY01)",
            "",
        ),
    ]

    rows, refs, _ = converter._build_children_rows(
        "AmendChangeSettlementBICRequest",
        children,
        usage_ctx="amendChangeSettlementBIC (Body)",
        inject_validation_overrides=True,
    )

    parent_row = next(row for row in rows if row[0] == "settlementBIC")
    child_row = next(row for row in rows if row[0] == "settlementBICCode")

    assert parent_row[1] == "AmendChangeSettlementBICRequest"
    assert parent_row[3] == "object"
    assert parent_row[5] == ""
    assert child_row[1] == "settlementBIC"
    assert "**Validation Rule(s)**" in child_row[2]
    assert "SettlementBIC" not in refs


def test_shared_children_rows_keep_validation_rules_in_request_context():
    converter = LegacyConverter(input_dir=".", output_dir=".")
    children = [
        (
            "settlementBICCode",
            "",
            "The CGS Settlement BIC",
            "Bic11Only",
            "M",
            "It must be present in Routing Repositories (errorCode PY01)",
            "",
        )
    ]

    neutral_rows, _, _ = converter._build_children_rows(
        "SettlementBIC",
        children,
        usage_ctx="amendChangeSettlementBIC (Body)",
    )

    assert "**Validation Rule(s)**" in neutral_rows[0][2]
    assert "Routing Repositories" in neutral_rows[0][2]


def test_request_and_response_subtrees_with_different_validation_rules_split_into_distinct_components():
    converter = LegacyConverter(input_dir=".", output_dir=".")
    request_children = [
        ("lacDefaultAgenda", "", "", "object", "M", "", "", ""),
        (
            "lacNumber",
            "lacDefaultAgenda",
            "The relevant LAC",
            "LacNumber",
            "M",
            "",
            "It must a valid code (errorCode SC01)",
            "",
        ),
    ]
    response_children = [
        ("lacDefaultAgenda", "", "", "object", "M", "", "", ""),
        (
            "lacNumber",
            "lacDefaultAgenda",
            "The relevant LAC",
            "LacNumber",
            "M",
            "",
            "",
            "",
        ),
    ]

    request_rows, _, request_extra = converter._build_children_rows(
        "CommandDetailsRequest",
        request_children,
        usage_ctx="commandDetails (Body)",
    )
    response_rows, _, response_extra = converter._build_children_rows(
        "CommandDetailsResponse",
        response_children,
        usage_ctx="commandDetails (200)",
    )

    assert request_rows[0][5] == "LacDefaultAgenda"
    assert response_rows[0][5] == "LacDefaultAgenda1"
    assert request_extra[1][2].endswith("It must a valid code (errorCode SC01)")
    assert response_extra[1][2] == "The relevant LAC"


def test_inline_components_split_when_only_constraint_differs():
    converter = LegacyConverter(input_dir=".", output_dir=".")
    first_children = [
        ("filePCF", "", "The information related to the Payment Cancellation File", "object", "O", "", "", ""),
        ("fileType", "filePCF", "The file type-PCF", "FileType", "M", "Allowed values: PCF", "", ""),
        ("receiverBIC", "filePCF", "The BIC of the receiving DP", "Bic8", "M", "Pattern: 4!c2!a2!c", "", ""),
    ]
    second_children = [
        ("filePSR", "", "The information related to the Pre-Settlement Report File", "object", "O", "", "", ""),
        ("fileType", "filePSR", "The file type-PSR", "FileType", "M", "Allowed values: PSR", "", ""),
        ("receiverBIC", "filePSR", "The BIC of the receiving DP", "Bic8", "M", "Pattern: 4!c2!a2!c", "", ""),
    ]

    first_rows, _, _ = converter._build_children_rows(
        "FileDetailsResponse",
        first_children,
        usage_ctx="fileDetails (200)",
    )
    second_rows, _, _ = converter._build_children_rows(
        "FileDetailsResponse",
        second_children,
        usage_ctx="fileDetails (200)",
    )

    assert first_rows[0][5] == "FilePCF"
    assert second_rows[0][5] == "FilePSR"


def test_request_rows_expand_named_array_parent_locally_when_nested_children_need_overrides():
    converter = LegacyConverter(input_dir=".", output_dir=".")
    converter.global_schemas["DefaultDailyThresholds"] = DataType(
        name="DefaultDailyThresholds",
        type="array",
        items_type="object",
        source_file="$global",
    )
    converter.output_names[("$global", "DefaultDailyThresholds")] = "DefaultDailyThresholds"
    children = [
        ("defaultDailyThresholds", "", "", "DefaultDailyThresholds", "M", "", ""),
        (
            "day",
            "defaultDailyThresholds",
            "The day of the week.",
            "Day",
            "M",
            "It must be present 5 times: 1 occurrence/day",
            "",
        ),
    ]

    rows, refs, _ = converter._build_children_rows(
        "SetDefaultAgendaRequest",
        children,
        usage_ctx="setDefaultAgenda (Body)",
        inject_validation_overrides=True,
    )

    parent_row = next(row for row in rows if row[0] == "defaultDailyThresholds")
    child_row = next(row for row in rows if row[0] == "day")

    assert parent_row[1] == "SetDefaultAgendaRequest"
    assert parent_row[3] == "array"
    assert parent_row[4] == "object"
    assert parent_row[5] == ""
    assert child_row[1] == "defaultDailyThresholds"
    assert "**Validation Rule(s)**" in child_row[2]
    assert "DefaultDailyThresholds" not in refs


def test_generator_builds_request_overlay_for_children_under_ref_parent():
    generator = OASGenerator(version="3.1.0")
    df = pd.DataFrame(
        [
            {"Name": "SettlementBIC", "Parent": "", "Type": "object"},
            {
                "Name": "settlementBICCode",
                "Parent": "SettlementBIC",
                "Type": "schema",
                "Schema Name\n(if Type = schema)": "Bic11Only",
                "Mandatory": "M",
            },
            {"Name": "AmendChangeSettlementBICRequest", "Parent": "", "Type": "object"},
            {
                "Name": "settlementBIC",
                "Parent": "AmendChangeSettlementBICRequest",
                "Type": "schema",
                "Schema Name\n(if Type = schema)": "SettlementBIC",
                "Mandatory": "M",
            },
            {
                "Name": "settlementBICCode",
                "Parent": "settlementBIC",
                "Type": "schema",
                "Schema Name\n(if Type = schema)": "Bic11Only",
                "Description": "The CGS Settlement BIC\n\n **Validation Rule(s)** It must be present in Routing Repositories (errorCode PY01)",
                "Mandatory": "M",
            },
        ]
    )

    schemas = generator._build_schema_group(df)
    settlement_bic = schemas["AmendChangeSettlementBICRequest"]["properties"]["settlementBIC"]

    assert "allOf" in settlement_bic
    assert settlement_bic["allOf"][0]["$ref"] == "#/components/schemas/SettlementBIC"
    overlay = settlement_bic["allOf"][1]
    assert overlay["type"] == "object"
    assert overlay["properties"]["settlementBICCode"]["$ref"] == "#/components/schemas/Bic11Only"
    assert "**Validation Rule(s)**" in overlay["properties"]["settlementBICCode"]["description"]
    assert overlay["required"] == ["settlementBICCode"]


def test_generator_builds_array_overlay_for_request_children_under_array_ref_parent():
    generator = OASGenerator(version="3.1.0")
    df = pd.DataFrame(
        [
            {
                "Name": "DefaultDailyThresholds",
                "Parent": "",
                "Type": "array",
                "Items Data Type \n(Array only)": "object",
                "Max  \nValue/Length/Item": "5",
            },
            {
                "Name": "day",
                "Parent": "DefaultDailyThresholds",
                "Type": "schema",
                "Schema Name\n(if Type = schema)": "Day",
                "Mandatory": "M",
            },
            {
                "Name": "SetDefaultAgendaRequest",
                "Parent": "",
                "Type": "object",
            },
            {
                "Name": "defaultDailyThresholds",
                "Parent": "SetDefaultAgendaRequest",
                "Type": "schema",
                "Schema Name\n(if Type = schema)": "DefaultDailyThresholds",
                "Description": " **Validation Rule(s)** It must be present 5 times: 1 occurrence/day.",
                "Mandatory": "M",
            },
            {
                "Name": "day",
                "Parent": "defaultDailyThresholds",
                "Type": "schema",
                "Schema Name\n(if Type = schema)": "Day",
                "Description": "The day of the week.\n\n **Validation Rule(s)** It must be present 5 times: 1 occurrence/day",
                "Mandatory": "M",
            },
        ]
    )

    schemas = generator._build_schema_group(df)
    default_daily_thresholds = schemas["SetDefaultAgendaRequest"]["properties"]["defaultDailyThresholds"]

    assert "allOf" in default_daily_thresholds
    assert default_daily_thresholds["allOf"][0]["$ref"] == "#/components/schemas/DefaultDailyThresholds"
    overlay = default_daily_thresholds["allOf"][1]
    assert overlay["type"] == "array"
    assert overlay["items"]["type"] == "object"
    assert overlay["items"]["properties"]["day"]["$ref"] == "#/components/schemas/Day"
    assert "**Validation Rule(s)**" in overlay["items"]["properties"]["day"]["description"]
    assert overlay["items"]["required"] == ["day"]


def test_generator_builds_inline_combinator_ref_override_for_object_branch():
    generator = OASGenerator(version="3.1.0")
    df = pd.DataFrame(
        [
            {"Name": "AltA", "Parent": "", "Type": "object"},
            {
                "Name": "foo",
                "Parent": "AltA",
                "Type": "schema",
                "Schema Name\n(if Type = schema)": "Bic11Only",
                "Mandatory": "M",
            },
            {"Name": "Choice", "Parent": "", "Type": "oneOf"},
            {
                "Name": "Choice[0]",
                "Parent": "Choice",
                "Type": "schema",
                "Schema Name\n(if Type = schema)": "AltA",
            },
            {
                "Name": "foo",
                "Parent": "Choice[0]",
                "Type": "schema",
                "Schema Name\n(if Type = schema)": "Bic11Only",
                "Description": "Override in oneOf branch",
                "Mandatory": "M",
            },
        ]
    )

    schemas = generator._build_schema_group(df)
    branch = schemas["Choice"]["oneOf"][0]

    assert branch["allOf"][0]["$ref"] == "#/components/schemas/AltA"
    overlay = branch["allOf"][1]
    assert overlay["type"] == "object"
    assert overlay["properties"]["foo"]["description"] == "Override in oneOf branch"
    assert overlay["required"] == ["foo"]


def test_generator_builds_request_overlay_for_ref_parent_across_schema_blocks():
    generator = OASGenerator(version="3.1.0")
    df = pd.DataFrame(
        [
            {"Name": "SettlementBIC", "Parent": "", "Type": "object"},
            {
                "Name": "settlementBICCode",
                "Parent": "SettlementBIC",
                "Type": "schema",
                "Schema Name\n(if Type = schema)": "Bic11Only",
                "Mandatory": "M",
            },
            {"Name": "", "Parent": "", "Type": ""},
            {"Name": "Wrapper", "Parent": "", "Type": "object"},
            {
                "Name": "settlementBIC",
                "Parent": "Wrapper",
                "Type": "schema",
                "Schema Name\n(if Type = schema)": "SettlementBIC",
                "Mandatory": "M",
            },
            {
                "Name": "settlementBICCode",
                "Parent": "settlementBIC",
                "Type": "schema",
                "Schema Name\n(if Type = schema)": "Bic11Only",
                "Description": "Cross-block override",
                "Mandatory": "M",
            },
        ]
    )

    schemas = generator._build_schema_group(df)
    settlement_bic = schemas["Wrapper"]["properties"]["settlementBIC"]

    assert settlement_bic["allOf"][0]["$ref"] == "#/components/schemas/SettlementBIC"
    overlay = settlement_bic["allOf"][1]
    assert overlay["type"] == "object"
    assert overlay["properties"]["settlementBICCode"]["description"] == "Cross-block override"
    assert overlay["required"] == ["settlementBICCode"]


def test_generator_builds_array_overlay_for_ref_parent_across_schema_blocks():
    generator = OASGenerator(version="3.1.0")
    df = pd.DataFrame(
        [
            {
                "Name": "DefaultDailyThresholds",
                "Parent": "",
                "Type": "array",
                "Items Data Type \n(Array only)": "object",
                "Max  \nValue/Length/Item": "5",
            },
            {
                "Name": "day",
                "Parent": "DefaultDailyThresholds",
                "Type": "schema",
                "Schema Name\n(if Type = schema)": "Day",
                "Mandatory": "M",
            },
            {"Name": "", "Parent": "", "Type": ""},
            {"Name": "Wrapper", "Parent": "", "Type": "object"},
            {
                "Name": "defaultDailyThresholds",
                "Parent": "Wrapper",
                "Type": "schema",
                "Schema Name\n(if Type = schema)": "DefaultDailyThresholds",
                "Mandatory": "M",
            },
            {
                "Name": "day",
                "Parent": "defaultDailyThresholds",
                "Type": "schema",
                "Schema Name\n(if Type = schema)": "Day",
                "Description": "Cross-block array override",
                "Mandatory": "M",
            },
        ]
    )

    schemas = generator._build_schema_group(df)
    default_daily_thresholds = schemas["Wrapper"]["properties"]["defaultDailyThresholds"]

    assert default_daily_thresholds["allOf"][0]["$ref"] == "#/components/schemas/DefaultDailyThresholds"
    overlay = default_daily_thresholds["allOf"][1]
    assert overlay["type"] == "array"
    assert overlay["items"]["type"] == "object"
    assert overlay["items"]["properties"]["day"]["description"] == "Cross-block array override"
    assert overlay["items"]["required"] == ["day"]


def test_generator_handles_nested_inline_combinators():
    generator = OASGenerator(version="3.1.0")
    df = pd.DataFrame(
        [
            {"Name": "AltA", "Parent": "", "Type": "object"},
            {
                "Name": "foo",
                "Parent": "AltA",
                "Type": "schema",
                "Schema Name\n(if Type = schema)": "Bic11Only",
                "Mandatory": "M",
            },
            {"Name": "AltB", "Parent": "", "Type": "object"},
            {
                "Name": "bar",
                "Parent": "AltB",
                "Type": "schema",
                "Schema Name\n(if Type = schema)": "Day",
                "Mandatory": "M",
            },
            {"Name": "Root", "Parent": "", "Type": "oneOf"},
            {"Name": "Root[0]", "Parent": "Root", "Type": "oneOf"},
            {
                "Name": "Root[0][0]",
                "Parent": "Root[0]",
                "Type": "schema",
                "Schema Name\n(if Type = schema)": "AltA",
            },
            {
                "Name": "Root[0][1]",
                "Parent": "Root[0]",
                "Type": "schema",
                "Schema Name\n(if Type = schema)": "AltB",
            },
        ]
    )

    schemas = generator._build_schema_group(df)
    nested = schemas["Root"]["oneOf"][0]

    assert "oneOf" in nested
    assert nested["oneOf"][0]["$ref"] == "#/components/schemas/AltA"
    assert nested["oneOf"][1]["$ref"] == "#/components/schemas/AltB"


def test_generator_builds_inline_combinator_array_override_across_schema_blocks():
    generator = OASGenerator(version="3.1.0")
    df = pd.DataFrame(
        [
            {
                "Name": "DefaultDailyThresholds",
                "Parent": "",
                "Type": "array",
                "Items Data Type \n(Array only)": "object",
                "Max  \nValue/Length/Item": "5",
            },
            {
                "Name": "day",
                "Parent": "DefaultDailyThresholds",
                "Type": "schema",
                "Schema Name\n(if Type = schema)": "Day",
                "Mandatory": "M",
            },
            {"Name": "", "Parent": "", "Type": ""},
            {"Name": "Choice", "Parent": "", "Type": "oneOf"},
            {
                "Name": "Choice[0]",
                "Parent": "Choice",
                "Type": "schema",
                "Schema Name\n(if Type = schema)": "DefaultDailyThresholds",
            },
            {
                "Name": "day",
                "Parent": "Choice[0]",
                "Type": "schema",
                "Schema Name\n(if Type = schema)": "Day",
                "Description": "Inline array branch override",
                "Mandatory": "M",
            },
        ]
    )

    schemas = generator._build_schema_group(df)
    branch = schemas["Choice"]["oneOf"][0]

    assert branch["allOf"][0]["$ref"] == "#/components/schemas/DefaultDailyThresholds"
    overlay = branch["allOf"][1]
    assert overlay["type"] == "array"
    assert overlay["items"]["properties"]["day"]["description"] == "Inline array branch override"
    assert overlay["items"]["required"] == ["day"]


def test_generator_rejects_local_children_under_array_with_non_object_items():
    generator = OASGenerator(version="3.1.0")
    df = pd.DataFrame(
        [
            {
                "Name": "StringList",
                "Parent": "",
                "Type": "array",
                "Items Data Type \n(Array only)": "string",
            },
            {"Name": "Wrapper", "Parent": "", "Type": "object"},
            {
                "Name": "values",
                "Parent": "Wrapper",
                "Type": "schema",
                "Schema Name\n(if Type = schema)": "StringList",
                "Mandatory": "M",
            },
            {
                "Name": "itemNote",
                "Parent": "values",
                "Type": "string",
                "Description": "Ambiguous child override",
            },
        ]
    )

    with pytest.raises(ValueError, match="require object items"):
        generator._build_schema_group(df)


def test_generator_rejects_local_children_under_array_of_arrays():
    generator = OASGenerator(version="3.1.0")
    df = pd.DataFrame(
        [
            {
                "Name": "NestedList",
                "Parent": "",
                "Type": "array",
                "Items Data Type \n(Array only)": "array",
            },
            {"Name": "Wrapper", "Parent": "", "Type": "object"},
            {
                "Name": "values",
                "Parent": "Wrapper",
                "Type": "schema",
                "Schema Name\n(if Type = schema)": "NestedList",
                "Mandatory": "M",
            },
            {
                "Name": "innerChild",
                "Parent": "values",
                "Type": "string",
                "Description": "Ambiguous nested-array child override",
            },
        ]
    )

    with pytest.raises(ValueError, match="require object items"):
        generator._build_schema_group(df)
