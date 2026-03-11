"""
Legacy Excel to Modern OAS Converter - Clean Implementation

Converts legacy Excel API specifications to modern OAS format.
Architecture: Simple linear flow with direct sheet transformations.
"""
import os
import shutil
import re
from pathlib import Path
from collections import OrderedDict
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Any
import pandas as pd
import openpyxl
from openpyxl import load_workbook
from openpyxl.styles import Alignment
from openpyxl.utils import get_column_letter
import yaml


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
    items_type: str = ""
    source_file: str = "" # Track origin for collision resolution


class LegacyConverter:
    """Converts legacy Excel templates to modern OAS format."""
    
    def __init__(self, input_dir: str, output_dir: str, master_dir: str = None, log_callback=None):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.master_dir = Path(master_dir) if master_dir else None
        self.log = log_callback or print
        self.tracing_enabled = True # Default
        
        # Internal registry
        self.global_schemas: Dict[str, DataType] = {} # out_name -> DataType
        self.used_names = set()
        self.fingerprints = {} # fingerprint -> out_name
        self.output_names = {} # (filename, original_name) -> out_name
        
        # Double-pass state
        self.raw_data_types: Dict[str, Dict[str, DataType]] = {} # file_key -> {norm_name -> DataType}
        self.ordered_filenames: List[str] = [] # list of filenames in index order
        self.schema_usage: Dict[str, List[str]] = {} # out_name -> ["op_id (sheet)", ...]
        
        # Operation IDs mapping
        self.filename_to_opid = {}
        self.emitted_wrappers = set()
        self.current_ep_name = None
        self.all_tags = set() # Track all tags for the index

    def _resolve_internal_master_dir(self):
        """Finds 'Templates Master' folder as an internal resource."""
        import sys
        # 1. If frozen (PyInstaller EXE)
        if getattr(sys, 'frozen', False):
            base = Path(sys._MEIPASS)
            cand = base / "Templates Master"
            if cand.exists():
                return cand

        # 2. Development mode - Relative to script
        # src/legacy_converter.py -> project_root/Templates Master
        cand = Path(__file__).parent.parent / "Templates Master"
        if cand.exists():
            return cand

        # 3. Fallback to CWD
        cand = Path.cwd() / "Templates Master"
        if cand.exists():
            return cand
            
        return None

    def convert(self, tracing_enabled=True):
        """Main conversion entry point."""
        if self.master_dir is None:
            self.master_dir = self._resolve_internal_master_dir()
        
        if self.master_dir is None:
            self.log("CRITICAL ERROR: Internal 'Templates Master' folder not found. Please contact support.")
            return False
            
        self.tracing_enabled = tracing_enabled
        if not self.output_dir.exists():
            self.output_dir.mkdir(parents=True)
            
        # 1. Collection Phase
        index_path = self.input_dir / "$index.xlsm"
        if not index_path.exists():
            index_path = self.input_dir / "$index.xlsx"
            
        if index_path.exists():
            self._pre_read_index(index_path)
            
        self.log("Collecting data types from all endpoints...")
        self._collect_all_data_types()
        
        self.log("Performing naming and usage analysis pass...")
        self._perform_naming_and_usage_pass()
        self.log(f"  Loaded {len(self.global_schemas)} unique global schemas.")

        # 2. Index Phase
        if index_path.exists():
            self._convert_index(index_path)

        # 3. Endpoint Phase
        # Follow the same order as the naming pass for consistency
        for ep_filename in self.ordered_filenames:
            ep_file = self.input_dir / ep_filename
            if ep_file.exists():
                self._convert_endpoint(ep_file)
                
        # Also catch any files not in the index (edge case)
        for ep_file in self.input_dir.glob("*.xlsm"):
            if ep_file.name.startswith(("$", "~")): continue
            if ep_file.name not in self.ordered_filenames:
                self._convert_endpoint(ep_file)
        for ep_file in self.input_dir.glob("*.xlsx"):
            if ep_file.name.startswith(("$", "~")): continue
            if ep_file.name not in self.ordered_filenames:
                self._convert_endpoint(ep_file)

        # 11. Final Summary
        if self.tracing_enabled:
            self._log_usage_summary()
        self.log(f"Conversion complete. Output: {self.output_dir}")
        return True


    def _collect_all_data_types(self):
        """Collect all data types from all endpoint 'Data Type' sheets."""
        # First from $index (if any global types defined there)
        idx_path = self.input_dir / "$index.xlsm"
        if not idx_path.exists():
            idx_path = self.input_dir / "$index.xlsx"
            
        if idx_path.exists():
            self._collect_data_types_from_file(idx_path, is_global=True)
            
        # Then from all endpoints (unordered first to collect all possible definitions)
        ep_files = list(self.input_dir.glob("*.xlsm")) + list(self.input_dir.glob("*.xlsx"))
        for ep_file in ep_files:
            if not ep_file.name.startswith(("$", "~")):
                self._collect_data_types_from_file(ep_file)

    def _collect_data_types_from_file(self, file_path: Path, is_global: bool = False):
        """Collect data types from a single file's 'Data Type' sheet."""
        xl = pd.ExcelFile(file_path)
        if "Data Type" not in xl.sheet_names:
            return
            
        df = pd.read_excel(xl, sheet_name="Data Type", dtype=str, header=None)
        header_keywords = ["name", "type", "description"]
        header_row_idx = self._find_header_row(df, header_keywords)
        
        if header_row_idx == -1:
            return
            
        df.columns = [str(c).strip().lower() for c in df.iloc[header_row_idx]]
        df = df.iloc[header_row_idx + 1:].reset_index(drop=True)
        file_key = "$global" if is_global else file_path.name
        
        def gv(keywords, default=""):
            for col in df.columns:
                if any(kw in str(col).lower() for kw in keywords):
                    return col
            return None

        name_c = gv(["name"])
        desc_c = gv(["description"])
        type_c = gv(["type"])
        fmt_c = gv(["format"])
        items_c = gv(["items data type", "array only"])
        min_c = gv(["min"])
        max_c = gv(["max"])
        reg_c = gv(["regex"])
        pat_c = gv(["pattern", "eba"])
        all_c = gv(["allowed value", "allowed"])
        ex_c = gv(["example"])
        
        for _, row in df.iterrows():
            name = self._clean_value(row.get(name_c, ""))
            if not name or str(name).lower() == "nan": continue
            
            norm_name = self._to_pascal_case(name)
            dt = DataType(
                name=norm_name,
                type=self._clean_value(row.get(type_c, "string")),
                format=self._clean_value(row.get(fmt_c, "")),
                min_val=self._clean_value(row.get(min_c, "")),
                max_val=self._clean_value(row.get(max_c, "")),
                description=self._clean_value(row.get(desc_c, "")),
                pattern_eba=self._clean_value(row.get(pat_c, "")),
                regex=self._clean_value(row.get(reg_c, "")),
                allowed_values=self._clean_value(row.get(all_c, "")),
                example=self._clean_value(row.get(ex_c, "")),
                items_type=self._clean_value(row.get(items_c, "")),
                source_file=file_key
            )
            
            # Defer registration naming
            if file_key not in self.raw_data_types:
                self.raw_data_types[file_key] = {}
            self.raw_data_types[file_key][norm_name] = dt

    def _register_data_type(self, file_key: str, norm_name: str, dt: DataType):
        """Registers a data type, deduplicating by content and handling name collisions."""
        # Fingerprint for deduplication (exclude name, source_file, and pattern_eba)
        fp_data = {k: v for k, v in dt.__dict__.items() if k not in ['name', 'source_file', 'pattern_eba']}
        
        # Normalize lists (ignore separators and extra spaces)
        def normalize_list(v):
            if not isinstance(v, str): return v
            # Replace ; with , and normalize spaces around commas
            v = re.sub(r'\s*;\s*', ',', v)
            v = re.sub(r'\s*,\s*', ',', v)
            return v.strip().strip(',')

        if 'allowed_values' in fp_data:
            fp_data['allowed_values'] = normalize_list(fp_data['allowed_values'])
        if 'example' in fp_data:
            fp_data['example'] = normalize_list(fp_data['example'])
            
        fingerprint = tuple(sorted(fp_data.items()))
        
        mapping_key = (file_key, norm_name)
        
        # 1. Content-based deduplication
        if fingerprint in self.fingerprints:
            out_name = self.fingerprints[fingerprint]
            self.output_names[mapping_key] = out_name
            return out_name
            
        # 2. Name collision handling for new unique content
        output_name = norm_name
        counter = 1
        while output_name in self.used_names:
            output_name = f"{norm_name}{counter}"
            counter += 1
            
        # 3. Commit to registry
        self.global_schemas[output_name] = dt
        self.used_names.add(output_name)
        self.fingerprints[fingerprint] = output_name
        self.output_names[mapping_key] = output_name
        return output_name

    def _resolve_data_type(self, name: str, ep_filename: Optional[str] = None) -> Tuple[Optional[str], Optional[DataType]]:
        """Resolves a named data type to its unique global output name and DataType object."""
        norm_name = self._to_pascal_case(name)
        
        # 1. Try currently registered types (output_names already has the final name)
        # Check specific file context first
        if ep_filename:
            mapping_key = (ep_filename, norm_name)
            if mapping_key in self.output_names:
                out_name = self.output_names[mapping_key]
                return out_name, self.global_schemas.get(out_name)
        
        # Check global context
        mapping_key_global = ("$global", norm_name)
        if mapping_key_global in self.output_names:
            out_name = self.output_names[mapping_key_global]
            return out_name, self.global_schemas.get(out_name)
            
        # 2. Not registered yet. This happens during the Naming Pass.
        # Find the best raw definition available
        raw_dt = None
        # Prioritize the current file's raw definition
        if ep_filename and ep_filename in self.raw_data_types and norm_name in self.raw_data_types[ep_filename]:
            raw_dt = self.raw_data_types[ep_filename][norm_name]
            file_key_for_registration = ep_filename
        # Fallback to global raw definition
        elif "$global" in self.raw_data_types and norm_name in self.raw_data_types["$global"]:
            raw_dt = self.raw_data_types["$global"][norm_name]
            file_key_for_registration = "$global"
            
        if raw_dt:
            # During naming pass, we REGISTER it now
            out_name = self._register_data_type(file_key_for_registration, norm_name, raw_dt)
            return out_name, raw_dt
            
        return None, None

    def _perform_naming_and_usage_pass(self):
        """Pass 2: Determine naming priority based on index order and track usage."""
        # 1. First, register all Global types from $index (highest priority)
        global_types = self.raw_data_types.get("$global", {})
        for norm_name, dt in global_types.items():
            self._register_data_type("$global", norm_name, dt)
            
        # 2. Then follow index order
        for ep_filename in self.ordered_filenames:
            ep_file = self.input_dir / ep_filename
            if not ep_file.exists(): continue
            
            try:
                xl = pd.ExcelFile(ep_file)
                op_id = self.filename_to_opid.get(ep_filename, self._extract_operation_id(ep_filename))
                
                # Check Path & Header for refs
                for sheet in ["Path", "Header"]:
                    if sheet in xl.sheet_names:
                        df = pd.read_excel(xl, sheet_name=sheet, dtype=str, header=None)
                        hr = self._find_header_row(df, ["name", "type"])
                        if hr != -1:
                            df.columns = [str(c).strip() for c in df.iloc[hr]]
                            df = df.iloc[hr+1:]
                            for _, row in df.iterrows():
                                dtype = self._clean_value(row.get("Type", ""))
                                if dtype and dtype.lower() not in ["string", "number", "integer", "boolean", "array", "object"]:
                                    out_name, _ = self._resolve_data_type(dtype, ep_filename)
                                    if out_name:
                                        if out_name not in self.schema_usage: self.schema_usage[out_name] = []
                                        usage_str = f"{op_id} ({sheet})"
                                        if usage_str not in self.schema_usage[out_name]:
                                            self.schema_usage[out_name].append(usage_str)
                                            
                # Check Body & Responses
                for sheet in xl.sheet_names:
                    if sheet in ["Body", "200", "201", "400", "401", "403", "404", "500"]:
                        children = self._read_legacy_structure(xl, sheet)
                        for child_tuple in children:
                            # Unpack: (name, parent, desc, dtype, mandatory, v_rules)
                            self._track_recursive_usage(child_tuple, ep_filename, op_id, sheet)
            except Exception as e:
                self.log(f"Error in naming pass for {ep_filename}: {e}")

    def _track_recursive_usage(self, child_tuple, ep_filename, op_id, sheet):
        """Recursively track usage of types in objects/arrays."""
        # Tuple: (name, parent, desc, dtype, mandatory, v_rules, items_type)
        dtype = child_tuple[3]
        items_type_ref = child_tuple[6] if len(child_tuple) > 6 else ""
        
        def track_name(name_to_track):
            if not name_to_track: return
            if name_to_track.lower() in ["string", "number", "integer", "boolean", "array", "object"]:
                return
            out_name, dt = self._resolve_data_type(name_to_track, ep_filename)
            if out_name:
                if out_name not in self.schema_usage: self.schema_usage[out_name] = []
                usage_str = f"{op_id} ({sheet})"
                if usage_str not in self.schema_usage[out_name]:
                    self.schema_usage[out_name].append(usage_str)
                
                # If this is an array, track its items too
                if dt and dt.type.lower() == "array" and dt.items_type:
                    track_name(dt.items_type)

        track_name(dtype)
        if items_type_ref:
            track_name(items_type_ref)

    def _log_usage_summary(self):
        """Log the alphabetical list of schemas and where they are used with absolute property values."""
        
        col1_w, col2_w, col3_w = 45, 55, 50
        header = f"| {'SCHEMA NAME':<{col1_w}} | {'USED IN (OPERATIONID - SHEET)':<{col2_w}} | {'DIFFERENCES':<{col3_w}} |"
        sep = "-" * len(header)
        
        self.log("\n" + "="*len(header))
        self.log(header)
        self.log(sep)
        
        sorted_names = sorted(self.schema_usage.keys(), key=lambda x: x.lower())
        
        # Grouping by strictly contiguous suffix only if base stem exists
        groups = {}
        for name in sorted_names:
            groups[name] = [name] # Default initialized to solo group
            
        base_names = set(sorted_names)
        processed = set()
        
        # We need to iterate over all names, identify pure base names, and scoop contiguous children.
        # A pure base name has no trailing digits (or isn't considered a variant root).
        for name in sorted_names:
            if name in processed: continue
            
            # Check if it has trailing digits
            m = re.search(r'(\d+)$', name)
            if not m:
                # This is a potential base. Let's scoop its contiguous children.
                current_group = [name]
                processed.add(name)
                
                suffix = 1
                while True:
                    expected_child = f"{name}{suffix}"
                    if expected_child in base_names:
                        current_group.append(expected_child)
                        processed.add(expected_child)
                        suffix += 1
                    else:
                        break # Contiguity broken
                
                groups[name] = current_group

        # Any name that has trailing digits but WAS NOT scooped by its exact stem (either because 
        # the stem doesn't exist, or it was non-contiguous) is already in `groups` as a solo group.
        # We just need to clean up `groups` to only contain the roots we actually want to display 
        # (the keys of `groups` must be the first element of each group block).
        
        final_groups = {}
        for v_list in groups.values():
            if not v_list: continue
            root_key = v_list[0]
            # Since `groups` started with {each_name: [each_name]}, an unscooped variant 
            # will still have itself as root_key. This is correct.
            final_groups[root_key] = v_list
            
        # Find which attributes actually differ in each group
        mismatches_by_group = {}
        attrs = ['type', 'format', 'min_val', 'max_val', 'regex', 'allowed_values', 'items_type']
        for root_name, members in final_groups.items():
            if len(members) <= 1: continue
            
            diff_fields = set()
            dts = [self.global_schemas.get(m) for m in members if self.global_schemas.get(m)]
            if not dts: continue
            
            # Compare all against first
            base = dts[0]
            for other in dts[1:]:
                for attr in attrs:
                    v_base = getattr(base, attr) or ""
                    v_other = getattr(other, attr) or ""
                    # Normalize strings for comparison (NaN already handled as empty string during load)
                    if str(v_base).strip() != str(v_other).strip():
                        diff_fields.add(attr)
            
            if diff_fields:
                mismatches_by_group[root_name] = sorted(list(diff_fields))

        def wrap_text(text, width):
            """Robust text wrapping that breaks long words."""
            if not text: return []
            lines = []
            paragraphs = text.split('\n')
            for p in paragraphs:
                words = p.split()
                if not words:
                    lines.append("")
                    continue
                current_line = []
                for word in words:
                    # If word exceeds width, break it
                    if len(word) > width:
                        if current_line:
                            lines.append(" ".join(current_line))
                            current_line = []
                        while len(word) > width:
                            lines.append(word[:width])
                            word = word[width:]
                        current_line = [word]
                    elif sum(len(w) for w in current_line) + len(current_line) + len(word) <= width:
                        current_line.append(word)
                    else:
                        lines.append(" ".join(current_line))
                        current_line = [word]
                if current_line:
                    lines.append(" ".join(current_line))
            return lines

        for out_name in sorted_names:
            usages = self.schema_usage[out_name]
            
            # Figure out which root group this name belongs to for mismatch lookup
            # If it's the root itself, use it.
            # If it's a child, we need to know its root. We can inverse map final_groups.
            root_for_mismatch = out_name
            for r_key, members in final_groups.items():
                if out_name in members:
                    root_for_mismatch = r_key
                    break
                    
            relevant_fields = mismatches_by_group.get(root_for_mismatch, [])
            
            diff_str = ""
            if relevant_fields:
                dt = self.global_schemas.get(out_name)
                if dt:
                    bits = []
                    for attr in relevant_fields:
                        val = getattr(dt, attr)
                        label = attr.replace('_', ' ').title()
                        disp = val if val and str(val).lower() != "nan" else "(empty)"
                        bits.append(f"{label}: {disp}")
                    diff_str = "; ".join(bits)
            
            # WRAP ALL COLUMNS
            name_lines = wrap_text(out_name, col1_w)
            usage_lines = []
            for u in usages:
                usage_lines.extend(wrap_text(u, col2_w))
            diff_lines = wrap_text(diff_str, col3_w)
            
            max_lines = max(len(name_lines), len(usage_lines), len(diff_lines), 1)
            for i in range(max_lines):
                n_cell = name_lines[i] if i < len(name_lines) else ""
                u_cell = usage_lines[i] if i < len(usage_lines) else ""
                d_cell = diff_lines[i] if i < len(diff_lines) else ""
                self.log(f"| {n_cell:<{col1_w}} | {u_cell:<{col2_w}} | {d_cell:<{col3_w}} |")
            
            self.log(sep)
            
        self.log("="*len(header) + "\n")

    def run_standalone_check(self, folder_path):
        """Analyze an existing converted folder by reading its $index file and all endpoints."""
        p = Path(folder_path)
        index_file = None
        for name in ["$index.xlsx", "$index.xlsm"]:
            if (p / name).exists():
                index_file = p / name
                break
        
        if not index_file:
            self.log(f"Error: Could not find $index file in {folder_path}")
            return False
            
        self.log(f"Analyzing project: {p.name}")
        self.log(f"Reading index: {index_file.name}")
        
        try:
            xl_idx = pd.ExcelFile(index_file)
            
            # 1. Load Schemas for definition details
            if "Schemas" in xl_idx.sheet_names:
                df_s = pd.read_excel(xl_idx, sheet_name="Schemas", dtype=str, header=None)
                header_idx = self._find_header_row(df_s, ["name", "type"])
                if header_idx != -1:
                    header_vals = [str(c).strip().lower() for c in df_s.iloc[header_idx]]
                    df_s.columns = header_vals
                    df_s = df_s.iloc[header_idx + 1:].reset_index(drop=True)
                    
                    def get_col_val(r, exact_kws, partial_kws=None):
                        for c in df_s.columns:
                            if str(c) in exact_kws: return self._clean_value(r.get(c))
                        if partial_kws:
                            for c in df_s.columns:
                                if any(kw in str(c) for kw in partial_kws): return self._clean_value(r.get(c))
                        return ""

                    for _, row in df_s.iterrows():
                        name = self._clean_value(row.get('name'))
                        if not name: continue
                        
                        dt = DataType(
                            name=name,
                            type=get_col_val(row, ['type']) or 'string',
                            format=get_col_val(row, ['format']),
                            min_val=get_col_val(row, ['minimum'], ['min ']),
                            max_val=get_col_val(row, ['maximum'], ['max ']),
                            regex=get_col_val(row, ['regex', 'pattern']),
                            allowed_values=get_col_val(row, ['enum', 'allowed value']),
                            items_type=get_col_val(row, ['items type'], ['items data type'])
                        )
                        self.global_schemas[name] = dt


            # 2. Get list of endpoint files from Paths sheet
            ep_files = []
            if "Paths" in xl_idx.sheet_names:
                df_p = pd.read_excel(xl_idx, sheet_name="Paths", dtype=str, header=None)
                h_idx = self._find_header_row(df_p, ["excel file", "operationid"])
                if h_idx != -1:
                    h_vals = [str(c).strip().lower() for c in df_p.iloc[h_idx]]
                    df_p.columns = h_vals
                    df_p = df_p.iloc[h_idx + 1:].reset_index(drop=True)
                    for _, row in df_p.iterrows():
                        fname = self._clean_value(row.get('excel file'))
                        opid = self._clean_value(row.get('operationid'))
                        if fname:
                            ep_files.append((fname, opid))

            # 3. Map usages across all endpoint files
            for fname, op_id in ep_files:
                fpath = p / fname
                if not fpath.exists():
                    self.log(f"Warning: Endpoint file {fname} not found, skipping usage mapping.")
                    continue
                
                try:
                    xl_ep = pd.ExcelFile(fpath)
                    for sheet_name in xl_ep.sheet_names:
                        if sheet_name in ["General Description", "Paths", "Tags", "Schemas"]: continue
                        
                        df = pd.read_excel(xl_ep, sheet_name=sheet_name, dtype=str, header=None)
                        
                        # Search for 'data type' columns
                        potential_cols = []
                        header_row = -1
                        for r_idx in range(min(10, len(df))):
                            try:
                                row_vals = [str(v).lower() for v in df.iloc[r_idx]]
                                if any("data type" in v for v in row_vals):
                                    potential_cols = [i for i, v in enumerate(row_vals) if "data type" in v]
                                    header_row = r_idx
                                    break
                            except: continue
                        
                        if potential_cols and header_row != -1:
                            for _, row in df.iloc[header_row+1:].iterrows():
                                for col_idx in potential_cols:
                                    dtype = self._clean_value(row.iloc[col_idx])
                                    if dtype and dtype not in ["string", "number", "integer", "boolean", "array", "object"]:
                                        if dtype not in self.schema_usage: self.schema_usage[dtype] = []
                                        usage_str = f"{op_id} ({sheet_name})"
                                        if usage_str not in self.schema_usage[dtype]:
                                            self.schema_usage[dtype].append(usage_str)
                except Exception as ex:
                    self.log(f"Error reading endpoint {fname}: {ex}")

            self._log_usage_summary()
            return True
            
        except Exception as e:
            self.log(f"Error during standalone check: {e}")
            return False
    
    def _pre_read_index(self, index_path: Path):
        """Pre-read index to map filenames to operationIds."""
        try:
            xl = pd.ExcelFile(index_path)
            if "Paths" in xl.sheet_names:
                df = pd.read_excel(xl, sheet_name="Paths", dtype=str, header=None)
                header_row_idx = self._find_header_row(df, ["excel file", "operationid"])
                if header_row_idx == -1: return
                
                # Robust headers
                header_vals = [str(c).strip().lower() for c in df.iloc[header_row_idx]]
                df.columns = header_vals
                df = df.iloc[header_row_idx + 1:].reset_index(drop=True)
                
                # Find indices by keyword to avoid series issues if duplicate columns exist
                file_idx = next((i for i, h in enumerate(header_vals) if "excel file" in h or "file" in h), -1)
                op_idx = next((i for i, h in enumerate(header_vals) if "operationid" in h or "operation id" in h), -1)
                
                if file_idx != -1 and op_idx != -1:
                    for _, row in df.iterrows():
                        entry_name = self._clean_value(row.iloc[file_idx])
                        opid = self._clean_value(row.iloc[op_idx])
                        if entry_name and opid:
                            # Find physical file on disk (index often omits extension)
                            actual_fname = None
                            for ext in [".xlsm", ".xlsx", ""]:
                                test_name = entry_name if entry_name.lower().endswith(tuple([".xlsm", ".xlsx"])) else f"{entry_name}{ext}"
                                if (self.input_dir / test_name).exists():
                                    actual_fname = test_name
                                    break
                            
                            if actual_fname:
                                self.filename_to_opid[actual_fname] = opid
                                if actual_fname not in self.ordered_filenames:
                                    self.ordered_filenames.append(actual_fname)
                                # Also map without extension for robustness
                                self.filename_to_opid[actual_fname.replace(".xlsx", "").replace(".xlsm", "")] = opid
                            else:
                                self.log(f"  WARNING: File '{entry_name}' from index not found in {self.input_dir}")
        except Exception as e:
            self.log(f"Error pre-reading index: {e}")

    def _convert_index(self, legacy_path: Path):
        """Convert $index.xlsm or $index.xlsx to $index.xlsx in output."""
        self.log(f"Converting index: {legacy_path.name}")
        
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
        
        # Cosmetic Polish
        try:
            wb = load_workbook(output_path)
            for sheet_name in wb.sheetnames:
                self._autofit_columns(wb[sheet_name])
            wb.save(output_path)
        except Exception as e:
            self.log(f"  WARNING: Could not apply cosmetic polish to index: {e}")
        self.log(f"  Saved: {output_path}")
    
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
                # Handle servers with 4 columns: [servers url, url, servers description, desc]
                if key == "servers url":
                    url = vals[1]
                    # FIX: Ignore labels or placeholders
                    if url.lower() in ["servers url", "server url", "url", "servers description", "server description"]:
                        continue
                        
                    desc = vals[3] if len(vals) >= 4 else ""
                    # FIX: Clean placeholder description
                    if desc.lower() in ["servers description", "server description", "description"]:
                        desc = ""
                        
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
        
        # Format Custom Extensions to YAML (no curly braces)
        ext_col = self._find_column(df, ["custom extensions", "extension"])
        if ext_col:
            df[ext_col] = df[ext_col].apply(self._format_extensions)
        
        # Write rows
        rows = df.values.tolist()
        self._write_rows(ws, rows, start_row=3)
    
    def _format_extensions(self, val) -> str:
        """Convert JSON-formatted extensions to clean YAML key: value format.
        
        Only transforms strings that are valid JSON objects (dicts).
        All other strings are passed through unchanged.
        """
        import json
        s = str(val).strip()
        if not s or s.lower() == "nan":
            return ""
        
        # Only convert if the string is a valid JSON object
        if s.startswith("{") and s.endswith("}"):
            try:
                data = json.loads(s)
                if isinstance(data, dict):
                    return "\n".join([f"{k}: {v}" for k, v in data.items()])
            except (json.JSONDecodeError, ValueError):
                pass
        
        # Everything else: return as-is (already YAML or plain text)
        return s
    
    def _convert_tags(self, wb):
        """Convert Tags sheet."""
        ws = wb["Tags"]
        
        # Clear existing
        for row in range(2, ws.max_row + 1):
            for col in range(1, ws.max_column + 1):
                ws.cell(row=row, column=col).value = None
        
        tags_data = [[tag, tag] for tag in sorted(self.all_tags)]
        self._write_rows(ws, tags_data, start_row=2)
    
    def _convert_schemas(self, wb):
        """Convert Schemas sheet - builds hierarchy from Body/Response structures and Global Data Types."""
        ws = wb["Schemas"]
        
        # Clear existing
        for row in range(2, ws.max_row + 1):
            for col in range(1, ws.max_column + 1):
                ws.cell(row=row, column=col).value = None
        
        final_rows = []
        referenced_data_types = set()
        
        # 1. Collect all referenced schemas from endpoints
        ep_files = [f for f in self.input_dir.glob("*.xlsm") if not f.name.startswith(("$", "~"))] + \
                   [f for f in self.input_dir.glob("*.xlsx") if not f.name.startswith(("$", "~"))]
        for ep_file in ep_files:
            xl = pd.ExcelFile(ep_file)
            
            # 1.1 Params
            for sheet_name in ["Path", "Header"]:
                if sheet_name in xl.sheet_names:
                    df = pd.read_excel(xl, sheet_name=sheet_name, dtype=str, header=None)
                    header_row_idx = self._find_header_row(df, ["name", "type"])
                    if header_row_idx != -1:
                        df.columns = [str(c).strip() for c in df.iloc[header_row_idx]]
                        df = df.iloc[header_row_idx + 1:]
                        for _, row in df.iterrows():
                            dtype = self._clean_value(row.get("Type", ""))
                            if dtype and dtype.lower() not in ["string", "number", "integer", "boolean", "array", "object"]:
                                out_name, _ = self._resolve_data_type(dtype, ep_file.name)
                                if out_name: referenced_data_types.add(out_name)
            
            # 1.2 Body & Responses (Wrappers)
            op_id_raw = self.filename_to_opid.get(ep_file.name, self._extract_operation_id(ep_file.name))
            op_id = self._to_pascal_case(op_id_raw)
            
            if "Body" in xl.sheet_names:
                children = self._read_legacy_structure(xl, "Body")
                if children:
                    wrapper = f"{op_id}Request"
                    self.emitted_wrappers.add(wrapper)
                    child_rows, refs = self._build_children_rows(wrapper, children, ep_file.name)
                    final_rows.append([wrapper, "", "", "object", "", "", "", "", "", "", "", "", "", ""])
                    final_rows.extend(child_rows)
                    referenced_data_types.update(refs)
            
            for code in ["200", "201", "400", "401", "403", "404", "500"]:
                if code in xl.sheet_names:
                    children = self._read_legacy_structure(xl, code)
                    if children:
                        wrapper = "ErrorResponse" if int(code) >= 400 else f"{op_id}Response"
                        if wrapper not in self.emitted_wrappers:
                            self.emitted_wrappers.add(wrapper)
                            child_rows, refs = self._build_children_rows(wrapper, children, ep_file.name)
                            final_rows.append([wrapper, "", "", "object", "", "", "", "", "", "", "", "", "", ""])
                            final_rows.extend(child_rows)
                            referenced_data_types.update(refs)
                        else:
                            _, refs = self._build_children_rows(wrapper, children, ep_file.name)
                            referenced_data_types.update(refs)

        # 2. Emit actually used Global Schemas
        global_blocks = []
        for out_name in sorted(referenced_data_types):
            if out_name in self.emitted_wrappers: continue
            
            # RULE: Filter out literal 'array' or 'object' schemas as they are handled inlined
            if out_name.lower() in ["array", "object"]: continue

            dt = self.global_schemas.get(out_name)
            if not dt: continue
            
            # Resolve Items Type recursively if it's an array
            # Rule: only inline if name is 'object' or 'array'
            items_out = dt.items_type
            if dt.type.lower() == "array" and dt.items_type:
                # Use recursive resolution helper
                items_out = self._recursive_resolve_items(dt.items_type, dt.source_file)
            
            row = [out_name, "", dt.description, dt.type if dt.type else "string",
                   items_out, "", dt.format, "", dt.min_val, dt.max_val,
                   dt.pattern_eba, dt.regex, dt.allowed_values, dt.example, ""]
            global_blocks.append((out_name, [row]))

        # 3. Final Write-back with Cosmetics
        all_blocks = []
        # Group final_rows back into blocks for sorting
        curr_b = []
        for r in final_rows:
            if r[1] == "":
                if curr_b: all_blocks.append((curr_b[0][0], curr_b))
                curr_b = [r]
            else: curr_b.append(r)
        if curr_b: all_blocks.append((curr_b[0][0], curr_b))
        
        all_blocks.extend(global_blocks)
        all_blocks.sort(key=lambda x: str(x[0]).lower())
        
        final_final_rows = []
        for i, (_, block) in enumerate(all_blocks):
            final_final_rows.extend(block)
            if i < len(all_blocks) - 1:
                final_final_rows.append([None] * 14) # Blank line R10
                
        # Compute hierarchy levels for grouping.
        # Level is written to column O (15) and used for Excel outline grouping.
        def _ensure_len_15(r: List[Any]) -> List[Any]:
            rr = list(r)
            while len(rr) < 15:
                rr.append("")
            return rr

        enriched_rows: List[List[Any]] = []
        parent_map: Dict[str, str] = {}
        in_block = False
        for r in final_final_rows:
            if r is None:
                continue
            if all(v is None or v == "" for v in r):
                enriched_rows.append(_ensure_len_15(r))
                parent_map = {}
                in_block = False
                continue

            rr = _ensure_len_15(r)
            name = rr[0] if len(rr) > 0 else ""
            parent = rr[1] if len(rr) > 1 else ""
            if parent == "" or parent is None:
                level = 0
                parent_map = {}
                in_block = True
            else:
                if in_block and isinstance(name, str) and name:
                    parent_map[str(name)] = str(parent) if parent is not None else ""

                level = 1
                cur = str(parent) if parent is not None else ""
                guard = 0
                while cur and guard < 50:
                    p2 = parent_map.get(cur)
                    if not p2:
                        break
                    level += 1
                    cur = p2
                    guard += 1

            rr[14] = level
            enriched_rows.append(rr)

        self._write_rows(ws, enriched_rows, start_row=2)

        try:
            ws.column_dimensions["O"].hidden = True
        except Exception:
            pass

        try:
            ws.sheet_properties.outlinePr.summaryBelow = True
        except Exception:
            pass

        try:
            for i, r in enumerate(enriched_rows, start=2):
                lvl = r[14]
                if isinstance(lvl, int) and lvl >= 0:
                    ws.row_dimensions[i].outlineLevel = min(lvl, 7)
                    ws.row_dimensions[i].hidden = False

                    # Visual indent in column A based on level (does not change cell content)
                    try:
                        cell = ws.cell(row=i, column=1)
                        indent = min(max(lvl, 0) * 2, 15)
                        cell.alignment = Alignment(horizontal="left", wrap_text=False, indent=indent)
                    except Exception:
                        pass
        except Exception:
            pass
    
    def _convert_endpoint(self, legacy_path: Path):
        """Convert endpoint *.xlsm to *.xlsx."""
        filename = legacy_path.name.replace(".xlsm", ".xlsx")
        self.log(f"Converting endpoint: {filename}")
        
        master_ep = self.master_dir / "endpoint.xlsm"
        if not master_ep.exists():
            master_ep = self.master_dir / "endpoint.xlsx"
            
        output_path = self.output_dir / filename
        shutil.copy(master_ep, output_path)
        
        self.current_ep_name = legacy_path.name
        
        wb = load_workbook(output_path)
        xl = pd.ExcelFile(legacy_path)
        
        # Get op_id from mapping or fallback to filename
        op_id_raw = self.filename_to_opid.get(legacy_path.name, 
                 self.filename_to_opid.get(legacy_path.name.replace(".xlsm", "").replace(".xlsx", ""),
                 self._extract_operation_id(legacy_path.name)))
        op_id = self._to_pascal_case(op_id_raw)
        
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
        if "Body" in xl.sheet_names:
            self._convert_body(wb, xl, op_id, legacy_path.name)
            self._convert_body_example(wb, xl, op_id, legacy_path.name)
        
        # 3. Response sheets
        if status_codes:
            self._convert_responses(wb, xl, op_id, status_codes, legacy_path.name)
        
        wb.save(output_path)
        
        # Cosmetic Polish
        try:
            wb = load_workbook(output_path)
            for sheet_name in wb.sheetnames:
                self._autofit_columns(wb[sheet_name])
            wb.save(output_path)
        except Exception as e:
            self.log(f"  WARNING: Could not apply cosmetic polish to {filename}: {e}")
        self.log(f"  Saved: {output_path}")
    
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
            schema_name = ""
            param_format = ""
            
            # Resolve data type to schema reference (R2.6: parameters refer to dynamic schemas)
            out_name, dt = self._resolve_data_type(param_type, ep_filename)
            if out_name:
                param_type = "schema"
                schema_name = out_name
            elif param_type.lower() in ["string", "number", "integer", "boolean", "array", "object"]:
                param_type = param_type.lower()
            
            rows.append([
                p["name"], p["description"], p["in"], param_type,
                schema_name, "", param_format, p["mandatory"],
                "", "", "", "", "", ""  # Min, Max, PatternEba, Regex, Allowed, Example (empty in endpoint)
            ])
        
        self._write_rows(ws, rows, start_row=3)
    
    def _convert_body(self, wb, xl_legacy, op_id: str, ep_filename: str):
        """Convert Body sheet - media type row references wrapper schema."""
        ws = wb["Body"]
        
        wrapper_name = f"{op_id}Request"
        if wrapper_name not in self.emitted_wrappers:
            return
            
        # Media Type row with schema reference to wrapper
        # Properties are already defined in the component schema - no need to duplicate inline
        media_row = ["content", "application/json", "", "", "schema", "", wrapper_name, "", "M",
                     "", "", "", "", "", ""]
        self._write_rows(ws, [media_row], start_row=3)
    
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
            
            # Tab Coloring (R1 colors)
            status_int = int(code) if code.isdigit() else 0
            if 200 <= status_int < 300:
                ws.sheet_properties.tabColor = "FFD3ECB9"  # Light Green
            else:
                ws.sheet_properties.tabColor = "FFFF9999"  # Light Red
            
            # Row 1: Response | code | description
            ws.cell(row=1, column=1).value = "Response"
            ws.cell(row=1, column=2).value = code
            ws.cell(row=1, column=3).value = desc
            
            # Row 3+: media type row with schema reference to wrapper
            # PROPERTIES CHECK: If the legacy sheet is empty, do not add any content row.
            children = self._read_legacy_structure(xl, code)
            if children:
                # Media type row with schema reference to wrapper
                # Properties are already defined in the component schema - no need to duplicate inline
                media_row = ["content", "application/json", "", "", "schema", "", wrapper_name, "", "M",
                             "", "", "", "", "", ""]
                self._write_rows(ws, [media_row], start_row=3)

                if str(code) in ("200", "201"):
                    self._add_ok_response_example(
                        ws=ws,
                        xl_legacy=xl,
                        response_code=str(code),
                        response_children=children,
                        ep_filename=filename,
                    )

                if str(code) == "400":
                    self._add_400_response_example(
                        ws=ws,
                        xl_legacy=xl,
                        response_children=children,
                        ep_filename=filename,
                    )
    
    # === Helper Methods ===
    
    def _read_legacy_structure(self, xl, sheet_name: str) -> List[Tuple]:
        """Read legacy Body/Response structure: (name, parent, description, type, mandatory)."""
        df = pd.read_excel(xl, sheet_name=sheet_name, dtype=str, header=None)
        
        # Representative keywords for header detection
        header_keywords = ["name", "element", "type", "parent", "data type", "description", "mandatory"]
        header_row_idx = self._find_header_row(df, header_keywords)
        
        if header_row_idx == -1:
            return []
        
        # Determine actual header names (case-insensitive)
        headers = [str(c).strip().lower() for c in df.iloc[header_row_idx]]
        df = df.iloc[header_row_idx + 1:].reset_index(drop=True)
        
        def find_idx(candidates):
            # Perfect match first
            for i, h in enumerate(headers):
                if any(c.lower() == h for c in candidates):
                    return i
            # Substring match fallback
            for i, h in enumerate(headers):
                if any(c.lower() in h for c in candidates):
                    return i
            return -1

        name_idx = find_idx(["element", "name"])
        parent_idx = find_idx(["parent", "parents"])
        desc_idx = find_idx(["description", "description "])
        type_idx = find_idx(["type", "data type", "dtype"])
        items_idx = find_idx(["items data type", "items type", "array only"])
        mand_idx = find_idx(["mandatory", "required"])
        v_rules_idx = find_idx(["validation rules", "validation rule", "validation"])

        children = []
        for _, row in df.iterrows():
            name = self._clean_value(row.iloc[name_idx]) if name_idx != -1 else ""
            if not name or name.lower() == "nan":
                continue
            
            parent = self._clean_value(row.iloc[parent_idx]) if parent_idx != -1 else ""
            desc = self._clean_value(row.iloc[desc_idx]) if desc_idx != -1 else ""
            dtype = self._clean_value(row.iloc[type_idx]) if type_idx != -1 else "string"
            items_type = self._clean_value(row.iloc[items_idx]) if items_idx != -1 else ""
            mandatory = self._clean_value(row.iloc[mand_idx]) if mand_idx != -1 else ""
            v_rules = self._clean_value(row.iloc[v_rules_idx]) if v_rules_idx != -1 else ""
            
            children.append((name, parent, desc, dtype, mandatory, v_rules, items_type))
        
        return children
    
    def _build_children_rows(self, wrapper_name: str, children: List[Tuple], ep_filename: Optional[str] = None, legato_parent: Optional[str] = None) -> Tuple[List[List], set]:
        """Build child rows with proper parent hierarchy and type resolution.
        If legato_parent is provided, use it as Parent for root items.
        Returns (rows, referenced_data_types set).
        
        When a node resolves to a schema $ref, its children are NOT emitted
        because they already exist in the referenced component schema.
        """
        rows = []
        referenced_data_types = set()
        
        # First pass: determine which nodes resolve to a schema reference.
        # Children of such nodes should be suppressed (they live in the component schema).
        schema_ref_nodes = set()
        
        for name, parent, desc, dtype, mandatory, v_rules, items_type_row in children:
            low_dtype = dtype.lower()
            out_name, dt = self._resolve_data_type(dtype, ep_filename)
            
            # If it resolves to a named schema (not literal 'object' or 'array'), mark it
            if out_name and low_dtype not in ["object", "array"] and dt and dt.type and dt.type.lower() not in ["object", "array"]:
                schema_ref_nodes.add(name.lower())
                referenced_data_types.add(out_name)
        
        # Build parent lookup (case-insensitive)
        parent_map = {}
        for name, parent, desc, dtype, mandatory, v_rules, items_type_row in children:
            if parent:
                parent_map[name.lower()] = parent
        
        # Second pass: build rows, skipping children of schema-ref nodes
        for name, parent, desc, dtype, mandatory, v_rules, items_type_row in children:
            # Skip this row if its parent is a node that resolves to a schema $ref:
            # the children are already defined in the referenced component schema.
            if parent and parent.lower() in schema_ref_nodes:
                continue
            
            # Also skip if any ancestor resolves to a schema ref (deeply nested case)
            skip = False
            ancestor = parent.lower() if parent else None
            while ancestor:
                if ancestor in schema_ref_nodes:
                    skip = True
                    break
                ancestor = parent_map.get(ancestor)
                if ancestor:
                    ancestor = ancestor.lower()
            if skip:
                continue
            
            # Determine actual parent
            if legato_parent:
                actual_parent = parent if parent else legato_parent
            else:
                actual_parent = parent if parent else wrapper_name
            
            # Decorate description with validation rules if present (R3.3)
            final_desc = desc
            if v_rules:
                final_desc = f"{desc}\n\n**ValidationRule(s)** {v_rules}" if desc else f"**ValidationRule(s)** {v_rules}"
            
            # Resolve type with recursive inlining rules
            resolved_type = "string"
            schema_name = ""
            items_type = ""
            
            low_dtype = dtype.lower()
            out_name, dt = self._resolve_data_type(dtype, ep_filename)
            
            # RULE: Only inline if the literal NAME is 'object' or 'array'.
            if low_dtype == "object":
                resolved_type = "object"
                schema_name = ""
            elif low_dtype == "array":
                resolved_type = "array"
                schema_name = ""
                # Resolve items recursively using the definition of 'array'
                it_to_resolve = items_type_row
                if not it_to_resolve and dt:
                    it_to_resolve = dt.items_type
                items_type = self._recursive_resolve_items(it_to_resolve, dt.source_file if dt and dt.source_file != "$global" else None)
            elif dt and dt.type and dt.type.lower() in ["object", "array"]:
                # Inline resolved object/array schemas to preserve legacy structure
                resolved_type = dt.type.lower()
                schema_name = ""
                if resolved_type == "array":
                    it_to_resolve = items_type_row
                    if not it_to_resolve:
                        it_to_resolve = dt.items_type or ""
                    items_type = self._recursive_resolve_items(it_to_resolve, dt.source_file if dt and dt.source_file != "$global" else None)
            elif dt:
                resolved_type = "schema"
                schema_name = out_name
                referenced_data_types.add(out_name)
            else:
                # Fallback to literal primitives for any other case
                if low_dtype in ["string", "number", "integer", "boolean"]:
                    resolved_type = low_dtype
                else:
                    resolved_type = dtype # Pass through unknown
            
            # Convert mandatory
            mand_value = "M" if mandatory in ["M", "m", "Yes", "yes", "Y", "y"] else \
                         "O" if mandatory in ["O", "o", "No", "no", "N", "n"] else mandatory
            
            rows.append([
                name, actual_parent, final_desc, resolved_type,
                items_type, schema_name, "", mand_value,
                "", "", "", "", "", "", "" # Col J-O: Min, Max, PatternEba, Regex, Allowed, Example
            ])
        
        return rows, referenced_data_types

    
    # =========================================================================
    # Body Example Generation
    # =========================================================================

    def _get_example_values(self, dt: Optional['DataType']) -> List[str]:
        """Return list of example values from a DataType (split by ';'), or [] if none."""
        if dt is None:
            return []
        raw = dt.example or ""
        if not raw or raw.lower() == "nan":
            # Fallback: first allowed value
            av = dt.allowed_values or ""
            if av and av.lower() != "nan":
                first = re.split(r'[;,]', av)[0].strip()
                if first:
                    return [first]
            return []
        parts = [p.strip() for p in raw.split(";") if p.strip()]
        return parts if parts else []

    def _generate_synthetic_value(self, dtype_lower: str) -> Any:
        """Return a type-appropriate synthetic fallback value."""
        if dtype_lower in ("integer", "int"):
            return 0
        if dtype_lower in ("number", "float", "double", "decimal"):
            return 0.0
        if dtype_lower == "boolean":
            return True
        return "string"

    def _resolve_leaf_dt(self, dtype: str, ep_filename: Optional[str]) -> Optional['DataType']:
        """Resolve a field type to its DataType, or None for primitives."""
        low = dtype.lower()
        if low in ("string", "number", "integer", "boolean", "array", "object", ""):
            return None
        _, dt = self._resolve_data_type(dtype, ep_filename)
        return dt

    def _build_body_example_dict(
        self,
        children: List[Tuple],
        ep_filename: Optional[str],
        omit_field: Optional[str] = None,
        override_field: Optional[str] = None,
        override_value: Any = None,
        override_fields: Optional[Dict[str, Any]] = None,
        array_item_index: int = 0,
    ) -> dict:
        """
        Build a Python dict representing one body example from the legacy structure.

        children  : list of (name, parent, desc, dtype, mandatory, v_rules, items_type)
        omit_field: if set, skip this field name (for Bad Request missing-mandatory)
        override_field / override_value: replace value for one field (other Bad Request violations)
        array_item_index: 0 = first array item, 1 = second array item (shifts rotation)
        """
        # Per-type rotation counter (shared across the whole call so siblings rotate)
        type_counters: Dict[str, int] = {}

        def get_rotated_value(dtype: str, dt: Optional['DataType'], item_offset: int = 0) -> Any:
            """Pick example value using per-type rotation + item_offset for array diversity."""
            examples = self._get_example_values(dt)
            low = dtype.lower() if dtype else "string"

            if examples:
                count = type_counters.get(low, 0)
                idx = (count + item_offset) % len(examples)
                type_counters[low] = count + 1
                raw = examples[idx]
                # Coerce to numeric if the DataType says so
                if dt:
                    if dt.type.lower() in ("integer", "int"):
                        try:
                            return int(raw)
                        except (ValueError, TypeError):
                            pass
                    elif dt.type.lower() in ("number", "float", "double", "decimal"):
                        try:
                            return float(raw)
                        except (ValueError, TypeError):
                            pass
                    elif dt.type.lower() == "boolean":
                        return raw.lower() in ("true", "yes", "1")
                return raw
            else:
                # Synthetic fallback
                if dt:
                    low_t = dt.type.lower()
                else:
                    low_t = low
                return self._generate_synthetic_value(low_t)

        # Build parent → children tree.
        # IMPORTANT: legacy structures can contain duplicate field names under different parents.
        # Use unique node ids internally to avoid overwriting nodes by name.

        node_parent: Dict[str, str] = {}
        node_name: Dict[str, str] = {}
        node_dtype: Dict[str, str] = {}
        node_mandatory: Dict[str, str] = {}
        node_items: Dict[str, str] = {}
        ordered_uids: List[str] = []

        name_to_last_uid: Dict[str, str] = {}
        for i, (name, parent, desc, dtype, mandatory, v_rules, items_type) in enumerate(children):
            uid = f"{name}__{i}"
            node_name[uid] = name
            node_dtype[uid] = dtype or "string"
            node_mandatory[uid] = mandatory or ""
            node_items[uid] = items_type or ""

            parent_name = parent or ""
            parent_uid = name_to_last_uid.get(parent_name, "") if parent_name else ""
            node_parent[uid] = parent_uid
            ordered_uids.append(uid)

            # Update last seen uid for this name
            name_to_last_uid[name] = uid

        def is_root(uid: str) -> bool:
            return not node_parent.get(uid, "")

        children_of: Dict[str, List[str]] = {}
        for uid in ordered_uids:
            p_uid = node_parent.get(uid, "")
            if p_uid not in children_of:
                children_of[p_uid] = []
            children_of[p_uid].append(uid)

        def build_node(uid: str, item_offset: int = 0) -> Any:
            dtype = node_dtype.get(uid, "string")
            low_dtype = dtype.lower()
            dt = self._resolve_leaf_dt(dtype, ep_filename)
            my_children = children_of.get(uid, [])

            # --- ARRAY ---
            if low_dtype == "array" or (dt and dt.type.lower() == "array"):
                items_type_name = node_items.get(uid, "")
                if not items_type_name and dt:
                    items_type_name = dt.items_type or ""
                items_dt = self._resolve_leaf_dt(items_type_name, ep_filename) if items_type_name else None
                items_low = items_type_name.lower() if items_type_name else "object"

                if my_children:
                    # Array of objects defined inline
                    item1 = {
                        node_name[c]: build_node(c, item_offset=0)
                        for c in my_children
                        if node_name.get(c) != omit_field or override_field is not None
                    }
                    # Check if we have enough examples for a second distinct item
                    can_make_second = _can_diversify(my_children, item_offset=1)
                    if can_make_second:
                        item2 = {
                            node_name[c]: build_node(c, item_offset=1)
                            for c in my_children
                            if node_name.get(c) != omit_field or override_field is not None
                        }
                        return [item1, item2]
                    return [item1]
                elif items_low == "object" or (items_dt and items_dt.type.lower() == "object"):
                    # Array of objects but no inline children — use empty dict
                    return [{}]
                else:
                    # Array of scalars
                    v1 = get_rotated_value(items_type_name or items_low, items_dt, item_offset=0)
                    examples_list = self._get_example_values(items_dt)
                    if len(examples_list) >= 2:
                        v2 = get_rotated_value(items_type_name or items_low, items_dt, item_offset=1)
                        return [v1, v2]
                    return [v1]

            # --- OBJECT ---
            if low_dtype == "object" or (dt and dt.type.lower() == "object" and my_children):
                result = {}
                for c in my_children:
                    cname = node_name.get(c)
                    if cname == omit_field:
                        continue
                    val = build_node(c, item_offset=item_offset)
                    if cname == override_field:
                        val = override_value
                    if override_fields and cname in override_fields:
                        val = override_fields.get(cname)
                    result[cname] = val
                return result

            # --- SCALAR (possibly a named schema that resolves to a scalar type) ---
            val = get_rotated_value(dtype, dt, item_offset=item_offset)
            if node_name.get(uid) == override_field:
                val = override_value
            if override_fields and node_name.get(uid) in override_fields:
                val = override_fields.get(node_name.get(uid))
            return val

        def _can_diversify(child_uids: List[str], item_offset: int) -> bool:
            """Check whether at least one child has >1 example value (enables 2nd array item)."""
            for c in child_uids:
                dtype = node_dtype.get(c, "string")
                dt = self._resolve_leaf_dt(dtype, ep_filename)
                examples = self._get_example_values(dt)
                if len(examples) >= 2:
                    return True
            return False

        # Step 3: build root dict
        result = {}
        for uid in ordered_uids:
            if not is_root(uid):
                continue
            name = node_name.get(uid)
            if name == omit_field:
                continue
            val = build_node(uid, item_offset=array_item_index)
            if name == override_field:
                val = override_value
            if override_fields and name in override_fields:
                val = override_fields.get(name)
            result[name] = val

        return result

    def _pick_bad_request_violation(
        self,
        children: List[Tuple],
        ep_filename: Optional[str],
    ) -> Tuple[str, Optional[str], Any]:
        """
        Scan body children and choose the best Bad Request violation.
        Returns (violation_type, field_name, bad_value).
        violation_type: 'omit' | 'enum' | 'range' | 'regex' | 'type'
        """
        mandatory_fields = []
        enum_fields = []
        range_fields = []
        regex_fields = []
        any_field = None

        for name, parent, desc, dtype, mandatory, v_rules, items_type in children:
            dt = self._resolve_leaf_dt(dtype, ep_filename)
            any_field = (name, dtype, dt)

            mand = mandatory.upper() if mandatory else ""
            if mand == "M":
                mandatory_fields.append(name)

            if dt:
                if dt.allowed_values and dt.allowed_values.lower() != "nan":
                    enum_fields.append((name, dt))
                if (dt.min_val and dt.min_val.lower() != "nan") or \
                   (dt.max_val and dt.max_val.lower() != "nan"):
                    range_fields.append((name, dt))
                if dt.regex and dt.regex.lower() != "nan":
                    regex_fields.append((name, dt))

        # Priority 1: omit mandatory
        if mandatory_fields:
            return ("omit", mandatory_fields[0], None)

        # Priority 2: invalid enum value
        if enum_fields:
            name, dt = enum_fields[0]
            return ("enum", name, "INVALID_VALUE")

        # Priority 3: out-of-range value
        if range_fields:
            name, dt = range_fields[0]
            low_t = dt.type.lower() if dt else "string"
            if dt.max_val and dt.max_val.lower() != "nan":
                try:
                    bad = int(float(dt.max_val)) + 1
                    return ("range", name, bad)
                except (ValueError, TypeError):
                    pass
            if dt.min_val and dt.min_val.lower() != "nan":
                try:
                    bad = int(float(dt.min_val)) - 1
                    return ("range", name, bad)
                except (ValueError, TypeError):
                    pass

        # Priority 4: regex violation
        if regex_fields:
            name, dt = regex_fields[0]
            return ("regex", name, "INVALID")

        # Priority 5: wrong type fallback
        if any_field:
            name, dtype, dt = any_field
            low_t = (dt.type.lower() if dt else dtype.lower()) if dtype else "string"
            if low_t in ("integer", "number", "float", "double", "decimal"):
                return ("type", name, "not_a_number")
            else:
                return ("type", name, 12345)

        return ("type", None, None)

    def _convert_body_example(self, wb, xl_legacy, op_id: str, ep_filename: str):
        """Generate and write the Body Example sheet with OK and Bad Request examples."""
        if "Body Example" not in wb.sheetnames:
            return

        if "Body" not in xl_legacy.sheet_names:
            return

        children = self._read_legacy_structure(xl_legacy, "Body")
        if not children:
            return

        ws = wb["Body Example"]

        # --- Build OK example ---
        ok_dict = self._build_body_example_dict(children, ep_filename)
        ok_yaml = yaml.dump(
            ok_dict,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        ).rstrip()

        # --- Build Bad Request example ---
        violation_type, viol_field, bad_val = self._pick_bad_request_violation(children, ep_filename)

        if violation_type == "omit":
            bad_dict = self._build_body_example_dict(
                children, ep_filename, omit_field=viol_field
            )
        else:
            bad_dict = self._build_body_example_dict(
                children, ep_filename,
                override_field=viol_field,
                override_value=bad_val,
            )

        bad_yaml = yaml.dump(
            bad_dict,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        ).rstrip()

        # --- Write to sheet (col A = name, col B = body YAML) ---
        examples = [
            ("OK", ok_yaml),
            ("Bad Request", bad_yaml),
        ]
        for row_idx, (ex_name, ex_body) in enumerate(examples, start=2):
            cell_name = ws.cell(row=row_idx, column=1, value=ex_name)
            cell_body = ws.cell(row=row_idx, column=2, value=ex_body)
            cell_name.alignment = Alignment(vertical="top")
            cell_body.alignment = Alignment(vertical="top", wrap_text=True)

    def _recursive_resolve_items(self, items_type_name: str, source_context: Optional[str]) -> str:
        """Recursively resolve items_type. If it resolves to object or array, return primitive."""
        if not items_type_name:
            return "object"
            
        low_it = items_type_name.lower()
        if low_it in ["string", "number", "integer", "boolean", "object", "array"]:
            return low_it
            
        it_out, it_dt = self._resolve_data_type(items_type_name, source_context)
        if it_dt:
            if it_dt.type.lower() == "object":
                return "object"
            elif it_dt.type.lower() == "array":
                return "array"
            else:
                return it_out or items_type_name
        return it_out or items_type_name

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
            v_rules = self._clean_value(row.get("Validation Rules", ""))
            
            mand_value = "M" if mandatory in ["M", "m", "Yes", "yes"] else "O"
            
            final_desc = desc
            if v_rules:
                final_desc = f"{desc}\n\n**ValidationRule(s)** {v_rules}" if desc else f"**ValidationRule(s)** {v_rules}"
            
            params.append({
                "name": name,
                "description": final_desc,
                "in": param_in,
                "type": dtype,
                "mandatory": mand_value
            })
        
        return params

    def _pick_first_example_value(self, raw: str) -> str:
        if raw is None:
            return ""
        s = str(raw).strip()
        if not s or s.lower() == "nan":
            return ""
        for sep in [";", "|", ",", "\n"]:
            if sep in s:
                parts = [p.strip() for p in s.split(sep) if p.strip()]
                if parts:
                    return parts[0]
        return s

    def _read_legacy_params_with_examples(self, xl_legacy, sheet_name: str) -> List[Dict[str, str]]:
        if sheet_name not in xl_legacy.sheet_names:
            return []

        try:
            df = pd.read_excel(xl_legacy, sheet_name=sheet_name, dtype=str, header=None)
        except Exception:
            return []

        header_row_idx = self._find_header_row(df, ["element", "name", "type"])
        if header_row_idx == -1:
            return []

        headers = [str(c).strip().lower() for c in df.iloc[header_row_idx].values]
        df = df.iloc[header_row_idx + 1:].reset_index(drop=True)
        df.columns = headers

        def _get_col(row, keys: List[str]) -> str:
            for k in keys:
                if k in df.columns:
                    return self._clean_value(row.get(k))
            # Partial match fallback
            for c in df.columns:
                for k in keys:
                    if k in str(c):
                        return self._clean_value(row.get(c))
            return ""

        out: List[Dict[str, str]] = []
        for _, row in df.iterrows():
            name = _get_col(row, ["element", "request header", "name"])
            if not name or name.lower() in ["nan", "element", "name"]:
                continue

            dtype = _get_col(row, ["type", "data type"])
            example_raw = _get_col(row, ["example"])
            out.append(
                {
                    "name": name,
                    "type": dtype or "string",
                    "example": self._pick_first_example_value(example_raw),
                }
            )
        return out

    def _find_last_used_row(self, ws, max_scan_cols: int = 6) -> int:
        try:
            last = ws.max_row
        except Exception:
            last = 1
        for r in range(last, 0, -1):
            for c in range(1, max_scan_cols + 1):
                try:
                    if ws.cell(row=r, column=c).value not in (None, ""):
                        return r
                except Exception:
                    continue
        return 1

    def _add_ok_response_example(
        self,
        ws,
        xl_legacy,
        response_code: str,
        response_children: List[Tuple],
        ep_filename: str,
    ) -> None:
        try:
            for r in range(1, min(ws.max_row, 200) + 1):
                if str(ws.cell(row=r, column=1).value).strip().lower() == "examples" and \
                   str(ws.cell(row=r, column=2).value).strip() == "OK":
                    return
        except Exception:
            pass

        try:
            ok_dict = self._build_body_example_dict(response_children, ep_filename)
            ok_yaml = yaml.dump(
                ok_dict,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            ).rstrip()
        except Exception:
            ok_yaml = ""

        path_params = self._read_legacy_params_with_examples(xl_legacy, "Path")
        headers = self._read_legacy_params_with_examples(xl_legacy, "Header")

        def _param_example(name: str, raw_ex: str) -> str:
            if name.strip().lower() == "senderbic":
                return f"TSTBICXX{response_code}"
            return raw_ex or ""

        rows: List[List[Any]] = []

        rows.append(["examples", "OK", "application/json", "", "", "", "", "", "", "", "", "", "", "", ""])

        if path_params:
            rows.append(["examples", "x-sandbox-request-path-params", "OK", "", "object", "", "", "", "", "", "", "", "", "", ""])
            for p in path_params:
                pname = p.get("name", "")
                exv = _param_example(pname, p.get("example", ""))
                rows.append(["examples", pname, "x-sandbox-request-path-params", "", "string", "", "", "", "", "", "", "", "", "", exv])

        if headers:
            rows.append(["examples", "x-sandbox-request-headers", "OK", "", "object", "", "", "", "", "", "", "", "", "", ""])
            for h in headers:
                hname = h.get("name", "")
                exv = h.get("example", "")
                rows.append(["examples", hname, "x-sandbox-request-headers", "", "string", "", "", "", "", "", "", "", "", "", exv])

        rows.append(["examples", "value", "OK", "", "object", "", "", "", "", "", "", "", "", "", ok_yaml])

        start_row = self._find_last_used_row(ws) + 1
        self._write_rows(ws, rows, start_row=start_row)

    def _add_400_response_example(
        self,
        ws,
        xl_legacy,
        response_children: List[Tuple],
        ep_filename: str,
    ) -> None:
        try:
            for r in range(1, min(ws.max_row, 200) + 1):
                if str(ws.cell(row=r, column=1).value).strip().lower() == "examples" and \
                   str(ws.cell(row=r, column=2).value).strip().lower() == "bad request":
                    return
        except Exception:
            pass

        try:
            bad_dict = self._build_body_example_dict(
                response_children,
                ep_filename,
                override_fields={
                    "errorCode": "SC01",
                    "errorCodeDescription": "Failed Parameter Validation",
                },
            )
            bad_yaml = yaml.dump(
                bad_dict,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            ).rstrip()
        except Exception:
            bad_yaml = ""

        path_params = self._read_legacy_params_with_examples(xl_legacy, "Path")
        headers = self._read_legacy_params_with_examples(xl_legacy, "Header")

        def _param_example(name: str, raw_ex: str) -> str:
            if name.strip().lower() == "senderbic":
                return "TSTBICXX400"
            return raw_ex or ""

        rows: List[List[Any]] = []
        rows.append(["examples", "Bad Request", "application/json", "", "", "", "", "", "", "", "", "", "", "", ""])

        if path_params:
            rows.append(["examples", "x-sandbox-request-path-params", "Bad Request", "", "object", "", "", "", "", "", "", "", "", "", ""])
            for p in path_params:
                pname = p.get("name", "")
                exv = _param_example(pname, p.get("example", ""))
                rows.append(["examples", pname, "x-sandbox-request-path-params", "", "string", "", "", "", "", "", "", "", "", "", exv])

        if headers:
            rows.append(["examples", "x-sandbox-request-headers", "Bad Request", "", "object", "", "", "", "", "", "", "", "", "", ""])
            for h in headers:
                hname = h.get("name", "")
                exv = h.get("example", "") or ""
                rows.append(["examples", hname, "x-sandbox-request-headers", "", "string", "", "", "", "", "", "", "", "", "", exv])

        rows.append(["examples", "value", "Bad Request", "", "object", "", "", "", "", "", "", "", "", "", bad_yaml])

        start_row = self._find_last_used_row(ws) + 1
        self._write_rows(ws, rows, start_row=start_row)
    
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
                cell = ws.cell(row=r_idx, column=c_idx)
                cell.value = value if value != "" else None
                try:
                    if cell.alignment:
                        cell.alignment = cell.alignment.copy(vertical="top")
                    else:
                        cell.alignment = Alignment(vertical="top")
                except Exception:
                    cell.alignment = Alignment(vertical="top")

    def _autofit_columns(self, ws, max_width: int = 60):
        """Adjust column widths based on content with a maximum limit and forced wrap."""
        try:
            for col in ws.columns:
                max_len = 0
                # Robustly get column letter (col[0] could be a MergedCell)
                first_cell = col[0]
                column_letter = get_column_letter(first_cell.column)
                
                for cell in col:
                    try:
                        if cell.value:
                            # Calculate max line length in the cell
                            lines = str(cell.value).split('\n')
                            for line in lines:
                                max_len = max(max_len, len(line))
                    except:
                        continue
                
                # Padding
                target_width = max_len + 2
                
                if target_width > max_width:
                    ws.column_dimensions[column_letter].width = max_width
                    # Apply wrap only if content is long
                    for cell in col:
                        # MergedCell does not support direct style assignment in some contexts
                        if not hasattr(cell, 'alignment'): continue
                        try:
                            if cell.alignment:
                                cell.alignment = cell.alignment.copy(wrapText=True, vertical="top")
                            else:
                                cell.alignment = Alignment(wrapText=True, vertical="top")
                        except Exception:
                            cell.alignment = Alignment(wrapText=True, vertical="top")
                else:
                    ws.column_dimensions[column_letter].width = max(target_width, 10)
                    # Keep vertical alignment
                    for cell in col:
                        if not hasattr(cell, 'alignment'): continue
                        if not cell.alignment or not cell.alignment.wrapText:
                            try:
                                if cell.alignment:
                                    cell.alignment = cell.alignment.copy(vertical="top")
                                else:
                                    cell.alignment = Alignment(vertical="top")
                            except Exception:
                                cell.alignment = Alignment(vertical="top")
        except Exception as e:
            self.log(f"  Note: Auto-fit skipped for sheet '{ws.title}': {e}")
