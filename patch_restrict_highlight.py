import os

fname = r'c:\Users\giuse\.gemini\antigravity\scratch\OASIS\src\oas_diff\generators\compatibility_generator.py'
with open(fname, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update in Summary Table
old_render_summary = """                       ov = "<None>" if not iss.old_val or str(iss.old_val).strip() in ("", "None") else str(iss.old_val)
                       nv = "<None>" if not iss.new_val or str(iss.new_val).strip() in ("", "None") else str(iss.new_val)
                       self._render_rich_diff(p_old, p_new, ov, nv)"""

new_render_summary = """                       ov = "<None>" if not iss.old_val or str(iss.old_val).strip() in ("", "None") else str(iss.old_val)
                       nv = "<None>" if not iss.new_val or str(iss.new_val).strip() in ("", "None") else str(iss.new_val)
                       is_highlight = ("description" in iss.issue_type.lower() or "description" in iss.details.lower() or "'enum'" in iss.details.lower())
                       if is_highlight:
                            self._render_rich_diff(p_old, p_new, ov, nv)
                       else:
                            p_old.add_run(ov)
                            p_new.add_run(nv)"""

text = text.replace(old_render_summary, new_render_summary)

# 2. Update in Details Table
old_render_details = """                           ov = "<None>" if not iss.old_val or str(iss.old_val).strip() in ("", "None") else str(iss.old_val)
                           nv = "<None>" if not iss.new_val or str(iss.new_val).strip() in ("", "None") else str(iss.new_val)
                           self._render_rich_diff(p_old, p_new, ov, nv)"""

new_render_details = """                           ov = "<None>" if not iss.old_val or str(iss.old_val).strip() in ("", "None") else str(iss.old_val)
                           nv = "<None>" if not iss.new_val or str(iss.new_val).strip() in ("", "None") else str(iss.new_val)
                           is_highlight = ("description" in iss.issue_type.lower() or "description" in iss.details.lower() or "'enum'" in iss.details.lower())
                           if is_highlight:
                                self._render_rich_diff(p_old, p_new, ov, nv)
                           else:
                                p_old.add_run(ov)
                                p_new.add_run(nv)"""

text = text.replace(old_render_details, new_render_details)

with open(fname, 'w', encoding='utf-8') as f:
    f.write(text)

print('Highlighting restrictions applied')
