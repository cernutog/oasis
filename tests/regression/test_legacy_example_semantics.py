import shutil
from pathlib import Path

from src.legacy_converter import DataType, LegacyConverter
from src.legacy_converter_dialog import LegacyConverterDialog


def _converter(**kwargs):
    log_callback = kwargs.pop("log_callback", lambda _message: None)
    converter = LegacyConverter(
        input_dir=".",
        output_dir=".",
        log_callback=log_callback,
        **kwargs,
    )
    converter.example_seed_values = converter._load_example_seed_values()
    converter.example_semantic_rules = converter._load_example_semantic_rules()
    return converter


def test_custom_semantic_category_is_available_when_rules_load_first():
    tmp_path = Path("tmp") / "test_legacy_example_semantics_rules_first"
    if tmp_path.exists():
        shutil.rmtree(tmp_path)
    tmp_path.mkdir(parents=True)
    try:
        seed_path = tmp_path / "legacy_example_seed_values.yaml"
        rules_path = tmp_path / "legacy_example_semantic_rules.yaml"
        seed_path.write_text(
            "clearing_system:\n"
            "  - STEP2\n"
            "  - RT1\n"
            "  - TIPS\n",
            encoding="utf-8",
        )
        rules_path.write_text(
            "rules:\n"
            "  - category: clearing_system\n"
            "    compact_exact:\n"
            "      - clrgsys\n",
            encoding="utf-8",
        )
        converter = LegacyConverter(
            input_dir=".",
            output_dir=".",
            log_callback=lambda _message: None,
            example_seed_values_path=seed_path,
            example_semantic_rules_path=rules_path,
        )

        rules = converter._load_example_semantic_rules()

        assert rules["rules"] == [
            {"category": "clearing_system", "compact_exact": ["clrgsys"]}
        ]
    finally:
        shutil.rmtree(tmp_path, ignore_errors=True)


def test_valid_excel_example_is_kept_even_when_semantic_category_has_other_defaults():
    converter = _converter()
    dt = DataType(
        name="TimeIndicator",
        type="string",
        pattern_eba="HH:MM",
        regex="[0-9]{2,2}:[0-9]{2,2}",
        example="16:00",
    )

    converter._fill_and_fix_examples_for_data_type(dt, schema_name="TimeIndicator")

    assert dt.example.startswith("16:00")


def test_configured_semantic_placeholders_are_repaired_but_valid_examples_are_kept():
    tmp_path = Path("tmp") / "test_legacy_example_semantic_placeholders"
    if tmp_path.exists():
        shutil.rmtree(tmp_path)
    tmp_path.mkdir(parents=True)
    try:
        rules_path = tmp_path / "legacy_example_semantic_rules.yaml"
        rules_path.write_text(
            "placeholder_patterns:\n"
            "  categories:\n"
            "    bic8:\n"
            "      - '^([A-Z0-9])\\\\1+$'\n",
            encoding="utf-8",
        )
        converter = _converter(example_semantic_rules_path=rules_path)
        bic = DataType(
            name="ReceiverBic",
            type="string",
            regex="[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}",
            example="AAAAAAAA",
        )
        time = DataType(
            name="TimeIndicator",
            type="string",
            regex="[0-9]{2,2}:[0-9]{2,2}",
            example="16:00",
        )

        converter._fill_and_fix_examples_for_data_type(bic, schema_name="ReceiverBic")
        converter._fill_and_fix_examples_for_data_type(time, schema_name="TimeIndicator")

        assert bic.example == "IPSDITM1; DEUTDEFF; BNPAFRPP"
        assert converter._example_trace_rows[-2]["action"] == "REPAIRED"
        assert converter._example_trace_rows[-2]["reason"] == "repaired invalid example: semantic placeholder"
        assert time.example.startswith("16:00")
    finally:
        shutil.rmtree(tmp_path, ignore_errors=True)


def test_semantic_time_candidates_are_filtered_by_regex_before_regex_fallback():
    converter = _converter()
    dt = DataType(
        name="TimeIndicator",
        type="string",
        pattern_eba="HH:MM",
        regex="[0-9]{2,2}:[0-9]{2,2}",
        example="",
    )

    converter._fill_and_fix_examples_for_data_type(dt, schema_name="TimeIndicator")

    assert dt.example
    values = [part.strip() for part in dt.example.split(";")]
    assert values[:3] == ["10:15", "12:00", "23:59"]


