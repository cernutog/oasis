import os
import sys

sys.path.append(os.path.join(os.getcwd(), 'src'))
from src.main import generate_oas

def main():
    base_dir = os.path.join(os.getcwd(), 'Imported Templates')
    out_dir = os.path.join(os.getcwd(), 'OAS Generated') # Standard output
    print(f"Running generation for: {base_dir}")
    
    generate_oas(
        base_dir=base_dir, 
        gen_30=False, 
        gen_31=True, # Focus on 3.1
        gen_swift=False, 
        log_callback=print
    )

if __name__ == "__main__":
    main()
