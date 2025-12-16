import yaml
import pandas as pd
import json
import textwrap
from collections import OrderedDict

# RawYAML - stores raw YAML text for literal insertion
class RawYAML:
    def __init__(self, raw_text, base_indent=0):
        self.raw_text = raw_text
        self.base_indent = base_indent

# LiteralString wrapper to force literal block style
class LiteralString(str):
    pass

# Custom YAML Loader that preserves order and wraps multiline strings
class OrderPreservingLoader(yaml.SafeLoader):
    pass

def construct_mapping(loader, node):
    loader.flatten_mapping(node)
    pairs = loader.construct_pairs(node)
    return OrderedDict(pairs)

def construct_scalar(loader, node):
    value = loader.construct_scalar(node)
    # Auto-wrap multiline strings in LiteralString
    if isinstance(value, str) and '\n' in value:
        return LiteralString(value)
    return value

OrderPreservingLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    construct_mapping)

OrderPreservingLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_SCALAR_TAG,
    construct_scalar)

# Custom YAML Dumper
class OASDumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(OASDumper, self).increase_indent(flow, False)

def raw_yaml_presenter(dumper, data):
    # Output raw YAML text as-is
    # Split by lines and output each
    lines = data.raw_text.strip().split('\n')
    # Return as a literal scalar block
    return dumper.represent_scalar('tag:yaml.org,2002:str', data.raw_text, style='|')

OASDumper.add_representer(RawYAML, raw_yaml_presenter)

# Preserve OrderedDict order in output
OASDumper.add_representer(OrderedDict, 
    lambda dumper, data: dumper.represent_mapping('tag:yaml.org,2002:map', data.items()))

