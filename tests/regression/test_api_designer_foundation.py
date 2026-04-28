from pathlib import Path
import shutil

import yaml

from src.api_designer.models import Change, ChangeStep, create_empty_workspace
from src.api_designer.persistence import FileSystemDesignerRepository


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
