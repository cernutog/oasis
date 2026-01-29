"""
Row Helper Utilities for OAS Generation.

Contains functions for extracting values from Excel DataFrame rows.
These are shared utilities used by schema_builder, response_builder, etc.
"""

import json
import yaml
import textwrap
import re
import pandas as pd
from src.generator_pkg.yaml_output import RawNumericValue, SafeLoaderRawNumbers, SafeLoaderNoTimestamp
from datetime import datetime, date


def get_col_value(row, keys):
    """
    Helper to get value from row checking multiple column headers.
    
    :param row: pandas Series (a row from DataFrame)
    :param keys: str or list of str - column names to check
    :return: First non-null value found, or None
    """
    if isinstance(keys, str):
        keys = [keys]
    for k in keys:
        if k in row:
            val = row[k]
            if pd.notna(val):
                return val
    return None


def get_schema_name(row):
    """Get schema name from row."""
    return get_col_value(
        row,
        [
            "Schema Name",
            "Schema Name\n(for Type or Items Data Type = 'schema')",
            "Schema Name\n(for Type or Items Data Type = 'schema'||'header')",
            "Schema Name\n(for Type or Items Data Type = 'schema' || 'header')",
            "Schema Name\n(if Type = schema)",
        ],
    )


def get_type(row):
    """Get type/data type from row."""
    return get_col_value(row, ["Type", "Data Type", "Item Type", "Type "])


def get_name(row):
    """Get name/field name from row."""
    return get_col_value(
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


def get_parent(row):
    """Get parent name from row."""
    return get_col_value(row, ["Parent", "Parent Name"])


def get_description(row):
    """Get description from row."""
    return get_col_value(row, ["Description", "Desc", "Description "])


def get_title(row):
    """Get title from row."""
    return get_col_value(row, ["Title", "title", "Title "])


def parse_example_string(ex_str):
    """
    Parses a string as JSON or YAML.
    
    :param ex_str: String to parse
    :return: Parsed value (dict, list, or original string if parsing fails)
    """
    # Return None for actual None, but preserve empty string ''
    if ex_str is None:
        return None
    
    # Handle datetime objects directly (if already converted by pandas)
    if isinstance(ex_str, (datetime, date)):
        return ex_str.isoformat()
    if hasattr(ex_str, 'isoformat'): # Handle pandas Timestamp
        return ex_str.isoformat()
    
    ex_str = str(ex_str).strip()
    
    # Preserve empty string (e.g., for 204 No Content responses)
    if ex_str == '':
        return ''

    # 1. Try JSON if it looks like JSON
    if ex_str.startswith("{") or ex_str.startswith("["):
        try:
            # Use parse_float=RawNumericValue to preserve exact string for decimals (e.g., 4800.00)
            return json.loads(ex_str, parse_float=RawNumericValue)
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

    # 2. Try YAML (Use SafeLoaderRawNumbers for precision-preserving numeric parsing)
    try:
        # Pre-process: ensure trailing newline so that block scalars (|) at the very 
        # end of the input (e.g. last href in links) preserve their mandatory newline.
        # Without this, yaml.load() returns the string WITHOUT the newline, which 
        # then prevents OASDumper from using block style.
        yaml_str = ex_str
        if not yaml_str.endswith("\n"):
            yaml_str += "\n"
        return yaml.load(yaml_str, Loader=SafeLoaderRawNumbers)
    except (yaml.YAMLError, ValueError, TypeError):
        # 3. If YAML failed, it might be because of outer braces wrapping block-style YAML
        if ex_str.startswith("{") and ex_str.endswith("}"):
            inner = ex_str[1:-1]
            inner = inner.expandtabs(2)
            inner = textwrap.dedent(inner)
            try:
                return yaml.load(inner, Loader=SafeLoaderRawNumbers)
            except Exception:
                return inner

        return ex_str


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
    if "$ref" in schema and components_schemas:
        ref_path = schema["$ref"]
        if ref_path.startswith("#/components/schemas/"):
            ref_name = ref_path.split("/")[-1]
            schema = components_schemas.get(ref_name, {})

    # For allOf with single $ref + description (common pattern), follow the $ref
    # to get schema info, but DON'T modify the original schema structure
    effective_schema = schema
    if "allOf" in schema and components_schemas:
        for sub_schema in schema["allOf"]:
            if isinstance(sub_schema, dict) and "$ref" in sub_schema:
                ref_path = sub_schema["$ref"]
                if ref_path.startswith("#/components/schemas/"):
                    ref_name = ref_path.split("/")[-1]
                    resolved = components_schemas.get(ref_name, {})
                    # Use resolved schema for type checking only, don't modify original
                    effective_schema = resolved
                    break

    schema_type = effective_schema.get("type")

    # Handle object: recurse into properties
    if isinstance(value, dict):
        properties = effective_schema.get("properties", {}).copy()
        # Also check allOf/anyOf/oneOf for properties in effective_schema
        for combinator in ["allOf", "anyOf", "oneOf"]:
            if combinator in effective_schema:
                for sub_schema in effective_schema[combinator]:
                    if isinstance(sub_schema, dict):
                        # Resolve $ref inside combinator
                        if "$ref" in sub_schema and components_schemas:
                            ref_path = sub_schema["$ref"]
                            if ref_path.startswith("#/components/schemas/"):
                                ref_name = ref_path.split("/")[-1]
                                sub_schema = components_schemas.get(ref_name, {})
                        
                        properties.update(sub_schema.get("properties", {}))
        
        result = {}
        for k, v in value.items():
            prop_schema = properties.get(k, {})
            result[k] = coerce_example_types(v, prop_schema, components_schemas)
        return result

    # Handle array: recurse into items
    if isinstance(value, list):
        items_schema = effective_schema.get("items", {})
        return [
            coerce_example_types(item, items_schema, components_schemas)
            for item in value
        ]

    # Handle scalar:
    # 1. Coerce numeric to string if schema expects string
    if schema_type == "string" and isinstance(value, (int, float)):
        return str(value)

    # 2. Coerce numeric string back to number if schema expects number/integer
    if schema_type in ["number", "integer"] and isinstance(value, (str, int, float)):
        try:
            # Check if it's a valid number
            float(value)
            # STRING PRESERVATION: Wrap in RawNumericValue to maintain source characters
            # (including trailing zeros like .00)
            return RawNumericValue(str(value))
        except (ValueError, TypeError):
            pass

    return value

