from pathlib import Path

import pytest

from src.gui import clean_oas_import_output_folder


def test_oas_import_clear_excel_reports_locked_files(tmp_path, monkeypatch):
    output_dir = tmp_path / "templates"
    output_dir.mkdir()
    locked_file = output_dir / "create-account-assessment-vop.260526.xlsx"
    locked_file.write_text("stale workbook", encoding="utf-8")

    def deny_remove(path):
        if Path(path) == locked_file:
            raise PermissionError("locked")

    monkeypatch.setattr("src.gui.os.remove", deny_remove)

    with pytest.raises(PermissionError) as exc_info:
        clean_oas_import_output_folder(str(output_dir), "clear_excel")

    assert str(locked_file) in str(exc_info.value)
