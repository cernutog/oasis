import os
import sys
import pandas as pd

# Add src to path if needed or assume relative imports work if run as module
# If run as script, parser/generator are in same dir.
# Standard relative imports for package structure
from . import excel_parser as parser
from .generator import OASGenerator


def find_best_match_file(target, directory, files_list):
    # Delegate to parser's logic or reimplement simple one
    return parser.find_best_match_file(target, directory, files_list)


def generate_oas(
    base_dir,
    gen_30=True,
    gen_31=True,
    gen_swift=False,
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

    log_callback(f"Starting generation in: {base_dir}")

    # 1. Setup Paths
    files_in_dir = os.listdir(base_dir)
    
    # Look for $index.xlsx directly (project standard is .xlsx, not .xlsm)
    index_filename = "$index.xlsx"
    if index_filename in files_in_dir:
        index_path = os.path.join(base_dir, index_filename)
    else:
        # Fallback to fuzzy match for legacy support
        index_path = find_best_match_file("$index.xlsx", base_dir, files_in_dir)
    
    if not index_path:
        log_callback("Error: $index.xlsx not found in the specified directory.")
        return

    # 2. Parse Master Index
    log_callback(f"Parsing index: {os.path.basename(index_path)}")
    df_info = parser.load_excel_sheet(index_path, "General Description")
    info_data, inline_servers = parser.parse_info(df_info)

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
        full_path = find_best_match_file(raw_file_name, base_dir, files_in_dir)
        if full_path:
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
    for internal_key in ["release", "filename_pattern"]:
        clean_info.pop(internal_key, None)

    # 4. Generate OAS 3.0
    if gen_30:
        log_callback("Generating OAS 3.0...")
        generator_30 = OASGenerator(version="3.0.0")
        generator_30.build_info(clean_info)
        if tags_data:
            generator_30.oas["tags"] = tags_data
        if servers_data:
            generator_30.oas["servers"] = servers_data
        if security_req:
            generator_30.oas["security"] = security_req

        generator_30.build_paths(paths_list, operations_details)

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
        out_30 = os.path.join(gen_dir, fname_30)
        log_callback(f"Writing OAS 3.0 to: {out_30}")
        with open(out_30, "w", encoding="utf-8") as f:
            f.write(generator_30.get_yaml())

        # Write Source Map
        map_30 = os.path.join(map_dir, fname_30 + ".map.json")
        with open(map_30, "w", encoding="utf-8") as f:
            f.write(generator_30.get_source_map_json())

    # 5. Generate OAS 3.1
    if gen_31:
        log_callback("Generating OAS 3.1...")
        generator_31 = OASGenerator(version="3.1.0")
        generator_31.build_info(clean_info)
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
        out_31 = os.path.join(gen_dir, fname_31)
        log_callback(f"Writing OAS 3.1 to: {out_31}")
        with open(out_31, "w", encoding="utf-8") as f:
            f.write(generator_31.get_yaml())

        # Write Source Map
        map_31 = os.path.join(map_dir, fname_31 + ".map.json")
        with open(map_31, "w", encoding="utf-8") as f:
            f.write(generator_31.get_source_map_json())

    # 6. Generate SWIFT OAS (Customized)
    if gen_swift:
        # SWIFT OAS 3.0
        log_callback("Generating SWIFT OAS 3.0...")
        sw_gen_30 = OASGenerator(version="3.0.0")
        sw_gen_30.build_info(clean_info)
        if tags_data:
            sw_gen_30.oas["tags"] = tags_data
        if servers_data:
            sw_gen_30.oas["servers"] = servers_data
        if security_req:
            sw_gen_30.oas["security"] = security_req

        sw_gen_30.build_paths(paths_list, operations_details)
        if security_schemes:
            if "securitySchemes" not in components_data:
                components_data["securitySchemes"] = {}
            components_data["securitySchemes"].update(security_schemes)

        sw_gen_30.build_components(components_data, source_file=os.path.basename(index_path))
        sw_gen_30.build_paths(paths_list, operations_details)

        # APPLY CUSTOMIZATION
        # Pass the filename of the corresponding standard OAS
        sw_gen_30.apply_swift_customization(source_filename=build_filename("3.0"))

        # Ensure OAS output folder exists
        os.makedirs(gen_dir, exist_ok=True)

        out_sw_30 = os.path.join(gen_dir, build_filename("3.0", "SWIFT"))
        log_callback(f"Writing OAS 3.0 (SWIFT) to: {out_sw_30}")
        with open(out_sw_30, "w", encoding="utf-8") as f:
            f.write(sw_gen_30.get_yaml())

        # Write Source Map
        map_sw_30 = os.path.join(map_dir, os.path.basename(out_sw_30) + ".map.json")
        with open(map_sw_30, "w", encoding="utf-8") as f:
            f.write(sw_gen_30.get_source_map_json())

        # SWIFT OAS 3.1
        log_callback("Generating SWIFT OAS 3.1...")
        sw_gen_31 = OASGenerator(version="3.1.0")
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
        sw_gen_31.apply_swift_customization(source_filename=build_filename("3.1"))

        out_sw_31 = os.path.join(gen_dir, build_filename("3.1", "SWIFT"))
        log_callback(f"Writing OAS 3.1 (SWIFT) to: {out_sw_31}")
        with open(out_sw_31, "w", encoding="utf-8") as f:
            f.write(sw_gen_31.get_yaml())
        
        # Write Source Map
        map_sw_31 = os.path.join(map_dir, os.path.basename(out_sw_31) + ".map.json")
        with open(map_sw_31, "w", encoding="utf-8") as f:
            f.write(sw_gen_31.get_source_map_json())

    log_callback("Done!")


def main():
    try:
        import customtkinter as ctk
        from src.gui import OASGenApp
    except ImportError:
        try:
            from gui import OASGenApp
            import customtkinter as ctk
        except ImportError:
            # Fallback for dev environment path issues
            import sys

            sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
            from src.gui import OASGenApp
            import customtkinter as ctk

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = OASGenApp()
    app.mainloop()


if __name__ == "__main__":
    main()
