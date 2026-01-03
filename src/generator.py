import yaml
import re
import json
import textwrap
import copy
import pandas as pd
from datetime import datetime
from collections import OrderedDict


# RawYAML - stores raw YAML text for literal insertion
class RawYAML:
    def __init__(self, raw_text, base_indent=0):
        self.raw_text = raw_text
        self.base_indent = base_indent


# Custom YAML Dumper
class OASDumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(OASDumper, self).increase_indent(flow, False)

    def represent_scalar(self, tag, value, style=None):
        if hasattr(value, "replace"):
            # Normalize artifacts
            if "_x000D_" in value:
                value = value.replace("_x000D_", "")
            if "\r" in value:
                value = value.replace("\r", "")
            if "\t" in value:
                value = value.replace("\t", "    ")

            # Strip trailing spaces from each line to ensure valid block style
            if "\n" in value:
                lines = value.split("\n")
                value = "\n".join([line.rstrip() for line in lines])
                style = "|"

        return super(OASDumper, self).represent_scalar(tag, value, style)


def raw_yaml_presenter(dumper, data):
    # Output raw YAML text as-is
    # Split by lines and output each
    lines = data.raw_text.strip().split("\n")
    # Return as a literal scalar block
    return dumper.represent_scalar("tag:yaml.org,2002:str", data.raw_text, style="|")


OASDumper.add_representer(RawYAML, raw_yaml_presenter)

