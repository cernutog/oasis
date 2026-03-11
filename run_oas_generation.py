
import os
import sys
from src.main import generate_oas

def run_oas_generation():
    input_dir = "Output OAS"
    output_dir = "Output OAS"
    
    if not os.path.exists(input_dir):
        print(f"Error: Input directory not found: {input_dir}")
        return

    print(f"Starting OAS Generation from {input_dir}...")
    generate_oas(
        base_dir=input_dir,
        gen_30=True,
        gen_31=True,
        output_dir=output_dir,
        log_callback=print
    )
    print("\n--- OAS Generation Complete ---")

if __name__ == "__main__":
    run_oas_generation()
