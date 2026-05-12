from pathlib import Path
import re
import shutil

import yaml
import pandas as pd
from openpyxl import Workbook, load_workbook

from src.api_designer.models import Change, ChangeStep, create_empty_workspace
from src.api_designer.persistence import FileSystemDesignerRepository
from src.excel_parser import parse_paths_index
from src.generator import OASGenerator
from src.legacy_converter import DataType, LegacyConverter
from src.legacy_converter_dialog import LegacyConverterDialog
from src.preferences import (
    GENERATION_MODE_MINIMAL,
    GENERATION_MODE_STANDARD,
    PreferencesManager,
)


TEST_TEMP_ROOT = Path(__file__).resolve().parents[1] / "_tmp_api_designer_foundation"


def _snapshot_files(root: Path) -> dict[str, str]:
    return {
        str(path.relative_to(root)).replace("\\", "/"): path.read_text(encoding="utf-8")
        for path in sorted(root.rglob("*.yaml"))
    }


def _clean_test_temp() -> Path:
    if TEST_TEMP_ROOT.exists():
        shutil.rmtree(TEST_TEMP_ROOT)
    TEST_TEMP_ROOT.mkdir(parents=True)
    return TEST_TEMP_ROOT


def test_designer_is_hidden_by_default_for_intermediate_releases():
    defaults = PreferencesManager.DEFAULT_PREFERENCES
    assert defaults["enable_api_designer"] is False
    assert defaults["default_tab"] == "OAS Generation"


def test_api_designer_workspace_roundtrip_is_deterministic():
    temp_root = _clean_test_temp()
    workspace = create_empty_workspace("Payments Workspace")
    api = workspace.apis[0]
    api.id = "api_payments"
    api.name = "Payments API"
    api.display_label = "Payments API"
    api.version = "1.2.0"
    api.info = {"title": "Payments API", "version": "1.2.0"}
    api.extensions["x-portal-owner"] = "payments"
    workspace.changes.append(
        Change(
            id="chg_cr5262",
            kind="CR",
            external_ref="CR5262",
            title="Add payment status endpoint",
            target_api_id=api.id,
            steps=[
                ChangeStep(
                    id="step_add_path",
                    order=1,
                    kind="add_path",
                    target_id=api.id,
                    path="/payments/{paymentId}/status",
                    after={"method": "get"},
                )
            ],
        )
    )

    try:
        repo = FileSystemDesignerRepository(temp_root / "API Models" / "Payments_Workspace")
        repo.save_workspace(workspace)
        first_snapshot = _snapshot_files(repo.root_path)

        loaded = repo.load_workspace()
        repo.save_workspace(loaded)
        second_snapshot = _snapshot_files(repo.root_path)

        assert first_snapshot == second_snapshot
        assert loaded.name == "Payments Workspace"
        assert loaded.apis[0].id == "api_payments"
        assert loaded.apis[0].extensions["x-portal-owner"] == "payments"
        assert loaded.changes[0].steps[0].kind == "add_path"
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


def test_api_designer_file_package_shape():
    temp_root = _clean_test_temp()
    workspace = create_empty_workspace("Initial Workspace")
    workspace.apis[0].id = "api_initial"

    try:
        repo = FileSystemDesignerRepository(temp_root / "Initial_Workspace")
        repo.save_workspace(workspace)

        assert (repo.root_path / "workspace.yaml").exists()
        assert (repo.root_path / "apis" / "api_initial.yaml").exists()
        assert (repo.root_path / "libraries").is_dir()
        assert (repo.root_path / "metadata" / "catalog.yaml").exists()
        assert (repo.root_path / "revisions").is_dir()

        manifest = yaml.safe_load((repo.root_path / "workspace.yaml").read_text(encoding="utf-8"))
        assert manifest["schema_version"] == "api-designer.workspace/v1"
        assert manifest["apis"] == [
            {
                "id": "api_initial",
                "name": "New API",
                "display_label": "New API",
                "file": "apis/api_initial.yaml",
            }
        ]
        assert "root_surface" not in manifest["apis"][0]
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


class _DummyEntry:
    def __init__(self, value: str):
        self._value = value

    def get(self) -> str:
        return self._value


class _DummyPrefs:
    def __init__(self, values: dict[str, str]):
        self._values = values

    def get(self, key: str, default=None):
        if key == "remember_paths":
            return True
        return self._values.get(key, default)


