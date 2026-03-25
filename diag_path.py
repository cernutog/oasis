import sys
import os
try:
    from src.oas_diff.generators import compatibility_generator
    print(f"compatibility_generator module location: {os.path.abspath(compatibility_generator.__file__)}")
except ImportError as e:
    print(f"Import Error: {e}")

print("Python executable:", sys.executable)
print("System path:")
for p in sys.path:
    print(f"  {p}")