class OASGenerator:
    def __init__(self, version="3.0.0"):
        self.version = version
        self.oas = {
            "openapi": version,
            "info": {},
            "paths": {},
            "components": {
                "schemas": {},
                "parameters": {},
                "headers": {},
                "responses": {},
                "securitySchemes": {}
            }
        }

    def build_info(self, info_data):
        self.oas["info"] = info_data

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
                "responses": {}
            }

            # Merge Custom Extensions - USE RAW TEXT, don't parse!
            extensions_yaml = op_meta.get("extensions")
            if extensions_yaml and isinstance(extensions_yaml, str) and extensions_yaml.strip():
                # Store raw text - use rstrip to remove trailing spaces only, preserve leading indent
                op_obj["__RAW_EXTENSIONS__"] = extensions_yaml.rstrip()

            # Populate details from Operation File
            if file_ref in operations_details:
                details = operations_details[file_ref]
                
                # Parameters
                if details.get("parameters") is not None:
                    op_obj["parameters"] = self._build_parameters(details["parameters"])

                # Request Body
                if details.get("body") is not None:
                    req_body = self._build_request_body(details["body"])
                    if req_body:
                        op_obj["requestBody"] = req_body

                # Responses
                if details.get("responses"):
                    body_examples_df = details.get("body_examples")
                    body_examples = {}
                    if body_examples_df is not None:
                        # Convert DF to dict {Name: Body}
                        # Assuming col 0 is Name, col 1 is Body
                        for _, row in body_examples_df.iterrows():
                            ex_name = str(row.iloc[0]).strip()
                            ex_body = row.iloc[1]
                            if pd.notna(ex_body):
                                body_examples[ex_name] = ex_body

                    for code, df_resp in details["responses"].items():
                        op_obj["responses"][str(code)] = self._build_single_response(df_resp, body_examples, str(code))
            
            # Fallback for empty responses
            if not op_obj["responses"]:
                op_obj["responses"]["default"] = {"description": "Default response"}

            # Reorder Operation Object keys
            # Don't sort extensions - preserve original order from Excel!
            standard_pre = ["summary", "description", "operationId", "tags", "parameters", "requestBody"]
            extensions = [k for k in op_obj.keys() if k.startswith("x-")]
            # Include __RAW_EXTENSIONS__ marker with other extensions (before responses)
            if "__RAW_EXTENSIONS__" in op_obj:
                extensions.append("__RAW_EXTENSIONS__")
            standard_post = ["responses"]
            
            final_order = standard_pre + extensions + standard_post
            
            op_obj = self._reorder_dict(op_obj, final_order)

            self.oas["paths"][path_url][method] = op_obj

    def _build_parameters(self, df):
        params = []
        if df is None: return params
        
        for _, row in df.iterrows():
            name = self._get_name(row)
            if pd.isna(name): continue
            
            in_loc = self._get_col_value(row, ["In", "Location"])
            if pd.isna(in_loc): 
                 # Default to header for 'parameter' type if missing
                 type_val = str(self._get_type(row)).lower().strip()
                 if type_val == 'parameter':
                      in_loc = 'header'
                 else:
                      continue 
            
            param = {
                "name": name,
                "in": str(in_loc).lower(),
                "description": self._get_description(row) or "",
                "required": str(self._get_col_value(row, ["Mandatory", "Required"]) or "").lower() in ["yes", "y", "true", "m"],
                "schema": self._map_type_to_schema(row)
            }
            params.append(param)
        return params

    def _build_request_body(self, df):
        if df is None or df.empty: return None
        
        # The structure usually has the content-type as a root or row 0
        # Let's find the content type. 
        # Heuristic: verify if 'application/json' is in Name column
        content_type = "application/json" # Default
        
        # We process the rows to build the schema
        # We need to filter out meta-rows if they exist
        
        schema = self._build_schema_from_flat_table(df)
        
        return {
            "content": {
                content_type: {
                    "schema": schema
                }
            }
        }

    def _get_col_value(self, row, keys):
        """
        Helper to get value from row checking multiple column headers.
        """
        if isinstance(keys, str): keys = [keys]
        for k in keys:
            if k in row: # direct check
                val = row[k]
                if pd.notna(val): return val
        return None

    def _get_schema_name(self, row):
        return self._get_col_value(row, [
            "Schema Name",
            "Schema Name\n(for Type or Items Data Type = 'schema')",
            "Schema Name\n(for Type or Items Data Type = 'schema'||'header')",
            "Schema Name\n(for Type or Items Data Type = 'schema' || 'header')"
        ])

    def _get_type(self, row):
        return self._get_col_value(row, ["Type", "Data Type", "Item Type", "Type "]) 

    def _get_name(self, row):
        return self._get_col_value(row, ["Name", "Parameter Name", "Field Name", "Request Parameters", "Path"])

    def _get_parent(self, row):
        return self._get_col_value(row, ["Parent", "Parent Name"])

    def _get_description(self, row):
        return self._get_col_value(row, ["Description", "Desc", "Description "])

    def _build_single_response(self, df, body_examples=None, code=""):
        if df is None or df.empty: return {"description": "Response"}
        
        # 1. Identify Root Info
        root_row = None
        header_rows = []
        schema_rows_mask = []
        
        for idx, row in df.iterrows():
             r_type = str(self._get_type(row)).strip().lower()
             if r_type == 'header':
                 header_rows.append(row)
                 schema_rows_mask.append(False)
             else:
                 schema_rows_mask.append(True)
                 if pd.isna(self._get_parent(row)) and root_row is None:
                     root_row = row

        if root_row is None: 
             # Fallback
             return {"description": "Response"}

        desc = self._get_name(root_row) or self._get_description(root_row) or "Response"
        type_val = str(self._get_type(root_row)).strip().lower()
        schema_ref = self._get_schema_name(root_row)

        # 2. Global Response Reference (Type == 'response')
        if type_val == 'response' and pd.notna(schema_ref):
             return {"$ref": f"#/components/responses/{schema_ref}"}

        # 3. Inline Response
        resp_obj = {"description": str(desc)}
        
        # Build Schema (filtering out header rows)
        df_schema = df[schema_rows_mask].copy()
        if not df_schema.empty:
            schema = self._build_schema_from_flat_table(df_schema)
            # If the root is 'Type: object' but mostly empty, schema might be empty dict.
            # If function returns empty dict, means no properties?
            # Check if schema is empty
            if schema:
                content_type = "application/json"
                # If explicit content type in Name?
                # If root name looks like mimetype?
                if "/" in str(self._get_name(root_row)):
                    content_type = str(self._get_name(root_row)).strip()
                
                resp_obj["content"] = {
                    content_type: {
                        "schema": schema
                    }
                }
                
                # Check for Example in Root Row
                ex_val = self._get_col_value(root_row, ["Example", "Examples"])
                if pd.notna(ex_val):
                     # Try parse as JSON/YAML
                     try:
                         ex_str = str(ex_val).strip()
                         # Heuristic: if it looks like a dict of named examples
                         parsed_ex = None
                         if ex_str.startswith("{") or ex_str.startswith("["):
                              parsed_ex = json.loads(ex_str)
                         else:
                              # Try YAML for multiline
                              parsed_ex = yaml.safe_load(ex_str)
                              
                         if isinstance(parsed_ex, dict) and any(k in parsed_ex for k in ["OK", "Default", "Bad Request", "Error"]):
                              # Likely named examples map
                              # Wrap in { value: ... } if not already?
                              # OAS expects: examples: { name: { value: ... } }
                              # If the user provided just the value map, we might need to assume structure
                              # But let's just dump it as is if it's a dict
                              resp_obj["content"][content_type]["examples"] = parsed_ex
                         else:
                              # Single example
                              resp_obj["content"][content_type]["example"] = parsed_ex if parsed_ex else ex_val
                     except:
                            resp_obj["content"][content_type]["example"] = ex_val
                        
                # Fallback: Hybrid Heuristic from Body Examples
                if "examples" not in resp_obj.get("content", {}).get(content_type, {}) and "example" not in resp_obj.get("content", {}).get(content_type, {}):
                    if body_examples:
                         # Heuristic Mapping
                         target_name = None
                         if code.startswith('2'): target_name = "OK"
                         elif code == '400': target_name = "Bad Request"
                         elif code == '401': target_name = "Unauthorized"
                         elif code == '403': target_name = "Forbidden"
                         elif code == '404': target_name = "Not Found"
                         elif code == '500': target_name = "Internal Server Error"
                         
                         if target_name and target_name in body_examples:
                             ex_str = str(body_examples[target_name]).strip()
                             # Parse
                             try:
                                 if ex_str.startswith("{") or ex_str.startswith("["):
                                     parsed = json.loads(ex_str)
                                 else:
                                     parsed = yaml.safe_load(ex_str)
                             except:
                                 parsed = ex_str
                                 
                             # Wrap in named example
                             if "content" in resp_obj and content_type in resp_obj["content"]:
                                 resp_obj["content"][content_type]["examples"] = {
                                     target_name: {"value": parsed}
                                 }

        # 4. Headers
        if header_rows:
            headers = {}
            for row in header_rows:
                 h_name = self._get_name(row)
                 if pd.notna(h_name):
                      # Check for Global Header Reference
                      schema_ref = self._get_schema_name(row)
                      if pd.notna(schema_ref):
                           headers[h_name] = {"$ref": f"#/components/headers/{schema_ref}"}
                      else:
                           # Headers: description + schema
                           h_schema = self._map_type_to_schema(row)
                           # Extract description from schema as sibling for Header Object
                           h_desc = h_schema.pop("description", None)
                           
                           head_obj = {"schema": h_schema}
                           if h_desc: head_obj["description"] = h_desc
                
                           headers[h_name] = head_obj
                           headers[h_name] = head_obj
            
            if headers:
                resp_obj["headers"] = headers

        # Reorder Response Object keys
        # Desired: description, headers, content
        resp_obj = self._reorder_dict(resp_obj, ["description", "headers", "content"])

        return resp_obj

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
            if pd.isna(name): continue
            name = str(name).strip()
            
            # Skip rows that look like content-types or section headers if they don't have schema info
            if name == "application/json" and pd.isna(self._get_parent(row)):
                continue
            
            node = {
                "name": name,
                "type": self._get_type(row),
                "description": self._get_description(row),
                "parent": self._get_parent(row),
                "mandatory": str(self._get_col_value(row, ["Mandatory", "Required"]) or "").lower() in ["yes", "y", "true", "m"],
                "schema_obj": self._map_type_to_schema(row, is_node=True)
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
                        
        # 3. Return the Root Schema
        if len(roots) == 1:
            return roots[0]["schema_obj"]
        elif len(roots) > 1:
            return {
                "type": "object",
                "properties": {r["name"]: r["schema_obj"] for r in roots}
            }
        else:
            return {}

    def _map_type_to_schema(self, row, is_node=False):
        """
        Maps Excel row data to an OAS schema object.
        """
        type_val = self._get_type(row)
        if pd.isna(type_val): type_val = "string"
        type_val = str(type_val).lower()
        
        schema = {}
        
        # Check if it's a ref
        schema_ref = self._get_schema_name(row)
        desc = self._get_description(row)
        
        if pd.notna(schema_ref):
            ref_path = f"#/components/schemas/{schema_ref}"
            
            if type_val == "array":
                schema["type"] = "array"
                schema["items"] = {"$ref": ref_path}
            else:
                # OAS 3.0 Workaround check
                has_desc = pd.notna(desc)
                is_oas30 = self.version.startswith("3.0")
                
                if is_oas30 and has_desc:
                    schema = {
                        "allOf": [ {"$ref": ref_path} ],
                        "description": str(desc)
                    }
                    return schema 
                else:
                    schema["$ref"] = ref_path
        
        if type_val != "array" and "$ref" not in schema and "allOf" not in schema:
            schema["type"] = type_val
        
        # Add Description 
        if pd.notna(desc) and "description" not in schema: 
            schema["description"] = str(desc)

        ex = self._get_col_value(row, ["Example", "Examples"])
        if pd.notna(ex): 
            # Try to parse complex examples (JSON/YAML)
            try:
                ex_str = str(ex).strip()
                if ex_str.startswith("{") or ex_str.startswith("["):
                    schema["example"] = json.loads(ex_str)
                else:
                     schema["example"] = ex
            except:
                schema["example"] = ex
        
        # Enums
        enum_val = self._get_col_value(row, ["Allowed value", "Allowed values"])
        if pd.notna(enum_val):
            schema["enum"] = [x.strip() for x in str(enum_val).split(',')]

        # Formatting / Constraints
        fmt = self._get_col_value(row, ["Format"])
        if pd.notna(fmt): schema["format"] = str(fmt)
        
        pattern = self._get_col_value(row, ["PatternEba", "Pattern", "Regex"])
        if pd.notna(pattern): schema["pattern"] = str(pattern)

        min_val = self._get_col_value(row, ["Min\nValue/Length/Item", "Min Value/Length/Item", "Min"])
        max_val = self._get_col_value(row, ["Max\nValue/Length/Item", "Max Value/Length/Item", "Max"])
        
        if pd.notna(min_val):
            # Infer if it's minLength, minimum, or minItems property based on type
            try:
                val = int(min_val) if float(min_val).is_integer() else float(min_val)
                if type_val == "string": schema["minLength"] = int(val)
                elif type_val in ["integer", "number"]: schema["minimum"] = val
                elif type_val == "array": schema["minItems"] = int(val)
            except: pass

        if pd.notna(max_val):
            try:
                val = int(max_val) if float(max_val).is_integer() else float(max_val)
                if type_val == "string": schema["maxLength"] = int(val)
                elif type_val in ["integer", "number"]: schema["maximum"] = val
                elif type_val == "array": schema["maxItems"] = int(val)
            except: pass

        if type_val == "array":
            # If explicit item type is given
            item_type = self._get_col_value(row, ["Items Data Type\n(Array only)", "Items Data Type", "Item Type"])
            if pd.notna(item_type):
                 schema["items"] = {"type": str(item_type).lower()}
            elif "items" not in schema:
                 schema["items"] = {} 

        return schema

    def build_components(self, global_components):
        """
        Populates self.oas["components"]
        """
        if not global_components: return

        # Schemas
        if global_components.get("schemas") is not None:
             schema_tree = self._build_schema_group(global_components["schemas"])
             self.oas["components"]["schemas"] = schema_tree
        
        # Parameters (Global)
        if global_components.get("parameters") is not None:
            params = self._build_parameters(global_components["parameters"])
            for p in params:
                self.oas["components"]["parameters"][p["name"]] = p

        # Responses (Global)
        if global_components.get("responses") is not None:
             # Global responses are usually 1 row per response in the sheet?
             # Or multiple rows per response (complex)?
             # Assuming flattening like paths: group by Name
             df_resp = global_components["responses"]
             df_resp.columns = df_resp.columns.str.strip()
             
             # Group by 'Name'
             # resp_groups = df_resp.groupby(...) -> CRASHES
             
             current_name = None
             current_rows = []
             
             for idx, row in df_resp.iterrows():
                 name = self._get_name(row)
                 if pd.notna(name):
                     if current_name and current_name != name:
                         # Build previous
                         self.oas["components"]["responses"][str(current_name)] = self._build_single_response(pd.DataFrame(current_rows))
                         current_rows = []
                     current_name = name
                 
                 if current_name:
                     current_rows.append(row)
                     
             if current_name and current_rows:
                 self.oas["components"]["responses"][str(current_name)] = self._build_single_response(pd.DataFrame(current_rows))

        # Headers (Global)
        if global_components.get("headers") is not None:
             df_head = global_components["headers"]
             for idx, row in df_head.iterrows():
                 name = self._get_name(row)
                 if pd.notna(name):
                      schema = self._map_type_to_schema(row)
                      desc = schema.pop("description", None)
                      header_obj = {"schema": schema}
                      if desc: header_obj["description"] = desc
                      self.oas["components"]["headers"][str(name)] = header_obj
             
    def _build_schema_group(self, df):
        """
        Builds a dictionary of schema components from a single flat sheet containing multiple schemas.
        """
        nodes = {}
        roots = []
        df.columns = df.columns.str.strip()
        
        for idx, row in df.iterrows():
            name = self._get_name(row)
            if pd.isna(name): continue
            name = str(name).strip()
            
            # Parsing M for mandatory
            mand_raw = str(self._get_col_value(row, ["Mandatory", "Required"]) or "").strip().lower()
            is_mandatory = mand_raw in ["yes", "y", "true", "m"]

            node = {
                "name": name,
                "type": self._get_type(row),
                "description": self._get_description(row),
                "parent": self._get_parent(row),
                "mandatory": is_mandatory,
                "schema_obj": self._map_type_to_schema(row, is_node=True)
            }
            # Add title if Name is root?
            # If it's a root (no parent), usually schema name = title too?
            # Or description is used as title?
            # OAS schema 'title' property.
            
            nodes[name] = node

        # 2. Link
        for name, node in nodes.items():
            parent_name = node["parent"]
            if pd.isna(parent_name):
                roots.append(node)
                # Assign Title to Root if missing?
                if "title" not in node["schema_obj"]:
                    node["schema_obj"]["title"] = name
            elif str(parent_name).strip() in nodes:
                parent = nodes[str(parent_name).strip()]
                parent_schema = parent["schema_obj"]
                
                if parent_schema.get("type") == "array":
                    parent_schema["items"] = node["schema_obj"]
                else:
                    if "properties" not in parent_schema: parent_schema["properties"] = {}
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
        if "openapi" in self.oas: ordered_oas["openapi"] = self.oas["openapi"]
        
        # 2. Info
        if "info" in self.oas: ordered_oas["info"] = self.oas["info"]
        
        # 3. Servers
        if "servers" in self.oas: ordered_oas["servers"] = self.oas["servers"]
        
        # 4. Tags
        if "tags" in self.oas: ordered_oas["tags"] = self.oas["tags"]
        
        # 5. Paths
        if "paths" in self.oas: ordered_oas["paths"] = self.oas["paths"]
        
        # 6. Components
        if "components" in self.oas: ordered_oas["components"] = self.oas["components"]
        
        # 7. Security (Global)
        if "security" in self.oas: ordered_oas["security"] = self.oas["security"]
        
        # Add any other missing keys (e.g. externalDocs) at the end
        for k in self.oas:
            if k not in ordered_oas:
                ordered_oas[k] = self.oas[k]

        # Generate YAML
        yaml_output = yaml.dump(ordered_oas, Dumper=OASDumper, sort_keys=False, default_flow_style=False, allow_unicode=True, width=120)
        
        # Post-process: Replace __RAW_EXTENSIONS__ markers with actual raw YAML
        yaml_output = self._insert_raw_extensions(yaml_output, ordered_oas)
        
        return yaml_output
    
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
                    output_lines = yaml_text.split('\n')
                    new_output = []
                    i = 0
                    while i < len(output_lines):
                        line = output_lines[i]
                        if '__RAW_EXTENSIONS__:' in line:
                            # Excel text ALREADY has absolute indentation (6 spaces)
                            # Don't add marker_indent - just use text as-is
                            marker_indent = len(line) - len(line.lstrip())  # Still need for skipping
                            for raw_line in raw_text.split('\n'):
                                new_output.append(raw_line)  # Insert exactly as-is from Excel
                            
                            # Skip lines that are part of the __RAW_EXTENSIONS__ value
                            # (YAML will dump it as |- multiline or quoted)
                            i += 1
                            # Skip continuation lines (indented more than current)
                            while i < len(output_lines):
                                next_line = output_lines[i]
                                if next_line.strip() == '':
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
                    
                    yaml_text = '\n'.join(new_output)
        
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
