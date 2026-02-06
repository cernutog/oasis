
import os
import time
from src.v3_parser import V3Parser
from src.v3_modeling import V3Modeler
from src.v3_naming_mod import V3Harmonizer
from src.v3_writer import V3Writer

def main():
    start_time = time.time()
    
    legacy_dir = "Templates Legacy"
    master_dir = "Templates Master"
    output_dir = "Templates Converted V3"
    
    print("--- Legacy Converter v3.0: Esecuzione Pipeline ---")
    
    # 1. Extraction
    print("[1/4] Estrazione (Parser)...")
    parser = V3Parser(legacy_dir)
    ir = parser.parse_all()
    
    # 2. Modeling
    print("[2/4] Modellazione (Hoisting)...")
    modeler = V3Modeler(ir)
    graph = modeler.build_graph()
    
    # 3. Harmonization
    print("[3/4] Armonizzazione (Naming & Deduplicazione)...")
    harmonizer = V3Harmonizer(graph)
    harmonizer.harmonize()
    
    # 4. Writing
    print("[4/4] Esportazione (Excel Writer)...")
    writer = V3Writer(graph, master_dir)
    writer.write_all(output_dir)
    
    duration = time.time() - start_time
    print(f"\nConversione completata in {duration:.2f} secondi.")
    print(f"I file sono disponibili in: {output_dir}")

if __name__ == "__main__":
    main()
