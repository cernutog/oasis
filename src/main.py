import os
import sys
# Add src to path if needed or assume relative imports work if run as module
# If run as script, parser/generator are in same dir.
try:
    import parser
    from generator import OASGenerator
except ImportError:
    from src import parser
    from src.generator import OASGenerator

def find_best_match_file(target, directory, files_list):
    # Delegate to parser's logic or reimplement simple one
    return parser.find_best_match_file(target, directory, files_list)

def generate_oas(base_dir, gen_30=True, gen_31=True, log_callback=print):
    """
    Main execution function.
    base_dir: Directory containing '$index.xlsm'
    """
    if not os.path.exists(base_dir):
        log_callback(f"Error: Directory not found: {base_dir}")
        return

    log_callback(f"Starting generation in: {base_dir}")
    
    # 1. Setup Paths
    files_in_dir = os.listdir(base_dir)
    index_path = find_best_match_file("$index.xlsm", base_dir, files_in_dir)
    if not index_path:
        log_callback("Error: $index.xlsm not found in the specified directory.")
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

    security_schemes, security_req = parser.parse_security(parser.load_excel_sheet(index_path, "Security"))

    df_paths = parser.load_excel_sheet(index_path, "Paths")
    paths_list = parser.parse_paths_index(df_paths)
    
    components_data = parser.parse_components(index_path) # Global components

    # 3. Parse Operation Files
    log_callback("Parsing operation details...")
    operations_details = {}
    
    # Identify unique files to parse
    unique_files = set()
    for op in paths_list:
        if op.get("file"):
            unique_files.add(op.get("file"))
            
    for raw_file_name in unique_files:
        if not raw_file_name: continue
        full_path = find_best_match_file(raw_file_name, base_dir, files_in_dir)
        if full_path:
            # log_callback(f"  Parsing: {os.path.basename(full_path)}")
            op_det = parser.parse_operation_file(full_path)
            if op_det:
                operations_details[raw_file_name] = op_det
        else:
            log_callback(f"  Operation file not found for: {raw_file_name}")

    # Output Directory: Parent of templates dir, or same dir?
    # User said input is template folder. Let's output to the parent of that folder to avoid clutter?
    # Or just inside plain output folder.
    # Let's write to `base_dir` to keeps things simple as per current flow.
    output_dir = base_dir

    # 4. Generate OAS 3.0
    if gen_30:
        log_callback("Generating OAS 3.0...")
        generator_30 = OASGenerator(version="3.0.0")
        generator_30.build_info(info_data)
        if tags_data:
            generator_30.oas["tags"] = tags_data
        if servers_data:
            generator_30.oas["servers"] = servers_data
        if security_req:
            generator_30.oas["security"] = security_req
            
        generator_30.build_paths(paths_list, operations_details)
        
        # Add Security Schemes to Components
        if security_schemes:
            if "securitySchemes" not in components_data: components_data["securitySchemes"] = {}
            components_data["securitySchemes"].update(security_schemes)
            
        generator_30.build_components(components_data)
        generator_30.build_paths(paths_list, operations_details)
        
        # Ensure 'generated' folder exists
        gen_dir = os.path.join(output_dir, "generated")
        os.makedirs(gen_dir, exist_ok=True)

        out_30 = os.path.join(gen_dir, "generated_oas_3.0.yaml")
        log_callback(f"Writing OAS 3.0 to: {out_30}")
        with open(out_30, "w", encoding="utf-8") as f:
            f.write(generator_30.get_yaml())

    # 5. Generate OAS 3.1
    if gen_31:
        log_callback("Generating OAS 3.1...")
        generator_31 = OASGenerator(version="3.1.0")
        generator_31.build_info(info_data)
        if tags_data:
            generator_31.oas["tags"] = tags_data
        if servers_data:
            generator_31.oas["servers"] = servers_data
        if security_req:
            generator_31.oas["security"] = security_req
            
        generator_31.build_components(components_data)
        generator_31.build_paths(paths_list, operations_details)

        # Ensure 'generated' folder exists
        gen_dir = os.path.join(output_dir, "generated")
        os.makedirs(gen_dir, exist_ok=True)

        out_31 = os.path.join(gen_dir, "generated_oas_3.1.yaml")
        log_callback(f"Writing OAS 3.1 to: {out_31}")
        with open(out_31, "w", encoding="utf-8") as f:
            f.write(generator_31.get_yaml())
    
    log_callback("Done!")

def main():
    # Default CLI behavior
    cwd = os.getcwd()
    templates_dir = os.path.join(cwd, "API Templates")
    if not os.path.exists(templates_dir):
        templates_dir = cwd # Fallback
        
    # files = [f for f in files if "account_assessment.251111.xlsm" in f]
    # print(f"Processing filtered files: {files}")
    
    generate_oas(templates_dir)

if __name__ == "__main__":
    main()
