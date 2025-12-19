import os
import sys

# Ensure src is in path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from src.main import generate_oas

def main():
    base_dir = os.path.join(os.getcwd(), 'API Templates')
    print(f"Running generation for: {base_dir}")
    
    generate_oas(
        base_dir=base_dir, 
        gen_30=True, 
        gen_31=True, 
        gen_swift=True, 
        log_callback=print
    )

if __name__ == "__main__":
    main()
