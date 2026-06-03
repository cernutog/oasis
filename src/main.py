import os
import sys
import pandas as pd
from pathlib import Path

# Add src to path if needed or assume relative imports work if run as module
# If run as script, parser/generator are in same dir.
# Standard relative imports for package structure
from . import excel_parser as parser
from .generator import OASGenerator
from .preferences import DEFAULT_GENERATION_MODE, normalize_generation_mode, normalize_x_info_options


INDEX_FILENAME = "$index.xlsx"
LEGACY_INDEX_FILENAME = "$index.xlsm"
REQUIRED_INDEX_SHEETS = (
    "General Description",
    "Tags",
    "Paths",
    "Parameters",
    "Headers",
    "Schemas",
    "Responses",
)
REQUIRED_OPERATION_SHEETS = ("Parameters",)


def find_best_match_file(target, directory, files_list):
    # Delegate to parser's logic or reimplement simple one
    return parser.find_best_match_file(target, directory, files_list)


def _excel_sheet_names(path):
    xl = None
    try:
        xl = pd.ExcelFile(path)
        return set(xl.sheet_names)
    finally:
        if xl is not None:
            xl.close()


def _format_missing_sheets_error(template_path, missing_sheets):
    return [
        "ERROR: Invalid converted template structure.",
        f"Template: {template_path}",
        f"Missing sheet(s): {', '.join(sorted(missing_sheets))}",
        "Please make sure the selected folder contains a complete set of valid templates.",
    ]


def get_converted_template_validation_errors(base_dir):
    """Return blocking validation errors for an OAS Generation input folder."""
    base_path = Path(base_dir)
    index_path = base_path / INDEX_FILENAME
    legacy_index_path = base_path / LEGACY_INDEX_FILENAME

    if not index_path.exists():
        errors = ["ERROR: OAS Generation requires valid templates with $index.xlsx."]
        if legacy_index_path.exists():
            errors.append("The selected folder appears to contain legacy templates ($index.xlsm).")
        errors.append("Please select a folder containing a complete set of valid templates.")
        return errors

    try:
        index_sheet_names = _excel_sheet_names(index_path)
    except Exception as exc:
        return [
            "ERROR: Invalid converted template structure.",
            f"Template: {index_path}",
            f"Cannot read workbook: {exc}",
            "Please make sure the selected folder contains a complete set of valid templates.",
        ]

    missing_index_sheets = [name for name in REQUIRED_INDEX_SHEETS if name not in index_sheet_names]
    if missing_index_sheets:
        return _format_missing_sheets_error(index_path, missing_index_sheets)

    df_paths = parser.load_excel_sheet(index_path, "Paths")
    paths_list = parser.parse_paths_index(df_paths)
    endpoint_files = sorted(
        {
            str(op.get("file")).strip()
            for op in paths_list
            if op.get("file") is not None and not pd.isna(op.get("file")) and str(op.get("file")).strip()
        }
    )

    errors = []
    for raw_file_name in endpoint_files:
        endpoint_path = base_path / raw_file_name
        if not endpoint_path.exists():
            errors.extend(
                [
                    "ERROR: Invalid converted template structure.",
                    f"Template: {index_path}",
                    f"Missing endpoint file: {raw_file_name}",
                    "Please make sure the selected folder contains a complete set of valid templates.",
                ]
            )
            continue

        try:
            endpoint_sheet_names = _excel_sheet_names(endpoint_path)
        except Exception as exc:
            errors.extend(
                [
                    "ERROR: Invalid converted template structure.",
                    f"Template: {endpoint_path}",
                    f"Cannot read workbook: {exc}",
                    "Please make sure the selected folder contains a complete set of valid templates.",
                ]
            )
            continue

        missing_endpoint_sheets = [
            name for name in REQUIRED_OPERATION_SHEETS if name not in endpoint_sheet_names
        ]
        has_response_sheet = any(name.isdigit() for name in endpoint_sheet_names)
        if not has_response_sheet:
            missing_endpoint_sheets.append("<response sheet>")
        if missing_endpoint_sheets:
            errors.extend(_format_missing_sheets_error(endpoint_path, missing_endpoint_sheets))

    return errors


