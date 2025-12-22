import os
import sys
import customtkinter as ctk

# Ensure 'src' is importable
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from src.gui import OASGenApp
except ImportError as e:
    print(f"Failed to import app: {e}")
    # Fallback for frozen app if src structure is flattened (should not happen with this setup)
    try:
        from gui import OASGenApp
    except ImportError:
        raise e

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = OASGenApp()
    app.mainloop()
