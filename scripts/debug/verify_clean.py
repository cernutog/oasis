import re

FILE = "API Templates/generated/generated_oas_3.1.yaml"


def verify():
    with open(FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex for value: "{...
    # We want to catch `value: "` followed by `{`.
    # PyYAML dumps strings with quotes.

    matches = re.findall(r"value:\s*\"\{", content)
    if matches:
        print(
            f"FAILURE: Found {len(matches)} occurrences of JSON-like strings starting with {{."
        )
        print("This means some examples are still generated as strings with braces.")
    else:
        print("SUCCESS: No JSON-like strings starting with { found.")


if __name__ == "__main__":
    verify()
