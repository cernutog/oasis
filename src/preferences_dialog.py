"""
Preferences Dialog for OAS Generation Tool.
Modal dialog for configuring application settings.
"""

import customtkinter as ctk
from tkinter import filedialog
import os
import sys


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def ask_confirmation(parent, title, message):
    """Refactored to use Custom Dialog."""
    dialog = OASConfirmationDialog(parent, title, message)
    parent.wait_window(dialog)
    return dialog.result

class OASConfirmationDialog(ctk.CTkToplevel):
    """Custom confirmation dialog (Modal)."""
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.title(title)
        self.geometry("420x180")
        self.resizable(False, False)
        self.result = False

        # Center
        self.update_idletasks()
        try:
            x = parent.winfo_x() + (parent.winfo_width() // 2) - 210
            y = parent.winfo_y() + (parent.winfo_height() // 2) - 90
            self.geometry(f"+{int(x)}+{int(y)}")
        except:
            pass

        self.transient(parent)
        self.grab_set()
        
        # Icon
        self.after(200, self._set_icon)
        
        self._build_ui(message)
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)

    def _set_icon(self):
        try:
            # Try to grab icon from parent or resource
            if hasattr(self.master, "iconbitmap"):
                 pass # Already inherits?
        except:
            pass

    def _build_ui(self, message):
        # Container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Flex Row for Icon + Text
        row = ctk.CTkFrame(container, fg_color="transparent")
        row.pack(fill="x", pady=(0, 20))

        # Icon (Question Mark)
        ctk.CTkLabel(row, text="?", text_color="#0A809E", 
                     font=ctk.CTkFont(size=40, weight="bold")).pack(side="left", padx=(0, 15), anchor="n")

        # Message
        ctk.CTkLabel(row, text=message, wraplength=300, justify="left",
                     font=ctk.CTkFont(size=13)).pack(side="left", fill="both", expand=True)

        # Buttons
        btns = ctk.CTkFrame(container, fg_color="transparent")
        btns.pack(fill="x", side="bottom")

        ctk.CTkButton(btns, text="Cancel", fg_color="gray50", hover_color="gray40", width=100,
                      command=self._on_cancel).pack(side="right", padx=(10, 0))
        
        ctk.CTkButton(btns, text="OK", fg_color="#0A809E", hover_color="#076075", width=100,
                      command=self._on_ok).pack(side="right")

    def _on_ok(self):
        self.result = True
        self.destroy()

    def _on_cancel(self):
        self.result = False
        self.destroy()


class PreferencesDialog(ctk.CTkToplevel):
    """Non-modal dialog for editing user preferences."""

    THEMES = [
        "oas-dark",
        "oas-light",
        "github-dark",
        "nord",
        "one-dark",
        "vs-dark",
        "monokai",
        "dracula",
        "ayu-dark",
        "ayu-light",
    ]
    SORT_OPTIONS = [
        ("Alphabetical", "alphabetical"),
        ("Newest First", "newest_first"),
        ("Oldest First", "oldest_first"),
    ]
    TAB_OPTIONS = ["OAS Generation", "Validation", "View"]

    def __init__(self, parent, prefs_manager, on_save_callback=None):
        super().__init__(parent)

        self.prefs_manager = prefs_manager
        self.on_save_callback = on_save_callback
        self.result = None  # Will be True if saved, False/None if cancelled

        # Window setup
        self.title("Preferences")
        self.geometry("720x560")
        self.resizable(True, True) 

        # Non-modal: only transient
        self.transient(parent)

        # Center on parent
        self.update_idletasks()
        try:
            x = parent.winfo_x() + (parent.winfo_width() - 720) // 2
            y = parent.winfo_y() + (parent.winfo_height() - 560) // 2
            self.geometry(f"720x560+{int(x)}+{int(y)}")

        except:
             pass

        # Set window icon AFTER CTkToplevel's internal 200ms default icon setting
        self.after(250, self._set_icon)

        # Build UI
        self._build_ui()
        self._load_current_values()

        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)

    def _set_icon(self):
        """Set window icon - called 250ms after init to override CTkToplevel default."""
        try:
            icon_file = resource_path("icon.ico")
            if os.path.exists(icon_file):
                self.iconbitmap(icon_file)
        except (OSError, FileNotFoundError, Exception):
            pass

    def _add_section_separator(self, parent, text):
        """Add a captioned horizontal separator line to a tab."""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=10, pady=(12, 6))

        # Left line
        left_line = ctk.CTkFrame(frame, height=2, fg_color="#888888")
        left_line.pack(side="left", fill="x", expand=True, pady=8)

        # Caption (bold teal)
        lbl = ctk.CTkLabel(frame, text=f"  {text}  ", font=ctk.CTkFont(size=12, weight="bold"), text_color="#0A809E")
        lbl.pack(side="left")

        # Right line
        right_line = ctk.CTkFrame(frame, height=2, fg_color="#888888")
        right_line.pack(side="left", fill="x", expand=True, pady=8)

    def _build_ui(self):
        """Build the preferences UI with Tabs."""
        self.tabview = ctk.CTkTabview(self, segmented_button_selected_color="#0A809E", segmented_button_selected_hover_color="#076075")
        # .pack() moved to bottom of _build_ui for correct rendering order


        # Create Tabs
        self.tab_gen = self.tabview.add("General")
        self.tab_output = self.tabview.add("OAS Generation")
        self.tab_val = self.tabview.add("Validation")
        self.tab_view = self.tabview.add("View")
        self.tab_templates = self.tabview.add("Templates")
        self.tab_diff = self.tabview.add("OAS Comparison")
        self.tab_logs = self.tabview.add("Logs")

        # === 1. GENERAL TAB ===
        # Default Tab
        ctk.CTkLabel(self.tab_gen, text="Default Tab:").grid(row=0, column=0, sticky="w", padx=(10, 10), pady=10)
        self.cbo_tab = ctk.CTkComboBox(self.tab_gen, values=self.TAB_OPTIONS, width=150, button_color="#0A809E")
        self.cbo_tab.grid(row=0, column=1, sticky="w", pady=10)

        # Sort Order
        ctk.CTkLabel(self.tab_gen, text="File List Order:").grid(row=1, column=0, sticky="w", padx=(10, 10), pady=10)
        self.cbo_sort = ctk.CTkComboBox(self.tab_gen, values=[opt[0] for opt in self.SORT_OPTIONS], width=150, button_color="#0A809E")
        self.cbo_sort.grid(row=1, column=1, sticky="w", pady=10)

        # Remember Switches
        self.var_remember = ctk.BooleanVar(value=False)
        self.chk_remember = ctk.CTkSwitch(
            self.tab_gen, 
            text="Remember files and paths",
            variable=self.var_remember,
            progress_color="#0A809E"
        )
        self.chk_remember.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=(20, 10))

        self.chk_window_pos = ctk.CTkSwitch(
            self.tab_gen, text="Remember window size and position", progress_color="#0A809E"
        )
        self.chk_window_pos.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=10)


        # === 2. OAS GENERATION TAB ===
        self.chk_oas31 = ctk.CTkSwitch(self.tab_output, text="OAS 3.1", progress_color="#0A809E")
        self.chk_oas31.pack(anchor="w", padx=20, pady=(20, 10))

        self.chk_oas30 = ctk.CTkSwitch(self.tab_output, text="OAS 3.0", progress_color="#0A809E")
        self.chk_oas30.pack(anchor="w", padx=20, pady=10)

        self.chk_swift = ctk.CTkSwitch(self.tab_output, text="OAS SWIFT", progress_color="#0A809E")
        self.chk_swift.pack(anchor="w", padx=20, pady=10)


        # === 3. TEMPLATES TAB (merged Excel Generation + Tools) ===
        # --- Section: Create Template from OAS ---
        self._add_section_separator(self.tab_templates, "Create Template from OAS")

        self.chk_excel_attr_diff = ctk.CTkSwitch(self.tab_templates, text="Attribute Diff", progress_color="#0A809E")
        self.chk_excel_attr_diff.pack(anchor="w", padx=20, pady=(3, 6))

        self.chk_excel_line_diff = ctk.CTkSwitch(self.tab_templates, text="Line Diff", progress_color="#0A809E")
        self.chk_excel_line_diff.pack(anchor="w", padx=20, pady=(3, 6))

        # --- Section: Legacy Tools ---
        self._add_section_separator(self.tab_templates, "Legacy Tools")

        self.var_legacy_tracing = ctk.BooleanVar(value=True)
        self.chk_legacy_tracing = ctk.CTkSwitch(
            self.tab_templates, 
            text="Enable Schema Tracing by default",
            variable=self.var_legacy_tracing,
            progress_color="#0A809E"
        )
        self.chk_legacy_tracing.pack(anchor="w", padx=20, pady=(3, 6))

        self.var_legacy_collision_desc = ctk.BooleanVar(value=False)
        self.chk_legacy_collision_desc = ctk.CTkSwitch(
            self.tab_templates,
            text="Include descriptions in collision detection",
            variable=self.var_legacy_collision_desc,
            progress_color="#0A809E",
        )
        self.chk_legacy_collision_desc.pack(anchor="w", padx=20, pady=(3, 6))

        self.var_legacy_collision_examples = ctk.BooleanVar(value=False)
        self.chk_legacy_collision_examples = ctk.CTkSwitch(
            self.tab_templates,
            text="Include examples in collision detection",
            variable=self.var_legacy_collision_examples,
            progress_color="#0A809E",
        )
        self.chk_legacy_collision_examples.pack(anchor="w", padx=20, pady=(3, 6))

        self.var_legacy_capitalize_schemas = ctk.BooleanVar(value=True)
        self.chk_legacy_capitalize_schemas = ctk.CTkSwitch(
            self.tab_templates,
            text="Capitalize operationId in schema names (PascalCase)",
            variable=self.var_legacy_capitalize_schemas,
            progress_color="#0A809E",
        )
        self.chk_legacy_capitalize_schemas.pack(anchor="w", padx=20, pady=(3, 6))


        # === 4. VALIDATION TAB ===
        frame_linter = ctk.CTkFrame(self.tab_val, fg_color="transparent")
        frame_linter.pack(anchor="w", padx=20, pady=(20, 10))
        ctk.CTkLabel(frame_linter, text="Linter Engine:").pack(side="left", padx=(0, 10))
        self.cbo_linter_engine = ctk.CTkComboBox(
            frame_linter, values=["Spectral", "Vacuum"], width=150, button_color="#0A809E"
        )
        self.cbo_linter_engine.pack(side="left")

        self.chk_ignore_br = ctk.CTkSwitch(
            self.tab_val, text="Ignore 'Bad Request' Examples", progress_color="#0A809E"
        )
        self.chk_ignore_br.pack(anchor="w", padx=20, pady=(10, 20))


        # === 5. VIEW TAB ===
        ctk.CTkLabel(self.tab_view, text="Theme:").grid(row=0, column=0, sticky="w", padx=(10, 10), pady=10)
        self.cbo_theme = ctk.CTkComboBox(self.tab_view, values=self.THEMES, width=200, button_color="#0A809E")
        self.cbo_theme.grid(row=0, column=1, sticky="w", pady=10)

        ctk.CTkLabel(self.tab_view, text="Font:").grid(row=1, column=0, sticky="w", padx=(10, 10), pady=10)
        self.cbo_font = ctk.CTkComboBox(self.tab_view,
            values=["Consolas", "Courier New", "Monaco", "Fira Code", "JetBrains Mono", "Source Code Pro"],
            width=200, button_color="#0A809E")
        self.cbo_font.grid(row=1, column=1, sticky="w", pady=10)

        ctk.CTkLabel(self.tab_view, text="Font Size:").grid(row=2, column=0, sticky="w", padx=(10, 10), pady=10)
        self.frame_font = ctk.CTkFrame(self.tab_view, fg_color="transparent")
        self.frame_font.grid(row=2, column=1, sticky="w", pady=10)
        
        self.slider_font = ctk.CTkSlider(self.frame_font, from_=8, to=20, number_of_steps=12, width=150)
        self.slider_font.pack(side="left")
        self.lbl_font_val = ctk.CTkLabel(self.frame_font, text="12", width=30)
        self.lbl_font_val.pack(side="left", padx=(5, 0))
        self.slider_font.configure(command=lambda v: self.lbl_font_val.configure(text=str(int(v))))
        
        self.chk_word_wrap = ctk.CTkSwitch(
            self.tab_view, text="Word wrap in YAML viewer", progress_color="#0A809E"
        )
        self.chk_word_wrap.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=20)

        self.chk_snap_default = ctk.CTkSwitch(
            self.tab_view, text="Dock documentation viewer to main window", progress_color="#0A809E"
        )
        self.chk_snap_default.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 20))


        # === 6. OAS DIFF TAB ===
        self.tab_diff.grid_columnconfigure(0, weight=1)
        self.tab_diff.grid_rowconfigure(5, weight=1) # Spacer row to absorb vertical height

        # Row 0: Separator 1
        sep1 = ctk.CTkFrame(self.tab_diff, fg_color="transparent")
        sep1.grid(row=0, column=0, sticky="ew")
        self._add_section_separator(sep1, "Static Variables (User Defined)")
        
        # Row 1: Label
        help_lbl = ctk.CTkLabel(self.tab_diff, 
                                text="Use placeholders like {{variable_name}} in custom Word templates to inject these values.",
                                font=ctk.CTkFont(size=12, slant="italic"),
                                text_color="#333333")
        help_lbl.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 3))

        self.frame_vars = ctk.CTkFrame(self.tab_diff, fg_color="transparent", height=170)
        self.frame_vars.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 5))
        
        # Standard Frame for variables (replaces scrollable to prevent height expanding bugs)
        self.scroll_vars = ctk.CTkFrame(self.frame_vars, fg_color="transparent")
        self.scroll_vars.pack(fill="x", expand=False, pady=(0, 5))

        self.vars_controls = ctk.CTkFrame(self.frame_vars, fg_color="transparent")
        self.vars_controls.pack(fill="x", expand=False)

        
        ctk.CTkButton(self.vars_controls, text="Add Variable", width=100, fg_color="#0A809E", hover_color="#076075", command=self._on_add_var).pack(side="left", padx=(0, 5))
        ctk.CTkButton(self.vars_controls, text="Clear All", width=100, fg_color="#D04040", hover_color="#B03030", command=self._on_clear_vars).pack(side="left")

        # Row 3: Separator 2
        sep2 = ctk.CTkFrame(self.tab_diff, fg_color="transparent")
        sep2.grid(row=3, column=0, sticky="ew")
        self._add_section_separator(sep2, "Reports Custom Templates")
        
        # Row 4: Templates Frame
        self.frame_tmpl = ctk.CTkFrame(self.tab_diff, fg_color="transparent")
        self.frame_tmpl.grid(row=4, column=0, sticky="ew", padx=10, pady=(0, 5))

        self.frame_tmpl.grid_columnconfigure(1, weight=1) # Make entry column expand
        
        # Synthesis Template
        ctk.CTkLabel(self.frame_tmpl, text="Synthesis:").grid(row=0, column=0, sticky="w", padx=(5, 5))
        self.entry_tmpl_syn = ctk.CTkEntry(self.frame_tmpl)
        self.entry_tmpl_syn.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        ctk.CTkButton(self.frame_tmpl, text="...", width=30, fg_color="#0A809E", hover_color="#076075", command=lambda: self._browse_template("syn")).grid(row=0, column=2)

        # Analytical Template
        ctk.CTkLabel(self.frame_tmpl, text="Analytical:").grid(row=1, column=0, sticky="w", padx=(5, 5))
        self.entry_tmpl_ana = ctk.CTkEntry(self.frame_tmpl)
        self.entry_tmpl_ana.grid(row=1, column=1, sticky="ew", padx=5, pady=2)
        ctk.CTkButton(self.frame_tmpl, text="...", width=30, fg_color="#0A809E", hover_color="#076075", command=lambda: self._browse_template("ana")).grid(row=1, column=2)

        # Impact Template
        ctk.CTkLabel(self.frame_tmpl, text="Impact:").grid(row=2, column=0, sticky="w", padx=(5, 5))
        self.entry_tmpl_imp = ctk.CTkEntry(self.frame_tmpl)
        self.entry_tmpl_imp.grid(row=2, column=1, sticky="ew", padx=5, pady=2)
        ctk.CTkButton(self.frame_tmpl, text="...", width=30, fg_color="#0A809E", hover_color="#076075", command=lambda: self._browse_template("imp")).grid(row=2, column=2)

        # Compatibility Template
        ctk.CTkLabel(self.frame_tmpl, text="Interface:").grid(row=3, column=0, sticky="w", padx=(5, 5))
        self.entry_tmpl_comp = ctk.CTkEntry(self.frame_tmpl)
        self.entry_tmpl_comp.grid(row=3, column=1, sticky="ew", padx=5, pady=2)
        ctk.CTkButton(self.frame_tmpl, text="...", width=30, fg_color="#0A809E", hover_color="#076075", command=lambda: self._browse_template("comp")).grid(row=3, column=2)

        # Flexible spacer to absorb remaining space and pack items tightly at the top
        spacer = ctk.CTkFrame(self.tab_diff, fg_color="transparent")
        spacer.grid(row=5, column=0, sticky="nsew")






        # === 7. LOGS TAB ===
        self.tab_logs.grid_columnconfigure(1, weight=1)

        # OAS Generation Theme
        ctk.CTkLabel(self.tab_logs, text="OAS Generation Theme:").grid(row=0, column=0, sticky="w", padx=(10, 10), pady=10)
        self.cbo_gen_log_theme = ctk.CTkComboBox(self.tab_logs, values=["Light", "Dark"], width=150, button_color="#0A809E")
        self.cbo_gen_log_theme.grid(row=0, column=1, sticky="w", pady=10)

        # Template Import Theme
        ctk.CTkLabel(self.tab_logs, text="Template Import Theme:").grid(row=1, column=0, sticky="w", padx=(10, 10), pady=10)
        self.cbo_import_log_theme = ctk.CTkComboBox(self.tab_logs, values=["Light", "Dark"], width=150, button_color="#0A809E")
        self.cbo_import_log_theme.grid(row=1, column=1, sticky="w", pady=10)

        # App Logs
        ctk.CTkLabel(self.tab_logs, text="Application Logs Theme:").grid(row=2, column=0, sticky="w", padx=(10, 10), pady=10)
        self.cbo_app_log_theme = ctk.CTkComboBox(self.tab_logs, values=["Light", "Dark"], width=150, button_color="#0A809E")
        self.cbo_app_log_theme.grid(row=2, column=1, sticky="w", pady=10)
        
        # Spectral
        ctk.CTkLabel(self.tab_logs, text="Spectral Output Theme:").grid(row=3, column=0, sticky="w", padx=(10, 10), pady=10)
        self.cbo_spectral_log_theme = ctk.CTkComboBox(self.tab_logs, values=["Light", "Dark"], width=150, button_color="#0A809E")
        self.cbo_spectral_log_theme.grid(row=3, column=1, sticky="w", pady=10)


        # === BUTTONS ===
        self.frame_buttons = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_buttons.pack(fill="x", side="bottom", padx=15, pady=15)

        ctk.CTkButton(self.frame_buttons, text="Reset to Defaults", width=130,
                      fg_color=("#D04040", "#B03030"), hover_color=("#B03030", "#902020"),
                      command=self._on_reset).pack(side="left")

        ctk.CTkButton(self.frame_buttons, text="Cancel", width=100,
                      fg_color="#0A809E", hover_color="#076075",
                      command=self._on_cancel).pack(side="right", padx=(10, 0))

        ctk.CTkButton(self.frame_buttons, text="Apply & Close", width=120, 
                      fg_color="#0A809E", hover_color="#076075",
                      command=self._on_save).pack(side="right")

        # Failsafe: Pack tabview AFTER buttons to prevent container-stretch overlapping
        self.tabview.pack(fill="both", expand=True, padx=15, pady=(10, 5))

    # Removed _browse_master

    def _load_current_values(self):
        prefs = self.prefs_manager.get_all()

        # General
        default_tab = prefs.get("default_tab", "OAS to Excel") # Typo in defaults? No, stored as label
        if default_tab in self.TAB_OPTIONS: self.cbo_tab.set(default_tab)
        
        sort_order = prefs.get("file_sort_order", "alphabetical")
        for display, value in self.SORT_OPTIONS:
            if value == sort_order:
                self.cbo_sort.set(display)
                break
        
        self.var_remember.set(self.prefs_manager.get("remember_paths", False))
        if prefs.get("remember_window_pos", True): self.chk_window_pos.select()

        # OAS Generation
        if prefs.get("gen_oas_30", True): self.chk_oas30.select()
        if prefs.get("gen_oas_31", True): self.chk_oas31.select()
        if prefs.get("gen_oas_swift", False): self.chk_swift.select()

        # Excel Generation
        if prefs.get("excel_gen_attr_diff", True): self.chk_excel_attr_diff.select()
        else: self.chk_excel_attr_diff.deselect()
        if prefs.get("excel_gen_line_diff", False): self.chk_excel_line_diff.select()
        else: self.chk_excel_line_diff.deselect()

        # Validation
        engine = prefs.get("linter_engine", "spectral").capitalize()
        if engine in ["Spectral", "Vacuum"]: self.cbo_linter_engine.set(engine)
        if prefs.get("ignore_bad_request", True): self.chk_ignore_br.select()

        # View
        theme = prefs.get("yaml_theme", "oas-dark")
        if theme in self.THEMES: self.cbo_theme.set(theme)
        self.cbo_font.set(prefs.get("yaml_font", "Consolas"))
        self.slider_font.set(prefs.get("yaml_font_size", 12))
        self.lbl_font_val.configure(text=str(prefs.get("yaml_font_size", 12)))
        if prefs.get("doc_snap_default_enabled", True): self.chk_snap_default.select()
        if prefs.get("yaml_word_wrap", True):
            self.chk_word_wrap.select()
        else:
            self.chk_word_wrap.deselect()

        # Logs
        self.cbo_gen_log_theme.set(prefs.get("gen_log_theme", "Light"))
        self.cbo_import_log_theme.set(prefs.get("import_log_theme", "Light")) # New
        self.cbo_app_log_theme.set(prefs.get("app_log_theme", "Dark"))
        self.cbo_spectral_log_theme.set(prefs.get("spectral_log_theme", "Light"))

        # Tools
        self.var_legacy_tracing.set(prefs.get("tools_legacy_tracing_enabled", True))
        self.var_legacy_collision_desc.set(prefs.get("tools_legacy_collision_include_descriptions", False))
        self.var_legacy_collision_examples.set(prefs.get("tools_legacy_collision_include_examples", False))
        self.var_legacy_capitalize_schemas.set(prefs.get("tools_legacy_capitalize_schema_names", True))


        # OAS Comparison
        self.entry_tmpl_syn.delete(0, "end")
        self.entry_tmpl_syn.insert(0, prefs.get("diff_template_synthesis", ""))
        self.entry_tmpl_ana.delete(0, "end")
        self.entry_tmpl_ana.insert(0, prefs.get("diff_template_analytical", ""))
        
        # We need loaded entries for Impact/Compatibility too:
        if not hasattr(self, 'entry_tmpl_imp'): return # Safety catch if UI building skipped
        self.entry_tmpl_imp.delete(0, "end")
        self.entry_tmpl_imp.insert(0, prefs.get("diff_template_impact", ""))
        self.entry_tmpl_comp.delete(0, "end")
        self.entry_tmpl_comp.insert(0, prefs.get("diff_template_compatibility", ""))


            
        self.current_diff_vars = prefs.get("diff_static_variables", {}).copy()
        self._refresh_vars_list()


    def _refresh_vars_list(self):
        """Rebuilds the static variables list UI."""
        for child in self.scroll_vars.winfo_children():
            child.destroy()
            
        for i, (key, value) in enumerate(self.current_diff_vars.items()):
            row = ctk.CTkFrame(self.scroll_vars, fg_color="transparent")
            row.pack(fill="x", pady=1)
            
            ctk.CTkLabel(row, text=key, width=120, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=5)
            # Display value truncated if too long
            disp_val = (value[:30] + '...') if len(value) > 30 else value
            ctk.CTkLabel(row, text=disp_val, anchor="w").pack(side="left", padx=5, fill="x", expand=True)
            
            ctk.CTkButton(row, text="X", width=25, height=20, fg_color="#D04040", hover_color="#B03030",
                          command=lambda k=key: self._on_delete_var(k)).pack(side="right", padx=2)
            ctk.CTkButton(row, text="Edit", width=40, height=20, fg_color="#0A809E", hover_color="#076075",
                          command=lambda k=key, v=value: self._on_edit_var(k, v)).pack(side="right", padx=2)

    def _on_add_var(self):

        dialog = ctk.CTkInputDialog(text="Enter variable name:", title="Add Variable")
        name = dialog.get_input()
        if name:
            name = name.strip()
            if name in self.current_diff_vars:
                return # Already exists
            dialog_val = ctk.CTkInputDialog(text=f"Enter value for '{name}':", title="Variable Value")
            val = dialog_val.get_input()
            if val is not None:
                self.current_diff_vars[name] = val
                self._refresh_vars_list()

    def _on_edit_var(self, key, old_val):
        dialog = ctk.CTkInputDialog(text=f"Change value for '{key}':", title="Edit Variable")
        # Pre-filling would be nice but CTkInputDialog doesn't support it easily in this version?
        # Actually, let's just use it and user can re-type or we implement a custom one later.
        val = dialog.get_input()
        if val is not None:
            self.current_diff_vars[key] = val
            self._refresh_vars_list()

    def _on_delete_var(self, key):
        if key in self.current_diff_vars:
            del self.current_diff_vars[key]
            self._refresh_vars_list()

    def _on_clear_vars(self):
        self.current_diff_vars = {}
        self._refresh_vars_list()

    def _browse_template(self, type_key):
        entry_map = {
            "syn": self.entry_tmpl_syn,
            "ana": self.entry_tmpl_ana,
            "imp": self.entry_tmpl_imp,
            "comp": self.entry_tmpl_comp
        }
        entry = entry_map.get(type_key)
        current = entry.get() if entry else ""
        initial = os.path.dirname(current) if current and os.path.exists(current) else None
        
        path = filedialog.askopenfilename(parent=self, initialdir=initial, filetypes=[("Word Documents", "*.docx")])
        if path:
            if type_key == "syn":
                self.entry_tmpl_syn.delete(0, "end")
                self.entry_tmpl_syn.insert(0, path)
            elif type_key == "ana":
                self.entry_tmpl_ana.delete(0, "end")
                self.entry_tmpl_ana.insert(0, path)
            elif type_key == "imp":
                self.entry_tmpl_imp.delete(0, "end")
                self.entry_tmpl_imp.insert(0, path)
            elif type_key == "comp":
                self.entry_tmpl_comp.delete(0, "end")
                self.entry_tmpl_comp.insert(0, path)




    def save_preferences(self):
        """Save values to manager and close."""
        sort_display = self.cbo_sort.get()
        sort_value = "alphabetical"
        for display, value in self.SORT_OPTIONS:
            if display == sort_display:
                sort_value = value
                break

        new_prefs = {
            # General
            "default_tab": self.cbo_tab.get(),
            "file_sort_order": sort_value,
            "remember_paths": self.var_remember.get(),
            "remember_window_pos": bool(self.chk_window_pos.get()),
            
            # OAS Generation
            "gen_oas_30": bool(self.chk_oas30.get()),
            "gen_oas_31": bool(self.chk_oas31.get()),
            "gen_oas_swift": bool(self.chk_swift.get()),
            
            # Excel Generation
            "excel_gen_attr_diff": bool(self.chk_excel_attr_diff.get()),
            "excel_gen_line_diff": bool(self.chk_excel_line_diff.get()),
            
            # Validation
            "linter_engine": self.cbo_linter_engine.get().lower(),
            "ignore_bad_request": bool(self.chk_ignore_br.get()),
            
            # View
            "yaml_theme": self.cbo_theme.get(),
            "yaml_font": self.cbo_font.get(),
            "yaml_font_size": int(self.slider_font.get()),
            "doc_snap_default_enabled": bool(self.chk_snap_default.get()),
            "yaml_word_wrap": bool(self.chk_word_wrap.get()),
            
            # Logs
            "gen_log_theme": self.cbo_gen_log_theme.get(),
            "import_log_theme": self.cbo_import_log_theme.get(), # New
            "app_log_theme": self.cbo_app_log_theme.get(),
            "spectral_log_theme": self.cbo_spectral_log_theme.get(),
            
            # Tools
            "tools_legacy_capitalize_schema_names": self.var_legacy_capitalize_schemas.get(),
            
            # OAS Comparison
            "diff_template_synthesis": self.entry_tmpl_syn.get(),
            "diff_template_analytical": self.entry_tmpl_ana.get(),
            "diff_template_impact": self.entry_tmpl_imp.get(),
            "diff_template_compatibility": self.entry_tmpl_comp.get(),

            "diff_debug_mode": False,
            "diff_static_variables": self.current_diff_vars,
        }
        
        self.prefs_manager.update(new_prefs)
        self.prefs_manager.save()
        
        if self.on_save_callback:
            try:
                self.on_save_callback(new_prefs)
            except Exception as e:
                print(f"Error applying preferences: {e}")
                # We still destroy the window, or maybe show an error?
                # For now, let's allow closing to avoid 'stuck' UI, but logging is critical.

        self.result = True
        self.destroy()

    def _on_save(self):
        self.save_preferences()

    def _on_cancel(self):
        self.result = False
        self.destroy()

    def _on_reset(self):
        """Reset UI to default values."""
        self.cbo_tab.set("OAS Generation")
        self.cbo_sort.set("Alphabetical")
        self.var_remember.set(False)
        self.chk_window_pos.select()
        
        self.chk_oas30.select()
        self.chk_oas31.select()
        self.chk_swift.deselect()

        self.chk_excel_attr_diff.select()
        self.chk_excel_line_diff.deselect()
        
        self.chk_ignore_br.select()
        self.cbo_linter_engine.set("Spectral")
        
        self.cbo_theme.set("oas-dark")
        self.cbo_font.set("Consolas")
        self.slider_font.set(12)
        self.lbl_font_val.configure(text="12")
        self.chk_snap_default.select()
        
        self.cbo_gen_log_theme.set("Light")
        self.cbo_import_log_theme.set("Light")
        self.cbo_app_log_theme.set("Dark")
        self.cbo_spectral_log_theme.set("Light")

        self.var_legacy_tracing.set(True)
        self.var_legacy_collision_desc.set(False)
        self.var_legacy_collision_examples.set(False)
