
import os
import sys
from src.legacy_converter import LegacyConverter

def finalize():
    # Update official Templates Converted
    conv = LegacyConverter(
        legacy_dir="Templates Legacy",
        output_dir="Templates Converted", 
        log_callback=print
    )
    print("Updating Templates Converted...")
    conv.convert()
    
    # Also update Output Legacy for consistency
    conv_legacy = LegacyConverter(
        legacy_dir="Templates Legacy",
        output_dir="Output Legacy",
        log_callback=print
    )
    print("Updating Output Legacy...")
    conv_legacy.convert()
    
    print("\nFinalization complete.")

if __name__ == "__main__":
    finalize()
