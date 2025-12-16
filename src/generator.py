import yaml
import pandas as pd
import json
import textwrap
import re
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
                if details.get("body") is not None:
                    req_body = self._build_request_body(details["body"], body_examples)
                    if req_body:
                        op_obj["requestBody"] = req_body

                # Responses
                if details.get("responses"):
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
            
            type_val = str(self._get_type(row)).lower().strip() if pd.notna(self._get_type(row)) else ""
            schema_name = self._get_schema_name(row)
            
            # If Type=parameter/parameters and Schema Name is present, create a reference
            if type_val in ['parameter', 'parameters'] and pd.notna(schema_name):
                # Check if there's a description
                desc = self._get_description(row)
                ref_path = f"#/components/parameters/{name}"
                
                if pd.notna(desc):
                    # Reference with description - use allOf workaround for OAS 3.0
                    is_oas30 = self.version.startswith("3.0")
                    if is_oas30:
                        param = {
                            "allOf": [{"$ref": ref_path}],
                            "description": str(desc)
                        }
                    else:
                        # OAS 3.1 allows $ref and description at same level
                        param = {
                            "$ref": ref_path,
                            "description": str(desc)
                        }
                else:
                    # Just the reference
                    param = {"$ref": ref_path}
                
                params.append(param)
                continue
            
            in_loc = self._get_col_value(row, ["In", "Location"])
            if pd.isna(in_loc): 
                 # Default to header for 'parameter' type if missing
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

    def _build_request_body(self, df, body_examples=None):
        if df is None or df.empty: return None
        
        # DEBUG
        # print(f"DEBUG BODY COLS: {df.columns.tolist()}")
        
        # The structure usually has the content-type as a root or row 0
        # Let's find the content type. 
        # Check if 'application/json' is in Name column
        content_type = "application/json" # Default
        
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
                    **({"examples": {
                        k: {"value": self._parse_example_string(v)} 
                        for k, v in body_examples.items()
                    }} if body_examples else {})
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
            "Schema Name\n(for Type or Items Data Type = 'schema' || 'header')",
            "Schema Name\n(if Type = schema)"
        ])

    def _get_type(self, row):
        return self._get_col_value(row, ["Type", "Data Type", "Item Type", "Type "]) 

    def _get_name(self, row):
        return self._get_col_value(row, ["Name", "Parameter Name", "Field Name", "Request Parameters", "Path", "Name.1"])

    def _get_parent(self, row):
        return self._get_col_value(row, ["Parent", "Parent Name"])

    def _get_description(self, row):
        return self._get_col_value(row, ["Description", "Desc", "Description "])

    def _parse_example_string(self, ex_str):
        """
        Parses a string as JSON or YAML.
        """
        if not ex_str: return None
        try:
             ex_str = str(ex_str).strip()
             if ex_str.startswith("{") or ex_str.startswith("["):
                  return json.loads(ex_str)
             else:
                  return yaml.safe_load(ex_str)
        except:
             return ex_str

    def _build_single_response(self, df, body_examples=None, code=""):
        if df is None or df.empty: return {"description": "Response"}
        
        # 1. Identify Root Info
        root_row = None
        header_rows = []
        content_rows = [] # Track content rows
        example_rows = [] # Track example definition rows
        schema_rows_mask = []
        example_names = set()  # Names that are examples, not schema properties
        
        # First pass: identify headers, content, and example markers
        for idx, row in df.iterrows():
             r_type = str(self._get_type(row)).strip().lower()
             section = self._get_col_value(row, ["Section"])
             section_lower = str(section).strip().lower() if pd.notna(section) else ""
             
             name = self._get_name(row)
             desc = self._get_description(row)
             parent = self._get_parent(row)
             
             if r_type == 'header' or section_lower == 'header' or section_lower == 'headers':
                 header_rows.append(row)
                 schema_rows_mask.append(False)
             elif section_lower == 'content':
                 content_rows.append(row)
                 schema_rows_mask.append(True) # Content rows act as roots for schema building
                 if root_row is None: root_row = row # Fallback if content is first
             elif section_lower in ['example', 'examples']:
                 example_rows.append(row)
                 example_name = self._get_name(row)
                 if pd.notna(example_name):
                     example_names.add(str(example_name).strip())
                 schema_rows_mask.append(False)
             else:
                 # Check if this row is a child/descendant of an example
                 if pd.notna(parent) and str(parent).strip() in example_names:
                     if pd.notna(name): example_names.add(str(name).strip())
                     if pd.notna(desc): example_names.add(str(desc).strip())
                     
                     example_rows.append(row) # Add child row to example rows
                     schema_rows_mask.append(False)
                 else:
                     schema_rows_mask.append(True)
                     if pd.isna(self._get_parent(row)) and root_row is None:
                         root_row = row

        if root_row is None: 
             # Fallback
             return {"description": "Response"}

        # Response description extraction (same as before)
        if hasattr(df, 'attrs') and 'response_description' in df.attrs:
             desc = df.attrs['response_description']
        elif len(df) > 0:
            first_row = df.iloc[0]
            desc = self._get_parent(first_row) or "Response"
        else:
            desc = "Response"
        
        type_val = str(self._get_type(root_row)).strip().lower()
        schema_ref = self._get_schema_name(root_row)

        # 2. Global Response Reference (Type == 'response')
        # ONLY if no headers and no explicit content
        is_pure_ref = (type_val == 'response' and pd.notna(schema_ref)) and (not header_rows) and (not content_rows)
        
        if is_pure_ref:
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
                        
                # (Fallback logic removed)
                
                # Build Examples from Section=example rows
                if example_rows:
                    built_examples = self._build_examples_from_rows(pd.DataFrame(example_rows))
                    if built_examples:
                        existing = resp_obj["content"][content_type].get("examples", {})
                        for k, v in built_examples.items():
                            existing[k] = {"value": v}
                        resp_obj["content"][content_type]["examples"] = existing
                

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

    def _build_examples_from_rows(self, df):
        """
        Constructs example objects from rows marked as Section='example'.
        Handles nesting and list indices (e.g. items[0]).
        """
        if df.empty: return {}
        
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
            if pd.isna(name): continue
            name = str(name).strip()
            
            # Value from Example column
            ex_val = self._get_col_value(row, ["Example", "Examples"])
            
            nodes[idx] = {
                "name": name,
                "parent": self._get_parent(row),
                "value": ex_val,
                "children": []
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
            if n not in name_to_nodes: name_to_nodes[n] = []
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
                    m = re.match(r'(.+)\[(\d+)\]$', str(parent_name).strip())
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
                    roots.append(node) # Parent not found, treat as root
        
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
                    if idx not in list_grouped: list_grouped[idx] = {}
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
                
                m = re.match(r'(.+)\[(\d+)\]$', c_name)
                if m:
                     base = m.group(1)
                     idx = int(m.group(2))
                     if base not in obj: obj[base] = []
                     while len(obj[base]) <= idx: obj[base].append(None)
                     # If we are assigning a value to index, we assume it's a scalar or object?
                     # Ideally we merge?
                     # For now, just assign.
                     obj[base][idx] = child_val
                else:
                     obj[c_name] = child_val
                     
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
            if pd.isna(name): continue
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
        
        
        # Don't treat Excel-specific types as valid OAS types
        # These should be handled as references (parameter, schema, header) or are not valid types
        invalid_types = ['parameter', 'parameters', 'schema', 'header', 'response']
        if type_val in invalid_types:
            # If we reach here with these types, it means Schema Name was empty
            # Default to string type as fallback
            type_val = 'string'
        
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
            schema["type"] = "array"
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
             df_resp = global_components["responses"]
             df_resp.columns = df_resp.columns.str.strip()
             
             # Convert to list of dicts for easier processing
             all_rows = df_resp.to_dict('records')
             
             # 1. Build Adjacency Map (Parent -> [Children])
             # And identify Roots
             adjacency = {}
             roots = []
             
             for row in all_rows:
                 name = str(self._get_name(row)).strip()
                 parent = self._get_parent(row)
                 # Handle NaN parent
                 parent_str = str(parent).strip() if pd.notna(parent) else ""
                 
                 # Check if Root
                 # Root criteria: Type='response' OR Parent is empty
                 type_val = str(self._get_type(row)).strip().lower()
                 if type_val == 'response' or parent_str == "":
                     roots.append(row)
                 else:
                     # It's a child
                     if parent_str not in adjacency:
                         adjacency[parent_str] = []
                     adjacency[parent_str].append(row)

             # 2. Process each Root
             for root in roots:
                 root_name = str(self._get_name(root)).strip()
                 if not root_name or root_name.lower() == 'nan': continue
                 
                 # Gather all descendants recursively
                 collected_rows = [root]
                 
                 def gather_descendants(current_name):
                     if current_name in adjacency:
                         children = adjacency[current_name]
                         for child in children:
                             collected_rows.append(child)
                             child_name = str(self._get_name(child)).strip()
                             # Recursion
                             if child_name and child_name != 'nan':
                                 gather_descendants(child_name)
                 
                 gather_descendants(root_name)
                 
                 # Build Response Object from collected rows
                 response_df = pd.DataFrame(collected_rows)
                 self.oas["components"]["responses"][str(root_name)] = self._build_single_response(response_df)

        # Headers (Global)
        if global_components.get("headers") is not None:
             df_head = global_components["headers"]
             for idx, row in df_head.iterrows():
                 name = self._get_name(row)
                 if pd.notna(name):
                      name = str(name).strip()
                      schema = self._map_type_to_schema(row)
                      
                      # Description management: Header description vs Schema description
                      # Usually Header description is for the header itself.
                      # Schema description is for the value.
                      # In this tool, they might be mixed.
                      # self._map_type_to_schema adds description to schema if present.
                      
                      # 1. Promote to Component Schema
                      # Check if schema already exists (from Schemas sheet)?
                      # If exists, we might overwrite or skip.
                      # If we overwrite, we ensure consistency with Header def.
                      # "Last Good" had it in both.
                      if name not in self.oas["components"]["schemas"]:
                          self.oas["components"]["schemas"][name] = schema.copy()
                      
                      # 2. Create Header Object referencing the Schema
                      header_desc = self._get_description(row)
                      header_obj = {
                          "schema": {"$ref": f"#/components/schemas/{name}"}
                      }
                      if header_desc:
                          header_obj["description"] = str(header_desc)
                          
                      self.oas["components"]["headers"][name] = header_obj
        if global_components.get("responses") is not None:
             # ... (existing response logic) ...
             pass
             
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
            print(f"\n[WARNING] Found {len(missing)} missing schemas. analyzing references...")
            full_msg = "The following schemas are referenced but missing from the source Excel files:\n"
            
            for m in missing:
                refs = self._find_references(m)
                ref_str = "\n    - ".join(refs[:5]) # Limit to 5 examples
                if len(refs) > 5: ref_str += f"\n    - ... and {len(refs)-5} more"
                if not refs: ref_str = " (No explicit references found in generated output, possibly implicit or lost)"
                
                full_msg += f"\n  * {m}:\n    - Referenced in: {ref_str}"
                
            print(full_msg)
            print(f"See generation_deficiencies.log for details.\n")
            self._log_deficiency(full_msg)

    def _build_schema_group(self, df):
        """
        Builds a dictionary of schema components from a single flat sheet containing multiple schemas.
        """
        nodes = {}
        node_map = {} # Map Name -> Node
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
