import yaml
import textwrap

def test_parse(raw):
    print(f"--- Raw ---\n{repr(raw)}")
    
    # Current Logic
    stripped = raw.strip()
    print(f"--- Stripped ---\n{repr(stripped)}")
    
    try:
        parsed = yaml.safe_load(stripped)
        print(f"--- Result ---: SUCCESS Type: {type(parsed)}")
    except Exception as e:
        print(f"--- Result ---: FAILED {e}")

    # Proposed Logic
    dedented = textwrap.dedent(raw)
    print(f"--- Dedented ---\n{repr(dedented)}")
    try:
        parsed_d = yaml.safe_load(dedented)
        print(f"--- Result (Dedented) ---: SUCCESS Type: {type(parsed_d)}")
    except Exception as e:
        print(f"--- Result (Dedented) ---: FAILED {e}")

case_1 = """
    key1: val1
    key2: val2
"""

case_2 = """
    parent:
        child: val
"""

print("Running Case 1:")
test_parse(case_1)
print("\nRunning Case 2:")
test_parse(case_2)
