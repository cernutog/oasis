"""Generate OAS 3.1 from Imported Templates."""
import sys
import os

# Ensure src is in path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from src.main import generate_oas

def main():
    print("Generating OAS from Imported Templates...")
    try:
        generate_oas(
            base_dir=os.path.join(os.getcwd(), 'Imported Templates'),
            gen_30=False,
            gen_31=True,
            gen_swift=False,
            log_callback=print
        )
        print("Generation complete.")
    except Exception as e:
        print(f"Generation failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
