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


@dataclass
class FlatRow:
    """Represents a single row in the flattened schema table."""
    section: Optional[str] = None  # For response sheets: 'headers', 'content', 'links'
    name: str = ''
    parent: Optional[str] = None
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
    
    def flatten_schema(self, schema_name: str, 
                       root_name: Optional[str] = None,
                       section: Optional[str] = None,
                       include_root: bool = True) -> List[FlatRow]:
        """
        Flatten a schema by name into rows.
        
        Args:
            schema_name: Name of the schema in components/schemas
            root_name: Override for the root element name
            section: Section label for response sheets
            include_root: Whether to include a root row for the schema
            
        Returns:
            List of FlatRow objects
        """
        if schema_name not in self.schemas:
            return []
        
        rows = []
        schema = self.schemas[schema_name]
        name = root_name or schema_name
        
        # Add root row for top-level component schemas
        if include_root:
            schema_type = schema.get('type', 'object')
            root_row = FlatRow(
                section=section,
                name=name,
                parent=None,
                type=schema_type,
                description=schema.get('description'),
                mandatory=None  # Root schemas don't have mandatory flag
            )
            rows.append(root_row)
        
        # Flatten the schema with this name as parent for all children
        child_rows = self._flatten_schema_def(
            schema, 
            name=name,
            parent=name if include_root else None,
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
                            required: bool,
                            section: Optional[str] = None,
                            is_root: bool = False) -> List[FlatRow]:
        """Internal method to flatten a schema definition.
        
        Args:
            is_root: If True, this is the root call from flatten_schema() and we should
                     skip emitting a row for the schema itself (already emitted by caller).
        """
        rows = []
        
        # Handle $ref - always emit if not root, or emit with parent if root
        if '$ref' in schema:
            ref_name = self._extract_ref_name(schema['$ref'])
            if not is_root:
                row = FlatRow(
                    section=section,
                    name=name,
                    parent=parent,
                    type='schema',
                    schema_name=ref_name,
                    mandatory='M' if required else 'O'
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
            return self._handle_array(schema, name, parent, required, section)
        
        # Handle object type or properties directly
        if schema.get('type') == 'object' or 'properties' in schema:
            return self._handle_object(schema, name, parent, required, section, is_root)
        
        # Handle primitive type - only emit if not root (root already emitted)
        if not is_root:
            row = self._create_primitive_row(schema, name, parent, required, section)
            rows.append(row)
        return rows
    
    def _handle_combinator(self, schema: Dict[str, Any],
                           combinator: str,
                           name: str,
                           parent: Optional[str],
                           required: bool,
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
            mandatory='M' if required else 'O',
            description=schema.get('description')
        )
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
                      required: bool,
                      section: Optional[str]) -> List[FlatRow]:
        """Handle array type schemas."""
        rows = []
        items = schema.get('items', {})
        
        row = FlatRow(
            section=section,
            name=name,
            parent=parent,
            type='array',
            description=schema.get('description'),
            mandatory='M' if required else 'O',
            min_value=str(schema.get('minItems')) if schema.get('minItems') is not None else None,
            max_value=str(schema.get('maxItems')) if schema.get('maxItems') is not None else None
        )
        
        # Handle items type
        if '$ref' in items:
            row.items_type = 'schema'
            row.schema_name = self._extract_ref_name(items['$ref'])
        elif items.get('type'):
            row.items_type = items.get('type')
            if items.get('format'):
                row.format = items['format']
        
        rows.append(row)
        
        # If items is an inline object, flatten it as children
        if items.get('type') == 'object' or 'properties' in items:
            child_rows = self._flatten_schema_def(
                items,
                name='items',
                parent=name,
                required=True,
                section=section
            )
            # Skip the first row (the object row itself) - we already have the array row
            if child_rows and child_rows[0].type in ('object', None):
                rows.extend(child_rows[1:])
            else:
                rows.extend(child_rows)
        
        return rows
    
    def _handle_object(self, schema: Dict[str, Any],
                       name: str,
                       parent: Optional[str],
                       required: bool,
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
                description=schema.get('description'),
                mandatory='M' if required else 'O'
            )
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
        
        return rows
    
    def _create_primitive_row(self, schema: Dict[str, Any],
                              name: str,
                              parent: Optional[str],
                              required: bool,
                              section: Optional[str]) -> FlatRow:
        """Create a row for a primitive type."""
        row = FlatRow(
            section=section,
            name=name,
            parent=parent,
            type=schema.get('type'),
            format=schema.get('format'),
            description=schema.get('description'),
            mandatory='M' if required else 'O'
        )
        
        # Constraints
        if schema.get('minimum') is not None:
            row.min_value = str(schema['minimum'])
        elif schema.get('minLength') is not None:
            row.min_value = str(schema['minLength'])
        
        if schema.get('maximum') is not None:
            row.max_value = str(schema['maximum'])
        elif schema.get('maxLength') is not None:
            row.max_value = str(schema['maxLength'])
        
        if schema.get('pattern'):
            row.regex = schema['pattern']
        
        if schema.get('enum'):
            row.allowed_values = ', '.join(str(v) for v in schema['enum'])
        
        if schema.get('example') is not None:
            example = schema['example']
            if isinstance(example, (dict, list)):
                import json
                row.example = json.dumps(example)
            else:
                row.example = str(example)
        
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
            
            if '$ref' in schema:
                ref_name = self._extract_ref_name(schema['$ref'])
                # Flatten the referenced schema
                rows.extend(self.flatten_schema(ref_name, section=section))
            else:
                # Inline schema
                rows.extend(self.flatten_inline_schema(
                    schema, 
                    name='body',
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
                        description=schema.get('description', '').strip() if schema.get('description') else None  # Get description from schema and strip
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
        if isinstance(value, dict):
            row = FlatRow(
                section='examples',
                name=name,
                parent=parent,
                type='object'
            )
            rows.append(row)
            
            for key, val in value.items():
                if isinstance(val, dict):
                    self._flatten_example_value(rows, key, val, name)
                elif isinstance(val, list):
                    rows.append(FlatRow(
                        section='examples',
                        name=key,
                        parent=name,
                        type='array',
                        items_type=type(val[0]).__name__ if val else None
                    ))
                else:
                    rows.append(FlatRow(
                        section='examples',
                        name=key,
                        parent=name,
                        type=type(val).__name__ if val is not None else 'string',
                        example=str(val) if val is not None else None
                    ))
        elif isinstance(value, list):
            rows.append(FlatRow(
                section='examples',
                name=name,
                parent=parent,
                type='array'
            ))
        else:
            # Simple scalar values (string, number, etc.)
            rows.append(FlatRow(
                section='examples',
                name=name,
                parent=parent,
                type=_python_type_to_oas(value),
                example=str(value) if value is not None else None
            ))
    
    def _flatten_example_child(self, rows: List[FlatRow], name: str,
                               value: Any, parent: str) -> None:
        """Flatten example child values into rows with section='examples'.
        
        Child values of examples (like 'value', x-sandbox extensions inside examples)
        have section='examples' in the reference xlsm.
        """
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
            # Flatten array items - use array name as parent for item properties, not '-'
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    # Flatten dict properties directly with parent=array_name (e.g. 'errors')
                    for key, val in item.items():
                        self._flatten_example_child(rows, key, val, name)
        else:
            # Simple scalar values (string, number, etc.)
            rows.append(FlatRow(
                section='examples',
                name=name,
                parent=parent,
                type=_python_type_to_oas(value),
                example=str(value) if value is not None else None
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
                        example=str(val) if val is not None else None
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
                example=str(value) if value is not None else None
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
            rows.extend(header_rows)
        
        # Content
        content = response.get('content', {})
        for media_type, media_obj in content.items():
            schema = media_obj.get('schema', {})
            
            if '$ref' in schema:
                ref_name = self._extract_ref_name(schema['$ref'])
                content_rows = self.flatten_schema(ref_name, section='content')
            else:
                content_rows = self.flatten_inline_schema(
                    schema,
                    name='body',
                    section='content'
                )
            rows.extend(content_rows)
            break  # Only first media type
        
        # Links
        for link_name, link_def in response.get('links', {}).items():
            row = FlatRow(
                section='links',
                name=link_name,
                description=link_def.get('description')
            )
            rows.append(row)
        
        return rows
    
    def _flatten_header(self, name: str, header_def: Dict[str, Any]) -> List[FlatRow]:
        """Flatten a header definition."""
        ref_name = None
        
        # Handle top-level $ref (common for headers)
        if '$ref' in header_def:
            ref_name = self._extract_ref_name(header_def['$ref'])
            header_def = self._resolve_ref(header_def['$ref'])
        
        schema = header_def.get('schema', {})
        
        # Also handle schema-level $ref if present
        if not ref_name and '$ref' in schema:
            ref_name = self._extract_ref_name(schema['$ref'])
        
        row = FlatRow(
            name=name,
            description=header_def.get('description'),
            mandatory='M' if header_def.get('required') else 'O'
        )
        
        # Headers always have type='header'
        row.type = 'header'
        
        if ref_name:
            # If it's a reference (e.g. FpadResponseIdentifier), set schema name and clear format
             row.schema_name = ref_name
             row.format = None
        else:
             # Inline definition
             row.format = schema.get('format')
        
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