def test_legacy_converter_browse_initial_dir_uses_nearest_existing_path():
    temp_root = _clean_test_temp()
    missing_leaf = temp_root / "Templates" / "CGS API OPS" / "2026Q4"
    expected = missing_leaf.parent
    expected.mkdir(parents=True)

    try:
        dialog = object.__new__(LegacyConverterDialog)
        dialog.prefs_manager = _DummyPrefs({"last_legacy_src": str(temp_root)})

        initial = dialog._get_initial_dir(_DummyEntry(str(missing_leaf)), "last_legacy_src")

        assert Path(initial) == expected
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


def test_generation_mode_filters_request_body_examples():
    df = pd.DataFrame(
        [
            {
                "Section": "content",
                "Name": "application/json",
                "Parent": "",
                "Type": "schema",
                "Schema": "PaymentRequest",
                "Mandatory": "M",
            }
        ]
    )
    body_examples = {"OK": "amount: 100", "Bad Request": "amount: bad"}

    standard = OASGenerator(generation_mode=GENERATION_MODE_STANDARD)
    standard_body = standard._build_request_body(df, body_examples)
    assert list(standard_body["content"]["application/json"]["examples"].keys()) == ["OK"]

    minimal = OASGenerator(generation_mode=GENERATION_MODE_MINIMAL)
    minimal_body = minimal._build_request_body(df, body_examples)
    assert "examples" not in minimal_body["content"]["application/json"]

    oas_fragment = {
        "x-keep": "visible",
        "content": {"examples": {"OK": {"value": {"x-sandbox-request-name": "hidden"}}}},
    }
    standard._remove_sandbox_extensions(oas_fragment)
    assert oas_fragment == {
        "x-keep": "visible",
        "content": {"examples": {"OK": {"value": {}}}},
    }


def test_generation_mode_filters_response_examples_and_optional_placeholders():
    content = {
        "application/json": {
            "schema": {
                "type": "object",
                "required": ["settlementBIC"],
                "properties": {
                    "settlementBIC": {"type": "string"},
                    "preferredAgentBIC": {
                        "type": "string",
                        "pattern": "[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}",
                    },
                },
            },
            "examples": {
                "OK": {
                    "value": {
                        "settlementBIC": "IPSDID21XXX",
                        "preferredAgentBIC": "string",
                    }
                },
                "Bad Request": {"value": {"settlementBIC": "INVALID"}},
            },
        }
    }

    standard = OASGenerator(generation_mode=GENERATION_MODE_STANDARD)
    standard._coerce_content_examples(content, {})

    assert list(content["application/json"]["examples"].keys()) == ["OK"]
    assert content["application/json"]["examples"]["OK"]["value"] == {
        "settlementBIC": "IPSDID21XXX"
    }

    minimal_content = {
        "application/json": {
            "schema": {"type": "object"},
            "examples": {"OK": {"value": {"a": "b"}}},
        }
    }
    minimal = OASGenerator(generation_mode=GENERATION_MODE_MINIMAL)
    minimal._coerce_content_examples(minimal_content, {})

    assert "examples" not in minimal_content["application/json"]


def test_minimal_generation_removes_schema_examples_from_yaml_output():
    generator = OASGenerator(generation_mode=GENERATION_MODE_MINIMAL)
    generator.oas["components"]["schemas"]["Payment"] = {
        "type": "object",
        "example": {"amount": 100},
        "examples": [{"amount": 200}],
        "properties": {
            "amount": {"type": "number", "example": 100},
            "examples": {"type": "string", "example": "business-field"},
        },
    }
    generator.oas["paths"]["/payments"] = {
        "post": {
            "requestBody": {
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/Payment"},
                        "examples": {"OK": {"value": {"amount": 100}}},
                    }
                }
            },
            "responses": {
                "200": {
                    "description": "OK",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Payment"},
                            "example": {"amount": 100},
                        }
                    },
                }
            },
        }
    }

    generated = yaml.safe_load(generator.get_yaml())
    payment_schema = generated["components"]["schemas"]["Payment"]
    payment_media = generated["paths"]["/payments"]["post"]["requestBody"]["content"]["application/json"]
    response_media = generated["paths"]["/payments"]["post"]["responses"]["200"]["content"]["application/json"]

    assert "example" not in payment_schema
    assert "examples" not in payment_schema
    assert "example" not in payment_schema["properties"]["amount"]
    assert "examples" in payment_schema["properties"]
    assert "example" not in payment_schema["properties"]["examples"]
    assert "examples" not in payment_media
    assert "example" not in response_media


