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
    TAB_OPTIONS = ["OAS to Excel", "Excel to OAS", "Validation", "View"]

    def __init__(self, parent, prefs_manager, on_save_callback=None):
        super().__init__(parent)

        self.prefs_manager = prefs_manager
        self.on_save_callback = on_save_callback
        self.result = None  # Will be True if saved, False/None if cancelled

        # Window setup
        self.title("Preferences")
        self.geometry("600x380") # Reduced height (was 420)
        self.resizable(False, False) # Fixed size for cleaner look

        # Non-modal: only transient
        self.transient(parent)

        # Center on parent
        self.update_idletasks()
        try:
            x = parent.winfo_x() + (parent.winfo_width() - 600) // 2
            y = parent.winfo_y() + (parent.winfo_height() - 380) // 2
            self.geometry(f"+{int(x)}+{int(y)}")
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

    def _build_ui(self):
        """Build the preferences UI with Tabs."""
        self.tabview = ctk.CTkTabview(self, segmented_button_selected_color="#0A809E", segmented_button_selected_hover_color="#076075")
        self.tabview.pack(fill="both", expand=True, padx=15, pady=(10, 5))

        # Create Tabs
        self.tab_gen = self.tabview.add("General")
        self.tab_excel = self.tabview.add("Excel Generation")
        self.tab_output = self.tabview.add("OAS Generation")
        self.tab_val = self.tabview.add("Validation")
        self.tab_view = self.tabview.add("View")
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


        # === 2. EXCEL GENERATION TAB ===
        self.chk_excel_attr_diff = ctk.CTkSwitch(self.tab_excel, text="Attribute Diff", progress_color="#0A809E")
        self.chk_excel_attr_diff.pack(anchor="w", padx=20, pady=(20, 10))

        self.chk_excel_line_diff = ctk.CTkSwitch(self.tab_excel, text="Line Diff", progress_color="#0A809E")
        self.chk_excel_line_diff.pack(anchor="w", padx=20, pady=10)


        # === 3. OAS GENERATION TAB ===
        self.chk_oas31 = ctk.CTkSwitch(self.tab_output, text="OAS 3.1", progress_color="#0A809E")
        self.chk_oas31.pack(anchor="w", padx=20, pady=(20, 10))

        self.chk_oas30 = ctk.CTkSwitch(self.tab_output, text="OAS 3.0", progress_color="#0A809E")
        self.chk_oas30.pack(anchor="w", padx=20, pady=10)

        self.chk_swift = ctk.CTkSwitch(self.tab_output, text="OAS SWIFT", progress_color="#0A809E")
        self.chk_swift.pack(anchor="w", padx=20, pady=10)


        # === 4. VALIDATION TAB ===
        self.chk_ignore_br = ctk.CTkSwitch(
            self.tab_val, text="Ignore 'Bad Request' Examples", progress_color="#0A809E"
        )
        self.chk_ignore_br.pack(anchor="w", padx=20, pady=20)


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
        
        self.chk_snap_default = ctk.CTkSwitch(
            self.tab_view, text="Dock documentation viewer to main window", progress_color="#0A809E"
        )
        self.chk_snap_default.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=20)


        # === 6. LOGS TAB ===
        self.tab_logs.grid_columnconfigure(1, weight=1)

        # OAS to Excel Theme
        ctk.CTkLabel(self.tab_logs, text="OAS To Excel Theme:").grid(row=0, column=0, sticky="w", padx=(10, 10), pady=10)
        self.cbo_gen_log_theme = ctk.CTkComboBox(self.tab_logs, values=["Light", "Dark"], width=150, button_color="#0A809E")
        self.cbo_gen_log_theme.grid(row=0, column=1, sticky="w", pady=10)

        # Excel to OAS Theme
        ctk.CTkLabel(self.tab_logs, text="Excel To OAS Theme:").grid(row=1, column=0, sticky="w", padx=(10, 10), pady=10)
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
        if prefs.get("ignore_bad_request", True): self.chk_ignore_br.select()

        # View
        theme = prefs.get("yaml_theme", "oas-dark")
        if theme in self.THEMES: self.cbo_theme.set(theme)
        self.cbo_font.set(prefs.get("yaml_font", "Consolas"))
        self.slider_font.set(prefs.get("yaml_font_size", 12))
        self.lbl_font_val.configure(text=str(prefs.get("yaml_font_size", 12)))
        if prefs.get("doc_snap_default_enabled", True): self.chk_snap_default.select()

        # Logs
        self.cbo_gen_log_theme.set(prefs.get("gen_log_theme", "Light"))
        self.cbo_import_log_theme.set(prefs.get("import_log_theme", "Light")) # New
        self.cbo_app_log_theme.set(prefs.get("app_log_theme", "Dark"))
        self.cbo_spectral_log_theme.set(prefs.get("spectral_log_theme", "Light"))


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
            "ignore_bad_request": bool(self.chk_ignore_br.get()),
            
            # View
            "yaml_theme": self.cbo_theme.get(),
            "yaml_font": self.cbo_font.get(),
            "yaml_font_size": int(self.slider_font.get()),
            "doc_snap_default_enabled": bool(self.chk_snap_default.get()),
            
            # Logs
            "gen_log_theme": self.cbo_gen_log_theme.get(),
            "import_log_theme": self.cbo_import_log_theme.get(), # New
            "app_log_theme": self.cbo_app_log_theme.get(),
            "spectral_log_theme": self.cbo_spectral_log_theme.get(),
        }
        
        self.prefs_manager.update(new_prefs)
        self.prefs_manager.save()
        
        if self.on_save_callback:
            try:
                self.on_save_callback()
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
        self.cbo_tab.set("OAS to Excel")
        self.cbo_sort.set("Alphabetical")
        self.var_remember.set(False)
        self.chk_window_pos.select()
        
        self.chk_oas30.select()
        self.chk_oas31.select()
        self.chk_swift.deselect()

        self.chk_excel_attr_diff.select()
        self.chk_excel_line_diff.deselect()
        
        self.chk_ignore_br.select()
        
        self.cbo_theme.set("oas-dark")
        self.cbo_font.set("Consolas")
        self.slider_font.set(12)
        self.lbl_font_val.configure(text="12")
        self.chk_snap_default.select()
        
        self.cbo_gen_log_theme.set("Light")
        self.cbo_import_log_theme.set("Light")
        self.cbo_app_log_theme.set("Dark")
        self.cbo_spectral_log_theme.set("Light")
