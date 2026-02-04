
import os
import sys
import pandas as pd
from src.legacy_converter import LegacyConverter

def run_legacy_conversion():
    input_dir = "Templates Legacy"
    output_dir = "Output Legacy"
    index_path = os.path.join(input_dir, "$index.xlsm")
    
    if not os.path.exists(index_path):
        print(f"Error: Index not found at {index_path}")
        return

    print(f"Initializing LegacyConverter with index from: {input_dir}")
    converter = LegacyConverter(
        legacy_dir=input_dir,
        output_dir=output_dir,
        log_callback=print
    )

    print("Running full conversion...")
    converter.convert()
    
    print("\n--- Conversion Complete ---")

if __name__ == "__main__":
    run_legacy_conversion()