def test_raw_extension_filter_keeps_only_yaml_extension_blocks():
    generator = OASGenerator(generation_mode=GENERATION_MODE_MINIMAL)

    filtered = generator._filter_raw_extensions(
        "\n".join(
            [
                "[240520] - (SS) Description amended - CR5004",
                "x-visible:",
                "  enabled: true",
                "x-sandbox-rule-type: SCRIPT_JS",
            ]
        )
    )

    assert filtered == "x-visible:\n  enabled: true"


def test_paths_parser_does_not_treat_track_changes_as_custom_extensions():
    df = pd.DataFrame(
        [
            {
                "Excel": "updateSettlementBIC.xlsx",
                "Paths": "/updateSettlementBIC/{senderBic}",
                "Unnamed: 3": "put",
                "Unnamed: 4": "Update description",
                "Unnamed: 5": "Participant Management",
                "Unnamed: 6": "Update Settlement BIC",
                "Unnamed: 7": "updateSettlementBIC",
                "Unnamed: 8": "[240520] - (SS) Description amended - CR5004",
            }
        ]
    )

    operations = parse_paths_index(df)

    assert operations[0]["extensions"] is None


def test_legacy_converter_fill_fix_examples_replaces_invalid_bic_and_creates_config():
    temp_root = _clean_test_temp()
    config_path = temp_root / "prefs" / "legacy_example_seed_values.yaml"
    converter = LegacyConverter(
        str(temp_root),
        str(temp_root / "out"),
        fill_fix_examples=True,
        example_seed_values_path=config_path,
    )
    dtype = DataType(
        name="PreferredAgentBIC",
        type="string",
        pattern_eba="[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}",
        example="string",
    )

    try:
        converter._fill_and_fix_examples_for_data_type(dtype)
        examples = dtype.example.split("; ")

        assert config_path.exists()
        assert len(examples) == 3
        assert "string" not in examples
        assert all(re.fullmatch(r"[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}", value) for value in examples)
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


def test_legacy_converter_fill_fix_examples_respects_allowed_values_limit():
    temp_root = _clean_test_temp()
    converter = LegacyConverter(str(temp_root), str(temp_root / "out"), fill_fix_examples=True)
    dtype = DataType(
        name="Status",
        type="string",
        allowed_values="ACTV; INAC",
        example="string",
    )

    try:
        converter._fill_and_fix_examples_for_data_type(dtype)

        assert dtype.example == "ACTV; INAC"
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


def test_legacy_converter_repairs_consolidated_schemas_only_and_defers_example_tracer():
    temp_root = _clean_test_temp()
    detail_lines: list[str] = []
    converter = LegacyConverter(
        str(temp_root),
        str(temp_root / "out"),
        fill_fix_examples=True,
        detail_log_callback=detail_lines.append,
    )
    converter.tracing_enabled = True
    raw_dtype = DataType(
        name="PreferredAgentBIC",
        type="string",
        pattern_eba="[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}",
        example="string",
    )
    consolidated_dtype = DataType(
        name="PreferredAgentBIC",
        type="string",
        pattern_eba="[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}",
        example="string",
    )
    converter.raw_data_types = {"endpoint.xlsx": {"PreferredAgentBIC": raw_dtype}}
    converter.global_schemas = {"PreferredAgentBIC": consolidated_dtype}

    try:
        converter._fill_and_fix_consolidated_examples()

        assert raw_dtype.example == "string"
        assert consolidated_dtype.example != "string"
        assert not any("EXAMPLE TRACER" in line for line in detail_lines)

        converter._log_example_repair_report()

        assert any("EXAMPLE TRACER" in line for line in detail_lines)
        assert any("REPAIRED" in line and "PreferredAgentBIC" in line for line in detail_lines)
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


