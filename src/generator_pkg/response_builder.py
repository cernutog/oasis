"""
Response Builder for OAS Generation.

Contains functions for building OAS response objects from DataFrame rows.
Functions receive necessary dependencies as parameters for decoupling.
"""

import re
import pandas as pd
from collections import OrderedDict

from .row_helpers import (
    get_col_value,
    get_type,
    get_name,
    get_parent,
    get_description,
    get_schema_name,
    parse_example_string,
)
from .schema_builder import map_type_to_schema


def build_response_tree(df, get_name_fn, get_parent_fn, get_col_value_fn):
    """
    Builds a tree structure from flat DataFrame rows using synthetic root.
    
    :param df: DataFrame with response data
    :param get_name_fn: Function to get name from row
    :param get_parent_fn: Function to get parent from row
    :param get_col_value_fn: Function to get column value from row
    :return: Root node dict with 'children' list
    """
    df.columns = df.columns.str.strip()
    nodes = {}
    last_seen = {}
    roots = [{"name": "Response", "children": [], "idx": -1, "row": None}]

    for idx, row in df.iterrows():
        name = str(get_name_fn(row)).strip()
        parent = get_parent_fn(row)
        parent_str = str(parent).strip() if pd.notna(parent) else ""
        section = str(get_col_value_fn(row, ["Section"])).strip().lower()

        node = {"row": row, "children": [], "idx": idx, "name": name}
        nodes[idx] = node

        # Linking Logic
        # Headers always go to root (they're top-level response properties)
        # Content nodes without parent go to root (they're media types)
        # Content nodes WITH parent should be linked to their parent (they're schema properties)
        if section in ["header", "headers"]:
            roots[0]["children"].append(node)
        elif section == "content" and not parent_str:
            # Media type node (no parent) - add to root
            roots[0]["children"].append(node)
        else:
            # Has a parent or non-header/content section - link to parent
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


def extract_response_description(df, root_node, get_description_fn, get_parent_fn):
    """
    Extracts response description with priority:
    1. df.attrs['response_description']
    2. Description column
    3. Parent column (fallback)
    
    :return: Description string
    """
    desc = None
    if hasattr(df, "attrs") and "response_description" in df.attrs:
        desc = df.attrs["response_description"]

    if pd.isna(desc) or not str(desc).strip():
        if root_node["row"] is not None:
            desc = get_description_fn(root_node["row"])

    if pd.isna(desc) or not str(desc).strip():
        if root_node["row"] is not None:
            desc = get_parent_fn(root_node["row"])

    return str(desc).strip() if pd.notna(desc) else "Response"


def flatten_subtree(nodes):
    """Helper to collect all descendant rows from a list of nodes."""
    rows = []
    for n in nodes:
        rows.append(n)
        rows.extend(flatten_subtree(n["children"]))
    return rows


def build_schema_from_flat_table(df, version: str):
    """
    Reconstructs a nested schema from flat parent/child rows.
    
    :param df: DataFrame with schema data
    :param version: OAS version string
    :return: OAS schema dict
    """
    df.columns = df.columns.str.strip()

    nodes = {}
    roots = []

    for idx, row in df.iterrows():
        name = get_name(row)
        if pd.isna(name):
            continue
        name = str(name).strip()

        node = {
            "name": name,
            "type": get_type(row),
            "description": get_description(row),
            "parent": get_parent(row),
            "mandatory": str(
                get_col_value(row, ["Mandatory", "Required"]) or ""
            ).lower()
            in ["yes", "y", "true", "m"],
            "schema_obj": map_type_to_schema(row, version, is_node=True),
        }

        nodes[name] = node

    # Build Tree
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
                        # Overwrite items
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
                # Parent not in nodes. Treat as Root.
                roots.append(node)

    # Re-order 'example' and 'examples' to be the LAST keys
    for name, node in nodes.items():
        schema = node["schema_obj"]

        ex = schema.pop("example", None)
        exs = schema.pop("examples", None)

        new_schema = OrderedDict()
        for k, v in schema.items():
            new_schema[k] = v

        if ex is not None:
            new_schema["example"] = ex
        if exs is not None:
            new_schema["examples"] = exs

        schema.clear()
        schema.update(new_schema)

    # Return the Root Schema
    if len(roots) == 1:
        return roots[0]["schema_obj"]
    elif len(roots) > 1:
        return {
            "type": "object",
            "properties": {r["name"]: r["schema_obj"] for r in roots},
        }
    else:
        return {}


