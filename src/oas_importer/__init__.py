"""
OAS Importer Package

This package provides functionality to import OpenAPI Specification (OAS) files
and generate corresponding Excel templates for editing by functional analysts.

Modules:
    - style_extractor: Extract and save styles from reference templates
    - oas_parser: Parse OAS YAML files
    - schema_flattener: Convert nested schemas to flat table format
    - excel_writer: Base Excel writing with style application
    - index_writer: Generate $index.xlsx
    - operation_writer: Generate operation files
    - reverse_mapper: High-level orchestrator
"""

from .style_extractor import StyleExtractor
from .oas_parser import OASParser
from .schema_flattener import SchemaFlattener, FlatRow
from .excel_writer import ExcelWriter

__all__ = ['StyleExtractor', 'OASParser', 'SchemaFlattener', 'FlatRow', 'ExcelWriter']
