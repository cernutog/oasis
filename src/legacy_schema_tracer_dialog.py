import customtkinter as ctk
from tkinter import filedialog
import os
import threading
from .legacy_converter import LegacyConverter

class LegacySchemaTracerDialog(ctk.CTkToplevel):
    def __init__(self, parent, prefs_manager=None):
        super().__init__(parent)
        self.prefs_manager = prefs_manager
        self.title("Template Schema Tracer")
        
        # Match parent window size and position
        try:
            parent.update_idletasks()
            pw = parent.winfo_width()
            ph = parent.winfo_height()
            px = parent.winfo_x()
            py = parent.winfo_y()
            self.geometry(f"{pw}x{ph}+{px}+{py}")
        except:
            self.geometry("1000x800")
        
        self.resizable(True, True)
        self.after(300, self.lift)

        # Set icon if exists
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "icon.ico")
        if os.path.exists(icon_path):
            try:
                self.after(400, lambda: self.iconbitmap(icon_path))
            except:
                pass
        
        self._build_ui()
        self._load_saved_path()

    def _load_saved_path(self):
        if self.prefs_manager:
            last_path = self.prefs_manager.get("last_legacy_dst", "")
            if last_path and os.path.exists(last_path):
                self.entry_path.insert(0, last_path)

    def _build_ui(self):
        # Container
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        # Title/Description
        ctk.CTkLabel(self.container, text="Template Schema Tracer", 
                     text_color="#0A809E",
                     font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(0, 5))
        ctk.CTkLabel(self.container, 
                     text="Analyze an already converted project folder to find type forks and collisions.\nPowered by the modern $index structure.",
                     font=ctk.CTkFont(size=13)).pack(pady=(0, 20))

        # Input Frame
        input_frame = ctk.CTkFrame(self.container, corner_radius=10)
        input_frame.pack(fill="x", padx=10, pady=10)

        # Folder Selection
        path_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        path_frame.pack(fill="x", pady=10, padx=15)
        ctk.CTkLabel(path_frame, text="Converted Project Folder:", width=180, anchor="w").pack(side="left")
        self.entry_path = ctk.CTkEntry(path_frame, placeholder_text="Path to folder containing $index file...")
        self.entry_path.pack(side="left", fill="x", expand=True, padx=5)
        ctk.CTkButton(path_frame, text="Browse", width=80, 
                      fg_color="#0A809E", hover_color="#076075",
                      command=self._browse_path).pack(side="left")

        # Action Button
        btn_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        btn_frame.pack(pady=10)

        self.btn_trace = ctk.CTkButton(btn_frame, text="Run Analysis", 
                                      fg_color="#0A809E", hover_color="#076075",
                                      font=ctk.CTkFont(weight="bold"),
                                      command=self._start_tracing)
        self.btn_trace.pack()

        # Output Area
        self.log_area = ctk.CTkTextbox(self.container, font=("Consolas", 11), 
                                      fg_color="#F0F4F5", text_color="#333333",
                                      wrap="none",
                                      state="disabled")
        self.log_area.pack(fill="both", expand=True, pady=(10, 0))

    def _get_initial_dir(self):
        p = self.entry_path.get()
        if p and os.path.exists(p):
            return p if os.path.isdir(p) else os.path.dirname(p)
        return os.getcwd()

    def _browse_path(self):
        initial = self._get_initial_dir()
        p = filedialog.askdirectory(parent=self, initialdir=initial, title="Select Converted Project Folder")
        if p:
            self.lift()
            self.focus_force()
            self.entry_path.delete(0, "end")
            self.entry_path.insert(0, p)

    def _log(self, msg):
        self.log_area.configure(state="normal")
        self.log_area.insert("end", f"{msg}\n")
        self.log_area.see("end")
        self.log_area.configure(state="disabled")

    def _start_tracing(self):
        path = self.entry_path.get()
        if not path or not os.path.exists(path):
            self._log("Error: Invalid project folder.")
            return

        self.btn_trace.configure(state="disabled")
        self.log_area.configure(state="normal")
        self.log_area.delete("1.0", "end")
        self.log_area.configure(state="disabled")

        threading.Thread(target=self._run_tracing, args=(path,), daemon=True).start()

    def _run_tracing(self, path):
        try:
            self._log(f"Starting standalone analysis for {path}...\n")
            # We don't need real output/master dirs for standalone check
            converter = LegacyConverter(path, path, log_callback=self._log)
            success = converter.run_standalone_check(path)
            
            if success:
                self._log("\nANALYSIS COMPLETED SUCCESSFULLY.")
            else:
                self._log("\nANALYSIS FAILED.")
                
        except Exception as e:
            self._log(f"\nCRITICAL ERROR: {e}")
        finally:
            self.after(0, lambda: self.btn_trace.configure(state="normal"))
