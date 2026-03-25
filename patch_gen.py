import os
import re

fname = r'c:\Users\giuse\.gemini\antigravity\scratch\OASIS\src\oas_diff\generators\compatibility_generator.py'
with open(fname, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the Summary Table logic
old_summary_start = '''        freq = {}
        for issue in self.issues:
             key = (issue.issue_type, issue.details)
             freq[key] = freq.get(key, 0) + 1
        self.doc.add_paragraph().add_run(f'Total Issues Found: {len(self.issues)}').bold = True
             
        sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        widths_s = [Inches(0.4), Inches(2.2), Inches(3.4), Inches(1.0)] # total 7.0
        table = self._create_table(4, widths_s)
        hdr = table.rows[0].cells
        self._set_repeat_header(table.rows[0])
        hdr[0].text = '#'
        hdr[1].text = 'Issue Type'
        hdr[2].text = 'Details'
        hdr[3].text = 'Frequency'
        for t in hdr:'''

new_summary_start = '''        freq = {}
        schema_map = {}
        for issue in self.issues:
             key = (issue.issue_type, issue.details, issue.old_val, issue.new_val)
             freq[key] = freq.get(key, 0) + 1
             if key not in schema_map: schema_map[key] = set()
             schema_map[key].add(issue.item_name if issue.item_name else (issue.location or "-"))
        
        self.doc.add_paragraph().add_run(f'Total Issues Found: {len(self.issues)}').bold = True
             
        sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        widths_s = [Inches(0.3), Inches(1.4), Inches(1.8), Inches(2.8), Inches(0.7)] # total 7.0
        table = self._create_table(5, widths_s)
        hdr = table.rows[0].cells
        self._set_repeat_header(table.rows[0])
        hdr[0].text = '#'
        hdr[1].text = 'Issue Type'
        hdr[2].text = 'Schema'
        hdr[3].text = 'Details'
        hdr[4].text = 'Frequency'
        for t in hdr:'''

text = text.replace(old_summary_start, new_summary_start)

old_summary_body = '''        issue_id_map = {}
        for idx, ((issue_type, details), count) in enumerate(sorted_freq):
             issue_id_map[(issue_type, details)] = idx + 1
             row = table.add_row().cells
             row[0].text = f"[{idx + 1}]"
             row[1].text = issue_type
             row[2].text = details
             row[3].text = str(count)
             for j in range(4):
                 self._style_body_cell(row[j])'''

new_summary_body = '''        issue_id_map = {}
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
             
             row[4].text = str(count)
             for j in range(5):
                 self._style_body_cell(row[j])'''

text = text.replace(old_summary_body, new_summary_body)

old_details_loop = '''                  for idx, iss in enumerate(data):
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
                       else:'''

new_details_loop = '''                  for idx, iss in enumerate(data):
                       key = (iss.issue_type, iss.details, iss.old_val, iss.new_val)
                       map_idx = issue_id_map.get(key, "")
                       idx_str = f"[{map_idx}] " if map_idx else ""
                       
                       if iss.old_val is not None or iss.new_val is not None:
                           p_head = p_det if idx == 0 else row_cells[3].add_paragraph()
                           p_head.text = f"{idx_str}{iss.details}"
                           p_head.paragraph_format.left_indent = Inches(0.22)
                           p_head.paragraph_format.first_line_indent = Inches(-0.22)
                           
                           p_old = row_cells[3].add_paragraph()
                           p_old.add_run("Old:").italic = True
                           p_old.add_run(" ")
                           p_old.paragraph_format.left_indent = Inches(0.4)
                           
                           p_new = row_cells[3].add_paragraph()
                           p_new.add_run("New:").italic = True
                           p_new.add_run(" ")
                           p_new.paragraph_format.left_indent = Inches(0.4)
                           
                           ov = "<None>" if not iss.old_val or str(iss.old_val).strip() in ("", "None") else str(iss.old_val)
                           nv = "<None>" if not iss.new_val or str(iss.new_val).strip() in ("", "None") else str(iss.new_val)
                           self._render_rich_diff(p_old, p_new, ov, nv)
                       else:'''

text = text.replace(old_details_loop, new_details_loop)

if new_details_loop not in text: print("FAILED PATCHING DETAILS")
if new_summary_body not in text: print("FAILED PATCHING SUM BODY")

with open(fname, 'w', encoding='utf-8') as f:
    f.write(text)

print('Done')
