# Walkthrough - Custom Extension Formatting ✅

## Solution
Custom extensions (`x-sandbox-*`) needed to preserve:
1. **Literal block style** (`|`) for multiline strings
2. **Original order** from Excel (no alphabetical sorting)  
3. **Exact indentation** from source

## Implementation: Raw YAML Insertion

Instead of parsing extensions as YAML and re-dumping (which loses formatting), the solution inserts raw Excel text directly into the final YAML output.

### Key Changes

#### 1. Skip Parsing ([`generator.py:99-103`](file:///C:/Users/giuse/.gemini/antigravity/scratch/OAS_Generation_Tool/src/generator.py#L99-L103))
```python
extensions_yaml = op_meta.get("extensions")
if extensions_yaml and isinstance(extensions_yaml, str) and extensions_yaml.strip():
    # Store raw text - use rstrip to preserve leading indent
   op_obj["__RAW_EXTENSIONS__"] = extensions_yaml.rstrip()
```

**Critical**: Use `.rstrip()` not `.strip()` - Excel text has 6-space leading indent that must be preserved!

#### 2. Post-Process YAML Output ([`generator.py:688-751`](file:///C:/Users/giuse/.gemini/antigravity/scratch/OAS_Generation_Tool/src/generator.py#L688-L751))
```python
def _insert_raw_extensions(self, yaml_text, oas_dict):
    # Find __RAW_EXTENSIONS__ markers in dumped YAML
    # Replace with raw Excel text (already has correct absolute indentation)
    for raw_line in raw_text.split('\\n'):
        new_output.append(raw_line)  # Insert as-is, no indent adjustment
```

### Indentation Discovery

Excel source format (from debug):
```
'      x-sandbox-rule-type: SCRIPT_JS\n      x-sandbox-rule-content: |\n        var...'
```

**Key insight**: Excel text has **absolute** indentation (6 spaces = operation level), not relative. Insert as-is without adding indent.

## Results

✅ `x-sandbox-rule-type`: Correct 6-space indent  
✅ `x-sandbox-rule-content: |`: Literal block style with correct indent  
✅ `x-sandbox-response-body: |`: Nested literal block style  
✅ Extension order: Preserved from Excel  
✅ Template syntax: Preserved exactly

## Files Modified
- [`src/generator.py`](file:///C:/Users/giuse/.gemini/antigravity/scratch/OAS_Generation_Tool/src/generator.py#L99-L103): Skip parsing, store raw text with `.rstrip()`  
- [`src/generator.py`](file:///C:/Users/giuse/.gemini/antigravity/scratch/OAS_Generation_Tool/src/generator.py#L680-L751): _insert_raw_extensions() post-processing
