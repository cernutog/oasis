"""
OAS Generator Package.

This package provides the OASGenerator class for generating OpenAPI specifications
from Excel templates.
"""

from .yaml_output import RawYAML, OASDumper, raw_yaml_presenter

# Note: OASGenerator is still in the original generator.py file
# This package structure allows gradual migration

__all__ = ['RawYAML', 'OASDumper', 'raw_yaml_presenter']
