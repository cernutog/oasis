import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import threading
import os
import sys

# Ensure imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import main as main_script
from linter import SpectralRunner
from charts import PieChart

# Set Theme
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class OASGenApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("OAS Generation Tool")
        self.geometry("900x650") # Increased size for charts

        # Set Window Icon
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
        if not os.path.exists(icon_path):
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "icon.ico")
        
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass 
        
        # Grid Layout Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) # Tabview expands

        # --- Header ---
        self.frame_header = ctk.CTkFrame(self, corner_radius=0)
        self.frame_header.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        
        self.lbl_title = ctk.CTkLabel(self.frame_header, text="OAS Generator", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_title.pack(padx=20, pady=15, side="left")
        
        self.lbl_version = ctk.CTkLabel(self.frame_header, text="v1.1", font=ctk.CTkFont(size=12))
        self.lbl_version.pack(padx=20, pady=15, side="right")

        # --- Tab View ---
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        self.tab_gen = self.tabview.add("Generation")
        self.tab_val = self.tabview.add("Validation")

        # ==========================
        # TAB 1: GENERATION
        # ==========================
        self.tab_gen.grid_columnconfigure(0, weight=1)
        self.tab_gen.grid_rowconfigure(2, weight=1) # Log expands

        # Controls
        self.frame_controls = ctk.CTkFrame(self.tab_gen, fg_color="transparent")
        self.frame_controls.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.frame_controls.grid_columnconfigure(1, weight=1)

        self.lbl_dir = ctk.CTkLabel(self.frame_controls, text="Template Directory:")
        self.lbl_dir.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.entry_dir = ctk.CTkEntry(self.frame_controls, placeholder_text="Path to API Templates...")
        self.entry_dir.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ew")
        
        # Default Path Logic
        default_path = os.path.join(os.getcwd(), "..", "API Templates")
        if os.path.exists(default_path):
             self.entry_dir.insert(0, os.path.abspath(default_path))
        else:
             self.entry_dir.insert(0, os.getcwd())

        self.btn_browse = ctk.CTkButton(self.frame_controls, text="Browse", width=100, command=self.browse_dir)
        self.btn_browse.grid(row=0, column=2, padx=10, pady=10)

        # Options
        self.frame_opts = ctk.CTkFrame(self.tab_gen, fg_color="transparent")
        self.frame_opts.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 10))

        self.var_30 = ctk.BooleanVar(value=True)
        self.chk_30 = ctk.CTkCheckBox(self.frame_opts, text="Generate OAS 3.0", variable=self.var_30)
        self.chk_30.pack(side="left", padx=(0, 20))
        
        self.var_31 = ctk.BooleanVar(value=True)
        self.chk_31 = ctk.CTkCheckBox(self.frame_opts, text="Generate OAS 3.1", variable=self.var_31)
        self.chk_31.pack(side="left")

        # Generate Button layout on the right of opts? Or below? Below logs? 
        # Let's keep it prominent.
        self.btn_gen = ctk.CTkButton(self.frame_opts, text="GENERATE", font=ctk.CTkFont(weight="bold"), width=150, command=self.start_generation)
        self.btn_gen.pack(side="left", padx=40)

        # Log Area
        self.log_area = ctk.CTkTextbox(self.tab_gen)
        self.log_area.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.log_area.insert("0.0", "Ready to generate.\n")
        self.log_area.configure(state="disabled")

        # ==========================
        # TAB 2: VALIDATION
        # ==========================
        self.linter = SpectralRunner() # Initialized here
        
        self.tab_val.grid_columnconfigure(0, weight=1) # List
        self.tab_val.grid_columnconfigure(1, weight=1) # Chart
        self.tab_val.grid_rowconfigure(1, weight=1)

        # Top Bar
        self.frame_val_top = ctk.CTkFrame(self.tab_val, fg_color="transparent")
        self.frame_val_top.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        # File Selector
        self.lbl_sel = ctk.CTkLabel(self.frame_val_top, text="Select File:", font=ctk.CTkFont(weight="bold"))
        self.lbl_sel.grid(row=0, column=0, padx=(0, 10))

        self.file_map = {} 
        self.cbo_files = ctk.CTkComboBox(self.frame_val_top, width=300, values=["No OAS files found"], command=self.on_file_select)
        self.cbo_files.grid(row=0, column=1, sticky="w")
        
        # Refresh Button
        self.btn_lint = ctk.CTkButton(self.frame_val_top, text="↻ Refresh", width=80, command=self.run_validation)
        self.btn_lint.grid(row=0, column=2, padx=(10, 0))

        # Progress Bar (Indeterminate)
        self.progress_val = ctk.CTkProgressBar(self.frame_val_top, width=200, mode="indeterminate")
        self.progress_val.grid(row=0, column=3, padx=(20, 0), sticky="w")
        self.progress_val.set(0) # Hide initially

        # Main Layout: List vs Chart
        self.frame_val_content = ctk.CTkFrame(self.tab_val, fg_color="transparent")
        self.frame_val_content.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10)
        self.frame_val_content.grid_columnconfigure(0, weight=1)
        self.frame_val_content.grid_columnconfigure(1, weight=1)
        self.frame_val_content.grid_rowconfigure(0, weight=3) # Content takes most space
        self.frame_val_content.grid_rowconfigure(1, weight=1) # Log console takes less

        self.frame_list = ctk.CTkScrollableFrame(self.frame_val_content, label_text="Issues List")
        self.frame_list.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=5)
        
        self.frame_chart_container = ctk.CTkFrame(self.frame_val_content)
        self.frame_chart_container.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=5)
        self.chart = PieChart(self.frame_chart_container)
        self.chart.pack(fill="both", expand=True, padx=10, pady=10)

        # Log Console (Collapsed by default)
        
        self.btn_toggle_log = ctk.CTkButton(self.frame_val_top, text="Show Logs", width=80, fg_color="gray", command=self.toggle_log)
        self.btn_toggle_log.grid(row=0, column=4, padx=(10, 0))

        self.val_log_frame = ctk.CTkFrame(self.frame_val_content, height=100)
        self.val_log = ctk.CTkTextbox(self.val_log_frame, height=100, state="disabled", font=("Consolas", 11))
        self.val_log.pack(fill="both", expand=True)
        
        # Grid it initially? No, hide it.
        # self.val_log_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(10, 0))
        self.log_visible = False
        
        self.val_log_print("Ready.")
        
    def toggle_log(self):
        if self.log_visible:
            self.val_log_frame.grid_forget()
            self.btn_toggle_log.configure(text="Show Logs")
            self.log_visible = False
        else:
            self.val_log_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(10, 0))
            self.btn_toggle_log.configure(text="Hide Logs")
            self.log_visible = True

    def val_log_print(self, msg):
        self.val_log.configure(state="normal")
        self.val_log.insert("end", f"> {msg}\n")
        self.val_log.see("end")
        self.val_log.configure(state="disabled")

    # ... existing methods ...

    def show_results(self, result):
        if not result['success']:
            self.val_log_print(f"Error: {result.get('error_msg', 'Unknown Error')}")
            self.frame_list.configure(label_text="Error")
            # Clear previous
            for widget in self.frame_list.winfo_children(): widget.destroy()
            
            err_lbl = ctk.CTkLabel(self.frame_list, text=result.get('error_msg', 'Unknown Error'), text_color="red")
            err_lbl.pack()
            return

        summary = result['summary']
        code_summary = result.get('code_summary', summary) # Fallback if missing
        details = result['details']
        total_issues = len(details)
        
        self.val_log_print(f"Check Complete: {total_issues} issues found.")
        self.frame_list.configure(label_text=f"Issues ({total_issues})")
        
        # Update Chart - Use code_summary for detailed breakdown
        self.chart.set_data(code_summary)

        # Populate List
        for widget in self.frame_list.winfo_children(): widget.destroy()

        if total_issues == 0:
             ctk.CTkLabel(self.frame_list, text="No issues found! Great job!", text_color="green", font=("Arial", 16)).pack(pady=20)
        else:
            for item in details:
                # Severity Color
                color = "gray"
                if item['severity'] == "error": color = "#FF4444"
                elif item['severity'] == "warning": color = "#FFBB33"
                elif item['severity'] == "info": color = "#33B5E5"
                
                # Card Frame
                card = ctk.CTkFrame(self.frame_list, border_width=1, border_color="gray")
                card.pack(fill="x", pady=2, padx=2)
                
                # Row 1: Code + Severity
                r1 = ctk.CTkFrame(card, fg_color="transparent")
                r1.pack(fill="x", padx=5, pady=2)
                ctk.CTkLabel(r1, text=f"[{item['severity'].upper()}]", text_color=color, font=("Arial", 11, "bold")).pack(side="left")
                ctk.CTkLabel(r1, text=item['code'], font=("Arial", 11, "bold")).pack(side="left", padx=5)
                ctk.CTkLabel(r1, text=f"Line: {item['line']}", text_color="gray", font=("Arial", 10)).pack(side="right")
                
                # Row 2: Path
                if item['path'] and item['path'] != "Root":
                     ctk.CTkLabel(card, text=f"Path: {item['path']}", text_color="silver", font=("Consolas", 10), anchor="w").pack(fill="x", padx=5)

                # Row 3: Message
                ctk.CTkLabel(card, text=item['message'], anchor="w", justify="left", wraplength=350).pack(fill="x", padx=5, pady=(0, 5))

    
if __name__ == "__main__":
    app = OASGenApp()
    app.mainloop()

