"""
YAML Output Utilities for OAS Generation.

Contains custom YAML serialization classes for OpenAPI spec output.
"""

import yaml
from collections import OrderedDict


class SafeLoaderNoTimestamp(yaml.SafeLoader):
    """Custom YAML loader that doesn't parse timestamps into datetime objects."""
    pass

# Use the default string constructor for timestamps to preserve original format
SafeLoaderNoTimestamp.add_constructor(
    'tag:yaml.org,2002:timestamp', yaml.SafeLoader.construct_yaml_str
)


class SafeLoaderRawNumbers(SafeLoaderNoTimestamp):
    """
    Custom YAML loader that loads numbers as strings to preserve precision (e.g., 1.00).
    Inherits from SafeLoaderNoTimestamp to also preserve timestamps.
    """
    pass

# Add constructors for integers and floats to load them as strings
SafeLoaderRawNumbers.add_constructor(
    'tag:yaml.org,2002:int', yaml.SafeLoader.construct_yaml_str
)
SafeLoaderRawNumbers.add_constructor(
    'tag:yaml.org,2002:float', yaml.SafeLoader.construct_yaml_str
)


class RawYAML:
    """Stores raw YAML text for literal insertion."""
    
    def __init__(self, raw_text, base_indent=0):
        self.raw_text = raw_text
        self.base_indent = base_indent


class RawNumericValue(str):
    """
    A string subclass that should be output as a raw number in YAML.
    This preserves exact precision (e.g., 4800.00) while remaining unquoted.
    """
    pass


class OASDumper(yaml.SafeDumper):
    """Custom YAML Dumper for OpenAPI specifications."""
    
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
    """Presenter for RawYAML objects."""
    # Output raw YAML text as-is
    lines = data.raw_text.strip().split("\n")
    # Return as a literal scalar block
    return dumper.represent_scalar("tag:yaml.org,2002:str", data.raw_text, style="|")


def raw_numeric_presenter(dumper, data):
    """
    Presenter for RawNumericValue.
    Dynamically determines if the value looks like a float or int 
    to prevent explicit tags (like !!float '1') in the output.
    """
    if '.' in data:
        return dumper.represent_scalar("tag:yaml.org,2002:float", data)
    else:
        return dumper.represent_scalar("tag:yaml.org,2002:int", data)


# Register custom representers
OASDumper.add_representer(RawYAML, raw_yaml_presenter)
OASDumper.add_representer(RawNumericValue, raw_numeric_presenter)

# Preserve OrderedDict order in output
OASDumper.add_representer(
    OrderedDict,
    lambda dumper, data: dumper.represent_mapping(
        "tag:yaml.org,2002:map", data.items()
    ),
)
