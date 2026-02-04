
import pandas as pd
import os
import sys

# Add src to path
sys.path.append(os.path.abspath("src"))
from legacy_converter import LegacyConverter

legacy_dir = r"c:\Users\giuse\.gemini\antigravity\scratch\OASIS\Templates Legacy"
output_dir = r"c:\Users\giuse\.gemini\antigravity\scratch\OASIS\Templates Converted Test"

class Reporter(LegacyConverter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema_sources = {} # SchemaName -> Set(FileName)

    def _process_data_type_sheet(self, df_dt, source_file):
        # Heuristic to find header
        header_row_idx = -1
        keywords = ["data type", "type", "description", "example", "format"]
        for idx, row in df_dt.head(10).iterrows():
            row_vals = [str(v).strip().lower() for v in row.values]
            match_count = sum(1 for kw in keywords if kw in row_vals)
            if match_count >= 2:
                header_row_idx = idx
                break
        
        if header_row_idx != -1:
            df_dt.columns = [str(c).strip() for c in df_dt.iloc[header_row_idx]]
            df_dt = df_dt.iloc[header_row_idx+1:].reset_index(drop=True)
        else:
            df_dt.columns = [str(c).strip() for c in df_dt.iloc[0]]
            df_dt = df_dt.iloc[1:].reset_index(drop=True)
        
        for _, row in df_dt.iterrows():
            row_vals = row.values.tolist()
            if len(row_vals) < 2: continue
            name = str(row_vals[0]).strip()
            if not name or name.lower() in ["nan", "data type", "track changes", "description"]:
                continue
            
            # Attributes for collision tracking
            attrs = {
                "type": str(row.get("Type", row_vals[2] if len(row_vals)>2 else "")).strip(),
                "format": str(row.get("Format", "")).strip(),
                "items_type": str(row.get("Items Data Type \n(Array only)", "")).strip(),
                "min": str(row.get("Min  \nValue/Length/Item", "")).strip(),
                "max": str(row.get("Max  \nValue/Length/Item", "")).strip(),
                "pattern": str(row.get("PatternEba", "")).strip() or str(row.get("Regex", "")).strip(),
                "allowed_values": str(row.get("Allowed value", "")).strip(),
                "example": str(row.get("Example", "")).strip()
            }
            attrs_tuple = tuple(sorted(attrs.items()))
            
            # Global name resolution (collision logic)
            final_name = name
            if name not in self.schema_collision_map:
                self.schema_collision_map[name] = {attrs_tuple: name}
                self.global_schemas[name] = attrs
            else:
                if attrs_tuple not in self.schema_collision_map[name]:
                    count = 1
                    while f"{name}{count}" in self.global_schemas: count += 1
                    final_name = f"{name}{count}"
                    self.schema_collision_map[name][attrs_tuple] = final_name
                    self.global_schemas[final_name] = attrs
                else:
                    final_name = self.schema_collision_map[name][attrs_tuple]
            
            if final_name not in self.schema_sources:
                self.schema_sources[final_name] = set()
            self.schema_sources[final_name].add(source_file)

    def generate_report(self):
        self.convert() # Runs the passes
        
        unused = sorted([s for s in self.global_schemas if s not in self.used_global_schemas])
        
        report = []
        for s in unused:
            files = sorted(list(self.schema_sources.get(s, ["Unknown"])))
            report.append(f"- **{s}**: {', '.join(files)}")
        
        return report

rep = Reporter(legacy_dir, output_dir, log_callback=None)
results = rep.generate_report()

print("\n".join(results))
