import yaml
import re
import json
import textwrap
import copy
import pandas as pd
from datetime import datetime
from collections import OrderedDict

# Import YAML utilities from generator_pkg package
from src.generator_pkg.yaml_output import RawYAML, OASDumper, raw_yaml_presenter
from src.generator_pkg.swift_customizer import apply_swift_customization as _apply_swift_customization
from src.generator_pkg.row_helpers import (
    get_col_value as _get_col_value_fn,
    get_schema_name as _get_schema_name_fn,
    get_type as _get_type_fn,
    get_name as _get_name_fn,
    get_parent as _get_parent_fn,
    get_description as _get_description_fn,
    parse_example_string as _parse_example_string_fn,
)
from src.generator_pkg.schema_builder import (
    handle_combinator_refs as _handle_combinator_refs_fn,
    handle_schema_reference as _handle_schema_reference_fn,
    apply_schema_constraints as _apply_schema_constraints_fn,
    map_type_to_schema as _map_type_to_schema_fn,
)
from src.generator_pkg.response_builder import (
    build_response_tree as _build_response_tree_fn,
    extract_response_description as _extract_response_description_fn,
    flatten_subtree as _flatten_subtree_fn,
    build_schema_from_flat_table as _build_schema_from_flat_table_fn,
    build_examples_from_rows as _build_examples_from_rows_fn,
    process_response_headers as _process_response_headers_fn,
    process_response_content as _process_response_content_fn,
    coerce_example_types as _coerce_example_types_fn,
)


