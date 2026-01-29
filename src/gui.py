import webbrowser
import shutil
import difflib
try:
    import win32com.client
    HAS_COM = True
except ImportError:
    HAS_COM = False

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import threading
import datetime
import os
import sys
import json
import tempfile

# Conditional imports to support both development and PyInstaller frozen environments
try:
    # Try relative imports first (works in development when run as package)
    from . import main as main_script
    from .linter import SpectralRunner
    from .charts import SemanticPieChart
    from .redoc_gen import RedocGenerator
    from .preferences import PreferencesManager
    from .preferences_dialog import PreferencesDialog
    from .doc_viewer import DockedDocViewer
    from .version import VERSION, FULL_VERSION
    from .splash_screen import SplashScreen
    from .oas_importer.oas_converter import OASToExcelConverter
    from .oas_importer.oas_comparator import OASComparator
except ImportError:
    # Fall back to absolute imports (works when frozen or run directly)
    import main as main_script
    from linter import SpectralRunner
    from charts import SemanticPieChart
    from redoc_gen import RedocGenerator
    from preferences import PreferencesManager
    from preferences_dialog import PreferencesDialog
    from doc_viewer import DockedDocViewer
    from version import VERSION, FULL_VERSION
    from splash_screen import SplashScreen
    from oas_importer.oas_converter import OASToExcelConverter
    from oas_importer.oas_comparator import OASComparator

from chlorophyll import CodeView
import pygments.lexers

# Set Theme
# Set Theme - HANDLED IN MAIN.PY
# ctk.set_appearance_mode("System")
# ctk.set_default_color_theme("blue")


# Module-level function for multiprocessing (must be picklable)
def _run_webview_process(html_file, window_title):
    """Target function for multiprocessing - runs pywebview in separate process."""
    try:
        import webview

        webview.create_window(window_title, html_file, width=1200, height=800)
        webview.start()
    except Exception as e:
        print(f"WebView error: {e}")


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



class LogWindow(ctk.CTkToplevel):
    """Detached window for application logs."""

    def __init__(self, parent, theme="Light"):
        super().__init__(parent)
        self.title("Application Logs")
        self.geometry("800x600")

        # Icon Setup - Delayed to override CTk default (same as PreferencesDialog)
        self.after(250, self._set_icon)

        # Set appearance
        self.theme = theme

        # Main Textbox
        self.textbox = ctk.CTkTextbox(
            self, font=("Consolas", 11), wrap="word", state="disabled"
        )
        self.textbox.pack(fill="both", expand=True, padx=10, pady=10)

        # Apply initial theme
        self.apply_theme(self.theme)
        
        # Ensure window is on top when created (transient keeps it above parent)
        self.transient(parent)
        self.lift()
        self.focus_force()

    def _set_icon(self):
        try:
            icon_file = resource_path("icon.ico")
            if os.path.exists(icon_file):
                self.iconbitmap(icon_file)
        except Exception:
            pass




    def append_log(self, text):
        """Append text to the log window."""
        self.textbox.configure(state="normal")
        self.textbox.insert("end", text + "\n")
        self.textbox.see("end")
        self.textbox.configure(state="disabled")

    def clear_log(self):
        """Clear all logs."""
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.configure(state="disabled")

    def apply_theme(self, theme_mode):
        """Apply Light/Dark theme to the log window."""
        self.theme = theme_mode
        if theme_mode == "Dark":
            self.textbox.configure(fg_color="#1E1E1E", text_color="#D4D4D4")
        else:
            self.textbox.configure(fg_color="#F0F0F0", text_color="#000000")


