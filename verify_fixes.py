
import yaml

yaml_path = "API Templates/generated/generated_oas_3.1.yaml"

with open(yaml_path, 'r') as f:
    oas = yaml.safe_load(f)

print("--- Verifying GET Operations ---")
errors_found = False
for path, methods in oas.get("paths", {}).items():
    if "get" in methods:
        op = methods["get"]
        if "requestBody" in op:
            print(f"FAILURE: GET {path} has requestBody")
            errors_found = True
        else:
             print(f"PASS: GET {path} has no requestBody")

if not errors_found:
    print("SUCCESS: No GET operations have requestBody.")

print("\n--- Verifying Array oneOf ---")
# Looking for 'VopBulkResponse' or similar containing 'outcome'
# Or just scan all schemas for array items with oneOf
schemas = oas.get("components", {}).get("schemas", {})
found_oneof = False

for name, schema in schemas.items():
    props = schema.get("properties", {})
    if "outcome" in props:
        outcome = props["outcome"]
        if outcome.get("type") == "array":
             items = outcome.get("items", {})
             if "oneOf" in items:
                 print(f"PASS: Schema '{name}' property 'outcome' uses oneOf: {items['oneOf']}")
                 found_oneof = True
             else:
                 print(f"CHECK: Schema '{name}' property 'outcome' items: {items}")

if not found_oneof:
    print("WARNING: Did not find any schema with 'outcome' array using oneOf. Check if VopBulkResponse exists.")
else:
    print("SUCCESS: Found array with oneOf items.")