# Preserve OrderedDict order in output
OASDumper.add_representer(
    OrderedDict,
    lambda dumper, data: dumper.represent_mapping(
        "tag:yaml.org,2002:map", data.items()
    ),
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
                # Store raw text - use rstrip to remove trailing spaces only, preserve leading indent
                op_obj["__RAW_EXTENSIONS__"] = extensions_yaml.rstrip()

            # Populate details from Operation File
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

            self.oas["paths"][path_url][method] = op_obj

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
                "schema": self._map_type_to_schema(row),
            }
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
        """
        Helper to get value from row checking multiple column headers.
        """
        if isinstance(keys, str):
            keys = [keys]
        for k in keys:
            if k in row:  # direct check
                val = row[k]
                if pd.notna(val):
                    return val
        return None

    def _get_schema_name(self, row):
        return self._get_col_value(
            row,
            [
                "Schema Name",
                "Schema Name\n(for Type or Items Data Type = 'schema')",
                "Schema Name\n(for Type or Items Data Type = 'schema'||'header')",
                "Schema Name\n(for Type or Items Data Type = 'schema' || 'header')",
                "Schema Name\n(if Type = schema)",
            ],
        )

    def _get_type(self, row):
        return self._get_col_value(row, ["Type", "Data Type", "Item Type", "Type "])

    def _get_name(self, row):
        return self._get_col_value(
            row,
            [
                "Name",
                "Parameter Name",
                "Field Name",
                "Request Parameters",
                "Path",
                "Name.1",
            ],
        )

    def _get_parent(self, row):
        return self._get_col_value(row, ["Parent", "Parent Name"])

    def _get_description(self, row):
        return self._get_col_value(row, ["Description", "Desc", "Description "])

    def _parse_example_string(self, ex_str):
        """
        Parses a string as JSON or YAML.
        """
        if not ex_str:
            return None

        ex_str = str(ex_str).strip()

        # 1. Try JSON if it looks like JSON
        if ex_str.startswith("{") or ex_str.startswith("["):
            try:
                return json.loads(ex_str)
            except (json.JSONDecodeError, TypeError, ValueError):
                # Try fixing single quotes
                try:
                    fixed = ex_str.replace("'", '"')
                    fixed = (
                        fixed.replace("None", "null")
                        .replace("False", "false")
                        .replace("True", "true")
                    )
                    return json.loads(fixed)
                except (json.JSONDecodeError, TypeError, ValueError):
                    pass  # Fallback to YAML

        # 2. Try YAML (Safe Load)
        try:
            return yaml.safe_load(ex_str)
        except (yaml.YAMLError, ValueError, TypeError):
            # 3. If YAML failed, it might be because of outer braces wrapping block-style YAML?
            # e.g. "{ \n key: val \n }" -> Invalid flow style but valid block if stripped.
            if ex_str.startswith("{") and ex_str.endswith("}"):
                # Remove braces but preserve internal relative indentation
                inner = ex_str[1:-1]
                # Normalize tabs to spaces first
                inner = inner.expandtabs(2)
                # Use textwrap.dedent to normalize indentation
                inner = textwrap.dedent(inner)
                try:
                    return yaml.safe_load(inner)
                except Exception as e:
                    # print(f"DEBUG: Inner YAML parse failed: {e}")
                    # If parsing fails, return the stripped content as a string
                    # This produces a Literal Block (|) in YAML instead of a JSON-like string ("{...}")
                    return inner

            return ex_str

    def _build_response_tree(self, df):
        """
        Builds a tree structure from flat DataFrame rows using synthetic root.
        Returns root_node dict with 'children' list.
        """
        df.columns = df.columns.str.strip()
        nodes = {}
        last_seen = {}
        roots = [{"name": "Response", "children": [], "idx": -1, "row": None}]

        for idx, row in df.iterrows():
            name = str(self._get_name(row)).strip()
            parent = self._get_parent(row)
            parent_str = str(parent).strip() if pd.notna(parent) else ""
            section = str(self._get_col_value(row, ["Section"])).strip().lower()

            node = {"row": row, "children": [], "idx": idx, "name": name}
            nodes[idx] = node

            # Linking Logic
            if section in ["header", "headers", "content"]:
                roots[0]["children"].append(node)
            else:
                target_idx = -1
                if parent_str in last_seen:
                    target_idx = last_seen[parent_str]
                else:
                    m = re.match(r"(.+)\[(\d+)\]$", parent_str)
                    if m:
                        base = m.group(1)
                        if base in last_seen:
                            target_idx = last_seen[base]

                if target_idx != -1:
                    nodes[target_idx]["children"].append(node)
                else:
                    roots[0]["children"].append(node)

            if name and name.lower() != "nan":
                last_seen[name] = idx

        return roots[0] if roots else None

    def _extract_response_description(self, df, root_node):
        """
        Extracts response description with priority:
        1. df.attrs['response_description']
        2. Description column
        3. Parent column (fallback)
        """
        desc = None
        if hasattr(df, "attrs") and "response_description" in df.attrs:
            desc = df.attrs["response_description"]

        if pd.isna(desc) or not str(desc).strip():
            if root_node["row"] is not None:
                desc = self._get_description(root_node["row"])

        if pd.isna(desc) or not str(desc).strip():
            if root_node["row"] is not None:
                desc = self._get_parent(root_node["row"])

        return str(desc).strip() if pd.notna(desc) else "Response"

    def _process_response_headers(self, header_nodes):
        """
        Processes header nodes into OAS headers dict.
        Handles both header component refs and schema refs.
        """
        if not header_nodes:
            return None

        headers = {}
        for h_node in header_nodes:
            row = h_node["row"]
            h_name = h_node["name"]
            schema_ref = self._get_schema_name(row)

            if pd.notna(schema_ref):
                schema_ref = str(schema_ref).strip()
                if schema_ref in self.oas["components"]["headers"]:
                    headers[h_name] = {"$ref": f"#/components/headers/{schema_ref}"}
                else:
                    headers[h_name] = {
                        "schema": {"$ref": f"#/components/schemas/{schema_ref}"},
                        "description": self._get_description(row) or "",
                    }
            else:
                h_schema = self._map_type_to_schema(row)
                h_desc = h_schema.pop("description", None)
                head_obj = {"schema": h_schema}
                if h_desc:
                    head_obj["description"] = h_desc
                headers[h_name] = head_obj

        return headers

    def _process_response_content(self, content_nodes, schema_nodes, root_node):
        """
        Processes content nodes (explicit) or schema nodes (implicit) into OAS content dict.
        Returns content dict or None.
        """
        if content_nodes:
            content = {}
            for c_node in content_nodes:
                content_type = c_node["name"]

                # Split children into schema vs examples
                c_schema_nodes = []
                c_example_nodes = []
                for grand in c_node["children"]:
                    sec = (
                        str(self._get_col_value(grand["row"], ["Section"]))
                        .strip()
                        .lower()
                    )
                    if sec in ["example", "examples"]:
                        c_example_nodes.append(grand)
                    else:
                        c_schema_nodes.append(grand)

                # Build schema (include parent node for proper hierarchy)
                all_schema_rows = [c_node["row"]] + [
                    n["row"] for n in self._flatten_subtree(c_schema_nodes)
                ]
                c_schema_df = pd.DataFrame(all_schema_rows)

                if not c_schema_df.empty:
                    schema = self._build_schema_from_flat_table(c_schema_df)
                else:
                    schema = {}

                # Build examples
                examples = {}
                if c_example_nodes:
                    ex_df = pd.DataFrame(
                        [n["row"] for n in self._flatten_subtree(c_example_nodes)]
                    )
                    examples = self._build_examples_from_rows(ex_df)

                # Suppress schema for empty objects if no attributes
                c_type = str(self._get_type(c_node["row"])).strip().lower()
                has_attributes = len(c_schema_nodes) > 0

                if c_type == "object" and not has_attributes:
                    content_entry = {}
                else:
                    content_entry = {"schema": schema}

                if examples:
                    content_entry["examples"] = {}
                    for k, v in examples.items():
                        if isinstance(v, dict) and "value" in v:
                            content_entry["examples"][k] = v
                        else:
                            content_entry["examples"][k] = {"value": v}

                content[content_type] = content_entry

            return content

        elif schema_nodes:
            # Implicit content (legacy)
            default_ct = "application/json"
            if "/" in root_node["name"]:
                default_ct = root_node["name"]

            schema_df = pd.DataFrame(
                [n["row"] for n in self._flatten_subtree(schema_nodes)]
            )
            schema = self._build_schema_from_flat_table(schema_df)

            return {default_ct: {"schema": schema}}

        return None

    def _build_single_response(self, df, body_examples=None, code=""):
        """
        Builds a single OAS response object from DataFrame.
        Delegates to helper methods for tree building, headers, and content.
        """
        if df is None or df.empty:
            return {"description": "Response"}

        # Build tree structure from flat rows
        root_node = self._build_response_tree(df)
        if not root_node:
            return {"description": "Response"}

        # Extract response description
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
                    return {"$ref": f"#/components/responses/{schema_ref}"}

            # Classify node
            if section in ["header", "headers"] or r_type == "header":
                header_nodes.append(child)
            elif section == "content":
                content_nodes.append(child)
            elif c_name.startswith("x-"):
                # Extension on Response Object
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
        """Helper to collect all descendant rows from a list of nodes"""
        rows = []
        for n in nodes:
            rows.append(n)
            rows.extend(self._flatten_subtree(n["children"]))
        return rows

    def _build_examples_from_rows(self, df):
        """
        Constructs example objects from rows marked as Section='example'.
        Handles nesting and list indices (e.g. items[0]).
        """
        if df.empty:
            return {}

        # 1. Identify distinct examples (Root rows looking like Example Name)
        # Roots are rows where Section='example' (found in calling function logic)
        # But here we just have a pile of rows.
        # We assume the caller passes a DF containing the Example Roots AND their children.

        # Re-index by Name
        df = df.copy()
        df.columns = df.columns.str.strip()
        nodes = {}
        for idx, row in df.iterrows():
            name = self._get_name(row)
            # If name is "examples" or "example" (the section header), we might skip or use as root?
            # Actually, usually Name="Bad Request".
            if pd.isna(name):
                continue
            name = str(name).strip()

            # Value from Example column
            ex_val = self._get_col_value(row, ["Example", "Examples"])

            nodes[idx] = {
                "name": name,
                "parent": self._get_parent(row),
                "type": self._get_type(row),  # Capture type for array logic
                "value": ex_val,
                "children": [],
            }

        # Build IDs map
        # We need to map Parent Name -> List of Nodes
        # But names are not unique (e.g. 'code' might appear in multiple objects).
        # We need tree reconstruction relying on Parent.
        # This is tricky without unique IDs. We rely on the order or name matching?
        # The generator uses Name-based parent lookup in _build_schema...
        # So we assume Parent column refers to the Name of a previous row.

        name_to_nodes = {}
        for idx, node in nodes.items():
            n = node["name"]
            if n not in name_to_nodes:
                name_to_nodes[n] = []
            name_to_nodes[n].append(node)

        roots = []

        for idx, node in nodes.items():
            parent_name = node["parent"]
            if pd.isna(parent_name):
                roots.append(node)
            else:
                # Find parent
                p_nodes = name_to_nodes.get(str(parent_name).strip())

                # Check for array indexed parent (e.g. errors[0])
                if not p_nodes:
                    m = re.match(r"(.+)\[(\d+)\]$", str(parent_name).strip())
                    if m:
                        base = m.group(1)
                        idx = int(m.group(2))
                        p_nodes = name_to_nodes.get(base)
                        if p_nodes:
                            # We found the base array node!
                            # We attach this child to it.
                            # BUT we need to mark that it belongs to index 'idx'.
                            # For flat reconstruction, we can just attach it.
                            # But `build_node` needs to know about indices.
                            # We can store 'index' in the node metadata?
                            node["array_index"] = idx

                if p_nodes:
                    p_nodes[0]["children"].append(node)
                else:
                    roots.append(node)  # Parent not found, treat as root

        # Now convert trees to dict/value
        result = {}

        def build_node(node):
            # If leaf, return value (parsed)
            if not node["children"]:
                val = node["value"]
                return self._parse_example_string(val) if pd.notna(val) else None

            # Group children by array_index if present
            # This handles parent="list[0]" case
            list_grouped = {}
            has_indexed_children = False

            # Check if any child has array_index
            for child in node["children"]:
                if "array_index" in child:
                    has_indexed_children = True
                    idx = child["array_index"]
                    if idx not in list_grouped:
                        list_grouped[idx] = {}
                    # Build child value recursively
                    # Note: child name is the property name (e.g. 'dateTime')
                    list_grouped[idx][child["name"]] = build_node(child)

            if has_indexed_children:
                # Construct list from groups
                max_idx = max(list_grouped.keys()) if list_grouped else -1
                result_list = [None] * (max_idx + 1)
                for idx, obj in list_grouped.items():
                    result_list[idx] = obj
                return result_list

            # Function to handle name[0] notation (child name text)
            # (Existing logic implies child name itself is indexed, e.g. items[0], items[1]...)
            # We reuse similar logic?
            # If child name is "items[0]", then we are building a dict where key is "items"?
            # Or is the parent an array?
            # If parent is "items", and children are "items[0]", "items[1]"... that's weird naming.
            # Usually: Parent="items", Child="subfield", ParentRef="items[0]". (Handled above).
            # OR Parent="obj", Child="items[0]".
            # In formatting string: `items[0]` might mean `items` is a list, and we are defining index 0.

            # Legacy logic for name[idx]:
            obj = {}
            for child in node["children"]:
                child_val = build_node(child)
                c_name = child["name"]

                m = re.match(r"(.+)\[(\d+)\]$", c_name)
                if m:
                    base = m.group(1)
                    idx = int(m.group(2))
                    if base not in obj:
                        obj[base] = []
                    while len(obj[base]) <= idx:
                        obj[base].append(None)
                    # If we are assigning a value to index, we assume it's a scalar or object?
                    # Ideally we merge?
                    # For now, just assign.
                    obj[base][idx] = child_val
                else:
                    obj[c_name] = child_val

            # FIX: If node type is array but children were properties, wrap in list
            if str(node.get("type", "")).strip().lower() == "array":
                return [obj]

            return obj

        # Re-implement simple dict builder without complex array logic for now
        # Just standard Key-Value
        final_examples = {}
        for root in roots:
            final_examples[root["name"]] = build_node(root)

        return final_examples

    def _build_schema_from_flat_table(self, df):
        """
        Reconstructs a nested schema from flat parent/child rows.
        """
        # 1. Index rows by Name for parent lookup
        df.columns = df.columns.str.strip()

        nodes = {}
        roots = []

        for idx, row in df.iterrows():
            name = self._get_name(row)
            if pd.isna(name):
                continue
            name = str(name).strip()

            # Skip rows that look like content-types or section headers if they don't have schema info
            # FIX: Do NOT skip "application/json" if it acts as a parent!
            # if name == "application/json" and pd.isna(self._get_parent(row)):
            #    continue

            node = {
                "name": name,
                "type": self._get_type(row),
                "description": self._get_description(row),
                "parent": self._get_parent(row),
                "mandatory": str(
                    self._get_col_value(row, ["Mandatory", "Required"]) or ""
                ).lower()
                in ["yes", "y", "true", "m"],
                "schema_obj": self._map_type_to_schema(row, is_node=True),
            }

            nodes[name] = node

        # 2. Build Tree
        for name, node in nodes.items():
            parent_name = node["parent"]

            if pd.isna(parent_name) or str(parent_name).strip() == "":
                roots.append(node)
            else:
                parent_name = str(parent_name).strip()
                if parent_name in nodes:
                    parent = nodes[parent_name]
                    parent_schema = parent["schema_obj"]

                    if parent_schema.get("type") == "array":
                        # Handle Array of Objects
                        items = parent_schema.get("items", {})
                        is_object_array = isinstance(items, dict) and (
                            items.get("type") == "object" or "properties" in items
                        )

                        if is_object_array:
                            if "properties" not in items:
                                items["properties"] = {}
                            items["properties"][name] = node["schema_obj"]

                            # Handle Required for Items
                            if node["mandatory"]:
                                if "required" not in items:
                                    items["required"] = []
                                if name not in items["required"]:
                                    items["required"].append(name)

                            parent_schema["items"] = items
                        else:
                            # Original behavior: Overwrite items (e.g. for Array of Strings or Array of Refs)
                            parent_schema["items"] = node["schema_obj"]
                    else:
                        if "properties" not in parent_schema:
                            parent_schema["properties"] = {}
                        parent_schema["properties"][name] = node["schema_obj"]

                        # Handle Required
                        if node["mandatory"]:
                            if "required" not in parent_schema:
                                parent_schema["required"] = []
                            if name not in parent_schema["required"]:
                                parent_schema["required"].append(name)
                else:
                    # Parent not in nodes (e.g. application/json). Treat as Root.
                    roots.append(node)

        # FIX: Re-order 'example' and 'examples' to be the LAST keys in the schema object
        # Using destructive update with OrderedDict to ensure PyYAML respects the order
        from collections import OrderedDict

        for name, node in nodes.items():
            schema = node["schema_obj"]

            ex = schema.pop("example", None)
            exs = schema.pop("examples", None)

            # Create a new ordered dict with remaining items
            new_schema = OrderedDict()
            for k, v in schema.items():
                new_schema[k] = v

            # Add back examples at the end
            if ex is not None:
                new_schema["example"] = ex
            if exs is not None:
                new_schema["examples"] = exs

            # Destructive update of the original reference
            schema.clear()
            schema.update(new_schema)

        # 3. Return the Root Schema
        if len(roots) == 1:
            return roots[0]["schema_obj"]
        elif len(roots) > 1:
            return {
                "type": "object",
                "properties": {r["name"]: r["schema_obj"] for r in roots},
            }
        else:
            return {}

    def _handle_combinator_refs(self, type_val, schema_ref, desc=None):
        """
        Handles oneOf/allOf/anyOf combinators with schema references.
        Returns complete schema dict or None if not a combinator.
        """
        if type_val not in ["oneof", "allof", "anyof"]:
            return None

        refs = [r.strip() for r in str(schema_ref).split(",")]
        combinator_key = {"oneof": "oneOf", "allof": "allOf", "anyof": "anyOf"}.get(
            type_val
        )

        schema = {
            combinator_key: [{"$ref": f"#/components/schemas/{r}"} for r in refs if r]
        }

        if pd.notna(desc):
            schema["description"] = str(desc)

        return schema

    def _handle_schema_reference(self, type_val, schema_ref, desc):
        """
        Handles $ref with OAS 3.0 workaround for description.
        Returns schema dict with appropriate ref structure.
        """
        ref_path = f"#/components/schemas/{schema_ref}"

        if type_val == "array":
            return {"type": "array", "items": {"$ref": ref_path}}

        # OAS 3.0 Workaround: $ref + description requires allOf wrapper
        has_desc = pd.notna(desc)
        is_oas30 = self.version.startswith("3.0")

        if is_oas30 and has_desc:
            return {"allOf": [{"$ref": ref_path}], "description": str(desc)}
        else:
            return {"$ref": ref_path}

    def _apply_schema_constraints(self, schema, row, type_val):
        """
        Applies enums, format, pattern, and min/max constraints to schema.
        Modifies schema dict in-place.
        """
        # Enums
        enum_val = self._get_col_value(row, ["Allowed value", "Allowed values"])
        if pd.notna(enum_val):
            enum_list = [x.strip() for x in str(enum_val).split(",")]

            # Cast based on type
            if type_val == "integer":
                try:
                    enum_list = [int(x) for x in enum_list if x]
                except ValueError:
                    pass
            elif type_val == "number":
                try:
                    new_list = []
                    for x in enum_list:
                        if not x:
                            continue
                        f = float(x)
                        if f.is_integer():
                            new_list.append(int(f))
                        else:
                            new_list.append(f)
                    enum_list = new_list
                except ValueError:
                    pass

            schema["enum"] = enum_list

        # Format and Pattern
        fmt = self._get_col_value(row, ["Format"])
        if pd.notna(fmt):
            schema["format"] = str(fmt)

        pattern = self._get_col_value(row, ["PatternEba", "Pattern", "Regex"])
        if pd.notna(pattern):
            schema["pattern"] = str(pattern)

        # Min/Max constraints
        min_val = self._get_col_value(
            row,
            [
                "Min\nValue/Length/Item",
                "Min  \nValue/Length/Item",
                "Min Value/Length/Item",
                "Min",
            ],
        )
        max_val = self._get_col_value(
            row,
            [
                "Max\nValue/Length/Item",
                "Max  \nValue/Length/Item",
                "Max Value/Length/Item",
                "Max",
            ],
        )

        if pd.notna(min_val):
            try:
                val = int(min_val) if float(min_val).is_integer() else float(min_val)
                if type_val == "string":
                    schema["minLength"] = int(val)
                elif type_val in ["integer", "number"]:
                    schema["minimum"] = val
                elif type_val == "array":
                    schema["minItems"] = int(val)
            except (ValueError, TypeError):
                pass

        if pd.notna(max_val):
            try:
                val = int(max_val) if float(max_val).is_integer() else float(max_val)
                if type_val == "string":
                    schema["maxLength"] = int(val)
                elif type_val in ["integer", "number"]:
                    schema["maximum"] = val
                elif type_val == "array":
                    schema["maxItems"] = int(val)
            except (ValueError, TypeError):
                pass

    def _map_type_to_schema(self, row, is_node=False):
        """
        Maps Excel row data to an OAS schema object.
        Delegates to helper methods for combinators, references, and constraints.
        """
        type_val = self._get_type(row)
        if pd.isna(type_val):
            type_val = "string"
        type_val = str(type_val).strip().lower()

        schema = {}
        schema_ref = self._get_schema_name(row)
        desc = self._get_description(row)

        # Handle combinators (oneOf/allOf/anyOf)
        if pd.notna(schema_ref):
            combinator_schema = self._handle_combinator_refs(type_val, schema_ref, desc)
            if combinator_schema:
                return combinator_schema

            # Handle standard $ref
            ref_schema = self._handle_schema_reference(type_val, schema_ref, desc)
            schema.update(ref_schema)

        # Filter out Excel-specific type keywords
        invalid_types = ["parameter", "parameters", "schema", "header", "response"]
        if type_val in invalid_types:
            type_val = "string"  # Fallback to string

        # Set base type if not already set by ref handling
        if type_val != "array" and "$ref" not in schema and "allOf" not in schema:
            schema["type"] = type_val

        # Add description if not already present
        if pd.notna(desc) and "description" not in schema:
            schema["description"] = str(desc)

        # Apply constraints (enum, format, pattern, min/max)
        self._apply_schema_constraints(schema, row, type_val)

        # Handle array-specific logic
        if type_val == "array":
            schema["type"] = "array"
            item_type_raw = self._get_col_value(
                row,
                [
                    "Items Data Type\n(Array only)",
                    "Items Data Type \n(Array only)",
                    "Items Data Type",
                    "Item Type",
                ],
            )

            if pd.notna(item_type_raw):
                item_type = str(item_type_raw).strip().lower()

                # Handle combinators in array items
                if item_type in ["oneof", "allof", "anyof"] and pd.notna(schema_ref):
                    combinator_schema = self._handle_combinator_refs(
                        item_type, schema_ref
                    )
                    if combinator_schema:
                        schema["items"] = combinator_schema
                else:
                    # Set primitive type or reference
                    allowed_types = [
                        "string",
                        "number",
                        "integer",
                        "boolean",
                        "array",
                        "object",
                    ]
                    if item_type in allowed_types:
                        schema["items"] = {"type": item_type}
                    elif item_type not in invalid_types:
                        # Assume it's a reference
                        if pd.isna(schema_ref):
                            ref_name = str(item_type_raw).strip()
                            schema["items"] = {
                                "$ref": f"#/components/schemas/{ref_name}"
                            }
            elif "items" not in schema:
                schema["items"] = {}

        # Add examples (at the end for YAML formatting)
        ex = self._get_col_value(row, ["Example", "Examples"])
        if pd.notna(ex):
            parsed_ex = self._parse_example_string(ex)
            if self.version.startswith("3.1"):
                schema["examples"] = [parsed_ex]
            else:
                schema["example"] = parsed_ex

        return schema

    def build_components(self, global_components):
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
                    # Build Schema Inline
                    schema = self._map_type_to_schema(row)

                    header_desc = self._get_description(row)

                    # Create Header Object with INLINE schema
                    header_obj = {"schema": schema}
                    if header_desc:
                        header_obj["description"] = str(header_desc)

                    self.oas["components"]["headers"][name] = header_obj

        # 3. Schemas (Global)
        if global_components.get("schemas") is not None:
            schema_tree = self._build_schema_group(global_components["schemas"])
            self.oas["components"]["schemas"] = schema_tree

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
                        roots.append(node)

                # Update last_seen
                if name and name.lower() != "nan":
                    last_seen[name] = idx

            # Process Roots
            for root_node in roots:
                root_row = root_node["row"]
                root_name = root_node["name"]

                # Flatten tree
                collected_rows = []

                def collect(n):
                    collected_rows.append(n["row"])
                    for c in n["children"]:
                        collect(c)

                collect(root_node)

                if not root_name or root_name.lower() == "nan":
                    continue

                response_df = pd.DataFrame(collected_rows)
                self.oas["components"]["responses"][str(root_name)] = (
                    self._build_single_response(response_df)
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
        df.columns = df.columns.str.strip()

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
            # Add title if Name is root?
            # If it's a root (no parent), usually schema name = title too?
            # Or description is used as title?
            # OAS schema 'title' property.

            nodes[idx] = node
            node_map[name] = node

        # 2. Link
        for idx, node in nodes.items():
            name = node["name"]
            parent_name = node["parent"]
            if pd.isna(parent_name):
                roots.append(node)
                # Assign Title to Root if missing?
                if "title" not in node["schema_obj"]:
                    node["schema_obj"]["title"] = name
            elif str(parent_name).strip() in node_map:
                parent = node_map[str(parent_name).strip()]
                parent_schema = parent["schema_obj"]

                if parent_schema.get("type") == "array":
                    # If parent is array, child usually defines properties of the item object
                    # Check if items is explicitly object or empty dict (default from map_type)
                    items_schema = parent_schema.get("items", {})
                    # Ensure items is a dict
                    if not isinstance(items_schema, dict):
                        # Should not happen if map_type works, but safety check
                        parent_schema["items"] = {}
                        items_schema = parent_schema["items"]

                    # Logic: If we are adding multiple children to an array, they are properties of the item object.
                    # FORCE item type to object if we are adding properties
                    if "type" not in items_schema:
                        items_schema["type"] = "object"

                    if items_schema.get("type") == "object":
                        if "properties" not in items_schema:
                            items_schema["properties"] = {}

                        items_schema["properties"][name] = node["schema_obj"]

                        # Handle Required for Item
                        if node["mandatory"]:
                            if "required" not in items_schema:
                                items_schema["required"] = []
                            if name not in items_schema["required"]:
                                items_schema["required"].append(name)

                        parent_schema["items"] = items_schema
                    else:
                        # If items type is NOT object (e.g. array of strings with a child? Unlikely schema design)
                        # We fallback to overwriting (Last one wins - Legacy behavior)
                        parent_schema["items"] = node["schema_obj"]
                else:
                    if "properties" not in parent_schema:
                        parent_schema["properties"] = {}
                    parent_schema["properties"][name] = node["schema_obj"]

                    # Handle Required
                    if node["mandatory"]:
                        if "required" not in parent_schema:
                            parent_schema["required"] = []
                        if name not in parent_schema["required"]:
                            parent_schema["required"].append(name)

        # 3. Return map of Root Name -> Schema
        return {r["name"]: r["schema_obj"] for r in roots}

        return {r["name"]: r["schema_obj"] for r in roots}

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

    def _recursive_schema_fix(self, obj):
        """
        Recursively traverses the OAS structure and enforces that 'example' and 'examples'
        keys are strictly at the end of any dictionary containing them.
        """
        if isinstance(obj, dict):
            # 1. Process children first
            for k, v in obj.items():
                self._recursive_schema_fix(v)

            # 2. Re-order current dict if needed
            if "example" in obj or "examples" in obj:
                # Use destructive update to change order in-place
                from collections import OrderedDict

                ex = obj.pop("example", None)
                exs = obj.pop("examples", None)

                # Reconstruct dict order (remaining keys are already in order)
                new_d = OrderedDict()
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

    def _insert_raw_extensions(self, yaml_text, oas_dict):
        """Replace __RAW_EXTENSIONS__ markers with raw YAML text"""
        import re

        # Find all __RAW_EXTENSIONS__ values
        if "paths" not in oas_dict:
            return yaml_text

        for path_url, path_item in oas_dict["paths"].items():
            for method, operation in path_item.items():
                if isinstance(operation, dict) and "__RAW_EXTENSIONS__" in operation:
                    raw_text = operation["__RAW_EXTENSIONS__"]
                    # Don't dedent - Excel text already has correct relative indentation
                    # Just need to add base operation-level indent

                    # Find and replace the marker in YAML output
                    # Pattern: __RAW_EXTENSIONS__: followed by quoted string (possibly multiline with |- or |)
                    # Match variations: __RAW_EXTENSIONS__: 'text', "text", |- or |
                    pattern = r"__RAW_EXTENSIONS__:(?:\s+(?:['\"].*?['\"]|\|-[\s\S]*?(?=\n\S)|\|[\s\S]*?(?=\n\S)))"

                    # Simple approach: find the line with marker and replace it with raw text
                    output_lines = yaml_text.split("\n")
                    new_output = []
                    i = 0
                    while i < len(output_lines):
                        line = output_lines[i]
                        if "__RAW_EXTENSIONS__:" in line:
                            # Excel text ALREADY has absolute indentation (6 spaces)
                            # Don't add marker_indent - just use text as-is
                            marker_indent = len(line) - len(
                                line.lstrip()
                            )  # Still need for skipping
                            for raw_line in raw_text.split("\n"):
                                new_output.append(
                                    raw_line
                                )  # Insert exactly as-is from Excel

                            # Skip lines that are part of the __RAW_EXTENSIONS__ value
                            # (YAML will dump it as |- multiline or quoted)
                            i += 1
                            # Skip continuation lines (indented more than current)
                            while i < len(output_lines):
                                next_line = output_lines[i]
                                if next_line.strip() == "":
                                    # Empty line, might be part of content
                                    i += 1
                                    continue
                                next_indent = len(next_line) - len(next_line.lstrip())
                                if next_indent > marker_indent:
                                    # Continuation of the value, skip it
                                    i += 1
                                else:
                                    # Next key at same or less indent, stop skipping
                                    break
                        else:
                            new_output.append(line)
                            i += 1

                    yaml_text = "\n".join(new_output)

        return yaml_text

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
        :param source_filename: Optional filename of the base OAS file to reference in description.
        """
        # 0. Append source reference to Description
        if source_filename:
            if "info" not in self.oas:
                self.oas["info"] = {}
            if "description" not in self.oas["info"]:
                self.oas["info"]["description"] = ""

            # Use strict newline format as requested
            self.oas["info"]["description"] += f"\n\nBased on {source_filename}"

        # 1. SERVERS
        self.oas["servers"] = [
            {
                "url": "https://api.swiftnet.sipn.swift.com/ebacl-fpad/v1",
                "description": "Live environment",
            },
            {
                "url": "https://api-test.swiftnet.sipn.swift.com/ebacl-fpad-pilot/v1",
                "description": "Test environment",
            },
        ]

        # 2. GLOBAL SECURITY
        self.oas["security"] = [{"oauthBearerToken": []}]

        # 3. COMPONENTS
        if "components" not in self.oas:
            self.oas["components"] = {}
        comps = self.oas["components"]

        # 3.1 Security Schemes
        if "securitySchemes" not in comps:
            comps["securitySchemes"] = {}
        comps["securitySchemes"]["oauthBearerToken"] = {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "opaque OAuth 2.0",
            "description": "The access token obtained as a result of OAuth 2.0 flows. SWIFT supports two OAuth grant types depending on the API service.\n* JWT-Bearer grant type [RFC 7523](https://tools.ietf.org/html/rfc7523)\n* Password grant type\n\nThis API uses JWT-Bearer grant type.\n\nPlease visit [SWIFT OAuth Token API](https://developer.swift.com/swift-oauth-token-api) page for more information and examples on how to generate an OAuth token.\n\nIn this declaration only the basic security element to transport the bearer token of an OAuth2 process is declared.\n",
        }

        # 3.2 Parameters (ivUserKey, ivUserBic)
        if "parameters" not in comps:
            comps["parameters"] = {}

        # FIX: Ensure proper order - ivUserKey and ivUserBic MUST be first as per request
        new_params = {}

        # 1. Add specific params first
        specific_params = {
            "ivUserKey": {
                "name": "ivUserKey",
                "in": "header",
                "description": "The subscription key of a Participant. cn=<SSO+BIC+UserId+T>,o=BIC8,o=swift. SSO is a fixed string, last char is for environment (P for production and T for test) eg SSOUNCRITMMAPI12345P, o=uncritmm,o=swift",
                "required": True,
                "schema": {
                    "type": "string",
                    "description": "The subscription key of a Participant. cn=<SSO+BIC+UserId+T>,o=BIC8,o=swift. SSO is a fixed string, last char is for environment (P for production and T for test) eg SSOUNCRITMMAPI12345P, o=uncritmm,o=swift",
                    "example": "cn=SSOUNCRITMMAPI12345P,o=uncritmm,o=swift",
                },
            },
            "ivUserBic": {
                "name": "ivUserBic",
                "in": "header",
                "description": "BIC of the user.",
                "required": True,
                "schema": {
                    "type": "string",
                    "description": "BIC of the user.",
                    "example": "UNCRITMM",
                    "pattern": "^[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}([A-Z0-9]{3,3}){0,1}$",
                },
            },
        }

        # Add them to new dict
        new_params.update(specific_params)

        # 2. Add existing params (avoiding duplicates if any)
        for k, v in comps["parameters"].items():
            if k not in new_params:
                new_params[k] = v

        # 3. Replace component parameters
        comps["parameters"] = new_params

        # 3.3 Headers (X-Request-ID)
        if "headers" not in comps:
            comps["headers"] = {}
        comps["headers"]["X-Request-ID"] = {
            "description": "Specify an unique end to end tracking request ID. The element will be populated by the SWIFT API gateway",
            "schema": {"type": "string"},
        }

        # 3.4 Schemas (Errors, ErrorMessage)
        if "schemas" not in comps:
            comps["schemas"] = {}

        comps["schemas"]["Errors"] = {
            "description": "Container to return multiple ErrorMessage object. Collection of error can be useful when API needs to return multiple errors, for example validation errors. When the response code conveys application-specific functional semantics and consumer can parse machine-readable error code, this block can be useful. The error response must contain at least one error object.",
            "type": "array",
            "items": {"$ref": "#/components/schemas/ErrorMessage"},
        }

        comps["schemas"]["ErrorMessage"] = {
            "description": "Custom error schema to support detailed error message.",
            "type": "object",
            "additionalProperties": False,
            "required": ["code", "severity", "text"],
            "properties": {
                "severity": {
                    "description": "Specifies the severity of the error.",
                    "type": "string",
                    "enum": ["Fatal", "Transient", "Logic"],
                },
                "code": {
                    "description": "Specifies the custom error code as defined by the service provider.",
                    "type": "string",
                    "minLength": 3,
                    "maxLength": 70,
                },
                "text": {
                    "description": "Specifies the detail error message identifying the cause of the error.",
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 255,
                },
                "user_message": {
                    "description": "A human-readable text describing the error.",
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 255,
                },
                "more_info": {
                    "description": "Specifies an URL to find more information about the error.",
                    "type": "string",
                    "format": "uri",
                },
            },
        }

        # 4. COMPONENTS MODIFICATIONS (Responses)
        # Add Header X-Request-ID to ALL Response Components
        if "responses" in comps:
            for r_name, r_obj in comps["responses"].items():
                if "headers" not in r_obj:
                    r_obj["headers"] = {}
                r_obj["headers"]["X-Request-ID"] = {
                    "$ref": "#/components/headers/X-Request-ID"
                }

        # 5. PATHS MODIFICATIONS
        if "paths" in self.oas:
            for path_url, methods in self.oas["paths"].items():
                for method, op in methods.items():
                    if method.startswith("x-") or not isinstance(op, dict):
                        continue

                    # 5.1 Inject Parameters
                    if "parameters" not in op:
                        op["parameters"] = []

                    # Ensure ivUserKey/ivUserBic are at the top
                    # Remove existing if present to avoid duplication/misordering
                    new_refs = [
                        {"$ref": "#/components/parameters/ivUserKey"},
                        {"$ref": "#/components/parameters/ivUserBic"},
                    ]
                    existing_params = [p for p in op["parameters"] if p not in new_refs]

                    # Prepend new refs
                    op["parameters"] = new_refs + existing_params

                    if "responses" in op:
                        for code, resp in op["responses"].items():

                            # 5.2 Polymorphic 400
                            # If it's a 400 Ref, Resolve it first to allow modification
                            if str(code) == "400" and "$ref" in resp:
                                ref_path = resp["$ref"]
                                ref_name = ref_path.split("/")[-1]
                                if (
                                    "responses" in comps
                                    and ref_name in comps["responses"]
                                ):
                                    # Inline the component content
                                    resp = copy.deepcopy(comps["responses"][ref_name])
                                    op["responses"][code] = resp  # Update in place

                            if str(code) == "400":
                                if (
                                    "content" in resp
                                    and "application/json" in resp["content"]
                                ):
                                    resp["content"]["application/json"]["schema"] = {
                                        "oneOf": [
                                            {
                                                "$ref": "#/components/schemas/ErrorResponse"
                                            },
                                            {"$ref": "#/components/schemas/Errors"},
                                        ]
                                    }
                                    # Remove examples from 400 responses (SWIFT requirement)
                                    if "example" in resp["content"]["application/json"]:
                                        del resp["content"]["application/json"]["example"]
                                    if "examples" in resp["content"]["application/json"]:
                                        del resp["content"]["application/json"]["examples"]

                            # 5.3 Inject Headers to Responses (X-Request-ID)
                            # Only if NOT a ref (Refs are handled in Component Loop above)
                            if "$ref" not in resp:
                                if "headers" not in resp:
                                    resp["headers"] = {}
                                resp["headers"]["X-Request-ID"] = {
                                    "$ref": "#/components/headers/X-Request-ID"
                                }

        # 6. CLEANUP (Remove x-sandbox extensions)
        def clean_sandbox(d):
            if isinstance(d, dict):
                keys = list(d.keys())
                for k in keys:
                    if k == "__RAW_EXTENSIONS__" and isinstance(d[k], str):
                        lines = d[k].split("\n")
                        filtered_lines = []
                        skip_level = -1

                        for line in lines:
                            # Calculate indentation
                            stripped = line.lstrip()
                            if not stripped:  # Empty line
                                if skip_level == -1:
                                    filtered_lines.append(line)
                                continue

                            current_indent = len(line) - len(stripped)

                            # If we are strictly deeper than the key we skipped, continue skipping
                            if skip_level != -1 and current_indent > skip_level:
                                continue

                            # We are back to same level or easier, stop skipping (unless this is also a target)
                            skip_level = -1

                            # Check if this is a target key
                            if stripped.startswith("x-sandbox"):
                                skip_level = current_indent
                                continue

                            # Keep line
                            filtered_lines.append(line)

                        new_text = "\n".join(filtered_lines)

                        if not new_text.strip():
                            del d[k]
                        else:
                            d[k] = new_text

                    elif k.startswith("x-sandbox"):
                        del d[k]
                    else:
                        clean_sandbox(d[k])
            elif isinstance(d, list):
                for item in d:
                    clean_sandbox(item)

        clean_sandbox(self.oas)
