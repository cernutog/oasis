
yaml_path = "API Templates/generated/generated_oas_3.1.yaml"
found_201 = False
print_lines = False
count = 0

with open(yaml_path, 'r') as f:
    for line in f:
        if "'201':" in line:
            found_201 = True
            print(f"MATCH 201: {line.strip()}")
        
        if found_201:
            if "examples:" in line:
                 print_lines = True
            
            if print_lines:
                print(line.strip())
                count += 1
                if count > 50: break
