import os
import sys
import multiprocessing

# Fix TclError on Windows environments where Tcl/Tk paths are not correctly resolved
if os.name == 'nt' and not getattr(sys, 'frozen', False):
    import os
    # Dynamically find Tcl/Tk paths based on the Python installation
    base_prefix = getattr(sys, 'base_prefix', sys.prefix)
    tcl_dir = os.path.join(base_prefix, 'tcl')
    if os.path.exists(tcl_dir):
        for d in os.listdir(tcl_dir):
            if d.startswith('tcl8.'):
                os.environ['TCL_LIBRARY'] = os.path.join(tcl_dir, d)
            elif d.startswith('tk8.'):
                os.environ['TK_LIBRARY'] = os.path.join(tcl_dir, d)

# Required for PyInstaller to properly handle multiprocessing
if __name__ == "__main__":
    multiprocessing.freeze_support()

# Ensure project root is in sys.path
if getattr(sys, 'frozen', False):
    # Running in a bundle (PyInstaller)
    base_path = sys._MEIPASS
else:
    # Running in normal Python environment
    base_path = os.path.dirname(os.path.abspath(__file__))

if base_path not in sys.path:
    sys.path.insert(0, base_path)


if __name__ == "__main__":
    # Show splash screen and load app
    try:
        from src.splash_screen import show_splash_and_load_app
        app = show_splash_and_load_app(debug_mode=True)  # Wait for click
    except ImportError:
        # Fallback: direct import without splash
        import customtkinter as ctk
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        try:
            from src.gui import OASGenApp
        except ImportError:
            from gui import OASGenApp
        
        app = OASGenApp()
    
    app.mainloop()
