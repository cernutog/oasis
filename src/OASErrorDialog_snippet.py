
class OASErrorDialog(ctk.CTkToplevel):
    """Custom error dialog with consistent Petrol Blue styling."""
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.title(title)
        self.geometry("450x200") 
        self.resizable(False, False)
        
        # Center relative to parent
        self.update_idletasks()
        try:
            x = parent.winfo_x() + (parent.winfo_width() // 2) - 225
            y = parent.winfo_y() + (parent.winfo_height() // 2) - 100
            self.geometry(f"+{int(x)}+{int(y)}")
        except:
            pass

        self.transient(parent)
        self.grab_set()

        # Icon setup
        self.after(200, self._set_icon)
        
        self._build_ui(message)

    def _get_resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def _set_icon(self):
        try:
            icon_path = "icon.ico"
            if not os.path.exists(icon_path):
                icon_path = self._get_resource_path("icon.ico")
            if os.path.exists(icon_path):
                try:
                    self.iconbitmap(icon_path)
                    self.wm_iconbitmap(icon_path)
                except:
                    pass
        except:
            pass

    def _build_ui(self, message):
        # Main Container - Center everything
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.place(relx=0.5, rely=0.5, anchor="center")

        # Content Block (Icon + Text) - Row Layout
        content_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        content_frame.pack(pady=(0, 20))

        # Icon - Red X
        icon_label = ctk.CTkLabel(content_frame, text="\u274C", 
                                  text_color="#D32F2F", 
                                  font=ctk.CTkFont(size=48))
        icon_label.pack(side="left", padx=(0, 15))

        # Message Area
        msg_label = ctk.CTkLabel(content_frame, text=message, 
                                 font=ctk.CTkFont(size=14, weight="bold"),
                                 text_color=("black", "white"),
                                 wraplength=300,
                                 justify="left")
        msg_label.pack(side="left")

        # Button Area
        # HARDCODED PETROL BLUE
        ctk.CTkButton(self, text="OK (Fixed)", width=120, height=32,
                      fg_color="#0A809E", hover_color="#076075",
                      command=self.destroy).pack(side="bottom", pady=20)
