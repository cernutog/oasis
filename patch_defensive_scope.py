import os

fname = r'c:\Users\giuse\.gemini\antigravity\scratch\OASIS\src\oas_diff\generators\compatibility_generator.py'
with open(fname, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update issue loop to stringify scope defensively
old_loop_block = """        for issue in self.issues:
             scope = issue.schema_name if issue.schema_name else "-"
             try:
                 freq[scope] = freq.get(scope, 0) + 1"""

new_loop_block = """        def _safe_scope(s):
            if isinstance(s, (list, set)):
                return ", ".join(sorted([str(x) for x in s]))
            return str(s) if s else "-"

        for issue in self.issues:
             scope = _safe_scope(issue.schema_name)
             freq[scope] = freq.get(scope, 0) + 1"""

if "freq[scope] = freq.get(scope, 0) + 1" in text:
    if "try:" in text:
        # We previously added try/except block. Let's replace the whole try/except too
        text = re.sub(
            r'for issue in self\.issues:\s+scope = issue\.schema_name if issue\.schema_name else ".*?"\s+try:\s+freq\[scope\] = freq\.get\(scope, 0\) \+ 1\s+except TypeError:\s+.*?\s+raise',
            new_loop_block.replace('\\', '\\\\'),
            text,
            flags=re.MULTILINE | re.DOTALL
        )
    else:
        text = text.replace(old_loop_block, new_loop_block)

with open(fname, 'w', encoding='utf-8') as f:
    f.write(text)

print('Defensive scope stringifier applied')
