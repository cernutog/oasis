import customtkinter as ctk
from tkinter import filedialog
import os
import threading
from .oas_diff.report_manager import OASDiffReportManager

class OASDiffDialog(ctk.CTkToplevel):
    def __init__(self, parent, prefs_manager=None):
        super().__init__(parent)
        self.prefs_manager = prefs_manager
        self.title("OAS Comparison - Contract Comparison")
        
        # Report paths state
        self.report_paths = {"synthesis": None, "analytical": None, "impact": None}
        
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

        # Set icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "icon.ico")
        if os.path.exists(icon_path):
            try:
                self.after(400, lambda: self.iconbitmap(icon_path))
            except:
                pass
        
        self._build_ui()
        self._load_saved_paths()

        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _load_saved_paths(self):
        if self.prefs_manager:
            old_path = self.prefs_manager.get("diff_old_spec", "")
            new_path = self.prefs_manager.get("diff_new_spec", "")
            out_dir = self.prefs_manager.get("diff_output_dir", "")
            
            if old_path and os.path.exists(old_path):
                self.entry_old.insert(0, old_path)
            if new_path and os.path.exists(new_path):
                self.entry_new.insert(0, new_path)
            if out_dir and os.path.exists(out_dir):
                self.entry_out.insert(0, out_dir)

    def _build_ui(self):
        # Container
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        # --- Header ---
        header_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(header_frame, text="OAS Comparison", 
                     text_color="#0A809E",
                     font=ctk.CTkFont(size=26, weight="bold")).pack(side="left")
        ctk.CTkLabel(header_frame, 
                     text="Comparison and Impact Analysis Dashboard",
                     font=ctk.CTkFont(size=14, slant="italic")).pack(side="left", padx=15, pady=(8, 0))
        
        # Header Separator
        line = ctk.CTkFrame(self.container, height=2, fg_color="#E0E0E0")
        line.pack(fill="x", pady=(0, 20))

        # --- Configuration Card ---
        config_card = ctk.CTkFrame(self.container, corner_radius=12, border_width=1, border_color="#D0DCE0")
        config_card.pack(fill="x", pady=(0, 20), padx=2)
        
        input_grid = ctk.CTkFrame(config_card, fg_color="transparent")
        input_grid.pack(fill="x", padx=10, pady=10)
        input_grid.grid_columnconfigure(1, weight=1)

        # Old Spec
        ctk.CTkLabel(input_grid, text="Old Specification:", width=140, anchor="w").grid(row=0, column=0, padx=10, pady=5)
        self.entry_old = ctk.CTkEntry(input_grid, placeholder_text="Path to the previous version of the OAS...")
        self.entry_old.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        ctk.CTkButton(input_grid, text="Browse", width=80, fg_color="#0A809E", hover_color="#076075",
                      command=lambda: self._browse_file("old")).grid(row=0, column=2, padx=10, pady=5)

        # New Spec
        ctk.CTkLabel(input_grid, text="New Specification:", width=140, anchor="w").grid(row=1, column=0, padx=10, pady=5)
        self.entry_new = ctk.CTkEntry(input_grid, placeholder_text="Path to the current version of the OAS...")
        self.entry_new.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        ctk.CTkButton(input_grid, text="Browse", width=80, fg_color="#0A809E", hover_color="#076075",
                      command=lambda: self._browse_file("new")).grid(row=1, column=2, padx=10, pady=5)

        # Output Dir
        ctk.CTkLabel(input_grid, text="Output Directory:", width=140, anchor="w").grid(row=2, column=0, padx=10, pady=5)
        self.entry_out = ctk.CTkEntry(input_grid, placeholder_text="Folder where reports will be saved...")
        self.entry_out.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        ctk.CTkButton(input_grid, text="Browse", width=80, fg_color="#0A809E", hover_color="#076075",
                      command=self._browse_dir).grid(row=2, column=2, padx=10, pady=5)

        # --- Report Selection Dashboard (4 Columns) ---
        dash_grid = ctk.CTkFrame(self.container, fg_color="transparent")
        dash_grid.pack(fill="x", pady=(0, 20))
        for i in range(4): dash_grid.grid_columnconfigure(i, weight=1)

        # Synthesis Card
        self.var_syn = ctk.BooleanVar(value=True)
        self.card_syn = ctk.CTkFrame(dash_grid, corner_radius=10, border_width=1, border_color="#D0DCE0")
        self.card_syn.grid(row=0, column=0, padx=5, sticky="nsew")
        ctk.CTkCheckBox(self.card_syn, text="Synthesis Report", variable=self.var_syn, 
                        font=ctk.CTkFont(size=13, weight="bold"),
                        fg_color="#0A809E", hover_color="#076075").pack(pady=15)
        self.btn_open_syn = ctk.CTkButton(self.card_syn, text="Open", width=120, height=28,
                                          fg_color="#0A809E", hover_color="#076075", text_color="white",
                                          font=ctk.CTkFont(weight="bold"),
                                          command=lambda: self._open_file("synthesis"))
        self.btn_open_syn.pack_forget()

        # Analytical Card
        self.var_ana = ctk.BooleanVar(value=True)
        self.card_ana = ctk.CTkFrame(dash_grid, corner_radius=10, border_width=1, border_color="#D0DCE0")
        self.card_ana.grid(row=0, column=1, padx=5, sticky="nsew")
        ctk.CTkCheckBox(self.card_ana, text="Analytical Report", variable=self.var_ana,
                        font=ctk.CTkFont(size=13, weight="bold"),
                        fg_color="#0A809E", hover_color="#076075").pack(pady=15)
        self.btn_open_ana = ctk.CTkButton(self.card_ana, text="Open", width=120, height=28,
                                          fg_color="#0A809E", hover_color="#076075", text_color="white",
                                          font=ctk.CTkFont(weight="bold"),
                                          command=lambda: self._open_file("analytical"))
        self.btn_open_ana.pack_forget()

        # Impact Card
        self.var_imp = ctk.BooleanVar(value=True)
        self.card_imp = ctk.CTkFrame(dash_grid, corner_radius=10, border_width=1, border_color="#D0DCE0")
        self.card_imp.grid(row=0, column=2, padx=5, sticky="nsew")
        ctk.CTkCheckBox(self.card_imp, text="Impact Report", variable=self.var_imp,
                        font=ctk.CTkFont(size=13, weight="bold"),
                        fg_color="#0A809E", hover_color="#076075").pack(pady=15)
        self.btn_open_imp = ctk.CTkButton(self.card_imp, text="Open", width=120, height=28,
                                          fg_color="#0A809E", hover_color="#076075", text_color="white",
                                          font=ctk.CTkFont(weight="bold"),
                                          command=lambda: self._open_file("impact"))
        self.btn_open_imp.pack_forget()

        # Compatibility Card
        self.var_com = ctk.BooleanVar(value=True)
        self.card_com = ctk.CTkFrame(dash_grid, corner_radius=10, border_width=1, border_color="#D0DCE0")
        self.card_com.grid(row=0, column=3, padx=5, sticky="nsew")
        ctk.CTkCheckBox(self.card_com, text="Interface Report", variable=self.var_com,
                        font=ctk.CTkFont(size=13, weight="bold"),
                        fg_color="#0A809E", hover_color="#076075").pack(pady=15)

        self.btn_open_com = ctk.CTkButton(self.card_com, text="Open", width=120, height=28,
                                          fg_color="#0A809E", hover_color="#076075", text_color="white",
                                          font=ctk.CTkFont(weight="bold"),
                                          command=lambda: self._open_file("compatibility"))
        self.btn_open_com.pack_forget()

        # --- Primary Action Center ---
        action_center = ctk.CTkFrame(self.container, fg_color="transparent")
        action_center.pack(fill="x", pady=(0, 25))
        
        self.btn_run = ctk.CTkButton(action_center, text="START COMPARISON ENGINE", width=260, height=40,
                                     fg_color="#0A809E", hover_color="#076075",
                                     font=ctk.CTkFont(size=14, weight="bold"),
                                     command=self._start_diff)
        self.btn_run.pack()

        # --- Output Console Card ---
        console_card = ctk.CTkFrame(self.container, corner_radius=12, border_width=1, border_color="#D0DCE0")
        console_card.pack(fill="both", expand=True, padx=2)
        
        console_header = ctk.CTkFrame(console_card, fg_color="transparent", height=30)
        console_header.pack(fill="x", padx=15, pady=(5, 5))
        
        # Font Slider in Header
        slider_frame = ctk.CTkFrame(console_header, fg_color="transparent")
        slider_frame.pack(side="right")
        
        self.lbl_font_size = ctk.CTkLabel(slider_frame, text="11", width=25, font=ctk.CTkFont(size=11))
        self.lbl_font_size.pack(side="right")
        
        self.slider_font = ctk.CTkSlider(slider_frame, from_=8, to=24, number_of_steps=16, width=100, height=16,
                                        button_color="#0A809E", progress_color="#0A809E",
                                        command=self._update_font_size)
        self.slider_font.set(11)
        self.slider_font.pack(side="right", padx=5)
        ctk.CTkLabel(slider_frame, text="Font Size:", font=ctk.CTkFont(size=11)).pack(side="right")

        self.log_area = ctk.CTkTextbox(console_card, font=("Consolas", 11), 
                                      fg_color="#F0F4F5", text_color="#333333",
                                      border_width=0,
                                      wrap="none",
                                      state="disabled")
        self.log_area.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _browse_file(self, target):
        current_path = self.entry_old.get() if target == "old" else self.entry_new.get()
        initial_dir = os.path.dirname(current_path) if current_path and os.path.exists(current_path) else None
        
        path = filedialog.askopenfilename(
            parent=self,
            initialdir=initial_dir,
            title=f"Select {'Old' if target == 'old' else 'New'} OAS File",
            filetypes=[("OAS Files", "*.yaml *.yml *.json")]
        )
        if path:
            if target == "old":
                self.entry_old.delete(0, "end")
                self.entry_old.insert(0, path)
            else:
                self.entry_new.delete(0, "end")
                self.entry_new.insert(0, path)
            self.lift()
            self.focus_force()

    def _browse_dir(self):
        current_path = self.entry_out.get()
        initial_dir = current_path if current_path and os.path.exists(current_path) else None
        
        path = filedialog.askdirectory(parent=self, initialdir=initial_dir, title="Select Output Directory")
        if path:
            self.entry_out.delete(0, "end")
            self.entry_out.insert(0, path)
            self.lift()
            self.focus_force()

    def _on_close(self):
        """Save settings and close window."""
        if self.prefs_manager and self.prefs_manager.get("remember_paths", True):
            self.prefs_manager.update({
                "diff_old_spec": self.entry_old.get(),
                "diff_new_spec": self.entry_new.get(),
                "diff_output_dir": self.entry_out.get()
            })
            self.prefs_manager.save()
        self.destroy()

    def _log(self, msg):
        # 1. Local Log (No timestamp)
        self.log_area.configure(state="normal")
        self.log_area.insert("end", f"{msg}\n")
        self.log_area.see("end")
        self.log_area.configure(state="disabled")
        
        # 2. Application Log (Maintains timestamp via log_app)
        try:
            if hasattr(self.master, 'log_app'):
                self.master.log_app(f"[OAS Comparison] {msg}")
        except:
            pass

    def _update_font_size(self, value):
        size = int(value)
        self.lbl_font_size.configure(text=str(size))
        self.log_area.configure(font=("Consolas", size))

    def _open_file(self, type_key):
        path = self.report_paths.get(type_key)
        if path and os.path.exists(path):
            try:
                os.startfile(path)
            except Exception as e:
                self._log(f"Error opening report: {e}")
        else:
            self._log(f"Error: Report file not found at {path}")

    def _start_diff(self):
        old_p = self.entry_old.get()
        new_p = self.entry_new.get()
        out_d = self.entry_out.get()

        if not all([old_p, new_p, out_d]):
            self._log("Error: All paths are required.")
            return

        if not os.path.exists(old_p) or not os.path.exists(new_p):
            self._log("Error: Specification files not found.")
            return

        # Save paths to preferences
        if self.prefs_manager:
            self.prefs_manager.update({
                "diff_old_spec": old_p,
                "diff_new_spec": new_p,
                "diff_output_dir": out_d
            })

        self.btn_run.configure(state="disabled")
        self.log_area.configure(state="normal")
        self.log_area.delete("1.0", "end")
        self.log_area.configure(state="disabled")
        
        # Reset cards and buttons
        for card in [self.card_syn, self.card_ana, self.card_imp, self.card_com]:
            card.configure(border_color="#D0DCE0", border_width=1)
        
        self.btn_open_syn.pack_forget()
        self.btn_open_ana.pack_forget()
        self.btn_open_imp.pack_forget()
        self.btn_open_com.pack_forget()
        self.report_paths = {"synthesis": None, "analytical": None, "impact": None, "compatibility": None}

        threading.Thread(target=self._run_diff, args=(old_p, new_p, out_d), daemon=True).start()

    def _run_diff(self, old_p, new_p, out_d):
        try:
            self._log("Loading specifications...")
            manager = OASDiffReportManager(old_p, new_p, out_d, self.prefs_manager.get_all())
            
            self._log("Running comparison engine...")
            manager.run_comparison()
            
            report_types = []
            if self.var_syn.get(): report_types.append('synthesis')
            if self.var_ana.get(): report_types.append('analytical')
            if self.var_imp.get(): report_types.append('impact')
            if self.var_com.get(): report_types.append('compatibility')
            
            if not report_types:
                self._log("No report types selected. Comparison finished.")
                return

            self._log(f"Generating {len(report_types)} reports...")
            paths = manager.generate_reports(report_types)
            
            for p in paths:
                self._log(f"Generated: {os.path.basename(p)}")
                
                # Map paths back to buttons based on filename & Highlight cards
                if "Synthesis" in p: 
                    self.report_paths["synthesis"] = p
                    self.after(0, lambda: self.card_syn.configure(border_color="#0A809E", border_width=2))
                    self.after(0, lambda: self.btn_open_syn.pack(pady=(0, 15)))
                elif "Analytical" in p:
                    self.report_paths["analytical"] = p
                    self.after(0, lambda: self.card_ana.configure(border_color="#0A809E", border_width=2))
                    self.after(0, lambda: self.btn_open_ana.pack(pady=(0, 15)))
                elif "Impact" in p:
                    self.report_paths["impact"] = p
                    self.after(0, lambda: self.card_imp.configure(border_color="#0A809E", border_width=2))
                    self.after(0, lambda: self.btn_open_imp.pack(pady=(0, 15)))
                elif "Compatibility" in p:
                    self.report_paths["compatibility"] = p
                    self.after(0, lambda: self.card_com.configure(border_color="#0A809E", border_width=2))
                    self.after(0, lambda: self.btn_open_com.pack(pady=(0, 15)))
            
            self._log("SUCCESS: All operations completed.")
            
        except Exception as e:
            self._log(f"CRITICAL ERROR: {e}")
            import traceback
            print(traceback.format_exc())
        finally:
            self.after(0, lambda: self.btn_run.configure(state="normal"))