def test_legacy_converter_uses_plausible_bic8_and_bic11_seed_values():
    temp_root = _clean_test_temp()
    converter = LegacyConverter(str(temp_root), str(temp_root / "out"), fill_fix_examples=True)
    bic8 = DataType(
        name="BIC8",
        type="string",
        pattern_eba="4!c2!a2!c",
        regex="[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}",
        example="AAAAAAAA",
    )
    bic11 = DataType(
        name="BIC11Only",
        type="string",
        pattern_eba="4!c2!a2!c3!c",
        regex="[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}[A-Z0-9]{3,3}",
        example="AAAAAAAAAAA",
    )

    try:
        converter._fill_and_fix_examples_for_data_type(bic8)
        converter._fill_and_fix_examples_for_data_type(bic11)

        bic8_examples = bic8.example.split("; ")
        bic11_examples = bic11.example.split("; ")
        assert bic8_examples == ["IPSDITM1", "DEUTDEFF", "BNPAFRPP"]
        assert bic11_examples == ["IPSDITM1XXX", "DEUTDEFFXXX", "BNPAFRPPXXX"]
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


def test_legacy_converter_converts_eba_pattern_constraints_for_examples():
    converter = LegacyConverter("in", "out", fill_fix_examples=True)
    generic_bic = DataType(
        name="BIC11",
        type="string",
        pattern_eba="4!c2!a2!c[3!c]",
        example="AAAAAAAA",
    )
    bic11_only = DataType(
        name="Bic11Only",
        type="string",
        min_val="11",
        max_val="11",
        pattern_eba="4!c2!a2!c3!c",
        example="AAAAAAAA[A-Z0-9]{3,3}",
    )

    converter._fill_and_fix_examples_for_data_type(generic_bic)
    converter._fill_and_fix_examples_for_data_type(bic11_only)

    assert converter._classify_example_category(generic_bic) == "bic"
    assert generic_bic.example == "IPSDITM1; DEUTDEFFXXX; BNPAFRPP"
    assert bic11_only.example == "IPSDITM1XXX; DEUTDEFFXXX; BNPAFRPPXXX"


def test_legacy_converter_general_bic_semantics_use_mixed_lengths():
    converter = LegacyConverter("in", "out", fill_fix_examples=True)
    receiver_bic = DataType(
        name="ReceiverBic",
        type="string",
        description="The BIC of the message receiver",
        example="",
    )

    converter._fill_and_fix_examples_for_data_type(receiver_bic)

    assert converter._classify_example_category(receiver_bic) == "bic"
    assert receiver_bic.example == "IPSDITM1; DEUTDEFFXXX; BNPAFRPP"


def test_legacy_converter_schema_compaction_renames_block_root_parent_edges():
    converter = LegacyConverter("in", "out")
    blocks = [
        (
            "ProductList14",
            [
                ["ProductList14", "", "", "array", "object", "", "", "", "", "", "", "", "", ""],
                ["solutionPurposeId", "ProductList14", "", "schema", "", "SolutionPurposeId", "", "O", "", "", "", "", "", ""],
                ["pryRcvgNetAd", "ProductList14", "", "schema", "", "PryRcvgNetAd", "", "O", "", "", "", "", "", ""],
            ],
        ),
    ]

    renamed = converter._apply_schema_rename_to_blocks(blocks, {"ProductList14": "ProductList6"})

    assert renamed[0][0] == "ProductList6"
    assert renamed[0][1][0][0] == "ProductList6"
    assert [row[1] for row in renamed[0][1][1:]] == ["ProductList6", "ProductList6"]
    assert [row[5] for row in renamed[0][1][1:]] == ["SolutionPurposeId", "PryRcvgNetAd"]


