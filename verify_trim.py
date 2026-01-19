import re

def original_trim(text):
    if not text:
        return text
    lines = text.split('\n')
    min_indent = float('inf')
    for line in lines:
        stripped = line.lstrip()
        if stripped:
            indent = len(line) - len(stripped)
            min_indent = min(min_indent, indent)
    if min_indent == float('inf'):
        min_indent = 0
    trimmed_lines = []
    for line in lines:
        if line.strip():
            trimmed_lines.append(line[int(min_indent):])
        else:
            trimmed_lines.append('')
    return '\n'.join(trimmed_lines).rstrip()

def new_trim(text):
    if not text:
        return text
    lines = text.split('\n')
    
    # 1. Standard dedent first
    min_indent = float('inf')
    for line in lines:
        stripped = line.lstrip()
        if stripped:
            indent = len(line) - len(stripped)
            min_indent = min(min_indent, indent)
    if min_indent == float('inf'):
        min_indent = 0
        
    dedented_lines = []
    for line in lines:
        if line.strip():
            dedented_lines.append(line[int(min_indent):])
        else:
            dedented_lines.append('')
            
    # 2. Aggressive fix for known top-level extension keys that are mishandled
    # e.g. "      x-sandbox-rule-content: |" -> "x-sandbox-rule-content: |"
    final_lines = []
    for line in dedented_lines:
        # Check if line looks like "   x-sandbox-foo:"
        m = re.match(r'^(\s+)(x-sandbox-[a-zA-Z0-9-]+):', line)
        if m:
            # It's indented but looks like a known top-level key. Flatten it.
            # CAUTION: This might break nested extensions? 
            # But x-sandbox keys are usually top-level in our context.
            final_lines.append(line.lstrip())
        else:
            final_lines.append(line)
            
    return '\n'.join(final_lines).rstrip()

input_text = """x-sandbox-rule-type: SCRIPT_JS
      x-sandbox-rule-content: |
          var responseName = "OK";"""

print("--- Original ---")
print(original_trim(input_text))
print("\n--- New ---")
print(new_trim(input_text))
