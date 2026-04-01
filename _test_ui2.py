import customtkinter as ctk
from src.legacy_converter_dialog import LegacyConverterDialog
from src.legacy_schema_tracer_dialog import LegacySchemaTracerDialog

root = ctk.CTk()
root.geometry("1200x800")
root.title("UI Test")

main_frame = ctk.CTkFrame(root, fg_color="transparent")
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

left_frame = ctk.CTkFrame(main_frame)
left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

right_frame = ctk.CTkFrame(main_frame)
right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))

ctk.CTkButton(left_frame, text="Open Legacy Converter", command=lambda: LegacyConverterDialog(root)).pack(pady=20)
ctk.CTkButton(right_frame, text="Open Schema Tracer", command=lambda: LegacySchemaTracerDialog(root)).pack(pady=20)

root.mainloop()
