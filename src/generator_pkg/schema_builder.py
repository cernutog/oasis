"""
Schema Builder for OAS Generation.

Contains functions for building OAS schema objects from Excel row data.
All functions receive version as parameter for OAS 3.0/3.1 differences.
"""

import pandas as pd
from collections import OrderedDict

from .row_helpers import (
    get_col_value,
    get_type,
    get_name,
    get_parent,
    get_schema_name,
    get_description,
    get_title,
    parse_example_string,
    coerce_example_types,
)


def handle_combinator_refs(type_val: str, schema_ref: str, desc=None) -> dict | None:
    """
    Handles oneOf/allOf/anyOf combinators with schema references.
    
    :param type_val: Type value (lower case)
    :param schema_ref: Schema reference string (comma-separated for multiple)
    :param desc: Optional description
    :return: Complete schema dict or None if not a combinator
    """
    if type_val not in ["oneof", "allof", "anyof"]:
        return None

    refs = [r.strip() for r in str(schema_ref).split(",")]
    combinator_key = {"oneof": "oneOf", "allof": "allOf", "anyof": "anyOf"}.get(type_val)

    schema = {
        combinator_key: [{"$ref": f"#/components/schemas/{r}"} for r in refs if r]
    }

    if pd.notna(desc):
        schema["description"] = str(desc)

    return schema


def handle_schema_reference(type_val: str, schema_ref: str, desc, version: str) -> dict:
    """
    Handles $ref with OAS 3.0 workaround for description.
    
    :param type_val: Type value
    :param schema_ref: Schema name to reference
    :param desc: Description
    :param version: OAS version string
    :return: Schema dict with appropriate ref structure
    """
    ref_path = f"#/components/schemas/{schema_ref}"

    if type_val == "array":
        is_oas30 = version.startswith("3.0")
        if pd.notna(desc) and is_oas30:
            # OAS 3.0: items cannot have siblings with $ref. Wrap in allOf.
            items = {"allOf": [{"$ref": ref_path}], "description": str(desc)}
        else:
            items = {"$ref": ref_path}
            if pd.notna(desc):
                items["description"] = str(desc)
        return {"type": "array", "items": items}

    # OAS 3.0 Workaround: $ref + description requires allOf wrapper
    # OAS 3.1: $ref + description can coexist as siblings
    has_desc = pd.notna(desc)
    is_oas30 = version.startswith("3.0")

    if has_desc:
        if is_oas30:
            # OAS 3.0: use allOf workaround
            return {"allOf": [{"$ref": ref_path}], "description": str(desc)}
        else:
            # OAS 3.1: description as sibling of $ref
            return {"$ref": ref_path, "description": str(desc)}
    else:
        return {"$ref": ref_path}


