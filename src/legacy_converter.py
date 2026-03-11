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
    
    def __init__(
        self,
        input_dir: str,
        output_dir: str,
        master_dir: str = None,
        log_callback=None,
        include_descriptions_in_collision: bool = False,
        include_examples_in_collision: bool = False,
        capitalize_schema_names: bool = True,
    ):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.master_dir = Path(master_dir) if master_dir else None
        self.log = log_callback or print
        self.tracing_enabled = True # Default

        self.include_descriptions_in_collision = bool(include_descriptions_in_collision)
        self.include_examples_in_collision = bool(include_examples_in_collision)
        self.capitalize_schema_names = bool(capitalize_schema_names)
        
        # Internal registry
        self.global_schemas: Dict[str, DataType] = {} # out_name -> DataType
        self.used_names = set()
        self.fingerprints = {} # fingerprint -> out_name
        self.output_names = {} # (filename, original_name) -> out_name
        
        # Double-pass state
        self.raw_data_types: Dict[str, Dict[str, DataType]] = {} # file_key -> {norm_name -> DataType}
        self.ordered_filenames: List[str] = [] # list of filenames in index order
        self.schema_usage: Dict[str, List[str]] = {} # out_name -> ["opId.Context.prop[.sub...]", ...]
        
        # Operation IDs mapping
        self.filename_to_opid = {}
        self.emitted_wrappers = set()
        self.emitted_inline_components = set()
        self.inline_component_fingerprints: Dict[Tuple, str] = {}
        self.inline_component_fingerprint_by_name: Dict[str, Tuple] = {}
        self.inline_component_root_desc: Dict[str, str] = {}
        self.inline_component_example_sig: Dict[str, str] = {}
        self.merge_provenance: Dict[str, Dict[str, Dict[str, set]]] = {}  # out_name -> {field -> {value_key -> set(file_keys)}}
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
        # Optionally include description/examples depending on preferences.
        excluded = {'name', 'source_file', 'pattern_eba'}
        if not self.include_descriptions_in_collision:
            excluded.add('description')
        if not self.include_examples_in_collision:
            excluded.add('example')
        fp_data = {k: v for k, v in dt.__dict__.items() if k not in excluded}
        
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

            # Record merge provenance for neutral fields (description/examples) when they differ.
            try:
                canon = self.global_schemas.get(out_name)
                if canon:
                    if not self.include_descriptions_in_collision:
                        desc_in = (dt.description or "").strip()
                        desc_can = (canon.description or "").strip()
                        if desc_in and desc_in != desc_can:
                            self._record_merge_provenance(out_name, "description", desc_in, file_key)
                    if not self.include_examples_in_collision:
                        ex_in = (dt.example or "").strip()
                        ex_can = (canon.example or "").strip()
                        if ex_in and ex_in != ex_can:
                            self._record_merge_provenance(out_name, "example", ex_in, file_key)
            except Exception:
                pass
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

    def _record_merge_provenance(self, out_name: str, field: str, value: str, file_key: str) -> None:
        if not out_name or not field or value is None:
            return
        if out_name not in self.merge_provenance:
            self.merge_provenance[out_name] = {}
        if field not in self.merge_provenance[out_name]:
            self.merge_provenance[out_name][field] = {}
        key = str(value)
        if key not in self.merge_provenance[out_name][field]:
            self.merge_provenance[out_name][field][key] = set()
        if file_key:
            self.merge_provenance[out_name][field][key].add(str(file_key))

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

                def _add_usage(schema_name: str, ctx: str, prop_path: str = ""):
                    if not schema_name:
                        return
                    if schema_name not in self.schema_usage:
                        self.schema_usage[schema_name] = []
                    base = f"{op_id}.{ctx}" if op_id else ctx
                    usage_str = base if not prop_path else f"{base}.{prop_path}"
                    if usage_str not in self.schema_usage[schema_name]:
                        self.schema_usage[schema_name].append(usage_str)

                def _resolve_and_add(dtype_name: str, ctx: str, prop_path: str = ""):
                    if not dtype_name:
                        return
                    if str(dtype_name).strip().lower() in ["string", "number", "integer", "boolean", "array", "object"]:
                        return
                    out_name, dt = self._resolve_data_type(dtype_name, ep_filename)
                    if out_name:
                        _add_usage(out_name, ctx, prop_path)
                        # If this is an array DataType, also track its items type as used in the same place
                        if dt and dt.type and dt.type.lower() == "array" and dt.items_type:
                            _resolve_and_add(dt.items_type, ctx, prop_path)
                
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
                                name = self._clean_value(row.get("Name", ""))
                                ctx = "PathParam" if sheet == "Path" else "Header"
                                _resolve_and_add(dtype, ctx, name)
                                            
                # Check Body & Responses
                for sheet in xl.sheet_names:
                    if sheet in ["Body", "200", "201", "400", "401", "403", "404", "500"]:
                        children = self._read_legacy_structure(xl, sheet)

                        ctx = sheet  # Use real sheet name as context (e.g. '200', 'Body')

                        # Build adjacency for property path reconstruction
                        by_parent: Dict[str, List[Tuple]] = {}
                        roots: List[Tuple] = []
                        for t in children:
                            n = self._clean_value(t[0])
                            p = self._clean_value(t[1])
                            if not p:
                                roots.append(t)
                            by_parent.setdefault(p or "", []).append(t)

                        def walk(node: Tuple, prefix: str = ""):
                            name = self._clean_value(node[0])
                            if not name:
                                return
                            dtype = self._clean_value(node[3])
                            items_type_ref = self._clean_value(node[6]) if len(node) > 6 else ""

                            prop_path = f"{prefix}.{name}" if prefix else name
                            _resolve_and_add(dtype, ctx, prop_path)
                            if items_type_ref:
                                _resolve_and_add(items_type_ref, ctx, prop_path)

                            for ch in by_parent.get(name, []):
                                walk(ch, prop_path)

                        for r in roots:
                            walk(r, "")
            except Exception as e:
                self.log(f"Error in naming pass for {ep_filename}: {e}")

    def _track_recursive_usage(self, child_tuple, ep_filename, op_id, sheet):
        """Deprecated: retained for backward compatibility; usage tracking is now done with full property paths."""
        return

    def _log_usage_summary(self):
        """Log the alphabetical list of schemas and where they are used with absolute property values."""
        
        col1_w, col2_w, col3_w, col4_w = 45, 55, 50, 70
        header = f"| {'SCHEMA NAME':<{col1_w}} | {'USED IN':<{col2_w}} | {'DIFFERENCES':<{col3_w}} | {'MERGE':<{col4_w}} |"
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
        # For DataType-based schemas: compare DataType constraint fields.
        # For promoted inline component schemas: compute property-level diffs.
        mismatches_by_group: Dict[str, List[str]] = {}
        # attrs_display: fields shown in DIFFERENCES column (values only, no arrows)
        attrs = ['type', 'format', 'min_val', 'max_val', 'regex', 'allowed_values', 'items_type']
        # attrs_diff: fields compared when detecting group differences (broader - includes description/example)
        attrs_diff = attrs + ['description', 'example']

        def _short_usage(u: str) -> str:
            if not u:
                return ""
            parts = str(u).split(".")
            if len(parts) < 2:
                return str(u)
            op_id = parts[0]
            ctx = parts[1]
            ctx_map = {
                "PathParam": "Path",
                "Header": "Header",
            }
            disp_ctx = ctx_map.get(ctx, ctx)  # '200', 'Body', 'Path', 'Header' etc.
            return f"{op_id} ({disp_ctx})"

        def _inline_fp(name: str):
            return self.inline_component_fingerprint_by_name.get(name)

        def _dt_constraints(dt: Optional[DataType]) -> Dict[str, str]:
            if not dt:
                return {}
            out = {}
            for a in attrs_diff:
                v = getattr(dt, a, "")
                s = "" if v is None else str(v).strip()
                if s.lower() == "nan":
                    s = ""
                out[a] = s
            return out

        def _constraint_delta(old_dt: Optional[DataType], new_dt: Optional[DataType]) -> List[str]:
            """Return list of attr names that differ (used for grouping); values rendered per-schema separately."""
            o = _dt_constraints(old_dt)
            n = _dt_constraints(new_dt)
            differing = []
            for k in attrs_diff:
                if o.get(k, "") != n.get(k, ""):
                    differing.append(k)
            return differing

        def _schema_attr_display(dt: Optional[DataType], differing_attrs: List[str]) -> str:
            """Display only the differing attribute values for a given schema (no arrows)."""
            if not dt:
                return ""
            bits = []
            for k in differing_attrs:
                if k in attrs_diff:
                    val = getattr(dt, k, "")
                    label = k.replace('_', ' ').title()
                    disp = str(val).strip() if val and str(val).strip().lower() not in ("", "nan") else "(empty)"
                    bits.append(f"- {label}: {disp}")
            return "\n".join(bits)

        def _fp_to_propmap(fp: Tuple) -> Dict[str, Dict[str, str]]:
            """Convert inline component fingerprint entries to a property map keyed by fully-qualified path."""
            if not fp:
                return {}

            # fp entry structure (see _fp_inline_subtree):
            # (name, parent, desc_part, ex_part, dtype, items_type, mandatory, rules)
            children_by_parent: Dict[str, List[Tuple]] = {}
            node_by_key: Dict[Tuple[str, str], Tuple] = {}
            for e in fp:
                if not isinstance(e, tuple) or len(e) < 8:
                    continue
                nm, parent = e[0], e[1]
                node_by_key[(nm, parent)] = e
                children_by_parent.setdefault(parent or "", []).append(e)

            # Roots are those whose parent is "" (top-level under promoted root)
            out: Dict[str, Dict[str, str]] = {}

            def walk(entry: Tuple, prefix: str = ""):
                nm, parent, desc_part, ex_part, dtype, items_type, mandatory, rules = entry[:8]
                if not nm:
                    return
                path = f"{prefix}.{nm}" if prefix else nm
                out[path] = {
                    "dtype": dtype or "",
                    "items": items_type or "",
                    "mandatory": mandatory or "",
                    "rules": rules or "",
                }
                for ch in children_by_parent.get(nm, []):
                    walk(ch, path)

            for r in children_by_parent.get("", []):
                walk(r, "")
            return out

        def _promoted_diffs(base_name: str, other_name: str) -> Dict:
            """Return structured diff dict: {added, removed, changed, mandatory, rules}.
            Each entry carries base_val / other_val so the renderer can display per-schema."""
            base_fp = _inline_fp(base_name)
            other_fp = _inline_fp(other_name)
            if not base_fp or not other_fp:
                return {}
            bmap = _fp_to_propmap(base_fp)
            omap = _fp_to_propmap(other_fp)

            bkeys = set(bmap.keys())
            okeys = set(omap.keys())
            added   = sorted(okeys - bkeys)
            removed = sorted(bkeys - okeys)
            common  = sorted(bkeys & okeys)

            result: Dict = {}
            if added:
                result["added"] = added
            if removed:
                result["removed"] = removed

            changed: Dict[str, Dict] = {}
            mandatory: Dict[str, Dict] = {}
            rules: Dict[str, Dict] = {}
            for k in common:
                b = bmap[k]
                o = omap[k]
                b_type  = b.get("dtype", "")
                o_type  = o.get("dtype", "")
                b_items = b.get("items", "")
                o_items = o.get("items", "")
                if (b_type, b_items) != (o_type, o_items):
                    b_dt = self.global_schemas.get(b_type) if b_type in self.global_schemas else None
                    o_dt = self.global_schemas.get(o_type) if o_type in self.global_schemas else None
                    delta_attrs = _constraint_delta(b_dt, o_dt) if (b_dt or o_dt) else []
                    changed[k] = {
                        "base_type":  f"{b_type or '(empty)'}{('[]' if b_items else '')}",
                        "other_type": f"{o_type or '(empty)'}{('[]' if o_items else '')}",
                        "constraint_delta": delta_attrs,
                    }
                b_mand = (b.get("mandatory", "") or "").strip()
                o_mand = (o.get("mandatory", "") or "").strip()
                if b_mand != o_mand:
                    mandatory[k] = {"base_val": b_mand or "(empty)", "other_val": o_mand or "(empty)"}
                b_rules = (b.get("rules", "") or "").strip()
                o_rules = (o.get("rules", "") or "").strip()
                if b_rules != o_rules:
                    rules[k] = {"base_val": b_rules or "(empty)", "other_val": o_rules or "(empty)"}

            if changed:   result["changed"]   = changed
            if mandatory: result["mandatory"] = mandatory
            if rules:     result["rules"]     = rules
            return result

        for root_name, members in final_groups.items():
            if len(members) <= 1:
                continue

            diff_fields = set()
            dts = [self.global_schemas.get(m) for m in members if self.global_schemas.get(m)]
            fps = [(_inline_fp(m), m) for m in members if _inline_fp(m) is not None]

            if dts:
                base = dts[0]
                for other in dts[1:]:
                    for attr in attrs_diff:
                        v_base = getattr(base, attr, "") or ""
                        v_other = getattr(other, attr, "") or ""
                        if str(v_base).strip() != str(v_other).strip():
                            diff_fields.add(attr)

            # Inline fp diffs: run always (not only when dts is absent) to catch
            # mixed groups where base is a DataType but variants are inline-only.
            if fps:
                # Determine the reference name: prefer base without numeric suffix if present.
                base_nm = members[0]
                stem = re.sub(r'(\d+)$', '', base_nm)
                if stem and stem in base_names:
                    base_nm = stem

                # Only variants show diffs vs the base; base itself stays empty.
                for other_nm in members:
                    if other_nm == base_nm:
                        continue
                    # If other_nm has no inline fp but does have a DataType, flag it as
                    # "structure differs" (DataType vs inline promoted).
                    other_fp = _inline_fp(other_nm)
                    base_fp  = _inline_fp(base_nm)
                    if other_fp and not base_fp:
                        if other_nm not in mismatches_by_group:
                            mismatches_by_group[other_nm] = ("inline_fp_diff", base_nm, {"structure": "promoted inline (base is DataType)"})
                    elif base_fp and not other_fp:
                        if other_nm not in mismatches_by_group:
                            mismatches_by_group[other_nm] = ("inline_fp_diff", base_nm, {"structure": "DataType (base is promoted inline)"})
                    elif base_fp and other_fp:
                        promoted_dict = _promoted_diffs(base_nm, other_nm)
                        if promoted_dict:
                            # Store as ("inline_fp_diff", base_nm, promoted_dict) so renderer can access per-schema values
                            mismatches_by_group[other_nm] = ("inline_fp_diff", base_nm, promoted_dict)

            # If group root has no explicit base schema (e.g. only Name1 exists), flag it
            if root_name and re.search(r'(\d+)$', root_name):
                stem = re.sub(r'(\d+)$', '', root_name)
                if stem and stem not in base_names:
                    diff_fields.add("missing base name")

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

        def _label_values(values: List[str], label: str) -> List[Tuple[str, str]]:
            """Return list of (display_label, original_value) with stable numbering."""
            cleaned: List[str] = []
            for v in values:
                s = "" if v is None else str(v).strip()
                if not s:
                    continue
                cleaned.append(s)
            cleaned = sorted(set(cleaned))
            out: List[Tuple[str, str]] = []
            for i, v in enumerate(cleaned, start=1):
                out.append((f"<{label} {i}>", v))
            return out

        def _merge_summary(schema_name: str) -> str:
            prov = self.merge_provenance.get(schema_name)
            if not prov:
                return ""

            # Collect all unique short usages for each file_key
            def short_usages_for_file(file_key: str) -> List[str]:
                op = self.filename_to_opid.get(file_key, self._extract_operation_id(file_key))
                if not op:
                    return []
                prefix = f"{op}."
                raw = [u for u in (self.schema_usage.get(schema_name) or []) if u.startswith(prefix)]
                return sorted(set([_short_usage(u) for u in raw if _short_usage(u)]))

            # Group prov keys by (field_type, path): "description:bic8" -> ("description", "bic8")
            # Also support legacy plain "description"/"example" keys (DataType provenance)
            blocks: List[str] = []
            for field_key in sorted(prov.keys()):
                value_map = prov[field_key]
                # Parse field_key: "description:fieldpath", "example:fieldpath", or plain "description"/"example"
                if ":" in field_key:
                    field_type, prop_path = field_key.split(":", 1)
                else:
                    field_type, prop_path = field_key, ""
                if field_type not in ("description", "example"):
                    continue
                base_label = "Description" if field_type == "description" else "Example"
                pairs = _label_values(list(value_map.keys()), base_label)
                # Only show if multiple distinct values
                if len(pairs) < 2:
                    continue
                for disp_key, original in pairs:
                    file_keys = sorted(value_map.get(original, set()))
                    ep_lines: List[str] = []
                    for fk in file_keys:
                        ep_lines.extend(short_usages_for_file(fk))
                    ep_lines = sorted(set(ep_lines))
                    if not ep_lines:
                        continue
                    # Build header: "fieldpath (Description N):" or just "<Description N>:" for DataTypes
                    header = f"{prop_path} ({disp_key}):" if prop_path else f"{disp_key}:"
                    blocks.append(header)
                    for ep in ep_lines:
                        blocks.append(f"  {ep}")
                    blocks.append("")
            return "\n".join(blocks).rstrip()

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
                    
            relevant_fields = mismatches_by_group.get(out_name) or mismatches_by_group.get(root_for_mismatch, [])

            # If no direct entry found, check if this schema is the BASE of an inline_fp_diff group.
            # In that case, fabricate the tuple with is_base=True so the renderer shows this schema's values.
            if not relevant_fields:
                for _variant, _entry in mismatches_by_group.items():
                    if (isinstance(_entry, tuple) and len(_entry) == 3 and
                            _entry[0] == "inline_fp_diff" and _entry[1] == out_name):
                        relevant_fields = _entry  # same tuple; renderer uses is_base=(out_name==base_nm_ref)
                        break
            
            diff_str = ""
            if relevant_fields:
                dt = self.global_schemas.get(out_name)

                # Check if this is a structured inline fp diff tuple
                is_inline_diff = (isinstance(relevant_fields, tuple) and
                                  len(relevant_fields) == 3 and
                                  relevant_fields[0] == "inline_fp_diff")

                if is_inline_diff:
                    _, base_nm_ref, diff_dict = relevant_fields
                    # Determine if this out_name is the base or the variant
                    is_base = (out_name == base_nm_ref)
                    top_bits: List[str] = []
                    per_prop: Dict[str, List[str]] = {}

                    if "structure" in diff_dict:
                        top_bits.append(diff_dict["structure"])

                    if ("added" in diff_dict) and (not is_base):
                        added_list = diff_dict["added"]
                        top_bits.append("added:")
                        for a in added_list[:10]:
                            top_bits.append(f"- {a}")
                        if len(added_list) > 10:
                            top_bits.append(f"- (+{len(added_list) - 10} more)")

                    if ("removed" in diff_dict) and (not is_base):
                        removed_list = diff_dict["removed"]
                        top_bits.append("removed:")
                        for r in removed_list[:10]:
                            top_bits.append(f"- {r}")
                        if len(removed_list) > 10:
                            top_bits.append(f"- (+{len(removed_list) - 10} more)")

                    if "changed" in diff_dict:
                        for prop, info in list(diff_dict["changed"].items())[:10]:
                            val = info["base_type"] if is_base else info["other_type"]
                            delta = info.get("constraint_delta", [])
                            extra = f" ({', '.join(delta[:4])})" if delta else ""
                            per_prop.setdefault(prop, []).append(f"- Type: {val}{extra}")

                    if "mandatory" in diff_dict:
                        for prop, info in list(diff_dict["mandatory"].items())[:20]:
                            val = info["base_val"] if is_base else info["other_val"]
                            per_prop.setdefault(prop, []).append(f"- Mandatory: {str(val).upper()}")

                    if "rules" in diff_dict:
                        for prop, info in list(diff_dict["rules"].items())[:20]:
                            raw = info["base_val"] if is_base else info["other_val"]
                            short = (raw[:120] + "...") if len(raw) > 120 else raw
                            per_prop.setdefault(prop, []).append(f"- Validation rules: {short}")

                    prop_blocks: List[str] = []
                    for prop in sorted(per_prop.keys()):
                        prop_blocks.append(f"{prop}:")
                        prop_blocks.extend(per_prop[prop])
                        prop_blocks.append("")

                    diff_str = "\n".join([x for x in (top_bits + ([""] if top_bits and prop_blocks else []) + prop_blocks) if x is not None]).rstrip()

                elif dt:
                    # DataType group: show only the values of differing attrs for THIS schema (no arrows).
                    differing_attrs = [f for f in relevant_fields if f in attrs_diff]
                    diff_str = _schema_attr_display(dt, differing_attrs)
                else:
                    diff_str = "; ".join([str(a) for a in relevant_fields])

            merge_str = _merge_summary(out_name)
            
            # WRAP ALL COLUMNS
            name_lines = wrap_text(out_name, col1_w)
            usage_lines = []
            for u in sorted(set([_short_usage(x) for x in usages if _short_usage(x)])):
                usage_lines.extend(wrap_text(u, col2_w))
            diff_lines = wrap_text(diff_str, col3_w)
            merge_lines = wrap_text(merge_str, col4_w)
            
            max_lines = max(len(name_lines), len(usage_lines), len(diff_lines), len(merge_lines), 1)
            for i in range(max_lines):
                n_cell = name_lines[i] if i < len(name_lines) else ""
                u_cell = usage_lines[i] if i < len(usage_lines) else ""
                d_cell = diff_lines[i] if i < len(diff_lines) else ""
                m_cell = merge_lines[i] if i < len(merge_lines) else ""
                self.log(f"| {n_cell:<{col1_w}} | {u_cell:<{col2_w}} | {d_cell:<{col3_w}} | {m_cell:<{col4_w}} |")
            
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

    def _sync_endpoint_schemas_from_index(self, wb) -> None:
        try:
            ws_ep = wb["Schemas"]
        except Exception:
            try:
                ws_ep = wb.create_sheet("Schemas")
            except Exception:
                return

        idx_path = self.output_dir / "$index.xlsx"
        if not idx_path.exists():
            return

        try:
            wb_idx = load_workbook(idx_path)
        except Exception:
            return

        if "Schemas" not in wb_idx.sheetnames:
            return
        ws_idx = wb_idx["Schemas"]

        rows: List[List[Any]] = []
        for r in range(1, ws_idx.max_row + 1):
            row_vals = []
            for c in range(1, ws_idx.max_column + 1):
                row_vals.append(ws_idx.cell(row=r, column=c).value)
            if all(v is None or v == "" for v in row_vals):
                rows.append([None] * ws_idx.max_column)
            else:
                rows.append(row_vals)

        try:
            for r in range(1, ws_ep.max_row + 1):
                for c in range(1, ws_ep.max_column + 1):
                    ws_ep.cell(row=r, column=c).value = None
        except Exception:
            pass

        self._write_rows(ws_ep, rows, start_row=1)
    
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
                    child_rows, refs, extra_blocks = self._build_children_rows(
                        wrapper,
                        children,
                        ep_file.name,
                        usage_ctx=f"{op_id} (Body)",
                        reserved_names=set(referenced_data_types),
                    )
                    final_rows.append([wrapper, "", "", "object", "", "", "", "", "", "", "", "", "", ""])
                    final_rows.extend(child_rows)
                    final_rows.extend(extra_blocks)
                    referenced_data_types.update(refs)
            
            for code in ["200", "201", "400", "401", "403", "404", "500"]:
                if code in xl.sheet_names:
                    children = self._read_legacy_structure(xl, code)
                    if children:
                        wrapper = "ErrorResponse" if int(code) >= 400 else f"{op_id}Response"
                        if wrapper not in self.emitted_wrappers:
                            self.emitted_wrappers.add(wrapper)
                            child_rows, refs, extra_blocks = self._build_children_rows(
                                wrapper,
                                children,
                                ep_file.name,
                                usage_ctx=f"{op_id} ({code})",
                                reserved_names=set(referenced_data_types),
                            )
                            final_rows.append([wrapper, "", "", "object", "", "", "", "", "", "", "", "", "", ""])
                            final_rows.extend(child_rows)
                            final_rows.extend(extra_blocks)
                            referenced_data_types.update(refs)
                        else:
                            _, refs, extra_blocks = self._build_children_rows(
                                wrapper,
                                children,
                                ep_file.name,
                                usage_ctx=f"{op_id} ({code})",
                                reserved_names=set(referenced_data_types),
                            )
                            final_rows.extend(extra_blocks)
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

        try:
            self._sync_endpoint_schemas_from_index(wb)
        except Exception:
            pass
        
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
    
    def _build_children_rows(self, wrapper_name: str, children: List[Tuple], ep_filename: Optional[str] = None, legato_parent: Optional[str] = None, usage_ctx: Optional[str] = None, reserved_names: Optional[set] = None) -> Tuple[List[List], set, List[List]]:
        """Build child rows with proper parent hierarchy and type resolution.
        If legato_parent is provided, use it as Parent for root items.
        Returns (rows, referenced_data_types set, extra_schema_blocks).
        
        When a node resolves to a schema $ref, its children are NOT emitted
        because they already exist in the referenced component schema.
        """
        rows = []
        referenced_data_types = set()
        extra_schema_blocks: List[List] = []

        def _norm(v: Any) -> str:
            if v is None:
                return ""
            s = str(v).strip()
            if not s or s.lower() == "nan":
                return ""
            s = s.lower()
            try:
                s = re.sub(r"\[\s*\]$", "", s)
                s = re.sub(r"\[\d+\]$", "", s)
            except Exception:
                pass
            return s

        children_lower = [(_norm(n), _norm(p)) for (n, p, *_rest) in children]
        has_children = set()
        for n, p_low in children_lower:
            if p_low:
                has_children.add(p_low)

        def _unique_inline_component_name(base_name: str) -> str:
            candidate = base_name
            i = 1
            reserved = reserved_names or set()
            registered_names = set(self.inline_component_fingerprints.values())
            while (candidate in reserved
                   or candidate in self.emitted_wrappers
                   or candidate in self.emitted_inline_components
                   or candidate in registered_names):
                candidate = f"{base_name}{i}"
                i += 1
            return candidate

        def _row_example(dtype_val: Any, items_val: Any) -> str:
            """Return example text from referenced global DataType (or array items DataType)."""
            def _ex_for_type(type_name: str) -> str:
                if not type_name:
                    return ""
                low = str(type_name).strip().lower()
                if low in ["string", "number", "integer", "boolean", "array", "object", "schema"]:
                    return ""
                out_name, dt = self._resolve_data_type(str(type_name).strip(), ep_filename)
                if dt and getattr(dt, "example", None):
                    return str(dt.example).strip()
                return ""

            ex = _ex_for_type(dtype_val)
            if not ex:
                ex = _ex_for_type(items_val)
            return ex

        def _subtree_example_signature(subtree_children: List[Tuple]) -> str:
            parts = []
            for t_name, t_parent, t_desc, t_dtype, t_mand, t_rules, t_items in subtree_children:
                ex = _row_example(t_dtype, t_items)
                if not ex:
                    continue
                parts.append(f"{str(t_name).strip()}={ex}")
            parts = sorted(set(parts))
            return "; ".join(parts)

        def _fp_inline_subtree(subtree_children: List[Tuple], root_low: str) -> Tuple:
            entries = []
            for t_name, t_parent, t_desc, t_dtype, t_mand, t_rules, t_items in subtree_children:
                p_low = _norm(t_parent)
                p_low = "" if p_low == root_low else p_low
                # Always include description for rows whose dtype resolves to a DataType ($ref-typed
                # properties). A different description on such a row produces a structurally different
                # OAS property (allOf/$ref + description override), so it must drive a schema split
                # independently of the include_descriptions_in_collision preference.
                _ref_out, _ref_dt = self._resolve_data_type(str(t_dtype).strip() if t_dtype else "", ep_filename)
                is_ref_typed = _ref_dt is not None
                desc_part = ""
                if self.include_descriptions_in_collision or is_ref_typed:
                    desc_part = str(t_desc).strip() if t_desc is not None else ""
                ex_part = ""
                if self.include_examples_in_collision:
                    ex_part = _row_example(t_dtype, t_items)
                entries.append(
                    (
                        _norm(t_name),
                        p_low,
                        desc_part,
                        ex_part,
                        _norm(t_dtype),
                        _norm(t_items),
                        _norm(t_mand),
                        str(t_rules).strip() if t_rules is not None else "",
                    )
                )
            return tuple(sorted(entries))

        def _track_inline_component_usage(schema_name: str) -> None:
            if not usage_ctx:
                return
            if schema_name not in self.schema_usage:
                self.schema_usage[schema_name] = []
            if usage_ctx not in self.schema_usage[schema_name]:
                self.schema_usage[schema_name].append(usage_ctx)

        def _bfs_descendants(root_name_norm: str, root_parent_norm: str) -> List[Tuple]:
            """Collect descendants of a specific (name, parent) row instance using
            document-order greedy assignment.

            Key constraint: each parent expansion collects at most ONE row per
            distinct child-name.  This prevents the first 'dailyThresholds' block
            from absorbing both 'lacAgenda' subtrees when two parallel blocks share
            the same element names in the same flat children list.
            """
            root_idx = next(
                (i for i, (n, p, *_) in enumerate(children)
                 if _norm(n) == root_name_norm and _norm(p) == root_parent_norm),
                -1,
            )
            if root_idx == -1:
                return []

            result: List[Tuple] = []
            claimed: set = {root_idx}
            queue: list = [(root_idx, root_name_norm)]

            while queue:
                parent_idx, parent_name_norm = queue.pop(0)
                # For each distinct child name, claim only the first unclaimed row
                # with matching parent that appears after parent_idx.
                seen_child_names: set = set()
                for i in range(parent_idx + 1, len(children)):
                    if i in claimed:
                        continue
                    t_name, t_parent = children[i][0], children[i][1]
                    if _norm(t_parent) != parent_name_norm:
                        continue
                    t_name_norm = _norm(t_name)
                    if t_name_norm in seen_child_names:
                        # Skip duplicate child names — they belong to a sibling subtree
                        continue
                    seen_child_names.add(t_name_norm)
                    claimed.add(i)
                    result.append(children[i])
                    queue.append((i, t_name_norm))

            return result

        # Maps keyed by (name_norm, parent_norm) so parallel same-named subtrees each
        # get their own fingerprint, schema name, and emitted block.
        object_key_map: Dict[Tuple[str, str], str] = {}
        object_key_subtrees: Dict[Tuple[str, str], List[Tuple]] = {}
        array_key_map: Dict[Tuple[str, str], str] = {}
        array_key_subtrees: Dict[Tuple[str, str], List[Tuple]] = {}
        # Legacy name-only maps kept for has-children checks in schema_ref_nodes pass.
        object_ref_map: Dict[str, str] = {}
        array_items_ref_map: Dict[str, str] = {}
        for name, parent, desc, dtype, mandatory, v_rules, items_type_row in children:
            if _norm(dtype) != "object":
                continue
            name_norm = _norm(name)
            if name_norm not in has_children:
                continue
            parent_norm = _norm(parent)
            key = (name_norm, parent_norm)

            descendants = _bfs_descendants(name_norm, parent_norm)

            if descendants:
                object_key_subtrees[key] = descendants
                ex_sig = _subtree_example_signature(descendants)
                fp = _fp_inline_subtree(descendants, name_norm)
                if fp in self.inline_component_fingerprints:
                    existing = self.inline_component_fingerprints[fp]
                    object_ref_map[name_norm] = existing
                    object_key_map[key] = existing
                    # If descriptions are neutral, record merge provenance when root descriptions differ across endpoints
                    if not self.include_descriptions_in_collision:
                        root_desc = (str(desc).strip() if desc is not None else "")
                        canon_desc = (self.inline_component_root_desc.get(existing) or "").strip()
                        if root_desc and root_desc != canon_desc:
                            self._record_merge_provenance(existing, f"description:{name_norm}", root_desc, ep_filename or "")
                    if not self.include_examples_in_collision:
                        canon_ex = (self.inline_component_example_sig.get(existing) or "").strip()
                        if ex_sig and ex_sig != canon_ex:
                            self._record_merge_provenance(existing, f"example:{name_norm}", ex_sig, ep_filename or "")
                else:
                    comp_name = _unique_inline_component_name(self._to_pascal_case(name))
                    object_ref_map[name_norm] = comp_name
                    object_key_map[key] = comp_name
                    self.inline_component_fingerprints[fp] = comp_name
                    self.inline_component_fingerprint_by_name[comp_name] = fp
                    self.inline_component_root_desc[comp_name] = (str(desc).strip() if desc is not None else "")
                    self.inline_component_example_sig[comp_name] = ex_sig
            else:
                comp_name = _unique_inline_component_name(self._to_pascal_case(name))
                object_ref_map[name_norm] = comp_name
                object_key_map[key] = comp_name

            _track_inline_component_usage(object_key_map[key])

        for name, parent, desc, dtype, mandatory, v_rules, items_type_row in children:
            low_dtype = _norm(dtype)
            out_name, dt = self._resolve_data_type(str(dtype).strip() if dtype is not None else "", ep_filename)
            is_array = low_dtype == "array" or (dt and dt.type and dt.type.lower() == "array")
            if not is_array:
                continue
            name_norm = _norm(name)
            if name_norm not in has_children:
                continue
            parent_norm = _norm(parent)
            key = (name_norm, parent_norm)

            descendants = _bfs_descendants(name_norm, parent_norm)

            if descendants:
                array_key_subtrees[key] = descendants
                ex_sig = _subtree_example_signature(descendants)
                fp = _fp_inline_subtree(descendants, name_norm)
                if fp in self.inline_component_fingerprints:
                    existing = self.inline_component_fingerprints[fp]
                    array_items_ref_map[name_norm] = existing
                    array_key_map[key] = existing
                    if not self.include_descriptions_in_collision:
                        root_desc = (str(desc).strip() if desc is not None else "")
                        canon_desc = (self.inline_component_root_desc.get(existing) or "").strip()
                        if root_desc and root_desc != canon_desc:
                            self._record_merge_provenance(existing, "description", root_desc, ep_filename or "")
                    if not self.include_examples_in_collision:
                        canon_ex = (self.inline_component_example_sig.get(existing) or "").strip()
                        if ex_sig and ex_sig != canon_ex:
                            self._record_merge_provenance(existing, "example", ex_sig, ep_filename or "")
                else:
                    comp_name = _unique_inline_component_name(self._to_pascal_case(name))
                    array_items_ref_map[name_norm] = comp_name
                    array_key_map[key] = comp_name
                    self.inline_component_fingerprints[fp] = comp_name
                    self.inline_component_fingerprint_by_name[comp_name] = fp
                    self.inline_component_root_desc[comp_name] = (str(desc).strip() if desc is not None else "")
                    self.inline_component_example_sig[comp_name] = ex_sig
            else:
                comp_name = _unique_inline_component_name(self._to_pascal_case(name))
                array_items_ref_map[name_norm] = comp_name
                array_key_map[key] = comp_name

            _track_inline_component_usage(array_key_map[key])
        
        # First pass: determine which nodes resolve to a schema reference.
        # Children of such nodes should be suppressed (they live in the component schema).
        schema_ref_nodes = set()
        
        for name, parent, desc, dtype, mandatory, v_rules, items_type_row in children:
            name_norm = _norm(name)
            if name_norm in object_ref_map:
                schema_ref_nodes.add(name_norm)
                continue
            if name_norm in array_items_ref_map:
                schema_ref_nodes.add(name_norm)
                continue
            low_dtype = _norm(dtype)
            out_name, dt = self._resolve_data_type(str(dtype).strip() if dtype is not None else "", ep_filename)
            
            # If it resolves to a named schema (not literal 'object' or 'array'), mark it
            if out_name and low_dtype not in ["object", "array"] and dt and dt.type and dt.type.lower() not in ["object", "array"]:
                schema_ref_nodes.add(name_norm)
                referenced_data_types.add(out_name)
        
        # Build parent lookup (case-insensitive)
        parent_map = {}
        for name, parent, desc, dtype, mandatory, v_rules, items_type_row in children:
            if parent:
                parent_map[_norm(name)] = _norm(parent)
        
        # Second pass: build rows, skipping children of schema-ref nodes
        for name, parent, desc, dtype, mandatory, v_rules, items_type_row in children:
            # Skip this row if its parent is a node that resolves to a schema $ref:
            # the children are already defined in the referenced component schema.
            parent_norm = _norm(parent)
            if parent_norm and parent_norm in schema_ref_nodes:
                continue
            
            # Also skip if any ancestor resolves to a schema ref (deeply nested case)
            skip = False
            ancestor = parent_norm if parent_norm else None
            while ancestor:
                if ancestor in schema_ref_nodes:
                    skip = True
                    break
                ancestor = parent_map.get(ancestor)
            if skip:
                continue
            
            # Determine actual parent
            if legato_parent:
                actual_parent = str(parent).strip() if parent else legato_parent
            else:
                actual_parent = str(parent).strip() if parent else wrapper_name
            
            # Decorate description with validation rules if present (R3.3)
            final_desc = desc
            if v_rules:
                final_desc = f"{desc}\n\n**ValidationRule(s)** {v_rules}" if desc else f"**ValidationRule(s)** {v_rules}"
            
            # Resolve type with recursive inlining rules
            resolved_type = "string"
            schema_name = ""
            items_type = ""
            
            name_out = str(name).strip() if name is not None else ""
            low_dtype = _norm(dtype)
            out_name, dt = self._resolve_data_type(str(dtype).strip() if dtype is not None else "", ep_filename)
            
            # RULE: Only inline if the literal NAME is 'object' or 'array'.
            name_norm = _norm(name)
            parent_norm_emit = _norm(parent)
            key_emit = (name_norm, parent_norm_emit)
            if low_dtype == "object" and key_emit in object_key_map:
                resolved_type = "schema"
                schema_name = object_key_map[key_emit]
            elif low_dtype == "object" and name_norm in object_ref_map:
                resolved_type = "schema"
                schema_name = object_ref_map[name_norm]
            elif low_dtype == "object":
                resolved_type = "object"
                schema_name = ""
            elif low_dtype == "array":
                resolved_type = "array"
                schema_name = ""
                if key_emit in array_key_map:
                    items_type = array_key_map[key_emit]
                elif name_norm in array_items_ref_map:
                    items_type = array_items_ref_map[name_norm]
                else:
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
                    if key_emit in array_key_map:
                        items_type = array_key_map[key_emit]
                    elif name_norm in array_items_ref_map:
                        items_type = array_items_ref_map[name_norm]
                    else:
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
                name_out, actual_parent, final_desc, resolved_type,
                items_type, schema_name, "", mand_value,
                "", "", "", "", "", "", "" # Col J-O: Min, Max, PatternEba, Regex, Allowed, Example
            ])

        for (prop_low, prop_parent_low), comp_name in object_key_map.items():
            subtree = object_key_subtrees.get((prop_low, prop_parent_low))
            if not subtree:
                continue
            if comp_name in self.emitted_inline_components:
                continue
            self.emitted_inline_components.add(comp_name)

            transformed: List[Tuple] = []
            for t_name, t_parent, t_desc, t_dtype, t_mand, t_rules, t_items in subtree:
                new_parent = "" if _norm(t_parent) == prop_low else t_parent
                transformed.append((t_name, new_parent, t_desc, t_dtype, t_mand, t_rules, t_items))

            child_rows, _refs, nested_blocks = self._build_children_rows(comp_name, transformed, ep_filename)
            extra_schema_blocks.append([comp_name, "", "", "object", "", "", "", "", "", "", "", "", "", ""])
            extra_schema_blocks.extend(child_rows)
            extra_schema_blocks.extend(nested_blocks)

        for (prop_low, prop_parent_low), comp_name in array_key_map.items():
            subtree = array_key_subtrees.get((prop_low, prop_parent_low))
            if not subtree:
                continue
            if comp_name in self.emitted_inline_components:
                continue
            self.emitted_inline_components.add(comp_name)

            transformed: List[Tuple] = []
            for t_name, t_parent, t_desc, t_dtype, t_mand, t_rules, t_items in subtree:
                new_parent = "" if _norm(t_parent) == prop_low else t_parent
                transformed.append((t_name, new_parent, t_desc, t_dtype, t_mand, t_rules, t_items))

            child_rows, _refs, nested_blocks = self._build_children_rows(comp_name, transformed, ep_filename)
            extra_schema_blocks.append([comp_name, "", "", "object", "", "", "", "", "", "", "", "", "", ""])
            extra_schema_blocks.extend(child_rows)
            extra_schema_blocks.extend(nested_blocks)
        
        return rows, referenced_data_types, extra_schema_blocks

    
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
        
        if not self.capitalize_schema_names:
            return name
        
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
