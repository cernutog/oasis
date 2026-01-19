import os
import sys

# Runtime hook to set TCL_LIBRARY and TK_LIBRARY
# This is necessary because PyInstaller's auto-detection is failing for Python 3.13
if hasattr(sys, '_MEIPASS'):
    # Path where Tcl/Tk files are bundled
    tcl_dir = os.path.join(sys._MEIPASS, 'tcl', 'tcl8.6')
    tk_dir = os.path.join(sys._MEIPASS, 'tcl', 'tk8.6')
    
    os.environ['TCL_LIBRARY'] = tcl_dir
    os.environ['TK_LIBRARY'] = tk_dir
    
    # Also add to lib path if possible (optional)
    # print(f"Setting TCL_LIBRARY to {tcl_dir}")