def test_generated_time_seed_config_is_migrated_to_include_hh_mm_values():
    tmp_path = Path("tmp") / "test_legacy_example_semantics_time_seed_migration"
    if tmp_path.exists():
        shutil.rmtree(tmp_path)
    tmp_path.mkdir(parents=True)
    try:
        seed_path = tmp_path / "legacy_example_seed_values.yaml"
        seed_path.write_text(
            "time:\n"
            "  - '10:15:30'\n"
            "  - '12:00:00'\n"
            "  - '23:59:59'\n",
            encoding="utf-8",
        )
        converter = LegacyConverter(
            input_dir=".",
            output_dir=".",
            log_callback=lambda _message: None,
            example_seed_values_path=seed_path,
        )

        seeds = converter._load_example_seed_values()

        assert seeds["time"][:3] == ["10:15", "12:00", "23:59"]
    finally:
        shutil.rmtree(tmp_path, ignore_errors=True)


def test_custom_semantic_category_can_be_defined_by_seed_and_rules_files():
    tmp_path = Path("tmp") / "test_legacy_example_semantics"
    if tmp_path.exists():
        shutil.rmtree(tmp_path)
    tmp_path.mkdir(parents=True)
    try:
        seed_path = tmp_path / "legacy_example_seed_values.yaml"
        rules_path = tmp_path / "legacy_example_semantic_rules.yaml"
        seed_path.write_text(
            "clearing_system:\n"
            "  - STEP2\n"
            "  - RT1\n"
            "  - TIPS\n",
            encoding="utf-8",
        )
        rules_path.write_text(
            "rules:\n"
            "  - category: clearing_system\n"
            "    compact_exact:\n"
            "      - clrgsys\n",
            encoding="utf-8",
        )
        converter = _converter(
            example_seed_values_path=seed_path,
            example_semantic_rules_path=rules_path,
        )
        dt = DataType(name="ClrgSys", type="string", example="")

        converter._fill_and_fix_examples_for_data_type(dt, schema_name="ClrgSys")

        assert dt.example == "STEP2; RT1; TIPS"
    finally:
        shutil.rmtree(tmp_path, ignore_errors=True)


def test_regex_alternatives_are_used_when_semantic_candidates_do_not_match():
    converter = _converter()
    dt = DataType(
        name="MsgTp",
        type="string",
        regex=r"(pain\.013){1}|(pain\.014){1}|(pacs\.028){1}|(camt\.055){1}|(camt\.029){1}",
        example="",
    )

    converter._fill_and_fix_examples_for_data_type(dt, schema_name="MsgTp")

    assert dt.example == "pain.013; pain.014; pacs.028"


def test_existing_valid_example_completed_from_allowed_values_is_not_repaired():
    converter = _converter()
    dt = DataType(
        name="ReportStatus",
        type="string",
        allowed_values="RDY,WIG,NTF",
        example="RDY",
    )

    converter._fill_and_fix_examples_for_data_type(dt, schema_name="ReportStatus")

    assert dt.example == "RDY; WIG; NTF"
    assert converter._example_trace_rows[-1]["action"] == "COMPLETED"
    assert converter._example_trace_rows[-1]["reason"] == "completed missing examples from allowed values"


def test_invalid_existing_example_repaired_with_constraint_reason():
    converter = _converter()
    dt = DataType(
        name="TimeIndicator",
        type="string",
        regex="[0-9]{2,2}:[0-9]{2,2}",
        example="string",
    )

    converter._fill_and_fix_examples_for_data_type(dt, schema_name="TimeIndicator")

    assert dt.example == "10:15; 12:00; 23:59"
    assert converter._example_trace_rows[-1]["action"] == "REPAIRED"
    assert converter._example_trace_rows[-1]["reason"] == "repaired invalid example: regex mismatch"


def test_oas_pattern_examples_are_validated_with_json_schema_search_semantics():
    converter = _converter()
    dt = DataType(
        name="ProductId",
        type="string",
        min_val="4",
        max_val="4",
        regex="[0-9A-Z]",
        example="INST;EOLO",
    )

    converter._fill_and_fix_examples_for_data_type(dt, schema_name="ProductId")

    values = [part.strip() for part in dt.example.split(";")]
    assert values[:2] == ["INST", "EOLO"]
    assert all(converter._is_valid_example_token(dt, value) for value in values)


def test_body_example_fallback_is_constraint_compliant_for_named_string_schema():
    converter = _converter()
    dt = DataType(
        name="ProductId",
        type="string",
        min_val="4",
        max_val="4",
        regex="[0-9A-Z]",
        example="",
    )
    converter.global_schemas["ProductId"] = dt
    converter.output_names[("$global", "ProductId")] = "ProductId"

    body = converter._build_body_example_dict(
        [("productId", "", "", "ProductId", "M", "", "", "")],
        ep_filename=None,
    )

    assert body["productId"] != "string"
    assert converter._is_valid_example_token(dt, body["productId"])


