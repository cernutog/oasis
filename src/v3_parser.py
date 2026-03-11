
import pandas as pd
import os
from typing import List, Dict, Optional, Any
from .v3_models import (
    LegacyIntermediateRepresentation,
    OperationNode,
    RawNode,
    SourceLineage
)

class V3Parser:
    def __init__(self, legacy_dir: str):
        self.legacy_dir = legacy_dir
        self.ir = LegacyIntermediateRepresentation()

    def parse_all(self) -> LegacyIntermediateRepresentation:
        """End-to-end extraction from all legacy files."""
        # 1. Parse Index to find operations
        index_path = os.path.join(self.legacy_dir, "$index.xlsm")
        if not os.path.exists(index_path):
            # Try .xlsx
            index_path = os.path.join(self.legacy_dir, "$index.xlsx")
            
        if os.path.exists(index_path):
            self._parse_index(index_path)
            
        # 2. Parse individual operation files
        self._parse_operations()
        
        return self.ir

    def _parse_index(self, path: str):
        df = pd.read_excel(path, "Paths", dtype=str)
        # Identify columns (assuming standard V2/V3 layout)
        file_col = df.columns[0]
        path_col = df.columns[1]
        method_col = "Method" if "Method" in df.columns else df.columns[3]
        
        for _, row in df.iterrows():
            p_val = row.get(path_col)
            if not isinstance(p_val, str) or not p_val.startswith("/"):
                continue
                
            op_id = row.get("OperationId") or row.get("Unnamed: 7")
            if not op_id: continue
            
            self.ir.operations[op_id] = OperationNode(
                operation_id=op_id,
                method=row.get(method_col, "GET"),
                path=p_val,
                summary=row.get("Summary", ""),
                description=row.get("Description", ""),
                tags=[row.get("Tag", "")]
            )

    def _parse_operations(self):
        files_in_dir = os.listdir(self.legacy_dir)
        for op_id, op_node in self.ir.operations.items():
            # Find the file matching this operation
            # Standard: operationId.xlsx
            filename = f"{op_id}.xlsm"
            file_path = os.path.join(self.legacy_dir, filename)
            
            if not os.path.exists(file_path):
                # Fallback to search-by-prefix if exact match fails
                matches = [f for f in files_in_dir if f.startswith(op_id) and (f.endswith(".xlsm") or f.endswith(".xlsx"))]
                if matches:
                    file_path = os.path.join(self.legacy_dir, matches[0])
                    filename = matches[0]
                else:
                    continue
            
            print(f"Parsing operation: {op_id} from {filename}")
            try:
                xl = pd.ExcelFile(file_path)
                # We extract specific sheets: Body, Header, Path, Data Type, and Status Codes
                for sheet in xl.sheet_names:
                    if sheet in ["Body", "Header", "Path", "Data Type"] or sheet.isdigit():
                        roots = self._parse_sheet(xl, sheet, filename)
                        if sheet == "Data Type":
                            # Register as global domain concepts
                            for r in roots:
                                self.ir.domain_concepts[r.name] = r
                        else:
                            op_node.sheets[sheet] = roots
            except Exception as e:
                print(f"Error parsing {filename}: {e}")

    def _parse_sheet(self, xl: pd.ExcelFile, sheet_name: str, filename: str) -> List[RawNode]:
        """Extracts the Raw Forest from a specific operation sheet."""
        df = pd.read_excel(xl, sheet_name, dtype=str)
        
        # 1. Identify Headers
        col_map = {
            "name": -1, "parent": -1, "type": -1, "mandatory": -1, 
            "description": -1, "items_type": -1, "extensions": -1,
            "format": -1, "min": -1, "max": -1, "pattern_eba": -1, 
            "regex": -1, "allowed": -1, "example": -1, "constraint": -1
        }
        
        header_row_idx = 0
        for i, row in df.iterrows():
            row_vals = [str(v).lower().strip() for v in row.values]
            if ("name" in row_vals or "element" in row_vals) and ("type" in row_vals or "data type" in row_vals):
                header_row_idx = i
                for idx, val in enumerate(row_vals):
                    if val == "name" or val == "element": col_map["name"] = idx
                    elif "parent" in val: col_map["parent"] = idx
                    elif val == "type" or val == "data type" or val == "data type info": 
                        if col_map["type"] == -1: col_map["type"] = idx
                    elif "items data type" in val: col_map["items_type"] = idx
                    elif "mandatory" in val: col_map["mandatory"] = idx
                    elif "description" in val: col_map["description"] = idx
                    elif "custom" in val or "extension" in val: col_map["extensions"] = idx
                    elif "format" == val: col_map["format"] = idx
                    elif "min" in val: col_map["min"] = idx
                    elif "max" in val: col_map["max"] = idx
                    elif "patterneba" in val.replace(" ", ""): col_map["pattern_eba"] = idx
                    elif "regex" == val: col_map["regex"] = idx
                    elif "allowed" in val: col_map["allowed"] = idx
                    elif "example" == val: col_map["example"] = idx
                    elif "constraint" == val: col_map["constraint"] = idx
                break
        
        # 2. Extract Rows
        roots = []
        name_to_node = {}
        
        for i in range(header_row_idx + 1, len(df)):
            row = df.iloc[i]
            
            # DEBUG INJECTION
            if "listAlerts" in filename and ("Data Type" in sheet_name or "Body" in sheet_name):
                d_name = str(row.iloc[col_map["name"]]).strip() if col_map["name"] != -1 else ""
                d_parent = str(row.iloc[col_map["parent"]]).strip() if col_map["parent"] != -1 else ""
                d_item = str(row.iloc[col_map["items_type"]]).strip() if col_map["items_type"] != -1 else "n/a"
                d_type = str(row.iloc[col_map["type"]]).strip() if col_map["type"] != -1 else "n/a"
                print(f"DEBUG PARSER: Row {i}: Name='{d_name}', Parent='{d_parent}', Type='{d_type}', ItemType='{d_item}'")

            name = str(row.iloc[col_map["name"]]).strip() if col_map["name"] != -1 else ""
            if not name or name.lower() == "nan": continue
            
            parent_name = str(row.iloc[col_map["parent"]]).strip() if col_map["parent"] != -1 else None
            if parent_name and parent_name.lower() == "nan": parent_name = None
            
            type_lit = str(row.iloc[col_map["type"]]).strip() if col_map["type"] != -1 else "string"
            items_type = str(row.iloc[col_map["items_type"]]).strip() if col_map["items_type"] != -1 else None
            mandatory = str(row.iloc[col_map["mandatory"]]).lower().strip() in ["m", "yes", "true", "y"] if col_map["mandatory"] != -1 else False
            desc = str(row.iloc[col_map["description"]]).strip() if col_map["description"] != -1 else ""
            ext = str(row.iloc[col_map["extensions"]]).strip() if col_map["extensions"] != -1 else None
            
            lineage = SourceLineage(file=filename, sheet=sheet_name, row=i+1)
            
            node = RawNode(
                name=name,
                parent_name=parent_name,
                type_literal=type_lit if type_lit.lower() != "nan" else "object",
                mandatory=mandatory,
                description=desc if desc.lower() != "nan" else "",
                items_type_literal=items_type if items_type and items_type.lower() != "nan" else None,
                custom_extensions=ext if ext and ext.lower() != "nan" else None,
                lineage=lineage
            )
            
            # Extract Meta-Fields from columns
            if col_map["format"] != -1: node.format = self._clean_val(row.iloc[col_map["format"]])
            if col_map["min"] != -1: node.min_val = self._clean_val(row.iloc[col_map["min"]])
            if col_map["max"] != -1: node.max_val = self._clean_val(row.iloc[col_map["max"]])
            if col_map["pattern_eba"] != -1: node.pattern_eba = self._clean_val(row.iloc[col_map["pattern_eba"]])
            if col_map["regex"] != -1: node.regex = self._clean_val(row.iloc[col_map["regex"]])
            if col_map["allowed"] != -1: node.allowed_values = self._clean_val(row.iloc[col_map["allowed"]])
            if col_map["example"] != -1: node.example = self._clean_val(row.iloc[col_map["example"]])
            
            # Extract Meta-Fields from combined "Constraint" string
            if col_map["constraint"] != -1:
                const_str = self._clean_val(row.iloc[col_map["constraint"]])
                if const_str:
                    self._merge_constraints(node, const_str)

            # 3. Assemble Forest
            if not parent_name:
                roots.append(node)
            else:
                # Robust case-insensitive parent lookup
                parent_node = name_to_node.get(parent_name.lower())
                if parent_node:
                    parent_node.children.append(node)
                else:
                    # Fallback: Treat as root but log warning? For now safe fallback.
                   # If parent really exists but wasn't found (e.g. defined AFTER child?), 
                   # standard parser assumes definition order top-down for now or we need 2-pass.
                   # Assuming top-down is standard for Excel parser.
                    roots.append(node) 

            name_to_node[node.name.lower()] = node
            
        return roots

    def _clean_val(self, val: Any) -> Optional[str]:
        if pd.isna(val): return None
        s = str(val).strip()
        return s if s.lower() != "nan" and s != "" else None

    def _merge_constraints(self, node: RawNode, const_str: str):
        """Parses strings like 'Type: string\nAllowed values: A,B' into node fields."""
        lines = const_str.split('\n')
        for line in lines:
            line = line.strip()
            if not line: continue
            
            if ':' in line:
                key, val = [p.strip() for p in line.split(':', 1)]
                key = key.lower()
                
                if "allowed" in key: node.allowed_values = val
                elif "pattern" in key or "regex" in key: node.regex = val
                elif "min" in key and "length" in key: node.min_val = val
                elif "max" in key and "length" in key: node.max_val = val
                elif "format" in key: node.format = val
                elif "type" in key: 
                    # If type_literal is object/nan, update it, otherwise keep extracted
                    if node.type_literal.lower() in ["nan", "object", "string"] and val.lower() not in ["object", "array"]:
                        node.type_literal = val
                elif "items" in key: node.items_type_literal = val
