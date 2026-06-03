from src import main as main_script


def test_generate_oas_builds_components_before_paths(monkeypatch, tmp_path):
    base_dir = tmp_path / "templates"
    base_dir.mkdir()
    (base_dir / "$index.xlsx").write_text("", encoding="utf-8")
    (base_dir / "operation.xlsx").write_text("", encoding="utf-8")
    output_dir = tmp_path / "generated"

    monkeypatch.setattr(main_script, "get_converted_template_validation_errors", lambda _base_dir: [])
    monkeypatch.setattr(main_script.parser, "load_excel_sheet", lambda *_args, **_kwargs: object())
    monkeypatch.setattr(
        main_script.parser,
        "parse_info",
        lambda _df: (
            {
                "title": "Test API",
                "version": "1.0",
                "filename_pattern": "test_<oas_version>_<customization><api_version>_<release>.yaml",
                "release": "r1",
            },
            [],
        ),
    )
    monkeypatch.setattr(main_script.parser, "parse_tags", lambda _df: [])
    monkeypatch.setattr(main_script.parser, "parse_servers", lambda _df: [])
    monkeypatch.setattr(main_script.parser, "parse_security", lambda _df: ({}, []))
    monkeypatch.setattr(
        main_script.parser,
        "parse_paths_index",
        lambda _df: [
            {
                "file": "operation.xlsx",
                "path": "/v1/test",
                "method": "get",
            }
        ],
    )
    monkeypatch.setattr(
        main_script.parser,
        "parse_components",
        lambda _path: {
            "parameters": object(),
            "headers": object(),
            "schemas": object(),
            "responses": object(),
        },
    )
    monkeypatch.setattr(main_script.parser, "parse_operation_file", lambda _path: {"parameters": object()})

    class RecordingGenerator:
        instances = []

        def __init__(self, version, generation_mode, log_callback, x_info_options):
            self.version = version
            self.events = []
            self.oas = {"components": {"parameters": {}, "headers": {}, "schemas": {}, "responses": {}}}
            RecordingGenerator.instances.append(self)

        def build_info(self, _info):
            self.events.append("info")

        def _record_source(self, *_args):
            self.events.append("source")

        def build_components(self, *_args, **_kwargs):
            self.events.append("components")

        def build_paths(self, *_args, **_kwargs):
            self.events.append("paths")

        def apply_swift_customization(self, *_args, **_kwargs):
            self.events.append("swift")

        def get_yaml(self):
            return "openapi: 3.0.0\n"

        def get_source_map_json(self):
            return "{}"

        def get_schema_parent_issues(self):
            return []

    monkeypatch.setattr(main_script, "OASGenerator", RecordingGenerator)

    main_script.generate_oas(
        str(base_dir),
        gen_30=True,
        gen_31=True,
        gen_swift=True,
        output_dir=str(output_dir),
        log_callback=lambda _msg: None,
    )

    assert len(RecordingGenerator.instances) == 4
    for generator in RecordingGenerator.instances:
        assert "components" in generator.events
        assert "paths" in generator.events
        assert generator.events.index("components") < generator.events.index("paths"), generator.events