def test_diagnostic_provenance_fields_do_not_split_schema_fingerprints():
    converter = _converter()
    first = DataType(
        name="SenderBic",
        type="string",
        description="sender Bic",
        regex="[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}",
        example="IPSDITM1;DEUTDEFF;BNPAFRPP",
        source_file="first.xlsm",
        source_sheet="Data Type",
        source_row=10,
    )
    second = DataType(
        name="SenderBic",
        type="string",
        description="sender Bic",
        regex="[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}",
        example="IPSDITM1;DEUTDEFF;BNPAFRPP",
        source_file="second.xlsm",
        source_sheet="Data Type",
        source_row=42,
    )

    first_name = converter._register_data_type("first.xlsm", "SenderBic", first)
    second_name = converter._register_data_type("second.xlsm", "SenderBic", second)

    assert first_name == "SenderBic"
    assert second_name == "SenderBic"
    assert sorted(converter.global_schemas) == ["SenderBic"]


def test_impossible_example_constraints_are_recorded_as_blocking_errors():
    converter = _converter()
    dt = DataType(
        name="ImpossibleCode",
        type="string",
        min_val="5",
        max_val="4",
        regex="^[A-Z]{4}$",
        example="",
        source_file="example.xlsm",
    )

    converter.global_schemas["ImpossibleCode"] = dt
    converter._fill_and_fix_consolidated_examples()

    assert converter.example_generation_errors
    issue = converter.example_generation_errors[0]
    assert issue["field"] == "ImpossibleCode"
    assert issue["severity"] == "impossible"
    assert "min 5 > max 4" in issue["reason"]


def test_complex_non_generable_example_constraints_are_recorded_as_blocking_errors():
    converter = _converter()
    dt = DataType(
        name="ComplexCode",
        type="string",
        min_val="8",
        max_val="8",
        regex=r"^(?=.*[0-9])[a-z]{8}$",
        example="",
        source_file="example.xlsm",
    )

    converter.global_schemas["ComplexCode"] = dt
    converter._fill_and_fix_consolidated_examples()

    assert converter.example_generation_errors
    issue = converter.example_generation_errors[0]
    assert issue["field"] == "ComplexCode"
    assert issue["severity"] == "complex"
    assert "too complex regex" in issue["reason"]


def test_convert_blocks_before_writing_outputs_when_examples_cannot_be_generated(tmp_path, monkeypatch):
    input_dir = tmp_path / "legacy"
    output_dir = tmp_path / "converted"
    input_dir.mkdir()
    (input_dir / "dummy.xlsm").write_bytes(b"placeholder")
    logs = []
    converter = LegacyConverter(
        input_dir=str(input_dir),
        output_dir=str(output_dir),
        master_dir=".",
        log_callback=logs.append,
    )
    dt = DataType(
        name="ImpossibleCode",
        type="string",
        min_val="5",
        max_val="4",
        regex="^[A-Z]{4}$",
        example="",
        source_file="dummy.xlsm",
    )

    def collect_bad_data_type():
        converter.global_schemas["ImpossibleCode"] = dt

    monkeypatch.setattr(converter, "_collect_all_data_types", collect_bad_data_type)
    monkeypatch.setattr(converter, "_perform_naming_and_usage_pass", lambda: None)

    assert converter.convert(tracing_enabled=False) is False
    assert any("CONVERSION BLOCKED: EXAMPLE GENERATION ERRORS" in line for line in logs)
    assert not (output_dir / "dummy.xlsx").exists()


def test_blocking_example_report_uses_legacy_field_and_sheet_context():
    logs = []
    converter = _converter(log_callback=logs.append)
    dt = DataType(
        name="ProductId",
        type="string",
        min_val="4",
        max_val="4",
        regex="[0-9A-Z]{5}",
        example="INST;EOLO",
        source_file="apDetails.250410.xlsm",
        source_sheet="Data Type",
        source_row=21,
    )

    converter._record_example_generation_error(
        schema_name="ProductId2",
        dt=dt,
        severity="error",
        reason="no valid constraint-compliant example",
    )
    converter._log_example_generation_errors()

    joined = "\n".join(logs)
    assert "[1] ProductId\n" in joined
    assert "[1] ProductId2" not in joined
    assert "    Source field: ProductId" in joined
    assert "    Sheet: Data Type" in joined
    assert "    Row: 21" in joined


def test_action_required_log_tag_spans_all_box_lines():
    dialog = object.__new__(LegacyConverterDialog)
    dialog._action_required_log_block_active = False

    lines = [
        "+-- ACTION REQUIRED ----------------------------------------+",
        "| Provide valid examples in the Data Type sheet or fix      |",
        "| contradictory/too-complex constraints. OASIS will not     |",
        "| generate invalid or empty OAS examples as a fallback.     |",
        "+-----------------------------------------------------------+",
        "ISSUES",
    ]

    assert [dialog._is_action_required_log_line(line) for line in lines] == [
        True,
        True,
        True,
        True,
        True,
        False,
    ]
