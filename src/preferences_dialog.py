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
    TAB_OPTIONS = ["OAS to Excel", "Excel to OAS", "Validation", "View"]

    def __init__(self, parent, prefs_manager, on_save_callback=None):
        super().__init__(parent)

        self.prefs_manager = prefs_manager
        self.on_save_callback = on_save_callback
        self.result = None  # Will be True if saved, False/None if cancelled

        # Window setup
        self.title("Preferences")
        self.geometry("550x580")
        self.resizable(True, True)

        # Non-modal: only transient, no grab_set
        self.transient(parent)
        # Removed: self.grab_set() - allows interaction with main window

        # Center on parent
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 550) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 580) // 2
        self.geometry(f"+{x}+{y}")

        # Set window icon AFTER CTkToplevel's internal 200ms default icon setting
        # CTkToplevel sets a default icon at ~200ms, so we need 250ms+ to override it
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
                # At 250ms, CTkToplevel has already set its default icon,
                # so we can safely override it now
                self.iconbitmap(icon_file)
        except (OSError, FileNotFoundError, Exception):
            pass

    def _build_ui(self):
        """Build the preferences UI."""
        # Main scrollable frame
        self.main_frame = ctk.CTkScrollableFrame(self, label_text="")
        self.main_frame.pack(fill="both", expand=True, padx=15, pady=(15, 5))

        # === PATHS SECTION ===
        self._create_section_header("Paths")

        # Template Directory
        self.frame_template = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.frame_template.pack(fill="x", pady=5)
        self.frame_template.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.frame_template, text="Template Directory:").grid(
            row=0, column=0, sticky="w", padx=(0, 10)
        )
        self.entry_template = ctk.CTkEntry(
            self.frame_template, placeholder_text="Leave empty for default"
        )
        self.entry_template.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        ctk.CTkButton(
            self.frame_template, text="Browse", width=70, command=self._browse_template
        ).grid(row=0, column=2)

        # OAS Folder
        self.frame_oas = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.frame_oas.pack(fill="x", pady=5)
        self.frame_oas.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.frame_oas, text="OAS Folder:").grid(
            row=0, column=0, sticky="w", padx=(0, 10)
        )
        self.entry_oas = ctk.CTkEntry(
            self.frame_oas, placeholder_text="Leave empty for default"
        )
        self.entry_oas.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        ctk.CTkButton(
            self.frame_oas, text="Browse", width=70, command=self._browse_oas
        ).grid(row=0, column=2)

        # === GENERATION SECTION ===
        self._create_section_header("Generation Defaults")

        self.frame_gen = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.frame_gen.pack(fill="x", pady=5)

        self.chk_oas31 = ctk.CTkCheckBox(self.frame_gen, text="OAS 3.1")
        self.chk_oas31.pack(side="left", padx=(0, 20))

        self.chk_oas30 = ctk.CTkCheckBox(self.frame_gen, text="OAS 3.0")
        self.chk_oas30.pack(side="left", padx=(0, 20))

        self.chk_swift = ctk.CTkCheckBox(self.frame_gen, text="OAS SWIFT")
        self.chk_swift.pack(side="left")

        # === VALIDATION SECTION ===
        self._create_section_header("Validation")

        self.frame_val = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.frame_val.pack(fill="x", pady=5)

        self.chk_ignore_br = ctk.CTkCheckBox(
            self.frame_val, text="Ignore 'Bad Request' Examples by default"
        )
        self.chk_ignore_br.pack(anchor="w", pady=2)

        # === VIEW SECTION ===
        self._create_section_header("YAML Viewer")

        self.frame_view = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.frame_view.pack(fill="x", pady=5)
        self.frame_view.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.frame_view, text="Theme:").grid(
            row=0, column=0, sticky="w", padx=(0, 10)
        )
        self.cbo_theme = ctk.CTkComboBox(self.frame_view, values=self.THEMES, width=200)
        self.cbo_theme.grid(row=0, column=1, sticky="w", pady=5)

        ctk.CTkLabel(self.frame_view, text="Font:").grid(
            row=1, column=0, sticky="w", padx=(0, 10)
        )
        self.cbo_font = ctk.CTkComboBox(
            self.frame_view,
            values=[
                "Consolas",
                "Courier New",
                "Monaco",
                "Fira Code",
                "JetBrains Mono",
                "Source Code Pro",
            ],
            width=200,
        )
        self.cbo_font.grid(row=1, column=1, sticky="w", pady=5)

        ctk.CTkLabel(self.frame_view, text="Font Size:").grid(
            row=2, column=0, sticky="w", padx=(0, 10)
        )
        self.frame_font = ctk.CTkFrame(self.frame_view, fg_color="transparent")
        self.frame_font.grid(row=2, column=1, sticky="w", pady=5)

        self.slider_font = ctk.CTkSlider(
            self.frame_font, from_=8, to=20, number_of_steps=12, width=150
        )
        self.slider_font.pack(side="left")
        self.lbl_font_val = ctk.CTkLabel(self.frame_font, text="12", width=30)
        self.lbl_font_val.pack(side="left", padx=(10, 0))
        self.slider_font.configure(
            command=lambda v: self.lbl_font_val.configure(text=str(int(v)))
        )

        # === LOGS SECTION ===
        self._create_section_header("Logs Appearance")

        self.frame_logs = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.frame_logs.pack(fill="x", pady=5)
        self.frame_logs.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.frame_logs, text="Generation Logs:").grid(
            row=0, column=0, sticky="w", padx=(0, 10), pady=2
        )
        self.cbo_gen_log_theme = ctk.CTkComboBox(
            self.frame_logs, values=["Light", "Dark"], width=100
        )
        self.cbo_gen_log_theme.grid(row=0, column=1, sticky="w", pady=2)

        ctk.CTkLabel(self.frame_logs, text="Application Logs:").grid(
            row=1, column=0, sticky="w", padx=(0, 10), pady=2
        )
        self.cbo_app_log_theme = ctk.CTkComboBox(
            self.frame_logs, values=["Light", "Dark"], width=100
        )
        self.cbo_app_log_theme.grid(row=1, column=1, sticky="w", pady=2)

        ctk.CTkLabel(self.frame_logs, text="Spectral Output:").grid(
            row=2, column=0, sticky="w", padx=(0, 10), pady=2
        )
        self.cbo_spectral_log_theme = ctk.CTkComboBox(
            self.frame_logs, values=["Light", "Dark"], width=100
        )
        self.cbo_spectral_log_theme.grid(row=2, column=1, sticky="w", pady=2)

        # === FILE DISPLAY SECTION ===
        self._create_section_header("File Display")

        self.frame_sort = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.frame_sort.pack(fill="x", pady=5)

        ctk.CTkLabel(self.frame_sort, text="Sort Order:").pack(
            side="left", padx=(0, 10)
        )
        self.cbo_sort = ctk.CTkComboBox(
            self.frame_sort, values=[opt[0] for opt in self.SORT_OPTIONS], width=150
        )
        self.cbo_sort.pack(side="left")

        # === INTERFACE SECTION ===
        self._create_section_header("Interface")

        self.frame_iface = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.frame_iface.pack(fill="x", pady=5)
        self.frame_iface.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.frame_iface, text="Default Tab:").grid(
            row=0, column=0, sticky="w", padx=(0, 10)
        )
        self.cbo_tab = ctk.CTkComboBox(
            self.frame_iface, values=self.TAB_OPTIONS, width=150
        )
        self.cbo_tab.grid(row=0, column=1, sticky="w", pady=5)

        self.chk_window_pos = ctk.CTkCheckBox(
            self.frame_iface, text="Remember window size and position"
        )
        self.chk_window_pos.grid(row=1, column=0, columnspan=2, sticky="w", pady=5)

        self.chk_snap_default = ctk.CTkCheckBox(
            self.frame_iface, text="Dock documentation viewer to main window by default"
        )
        self.chk_snap_default.grid(row=2, column=0, columnspan=2, sticky="w", pady=5)

        # === BUTTONS ===
        # UX Best Practice: Primary=blue, Secondary=gray, Destructive=red
        self.frame_buttons = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_buttons.pack(fill="x", padx=15, pady=15)

        # Reset to Defaults - red for destructive action
        ctk.CTkButton(
            self.frame_buttons,
            text="Reset to Defaults",
            width=130,
            fg_color=("#D04040", "#B03030"),
            hover_color=("#B03030", "#902020"),
            command=self._on_reset,
        ).pack(side="left")

        # Cancel - gray for secondary action
        ctk.CTkButton(
            self.frame_buttons,
            text="Cancel",
            width=100,
            fg_color="gray50",
            hover_color="gray40",
            command=self._on_cancel,
        ).pack(side="right", padx=(10, 0))

        # Apply & Close - default blue for primary action
        ctk.CTkButton(
            self.frame_buttons, text="Apply & Close", width=120, command=self._on_save
        ).pack(side="right")

    def _create_section_header(self, text: str):
        """Create a section header with separator."""
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame.pack(fill="x", pady=(15, 5))
        ctk.CTkLabel(frame, text=text, font=ctk.CTkFont(weight="bold", size=14)).pack(
            anchor="w"
        )


    def _browse_template(self):
        """Browse for template directory."""
        current = self.entry_template.get()
        initial = current if current and os.path.exists(current) else os.getcwd()
        directory = filedialog.askdirectory(initialdir=initial)
        if directory:
            self.entry_template.delete(0, "end")
            self.entry_template.insert(0, directory)

    def _browse_oas(self):
        """Browse for OAS folder."""
        current = self.entry_oas.get()
        initial = current if current and os.path.exists(current) else os.getcwd()
        directory = filedialog.askdirectory(initialdir=initial)
        if directory:
            self.entry_oas.delete(0, "end")
            self.entry_oas.insert(0, directory)

    def _load_current_values(self):
        """Load current preference values into the UI."""
        prefs = self.prefs_manager.get_all()

        # Paths
        self.entry_template.insert(0, prefs.get("template_directory", ""))
        self.entry_oas.insert(0, prefs.get("oas_folder", ""))

        # Generation
        if prefs.get("gen_oas_30", True):
            self.chk_oas30.select()
        if prefs.get("gen_oas_31", True):
            self.chk_oas31.select()
        if prefs.get("gen_oas_swift", False):
            self.chk_swift.select()

        # Validation
        if prefs.get("ignore_bad_request", True):
            self.chk_ignore_br.select()

        # View
        theme = prefs.get("yaml_theme", "oas-dark")
        if theme in self.THEMES:
            self.cbo_theme.set(theme)

        font_family = prefs.get("yaml_font", "Consolas")
        self.cbo_font.set(font_family)

        font_size = prefs.get("yaml_font_size", 12)
        self.slider_font.set(font_size)
        self.lbl_font_val.configure(text=str(font_size))

        # Logs
        self.cbo_gen_log_theme.set(prefs.get("gen_log_theme", "Light"))
        self.cbo_app_log_theme.set(prefs.get("app_log_theme", "Dark"))  # Default Dark
        self.cbo_spectral_log_theme.set(prefs.get("spectral_log_theme", "Light"))

        # File Display
        sort_order = prefs.get("file_sort_order", "alphabetical")
        for display, value in self.SORT_OPTIONS:
            if value == sort_order:
                self.cbo_sort.set(display)
                break

        # Interface
        default_tab = prefs.get("default_tab", "Generation")
        if default_tab in self.TAB_OPTIONS:
            self.cbo_tab.set(default_tab)

        if prefs.get("remember_window_pos", True):
            self.chk_window_pos.select()

        if prefs.get("doc_snap_default_enabled", True):
            self.chk_snap_default.select()

    def _get_current_values(self) -> dict:
        """Get current values from UI as a dictionary."""
        # Map sort display name back to value
        sort_display = self.cbo_sort.get()
        sort_value = "alphabetical"
        for display, value in self.SORT_OPTIONS:
            if display == sort_display:
                sort_value = value
                break

        return {
            "template_directory": self.entry_template.get().strip(),
            "oas_folder": self.entry_oas.get().strip(),
            "gen_oas_30": self.chk_oas30.get() == 1,
            "gen_oas_31": self.chk_oas31.get() == 1,
            "gen_oas_swift": self.chk_swift.get() == 1,
            "ignore_bad_request": self.chk_ignore_br.get() == 1,
            "yaml_theme": self.cbo_theme.get(),
            "yaml_font": self.cbo_font.get(),
            "yaml_font_size": int(self.slider_font.get()),
            "gen_log_theme": self.cbo_gen_log_theme.get(),
            "app_log_theme": self.cbo_app_log_theme.get(),
            "spectral_log_theme": self.cbo_spectral_log_theme.get(),
            "file_sort_order": sort_value,
            "file_sort_order": sort_value,
            "default_tab": self.cbo_tab.get(),
            "remember_window_pos": self.chk_window_pos.get() == 1,
            "doc_snap_default_enabled": self.chk_snap_default.get() == 1,
        }

    def _on_save(self):
        """Save preferences and close."""
        new_prefs = self._get_current_values()
        self.prefs_manager.update(new_prefs)
        self.prefs_manager.save()
        self.result = True

        if self.on_save_callback:
            self.on_save_callback(new_prefs)

        self.destroy()

    def _on_cancel(self):
        """Cancel and close without saving."""
        self.result = False
        self.destroy()

    def _on_reset(self):
        """Reset UI to default values."""
        # Clear all
        self.entry_template.delete(0, "end")
        self.entry_oas.delete(0, "end")

        # Checkboxes
        self.chk_oas30.select()
        self.chk_oas31.select()
        self.chk_swift.deselect()
        self.chk_ignore_br.select()
        self.chk_window_pos.select()

        # Dropdowns
        self.cbo_theme.set("oas-dark")
        self.cbo_font.set("Consolas")
        self.cbo_gen_log_theme.set("Light")
        self.cbo_app_log_theme.set("Dark")  # Default Dark
        self.cbo_spectral_log_theme.set("Light")
        self.cbo_sort.set("Alphabetical")
        self.cbo_tab.set("OAS to Excel")
 
        # Slider
        self.slider_font.set(12)
        self.lbl_font_val.configure(text="12")
