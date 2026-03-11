"""
Run the Legacy Converter on fixtures to generate output.
"""
import sys, shutil
from pathlib import Path

project    = Path(__file__).resolve().parent.parent.parent  # tests/legacy_converter/ -> tests/ -> OASIS/
sys.path.insert(0, str(project / "src"))
from legacy_converter import LegacyConverter

input_dir  = project / "tests" / "legacy_converter" / "fixtures" / "input"
output_dir = project / "tests" / "legacy_converter" / "fixtures" / "output"
master_dir = project / "Templates Master"

# Pulizia output
if output_dir.exists():
    shutil.rmtree(output_dir, ignore_errors=True)
output_dir.mkdir(parents=True, exist_ok=True)

# --- Conversione ---
converter = LegacyConverter(str(input_dir), str(output_dir), str(master_dir))
converter.convert()

print("\n--- Conversione completata ---")
print(f"Output in: {output_dir}")
for f in sorted(output_dir.iterdir()):
    print(f"  {f.name}")
