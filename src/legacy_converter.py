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
        
        # Knowledge Base
        self.local_file_definitions = {} # filename -> {concept_name -> (parent, attrs_tuple, attrs)}
        self.concept_counters = {}       # base_name -> count (for variant naming)
        
        # Selection & Naming
        self.used_global_schemas = set() # {(base_name, attrs_tuple)}
        self.schema_collision_map = {}   # base_name -> {attrs_tuple -> stable_name}
        self.global_schemas_data = {}    # stable_name -> attrs
        self.global_schemas = OrderedDict()
        
        # Hoisting
        self.global_structures = []      # [[parent, name, attrs], ...]
        self.global_registry = OrderedDict() # concept_name -> {fingerprint -> stable_name}
        self.error_schema_map = {}       # (filename, code) -> ErrorResponse variant name
        
        self.used_properties = set()     # {(schema_name, prop_name)}
        
        self.all_tags = set()


    def _log(self, msg):
        if self.log_callback:
            self.log_callback(msg)

    def _normalize_name(self, name):
        if not name or not isinstance(name, str): return ""
        name = name.strip()
        if not name: return ""
        
        # Rule: Req/Resp variants are usually camelCase in our generation
        if name.endswith("Request") or name.endswith("Response"):
            return name[0].lower() + name[1:] if len(name) > 0 else name
            
        # Global definitions and Data Types MUST be PascalCase for parity
        # (e.g., searchCriteria -> SearchCriteria, BIC11 -> BIC11)
        if len(name) > 0:
            return name[0].upper() + name[1:]
        return name

    def _resolve_schema_name(self, name, source_file=None):
        """Resolves a local name to its global finalized stable name."""
        norm_key = self._normalize_name(name) # This will be PascalCase for global types
        if not name or name.lower() in ["object", "array", "string", "number", "integer", "boolean"]:
            return name
        
        if source_file and source_file in self.local_file_definitions:
            if norm_key in self.local_file_definitions[source_file]:
                _, attrs_tuple, _ = self.local_file_definitions[source_file][norm_key]
                return self.schema_collision_map.get(norm_key, {}).get(attrs_tuple, norm_key)
        
        return norm_key

    def _preload_master_schemas(self):
        """Loads the Schemas sheet from Templates Master to preserve hierarchy."""
        master_index = os.path.join(self.master_dir, "$index.xlsx")
        if not os.path.exists(master_index):
            self._log(f"Warning: Master Index not found at {master_index}. Hierarchy may be lost.")
            return

        self._log(f"Preloading Global Schemas from Master: {master_index}")
        try:
            xl = pd.ExcelFile(master_index)
            if "Schemas" not in xl.sheet_names: return
            
            df = pd.read_excel(xl, sheet_name="Schemas", dtype=str)
            # Detect columns (Standard Master Layout)
            # Naive mapping: 0=Name, 1=Parent, 3=Type, 4=Items, 5=SchemaName
            
            # Robust mapping
            cols = list(df.columns)
            name_idx = next((i for i, c in enumerate(cols) if "name" in str(c).lower() and "schema" not in str(c).lower()), 0)
            parent_idx = next((i for i, c in enumerate(cols) if "parent" in str(c).lower()), 1)
            type_idx = next((i for i, c in enumerate(cols) if "type" in str(c).lower() and "items" not in str(c).lower()), 3)
            
            master_defs = {}
            structs = []
            
            # First pass: Build local map for __MASTER__
            for idx, row in df.iterrows():
                name = str(row.iloc[name_idx]).strip()
                if not name or name.lower() in ["nan", "name", "empty"]: continue
                
                parent = str(row.iloc[parent_idx]).strip()
                if parent.lower() in ["nan", "empty"]: parent = ""
                
                orig_type = str(row.iloc[type_idx]).strip()
                
                # Capture all attributes for reconstruction
                attrs = {
                    "type": orig_type,
                    "description": str(row.get("Description", "")).strip(),
                    "format": str(row.get("Format", "")).strip(),
                    "items_type": str(row.get("Items Data Type \n(Array only)", "")).strip(),
                    "min": str(row.get("Min  \nValue/Length/Item", "")).strip(),
                    "max": str(row.get("Max  \nValue/Length/Item", "")).strip(),
                    "pattern": str(row.get("PatternEba", "")).strip(),
                    "allowed_values": str(row.get("Allowed value", "")).strip(),
                    "example": str(row.get("Example", "")).strip()
                }
                
                norm_name = self._normalize_name(name)
                
                # We store it in local_file_definitions as properly formatted
                # Filter None values from attrs for tuple key
                cmp_attrs = attrs.copy()
                if "description" in cmp_attrs: del cmp_attrs["description"]
                if "example" in cmp_attrs: del cmp_attrs["example"]
                # Clean up empty strings
                cmp_attrs = {k: v for k, v in cmp_attrs.items() if v and v.lower() != "nan"}
                
                attrs_tuple = tuple(sorted(cmp_attrs.items()))
                master_defs[norm_name] = (parent, name, attrs_tuple, attrs)
                
                # Also pre-populate global_structures for hierarchy awareness
                # NOTE: We must store normalized names for parents to match tracing
                norm_p = self._normalize_name(parent) if parent else None
                
                # Correction: global_structures expects [parent, name, attrs]
                # If we add it here, it will be written out.
                # However, we only want to write it IF it is used.
                # But since this is the Master Source, we might want to assume it's good?
                # No, strict usage tracing is better. But we need to make it AVAILABLE for usage tracing.
                
                pass # Only loading into definitions for now.
                
            self.local_file_definitions["__MASTER__"] = master_defs
            self._log(f"  Loaded {len(master_defs)} global schemas from Master.")
            
        except Exception as e:
            self._log(f"  Error loading Master Schemas: {e}")

    def _promote_unused_master_schemas(self):
        """Ensures all schemas from Master are in the output, even if supposedly unused."""
        if "__MASTER__" not in self.local_file_definitions: return
        
        master_defs = self.local_file_definitions["__MASTER__"]
        self._log(f"Promoting all {len(master_defs)} Master Schemas to Output...")
        
        for name, def_tuple in master_defs.items():
            parent, lit_name, attrs_tuple, attrs = def_tuple
            # Check if likely already processed via collisions
            # Using norm_name (name) as key
            
            # Note: name is PascalCase here because _preload_master_schemas normalizes it.
            if name not in self.global_schemas_data:
                # Add it directly
                # We need to register it in collision map too technically, but global_schemas is source of truth for index
                self.global_schemas_data[name] = attrs
                
                # Also ensure its structure is known if it has children
                # We need to verify if global_structures has its children.
                # Since we didn't trace it, we need to populate global_structures from Master Defs
                # Iterate Master Defs to find children of this parent
                pass

        # Second pass to populate structures for these promoted schemas
        # This is expensive but necessary for hierarchy
        for child_name, child_def in master_defs.items():
            c_p, c_n, c_a_t, c_a = child_def
            if c_p:
                norm_p = self._normalize_name(c_p)
                # If parent is in global_schemas (it should be now), ensure link exists
                if norm_p in self.global_schemas_data:
                    # Check if already in global_structures
                    # structure entry: [parent_stable, child_literal, child_attrs]
                    # We use c_n (literal name)
                    # We use norm_p (stable parent name)
                    
                    found = False
                    for gs in self.global_structures:
                        if gs[0] == norm_p and gs[1] == c_n:
                            found = True
                            break
                    
                    if not found:
                        self.global_structures.append([norm_p, c_n, c_a])

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

    def convert(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        legacy_index = os.path.join(self.legacy_dir, "$index.xlsm")
        if not os.path.exists(legacy_index):
            self._log(f"Error: $index.xlsm not found in {self.legacy_dir}")
            return False

        # Phase 0: Preload Master Schemas (The Source of Truth for Global Hierarchy)
        self._preload_master_schemas()
        
        # Phase 1: Knowledge Collection (Ordered)
        # Scan all files for Data Type sheets and store local definitions
        self._collect_all_local_definitions(legacy_index)
        
        # Phase 1.5: Force Promotion of Master Schemas (Zero Missing Policy)
        self._promote_unused_master_schemas()
        
        # Phase 2: Usage Tracing & Stable Naming
        # Trace from endpoint sheets to mark schemas as used (transitively)
        self._trace_all_usages(legacy_index)
        
        # Phase 3: Finalize Naming (Stable Sequence)
        self._finalize_naming()

        # Phase 4: Conversion Emission
        self._convert_index(legacy_index)
        self._convert_all_operations()

        return True

    def _collect_all_local_definitions(self, legacy_index_path):
        """Scans all operation files and the index to collect every available Data Type definition."""
        self._log("Collecting all local definitions...")
        
        # 1. Collect from Index (if any Data Type sheet exists there)
        try:
            xl_idx = pd.ExcelFile(legacy_index_path)
            if "Data Type" in xl_idx.sheet_names:
                self.local_file_definitions["$index.xlsm"] = self._load_local_data_types(xl_idx)
        except: pass

        # 2. Collect from all operation files listed in Paths sheet
        try:
            xl_idx = pd.ExcelFile(legacy_index_path)
            paths_df = pd.read_excel(xl_idx, sheet_name="Paths", dtype=str)
            files = paths_df[paths_df.columns[0]].dropna().unique()
            for filename in files:
                filename = str(filename).strip()
                if not filename.endswith(".xlsm"): filename += ".xlsm"
                file_path = os.path.join(self.legacy_dir, filename)
                if os.path.exists(file_path):
                    try:
                        xl = pd.ExcelFile(file_path)
                        self.local_file_definitions[filename] = self._load_local_data_types(xl)
                    except Exception as e:
                        self._log(f"  Error reading {filename}: {e}")
        except Exception as e:
            self._log(f"Error reading Paths from index: {e}")

    def _trace_all_usages(self, legacy_index_path):
        """Follows the usage order set by the index to name schemas stably."""
        self._log("Tracing all usages for stable naming...")
        try:
            xl_idx = pd.ExcelFile(legacy_index_path)
            paths_df = pd.read_excel(xl_idx, sheet_name="Paths", dtype=str)
            # Find column positions
            file_col = paths_df.columns[0]
            id_col = next((c for c in paths_df.columns if "operation" in c.lower()), paths_df.columns[7])
            
            for _, row in paths_df.iterrows():
                filename = str(row[file_col]).strip()
                if not filename.endswith(".xlsm"): filename += ".xlsm"
                op_id = str(row[id_col]).strip()
                
                file_path = os.path.join(self.legacy_dir, filename)
                if os.path.exists(file_path):
                    self._trace_file_usage(file_path, op_id)
        except Exception as e:
            self._log(f"Error tracing usages: {e}")

    def _trace_file_usage(self, file_path, op_id):
        """Analyze an operation file to see which schemas it actually uses."""
        filename = os.path.basename(file_path)
        try:
            xl = pd.ExcelFile(file_path)
            # 1. Body
            if "Body" in xl.sheet_names:
                self._harvest_from_sheet(xl, "Body", filename, op_id, is_error=False)
            
            # 2. Parameters (Header and Path)
            if "Header" in xl.sheet_names:
                self._harvest_from_sheet(xl, "Header", filename, op_id, is_error=False, force_param=True)
            if "Path" in xl.sheet_names:
                self._harvest_from_sheet(xl, "Path", filename, op_id, is_error=False, force_param=True)

            # 3. Responses (2xx and Errors)
            status_codes = [s for s in xl.sheet_names if s.isdigit() and int(s) >= 200]
            for code in status_codes:
                self._harvest_from_sheet(xl, code, filename, op_id, is_error=(int(code) >= 400))
        except: pass

    def _harvest_from_sheet(self, xl, code, filename, op_id, is_error=False, force_param=False):
        """Scans a Body/Response/Param sheet to register used schemas and hoisted structures."""
        try:
            df = pd.read_excel(xl, sheet_name=code, dtype=str)
            
            # Hoisting Naming
            if is_error: concept_name = "ErrorResponse"
            elif force_param: concept_name = "parameters"
            else: concept_name = f"{op_id}Request" if code == "Body" else f"{op_id}Response"
            # Hoisted names MUST be camelCase, but keep suffixes from op_id
            if concept_name != "parameters":
                concept_name = concept_name[0].lower() + concept_name[1:]
            
            # Collect all fields - Dynamic Column Detection
            # Name: "Element", "Name", "Request", etc. (usually Col 0 or 2)
            # Type: "Type", "Data Type", etc.
            # Parent: "Parent", "Parents"
            
            header_row_idx = -1
            for idx, row in df.head(5).iterrows():
                row_str = row.astype(str).str.lower()
                if "type" in row_str.values:
                    header_row_idx = idx
                    break
            
            if header_row_idx == -1: return

            cols = list(df.iloc[header_row_idx].astype(str).str.strip())
            type_idx = next((i for i, c in enumerate(cols) if "type" in c.lower()), 0)
            name_idx = next((i for i, c in enumerate(cols) if any(x in c.lower() for x in ["element", "name", "request"])), 2)
            parent_idx = next((i for i, c in enumerate(cols) if "parent" in c.lower()), -1)

            struct_fields = []
            inline_schemas = {}
            
            data_df = df.iloc[header_row_idx+1:]
            for _, row in data_df.iterrows():
                name = str(row.iloc[name_idx]).strip()
                if not name or name.lower() in ["nan", "element", "section", "type"]: continue
                
                p = str(row.iloc[parent_idx]).strip() if parent_idx != -1 else ""
                orig_t = str(row.iloc[type_idx]).strip()
                
                norm_name = name # Preserve Literal Casing for elements
                norm_p = p if p and p.lower() != "nan" else "" # Preserve Literal Casing for parents in structural sheets
                norm_t = self._normalize_name(orig_t) # Global types are PascalCase
                struct_fields.append((norm_name, norm_p, norm_t, orig_t))
                
                # Mark as used property for hoisting
                p_for_usage = norm_p if norm_p else concept_name
                self.used_properties.add((p_for_usage, norm_name))

                if orig_t.lower() in ["object", "array"]:
                    if norm_name.lower() == "searchcriteria":
                         self._log(f"DEBUG: Found inline SearchCriteria in {filename}. Type: {orig_t}")
                    # REFINEMENT: If this is an inline-defined structure, 
                    # we must ensure its name follows the PascalCase rule for global schemas
                    # unless it's a Request/Response model (handled by _normalize_name)
                    norm_inline = self._normalize_name(norm_name)
                    # FIX DUPLICATES: Key by PascalCase name to merge with existing Global Schemas
                    inline_schemas[norm_inline] = {"type": orig_t.lower(), "parent": norm_p}
                    # MOVED: self._mark_as_used(norm_inline, filename) to after extraction
                
                self._mark_as_used(orig_t, filename)

            # Register Inline Schemas
            # CRITICAL FIX: We must extract the structure of inline objects to allow collision detection
            # 1. Identify all parents
            parents_map = {}
            for f_n, f_p, f_t, o_t in struct_fields:
                if f_p:
                    # Normalize parent name to what it would be as an Object Name (PascalCase)
                    # BUT here f_p is the literal name found in the file (e.g. searchCriteria)
                    # We need to map it to the Global Name (SearchCriteria)
                    stable_p = self._normalize_name(f_p)
                    if stable_p not in parents_map: parents_map[stable_p] = {}
                    
                    # Create child attrs
                    child_attrs = {"type": f_t.lower()} if f_t.lower() not in ["object", "array"] else {"type": "object"}
                    # Basic attributes - we could extract more if we had them (e.g. format)
                    parents_map[stable_p][f_n] = child_attrs
            
            for s_name, s_info in inline_schemas.items():
                # s_name is PascalCase (SearchCriteria)
                
                # If we have extracted structure for this inline object, register it LOCALLY
                if s_name in parents_map:
                     props = parents_map[s_name]
                     # Construct full attrs
                     # 3. Create frozen attrs_tuple for fingerprinting (MUST BE HASHABLE)
                     # props is {name: {attrs}}
                     # We need ((name, ((attr_k, attr_v), ...)), ...)
                     frozen_props = []
                     for prop_name, prop_attrs in sorted(props.items()):
                         frozen_attrs = tuple(sorted(prop_attrs.items()))
                         frozen_props.append((prop_name, frozen_attrs))
                     attrs_tuple = tuple(frozen_props)
                     
                     local_attrs = {
                         "type": s_info["type"],
                         "description": s_name,
                         "properties": props
                     }
                     
                     # Register in local_file_definitions to enable collision detection!
                     if filename not in self.local_file_definitions:
                         self.local_file_definitions[filename] = {}
                     
                     # We store it for later resolution
                     self.local_file_definitions[filename][s_name] = (s_info["parent"], s_name, attrs_tuple, local_attrs)

                # TRIGGER COLLISION CHECK
                self._mark_as_used(s_name, filename)

                # Fallback: Populate global if missing (original logic)
                if s_name not in self.global_schemas_data:
                    self.global_schemas_data[s_name] = {
                        "type": s_info["type"], "description": s_name, "format": "",
                        "items_type": "" if s_info["type"] == "object" else "object",
                        "min": "", "max": "", "pattern": "", "allowed_values": "", "example": ""
                    }
                    if s_name not in self.global_schemas: # Ensure sync
                         self.global_schemas[s_name] = self.global_schemas_data[s_name]

            # Hoist structure
            if is_error:
                fp = tuple(sorted([(n, p, t) for n, p, t, _ in struct_fields]))
                if concept_name not in self.global_registry: self.global_registry[concept_name] = OrderedDict()
                if fp not in self.global_registry[concept_name]:
                    suffix = ""
                    count = len(self.global_registry[concept_name])
                    if count > 0: suffix = str(count)
                    fn = f"{concept_name}{suffix}"
                    self.global_registry[concept_name][fp] = fn
                    self.global_structures.append([None, fn, {"type": "object", "description": ""}])
                    for f_n, f_p, f_t, o_t in struct_fields:
                        p_f = f_p if f_p else fn
                        is_ref = f_t in self.local_file_definitions.get(filename, {}) or f_t in inline_schemas
                        f_t_res = self._resolve_schema_name(f_t, source_file=filename)
                        self.global_structures.append([p_f, f_n, {
                            "type": "schema" if is_ref else (o_t.lower() if o_t.lower() in ["string", "number", "integer", "boolean", "object", "array"] else "string"),
                            "schema_name": f_t_res if is_ref else ""
                        }])
                self.error_schema_map[(filename, code)] = self.global_registry[concept_name][fp]
            else:
                self.global_structures.append([None, concept_name, {"type": "object", "description": ""}])
                for f_n, f_p, f_t, o_t in struct_fields:
                    p_f = f_p if f_p and f_p.lower() != "nan" else concept_name
                    is_ref = f_t in self.local_file_definitions.get(filename, {}) or f_t in inline_schemas
                    f_t_res = self._resolve_schema_name(f_t, source_file=filename)
                    self.global_structures.append([p_f, f_n, {
                        "type": "schema" if is_ref else (o_t.lower() if o_t.lower() in ["string", "number", "integer", "boolean", "object", "array"] else "string"),
                        "schema_name": f_t_res if is_ref else ""
                    }])
        except: pass

    def _mark_as_used(self, orig_type, filename):
        if not orig_type or orig_type.lower() in ["nan", "string", "number", "integer", "boolean", "object", "array"]:
            return
        
        norm_type = self._normalize_name(orig_type)
        
        local_defs = self.local_file_definitions.get(filename, {})
        
        # FALLBACK TO MASTER: If not found locally, check Master
        if norm_type not in local_defs and "__MASTER__" in self.local_file_definitions:
            local_defs = self.local_file_definitions["__MASTER__"]
            filename = "__MASTER__" # Switch context to Master for this trace
        
        try:
            if norm_type in local_defs:
                p_val, literal_name, attrs_tuple, attrs = local_defs[norm_type]
                if (norm_type, attrs_tuple) not in self.used_global_schemas:
                    self.used_global_schemas.add((norm_type, attrs_tuple))
                    if attrs_tuple not in self.schema_collision_map.get(norm_type, {}):
                        count = self.concept_counters.get(norm_type, 0)
                        fn = norm_type if count == 0 else f"{norm_type}{count}"
                        self.schema_collision_map.setdefault(norm_type, {})[attrs_tuple] = fn
                        self.global_schemas_data[fn] = attrs
                        self.concept_counters[norm_type] = count + 1

                        # CRITICAL FIX for Index Generation:
                        # Ensure the properties of this new variant are added to global_structures
                        # AND marked as used, so they are not filtered out by _convert_index
                        if "properties" in attrs:
                            for prop_name, prop_attrs in attrs["properties"].items():
                                self.global_structures.append([fn, prop_name, prop_attrs])
                                self.used_properties.add((fn, prop_name))
                                self._log(f"DEBUG: Added ({fn}, {prop_name}) to used_properties")
                    
                    # Get the stable name for this instance
                    stable_name = self.schema_collision_map[norm_type][attrs_tuple]
                    
                    # Transitive 1: Items
                    it = attrs.get("items_type")
                    if it: self._mark_as_used(it, filename)
                    
                    # Transitive 2: Deep Nesting (all definitions that have this as parent)
                    # Parent in local_defs is the literal name from Excel (literal_name)
                    for child_norm, (parent_literal, child_literal, _, _) in local_defs.items():
                        if parent_literal == literal_name: # literal_name is the original name from Excel
                            # Record that child_literal is a used property of stable_name
                            self.used_properties.add((stable_name, child_literal))
                            
                            # MASTER FALLBACK SPECIFIC:
                            if filename == "__MASTER__":
                                _, _, _, c_attrs = local_defs[child_norm]
                                self.global_structures.append([stable_name, child_literal, c_attrs])

                            # RECURSION FIX
                            child_type = local_defs[child_norm][3].get("type")
                            if child_type:
                                self._mark_as_used(child_type, filename)
        except Exception as e:
            self._log(f"CRITICAL ERROR in _mark_as_used for {norm_type} in {filename}: {e}")
            import traceback
            self._log(traceback.format_exc())



    def _finalize_naming(self):
        self.global_schemas = self.global_schemas_data
        sc_keys = [k for k in self.global_schemas.keys() if "SearchCriteria" in k]
        self._log(f"  Final SearchCriteria keys: {sc_keys}")
        self._log(f"  Final Schemas resolved: {len(self.global_schemas)}")

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
        # Grouping: Root schemas sorted alphabetically, children immediately after their parent.
        if "Schemas" in wb.sheetnames:
            ws_schemas = wb["Schemas"]
            
            # 0. Deduplicate global_structures to avoid multiple identical parent-child rows
            seen_structs = set()
            dedup_structures = []
            for p, n, a in self.global_structures:
                a_type = a.get("type", "")
                a_schema = a.get("schema_name", "")
                # Ignore description for deduplication to prevent near-duplicates blowing up the sheet
                key = (p, n, a_type, a_schema)
                if key not in seen_structs:
                    seen_structs.add(key)
                    dedup_structures.append([p, n, a])
            self.global_structures = dedup_structures

            processed_structures = []
            seen_fields = set()
            
            # Step 1: Dedup and Filter root structures
            for parent, name, attrs in self.global_structures:
                # Filter: If it's a child, only keep if it was actually used in any template
                if parent:
                    if (parent, name) not in self.used_properties:
                        continue
                
                field_key = (parent, name, attrs.get("type"), attrs.get("schema_name"))
                if field_key not in seen_fields:
                    processed_structures.append([parent, name, attrs])
                    seen_fields.add(field_key)
            
            # SORT processed_structures to ensure consistent grouping and alphabetic order of properties
            processed_structures.sort(key=lambda x: (str(x[0] or "").lower(), str(x[1] or "").lower()))

            # Step 2: Grouping (Blocks per Parent)
            # Step 2: Grouping (Blocks per Parent)
            # Normalize all names to ensure consistency
            def normalize_schema_key(n):
                if not n or n == "nan": return ""
                return str(n).strip()

            parent_to_children = {}
            for p, n, a in processed_structures:
                if p:
                    p_norm = normalize_schema_key(p)
                    if p_norm:
                        if p_norm not in parent_to_children:
                            parent_to_children[p_norm] = []
                        parent_to_children[p_norm].append((n, a))

            # Collect ALL potential root names and normalize them
            all_root_names_raw = set(self.global_schemas.keys())
            for p, n, a in processed_structures:
                if p: all_root_names_raw.add(normalize_schema_key(p))
                else: all_root_names_raw.add(normalize_schema_key(n))
            
            # Filter empty and sort
            sorted_roots = sorted([r for r in all_root_names_raw if r], key=lambda x: x.lower())
            
            final_data = []
            seen_roots = set()
            for name in sorted_roots:
                # Avoid redundant blocks if normalization merged them
                if name.lower() in seen_roots: continue
                seen_roots.add(name.lower())
                
                # 1. Root row for this block
                block_root_attrs = {}
                if name in self.global_schemas:
                    block_root_attrs = self.global_schemas[name]
                else:
                    # Fallback lookup in processed_structures to find the definition record
                    for p, n, a in processed_structures:
                        if normalize_schema_key(n) == name:
                            block_root_attrs = a
                            break
                
                root_row = [
                    name, "", block_root_attrs.get("description", name if name in self.global_schemas else ""), 
                    block_root_attrs.get("type", "object"),
                    block_root_attrs.get("items_type", ""),
                    "", # Schema Name
                    block_root_attrs.get("format", ""),
                    "", # Mandatory
                    "", "", "", "", "", "" # Rest of columns
                ]
                final_data.append(root_row)
                
                # 2. Add direct children if any (using normalized key)
                if name in parent_to_children:
                    children = parent_to_children[name]
                    # Sort children alphabetically for perfect grouping
                    children.sort(key=lambda x: str(x[0]).lower())
                    for c_n, c_a in children:
                        child_row = [
                            c_n, name, c_a.get("description", ""), c_a.get("type", "string"),
                            "", # items_type
                            c_a.get("schema_name", ""),
                            "", # format
                            "", "", "", "", "", "", ""
                        ]
                        final_data.append(child_row)
                
                # 3. Add separator
                final_data.append([None] * 14)

            # Clear existing data first (if any headers exist, keep them)
            # (Note: _write_rows overwrites cells, but doesn't delete trailing rows)
            # For brevity in this script, we assume _write_rows is sufficient as we use fresh master
            self._write_rows(ws_schemas, final_data, start_row=2)

        
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
            concept_name = f"{filename.replace('.xlsx', '')}Request"
            concept_name = concept_name[0].lower() + concept_name[1:]
            
            # Simple Hoisted Row for Body
            body_rows = [
                ["Request Body", "Body Description", "M"], # Metadata
                ["Section", "Name", "Parent", "Description", "Type", "Items Data Type \n(Array only)", "Schema Name\n(for Type or Items Data Type = 'schema'||'header')", "Format", "Mandatory", "Min  \nValue/Length/Item", "Max  \nValue/Length/Item", "PatternEba", "Regex", "Allowed value", "Example"],
                ["body", concept_name, "", "", "schema", "", concept_name, "", "Yes", "", "", "", "", "", ""]
            ]
            self._write_rows(wb["Body"], body_rows[2:], start_row=3)
        
        # 3. Body Example
        if df_body is not None and "Body Example" in wb.sheetnames:
            body_ex_rows = self._generate_body_examples(df_body, local_data_types)
            self._write_rows(wb["Body Example"], body_ex_rows[1:], start_row=2)
        
        # 4. Responses
        for code in status_codes:
            if code in wb.sheetnames:
                if int(code) < 400:
                    concept_name = f"{filename.replace('.xlsx', '')}Response"
                    concept_name = concept_name[0].lower() + concept_name[1:]
                else:
                    concept_name = self.error_schema_map.get((filename.replace(".xlsx", ".xlsm"), code), "ErrorResponse")

                # Simple Hoisted Row for Response
                resp_rows = [
                    ["Response", code, "Description"],
                    ["Section", "Name", "Parent", "Description", "Type", "Items Data Type \n(Array only)", "Schema Name\n(for Type or Items Data Type = 'schema'||'header')", "Format", "Mandatory", "Min  \nValue/Length/Item", "Max  \nValue/Length/Item", "PatternEba", "Regex", "Allowed value", "Example"],
                    ["content", concept_name, "", "", "schema", "", concept_name, "", "Yes", "", "", "", "", "", ""]
                ]
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
            # Find header row
            header_row_idx = -1
            for idx, row in df_dt.head(10).iterrows():
                row_str = row.astype(str).str.lower()
                if "data type" in row_str.values or "type" in row_str.values or "name" in row_str.values:
                    header_row_idx = idx
                    break
            
            if header_row_idx != -1:
                df_dt.columns = [str(c).strip() for c in df_dt.iloc[header_row_idx]]
                df_dt = df_dt.iloc[header_row_idx+1:].reset_index(drop=True)
            
            cols = list(df_dt.columns)
            name_col = next((c for i, c in enumerate(cols) if any(x in c.lower() for x in ["data type", "name"])), cols[0])
            parent_col = next((c for c in cols if "parent" in c.lower()), None)
            
            for _, row in df_dt.iterrows():
                name = str(row.get(name_col)).strip()
                if not name or name.lower() in ["nan", "data type", "name"]: continue
                
                # Fingerprint for collision detection (ignore non-functional fields)
                attrs = {
                    "type": str(row.get("Type", "string")).strip(),
                    "format": str(row.get("Format", "")).strip(),
                    "items_type": str(row.get("Items Data Type \n(Array only)", "")).strip(),
                    "min": str(row.get("Min  \nValue/Length/Item", "")).strip(),
                    "max": str(row.get("Max  \nValue/Length/Item", "")).strip(),
                    "pattern": str(row.get("PatternEba", "")).strip() or str(row.get("Regex", "")).strip(),
                    "allowed_values": str(row.get("Allowed value", "")).strip(),
                    "example": str(row.get("Example", "")).strip(),
                    "description": str(row.get("Description", name)).strip()
                }
                
                cmp_attrs = attrs.copy()
                if "description" in cmp_attrs: del cmp_attrs["description"]
                if "example" in cmp_attrs: del cmp_attrs["example"]
                attrs_tuple = tuple(sorted(cmp_attrs.items()))
                
                p = str(row.get(parent_col, "")).strip() if parent_col else ""
                
                local_map[self._normalize_name(name)] = (p, name, attrs_tuple, attrs)
        return local_map



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
