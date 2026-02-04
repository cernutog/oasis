
import os
import subprocess
import sys

def run_conversion():
    print("Running conversion...")
    result = subprocess.run([sys.executable, "run_legacy_conversion.py"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Conversion failed:\n{result.stderr}")
        return False
    print("Conversion successful.")
    return True

def run_generation():
    print("Running generation...")
    result = subprocess.run([sys.executable, "run_oas_generation.py"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Generation failed:\n{result.stderr}")
        return False
    print("Generation successful.")
    return True

def inspect_results():
    print("Inspecting results...")
    result = subprocess.run([sys.executable, "inspect_converted.py"], capture_output=True, text=True)
    print(result.stdout)
    
    result = subprocess.run([sys.executable, "inspect_operations.py"], capture_output=True, text=True)
    print(result.stdout)

if __name__ == "__main__":
    if run_conversion():
        if run_generation():
            inspect_results()
