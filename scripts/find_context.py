def find_context():
    target = "#/components/schemas/FpadResponseIdentifier"
    path = "API Templates/generated/generated_oas_3.1.yaml"
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for i, line in enumerate(lines):
            if target in line:
                print(f"Match at line {i+1}:")
                start = max(0, i-5)
                end = min(len(lines), i+5)
                for j in range(start, end):
                    prefix = ">> " if j == i else "   "
                    print(f"{prefix}{j+1}: {lines[j].rstrip()}")
                print("-" * 40)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    find_context()
