import sys
import os
import yaml
from collections import OrderedDict

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from generator import OASGenerator

def verify_ordering():
    gen = OASGenerator("3.0.0")
    
    # Manually construct an OAS structure where 'example' is added BEFORE 'properties'
    # In a standard dict, insertion order is preserved.
    # We want to ensure that even if we insert 'example' first, it comes out last.
    
    schema = OrderedDict()
    schema["type"] = "object"
    schema["description"] = "Test Schema"
    schema["example"] = {"foo": "bar"} # Inserted EARLY
    schema["title"] = "TestTitle"
    schema["properties"] = {
        "prop1": {"type": "string"}
    }
    schema["required"] = ["prop1"]
    
    gen.oas = {
        "openapi": "3.0.0",
        "info": {"title": "Test", "version": "1.0"},
        "components": {
            "schemas": {
                "TestObject": schema
            }
        }
    }
    
    # TEST CASE 2: InvestigationTransactionData (Mimicking user's structure)
    schema2 = OrderedDict()
    schema2["type"] = "object"
    schema2["description"] = "Basic structure..."
    schema2["example"] = {
        "instructingAgentBic": "FPADITMM",
        "serviceType": "SCT"
    }
    schema2["title"] = "InvestigationTransactionData"
    schema2["properties"] = {
        "instructingAgentBic": {"allOf": [{"$ref": "..."}]},
        "serviceType": {"$ref": "..."}
    }
    schema2["required"] = ["serviceType"]

    gen.oas["components"]["schemas"]["InvestigationTransactionData"] = schema2
    
    # Generate YAML
    yaml_out = gen.get_yaml()
    
    print("--- GENERATED YAML START ---")
    print(yaml_out)
    print("--- GENERATED YAML END ---")
    
    # Check lines for InvestigationTransactionData
    lines = yaml_out.split('\n')
    
    def check_schema(name):
        print(f"\nChecking {name}...")
        start_idx = -1
        for i, line in enumerate(lines):
            if f"{name}:" in line:
                start_idx = i
                break
        
        if start_idx == -1:
            print(f"FAILURE: {name} not found.")
            sys.exit(1)
            
        prop_idx = -1
        example_idx = -1
        title_idx = -1
        
        # Scan until next schema (indentation check)
        parent_indent = lines[start_idx].find(name)
        
        for i in range(start_idx + 1, len(lines)):
            line = lines[i]
            if not line.strip(): continue
            curr_indent = len(line) - len(line.lstrip())
            if curr_indent <= parent_indent: break # End of schema
            
            if "properties:" in line:
                prop_idx = i
            if "example:" in line:
                example_idx = i
            if "title:" in line:
                title_idx = i
        
        print(f"Properties: {prop_idx}")
        print(f"Example: {example_idx}")
        
        if example_idx > prop_idx and example_idx > title_idx:
            print(f"SUCCESS for {name}: 'example' is at the end.")
        else:
            print(f"FAILURE for {name}: 'example' is NOT at the end.")
            sys.exit(1)

    check_schema("TestObject")
    check_schema("InvestigationTransactionData")

if __name__ == "__main__":
    verify_ordering()
