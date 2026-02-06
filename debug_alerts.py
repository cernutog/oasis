
from src.v3_parser import V3Parser
from src.v3_modeling import V3Modeler
from src.v3_naming_mod import V3Harmonizer
import json

def debug_alerts():
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
    
    print("\n=== ALERTS DUPLICATE ANALYSIS ===")
    targets = [n for n in graph.global_schemas if "Alerts" in n.name] # Case sensitive check for Alerts, Alerts1 etc.
    
    for n in targets:
        print(f"\n--- Node: '{n.name}' ---")
        h = harmonizer._calculate_deep_hash(n)
        print(f"Hash: {h}")
        print(f"Type: {n.type_literal}")
        print(f"Props: {[p.name for p in n.properties]}")
        # Print first prop type to see if deep structure differs
        if n.properties:
            p0 = n.properties[0]
            print(f"Prop '{p0.name}' Type: {p0.type_literal}")

if __name__ == "__main__":
    debug_alerts()
