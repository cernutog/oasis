"""
Schema Flattener Module

Converts nested OAS schemas into flat table format expected by OASIS Excel templates.
Handles object properties, arrays, $ref references, and combinators (allOf/anyOf/oneOf).

Usage:
    flattener = SchemaFlattener(oas_parser)
    rows = flattener.flatten_schema('MySchema')
"""

from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
import datetime
from collections import OrderedDict
import pandas as pd
from .oas_parser import OASParser
from src.generator_pkg.yaml_output import RawNumericValue, OASDumper


@dataclass
class FlatRow:
    """Represents a single row in the flattened schema table."""
    section: Optional[str] = None  # For response sheets: 'headers', 'content', 'links'
    name: str = ''
    parent: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    items_type: Optional[str] = None
    schema_name: Optional[str] = None
    format: Optional[str] = None
    mandatory: Optional[str] = None  # 'M', 'O', or 'C'
    min_value: Optional[str] = None
    max_value: Optional[str] = None
    pattern: Optional[str] = None
    regex: Optional[str] = None
    allowed_values: Optional[str] = None
    example: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for Excel writing."""
        return {
            'Section': self.section,
            'Name': self.name,
            'Parent': self.parent,
            'Title': self.title,
            'Description': self.description,
            'Type': self.type,
            'Items Data Type': self.items_type,
            'Schema Name': self.schema_name,
            'Format': self.format,
            'Mandatory': self.mandatory,
            'Min': self.min_value,
            'Max': self.max_value,
            'PatternEba': self.pattern,
            'Regex': self.regex,
            'Allowed value': self.allowed_values,
            'Example': self.example
        }


def _python_type_to_oas(value: Any) -> str:
    """Map Python type to OAS type name."""
    if value is None:
        return 'string'
    type_map = {
        'str': 'string',
        'int': 'integer',
        'float': 'number',
        'bool': 'boolean',
        'list': 'array',
        'dict': 'object',
        'datetime': 'string',
        'date': 'string',
    }
    py_type = type(value).__name__
    return type_map.get(py_type, py_type)


def _to_string(value: Any) -> str:
    """
    Convert value to string, handling datetime objects explicitly to preserve ISO 8601 format.
    Python's default str(datetime) uses space separator, we want 'T'.
    """
    if isinstance(value, (datetime.datetime, datetime.date)):
        return value.isoformat()
    return str(value)


class SchemaFlattener:
    """
    Flattens OAS schemas into table rows for Excel templates.
    
    Handles:
    - Object properties with nested structures
    - Array items
    - $ref references to other schemas
    - Combinators (allOf, anyOf, oneOf)
    - Required vs optional properties
    """
    
    def __init__(self, oas_dict: Dict[str, Any]):
        """
        Initialize with OAS dictionary.
        
        Args:
            oas_dict: The parsed OAS document
        """
        self.oas = oas_dict
        self.schemas = oas_dict.get('components', {}).get('schemas', {})
        self._visited: Set[str] = set()  # Prevent infinite recursion
    
    def _get_mandatory_flag(self, required: Optional[bool]) -> Optional[str]:
        """Convert required boolean to 'M', 'O', or None (empty)."""
        if required is True:
            return 'M'
        if required is False:
            return 'O'
        return None  # Not specified

    def _populate_row_from_schema(self, row: FlatRow, schema: Dict[str, Any]) -> None:
        # Format
        if schema.get('format'):
            row.format = schema['format']
        
        # Min constraints (value, length, or items)
        if schema.get('minimum') is not None:
            row.min_value = _to_string(schema['minimum'])
        elif schema.get('minLength') is not None:
            row.min_value = str(schema['minLength'])
        elif schema.get('minItems') is not None:
            row.min_value = str(schema['minItems'])
        
        # Max constraints (value, length, or items)
        if schema.get('maximum') is not None:
            row.max_value = _to_string(schema['maximum'])
        elif schema.get('maxLength') is not None:
            row.max_value = str(schema['maxLength'])
        elif schema.get('maxItems') is not None:
            row.max_value = str(schema['maxItems'])
        
        # Pattern/Regex
        if schema.get('pattern'):
            row.regex = schema['pattern']
        
        # Enum values
        if schema.get('enum'):
            row.allowed_values = ', '.join(_to_string(v) for v in schema['enum'])
        
        # Determine if this is a container (combinators only) OR a content root row
        # OR a combinator alternative root (e.g. Something[0])
        type_val = schema.get('type')
        is_combinator = any(k in schema for k in ['oneOf', 'anyOf', 'allOf'])
        is_branch_root = '[' in row.name and ']' in row.name and row.name.endswith(']')
        is_content_root = row.section == 'content' and not row.parent
        
        is_container = is_combinator or is_branch_root or is_content_root
        
        # Description and Title Mapping
        title = schema.get('title')
        description = schema.get('description')
        
        if title:
            if is_container:
                # CONTAINER: Map OAS 'title' to Excel 'Description' column
                row.description = str(title)
            else:
                row.title = str(title)
        
        if description and not row.description:
            row.description = str(description)

        # Examples (collect all from both 'example' and 'examples')
        all_examples = []
        if schema.get('example') is not None:
            all_examples.append(schema['example'])
        
        if 'examples' in schema:
            exs = schema['examples']
            if isinstance(exs, list):
                for ex in exs:
                    if ex not in all_examples:
                        all_examples.append(ex)
            elif exs is not None and exs not in all_examples:
                all_examples.append(exs)
        
        if all_examples:
            serialized_examples = [self._serialize_example(ex, schema) for ex in all_examples]
            # Smart Quoting for CSV-style preservation with comma + space
            quoted_parts = []
            for ex in serialized_examples:
                if ex is None:
                    continue
                ex_str = str(ex)
                if ',' in ex_str or '"' in ex_str:
                    # CSV quote rule: double existing quotes, wrap in quotes
                    ex_str = '"' + ex_str.replace('"', '""') + '"'
                quoted_parts.append(ex_str)
            
            # Join with comma and space as requested
            row.example = ", ".join(quoted_parts)

    def _sanitize_for_yaml(self, value: Any) -> Any:
        """
        Recursively convert date/datetime objects to ISO strings in complex structures.
        This prevents PyYAML from dumping them as non-ISO strings or YAML timestamp objects.
        """
        if isinstance(value, dict):
            return {k: self._sanitize_for_yaml(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [self._sanitize_for_yaml(v) for v in value]
        elif isinstance(value, (datetime.datetime, datetime.date)):
            return value.isoformat()
        else:
            return value

    def _serialize_example(self, value: Any, schema: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """Helper to serialize example value to YAML string with type-aware coercion."""
        if value is None:
            return None
        
        # Apply deep coercion and sanitization (dates to ISO, numbers to quoted strings if schema type is string)
        coerced = self._coerce_example(value, schema)
        
        if isinstance(coerced, (dict, list)):
            import yaml
            # Use literal_preserve_order style if needed? OASDump is usually global.
            # Here we just want a clean YAML block for the Excel cell.
            return yaml.dump(coerced, Dumper=OASDumper, default_flow_style=False, allow_unicode=True, sort_keys=False).strip()
        
        return str(coerced)

    def _coerce_example(self, value: Any, schema: Optional[Dict[str, Any]]) -> Any:
        """
        Recursively coerce example values based on schema types.
        Quotes numeric strings only if the schema type is 'string'.
        Also sanitizes dates/datetimes to ISO strings.
        """
        # Resolve schema $ref if present
        if schema and isinstance(schema, dict) and '$ref' in schema:
            schema = self._resolve_ref(schema['$ref'])

        target_type = schema.get('type') if schema and isinstance(schema, dict) else None
        
        if isinstance(value, dict):
            # Gather properties from schema and ALL combinator schemas
            properties = schema.get('properties', {}).copy() if schema and isinstance(schema, dict) else {}
            if schema and isinstance(schema, dict):
                for combinator in ['oneOf', 'anyOf', 'allOf']:
                    if combinator in schema and isinstance(schema[combinator], list):
                        for sub_schema in schema[combinator]:
                            if isinstance(sub_schema, dict):
                                # Resolve $ref inside combinator
                                if '$ref' in sub_schema:
                                    sub_schema = self._resolve_ref(sub_schema['$ref'])
                                properties.update(sub_schema.get('properties', {}))

            return {
                k: self._coerce_example(v, properties.get(k, {}))
                for k, v in value.items()
            }
        elif isinstance(value, list):
            items_schema = schema.get('items', {}) if schema and isinstance(schema, dict) else {}
            # If items_schema is a ref, resolve it to get accurate type
            if items_schema and isinstance(items_schema, dict) and '$ref' in items_schema:
                items_schema = self._resolve_ref(items_schema['$ref'])
            return [self._coerce_example(item, items_schema) for item in value]
        elif isinstance(value, (datetime.datetime, datetime.date)):
            return value.isoformat()
        elif isinstance(value, str):
            # 1. Handle explicit strings (sanitize/strip quotes)
            # PROACTIVE STRIPPING: Always strip redundant quotes from string inputs.
            # This handles cases where target_type is unknown or resolution failed.
            if isinstance(value, str):
                s_val = value.strip()
                if len(s_val) >= 2 and (
                    (s_val.startswith("'") and s_val.endswith("'")) or 
                    (s_val.startswith('"') and s_val.endswith('"'))
                ):
                    # Check if stripping makes it a number? 
                    # If we strip "'1.0'" -> "1.0", it becomes a number candidate below.
                    # This is DESIRED behavior.
                    value = s_val[1:-1]
                    
            if target_type == 'string':
                return value

            # 2. Check if it was originally a number preserved by SafeLoaderRawNumbers
            try:
                # If it's a valid number, we check if it needs quoting
                float(value)
                
                # PRECISE TYPE DETECTION: If not direct, look into combinators
                if not target_type and schema and isinstance(schema, dict):
                    for combinator in ['oneOf', 'anyOf', 'allOf']:
                        if combinator in schema and isinstance(schema[combinator], list):
                            for sub_schema in schema[combinator]:
                                if isinstance(sub_schema, dict):
                                    # Resolve $ref
                                    if '$ref' in sub_schema:
                                        sub_schema = self._resolve_ref(sub_schema['$ref'])
                                    if sub_schema.get('type'):
                                        target_type = sub_schema.get('type')
                                        break
                        if target_type: break

                # Redundant check (handled above), but harmless
                if target_type == 'string':
                    return value
                
                if target_type in ['number', 'integer']:
                    # STRING PRESERVATION: Return as RawNumericValue string
                    # This ensures Excel and subsequent Generator use exact string.
                    return RawNumericValue(value)
                
                # Default for numbers if type unknown: use RawNumericValue to preserve precision
                return RawNumericValue(value)

            except (ValueError, TypeError):
                pass
            return value
        else:
            return value

    def flatten_schema(self, schema_name: str, 
                       root_name: Optional[str] = None,
                       section: Optional[str] = None,
                       include_root: bool = True) -> List[FlatRow]:
        """
        Flatten a schema by name into rows.
        """
        print(f"DEBUG: flatten_schema called for {schema_name}")
        if schema_name not in self.schemas:
            print(f"DEBUG: {schema_name} not found in schemas: {list(self.schemas.keys())}")
            return []
        
        rows = []
        schema = self.schemas[schema_name]
        name = root_name or schema_name
        
        # Check if this schema is a combinator (has oneOf/anyOf/allOf)
        # Combinators will be handled directly by _flatten_schema_def, no root row needed
        is_combinator = any(key in schema for key in ['oneOf', 'anyOf', 'allOf'])
        print(f"DEBUG: flatten_schema {name} is_combinator={is_combinator} include_root={include_root} keys={list(schema.keys())}") 
        
        # Add root row for top-level component schemas (SKIP for combinators)
        if include_root and not is_combinator:
            schema_type = schema.get('type', 'object')
            root_row = FlatRow(
                section=section,
                name=name,
                parent=None,
                type=schema_type,
                description=schema.get('description'),
                mandatory=None  # Root schemas don't have mandatory flag
            )
            # Populate all other fields (enum, examples, min/max, pattern, format, etc.)
            self._populate_row_from_schema(root_row, schema)
            rows.append(root_row)
        
        # Flatten the schema with this name as parent for all children
        # For combinators: parent=None so combinator row becomes root
        # For regular schemas: parent=name so properties are nested under root
        child_rows = self._flatten_schema_def(
            schema, 
            name=name,
            parent=name if (include_root and not is_combinator) else None,
            required=True,
            section=section,
            is_root=True  # Signal that this is the root call
        )
        rows.extend(child_rows)
        return rows
    
    def flatten_inline_schema(self, schema: Dict[str, Any],
                              name: str = 'root',
                              parent: Optional[str] = None,
                              required: bool = True,
                              section: Optional[str] = None) -> List[FlatRow]:
        """
        Flatten an inline schema definition.
        
        Args:
            schema: The schema definition dict
            name: Name for this element
            parent: Parent element name
            required: Whether this element is required
            section: Section label for response sheets
            
        Returns:
            List of FlatRow objects
        """
        return self._flatten_schema_def(schema, name, parent, required, section)
    
    def _flatten_schema_def(self, schema: Dict[str, Any],
                            name: str,
                            parent: Optional[str],
                            required: Optional[bool],
                            section: Optional[str] = None,
                            is_root: bool = False) -> List[FlatRow]:
        """Internal method to flatten a schema definition.
        
        Args:
            is_root: If True, this is the root call from flatten_schema() and we should
                     skip emitting a row for the schema itself (already emitted by caller).
        """
        rows = []
        
        # Handle $ref - always emit if not root, or emit with parent if root
        # Also capture sibling fields like description and example (valid in OAS 3.1)
        if '$ref' in schema:
            ref_name = self._extract_ref_name(schema['$ref'])
            if not is_root:
                row = FlatRow(
                    section=section,
                    name=name,
                    parent=parent,
                    description=schema.get('description'),  # Capture sibling description
                    type='schema',
                    schema_name=ref_name,
                    mandatory=self._get_mandatory_flag(required),
                    items_type=None,
                    example=self._serialize_example(schema.get('example'), schema) if schema.get('example') is not None else None  # Capture sibling example
                )
                rows.append(row)
            return rows
        
        # Handle combinators
        for combinator in ['allOf', 'anyOf', 'oneOf']:
            if combinator in schema:
                return self._handle_combinator(
                    schema, combinator, name, parent, required, section
                )
        
        # Handle array type
        if schema.get('type') == 'array':
            return self._handle_array(schema, name, parent, required, section, is_root)
        
        # Handle object type or properties directly
        if schema.get('type') == 'object' or 'properties' in schema:
            return self._handle_object(schema, name, parent, required, section, is_root)
        
        # Handle primitive type - only emit if not root (root already emitted)
        if not is_root:
            res = self._create_primitive_row(schema, name, parent, required, section)
            if isinstance(res, list):
                rows.extend(res)
            else:
                rows.append(res)
        return rows
    
    def _handle_combinator(self, schema: Dict[str, Any],
                           combinator: str,
                           name: str,
                           parent: Optional[str],
                           required: Optional[bool],
                           section: Optional[str]) -> List[FlatRow]:
        """Handle allOf, anyOf, oneOf combinators."""
        rows = []
        
        # Collect all refs in the combinator
        refs = []
        inline_schemas = []
        
        for item in schema[combinator]:
            if '$ref' in item:
                refs.append(self._extract_ref_name(item['$ref']))
            else:
                inline_schemas.append(item)
        
        # Create main row with combinator type
        row = FlatRow(
            section=section,
            name=name,
            parent=parent,
            type=combinator,
            schema_name=', '.join(refs) if refs else None,
            mandatory=self._get_mandatory_flag(required)
        )
        self._populate_row_from_schema(row, schema)
        rows.append(row)
        
        # Flatten inline schemas as children
        for i, inline in enumerate(inline_schemas):
            child_rows = self._flatten_schema_def(
                inline,
                name=f"{name}[{i}]",
                parent=name,
                required=required,
                section=section
            )
            rows.extend(child_rows)
        
        return rows
    
    def _handle_array(self, schema: Dict[str, Any],
                      name: str,
                      parent: Optional[str],
                      required: Optional[bool],
                      section: Optional[str],
                      is_root: bool = False) -> List[FlatRow]:
        """Handle array type schemas.
        
        Args:
            is_root: If True, skip emitting the array row (already emitted by flatten_schema)
        """
        rows = []
        items = schema.get('items', {})
        
        # Only emit array row if not root (root row already emitted by flatten_schema)
        if not is_root:
            row = FlatRow(
                section=section,
                name=name,
                parent=parent,
                type='array',
                mandatory=self._get_mandatory_flag(required),
                min_value=str(schema.get('minItems')) if schema.get('minItems') is not None else None,
                max_value=str(schema.get('maxItems')) if schema.get('maxItems') is not None else None
            )
            self._populate_row_from_schema(row, schema)
            
            # Capture description from items if row's description is empty
            if not row.description and isinstance(items, dict) and items.get('description'):
                row.description = str(items['description'])
            
            # Handle items type
            combinator = next((k for k in ['oneOf', 'allOf', 'anyOf'] if k in items), None)
            
            if combinator:
                 row.items_type = combinator
                 # Collect refs
                 refs = []
                 for item in items[combinator]:
                     if '$ref' in item:
                         refs.append(self._extract_ref_name(item['$ref']))
                 if refs:
                     row.schema_name = ', '.join(refs)
            elif '$ref' in items:
                row.items_type = 'schema'
                row.schema_name = self._extract_ref_name(items['$ref'])
            elif items.get('type'):
                row.items_type = items.get('type')
                if items.get('format'):
                    row.format = items['format']
            
            rows.append(row)
        
        # If items is an inline object, flatten its properties directly with array as parent
        if items.get('type') == 'object' or 'properties' in items:
            # Flatten the object's properties directly, using the array name as parent
            # This way the generator knows these are properties of the array's items
            for prop_name, prop_schema in items.get('properties', {}).items():
                is_required = prop_name in items.get('required', [])
                child_rows = self._flatten_schema_def(
                    prop_schema,
                    name=prop_name,
                    parent=name,  # Use array name as parent, not 'items'
                    required=is_required,
                    section=section
                )
                rows.extend(child_rows)
        
        # Handle custom extensions (x-*)
        for key, val in schema.items():
            if key.startswith('x-'):
                self._flatten_response_extension(rows, key, val, name)
                
        return rows
    
    def _handle_object(self, schema: Dict[str, Any],
                       name: str,
                       parent: Optional[str],
                       required: Optional[bool],
                       section: Optional[str],
                       is_root: bool = False) -> List[FlatRow]:
        """Handle object type schemas."""
        rows = []
        required_props = set(schema.get('required', []))
        
        # Add object row only if it has a parent AND is not root (root already emitted by flatten_schema)
        if parent is not None and not is_root:
            row = FlatRow(
                section=section,
                name=name,
                parent=parent,
                type='object',
                mandatory=self._get_mandatory_flag(required)
            )
            self._populate_row_from_schema(row, schema)
            rows.append(row)
        
        # Flatten properties - children always have this schema as parent
        for prop_name, prop_schema in schema.get('properties', {}).items():
            prop_required = prop_name in required_props
            child_rows = self._flatten_schema_def(
                prop_schema,
                name=prop_name,
                parent=name,  # Children always have parent set
                required=prop_required,
                section=section
            )
            rows.extend(child_rows)
        
        # Handle additionalProperties if present and is a schema
        if isinstance(schema.get('additionalProperties'), dict):
            add_prop = schema['additionalProperties']
            child_rows = self._flatten_schema_def(
                add_prop,
                name='<additionalProperties>',
                parent=name,
                required=False,
                section=section
            )
            rows.extend(child_rows)
        
        # Handle custom extensions (x-*)
        for key, val in schema.items():
            if key.startswith('x-'):
                self._flatten_response_extension(rows, key, val, name)
                
        return rows
    
    def _create_primitive_row(self, schema: Dict[str, Any],
                              name: str,
                              parent: Optional[str],
                              required: Optional[bool],
                              section: Optional[str]) -> FlatRow:
        """Create a row for a primitive type."""
        row = FlatRow(
            section=section,
            name=name,
            parent=parent,
            type=schema.get('type'),
            description=schema.get('description'),
            mandatory=self._get_mandatory_flag(required)
        )
        
        # Use helper to populate all other fields consistently
        self._populate_row_from_schema(row, schema)
        
        # Handle custom extensions (x-*)
        # For primitives, extensions are added as separate rows
        extensions_rows = []
        for key, val in schema.items():
            if key.startswith('x-'):
                self._flatten_response_extension(extensions_rows, key, val, name)
        
        if extensions_rows:
            return [row] + extensions_rows
            
        return row
    
    def _extract_ref_name(self, ref: str) -> str:
        """Extract schema name from $ref string."""
        return ref.split('/')[-1]
    
    def flatten_request_body(self, request_body: Dict[str, Any],
                             section: Optional[str] = None) -> List[FlatRow]:
        """
        Flatten a request body definition.
        
        Args:
            request_body: The requestBody object
            section: Section label
            
        Returns:
            List of FlatRow objects
        """
        rows = []
        content = request_body.get('content', {})
        
        for media_type, media_obj in content.items():
            schema = media_obj.get('schema', {})
            
            # 1. Content Root Row (Media Type)
            # Reference has explicit row for 'application/json' with Section='content'
            root_row = FlatRow(
                section='content' if section is None else section,
                name=media_type,
                type=schema.get('type') or 'object',
                description=schema.get('description'),
                mandatory='M'
            )
            self._populate_row_from_schema(root_row, schema)
            rows.append(root_row)
            
            # 2. Flatten Schema
            if '$ref' in schema:
                ref_name = self._extract_ref_name(schema['$ref'])
                # Use Reference directly instead of flattening
                # This ensures Generator uses $ref to Global Component
                root_row.schema_name = ref_name
                root_row.type = 'schema'
            else:
                rows.extend(self.flatten_inline_schema(
                    schema, 
                    name=media_type,
                    section=section
                ))
            
            # Only process first media type (usually application/json)
            break
        
        return rows
    
    def flatten_component_response(self, resp_name: str, response: Dict[str, Any]) -> List[FlatRow]:
        """
        Flatten a named component response including a root row.
        
        Args:
            resp_name: Name of the response component
            response: The response object
            
        Returns:
            List of FlatRow objects with root row first
        """
        rows = []
        
        # Handle $ref
        if '$ref' in response:
            response = self._resolve_ref(response['$ref'])
        
        # Root row for the response
        root_row = FlatRow(
            section=None,
            name=resp_name,
            parent=None,
            description=response.get('description'),
            type=None,
            mandatory=None
        )
        rows.append(root_row)
        
        # Iterate over response keys to preserve definition order
        # This fixes ordering mismatches between xlsm and xlsx (e.g. content vs extensions)
        for key, val in response.items():
            if key == 'headers':
                # Headers with parent set to response name
                for header_name, header_def in val.items():
                    header_rows = self._flatten_header(header_name, header_def)
                    for row in header_rows:
                        row.section = 'headers'
                        row.parent = resp_name
                    rows.extend(header_rows)
            
            elif key.startswith('x-'):
                # Response-level x-sandbox extensions
                self._flatten_response_extension(rows, key, val, resp_name)
            
            elif key == 'content':
                # Content
                for media_type, media_obj in val.items():
                    schema = media_obj.get('schema', {})
                    
                    # Content row with media type
                    content_row = FlatRow(
                        section='content',
                        name=media_type,
                        parent=resp_name,
                        type='schema' if '$ref' in schema else schema.get('type'),
                        description=schema.get('title') or schema.get('description', '').strip() if (schema.get('title') or schema.get('description')) else None  # Use title as description for content root
                    )
                    if '$ref' in schema:
                        content_row.schema_name = self._extract_ref_name(schema['$ref'])
                    rows.append(content_row)
                    
                    # Examples - parent is the content type (media_type)
                    examples = media_obj.get('examples', {})
                    for example_name, example_def in examples.items():
                        ex_row = FlatRow(
                            section='examples',
                            name=example_name,
                            parent=media_type,  # Parent is content type like 'text/plain'
                            description=example_def.get('summary') if isinstance(example_def, dict) else None
                        )
                        rows.append(ex_row)
                        
                        # Flatten all example properties
                        if isinstance(example_def, dict):
                            for k, v in example_def.items():
                                if k == 'summary':
                                    continue
                                self._flatten_example_child(rows, k, v, example_name)
            
            # Process all content types, not just the first one
        
        return rows
    
    def _flatten_example_value(self, rows: List[FlatRow], name: str, 
                               value: Any, parent: str) -> None:
        """Flatten an example value into rows."""
        if isinstance(value, (dict, list)):
            row = FlatRow(
                section='examples',
                name=name,
                parent=parent,
                type='object' if isinstance(value, dict) else 'array',
                example=self._serialize_example(value, None)
            )
            rows.append(row)
        else:
            # Simple scalar values (string, number, etc.)
            rows.append(FlatRow(
                section='examples',
                name=name,
                parent=parent,
                type=_python_type_to_oas(value),
                example=_to_string(value) if value is not None else None
            ))
    
    def _flatten_example_child(self, rows: List[FlatRow], name: str,
                               value: Any, parent: str) -> None:
        """Flatten example child values into rows with section='examples'.
        
        Child values of examples (like 'value', x-sandbox extensions inside examples)
        have section='examples' in the reference xlsm.
        """
        # Fix: Serialize 'value' property as YAML block if it's a complex object/array
        if name == 'value' and isinstance(value, (dict, list)):
             row = FlatRow(
                 section='examples',
                 name=name,
                 parent=parent,
                 type='object' if isinstance(value, dict) else 'array',
                 example=self._serialize_example(value, None)
             )
             rows.append(row)
             return

        if isinstance(value, dict):
            row = FlatRow(
                section='examples',  # Child of example, section='examples'
                name=name,
                parent=parent,
                type=None  # Set type to None (empty) for dicts, matching xlsm
            )
            rows.append(row)
            
            for key, val in value.items():
                self._flatten_example_child(rows, key, val, name)
        elif isinstance(value, list):
            items_type = _python_type_to_oas(value[0]) if value else None
            # If items are objects (dicts), we don't know the schema name from the example value alone.
            # Reference xlsm has specific types (e.g. 'ErrorResponse') which are likely manual entries 
            # or derived from schema context not available here.
            # We leave it empty (None) to avoid incorrect 'object' type.
            if items_type == 'object':
                items_type = None 
                
            rows.append(FlatRow(
                section='examples',
                name=name,
                parent=parent,
                type='array',
                items_type=items_type
            ))
            # Flatten array items - use array name[i] as parent for item properties
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    # Flatten dict properties directly with parent=array_name[i]
                    parent_indexed = f"{name}[{i}]"
                    for key, val in item.items():
                        self._flatten_example_child(rows, key, val, parent_indexed)
        else:
            # Simple scalar values (string, number, etc.)
            rows.append(FlatRow(
                section='examples',
                name=name,
                parent=parent,
                type=_python_type_to_oas(value),
                example=_to_string(value) if value is not None else None
            ))
    
    def _flatten_response_extension(self, rows: List[FlatRow], name: str,
                                    value: Any, parent: str) -> None:
        """Flatten a response-level extension into rows with section=None.
        
        Unlike _flatten_example_value, this preserves section=None since
        response-level extensions are direct descendants of the response root.
        """
        if isinstance(value, dict):
            row = FlatRow(
                section=None,  # Direct descendant of response, no section
                name=name,
                parent=parent,
                type=None  # Container object has no type in xlsm (empty cell)
            )
            rows.append(row)
            
            for key, val in value.items():
                if isinstance(val, dict):
                    self._flatten_response_extension(rows, key, val, name)
                elif isinstance(val, list):
                    rows.append(FlatRow(
                        section=None,
                        name=key,
                        parent=name,
                        type='array',
                        items_type=_python_type_to_oas(val[0]) if val else None
                    ))
                else:
                    rows.append(FlatRow(
                        section=None,
                        name=key,
                        parent=name,
                        type=_python_type_to_oas(val),
                        example=_to_string(val) if val is not None else None
                    ))
        elif isinstance(value, list):
            rows.append(FlatRow(
                section=None,
                name=name,
                parent=parent,
                type='array'
            ))
        else:
            # Simple scalar values (string, number, etc.)
            rows.append(FlatRow(
                section=None,
                name=name,
                parent=parent,
                type=_python_type_to_oas(value),
                example=_to_string(value) if value is not None else None
            ))
    
    def flatten_response(self, response: Dict[str, Any]) -> List[FlatRow]:
        """
        Flatten a response definition including headers and content.
        
        Args:
            response: The response object
            
        Returns:
            List of FlatRow objects with section labels
        """
        rows = []
        
        # Handle $ref
        if '$ref' in response:
            response = self._resolve_ref(response['$ref'])
        
        # Headers
        for header_name, header_def in response.get('headers', {}).items():
            header_rows = self._flatten_header(header_name, header_def)
            for row in header_rows:
                row.section = 'headers'
                # Use response description or status code as parent for headers
                # if no parent is already set (e.g. not a global response)
                if not row.parent:
                    # Strip long descriptions for parent field
                    parent_val = response.get('description', '')
                    if parent_val:
                        parent_val = parent_val.split('.')[0].strip()
                    row.parent = parent_val or response.get('status_code', 'Response')
            rows.extend(header_rows)
        
        # Content
        content = response.get('content', {})
        for media_type, media_obj in content.items():
            schema = media_obj.get('schema', {})
            
            # Check for $ref
            ref_name = None
            if '$ref' in schema:
                ref_name = self._extract_ref_name(schema['$ref'])

            # 1. Content Root Row (Media Type)
            content_row = FlatRow(
                section='content',
                name=media_type,
                type='schema' if ref_name else (schema.get('type') or 'object'),
                description=schema.get('title') or schema.get('description'),
                mandatory='M',  # Content is usually mandatory if present
                schema_name=ref_name
            )
            self._populate_row_from_schema(content_row, schema)
            rows.append(content_row)
            
            # 2. Flatten Schema Children
            # Only flatten if NOT a Ref (preserves usage of Global Components)
            if not ref_name:
                child_rows = self._flatten_schema_def(
                    schema,
                    name=media_type,
                    parent=None, # Parent of root is None
                    required=True,
                    section='content',
                    is_root=True # Skip re-emitting media_type row
                )
                rows.extend(child_rows)
            
            # 3. Examples
            examples = media_obj.get('examples', {})
            for example_name, example_def in examples.items():
                ex_row = FlatRow(
                    section='examples',
                    name=example_name,
                    parent=media_type,  # Parent is content type
                    description=example_def.get('summary') if isinstance(example_def, dict) else None
                )
                rows.append(ex_row)
                
                # Flatten all example properties
                if isinstance(example_def, dict):
                    for k, v in example_def.items():
                        if k == 'summary':
                            continue
                        self._flatten_example_child(rows, k, v, example_name)
            
            # Only process first media type? Reference supports only one usually.
            # But loop implies support. Let's not break.
            break
        
        # Links
        for link_name, link_def in response.get('links', {}).items():
            row = FlatRow(
                section='links',
                name=link_name,
                description=link_def.get('description')
            )
            rows.append(row)
        
        # Extensions (x-*)
        # Flatten all top-level extensions provided in the response_dict
        for ext_name, ext_val in response.get('extensions', {}).items():
            self._flatten_response_extension(rows, ext_name, ext_val, 'Response')
            
        return rows
    
    def _flatten_header(self, name: str, header_def: Dict[str, Any]) -> List[FlatRow]:
        """Flatten a header definition."""
        ref_name = None
        
        # Priority for Description: Capture local description BEFORE resolving ref
        # This prevents pulling global component descriptions into local Excel rows
        local_description = header_def.get('description')

        # Handle top-level $ref (common for headers)
        if '$ref' in header_def:
            ref_name = self._extract_ref_name(header_def['$ref'])
            # We resolve to get structure (schema, format, etc.)
            resolved_def = self._resolve_ref(header_def['$ref'])
            # But we only use description if it was locally overridden
            header_def = resolved_def
        
        schema = header_def.get('schema', {})
        
        # Also handle schema-level $ref if present
        if not ref_name and '$ref' in schema:
            ref_name = self._extract_ref_name(schema['$ref'])
        
        # Final description decision:
        # If local description exists (even as sibling to $ref), use it.
        # If no local description and NOT a ref, use schema description.
        description = local_description
        if not description and not ref_name and isinstance(schema, dict):
            description = schema.get('description')

        row = FlatRow(
            name=name,
            description=description,
            mandatory=self._get_mandatory_flag(header_def.get('required')),
        )
        
        # Headers always have type='header'
        row.type = 'header'
        
        if ref_name:
            # If it's a reference (e.g. FpadResponseIdentifier), set schema name and clear format
             row.schema_name = ref_name
             row.format = None
        
        # Ensure we capture examples and format even for non-ref headers
        # or capture constraints if they exist at header schema level
        if isinstance(schema, dict):
            self._populate_row_from_schema(row, schema)
            
        # Example priority: Header level > Schema level (already handled by populate)
        if header_def.get('example') is not None:
             row.example = self._serialize_example(header_def['example'], schema)
        elif header_def.get('examples'):
             # Handle OAS 3.1 header examples dict
             exs = header_def.get('examples')
             if isinstance(exs, dict) and exs:
                 first_ex = next(iter(exs.values()))
                 if isinstance(first_ex, dict) and 'value' in first_ex:
                      row.example = self._serialize_example(first_ex['value'], schema)
                 else:
                      row.example = self._serialize_example(first_ex, schema)

        return [row]
    
    def _resolve_ref(self, ref: str) -> Dict[str, Any]:
        """Resolve a $ref to its definition."""
        if not ref.startswith('#/'):
            return {}
        
        parts = ref[2:].split('/')
        result = self.oas
        for part in parts:
            result = result.get(part, {})
        return result


def main():
    """Test the schema flattener."""
    import sys
    import yaml
    
    if len(sys.argv) < 2:
        print("Usage: python schema_flattener.py <oas_file> [schema_name]")
        sys.exit(1)
    
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        oas = yaml.safe_load(f)
    
    flattener = SchemaFlattener(oas)
    
    schema_name = sys.argv[2] if len(sys.argv) > 2 else list(flattener.schemas.keys())[0]
    
    print(f"Flattening schema: {schema_name}")
    print("-" * 60)
    
    rows = flattener.flatten_schema(schema_name)
    
    for row in rows:
        parent_str = f" (parent: {row.parent})" if row.parent else ""
        type_str = row.type or row.schema_name or ""
        print(f"{row.mandatory or 'O'} | {row.name}{parent_str} | {type_str}")


if __name__ == '__main__':
    main()