def build_examples_from_rows(df):
    """
    Constructs example objects from rows marked as Section='example'.
    Handles nesting and list indices (e.g. items[0]).
    
    :param df: DataFrame with example data
    :return: dict of example objects
    """
    if df.empty:
        return {}

    df = df.copy()
    df.columns = df.columns.str.strip()
    nodes = {}
    
    for idx, row in df.iterrows():
        name = get_name(row)
        if pd.isna(name):
            continue
        name = str(name).strip()

        ex_val = get_col_value(row, ["Example", "Examples"])

        nodes[idx] = {
            "name": name,
            "parent": get_parent(row),
            "type": get_type(row),
            "value": ex_val,
            "children": [],
        }

    # Build IDs map
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
            p_nodes = name_to_nodes.get(str(parent_name).strip())

            if not p_nodes:
                m = re.match(r"(.+)\[(\d+)\]$", str(parent_name).strip())
                if m:
                    base = m.group(1)
                    arr_idx = int(m.group(2))
                    p_nodes = name_to_nodes.get(base)
                    if p_nodes:
                        node["array_index"] = arr_idx

            if p_nodes:
                p_nodes[0]["children"].append(node)
            else:
                roots.append(node)

    def build_node(node):
        if not node["children"]:
            val = node["value"]
            node_type = str(node.get("type", "")).strip().lower() if pd.notna(node.get("type")) else ""
            if pd.notna(val):
                return parse_example_string(val)
            else:
                # For string types, return empty string instead of None
                # This handles 204 No Content responses with value: '' 
                return "" if node_type == "string" else None

        list_grouped = {}
        has_indexed_children = False

        for child in node["children"]:
            if "array_index" in child:
                has_indexed_children = True
                arr_idx = child["array_index"]
                if arr_idx not in list_grouped:
                    list_grouped[arr_idx] = {}
                list_grouped[arr_idx][child["name"]] = build_node(child)

        if has_indexed_children:
            max_idx = max(list_grouped.keys()) if list_grouped else -1
            result_list = [None] * (max_idx + 1)
            for arr_idx, obj in list_grouped.items():
                result_list[arr_idx] = obj
            return result_list

        obj = {}
        for child in node["children"]:
            child_val = build_node(child)
            c_name = child["name"]

            m = re.match(r"(.+)\[(\d+)\]$", c_name)
            if m:
                base = m.group(1)
                arr_idx = int(m.group(2))
                if base not in obj:
                    obj[base] = []
                while len(obj[base]) <= arr_idx:
                    obj[base].append(None)
                obj[base][arr_idx] = child_val
            else:
                obj[c_name] = child_val

        if str(node.get("type", "")).strip().lower() == "array":
            return [obj]

        return obj

    final_examples = {}
    for root in roots:
        final_examples[root["name"]] = build_node(root)

    return final_examples


def process_response_headers(header_nodes, headers_components: dict, version: str):
    """
    Processes header nodes into OAS headers dict.
    
    :param header_nodes: List of header node dicts
    :param headers_components: The components/headers dict from OAS
    :param version: OAS version string
    :return: Headers dict or None
    """
    if not header_nodes:
        return None

    headers = {}
    for h_node in header_nodes:
        row = h_node["row"]
        h_name = h_node["name"]
        schema_ref = get_schema_name(row)

        if pd.notna(schema_ref):
            schema_ref = str(schema_ref).strip()
            if schema_ref in headers_components:
                headers[h_name] = {"$ref": f"#/components/headers/{schema_ref}"}
            else:
                headers[h_name] = {
                    "schema": {"$ref": f"#/components/schemas/{schema_ref}"},
                    "description": get_description(row) or "",
                }
        else:
            h_schema = map_type_to_schema(row, version)
            h_desc = h_schema.pop("description", None)
            head_obj = {"schema": h_schema}
            if h_desc:
                head_obj["description"] = h_desc
            headers[h_name] = head_obj

    return headers


