import yaml
import pandas as pd
import json

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

            # Merge Custom Extensions (YAML format)
            extensions_yaml = op_meta.get("extensions")
            if extensions_yaml and isinstance(extensions_yaml, str) and extensions_yaml.strip():
                try:
                    # Clean up YAML: sometimes indentation is messed up in Excel cells
                    # Simple heuristic: remove leading whitespace from first line, 
                    # and adjust subsequent lines? Or just trust safe_load
                    
                    # Problem seen: "x-sandbox-rule-type: ...\n      x-sandbox-rule-content: |"
                    # The second line has 6 spaces, first has 0. This is valid YAML if it's top level?
                    # No, top level map keys must be same indent.
                    
                    # Normalize indentation
                    lines = extensions_yaml.split('\n')
                    if lines:
                        # Strip common leading whitespace?
                        # Or just replace the weird large spacing on line 2+
                        pass

                    ext_dict = yaml.safe_load(extensions_yaml)
                    if isinstance(ext_dict, dict):
                        op_obj.update(ext_dict)
                except Exception as e:
                    print(f"Error parsing custom extensions for {op_meta.get('operationId')}: {e}")

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
                    for code, df_resp in details["responses"].items():
                        op_obj["responses"][str(code)] = self._build_single_response(df_resp)
            
            # Fallback for empty responses
            if not op_obj["responses"]:
                op_obj["responses"]["default"] = {"description": "Default response"}

            self.oas["paths"][path_url][method] = op_obj

    def _build_parameters(self, df):
        params = []
        if df is None: return params
        
        for _, row in df.iterrows():
            name = self._get_name(row)
            if pd.isna(name): continue
            
            in_loc = self._get_col_value(row, ["In", "Location"])
            if pd.isna(in_loc): 
                 # Try to infer or default? Usually 'query' or 'header'
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

    def _build_single_response(self, df):
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
            resp_obj["headers"] = headers

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
            if pd.isna(parent_name):
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
        if pd.notna(ex): schema["example"] = ex
        
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
             # Global responses are slightly different? Usually definitions.
             # Need to see structure. Assuming similar flat table.
             # If "Name" column gives the component name.
             pass # Logic to be refined if needed, using generic builder
             
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

    def get_yaml(self):
        return yaml.dump(self.oas, sort_keys=False, allow_unicode=True)
