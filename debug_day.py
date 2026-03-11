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

input_dir = Path(r"c:\Users\giuse\.gemini\antigravity\scratch\OASIS\Templates Legacy")
registrations = []

for f in input_dir.glob("*.xlsm"):
    if f.name.startswith(("$", "~")): continue
    try:
        xl = pd.ExcelFile(f)
        if "Data Type" not in xl.sheet_names: continue
        df = pd.read_excel(xl, sheet_name="Data Type", dtype=str, header=None)
        # Find header
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
            if not raw: continue
            norm = to_pascal_case(raw)
            if "day" in norm.lower():
                registrations.append((f.name, raw, norm))
    except: pass

print("Registrations for 'day':")
for f, raw, norm in registrations:
    print(f"  {f:40} | Raw: {raw:15} | Norm: {norm}")

# Simulate registry
used = set()
for f, raw, norm in registrations:
    out = norm
    if out in used:
        counter = 1
        while f"{norm}{counter}" in used:
            counter += 1
        out = f"{norm}{counter}"
    used.add(out)
    print(f"  -> Generated: {out} (from {raw})")

print("\nFinal 'used' set for 'day':", [u for u in used if "day" in u.lower()])
