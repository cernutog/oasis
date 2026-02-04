
def search_pattern():
    with open("src/legacy_converter.py", "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines):
        if "self.used_properties =" in line:
            print(f"Line {i+1}: {line.strip()}")
        if "self.used_properties.clear" in line:
            print(f"Line {i+1}: {line.strip()}")

if __name__ == "__main__":
    search_pattern()
