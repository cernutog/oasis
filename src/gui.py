import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import threading
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
except ImportError:
    # Fall back to absolute imports (works when frozen or run directly)
    import main as main_script
    from linter import SpectralRunner
    from charts import SemanticPieChart
    from redoc_gen import RedocGenerator
    from preferences import PreferencesManager
    from preferences_dialog import PreferencesDialog
    from doc_viewer import DockedDocViewer

from chlorophyll import CodeView
import pygments.lexers

# Set Theme
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


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


class OASGenApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("OASIS - OAS Integration Suite")
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

        # --- Header ---
        self.frame_header = ctk.CTkFrame(self, corner_radius=0)
        self.frame_header.grid(row=0, column=0, sticky="ew", padx=0, pady=0)

        self.lbl_title = ctk.CTkLabel(
            self.frame_header,
            text="OASIS",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.lbl_title.pack(padx=20, pady=15, side="left")

        self.lbl_version = ctk.CTkLabel(
            self.frame_header, text="v1.2.2", font=ctk.CTkFont(size=12)
        )
        self.lbl_version.pack(padx=20, pady=15, side="right")

        # Settings button - use text for clarity
        self.btn_settings = ctk.CTkButton(
            self.frame_header,
            text="⛭",  # Gear without hub, cleaner look
            width=35,
            height=35,
            font=ctk.CTkFont(size=20),
            command=self.open_preferences,
        )
        self.btn_settings.pack(padx=(0, 5), pady=10, side="right")

        # Add tooltip on hover
        self._tooltip = None
        self.btn_settings.bind("<Enter>", self._show_settings_tooltip)
        self.btn_settings.bind("<Leave>", self._hide_settings_tooltip)

        # --- Tab View ---
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        self.tab_gen = self.tabview.add("Generation")
        self.tab_val = self.tabview.add("Validation")

        # ==========================
        # TAB 1: GENERATION
        # ==========================
        self.tab_gen.grid_columnconfigure(0, weight=1)
        self.tab_gen.grid_rowconfigure(2, weight=1)  # Log expands

        # Controls
        self.frame_controls = ctk.CTkFrame(self.tab_gen, fg_color="transparent")
        self.frame_controls.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.frame_controls.grid_columnconfigure(1, weight=1)

        self.lbl_dir = ctk.CTkLabel(
            self.frame_controls,
            text="Template Directory:",
            font=ctk.CTkFont(weight="bold"),
        )
        self.lbl_dir.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.entry_dir = ctk.CTkEntry(
            self.frame_controls, placeholder_text="Path to API Templates..."
        )
        self.entry_dir.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ew")

        # Use saved preference or default path
        saved_template_dir = self.prefs_manager.get("template_directory", "")
        if saved_template_dir and os.path.exists(saved_template_dir):
            self.entry_dir.insert(0, saved_template_dir)
        else:
            default_path = os.path.join(os.getcwd(), "..", "API Templates")
            if os.path.exists(default_path):
                self.entry_dir.insert(0, os.path.abspath(default_path))
            else:
                self.entry_dir.insert(0, os.getcwd())

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

        # Use saved preference or default OAS folder
        saved_oas_folder = self.prefs_manager.get("oas_folder", "")
        if saved_oas_folder and os.path.exists(saved_oas_folder):
            self.entry_oas_folder.insert(0, saved_oas_folder)
        else:
            default_oas_folder = os.path.join(os.getcwd(), "OAS Generated")
            self.entry_oas_folder.insert(0, os.path.abspath(default_oas_folder))

        self.btn_browse_oas = ctk.CTkButton(
            self.frame_controls,
            text="Browse",
            width=100,
            command=self.browse_oas_folder,
        )
        self.btn_browse_oas.grid(row=1, column=2, padx=10, pady=10)

        # Options
        self.frame_opts = ctk.CTkFrame(self.tab_gen, fg_color="transparent")
        self.frame_opts.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 10))

        self.var_31 = ctk.BooleanVar(value=self.prefs_manager.get("gen_oas_31", True))
        self.chk_31 = ctk.CTkCheckBox(
            self.frame_opts, text="OAS 3.1", variable=self.var_31
        )
        self.chk_31.pack(side="left", padx=(0, 20))

        self.var_30 = ctk.BooleanVar(value=self.prefs_manager.get("gen_oas_30", True))
        self.chk_30 = ctk.CTkCheckBox(
            self.frame_opts, text="OAS 3.0", variable=self.var_30
        )
        self.chk_30.pack(side="left", padx=(0, 20))

        self.var_swift = ctk.BooleanVar(
            value=self.prefs_manager.get("gen_oas_swift", False)
        )
        self.chk_swift = ctk.CTkCheckBox(
            self.frame_opts, text="OAS SWIFT", variable=self.var_swift
        )
        self.chk_swift.pack(side="left")

        # Generate Button layout on the right of opts? Or below? Below logs?
        # Let's keep it prominent.
        self.btn_gen = ctk.CTkButton(
            self.frame_opts,
            text="GENERATE",
            font=ctk.CTkFont(weight="bold"),
            width=150,
            command=self.start_generation,
        )
        self.btn_gen.pack(side="left", padx=40)

        # Log Area with theme from preferences
        gen_log_theme = self.prefs_manager.get("gen_log_theme", "Light")
        if gen_log_theme == "Dark":
            self.log_area = ctk.CTkTextbox(
                self.tab_gen, fg_color="#1e1e1e", text_color="#d4d4d4"
            )
        else:
            self.log_area = ctk.CTkTextbox(
                self.tab_gen, fg_color="#ffffff", text_color="#333333"
            )
        self.log_area.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.log_area.insert("0.0", "Ready to generate.\n")
        self.log_area.configure(state="disabled")

        # ==========================
        # TAB 2: VALIDATION
        # ==========================
        self.linter = SpectralRunner()
        self.last_lint_result = None
        self.last_generated_files = []  # Track files from generation
        self.validated_file = None  # Track which file was validated
        self.validation_issues = {}  # {line_number: [(severity, message), ...]}

        self.tab_val.grid_columnconfigure(0, weight=1)  # List
        self.tab_val.grid_columnconfigure(1, weight=1)  # Chart
        self.tab_val.grid_rowconfigure(2, weight=1)  # Content pane expands
        self.tab_val.grid_rowconfigure(3, weight=0)  # Footer row

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
        # Progress Bar Removed as per user request

        # Main Layout: List vs Chart

        # Use PanedWindow for resizable Log Console
        self.paned_val = tk.PanedWindow(
            self.tab_val, orient="vertical", sashrelief="raised", bg="#d0d0d0"
        )
        self.paned_val.grid(
            row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5
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
            text="▼ Logs",
            width=60,
            height=20,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.toggle_log,
        )
        self.btn_toggle_log_h.pack(side="left", padx=5, pady=2)

        self.tab_logs = ctk.CTkTabview(self.val_log_frame, height=150)
        self.tab_logs.pack(
            fill="both", expand=True, padx=2, pady=0
        )  # reduced top padding

        self.tab_logs.add("Analysis Logs")
        self.tab_logs.add("Spectral Output")

        # Tab 1: Analysis Logs with theme from preferences
        analysis_log_theme = self.prefs_manager.get("analysis_log_theme", "Light")
        if analysis_log_theme == "Dark":
            self.val_log = ctk.CTkTextbox(
                self.tab_logs.tab("Analysis Logs"),
                font=("Consolas", 11),
                state="disabled",
                fg_color="#1e1e1e",
                text_color="#d4d4d4",
            )
        else:
            self.val_log = ctk.CTkTextbox(
                self.tab_logs.tab("Analysis Logs"),
                font=("Consolas", 11),
                state="disabled",
                fg_color="#ffffff",
                text_color="#333333",
            )
        self.val_log.pack(fill="both", expand=True)

        # Tab 2: Spectral Output with theme from preferences
        spectral_log_theme = self.prefs_manager.get("spectral_log_theme", "Light")
        if spectral_log_theme == "Dark":
            self.val_json_log = ctk.CTkTextbox(
                self.tab_logs.tab("Spectral Output"),
                font=("Consolas", 11),
                state="disabled",
                wrap="none",
                fg_color="#1e1e1e",
                text_color="#d4d4d4",
            )
        else:
            self.val_json_log = ctk.CTkTextbox(
                self.tab_logs.tab("Spectral Output"),
                font=("Consolas", 11),
                state="disabled",
                wrap="none",
                fg_color="#ffffff",
                text_color="#333333",
            )
        self.val_json_log.pack(fill="both", expand=True)

        # Persistent Footer (Status Bar + Log Toggle) -> For Collapsed State
        self.footer_frame = ctk.CTkFrame(
            self.tab_val, height=30, corner_radius=0, fg_color=("gray85", "gray20")
        )
        self.footer_frame.grid(row=3, column=0, columnspan=2, sticky="ew")

        self.btn_toggle_log_f = ctk.CTkButton(
            self.footer_frame,
            text="▶ Logs",
            width=60,
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

        # Apply saved theme after initialization
        saved_theme = self.prefs_manager.get("yaml_theme", "oas-dark")
        self.after(100, lambda: self.on_theme_change(saved_theme))

        # Redoc Generator initialization
        self.redoc_gen = RedocGenerator()

        self.val_log_print("Ready.")
        self.log_visible = False

        # Load file lists on startup (after widgets are ready)
        self.after(200, self._load_files_on_startup)

    def _load_files_on_startup(self):
        """Load file lists in Validation and View tabs on startup."""
        oas_dir = self.entry_oas_folder.get()
        if os.path.exists(oas_dir):
            self.update_file_list()
        else:
            self.val_log_print(f"OAS folder not found: {oas_dir}")

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

    def _show_settings_tooltip(self, event):
        """Show tooltip for settings button."""
        if self._tooltip is None:
            x = self.btn_settings.winfo_rootx() + self.btn_settings.winfo_width() // 2
            y = self.btn_settings.winfo_rooty() + self.btn_settings.winfo_height() + 5
            self._tooltip = tk.Toplevel(self)
            self._tooltip.wm_overrideredirect(True)
            self._tooltip.wm_geometry(f"+{x - 40}+{y}")
            label = tk.Label(
                self._tooltip,
                text="Preferences",
                bg="#333",
                fg="white",
                font=("Segoe UI", 9),
                padx=8,
                pady=4,
            )
            label.pack()

    def _hide_settings_tooltip(self, event):
        """Hide tooltip for settings button."""
        if self._tooltip:
            self._tooltip.destroy()
            self._tooltip = None

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

    def _apply_preferences(self, new_prefs: dict):
        """Apply new preferences to the UI."""
        # Apply YAML theme
        if "yaml_theme" in new_prefs:
            self.on_theme_change(new_prefs["yaml_theme"])
            self.cbo_yaml_theme.set(new_prefs["yaml_theme"])

        # Apply font size (if CodeView supports it)
        if "yaml_font_size" in new_prefs:
            try:
                font_size = new_prefs["yaml_font_size"]
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

        if "analysis_log_theme" in new_prefs:
            theme = new_prefs["analysis_log_theme"]
            if theme == "Dark":
                self.val_log.configure(fg_color="#1e1e1e", text_color="#d4d4d4")
            else:
                self.val_log.configure(fg_color="#ffffff", text_color="#333333")

        if "spectral_log_theme" in new_prefs:
            theme = new_prefs["spectral_log_theme"]
            if theme == "Dark":
                self.val_json_log.configure(fg_color="#1e1e1e", text_color="#d4d4d4")
            else:
                self.val_json_log.configure(fg_color="#ffffff", text_color="#333333")

        # Refresh file list with new sort order
        self.update_file_list()

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
        self.val_log.configure(state="normal")
        self.val_log.insert("end", f"> {msg}\n")
        self.val_log.see("end")
        self.val_log.configure(state="disabled")

    def browse_dir(self):
        current_path = self.entry_dir.get()
        initial_dir = current_path if os.path.exists(current_path) else os.getcwd()
        directory = filedialog.askdirectory(initialdir=initial_dir)
        if directory:
            self.entry_dir.delete(0, "end")
            self.entry_dir.insert(0, directory)

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
        self.refresh_view_files()

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

    def log(self, message):
        self.log_area.configure(state="normal")
        self.log_area.insert("end", message + "\n")
        self.log_area.see("end")
        self.log_area.configure(state="disabled")

    def start_generation(self):
        base_dir = self.entry_dir.get()
        gen_30 = self.var_30.get()
        gen_31 = self.var_31.get()
        gen_swift = self.var_swift.get()

        if not base_dir:
            self.log("ERROR: Please select a directory.")
            return

        self.btn_gen.configure(state="disabled", text="GENERATING...")
        self.log("Starting generation process...")

        t = threading.Thread(
            target=self.run_process, args=(base_dir, gen_30, gen_31, gen_swift)
        )
        t.start()

    def run_process(self, base_dir, gen_30, gen_31, gen_swift):
        try:
            self.last_generated_files = []
            output_dir = self.entry_oas_folder.get()  # Get OAS output folder

            def gui_logger(msg):
                self.after(0, self.log, msg)
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
            self.after(0, self.log, f"CRITICAL ERROR: {e}")
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
            self.run_validation()
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

        self.val_log_print(f"Starting validation for: {selected_name}")
        # self.progress_val.start()

        for widget in self.frame_list.winfo_children():
            widget.destroy()

        def validate_thread():
            try:
                # Capture logs from linter
                def thread_logger(msg):
                    self.after(0, lambda: self.val_log_print(msg))

                result = self.linter.run_lint(selected_file, log_callback=thread_logger)
                self.after(0, lambda: self.show_results(result))
            except Exception as e:
                self.after(0, lambda: self.val_log_print(f"THREAD CRASH: {e}"))
            finally:
                pass
                # self.after(0, self.progress_val.stop)

        t = threading.Thread(target=validate_thread)
        t.start()

    def on_filter_change(self):
        if self.last_lint_result:
            self.show_results(self.last_lint_result)

    def show_results(self, result):
        self.last_lint_result = result  # Store for filtering

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
        self.validated_file = self.cbo_files.get()  # Get filename being validated
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

        # Populate Raw JSON Tab
        raw_data = result.get("raw_data", [])
        formatted_json = json.dumps(raw_data, indent=2)

        self.val_json_log.configure(state="normal")
        self.val_json_log.delete("0.0", "end")
        self.val_json_log.insert("0.0", formatted_json)
        self.val_json_log.configure(state="disabled")

        # Populate List
        for widget in self.frame_list.winfo_children():
            widget.destroy()

        if total_issues == 0:
            ctk.CTkLabel(
                self.frame_list,
                text="No issues found! Great job!",
                text_color="green",
                font=("Arial", 16),
            ).pack(pady=20)
        else:
            for item in details:
                # Severity Color
                color = "gray"
                if item["severity"] == "error":
                    color = "#FF4444"
                elif item["severity"] == "warning":
                    color = "#FFBB33"
                elif item["severity"] == "info":
                    color = "#33B5E5"

                # Card Frame
                card = ctk.CTkFrame(
                    self.frame_list, border_width=1, border_color="gray"
                )
                card.pack(fill="x", pady=2, padx=2)

                # Row 1: Code + Severity
                r1 = ctk.CTkFrame(card, fg_color="transparent")
                r1.pack(fill="x", padx=5, pady=2)
                ctk.CTkLabel(
                    r1,
                    text=f"[{item['severity'].upper()}]",
                    text_color=color,
                    font=("Arial", 11, "bold"),
                ).pack(side="left")
                ctk.CTkLabel(r1, text=item["code"], font=("Arial", 11, "bold")).pack(
                    side="left", padx=5
                )

                # Clickable line number - styled as button
                line_num = item["line"]
                line_btn = ctk.CTkButton(
                    r1,
                    text=f"Line: {line_num}",
                    font=("Arial", 10),
                    fg_color=("#E8E8E8", "#3D3D3D"),  # Light gray / dark gray
                    text_color=("#333333", "#FFFFFF"),
                    hover_color=("#D0D0D0", "#505050"),
                    border_width=1,
                    border_color=("#AAAAAA", "#666666"),
                    corner_radius=4,
                    width=70,
                    height=22,
                    command=lambda ln=line_num: self._goto_line(ln),
                )
                line_btn.pack(side="right")

                # Row 2: Path
                if item["path"] and item["path"] != "Root":
                    # High contrast for path
                    path_color = (
                        "#333333",
                        "#CCCCCC",
                    )  # Dark in light mode, Light in dark mode
                    ctk.CTkLabel(
                        card,
                        text=f"Path: {item['path']}",
                        text_color=path_color,
                        font=("Consolas", 10, "bold"),
                        anchor="w",
                        justify="left",
                        wraplength=350,
                    ).pack(fill="x", padx=5)

                # Row 3: Message
                ctk.CTkLabel(
                    card,
                    text=item["message"],
                    anchor="w",
                    justify="left",
                    wraplength=350,
                ).pack(fill="x", padx=5, pady=(0, 5))

        # Refresh markers in View tab if viewing the same file
        current_view_file = (
            self.cbo_view_files.get() if hasattr(self, "cbo_view_files") else None
        )
        if current_view_file and current_view_file == self.validated_file:
            self._apply_validation_markers(current_view_file)

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
            # Trigger validation for the new file if it's different
            if self.validated_file and self.validated_file != value:
                self.run_validation()

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

            self.txt_yaml.config(state="disabled")

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

        # Debug logging
        self.val_log_print(
            f"Markers check: file='{filename}', validated='{self.validated_file}', issues={len(self.validation_issues)}"
        )

        # Check if this is the validated file
        if filename != self.validated_file or not self.validation_issues:
            self.val_log_print(f"Markers not applied: filename mismatch or no issues")
            # Hide nav bar when viewing a different file
            self.nav_frame.pack_forget()
            self._clear_marker_indicator()
            return

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

        self.val_log_print(f"Markers applied to {len(self.validation_issues)} lines")

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


if __name__ == "__main__":
    app = OASGenApp()
    app.mainloop()
