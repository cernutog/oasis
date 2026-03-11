"""Scan the legacy revokeLcr Body sheet and show any row mentioning networkFileName."""
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from src.legacy_converter import LegacyConverter

INPUT_DIR = ROOT / "Templates Legacy"

def log(msg):
    pass

conv = LegacyConverter(
    input_dir=str(INPUT_DIR),
    output_dir=str(ROOT / "tests" / "_debug_out"),
    master_dir=str(ROOT / "Templates Master"),
    log_callback=log,
)

legacy_path = INPUT_DIR / "revokeLcr.230301.xlsm"
if not legacy_path.exists():
    print(f"Not found: {legacy_path}")
    raise SystemExit(1)

xl = pd.ExcelFile(legacy_path)
if "Body" not in xl.sheet_names:
    print("No Body sheet")
    raise SystemExit(1)

# Raw scan
df_raw = pd.read_excel(xl, sheet_name="Body", header=None, dtype=str)

hits = []
for r in range(len(df_raw)):
    row = df_raw.iloc[r].tolist()
    for c, v in enumerate(row):
        if isinstance(v, str) and "networkfilename" in v.lower():
            hits.append((r + 1, c + 1, v, row))

print(f"Hits in raw Body sheet: {len(hits)}")
for r, c, v, row in hits[:20]:
    print(f"Row {r}, Col {c}: {v}")

# Parsed structure
children = conv._read_legacy_structure(xl, "Body")
print(f"\nParsed children count: {len(children)}")
for tup in children:
    name = tup[0]
    if "network" in str(name).lower():
        print("FOUND IN PARSED:", tup)

# Also print the full list of parsed names for quick eyeballing
print("\nParsed names:")
for tup in children:
    print("-", tup[0])
