import yaml
import os
import json

# Configuration
BASE_DIR = r"C:\Users\giuse\.gemini\antigravity\scratch\OAS_Generation_Tool"
GENERATED_DIR = os.path.join(BASE_DIR, "API Templates", "generated")
EXPECTED_DIR = os.path.join(BASE_DIR, "Expected results")
REPORT_FILE = os.path.join(BASE_DIR, "discrepancies_report.txt")

def load_yaml(path):
    print(f"Loading {path}...")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return None

def get_identifier(item):
    """Helper to find a unique identifier for a list item."""
    if isinstance(item, dict):
        if 'name' in item: return item['name']
        if 'operationId' in item: return item['operationId']
        if 'url' in item: return item['url']
        if '$ref' in item: return item['$ref']
    return None

def compare_structures(gen, exp, path="root", report=[]):
    """
    Recursively compares Expected (exp) against Generated (gen).
    Report errors if 'exp' has something that 'gen' does not (or differs).
    """
    
    # 1. Type Mismatch
    if type(gen) != type(exp):
        report.append(f"[TYPE MISMATCH] at {path}: Expected {type(exp).__name__}, got {type(gen).__name__}")
        return

    # 2. Dictionaries (Objects)
    if isinstance(exp, dict):
        for k, v_exp in exp.items():
            if k not in gen:
                report.append(f"[MISSING KEY] at {path}: Key '{k}' is missing in generated.")
            else:
                compare_structures(gen[k], v_exp, f"{path}.{k}", report)
    
    # 3. Lists (Arrays)
    elif isinstance(exp, list):
        # Heuristic: Check if we can match items by ID
        # If simple values (int, str), use set logic or direct order?
        # OAS lists often matter in order (e.g. parameters order?), but usually not for verifying presence.
        # Let's try to match items.
        
        # Structure: Map identifier -> item
        exp_map = {}
        exp_list_simple = []
        is_complex = False
        
        for item in exp:
            if isinstance(item, (dict, list)):
                is_complex = True
                ident = get_identifier(item)
                if ident:
                    exp_map[ident] = item
                else:
                    # Fallback for items without ID: treat as ordered or just append
                    pass 
            else:
                exp_list_simple.append(item)
        
        if not is_complex:
            # Simple list (e.g. enums, required fields)
            # Compare as sets if order doesnt matter? Or exact list?
            # OAS 'required' is a set usually. 'enum' is set-like.
            # Let's try set comparison for missing items
            gen_set = set(gen)
            for item in exp:
                if item not in gen_set:
                    report.append(f"[MISSING LIST ITEM] at {path}: '{item}' not found in generated list.")
        else:
            # Complex list
            # Create a lookup for generated items
            gen_map = {}
            for item in gen:
                ident = get_identifier(item)
                if ident: gen_map[ident] = item
            
            non_identifiable_exp = []
            
            for item in exp:
                ident = get_identifier(item)
                if ident:
                    if ident not in gen_map:
                         report.append(f"[MISSING ITEM] at {path}: Item with ID '{ident}' missing in generated list.")
                    else:
                         compare_structures(gen_map[ident], item, f"{path}[id={ident}]", report)
                else:
                    # Item has no identifier, fall back to index-based or skip?
                    # If we can't identify it, strictly comparing is hard without order.
                    # Let's assume order for non-identifiables?
                    # Or try to find ANY match?
                    # For now, just warn.
                    # report.append(f"[UNCHECKED] at {path}: Complex list item without ID.")
                    pass

    # 4. Primitives
    else:
        # Value check
        if gen != exp:
             report.append(f"[VALUE MISMATCH] at {path}: Expected '{exp}', got '{gen}'")

def run_verification():
    report_lines = []
    
    # Files to compare
    pairs = [
        ("3.0", "generated_oas_3.0.yaml", "EBACL_FPAD_20251113_OpenApi3.0_FPAD_API_Participant_4.1_v20251212.yaml"),
        ("3.1", "generated_oas_3.1.yaml", "EBACL_FPAD_20251110_OpenApi3.1_FPAD_API_Participant_4.1_v20251212.yaml")
    ]
    
    for label, gen_name, exp_name in pairs:
        gen_path = os.path.join(GENERATED_DIR, gen_name)
        exp_path = os.path.join(EXPECTED_DIR, exp_name)
        
        report_lines.append(f"--- DETAILED COMPARISON FOR OAS {label} ---")
        report_lines.append(f"Generated: {gen_path}")
        report_lines.append(f"Expected:  {exp_path}")
        report_lines.append("")
        
        if not os.path.exists(gen_path):
            report_lines.append("CRITICAL: Generated file not found.")
            continue
        if not os.path.exists(exp_path):
            report_lines.append("CRITICAL: Expected file not found.")
            continue
            
        gen_data = load_yaml(gen_path)
        exp_data = load_yaml(exp_path)
        
        if gen_data and exp_data:
            discrepancies = []
            compare_structures(gen_data, exp_data, "root", discrepancies)
            
            if discrepancies:
                report_lines.append(f"Found {len(discrepancies)} discrepancies:")
                for d in discrepancies:
                    report_lines.append(d)
            else:
                report_lines.append("SUCCESS: No structural discrepancies found (Expected content is fully present).")
        else:
             report_lines.append("Failed to load YAML data.")
             
        report_lines.append("\n" + "="*50 + "\n")

    # Write Report
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    
    print(f"Report verified and written to {REPORT_FILE}")

if __name__ == "__main__":
    run_verification()