def test_legacy_converter_repairs_bic_semantic_fields_without_generic_fallback():
    converter = LegacyConverter("in", "out", fill_fix_examples=True)
    cases = [
        (
            DataType(
                name="ReBic",
                type="string",
                description="Reachable Entity BIC (BIC11)",
                pattern_eba="4!c2!a2!c3!c",
                regex=r"[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}([A-Z0-9]{3,3})",
                example="AAAAAAAAAAA",
            ),
            {"bic11"},
        ),
        (
            DataType(
                name="ReceiverBic",
                type="string",
                description="The BIC of the message receiver",
                pattern_eba="4!c2!a2!c",
                regex=r"[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}",
                example="AAAAAAAA",
            ),
            {"bic8"},
        ),
        (
            DataType(
                name="ReachableBic",
                type="string",
                regex=r"[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}([A-Z0-9]{3,3})",
                example="",
            ),
            {"bic11"},
        ),
        (
            DataType(
                name="ReachableEntity",
                type="string",
                description="BIC of the reachable entity (BIC11)",
                pattern_eba="4!c2!a2!c3!c",
                example="AAAAAAAAAAA",
            ),
            {"bic11"},
        ),
        (
            DataType(
                name="FinancialInstitution",
                type="string",
                description="Financial institution BIC",
                pattern_eba="4!c2!a2!c[3!c]",
                example="AAAAAAAA",
            ),
            {"bic", "bic8", "bic11"},
        ),
    ]

    for dt, expected_categories in cases:
        converter._example_trace_rows = []
        converter._fill_and_fix_examples_for_data_type(dt, schema_name=dt.name)

        examples = dt.example.split("; ")
        category = converter._classify_example_category(dt)
        assert category in expected_categories
        assert len(examples) == 3
        assert all(converter._is_valid_example_token(dt, value) for value in examples)
        assert not any(re.fullmatch(r"([A-Z0-9])\1+", value) for value in examples)
        assert converter._example_trace_rows[-1]["reason"].startswith("semantic category: bic")


def test_legacy_converter_regex_example_generation_unescapes_literal_dots():
    converter = LegacyConverter("in", "out", fill_fix_examples=True)
    msg_type = DataType(
        name="msgTp",
        type="string",
        regex=r"(pain\.013){1}|(pain\.014){1}|(pacs\.028){1}|(camt\.055){1}|(camt\.029){1}",
        example="string",
    )

    converter._fill_and_fix_examples_for_data_type(msg_type)

    assert msg_type.example == "pain.013; pain.014; pacs.028"
    assert all(re.fullmatch(msg_type.regex, value) for value in msg_type.example.split("; "))


def test_legacy_converter_regex_example_generation_validates_simple_quantifiers_and_groups():
    converter = LegacyConverter("in", "out", fill_fix_examples=True)
    cases = [
        r"MSG[0-9]{2}",
        r"^MSG[0-9]{2}$",
        r"AB+",
        r"(AB)+",
        r"X[A-Z]*",
        r"A{0,3}",
        r"[^0-9]{3}",
        r"(AA|BB)[0-9]{2}",
        r"ABC\+DEF",
        r"AMOUNT\$",
    ]

    for pattern in cases:
        generated = converter._generate_valid_from_regex(pattern)
        assert generated is not None, pattern
        assert re.fullmatch(pattern, generated), (pattern, generated)


def test_legacy_converter_example_generation_respects_numeric_and_length_constraints():
    converter = LegacyConverter("in", "out", fill_fix_examples=True)
    integer = DataType(name="RetryCount", type="integer", min_val="2.2", max_val="4.8", example="string")
    decimal = DataType(name="Amount", type="number", min_val="10.5", max_val="11.5", example="string")
    short_text = DataType(name="ShortCode", type="string", min_val="3", max_val="5", example="string")
    empty_allowed_text = DataType(name="EmptyString", type="string", min_val="0", max_val="0", example="string")

    converter._fill_and_fix_examples_for_data_type(integer)
    converter._fill_and_fix_examples_for_data_type(decimal)
    converter._fill_and_fix_examples_for_data_type(short_text)
    converter._fill_and_fix_examples_for_data_type(empty_allowed_text)

    assert integer.example == "3"
    assert converter._is_valid_example_token(integer, integer.example)
    assert decimal.example == "11.0"
    assert converter._is_valid_example_token(decimal, decimal.example)
    assert converter._is_valid_example_token(short_text, short_text.example)
    assert 3 <= len(short_text.example) <= 5
    assert empty_allowed_text.example == ""


def test_legacy_converter_does_not_write_best_effort_when_constraints_are_impossible():
    converter = LegacyConverter("in", "out", fill_fix_examples=True)
    impossible_integer = DataType(name="ImpossibleInteger", type="integer", min_val="1.2", max_val="1.8", example="")
    impossible_text = DataType(name="ImpossibleText", type="string", min_val="5", max_val="3", example="")

    converter._fill_and_fix_examples_for_data_type(impossible_integer)
    converter._fill_and_fix_examples_for_data_type(impossible_text)

    assert impossible_integer.example == ""
    assert impossible_text.example == ""
    impossible_rows = [row for row in converter._example_trace_rows if row["action"] == "IMPOSSIBLE"]
    assert len(impossible_rows) == 2
    assert {row["severity"] for row in impossible_rows} == {"impossible"}


