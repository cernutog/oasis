import customtkinter as ctk
from tkinter import filedialog
import os
import threading
from .legacy_converter import LegacyConverter

class CleanFolderDialog(ctk.CTkToplevel):
    def __init__(self, parent, folder_path):
        super().__init__(parent)
        self.folder_path = folder_path
        self.title("Folder Not Empty")
        self.geometry("600x250")
        self.resizable(False, False)
        self.choice = "cancel"

        # Center relative to parent
        self.update_idletasks()
        try:
            x = parent.winfo_x() + (parent.winfo_width() // 2) - 300
            y = parent.winfo_y() + (parent.winfo_height() // 2) - 125
            self.geometry(f"+{int(x)}+{int(y)}")
        except:
            pass

        self.transient(parent)
        self.grab_set()

        # Icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "icon.ico")
        if os.path.exists(icon_path):
            self.after(200, lambda: self.iconbitmap(icon_path))
        
        self._build_ui()

    def _build_ui(self):
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        content_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        content_frame.pack(fill="x", expand=True)

        icon_label = ctk.CTkLabel(content_frame, text="\u26A0", 
                                  text_color="#FBC02D", 
                                  font=ctk.CTkFont(size=52))
        icon_label.pack(side="left", padx=(10, 20))

        msg_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        msg_frame.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(msg_frame, text="The Destination Folder is not empty.", 
                     font=ctk.CTkFont(size=18, weight="bold"),
                     anchor="w", justify="left").pack(fill="x")
        
        # Display the path
        path_label = ctk.CTkLabel(msg_frame, text=self.folder_path, 
                                 font=ctk.CTkFont(size=11), text_color="#0A809E",
                                 anchor="w", justify="left")
        path_label.pack(fill="x", pady=(2, 5))

        ctk.CTkLabel(msg_frame, text="What would you like to do with the existing files?", 
                     font=ctk.CTkFont(size=12), text_color="gray",
                     anchor="w", justify="left").pack(fill="x")

        btn_container = ctk.CTkFrame(main_container, fg_color="transparent")
        btn_container.pack(fill="x", side="bottom", pady=(0, 5))

        row1 = ctk.CTkFrame(btn_container, fg_color="transparent")
        row1.pack(side="top", pady=(0, 10))

        ctk.CTkButton(row1, text="Keep Files", width=120, height=32,
                      command=lambda: self._set_choice("keep")).pack(side="left", padx=5)
        ctk.CTkButton(row1, text="Clear Excel Files", width=140, height=32,
                      command=lambda: self._set_choice("clear_excel")).pack(side="left", padx=5)
        ctk.CTkButton(row1, text="Clear ALL", width=120, height=32,
                      fg_color="#D32F2F", hover_color="#B71C1C",
                      command=lambda: self._set_choice("clear_all")).pack(side="left", padx=5)

        ctk.CTkButton(btn_container, text="Cancel", width=120, height=32,
                      command=lambda: self._set_choice("cancel")).pack(side="top", pady=(0, 5))

    def _set_choice(self, choice):
        self.choice = choice
        self.destroy()

class LegacyConverterDialog(ctk.CTkToplevel):
    def __init__(self, parent, master_dir=None, prefs_manager=None):
        super().__init__(parent)
        self.master_dir = master_dir
        self.prefs_manager = prefs_manager
        self.title("Legacy Template Converter")
        
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
        
        # Remove transient if we want it to be truly independent and allow main window on top
        # self.transient(parent) 
        # self.grab_set() # Do NOT use grab_set to keep it non-modal

        # Focus management
        self.after(300, self.lift)

        # Set icon if exists
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "icon.ico")
        if os.path.exists(icon_path):
            try:
                self.after(400, lambda: self.iconbitmap(icon_path))
            except:
                pass
        
        # Connect to parent
        # self.transient(parent) # REMOVED to allow maximize/minimize on Windows
        
        self._build_ui()
        self._load_saved_paths()

        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self._on_close)


    def _load_saved_paths(self):
        if self.prefs_manager and self.prefs_manager.get("remember_paths", True):
            last_src = self.prefs_manager.get("last_legacy_src", "")
            last_dst = self.prefs_manager.get("last_legacy_dst", "")
            if last_src and os.path.exists(last_src):
                self.entry_src.insert(0, last_src)
            if last_dst and os.path.exists(last_dst):
                self.entry_dst.insert(0, last_dst)
        else:
            print("DEBUG: remember_paths is False or prefs_manager is None")

    def _on_close(self):
        """Save settings and close window."""
        if self.prefs_manager and self.prefs_manager.get("remember_paths", True):
            self.prefs_manager.set("last_legacy_src", self.entry_src.get())
            self.prefs_manager.set("last_legacy_dst", self.entry_dst.get())
            self.prefs_manager.save()
        self.destroy()

    def _build_ui(self):
        # Container
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        # --- Header ---
        header_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(header_frame, text="Legacy Template Converter", 
                     text_color="#0A809E",
                     font=ctk.CTkFont(size=26, weight="bold")).pack(side="left")
        ctk.CTkLabel(header_frame, 
                     text="Convert legacy .xlsm templates to modern Excel format",
                     font=ctk.CTkFont(size=14, slant="italic")).pack(side="left", padx=15, pady=(8, 0))
        
        # Header Separator
        line = ctk.CTkFrame(self.container, height=2, fg_color="#E0E0E0")
        line.pack(fill="x", pady=(0, 20))


        # Input Frame
        input_frame = ctk.CTkFrame(self.container, corner_radius=10)
        input_frame.pack(fill="x", padx=10, pady=10)

        # Folder Selection
        # Source
        src_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        src_frame.pack(fill="x", pady=10, padx=15)
        ctk.CTkLabel(src_frame, text="Source Folder (Legacy):", width=160, anchor="w").pack(side="left")
        self.entry_src = ctk.CTkEntry(src_frame, placeholder_text="Path to legacy templates folder...")
        self.entry_src.pack(side="left", fill="x", expand=True, padx=5)
        ctk.CTkButton(src_frame, text="Browse", width=80, 
                      fg_color="#0A809E", hover_color="#076075",
                      command=self._browse_src).pack(side="left")

        # Destination
        dst_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        dst_frame.pack(fill="x", pady=(0, 10), padx=15)
        ctk.CTkLabel(dst_frame, text="Destination Folder:", width=160, anchor="w").pack(side="left")
        self.entry_dst = ctk.CTkEntry(dst_frame, placeholder_text="Path where converted templates will be saved...")
        self.entry_dst.pack(side="left", fill="x", expand=True, padx=5)
        ctk.CTkButton(dst_frame, text="Browse", width=80, 
                      fg_color="#0A809E", hover_color="#076075",
                      command=self._browse_dst).pack(side="left")


        # Options Frame
        opts_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        opts_frame.pack(fill="x", pady=5, padx=10)
        
        self.var_tracing = ctk.BooleanVar(value=True)
        if self.prefs_manager:
            self.var_tracing.set(self.prefs_manager.get("tools_legacy_tracing_enabled", True))
            
        self.chk_tracing = ctk.CTkCheckBox(opts_frame, text="Enable Schema Tracing (Collision analysis in log)", 
                                           variable=self.var_tracing,
                                           fg_color="#0A809E", # Fill color when checked
                                           hover_color="#076075",
                                           font=ctk.CTkFont(size=12))
        self.chk_tracing.pack(side="left", padx=15)

        # Action Buttons Frame
        btn_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        btn_frame.pack(pady=10)

        self.btn_convert = ctk.CTkButton(btn_frame, text="Start Conversion", 
                                        fg_color="#0A809E", hover_color="#076075",
                                        font=ctk.CTkFont(weight="bold"),
                                        command=self._start_conversion)
        self.btn_convert.pack(side="left", padx=10)

        self.btn_open_folder = ctk.CTkButton(btn_frame, text="Open Output Folder", 
                                            fg_color="transparent", border_width=2,
                                            border_color="#0A809E", text_color="#0A809E",
                                            font=ctk.CTkFont(weight="bold"),
                                            hover_color="#E0F0F3",
                                            state="disabled",
                                            command=self._open_output_folder)
        self.btn_open_folder.pack(side="left", padx=10)

        # Progress/Logs
        self.log_area = ctk.CTkTextbox(self.container, font=("Consolas", 11), 
                                      fg_color="#F0F4F5", text_color="#333333",
                                      wrap="none", # Important for table alignment
                                      state="disabled")
        self.log_area.pack(fill="both", expand=True, pady=(10, 0))

    def _get_initial_dir(self, entry_widget):
        """Returns the folder from entry if it exists, otherwise cwd."""
        p = entry_widget.get()
        if p and os.path.exists(p):
            return p if os.path.isdir(p) else os.path.dirname(p)
        return os.getcwd()

    def _browse_src(self):
        initial = self._get_initial_dir(self.entry_src)
        p = filedialog.askdirectory(parent=self, initialdir=initial, title="Select Legacy Templates Folder")
        if p:
            self.lift()
            self.focus_force()
            p = p.replace("\\", "/") # Use forward slashes for consistency in JSON
            self.entry_src.delete(0, "end")
            self.entry_src.insert(0, p)
            if not self.entry_dst.get():
                target_dst = os.path.join(os.path.dirname(p), "Converted Templates").replace("\\", "/")
                self.entry_dst.insert(0, target_dst)
            
            # Save immediately
            if self.prefs_manager and self.prefs_manager.get("remember_paths", True):
                self.prefs_manager.set("last_legacy_src", p)
                self.prefs_manager.set("last_legacy_dst", self.entry_dst.get())
                self.prefs_manager.save()
                print(f"DEBUG: Saved src='{p}', dst='{self.entry_dst.get()}'")

    def _browse_dst(self):
        initial = self._get_initial_dir(self.entry_dst)
        p = filedialog.askdirectory(parent=self, initialdir=initial, title="Select Destination Folder")
        if p:
            self.lift()
            self.focus_force()
            p = p.replace("\\", "/") # Use forward slashes for consistency in JSON
            self.entry_dst.delete(0, "end")
            self.entry_dst.insert(0, p)

            # Save immediately
            if self.prefs_manager and self.prefs_manager.get("remember_paths", True):
                self.prefs_manager.set("last_legacy_dst", p)
                self.prefs_manager.save()
                print(f"DEBUG: Saved dst='{p}'")


    def _open_output_folder(self):
        dst = self.entry_dst.get()
        if dst and os.path.exists(dst):
            os.startfile(dst)

    def _log(self, msg):
        self.log_area.configure(state="normal")
        self.log_area.insert("end", f"{msg}\n")
        self.log_area.see("end")
        self.log_area.configure(state="disabled")

    def _start_conversion(self):
        src = self.entry_src.get()
        dst = self.entry_dst.get()

        if not src or not os.path.exists(src):
            self._log("Error: Invalid source folder.")
            return
        if not dst:
            self._log("Error: Destination folder is required.")
            return

        # Check if destination is empty
        if os.path.exists(dst) and os.listdir(dst):
            self._log(f"Checking destination folder: {dst}")
            choice = self._show_clean_folder_dialog(dst)
            if choice == "cancel":
                return
            
            if not self._clean_destination(dst, choice):
                return

        # Save paths if remembered
        if self.prefs_manager and self.prefs_manager.get("remember_paths", True):
            self.prefs_manager.set("last_legacy_src", src)
            self.prefs_manager.set("last_legacy_dst", dst)
            self.prefs_manager.save()

        self.btn_convert.configure(state="disabled")
        self.btn_open_folder.configure(state="disabled")
        self.log_area.configure(state="normal")
        self.log_area.delete("1.0", "end")
        self.log_area.configure(state="disabled")

        threading.Thread(target=self._run_conversion, args=(src, dst), daemon=True).start()

    def _show_clean_folder_dialog(self, folder_path):
        dialog = CleanFolderDialog(self, folder_path)
        self.wait_window(dialog)
        return dialog.choice

    def _clean_destination(self, folder, choice):
        try:
            if choice == "keep":
                return True
            import shutil
            import glob
            if choice == "clear_all":
                self._log(f"Cleaning ALL files in {folder}...")
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
            elif choice == "clear_excel":
                self._log(f"Cleaning Excel files in {folder}...")
                for pat in ["*.xlsx", "*.xlsm"]:
                    for f in glob.glob(os.path.join(folder, pat)):
                        os.remove(f)
            return True
        except Exception as e:
            self._log(f"Error cleaning folder: {e}")
            return False

    def _run_conversion(self, src, dst):
        try:
            tracing = self.var_tracing.get()
            self._log(f"Starting conversion from {src} to {dst}...")
            include_desc = False
            include_ex = False
            capitalize_schemas = True
            if self.prefs_manager:
                include_desc = bool(self.prefs_manager.get("tools_legacy_collision_include_descriptions", False))
                include_ex = bool(self.prefs_manager.get("tools_legacy_collision_include_examples", False))
                capitalize_schemas = bool(self.prefs_manager.get("tools_legacy_capitalize_schema_names", True))

            converter = LegacyConverter(
                src,
                dst,
                log_callback=self._log,
                include_descriptions_in_collision=include_desc,
                include_examples_in_collision=include_ex,
                capitalize_schema_names=capitalize_schemas,
            )
            success = converter.convert(tracing_enabled=tracing)
            
            if success:
                self._log("\nCONVERSION COMPLETED SUCCESSFULLY.")
                
                # SYNC: Update main application input folder
                if hasattr(self.master, "entry_dir"):
                    self.master.entry_dir.delete(0, "end")
                    self.master.entry_dir.insert(0, dst)
                    if hasattr(self.master, "prefs_manager"):
                        self.master.prefs_manager.set("last_excel_input", dst)
                        self.master.prefs_manager.save()
                    self._log(f"Synced path to Generation tab: {dst}")

                self.after(0, lambda: self.btn_open_folder.configure(
                    state="normal", 
                    fg_color="#0A809E", 
                    text_color="white", 
                    hover_color="#076075",
                    border_width=0
                ))
            else:
                self._log("\nCONVERSION FAILED.")
            
        except Exception as e:
            self._log(f"\nCRITICAL ERROR: {e}")
        finally:
            self.after(0, lambda: self.btn_convert.configure(state="normal"))
