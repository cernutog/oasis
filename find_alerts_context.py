
import yaml
import sys

def find_context(path, query, context=5):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines):
        if query in line:
            start = max(0, i - context)
            end = min(len(lines), i + context + 1)
            print(f"--- Line {i+1} ---")
            for j in range(start, end):
                print(f"{j+1}: {lines[j].rstrip()}")
            print("-" * 20)

if __name__ == "__main__":
    path = r"C:\Users\giuse\Downloads\EBACL_STEP2_20250507_Openapi3.1_CGS-DKK_API_Participants_2_0_v20251006.yaml"
    find_context(path, "/Alerts")
    find_context(path, "Alerts:")