def test_legacy_converter_marks_too_complex_regex_examples_in_trace():
    converter = LegacyConverter("in", "out", fill_fix_examples=True)
    complex_regex = DataType(name="ComplexPattern", type="string", regex=r"(?=ABC)ABC", example="string")

    converter._fill_and_fix_examples_for_data_type(complex_regex)

    assert complex_regex.example == ""
    assert converter._example_trace_rows[-1]["action"] == "TOO COMPLEX"
    assert converter._example_trace_rows[-1]["severity"] == "complex"


def test_legacy_converter_boolean_examples_respect_allowed_values():
    converter = LegacyConverter("in", "out", fill_fix_examples=True)
    yes_no = DataType(name="ActiveFlag", type="boolean", allowed_values="yes; no", example="maybe")

    converter._fill_and_fix_examples_for_data_type(yes_no)

    assert yes_no.example == "yes; no"
    assert converter._is_valid_example_set(yes_no, yes_no.example)


def test_legacy_converter_example_tracer_does_not_truncate_values():
    temp_root = _clean_test_temp()
    detail_lines: list[str] = []
    converter = LegacyConverter(
        str(temp_root),
        str(temp_root / "out"),
        fill_fix_examples=True,
        detail_log_callback=detail_lines.append,
    )
    long_after = "banking-data.xml; banking-report.csv; banking-document.txt"

    try:
        converter._record_example_trace(
            "FileName",
            DataType(name="FileName", type="string"),
            "COMPLETED",
            "",
            long_after,
            "semantic category: filename",
        )
        converter._log_example_trace_summary()

        joined = "\n".join(detail_lines)
        assert "banking-data.xml" in joined
        assert "banking-report.csv" in joined
        assert "banking-document.txt" in joined
        assert "..." not in joined
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


def test_legacy_converter_example_tracer_wraps_long_unbroken_values_in_grid():
    detail_lines: list[str] = []
    converter = LegacyConverter("in", "out", fill_fix_examples=True, detail_log_callback=detail_lines.append)
    long_value = (
        "P08M59270578EA544566A8DB7D970D;"
        "P08B59450578EA544526A8DB7D060D;"
        "P08R59805521EA544566A8DB7P998C"
    )
    converter._record_example_trace(
        "MessageId",
        DataType(name="MessageId", type="string"),
        "REPAIRED",
        long_value,
        long_value,
        "semantic category: message_id",
    )

    converter._log_example_trace_summary()

    table_lines = [line for line in detail_lines if line.startswith("| ")]
    assert len(table_lines) > 2
    assert len({len(line) for line in table_lines}) == 1
    assert long_value.replace(";", "") not in "\n".join(table_lines)


def test_legacy_converter_example_tracer_shows_field_usage_context():
    detail_lines: list[str] = []
    converter = LegacyConverter("in", "out", fill_fix_examples=True, detail_log_callback=detail_lines.append)
    converter._record_example_schema_field("BIC8", "InsertSettlementBICRequest.preferredAgentBIC")
    converter._record_example_trace(
        "BIC8",
        DataType(name="BIC8", type="string"),
        "REPAIRED",
        "AAAAAAAA",
        "IPSDITM1; DEUTDEFF; BNPAFRPP",
        "semantic category: bic8",
    )

    converter._log_example_trace_summary()

    joined = "\n".join(detail_lines)
    assert "FIELD/USAGE" in joined
    assert "FIELD USAGE DETAILS" not in joined
    assert "InsertSettlementBICRequest.preferredAgentBIC" in joined


def test_legacy_converter_example_tracer_marks_constraint_severity_lines():
    detail_lines: list[str] = []
    converter = LegacyConverter("in", "out", fill_fix_examples=True, detail_log_callback=detail_lines.append)
    converter._record_example_trace(
        "ImpossibleText",
        DataType(name="ImpossibleText", type="string"),
        "IMPOSSIBLE",
        "",
        "",
        "impossible length range",
        severity="impossible",
    )
    converter._record_example_trace(
        "ComplexPattern",
        DataType(name="ComplexPattern", type="string"),
        "TOO COMPLEX",
        "",
        "",
        "too complex regex",
        severity="complex",
    )

    converter._log_example_trace_summary()

    joined = "\n".join(detail_lines)
    assert "[[OASIS_EXAMPLE_TRACE_IMPOSSIBLE]]" in joined
    assert "[[OASIS_EXAMPLE_TRACE_COMPLEX]]" in joined


