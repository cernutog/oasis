"""
OAS Parser Module

Parses OpenAPI Specification (3.0 and 3.1) YAML files and extracts
structured data for Excel template generation.

Usage:
    parser = OASParser('path/to/oas.yaml')
    info = parser.get_info()
    paths = parser.get_paths()
    components = parser.get_components()
"""

import yaml
import os
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from collections import OrderedDict


@dataclass
class ParameterInfo:
    """Represents an OAS parameter."""
    name: str
    location: str  # 'path', 'query', 'header', 'cookie'
    description: Optional[str] = None
    required: bool = False
    schema_type: Optional[str] = None
    schema_ref: Optional[str] = None
    schema_format: Optional[str] = None
    items_type: Optional[str] = None
    minimum: Optional[Any] = None
    maximum: Optional[Any] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    min_items: Optional[int] = None
    max_items: Optional[int] = None
    pattern: Optional[str] = None
    enum: Optional[List[str]] = None
    example: Optional[Any] = None


@dataclass
class SchemaProperty:
    """Represents a property in an OAS schema."""
    name: str
    parent: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    schema_ref: Optional[str] = None
    items_type: Optional[str] = None
    format: Optional[str] = None
    required: bool = False
    minimum: Optional[Any] = None
    maximum: Optional[Any] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    min_items: Optional[int] = None
    max_items: Optional[int] = None
    pattern: Optional[str] = None
    enum: Optional[List[str]] = None
    example: Optional[Any] = None


@dataclass
class ResponseInfo:
    """Represents an OAS response."""
    status_code: str
    description: Optional[str] = None
    headers: List[Dict[str, Any]] = field(default_factory=list)
    content: Dict[str, Any] = field(default_factory=dict)
    links: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OperationInfo:
    """Represents a complete OAS operation."""
    path: str
    method: str
    operation_id: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    parameters: List[ParameterInfo] = field(default_factory=list)
    request_body: Optional[Dict[str, Any]] = None
    responses: Dict[str, ResponseInfo] = field(default_factory=dict)
    extensions: Dict[str, Any] = field(default_factory=dict)


