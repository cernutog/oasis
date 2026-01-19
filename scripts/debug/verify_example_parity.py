
import yaml
import sys
import collections

def extract_examples(node, version, examples_list):
    if isinstance(node, dict):
        # 1. Check 'example' (OAS 3.0 Schema / 3.0-3.1 Header/Param)
        if 'example' in node:
            examples_list.append(str(node['example']).strip())
            
        # 2. Check 'examples' (OAS 3.1 Schema / 3.0-3.1 Header/Media)
        if 'examples' in node:
            exs = node['examples']
            if isinstance(exs, list) and version.startswith('3.1'):
                # OAS 3.1 Schema examples are a list of values
                for e in exs:
                    examples_list.append(str(e).strip())
            elif isinstance(exs, dict):
                # Map of Example Objects (Header/Media)
                for k, v in exs.items():
                    if isinstance(v, dict) and 'value' in v:
                        examples_list.append(str(v['value']).strip())
                    elif isinstance(v, dict):
                        # Might be ref or legacy? Just grab as string if no value key
                        examples_list.append(str(v).strip()) 
                    else:
                        examples_list.append(str(v).strip())

        # Recursion
        for k, v in node.items():
            extract_examples(v, version, examples_list)
            
    elif isinstance(node, list):
        for item in node:
            extract_examples(item, version, examples_list)

def main():
    try:
        f30_path = sys.argv[1]
        f31_path = sys.argv[2]
        
        print(f"Loading OAS 3.0: {f30_path}")
        with open(f30_path, 'r', encoding='utf-8') as f:
            data30 = yaml.safe_load(f)
            
        print(f"Loading OAS 3.1: {f31_path}")
        with open(f31_path, 'r', encoding='utf-8') as f:
            data31 = yaml.safe_load(f)
            
        ex30 = []
        extract_examples(data30, '3.0', ex30)
        
        ex31 = []
        extract_examples(data31, '3.1', ex31)
        
        # Sort
        ex30.sort()
        ex31.sort()
        
        print(f"OAS 3.0 Examples Found: {len(ex30)}")
        print(f"OAS 3.1 Examples Found: {len(ex31)}")
        
        if len(ex30) == len(ex31):
            if ex30 == ex31:
                print("SUCCESS: Example sets are DETEMINISTICALLY IDENTICAL.")
            else:
                print("FAILURE: Counts match but content differs.")
        else:
            print("FAILURE: Counts do not match.")
            
        # Diff
        set30 = collections.Counter(ex30)
        set31 = collections.Counter(ex31)
        
        diff30 = set30 - set31
        diff31 = set31 - set30
        
        if diff30:
            print("\nValues present in 3.0 but MISSING/FEWER in 3.1:")
            for item, count in diff30.items():
                print(f"  '{item}' (Diff: {count})")
                
        if diff31:
            print("\nValues present in 3.1 but MISSING/FEWER in 3.0:")
            for item, count in diff31.items():
                print(f"  '{item}' (Diff: {count})")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