def apply_schema_constraints(schema: dict, row, type_val: str) -> None:
    """
    Applies enums, format, pattern, and min/max constraints to schema.
    Modifies schema dict in-place.
    
    :param schema: Schema dict to modify
    :param row: DataFrame row
    :param type_val: Type value
    """
    # Enums
    enum_val = get_col_value(row, ["Allowed value", "Allowed values"])
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
    fmt = get_col_value(row, ["Format"])
    if pd.notna(fmt):
        schema["format"] = str(fmt)

    pattern = get_col_value(row, ["PatternEba", "Pattern", "Regex"])
    if pd.notna(pattern):
        schema["pattern"] = str(pattern)

    # Min/Max constraints
    min_val = get_col_value(
        row,
        [
            "Min\nValue/Length/Item",
            "Min  \nValue/Length/Item",
            "Min Value/Length/Item",
            "Min",
        ],
    )
    max_val = get_col_value(
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
            # Use RawNumericValue for perfect fidelity: Excel string → YAML as-is
            from .yaml_output import RawNumericValue
            str_val = str(min_val).strip()
            
            if type_val == "string":
                schema["minLength"] = int(float(str_val))
            elif type_val in ["integer", "number"]:
                schema["minimum"] = RawNumericValue(str_val)
            elif type_val == "array":
                schema["minItems"] = int(float(str_val))
        except (ValueError, TypeError):
            pass

    if pd.notna(max_val):
        try:
            # Use RawNumericValue for perfect fidelity: Excel string → YAML as-is
            from .yaml_output import RawNumericValue
            str_val = str(max_val).strip()
            
            if type_val == "string":
                schema["maxLength"] = int(float(str_val))
            elif type_val in ["integer", "number"]:
                schema["maximum"] = RawNumericValue(str_val)
            elif type_val == "array":
                schema["maxItems"] = int(float(str_val))
        except (ValueError, TypeError):
            pass


def map_type_to_schema(row, version: str, is_node: bool = False, components_schemas: dict = None) -> dict:
    """
    Maps Excel row data to an OAS schema object.
    
    :param row: DataFrame row
    :param version: OAS version string
    :param is_node: Whether this is a node (affects some processing)
    :return: OAS schema dict
    """
    type_val = get_type(row)
    if pd.isna(type_val):
        type_val = "string"
    type_val = str(type_val).strip().lower()

    schema = {}
    schema_ref = get_schema_name(row)
    desc = get_description(row)
    title = get_title(row)

    # Handle standard $ref
    if pd.notna(schema_ref):
        combinator_schema = handle_combinator_refs(type_val, schema_ref, desc)
        if combinator_schema:
            return combinator_schema

        ref_schema = handle_schema_reference(type_val, schema_ref, desc, version)
        schema.update(ref_schema)

    # Filter out Excel-specific type keywords
    invalid_types = ["parameter", "parameters", "schema", "header", "response"]
    if type_val in invalid_types:
        type_val = "string"  # Fallback to string

    # Set base type if not already set by ref handling
    has_ref_in_items = isinstance(schema.get("items"), dict) and "$ref" in schema["items"]
    if type_val != "array" and "$ref" not in schema and "allOf" not in schema:
        schema["type"] = type_val
    elif type_val == "array" and "items" not in schema:
        schema["type"] = type_val

    # Add title and description
    if pd.notna(title):
        schema["title"] = str(title)
    
    if pd.notna(desc):
        # Special case for arrays: if desc is already in items, don't duplicate it at top level
        should_add_top_desc = True
        if type_val == "array" and has_ref_in_items:
             # If we put it in items, don't put it here too
             should_add_top_desc = False
        
        if should_add_top_desc and "description" not in schema:
            schema["description"] = str(desc)

    # FINAL DEDUPLICATION: If Title and Description are identical, keep only Description
    if "title" in schema and "description" in schema:
        if str(schema["title"]).strip() == str(schema["description"]).strip():
            del schema["title"]
    elif "title" in schema and "description" not in schema:
        # If we promoted description to title, but user wants it as description if identical...
        # Wait, if only title is present (e.g. from promotion), keep it as title for containers.
        pass

    # Apply constraints (enum, format, pattern, min/max)
    apply_schema_constraints(schema, row, type_val)

    # Handle array-specific logic
    if type_val == "array":
        schema["type"] = "array"
        item_type_raw = get_col_value(
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
                combinator_schema = handle_combinator_refs(item_type, schema_ref)
                if combinator_schema:
                    schema["items"] = combinator_schema
            elif not has_ref_in_items:
                # Set primitive type or reference (only if items not already set by ref)
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
                        items_obj = {"$ref": f"#/components/schemas/{ref_name}"}
                        if pd.notna(desc):
                            items_obj["description"] = str(desc)
                        schema["items"] = items_obj
        elif "items" not in schema:
            schema["items"] = {}

    # Add examples (at the end for YAML formatting)
    # Both OAS 3.0 and 3.1 support examples at schema level
    # OAS 3.1 uses `examples` array, OAS 3.0 uses singular `example`
    ex = get_col_value(row, ["Example", "Examples"])
    if pd.notna(ex) and str(ex).strip():
        import io
        import csv
        # Use csv.reader to handle quoted commas and skipinitialspace for the comma+space separator
        f = io.StringIO(str(ex).strip())
        reader = csv.reader(f, skipinitialspace=True)
        try:
            raw_parts = next(reader)
        except (StopIteration, csv.Error):
            raw_parts = []
            
        parsed_examples = []
        for part in raw_parts:
            if part is None or (isinstance(part, str) and not part.strip() and not part == ""):
                continue
            parsed_ex = parse_example_string(part)
            # Apply coercion if possible (for primitives and arrays)
            parsed_ex = coerce_example_types(parsed_ex, schema, components_schemas)
            parsed_examples.append(parsed_ex)
            
        if parsed_examples:
            if version.startswith("3.1"):
                schema["examples"] = parsed_examples
            else:
                # OAS 3.0: use singular example, take the first one
                schema["example"] = parsed_examples[0]

    return schema
