import pandas as pd
import os
import shutil
from collections import OrderedDict
import numpy as np

class LegacyConverter:
    def __init__(self, legacy_dir, output_dir, master_dir=None, log_callback=print):
        self.legacy_dir = legacy_dir
        self.output_dir = output_dir
        self.master_dir = master_dir or os.path.join(os.path.dirname(os.path.dirname(__file__)), "Templates Master")
        self.log_callback = log_callback
        self.global_schemas = OrderedDict()
        self.schema_collision_map = {} # OriginalName -> {AttributesTuple: ActiveName}
        self.all_tags = set()

    def _log(self, msg):
        if self.log_callback:
            self.log_callback(msg)

    def convert(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        legacy_index = os.path.join(self.legacy_dir, "$index.xlsm")
        if not os.path.exists(legacy_index):
            self._log(f"Error: $index.xlsm not found in {self.legacy_dir}")
            return False

        # 1. First pass: Collect all Data Types from all operation files
        # This is necessary to build the global Schemas for $index.xlsx
        self._collect_global_data_types()

        # 2. Second pass: Convert index file
        self._convert_index(legacy_index)

        # 3. Third pass: Convert all operation files
        self._convert_all_operations()

        return True

    def _collect_global_data_types(self):
        self._log("Collecting global data types...")
        for filename in os.listdir(self.legacy_dir):
            if filename.endswith(".xlsm") and filename != "$index.xlsm":
                file_path = os.path.join(self.legacy_dir, filename)
                try:
                    xl = pd.ExcelFile(file_path)
                    if "Data Type" in xl.sheet_names:
                        df_dt = pd.read_excel(xl, sheet_name="Data Type", dtype=str)
                        self._process_data_type_sheet(df_dt, filename)
                except Exception as e:
                    self._log(f"Error collecting data types from {filename}: {e}")

    def _process_data_type_sheet(self, df_dt, source_file):
        # Data Type sheet columns: Data Type (Name), Type, Format, etc.
        # But we saw from analysis that some columns are unnamed or differently named.
        # Let's use a heuristic to find the name column.
        
        # Heuristic: find row with multiple keywords to identify the REAL header row
        header_row_idx = -1
        keywords = ["data type", "type", "description", "example", "format"]
        for idx, row in df_dt.head(10).iterrows():
            row_vals = [str(v).strip().lower() for v in row.values]
            match_count = sum(1 for kw in keywords if kw in row_vals)
            if match_count >= 2:
                header_row_idx = idx
                break
        
        if header_row_idx != -1:
            df_dt.columns = [str(c).strip() for c in df_dt.iloc[header_row_idx]]
            df_dt = df_dt.iloc[header_row_idx+1:].reset_index(drop=True)
        else:
            # Fallback if no clear header row found
            df_dt.columns = [str(c).strip() for c in df_dt.iloc[0]]
            df_dt = df_dt.iloc[1:].reset_index(drop=True)
        
        # The first column (index 0) is Technical Name
        # The second column (index 1) is Description
        for _, row in df_dt.iterrows():
            row_vals = row.values.tolist()
            if len(row_vals) < 2: continue
            
            name = str(row_vals[0]).strip()
            description = str(row_vals[1]).strip()
            
            if not name or name.lower() in ["nan", "data type", "track changes", "description"]:
                continue
            
            # Simple check: if col 1 looks like a long sentence and col 0 is a single word, that's correct.
            # But the user says we swapped them. Wait, if name is descriptive... 
            # Let's inspect Col 0 content. In row 4, Col 0 was "The Generic BIC...".
            # Is there a technical name in col 1? No, col 1 was NaN.
            # This legacy template might be very inconsistent.
            
            # Attributes to compare for collisions
            attrs = {
                "type": str(row.get("Type", row_vals[2] if len(row_vals)>2 else "")).strip(),
                "description": description if description.lower() != "nan" else name,
                "format": str(row.get("Format", "")).strip(),
                "items_type": str(row.get("Items Data Type \n(Array only)", "")).strip(),
                "min": str(row.get("Min  \nValue/Length/Item", "")).strip(),
                "max": str(row.get("Max  \nValue/Length/Item", "")).strip(),
                "pattern": str(row.get("PatternEba", "")).strip() or str(row.get("Regex", "")).strip(),
                "allowed_values": str(row.get("Allowed value", "")).strip(),
                "example": str(row.get("Example", "")).strip()
            }
            
            # Create a comparison key (excluding description for collision logic if preferred, 
            # but usually name collision is enough)
            cmp_attrs = attrs.copy()
            del cmp_attrs["description"]
            attrs_tuple = tuple(sorted(cmp_attrs.items()))
            
            if name not in self.schema_collision_map:
                self.schema_collision_map[name] = {attrs_tuple: name}
                self.global_schemas[name] = attrs
            else:
                if attrs_tuple not in self.schema_collision_map[name]:
                    # Collision! Create new name
                    count = 1
                    while f"{name}{count}" in self.global_schemas:
                        count += 1
                    new_name = f"{name}{count}"
                    self.schema_collision_map[name][attrs_tuple] = new_name
                    self.global_schemas[new_name] = attrs
                else:
                    # Already exists with same attributes, use existing mapping
                    pass

    def _convert_index(self, legacy_index_path):
        self._log(f"Converting index using Master Template: {legacy_index_path}")
        master_index = os.path.join(self.master_dir, "$index.xlsx")
        target_path = os.path.join(self.output_dir, "$index.xlsx")
        
        if os.path.exists(master_index):
            shutil.copy(master_index, target_path)
        else:
            self._log(f"Warning: Master Index not found at {master_index}. Creating fallback.")
            # Create a basic index if master is missing (unlikely in prod)
            pd.DataFrame().to_excel(target_path)

        from openpyxl import load_workbook
        wb = load_workbook(target_path)

        # 1. General Description (Global)
        # Load raw without header detection to avoid skipping the first info row
        df_global = None
        try:
            xl_temp = pd.ExcelFile(legacy_index_path)
            for sname in ["General Description", "General description", "Global", "Info"]:
                if sname in xl_temp.sheet_names:
                    df_global = pd.read_excel(xl_temp, sheet_name=sname, header=None)
                    break
            xl_temp.close()
        except:
            pass
        
        # Target sheet name in Modern Index is "General Description"
        target_sheet_name = "General Description"
        if df_global is not None and target_sheet_name in wb.sheetnames:
            self._log("  Mapping General Description metadata...")
            ws_gen = wb[target_sheet_name]
            
            # Create a map of legacy keys (case-insensitive)
            legacy_map = {}
            for _, row in df_global.iterrows():
                # Get non-NaN values as strings
                vals = [str(v).strip() for v in row.values if str(v).lower() != "nan" and v is not None]
                if len(vals) >= 2:
                    key = vals[0].lower()
                    val = vals[1]
                    if key not in legacy_map:
                        legacy_map[key] = []
                    
                    if key == "servers url" and len(vals) >= 3:
                         legacy_map[key].append((val, vals[2]))
                    else:
                         legacy_map[key].append(val)
            
            self._log(f"    Legacy keys found: {list(legacy_map.keys())}")
            
            # Map to Modern Layout
            # Rows in modern are mostly fixed
            mapping = {
                "info description": 2,
                "info version": 3,
                "info title": 4,
                "info contact name": 5,
                "info contact url": 6,
                "release": 9,
                "filename pattern": 10
            }
            
            for key, row_idx in mapping.items():
                if key in legacy_map and legacy_map[key]:
                    self._log(f"    Setting {key} at row {row_idx}")
                    ws_gen.cell(row=row_idx, column=2).value = legacy_map[key][0]
                else:
                    self._log(f"    Warning: Key '{key}' not found in legacy global info.")
            
            # Servers (can be multiple)
            if "servers url" in legacy_map:
                server_rows = [7, 8] # Modern supports 2 servers in default layout
                for i, s_data in enumerate(legacy_map["servers url"]):
                    if i >= len(server_rows): break
                    r_idx = server_rows[i]
                    self._log(f"    Setting server {i+1} at row {r_idx}")
                    if isinstance(s_data, tuple):
                        url, desc = s_data
                        ws_gen.cell(row=r_idx, column=2).value = url
                        ws_gen.cell(row=r_idx, column=4).value = desc
                    else:
                        ws_gen.cell(row=r_idx, column=2).value = s_data
        
        # 2. Paths sheet
        df_paths = self._load_sheet_with_fallback(legacy_index_path, ["Paths"])
        if df_paths is not None and "Paths" in wb.sheetnames:
            self._log(f"  Paths sheet loaded. Columns: {df_paths.columns.tolist()}")
            if "Request Path" in df_paths.columns:
                df_paths.rename(columns={"Request Path": "Paths"}, inplace=True)
            
            # Robust Tag Extraction
            tag_col = None
            for col in df_paths.columns:
                c_str = str(col).strip().lower()
                if c_str == "tag" or c_str == "tags":
                    tag_col = col
                    break
            if not tag_col:
                tag_col = next((c for c in df_paths.columns if "tag" in str(c).lower()), None)

            if tag_col:
                tags = df_paths[tag_col].dropna().unique()
                tags = [str(t).strip() for t in tags if str(t).strip() and str(t).lower() != "nan" and str(t).lower() != "tag"]
                self.all_tags.update(tags)
            
            # Remove any header-like rows from data
            if not df_paths.empty:
                first_row_vals = [str(v).lower() for v in df_paths.iloc[0].values]
                if "excel file" in first_row_vals or "path" in first_row_vals:
                    df_paths = df_paths.iloc[1:]
            
            # Note: Paths master has headers in row 2 (title in row 1), so start_row=3 is correct for Paths.
            self._write_rows(wb["Paths"], df_paths.values.tolist(), start_row=3)
        
        # 3. Tags sheet
        if "Tags" in wb.sheetnames:
            tags_data = [[tag, tag] for tag in sorted(list(self.all_tags))]
            # Tags master usually has headers in row 1, so start_row=2
            self._write_rows(wb["Tags"], tags_data, start_row=2)
        
        # 4. Schemas sheet
        # Mapping: [Name, Parent, Description, Type, Items Data Type, Schema Name, Format, ...]
        if "Schemas" in wb.sheetnames:
            schemas_data = []
            for name, attrs in self.global_schemas.items():
                schemas_data.append([
                    name,                       # Name
                    "",                         # Parent (always empty as requested)
                    attrs.get("description", name), # Description
                    attrs["type"],              # Type
                    attrs["items_type"],        # Items Data Type
                    "",                         # Schema Name (for type=schema)
                    attrs["format"],            # Format
                    "",                         # Mandatory
                    attrs["min"],               # Min
                    attrs["max"],               # Max
                    attrs["pattern"],           # PatternEba
                    "",                         # Regex
                    attrs["allowed_values"],    # Allowed value
                    attrs["example"]            # Example
                ])
            # Schemas master only has headers in Row 1, start data at Row 2
            self._write_rows(wb["Schemas"], schemas_data, start_row=2)
        
        # 5. Servers
        df_servers = self._load_sheet_with_fallback(legacy_index_path, ["Servers"])
        if df_servers is not None and "Servers" in wb.sheetnames:
            self._write_rows(wb["Servers"], df_servers.values.tolist(), start_row=3)

        wb.save(target_path)

    def _convert_all_operations(self):
        self._log("Converting all operation files...")
        for filename in os.listdir(self.legacy_dir):
            if filename.endswith(".xlsm") and filename != "$index.xlsm":
                legacy_op_path = os.path.join(self.legacy_dir, filename)
                self._convert_operation(legacy_op_path)

    def _convert_operation(self, legacy_op_path):
        filename = os.path.basename(legacy_op_path).replace(".xlsm", ".xlsx")
        self._log(f"  -> Converting operation using endpoint.xlsx Master: {filename}")
        master_endpoint = os.path.join(self.master_dir, "endpoint.xlsx")
        target_path = os.path.join(self.output_dir, filename)
        
        if os.path.exists(master_endpoint):
            shutil.copy(master_endpoint, target_path)
        else:
            self._log(f"Warning: Master endpoint not found at {master_endpoint}.")
            pd.DataFrame().to_excel(target_path)
        
        xl = pd.ExcelFile(legacy_op_path)
        local_data_types = self._load_local_data_types(xl)
        status_codes = [s for s in xl.sheet_names if s.isdigit()]

        from openpyxl import load_workbook
        wb = load_workbook(target_path)

        # Prepare Response sheets
        if "Response" in wb.sheetnames:
            response_tpl = wb["Response"]
            for code in status_codes:
                if code not in wb.sheetnames:
                    new_sheet = wb.copy_worksheet(response_tpl)
                    new_sheet.title = code
            if "Response" in wb.sheetnames and "Response" not in status_codes:
                 del wb["Response"]

        # 1. Parameters
        df_path = self._load_sheet_with_fallback(xl, ["Path"])
        df_header = self._load_sheet_with_fallback(xl, ["Header"])
        params_data = []
        if df_path is not None: params_data.extend(self._process_params(df_path, "path"))
        if df_header is not None: params_data.extend(self._process_params(df_header, "header"))
        if params_data and "Parameters" in wb.sheetnames:
            # Convert dicts from _process_params to lists matching Master Columns
            # Section, Name, In, Description, Type, Schema Name, Mandatory
            rows = []
            for p in params_data:
                rows.append([
                    p["Section"], p["Name"], p["In"], p["Description"], p["Type"], 
                    p.get("Schema Name\n(for Type or Items Data Type = 'schema'||'header')", ""), 
                    p["Mandatory"]
                ])
            self._write_rows(wb["Parameters"], rows, start_row=3)
        
        # 2. Body
        df_body = self._load_sheet_with_fallback(xl, ["Body"])
        if df_body is not None and "Body" in wb.sheetnames:
            body_rows = self._process_schema_sheet(df_body, "Body", local_data_types)
            # _process_schema_sheet returns [MetaRow, HeaderRow, DataRow1, ...]
            self._write_rows(wb["Body"], body_rows[2:], start_row=3)
        
        # 3. Body Example
        if df_body is not None and "Body Example" in wb.sheetnames:
            body_ex_rows = self._generate_body_examples(df_body, local_data_types)
            self._write_rows(wb["Body Example"], body_ex_rows[1:], start_row=2) # Header at 1, data at 2
        
        # 4. Responses
        for code in status_codes:
            if code in wb.sheetnames:
                df_resp = pd.read_excel(xl, sheet_name=code)
                resp_rows = self._process_schema_sheet(df_resp, code, local_data_types, is_response=True)
                self._write_rows(wb[code], resp_rows[2:], start_row=3)

        wb.save(target_path)

    def _write_rows(self, ws, rows, start_row=3):
        for r_idx, row in enumerate(rows, start=start_row):
            for c_idx, value in enumerate(row, start=1):
                if value == "nan" or (isinstance(value, float) and np.isnan(value)):
                    value = ""
                ws.cell(row=r_idx, column=c_idx, value=value)

    def _load_local_data_types(self, xl):
        local_map = {}
        if "Data Type" in xl.sheet_names:
            df_dt = pd.read_excel(xl, sheet_name="Data Type", dtype=str)
            # Find header
            header_row_idx = -1
            for idx, row in df_dt.head(5).iterrows():
                row_str = row.astype(str).str.lower()
                if "data type" in row_str.values or "type" in row_str.values:
                    header_row_idx = idx
                    break
            
            if header_row_idx != -1:
                df_dt.columns = df_dt.iloc[header_row_idx]
                df_dt = df_dt.iloc[header_row_idx+1:].reset_index(drop=True)
            
            df_dt.columns = [str(c).strip() for c in df_dt.columns]
            name_col = next((c for c in df_dt.columns if "data type" in c.lower() or "name" in c.lower()), df_dt.columns[1])
            
            for _, row in df_dt.iterrows():
                name = str(row.get(name_col)).strip()
                if not name or name == "nan": continue
                
                local_map[name] = {
                    "type": str(row.get("Type", "string")).strip(),
                    "format": str(row.get("Format", "")).strip(),
                    "items_type": str(row.get("Items Data Type \n(Array only)", "")).strip(),
                    "min": str(row.get("Min  \nValue/Length/Item", "")).strip(),
                    "max": str(row.get("Max  \nValue/Length/Item", "")).strip(),
                    "pattern": str(row.get("PatternEba", "")).strip() or str(row.get("Regex", "")).strip(),
                    "allowed_values": str(row.get("Allowed value", "")).strip(),
                    "example": str(row.get("Example", "")).strip()
                }
        return local_map

    def _process_schema_sheet(self, df, sheet_name, local_data_types, is_response=False):
        processed = []
        if is_response:
            # Metadata row: Response | Code | Description
            # Legacy might have redundant info in Row 0, Col 2
            desc = "Description Placeholder"
            try:
                # Heuristic: Row 0 usually has the status code and description
                r0 = df.iloc[0].astype(str).values
                for val in r0:
                    if "response" in val.lower() and "-" in val:
                        desc = val.split("-", 1)[1].strip()
                        break
            except: pass
            processed.append(["Response", sheet_name, desc])
        else:
            # For Body
            processed.append(["Request Body", "Body Description Placeholder", "M"])

        # Header Row
        cols = ["Section", "Name", "Parent", "Description", "Type", "Items Data Type \n(Array only)", "Schema Name\n(for Type or Items Data Type = 'schema'||'header')", "Format", "Mandatory", "Min  \nValue/Length/Item", "Max  \nValue/Length/Item", "PatternEba", "Regex", "Allowed value", "Example"]
        processed.append(cols)

        # Identify columns in legacy df
        header_row_idx = -1
        for idx, row in df.head(10).iterrows():
            row_str = row.astype(str).str.lower()
            if "element" in row_str.values or "name" in row_str.values:
                header_row_idx = idx
                break
        
        if header_row_idx != -1:
            df.columns = df.iloc[header_row_idx]
            df = df.iloc[header_row_idx+1:].reset_index(drop=True)
        
        df.columns = [str(c).strip() for c in df.columns]
        
        name_col = next((c for c in df.columns if "element" in c.lower() or "name" in c.lower()), df.columns[1])
        type_col = "Type" if "Type" in df.columns else df.columns[2]
        parent_col = "Parent" if "Parent" in df.columns else None
        mand_col = "Mandatory" if "Mandatory" in df.columns else None
        desc_col = "Description" if "Description" in df.columns else None
        val_col = "Validation rules" if "Validation rules" in df.columns else None

        section = "content" if is_response else "body"

        for _, row in df.iterrows():
            name = str(row.get(name_col)).strip()
            if not name or name == "nan" or name.lower() == "section" or name.lower() == "element": continue
            
            orig_type = str(row.get(type_col, "")).strip()
            parent = str(row.get(parent_col, "")).strip() if parent_col else ""
            if parent.lower() == "nan": parent = ""
            
            desc = str(row.get(desc_col, "")).strip() if desc_col else ""
            if val_col and pd.notna(row.get(val_col)) and str(row.get(val_col)).strip().lower() != "nan":
                desc += f"\n\n**Validation rule(s) ** {row.get(val_col)}"
            
            # Enriched from local data types
            dt_info = local_data_types.get(orig_type, {})
            
            # Resolve collision name
            final_type_name = orig_type
            if orig_type in self.schema_collision_map:
                # Find the correct collision target by matching attributes
                attrs_tuple = tuple(sorted(dt_info.items()))
                final_type_name = self.schema_collision_map[orig_type].get(attrs_tuple, orig_type)

            processed.append([
                section,
                name,
                parent,
                desc,
                dt_info.get("type", "object") if not parent or parent == "" else "schema", # Heuristic: if has children it's object/schema
                dt_info.get("items_type", ""),
                final_type_name if dt_info.get("type") in ["schema", "object", "array"] or (parent and parent != "") else "",
                dt_info.get("format", ""),
                row.get(mand_col, ""),
                dt_info.get("min", ""),
                dt_info.get("max", ""),
                dt_info.get("pattern", ""),
                "", # Regex
                dt_info.get("allowed_values", ""),
                dt_info.get("example", "")
            ])
            
        return processed

    def _process_params(self, df, param_in):
        processed = []
        header_row_idx = -1
        for idx, row in df.head(5).iterrows():
            row_str = row.astype(str).str.lower()
            if "element" in row_str.values or "request" in row_str.values:
                header_row_idx = idx
                break
        
        if header_row_idx != -1:
            df.columns = df.iloc[header_row_idx]
            df = df.iloc[header_row_idx+1:].reset_index(drop=True)

        df.columns = [str(c).strip() for c in df.columns]
        name_col = next((c for c in df.columns if "element" in c.lower() or "request" in c.lower()), df.columns[1])
        type_col = "Type" if "Type" in df.columns else df.columns[2]
        mand_col = "Mandatory" if "Mandatory" in df.columns else df.columns[3]
        desc_col = "Description" if "Description" in df.columns else None
        val_col = "Validation rules" if "Validation rules" in df.columns else None

        for _, row in df.iterrows():
            name = str(row.get(name_col)).strip()
            if not name or name == "nan" or name.lower() == "element": continue
            
            desc = str(row.get(desc_col, "")).strip() if desc_col else ""
            val_rules = str(row.get(val_col, "")).strip()
            if val_rules and val_rules.lower() != "nan":
                desc += f"\n\n**Validation rule(s) ** {val_rules}"
            
            orig_type = str(row.get(type_col, "")).strip()
            
            row_map = {
                "Section": "parameters",
                "Name": name,
                "In": param_in,
                "Description": desc,
                "Type": "schema",
                "Schema Name\n(for Type or Items Data Type = 'schema'||'header')": orig_type,
                "Mandatory": row.get(mand_col)
            }
            # Note: The modern generator handles the rest based on Schema Name
            processed.append(row_map)
        return processed

    def _generate_body_examples(self, df_body, local_data_types):
        import json
        header = ["Example Name", "Body"]
        
        # Identify name and mandatory columns
        header_row_idx = -1
        for idx, row in df_body.head(5).iterrows():
            row_str = row.astype(str).str.lower()
            if "element" in row_str.values or "name" in row_str.values:
                header_row_idx = idx
                break
        
        if header_row_idx == -1: return [header, ["OK", "{}"], ["Bad Request", "{}"]]
        
        cols_df = df_body.iloc[header_row_idx]
        data_df = df_body.iloc[header_row_idx+1:]
        
        name_col_idx = next((i for i, c in enumerate(cols_df) if "element" in str(c).lower() or "name" in str(c).lower()), 1)
        type_col_idx = next((i for i, c in enumerate(cols_df) if "type" in str(c).lower()), 2)
        mand_col_idx = next((i for i, c in enumerate(cols_df) if "mandatory" in str(c).lower()), 3)
        parent_col_idx = next((i for i, c in enumerate(cols_df) if "parent" in str(c).lower()), -1)

        ok_obj = {}
        bad_obj = {}
        
        mandatory_fields = []
        optional_fields = []
        
        for _, row in data_df.iterrows():
            name = str(row.iloc[name_col_idx]).strip()
            if not name or name == "nan" or name.lower() == "element": continue
            
            parent = str(row.iloc[parent_col_idx]).strip() if parent_col_idx != -1 else ""
            if parent.lower() == "nan": parent = ""
            if parent: continue # Nested fields handled by structure, for simple logic we focus on flat for now
            
            is_mand = str(row.iloc[mand_col_idx]).upper() in ["M", "YES", "TRUE", "X"]
            type_name = str(row.iloc[type_col_idx]).strip()
            
            field_info = {"name": name, "type": type_name, "is_mand": is_mand}
            if is_mand:
                mandatory_fields.append(field_info)
            else:
                optional_fields.append(field_info)

        def get_valid_value(tname):
            dt = local_data_types.get(tname, {})
            ex = dt.get("example")
            if ex and ex.lower() != "nan": return ex.split(";")[0].strip() # Take first example
            t = dt.get("type", "string").lower()
            if "int" in t or "number" in t: return 123
            if "bool" in t: return True
            return "string_value"

        def get_invalid_value(tname):
            dt = local_data_types.get(tname, {})
            t = dt.get("type", "string").lower()
            if "int" in t or "number" in t: return "not_a_number"
            if "bool" in t: return "not_a_bool"
            # Pattern check would be better but for now just type violation
            return 999 

        # OK Scenario
        target_fields = mandatory_fields if mandatory_fields else optional_fields
        for f in target_fields:
            ok_obj[f["name"]] = get_valid_value(f["type"])
        
        # Bad Request Scenario
        if mandatory_fields:
            # Missing one mandatory
            for f in mandatory_fields[:-1]:
                bad_obj[f["name"]] = get_valid_value(f["type"])
            # Invalidate one existing
            if bad_obj:
                last_key = list(bad_obj.keys())[-1]
                # find type for last_key
                tname = next(f["type"] for f in mandatory_fields if f["name"] == last_key)
                bad_obj[last_key] = get_invalid_value(tname)
        else:
            # Generic invalid for optional
            for f in optional_fields:
                bad_obj[f["name"]] = get_invalid_value(f["type"])

        return [header, ["OK", json.dumps(ok_obj)], ["Bad Request", json.dumps(bad_obj)]]

    def _load_sheet_with_fallback(self, source, fallbacks):
        try:
            xl = source if isinstance(source, pd.ExcelFile) else pd.ExcelFile(source)
            for f in fallbacks:
                if f in xl.sheet_names:
                    # Read more rows to find header
                    df = pd.read_excel(xl, sheet_name=f, dtype=str, header=None)
                    
                    # Robust Header Detection
                    header_row_idx = -1
                    # Keywords that strongly indicate a header row
                    keywords = ["paths", "element", "description", "type", "tag", "excel file", "method"]
                    for idx, row in df.head(10).iterrows():
                        row_vals = [str(v).strip().lower() for v in row.values]
                        # Check for exact matches or significant presence
                        match_count = sum(1 for kw in keywords if kw in row_vals)
                        if match_count >= 2 or ("excel file" in row_vals) or ("element" in row_vals):
                            header_row_idx = idx
                            break
                    
                    if header_row_idx != -1:
                        self._log(f"  Detected header at row {header_row_idx} for sheet {f}")
                        df.columns = [str(c).strip() for c in df.iloc[header_row_idx]]
                        df = df.iloc[header_row_idx+1:].reset_index(drop=True)
                    else:
                        self._log(f"  No header detected for sheet {f}, using row 0 as columns")
                        df.columns = [str(c).strip() for c in df.iloc[0]]
                        df = df.iloc[1:].reset_index(drop=True)
                    
                    if not isinstance(source, pd.ExcelFile): xl.close()
                    return df
            if not isinstance(source, pd.ExcelFile): xl.close()
        except Exception as e:
            self._log(f"  Error loading sheet {fallbacks}: {e}")
        return None

if __name__ == "__main__":
    # Test call
    conv = LegacyConverter(r"c:\Users\giuse\.gemini\antigravity\scratch\OASIS\Templates Legacy", r"c:\Users\giuse\.gemini\antigravity\scratch\OASIS\Templates Converted")
    conv.convert()
