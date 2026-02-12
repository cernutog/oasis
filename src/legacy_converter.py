"""
Legacy Excel to Modern OAS Converter - Clean Implementation

Converts legacy Excel API specifications to modern OAS format.
Architecture: Simple linear flow with direct sheet transformations.
"""
import os
import shutil
from pathlib import Path
from collections import OrderedDict
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import pandas as pd
import openpyxl
from openpyxl import load_workbook


@dataclass
class DataType:
    """Data type definition from legacy 'Data Type' sheet."""
    name: str
    type: str
    format: str = ""
    min_val: str = ""
    max_val: str = ""
    description: str = ""
    pattern_eba: str = ""
    regex: str = ""
    allowed_values: str = ""
    example: str = ""
    items_type: str = ""  # For arrays


class LegacyConverter:
    """Converts legacy Excel templates to modern OAS format."""
    
    def __init__(self, input_dir: str, output_dir: str, master_dir: str):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.master_dir = Path(master_dir)
        
        # Global registries populated during conversion
        self.file_data_types: Dict[Tuple[str, str], DataType] = {} # (file, name) -> DataType
        self.output_names: Dict[Tuple[str, str], str] = {}        # (file, name) -> Unique Global Name
        self.global_schemas: Dict[str, DataType] = {}             # Unique Global Name -> DataType
        self.used_names = set()                                   # Set of unique output names used
        self.fingerprints: Dict[tuple, str] = {}                  # Content Fingerprint -> Unique Global Name
        self.all_tags = set()
        
        # Track active endpoint during per-file resolution
        self.current_ep_name: Optional[str] = None
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def convert(self) -> bool:
        """Main conversion entry point."""
        print(f"Converting legacy templates from {self.input_dir}")
        
        # Phase 1: Load all data types from endpoint files first
        self._collect_all_data_types()
        
        # Phase 1: Convert $index.xlsm or $index.xlsx
        index_path = self.input_dir / "$index.xlsm"
        if not index_path.exists():
            index_path = self.input_dir / "$index.xlsx"
            
        if index_path.exists():
            self._convert_index(index_path)
        else:
            print("Warning: $index.xlsm/xlsx not found")
            return False
        
        # Phase 3: Convert all endpoint files
        ep_files = list(self.input_dir.glob("*.xlsm")) + list(self.input_dir.glob("*.xlsx"))
        for ep_file in ep_files:
            if ep_file.name.startswith("$"):
                continue  # Skip index
            self._convert_endpoint(ep_file)
        
        print(f"Conversion complete. Output: {self.output_dir}")
        return True
    def _collect_all_data_types(self):
        """Collect all data types from all endpoint 'Data Type' sheets."""
        print("Collecting data types from all endpoints...")
        
        # First, check if $index.xlsm or $index.xlsx has a Data Type sheet
        index_files = [self.input_dir / "$index.xlsm", self.input_dir / "$index.xlsx"]
        for index_file in index_files:
            if index_file.exists():
                self._collect_data_types_from_file(index_file, is_global=True)
            
        # Then, collect from all endpoint files
        ep_files = list(self.input_dir.glob("*.xlsm")) + list(self.input_dir.glob("*.xlsx"))
        for ep_file in ep_files:
            if ep_file.name.startswith("$"):
                continue
            self._collect_data_types_from_file(ep_file, is_global=False)
        
        print(f"  Loaded {len(self.global_schemas)} unique global schemas.")

    def _collect_data_types_from_file(self, file_path: Path, is_global: bool = False):
        """Collect data types from a single file's 'Data Type' sheet."""
        header_keywords = ["name", "element", "type", "parent", "data type", "description", "mandatory"]
        xl = pd.ExcelFile(file_path)
        if "Data Type" not in xl.sheet_names:
            return
            
        df = pd.read_excel(xl, sheet_name="Data Type", dtype=str, header=None)
        header_row_idx = self._find_header_row(df, header_keywords)
        if header_row_idx == -1:
            return
            
        df.columns = [str(c).strip() for c in df.iloc[header_row_idx]]
        df = df.iloc[header_row_idx + 1:].reset_index(drop=True)
        
        file_key = "$global" if is_global else file_path.name
        
        # Helper to get first non-empty value from any column matching keywords
        def gv(keywords, default=""):
            for col in df.columns:
                col_str = str(col).lower()
                if any(k in col_str for k in keywords):
                    val = self._clean_value(row.get(col, ""))
                    if val: return val
            return default

        for _, row in df.iterrows():
            name_col = self._find_column(df, ["name", "data type", "element"])
            name_raw = row.get(name_col) if name_col else None
            
            if name_raw is None or pd.isna(name_raw):
                continue
            name = str(name_raw).strip()
            if not name or name.lower() == "nan":
                continue
            
            norm_name = self._to_pascal_case(name)
            
            dt = DataType(
                name=norm_name,
                type=gv(["type"], "string"),
                format=gv(["format"]),
                min_val=gv(["min"]),
                max_val=gv(["max"]),
                description=gv(["description"], norm_name),
                pattern_eba=gv(["pattern", "regex"]),
                regex=gv(["regex", "pattern"]),
                allowed_values=gv(["allowed"]),
                example=gv(["example"]),
                items_type=gv(["items data type", "array only"])
            )
            
            if dt.items_type:
                dt.items_type = self._to_pascal_case(dt.items_type)
            
            self._register_data_type(file_key, norm_name, dt)

    def _register_data_type(self, file_key: str, norm_name: str, dt: DataType):
        """Registers a data type, deduplicating by content and handling name collisions."""
        # Fingerprint for deduplication
        fingerprint = tuple(sorted([(k, v) for k, v in dt.__dict__.items() if k != 'name']))
        
        # Mapping key for this specific file/name combination
        mapping_key = (file_key, norm_name)
        
        # 1. Content-based deduplication
        if fingerprint in self.fingerprints:
            out_name = self.fingerprints[fingerprint]
            self.output_names[mapping_key] = out_name
            self.file_data_types[mapping_key] = dt
            return
            
        # 2. Name collision handling for new unique content
        output_name = norm_name
        counter = 1
        while output_name in self.used_names:
            output_name = f"{norm_name}{counter}"
            counter += 1
            
        # 3. Registering the new unique schema
        self.global_schemas[output_name] = dt
        self.used_names.add(output_name)
        self.fingerprints[fingerprint] = output_name
        
        # 4. Map the (file, name) to this global output name
        self.output_names[mapping_key] = output_name
        self.file_data_types[mapping_key] = dt

    def _resolve_data_type(self, name: str, ep_filename: Optional[str] = None) -> Tuple[Optional[str], Optional[DataType]]:
        """Resolves a named data type to its unique global output name and DataType object.
        Checks current endpoint file first, then the global registry."""
        norm_name = self._to_pascal_case(name)
        
        # Priority 1: Current endpoint file
        if ep_filename:
            key = (ep_filename, norm_name)
            if key in self.output_names:
                out_name = self.output_names[key]
                return out_name, self.global_schemas[out_name]
                
        # Priority 2: Global registry ($index)
        global_key = ("$global", norm_name)
        if global_key in self.output_names:
            out_name = self.output_names[global_key]
            return out_name, self.global_schemas[out_name]
            
        # Priority 3: Fallback to any file if it exists only in one place (heuristic)
        for key, out_name in self.output_names.items():
            if key[1] == norm_name:
                return out_name, self.global_schemas[out_name]
                
        return None, None
    
    def _convert_index(self, legacy_path: Path):
        """Convert $index.xlsm or $index.xlsx to $index.xlsx in output."""
        print(f"Converting index: {legacy_path.name}")
        
        # Copy master template
        master_index = self.master_dir / "$index.xlsm"
        if not master_index.exists():
            master_index = self.master_dir / "$index.xlsx"
            
        output_path = self.output_dir / "$index.xlsx"
        shutil.copy(master_index, output_path)
        
        wb = load_workbook(output_path)
        xl_legacy = pd.ExcelFile(legacy_path)
        
        # 1. General Description
        self._convert_general_description(wb, xl_legacy)
        
        # 2. Paths
        self._convert_paths(wb, xl_legacy)
        
        # 3. Tags
        self._convert_tags(wb)
        
        # 4. Schemas (most complex - builds from Body/Response structures)
        self._convert_schemas(wb)
        
        wb.save(output_path)
        print(f"  Saved: {output_path}")
    
    def _convert_general_description(self, wb, xl_legacy):
        """Convert General Description sheet."""
        ws = wb["General Description"]
        
        # Read legacy key-value format
        df = pd.read_excel(xl_legacy, sheet_name="General Description", dtype=str, header=None)
        
        # Build key-value map
        kv_map = {}
        for _, row in df.iterrows():
            vals = [str(v).strip() for v in row.values if str(v).lower() != "nan"]
            if len(vals) >= 2:
                key = vals[0].lower()
                
                # Handle servers with 4 columns: [servers url, url, servers description, desc]
                if key == "servers url":
                    url = vals[1]
                    desc = vals[3] if len(vals) >= 4 else ""
                    if key not in kv_map:
                        kv_map[key] = []
                    kv_map[key].append((url, desc))
                else:
                    kv_map[key] = vals[1]
        
        # Map to modern fixed positions
        mappings = {
            "info description": (2, 2),
            "info version": (3, 2),
            "info title": (4, 2),
            "info contact name": (5, 2),
            "info contact url": (6, 2),
            "release": (9, 2),
            "filename pattern": (10, 2)
        }
        
        for key, (row, col) in mappings.items():
            if key in kv_map:
                ws.cell(row=row, column=col).value = kv_map[key]
        
        # Servers
        if "servers url" in kv_map:
            server_rows = [7, 8]
            for i, (url, desc) in enumerate(kv_map["servers url"]):
                if i >= len(server_rows):
                    break
                r = server_rows[i]
                ws.cell(row=r, column=2).value = url
                ws.cell(row=r, column=4).value = desc
    
    def _convert_paths(self, wb, xl_legacy):
        """Convert Paths sheet."""
        ws = wb["Paths"]
        
        df = pd.read_excel(xl_legacy, sheet_name="Paths", dtype=str)
        header_row_idx = self._find_header_row(df, ["excel file", "path"])
        
        if header_row_idx == -1:
            return
        
        if header_row_idx != -2:
            df.columns = df.iloc[header_row_idx]
            df = df.iloc[header_row_idx + 1:].reset_index(drop=True)
        
        # Collect tags
        tag_col = self._find_column(df, ["tag", "tags"])
        if tag_col:
            tags = df[tag_col].dropna().unique()
            self.all_tags.update([str(t).strip() for t in tags if str(t).strip() and str(t).lower() != "nan"])
        
        # Ensure .xlsx extension on filenames
        filename_col = self._find_column(df, ["excel file", "file"])
        if filename_col:
            df[filename_col] = df[filename_col].apply(self._ensure_xlsx_extension)
        
        # Write rows
        rows = df.values.tolist()
        self._write_rows(ws, rows, start_row=3)
    
    def _convert_tags(self, wb):
        """Convert Tags sheet."""
        ws = wb["Tags"]
        
        # Clear existing
        for row in range(2, ws.max_row + 1):
            for col in range(1, ws.max_column + 1):
                ws.cell(row=row, column=col).value = None
        
        # Write tags
        tags_data = [[tag, tag] for tag in sorted(self.all_tags)]
        self._write_rows(ws, tags_data, start_row=2)
    
    def _convert_schemas(self, wb):
        """Convert Schemas sheet - builds hierarchy from Body/Response structures."""
        ws = wb["Schemas"]
        
        # Clear existing
        for row in range(2, ws.max_row + 1):
            for col in range(1, ws.max_column + 1):
                ws.cell(row=row, column=col).value = None
        
        final_rows = []
        referenced_data_types = set()  # Track which data types are actually used
        
        # Representative keywords for header detection
        header_keywords = ["name", "element", "type", "parent", "data type", "description", "mandatory"]
        
        # Section 0: Track data types from endpoint parameters
        ep_files = list(self.input_dir.glob("*.xlsm")) + list(self.input_dir.glob("*.xlsx"))
        for ep_file in ep_files:
            if ep_file.name.startswith("$"):
                continue
            
            xl = pd.ExcelFile(ep_file)
            
            # Check Path and Header parameters
            for sheet_name in ["Path", "Header"]:
                if sheet_name in xl.sheet_names:
                    # Read without header to find it manually
                    df = pd.read_excel(xl, sheet_name=sheet_name, dtype=str, header=None)
                    header_row_idx = self._find_header_row(df, header_keywords)
                    if header_row_idx == -1:
                        continue
                    
                    df.columns = [str(c).strip() for c in df.iloc[header_row_idx]]
                    df = df.iloc[header_row_idx + 1:].reset_index(drop=True)
                    
                    # Track types
                    for _, row in df.iterrows():
                        dtype = self._clean_value(row.get("Type", ""))
                        if not dtype or dtype.lower() in ["string", "number", "integer", "boolean", "array", "object", "nan"]:
                            continue
                        out_name, _ = self._resolve_data_type(dtype, ep_file.name)
                        if out_name:
                            referenced_data_types.add(out_name)
        
        # Section 1: Request/Response wrappers with children
        ep_files = list(self.input_dir.glob("*.xlsm")) + list(self.input_dir.glob("*.xlsx"))
        for ep_file in ep_files:
            if ep_file.name.startswith("$"):
                continue
            
            # Read endpoint structure
            xl = pd.ExcelFile(ep_file)
            
            op_id = self._extract_operation_id(ep_file.name)
            
            # Request wrapper from Body
            if "Body" in xl.sheet_names:
                children = self._read_legacy_structure(xl, "Body")
                if children:  # Only emit if has children
                    wrapper_name = f"{op_id}Request"
                    final_rows.append([wrapper_name, "", "", "object", "", "", "", "", "", "", "", "", "", ""])
                    child_rows, refs = self._build_children_rows(wrapper_name, children, ep_file.name)
                    final_rows.extend(child_rows)
                    referenced_data_types.update(refs)
            
            # Response wrapper from 200
            if "200" in xl.sheet_names:
                wrapper_name = f"{op_id}Response"
                children = self._read_legacy_structure(xl, "200")
                final_rows.append([wrapper_name, "", "", "object", "", "", "", "", "", "", "", "", "", ""])
                child_rows, refs = self._build_children_rows(wrapper_name, children, ep_file.name)
                final_rows.extend(child_rows)
                referenced_data_types.update(refs)
        
        # Section 1.5: Error wrappers (process early to track refs before emitting data types)
        error_wrapper_rows = []
        ep_files = list(self.input_dir.glob("*.xlsm")) + list(self.input_dir.glob("*.xlsx"))
        for ep_file in ep_files:
            if ep_file.name.startswith("$"):
                continue
            
            xl = pd.ExcelFile(ep_file)
            
            # ErrorResponse from 400+
            for sheet in xl.sheet_names:
                if sheet.isdigit() and int(sheet) >= 400:
                    children = self._read_legacy_structure(xl, sheet)
                    if children:  # Only emit if has children
                        child_rows, refs = self._build_children_rows("ErrorResponse", children, ep_file.name)
                        error_wrapper_rows = child_rows  # Store for later
                        referenced_data_types.update(refs)
                        break  # Only emit once

        # Section 1.8: Recursive reference expansion (transitive closures)
        processed_refs = set()
        while True:
            new_refs = set()
            for ref in referenced_data_types:
                if ref in processed_refs:
                    continue
                processed_refs.add(ref)
                
                # Fetch the DataType for this reference
                if ref in self.global_schemas:
                    dt = self.global_schemas[ref]
                    # If it's an array, it might reference another schema
                    if dt.items_type:
                        # Resolve items_type globally (heuristic fallback is fine here)
                        res_name, _ = self._resolve_data_type(dt.items_type)
                        if res_name and res_name not in referenced_data_types:
                            new_refs.add(res_name)
            
            if not new_refs:
                break
            referenced_data_types.update(new_refs)
        
        # Section 2: Data types (only those referenced - in insertion order)
        for out_name, dt in self.global_schemas.items():
            if out_name not in referenced_data_types:
                continue
                
            # Resolve items_type if it's a schema reference
            items_out_name = dt.items_type
            if dt.items_type:
                # Resolve items_type globally or within same schema context
                res_items_name, _ = self._resolve_data_type(dt.items_type)
                if res_items_name:
                    items_out_name = res_items_name
            
            final_rows.append([
                out_name, "", dt.description, dt.type if dt.type else "string",
                items_out_name,
                "", dt.format, "",
                dt.min_val, dt.max_val, dt.pattern_eba, dt.regex,
                dt.allowed_values, dt.example
            ])
        
        # Section 3: Error wrappers (emit pre-built rows)
        if error_wrapper_rows:
            final_rows.append(["ErrorResponse", "", "", "object", "", "", "", "", "", "", "", "", "", ""])
            final_rows.extend(error_wrapper_rows)
        
        self._write_rows(ws, final_rows, start_row=2)
    
    def _convert_endpoint(self, legacy_path: Path):
        """Convert endpoint *.xlsm to *.xlsx."""
        filename = legacy_path.name.replace(".xlsm", ".xlsx")
        print(f"Converting endpoint: {filename}")
        
        master_ep = self.master_dir / "endpoint.xlsm"
        if not master_ep.exists():
            master_ep = self.master_dir / "endpoint.xlsx"
            
        output_path = self.output_dir / filename
        shutil.copy(master_ep, output_path)
        
        self.current_ep_name = legacy_path.name
        
        wb = load_workbook(output_path)
        xl = pd.ExcelFile(legacy_path)
        
        op_id = self._extract_operation_id(legacy_path.name)
        status_codes = [s for s in xl.sheet_names if s.isdigit()]
        
        # Remove unused response sheets
        sheets_to_remove = [s for s in wb.sheetnames if s.isdigit() and s not in status_codes]
        for s in sheets_to_remove:
            del wb[s]
        
        # Create needed response sheets
        if "Response" in wb.sheetnames:
            response_tpl = wb["Response"]
            for code in status_codes:
                if code not in wb.sheetnames:
                    new_sheet = wb.copy_worksheet(response_tpl)
                    new_sheet.title = code
            del wb["Response"]
        
        # 1. Parameters
        self._convert_parameters(wb, xl)
        
        # 2. Body
        self._convert_body(wb, op_id)
        
        # 3. Response sheets
        self._convert_responses(wb, xl, op_id, status_codes, filename)
        
        wb.save(output_path)
        print(f"  Saved: {output_path}")
    
    def _convert_parameters(self, wb, xl):
        """Convert Parameters from Path and Header sheets."""
        ws = wb["Parameters"]
        
        params = []
        
        # Path parameters
        if "Path" in xl.sheet_names:
            df = pd.read_excel(xl, sheet_name="Path", dtype=str)
            params.extend(self._parse_params(df, "path"))
        
        # Header parameters
        if "Header" in xl.sheet_names:
            df = pd.read_excel(xl, sheet_name="Header", dtype=str)
            params.extend(self._parse_params(df, "header"))
            
        ep_filename = wb.properties.title if hasattr(wb, 'properties') and wb.properties.title else None
        # Since openpyxl title might not be set, use a better way to pass the filename
        # Actually, let's just use self.current_ep_filename if we set it
        ep_filename = self.current_ep_name
        
        # Write parameters with data type resolution
        rows = []
        for p in params:
            param_type = p["type"]
            param_format = ""
            param_min = ""
            param_max = ""
            # Resolve data type to primitive (v3: parameters stay inline as primitives)
            out_name, dt = self._resolve_data_type(param_type, ep_filename)
            if dt:
                param_type = dt.type
                param_format = dt.format
                param_min = dt.min_val
                param_max = dt.max_val
            
            rows.append([
                p["name"], p["description"], p["in"], param_type,
                "", "", param_format, p["mandatory"],
                param_min, param_max
            ])
        
        self._write_rows(ws, rows, start_row=3)
    
    def _convert_body(self, wb, op_id: str):
        """Convert Body sheet - simple wrapper reference."""
        ws = wb["Body"]
        
        wrapper_name = f"{op_id}Request"
        row = ["", wrapper_name, "", "", "object", "", "", "", "", "", "", "", "", "", ""]
        self._write_rows(ws, [row], start_row=3)
    
    def _convert_responses(self, wb, xl, op_id: str, status_codes: List[str], filename: str):
        """Convert response sheets."""
        for code in status_codes:
            if code not in wb.sheetnames:
                continue
            
            ws = wb[code]
            
            # Determine wrapper
            if int(code) < 400:
                wrapper_name = f"{op_id}Response"
            else:
                wrapper_name = "ErrorResponse"
            
            # Extract description from legacy title
            desc = ""
            try:
                df = pd.read_excel(xl, sheet_name=code, dtype=str, header=None)
                if not df.empty:
                    title_row = df.iloc[0].dropna().tolist()
                    for val in title_row:
                        s = str(val).strip()
                        if s.startswith(f"Response {code}"):
                            if " - " in s:
                                desc = s.split(" - ", 1)[1].strip()
                            break
            except:
                pass
            
            if not desc:
                desc = {"200": "OK", "201": "Created", "400": "Bad Request",
                        "401": "Unauthorized", "403": "Forbidden", "404": "Not Found"}.get(code, "")
            
            # Row 1: Response | code | description
            ws.cell(row=1, column=1).value = "Response"
            ws.cell(row=1, column=2).value = code
            ws.cell(row=1, column=3).value = desc
            
            # Row 3: content row
            row = ["content", "application/json", "", "", "schema", "", wrapper_name, "", "M",
                   "", "", "", "", "", ""]
            self._write_rows(ws, [row], start_row=3)
    
    # === Helper Methods ===
    
    def _read_legacy_structure(self, xl, sheet_name: str) -> List[Tuple]:
        """Read legacy Body/Response structure: (name, parent, description, type, mandatory)."""
        df = pd.read_excel(xl, sheet_name=sheet_name, dtype=str, header=None)
        
        # Representative keywords for header detection
        header_keywords = ["name", "element", "type", "parent", "data type", "description", "mandatory"]
        
        header_row_idx = self._find_header_row(df, header_keywords)
        
        if header_row_idx == -1:
            return []
        
        df.columns = [str(c).strip() for c in df.iloc[header_row_idx]]
        df = df.iloc[header_row_idx + 1:].reset_index(drop=True)
        
        children = []
        for _, row in df.iterrows():
            name = self._clean_value(row.get("Element", row.get("Name", "")))
            if not name or name.lower() == "nan":
                continue
            
            parent = self._clean_value(row.get("Parent", row.get("Parents", "")))
            desc = self._clean_value(row.get("Description ", row.get("Description", "")))
            # Handle 'Data Type' alias for 'Type'
            dtype = self._clean_value(row.get("Data Type", row.get("Type", "string")))
            mandatory = self._clean_value(row.get("Mandatory", ""))
            
            children.append((name, parent, desc, dtype, mandatory))
        
        return children
    
    def _build_children_rows(self, wrapper_name: str, children: List[Tuple], ep_filename: Optional[str] = None) -> Tuple[List[List], set]:
        """Build child rows with proper parent hierarchy and type resolution.
        Returns (rows, referenced_data_types set)."""
        rows = []
        referenced_data_types = set()
        
        # Build parent lookup (case-insensitive)
        parent_map = {}
        for name, parent, desc, dtype, mandatory in children:
            if parent:
                parent_map[name.lower()] = parent
        
        for name, parent, desc, dtype, mandatory in children:
            # Determine actual parent
            actual_parent = parent if parent else wrapper_name
            
            # Resolve type
            resolved_type = dtype
            schema_name = ""
            
            if dtype.lower() == "object":
                resolved_type = "object"
            elif dtype.lower() in ["string", "number", "integer", "boolean", "array"]:
                resolved_type = dtype.lower()
            else:
                # Data type reference
                out_name, _ = self._resolve_data_type(dtype, ep_filename)
                if out_name:
                    resolved_type = "schema"
                    schema_name = out_name
                    referenced_data_types.add(out_name)
                else:
                    resolved_type = dtype
            
            # Convert mandatory
            mand_value = "M" if mandatory in ["M", "m", "Yes", "yes", "Y", "y"] else \
                         "O" if mandatory in ["O", "o", "No", "no", "N", "n"] else mandatory
            
            rows.append([
                name, actual_parent, desc, resolved_type,
                "", schema_name, "", mand_value,
                "", "", "", "", "", ""
            ])
        
        return rows, referenced_data_types
    
    def _parse_params(self, df: pd.DataFrame, param_in: str) -> List[Dict]:
        """Parse parameters from Path/Header sheet."""
        header_row_idx = self._find_header_row(df, ["element", "name", "type"])
        
        if header_row_idx == -1:
            return []
        
        df.columns = df.iloc[header_row_idx]
        df = df.iloc[header_row_idx + 1:].reset_index(drop=True)
        
        params = []
        for _, row in df.iterrows():
            name = self._clean_value(row.get("Element", row.get("Request Header", row.get("Name", ""))))
            if not name or name.lower() in ["nan", "element", "name"]:
                continue
            
            desc = self._clean_value(row.get("Description ", row.get("Description", "")))
            dtype = self._clean_value(row.get("Type", "string"))
            mandatory = self._clean_value(row.get("Mandatory", ""))
            
            mand_value = "M" if mandatory in ["M", "m", "Yes", "yes"] else "O"
            
            params.append({
                "name": name,
                "description": desc,
                "in": param_in,
                "type": dtype,
                "mandatory": mand_value
            })
        
        return params
    
    def _extract_operation_id(self, filename: str) -> str:
        """Extract operationId from filename: testOperation.260209.xlsm → testOperation"""
        base = filename.replace(".xlsm", "").replace(".xlsx", "")
        parts = base.rsplit(".", 1)
        return parts[0] if len(parts) > 1 and parts[1].isdigit() else base
    
    def _find_header_row(self, df: pd.DataFrame, keywords: List[str]) -> int:
        """Find row containing header keywords by scoring matches."""
        best_idx = -1
        max_score = 0
        
        # Search first 15 rows for the best header candidate
        for idx in range(min(15, len(df))):
            row_vals = [str(v).lower().strip() for v in df.iloc[idx].values if v is not None]
            
            # Score this row based on how many keywords it matches
            score = 0
            for kw in keywords:
                # Check if keyword is present as a standalone part of any cell value
                if any(kw in val for val in row_vals):
                    score += 1
            
            if score > max_score:
                max_score = score
                best_idx = idx
        
        # Confidence threshold: at least 2 keywords must match
        return best_idx if max_score >= 2 else -1
    
    def _find_column(self, df: pd.DataFrame, keywords: List[str]) -> Optional[str]:
        """Find column by keywords."""
        for col in df.columns:
            col_lower = str(col).lower()
            if any(kw in col_lower for kw in keywords):
                return col
        return None
    
    def _to_pascal_case(self, name: str) -> str:
        """Simple PascalCase conversion to match R1 expectations."""
        if not name: return name
        name = str(name).strip()
        if not name or name.lower() == "nan": return name
        
        # For simplicity and R1 compatibility, only uppercase first char 
        # unless it has underscores which we convert to CamelCase.
        if "_" in name or "-" in name:
            import re
            parts = re.split(r'[^a-zA-Z0-9]+', name)
            return "".join(p.capitalize() for p in parts if p)
        
        return name[0].upper() + name[1:]
    
    def _clean_value(self, val) -> str:
        """Clean cell value."""
        s = str(val).strip()
        return "" if s.lower() == "nan" else s
    
    def _ensure_xlsx_extension(self, filename) -> str:
        """Ensure filename has .xlsx extension."""
        fname = str(filename).strip()
        if not fname or fname.lower() == "nan":
            return fname
        if not fname.endswith(".xlsx") and not fname.endswith(".xlsm"):
            return fname + ".xlsx"
        if fname.endswith(".xlsm"):
            return fname.replace(".xlsm", ".xlsx")
        return fname
    
    def _write_rows(self, ws, rows: List[List], start_row: int = 3):
        """Write rows to worksheet."""
        for r_idx, row in enumerate(rows, start=start_row):
            for c_idx, value in enumerate(row, start=1):
                ws.cell(row=r_idx, column=c_idx).value = value if value != "" else None
