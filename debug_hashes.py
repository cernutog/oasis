
import logging
from src.v3_parser import V3Parser
from src.v3_modeling import V3Modeler
from src.v3_naming import V3Harmonizer

def debug_hashes():
    # 1. Parse & Model
    print("Parsing templates...")
    # V3Parser(source_dir) - only one argument
    parser = V3Parser("Templates Legacy")
    
    raw_data = parser.parse_all()
    modeler = V3Modeler(raw_data)
    graph = modeler.build_graph()
    
    print(f"Graph built. Global Schemas: {len(graph.global_schemas)}")
    print("Global Schema Names:", [n.name for n in graph.global_schemas])
    
    # Find Alerts in Globals (Case Insensitive)
    global_alerts = next((n for n in graph.global_schemas if n.name.lower() == "alerts"), None)
    if not global_alerts:
        print("CRITICAL: Alerts not found in Global Schemas!")
        return

    # Find Alerts in Operations (listAlerts)
    op = graph.operations.get("listAlerts")
    if not op:
        print("CRITICAL: listAlerts operation not found!")
        return
        
    # In listAlertsRequest (Body), we expect an 'alerts' property that IS the Alerts object?
    # Or is listAlertsResponse?
    # Typically listAlertsResponse returns [Alerts].
    
    # Let's verify response 200
    resp200 = op.responses.get("200")
    if not resp200:
        print("CRITICAL: Response 200 not found for listAlerts")
        return
        
    # Traverse to find 'alerts' node or similar
    # Response 200 -> alerts (array) -> items (Alerts object)
    # OR Response 200 -> Alerts (if it's direct list?)
    
    target_nested = None
    
    # Recursive searcher
    def find_alerts_node(node):
        if node.name.lower() == "alerts" or node.type_literal.lower() == "alerts":
            return node
        if node.properties:
            for p in node.properties:
                res = find_alerts_node(p)
                if res: return res
        return None

    target_nested = find_alerts_node(resp200)
    
    if not target_nested:
        print("Could not find nested 'Alerts' node in listAlerts response.")
        # Try request?
        target_nested = find_alerts_node(op.request)
        
    if not target_nested:
        print("Could not find nested 'Alerts' node ANYWHERE.")
        return

    print("\n=== HASH DEBUG ===")
    harmonizer = V3Harmonizer(graph)
    
    # Compute Hash for Global (Simulation of Phase 1)
    # Note: Phase 1 happens on RAW nodes (before recusion).
    # Phase 2 recurses.
    
    # We need to simulate exactly what Harmonizer does.
    # Harmonizer._calculate_deep_hash uses current node state.
    
    h_global = harmonizer._calculate_deep_hash(global_alerts)
    print(f"Global Alerts Hash: {h_global}")
    print(f"Global Props Content:")
    for p in global_alerts.properties:
        print(f"  - Name: {p.name}, Type: {p.type_literal}, Mand: {p.mandatory}, Fmt: {p.format}, Enum: {p.allowed_values}")

    print("\n---")
    
    # For nested, we must simulate "Phase 2 recursion" which MUTATES the node (camelCase lookup)
    # We can't easily undo mutation, so let's just print current state
    # But wait, we haven't run harmonizer yet, so nodes are "raw" from Modeler.
    
    # Modeler creates tree. 
    # Global Alerts properties have types like "DateTime", "EventType".
    # Nested Alerts properties have types like "dateTime", "eventType" (if from Ops sheet)?
    # Or "DateTime" if referenced?
    
    print(f"Nested Alerts Hash (Pre-Harmonization): {harmonizer._calculate_deep_hash(target_nested)}")
    print(f"Nested Props Content:")
    for p in target_nested.properties:
        print(f"  - Name: {p.name}, Type: {p.type_literal}, Mand: {p.mandatory}, Fmt: {p.format}, Enum: {p.allowed_values}")

if __name__ == "__main__":
    debug_hashes()
