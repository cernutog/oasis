"""Validate Generated OAS YAML."""
import yaml
import sys

filename = 'Imported Templates/generated/generated_oas_3.1.yaml'
try:
    with open(filename, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    print("YAML is valid.")
    # Check if duplicate keys logic is enforced by safe_load? 
    # Standard PyYAML safe_load usually allows duplicates (last one wins) or might error depending on loader.
    # To be strict, we can use a custom loader or just assume if it parses and looks right, it's okay.
    # Actually, let's just count occurrences of keys in specific blocks if needed.
    
    # Check strictly for duplicate keys
    class UniqueKeyLoader(yaml.SafeLoader):
        def construct_mapping(self, node, deep=False):
            mapping = set()
            for key_node, value_node in node.value:
                key = self.construct_object(key_node, deep=deep)
                if key in mapping:
                    raise yaml.constructor.ConstructorError(None, None, f"duplicate key '{key}'", key_node.start_mark)
                mapping.add(key)
            return super().construct_mapping(node, deep)

    with open(filename, 'r', encoding='utf-8') as f:
        yaml.load(f, Loader=UniqueKeyLoader)
    print("Strict YAML check passed (no duplicate keys).")

except Exception as e:
    print(f"YAML Validation Failed: {e}")
    sys.exit(1)
