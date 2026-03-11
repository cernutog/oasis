import os
import pandas as pd
from pathlib import Path
import re

def to_pascal_case(name):
    if not name: return ""
    tokens = re.split(r'[^a-zA-Z0-9]', str(name))
    return "".join(t.capitalize() for t in tokens if t)

def clean_val(v):
    if pd.isna(v): return ""
    return str(v).strip()

def normalize_list(v):
    if not isinstance(v, str): return v
    v = re.sub(r'\s*;\s*', ',', v)
    v = re.sub(r'\s*,\s*', ',', v)
    return v.strip().strip(',')

input_dir = Path(r"c:\Users\giuse\.gemini\antigravity\scratch\OASIS\Templates Legacy")
versions = {} # fingerprint -> {fields, files}

for f in input_dir.glob("*.xlsm"):
    if f.name.startswith(("$", "~")): continue
    try:
        xl = pd.ExcelFile(f)
        if "Data Type" not in xl.sheet_names: continue
        df = pd.read_excel(xl, sheet_name="Data Type", dtype=str, header=None)
        hr = -1
        for i, row in df.iterrows():
            if "name" in [str(x).lower() for x in row if pd.notna(x)]:
                hr = i; break
        if hr == -1: continue
        df.columns = [str(c).strip().lower() for c in df.iloc[hr]]
        df = df.iloc[hr+1:]
        name_col = next((c for c in df.columns if "name" in c), None)
        for _, row in df.iterrows():
            raw = clean_val(row.get(name_col, ""))
            if to_pascal_case(raw) == "Day":
                fields = {
                    "type": clean_val(row.get("type", "")),
                    "min": clean_val(row.get("min", "")),
                    "max": clean_val(row.get("max", "")),
                    "regex": clean_val(row.get("regex", "")),
                    "allowed": normalize_list(clean_val(row.get("allowed", "") or row.get("allowed value", ""))),
                    "example": normalize_list(clean_val(row.get("example", "")))
                }
                fp = tuple(sorted(fields.items()))
                if fp not in versions:
                    versions[fp] = {"fields": fields, "files": []}
                versions[fp]["files"].append(f.name)
    except: pass

print(f"Found {len(versions)} unique versions of 'Day':")
for i, (fp, data) in enumerate(versions.items(), 1):
    print(f"\n--- Version {i} ---")
    for k, v in data["fields"].items():
        print(f"  {k:8}: '{v}'")
    print(f"  Source files ({len(data['files'])}): {data['files'][:3]} ...")