def coerce_example_types(value, schema, components_schemas=None):
    """
    Recursively coerce example value types to match schema expectations.
    
    When schema type is 'string' but value is a number, converts to quoted string.
    This ensures proper YAML serialization while respecting the schema.
    
    Args:
        value: The example value to check
        schema: The schema definition for this value
        components_schemas: Dict of component schemas for $ref resolution
        
    Returns:
        Coerced value with proper types
    """
    if schema is None or not isinstance(schema, dict):
        return value
    
    # Resolve $ref if present (direct $ref)
    if '$ref' in schema and components_schemas:
        ref_path = schema['$ref']
        if ref_path.startswith('#/components/schemas/'):
            ref_name = ref_path.split('/')[-1]
            schema = components_schemas.get(ref_name, {})
    
    # For allOf with single $ref + description (common pattern), follow the $ref
    # to get schema info, but DON'T modify the original schema structure
    effective_schema = schema
    if 'allOf' in schema and components_schemas:
        for sub_schema in schema['allOf']:
            if isinstance(sub_schema, dict) and '$ref' in sub_schema:
                ref_path = sub_schema['$ref']
                if ref_path.startswith('#/components/schemas/'):
                    ref_name = ref_path.split('/')[-1]
                    resolved = components_schemas.get(ref_name, {})
                    # Use resolved schema for type checking only, don't modify original
                    effective_schema = resolved
                    break
    
    schema_type = effective_schema.get('type')
    
    # Handle object: recurse into properties
    if isinstance(value, dict):
        properties = effective_schema.get('properties', {})
        # Also check allOf/anyOf/oneOf for properties in effective_schema
        for combinator in ['allOf', 'anyOf', 'oneOf']:
            if combinator in effective_schema:
                for sub_schema in effective_schema[combinator]:
                    if isinstance(sub_schema, dict):
                        properties.update(sub_schema.get('properties', {}))
        
        result = {}
        for k, v in value.items():
            prop_schema = properties.get(k, {})
            result[k] = coerce_example_types(v, prop_schema, components_schemas)
        return result
    
    # Handle array: recurse into items
    if isinstance(value, list):
        items_schema = effective_schema.get('items', {})
        return [coerce_example_types(item, items_schema, components_schemas) for item in value]
    
    # Handle scalar: coerce numeric to string if schema expects string  
    if schema_type == 'string' and isinstance(value, (int, float)):
        # Convert number to string - YAML dumper will add appropriate quotes
        return str(value)
    
    return value

def process_response_content(content_nodes, schema_nodes, root_node, version: str, components_schemas=None):
    """
    Processes content nodes (explicit) or schema nodes (implicit) into OAS content dict.
    
    :param content_nodes: List of content node dicts
    :param schema_nodes: List of schema node dicts
    :param root_node: Root node dict
    :param version: OAS version string
    :param components_schemas: Dict of component schemas for $ref resolution
    :return: Content dict or None
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
                    str(get_col_value(grand["row"], ["Section"]))
                    .strip()
                    .lower()
                )
                if sec in ["example", "examples"]:
                    c_example_nodes.append(grand)
                else:
                    c_schema_nodes.append(grand)

            # Build schema
            all_schema_rows = [c_node["row"]] + [
                n["row"] for n in flatten_subtree(c_schema_nodes)
            ]
            c_schema_df = pd.DataFrame(all_schema_rows)

            if not c_schema_df.empty:
                schema = build_schema_from_flat_table(c_schema_df, version)
            else:
                schema = {}

            # Build examples
            examples = {}
            if c_example_nodes:
                ex_df = pd.DataFrame(
                    [n["row"] for n in flatten_subtree(c_example_nodes)]
                )
                examples = build_examples_from_rows(ex_df)

            # Suppress schema for empty objects if no attributes
            c_type = str(get_type(c_node["row"])).strip().lower()
            has_attributes = len(c_schema_nodes) > 0

            if c_type == "object" and not has_attributes:
                content_entry = {}
            else:
                content_entry = {"schema": schema}

            if examples:
                content_entry["examples"] = {}
                for k, v in examples.items():
                    # Coerce example types based on schema
                    coerced_v = coerce_example_types(v, schema, components_schemas)
                    if isinstance(coerced_v, dict) and "value" in coerced_v:
                        content_entry["examples"][k] = coerced_v
                    else:
                        content_entry["examples"][k] = {"value": coerced_v}

            content[content_type] = content_entry

        return content

    elif schema_nodes:
        # Implicit content (legacy)
        default_ct = "application/json"
        if "/" in root_node["name"]:
            default_ct = root_node["name"]

        schema_df = pd.DataFrame(
            [n["row"] for n in flatten_subtree(schema_nodes)]
        )
        schema = build_schema_from_flat_table(schema_df, version)

        return {default_ct: {"schema": schema}}

    return None
