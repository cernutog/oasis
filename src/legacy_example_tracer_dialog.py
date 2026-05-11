import customtkinter as ctk
from tkinter import filedialog
import os
import threading

from .legacy_converter import (
    EXAMPLE_TRACE_COMPLEX_MARKER,
    EXAMPLE_TRACE_IMPOSSIBLE_MARKER,
    LegacyConverter,
)


class LegacyExampleTracerDialog(ctk.CTkToplevel):
    def __init__(self, parent, prefs_manager=None):
        super().__init__(parent)
        self.prefs_manager = prefs_manager
        self.title("Template Example Tracer")

        try:
            parent.update_idletasks()
            pw = parent.winfo_width()
            ph = parent.winfo_height()
            px = parent.winfo_x()
            py = parent.winfo_y()
            self.geometry(f"{pw}x{ph}+{px+50}+{py+50}")
        except Exception:
            self.geometry("1000x800")

        self.resizable(True, True)
        self.after(300, self.lift)

        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "icon.ico")
        if os.path.exists(icon_path):
            try:
                self.after(400, lambda: self.iconbitmap(icon_path))
            except Exception:
                pass

        self._build_ui()
        self._load_saved_path()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _load_saved_path(self):
        if self.prefs_manager:
            last_path = self.prefs_manager.get("last_legacy_dst", "")
            if last_path and os.path.exists(last_path):
                self.entry_path.insert(0, last_path)

    def _build_ui(self):
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        header_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            header_frame,
            text="Template Example Tracer",
            text_color="#0A809E",
            font=ctk.CTkFont(size=26, weight="bold"),
        ).pack(side="left")
        ctk.CTkLabel(
            header_frame,
            text="Analyze and repair converted template examples",
            font=ctk.CTkFont(size=14, slant="italic"),
        ).pack(side="left", padx=15, pady=(8, 0))

        line = ctk.CTkFrame(self.container, height=2, fg_color="#E0E0E0")
        line.pack(fill="x", pady=(0, 20))

        input_frame = ctk.CTkFrame(self.container, corner_radius=10)
        input_frame.pack(fill="x", padx=10, pady=10)

        path_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        path_frame.pack(fill="x", pady=10, padx=15)
        ctk.CTkLabel(path_frame, text="Template Folder:", width=180, anchor="w").pack(side="left")
        self.entry_path = ctk.CTkEntry(path_frame, placeholder_text="Path to converted templates folder...")
        self.entry_path.pack(side="left", fill="x", expand=True, padx=5)
        ctk.CTkButton(
            path_frame,
            text="Browse",
            width=80,
            fg_color="#0A809E",
            hover_color="#076075",
            command=self._browse_path,
        ).pack(side="left")

        opts_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        opts_frame.pack(fill="x", pady=(0, 10), padx=15)
        self.repair_files_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            opts_frame,
            text="Repair files",
            variable=self.repair_files_var,
            fg_color="#0A809E",
            hover_color="#076075",
            font=ctk.CTkFont(size=13),
        ).pack(side="left")

        btn_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        btn_frame.pack(pady=10)

        self.btn_trace = ctk.CTkButton(
            btn_frame,
            text="Analyze Examples",
            fg_color="#0A809E",
            hover_color="#076075",
            font=ctk.CTkFont(weight="bold"),
            command=self._start_tracing,
        )
        self.btn_trace.pack()

        self.log_area = ctk.CTkTextbox(
            self.container,
            font=("Consolas", 11),
            fg_color="#F0F4F5",
            text_color="#333333",
            wrap="none",
            state="disabled",
        )
        self.log_area.pack(fill="both", expand=True, pady=(10, 0))
        self._configure_log_tags()

    def _get_initial_dir(self):
        p = self.entry_path.get()
        if p and os.path.exists(p):
            return p if os.path.isdir(p) else os.path.dirname(p)
        return os.getcwd()

    def _browse_path(self):
        p = filedialog.askdirectory(parent=self, initialdir=self._get_initial_dir(), title="Select Template Folder")
        if p:
            self.lift()
            self.focus_force()
            self.entry_path.delete(0, "end")
            self.entry_path.insert(0, p)
            if self.prefs_manager and self.prefs_manager.get("remember_paths", True):
                self.prefs_manager.set("last_legacy_dst", p)
                self.prefs_manager.save()

    def _on_close(self):
        if self.prefs_manager and self.prefs_manager.get("remember_paths", True):
            self.prefs_manager.set("last_legacy_dst", self.entry_path.get())
            self.prefs_manager.save()
        self.destroy()

    def _log(self, msg):
        text = str(msg)
        tag = None
        if text.startswith(EXAMPLE_TRACE_IMPOSSIBLE_MARKER):
            text = text[len(EXAMPLE_TRACE_IMPOSSIBLE_MARKER):]
            tag = "example_impossible"
        elif text.startswith(EXAMPLE_TRACE_COMPLEX_MARKER):
            text = text[len(EXAMPLE_TRACE_COMPLEX_MARKER):]
            tag = "example_complex"

        self.log_area.configure(state="normal")
        if tag:
            self._insert_tagged_log(f"{text}\n", tag)
        else:
            self.log_area.insert("end", f"{text}\n")
        self.log_area.see("end")
        self.log_area.configure(state="disabled")

    def _configure_log_tags(self):
        tag_target = getattr(self.log_area, "_textbox", self.log_area)
        try:
            tag_target.tag_configure("example_impossible", foreground="#A65A5A")
            tag_target.tag_configure("example_complex", foreground="#9A8700")
        except Exception:
            pass

    def _insert_tagged_log(self, text, tag):
        tag_target = getattr(self.log_area, "_textbox", None)
        try:
            if tag_target is not None:
                tag_target.insert("end", text, tag)
            else:
                self.log_area.insert("end", text, tag)
        except Exception:
            self.log_area.insert("end", text)

    def _start_tracing(self):
        path = self.entry_path.get()
        if not path or not os.path.exists(path):
            self._log("Error: Invalid template folder.")
            return

        self.btn_trace.configure(state="disabled")
        self.log_area.configure(state="normal")
        self.log_area.delete("1.0", "end")
        self.log_area.configure(state="disabled")
        threading.Thread(target=self._run_tracing, args=(path,), daemon=True).start()

    def _run_tracing(self, path):
        try:
            repair_files = bool(self.repair_files_var.get())
            mode = "repair" if repair_files else "trace only"
            self._log(f"Starting example analysis for {path} ({mode})...\n")

            seed_path = None
            if self.prefs_manager and hasattr(self.prefs_manager, "get_legacy_example_seed_values_path"):
                seed_path = self.prefs_manager.get_legacy_example_seed_values_path()
            semantic_rules_path = None
            if self.prefs_manager and hasattr(self.prefs_manager, "get_legacy_example_semantic_rules_path"):
                semantic_rules_path = self.prefs_manager.get_legacy_example_semantic_rules_path()

            converter = LegacyConverter(
                path,
                path,
                log_callback=self._log,
                detail_log_callback=self._log,
                fill_fix_examples=True,
                example_seed_values_path=seed_path,
                example_semantic_rules_path=semantic_rules_path,
                example_tracing_enabled=True,
            )
            success = converter.run_standalone_example_trace(path, repair_files=repair_files)

            if success:
                self._log("\nEXAMPLE ANALYSIS COMPLETED SUCCESSFULLY.")
            else:
                self._log("\nEXAMPLE ANALYSIS FAILED.")
        except Exception as exc:
            self._log(f"\nCRITICAL ERROR: {exc}")
        finally:
            self.after(0, lambda: self.btn_trace.configure(state="normal"))
