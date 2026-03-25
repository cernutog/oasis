import os
import sys

# Add src to python path 
sys.path.insert(0, r'c:\Users\giuse\.gemini\antigravity\scratch\OASIS\src')

import yaml
from oas_diff.resolver import resolve_spec
from oas_diff.compatibility_analyzer import CompatibilityAnalyzer

print("Loading specs...")
# Let's find some specs to run on
spec_files = []
for root, dirs, files in os.walk(r'c:\Users\giuse\.gemini\antigravity\scratch\OASIS'):
    for f in files:
        if f.endswith('.yaml') or f.endswith('.json'):
            spec_files.append(os.path.join(root, f))
    if len(spec_files) > 2: break

if not spec_files:
    print("No specs found to run.")
    sys.exit(0)

print(f"Testing with: {spec_files[0]}")
with open(spec_files[0], 'r', encoding='utf-8') as f:
    s1 = yaml.safe_load(f)

# Use same for both to simulate
r1 = resolve_spec(s1)

analyzer = CompatibilityAnalyzer(r1, r1)
issues = analyzer.analyze()

print(f"Found {len(issues)} issues")
for i in issues:
    if not isinstance(i.schema_name, str):
        print(f"FOUND NON-STRING SCOPE: {type(i.schema_name)} on item_name {i.item_name}")

print("Diagnostic complete.")
