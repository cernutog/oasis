"""
Preferences Dialog for OAS Generation Tool.
Modal dialog for configuring application settings.
"""

import customtkinter as ctk
from tkinter import filedialog
import os
import sys
from copy import deepcopy

try:
    from .preferences import DEFAULT_GENERATION_MODE, GENERATION_MODES, PreferencesManager, normalize_generation_mode
    from .swift_services import normalize_swift_services
except ImportError:
    from preferences import DEFAULT_GENERATION_MODE, GENERATION_MODES, PreferencesManager, normalize_generation_mode
    from swift_services import normalize_swift_services


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class AutoHideScrollableFrame(ctk.CTkScrollableFrame):
    """Scrollable frame that shows its scrollbar only when content overflows."""

    def _create_grid(self):
        super()._create_grid()
        if hasattr(self, "_scrollbar"):
            self._scrollbar_grid_info = self._scrollbar.grid_info()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._scrollbar_grid_info = self._scrollbar.grid_info()
        if self._orientation == "vertical":
            self._parent_canvas.configure(yscrollcommand=self._set_vertical_scrollbar)
        elif self._orientation == "horizontal":
            self._parent_canvas.configure(xscrollcommand=self._set_horizontal_scrollbar)
        self.bind("<Configure>", self._on_autohide_configure, add="+")
        self._parent_canvas.bind("<Configure>", self._on_autohide_configure, add="+")
        self.after_idle(self._update_scrollbar_visibility)

    def _set_vertical_scrollbar(self, first, last):
        self._scrollbar.set(first, last)
        self._toggle_scrollbar(float(first) > 0.0 or float(last) < 1.0)

    def _set_horizontal_scrollbar(self, first, last):
        self._scrollbar.set(first, last)
        self._toggle_scrollbar(float(first) > 0.0 or float(last) < 1.0)

    def _toggle_scrollbar(self, should_show):
        if should_show:
            if not self._scrollbar.winfo_ismapped():
                self._scrollbar.grid(**self._scrollbar_grid_info)
        else:
            if self._scrollbar.winfo_ismapped():
                self._scrollbar.grid_remove()

    def _on_autohide_configure(self, _event=None):
        self.after_idle(self._update_scrollbar_visibility)

    def _update_scrollbar_visibility(self):
        self._parent_canvas.configure(scrollregion=self._parent_canvas.bbox("all"))
        first, last = self._parent_canvas.yview() if self._orientation == "vertical" else self._parent_canvas.xview()
        self._toggle_scrollbar(first > 0.0 or last < 1.0)

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
        
        # Set window icon AFTER CTkToplevel's internal 200ms default icon setting
        self.after(250, self._set_icon)
        
        self._build_ui(message)
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)

    def _set_icon(self):
        try:
            icon_file = resource_path("icon.ico")
            if os.path.exists(icon_file):
                self.iconbitmap(icon_file)
                self.wm_iconbitmap(icon_file)
        except (OSError, FileNotFoundError, Exception):
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
    DESIGNER_TAB_OPTION = "Designer"
    SWIFT_COLUMN_DEFAULTS = {"service": 90, "url": 300, "description": 180}
    SWIFT_COLUMN_MIN_WIDTHS = {"service": 75, "url": 240, "description": 150}
    SWIFT_COLUMN_MAX_TOTAL = 570

    def __init__(self, parent, prefs_manager, on_save_callback=None):
        super().__init__(parent)

        self.prefs_manager = prefs_manager
        self.on_save_callback = on_save_callback
        self.result = None  # Will be True if saved, False/None if cancelled
        self.swift_column_widths = dict(self.SWIFT_COLUMN_DEFAULTS)
        self.swift_column_widgets = []
        if hasattr(self.prefs_manager, "load"):
            self.prefs_manager.load()

        # Window setup
        self.title("Preferences")
        dialog_width = 780
        dialog_height = 640
        self.geometry(f"{dialog_width}x{dialog_height}")
        self.minsize(720, 560)
        self.resizable(True, True) 

        # Non-modal: only transient
        self.transient(parent)

        # Center on parent
        self.update_idletasks()
        try:
            x = parent.winfo_x() + (parent.winfo_width() - dialog_width) // 2
            y = parent.winfo_y() + (parent.winfo_height() - dialog_height) // 2
            self.geometry(f"{dialog_width}x{dialog_height}+{int(x)}+{int(y)}")

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

        self.var_enable_designer = ctk.BooleanVar(value=False)
        self.chk_enable_designer = ctk.CTkSwitch(
            self.tab_gen,
            text="Enable API Designer (experimental)",
            variable=self.var_enable_designer,
            progress_color="#0A809E",
            command=self._on_enable_designer_toggle,
        )
        self.chk_enable_designer.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=10)

        self.var_update_check = ctk.BooleanVar(value=True)
        self.chk_update_check = ctk.CTkSwitch(
            self.tab_gen,
            text="Check for updates at startup",
            variable=self.var_update_check,
            progress_color="#0A809E",
        )
        self.chk_update_check.grid(row=5, column=0, columnspan=2, sticky="w", padx=10, pady=(22, 10))
        self.tab_gen.grid_columnconfigure(1, weight=1)


        # === 2. OAS GENERATION TAB ===
        self.chk_oas31 = ctk.CTkSwitch(self.tab_output, text="OAS 3.1", progress_color="#0A809E")
        self.chk_oas31.pack(anchor="w", padx=20, pady=(20, 10))

        self.chk_oas30 = ctk.CTkSwitch(self.tab_output, text="OAS 3.0", progress_color="#0A809E")
        self.chk_oas30.pack(anchor="w", padx=20, pady=10)

        self.chk_swift = ctk.CTkSwitch(self.tab_output, text="OAS SWIFT", progress_color="#0A809E")
        self.chk_swift.pack(anchor="w", padx=20, pady=10)

        self.frame_generation_mode = ctk.CTkFrame(self.tab_output, fg_color="transparent")
        self.frame_generation_mode.pack(fill="x", padx=20, pady=(18, 10))
        ctk.CTkLabel(self.frame_generation_mode, text="Mode:", width=38, anchor="w").pack(side="left")
        self.cbo_generation_mode = ctk.CTkComboBox(
            self.frame_generation_mode,
            values=list(GENERATION_MODES),
            width=190,
            button_color="#0A809E",
        )
        self.cbo_generation_mode.pack(side="left", fill="x", expand=False)

        self._add_section_separator(self.tab_output, "Info Extensions")
        self.frame_x_info = ctk.CTkFrame(self.tab_output, fg_color="transparent")
        self.frame_x_info.pack(fill="x", padx=20, pady=(2, 8))
        self.frame_x_info.grid_columnconfigure(0, weight=1)
        self.frame_x_info.grid_columnconfigure(1, weight=1)
        self.chk_x_info_creation_date = ctk.CTkSwitch(
            self.frame_x_info,
            text="x-info-creation-date",
            progress_color="#0A809E",
        )
        self.chk_x_info_creation_date.grid(row=0, column=0, sticky="w", pady=6)
        self.chk_x_info_release = ctk.CTkSwitch(
            self.frame_x_info,
            text="x-info-release",
            progress_color="#0A809E",
        )
        self.chk_x_info_release.grid(row=1, column=0, sticky="w", pady=6)
        self.chk_x_info_customization = ctk.CTkSwitch(
            self.frame_x_info,
            text="x-info-customization",
            progress_color="#0A809E",
        )
        self.chk_x_info_customization.grid(row=0, column=1, sticky="w", pady=6)
        self.chk_x_info_oasis_version = ctk.CTkSwitch(
            self.frame_x_info,
            text="x-info-oasis-version",
            progress_color="#0A809E",
        )
        self.chk_x_info_oasis_version.grid(row=1, column=1, sticky="w", pady=6)

        # === 3. TEMPLATES TAB (merged Excel Generation + Tools) ===
        self.tab_templates.grid_columnconfigure(0, weight=1)
        self.tab_templates.grid_rowconfigure(0, weight=1)

        self.templates_tabview = ctk.CTkTabview(
            self.tab_templates,
            fg_color="transparent",
            segmented_button_selected_color="#0A809E",
            segmented_button_selected_hover_color="#076075",
        )
        self.templates_tabview.grid(row=0, column=0, sticky="nsew", padx=6, pady=0)
        self.tab_templates_general = self.templates_tabview.add("General")
        self.tab_templates_swift = self.templates_tabview.add("SWIFT Servers")
        self.tab_templates_general.grid_columnconfigure(0, weight=1)
        self.tab_templates_swift.grid_columnconfigure(0, weight=1)
        self.tab_templates_swift.grid_rowconfigure(0, weight=1)

        self.scroll_templates_general = AutoHideScrollableFrame(
            self.tab_templates_general,
            fg_color="transparent",
        )
        self.scroll_templates_general.pack(fill="both", expand=True, padx=0, pady=0)

        self._build_swift_servers_preferences_tab()

        # --- Section: Create Template from OAS ---
        self._add_section_separator(self.scroll_templates_general, "Create Template from OAS")

        self.chk_excel_attr_diff = ctk.CTkSwitch(self.scroll_templates_general, text="Attribute Diff", progress_color="#0A809E")
        self.chk_excel_attr_diff.pack(anchor="w", padx=20, pady=(3, 6))

        self.chk_excel_line_diff = ctk.CTkSwitch(self.scroll_templates_general, text="Line Diff", progress_color="#0A809E")
        self.chk_excel_line_diff.pack(anchor="w", padx=20, pady=(3, 6))

        # --- Section: Legacy Tools ---
        self._add_section_separator(self.scroll_templates_general, "Legacy Tools")
        self.frame_legacy_switches = ctk.CTkFrame(self.scroll_templates_general, fg_color="transparent")
        self.frame_legacy_switches.pack(fill="x", padx=20, pady=(0, 4))
        self.frame_legacy_switches.grid_columnconfigure(0, weight=1)
        self.frame_legacy_switches.grid_columnconfigure(1, weight=1)
        self.frame_legacy_switches_left = ctk.CTkFrame(self.frame_legacy_switches, fg_color="transparent")
        self.frame_legacy_switches_left.grid(row=0, column=0, sticky="nw")
        self.frame_legacy_switches_right = ctk.CTkFrame(self.frame_legacy_switches, fg_color="transparent")
        self.frame_legacy_switches_right.grid(row=0, column=1, sticky="nw", padx=(35, 0))

        self.var_legacy_tracing = ctk.BooleanVar(value=True)
        self.chk_legacy_tracing = ctk.CTkSwitch(
            self.frame_legacy_switches_left,
            text="Enable Schema Tracing by default",
            variable=self.var_legacy_tracing,
            progress_color="#0A809E"
        )
        self.chk_legacy_tracing.pack(anchor="w", pady=(3, 6))

        self.var_legacy_collision_desc = ctk.BooleanVar(value=False)
        self.chk_legacy_collision_desc = ctk.CTkSwitch(
            self.frame_legacy_switches_left,
            text="Include descriptions in collision detection",
            variable=self.var_legacy_collision_desc,
            progress_color="#0A809E",
        )
        self.chk_legacy_collision_desc.pack(anchor="w", pady=(3, 6))

        self.var_legacy_collision_examples = ctk.BooleanVar(value=False)
        self.chk_legacy_collision_examples = ctk.CTkSwitch(
            self.frame_legacy_switches_left,
            text="Include examples in collision detection",
            variable=self.var_legacy_collision_examples,
            progress_color="#0A809E",
        )
        self.chk_legacy_collision_examples.pack(anchor="w", pady=(3, 6))

        self.var_legacy_capitalize_schemas = ctk.BooleanVar(value=True)
        self.chk_legacy_capitalize_schemas = ctk.CTkSwitch(
            self.frame_legacy_switches_left,
            text="Capitalize wrapper names (PascalCase)",
            variable=self.var_legacy_capitalize_schemas,
            progress_color="#0A809E",
        )
        self.chk_legacy_capitalize_schemas.pack(anchor="w", pady=(3, 6))

        self.var_legacy_fill_fix_examples = ctk.BooleanVar(value=True)
        self.chk_legacy_fill_fix_examples = ctk.CTkSwitch(
            self.frame_legacy_switches_right,
            text="Repair and complete examples",
            variable=self.var_legacy_fill_fix_examples,
            progress_color="#0A809E",
        )
        self.chk_legacy_fill_fix_examples.pack(anchor="w", pady=(3, 6))

        self.var_legacy_example_tracing = ctk.BooleanVar(value=True)
        self.chk_legacy_example_tracing = ctk.CTkSwitch(
            self.frame_legacy_switches_right,
            text="Enable Example Tracing",
            variable=self.var_legacy_example_tracing,
            progress_color="#0A809E",
        )
        self.chk_legacy_example_tracing.pack(anchor="w", pady=(3, 6))

        self.frame_legacy_metadata = ctk.CTkFrame(self.scroll_templates_general, fg_color="transparent")
        self.frame_legacy_metadata.pack(fill="x", padx=20, pady=(8, 4))
        self.frame_legacy_metadata.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.frame_legacy_metadata, text="Contact name:", width=105, anchor="w").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=3)
        self.entry_legacy_contact_name = ctk.CTkEntry(self.frame_legacy_metadata)
        self.entry_legacy_contact_name.grid(row=0, column=1, sticky="ew", pady=3)

        ctk.CTkLabel(self.frame_legacy_metadata, text="Release:", width=105, anchor="w").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=3)
        self.entry_legacy_release = ctk.CTkEntry(self.frame_legacy_metadata)
        self.entry_legacy_release.grid(row=1, column=1, sticky="ew", pady=3)

        ctk.CTkLabel(self.frame_legacy_metadata, text="Contact URL:", width=105, anchor="w").grid(row=2, column=0, sticky="w", padx=(0, 8), pady=3)
        self.entry_legacy_contact_url = ctk.CTkEntry(self.frame_legacy_metadata)
        self.entry_legacy_contact_url.grid(row=2, column=1, sticky="ew", pady=3)

        ctk.CTkLabel(self.frame_legacy_metadata, text="Filename pattern:", width=105, anchor="w").grid(row=3, column=0, sticky="w", padx=(0, 8), pady=3)
        self.entry_legacy_filename_pattern = ctk.CTkEntry(self.frame_legacy_metadata)
        self.entry_legacy_filename_pattern.grid(row=3, column=1, sticky="ew", pady=3)


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

        frame_val_font = ctk.CTkFrame(self.tab_val, fg_color="transparent")
        frame_val_font.pack(anchor="w", padx=20, pady=(0, 20))
        ctk.CTkLabel(frame_val_font, text="Issues Font Size:").pack(side="left", padx=(0, 10))
        self.slider_validation_font = ctk.CTkSlider(
            frame_val_font,
            from_=8,
            to=24,
            number_of_steps=16,
            width=150,
            button_color="#0A809E",
            progress_color="#0A809E",
            button_hover_color="#076075",
        )
        self.slider_validation_font.pack(side="left")
        self.lbl_validation_font_val = ctk.CTkLabel(frame_val_font, text="11", width=30)
        self.lbl_validation_font_val.pack(side="left", padx=(5, 0))
        self.slider_validation_font.configure(
            command=lambda v: self.lbl_validation_font_val.configure(text=str(int(v)))
        )


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
        
        self.slider_font = ctk.CTkSlider(
            self.frame_font,
            from_=8,
            to=24,
            number_of_steps=16,
            width=150,
            button_color="#0A809E",
            progress_color="#0A809E",
            button_hover_color="#076075",
        )
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
        self.tab_diff.grid_rowconfigure(0, weight=1)

        self.diff_tabview = ctk.CTkTabview(
            self.tab_diff,
            fg_color="transparent",
            segmented_button_selected_color="#0A809E",
            segmented_button_selected_hover_color="#076075",
        )
        self.diff_tabview.grid(row=0, column=0, sticky="nsew", padx=6, pady=0)

        self.diff_tab_general = self.diff_tabview.add("General")
        self.diff_tab_synthesis = self.diff_tabview.add("Synthesis")
        self.diff_tab_analytical = self.diff_tabview.add("Analytical")
        self.diff_tab_impact = self.diff_tabview.add("Impact")
        self.diff_tab_interface = self.diff_tabview.add("Interface")

        for tab in (
            self.diff_tab_general,
            self.diff_tab_synthesis,
            self.diff_tab_analytical,
            self.diff_tab_impact,
            self.diff_tab_interface,
        ):
            tab.grid_columnconfigure(0, weight=1)

        self._add_section_separator(self.diff_tab_general, "Static Variables (User Defined)")
        
        help_lbl = ctk.CTkLabel(self.diff_tab_general,
                                text="Use placeholders like {{variable_name}} in custom Word templates to inject these values.",
                                font=ctk.CTkFont(size=12, slant="italic"),
                                text_color="#333333")
        help_lbl.pack(anchor="w", padx=20, pady=(0, 3))

        self.frame_vars = ctk.CTkFrame(self.diff_tab_general, fg_color="transparent", height=170)
        self.frame_vars.pack(fill="x", padx=10, pady=(0, 5))
        
        self.scroll_vars = ctk.CTkFrame(self.frame_vars, fg_color="transparent")
        self.scroll_vars.pack(fill="x", expand=False, pady=(0, 5))

        self.vars_controls = ctk.CTkFrame(self.frame_vars, fg_color="transparent")
        self.vars_controls.pack(fill="x", expand=False)

        
        ctk.CTkButton(self.vars_controls, text="Add Variable", width=100, fg_color="#0A809E", hover_color="#076075", command=self._on_add_var).pack(side="left", padx=(0, 5))
        ctk.CTkButton(self.vars_controls, text="Clear All", width=100, fg_color="#D04040", hover_color="#B03030", command=self._on_clear_vars).pack(side="left")

        def _add_report_template_tab(tab, label, attr_name, browse_key):
            self._add_section_separator(tab, "Custom Template")
            frame = ctk.CTkFrame(tab, fg_color="transparent")
            frame.pack(fill="x", padx=10, pady=(8, 5))
            frame.grid_columnconfigure(1, weight=1)
            ctk.CTkLabel(frame, text=f"{label}:", width=95, anchor="w").grid(row=0, column=0, sticky="w", padx=(5, 5))
            entry = ctk.CTkEntry(frame)
            entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
            setattr(self, attr_name, entry)
            ctk.CTkButton(
                frame,
                text="...",
                width=30,
                fg_color="#0A809E",
                hover_color="#076075",
                command=lambda: self._browse_template(browse_key),
            ).grid(row=0, column=2)

        _add_report_template_tab(self.diff_tab_synthesis, "Synthesis", "entry_tmpl_syn", "syn")
        _add_report_template_tab(self.diff_tab_analytical, "Analytical", "entry_tmpl_ana", "ana")
        _add_report_template_tab(self.diff_tab_impact, "Impact", "entry_tmpl_imp", "imp")
        _add_report_template_tab(self.diff_tab_interface, "Interface", "entry_tmpl_comp", "comp")

        self._add_section_separator(self.diff_tab_interface, "Interface Filters")
        self.var_diff_show_enum_order_changes = ctk.BooleanVar(value=False)
        self.chk_diff_show_enum_order_changes = ctk.CTkSwitch(
            self.diff_tab_interface,
            text="Show enum order changes",
            variable=self.var_diff_show_enum_order_changes,
            progress_color="#0A809E",
        )
        self.chk_diff_show_enum_order_changes.pack(anchor="w", padx=20, pady=(8, 6))

        self.var_diff_show_validation_rule_only_description_changes = ctk.BooleanVar(value=True)
        self.chk_diff_show_validation_rule_only_description_changes = ctk.CTkSwitch(
            self.diff_tab_interface,
            text="Show description changes caused only by added validation rules",
            variable=self.var_diff_show_validation_rule_only_description_changes,
            progress_color="#0A809E",
        )
        self.chk_diff_show_validation_rule_only_description_changes.pack(anchor="w", padx=20, pady=(3, 6))






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

        self.btn_reset_defaults = ctk.CTkButton(
            self.frame_buttons,
            text="Reset to Defaults",
            width=130,
            fg_color=("#D04040", "#B03030"),
            hover_color=("#B03030", "#902020"),
            command=self._on_reset,
        )
        self.btn_reset_defaults.pack(side="left")

        self.btn_reset_current_section = ctk.CTkButton(
            self.frame_buttons,
            text="Reset Current Section",
            width=165,
            fg_color=("#D04040", "#B03030"),
            hover_color=("#B03030", "#902020"),
            command=self._on_reset_current_section,
        )
        self.btn_reset_current_section.pack(side="left", padx=(10, 0))

        self.btn_cancel = ctk.CTkButton(
            self.frame_buttons,
            text="Cancel",
            width=100,
            fg_color="#0A809E",
            hover_color="#076075",
            command=self._on_cancel,
        )
        self.btn_cancel.pack(side="right", padx=(10, 0))

        self.btn_apply_close = ctk.CTkButton(
            self.frame_buttons,
            text="Apply & Close",
            width=120,
            fg_color="#0A809E",
            hover_color="#076075",
            command=self._on_save,
        )
        self.btn_apply_close.pack(side="right")

        # Failsafe: Pack tabview AFTER buttons to prevent container-stretch overlapping
        self.tabview.pack(fill="both", expand=True, padx=15, pady=(10, 5))

    def _build_swift_servers_preferences_tab(self):
        self.swift_server_rows = []
        self.swift_server_add_frame = None
        self.btn_add_swift_server = None

        self.swift_header = ctk.CTkFrame(self.tab_templates_swift, fg_color="transparent")
        self.swift_header.pack(fill="x", padx=(18, 12), pady=(14, 4))
        self.swift_header_service = ctk.CTkLabel(
            self.swift_header,
            text="Service",
            anchor="w",
            font=ctk.CTkFont(weight="bold"),
        )
        self.swift_header_url = ctk.CTkLabel(
            self.swift_header,
            text="URL",
            anchor="w",
            font=ctk.CTkFont(weight="bold"),
        )
        self.swift_header_description = ctk.CTkLabel(
            self.swift_header,
            text="Description",
            anchor="w",
            font=ctk.CTkFont(weight="bold"),
        )
        self.swift_handle_service_url = self._create_swift_column_handle(self.swift_header, "service_url")
        self.swift_handle_url_description = self._create_swift_column_handle(self.swift_header, "url_description")
        self._configure_swift_columns(self.swift_header)
        self.swift_header_service.grid(row=0, column=0, sticky="ew", padx=(0, 4))
        self.swift_handle_service_url.grid(row=0, column=1, padx=(0, 4), pady=5)
        self.swift_header_url.grid(row=0, column=2, sticky="ew", padx=(0, 4))
        self.swift_handle_url_description.grid(row=0, column=3, padx=(0, 4), pady=5)
        self.swift_header_description.grid(row=0, column=4, sticky="ew", padx=(0, 4))

        self.scroll_swift_servers = AutoHideScrollableFrame(self.tab_templates_swift, height=340)
        self.scroll_swift_servers.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.swift_rows_container = ctk.CTkFrame(self.scroll_swift_servers, fg_color="transparent")
        self.swift_rows_container.pack(fill="x")
        self._configure_swift_columns(self.swift_rows_container)
        self.swift_grid_row = 0

    # Removed _browse_master

    def _load_current_values(self):
        prefs = self.prefs_manager.get_all()

        # General
        self.var_enable_designer.set(bool(prefs.get("enable_api_designer", False)))
        self._refresh_default_tab_options()
        default_tab = prefs.get("default_tab", "OAS Generation")
        if default_tab in self._current_tab_options():
            self.cbo_tab.set(default_tab)
        else:
            self.cbo_tab.set("OAS Generation")
        
        sort_order = prefs.get("file_sort_order", "alphabetical")
        for display, value in self.SORT_OPTIONS:
            if value == sort_order:
                self.cbo_sort.set(display)
                break
        
        self.var_remember.set(self.prefs_manager.get("remember_paths", False))
        if prefs.get("remember_window_pos", True): self.chk_window_pos.select()
        self.var_update_check.set(bool(prefs.get("update_check_enabled", True)))

        # OAS Generation
        if prefs.get("gen_oas_30", True): self.chk_oas30.select()
        if prefs.get("gen_oas_31", True): self.chk_oas31.select()
        if prefs.get("gen_oas_swift", False): self.chk_swift.select()
        self.cbo_generation_mode.set(normalize_generation_mode(prefs.get("generation_mode", DEFAULT_GENERATION_MODE)))
        if prefs.get("gen_x_info_creation_date", True): self.chk_x_info_creation_date.select()
        else: self.chk_x_info_creation_date.deselect()
        if prefs.get("gen_x_info_release", True): self.chk_x_info_release.select()
        else: self.chk_x_info_release.deselect()
        if prefs.get("gen_x_info_customization", True): self.chk_x_info_customization.select()
        else: self.chk_x_info_customization.deselect()
        if prefs.get("gen_x_info_oasis_version", True): self.chk_x_info_oasis_version.select()
        else: self.chk_x_info_oasis_version.deselect()
        self.swift_column_widths = self._sanitize_swift_column_widths(
            prefs.get("swift_servers_column_widths", self.SWIFT_COLUMN_DEFAULTS)
        )
        self._apply_swift_column_widths()
        self._load_swift_server_rows(prefs.get("swift_services", {}))

        # Excel Generation
        if prefs.get("excel_gen_attr_diff", True): self.chk_excel_attr_diff.select()
        else: self.chk_excel_attr_diff.deselect()
        if prefs.get("excel_gen_line_diff", False): self.chk_excel_line_diff.select()
        else: self.chk_excel_line_diff.deselect()

        # Validation
        engine = prefs.get("linter_engine", "spectral").capitalize()
        if engine in ["Spectral", "Vacuum"]: self.cbo_linter_engine.set(engine)
        if prefs.get("ignore_bad_request", True): self.chk_ignore_br.select()
        else: self.chk_ignore_br.deselect()
        self.slider_validation_font.set(prefs.get("validation_font_size", 11))
        self.lbl_validation_font_val.configure(text=str(prefs.get("validation_font_size", 11)))

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
        self.var_legacy_fill_fix_examples.set(prefs.get("tools_legacy_fill_fix_examples", True))
        self.var_legacy_example_tracing.set(prefs.get("tools_legacy_example_tracing_enabled", True))
        self.entry_legacy_contact_name.delete(0, "end")
        self.entry_legacy_contact_name.insert(0, prefs.get("tools_legacy_contact_name", ""))
        self.entry_legacy_contact_url.delete(0, "end")
        self.entry_legacy_contact_url.insert(0, prefs.get("tools_legacy_contact_url", ""))
        self.entry_legacy_release.delete(0, "end")
        self.entry_legacy_release.insert(0, prefs.get("tools_legacy_release", ""))
        self.entry_legacy_filename_pattern.delete(0, "end")
        self.entry_legacy_filename_pattern.insert(0, prefs.get("tools_legacy_filename_pattern", ""))


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
        self.var_diff_show_enum_order_changes.set(prefs.get("diff_show_enum_order_changes", False))
        self.var_diff_show_validation_rule_only_description_changes.set(
            prefs.get("diff_show_validation_rule_only_description_changes", True)
        )


            
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

    def _load_swift_server_rows(self, services):
        for child in self.swift_rows_container.winfo_children():
            child.destroy()
        self.swift_server_rows = []
        self.swift_server_add_frame = None
        self.btn_add_swift_server = None
        self.swift_grid_row = 0
        self._configure_swift_columns(self.swift_rows_container)
        self.scroll_swift_servers._parent_canvas.yview_moveto(0)

        normalized = normalize_swift_services(services)
        for service_name, service in sorted(normalized.items()):
            servers = service.get("servers", [])
            if not servers:
                self._add_swift_server_row(service_name=service_name)
            for server in servers:
                self._add_swift_server_row(
                    service_name=service_name,
                    url=server.get("url", ""),
                    description=server.get("description", ""),
                )
        self._pack_swift_server_add_button()

    def _sanitize_swift_column_widths(self, widths):
        sanitized = dict(self.SWIFT_COLUMN_DEFAULTS)
        if isinstance(widths, dict):
            for key in sanitized:
                try:
                    sanitized[key] = int(widths.get(key, sanitized[key]))
                except (TypeError, ValueError):
                    pass
        for key, min_width in self.SWIFT_COLUMN_MIN_WIDTHS.items():
            sanitized[key] = max(min_width, sanitized[key])
        overflow = sum(sanitized.values()) - self.SWIFT_COLUMN_MAX_TOTAL
        for key in ("description", "url", "service"):
            if overflow <= 0:
                break
            reducible = sanitized[key] - self.SWIFT_COLUMN_MIN_WIDTHS[key]
            reduction = min(overflow, reducible)
            sanitized[key] -= reduction
            overflow -= reduction
        return sanitized

    def _configure_swift_columns(self, frame):
        frame.grid_columnconfigure(0, weight=0, minsize=self.swift_column_widths["service"])
        frame.grid_columnconfigure(1, weight=0, minsize=6)
        frame.grid_columnconfigure(2, weight=1, minsize=self.swift_column_widths["url"])
        frame.grid_columnconfigure(3, weight=0, minsize=6)
        frame.grid_columnconfigure(4, weight=0, minsize=self.swift_column_widths["description"])
        frame.grid_columnconfigure(5, weight=0, minsize=34)

    def _apply_swift_column_widths(self):
        if hasattr(self, "swift_header"):
            self._configure_swift_columns(self.swift_header)
            self.swift_header_service.configure(width=self.swift_column_widths["service"])
            self.swift_header_url.configure(width=self.swift_column_widths["url"])
            self.swift_header_description.configure(width=self.swift_column_widths["description"])
        if hasattr(self, "swift_rows_container"):
            self._configure_swift_columns(self.swift_rows_container)
        for row in self.swift_server_rows:
            row["service"].configure(width=self.swift_column_widths["service"])
            row["url"].configure(width=self.swift_column_widths["url"])
            row["description"].configure(width=self.swift_column_widths["description"])

    def _create_swift_column_handle(self, parent, handle_name):
        handle = ctk.CTkFrame(parent, width=4, height=18, fg_color="#9AA3AA")
        handle.configure(cursor="sb_h_double_arrow")
        handle.bind("<ButtonPress-1>", lambda event, name=handle_name: self._start_swift_column_resize(event, name))
        handle.bind("<B1-Motion>", self._drag_swift_column_resize)
        handle.bind("<ButtonRelease-1>", self._finish_swift_column_resize)
        return handle

    def _start_swift_column_resize(self, event, handle_name):
        self._swift_resize_state = {
            "handle": handle_name,
            "x": event.x_root,
            "widths": dict(self.swift_column_widths),
        }

    def _drag_swift_column_resize(self, event):
        state = getattr(self, "_swift_resize_state", None)
        if not state:
            return
        delta = event.x_root - state["x"]
        widths = dict(state["widths"])
        if state["handle"] == "service_url":
            left_key, right_key = "service", "url"
        else:
            left_key, right_key = "url", "description"
        left = max(self.SWIFT_COLUMN_MIN_WIDTHS[left_key], widths[left_key] + delta)
        right = max(self.SWIFT_COLUMN_MIN_WIDTHS[right_key], widths[right_key] - delta)
        total = widths[left_key] + widths[right_key]
        if left + right > total:
            if widths[left_key] + delta < self.SWIFT_COLUMN_MIN_WIDTHS[left_key]:
                left = self.SWIFT_COLUMN_MIN_WIDTHS[left_key]
                right = total - left
            else:
                right = self.SWIFT_COLUMN_MIN_WIDTHS[right_key]
                left = total - right
        widths[left_key] = left
        widths[right_key] = right
        self.swift_column_widths = self._sanitize_swift_column_widths(widths)
        self._apply_swift_column_widths()

    def _finish_swift_column_resize(self, _event):
        self._swift_resize_state = None

    def _pack_swift_server_add_button(self):
        if self.swift_server_add_frame is None:
            self.swift_server_add_frame = ctk.CTkFrame(self.swift_rows_container, fg_color="transparent", height=34)
            self.swift_server_add_frame.pack_propagate(False)
            self.btn_add_swift_server = ctk.CTkButton(
                self.swift_server_add_frame,
                text="Add",
                width=80,
                fg_color="#0A809E",
                hover_color="#076075",
                command=self._on_add_swift_server_row,
            )
            self.btn_add_swift_server.pack(side="left")
        else:
            self.swift_server_add_frame.grid_forget()
        self.swift_server_add_frame.grid(
            row=self.swift_grid_row,
            column=0,
            columnspan=6,
            sticky="ew",
            pady=(8, 2),
        )

    def _add_swift_server_row(self, service_name="", url="", description=""):
        if self.swift_server_add_frame is not None:
            self.swift_server_add_frame.grid_forget()
        row_index = self.swift_grid_row

        entry_service = ctk.CTkEntry(self.swift_rows_container, width=self.swift_column_widths["service"])
        entry_service.grid(row=row_index, column=0, sticky="ew", padx=(0, 4), pady=2)
        entry_service.insert(0, service_name)

        row_spacer_service_url = ctk.CTkFrame(self.swift_rows_container, width=4, height=28, fg_color="transparent")
        row_spacer_service_url.grid(row=row_index, column=1, sticky="ns", padx=(0, 4), pady=2)

        entry_url = ctk.CTkEntry(self.swift_rows_container, width=self.swift_column_widths["url"])
        entry_url.grid(row=row_index, column=2, sticky="ew", padx=(0, 4), pady=2)
        entry_url.insert(0, url)

        row_spacer_url_description = ctk.CTkFrame(self.swift_rows_container, width=4, height=28, fg_color="transparent")
        row_spacer_url_description.grid(row=row_index, column=3, sticky="ns", padx=(0, 4), pady=2)

        entry_description = ctk.CTkEntry(self.swift_rows_container, width=self.swift_column_widths["description"])
        entry_description.grid(row=row_index, column=4, sticky="ew", padx=(0, 4), pady=2)
        entry_description.insert(0, description)

        row_data = {
            "frame": entry_service,
            "service": entry_service,
            "url": entry_url,
            "description": entry_description,
            "spacer_service_url": row_spacer_service_url,
            "spacer_url_description": row_spacer_url_description,
        }
        delete_button = ctk.CTkButton(
            self.swift_rows_container,
            text="X",
            width=28,
            height=28,
            fg_color="#D04040",
            hover_color="#B03030",
            command=lambda data=row_data: self._on_delete_swift_server_row(data),
        )
        delete_button.grid(row=row_index, column=5, sticky="w", pady=2)
        row_data["delete"] = delete_button
        row_data["widgets"] = [
            entry_service,
            row_spacer_service_url,
            entry_url,
            row_spacer_url_description,
            entry_description,
            delete_button,
        ]
        self.swift_server_rows.append(row_data)
        self.swift_grid_row += 1
        self._pack_swift_server_add_button()

    def _on_add_swift_server_row(self):
        self._add_swift_server_row()

    def _on_delete_swift_server_row(self, row_data):
        if row_data in self.swift_server_rows:
            self.swift_server_rows.remove(row_data)
        for widget in row_data.get("widgets", []):
            widget.destroy()
        self._regrid_swift_server_rows()

    def _regrid_swift_server_rows(self):
        self.swift_grid_row = 0
        for row in self.swift_server_rows:
            row["service"].grid(row=self.swift_grid_row, column=0, sticky="ew", padx=(0, 4), pady=2)
            row["spacer_service_url"].grid(row=self.swift_grid_row, column=1, sticky="ns", padx=(0, 4), pady=2)
            row["url"].grid(row=self.swift_grid_row, column=2, sticky="ew", padx=(0, 4), pady=2)
            row["spacer_url_description"].grid(row=self.swift_grid_row, column=3, sticky="ns", padx=(0, 4), pady=2)
            row["description"].grid(row=self.swift_grid_row, column=4, sticky="ew", padx=(0, 4), pady=2)
            row["delete"].grid(row=self.swift_grid_row, column=5, sticky="w", pady=2)
            self.swift_grid_row += 1
        self._pack_swift_server_add_button()

    def _collect_swift_services_from_rows(self):
        services = {}
        for row in self.swift_server_rows:
            service_name = row["service"].get().strip()
            url = row["url"].get().strip()
            description = row["description"].get().strip()

            if not service_name and not url and not description:
                continue
            if not service_name:
                dialog = OASConfirmationDialog(
                    self,
                    "Invalid SWIFT Server",
                    "Every SWIFT server row with URL or Description must have a Service.",
                )
                self.wait_window(dialog)
                return None

            service = services.setdefault(service_name, {"servers": []})
            if url or description:
                service["servers"].append({"url": url, "description": description})

        return services

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
        swift_services = self._collect_swift_services_from_rows()
        if swift_services is None:
            return

        sort_display = self.cbo_sort.get()
        sort_value = "alphabetical"
        for display, value in self.SORT_OPTIONS:
            if display == sort_display:
                sort_value = value
                break

        enable_designer = bool(self.var_enable_designer.get())
        default_tab = self.cbo_tab.get()
        if default_tab == self.DESIGNER_TAB_OPTION and not enable_designer:
            default_tab = "OAS Generation"

        new_prefs = {
            # General
            "default_tab": default_tab,
            "enable_api_designer": enable_designer,
            "file_sort_order": sort_value,
            "remember_paths": self.var_remember.get(),
            "remember_window_pos": bool(self.chk_window_pos.get()),
            "update_check_enabled": bool(self.var_update_check.get()),
            
            # OAS Generation
            "gen_oas_30": bool(self.chk_oas30.get()),
            "gen_oas_31": bool(self.chk_oas31.get()),
            "gen_oas_swift": bool(self.chk_swift.get()),
            "generation_mode": normalize_generation_mode(self.cbo_generation_mode.get()),
            "gen_x_info_creation_date": bool(self.chk_x_info_creation_date.get()),
            "gen_x_info_release": bool(self.chk_x_info_release.get()),
            "gen_x_info_customization": bool(self.chk_x_info_customization.get()),
            "gen_x_info_oasis_version": bool(self.chk_x_info_oasis_version.get()),
            "swift_services": normalize_swift_services(swift_services),
            "swift_servers_column_widths": dict(self.swift_column_widths),
            
            # Excel Generation
            "excel_gen_attr_diff": bool(self.chk_excel_attr_diff.get()),
            "excel_gen_line_diff": bool(self.chk_excel_line_diff.get()),
            
            # Validation
            "linter_engine": self.cbo_linter_engine.get().lower(),
            "ignore_bad_request": bool(self.chk_ignore_br.get()),
            "validation_font_size": int(self.slider_validation_font.get()),
            
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
            "tools_legacy_tracing_enabled": self.var_legacy_tracing.get(),
            "tools_legacy_example_tracing_enabled": self.var_legacy_example_tracing.get(),
            "tools_legacy_collision_include_descriptions": self.var_legacy_collision_desc.get(),
            "tools_legacy_collision_include_examples": self.var_legacy_collision_examples.get(),
            "tools_legacy_capitalize_schema_names": self.var_legacy_capitalize_schemas.get(),
            "tools_legacy_fill_fix_examples": self.var_legacy_fill_fix_examples.get(),
            "tools_legacy_contact_name": self.entry_legacy_contact_name.get().strip(),
            "tools_legacy_contact_url": self.entry_legacy_contact_url.get().strip(),
            "tools_legacy_release": self.entry_legacy_release.get().strip(),
            "tools_legacy_filename_pattern": self.entry_legacy_filename_pattern.get().strip(),
            
            # OAS Comparison
            "diff_template_synthesis": self.entry_tmpl_syn.get(),
            "diff_template_analytical": self.entry_tmpl_ana.get(),
            "diff_template_impact": self.entry_tmpl_imp.get(),
            "diff_template_compatibility": self.entry_tmpl_comp.get(),
            "diff_show_enum_order_changes": bool(self.var_diff_show_enum_order_changes.get()),
            "diff_show_validation_rule_only_description_changes": bool(
                self.var_diff_show_validation_rule_only_description_changes.get()
            ),

            "diff_debug_mode": False,
            "diff_static_variables": self.current_diff_vars,
        }
        
        self._persist_preferences(new_prefs)

        self.result = True
        self.destroy()

    def _on_save(self):
        self.save_preferences()

    def _on_cancel(self):
        self.result = False
        self.destroy()

    def _current_tab_options(self):
        if bool(self.var_enable_designer.get()):
            return [self.DESIGNER_TAB_OPTION] + self.TAB_OPTIONS
        return list(self.TAB_OPTIONS)

    def _refresh_default_tab_options(self):
        values = self._current_tab_options()
        self.cbo_tab.configure(values=values)
        if self.cbo_tab.get() not in values:
            self.cbo_tab.set("OAS Generation")

    def _on_enable_designer_toggle(self):
        self._refresh_default_tab_options()

    def _default_value(self, key):
        return deepcopy(PreferencesManager.DEFAULT_PREFERENCES[key])

    def _set_switch_value(self, switch, value):
        if bool(value):
            switch.select()
        else:
            switch.deselect()

    def _set_entry_value(self, entry, value):
        entry.delete(0, "end")
        entry.insert(0, str(value or ""))

    def _reset_general_defaults(self):
        self.var_enable_designer.set(self._default_value("enable_api_designer"))
        self._refresh_default_tab_options()
        self.cbo_tab.set(self._default_value("default_tab"))

        default_sort = self._default_value("file_sort_order")
        for display, value in self.SORT_OPTIONS:
            if value == default_sort:
                self.cbo_sort.set(display)
                break

        self.var_remember.set(self._default_value("remember_paths"))
        self._set_switch_value(self.chk_window_pos, self._default_value("remember_window_pos"))
        self.var_update_check.set(self._default_value("update_check_enabled"))

    def _reset_oas_generation_defaults(self):
        self._set_switch_value(self.chk_oas30, self._default_value("gen_oas_30"))
        self._set_switch_value(self.chk_oas31, self._default_value("gen_oas_31"))
        self._set_switch_value(self.chk_swift, self._default_value("gen_oas_swift"))
        self.cbo_generation_mode.set(self._default_value("generation_mode"))
        self._set_switch_value(self.chk_x_info_creation_date, self._default_value("gen_x_info_creation_date"))
        self._set_switch_value(self.chk_x_info_release, self._default_value("gen_x_info_release"))
        self._set_switch_value(self.chk_x_info_customization, self._default_value("gen_x_info_customization"))
        self._set_switch_value(self.chk_x_info_oasis_version, self._default_value("gen_x_info_oasis_version"))

    def _reset_templates_general_defaults(self):
        self._set_switch_value(self.chk_excel_attr_diff, self._default_value("excel_gen_attr_diff"))
        self._set_switch_value(self.chk_excel_line_diff, self._default_value("excel_gen_line_diff"))

        self.var_legacy_tracing.set(self._default_value("tools_legacy_tracing_enabled"))
        self.var_legacy_collision_desc.set(self._default_value("tools_legacy_collision_include_descriptions"))
        self.var_legacy_collision_examples.set(self._default_value("tools_legacy_collision_include_examples"))
        self.var_legacy_capitalize_schemas.set(self._default_value("tools_legacy_capitalize_schema_names"))
        self.var_legacy_fill_fix_examples.set(self._default_value("tools_legacy_fill_fix_examples"))
        self.var_legacy_example_tracing.set(self._default_value("tools_legacy_example_tracing_enabled"))
        self._set_entry_value(self.entry_legacy_contact_name, self._default_value("tools_legacy_contact_name"))
        self._set_entry_value(self.entry_legacy_contact_url, self._default_value("tools_legacy_contact_url"))
        self._set_entry_value(self.entry_legacy_release, self._default_value("tools_legacy_release"))
        self._set_entry_value(self.entry_legacy_filename_pattern, self._default_value("tools_legacy_filename_pattern"))

    def _reset_templates_swift_defaults(self):
        self.swift_column_widths = self._sanitize_swift_column_widths(
            self._default_value("swift_servers_column_widths")
        )
        self._apply_swift_column_widths()
        self._load_swift_server_rows(self._default_value("swift_services"))

    def _reset_validation_defaults(self):
        self.cbo_linter_engine.set(str(self._default_value("linter_engine")).capitalize())
        self._set_switch_value(self.chk_ignore_br, self._default_value("ignore_bad_request"))
        font_size = self._default_value("validation_font_size")
        self.slider_validation_font.set(font_size)
        self.lbl_validation_font_val.configure(text=str(font_size))

    def _reset_view_defaults(self):
        self.cbo_theme.set(self._default_value("yaml_theme"))
        self.cbo_font.set(self._default_value("yaml_font"))
        font_size = self._default_value("yaml_font_size")
        self.slider_font.set(font_size)
        self.lbl_font_val.configure(text=str(font_size))
        self._set_switch_value(self.chk_snap_default, self._default_value("doc_snap_default_enabled"))
        self._set_switch_value(self.chk_word_wrap, self._default_value("yaml_word_wrap"))

    def _reset_logs_defaults(self):
        self.cbo_gen_log_theme.set(self._default_value("gen_log_theme"))
        self.cbo_import_log_theme.set(self._default_value("import_log_theme"))
        self.cbo_app_log_theme.set(self._default_value("app_log_theme"))
        self.cbo_spectral_log_theme.set(self._default_value("spectral_log_theme"))

    def _reset_diff_general_defaults(self):
        self.current_diff_vars = self._default_value("diff_static_variables")
        self._refresh_vars_list()

    def _reset_diff_template_entry(self, entry, preference_key):
        self._set_entry_value(entry, self._default_value(preference_key))

    def _reset_diff_interface_defaults(self):
        self._reset_diff_template_entry(self.entry_tmpl_comp, "diff_template_compatibility")
        self.var_diff_show_enum_order_changes.set(self._default_value("diff_show_enum_order_changes"))
        self.var_diff_show_validation_rule_only_description_changes.set(
            self._default_value("diff_show_validation_rule_only_description_changes")
        )

    def _persist_preferences(self, preferences):
        self.prefs_manager.update(preferences)
        self.prefs_manager.save()

        if self.on_save_callback:
            try:
                self.on_save_callback(preferences)
            except Exception as e:
                print(f"Error applying preferences: {e}")

    def _default_preferences_for_keys(self, keys):
        return {key: self._default_value(key) for key in keys}

    def _current_reset_target(self):
        current_tab = self.tabview.get()
        if current_tab == "Templates":
            current_subtab = self.templates_tabview.get()
            if current_subtab == "SWIFT Servers":
                return (
                    "Templates > SWIFT Servers",
                    self._reset_templates_swift_defaults,
                    ["swift_services", "swift_servers_column_widths"],
                )
            return (
                "Templates > General",
                self._reset_templates_general_defaults,
                [
                    "excel_gen_attr_diff",
                    "excel_gen_line_diff",
                    "tools_legacy_tracing_enabled",
                    "tools_legacy_collision_include_descriptions",
                    "tools_legacy_collision_include_examples",
                    "tools_legacy_capitalize_schema_names",
                    "tools_legacy_fill_fix_examples",
                    "tools_legacy_example_tracing_enabled",
                    "tools_legacy_contact_name",
                    "tools_legacy_contact_url",
                    "tools_legacy_release",
                    "tools_legacy_filename_pattern",
                ],
            )
        if current_tab == "OAS Comparison":
            current_subtab = self.diff_tabview.get()
            if current_subtab == "General":
                return "OAS Comparison > General", self._reset_diff_general_defaults, ["diff_static_variables"]
            if current_subtab == "Synthesis":
                return (
                    "OAS Comparison > Synthesis",
                    lambda: self._reset_diff_template_entry(self.entry_tmpl_syn, "diff_template_synthesis"),
                    ["diff_template_synthesis"],
                )
            if current_subtab == "Analytical":
                return (
                    "OAS Comparison > Analytical",
                    lambda: self._reset_diff_template_entry(self.entry_tmpl_ana, "diff_template_analytical"),
                    ["diff_template_analytical"],
                )
            if current_subtab == "Impact":
                return (
                    "OAS Comparison > Impact",
                    lambda: self._reset_diff_template_entry(self.entry_tmpl_imp, "diff_template_impact"),
                    ["diff_template_impact"],
                )
            return (
                "OAS Comparison > Interface",
                self._reset_diff_interface_defaults,
                [
                    "diff_template_compatibility",
                    "diff_show_enum_order_changes",
                    "diff_show_validation_rule_only_description_changes",
                ],
            )

        resetters = {
            "General": (
                self._reset_general_defaults,
                [
                    "default_tab",
                    "enable_api_designer",
                    "file_sort_order",
                    "remember_paths",
                    "remember_window_pos",
                    "update_check_enabled",
                ],
            ),
            "OAS Generation": (
                self._reset_oas_generation_defaults,
                [
                    "gen_oas_30",
                    "gen_oas_31",
                    "gen_oas_swift",
                    "generation_mode",
                    "gen_x_info_creation_date",
                    "gen_x_info_release",
                    "gen_x_info_customization",
                    "gen_x_info_oasis_version",
                ],
            ),
            "Validation": (
                self._reset_validation_defaults,
                ["linter_engine", "ignore_bad_request", "validation_font_size"],
            ),
            "View": (
                self._reset_view_defaults,
                [
                    "yaml_theme",
                    "yaml_font",
                    "yaml_font_size",
                    "doc_snap_default_enabled",
                    "yaml_word_wrap",
                ],
            ),
            "Logs": (
                self._reset_logs_defaults,
                ["gen_log_theme", "import_log_theme", "app_log_theme", "spectral_log_theme"],
            ),
        }
        resetter_and_keys = resetters.get(current_tab)
        if resetter_and_keys is None:
            return current_tab, None, []
        resetter, keys = resetter_and_keys
        return current_tab, resetter, keys

    def _on_reset_current_section(self):
        scope_name, resetter, preference_keys = self._current_reset_target()
        if resetter is None:
            return
        if not ask_confirmation(
            self,
            "Reset Current Section",
            f"Reset {scope_name} to default values and save immediately?\nOnly this section will change.",
        ):
            return
        resetter()
        self._persist_preferences(self._default_preferences_for_keys(preference_keys))

    def _on_reset(self):
        """Reset UI to default values."""
        if not ask_confirmation(
            self,
            "Reset to Defaults",
            "Reset all Preferences to default values and save immediately?",
        ):
            return
        self._reset_general_defaults()
        self._reset_oas_generation_defaults()
        self._reset_templates_general_defaults()
        self._reset_templates_swift_defaults()
        self._reset_validation_defaults()
        self._reset_view_defaults()
        self._reset_logs_defaults()
        self._reset_diff_general_defaults()
        self._reset_diff_template_entry(self.entry_tmpl_syn, "diff_template_synthesis")
        self._reset_diff_template_entry(self.entry_tmpl_ana, "diff_template_analytical")
        self._reset_diff_template_entry(self.entry_tmpl_imp, "diff_template_impact")
        self._reset_diff_interface_defaults()
        self._persist_preferences(deepcopy(PreferencesManager.DEFAULT_PREFERENCES))