def generate_oas(
    base_dir,
    gen_30=True,
    gen_31=True,
    gen_swift=False,
    generation_mode=DEFAULT_GENERATION_MODE,
    x_info_options=None,
    output_dir=None,
    log_callback=print,
):
    """
    Main execution function.
    base_dir: Directory containing '$index.xlsm'
    output_dir: Directory to write generated OAS files (defaults to base_dir/generated if None)
    """
    if not os.path.exists(base_dir):
        log_callback(f"Error: Directory not found: {base_dir}")
        return

    validation_errors = get_converted_template_validation_errors(base_dir)
    if validation_errors:
        for error in validation_errors:
            log_callback(error)
        return

    generation_mode = normalize_generation_mode(generation_mode)
    x_info_options = normalize_x_info_options(x_info_options)
    log_callback(f"Starting generation in: {base_dir}")
    log_callback(f"Generation mode: {generation_mode}")

    # 1. Setup Paths
    index_path = os.path.join(base_dir, INDEX_FILENAME)

    # 2. Parse Master Index
    log_callback(f"Parsing index: {os.path.basename(index_path)}")
    df_info = parser.load_excel_sheet(index_path, "General Description")
    info_data, inline_servers = parser.parse_info(df_info)
    swift_servers_data = info_data.get("swift_servers", [])

    df_tags = parser.load_excel_sheet(index_path, "Tags")
    tags_data = parser.parse_tags(df_tags)

    # Parse Servers and Security
    servers_data = parser.parse_servers(parser.load_excel_sheet(index_path, "Servers"))
    if not servers_data and inline_servers:
        servers_data = inline_servers

    security_schemes, security_req = parser.parse_security(
        parser.load_excel_sheet(index_path, "Security")
    )

    df_paths = parser.load_excel_sheet(index_path, "Paths")
    paths_list = parser.parse_paths_index(df_paths)

    components_data = parser.parse_components(index_path)  # Global components

    # 3. Parse Operation Files
    log_callback("Parsing operation details...")
    operations_details = {}

    # Identify unique files to parse
    unique_files = set()
    for op in paths_list:
        if op.get("file"):
            unique_files.add(op.get("file"))

    for raw_file_name in unique_files:
        if not raw_file_name:
            continue
        full_path = os.path.join(base_dir, raw_file_name)
        if os.path.exists(full_path):
            # log_callback(f"  Parsing: {os.path.basename(full_path)}")
            op_det = parser.parse_operation_file(full_path)
            if op_det:
                operations_details[raw_file_name] = op_det
        else:
            log_callback(f"  Operation file not found for: {raw_file_name}")

    # Output Directory: Use provided output_dir or fall back to base_dir/generated
    if output_dir is None:
        gen_dir = os.path.join(base_dir, "generated")
    else:
        gen_dir = output_dir

    schema_parent_issues = {}

    def collect_schema_parent_issues(generator):
        for issue in generator.get_schema_parent_issues():
            key = (
                issue.get("severity"),
                issue.get("schema"),
                issue.get("field"),
                issue.get("parent"),
                issue.get("status"),
            )
            schema_parent_issues[key] = issue

    def format_schema_parent_issue(issue):
        severity = issue.get("severity", "WARNING")
        schema = issue.get("schema", "<schema>")
        field = issue.get("field", "<field>")
        parent = issue.get("parent", "<parent>")
        return (
            f"[{severity}] {schema}.{field} has a wrong parent ({parent}). "
            "Fallback applied but correct result is not guaranteed."
        )

    def log_schema_parent_issue_report():
        if not schema_parent_issues:
            return

        issues = sorted(
            schema_parent_issues.values(),
            key=lambda item: (
                item.get("schema", ""),
                item.get("field", ""),
                item.get("parent", ""),
                item.get("severity", ""),
            ),
        )
        log_callback("")
        log_callback("=== TEMPLATE ISSUES: BAD PARENTS ===")
        log_callback(f"{len(issues)} wrong parent reference(s) found.")
        log_callback("+-- ACTION REQUIRED ----------------------------------------+")
        log_callback("| Fix the Parent column in $index.xlsx, sheet Schemas.      |")
        log_callback("| Then regenerate the OAS.                                  |")
        log_callback("+-----------------------------------------------------------+")
        log_callback("")

        current_schema = None
        for issue in issues:
            schema = issue.get("schema", "<schema>")
            if schema != current_schema:
                if current_schema is not None:
                    log_callback("")
                current_schema = schema
                log_callback(f"Schema {schema}")
            log_callback(f"  - {format_schema_parent_issue(issue)}")
        log_callback("")

    # Output Map Directory and Cleanup
    map_dir = os.path.join(gen_dir, ".oasis_excel_maps")
    os.makedirs(map_dir, exist_ok=True)

    # Cleanup Orphan Maps
    try:
        for map_file in os.listdir(map_dir):
            if map_file.endswith(".map.json"):
                # derived from assumptions: name + .map.json
                parent_yaml_name = map_file.replace(".map.json", "")
                parent_yaml_path = os.path.join(gen_dir, parent_yaml_name)
                if not os.path.exists(parent_yaml_path):
                    try:
                        os.remove(os.path.join(map_dir, map_file))
                        log_callback(f"Cleaned up orphan map: {map_file}")
                    except OSError:
                        pass
    except OSError:
        pass

    def build_filename(oas_ver, customization=""):
        pattern = info_data.get("filename_pattern")
        if not pattern or pd.isna(pattern):
            # Fallback to legacy naming if pattern missing
            suffix = "_SWIFT" if customization else ""
            return f"generated_oas_{oas_ver}{suffix}.yaml"

        # Placeholders
        # <current_date>
        from datetime import datetime

        now_str = datetime.now().strftime("%Y%m%d")

        # <oas_version>
        ver_str = oas_ver  # "3.0" or "3.1"

        # <customization>
        cust_str = f"{customization}_" if customization else ""

        # <api_version>
        api_ver = info_data.get("version", "1.0")

        # <release>
        release_str = info_data.get("release", "")

        fname = (
            pattern.replace("<current_date>", now_str)
            .replace("<oas_version>", ver_str)
            .replace("<customization>", cust_str)
            .replace("<api_version>", api_ver)
            .replace("<release>", release_str)
        )

        return fname.strip()

    # Prepare Clean Info (Exclude internal fields)
    clean_info = info_data.copy()
    for internal_key in ["filename_pattern", "swift_servers"]:
        clean_info.pop(internal_key, None)

    # 4. Generate OAS 3.0
    if gen_30:
        log_callback("Generating OAS 3.0...")
        generator_30 = OASGenerator(
            version="3.0.0",
            generation_mode=generation_mode,
            log_callback=log_callback,
            x_info_options=x_info_options,
        )
        generator_30.build_info(clean_info)
        # Always record tags source - needed for validation warnings even when tags are empty
        generator_30._record_source("tags", "$index.xlsx", "Tags")
        if tags_data:
            generator_30.oas["tags"] = tags_data
        if servers_data:
            generator_30.oas["servers"] = servers_data
        if security_req:
            generator_30.oas["security"] = security_req

        # Add Security Schemes to Components
        if security_schemes:
            if "securitySchemes" not in components_data:
                components_data["securitySchemes"] = {}
            components_data["securitySchemes"].update(security_schemes)

            components_data["securitySchemes"].update(security_schemes)

        generator_30.build_components(components_data, source_file=os.path.basename(index_path))
        generator_30.build_paths(paths_list, operations_details)

        # Ensure OAS output folder exists
        os.makedirs(gen_dir, exist_ok=True)

        fname_30 = build_filename("3.0")
        out_30 = Path(gen_dir) / fname_30
        log_callback(f"Writing OAS 3.0 to: {out_30.as_posix()}")
        with open(out_30, "w", encoding="utf-8") as f:
            f.write(generator_30.get_yaml())

        # Write Source Map
        map_30 = Path(map_dir) / (fname_30 + ".map.json")
        with open(map_30, "w", encoding="utf-8") as f:
            f.write(generator_30.get_source_map_json())
        collect_schema_parent_issues(generator_30)

    # 5. Generate OAS 3.1
    if gen_31:
        log_callback("Generating OAS 3.1...")
        generator_31 = OASGenerator(
            version="3.1.0",
            generation_mode=generation_mode,
            log_callback=log_callback,
            x_info_options=x_info_options,
        )
        generator_31.build_info(clean_info)
        # Always record tags source - needed for validation warnings even when tags are empty
        generator_31._record_source("tags", "$index.xlsx", "Tags")
        if tags_data:
            generator_31.oas["tags"] = tags_data
        if servers_data:
            generator_31.oas["servers"] = servers_data
        if security_req:
            generator_31.oas["security"] = security_req

        generator_31.build_components(components_data, source_file=os.path.basename(index_path))
        generator_31.build_paths(paths_list, operations_details)

        # Ensure OAS output folder exists
        os.makedirs(gen_dir, exist_ok=True)

        fname_31 = build_filename("3.1")
        out_31 = Path(gen_dir) / fname_31
        log_callback(f"Writing OAS 3.1 to: {out_31.as_posix()}")
        with open(out_31, "w", encoding="utf-8") as f:
            f.write(generator_31.get_yaml())

        # Write Source Map
        map_31 = Path(map_dir) / (fname_31 + ".map.json")
        with open(map_31, "w", encoding="utf-8") as f:
            f.write(generator_31.get_source_map_json())
        collect_schema_parent_issues(generator_31)

    # 6. Generate SWIFT OAS (Customized)
    if gen_swift:
        # SWIFT OAS 3.0
        log_callback("Generating SWIFT OAS 3.0...")
        sw_gen_30 = OASGenerator(
            version="3.0.0",
            generation_mode=generation_mode,
            log_callback=log_callback,
            x_info_options=x_info_options,
        )
        sw_gen_30.build_info(clean_info)
        if tags_data:
            sw_gen_30.oas["tags"] = tags_data
        if servers_data:
            sw_gen_30.oas["servers"] = servers_data
        if security_req:
            sw_gen_30.oas["security"] = security_req

        if security_schemes:
            if "securitySchemes" not in components_data:
                components_data["securitySchemes"] = {}
            components_data["securitySchemes"].update(security_schemes)

        sw_gen_30.build_components(components_data, source_file=os.path.basename(index_path))
        sw_gen_30.build_paths(paths_list, operations_details)

        # APPLY CUSTOMIZATION
        # Pass the filename of the corresponding standard OAS
        sw_gen_30.apply_swift_customization(
            source_filename=build_filename("3.0"),
            swift_servers=swift_servers_data,
        )

        # Ensure OAS output folder exists
        os.makedirs(gen_dir, exist_ok=True)

        out_sw_30 = Path(gen_dir) / build_filename("3.0", "SWIFT")
        log_callback(f"Writing OAS 3.0 (SWIFT) to: {out_sw_30.as_posix()}")
        with open(out_sw_30, "w", encoding="utf-8") as f:
            f.write(sw_gen_30.get_yaml())

        # Write Source Map
        map_sw_30 = Path(map_dir) / (out_sw_30.name + ".map.json")
        with open(map_sw_30, "w", encoding="utf-8") as f:
            f.write(sw_gen_30.get_source_map_json())
        collect_schema_parent_issues(sw_gen_30)

        # SWIFT OAS 3.1
        log_callback("Generating SWIFT OAS 3.1...")
        sw_gen_31 = OASGenerator(
            version="3.1.0",
            generation_mode=generation_mode,
            log_callback=log_callback,
            x_info_options=x_info_options,
        )
        sw_gen_31.build_info(clean_info)
        if tags_data:
            sw_gen_31.oas["tags"] = tags_data
        if servers_data:
            sw_gen_31.oas["servers"] = servers_data
        if security_req:
            sw_gen_31.oas["security"] = security_req

        sw_gen_31.build_components(components_data, source_file=os.path.basename(index_path))
        sw_gen_31.build_paths(paths_list, operations_details)

        # APPLY CUSTOMIZATION
        # Pass the filename of the corresponding standard OAS
        sw_gen_31.apply_swift_customization(
            source_filename=build_filename("3.1"),
            swift_servers=swift_servers_data,
        )

        out_sw_31 = Path(gen_dir) / build_filename("3.1", "SWIFT")
        log_callback(f"Writing OAS 3.1 (SWIFT) to: {out_sw_31.as_posix()}")
        with open(out_sw_31, "w", encoding="utf-8") as f:
            f.write(sw_gen_31.get_yaml())
        
        # Write Source Map
        map_sw_31 = Path(map_dir) / (out_sw_31.name + ".map.json")
        with open(map_sw_31, "w", encoding="utf-8") as f:
            f.write(sw_gen_31.get_source_map_json())
        collect_schema_parent_issues(sw_gen_31)

    log_schema_parent_issue_report()
    log_callback("\n=== OAS GENERATION COMPLETED ===\n")


