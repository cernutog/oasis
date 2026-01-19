import pandas as pd
import yaml
import json
import os
import glob


def parse_example_string(ex_str):
    if pd.isna(ex_str) or ex_str is None:
        return None
    try:
        ex_str = str(ex_str).strip()
        print(f"DEBUG: Processing string starting with: {ex_str[:50]!r}")
        if ex_str.startswith("{") or ex_str.startswith("["):
            print("DEBUG: Detected JSON start")
            try:
                return json.loads(ex_str)
            except Exception as e:
                print(f"DEBUG: JSON load failed: {e}")
                fixed = (
                    ex_str.replace("'", '"')
                    .replace("None", "null")
                    .replace("False", "false")
                    .replace("True", "true")
                )
                return json.loads(fixed)
        else:
            print("DEBUG: Trying YAML load")
            return yaml.safe_load(ex_str)
    except Exception as e:
        print(f"DEBUG: Parse failed: {e}")
        return ex_str


def debug_examples():
    files = glob.glob("API Templates/*account_assessment_vop.251111.xlsm")
    for f in files:
        if "bulk" in f:
            continue
        print(f"Loading {f}...")
        try:
            # Try header=0 first
            df = pd.read_excel(f, sheet_name="Body Example", header=0)
            print("Columns:", df.columns.tolist())

            # Find the 'Body' column
            body_col = None
            for c in df.columns:
                if str(c).strip() == "Body":
                    body_col = c
                    break

            if body_col:
                for idx, row in df.iterrows():
                    name = row[0]  # Assumption
                    val = row[body_col]
                    print(f"--- Row {idx} ({name}) ---")
                    print(f"Raw Value Type: {type(val)}")
                    print(f"Raw Value Preview: {str(val)[:100]!r}")

                    parsed = parse_example_string(val)
                    print(f"Parsed Type: {type(parsed)}")
                    if isinstance(parsed, dict) or isinstance(parsed, list):
                        print("Parsed successfully as structure.")
                    else:
                        print("Parsed as STRING (failed to structure?)")
            else:
                print("Body column not found.")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    debug_examples()
