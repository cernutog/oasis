
from src.v3_parser import V3Parser
from src.v3_modeling import V3Modeler
from src.v3_naming_mod import V3Harmonizer
import json

def debug_duplicates():
    # Use Legacy dir
    legacy_dir = "Templates Legacy"
    
    print("Parsing...")
    parser = V3Parser(legacy_dir)
    ir = parser.parse_all()
    
    print("Modeling...")
    modeler = V3Modeler(ir)
    graph = modeler.build_graph()
    
    print("Harmonizing...")
    harmonizer = V3Harmonizer(graph)
    harmonizer.harmonize()
    
    print("\n=== DUPLICATE ANALYSIS ===")
    amounts = [n for n in graph.global_schemas if "Amount" in n.name]
    
    for n in amounts:
        print(f"\n--- Node: '{n.name}' ---")
        h = harmonizer._calculate_deep_hash(n)
        print(f"Hash: {h}")
        print(f"Type: {n.type_literal}")
        print(f"Desc: {n.description}")
        print(f"Format: {n.format}, Min: {n.min_val}, Max: {n.max_val}")
        
    # Check if hashes are identical
    hashes = [harmonizer._calculate_deep_hash(n) for n in amounts]
    if len(hashes) > 1 and len(set(hashes)) < len(hashes):
        print("\nALERT: Identical hashes detected but different names!")
    else:
        print("\nHashes are distinct.")

if __name__ == "__main__":
    debug_duplicates()
