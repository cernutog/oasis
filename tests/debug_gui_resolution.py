import json

# Load the source map we generated
with open("test_source_map.json", "r") as f:
    source_map = json.load(f)

# Simulate Spectral paths from the screenshot
spectral_paths = [
    "info",  # info-contact warning, Path: info
    "paths > /vop/v1/payee-information > post",  # operation-tags
    "paths > /vop/v1/payee-verifications > post",  # operation-tags
    "paths > /vop/v1/health-check > get",  # operation-tags
]

print("=== Simulating GUI Path Resolution ===\n")

for spectral_path in spectral_paths:
    print(f"Spectral Path: {spectral_path}")
    
    # Convert to dot notation (as GUI does)
    clean_path = spectral_path.replace(" > ", ".")
    clean_path = clean_path.replace("Root.", "")
    print(f"Cleaned Path: {clean_path}")
    
    # Try to resolve (as GUI does)
    keys = clean_path.split(".")
    found = None
    
    while keys:
        current_path = ".".join(keys)
        if current_path in source_map:
            found = source_map[current_path]
            print(f"  [OK] Found: {current_path}")
            print(f"    File: {found['file']}")
            print(f"    Sheet: {found['sheet']}")
            break
        keys.pop()
    
    if not found:
        print(f"  [MISSING] NOT FOUND in source map")
    
    print()

# Show what keys are actually in the source map for paths
print("\n=== Paths Keys in Source Map ===")
for key in sorted(source_map.keys()):
    if key.startswith("paths."):
        print(f"  {key}")
