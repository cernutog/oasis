
import os
import sys

# Add src to path
sys.path.append(os.path.abspath("src"))
from legacy_converter import LegacyConverter

legacy_dir = r"c:\Users\giuse\.gemini\antigravity\scratch\OASIS\Templates Legacy"
output_dir = r"c:\Users\giuse\.gemini\antigravity\scratch\OASIS\Templates Converted Test"

conv = LegacyConverter(legacy_dir, output_dir)
conv.convert()

print("\n--- GLOBAL REGISTRY KEYS ---")
for k in sorted(conv.global_registry.keys()):
    print(f"'{k}'")

print("\n--- USED SCHEMAS PAIRS ---")
for pair in sorted(list(conv.used_global_schemas)):
    if "Amount" in pair[0]:
        print(pair)
