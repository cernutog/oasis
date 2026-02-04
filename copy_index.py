
import shutil
import os

src = r"Output Legacy\$index.xlsx"
dst = r"Templates Master\$index.xlsx"

if os.path.exists(src):
    try:
        shutil.copy2(src, dst)
        print(f"Success: Copied {src} to {dst}")
    except Exception as e:
        print(f"Error copying: {e}")
else:
    print(f"Error: Source {src} not found")
