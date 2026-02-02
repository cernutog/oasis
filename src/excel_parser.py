import pandas as pd
import os
import difflib


def load_excel_sheet(file_path, sheet_name):
    """
    Helper function to load a specific sheet from an Excel file.
    Includes smart header detection.
    """
    try:
        # First read with no header to find the header row
        df_raw = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

        # Search for the header row
        header_row_idx = -1
        # Check first 10 rows
        for idx, row in df_raw.head(10).iterrows():
            row_str = row.astype(str).str.lower()
            # Count how many "header-like" keywords are in this row
            # A true header row should have multiple column names
            header_keywords = [
                "name",
                "description",
                "type",
                "in",
                "mandatory",
                "required",
            ]
            matches = sum(1 for keyword in header_keywords if keyword in row_str.values)

            # If we find multiple header keywords, this is likely the header row
            if matches >= 2:
                header_row_idx = idx
                break

        if header_row_idx != -1:
            # Read with dtype=str to preserve exact numeric format (e.g., 100000000000000 not 1e14)
            df = pd.read_excel(file_path, sheet_name=sheet_name, header=header_row_idx, dtype=str)

            # Capture Metadata from rows above header (Gener generalized parsing)
            # Scan rows preceding the header for "Response" definition layout
            if header_row_idx > 0:
                try:
                    # Iterate rows 0 to header_idx - 1
                    meta_rows = df_raw.iloc[:header_row_idx]
                    for meta_idx, meta_row in meta_rows.iterrows():
                        # Find first non-empty cell
                        row_vals = [
                            str(x).strip()
                            for x in meta_row.values
                            if pd.notna(x) and str(x).strip()
                        ]
                        if not row_vals:
                            continue

                        first_val = row_vals[0]
                        if first_val.lower() == "response":
                            # Found Definition Row: "Response" | Code | Description
                            # We expect at least 3 values: Response, Code, Description
                            if len(row_vals) > 2:
                                desc = row_vals[2]
                                df.attrs["response_description"] = str(desc).strip()
                                break
                    
                    # NEW: Specific metadata for "Body" sheet (B1=Description, C1=Required)
                    if sheet_name == "Body":
                        try:
                            # Row 0, Col 1 is B1; Col 2 is C1
                            b1_val = df_raw.iloc[0, 1]
                            c1_val = df_raw.iloc[0, 2]
                            if pd.notna(b1_val):
                                df.attrs["body_description"] = str(b1_val).strip()
                            if pd.notna(c1_val):
                                df.attrs["body_required"] = str(c1_val).strip()
                        except Exception:
                            pass
                except Exception:
                    pass

        else:
            # Fallback to default - still use dtype=str for consistency
            df = pd.read_excel(file_path, sheet_name=sheet_name, dtype=str)

        df.columns = df.columns.str.strip()
        df.attrs["sheet_name"] = sheet_name
        return df
    except ValueError:
        # Sheet might not exist
        return None
    except Exception as e:
        print(f"Error loading {sheet_name} from {file_path}: {e}")
        return None


def find_best_match_file(target_name, directory, files_list):
    """
    Tries to find the actual file in directory that matches target_name.
    Handles exact match, case insensitivity, and minor typos.
    """
    if not target_name:
        return None

    # Normalize target
    target = target_name.strip()
    if not target.endswith(".xlsm") and not target.endswith(".xlsx"):
        target += ".xlsm"

    # 1. Exact match
    if target in files_list:
        return os.path.join(directory, target)

    # 2. Case insensitive
    for f in files_list:
        if f.lower() == target.lower():
            return os.path.join(directory, f)

    # 3. Fuzzy match / typo correction
    # Using difflib to find closest match
    matches = difflib.get_close_matches(target, files_list, n=1, cutoff=0.6)
    if matches:
        print(f"Warning: fuzzy matching '{target_name}' to '{matches[0]}'")
        return os.path.join(directory, matches[0])

    return None


def parse_info(df_info):
    """
    Parses 'General Description' sheet.
    Structure: Key, Value.
    Keys usually: 'info description', 'info version', 'info title'
    """
    info = {"title": "API Specification", "version": "1.0.0"}  # Default
    servers = []

    if df_info is not None:
        # Expecting col 0 to be key, col 1 to be val
        # Headers might be shifted or named 'General Description'

        # Iterate through rows
        for index, row in df_info.iterrows():
            key = str(row.iloc[0]).strip().lower()
            val = row.iloc[1]
            if pd.isna(val):
                continue

            if "description" in key and "info" in key:
                info["description"] = val
            elif "version" in key and "info" in key:
                info["version"] = str(val)
            elif "title" in key and "info" in key:
                info["title"] = val
            elif "contact" in key:
                if "contact" not in info:
                    info["contact"] = {}
                if "email" in key:
                    info["contact"]["email"] = val
                if "name" in key:
                    info["contact"]["name"] = val
                if "url" in key:
                    info["contact"]["url"] = val
            elif "release" in key:
                info["release"] = str(val)
            elif "filename" in key and "pattern" in key:
                info["filename_pattern"] = str(val)

            # Servers (Inline)
            if "servers" in key and "url" in key:
                server_obj = {"url": val}
                # Check if description exists in column D (index 3)
                if len(row) > 3:
                    desc_val = row.iloc[3]
                    if pd.notna(desc_val) and str(desc_val).strip():
                        server_obj["description"] = str(desc_val).strip()
                servers.append(server_obj)

    return info, servers


