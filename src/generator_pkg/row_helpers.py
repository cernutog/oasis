"""
Row Helper Utilities for OAS Generation.

Contains functions for extracting values from Excel DataFrame rows.
These are shared utilities used by schema_builder, response_builder, etc.
"""

import json
import yaml
import textwrap
import pandas as pd


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


def parse_example_string(ex_str):
    """
    Parses a string as JSON or YAML.
    
    :param ex_str: String to parse
    :return: Parsed value (dict, list, or original string if parsing fails)
    """
    # Return None for actual None, but preserve empty string ''
    if ex_str is None:
        return None
    
    ex_str = str(ex_str).strip()
    
    # Preserve empty string (e.g., for 204 No Content responses)
    if ex_str == '':
        return ''

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
        # 3. If YAML failed, it might be because of outer braces wrapping block-style YAML
        if ex_str.startswith("{") and ex_str.endswith("}"):
            inner = ex_str[1:-1]
            inner = inner.expandtabs(2)
            inner = textwrap.dedent(inner)
            try:
                return yaml.safe_load(inner)
            except Exception:
                return inner

        return ex_str
