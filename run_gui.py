import os
import sys
import multiprocessing

# Required for PyInstaller to properly handle multiprocessing
if __name__ == "__main__":
    multiprocessing.freeze_support()

import customtkinter as ctk

# Ensure project root is in sys.path
if getattr(sys, 'frozen', False):
    # Running in a bundle (PyInstaller)
    base_path = sys._MEIPASS
else:
    # Running in normal Python environment
    base_path = os.path.dirname(os.path.abspath(__file__))

if base_path not in sys.path:
    sys.path.insert(0, base_path)

try:
    from src.gui import OASGenApp
except ImportError as e:
    print(f"Primary import failed: {e}. Trying fallback...")
    try:
        from gui import OASGenApp
    except ImportError:
        # Final attempt: direct import might work if flattened
        try:
            import gui
            OASGenApp = gui.OASGenApp
        except ImportError:
            raise e

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = OASGenApp()
    app.mainloop()