class OASErrorDialog(ctk.CTkToplevel):
    """Custom error dialog with consistent Petrol Blue styling."""
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.title(title)
        self.geometry("380x160") 
        self.resizable(False, False)
        
        # Center relative to parent
        self.update_idletasks()
        try:
            x = parent.winfo_x() + (parent.winfo_width() // 2) - 190
            y = parent.winfo_y() + (parent.winfo_height() // 2) - 80
            self.geometry(f"+{int(x)}+{int(y)}")
        except:
            pass

        self.transient(parent)
        self.grab_set()

        # Icon setup
        self.after(200, self._set_icon)
        
        self._build_ui(message)

    def _get_resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def _set_icon(self):
        try:
            icon_path = "icon.ico"
            if not os.path.exists(icon_path):
                icon_path = self._get_resource_path("icon.ico")
            if os.path.exists(icon_path):
                try:
                    self.iconbitmap(icon_path)
                    self.wm_iconbitmap(icon_path)
                except:
                    pass
        except:
            pass

    def _build_ui(self, message):
        # Main Container - Shift up slightly for visual balance
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.place(relx=0.5, rely=0.45, anchor="center")

        # Content Block (Icon + Text) - Row Layout
        content_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        content_frame.pack(pady=(0, 15))

        # Icon - Red X
        icon_label = ctk.CTkLabel(content_frame, text="\u274C", 
                                  text_color="#D32F2F", 
                                  font=ctk.CTkFont(size=48))
        icon_label.pack(side="left", padx=(0, 15))

        # Message Area
        msg_label = ctk.CTkLabel(content_frame, text=message, 
                                 font=ctk.CTkFont(size=14, weight="bold"),
                                 text_color=("black", "white"),
                                 wraplength=300,
                                 justify="left")
        msg_label.pack(side="left")

        # Button Area
        # HARDCODED PETROL BLUE
        ctk.CTkButton(self, text="OK", width=120, height=32,
                      fg_color="#0A809E", hover_color="#076075",
                      command=self.destroy).pack(side="bottom", pady=20)

        # Handle close (hide instead of destroy? No, destroy is fine, we recreate)
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.on_close_callback = None

    def _on_close(self):
        if self.on_close_callback:
            self.on_close_callback()
        self.destroy()

import customtkinter as ctk
from customtkinter import ThemeManager  # REQUIRED FOR DIRECT OVERRIDE
import tkinter as tk
import tkinter.messagebox # debug

# ... [imports] ...

class OASGenApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # NUCLEAR OPTION: FORCE THEME COLORS HERE
        # This bypasses file loading issues entirely.
        try:
            PETROL = "#0A809E"
            HOVER = "#076075"
            
            # Button
            ThemeManager.theme["CTkButton"]["fg_color"] = [PETROL, PETROL]
            ThemeManager.theme["CTkButton"]["hover_color"] = [HOVER, HOVER]
            
            # Slider
            ThemeManager.theme["CTkSlider"]["button_color"] = [PETROL, PETROL]
            ThemeManager.theme["CTkSlider"]["progress_color"] = [PETROL, PETROL]
            
            # CheckBox
            ThemeManager.theme["CTkCheckBox"]["fg_color"] = [PETROL, PETROL]
            ThemeManager.theme["CTkCheckBox"]["hover_color"] = [HOVER, HOVER]
            
            # Switch
            ThemeManager.theme["CTkSwitch"]["progress_color"] = [PETROL, PETROL]
            
            # OptionMenu/ComboBox/SegmentedButton
            ThemeManager.theme["CTkOptionMenu"]["fg_color"] = [PETROL, PETROL]
            ThemeManager.theme["CTkOptionMenu"]["button_color"] = [PETROL, PETROL]
            ThemeManager.theme["CTkComboBox"]["button_color"] = [PETROL, PETROL]
            ThemeManager.theme["CTkSegmentedButton"]["selected_color"] = [PETROL, PETROL]
            ThemeManager.theme["CTkSegmentedButton"]["selected_hover_color"] = [HOVER, HOVER]

        except Exception as e:
            print(f"Failed to enforce theme: {e}")

        # Window Setup
        self.title(f"OASIS - OAS Integration Suite v{FULL_VERSION}")
        self.geometry("1100x700")

        # Icon Setup
        try:
            icon_file = resource_path("icon.ico")
            if os.path.exists(icon_file):
                self.iconbitmap(icon_file)
        except Exception:
            pass

        # Initialize Preferences Manager
        self.prefs_manager = PreferencesManager()
        self.log_window = None # Init before logging
        self.log_history = []
        
        # Open Log Window immediately if desired, or just init history
        # self.log("[Init] Loading preferences...")

        # Log Window State
        self.log_window = None
        self.log_history = []  # Store logs to populate window when opened

        # Track open documentation viewers
        self._doc_viewers = []

        # Apply saved window geometry if available
        if self.prefs_manager.get("remember_window_pos") and self.prefs_manager.get(
            "window_geometry"
        ):
            try:
                self.geometry(self.prefs_manager.get("window_geometry"))
            except (tk.TclError, ValueError):
                pass

        # Bind window close to save geometry
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # Grid Layout Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)  # Tabview expands

        # --- Menu Bar ---
        self._create_menu()

        # --- Tab View ---
        self.tabview = ctk.CTkTabview(self, command=self._on_tab_change)
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        # Define Tabs Order
        self.tab_import = self.tabview.add("OAS to Excel")
        self.tab_gen = self.tabview.add("Excel to OAS")
        self.tab_val = self.tabview.add("Validation")
        
        # Setup OAS to Excel Tab
        self._setup_import_tab()
        
        # Global search binding - bind_all to be robust regardless of focus
        self.bind_all("<Control-f>", self._handle_global_search)
        self.bind_all("<Control-F>", self._handle_global_search)
        self.bind_all("<Control-Key-f>", self._handle_global_search)
        self.bind_all("<Control-Key-F>", self._handle_global_search)


        # ==========================
        # TAB 2: EXCEL TO OAS (Formerly Generation)
        # ==========================

        self.tab_gen.grid_columnconfigure(0, weight=1)
        self.tab_gen.grid_rowconfigure(1, weight=0)  # Actions (Row 1) do NOT expand
        self.tab_gen.grid_rowconfigure(2, weight=1)  # Log (Row 2) DOES expand

        # Controls
        self.frame_controls = ctk.CTkFrame(self.tab_gen, fg_color="transparent")
        self.frame_controls.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.frame_controls.grid_columnconfigure(1, weight=1)

        # Label: Excel Input Folder
        self.lbl_dir = ctk.CTkLabel(
            self.frame_controls,
            text="Excel Input Folder:",
            font=ctk.CTkFont(weight="bold"),
        )
        self.lbl_dir.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.entry_dir = ctk.CTkEntry(
            self.frame_controls, placeholder_text="Path to Excel templates..."
        )
        self.entry_dir.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ew")

        # Startup Logic: Load Paths
        remember = self.prefs_manager.get("remember_paths", True)
        
        # 1. Excel Input (Template)
        if remember:
             load_path = self.prefs_manager.get("last_excel_input", "")
             if load_path and os.path.exists(load_path):
                 self.entry_dir.insert(0, load_path)

        self.btn_browse = ctk.CTkButton(
            self.frame_controls, text="Browse", width=100, command=self.browse_dir
        )
        self.btn_browse.grid(row=0, column=2, padx=10, pady=10)

        # OAS Output Folder (shared across all tabs)
        self.lbl_oas_folder = ctk.CTkLabel(
            self.frame_controls,
            text="OAS Output Folder:",
            font=ctk.CTkFont(weight="bold"),
        )
        self.lbl_oas_folder.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.entry_oas_folder = ctk.CTkEntry(
            self.frame_controls, placeholder_text="Path to OAS output folder..."
        )
        self.entry_oas_folder.grid(row=1, column=1, padx=(0, 10), pady=10, sticky="ew")

        # 2. OAS Output Folder
        if remember:
            saved_oas_folder = self.prefs_manager.get("last_oas_folder", "")
            if saved_oas_folder and os.path.exists(saved_oas_folder):
                self.entry_oas_folder.insert(0, saved_oas_folder)

        self.btn_browse_oas = ctk.CTkButton(
            self.frame_controls,
            text="Browse",
            width=100,
            command=self.browse_oas_folder,
        )
        self.btn_browse_oas.grid(row=1, column=2, padx=10, pady=10)

        # Store checkbox variables (moved to action bar below)
        self.var_31 = ctk.BooleanVar(value=self.prefs_manager.get("gen_oas_31", True))
        self.var_30 = ctk.BooleanVar(value=self.prefs_manager.get("gen_oas_30", True))
        self.var_swift = ctk.BooleanVar(value=self.prefs_manager.get("gen_oas_swift", False))

        # Actions Frame (Row 1 - previously Row 2) - Unified Toolbar with Options
        self.frame_gen_act = ctk.CTkFrame(self.tab_gen, fg_color="transparent")
        self.frame_gen_act.grid(row=1, column=0, sticky="ew", padx=10, pady=(0,10))
        
        # Left Side: OAS Version Checkboxes
        self.chk_31 = ctk.CTkCheckBox(
            self.frame_gen_act, text="OAS 3.1", variable=self.var_31
        )
        self.chk_31.pack(side="left", padx=(0, 15))

        self.chk_30 = ctk.CTkCheckBox(
            self.frame_gen_act, text="OAS 3.0", variable=self.var_30
        )
        self.chk_30.pack(side="left", padx=(0, 15))

        self.chk_swift = ctk.CTkCheckBox(
            self.frame_gen_act, text="OAS SWIFT", variable=self.var_swift
        )
        self.chk_swift.pack(side="left", padx=(0, 20))
        
        # Generate Button
        self.btn_gen = ctk.CTkButton(
            self.frame_gen_act, 
            text="Generate OAS",
            width=150,
            font=ctk.CTkFont(weight="bold"),
            command=self.start_generation,
        )
        self.btn_gen.pack(side="left", padx=0)

        # Right Side: Font Size Control (Corrected for Tab 2)
        self.frame_gen_font = ctk.CTkFrame(self.frame_gen_act, fg_color="transparent")
        self.frame_gen_font.pack(side="right") # Pack to right of the Action Frame

        self.lbl_font_size_gen_val = ctk.CTkLabel(self.frame_gen_font, text="11", width=20)
        self.lbl_font_size_gen_val.pack(side="right")

        self.slider_font_gen = ctk.CTkSlider(self.frame_gen_font, from_=8, to=24, number_of_steps=16, width=150, command=self.update_font_size_gen)
        self.slider_font_gen.set(11)
        self.slider_font_gen.pack(side="right", padx=(5,5))

        ctk.CTkLabel(self.frame_gen_font, text="Font Size:", font=("Arial", 12)).pack(side="right", padx=5)

        # Log Area (Row 2)
        self.log_area = ctk.CTkTextbox(self.tab_gen, font=("Consolas", 11), wrap="word")
        self.log_area.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.log_area.configure(state="disabled")
        
        # Add Context Menu for clearing
        self.log_area.bind("<Button-3>", self._show_log_context_menu)

        # ==========================
        # TAB 2: VALIDATION
        # ==========================
        # TAB 2: VALIDATION
        # ==========================
        # Resolve Spectral Binary (Standalone)
        spectral_cmd = "spectral" # Fallback
        
        # 1. Check Bundled (Frozen)
        if getattr(sys, 'frozen', False):
            bundled_path = os.path.join(sys._MEIPASS, "src", "bin", "spectral.exe")
            if os.path.exists(bundled_path):
                spectral_cmd = bundled_path
        # 2. Check Local (Dev)
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
            local_path = os.path.join(base_path, "bin", "spectral.exe")
            if os.path.exists(local_path):
                spectral_cmd = local_path
                
        self.linter = SpectralRunner(spectral_cmd=spectral_cmd)
        self.last_lint_result = None
        self.last_generated_files = []  # Track files from generation
        self.validated_file = None  # Track which file was validated (basename)
        self.validated_file_path = None  # Full path for caching
        self.validated_file_mtime = 0 
        self.validation_issues = {}  # {line_number: [(severity, message), ...]}

        self.tab_val.grid_columnconfigure(0, weight=1)  # List
        self.tab_val.grid_columnconfigure(1, weight=1)  # Chart
        # Content pane moves to row 3
        self.tab_val.grid_rowconfigure(3, weight=1)  
        self.tab_val.grid_rowconfigure(4, weight=0)  # Footer row

        # Top Bar - OAS Folder
        self.frame_val_folder = ctk.CTkFrame(self.tab_val, fg_color="transparent")
        self.frame_val_folder.grid(
            row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(10, 0)
        )
        self.frame_val_folder.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self.frame_val_folder, text="OAS Folder:", font=ctk.CTkFont(weight="bold")
        ).grid(row=0, column=0, padx=(0, 10), sticky="w")
        self.entry_val_oas_folder = ctk.CTkEntry(
            self.frame_val_folder, placeholder_text="Path to OAS folder..."
        )
        self.entry_val_oas_folder.grid(row=0, column=1, padx=(0, 10), sticky="ew")
        # Sync with Generation tab (which uses preferences)
        self.entry_val_oas_folder.insert(0, self.entry_oas_folder.get())
        self.btn_browse_val_oas = ctk.CTkButton(
            self.frame_val_folder,
            text="Browse",
            width=80,
            command=self.browse_oas_folder_validation,
        )
        self.btn_browse_val_oas.grid(row=0, column=2)

        # Top Bar - File Selector
        self.frame_val_top = ctk.CTkFrame(self.tab_val, fg_color="transparent")
        self.frame_val_top.grid(
            row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=10
        )

        # File Selector - use grid with weight for expansion
        self.frame_val_top.grid_columnconfigure(1, weight=1)  # Make combo column expand

        self.lbl_sel = ctk.CTkLabel(
            self.frame_val_top, text="Select File:", font=ctk.CTkFont(weight="bold")
        )
        self.lbl_sel.grid(row=0, column=0, padx=(0, 10))

        self.file_map = {}
        self.cbo_files = ctk.CTkComboBox(
            self.frame_val_top,
            width=300,
            values=["No OAS files found"],
            command=self.on_file_select,
        )
        self.cbo_files.grid(
            row=0, column=1, sticky="ew"
        )  # Changed from 'w' to 'ew' for expansion

        # Refresh Button (reload file list)
        self.btn_refresh_val = ctk.CTkButton(
            self.frame_val_top,
            text="↻ Refresh",
            width=80,
            command=self.update_file_list,
        )
        self.btn_refresh_val.grid(row=0, column=2, padx=(10, 0))

        # Filter Checkbox
        self.chk_ignore_br = ctk.CTkCheckBox(
            self.frame_val_top,
            text="Ignore 'Bad Request' Examples",
            command=self.on_filter_change,
        )
        self.chk_ignore_br.grid(row=0, column=3, padx=(20, 0), sticky="w")
        self.chk_ignore_br.select()  # Default Checked

        # Progress Bar (Indeterminate)
        self.progress_val = ctk.CTkProgressBar(self.tab_val, orientation="horizontal", mode="indeterminate")
        self.progress_val.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 5))
        self.progress_val.grid_remove() # Hide initially

        # Main Layout: List vs Chart

        # Use PanedWindow for resizable Log Console
        self.paned_val = tk.PanedWindow(
            self.tab_val, orient="vertical", sashrelief="raised", bg="#d0d0d0"
        )
        self.paned_val.grid(
            row=3, column=0, columnspan=2, sticky="nsew", padx=5, pady=5
        )

        # TOP PANE: Content (List + Chart)
        self.frame_val_content = ctk.CTkFrame(self.paned_val)
        self.paned_val.add(
            self.frame_val_content, minsize=200, sticky="nsew", stretch="always"
        )

        self.frame_val_content.grid_columnconfigure(0, weight=1)
        self.frame_val_content.grid_columnconfigure(1, weight=1)
        self.frame_val_content.grid_rowconfigure(0, weight=1)

        self.frame_list = ctk.CTkScrollableFrame(
            self.frame_val_content, label_text="Issues List"
        )
        self.frame_list.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=5)

        self.frame_chart_container = ctk.CTkFrame(self.frame_val_content)
        self.frame_chart_container.grid(
            row=0, column=1, sticky="nsew", padx=(5, 0), pady=5
        )
        self.chart = SemanticPieChart(self.frame_chart_container)
        self.chart.pack(fill="both", expand=True, padx=10, pady=10)

        # Log Pane (Created but added dynamically)
        self.val_log_frame = ctk.CTkFrame(self.paned_val)  # Container

        # Internal Log Header (Visible when expanded)
        self.log_internal_header = ctk.CTkFrame(
            self.val_log_frame,
            height=28,
            corner_radius=0,
            fg_color=("gray85", "gray20"),
        )
        self.log_internal_header.pack(fill="x", side="top")

        self.btn_toggle_log_h = ctk.CTkButton(
            self.log_internal_header,
            text="▼ Spectral Output",
            width=120,
            height=20,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.toggle_log,
        )
        self.btn_toggle_log_h.pack(side="left", padx=5, pady=2)

        # Spectral Output (Directly in frame, no tabs)
        self.val_log_frame_inner = ctk.CTkFrame(self.val_log_frame, fg_color="transparent")
        self.val_log_frame_inner.pack(fill="both", expand=True, padx=2, pady=0)

        spectral_log_theme = self.prefs_manager.get("spectral_log_theme", "Light")
        fg_col = "#1e1e1e" if spectral_log_theme == "Dark" else "#ffffff"
        txt_col = "#d4d4d4" if spectral_log_theme == "Dark" else "#333333"

        self.val_json_log = ctk.CTkTextbox(
            self.val_log_frame_inner,
            font=("Consolas", 11),
            state="normal",
            wrap="none",
            fg_color=fg_col,
            text_color=txt_col,
        )
        self.val_json_log.bind("<Key>", self._on_log_key_press)
        self.val_json_log.pack(fill="both", expand=True)

        # Remove old val_log (Analysis Log) reference
        self.val_log = None

        # Persistent Footer (Status Bar + Log Toggle) -> For Collapsed State
        self.footer_frame = ctk.CTkFrame(
            self.tab_val, height=30, corner_radius=0, fg_color=("gray85", "gray20")
        )
        self.footer_frame.grid(row=4, column=0, columnspan=2, sticky="ew")

        self.btn_toggle_log_f = ctk.CTkButton(
            self.footer_frame,
            text="▶ Spectral Output",
            width=120,
            height=24,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.toggle_log,
        )
        self.btn_toggle_log_f.pack(side="left", padx=5, pady=2)
        # ==========================
        # TAB 3: VIEW (REDOC)
        # ==========================
        self.tab_view_oas = self.tabview.add("View")
        self.tab_view_oas.grid_columnconfigure(0, weight=1)
        self.tab_view_oas.grid_rowconfigure(2, weight=1)  # Content at row 2

        # Top Bar - OAS Folder
        self.frame_view_folder = ctk.CTkFrame(self.tab_view_oas, fg_color="transparent")
        self.frame_view_folder.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))
        self.frame_view_folder.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self.frame_view_folder, text="OAS Folder:", font=ctk.CTkFont(weight="bold")
        ).grid(row=0, column=0, padx=(0, 10), sticky="w")
        self.entry_view_oas_folder = ctk.CTkEntry(
            self.frame_view_folder, placeholder_text="Path to OAS folder..."
        )
        self.entry_view_oas_folder.grid(row=0, column=1, padx=(0, 10), sticky="ew")
        # Sync with Generation tab (which uses preferences)
        self.entry_view_oas_folder.insert(0, self.entry_oas_folder.get())
        self.btn_browse_view_oas = ctk.CTkButton(
            self.frame_view_folder,
            text="Browse",
            width=80,
            command=self.browse_oas_folder_view,
        )
        self.btn_browse_view_oas.grid(row=0, column=2)

        # Top Bar - File Selector (row 1)
        self.frame_view_top = ctk.CTkFrame(self.tab_view_oas, fg_color="transparent")
        self.frame_view_top.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

        ctk.CTkLabel(
            self.frame_view_top, text="Select File:", font=ctk.CTkFont(weight="bold")
        ).pack(side="left", padx=(0, 10))

        # Combobox expands to fill available space
        self.cbo_view_files = ctk.CTkComboBox(
            self.frame_view_top,
            width=400,
            values=["No OAS files found"],
            command=self.on_view_file_select,
        )
        self.cbo_view_files.pack(side="left", fill="x", expand=True)

        self.btn_refresh_view = ctk.CTkButton(
            self.frame_view_top,
            text="↻ Refresh",
            width=80,
            command=self.refresh_view_files,
        )
        self.btn_refresh_view.pack(side="left", padx=(10, 0))

        # View Documentation button (no emoji, standard text)
        self.btn_open_viewer = ctk.CTkButton(
            self.frame_view_top,
            text="View Documentation",
            width=150,
            command=self.open_documentation_viewer,
        )
        self.btn_open_viewer.pack(side="left", padx=(10, 0))

        # Content Area - YAML Viewer with syntax highlighting (full width) - row 2
        self.frame_yaml = ctk.CTkFrame(self.tab_view_oas)
        self.frame_yaml.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        # Header bar with title and theme selector
        self.yaml_header = ctk.CTkFrame(self.frame_yaml, fg_color="transparent")
        self.yaml_header.pack(fill="x", padx=5, pady=2)

        ctk.CTkLabel(
            self.yaml_header, text="YAML Source", font=ctk.CTkFont(weight="bold")
        ).pack(side="left")

        # Sync Viewer button - Show current YAML section in documentation
        # Starts hidden until a viewer is opened (shown via pack in open_docked_doc)
        self.btn_sync_viewer = ctk.CTkButton(
            self.yaml_header,
            text="Locate in Docs",
            width=115,
            height=24,
            font=("Arial", 11),
            command=self.sync_viewer,
        )
        # Don't pack yet - will be packed when viewer opens

        # Marker navigation variable (buttons will be packed on right side later)
        self.current_marker_index = -1  # Track current position in markers list

        # Custom colorschemes directory
        if getattr(sys, "frozen", False):
            self.colorschemes_dir = os.path.join(sys._MEIPASS, "src", "colorschemes")
        else:
            self.colorschemes_dir = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "colorschemes"
            )

        # Theme selector on the right (custom + bundled themes)
        self.available_themes = [
            "oas-dark",
            "oas-light",  # Custom app themes
            "github-dark",
            "nord",
            "one-dark",
            "vs-dark",  # Custom popular themes
            "monokai",
            "dracula",
            "ayu-dark",
            "ayu-light",  # Bundled chlorophyll themes
        ]
        self.cbo_yaml_theme = ctk.CTkComboBox(
            self.yaml_header,
            width=140,
            values=self.available_themes,
            command=self.on_theme_change,
        )
        self.cbo_yaml_theme.set(self.prefs_manager.get("yaml_theme", "oas-dark"))
        self.cbo_yaml_theme.pack(side="right")
        ctk.CTkLabel(self.yaml_header, text="Theme:", font=ctk.CTkFont(size=12)).pack(
            side="right", padx=(0, 5)
        )

        # Font size slider (before theme)
        self.lbl_font_val = ctk.CTkLabel(
            self.yaml_header,
            text=str(self.prefs_manager.get("yaml_font_size", 12)),
            width=25,
        )
        self.lbl_font_val.pack(side="right", padx=(0, 10))
        self.slider_font_size = ctk.CTkSlider(
            self.yaml_header,
            from_=8,
            to=20,
            number_of_steps=12,
            width=100,
            command=self._on_font_size_change,
        )
        self.slider_font_size.set(self.prefs_manager.get("yaml_font_size", 12))
        self.slider_font_size.pack(side="right")
        ctk.CTkLabel(self.yaml_header, text="Font:", font=ctk.CTkFont(size=12)).pack(
            side="right", padx=(0, 5)
        )

        # Marker navigation buttons (right side, near font) - initially hidden
        self.nav_frame = ctk.CTkFrame(self.yaml_header, fg_color="transparent")
        # Don't pack yet - will be shown only when there are markers

        self.btn_last_marker = ctk.CTkButton(
            self.nav_frame,
            text="»",
            width=26,
            height=22,
            font=("Arial", 14),
            command=self._goto_last_marker,
        )
        self.btn_last_marker.pack(side="right", padx=1)

        self.btn_next_marker = ctk.CTkButton(
            self.nav_frame,
            text="›",
            width=26,
            height=22,
            font=("Arial", 14),
            command=self._goto_next_marker,
        )
        self.btn_next_marker.pack(side="right", padx=1)
        # Marker position counter - clickable button to jump to current marker
        self.btn_marker_pos = ctk.CTkButton(
            self.nav_frame,
            text="1/1",
            width=50,
            height=22,
            font=("Arial", 10),
            fg_color=("#D0D0D0", "#4A4A4A"),  # Light gray / dark gray
            hover_color=("#B0B0B0", "#5A5A5A"),  # Darker on hover
            text_color=("#333333", "#FFFFFF"),
            corner_radius=4,
            command=self._goto_current_marker,
        )
        self.btn_marker_pos.pack(side="right", padx=3)

        self.btn_prev_marker = ctk.CTkButton(
            self.nav_frame,
            text="‹",
            width=26,
            height=22,
            font=("Arial", 14),
            command=self._goto_prev_marker,
        )
        self.btn_prev_marker.pack(side="right", padx=1)

        self.btn_first_marker = ctk.CTkButton(
            self.nav_frame,
            text="«",
            width=26,
            height=22,
            font=("Arial", 14),
            command=self._goto_first_marker,
        )
        self.btn_first_marker.pack(side="right", padx=1)
        # CodeView with YAML lexer and line numbers
        self._current_marker_line = None
        yaml_font_size = self.prefs_manager.get("yaml_font_size", 12)
        yaml_font_family = self.prefs_manager.get("yaml_font", "Consolas")
        self.txt_yaml = CodeView(
            self.frame_yaml,
            lexer=pygments.lexers.YamlLexer,
            color_scheme="monokai",  # Use built-in initially
            font=(yaml_font_family, yaml_font_size),
        )
        self.txt_yaml.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Bind Ctrl+F for search
        self.txt_yaml.bind("<Control-f>", self._show_search_dialog)
        
        # Override Double-Click Selection to trim punctuation
        # Using add="+" so we don't prevent Tkinter's default behavior
        self.txt_yaml.bind("<Double-Button-1>", self._on_yaml_double_click, add="+")
        
        # Fix selection anchor before Shift+Arrow keys
        self.txt_yaml.bind("<Shift-Left>", self._on_shift_left)
        self.txt_yaml.bind("<Shift-Right>", self._on_shift_right)

        # Apply saved theme after initialization
        saved_theme = self.prefs_manager.get("yaml_theme", "oas-dark")
        self.after(100, lambda: self.on_theme_change(saved_theme))

        # Redoc Generator initialization
        self.redoc_gen = RedocGenerator()

        # self.val_log_print("Ready.") # Removed - handled by [Init] log
        self.log_visible = False
        
        # Load file lists on startup (after widgets are ready)
        self.after(200, self._load_files_on_startup)



    def _create_menu(self):
        """Create standard menu bar."""
        menubar = tk.Menu(self)
        self.file_menu = tk.Menu(menubar, tearoff=0)  # Save reference for enabling/disabling
        
        # File Menu
        self.file_menu.add_command(label="Select Import Source...", command=self._smart_select_import)
        self.file_menu.add_command(label="Select Template Folder...", command=self._smart_select_template)
        self.file_menu.add_command(label="Select Output Folder...", command=self._smart_select_output)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.destroy)
        menubar.add_cascade(label="File", menu=self.file_menu)
        
        # Edit Menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Preferences", command=self.open_preferences)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        # View Menu (Generation, Validation, YAML Viewer)
        self.view_menu = tk.Menu(menubar, tearoff=0)
        self.view_menu.add_command(label="OAS to Excel", command=self._view_import)
        self.view_menu.add_command(label="Excel to OAS", command=self._view_generation)
        self.view_menu.add_command(label="Validation", command=self._view_validation)
        self.view_menu.add_command(label="YAML Viewer", command=self._view_yaml_viewer)
        self.view_menu.add_separator()
        self.view_menu.add_command(
            label="Application Logs...", command=self.show_application_logs
        )
        menubar.add_cascade(label="View", menu=self.view_menu)

        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="User Guide", command=self.open_user_guide)
        help_menu.add_command(label="About", command=self.show_about_dialog)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        # Attach menu to root window (this will attach it to the ctk window)
        # Note: ctk doesn't directly support standard menus well on all platforms,
        # but configured it on the underlying tk root usually works on Windows.
        self.config(menu=menubar)

    def show_application_logs(self):
        """Open detached application logs window."""
        if self.log_window is None or not self.log_window.winfo_exists():
            theme = self.prefs_manager.get("app_log_theme", "Dark") # Default Dark
            self.log_window = LogWindow(self, theme=theme)
            self.log_window.on_close_callback = self._on_log_window_close

            # Populate with history
            for line in self.log_history:
                self.log_window.append_log(line)

        else:
            self.log_window.lift()
            self.log_window.focus()

    def _on_log_window_close(self):
        """Callback when log window is closed."""
        self.log_window = None

    def _on_tab_change(self):
        """Handle tab changes to update menu state."""
        current_tab = self.tabview.get()
        
        # Enable 'Select Template Folder' only in Generation tab
        # Enable 'Select Template Folder' only in Generation tab
        if current_tab == "Excel to OAS":
            self.file_menu.entryconfig("Select Template Folder...", state="normal")
            self.file_menu.entryconfig("Select Import Source...", state="disabled")
        elif current_tab == "OAS to Excel":
            self.file_menu.entryconfig("Select Template Folder...", state="disabled")
            self.file_menu.entryconfig("Select Import Source...", state="normal")
        else:
            self.file_menu.entryconfig("Select Template Folder...", state="disabled")
            self.file_menu.entryconfig("Select Import Source...", state="disabled")
            
        if current_tab == "Validation":
            self.run_validation()

    def _view_yaml_viewer(self):
        self.tabview.set("View")

    def _smart_select_import(self):
        """Switch to OAS to Excel tab and open source selector."""
        self.tabview.set("OAS to Excel")
        self.after(500, lambda: self.browse_import_source_folder())

    def _smart_select_template(self):
        """Switch to Generation tab and open template selector."""
        self.tabview.set("Excel to OAS")
        # Use delay to ensure tab switch renders and state updates
        self.after(1000, lambda: self.browse_dir()) # Increased delay just in case

    def _smart_select_output(self):
        """Switch to Generation tab and open output folder selector."""
        self.tabview.set("Excel to OAS")
        self.update_idletasks()
        self.browse_oas_folder()

    def _view_import(self):
        self.tabview.set("OAS to Excel")

    def _view_generation(self):
        self.tabview.set("Excel to OAS")

    def _view_validation(self):
        self.tabview.set("Validation")
        
    def _load_files_on_startup(self):
        """Load file lists in Validation and View tabs on startup."""
        self.log_app("[Init] Application Ready.")
        
        oas_dir = self.entry_oas_folder.get()
        if os.path.exists(oas_dir):
            self.update_file_list()
        else:
            # Benign info log, don't scare the user
            self.log_app(f"[Init] Default output folder not found (will be created on first generation): {oas_dir}")
        
        # Apply all preferences (themes, fonts, etc.) on startup
        self._apply_preferences(self.prefs_manager.get_all())


    def _load_custom_theme(self, theme_name):
        """Load a custom TOML theme file and return as dict."""
        import toml

        custom_path = os.path.join(self.colorschemes_dir, f"{theme_name}.toml")
        if os.path.exists(custom_path):
            return toml.load(custom_path)
        return None

    def on_theme_change(self, theme_name):
        """Change the color scheme of the YAML viewer."""
        try:
            # Check if it's a custom theme (in our colorschemes folder)
            theme_dict = self._load_custom_theme(theme_name)
            if theme_dict:
                self.txt_yaml._set_color_scheme(theme_dict)
            else:
                # Use bundled chlorophyll theme
                self.txt_yaml._set_color_scheme(theme_name)

            # Reapply validation markers with new theme colors
            current_file = (
                self.cbo_view_files.get() if hasattr(self, "cbo_view_files") else None
            )
            if current_file:
                self._apply_validation_markers(current_file)

        except Exception as e:
            self.val_log_print(f"Error changing theme: {e}")

    # Tooltips removed


    def _on_font_size_change(self, value):
        """Handle font size slider change in View tab."""
        font_size = int(value)
        self.lbl_font_val.configure(text=str(font_size))
        try:
            self.txt_yaml.configure(font=("Consolas", font_size))
            # Save to preferences
            self.prefs_manager.set("yaml_font_size", font_size)
            self.prefs_manager.save()
        except (tk.TclError, AttributeError):
            pass

    def _on_close(self):
        """Handle window close - save geometry and exit."""
        if self.prefs_manager.get("remember_window_pos"):
            geometry = self.geometry()
            self.prefs_manager.set("window_geometry", geometry)
            self.prefs_manager.save()
        self.destroy()

    def open_preferences(self):
        """Open the preferences dialog."""
        dialog = PreferencesDialog(
            self, self.prefs_manager, on_save_callback=self._apply_preferences
        )
        self.wait_window(dialog)

    def show_about_dialog(self):
        """Show About dialog using SplashScreen."""
        try:
            # Create splash as generic toplevel
            splash = SplashScreen(root=self)
            
            # Configure About Layout
            description = (
                "The OAS Integration Suite is a toolset for the design,\n"
                "generation, validation, and documentation of\n"
                "OpenAPI Specifications."
            )
            splash.set_about_mode(f"v{VERSION}", description)
            
            # Use destroy instead of close to avoid app shutdown logic if any
            # SplashScreen.close calls destroy() which is fine.
            splash.root.bind("<Button-1>", lambda e: splash.close())
            
        except Exception as e:
            print(f"Error showing about dialog: {e}")

    def open_user_guide(self):
        """Open the HTML User Guide."""
        import webbrowser
        try:
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            doc_path = os.path.join(base_path, 'src', 'docs', 'user_manual.html')
            
            if os.path.exists(doc_path):
                webbrowser.open_new_tab(f"file:///{doc_path}")
            else:
                # Fallback or dev mode simplified path check
                # Try finding it relative to current script if above failed
                dev_path = os.path.join(os.getcwd(), 'src', 'docs', 'user_manual.html')
                if os.path.exists(dev_path):
                    webbrowser.open_new_tab(f"file:///{dev_path}")
                else:
                    self.val_log_print(f"Documentation not found at: {doc_path}")
                    tk.messagebox.showerror("Error", "User Guide not found.")
        except Exception as e:
            print(f"Error opening user guide: {e}")

    def open_faq(self):
        """Open the HTML FAQ."""
        import webbrowser
        try:
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            doc_path = os.path.join(base_path, 'src', 'docs', 'faq.html')
            
            if os.path.exists(doc_path):
                webbrowser.open_new_tab(f"file:///{doc_path}")
            else:
                # Fallback or dev mode simplified path check
                dev_path = os.path.join(os.getcwd(), 'src', 'docs', 'faq.html')
                if os.path.exists(dev_path):
                    webbrowser.open_new_tab(f"file:///{dev_path}")
                else:
                    self.val_log_print(f"FAQ not found at: {doc_path}")
                    tk.messagebox.showerror("Error", "FAQ not found.")
        except Exception as e:
            print(f"Error opening FAQ: {e}")

    def _apply_preferences(self, new_prefs: dict):
        """Apply new preferences to the UI."""
        # Apply YAML theme
        if "yaml_theme" in new_prefs:
            self.on_theme_change(new_prefs["yaml_theme"])
            # Update combo if it exists (legacy support or logic separation)
            if hasattr(self, "cbo_yaml_theme"):
                self.cbo_yaml_theme.set(new_prefs["yaml_theme"])

        # Apply font size (if CodeView supports it)
        if "yaml_font_size" in new_prefs:
            try:
                font_size = new_prefs["yaml_font_size"]
                # Ensure txt_yaml exists
                if hasattr(self, "txt_yaml"):
                    current_font = self.txt_yaml.cget("font")
                    if isinstance(current_font, tuple):
                        self.txt_yaml.configure(font=(current_font[0], font_size))
                    else:
                        self.txt_yaml.configure(font=("Consolas", font_size))
            except (tk.TclError, AttributeError, TypeError):
                pass

        # Apply generation checkboxes
        if new_prefs.get("gen_oas_30", True):
            self.var_30.set(True)
        else:
            self.var_30.set(False)

        if new_prefs.get("gen_oas_31", True):
            self.var_31.set(True)
        else:
            self.var_31.set(False)

        if new_prefs.get("gen_oas_swift", False):
            self.var_swift.set(True)
        else:
            self.var_swift.set(False)

        # Apply validation checkbox
        if new_prefs.get("ignore_bad_request", True):
            self.chk_ignore_br.select()
        else:
            self.chk_ignore_br.deselect()

        # Apply log themes immediately
        if "gen_log_theme" in new_prefs:
            theme = new_prefs["gen_log_theme"]
            if theme == "Dark":
                self.log_area.configure(fg_color="#1e1e1e", text_color="#d4d4d4")
            else:
                self.log_area.configure(fg_color="#ffffff", text_color="#333333")

        if "app_log_theme" in new_prefs:
            theme = new_prefs["app_log_theme"]
            if self.log_window:
                self.log_window.apply_theme(theme)

        if "import_log_theme" in new_prefs:
            theme = new_prefs["import_log_theme"]
            if hasattr(self, 'import_log_area'):
                if theme == "Dark":
                    self.import_log_area.configure(fg_color="#1e1e1e", text_color="#d4d4d4")
                else:
                    self.import_log_area.configure(fg_color="#ffffff", text_color="#333333")

        if "spectral_log_theme" in new_prefs:
            theme = new_prefs["spectral_log_theme"]
            if theme == "Dark":
                self.val_json_log.configure(fg_color="#1e1e1e", text_color="#d4d4d4")
            else:
                self.val_json_log.configure(fg_color="#ffffff", text_color="#333333")

        # Refresh file list with new sort order
        # Refresh file list with new sort order
        self.update_file_list()

        # [Init] Application Ready moved to _load_files_on_startup to ensure it's last

    def toggle_log(self):
        if self.log_visible:
            # COLLAPSE
            self.paned_val.forget(self.val_log_frame)  # Hide Pane 2
            self.footer_frame.grid()  # Show Footer
            self.log_visible = False
        else:
            # EXPAND
            self.footer_frame.grid_remove()  # Hide Footer
            self.paned_val.add(
                self.val_log_frame, minsize=100, sticky="nsew", stretch="always"
            )  # Show Pane 2
            self.log_visible = True

    def val_log_print(self, msg):
        # Redirect to global application log via self.log_app to ensure timestamp
        # self.log_app already handles history and window appending
        self.log_app(f"[Validation] {msg}")
            
        print(f"[Validation] {msg}") # Keep stdout for debugging

    def browse_dir(self):
        current_path = self.entry_dir.get()
        initial_dir = current_path if os.path.exists(current_path) else os.getcwd()
        directory = filedialog.askdirectory(initialdir=initial_dir)
        if directory:
            self.entry_dir.delete(0, "end")
            self.entry_dir.insert(0, directory)
            self.prefs_manager.set("excel_input_folder", directory)
            self.prefs_manager.set("last_excel_input", directory)
            self.prefs_manager.save()

    def _sync_oas_folders(self, new_path):
        """Sync OAS folder value across all tabs."""
        # Update Generation tab
        self.entry_oas_folder.delete(0, "end")
        self.entry_oas_folder.insert(0, new_path)
        # Update Validation tab
        self.entry_val_oas_folder.delete(0, "end")
        self.entry_val_oas_folder.insert(0, new_path)
        # Update View tab
        self.entry_view_oas_folder.delete(0, "end")
        self.entry_view_oas_folder.insert(0, new_path)
        # Clear last generated files so update_file_list reads from folder
        self.last_generated_files = []
        # Refresh file lists
        self.update_file_list()
        self.update_file_list()
        self.refresh_view_files()
        # Save preference
        self.prefs_manager.set("oas_folder", new_path)
        self.prefs_manager.set("last_oas_folder", new_path)
        self.prefs_manager.save()

    def browse_oas_folder(self):
        """Browse for OAS folder (Generation tab)."""
        current_path = self.entry_oas_folder.get()
        initial_dir = current_path if os.path.exists(current_path) else os.getcwd()
        directory = filedialog.askdirectory(initialdir=initial_dir)
        if directory:
            self._sync_oas_folders(directory)

    def browse_oas_folder_validation(self):
        """Browse for OAS folder (Validation tab)."""
        current_path = self.entry_val_oas_folder.get()
        initial_dir = current_path if os.path.exists(current_path) else os.getcwd()
        directory = filedialog.askdirectory(initialdir=initial_dir)
        if directory:
            self._sync_oas_folders(directory)

    def browse_oas_folder_view(self):
        """Browse for OAS folder (View tab)."""
        current_path = self.entry_view_oas_folder.get()
        initial_dir = current_path if os.path.exists(current_path) else os.getcwd()
        directory = filedialog.askdirectory(initialdir=initial_dir)
        if directory:
            self._sync_oas_folders(directory)

    def update_font_size_gen(self, value):
        val = int(value)
        self.log_area.configure(font=("Consolas", val))
        self.lbl_font_size_gen_val.configure(text=str(val))

    def log_gen(self, message):
        # Timestamp Construction (For App Log only)
        now = datetime.datetime.now()
        timestamp = f"{now.strftime('%H:%M:%S')}.{now.microsecond // 1000:03d}"
        
        # 1. GUI Message (No Timestamp per user request)
        gui_msg = message
        
        # 2. App Log Message (With Timestamp)
        full_msg = f"{timestamp} > {message}"

        # Update Generation Tab Log
        self.log_area.configure(state="normal")
        
        # Formatting for "Done!" message (Green + Bold)
        # Formatting for "Done!" message (Green + Bold)
        self.log_area.insert("end", gui_msg + "\n")
        
        self.log_area.see("end")
        self.log_area.configure(state="disabled")
        
        # Duplicate to Global Application Log (with timestamp)
        self._log_history_append(full_msg)


    def log_app(self, message):
        # Add Timestamp: HH:MM:SS.mmm > 
        now = datetime.datetime.now()
        timestamp = f"{now.strftime('%H:%M:%S')}.{now.microsecond // 1000:03d}"
        full_msg = f"{timestamp} > {message}"
        
        # Write to Global Application Log ONLY
        self._log_history_append(full_msg)

    def _log_history_append(self, full_msg):
        # Add to history
        self.log_history.append(full_msg)
        if len(self.log_history) > 1000:
            self.log_history.pop(0)

        # Update window if open
        if self.log_window and self.log_window.winfo_exists():
            self.log_window.append_log(full_msg)

    def _show_log_context_menu(self, event):
        """Show context menu for log area."""
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Clear Log", command=self.clear_gen_log)
        menu.add_separator()
        menu.add_command(label="Copy", command=lambda: self.log_area.event_generate("<<Copy>>"))
        menu.post(event.x_root, event.y_root)

    def clear_gen_log(self):
        """Clear the generation log area."""
        self.log_area.configure(state="normal")
        self.log_area.delete("1.0", "end")
        self.log_area.configure(state="disabled")

    def start_generation(self):
        base_dir = self.entry_dir.get()
        gen_30 = self.var_30.get()
        gen_31 = self.var_31.get()
        gen_swift = self.var_swift.get()

        if not base_dir:
            self.log_gen("ERROR: Please select a directory.")
            return

        self.btn_gen.configure(state="disabled", text="GENERATING...")
        self.log_gen("Starting generation process...")

        t = threading.Thread(
            target=self.run_process, args=(base_dir, gen_30, gen_31, gen_swift)
        )
        t.start()

    def run_process(self, base_dir, gen_30, gen_31, gen_swift):
        try:
            self.last_generated_files = []
            output_dir = self.entry_oas_folder.get()  # Get OAS output folder

            def gui_logger(msg):
                self.after(0, self.log_gen, msg)
                if "Writing OAS" in msg:
                    parts = msg.split(": ")
                    if len(parts) > 1:
                        self.last_generated_files.append(parts[1].strip())
                        self.after(0, self.update_file_list)

            main_script.generate_oas(
                base_dir,
                gen_30=gen_30,
                gen_31=gen_31,
                gen_swift=gen_swift,
                output_dir=output_dir,
                log_callback=gui_logger,
            )

        except Exception as e:
            self.after(0, self.log_gen, f"CRITICAL ERROR: {e}")
        finally:

            def reset_btn():
                self.btn_gen.configure(state="normal", text="GENERATE")
                self.after(0, self.update_file_list)  # Final refresh

            self.after(0, reset_btn)

    def update_file_list(self):
        files_to_show = []
        candidates = set()  # Use set to avoid duplicates

        # Always read from OAS folder
        oas_dir = self.entry_oas_folder.get()
        if os.path.exists(oas_dir):
            for f in os.listdir(oas_dir):
                if f.endswith(".yaml") or f.endswith(".json"):
                    candidates.add(os.path.join(oas_dir, f))

        # Also add last generated files (in case they're in a different folder)
        for f in self.last_generated_files:
            if os.path.exists(f):
                candidates.add(f)

        # Sort based on preference
        sort_order = self.prefs_manager.get("file_sort_order", "alphabetical")
        if sort_order == "newest_first":
            sorted_candidates = sorted(
                candidates, key=lambda f: os.path.getmtime(f), reverse=True
            )
        elif sort_order == "oldest_first":
            sorted_candidates = sorted(candidates, key=lambda f: os.path.getmtime(f))
        else:  # alphabetical
            sorted_candidates = sorted(candidates)

        self.file_map = {}
        display_names = []
        for path in sorted_candidates:
            name = os.path.basename(path)
            self.file_map[name] = path
            display_names.append(name)

        if display_names:
            self.cbo_files.configure(values=display_names)
            self.cbo_files.set(display_names[0])
            # Always run validation on file selection
            # self.run_validation() # Disabled auto-run on startup
        else:
            self.cbo_files.configure(values=["No OAS files found"])
            self.cbo_files.set("No OAS files found")

        # Refresh View Tab
        self.refresh_view_files()

    def on_file_select(self, value):
        # Sync with View tab combo and load YAML
        if value in self.view_file_map:
            self.cbo_view_files.set(value)
            self.on_view_file_select(value)  # Load YAML content in View tab
        self.run_validation()

    def run_validation(self):
        selected_name = self.cbo_files.get()
        selected_file = self.file_map.get(selected_name)

        if not selected_file or not os.path.exists(selected_file):
            self.val_log_print("File not found or not selected.")
            return

        # Optimization: Check if file needs re-validation
        current_mtime = os.path.getmtime(selected_file)
        # Use normpath to ensure path string consistency
        if (self.validated_file_path and selected_file and
            os.path.normcase(os.path.normpath(self.validated_file_path)) == os.path.normcase(os.path.normpath(selected_file)) and 
            self.validated_file_mtime == current_mtime):
             self.val_log_print(f"File '{selected_name}' unchanged. Using cached validation results.")
             return
            
        # Update cache state (full path for caching)
        self.validated_file_path = selected_file
        self.validated_file_mtime = current_mtime
        
        self.val_log_print(f"Starting validation for: {selected_name}")
        
        # Show Floating Progress Modal (Splash Style)
        prog_win, prog_lbl = self._show_progress_modal("Running Spectral...")

        for widget in self.frame_list.winfo_children():
            widget.destroy()

        def validate_thread():
            try:
                # Capture logs from linter
                def thread_logger(msg):
                    self.after(0, lambda: self.val_log_print(msg))

                result = self.linter.run_lint(selected_file, log_callback=thread_logger)
                # Pass prog_win and prog_lbl for label update and closing
                self.after(0, lambda: self.show_results(result, prog_win, prog_lbl))
            except Exception as e:
                self.after(0, lambda: self.val_log_print(f"THREAD CRASH: {e}"))
                self.after(0, prog_win.destroy) # Close on error
            finally:
                pass # Closed by show_results or exception handler

        t = threading.Thread(target=validate_thread)
        t.start()

    def _show_progress_modal(self, message="Validating..."):
        """Create a floating modal with progress bar."""
        top = ctk.CTkToplevel(self)
        top.title("")
        top.geometry("300x120")
        top.overrideredirect(True) # Splash screen style (no borders)
        top.resizable(False, False)
        # Center the modal
        top.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - 150
        y = self.winfo_y() + (self.winfo_height() // 2) - 60
        top.geometry(f"+{x}+{y}")
        
        top.transient(self) # Keep on top of main window
        top.grab_set()      # RAM: Modal behavior
        top.focus_set()
        
        # Container Frame with Border
        main_frame = ctk.CTkFrame(top, border_width=1, border_color="#555555", corner_radius=0)
        main_frame.pack(fill="both", expand=True)

        lbl = ctk.CTkLabel(main_frame, text=message, font=ctk.CTkFont(size=14, weight="bold"))
        lbl.pack(pady=(20, 10))
        
        prog = ctk.CTkProgressBar(main_frame, mode="indeterminate", width=250)
        prog.pack(pady=10)
        prog.start()
        
        # Return both window and label for dynamic updates
        return top, lbl

    def on_filter_change(self):
        if self.last_lint_result:
            self.show_results(self.last_lint_result)

    def show_results(self, result, progress_window=None, progress_label=None):
        self.last_lint_result = result  # Store for filtering

        # Helper to close progress
        def close_progress():
            if progress_window:
                progress_window.destroy()

        if not result["success"]:
            self.val_log_print(f"Error: {result.get('error_msg', 'Unknown Error')}")
            self.frame_list.configure(label_text="Error")
            # Clear previous
            for widget in self.frame_list.winfo_children():
                widget.destroy()

            err_lbl = ctk.CTkLabel(
                self.frame_list,
                text=result.get("error_msg", "Unknown Error"),
                text_color="red",
            )
            err_lbl.pack()
            close_progress()
            return

        summary = result["summary"]
        code_summary = result.get("code_summary", summary)  # Fallback if missing
        details = result["details"]

        # Apply Filters
        if self.chk_ignore_br.get() == 1:
            filtered_details = []
            # Recalculate code_summary from filtered details
            filtered_code_summary = {}
            filtered_summary = {"error": 0, "warning": 0, "info": 0, "hint": 0}

            for item in details:
                path_str = item.get("path", "")
                # Filter Condition: Path contains 'examples' AND 'Bad Request' (case insensitive match if needed, but usually strict)
                # Adding some flexibility: "examples" > ... "Bad Request"
                if "examples" in path_str and "Bad Request" in path_str:
                    continue  # Skip this issue

                filtered_details.append(item)

                # Rebuild stats
                code = item["code"]
                sev = item["severity"]
                filtered_summary[sev] = filtered_summary.get(sev, 0) + 1

                if code not in filtered_code_summary:
                    filtered_code_summary[code] = {"count": 0, "severity": sev}
                filtered_code_summary[code]["count"] += 1

            details = filtered_details
            summary = filtered_summary
            code_summary = filtered_code_summary

        total_issues = len(details)

        self.val_log_print(f"Check Complete: {total_issues} issues found.")
        self.frame_list.configure(label_text=f"Issues ({total_issues})")

        # Store validation issues by line for YAML viewer markers
        # Update validated_file to basename for marker matching (full path stays in validated_file_path)
        self.validated_file = self.cbo_files.get()  # Get filename (basename) being validated
        self.validation_issues = {}
        for item in details:
            line = item.get("line", 0)
            if line > 0:
                if line not in self.validation_issues:
                    self.validation_issues[line] = []
                self.validation_issues[line].append(
                    {
                        "severity": item["severity"],
                        "message": item["message"],
                        "code": item["code"],
                    }
                )

        # Update Chart - Use code_summary for detailed breakdown
        self.chart.set_data(code_summary)
        
        # Load Source Map if available
        self.current_source_map = {}
        try:
            if self.validated_file:
                # validated_file is just the basename (from checkbox)
                # We need the full path from self.file_map
                full_path = self.file_map.get(self.validated_file)
                if full_path:
                    dir_name = os.path.dirname(full_path)
                    map_path = os.path.join(dir_name, ".oasis_excel_maps", self.validated_file + ".map.json")
                    if os.path.exists(map_path):
                        with open(map_path, "r", encoding="utf-8") as f:
                            self.current_source_map = json.load(f)
        except Exception as e:
            print(f"Error loading source map: {e}")

        # Populate Raw JSON Tab
        raw_data = result.get("raw_data", [])
        formatted_json = json.dumps(raw_data, indent=2)

        self.val_json_log.delete("0.0", "end")
        self.val_json_log.insert("0.0", formatted_json)

        # Update modal message for card construction phase
        if progress_label:
            progress_label.configure(text="Building issue list...")
            self.update_idletasks()  # Force label update
        
        # Populate List - Clear previous cards
        for widget in self.frame_list.winfo_children():
            widget.destroy()

        if total_issues == 0:
            ctk.CTkLabel(
                self.frame_list,
                text="No issues found! Great job!",
                text_color="#0A809E",
                font=("Arial", 16),
            ).pack(pady=20)
        else:
            for item in details:
                # Card Frame - RESTORED BOX (Subtle & Elegant)
                # Tuned for visual comfort: #E0E0E0 prevents the "glare" of pure white
                card = ctk.CTkFrame(
                    self.frame_list,
                    border_width=1,
                    border_color="#C0C0C0",  # Slightly darker border for definition
                    fg_color=("#E0E0E0", "#2B2B2B"),  # Calm grey in light mode
                    corner_radius=6,
                )
                card.pack(fill="x", pady=3, padx=2)  # Balanced spacing

                # Row 1: Code + Severity
                r1 = ctk.CTkFrame(card, fg_color="transparent")
                r1.pack(fill="x", padx=6, pady=6)

                # SEVERITY BADGE (Colored Label)
                badge_fg = "gray"
                badge_text_color = "white"
                if item["severity"] == "error":
                    badge_fg = "#FF4444"
                elif item["severity"] == "warning":
                    badge_fg = "#FFBB33"
                    badge_text_color = "black"  # Black text on Yellow for readability
                elif item["severity"] == "info":
                    badge_fg = "#33B5E5"

                ctk.CTkLabel(
                    r1,
                    text=f" {item['severity'].upper()} ",  # Spaces for padding effect
                    fg_color=badge_fg,
                    text_color=badge_text_color,
                    corner_radius=6,  # Rounded badge
                    font=("Arial", 10, "bold"),
                    height=20
                ).pack(side="left")

                ctk.CTkLabel(
                    r1,
                    text=item["code"],
                    font=("Arial", 11, "bold"),
                    text_color=("#333333", "#F0F0F0") # Dark in light mode
                ).pack(
                    side="left", padx=8
                )

                # Clickable line number - styled as minimal button
                line_num = item["line"]
                line_btn = ctk.CTkButton(
                    r1,
                    text=f"Line {line_num}",
                    font=("Arial", 10),
                    fg_color="transparent",
                    text_color=("#666666", "#AAAAAA"),
                    hover_color=("#D0D0D0", "#3A3A3A"), # Darker than bg for visibility
                    border_width=1,
                    border_color=("#BBBBBB", "#555555"),
                    corner_radius=4,
                    width=60,
                    height=20,
                    command=lambda ln=line_num: self._goto_line(ln),
                )
                line_btn.pack(side="right")

                # Excel Link (Moved to Header) - "Open Template"
                if self.current_source_map and item["path"]:
                     source_info = self._resolve_source_file(item["path"])
                     if source_info:
                         # Handle both string (old) and dict (new) format
                         if isinstance(source_info, dict):
                             filename = source_info.get("file")
                             sheetname = source_info.get("sheet")
                         else:
                             filename = source_info
                             sheetname = None

                         if filename:
                             ctk.CTkButton(
                                 r1, # Pack in Row 1
                                 text="Template Sheet",
                                 height=20,
                                 width=100,
                                 fg_color="transparent",
                                 border_width=1,          # Thinner 1px
                                 border_color="#107C41",  # Excel Green
                                 text_color="#107C41",    
                                 hover_color="#E6F2EA",  
                                 font=("Arial", 10, "bold"),
                                 corner_radius=4,
                                 command=lambda f=filename, s=sheetname: self._open_excel_file(f, s)
                             ).pack(side="right", padx=5)

                # Row 2: Path
                if item["path"] and item["path"] != "Root":
                    path_color = ("#555555", "#AAAAAA")
                    ctk.CTkLabel(
                        card,
                        text=f"Path: {item['path']}",
                        text_color=path_color,
                        font=("Consolas", 10),
                        anchor="w",
                        justify="left",
                        wraplength=350,
                    ).pack(fill="x", padx=5, pady=2)

                # Row 3: Message
                ctk.CTkLabel(
                    card,
                    text=item["message"],
                    anchor="w",
                    justify="left",
                    wraplength=350,
                    font=("Arial", 11),
                    text_color=("#333333", "#FFFFFF") # Standard text color
                ).pack(fill="x", padx=5, pady=(0, 5))

        # Force complete rendering of all cards BEFORE closing modal
        # This ensures the "PAM!" effect where everything appears at once
        self.update()
        
        # Refresh markers in View tab if viewing the same file
        current_view_file = (
            self.cbo_view_files.get() if hasattr(self, "cbo_view_files") else None
        )
        if current_view_file and current_view_file == self.validated_file:
            self._apply_validation_markers(current_view_file)

        # Close progress modal after everything is rendered
        close_progress()

    def _goto_line(self, line_num):
        """Navigate to View tab and scroll to the specified line number."""
        # Switch to View tab
        self.tabview.set("View")

        # Select the validated file in View tab
        if self.validated_file and self.validated_file in self.view_file_map:
            self.cbo_view_files.set(self.validated_file)
            self.on_view_file_select(self.validated_file)

        # Find and set the marker index for this line
        lines = self._get_sorted_marker_lines()
        if line_num in lines:
            self.current_marker_index = lines.index(line_num)
            self._update_marker_position_label()
            # Schedule to update current marker indicator after scroll
            self.after(150, lambda: self._highlight_current_marker(line_num))

        # Schedule scroll after a brief delay to allow content to load
        self.after(100, lambda: self._scroll_to_line(line_num))

    def _scroll_to_line(self, line_num):
        """Scroll the YAML viewer to center on the specified line."""
        try:
            # Target line index
            target_index = f"{line_num}.0"

            # First make sure the line is visible
            self.txt_yaml.see(target_index)
            self.txt_yaml.update_idletasks()

            # Get visible area info
            # yview returns (first_visible_fraction, last_visible_fraction)
            first, last = self.txt_yaml.yview()
            visible_fraction = last - first

            # Get total lines
            total_lines = int(self.txt_yaml.index("end-1c").split(".")[0])

            if total_lines > 0:
                # Calculate target position as fraction
                target_fraction = (line_num - 1) / total_lines

                # Center it by offsetting by half the visible area
                centered_pos = target_fraction - (visible_fraction / 2)

                # Clamp to valid range
                centered_pos = max(0, min(1 - visible_fraction, centered_pos))

                self.txt_yaml.yview_moveto(centered_pos)

        except Exception as e:
            self.val_log_print(f"Error scrolling to line: {e}")

    def _get_sorted_marker_lines(self):
        """Get sorted list of line numbers with validation issues."""
        if not self.validation_issues:
            return []
        return sorted(self.validation_issues.keys())

    def _update_marker_position_label(self):
        """Update the marker position counter label and show/hide nav bar."""
        lines = self._get_sorted_marker_lines()
        total = len(lines)

        if total == 0:
            # No markers - hide navigation bar
            self.nav_frame.pack_forget()
            # Clear marker indicator
            self._clear_marker_indicator()
        else:
            # Has markers - show navigation bar
            self.nav_frame.pack(side="right", padx=(0, 20))

            first_selection = False
            if self.current_marker_index < 0:
                self.current_marker_index = 0
                first_selection = True
            current = self.current_marker_index + 1
            self.btn_marker_pos.configure(text=f"{current}/{total}")

            # Highlight first marker if just selected
            if first_selection:
                self._highlight_current_marker(lines[0])

    def _goto_current_marker(self):
        """Scroll to the current marker position (clicked from counter button)."""
        lines = self._get_sorted_marker_lines()
        if not lines or self.current_marker_index < 0:
            return
        if self.current_marker_index < len(lines):
            self._scroll_to_line(lines[self.current_marker_index])

    def _goto_first_marker(self):
        """Navigate to the first marker."""
        lines = self._get_sorted_marker_lines()
        if not lines:
            return
        self.current_marker_index = 0
        self._scroll_to_line(lines[0])
        self._update_marker_position_label()
        self._highlight_current_marker(lines[0])

    def _goto_prev_marker(self):
        """Navigate to the previous marker."""
        lines = self._get_sorted_marker_lines()
        if not lines:
            return
        if self.current_marker_index > 0:
            self.current_marker_index -= 1
        else:
            self.current_marker_index = len(lines) - 1  # Wrap to last
        self._scroll_to_line(lines[self.current_marker_index])
        self._update_marker_position_label()
        self._highlight_current_marker(lines[self.current_marker_index])

    def _goto_next_marker(self):
        """Navigate to the next marker."""
        lines = self._get_sorted_marker_lines()
        if not lines:
            return
        if self.current_marker_index < len(lines) - 1:
            self.current_marker_index += 1
        else:
            self.current_marker_index = 0  # Wrap to first
        self._scroll_to_line(lines[self.current_marker_index])
        self._update_marker_position_label()
        self._highlight_current_marker(lines[self.current_marker_index])

    def _goto_last_marker(self):
        """Navigate to the last marker."""
        lines = self._get_sorted_marker_lines()
        if not lines:
            return
        self.current_marker_index = len(lines) - 1
        self._scroll_to_line(lines[-1])
        self._update_marker_position_label()
        self._highlight_current_marker(lines[-1])

    def _highlight_current_marker(self, line_num):
        """Store the current marker line number (no visual highlight)."""
        self._current_marker_line = line_num

    def _clear_marker_indicator(self):
        """Clear the current marker indicator."""
        self._current_marker_line = None

    def refresh_view_files(self):
        # Use OAS folder from View tab entry
        oas_dir = self.entry_view_oas_folder.get()
        candidates = []
        if os.path.exists(oas_dir):
            for f in os.listdir(oas_dir):
                if f.endswith(".yaml") or f.endswith(".json"):
                    candidates.append(os.path.join(oas_dir, f))

        # Sort based on preference (same as Validation tab)
        sort_order = self.prefs_manager.get("file_sort_order", "alphabetical")
        if sort_order == "newest_first":
            sorted_candidates = sorted(
                candidates, key=lambda f: os.path.getmtime(f), reverse=True
            )
        elif sort_order == "oldest_first":
            sorted_candidates = sorted(candidates, key=lambda f: os.path.getmtime(f))
        else:  # alphabetical
            sorted_candidates = sorted(candidates)

        self.view_file_map = {}
        display_names = []
        for path in sorted_candidates:
            name = os.path.basename(path)
            self.view_file_map[name] = path
            display_names.append(name)

        if display_names:
            self.cbo_view_files.configure(values=display_names)
            self.cbo_view_files.set(display_names[0])
            self.on_view_file_select(display_names[0])
        else:
            self.cbo_view_files.configure(values=["No OAS files found"])
            self.cbo_view_files.set("No OAS files found")

    def on_view_file_select(self, value):
        # Sync with Validation tab combo
        if value in self.file_map:
            self.cbo_files.set(value)
            # Lazy Sync: Don't force validation here. 
            # It will run when the user switches to the Validation tab.

        filepath = self.view_file_map.get(value)
        if not filepath or not os.path.exists(filepath):
            return

        # Load YAML into viewer
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # CodeView uses standard tk.Text API
            self.txt_yaml.config(state="normal")
            self.txt_yaml.delete("1.0", "end")
            self.txt_yaml.insert("1.0", content)

            # Apply validation markers if this is the validated file
            self._apply_validation_markers(os.path.basename(filepath))

            # READ-ONLY MODE WITH CURSOR
            # To show cursor, state must be normal. We block edits via binding.
            self.txt_yaml.config(state="normal")
            
            # Fixed Selection logic: bind read-only handler
            self.txt_yaml.bind("<Key>", self._on_yaml_key_press)

            # Bind Double Click to fix cursor position
            self.txt_yaml.bind("<Double-Button-1>", self._on_yaml_double_click)
            
            # Robus Search Binding: EXCLUSIVE OVERRIDE (No add="+") to ensure priority over internal bindings
            # Binding all variants to be safe against CapsLock/Shift states
            self.txt_yaml.bind("<Control-f>", lambda e: self._handle_global_search(e) or "break")
            self.txt_yaml.bind("<Control-F>", lambda e: self._handle_global_search(e) or "break")
            self.txt_yaml.bind("<Control-Key-f>", lambda e: self._handle_global_search(e) or "break")
            self.txt_yaml.bind("<Control-Key-F>", lambda e: self._handle_global_search(e) or "break")





            
            # We specifically want to allow Copy (Ctrl+C) and Select All (Ctrl+A) and Navigation
            # This is handled in _on_yaml_key_press

            # Store the current content for browser opening
            self._current_yaml_content = content
            self._current_file_name = os.path.basename(filepath)

        except Exception as e:
            self.val_log_print(f"Error loading view: {e}")

        # Update sync button visibility based on new file
        self._update_sync_button_visibility()

    def open_in_browser(self):
        """Generate Redoc HTML and open it in the system's default browser."""
        import webbrowser

        if not hasattr(self, "_current_yaml_content") or not self._current_yaml_content:
            return

        try:
            # Generate HTML
            html_content = self.redoc_gen.get_html_content(self._current_yaml_content)

            # Save to file in the generated folder
            base_dir = self.entry_dir.get()
            gen_dir = os.path.join(base_dir, "generated")
            if not os.path.exists(gen_dir):
                os.makedirs(gen_dir)

            # Create a nice filename
            html_filename = self._current_file_name.replace(
                ".yaml", "_redoc.html"
            ).replace(".json", "_redoc.html")
            html_path = os.path.join(gen_dir, html_filename)

            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            # Open in browser
            webbrowser.open(f"file:///{html_path.replace(os.sep, '/')}")

            self.val_log_print(f"Opened documentation in browser: {html_path}")

        except Exception as e:
            self.val_log_print(f"Error opening browser: {e}")

    def open_documentation_viewer(self):
        """Open documentation in a docked viewer window."""
        if not hasattr(self, "_current_yaml_content") or not self._current_yaml_content:
            return

        try:
            # Generate HTML content
            html_content = self.redoc_gen.get_html_content(self._current_yaml_content)

            # Save to file (pywebview needs a file path)
            base_dir = self.entry_dir.get()
            gen_dir = os.path.join(base_dir, "generated")
            if not os.path.exists(gen_dir):
                os.makedirs(gen_dir)

            # Correct filename: same as YAML but with .html
            base_name = os.path.splitext(self._current_file_name)[0]
            html_filename = f"{base_name}.html"
            html_path = os.path.join(gen_dir, html_filename)

            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            # Store path for potential reuse
            self._current_html_path = html_path

            title = f"API Documentation - {self._current_file_name}"

            # Initialise list if missing (for safety)
            if not hasattr(self, "_doc_viewers"):
                self._doc_viewers = []

            # Clean up closed viewers (those with _closed flag set)
            self._doc_viewers = [v for v in self._doc_viewers if v and not v._closed]

            # Update button visibility based on remaining viewers
            self._update_sync_button_visibility()

            # Check if viewer for this file is already open
            for viewer in self._doc_viewers:
                if (
                    hasattr(viewer, "file_name")
                    and viewer.file_name == self._current_file_name
                ):
                    # Try to focus - if it fails, the window is closed
                    if viewer.focus():
                        self.val_log_print(
                            f"Bringing existing documentation to front: {self._current_file_name}"
                        )
                        return
                    else:
                        # Window was closed, mark it and continue to create a new one
                        self.val_log_print(
                            f"Viewer for {self._current_file_name} was closed, creating new one"
                        )
                        viewer._closed = True
                        # Remove from list
                        self._doc_viewers = [
                            v for v in self._doc_viewers if v != viewer
                        ]
                        break

            # Determine snap state (exclusive)
            snap_default = self.prefs_manager.get("doc_snap_default_enabled", True)

            # If starting snapped, unsnap all others
            if snap_default:
                for viewer in self._doc_viewers:
                    if (
                        viewer.process
                        and viewer.process.is_alive()
                        and not viewer._closed
                    ):
                        # Force unsnap blindly to avoid race conditions or sync lags
                        viewer.set_snap(False)
                
                # Restore from maximized state before docking
                # Maximized windows can't be resized, so we need to un-maximize first
                if self.state() == "zoomed":
                    self.state("normal")
                    self.update_idletasks()  # Process pending geometry changes
                
                # Bring main window to front when starting snapped
                self.lift()
                self.focus_force()

            # Create new docked viewer
            new_viewer = DockedDocViewer(
                self,
                html_path,
                title,
                snap_default=snap_default,
                file_name=self._current_file_name,
                on_snap_callback=self._on_doc_snap_enabled,
                on_focus_callback=self._on_doc_focus,
                on_sync_editor_callback=self._on_doc_sync_editor,
            )
            self._doc_viewers.append(new_viewer)
            self.val_log_print(f"Opened documentation: {self._current_file_name}")

            # Show "Locate in Docs" button now that a viewer is open
            self.btn_sync_viewer.pack(side="left", padx=10)

            # If dock is enabled by default, position windows side-by-side
            if snap_default:
                self._position_windows_side_by_side(new_viewer)

        except Exception as e:
            self.val_log_print(f"Error opening viewer: {e}")

    def _update_sync_button_visibility(self):
        """Show or hide the 'Show in Docs' button based on active viewers for current file."""
        if not hasattr(self, "_doc_viewers"):
            self._doc_viewers = []

        # Clean up closed viewers using is_closed property (checks process status)
        self._doc_viewers = [v for v in self._doc_viewers if v and not v.is_closed]

        # Get current file in editor
        current_file = (
            self.cbo_view_files.get() if hasattr(self, "cbo_view_files") else ""
        )

        # Check if there's a viewer for the current file
        has_viewer_for_current_file = any(
            hasattr(v, "file_name") and v.file_name == current_file
            for v in self._doc_viewers
        )

        # Show button only if there's a viewer for this specific file
        if has_viewer_for_current_file:
            if not self.btn_sync_viewer.winfo_ismapped():
                self.btn_sync_viewer.pack(side="left", padx=10)
        else:
            self.btn_sync_viewer.pack_forget()

    def _apply_validation_markers(self, filename):
        """Apply visual markers to lines with validation issues."""
        # Remove previous tags
        self.txt_yaml.tag_remove("error_line", "1.0", "end")
        self.txt_yaml.tag_remove("warning_line", "1.0", "end")
        self.txt_yaml.tag_remove("info_line", "1.0", "end")

        # Configure tags for highlighting with theme-aware colors
        current_theme = (
            self.cbo_yaml_theme.get() if hasattr(self, "cbo_yaml_theme") else "oas-dark"
        )
        is_dark_theme = "dark" in current_theme.lower()

        if is_dark_theme:
            # Saturated colors for dark backgrounds
            self.txt_yaml.tag_configure("error_line", background="#8B0000")  # DarkRed
            self.txt_yaml.tag_configure(
                "warning_line", background="#B8860B"
            )  # DarkGoldenrod
            self.txt_yaml.tag_configure("info_line", background="#00008B")  # DarkBlue
        else:
            # Slightly darker pastel colors for light backgrounds (visible but not harsh)
            self.txt_yaml.tag_configure(
                "error_line", background="#FFCCCC"
            )  # Salmon pink
            self.txt_yaml.tag_configure(
                "warning_line", background="#FFE6A0"
            )  # Light gold
            self.txt_yaml.tag_configure("info_line", background="#CCE0FF")  # Soft blue

        # SILENCED ALL MARKER LOGS PER USER REQUEST
        # (Marker Check, Fail/No Issues, Mismatch)
        # Prevents log pollution on startup


        # Apply tags to lines with issues
        for line_num, issues in self.validation_issues.items():
            # Determine highest severity for this line
            severities = [issue["severity"] for issue in issues]
            if "error" in severities:
                tag = "error_line"
            elif "warning" in severities:
                tag = "warning_line"
            else:
                tag = "info_line"

            # Apply tag to entire line (including beyond last character)
            start = f"{line_num}.0"
            end = f"{line_num}.end+1c"  # +1c includes the newline, making full line colored
            try:
                self.txt_yaml.tag_add(tag, start, end)
            except:
                pass  # Line might not exist

        # Raise tag priority to be above syntax highlighting
        self.txt_yaml.tag_raise("error_line")
        self.txt_yaml.tag_raise("warning_line")
        self.txt_yaml.tag_raise("info_line")

        # self.val_log_print(f"Markers applied to {len(self.validation_issues)} lines")


        # Reset marker navigation and update counter
        self.current_marker_index = -1
        self._update_marker_position_label()

        # Bind tooltip events
        self.txt_yaml.bind("<Motion>", self._on_yaml_hover)
        self.txt_yaml.bind("<Leave>", self._hide_tooltip)

        # Initialize tooltip variables
        if not hasattr(self, "_tooltip_window"):
            self._tooltip_window = None
            self._tooltip_line = None

    def _on_yaml_hover(self, event):
        """Show tooltip when hovering over a line with validation issues."""
        # Get line number at cursor position
        index = self.txt_yaml.index(f"@{event.x},{event.y}")
        line_num = int(index.split(".")[0])

        # Check if this line has issues
        if line_num in self.validation_issues and self._tooltip_line != line_num:
            self._show_tooltip(event, line_num)
        elif line_num not in self.validation_issues:
            self._hide_tooltip(event)

    def _show_tooltip(self, event, line_num):
        """Show tooltip with validation messages for the given line."""
        self._hide_tooltip(event)
        self._tooltip_line = line_num

        issues = self.validation_issues.get(line_num, [])
        if not issues:
            return

        # Build tooltip text
        tooltip_text = ""
        for issue in issues:
            sev = issue["severity"].upper()
            code = issue["code"]
            msg = issue["message"]
            tooltip_text += f"[{sev}] {code}\n{msg}\n\n"
        tooltip_text = tooltip_text.strip()

        # Create tooltip window
        self._tooltip_window = tk.Toplevel(self)
        self._tooltip_window.wm_overrideredirect(True)

        # Position tooltip close to cursor, using text widget coordinates
        # Get the text widget's screen position
        text_x = self.txt_yaml.winfo_rootx()
        text_y = self.txt_yaml.winfo_rooty()
        x = text_x + event.x + 15
        y = text_y + event.y + 20  # Below cursor line
        self._tooltip_window.wm_geometry(f"+{x}+{y}")

        # Determine tooltip colors based on current YAML theme
        # Light themes get DARK tooltip, Dark themes get LIGHT tooltip (inverted for contrast)
        current_theme = (
            self.cbo_yaml_theme.get() if hasattr(self, "cbo_yaml_theme") else "oas-dark"
        )
        is_dark_theme = "dark" in current_theme.lower()

        if is_dark_theme:
            # Light tooltip for dark theme (light bg, dark text)
            bg_color = "#F5F5F5"
            fg_color = "#1A1A1A"
        else:
            # DARK tooltip for light theme (dark bg, light text)
            bg_color = "#1A1A1A"
            fg_color = "#F5F5F5"

        # Style the tooltip
        label = tk.Label(
            self._tooltip_window,
            text=tooltip_text,
            justify="left",
            background=bg_color,
            foreground=fg_color,
            relief="solid",
            borderwidth=1,
            font=("Consolas", 10),
            padx=8,
            pady=5,
        )
        label.pack()

    def _hide_tooltip(self, event=None):
        """Hide the tooltip window."""
        if hasattr(self, "_tooltip_window") and self._tooltip_window:
            self._tooltip_window.destroy()
            self._tooltip_window = None
            self._tooltip_line = None

    def _on_doc_snap_enabled(self, active_viewer):
        """Callback when a doc viewer enables snap - disable snap on others (exclusive snap)."""
        # Bring main window to front when snapping
        self.lift()
        self.focus_force()
        # Also trigger context sync
        self._on_doc_focus(active_viewer)

        # Position windows side-by-side on the same screen
        self._position_windows_side_by_side(active_viewer)

        # Iterate through all viewers
        if hasattr(self, "_doc_viewers"):
            for viewer in self._doc_viewers:
                # Skip the one that just enabled snap
                if viewer == active_viewer:
                    continue
                # If another viewer is snapped, unsnap it
                # We check process liveness too just in case
                if viewer.process and viewer.process.is_alive() and not viewer._closed:
                    if viewer.is_snapped:
                        viewer.set_snap(False)

    def _position_windows_side_by_side(self, viewer):
        """Position main window and viewer side-by-side (snap-like behavior).
        Uses non-blocking scheduling to avoid freezing the UI."""

        def do_positioning():
            """Actual positioning logic, called after delay."""
            try:
                import pygetwindow as gw
                import ctypes

                # Get the work area (screen excluding taskbar) using Windows API
                # SPI_GETWORKAREA = 0x0030
                work_area = ctypes.wintypes.RECT()
                ctypes.windll.user32.SystemParametersInfoW(
                    0x0030, 0, ctypes.byref(work_area), 0
                )

                # Work area dimensions
                work_left = work_area.left
                work_top = work_area.top
                work_width = work_area.right - work_area.left
                work_height = work_area.bottom - work_area.top

                # Windows 11 has invisible borders (7px) plus rounded corners (~10px)
                # We compensate to position windows correctly and show rounded corners above taskbar
                BORDER = 7
                BOTTOM_MARGIN = 30  # Extra space to show UI elements above taskbar

                # Calculate half-width for each window
                half_width = work_width // 2

                # Position main window on left half of work area
                self.geometry(
                    f"{half_width + BORDER}x{work_height - BOTTOM_MARGIN}+{work_left - BORDER}+{work_top}"
                )
                self.update_idletasks()

                # Find and position doc viewer window by its actual title
                if hasattr(viewer, "_window_title") and viewer._window_title:
                    doc_windows = gw.getWindowsWithTitle(viewer._window_title)
                    if doc_windows:
                        doc_win = doc_windows[0]
                        doc_win.moveTo(work_left + half_width - BORDER, work_top)
                        doc_win.resizeTo(
                            half_width + BORDER, work_height - BOTTOM_MARGIN
                        )

            except Exception:
                # If positioning fails, just continue without it
                pass

        # Schedule positioning after 1 second (non-blocking)
        self.after(1000, do_positioning)

    def _on_doc_focus(self, viewer):
        """Callback when a doc viewer window gets focus while bound."""
        if not viewer.is_snapped:
            return

        # 1. Bring main window to front robustly
        try:
            import pygetwindow as gw

            # Find windows that match the app title
            app_windows = gw.getWindowsWithTitle(self.title())
            if app_windows:
                # Use the first match
                win = app_windows[0]
                if win.isMinimized:
                    win.restore()
                win.activate()
        except Exception:
            # Fallback to standard tkinter lift
            self.attributes("-topmost", True)
            self.after(10, lambda: self.attributes("-topmost", False))
            self.lift()

        # Ensure focus on the application
        self.focus_force()
        # 2. Sync Tab: Switch to View tab
        if self.tabview.get() != "View":
            self.tabview.set("View")

        # 3. Sync File: Select the viewer's file
        if hasattr(viewer, "file_name") and viewer.file_name:
            if self.cbo_view_files.get() != viewer.file_name:
                self.val_log_print(f"Binding context to: {viewer.file_name}")
                self.cbo_view_files.set(viewer.file_name)
                self.on_view_file_select(viewer.file_name)

    def sync_viewer(self):
        """Sync Redoc viewer to current YAML cursor position."""
        # Clean up closed viewers and update button visibility
        self._update_sync_button_visibility()

        # Find active viewer for the current file
        current_file = self.cbo_view_files.get()
        active_viewer = None
        if hasattr(self, "_doc_viewers"):
            for v in self._doc_viewers:
                if (
                    not v._closed
                    and hasattr(v, "file_name")
                    and v.file_name == current_file
                ):
                    active_viewer = v
                    break

        if not active_viewer:
            self.val_log_print(
                "No active documentation viewer for this file. Open documentation first."
            )
            return

        # Find first operationId visible in the editor viewport
        try:
            import re

            # Get the visible range in the text widget
            # @0,0 is the top-left corner of the visible area
            first_visible = self.txt_yaml.index("@0,0")
            first_line = int(first_visible.split(".")[0])

            # Get all content
            content_lines = self.txt_yaml.get("1.0", "end").splitlines()
            target_path = ""

            # Search from the first visible line downwards for the first operationId
            for i in range(first_line - 1, len(content_lines)):
                line = content_lines[i]

                # Regex for operationId (handles optional quotes and spacing)
                op_id_match = re.search(r"operationId:\s+['\"]?([\w\.-]+)['\"]?", line)
                if op_id_match:
                    op_id = op_id_match.group(1)
                    target_path = f"#/operations/{op_id}"
                    self.val_log_print(
                        f"Found visible operationId '{op_id}' at line {i+1}"
                    )
                    break

            if target_path:
                self.val_log_print(f"📲 Syncing viewer to: {target_path}")
                # Execute in viewer process
                active_viewer.evaluate_js(f"window.scrollToPath('{target_path}')")
            else:
                self.val_log_print("⚠️ No operationId found in visible area.")
        except Exception as e:
            self.val_log_print(f"Error during viewer sync: {e}")

    def _on_doc_sync_editor(self, viewer, info):
        """Callback from Doc Viewer to sync YAML editor to its current section with highlighting."""
        # Ensure we are on the right file and tab
        self._on_doc_focus(viewer)

        # Extract info from JavaScript
        operation_id = info.get("operationId", "")
        hash_val = info.get("hash", "")
        section_title = info.get("sectionTitle", "")
        debug_info = info.get("debug", "")

        # Log debug info from JavaScript for troubleshooting
        if debug_info:
            self.val_log_print(f"🔍 JS Detection: {debug_info}")

        search_terms = []

        # 1. Prioritize operationId (most reliable if present)
        if operation_id:
            search_terms.append(f"operationId: {operation_id}")
            search_terms.append(f"operationId: '{operation_id}'")
            search_terms.append(f'operationId: "{operation_id}"')

        # 2. Try to extract from hash
        if hash_val and not search_terms:
            clean_hash = hash_val.lstrip("#/")
            if "operations/" in clean_hash:
                op_id = clean_hash.split("operations/")[1]
                search_terms.append(f"operationId: {op_id}")
            elif "paths/" in clean_hash:
                path_raw = clean_hash.split("paths/")[1]
                path = path_raw.replace("~1", "/")
                search_terms.append(f"  {path}:")  # 2-space indent for path entries

        # 3. Fallback to section title
        if section_title and not search_terms:
            search_terms.append(f"summary: {section_title}")

        if not search_terms:
            self.val_log_print(
                "⚠️ Sync: No valid operationId or path detected from viewer."
            )
            return

        # Search in YAML
        content = self.txt_yaml.get("1.0", "end")
        lines = content.splitlines()

        found_line = -1
        matched_term = ""
        for term in search_terms:
            if not term:
                continue
            for i, line in enumerate(lines):
                if term in line:
                    found_line = i + 1
                    matched_term = term
                    break
            if found_line != -1:
                break

        if found_line != -1:
            self.val_log_print(
                f"⬆️ Syncing editor to line {found_line} (matched: '{matched_term}')"
            )
            # Defer highlight slightly to ensure window focus and tab switch are complete
            self.after(50, lambda: self._scroll_to_line_and_highlight(found_line))
        else:
            self.val_log_print(f"⚠️ Sync: Could not find '{search_terms[0]}' in YAML.")

    def _scroll_to_line_and_highlight(self, line_no):
        """Scroll to a line, center it, and apply a temporary highlight 'flash' effect."""
        try:
            # 1. Center the line in the view instead of just 'see'
            # Calculate view fraction (approximate)
            total_lines = int(self.txt_yaml.index("end-1c").split(".")[0])
            if total_lines > 0:
                fraction = max(0, (line_no - 15) / total_lines)
                self.txt_yaml.yview_moveto(fraction)

            # Ensure it is visible regardless
            self.txt_yaml.see(f"{line_no}.0")
            self.txt_yaml.mark_set(tk.INSERT, f"{line_no}.0")

            # 2. Apply highlight
            tag_name = "sync_highlight"
            self.txt_yaml.tag_remove(tag_name, "1.0", "end")
            self.txt_yaml.tag_add(tag_name, f"{line_no}.0", f"{line_no}.end")

            # High-contrast Gold
            self.txt_yaml.tag_config(
                tag_name, background="#FFD700", foreground="#000000"
            )

            # 3. Fade out highlight after 2 seconds
            self.after(2000, lambda: self.txt_yaml.tag_remove(tag_name, "1.0", "end"))
        except Exception as e:
            self.val_log_print(f"Highlight error: {e}")

    def _show_search_dialog(self, event=None):
        """Show or focus the finding dialog."""
        # Capture selection BEFORE acting on windows (focus change clears selection)
        initial_search_text = None
        try:
             if self.txt_yaml.tag_ranges("sel"):
                 initial_search_text = self.txt_yaml.get("sel.first", "sel.last")
        except:
             pass

        # Create Search Window if not exists
        if hasattr(self, "search_window") and self.search_window and self.search_window.winfo_exists():
            self.search_window.attributes("-topmost", True)
            self.search_window.lift()
            self.search_window.focus_force()

            
            # Dynamic Autofill for existing window
            if initial_search_text:
                 self.search_entry.delete(0, "end")
                 self.search_entry.insert(0, initial_search_text)
                 self.search_entry.select_range(0, "end")
                 # Update count relative to current cursor (after short delay for UI)
                 self.after(50, lambda: self._update_match_count(current_match_start=self.txt_yaml.index("insert")))
            
            self.search_entry.focus_set()
            return

        try:
            self.search_window = ctk.CTkToplevel(self)
            self.search_window.title("Find")
            self.search_window.geometry("450x60")
            self.search_window.resizable(False, False)
            self.search_window.attributes("-topmost", True) 

            
            # FIX: Clear highlights when search window is closed
            def on_search_close():
                try:
                    self.txt_yaml.tag_remove("found", "1.0", "end")
                except:
                    pass
                self.search_window.destroy()
                self.search_window = None

            self.search_window.protocol("WM_DELETE_WINDOW", on_search_close)

            
            # Icon
            try:
                icon_file = resource_path("icon.ico")
                if os.path.exists(icon_file):
                    self.search_window.after(200, lambda: self.search_window.iconbitmap(icon_file))
            except:
                pass

            # Position logic
            try:
                print("DEBUG: Calculating geometry")
                parent_x = self.winfo_x()
                parent_y = self.winfo_y()
                parent_w = self.winfo_width()
                x = parent_x + (parent_w // 2) - 225
                y = parent_y + 100 
                self.search_window.geometry(f"+{x}+{y}")
            except Exception as e:
                print(f"DEBUG: Geometry error: {e}")

            # UI Container
            frame = ctk.CTkFrame(self.search_window, fg_color="transparent")
            frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Grid Layout: [Entry][Hist] [Count] [Prev] [Next]
            frame.grid_columnconfigure(0, weight=1)
            
            # 1. Search Entry (Standard Entry for stability)
            self.search_entry = ctk.CTkEntry(
                frame, 
                placeholder_text="Find...", 
                height=28
            )
            self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 2))
            
            # History Button (Dropdown style)
            self.btn_history = ctk.CTkButton(
                frame,
                text="▼",
                width=24,
                height=28,
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                command=self._show_history_menu
            )
            self.btn_history.grid(row=0, column=1, padx=(0, 5))

            # Bindings
            self.search_entry.bind("<Return>", lambda e: self._find_next())
            self.search_entry.bind("<Shift-Return>", lambda e: self._find_prev())
            self.search_entry.bind("<KeyRelease>", self._on_search_key_release)
            
            # 2. Count Label
            self.lbl_search_count = ctk.CTkLabel(frame, text="0/0", width=60, text_color="gray60")
            self.lbl_search_count.grid(row=0, column=2, padx=(0, 5))

            # 3. Buttons (Icon style)
            btn_prev = ctk.CTkButton(
                frame, 
                text="▲", 
                width=30, 
                height=28,
                command=self._find_prev
            )
            btn_prev.grid(row=0, column=3, padx=(0, 2))

            btn_next = ctk.CTkButton(
                frame, 
                text="▼", 
                width=30, 
                height=28,
                command=self._find_next
            )
            btn_next.grid(row=0, column=4)
            
            # Pre-fill (Initial)
            if initial_search_text:
                 self.search_entry.insert(0, initial_search_text) 
                 self.search_entry.select_range(0, "end")
                 # Trigger initial count safely with DEBOUNCE and CURSOR POS
                 # Using "insert" gives us the cursor location to find the "current" match index
                 self.after(500, lambda: self._update_match_count(current_match_start=self.txt_yaml.index("insert")))

            # Safe focus
            def safe_focus():
                try:
                    if hasattr(self.search_entry, "_entry"):
                        self.search_entry._entry.focus_set()
                    else:
                        self.search_entry.focus_set()
                except:
                    pass
            
            self.after(100, safe_focus)
            
        except Exception as e:
            self.val_log_print(f"Error creating search dialog: {e}")
            if hasattr(self, "search_window") and self.search_window:
                self.search_window.destroy()
                self.search_window = None

    def _on_yaml_double_click(self, event):
        """Trim punctuation from double-click selection without interfering with Tkinter's selection mechanics."""
        def trim_punctuation():
            try:
                # Check if there's a selection from the double-click
                if not self.txt_yaml.tag_ranges("sel"):
                    return
                
                start = self.txt_yaml.index("sel.first")
                end = self.txt_yaml.index("sel.last")
                text = self.txt_yaml.get(start, end)
                
                # Trim trailing punctuation
                original_end = end
                while text and text[-1] in ":\",'.]":
                    text = text[:-1]
                    end = self.txt_yaml.index(f"{end}-1c")
                
                # Re-apply the selection if we trimmed something
                if end != original_end:
                    self.txt_yaml.tag_remove("sel", "1.0", "end")
                    self.txt_yaml.tag_add("sel", start, end)
                
                # ALWAYS set cursor to END so Shift+Left contracts from right
                self.txt_yaml.mark_set("insert", end)
            except:
                pass
        
        # Schedule this to run after Tkinter's default double-click has completed
        # Don't return "break" - let Tkinter handle the double-click normally
        self.after(1, trim_punctuation)

    def _on_shift_left(self, event):
        """Handle Shift+Left: contract from right, or expand left when cursor at start."""
        try:
            if not self.txt_yaml.tag_ranges("sel"):
                return  # No selection, let default behavior handle it
            
            start = self.txt_yaml.index("sel.first")
            end = self.txt_yaml.index("sel.last")
            insert = self.txt_yaml.index("insert")
            
            # If cursor is at start of selection, expand to the left
            if self.txt_yaml.compare(insert, "==", start):
                new_start = self.txt_yaml.index(f"{start}-1c")
                self.txt_yaml.tag_remove("sel", "1.0", "end")
                self.txt_yaml.tag_add("sel", new_start, end)
                self.txt_yaml.mark_set("insert", new_start)
            # Otherwise shrink from the right
            elif self.txt_yaml.compare(end, ">", start):
                new_end = self.txt_yaml.index(f"{end}-1c")
                self.txt_yaml.tag_remove("sel", "1.0", "end")
                self.txt_yaml.tag_add("sel", start, new_end)
                self.txt_yaml.mark_set("insert", new_end)
            
            return "break"
            
        except:
            pass
    
    def _on_shift_right(self, event):
        """Handle Shift+Right: contract from left, or expand right when cursor at end."""
        try:
            if not self.txt_yaml.tag_ranges("sel"):
                return  # No selection, let default behavior handle it
            
            start = self.txt_yaml.index("sel.first")
            end = self.txt_yaml.index("sel.last")
            insert = self.txt_yaml.index("insert")
            
            # If cursor is at start of selection, contract from the left
            if self.txt_yaml.compare(insert, "==", start):
                if self.txt_yaml.compare(start, "<", end):  # Don't contract past end
                    new_start = self.txt_yaml.index(f"{start}+1c")
                    self.txt_yaml.tag_remove("sel", "1.0", "end")
                    self.txt_yaml.tag_add("sel", new_start, end)
                    self.txt_yaml.mark_set("insert", new_start)
            # Otherwise expand to the right
            else:
                new_end = self.txt_yaml.index(f"{end}+1c")
                self.txt_yaml.tag_remove("sel", "1.0", "end")
                self.txt_yaml.tag_add("sel", start, new_end)
                self.txt_yaml.mark_set("insert", new_end)
            
            return "break"
            
        except:
            pass

    def _on_search_key_release(self, event):
        """Update match count on typing."""
        # Debounce slightly could be good, but simple is fine for now
        self._update_match_count()

    def _update_match_count(self, current_match_start=None):
        """Count all occurrences and identify current index."""
        if current_match_start is None:
            try:
                current_match_start = self.txt_yaml.index("insert")
            except:
                pass
                
        if not hasattr(self, "lbl_search_count") or not self.lbl_search_count.winfo_exists():
            return
            
        query = self.search_entry.get()
        if not query:
            self.lbl_search_count.configure(text="0/0")
            return
            
        # Count matches
        try:
            matches = []
            start = "1.0"
            max_count = 100 # Safety limit to prevent freezing on large files/many matches
            
            while True:
                pos = self.txt_yaml.search(query, start, stopindex="end", nocase=True)
                if not pos:
                    break
                matches.append(pos)
                start = f"{pos}+1c"
                
                if len(matches) >= max_count:
                    break
            
            total = len(matches)
            current = 0
            
            if current_match_start:
                 # Find which match corresponds to current_match_start
                 # Robust logic: The "current" match is the LAST match that starts BEFORE (or at) the cursor.
                 # This handles cases where user deletes char from search query:
                 # Query: "Foo" -> Cursor at end of "Foo".
                 # User deletes "o" -> Query: "Fo". Match ends before cursor.
                 # But we still want this to be the "current" match.
                 
                 found_current = False
                 for i, pos in enumerate(matches):
                     # If start of match is > cursor, then we passed our candidate
                     if self.txt_yaml.compare(pos, ">", current_match_start):
                         break
                     
                     # Otherwise, this match is a candidate (starts before or at cursor)
                     # We keep updating 'current' until we find one that is strictly after
                     current = i + 1
                     found_current = True
                     
                     # Optimization: If we find a match that explicitly *contains* the cursor, that's definitely it.
                     # But the "last start <= cursor" logic covers containment too, provided matches are ordered.
                     # The only edge case is if cursor is way past the match (e.g. standard editing).
                     # In that case, showing the "previous" match as current is still acceptable/helpful.
                     
                 # If we didn't find any match starting before cursor (cursor is at top of doc, matches are below)
                 # Then current remains 0 (correct, we are before first match)
            
            if total == 0:
                self.lbl_search_count.configure(text="0/0")
            elif total >= max_count:
                # Indicate limit reached
                prefix = f"{current}/" if current > 0 else "?/"
                self.lbl_search_count.configure(text=f"{prefix}{max_count}+")
            else:
                prefix = f"{current}/" if current > 0 else "?/"
                self.lbl_search_count.configure(text=f"{prefix}{total}")

        except Exception as e:
            print(f"Count error: {e}")
            self.lbl_search_count.configure(text="Err")
            
    def _show_history_menu(self):
        """Show search history in a native menu."""
        try:
            history = self.prefs_manager.get("search_history", [])
            if not history:
                return
                
            menu = tk.Menu(self, tearoff=0)
            
            def load_search(text):
                self.search_entry.delete(0, "end")
                self.search_entry.insert(0, text)
                self._find_next()
                
            for item in history:
                if item:
                    menu.add_command(label=str(item), command=lambda t=item: load_search(t))
            
            # Post menu under button
            try:
                x = self.btn_history.winfo_rootx()
                y = self.btn_history.winfo_rooty() + self.btn_history.winfo_height()
                menu.post(x, y)
            except:
                menu.post(self.winfo_pointerx(), self.winfo_pointery())
                
                
        except Exception as e:
            print(f"History menu error: {e}")

    def _add_to_search_history(self, query):
        """Add query to history if new."""
        if not query: 
            return
            
        history = self.prefs_manager.get("search_history", [])
        # Ensure list
        if not isinstance(history, list):
             history = []
             
        if query in history:
            history.remove(query) # Move to top
        history.insert(0, query)
        
        # Limit to 20
        history = history[:20]
        self.prefs_manager.set("search_history", history)
        self.prefs_manager.save()
        
        # Update combo
        self.search_entry.configure(values=history)

    def _safe_search_trigger(self, event=None):
        """Directly trigger search from binding, ensuring 'break'."""
        try:
            self._show_search_dialog(event)
            return "break" 
        except Exception as e:
            if hasattr(self, "val_log_print"):
                 self.val_log_print(f"Search Prompt Error: {e}")
            else:
                 print(f"Search Prompt Error: {e}")

    def _handle_global_search(self, event=None):
        """Handle Ctrl+F globally."""
        # Removed tab check to maximize reliability during debugging
        # Search dialog handles its own safety checks
        self._show_search_dialog()



    def _on_log_key_press(self, event):
        """Handle key presses in Spectral Log to enforce read-only but allow copy."""
        # Allow navigation
        if event.keysym in ["Up", "Down", "Left", "Right", "Home", "End", "Next", "Prior"]:
            return None
            
        # Check for Control key
        if event.state & 0x4:
            # Allow Ctrl+C (Copy), Ctrl+A (Select All)
            if event.keysym.lower() in ['c', 'a']:
                return None
            # Block Ctrl+V (Paste), Ctrl+X (Cut) and others
            return "break"
            
        # Block modification keys (BackSpace, Delete, Return, Tab)
        if event.keysym in ["BackSpace", "Delete", "Return", "Tab"]:
            return "break"
            
        # Block printable characters
        if event.char and len(event.char) > 0 and ord(event.char) >= 32:
             return "break"
             
        return None

    def _on_yaml_key_press(self, event):
        """Handle key presses in YAML viewer to enforce read-only but allow navigation/copy."""
        # Allow navigation keys
        if event.keysym in ["Up", "Down", "Left", "Right", "Home", "End", "Next", "Prior"]:
            return None
            
        # Allow Ctrl+C, Ctrl+A (Copy, Select All)
        # event.state check: 4 is Control (on Windows/Linux usually), but typically implicit in event.keysym if modifier used?
        # Actually standard check is (event.state & 0x0004) or similar.
        # Simpler: Check event.keysym with strict binding or let through if ctrl is held?
        # Let's rely on common blocked keys.
        
        # Block modification keys
        if event.char and len(event.char) > 0 and ord(event.char) >= 32:
             # Check for Control modifier (Bit 2 normally)
             # If Control is pressed, allow (e.g. Ctrl+C)
             if event.state & 0x4: 
                 return None
             return "break"
             
        if event.keysym in ["BackSpace", "Delete", "Return", "Tab"]:
            return "break"
            
        return None
        
    def _find_prev(self, event=None):
        """Find previous occurrence."""
        self._find_next(backwards=True)

    def _find_next(self, event=None, backwards=False):
        """Find next (or prev) occurrence of text in YAML viewer."""
        query = self.search_entry.get()
        if not query:
            return

        # Remove previous highlight
        self.txt_yaml.tag_remove("found", "1.0", "end")
        
        # Start search from insert cursor
        start_pos = self.txt_yaml.index("insert")
        
        # Perform Search
        # Perform Search
        if backwards:
            # Search backwards from cursor
            # If we are currently at a match, we need to move back 1 char or else we find same match
            start_search = self.txt_yaml.index(f"{start_pos}-1c")
            
            pos = self.txt_yaml.search(query, start_search, stopindex="1.0", backwards=True, nocase=True)
            
            if not pos: # Wrap to end
                 pos = self.txt_yaml.search(query, "end", stopindex="1.0", backwards=True, nocase=True)
        else:
            # Search forwards
            pos = self.txt_yaml.search(query, start_pos, stopindex="end", nocase=True)
            
            # If stuck on same match (because search starts AT index)
            if pos and self.txt_yaml.compare(pos, "==", start_pos):
                 pos = self.txt_yaml.search(query, f"{start_pos}+1c", stopindex="end", nocase=True)

            if not pos: # Wrap to start
                 pos = self.txt_yaml.search(query, "1.0", stopindex="end", nocase=True)

        if pos:
            # Calculate end position
            length = len(query)
            end_pos = f"{pos}+{length}c"
            
            # Highlight
            self.txt_yaml.tag_add("found", pos, end_pos)
            self.txt_yaml.tag_config("found", background="#FFFF00", foreground="#000000")
            self.txt_yaml.tag_raise("found")
            
            # Scroll to show
            self.txt_yaml.see(pos)
            
            # Move cursor to start of match (so next search continues from there? No, from end for fwd, start for back)
            if backwards:
                 self.txt_yaml.mark_set("insert", pos)
            else:
                 self.txt_yaml.mark_set("insert", end_pos)
                 
            # Update Count with current index
            self._update_match_count(current_match_start=pos)
            
            # Add to history
            self._add_to_search_history(query)
            
        else:
            # Not found
            self._update_match_count()
            pass


    def _on_close(self):
        """Handle window close event."""
        # Save window geometry
        if self.prefs_manager.get("remember_window_pos"):
            self.prefs_manager.set("window_geometry", self.geometry())
            self.prefs_manager.save()

        # Close all doc viewers
        if hasattr(self, "_doc_viewers"):
            for viewer in self._doc_viewers:
                if viewer and not viewer._closed:
                    viewer.close()
            self._doc_viewers = []

        # Close main window
        self.destroy()
        sys.exit(0)

    def _resolve_source_file(self, json_path):
        """
        Attempts to find the source Excel file for a given OAS path.
        Traverses up the path keys if exact match is not found.
        """
        if not json_path:
            return None
            
        # Standardize path: Linter uses " > ", Map uses "."
        # Note: Paths like /v1/foo are preserved as single segments if we just string replace
        # But wait, 2.0 > /v1/foo > post
        # If we replace " > " with "." we get paths./v1/foo.post which matches the map key!
        clean_path = json_path.replace(" > ", ".")
        clean_path = clean_path.replace("Root.", "") # Just in case
        
        keys = clean_path.split(".")
        
        # Try full path first, then parent, etc.
        while keys:
            current_path = ".".join(keys)
            if current_path in self.current_source_map:
                return self.current_source_map[current_path]
            keys.pop() # Remove last segment
            
        return None

    def _open_excel_file(self, filename, sheetname=None):
        """Opens the specified Excel file, optionally navigating to a sheet."""
        # Need to find the full path. 
        # Strategy: Look in the Template Directory (self.entry_dir)
        template_dir = self.entry_dir.get()
        if not template_dir or not os.path.exists(template_dir):
             tk.messagebox.showerror("Error", "Template directory is not set or valid.")
             return

        # Simple search in the template directory
        target_path = None
        
        # 1. Exact Match
        for root, dirs, files in os.walk(template_dir):
            if filename in files:
                target_path = os.path.join(root, filename)
                break
        
        # 2. Try with extensions if not found
        if not target_path:
            candidates = []
            for root, dirs, files in os.walk(template_dir):
                for f in files:
                    candidates.append(f)
                    # Check if filename + .xlsm or .xlsx matches
                    if f == filename + ".xlsm" or f == filename + ".xlsx":
                        target_path = os.path.join(root, f)
                        break
                if target_path:
                    break
            
            # 3. Fuzzy Match if still not found
            if not target_path:
                 # Gather all files in a flat list for fuzzy matching
                 all_files = []
                 file_to_path = {}
                 for root, dirs, files in os.walk(template_dir):
                     for f in files:
                         if f.endswith(".xlsm") or f.endswith(".xlsx"):
                             all_files.append(f)
                             file_to_path[f] = os.path.join(root, f)
                 
                 # Fuzzy search
                 matches = difflib.get_close_matches(filename, all_files, n=1, cutoff=0.6)
                 if matches:
                     print(f"Fuzzy matched '{filename}' to '{matches[0]}'")
                     target_path = file_to_path[matches[0]]
        
        if target_path:
            try:
                if HAS_COM and sheetname:
                    # Use COM to open specific sheet
                    try:
                        excel = win32com.client.Dispatch("Excel.Application")
                        excel.Visible = True
                        wb = excel.Workbooks.Open(target_path)
                        # Find sheet
                        try:
                            ws = wb.Sheets(sheetname)
                            ws.Activate()
                        except Exception:
                            print(f"Sheet {sheetname} not found.")
                        
                        # Bring to front (Aggressive)
                        try:
                            # 1. Windows specific focus
                            import ctypes
                            excel_hwnd = excel.Hwnd
                            if excel_hwnd:
                                ctypes.windll.user32.SetForegroundWindow(excel_hwnd)
                            
                            # 2. Excel internal State
                            excel.Visible = True
                            excel.WindowState = -4143 # xlNormal
                            excel.WindowState = -4137 # xlMaximized
                        except:
                            pass
                            
                    except Exception as e:
                         print(f"COM Error, falling back to os.startfile: {e}")
                         os.startfile(target_path)
                else:
                    # Fallback or standard open
                    os.startfile(target_path)
            except Exception as e:
                tk.messagebox.showerror("Error", f"Could not open file: {e}")
        else:
             tk.messagebox.showerror("Error", f"File '{filename}' not found in Template Directory.")

    def _setup_import_tab(self):
        """Setup UI for Tab 1: OAS to Excel (Import/Roundtrip)."""
        self.tab_import.grid_columnconfigure(0, weight=1)
        self.tab_import.grid_rowconfigure(1, weight=0) # Actions (no expansion)
        self.tab_import.grid_rowconfigure(2, weight=1) # Log expands

        # Consolidate Inputs into Single Frame for Alignment
        self.frame_imp_inputs = ctk.CTkFrame(self.tab_import, fg_color="transparent")
        self.frame_imp_inputs.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.frame_imp_inputs.grid_columnconfigure(1, weight=1)

        # Row 0: OAS Source File
        ctk.CTkLabel(self.frame_imp_inputs, text="OAS Source File:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_imp_file = ctk.CTkEntry(self.frame_imp_inputs, placeholder_text="Path to OAS file...")
        self.entry_imp_file.grid(row=0, column=1, padx=(0,10), pady=10, sticky="ew")
        
        # Startup Logic: Load OAS Source File
        remember = self.prefs_manager.get("remember_paths", False)
        if remember:
            saved_imp_file = self.prefs_manager.get("import_source_file", "")
            if saved_imp_file and os.path.exists(saved_imp_file):
                self.entry_imp_file.insert(0, saved_imp_file)
            
        self.btn_browse_imp_file = ctk.CTkButton(self.frame_imp_inputs, text="Browse", width=100, command=self.browse_import_file)
        self.btn_browse_imp_file.grid(row=0, column=2, padx=10, pady=10)

        # Row 1: Excel Output Folder
        ctk.CTkLabel(self.frame_imp_inputs, text="Excel Output Folder:", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_imp_dst = ctk.CTkEntry(self.frame_imp_inputs, placeholder_text="Path to Excel Output Folder...")
        self.entry_imp_dst.grid(row=1, column=1, padx=(0,10), pady=10, sticky="ew")
        

             
        # Startup Logic: Load Excel Output Folder
        remember = self.prefs_manager.get("remember_paths", True)
        if remember:
             load_path = self.prefs_manager.get("excel_output_folder", "")
             if not load_path:
                 load_path = self.prefs_manager.get("last_excel_output", "")
                 
             if load_path and os.path.exists(load_path):
                 self.entry_imp_dst.delete(0, "end")
                 self.entry_imp_dst.insert(0, load_path)
             
        self.btn_browse_imp_dst = ctk.CTkButton(self.frame_imp_inputs, text="Browse", width=100, command=self.browse_import_template_folder)
        self.btn_browse_imp_dst.grid(row=1, column=2, padx=10, pady=10)
        
        # Actions Row (Row 1 - aligned with Tab 2)
        self.frame_imp_act = ctk.CTkFrame(self.tab_import, fg_color="transparent")
        self.frame_imp_act.grid(row=1, column=0, sticky="ew", padx=10, pady=(0,10)) # Match Tab 2 padding
        
        # Import Button
        self.btn_import = ctk.CTkButton(self.frame_imp_act, text="Import to Excel", width=150, font=ctk.CTkFont(weight="bold"), command=self.start_oas_import)
        self.btn_import.pack(side="left", padx=(0, 20))
        
        # Roundtrip Controls (no separator)
        self.btn_roundtrip = ctk.CTkButton(self.frame_imp_act, text="Roundtrip Check", width=150, font=ctk.CTkFont(weight="bold"), command=self.start_roundtrip_check)
        self.btn_roundtrip.pack(side="left", padx=(0, 10))
        
        self.var_line_diff = ctk.BooleanVar(value=False)
        self.chk_line_diff = ctk.CTkCheckBox(self.frame_imp_act, text="Line Diff", variable=self.var_line_diff)
        self.chk_line_diff.pack(side="left", padx=(0, 20))

        # Font Size Control (Cleaned for Tab 1)
        self.frame_imp_font = ctk.CTkFrame(self.frame_imp_act, fg_color="transparent")
        self.frame_imp_font.pack(side="right")

        self.lbl_font_size_imp_val = ctk.CTkLabel(self.frame_imp_font, text="11", width=20)
        self.lbl_font_size_imp_val.pack(side="right")

        self.slider_font_imp = ctk.CTkSlider(self.frame_imp_font, from_=8, to=24, number_of_steps=16, width=150, command=self.update_font_size_imp)
        self.slider_font_imp.set(11)
        self.slider_font_imp.pack(side="right", padx=(5,5))

        ctk.CTkLabel(self.frame_imp_font, text="Font Size:", font=("Arial", 12)).pack(side="right", padx=5)

        # Log Area
        self.import_log_area = ctk.CTkTextbox(self.tab_import, font=("Consolas", 11), wrap="word") 
        self.import_log_area.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        # self.import_log_area.insert("0.0", "Ready for Import/Roundtrip.\n") # Removed
        self.import_log_area.configure(state="disabled")





    def update_font_size_imp(self, value):
        val = int(value)
        self.import_log_area.configure(font=("Consolas", val))
        self.lbl_font_size_imp_val.configure(text=str(val))

    def browse_import_file(self):
        f = filedialog.askopenfilename(filetypes=[("OAS Files", "*.yaml *.yml *.json")])
        if f:
            self.entry_imp_file.delete(0, "end")
            self.entry_imp_file.insert(0, f)
            self.prefs_manager.set("import_source_file", f)
            self.prefs_manager.save()

    def browse_import_template_folder(self):
        d = filedialog.askdirectory()
        if d:
            self.entry_imp_dst.delete(0, "end")
            self.entry_imp_dst.insert(0, d)
            # Decoupled: Only set output folder for Tab 1
            self.prefs_manager.set("excel_output_folder", d)
            self.prefs_manager.set("last_excel_output", d)
            self.prefs_manager.save()



    def _log_import(self, msg):
        def _append():
            self.import_log_area.configure(state="normal")
            self.import_log_area.insert("end", f"{msg}\n")
            self.import_log_area.see("end")
            self.import_log_area.configure(state="disabled")
            self.import_log_area.configure(state="disabled")
            # Also log to main application log window (BUT NOT Gen Tab)
            self.log_app(f"[Import] {msg}") 
            
        self.after(0, _append)

    def start_oas_import(self):
        src_path = self.entry_imp_file.get()
        dst_folder = self.entry_imp_dst.get()
        
        if not src_path or not os.path.exists(src_path):
            self.show_custom_error_dialog("Error", "Invalid OAS File")
            return
        if not dst_folder:
            self.show_custom_error_dialog("Error", "Invalid Output Folder")
            return

        # Check for non-empty output folder
        if os.path.exists(dst_folder) and os.listdir(dst_folder):
             choice = self.show_clean_folder_dialog(dst_folder)
             if choice == "cancel":
                 return
             
             try:
                 if choice == "clear_all":
                     self._log_import(f"Cleaning ALL files in {dst_folder}...")
                     for filename in os.listdir(dst_folder):
                         file_path = os.path.join(dst_folder, filename)
                         try:
                             if os.path.isfile(file_path) or os.path.islink(file_path):
                                 os.unlink(file_path)
                             elif os.path.isdir(file_path):
                                 shutil.rmtree(file_path)
                         except Exception as e:
                             print(f"Failed to delete {file_path}. Reason: {e}")
                             
                 elif choice == "clear_excel":
                     self._log_import(f"Cleaning Excel files in {dst_folder}...")
                     import glob
                     for pat in ["*.xlsx", "*.xlsm"]:
                         for f in glob.glob(os.path.join(dst_folder, pat)):
                             try:
                                 os.remove(f)
                             except Exception as e:
                                 print(f"Failed to delete {f}: {e}")
             except Exception as e:
                 self.show_custom_error_dialog("Error", f"Failed to clean directory: {e}")
                 return

            
        self.btn_import.configure(state="disabled")
        self.import_log_area.configure(state="normal")
        # Do NOT clear log to preserve history if requested
        # self.import_log_area.delete("1.0", "end") 
        self.import_log_area.configure(state="disabled")
        
        threading.Thread(target=self._run_oas_import, args=(src_path, dst_folder)).start()

    def show_custom_error_dialog(self, title, message):
        """Shows a custom error dialog with consistent styling."""
        # Use the module-level class
        dialog = OASErrorDialog(self, title, message)
        self.wait_window(dialog)

    def show_clean_folder_dialog(self, folder_path):
        """Shows a custom dialog to ask user how to handle non-empty folder.
           Returns: 'clear_all', 'clear_excel', 'keep', or 'cancel'
        """
        # Inner class to handle the dialog properly and fix icon issue
        class CleanFolderDialog(ctk.CTkToplevel):
            def __init__(self, parent):
                super().__init__(parent)
                self.title("Folder Not Empty")
                self.geometry("550x220") # Reduced height for balance
                self.resizable(False, False)
                self.choice = "cancel"

                # Center relative to parent
                self.update_idletasks()
                x = parent.winfo_x() + (parent.winfo_width() // 2) - 275
                y = parent.winfo_y() + (parent.winfo_height() // 2) - 110
                try:
                    self.geometry(f"+{int(x)}+{int(y)}")
                except:
                    pass

                self.transient(parent)
                self.grab_set()

                # Icon application with robust path handling
                self.after(200, self._set_icon)
                
                self._build_ui()

            def _get_resource_path(self, relative_path):
                """Get absolute path to resource, works for dev and for PyInstaller"""
                try:
                    # PyInstaller creates a temp folder and stores path in _MEIPASS
                    base_path = sys._MEIPASS
                except Exception:
                    base_path = os.path.abspath(".")

                return os.path.join(base_path, relative_path)

            def _set_icon(self):
                try:
                    # Check both local and bundled path
                    icon_path = "icon.ico"
                    if not os.path.exists(icon_path):
                        icon_path = self._get_resource_path("icon.ico")
                    
                    if os.path.exists(icon_path):
                        try:
                            self.iconbitmap(icon_path)
                        except:
                            pass
                        try:
                            self.wm_iconbitmap(icon_path)
                        except:
                            pass
                except:
                    pass

            def _build_ui(self):
                # Main Container - No top padding to push content up
                main_container = ctk.CTkFrame(self, fg_color="transparent")
                main_container.pack(fill="both", expand=True, padx=20, pady=(0, 10))

                # 1. Content Block (Icon + Text) - Centered Vertically
                content_frame = ctk.CTkFrame(main_container, fg_color="transparent")
                content_frame.pack(fill="x", expand=True) # expand=True centers it in available space

                # Icon - Darker Gold using unicode
                icon_label = ctk.CTkLabel(content_frame, text="\u26A0", 
                                          text_color="#FBC02D", 
                                          font=ctk.CTkFont(size=52)) # Slightly larger
                icon_label.pack(side="left", padx=(10, 20))

                # Message Area
                msg_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
                msg_frame.pack(side="left", fill="both", expand=True)

                msg_label = ctk.CTkLabel(msg_frame, text="The Excel Output Folder is not empty.", 
                                         font=ctk.CTkFont(size=18, weight="bold"),
                                         text_color=("#000000", "#FFFFFF"),
                                         anchor="w", justify="left")
                msg_label.pack(fill="x", pady=(0, 0)) # Tighten

                detail_label = ctk.CTkLabel(msg_frame, text="What would you like to do with the existing files?", 
                                         font=ctk.CTkFont(size=12),
                                         text_color="gray",
                                         anchor="w", justify="left")
                detail_label.pack(fill="x", pady=(5, 0))

                # 2. Buttons Area - Bottom Aligned
                btn_container = ctk.CTkFrame(main_container, fg_color="transparent")
                btn_container.pack(fill="x", side="bottom", pady=(0, 5))

                # Row 1: Action Buttons
                row1 = ctk.CTkFrame(btn_container, fg_color="transparent")
                row1.pack(side="top", pady=(0, 10))

                ctk.CTkButton(row1, text="Keep Files", width=120, height=32,
                              command=lambda: self._set_choice("keep")).pack(side="left", padx=5)
                ctk.CTkButton(row1, text="Clear Excel Files", width=140, height=32,
                              command=lambda: self._set_choice("clear_excel")).pack(side="left", padx=5)
                ctk.CTkButton(row1, text="Clear ALL", width=120, height=32, # Red
                              fg_color="#D32F2F", hover_color="#B71C1C",
                              command=lambda: self._set_choice("clear_all")).pack(side="left", padx=5)

                # Row 2: Cancel - Same height, reduced padding
                ctk.CTkButton(btn_container, text="Cancel", width=120, height=32, # Height 32 match
                              command=lambda: self._set_choice("cancel")).pack(side="top", pady=(0, 5))

            def _set_choice(self, choice):
                self.choice = choice
                self.destroy()

        dialog = CleanFolderDialog(self)
        self.wait_window(dialog)
        self.clean_folder_choice = dialog.choice
        return self.clean_folder_choice

    def _run_oas_import(self, src_path, dst_folder):
        try:
            self._log_import(f"Starting Import...")
            self._log_import(f"Source: {src_path}")
            self._log_import(f"Destination: {dst_folder}")
            
            # Helper to adapt _log_import for the converter
            def converter_logger(msg):
                self._log_import(msg)

            converter = OASToExcelConverter(src_path, log_callback=converter_logger)
            
            self._log_import("Generating Index File...")
            converter.generate_index_file(os.path.join(dst_folder, "$index.xlsx"))
            
            self._log_import("Generating Endpoint Files (this may take time)...")
            files = converter.generate_all_endpoint_files(dst_folder)
            
            for f in files:
                 self._log_import(f"   [Created] {os.path.basename(f)}")
            
            self._log_import(f"Success! Generated {len(files)} files.")
            self._log_import("Import Completed.")
            
        except PermissionError:
            err_msg = "Permission Denied: Please close any open Excel files (e.g., $index.xlsx) and try again."
            self._log_import(f"ERROR: {err_msg}")
            self.show_custom_error_dialog("Permission Error", err_msg)
        except Exception as e:
            self._log_import(f"ERROR: {e}")
            import traceback
            self._log_import(traceback.format_exc())
            self.show_custom_error_dialog("Error", f"An unexpected error occurred:\n{e}")
        finally:
            self.after(0, lambda: self.btn_import.configure(state="normal"))

    def start_roundtrip_check(self):
        src_path = self.entry_imp_file.get()
        dst_folder = self.entry_imp_dst.get()
        line_diff = self.var_line_diff.get()
        
        if not src_path or not os.path.exists(src_path):
            self.show_custom_error_dialog("Error", "Invalid OAS File")
            return
        if not dst_folder:
            self.show_custom_error_dialog("Error", "Invalid Output Folder")
            return

        self.btn_roundtrip.configure(state="disabled")
        self.import_log_area.configure(state="normal")
        # Do NOT clear log
        # self.import_log_area.delete("1.0", "end")
        self.import_log_area.configure(state="disabled")
        
        threading.Thread(target=self._run_roundtrip_check, args=(src_path, dst_folder, line_diff)).start()

    def _run_roundtrip_check(self, src_path, dst_folder, line_diff):
        try:
            self._log_import("\n=== STARTING ROUNDTRIP CHECK ===")
            
            # Detect OAS Version from Source
            import yaml
            # Use safe parse to get version
            gen_30 = False
            gen_31 = False
            try:
                with open(src_path, 'r', encoding='utf-8') as f:
                    # Simple check to avoid parsing huge files fully if not needed
                    # But safe_load is robust.
                    data = yaml.safe_load(f)
                    version = data.get('openapi', '')
                    if version.startswith('3.1'):
                        gen_31 = True
                        self._log_import(f"[Setup] Detected OAS 3.1 (Version: {version})")
                    elif version.startswith('3.0'):
                        gen_30 = True
                        self._log_import(f"[Setup] Detected OAS 3.0 (Version: {version})")
                    else:
                        # Fallback or Error
                        self._log_import(f"[Setup] Unknown OAS version '{version}'. Defaulting to 3.0 Generation.")
                        gen_30 = True
            except Exception as e:
                self._log_import(f"[Setup] Could not detect version: {e}. Defaulting to 3.0.")
                gen_30 = True

            # 2. Setup Output Dir
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            rt_dir = os.path.join(dst_folder, "_roundtrip_history", timestamp)
            os.makedirs(rt_dir, exist_ok=True)
            self._log_import(f"[Gen] Generating OAS from Templates...")
            self._log_import(f"Target: {rt_dir}")
            
            # 3. Generate (Only detected version)
            generated_paths = []
            def gen_log(msg):
                self._log_import(f"  [Gen] {msg}")
                if "Writing OAS" in msg:
                    parts = msg.split(": ")
                    if len(parts) > 1:
                        generated_paths.append(parts[1].strip())
                
            main_script.generate_oas(dst_folder, gen_30=gen_30, gen_31=gen_31, gen_swift=False, output_dir=rt_dir, log_callback=gen_log)
            self._log_import("[Gen] Generation Complete.")
            
            # Select Generated File (Dynamic)
            if not generated_paths:
                 self._log_import("ERROR: No OAS files were generated for comparison.")
                 return
                 
            # If multiple versions generated (not expected here due to version detection), pick the first one
            gen_path = generated_paths[0]
            
            if not os.path.exists(gen_path):
                 self._log_import(f"ERROR: Generated OAS file not found at expected path: {gen_path}")
                 return

            self._log_import(f"[Compare] Comparing Source ({os.path.basename(src_path)}) vs Generated ({os.path.basename(gen_path)})...")
            
            comparator = OASComparator(src_path, gen_path)
            
            # Structure Diff
            struct_stats = comparator.get_structure_comparison()
            
            self._log_import("\n=== STRUCTURE SUMMARY ===")
            header_fmt = "{:<30} | {:<10} | {:<10} | {:<7} | {:<10}"
            row_fmt = "{:<30} | {:<10} | {:<10} | {:<7} | {:<10}"
            
            self._log_import(header_fmt.format("Metric", "Source", "Generated", "Match", "Delta"))
            self._log_import("-" * 75)
            
            for metric, (source_val, gen_val) in struct_stats.items():
                delta = gen_val - source_val  # Generated - Source (positive = more in generated)
                match_symbol = "✓" if delta == 0 else "✗"
                delta_str = f"+{delta}" if delta > 0 else str(delta)
                self._log_import(row_fmt.format(metric, str(source_val), str(gen_val), match_symbol, delta_str))
            
            if line_diff:
                # Line Difference Stats (Global Delta)
                self._log_import("\n=== LINE COUNT SUMMARY ===")
                line_stats = comparator.get_line_comparison()
                # {'Total Lines': (source_lines, gen_lines)}
                if 'Total Lines' in line_stats:
                    src_lines, gen_lines = line_stats['Total Lines']
                    delta = gen_lines - src_lines
                    delta_str = f"+{delta}" if delta > 0 else str(delta)
                    
                    self._log_import(f"Source Lines:    {src_lines}")
                    self._log_import(f"Generated Lines: {gen_lines}")
                    self._log_import(f"Delta:           {delta_str}")
                
                # Detailed Breakdown (Calculated only if diff is requested)
                breakdown = comparator.get_detailed_structure_breakdown()

                # 1. COMPONENTS BREAKDOWN (Summary Item Counts)
                if 'components' in breakdown and breakdown['components']:
                    self._log_import("\n=== COMPONENTS BREAKDOWN (Item Counts) ===")
                    comp_fmt = "{:<25} | {:<10} | {:<10} | {:<10}"
                    self._log_import(comp_fmt.format("Subsection", "Source", "Generated", "Delta"))
                    self._log_import("-" * 65)
                    
                    for subsection, (src, gen, delta) in breakdown['components'].items():
                        delta_str = f"+{delta}" if delta > 0 else str(delta)
                        self._log_import(comp_fmt.format(subsection, str(src), str(gen), delta_str))

                # 2. PATHS BREAKDOWN (Line Content Differences)
                if 'paths' in breakdown and breakdown['paths']:
                    self._log_import("\n=== PATHS BREAKDOWN (Line Content Differences) ===")
                    path_fmt = "{:<50} | {:<10} | {:<10} | {:<10}"
                    self._log_import(path_fmt.format("Path", "Source", "Generated", "Delta"))
                    self._log_import("-" * 90)
                    
                    for path_name, src, gen, delta in breakdown['paths']:
                        delta_str = f"+{delta}" if delta > 0 else str(delta)
                        # Truncate path if too long
                        display_path = path_name if len(path_name) <= 50 else path_name[:47] + "..."
                        self._log_import(path_fmt.format(display_path, str(src), str(gen), delta_str))

                # 3. DETAILED COMPONENT DISCREPANCIES (New Section)
                comp_discrepancies = comparator.get_component_discrepancies()
                has_issues = any(len(v) > 0 for v in comp_discrepancies.values())
                
                if has_issues:
                        self._log_import("\n=== DETAILED COMPONENT DISCREPANCIES (Content/Line Differences) ===")
                        for comp_type, items in comp_discrepancies.items():
                            if not items: continue
                            self._log_import(f"\n--- {comp_type.upper()} ---")
                            self._log_import(f"{'Name':<50} | {'Source':<7} | {'Gen':<7} | {'Delta':<5}")
                            for name, s_l, g_l, d in items: # Showing ALL Discrepancies
                                d_str = f"+{d}" if d > 0 else str(d)
                                disp_name = name if len(name) < 50 else name[:47] + "..."
                                self._log_import(f"{disp_name:<50} | {s_l:<7} | {g_l:<7} | {d_str:<5}")
            
            # REMOVED DETAILED DIFF PER USER REQUEST
            # if line_diff and (diff_stats['Added Lines'] > 0 or diff_stats['Removed Lines'] > 0):
                # ...
            
            self._log_import("\n=== ROUNDTRIP CHECK COMPLETED ===")
            
        except Exception as e:
            self._log_import(f"CRITICAL ERROR: {e}")
            import traceback
            self._log_import(traceback.format_exc())
            
        finally:
            self.after(0, lambda: self.btn_roundtrip.configure(state="normal"))




    def _on_close(self):
        """Handle application close: Save session state and geometry."""
        # Save Window Geometry
        self.prefs_manager.set("window_geometry", self.geometry())

        # Save Session State (Last Used Paths)
        # We save these regardless of the 'remember' setting, so they are available
        # if the user toggles 'remember' on later.
        try:
            current_excel_in = self.entry_dir.get()
            current_excel_out = self.entry_imp_dst.get()
            current_oas = self.entry_oas_folder.get()
            
            self.prefs_manager.set("last_excel_input", current_excel_in)
            self.prefs_manager.set("last_excel_output", current_excel_out)
            self.prefs_manager.set("last_oas_folder", current_oas)
            
            # Also save OAS Source File from Import tab
            if hasattr(self, 'entry_imp_file'):
                 self.prefs_manager.set("import_source_file", self.entry_imp_file.get())
            
            self.prefs_manager.save()
        except Exception as e:
            print(f"Error saving session state: {e}")

        # specific cleanup
        try:
             # Stop any running threads or processes if needed
             pass
        except:
            pass

        self.destroy()

if __name__ == "__main__":
    app = OASGenApp()
    app.mainloop()
