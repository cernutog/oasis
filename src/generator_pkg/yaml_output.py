"""
YAML Output Utilities for OAS Generation.

Contains custom YAML serialization classes for OpenAPI spec output.
"""

import yaml
from collections import OrderedDict


class RawYAML:
    """Stores raw YAML text for literal insertion."""
    
    def __init__(self, raw_text, base_indent=0):
        self.raw_text = raw_text
        self.base_indent = base_indent


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


# Register custom representers
OASDumper.add_representer(RawYAML, raw_yaml_presenter)

# Preserve OrderedDict order in output
OASDumper.add_representer(
    OrderedDict,
    lambda dumper, data: dumper.represent_mapping(
        "tag:yaml.org,2002:map", data.items()
    ),
)
