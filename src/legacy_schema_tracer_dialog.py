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
            self.geometry(f"{pw}x{ph}+{px+50}+{py+50}")
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

        # Focus management (same as Legacy Converter)
        self.after(300, self.lift)

        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _load_saved_path(self):
        if self.prefs_manager:
            last_path = self.prefs_manager.get("last_legacy_dst", "")
            if last_path and os.path.exists(last_path):
                self.entry_path.insert(0, last_path)

    def _build_ui(self):
        # Container
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        # --- Header ---
        header_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(header_frame, text="Template Schema Tracer", 
                     text_color="#0A809E",
                     font=ctk.CTkFont(size=26, weight="bold")).pack(side="left")
        ctk.CTkLabel(header_frame, 
                     text="Analyze converted projects for type collisions and forks",
                     font=ctk.CTkFont(size=14, slant="italic")).pack(side="left", padx=15, pady=(8, 0))
        
        # Header Separator
        line = ctk.CTkFrame(self.container, height=2, fg_color="#E0E0E0")
        line.pack(fill="x", pady=(0, 20))


        # Input Frame
        input_frame = ctk.CTkFrame(self.container, corner_radius=10)
        input_frame.pack(fill="x", padx=10, pady=10)

        # Folder Selection
        path_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        path_frame.pack(fill="x", pady=10, padx=15)
        ctk.CTkLabel(path_frame, text="Template Folder:", width=180, anchor="w").pack(side="left")
        self.entry_path = ctk.CTkEntry(path_frame, placeholder_text="Path to folder containing $index file...")
        self.entry_path.pack(side="left", fill="x", expand=True, padx=5)
        ctk.CTkButton(path_frame, text="Browse", width=80, 
                      fg_color="#0A809E", hover_color="#076075",
                      command=self._browse_path).pack(side="left")
        self.btn_open_folder = ctk.CTkButton(path_frame, text="📁", width=40,
                                            fg_color="#0A809E", hover_color="#076075",
                                            font=ctk.CTkFont(size=18),
                                            anchor="center",
                                            command=self._open_template_folder)
        self.btn_open_folder.pack(side="left", padx=(5, 0), pady=(2, 0))

        # Options Frame
        opts_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        opts_frame.pack(fill="x", pady=(0, 10), padx=15)
        self.inject_refs_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(opts_frame,
                        text="Inject Schema References into $index.xlsx",
                        variable=self.inject_refs_var,
                        fg_color="#0A809E", hover_color="#076075",
                        font=ctk.CTkFont(size=13)).pack(side="left")

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
        p = filedialog.askdirectory(parent=self, initialdir=initial, title="Select Template Folder")
        if p:
            self.lift()
            self.focus_force()
            self.entry_path.delete(0, "end")
            self.entry_path.insert(0, p)
            # Save immediately
            if self.prefs_manager and self.prefs_manager.get("remember_paths", True):
                self.prefs_manager.set("last_legacy_dst", p)
                self.prefs_manager.save()

    def _open_template_folder(self):
        p = self.entry_path.get()
        if p and os.path.exists(p):
            os.startfile(p)

    def _on_close(self):
        """Save settings and close window."""
        if self.prefs_manager and self.prefs_manager.get("remember_paths", True):
            self.prefs_manager.set("last_legacy_dst", self.entry_path.get())
            self.prefs_manager.save()
        self.destroy()

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
            include_desc = False
            include_ex = False
            if self.prefs_manager:
                include_desc = bool(self.prefs_manager.get("tools_legacy_collision_include_descriptions", False))
                include_ex = bool(self.prefs_manager.get("tools_legacy_collision_include_examples", False))

            converter = LegacyConverter(
                path,
                path,
                log_callback=self._log,
                include_descriptions_in_collision=include_desc,
                include_examples_in_collision=include_ex,
            )
            inject_refs = self.inject_refs_var.get()
            success = converter.run_standalone_check(path, inject_refs=inject_refs)
            
            if success:
                self._log("\nANALYSIS COMPLETED SUCCESSFULLY.")
            else:
                self._log("\nANALYSIS FAILED.")
                
        except Exception as e:
            self._log(f"\nCRITICAL ERROR: {e}")
        finally:
            self.after(0, lambda: self.btn_trace.configure(state="normal"))
