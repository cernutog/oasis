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

    assert generic_bic.example == "IPSDITM1XXX; DEUTDEFFXXX; BNPAFRPPXXX"
    assert bic11_only.example == "IPSDITM1XXX; DEUTDEFFXXX; BNPAFRPPXXX"


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
