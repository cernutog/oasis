import re
import sys
from pathlib import Path

def increment():
    version_file = Path('src/version.py')
    content = version_file.read_text(encoding='utf-8')
    m = re.search(r'BUILD_NUMBER\s*=\s*(\d+)', content)
    if m:
        old = int(m.group(1))
        new = old + 1
        content = re.sub(r'BUILD_NUMBER\s*=\s*\d+', f'BUILD_NUMBER = {new}', content)
        version_file.write_text(content, encoding='utf-8')
        print(f"  Build number: {old} -> {new}")
    else:
        print("ERROR: BUILD_NUMBER not found")
        sys.exit(1)

def get_version():
    root = Path(__file__).parent.parent
    sys.path.insert(0, str(root))
    from src.version import FULL_VERSION
    print(FULL_VERSION)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "increment":
        increment()
    elif len(sys.argv) > 1 and sys.argv[1] == "get":
        get_version()