class OASGenerator:
    def __init__(self, version="3.0.0"):
        self.version = version
        self.oas = {
            "openapi": version,
            "info": {},
            "paths": {},
            "components": {
                "parameters": {},
                "headers": {},
                "schemas": {},
                "responses": {},
                "securitySchemes": {},
            },
        }
        self.source_map = {}

    def _record_source(self, json_path, filename, sheet_name=None):
        """Records the source file and sheet for a given OAS path."""
        if filename:
            # key: JSON path, value: dict {file: ..., sheet: ...}
            self.source_map[json_path] = {"file": filename, "sheet": sheet_name}

    def build_info(self, info_data):
        self.oas["info"] = copy.deepcopy(info_data)

    def build_paths(self, paths_list, operations_details):
        for op_meta in paths_list:
            path_url = op_meta.get("path")
            method = op_meta.get("method", "").lower()
            file_ref = op_meta.get("file")

            if not path_url or not method:
                continue

            if path_url not in self.oas["paths"]:
                self.oas["paths"][path_url] = {}

            op_obj = {
                "summary": op_meta.get("summary"),
                "description": op_meta.get("description"),
                "operationId": op_meta.get("operationId"),
                "tags": [op_meta.get("tags")] if op_meta.get("tags") else [],
                "parameters": [],
                "responses": {},
            }

            # Merge Custom Extensions - USE RAW TEXT, don't parse!
            extensions_yaml = op_meta.get("extensions")
            if (
                extensions_yaml
                and isinstance(extensions_yaml, str)
                and extensions_yaml.strip()
            ):
                # Trim common indentation - normalize to column 0
                # This ensures consistent handling regardless of Excel formatting
                trimmed_ext = self._trim_extension_indent(extensions_yaml)
                op_obj["__RAW_EXTENSIONS__"] = trimmed_ext

            # Populate details from Operation File
            details = {}
            if file_ref in operations_details:
                details = operations_details[file_ref]

            # Extract Body Examples Global for this Op
            body_examples = {}
            if details.get("body_examples") is not None:
                body_examples_df = details.get("body_examples")
                # Convert DF to dict {Name: Body}
                # Assuming col 0 is Name, col 1 is Body
                for _, row in body_examples_df.iterrows():
                    ex_name = str(row.iloc[0]).strip()
                    ex_body = row.iloc[1]
                    if pd.notna(ex_body):
                        # Detect if body is typical "request" example?
                        # For now just store by name
                        body_examples[ex_name] = ex_body

            # Parameters
            if details.get("parameters") is not None:
                op_obj["parameters"] = self._build_parameters(details["parameters"])

            # Request Body
            # Skip for GET, DELETE, HEAD
            if details.get("body") is not None and method not in [
                "get",
                "delete",
                "head",
            ]:
                req_body = self._build_request_body(details["body"], body_examples)

                if req_body:
                    op_obj["requestBody"] = req_body

            # Responses
            if details.get("responses"):
                for code, df_resp in details["responses"].items():
                    op_obj["responses"][str(code)] = self._build_single_response(
                        df_resp, body_examples, str(code)
                    )

            # Fallback for empty responses
            if not op_obj["responses"]:
                op_obj["responses"]["default"] = {"description": "Default response"}

            # Reorder Operation Object keys
            # Don't sort extensions - preserve original order from Excel!
            standard_pre = [
                "summary",
                "description",
                "operationId",
                "tags",
                "parameters",
                "requestBody",
            ]
            extensions = [k for k in op_obj.keys() if k.startswith("x-")]
            if "__RAW_EXTENSIONS__" in op_obj:
                extensions.append("__RAW_EXTENSIONS__")
            standard_post = ["responses"]

            final_order = standard_pre + extensions + standard_post

            op_obj = self._reorder_dict(op_obj, final_order)

            op_obj = self._reorder_dict(op_obj, final_order)

            self.oas["paths"][path_url][method] = op_obj
            
            self.oas["paths"][path_url][method] = op_obj
            
            # Record Source Map (Granular)
            # 1. Parameters
            if details.get("parameters") is not None:
                sheet = details["parameters"].attrs.get("sheet_name")
                self._record_source(f"paths.{path_url}.{method}.parameters", file_ref, sheet)
                
            # 2. Request Body
            if details.get("body") is not None:
                 sheet = details["body"].attrs.get("sheet_name")
                 self._record_source(f"paths.{path_url}.{method}.requestBody", file_ref, sheet)
                 
                 # 2.1 Body Examples
                 if details.get("body_examples") is not None:
                     ex_sheet = details["body_examples"].attrs.get("sheet_name")
                     # Assuming application/json for now as per _build_request_body
                     base_ex_path = f"paths.{path_url}.{method}.requestBody.content.application/json.examples"
                     self._record_source(base_ex_path, file_ref, ex_sheet)

            # 3. Responses
            if details.get("responses"):
                for code, df_resp in details["responses"].items():
                     sheet = df_resp.attrs.get("sheet_name")
                     self._record_source(f"paths.{path_url}.{method}.responses.{code}", file_ref, sheet)

            # 4. Root Operation Fallback
            # Link the operation root to the Parameters sheet (most common entry point) 
            # or Body if no params.
            root_sheet = None
            if details.get("parameters") is not None:
                root_sheet = details["parameters"].attrs.get("sheet_name")
            elif details.get("body") is not None:
                root_sheet = details["body"].attrs.get("sheet_name")
            # If no params or body, maybe it's just responses? or just metadata.
            # If root_sheet is None, it will default to just opening the file, which is fine.
            self._record_source(f"paths.{path_url}.{method}", file_ref, root_sheet)

    def _build_parameters(self, df):
        params = []
        if df is None:
            return params

        for _, row in df.iterrows():
            name = self._get_name(row)
            if pd.isna(name):
                continue

            type_val = (
                str(self._get_type(row)).lower().strip()
                if pd.notna(self._get_type(row))
                else ""
            )
            schema_name = self._get_schema_name(row)

            # If Type=parameter/parameters and Schema Name is present, create a reference
            if type_val in ["parameter", "parameters"] and pd.notna(schema_name):
                # Check if there's a description
                desc = self._get_description(row)
                ref_path = f"#/components/parameters/{name}"

                if pd.notna(desc):
                    # Reference with description
                    is_oas30 = self.version.startswith("3.0")
                    if is_oas30:
                        # OAS 3.0 does not support 'allOf' for parameters, nor '$ref' with siblings.
                        # We must resolve the reference inline.

                        # Note: This assumes build_components has run and populated self.oas["components"]["parameters"]
                        # The global parameter name is likely the same as 'name' here, or derived from schema_name
                        # Logic: schema_name in Excel usually maps to the component name

                        global_param = None
                        target_ref_name = name  # Default assumption

                        # Try to find the global parameter
                        if (
                            "components" in self.oas
                            and "parameters" in self.oas["components"]
                        ):
                            if name in self.oas["components"]["parameters"]:
                                global_param = self.oas["components"]["parameters"][
                                    name
                                ]

                        if global_param:
                            import copy

                            param = copy.deepcopy(global_param)
                            param["description"] = str(desc)
                            param["x-comment"] = (
                                f"Reference from '#/components/parameters/{name}' resolved inline to allow description override."
                            )
                        else:
                            # Fallback if not found (should not happen if build order is correct)
                            # Retain old invalid behavior or maybe minimal def?
                            # Using allOf as last resort or error?
                            # Let's stick to the allOf "invalid" approach if we can't find the parent,
                            # but simpler: just a ref without description and a warning?
                            # Or better: Create a minimal parameter with just description and schema ref?
                            # But we don't know 'in' or 'required'.
                            # Let's fallback to the broken allOf but print a warning.
                            print(
                                f"WARNING: Global parameter '{name}' not found for inline resolution. Generating invalid 'allOf' parameter."
                            )
                            param = {
                                "allOf": [{"$ref": ref_path}],
                                "description": str(desc),
                            }
                    else:
                        # OAS 3.1 allows $ref and description at same level
                        param = {"$ref": ref_path, "description": str(desc)}
                else:
                    # Just the reference
                    param = {"$ref": ref_path}

                params.append(param)
                continue

            in_loc = self._get_col_value(row, ["In", "Location"])
            if pd.isna(in_loc):
                # Default to header for 'parameter' type if missing
                if type_val == "parameter":
                    in_loc = "header"
                else:
                    continue

            param = {
                "name": name,
                "in": str(in_loc).lower(),
                "description": self._get_description(row) or "",
                "required": str(
                    self._get_col_value(row, ["Mandatory", "Required"]) or ""
                ).lower()
                in ["yes", "y", "true", "m"],
            }
            # Build schema but remove description and examples (they go at param level)
            schema = self._map_type_to_schema(row)
            schema.pop("description", None)
            # Extract example from schema if present (put at param level instead)
            example = schema.pop("example", None)
            examples = schema.pop("examples", None)
            param["schema"] = schema
            
            # Add example at param level (singular form)
            if example is not None:
                param["example"] = example
            elif examples and len(examples) > 0:
                param["example"] = examples[0]
            
            params.append(param)
        return params

    def _build_request_body(self, df, body_examples=None):

        if df is None or df.empty:
            return None

        # The structure usually has the content-type as a root or row 0
        # Let's find the content type.
        # Check if 'application/json' is in Name column
        content_type = "application/json"  # Default

        # We process the rows to build the schema
        # We need to filter out meta-rows if they exist

        schema = self._build_schema_from_flat_table(df)

        # Unwrap if schema has a single property matching content_type
        # e.g. schema = { properties: { "application/json": { ... } } }
        if schema and "properties" in schema and len(schema["properties"]) == 1:
            root_key = list(schema["properties"].keys())[0]
            if root_key == content_type or root_key == "application/json":
                schema = schema["properties"][root_key]

        return {
            "content": {
                content_type: {
                    "schema": schema,
                    **(
                        {
                            "examples": {
                                k: {"value": self._parse_example_string(v)}
                                for k, v in body_examples.items()
                            }
                        }
                        if body_examples
                        else {}
                    ),
                }
            }
        }

    def _get_col_value(self, row, keys):
        """Delegate to row_helpers.get_col_value."""
        return _get_col_value_fn(row, keys)

    def _get_schema_name(self, row):
        """Delegate to row_helpers.get_schema_name."""
        return _get_schema_name_fn(row)

    def _get_type(self, row):
        """Delegate to row_helpers.get_type."""
        return _get_type_fn(row)

    def _get_name(self, row):
        """Delegate to row_helpers.get_name."""
        return _get_name_fn(row)

    def _get_parent(self, row):
        """Delegate to row_helpers.get_parent."""
        return _get_parent_fn(row)

    def _get_description(self, row):
        """Delegate to row_helpers.get_description."""
        return _get_description_fn(row)

    def _parse_example_string(self, ex_str):
        """Delegate to row_helpers.parse_example_string."""
        return _parse_example_string_fn(ex_str)

    def _build_response_tree(self, df):
        """Delegate to response_builder.build_response_tree."""
        return _build_response_tree_fn(df, self._get_name, self._get_parent, self._get_col_value)

    def _extract_response_description(self, df, root_node):
        """Delegate to response_builder.extract_response_description."""
        return _extract_response_description_fn(df, root_node, self._get_description, self._get_parent)

    def _process_response_headers(self, header_nodes):
        """Delegate to response_builder.process_response_headers."""
        return _process_response_headers_fn(
            header_nodes, self.oas["components"]["headers"], self.version
        )

    def _process_response_content(self, content_nodes, schema_nodes, root_node):
        """Delegate to response_builder.process_response_content."""
        # Pass components schemas for $ref resolution in example type coercion
        components_schemas = self.oas.get("components", {}).get("schemas", {})
        return _process_response_content_fn(
            content_nodes, schema_nodes, root_node, self.version, components_schemas
        )

    def _build_single_response(self, df, body_examples=None, code="", description_override=None):
        """
        Builds a single OAS response object from DataFrame.
        Delegates to helper methods for tree building, headers, and content.
        """
        if df is None or df.empty:
            return {"description": description_override or "Response"}

        # Build tree structure from flat rows
        root_node = self._build_response_tree(df)
        if not root_node:
            return {"description": description_override or "Response"}

        # Extract response description
        if description_override:
            desc = description_override
        else:
            desc = self._extract_response_description(df, root_node)
        resp_obj = {"description": desc}

        # Classify children nodes
        header_nodes = []
        content_nodes = []
        schema_nodes = []

        for child in root_node["children"]:
            row = child["row"]
            section = str(self._get_col_value(row, ["Section"])).strip().lower()
            r_type = str(self._get_type(row)).strip().lower()
            c_name = child["name"]

            # Check for response reference (early return)
            if r_type == "response":
                schema_ref = self._get_schema_name(row)
                if pd.notna(schema_ref):
                    ref_path = f"#/components/responses/{schema_ref}"
                    child_desc = self._get_description(row)
                    
                    # OAS 3.0 does not allow $ref with any siblings - description is in the component
                    # OAS 3.1 allows $ref with siblings like description
                    if pd.notna(child_desc) and child_desc and not self.version.startswith("3.0"):
                        return {"$ref": ref_path, "description": child_desc}
                    else:
                        return {"$ref": ref_path}

            # Classify node
            if section in ["header", "headers"] or r_type == "header":
                header_nodes.append(child)
            elif section == "content":
                content_nodes.append(child)
            elif c_name.startswith("x-"):
                # Extension on Response Object (Direct child of Synthetic Root)
                # Check if this extension has children (like x-sandbox-request-headers)
                if child.get("children"):
                    # Build object from children's Example values
                    ext_obj = {}
                    for ext_child in child["children"]:
                        ext_child_row = ext_child["row"]
                        ext_child_name = ext_child["name"]
                        ext_val = self._get_col_value(ext_child_row, ["Example", "Examples"])
                        if pd.notna(ext_val):
                            ext_obj[ext_child_name] = self._parse_example_string(ext_val)
                    if ext_obj:
                        resp_obj[c_name] = ext_obj
                else:
                    # Simple extension with a single value
                    ex_val = self._get_col_value(row, ["Example", "Examples"])
                    if pd.notna(ex_val):
                        resp_obj[c_name] = self._parse_example_string(ex_val)
            else:
                schema_nodes.append(child)

        # Process headers
        headers = self._process_response_headers(header_nodes)
        if headers:
            resp_obj["headers"] = headers

        # Process content
        content = self._process_response_content(content_nodes, schema_nodes, root_node)
        if content:
            resp_obj["content"] = content

        # Check for standalone response reference (no headers/content)
        if root_node["row"] is not None:
            type_val = str(self._get_type(root_node["row"])).strip().lower()
            schema_ref = self._get_schema_name(root_node["row"])
            if (
                type_val == "response"
                and pd.notna(schema_ref)
                and not header_nodes
                and not content_nodes
                and not schema_nodes
            ):
                return {"$ref": f"#/components/responses/{schema_ref}"}

        return resp_obj

    def _flatten_subtree(self, nodes):
        """Delegate to response_builder.flatten_subtree."""
        return _flatten_subtree_fn(nodes)

    def _build_examples_from_rows(self, df):
        """Delegate to response_builder.build_examples_from_rows."""
        return _build_examples_from_rows_fn(df)

    def _build_schema_from_flat_table(self, df):
        """Delegate to response_builder.build_schema_from_flat_table."""
        return _build_schema_from_flat_table_fn(df, self.version)

    def _handle_combinator_refs(self, type_val, schema_ref, desc=None):
        """Delegate to schema_builder.handle_combinator_refs."""
        return _handle_combinator_refs_fn(type_val, schema_ref, desc)

    def _handle_schema_reference(self, type_val, schema_ref, desc):
        """Delegate to schema_builder.handle_schema_reference."""
        return _handle_schema_reference_fn(type_val, schema_ref, desc, self.version)

    def _apply_schema_constraints(self, schema, row, type_val):
        """Delegate to schema_builder.apply_schema_constraints."""
        _apply_schema_constraints_fn(schema, row, type_val)

    def _map_type_to_schema(self, row, is_node=False):
        """Delegate to schema_builder.map_type_to_schema."""
        return _map_type_to_schema_fn(row, self.version, is_node)

    def build_components(self, global_components, source_file=None):
        """
        Populates self.oas["components"]
        Strictly enforces order: parameters, headers, schemas, responses
        Strictly enforces separation: Headers stay in headers, etc.
        """
        if not global_components:
            return

        # Initialize ordered groups
        # Note: In Python 3.7+, insertion order is preserved.
        # We process in order to ensure the final OAS JSON/YAML respects this order.
        self.oas["components"]["parameters"] = {}
        self.oas["components"]["headers"] = {}
        self.oas["components"]["schemas"] = {}
        self.oas["components"]["responses"] = {}

        # 1. Parameters (Global)
        if global_components.get("parameters") is not None:
            params = self._build_parameters(global_components["parameters"])
            for p in params:
                self.oas["components"]["parameters"][p["name"]] = p

        # 2. Headers (Global)
        if global_components.get("headers") is not None:
            df_head = global_components["headers"]
            for idx, row in df_head.iterrows():
                name = self._get_name(row)
                if pd.notna(name):
                    name = str(name).strip()
                    # Build Schema Inline but remove description and examples (they go at header level)
                    schema = self._map_type_to_schema(row)
                    schema.pop("description", None)
                    schema.pop("examples", None)
                    schema.pop("example", None)

                    header_desc = self._get_description(row)
                    
                    # Get required and example from row
                    mandatory = self._get_col_value(row, ["Mandatory", "Required"])
                    is_required = str(mandatory).lower() in ["yes", "y", "true", "m"] if pd.notna(mandatory) else False
                    example = self._get_col_value(row, ["Example", "Examples"])

                    # Create Header Object with INLINE schema
                    header_obj = {"schema": schema}
                    if header_desc:
                        header_obj["description"] = str(header_desc)
                    if is_required:
                        header_obj["required"] = True
                    if pd.notna(example):
                        header_obj["example"] = self._parse_example_string(example)

                    self.oas["components"]["headers"][name] = header_obj

        # 3. Schemas (Global)
        if global_components.get("schemas") is not None:
            schema_tree = self._build_schema_group(global_components["schemas"])
            self.oas["components"]["schemas"] = schema_tree
            
            # Record Source for Schemas
            if source_file:
                for schema_name in schema_tree.keys():
                    # For schemas, we might have specific sheet info if 'schemas' was a DF with attrs
                    # But here 'schema_tree' is a dict of built schemas.
                    # 'global_components["schemas"]' IS the dataframe!
                    sheet_name = global_components["schemas"].attrs.get("sheet_name")
                    self._record_source(f"components.schemas.{schema_name}", source_file, sheet_name)

        # 4. Responses (Global)
        if global_components.get("responses") is not None:
            df_resp = global_components["responses"]
            df_resp.columns = df_resp.columns.str.strip()

            # Convert to list of dicts for easier processing
            all_rows = df_resp.to_dict("records")

            # Build Tree using Nearest Preceding Parent Logic
            nodes = {}  # idx -> node
            last_seen = {}  # name -> idx
            roots = []

            for idx, row in enumerate(all_rows):
                name = str(self._get_name(row)).strip()
                parent = self._get_parent(row)
                parent_str = str(parent).strip() if pd.notna(parent) else ""

                # Logic for Root criteria (Type='response' or Parent is empty)
                type_val = str(self._get_type(row)).strip().lower()
                is_root = type_val == "response" or parent_str == ""

                node = {"row": row, "children": [], "idx": idx, "name": name}
                nodes[idx] = node

                # Link to Parent
                if is_root:
                    roots.append(node)
                else:
                    if parent_str in last_seen:
                        p_idx = last_seen[parent_str]
                        nodes[p_idx]["children"].append(node)
                    else:
                        # Try regex match for arrays (e.g. errors[0])
                        target_idx = -1
                        m = re.match(r"(.+)\[(\d+)\]$", parent_str)
                        if m:
                            base = m.group(1)
                            if base in last_seen:
                                target_idx = last_seen[base]
                        
                        if target_idx != -1:
                            nodes[target_idx]["children"].append(node)
                        else:
                            roots.append(node)

                # Update last_seen
                if name and name.lower() != "nan":
                    last_seen[name] = idx

            # Process Roots
            for root_node in roots:
                root_row = root_node["row"]
                root_name = root_node["name"]

                # Flatten tree
                # Extract Description from Root Row (first priority)
                root_description = self._get_description(root_row)

                # Flatten tree AND Reparent children to Top Level (Empty Parent)
                # We exclude the root_row itself from the DataFrame, effectively promoting children
                collected_rows = []

                # Iterate immediate children of the root and promote them
                for child in root_node["children"]:
                    c_row = child["row"].copy()
                    if "Parent" in c_row:
                        c_row["Parent"] = ""
                    collected_rows.append(c_row)
                    
                    # Recursively add descendants (preserving their hierarchy relative to the promoted child)
                    def collect_descendants(n):
                        for c in n["children"]:
                            collected_rows.append(c["row"])
                            collect_descendants(c)
                    
                    collect_descendants(child)

                if not root_name or root_name.lower() == "nan":
                    continue

                response_df = pd.DataFrame(collected_rows)
                self.oas["components"]["responses"][str(root_name)] = (
                    self._build_single_response(response_df, description_override=root_description)
                )

        # Rule 10: Check for missing critical schemas and report them
        self._check_and_report_deficiencies()

    def _log_deficiency(self, msg):
        log_file = "generation_deficiencies.log"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [MISSING DATA] {msg}\n")

    def _find_references(self, target_name):
        """
        Scans the OAS structure to find where a specific component is referenced.
        Returns a list of 'Breadcrumbs' strings.
        """
        refs = []
        target_ref_lower = f"#/components/schemas/{target_name}".lower()

        def scan_dict(d, path_prefix=""):
            for k, v in d.items():
                current_path = f"{path_prefix}.{k}" if path_prefix else k
                if isinstance(v, dict):
                    scan_dict(v, current_path)
                elif isinstance(v, list):
                    for idx, item in enumerate(v):
                        if isinstance(item, dict):
                            scan_dict(item, f"{current_path}[{idx}]")
                elif isinstance(v, str):
                    if target_ref_lower in v.lower():
                        refs.append(f"{current_path} (ref: {v})")

        scan_dict(self.oas)
        # Deduplicate
        return list(set(refs))

    def _check_and_report_deficiencies(self):
        """
        Checks if expected standard schemas are present.
        If not, logs them to a report file to be corrected in Excel.
        """
        required_schemas = ["DateTime"]
        schemas = self.oas["components"]["schemas"]

        missing = []
        for req in required_schemas:
            if req not in schemas:
                missing.append(req)

        if missing:
            print(
                f"\n[WARNING] Found {len(missing)} missing schemas. analyzing references..."
            )
            full_msg = "The following schemas are referenced but missing from the source Excel files:\n"

            for m in missing:
                refs = self._find_references(m)
                ref_str = "\n    - ".join(refs[:5])  # Limit to 5 examples
                if len(refs) > 5:
                    ref_str += f"\n    - ... and {len(refs)-5} more"
                if not refs:
                    ref_str = " (No explicit references found in generated output, possibly implicit or lost)"

                full_msg += f"\n  * {m}:\n    - Referenced in: {ref_str}"

            print(full_msg)
            print(f"See generation_deficiencies.log for details.\n")
            self._log_deficiency(full_msg)

    def _build_schema_group(self, df):
        """
        Builds a dictionary of schema components from a single flat sheet containing multiple schemas.
        """
        nodes = {}
        node_map = {}  # Map Name -> Node
        roots = []
        combinator_schemas = {}  # Track processed combinators
        df.columns = df.columns.str.strip()

        # 1. Build nodes & Map
        print(f"DEBUG: Generator processing {len(df)} rows. Logic: Robust Combinator Fix v3")
        for idx, row in df.iterrows():
            name = self._get_name(row)
            if pd.isna(name):
                continue
            name = str(name).strip()

            # Parsing M for mandatory
            mand_raw = (
                str(self._get_col_value(row, ["Mandatory", "Required"]) or "")
                .strip()
                .lower()
            )
            is_mandatory = mand_raw in ["yes", "y", "true", "m"]

            node = {
                "name": name,
                "type": self._get_type(row),
                "description": self._get_description(row),
                "parent": self._get_parent(row),
                "mandatory": is_mandatory,
                "schema_obj": self._map_type_to_schema(row, is_node=True),
            }

            nodes[idx] = node
            node_map[name] = node # Add EVERYTHING to node_map initially

        # Optimization: Build children map (Parent -> [Children Nodes])
        children_map = {}
        for idx, node in nodes.items():
            p = node["parent"]
            if pd.notna(p):
                p = str(p).strip()
                if p not in children_map:
                    children_map[p] = []
                children_map[p].append(node)

        # 2. Process combinators FIRST (before regular linking)
        import re
        for idx, node in nodes.items():
            name = node["name"]
            type_val = str(node["type"]).strip().lower() if pd.notna(node["type"]) else ""
            
            if type_val in ["oneof", "anyof", "allof"]:
                # Check for children matching name[n]
                combinator_key = {"oneof": "oneOf", "anyof": "anyOf", "allof": "allOf"}[type_val]
                
                potential_children = children_map.get(name, [])
                pattern = re.compile(rf'^{re.escape(name)}\[(\d+)\]$')
                indexed_children = []
                
                for child_node in potential_children:
                    match = pattern.match(child_node["name"])
                    if match:
                        alt_index = int(match.group(1))
                        indexed_children.append((alt_index, child_node))
                
                if indexed_children:
                    # Found children -> It IS an inline combinator
                    indexed_children.sort(key=lambda x: x[0])
                    alternatives = []
                    
                    for _, child_node in indexed_children:
                        alt_schema = self._build_inline_alternative(nodes, child_node, children_map, parent_type=type_val)
                        alternatives.append(alt_schema)
                    
                    # BUG FIX Refined: The root node's schema_obj might already be a combinator 
                    # (e.g. Type='allOf', Schema='Core' -> {'allOf': [{'$ref': 'Core'}]})
                    # We must merge it into the new list effectively.
                    root_schema = node.get("schema_obj", {})
                    
                    if combinator_key in root_schema and isinstance(root_schema[combinator_key], list):
                        # Merge existing combinator alternatives (e.g. the inheritance ref)
                        alternatives.extend(root_schema[combinator_key])
                    elif "$ref" in root_schema:
                        # Case where root is a direct Ref (e.g. Type='object', Schema='Core')
                        alternatives.append(root_schema)

                    schema_obj = {combinator_key: alternatives}
                    desc = node["description"]
                    if pd.notna(desc):
                        schema_obj["description"] = str(desc)
                    
                    combinator_schemas[name] = schema_obj
                    # CRITICAL: Update the node's schema_obj so linking uses the combinator structure
                    node["schema_obj"] = schema_obj

        # 3. Regular linking for non-combinator nodes
        for idx, node in nodes.items():
            name = node["name"]
            parent_name = node["parent"]
            type_val = str(node["type"]).strip().lower() if pd.notna(node["type"]) else ""
            
            # Check if child of ANY combinator
            is_combinator_child = False
            for comb_name in combinator_schemas:
                # Optimized check: name starts with comb_name + "["
                if name.startswith(comb_name + "["):
                     # Verify exact pattern (name matches comb_name[digits...])
                     # Note: this handles recursion (e.g. A[0][1]) if A[0] is in combinator_schemas?
                     # Actually, if A[0] is a combinator, it is in combinator_schemas.
                     # So A[0][1] is a child of A[0].
                     # A[0] is a child of A.
                     # We must skip all of them from ROOT/PARENT linking?
                     # Yes, because they are handled by recursion inside _build_inline_alternative.
                     if re.match(rf'^{re.escape(comb_name)}\[\d+\]', name):
                         is_combinator_child = True
                         break
            
            if is_combinator_child:
                continue
            
            if pd.isna(parent_name):
                roots.append(node)
            elif str(parent_name).strip() in node_map:
                parent = node_map[str(parent_name).strip()]
                parent_schema = parent["schema_obj"]

                if parent_schema.get("type") == "array":
                    items_schema = parent_schema.get("items", {})
                    if not isinstance(items_schema, dict):
                        parent_schema["items"] = {}
                        items_schema = parent_schema["items"]

                    if "type" not in items_schema:
                        items_schema["type"] = "object"

                    if items_schema.get("type") == "object":
                        if "properties" not in items_schema:
                            items_schema["properties"] = {}

                        items_schema["properties"][name] = node["schema_obj"]

                        if node["mandatory"]:
                            if "required" not in items_schema:
                                items_schema["required"] = []
                            if name not in items_schema["required"]:
                                items_schema["required"].append(name)

                        parent_schema["items"] = items_schema
                    else:
                        parent_schema["items"] = node["schema_obj"]
                else:
                    if "properties" not in parent_schema:
                        parent_schema["properties"] = {}
                    parent_schema["properties"][name] = node["schema_obj"]

                    if node["mandatory"]:
                        if "required" not in parent_schema:
                            parent_schema["required"] = []
                        if name not in parent_schema["required"]:
                            parent_schema["required"].append(name)

        # 4. Return combined results
        # Note: combinator_schemas are already integrated into roots or parents via node['schema_obj'] update
        return {r["name"]: r["schema_obj"] for r in roots}
    
    def _build_inline_alternative(self, nodes, alt_node, children_map=None, parent_type=None):
        """Build schema for inline combinator alternative recursively (e.g., InsightNotificationSearchFilter[0])"""
        from collections import OrderedDict
        
        alt_name = alt_node["name"]
        schema = alt_node["schema_obj"].copy() if alt_node["schema_obj"] else {}
        
        # Use description as 'title' for combinator alternatives
        desc = alt_node["description"]
        if pd.notna(desc) and desc:
            schema["title"] = str(desc)
        
        # Check for nested combinator (if this alternative is itself a oneOf/...)
        # If it is, node['schema_obj'] might already be the combinator structure?
        # Yes, loop 2 processed ALL nodes.
        # So if alt_node was detected as combinator, schema_obj is ALREADY correct.
        # We just need to handle PROPERTIES (children) if it is NOT a combinator (or if it's mixed?)
        # Usually oneOf alternatives are objects.
        # We need to find children of THIS node (properties).
        
        if not children_map:
            return schema

        children = children_map.get(alt_name, [])
        
        # But wait! If this node IS a combinator, its children are [0], [1]...
        # Loop 2 already handled them into schema_obj['oneOf']...
        # So we don't need to do anything?
        # BUT Loop 2 only handled INLINE COMBINATORS.
        # What if it's an OBJECT with properties?
        # Then Loop 2 did NOT touch it (unless it had oneOf type).
        # So we must manually build properties here for recursion.
        
        # Filter children that are NOT alternatives (e.g. properties)
        # Actually, Importer flattens object properties as children with Parent=Name.
        # So we just iterate children.
        
        if children and schema.get("type") == "object":
            if "properties" not in schema:
                from collections import OrderedDict
                schema["properties"] = OrderedDict()
            required = []
            
            # Sort children? (optional, alphabetical or document order - dict key order usually preserves insertion)
            # Importer output usually has order.
            
            for child_node in children:
                child_name = child_node["name"]
                
                # Recursion: Build child schema
                child_schema = self._build_inline_alternative(nodes, child_node, children_map)
                schema["properties"][child_name] = child_schema
                
                if child_node["mandatory"]:
                    required.append(child_name)
            
            if required:
                schema["required"] = required
            
            # CRITICAL FIX: Enforce exclusivity for oneOf matching ONLY
            # For allOf (inheritance), we MUST allow additional properties (from the parent/other schemas)
            if parent_type == "oneof":
                schema["additionalProperties"] = False
        
        return schema

    def get_yaml(self):
        # Enforce Section Order
        ordered_oas = OrderedDict()
        # 1. OpenAPI Version
        if "openapi" in self.oas:
            ordered_oas["openapi"] = self.oas["openapi"]

        # 2. Info
        if "info" in self.oas:
            ordered_oas["info"] = self.oas["info"]

        # 3. Servers
        if "servers" in self.oas:
            ordered_oas["servers"] = self.oas["servers"]

        # 4. Tags
        if "tags" in self.oas:
            ordered_oas["tags"] = self.oas["tags"]

        # 5. Security (Global) - Reordered: Before Paths
        if "security" in self.oas:
            ordered_oas["security"] = self.oas["security"]

        # 6. Paths
        if "paths" in self.oas:
            ordered_oas["paths"] = self.oas["paths"]

        # 7. Components
        if "components" in self.oas:
            # Clean up empty global component sections
            comps = self.oas["components"]
            # Specific cleanups
            if "securitySchemes" in comps and not comps["securitySchemes"]:
                del comps["securitySchemes"]

            # Reorder Components: securitySchemes FIRST
            ordered_comps = OrderedDict()
            if "securitySchemes" in comps:
                ordered_comps["securitySchemes"] = comps["securitySchemes"]
            for k, v in comps.items():
                if k != "securitySchemes":
                    ordered_comps[k] = v

            ordered_oas["components"] = ordered_comps

        # Add any other missing keys (e.g. externalDocs) at the end
        for k in self.oas:
            if k not in ordered_oas:
                ordered_oas[k] = self.oas[k]

        # FINAL FIX: Recursively enforce 'example'/'examples' at the bottom of every object
        self._recursive_schema_fix(ordered_oas)
        
        # Post-process: Coerce example types based on schema
        # (e.g., convert numeric values to strings when schema expects string)
        self._coerce_all_example_types(ordered_oas)

        # Generate YAML
        yaml_output = yaml.dump(
            ordered_oas,
            Dumper=OASDumper,
            sort_keys=False,
            default_flow_style=False,
            allow_unicode=True,
            width=120,
        )

        # Post-process: Replace __RAW_EXTENSIONS__ markers with actual raw YAML
        yaml_output = self._insert_raw_extensions(yaml_output, ordered_oas)

        return yaml_output

    def get_source_map_json(self):
        """Returns the source map as a JSON string."""
        return json.dumps(self.source_map, indent=2)

    def _recursive_schema_fix(self, obj):
        """
        Recursively traverses the OAS structure and enforces key ordering:
        - 'description' is always first (for human readability)
        - 'example' and 'examples' are always last (for YAML formatting)
        """
        if isinstance(obj, dict):
            # 1. Process children first
            for k, v in obj.items():
                self._recursive_schema_fix(v)

            # 2. Re-order current dict if description or example/examples present
            has_desc = "description" in obj
            has_example = "example" in obj or "examples" in obj
            
            if has_desc or has_example:
                from collections import OrderedDict
                
                # Extract special keys
                desc = obj.pop("description", None)
                ex = obj.pop("example", None)
                exs = obj.pop("examples", None)

                # Reconstruct with correct order: description first
                new_d = OrderedDict()
                if desc is not None:
                    new_d["description"] = desc
                
                # Add remaining keys
                for k, v in obj.items():
                    new_d[k] = v

                # Append example/s at the end
                if ex is not None:
                    new_d["example"] = ex
                if exs is not None:
                    new_d["examples"] = exs

                # Destructive update
                obj.clear()
                obj.update(new_d)

        elif isinstance(obj, list):
            for item in obj:
                self._recursive_schema_fix(item)

    def _coerce_all_example_types(self, oas: dict) -> None:
        """
        Post-process all examples in the OAS to coerce types based on schema.
        
        When schema type is 'string' but example value is numeric, converts to string.
        This is called after the entire OAS is built so all $refs can be resolved.
        
        Args:
            oas: Complete OAS dictionary
        """
        components_schemas = oas.get("components", {}).get("schemas", {})
        paths = oas.get("paths", {})
        
        for path_url, path_item in paths.items():
            for method, operation in path_item.items():
                if not isinstance(operation, dict):
                    continue
                    
                # Process request body examples
                request_body = operation.get("requestBody", {})
                if request_body:
                    self._coerce_content_examples(request_body.get("content", {}), components_schemas)
                
                # Process response examples
                responses = operation.get("responses", {})
                for code, response in responses.items():
                    if isinstance(response, dict) and "content" in response:
                        self._coerce_content_examples(response.get("content", {}), components_schemas)
        
        # Also process component response examples
        component_responses = oas.get("components", {}).get("responses", {})
        for resp_name, response in component_responses.items():
            if isinstance(response, dict) and "content" in response:
                self._coerce_content_examples(response.get("content", {}), components_schemas)

    def _coerce_content_examples(self, content: dict, components_schemas: dict) -> None:
        """
        Coerce example types in a content dictionary based on schema.
        
        Args:
            content: Dict mapping media types to content definitions
            components_schemas: Dict of component schemas for $ref resolution
        """
        for media_type, media_def in content.items():
            if not isinstance(media_def, dict):
                continue
                
            schema = media_def.get("schema", {})
            examples = media_def.get("examples", {})
            
            if examples and schema:
                for example_name, example_def in examples.items():
                    if isinstance(example_def, dict) and "value" in example_def:
                        coerced_value = _coerce_example_types_fn(
                            example_def["value"], 
                            schema, 
                            components_schemas
                        )
                        example_def["value"] = coerced_value

    def _trim_extension_indent(self, text: str) -> str:
        """
        Remove common leading indentation from extension text.
        
        This normalizes the text to start at column 0, regardless of how
        it was formatted in the Excel source. The generator will add the
        correct indentation when inserting into the YAML output.
        
        Args:
            text: Raw extension text, possibly with leading spaces on each line
            
        Returns:
            Text with common indentation removed (normalized to column 0)
        """
        if not text:
            return text
            
        lines = text.split('\n')
        
        # Find minimum indentation (ignoring empty lines)
        min_indent = float('inf')
        for line in lines:
            stripped = line.lstrip()
            if stripped:  # Non-empty line
                indent = len(line) - len(stripped)
                min_indent = min(min_indent, indent)
        
        if min_indent == float('inf'):
            min_indent = 0
        
        # Remove common indentation
        trimmed_lines = []
        for line in lines:
            if line.strip():
                trimmed_lines.append(line[int(min_indent):])
            else:
                trimmed_lines.append('')
        
        return '\n'.join(trimmed_lines).rstrip()

    def _insert_raw_extensions(self, yaml_text: str, oas_dict: dict) -> str:
        """
        Replace __RAW_EXTENSIONS__ markers with raw YAML text.
        
        This uses a simple approach:
        1. Find each __RAW_EXTENSIONS__: marker line in the YAML output
        2. Replace it with the actual extension text, properly indented
        3. Skip any continuation lines that yaml.dump added for the string value
        
        The extension text is already trimmed (normalized to column 0), so we
        just need to add the operation-level indentation (6 spaces).
        """
        if "paths" not in oas_dict:
            return yaml_text

        OPERATION_INDENT = "      "  # 6 spaces for operation-level content
        
        output_lines = yaml_text.split("\n")
        new_output = []
        i = 0
        
        while i < len(output_lines):
            line = output_lines[i]
            
            if "__RAW_EXTENSIONS__:" in line:
                # Found a marker - get the indentation level
                marker_indent = len(line) - len(line.lstrip())
                
                # Find which operation this belongs to by scanning backwards
                raw_text = None
                for path_url, path_item in oas_dict["paths"].items():
                    for method, operation in path_item.items():
                        if isinstance(operation, dict) and "__RAW_EXTENSIONS__" in operation:
                            # Check if we've already processed this one
                            raw_text = operation.get("__RAW_EXTENSIONS__")
                            if raw_text:
                                # Mark as processed by removing from dict
                                del operation["__RAW_EXTENSIONS__"]
                                break
                    if raw_text:
                        break
                
                if raw_text:
                    # Insert the extension text with proper indentation
                    for ext_line in raw_text.split("\n"):
                        if ext_line.strip():
                            new_output.append(OPERATION_INDENT + ext_line)
                        else:
                            new_output.append("")
                
                # Skip the marker line and any continuation (yaml.dump may have
                # serialized the string as multiline |- or quoted)
                i += 1
                while i < len(output_lines):
                    next_line = output_lines[i]
                    if next_line.strip() == "":
                        # Empty line could be part of the value or separator
                        i += 1
                        continue
                    next_indent = len(next_line) - len(next_line.lstrip())
                    if next_indent > marker_indent:
                        # Continuation of the yaml value, skip it
                        i += 1
                    else:
                        # Back to normal content
                        break
            else:
                new_output.append(line)
                i += 1

        return "\n".join(new_output)

    def _reorder_dict(self, d, keys_order):
        """
        Returns a new dictionary with keys in the specified order.
        Keys not in keys_order are appended at the end.
        """
        new_d = OrderedDict()
        # 1. Add known keys in order
        for k in keys_order:
            if k in d:
                new_d[k] = d[k]

        # 2. Add remaining keys
        for k, v in d.items():
            if k not in new_d:
                new_d[k] = v

        return new_d

    def apply_swift_customization(self, source_filename=None):
        """
        Applies SWIFT-specific customizations (Hardcoded as per exception).
        Delegates to extracted swift_customizer module.
        
        :param source_filename: Optional filename of the base OAS file to reference in description.
        """
        _apply_swift_customization(self.oas, source_filename)

