import os
import sys


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


from src.gui import OASGenApp


class _DummyEntry:
    def __init__(self, value):
        self.value = str(value)

    def get(self):
        return self.value


class _DummyCombo:
    def __init__(self):
        self.values = []
        self.selected = None

    def configure(self, **kwargs):
        if "values" in kwargs:
            self.values = list(kwargs["values"])

    def set(self, value):
        self.selected = value


class _DummyPrefs:
    def get(self, key, default=None):
        return default


class _DummyTabView:
    def __init__(self, current):
        self.current = current

    def get(self):
        return self.current


class _DummyMenu:
    def entryconfig(self, *args, **kwargs):
        pass


def test_validation_file_list_reads_validation_folder(tmp_path):
    generation_dir = tmp_path / "generation"
    validation_dir = tmp_path / "validation"
    generation_dir.mkdir()
    validation_dir.mkdir()
    (validation_dir / "api.yaml").write_text("openapi: 3.1.0\n", encoding="utf-8")

    app = object.__new__(OASGenApp)
    app.entry_oas_folder = _DummyEntry(generation_dir)
    app.entry_val_oas_folder = _DummyEntry(validation_dir)
    app.last_generated_files = []
    app.prefs_manager = _DummyPrefs()
    app.cbo_files = _DummyCombo()
    app.refresh_view_files = lambda: None

    app.update_file_list()

    assert app.cbo_files.values == ["api.yaml"]
    assert app.cbo_files.selected == "api.yaml"
    assert app.file_map["api.yaml"] == str(validation_dir / "api.yaml")


def test_switching_to_validation_refreshes_file_list_before_validation():
    app = object.__new__(OASGenApp)
    app.tabview = _DummyTabView("Validation")
    app.file_menu = _DummyMenu()
    calls = []

    app.update_file_list = lambda: calls.append("update_file_list")
    app.run_validation = lambda: calls.append("run_validation")

    app._on_tab_change()

    assert calls == ["update_file_list", "run_validation"]
