import sys
import os
import re

# Add src to path
sys.path.insert(0, os.path.abspath('src'))

import yaml
from oas_diff.resolver import resolve_spec
from oas_diff.compatibility_analyzer import CompatibilityAnalyzer

def analyze_specs(file1, file2):
    print(f"Analyzing {file1} vs {file2}")
    with open(file1, 'r', encoding='utf-8') as f:
        s1 = yaml.safe_load(f)
    with open(file2, 'r', encoding='utf-8') as f:
        s2 = yaml.safe_load(f)

    r1 = resolve_spec(s1)
    r2 = resolve_spec(s2)

    analyzer = CompatibilityAnalyzer(r1, r2)
    issues = analyzer.analyze()

    lac_issues = [i for i in issues if 'LacAmount' in str(i.schema_name)]
    
    print(f"Total LacAmount issues: {len(lac_issues)}")
    for idx, i in enumerate(lac_issues):
        print(f"ISSUE {idx+1}:")
        print(f"  Location: {i.location}")
        print(f"  Item Name (Prefix): {i.item_name}")
        print(f"  Current Schema (Scope): {i.schema_name}")
        print(f"  Details: {i.details}")
        print(f"  Old Val: {str(i.old_val)[:50]}...")
        print(f"  New Val: {str(i.new_val)[:50]}...")
        print("-" * 20)

    # Find LacAmount schema in resolved specs to see its structure
    # We check components/schemas
    def find_lac(spec):
        # The resolver flattens and returns a dict mapping paths.
        # But where are the components?
        # Resolver:
        # self.components = spec.get('components', {})
        # resolve() returns resolved_paths.
        # It doesn't return resolved components!
        pass

    # Let's inspect the analyzer's spec1/spec2 which are resolved results
    # They are dicts mapping 'path' -> resolved_node
    for path, node in r1.items():
        # Search for LacAmount in the node (schema)
        node_str = str(node)
        if 'LacAmount' in node_str:
            print(f"Found LacAmount in path: {path}")
            # Differentiate by finding where x-ref contains LacAmount
            def find_node_with_xref(n, target, visited=None):
                if visited is None: visited = set()
                if id(n) in visited: return None
                visited.add(id(n))
                if isinstance(n, dict):
                    xref = n.get('x-ref', '')
                    if target in xref: return n
                    for k, v in n.items():
                        res = find_node_with_xref(v, target, visited)
                        if res: return res
                elif isinstance(n, list):
                    for item in n:
                        res = find_node_with_xref(item, target, visited)
                        if res: return res
                return None

            lac_node = find_node_with_xref(node, 'LacAmount')
            if lac_node:
                print("LacAmount Node Structure (first 500 chars):")
                print(str(lac_node)[:500])
                break

if __name__ == "__main__":
    # We need the actual files being compared
    # I'll try to find them from the current state or workspace
    # Usually they are in 'Output OAS' or defined in prefs.
    # I'll search for likely files.
    yamls = []
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f.endswith('.yaml'):
                yamls.append(os.path.join(root, f))
    
    # Try to find a pair from a likely location
    # Swift specs often have version numbers
    potential_pairs = []
    for i in range(len(yamls)):
        for j in range(i + 1, len(yamls)):
            if 'generated_oas' in yamls[i] and 'generated_oas' in yamls[j]:
                potential_pairs.append((yamls[i], yamls[j]))

    if potential_pairs:
        analyze_specs(potential_pairs[0][0], potential_pairs[0][1])
    else:
        print("No paired yaml specs found for analysis.")