def parse_paths_index(df_paths):
    """
    Parses the 'Paths' sheet.
    """
    operations = []
    if df_paths is not None:
        # Print columns to help debugging
        # print(f"DEBUG Paths cols: {df_paths.columns.tolist()}")

        # Ensure we locate the correct columns even if named 'Unnamed'
        # Heuristic: Find which column contains '/v1' to identify Path column
        path_col = None
        file_col = None
        method_col = None

        # Simple mapping based on known structure or fallback to index
        # 'Paths' usually contains the path
        if "Paths" in df_paths.columns:
            path_col = "Paths"
        elif "Path" in df_paths.columns:
            path_col = "Path"

        for idx, col in enumerate(df_paths.columns):
            if "Excel" in col or "Unnamed: 0" == col:  # First col usually file
                file_col = col
            if not path_col and ("Unnamed: 1" == col or "Paths" in col):
                path_col = col
            if "Method" in col or "Unnamed: 3" == col:
                method_col = col

        # If still None, assume standard layout
        file_col = file_col or df_paths.columns[0]
        path_col = path_col or df_paths.columns[1]

        for _, row in df_paths.iterrows():
            path_val = row.get(path_col)
            # Skip empty or header-like rows
            if not isinstance(path_val, str) or not path_val.startswith("/"):
                continue

            op = {
                "file": row.get(file_col),
                "path": path_val,
                "method": row.get("Method") or row.get("Unnamed: 3"),
                "summary": row.get("Summary") or row.get("Unnamed: 6"),
                "description": row.get("Description") or row.get("Unnamed: 4"),
                "operationId": row.get("OperationId") or row.get("Unnamed: 7"),
                "tags": row.get("Tag") or row.get("Unnamed: 5"),
                "extensions": row.get("Custom Extensions") or row.get("Unnamed: 8"),
            }
            operations.append(op)
    return operations


from collections import OrderedDict

def parse_tags(df_tags):
    """
    Parses 'Tags' sheet.
    Expected columns: Name, Description, ExternalDocs...
    """
    tags = []
    if df_tags is not None:
        for _, row in df_tags.iterrows():
            # Use OrderedDict to enforce YAML output order via OASDumper
            tag = OrderedDict([
                ("name", row.get("Name")),
                ("description", row.get("Description"))
            ])
            if pd.notna(tag["name"]) and str(tag["name"]).strip():
                tags.append(tag)
    return tags


def parse_servers(df_servers):
    """
    Parses 'Servers' sheet.
    Expected columns: URL, Description
    """
    servers = []
    if df_servers is not None:
        # Normalize cols
        df_servers.columns = df_servers.columns.str.strip()
        for _, row in df_servers.iterrows():
            srv = {"url": row.get("URL"), "description": row.get("Description")}
            if pd.notna(srv["url"]):
                servers.append(srv)
    return servers


def parse_security(df_sec):
    """
    Parses 'Security' sheet.
    Expected columns: Name, Type, Scheme, Format, Description
    """
    security_schemes = {}
    security_req = []

    if df_sec is not None:
        df_sec.columns = df_sec.columns.str.strip()
        for _, row in df_sec.iterrows():
            name = row.get("Name")
            if pd.isna(name):
                continue

            # Simple Scheme definition
            scheme = {
                "type": str(row.get("Type")).lower(),
                "description": row.get("Description"),
            }
            if pd.notna(row.get("Scheme")):
                scheme["scheme"] = row.get("Scheme")
            if pd.notna(row.get("Format")):
                scheme["bearerFormat"] = row.get("Format")

            security_schemes[name] = scheme
            security_req.append({name: []})

    return security_schemes, security_req


def parse_components(file_path):
    """
    Parses global components from sheets: Parameters, Headers, Schemas, Responses.
    """
    components = {
        "parameters": load_excel_sheet(file_path, "Parameters"),
        "headers": load_excel_sheet(file_path, "Headers"),
        "schemas": load_excel_sheet(file_path, "Schemas"),
        "responses": load_excel_sheet(file_path, "Responses"),
    }
    return components


def parse_operation_file(file_path):
    """
    Parses a single operation Excel file.
    """
    if not os.path.exists(file_path):
        return None

    op_details = {}

    # Load Sheets
    op_details["parameters"] = load_excel_sheet(file_path, "Parameters")
    op_details["body"] = load_excel_sheet(file_path, "Body")
    op_details["body_examples"] = load_excel_sheet(file_path, "Body Example")

    # Responses
    try:
        xl = pd.ExcelFile(file_path)
        response_sheets = [s for s in xl.sheet_names if s.isdigit()]
        xl.close()  # Close Excel file to release file handle
        op_details["responses"] = {}
        for code in response_sheets:
            op_details["responses"][code] = load_excel_sheet(file_path, code)
    except Exception:
        pass

    return op_details