def test_legacy_converter_standalone_example_trace_reports_kept_examples():
    temp_root = _clean_test_temp()
    template_path = temp_root / "$index.xlsx"
    detail_lines: list[str] = []
    wb = Workbook()
    ws = wb.active
    ws.title = "Schemas"
    ws.append(["Name", "Parent", "Type", "Pattern", "Example"])
    ws.append(["BIC8", "", "string", "4!c2!a2!c", "IPSDITM1; DEUTDEFF; BNPAFRPP"])
    wb.save(template_path)
    wb.close()

    try:
        converter = LegacyConverter(
            str(temp_root),
            str(temp_root / "out"),
            fill_fix_examples=True,
            log_callback=detail_lines.append,
            detail_log_callback=detail_lines.append,
        )

        assert converter.run_standalone_example_trace(str(temp_root), repair_files=False)

        joined = "\n".join(detail_lines)
        assert "Repair and complete examples: kept 1" in joined
        assert "EXAMPLE TRACER" in joined
        assert "KEPT" in joined
        assert "BIC8" in joined
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


def test_legacy_converter_semantic_classifier_uses_template_wide_categories():
    converter = LegacyConverter("in", "out", fill_fix_examples=True)

    assert converter._classify_example_category(DataType(name="FileStatus", type="string")) == "status"
    assert converter._classify_example_category(DataType(name="FileReference", type="string")) == "reference"
    assert converter._classify_example_category(DataType(name="NetworkFileName", type="string")) == "filename"
    assert converter._classify_example_category(DataType(name="RequestId", type="string")) == "request_id"
    assert converter._classify_example_category(DataType(name="EndToEndId", type="string")) == "transaction_id"
    assert converter._classify_example_category(DataType(name="ModuleIdentifier", type="string")) == "identifier"
    assert converter._classify_example_category(DataType(name="AOSList", type="string")) == "aos"
    assert converter._classify_example_category(DataType(name="FlowIndicator", type="string")) == "flag"
    assert converter._classify_example_category(DataType(name="LSP", type="string", allowed_values="0,1")) == "flag"
    assert converter._classify_example_category(DataType(name="AdmissionProfile", type="string")) == "profile"
    assert converter._classify_example_category(DataType(name="CmndRfrnc", type="string")) == "reference"
    assert converter._classify_example_category(DataType(name="FileTypeList", type="string")) == "type"
    assert converter._classify_example_category(DataType(name="Requestor", type="string")) == "role"
    assert converter._classify_example_category(DataType(name="LacNumber", type="string")) == "lac"
    assert converter._classify_example_category(DataType(name="BeneficiaryName", type="string")) == "name"
    assert converter._classify_example_category(DataType(name="SentReceived", type="string", allowed_values="SNT,RCV")) == "direction"
    assert converter._classify_example_category(DataType(name="UETR", type="string")) == "uuid"
    assert converter._classify_example_category(DataType(name="TotNumOfMsgRcv", type="string")) == "count"
    assert converter._classify_example_category(DataType(name="ErrorDetails", type="string")) == "validation_detail"
    assert converter._classify_example_category(DataType(name="SecRcvgNetAd", type="string")) == "network_address"
    assert converter._classify_example_category(DataType(name="FreezeUnfreeze", type="string")) == "operation"
    assert converter._classify_example_category(DataType(name="XmlMsgSts", type="string")) == "status"
    assert converter._classify_example_category(DataType(name="XmlStsRsn", type="string")) == "reason"
    assert converter._classify_example_category(DataType(name="PryApiEndpoint", type="string")) == "endpoint"
    assert converter._classify_example_category(DataType(name="MaxFileSize", type="string")) == "file_size"
    assert converter._classify_example_category(DataType(name="Account", type="string")) == "account"
    assert converter._classify_example_category(
        DataType(name="AccptncDtTm", type="string", pattern_eba="YYYY-MM-DDTHH:MM:SS[.M{1,6}]")
    ) == "datetime"
    assert converter._classify_example_category(
        DataType(
            name="dataTime",
            type="string",
            regex=r"[0-9]{4,4}-[0-9]{2,2}-[0-9]{2,2}[T][0-9]{2,2}:[0-9]{2,2}:[0-9]{2,2}",
        )
    ) == "datetime"