def main():
    import customtkinter as ctk
    import os
    import sys
    import tkinter.messagebox
    from customtkinter import ThemeManager

    # 1. SETUP THEME BEFORE IMPORTING GUI (Prevents default blue init)
    ctk.set_appearance_mode("System")
    
    theme_loaded = False
    try:
        if getattr(sys, 'frozen', False):
            # PyInstaller mode
            theme_path = os.path.join(sys._MEIPASS, "src", "resources", "oasis_theme.json")
        else:
            # Dev mode
            theme_path = os.path.join(os.path.dirname(__file__), "resources", "oasis_theme.json")
            
        if os.path.exists(theme_path):
            ctk.set_default_color_theme(theme_path)
            theme_loaded = True
        else:
            tkinter.messagebox.showwarning("Theme Error", f"Theme file missing at:\n{theme_path}")
            ctk.set_default_color_theme("blue")
            
    except Exception as e:
        tkinter.messagebox.showerror("Theme Exception", f"Error setting theme:\n{e}")
        ctk.set_default_color_theme("blue")

    # 2. IMPORT GUI NOW
    try:
        from src.gui import OASGenApp
    except ImportError:
        try:
            from gui import OASGenApp
        except ImportError:
            sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
            from src.gui import OASGenApp

    app = OASGenApp()
    
    # 3. RUNTIME FALLBACK CHECK (The "Nuclear Option")
    # If the button color is still Blue (#3B8ED0 is standard CTk Blue), force it.
    try:
        current_fg = ThemeManager.theme["CTkButton"]["fg_color"]
        # Standard Blue is usually ["#3B8ED0", "#1F6AA5"]
        if "#3B8ED0" in str(current_fg) or "3B8ED0" in str(current_fg):
            # Force Petrol Blue Override
            PETROL = "#0A809E"
            HOVER = "#076075"
            
            ThemeManager.theme["CTkButton"]["fg_color"] = [PETROL, PETROL]
            ThemeManager.theme["CTkButton"]["hover_color"] = [HOVER, HOVER]
            ThemeManager.theme["CTkSlider"]["button_color"] = [PETROL, PETROL]
            ThemeManager.theme["CTkSlider"]["progress_color"] = [PETROL, PETROL]
            ThemeManager.theme["CTkCheckBox"]["fg_color"] = [PETROL, PETROL]
            ThemeManager.theme["CTkCheckBox"]["hover_color"] = [HOVER, HOVER]
            # Force refresh if app already drew? No, app didn't mainloop yet.
    except Exception:
        pass

    app.mainloop()


if __name__ == "__main__":
    main()
