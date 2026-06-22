from pathlib import Path

import pytest
import yaml

from src.api_designer.oas_importer import import_oas_file_to_workspace


FPAD_OAS_PATH = Path(
    r"C:\EBA Clearing\APIs\Generated OAS\FPAD API Participants\2026-Q4\EBACL_FPAD_20260330_OpenApi3.1_FPAD_API_Participant_5.1.0_v20260418.yaml"
)


@pytest.mark.skipif(not FPAD_OAS_PATH.exists(), reason="FPAD OAS file not available on this machine")
def test_import_fpad_oas_roundtrips_without_information_loss():
    original = yaml.safe_load(FPAD_OAS_PATH.read_text(encoding="utf-8"))

    workspace = import_oas_file_to_workspace(FPAD_OAS_PATH)
    assert len(workspace.apis) == 1

    api = workspace.apis[0]

    assert api.openapi_version == original["openapi"]
    assert api.info == original["info"]
    assert api.servers == original["servers"]
    assert api.tags == original["tags"]
    assert len(api.path_items) == len(original["paths"])
    assert api.local_components == original["components"]

    assert api.to_oas_dict() == original
