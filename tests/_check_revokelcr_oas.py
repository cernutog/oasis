"""
Check what's in the generated OAS for revokeLcr
"""
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import yaml

# Read the generated OAS file
oas_path = ROOT / "OAS Generated Test" / "revokeLcr.230301.yaml"

if oas_path.exists():
    print(f"=== Checking {oas_path.name} ===")
    
    with open(oas_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"\n=== Full OAS Content ===")
    print(content)
    
    # Look for request body schema
    print(f"\n=== Looking for request body schema ===")
    lines = content.splitlines()
    in_request_body = False
    in_schema = False
    
    for i, line in enumerate(lines):
        if 'requestBody:' in line:
            in_request_body = True
            print(f"Line {i+1}: {line}")
        elif in_request_body and 'schema:' in line:
            in_schema = True
            print(f"Line {i+1}: {line}")
        elif in_request_body and line.strip().startswith('$ref:'):
            print(f"Line {i+1}: {line}")
            # Try to find the referenced schema
            ref = line.split('#/components/schemas/')[-1].strip()
            print(f"  -> Looking for schema: {ref}")
            
            # Find the schema in components
            for j, comp_line in enumerate(lines):
                if f"{ref}:" in comp_line:
                    print(f"Found schema at line {j+1}:")
                    # Print the schema definition
                    k = j + 1
                    indent_level = len(comp_line) - len(comp_line.lstrip())
                    while k < len(lines):
                        schema_line = lines[k]
                        if schema_line.strip() == '':
                            k += 1
                            continue
                        current_indent = len(schema_line) - len(schema_line.lstrip())
                        if current_indent <= indent_level and schema_line.strip() and not schema_line.strip().startswith('-'):
                            break
                        print(f"  Line {k+1}: {schema_line}")
                        k += 1
                    break
        elif in_request_body and line.strip() and not line.startswith(' '):
            in_request_body = False
            in_schema = False
else:
    print(f"OAS file not found: {oas_path}")
