
from src.legacy_converter import LegacyConverter
import os

def run():
    base = os.getcwd()
    c = LegacyConverter(
        legacy_dir=os.path.join(base, "Templates Legacy"),
        output_dir=os.path.join(base, "Output OAS"),
        master_dir=os.path.join(base, "Templates Master")
    )
    success = c.convert()
    print(f"Conversion success: {success}")

if __name__ == "__main__":
    run()
