import shutil
from pathlib import Path

from src.legacy_converter import DataType, LegacyConverter


def _converter(**kwargs):
    converter = LegacyConverter(
        input_dir=".",
        output_dir=".",
        log_callback=lambda _message: None,
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