def test_legacy_converter_datetime_regex_drives_realistic_examples():
    converter = LegacyConverter("in", "out", fill_fix_examples=True)
    data_time = DataType(
        name="dataTime",
        type="string",
        regex=r"[0-9]{4,4}-[0-9]{2,2}-[0-9]{2,2}[T][0-9]{2,2}:[0-9]{2,2}:[0-9]{2,2}",
        example="1111-11-11T11:11:11A1",
    )

    converter._fill_and_fix_examples_for_data_type(data_time)

    examples = data_time.example.split("; ")
    assert examples == [
        "2026-01-31T10:15:30",
        "2026-06-30T12:00:00",
        "2026-12-31T23:59:59",
    ]
    assert all(converter._is_valid_example_token(data_time, value) for value in examples)


def test_legacy_converter_semantic_classifier_uses_configured_overrides_and_rules():
    temp_root = _clean_test_temp()
    rules_path = temp_root / "prefs" / "legacy_example_semantic_rules.yaml"
    rules_path.parent.mkdir(parents=True)
    rules_path.write_text(
        yaml.safe_dump(
            {
                "overrides": {
                    "exact": {"LSP": "service"},
                    "compact_exact": {"Instruction": "instruction_id"},
                },
                "rules": [
                    {"category": "channel", "compact_exact": ["accesspoint"]},
                ],
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    converter = LegacyConverter(
        str(temp_root),
        str(temp_root / "out"),
        fill_fix_examples=True,
        example_semantic_rules_path=rules_path,
    )

    try:
        assert converter._classify_example_category(DataType(name="LSP", type="string", allowed_values="0,1")) == "service"
        assert converter._classify_example_category(DataType(name="Instruction", type="string")) == "instruction_id"
        assert converter._classify_example_category(DataType(name="AccessPoint", type="string")) == "channel"
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


def test_legacy_converter_semantic_classifier_creates_default_rules_config():
    temp_root = _clean_test_temp()
    rules_path = temp_root / "prefs" / "legacy_example_semantic_rules.yaml"
    converter = LegacyConverter(
        str(temp_root),
        str(temp_root / "out"),
        fill_fix_examples=True,
        example_semantic_rules_path=rules_path,
    )

    try:
        assert converter._classify_example_category(DataType(name="RequestId", type="string")) == "request_id"
        assert rules_path.exists()
        loaded = yaml.safe_load(rules_path.read_text(encoding="utf-8"))
        assert "rules" in loaded
        assert "overrides" in loaded
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


def test_legacy_converter_standalone_example_trace_repairs_template_schema_examples():
    temp_root = _clean_test_temp()
    template_path = temp_root / "$index.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Schemas"
    ws.append(["Name", "Parent", "Type", "Pattern", "Example"])
    ws.append(["PreferredAgentBIC", "", "string", "[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}", "string"])
    wb.save(template_path)
    wb.close()

    try:
        converter = LegacyConverter(str(temp_root), str(temp_root / "out"), fill_fix_examples=True)
        assert converter.run_standalone_example_trace(str(temp_root), repair_files=True)

        repaired_wb = load_workbook(template_path)
        try:
            repaired = repaired_wb["Schemas"].cell(row=2, column=5).value
        finally:
            repaired_wb.close()

        assert repaired != "string"
        assert all(re.fullmatch(r"[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}", value) for value in repaired.split("; "))
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


def test_legacy_converter_blocks_conversion_when_index_references_missing_file():
    temp_root = _clean_test_temp()
    index_path = temp_root / "$index.xlsx"
    logs: list[str] = []
    wb = Workbook()
    ws = wb.active
    ws.title = "Paths"
    ws.append(["Path", "Method", "Excel File", "OperationId"])
    ws.append(["/missing", "get", "listLCR.260424", "listLCR"])
    wb.save(index_path)
    wb.close()

    try:
        converter = LegacyConverter(str(temp_root), str(temp_root / "out"), log_callback=logs.append)

        assert converter.convert() is False
        assert converter.missing_index_files == ["listLCR.260424"]
        assert any("ERROR: $index.xlsx references missing endpoint templates" in line for line in logs)
        assert any("ERROR: Conversion aborted because $index.xlsx references missing endpoint templates." in line for line in logs)
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)
