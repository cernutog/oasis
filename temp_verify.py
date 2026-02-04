
import subprocess
import os

def run_cmd(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"FAILED: {cmd}")
        print(result.stdout)
        print(result.stderr)
        return False
    print(result.stdout)
    return True

def verify_all():
    venv_python = os.path.join(".venv", "Scripts", "python.exe")
    
    # 1. Conversion
    if not run_cmd(f"{venv_python} run_conversion.py"): return
    
    # 2. Generation
    if not run_cmd(f"{venv_python} run_oas_generation.py"): return
    
    # 3. Audit
    if not run_cmd(f"{venv_python} audit_oas_parity.py"): return

if __name__ == "__main__":
    verify_all()
