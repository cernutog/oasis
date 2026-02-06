
from src.v3_parser import V3Parser
from src.v3_modeling import V3Modeler
from src.v3_naming_mod import V3Harmonizer

def debug_final_memory():
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
    
    print("\n=== FINAL GRAPH STATE ===")
    globals = graph.global_schemas
    print(f"Total Global Schemas: {len(globals)}")
    
    # Check Alerts variants
    targets = ["Alerts", "alerts", "Alerts1", "alerts1"]
    found = []
    
    for node in globals:
        if node.name in targets:
            found.append(node)
            print(f"\n--- Found Node: '{node.name}' ---")
            print(f"Type: {node.type_literal}")
            print(f"Hash in Registry: {next((h for h, n in harmonizer.registry.hash_to_name.items() if n == node.name), 'N/A')}")
            print(f"Prop Count: {len(node.properties) if node.properties else 0}")
            if node.properties:
                print("First 3 Props:")
                for p in node.properties[:3]:
                    print(f"  - {p.name} ({p.type_literal})")
            else:
                print("  (No properties)")

    print("\n--- Summary ---")
    print(f"Found targets: {[n.name for n in found]}")

if __name__ == "__main__":
    debug_final_memory()