class OASParser:
    """
    Parser for OpenAPI Specification files.
    
    Supports both OAS 3.0 and 3.1 formats.
    """
    
    def __init__(self, filepath: str):
        """
        Initialize parser with an OAS file.
        
        Args:
            filepath: Path to the OAS YAML file
        """
        self.filepath = filepath
        self.oas: Dict[str, Any] = {}
        self._load()
    
    def _load(self) -> None:
        """Load and parse the OAS YAML file."""
        with open(self.filepath, 'r', encoding='utf-8') as f:
            self._raw_content = f.read()
        self.oas = yaml.safe_load(self._raw_content)
    
    @property
    def version(self) -> str:
        """Get the OpenAPI version."""
        return self.oas.get('openapi', '3.0.0')
    
    @property
    def is_3_1(self) -> bool:
        """Check if this is an OAS 3.1 file."""
        return self.version.startswith('3.1')
    
    def get_info(self) -> Dict[str, Any]:
        """
        Extract info object for General Description sheet.
        
        Returns:
            Dict with title, version, description, contact, etc.
        """
        info = self.oas.get('info', {})
        result = {
            'title': info.get('title', 'API'),
            'version': info.get('version', '1.0.0'),
            'description': info.get('description', ''),
        }
        
        # Contact info
        if 'contact' in info:
            contact = info['contact']
            if 'email' in contact:
                result['contact_email'] = contact['email']
            if 'name' in contact:
                result['contact_name'] = contact['name']
            if 'url' in contact:
                result['contact_url'] = contact['url']
        
        # License
        if 'license' in info:
            result['license'] = info['license'].get('name', '')
        
        return result
    
    def get_servers(self) -> List[Dict[str, str]]:
        """
        Extract servers list.
        
        Returns:
            List of server objects with url and description
        """
        servers = self.oas.get('servers', [])
        return [{'url': s.get('url', ''), 'description': s.get('description', '')} 
                for s in servers]
    
    def get_tags(self) -> List[Dict[str, str]]:
        """
        Extract tags list.
        
        Returns:
            List of tag objects with name and description
        """
        tags = self.oas.get('tags', [])
        return [{'name': t.get('name', ''), 'description': t.get('description', '')} 
                for t in tags]
    
    def get_security_schemes(self) -> Dict[str, Dict[str, Any]]:
        """
        Extract security schemes from components.
        
        Returns:
            Dict of security scheme definitions
        """
        return self.oas.get('components', {}).get('securitySchemes', {})
    
    def get_operations(self) -> List[OperationInfo]:
        """
        Extract all operations from paths.
        
        Returns:
            List of OperationInfo dataclasses
        """
        operations = []
        paths = self.oas.get('paths', {})
        
        for path, path_item in paths.items():
            # Handle common parameters at path level
            path_params = path_item.get('parameters', [])
            
            for method in ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']:
                if method in path_item:
                    op_data = path_item[method]
                    operation = self._parse_operation(path, method, op_data, path_params)
                    operations.append(operation)
        
        return operations
    
    def _parse_operation(self, path: str, method: str, op_data: Dict, 
                         path_params: List[Dict]) -> OperationInfo:
        """Parse a single operation into OperationInfo."""
        operation = OperationInfo(
            path=path,
            method=method.upper(),
            operation_id=op_data.get('operationId'),
            summary=op_data.get('summary'),
            description=op_data.get('description'),
            tags=op_data.get('tags', [])
        )
        
        # Merge path-level and operation-level parameters
        all_params = path_params + op_data.get('parameters', [])
        operation.parameters = [self._parse_parameter(p) for p in all_params]
        
        # Request body
        if 'requestBody' in op_data:
            operation.request_body = op_data['requestBody']
        
        # Responses
        for status_code, resp_data in op_data.get('responses', {}).items():
            operation.responses[status_code] = self._parse_response(status_code, resp_data)
        
        # Extract custom extensions (x-*)
        for key, value in op_data.items():
            if key.startswith('x-'):
                operation.extensions[key] = value
        
        return operation
    
    def _parse_parameter(self, param_data: Dict) -> ParameterInfo:
        """Parse a parameter definition."""
        # Handle $ref
        if '$ref' in param_data:
            param_data = self._resolve_ref(param_data['$ref'])
        
        schema = param_data.get('schema', {})
        
        param = ParameterInfo(
            name=param_data.get('name', ''),
            location=param_data.get('in', ''),
            description=param_data.get('description'),
            required=param_data.get('required', False)
        )
        
        # Schema properties
        if '$ref' in schema:
            param.schema_ref = self._extract_ref_name(schema['$ref'])
        else:
            param.schema_type = schema.get('type')
            param.schema_format = schema.get('format')
            
            if schema.get('type') == 'array' and 'items' in schema:
                items = schema['items']
                if '$ref' in items:
                    param.items_type = self._extract_ref_name(items['$ref'])
                else:
                    param.items_type = items.get('type')
            
            # Constraints
            param.minimum = schema.get('minimum')
            param.maximum = schema.get('maximum')
            param.min_length = schema.get('minLength')
            param.max_length = schema.get('maxLength')
            param.min_items = schema.get('minItems')
            param.max_items = schema.get('maxItems')
            param.pattern = schema.get('pattern')
            param.enum = schema.get('enum')
        
        param.example = param_data.get('example') or schema.get('example')
        
        return param
    
    def _parse_response(self, status_code: str, resp_data: Dict) -> ResponseInfo:
        """Parse a response definition."""
        # Handle $ref
        if '$ref' in resp_data:
            resp_data = self._resolve_ref(resp_data['$ref'])
        
        response = ResponseInfo(
            status_code=status_code,
            description=resp_data.get('description')
        )
        
        # Headers
        for header_name, header_data in resp_data.get('headers', {}).items():
            response.headers.append({
                'name': header_name,
                **header_data
            })
        
        # Content
        response.content = resp_data.get('content', {})
        
        # Links
        response.links = resp_data.get('links', {})
        
        return response
    
    def _resolve_ref(self, ref: str) -> Dict[str, Any]:
        """
        Resolve a $ref to its actual definition.
        
        Args:
            ref: Reference string like '#/components/schemas/MySchema'
            
        Returns:
            The resolved definition dict
        """
        if not ref.startswith('#/'):
            # External refs not supported yet
            return {}
        
        parts = ref[2:].split('/')
        result = self.oas
        for part in parts:
            result = result.get(part, {})
        return result
    
    def _extract_ref_name(self, ref: str) -> str:
        """Extract the name from a $ref string."""
        return ref.split('/')[-1]
    
    def get_components(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all components.
        
        Returns:
            Dict with schemas, parameters, headers, responses, etc.
        """
        return self.oas.get('components', {})
    
    def get_raw_extensions(self, path: str, method: str) -> str:
        """
        Extract raw custom extensions text from OAS file for a specific operation.
        
        This extracts the exact text from the file to preserve formatting (literal blocks),
        but removes the common indentation so it fits cleanly into Excel.
        """
        if not hasattr(self, '_raw_content'):
            return ""

        lines = self._raw_content.split('\n')
        
        # State machine to find the specific operation
        in_path = False
        in_method = False
        extensions_lines = []
        collecting = False
        base_indent = None
        
        path_indent = -1
        method_indent = -1
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                if collecting:
                     extensions_lines.append(line)
                continue
                
            indent = len(line) - len(line.lstrip())
            
            # Find Path
            if not in_path and stripped.startswith(f"'{path}':"): # YAML path keys are often quoted
                 path_indent = indent
                 in_path = True
                 continue
            if not in_path and stripped.startswith(f"{path}:"):
                 path_indent = indent
                 in_path = True
                 continue
            
            if in_path:
                # Check if we left the path
                if indent <= path_indent and not collecting:
                    in_path = False
                    continue
                
                # Find Method
                if not in_method:
                    target_method = method.lower()
                    if stripped.startswith(f"{target_method}:") or stripped.startswith(f"'{target_method}':"):
                        method_indent = indent
                        in_method = True
                        continue
                
                if in_method:
                    # Check if we left the method
                    if indent <= method_indent and not collecting:
                         in_method = False
                         # If we left the method we wanted, we are done
                         break
                    
                    # Look for extensions
                    if stripped.startswith('x-'):
                        if not collecting:
                            collecting = True
                            base_indent = indent
                        extensions_lines.append(line)
                        continue
                    
                    if collecting:
                        # If we are collecting, we continue until indentation drops below extension level
                        # OR we encounter a new key at the same level as extensions (that isn't an extension)
                        if indent < base_indent:
                            collecting = False
                            # Only break if we are sure we left the method? 
                            # Actually extensions usually come at the end or together. 
                            # But we might have other keys after. 
                            # If indentation matches method_indent, it's a sibling key.
                            if indent <= method_indent:
                                break
                        elif indent == base_indent and not stripped.startswith('x-'):
                            collecting = False
                            continue # Sibling key, not extension
                        else:
                             extensions_lines.append(line)

        if not extensions_lines:
            return ""
            
        # Normalize indentation (remove common prefix)
        # Calculate min common indent (ignoring empty lines)
        common_indent = 1000
        for line in extensions_lines:
            if line.strip():
                ind = len(line) - len(line.lstrip())
                if ind < common_indent:
                    common_indent = ind
        
        if common_indent == 1000:
            return "\n".join(extensions_lines)
            
        trimmed_lines = []
        for line in extensions_lines:
            if len(line) >= common_indent:
                trimmed_lines.append(line[common_indent:])
            else:
                trimmed_lines.append(line)
                
        return "\n".join(trimmed_lines).strip()

    def get_schemas(self) -> Dict[str, Dict[str, Any]]:
        """Get all schemas from components."""
        return self.get_components().get('schemas', {})
    
    def get_global_parameters(self) -> Dict[str, Dict[str, Any]]:
        """Get all global parameters from components."""
        return self.get_components().get('parameters', {})
    
    def get_global_headers(self) -> Dict[str, Dict[str, Any]]:
        """Get all global headers from components."""
        return self.get_components().get('headers', {})
    
    def get_global_responses(self) -> Dict[str, Dict[str, Any]]:
        """Get all global responses from components."""
        return self.get_components().get('responses', {})
    
    def flatten_schema(self, schema_name: str, schema: Dict[str, Any], 
                       parent: Optional[str] = None) -> List[SchemaProperty]:
        """
        Flatten a nested schema into a list of properties.
        
        Args:
            schema_name: Name of the root schema
            schema: The schema definition
            parent: Parent property name for nested properties
            
        Returns:
            List of SchemaProperty objects
        """
        properties = []
        required_props = set(schema.get('required', []))
        
        # Handle combinators
        for combinator in ['allOf', 'anyOf', 'oneOf']:
            if combinator in schema:
                # Add a property row for the combinator
                prop = SchemaProperty(
                    name=schema_name if not parent else f"{parent}.{schema_name}",
                    parent=parent,
                    type=combinator
                )
                # Collect schema refs
                refs = []
                for item in schema[combinator]:
                    if '$ref' in item:
                        refs.append(self._extract_ref_name(item['$ref']))
                if refs:
                    prop.schema_ref = ', '.join(refs)
                properties.append(prop)
                return properties
        
        # Handle $ref at schema level
        if '$ref' in schema:
            return [SchemaProperty(
                name=schema_name,
                parent=parent,
                type='schema',
                schema_ref=self._extract_ref_name(schema['$ref'])
            )]
        
        # Handle object properties
        for prop_name, prop_schema in schema.get('properties', {}).items():
            prop = self._schema_to_property(
                prop_name, 
                prop_schema, 
                parent=schema_name,
                required=prop_name in required_props
            )
            properties.append(prop)
            
            # Recurse for nested objects
            if prop_schema.get('type') == 'object' and 'properties' in prop_schema:
                nested = self.flatten_schema(prop_name, prop_schema, parent=schema_name)
                properties.extend(nested)
        
        return properties
    
    def _schema_to_property(self, name: str, schema: Dict[str, Any], 
                            parent: Optional[str] = None,
                            required: bool = False) -> SchemaProperty:
        """Convert a schema definition to SchemaProperty."""
        prop = SchemaProperty(
            name=name,
            parent=parent,
            description=schema.get('description'),
            required=required
        )
        
        if '$ref' in schema:
            prop.type = 'schema'
            prop.schema_ref = self._extract_ref_name(schema['$ref'])
        else:
            prop.type = schema.get('type')
            prop.format = schema.get('format')
            
            # Array items
            if schema.get('type') == 'array' and 'items' in schema:
                items = schema['items']
                if '$ref' in items:
                    prop.items_type = 'schema'
                    prop.schema_ref = self._extract_ref_name(items['$ref'])
                else:
                    prop.items_type = items.get('type')
            
            # Constraints
            prop.minimum = schema.get('minimum')
            prop.maximum = schema.get('maximum')
            prop.min_length = schema.get('minLength')
            prop.max_length = schema.get('maxLength')
            prop.min_items = schema.get('minItems')
            prop.max_items = schema.get('maxItems')
            prop.pattern = schema.get('pattern')
            prop.enum = schema.get('enum')
            prop.example = schema.get('example')
        
        return prop


def main():
    """Test the OAS parser."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python oas_parser.py <oas_file>")
        sys.exit(1)
    
    parser = OASParser(sys.argv[1])
    
    print(f"OpenAPI Version: {parser.version}")
    print(f"Info: {parser.get_info()}")
    print(f"Tags: {parser.get_tags()}")
    print(f"Servers: {parser.get_servers()}")
    
    operations = parser.get_operations()
    print(f"\nOperations ({len(operations)}):")
    for op in operations:
        print(f"  {op.method} {op.path} - {op.operation_id}")
        print(f"    Tags: {op.tags}")
        print(f"    Parameters: {len(op.parameters)}")
        print(f"    Responses: {list(op.responses.keys())}")
        if op.extensions:
            print(f"    Extensions: {list(op.extensions.keys())}")
    
    schemas = parser.get_schemas()
    print(f"\nSchemas ({len(schemas)}): {list(schemas.keys())[:5]}...")


if __name__ == '__main__':
    main()
