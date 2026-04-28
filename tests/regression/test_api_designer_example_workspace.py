from pathlib import Path

from src.api_designer.persistence import FileSystemDesignerRepository


def test_api_designer_example_workspace_loads():
    root = Path(__file__).resolve().parents[2]
    example_root = root / "docs" / "examples" / "api_designer" / "payments_demo_workspace"

    workspace = FileSystemDesignerRepository(example_root).load_workspace()

    assert workspace.name == "Payments Demo Workspace"
    assert len(workspace.apis) == 1
    assert workspace.apis[0].name == "Payments API"
    assert len(workspace.apis[0].path_items) == 3
    assert workspace.changes[0].steps[0].kind == "add_path"
