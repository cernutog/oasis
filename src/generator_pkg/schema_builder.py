"""
Schema Builder for OAS Generation.

Contains functions for building OAS schema objects from Excel row data.
All functions receive version as parameter for OAS 3.0/3.1 differences.
"""

import re

import pandas as pd
from collections import OrderedDict

from .yaml_output import RawNumericValue, QuotedString

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

    if desc and str(desc).strip():
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
        return {"type": "array", "items": {"$ref": ref_path}}

    # OAS 3.0 Workaround: $ref + description requires allOf wrapper
    # OAS 3.1: $ref + description can coexist as siblings
    # NOTE: Pandas may pass NaN (float) for empty cells; str(NaN) == 'nan' must be treated as empty.
    has_desc = pd.notna(desc) and bool(str(desc).strip()) and str(desc).strip().lower() != "nan"
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


def collapse_allof_ref_if_redundant(schema: dict) -> dict:
    """Collapse {'allOf': [{'$ref': ...}]} into {'$ref': ...} when no other siblings exist.

    This is used when upstream logic applied the OAS 3.0 '$ref + description' workaround
    (allOf wrapper) but the description is later moved to a parent object (e.g. Parameter
    or Header). In that case, keeping the allOf wrapper is unnecessary noise.
    """
    if not isinstance(schema, dict):
        return schema
    if "allOf" not in schema:
        return schema
    if any(k for k in schema.keys() if k not in ("allOf",)):
        return schema
    all_of = schema.get("allOf")
    if not isinstance(all_of, list) or len(all_of) != 1:
        return schema
    first = all_of[0]
    if not isinstance(first, dict) or set(first.keys()) != {"$ref"}:
        return schema
    return {"$ref": first["$ref"]}


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

        elif type_val == "string":
            # If the schema expects a string but the enum token looks numeric,
            # force quoting to avoid YAML type inference / octal-like artifacts.
            out = []
            for x in enum_list:
                if not x:
                    continue
                if re.fullmatch(r"[+-]?\d+(?:\.\d+)?", x.strip()):
                    out.append(QuotedString(x.strip()))
                else:
                    out.append(x)
            enum_list = out

        schema["enum"] = enum_list

    # Format and Pattern
    fmt = get_col_value(row, ["Format"])
    if pd.notna(fmt):
        schema["format"] = str(fmt)

    pattern = get_col_value(row, ["Regex", "Pattern", "PatternEba"])
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
        raw = str(min_val).strip()
        if raw:
            if type_val == "string":
                # Must be an integer in OAS; emit as raw numeric scalar.
                schema["minLength"] = RawNumericValue(raw.split(",")[0].split(".")[0])
            elif type_val in ["integer", "number"]:
                # Preserve original as-is, but emit a YAML-valid numeric scalar.
                norm = raw.replace(",", ".")
                schema["minimum"] = RawNumericValue(norm)
            elif type_val == "array":
                schema["minItems"] = RawNumericValue(raw.split(",")[0].split(".")[0])

    if pd.notna(max_val):
        raw = str(max_val).strip()
        if raw:
            if type_val == "string":
                schema["maxLength"] = RawNumericValue(raw.split(",")[0].split(".")[0])
            elif type_val in ["integer", "number"]:
                norm = raw.replace(",", ".")
                schema["maximum"] = RawNumericValue(norm)
            elif type_val == "array":
                schema["maxItems"] = RawNumericValue(raw.split(",")[0].split(".")[0])


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

    # Handle combinators (oneOf/allOf/anyOf)
    if pd.notna(schema_ref):
        combinator_schema = handle_combinator_refs(type_val, schema_ref, desc)
        if combinator_schema:
            return combinator_schema

        # Handle standard $ref
        ref_schema = handle_schema_reference(type_val, schema_ref, desc, version)
        schema.update(ref_schema)

    # Filter out Excel-specific type keywords
    invalid_types = ["parameter", "parameters", "schema", "header", "response"]
    if type_val in invalid_types:
        type_val = "string"  # Fallback to string

    # Set base type if not already set by ref handling
    if type_val != "array" and "$ref" not in schema and "allOf" not in schema:
        schema["type"] = type_val

    # Add title and description
    if pd.notna(title):
        schema["title"] = str(title)
    
    if desc and str(desc).strip():
        if "description" not in schema:
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
    # Both OAS 3.0 and 3.1 support examples at schema level
    # OAS 3.1 uses `examples` array, OAS 3.0 uses singular `example`
    ex = get_col_value(row, ["Example", "Examples"])
    if pd.notna(ex):
        ex_first = str(ex).split(";")[0].strip()
        parsed_ex = parse_example_string(ex_first)
        # Apply coercion if possible (for primitives and arrays)
        # For complex objects, full coercion happens at response/component building level
        parsed_ex = coerce_example_types(parsed_ex, schema, components_schemas)
        
        if version.startswith("3.1"):
            schema["examples"] = [parsed_ex]
        else:
            # OAS 3.0: use singular example
            schema["example"] = parsed_ex

    return schema
