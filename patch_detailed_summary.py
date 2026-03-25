import os
import re

fname_a = r'c:\Users\giuse\.gemini\antigravity\scratch\OASIS\src\oas_diff\compatibility_analyzer.py'
with open(fname_a, 'r', encoding='utf-8') as f:
    text_a = f.read()

text_a = text_a.replace(
    'self.issues.append(CompatibilityIssue(path, method, "Request Body", "-", "Constraint Mismatch", f"Property \'required\' changed from {req1} to {req2}"))',
    'self.issues.append(CompatibilityIssue(path, method, "Request Body", "-", "Constraint Mismatch", f"Property \'required\' changed from {req1} to {req2}\", schema_name=\"Request Body\"))'
)

with open(fname_a, 'w', encoding='utf-8') as f:
    f.write(text_a)



print("Patching generator for Detailed Grouping on Scope...")
fname_g = r'c:\Users\giuse\.gemini\antigravity\scratch\OASIS\src\oas_diff\generators\compatibility_generator.py'
with open(fname_g, 'r', encoding='utf-8') as f:
    text_g = f.read()

# 1. Swap Column text and widths
old_widths_swap = 'widths_s = [Inches(0.5), Inches(1.4), Inches(1.4), Inches(2.9), Inches(0.8)]'
new_widths_swap = 'widths_s = [Inches(0.5), Inches(1.4), Inches(1.4), Inches(2.7), Inches(1.0)]' # Scale Frequency to 1.0 to fit
text_g = text_g.replace(old_widths_swap, new_widths_swap)

old_headers = """        hdr[0].text = '#'
        hdr[1].text = 'Issue Type'
        hdr[2].text = 'Scope'
        hdr[3].text = 'Details'
        hdr[4].text = 'Frequency'"""

new_headers = """        hdr[0].text = '#'
        hdr[1].text = 'Scope'
        hdr[2].text = 'Issue Type'
        hdr[3].text = 'Details'
        hdr[4].text = 'Frequency'"""

text_g = text_g.replace(old_headers, new_headers)

# 2. Update freq to aggregate strictly by Scope
old_freq_agg = """        freq = {}
        schema_map = {}
        for issue in self.issues:
             key = (issue.issue_type, issue.details, issue.old_val, issue.new_val)
             freq[key] = freq.get(key, 0) + 1
             if key not in schema_map: schema_map[key] = set()
             schema_map[key].add(issue.schema_name)"""

new_freq_agg = """        freq = {}
        details_map = {}
        for issue in self.issues:
             scope = issue.schema_name if issue.schema_name else "-"
             freq[scope] = freq.get(scope, 0) + 1
             if scope not in details_map: details_map[scope] = []
             details_map[scope].append(issue)"""

text_g = text_g.replace(old_freq_agg, new_freq_agg)

# 3. Update body generator loop
old_freq_loop = """        issue_id_map = {}
        for idx, (key, count) in enumerate(sorted_freq):
             issue_type, details, old_val, new_val = key
             issue_id_map[key] = idx + 1
             row = table.add_row().cells
             row[0].text = f"[{idx + 1}]"
             row[1].text = issue_type
             
             s_list = sorted(list(schema_map[key]))
             if len(s_list) > 3: row[2].text = ", ".join(s_list[:3]) + "..."
             else: row[2].text = ", ".join(s_list)
             
             row[3].text = ""
             p_det = row[3].paragraphs[0]
             p_det.text = details
             if old_val is not None or new_val is not None:
                 p_old = row[3].add_paragraph()
                 p_old.add_run("Old:").italic = True
                 p_old.add_run(" ")
                 p_new = row[3].add_paragraph()
                 p_new.add_run("New:").italic = True
                 p_new.add_run(" ")
                 ov = "<None>" if not old_val or str(old_val).strip() in ("", "None") else str(old_val)
                 nv = "<None>" if not new_val or str(new_val).strip() in ("", "None") else str(new_val)
                 self._render_rich_diff(p_old, p_new, ov, nv)
             
             row[4].text = str(count)"""

new_freq_loop = """        issue_id_map = {}
        for idx, (scope, count) in enumerate(sorted_freq):
             issue_id_map[scope] = idx + 1
             row = table.add_row().cells
             row[0].text = f"[{idx + 1}]"
             row[1].text = scope
             
             # Aggregate types
             types = sorted(list(set([i.issue_type for i in details_map[scope]])))
             row[2].text = ", ".join(types)
             
             row[3].text = "" # Clear anything default
             p_det = row[3].paragraphs[0] if len(row[3].paragraphs) > 0 else row[3].add_paragraph()
             
             # Dedup items in Scope before list
             dedup_dict = {}
             for iss in details_map[scope]:
                  dk = (iss.details, iss.old_val, iss.new_val)
                  if dk not in dedup_dict: dedup_dict[dk] = iss
             
             for j_idx, iss in enumerate(dedup_dict.values()):
                  p_item = p_det if j_idx == 0 else row[3].add_paragraph()
                  p_item.text = f"• {iss.details}"
                  
                  if iss.old_val is not None or iss.new_val is not None:
                       p_old = row[3].add_paragraph()
                       p_old.add_run("    Old:").italic = True
                       p_old.add_run(" ")
                       
                       p_new = row[3].add_paragraph()
                       p_new.add_run("    New:").italic = True
                       p_new.add_run(" ")
                       
                       ov = "<None>" if not iss.old_val or str(iss.old_val).strip() in ("", "None") else str(iss.old_val)
                       nv = "<None>" if not iss.new_val or str(iss.new_val).strip() in ("", "None") else str(iss.new_val)
                       self._render_rich_diff(p_old, p_new, ov, nv)
                       
             row[4].text = str(count)"""

text_g = text_g.replace(old_freq_loop, new_freq_loop)

# 4. Update Detailed details loop to map with key=scope instead of issue keys
old_idx_fetch = """                       key = (iss.issue_type, iss.details, iss.old_val, iss.new_val)
                       map_idx = issue_id_map.get(key, "")"""

new_idx_fetch = """                       key = iss.schema_name if iss.schema_name else "-"
                       map_idx = issue_id_map.get(key, "")"""

text_g = text_g.replace(old_idx_fetch, new_idx_fetch)

if new_freq_loop not in text_g: print("FAILED PATCHING LOOP")

with open(fname_g, 'w', encoding='utf-8') as f:
    f.write(text_g)

print('Done restructure patch')
