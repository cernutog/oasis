import os
import re

print("Patching Analyzer...")
fname = r'c:\Users\giuse\.gemini\antigravity\scratch\OASIS\src\oas_diff\compatibility_analyzer.py'
with open(fname, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Dataclass
text = text.replace('    severity: str = "HIGH" # Can be added for sorting', '    severity: str = "HIGH" # Can be added for sorting\n    old_val: Any = None\n    new_val: Any = None')

# 2. _analyze_operation
old_d_op = 'self.issues.append(CompatibilityIssue(path, method, "Operation", "description", "Description Change", f"From:\\n{d1}\\n\\nTo:\\n{d2}", severity="INFO"))'
new_d_op = 'self.issues.append(CompatibilityIssue(path, method, "Operation", "description", "Description Change", "Description changed", severity="INFO", old_val=d1, new_val=d2))'
text = text.replace(old_d_op, new_d_op)
if new_d_op not in text: print("Failed patch 2")

# 3. _compare_parameters
old_d_param = 'self.issues.append(CompatibilityIssue(path, method, f"Parameter ({location})", name, "Description Change", f"From:\\n{d1}\\n\\nTo:\\n{d2}", severity="INFO"))'
new_d_param = 'self.issues.append(CompatibilityIssue(path, method, f"Parameter ({location})", name, "Description Change", "Description changed", severity="INFO", old_val=d1, new_val=d2))'
text = text.replace(old_d_param, new_d_param)
if new_d_param not in text: print("Failed patch 3")

# 4. _compare_schemas enum order
old_e_order = 'self.issues.append(CompatibilityIssue(path, method, location, item_name_prefix, "Enum values order changed", f"Constraint \'enum\' changed from {v1} to {v2}", severity="INFO"))'
new_e_order = 'self.issues.append(CompatibilityIssue(path, method, location, item_name_prefix, "Enum values order changed", f"Constraint \'enum\' order changed", severity="INFO", old_val=str(v1), new_val=str(v2)))'
text = text.replace(old_e_order, new_e_order)
if new_e_order not in text: print("Failed patch 4")

# 5. _compare_schemas description constraint
old_d_cons = 'self.issues.append(CompatibilityIssue(path, method, location, item_name_prefix, "Description Change", f"From:\\n{v1}\\n\\nTo:\\n{v2}", severity="INFO"))'
new_d_cons = 'self.issues.append(CompatibilityIssue(path, method, location, item_name_prefix, "Description Change", "Description changed", severity="INFO", old_val=str(v1 or "").strip(), new_val=str(v2 or "").strip()))'
text = text.replace(old_d_cons, new_d_cons)
if new_d_cons not in text: print("Failed patch 5")

# 6. _compare_schemas generic constraint
old_g_cons = 'self.issues.append(CompatibilityIssue(path, method, location, item_name_prefix, "Constraint Mismatch", f"Constraint \'{c}\' changed from {v1} to {v2}"))'
new_g_cons = 'self.issues.append(CompatibilityIssue(path, method, location, item_name_prefix, "Constraint Mismatch", f"Constraint \'{c}\' changed", old_val=str(v1), new_val=str(v2)))'
text = text.replace(old_g_cons, new_g_cons)
if new_g_cons not in text: print("Failed patch 6")

with open(fname, 'w', encoding='utf-8') as f:
    f.write(text)

print('Analyzer patched')


print("Patching Generator...")
fname = r'c:\Users\giuse\.gemini\antigravity\scratch\OASIS\src\oas_diff\generators\compatibility_generator.py'
with open(fname, 'r', encoding='utf-8') as f:
    text = f.read()

rich_diff_src = """

    def _apply_shading(self, run, color_hex):
        R_PR_ORDER = ['w:rStyle', 'w:rFonts', 'w:b', 'w:bCs', 'w:i', 'w:iCs', 'w:caps', 'w:smallCaps', 'w:strike', 'w:dstrike', 'w:outline', 'w:shadow', 'w:emboss', 'w:imprint', 'w:noProof', 'w:snapToGrid', 'w:vanish', 'w:webHidden', 'w:color', 'w:spacing', 'w:w', 'w:kern', 'w:position', 'w:sz', 'w:szCs', 'w:highlight', 'w:u', 'w:effect', 'w:bdr', 'w:shd', 'w:fitText', 'w:vertAlign', 'w:rtl', 'w:cs', 'w:em', 'w:lang', 'w:eastAsianLayout', 'w:specVanish', 'w:oMath']
        rPr = run._r.get_or_add_rPr()
        shd = get_or_add_child(rPr, 'w:shd', R_PR_ORDER)
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:fill'), color_hex)

    def _render_rich_diff(self, para_old, para_new, t_old, t_new):
        import difflib
        import re
        
        if not isinstance(t_old, str): t_old = str(t_old or "")
        if not isinstance(t_new, str): t_new = str(t_new or "")
        
        def split_words(text):
            return re.findall(r'\\w+|[^\\w\\s]|\\s+', text)
            
        w_old = split_words(t_old)
        w_new = split_words(t_new)
        ws = difflib.SequenceMatcher(None, w_old, w_new, autojunk=False)
        
        for wt, wi1, wi2, wj1, wj2 in ws.get_opcodes():
            txt_o = "".join(w_old[wi1:wi2])
            txt_n = "".join(w_new[wj1:wj2])
            if wt == 'equal':
                para_old.add_run(txt_o)
                para_new.add_run(txt_n)
            elif wt == 'replace':
                self._apply_shading(para_old.add_run(txt_o), "FFF3CD")  # Yellow
                self._apply_shading(para_new.add_run(txt_n), "FFF3CD")
            elif wt == 'delete':
                self._apply_shading(para_old.add_run(txt_o), "F8D7DA")  # Red
            elif wt == 'insert':
                self._apply_shading(para_new.add_run(txt_n), "D4EDDA")  # Green
"""

text = text.replace('    def _add_metadata_table(self):', rich_diff_src + '\n    def _add_metadata_table(self):')


old_issue_grouping_loop = '''             # Group by (location, item_name)
             dedup = {}
             dedup = {}
             for issue in issues:
                  k = (issue.location, issue.item_name)
                  if k not in dedup:
                       dedup[k] = []
                  pair = (issue.issue_type, issue.details)
                  if pair not in dedup[k]:
                       dedup[k].append(pair)'''

new_issue_grouping_loop = '''             # Group by (location, item_name)
             dedup = {}
             for issue in issues:
                  k = (issue.location, issue.item_name)
                  if k not in dedup:
                       dedup[k] = []
                  found = False
                  for ex_iss in dedup[k]:
                      if ex_iss.issue_type == issue.issue_type and ex_iss.details == issue.details:
                          found = True; break
                  if not found:
                       dedup[k].append(issue)'''

text = text.replace(old_issue_grouping_loop, new_issue_grouping_loop)

old_details_writing_loop = '''                  types_strs = []
                  details_strs = []
                  for (it, det) in data:
                       map_idx = issue_id_map.get((it, det), "")
                       idx_str = f"[{map_idx}]" if map_idx else ""
                       types_strs.append(f"{it}")
                       details_strs.append(f"[{map_idx}] {det}")

                  types_strs = list(dict.fromkeys(types_strs))
                  # Issue Type (column 2)
                  if types_strs:
                      p_it = row_cells[2].paragraphs[0]
                      p_it.text = types_strs[0]
                      for t in types_strs[1:]:
                           row_cells[2].add_paragraph(t)
                       
                  # Details (column 3)
                  if details_strs:
                      p_det = row_cells[3].paragraphs[0]
                      p_det.text = details_strs[0]
                      p_det.paragraph_format.left_indent = Inches(0.22)
                      p_det.paragraph_format.first_line_indent = Inches(-0.22)
                      for d in details_strs[1:]:
                           p = row_cells[3].add_paragraph(d)
                           p.paragraph_format.left_indent = Inches(0.22)
                           p.paragraph_format.first_line_indent = Inches(-0.22)'''

new_details_writing_loop = '''                  types_strs = []
                  for iss in data:
                       if iss.issue_type not in types_strs:
                            types_strs.append(iss.issue_type)

                  # Issue Type (column 2)
                  if types_strs:
                      p_it = row_cells[2].paragraphs[0]
                      p_it.text = types_strs[0]
                      for t in types_strs[1:]:
                           row_cells[2].add_paragraph(t)
                       
                  # Details (column 3)
                  row_cells[3].text = "" # clear anything default
                  p_det = row_cells[3].paragraphs[0] if len(row_cells[3].paragraphs) > 0 else row_cells[3].add_paragraph()
                  
                  for idx, iss in enumerate(data):
                       map_idx = issue_id_map.get((iss.issue_type, iss.details), "")
                       idx_str = f"[{map_idx}] " if map_idx else ""
                       
                       if iss.old_val is not None or iss.new_val is not None:
                           p_head = p_det if idx == 0 else row_cells[3].add_paragraph()
                           p_head.text = f"{idx_str}{iss.details}"
                           p_head.paragraph_format.left_indent = Inches(0.22)
                           p_head.paragraph_format.first_line_indent = Inches(-0.22)
                           
                           p_old = row_cells[3].add_paragraph()
                           p_old.add_run("From:").bold = True
                           p_old.add_run(" ")
                           p_old.paragraph_format.left_indent = Inches(0.4)
                           
                           p_new = row_cells[3].add_paragraph()
                           p_new.add_run("To:").bold = True
                           p_new.add_run(" ")
                           p_new.paragraph_format.left_indent = Inches(0.4)
                           
                           self._render_rich_diff(p_old, p_new, iss.old_val, iss.new_val)
                       else:
                           p_cur = p_det if idx == 0 else row_cells[3].add_paragraph()
                           p_cur.text = f"{idx_str}{iss.details}"
                           p_cur.paragraph_format.left_indent = Inches(0.22)
                           p_cur.paragraph_format.first_line_indent = Inches(-0.22)
'''

text = text.replace(old_details_writing_loop, new_details_writing_loop)

if new_details_writing_loop not in text: print("Failed generator loop patch")

with open(fname, 'w', encoding='utf-8') as f:
    f.write(text)
print('Generator patched')

