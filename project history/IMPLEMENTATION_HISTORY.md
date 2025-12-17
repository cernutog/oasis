# Implementation History - Custom Extension Formatting

## Problem Statement
Custom OpenAPI extensions (`x-sandbox-*`) in the Excel source use YAML literal block style (`|`) for multiline content. When generating the OAS YAML, these extensions were being:
1. Formatted as quoted strings instead of literal blocks
2. Sorted alphabetically instead of preserving Excel order

## User Requirements
1. Preserve literal block style (`|`) for multiline extension values
2. Maintain original order from Excel (no alphabetical sorting)
3. Position extensions BEFORE `responses` in operation objects

## Evolution of Solutions

### Attempt 1: PyYAML Type Wrappers (FAILED)
**Approach**: Create `LiteralString` class and custom YAML dumper
- Created `LiteralString(str)` wrapper class
- Registered custom representer with PyYAML dumper
- Created `OrderPreservingLoader` to wrap strings during parse

**Problems**:
- Parsing YAML and re-dumping loses formatting
- Nested structures not properly handled
- Type lost during dictionary operations

### Attempt 2: OrderedDict + Custom Loader (PARTIAL)
**Approach**: Use `OrderedDict` throughout and custom YAML loader
- Implemented `OrderPreservingLoader` with `OrderedDict`
- Auto-wrapped multiline strings in `LiteralString`
- Removed alphabetical sorting

**Problems**:
- Worked for top-level strings
- Failed for nested extensions like `x-sandbox-response-body`  
- PyYAML dumper behavior unpredictable with nested OrderedDict

### Final Solution: Raw YAML Insertion (SUCCESS)
**Approach**: Don't parse extensions as YAML - insert raw Excel text directly

**Implementation**:

1. **Skip Parsing** (`generator.py:99-103`):
```python
extensions_yaml = op_meta.get("extensions")
if extensions_yaml and isinstance(extensions_yaml, str) and extensions_yaml.strip():
    # Use rstrip() to preserve leading 6-space indent
    op_obj["__RAW_EXTENSIONS__"] = extensions_yaml.rstrip()
```

2. **Post-Process YAML** (`generator.py:688-751`):
```python
def _insert_raw_extensions(self, yaml_text, oas_dict):
    # Find __RAW_EXTENSIONS__ markers in dumped YAML
    # Replace with raw Excel text (already has correct indentation)
    for raw_line in raw_text.split('\n'):
        new_output.append(raw_line)  # Insert exactly as-is
```

3. **Order Extensions Before Responses** (`generator.py:140-150`):
```python
extensions = [k for k in op_obj.keys() if k.startswith("x-")]
if "__RAW_EXTENSIONS__" in op_obj:
    extensions.append("__RAW_EXTENSIONS__")
final_order = standard_pre + extensions + standard_post  # standard_post = ["responses"]
```

## Key Insights

### Excel Text Format
Debug revealed Excel source format:
```
'      x-sandbox-rule-type: SCRIPT_JS\n      x-sandbox-rule-content: |...'
```

**Critical Discovery**: Excel text has **absolute** indentation (6 spaces = operation level), not relative.

### Indentation Issue
Initially used `.strip()` which removed leading spaces:
```python
# WRONG - removes leading indent
op_obj["__RAW_EXTENSIONS__"] = extensions_yaml.strip()

# CORRECT - preserves leading indent  
op_obj["__RAW_EXTENSIONS__"] = extensions_yaml.rstrip()
```

### Post-Processing
Replace `__RAW_EXTENSIONS__` marker in YAML output:
1. Find marker line in dumped YAML
2. Insert raw text as-is (no indent adjustment needed)
3. Skip continuation lines (multiline YAML value from marker)

## Results

✅ **Literal Block Style**: `x-sandbox-rule-content: |` correctly formatted  
✅ **Nested Extensions**: `x-sandbox-response-body: |` within `x-sandbox-response-extension` works  
✅ **Order Preserved**: Extensions appear in Excel order  
✅ **Position**: Extensions before `responses` as required  
✅ **Indentation**: Correct 6-space indent at operation level

## Lessons Learned

1. **Don't fight the tool**: PyYAML's parse→dump cycle fundamentally loses formatting
2. **Trust the source**: Excel text already formatted correctly - use it directly
3. **Simple is better**: Direct text insertion beats complex type wrappers
4. **Debug at source**: Check Excel cell content directly, don't assume format

## Files Modified

- `src/generator.py` - Raw insertion logic, ordering
- `src/parser.py` - Read extensions field
- Test files created during debugging (can be deleted):
  - `test_literal.py`
  - `test_loader.py`
  - `test_update.py`
  - `test_reorder.py`
  - `test_reorder.py`
  - `test_full.py`

## Regression Logic Fix: 201 Headers & Orphan Nodes (2025-12-16)

### Problem Statement
The `201 Created` response was generating an empty schema (`schema: {}`) and missing the `fri` header, despite the data being present in the Excel source.

### Root Cause Analysis
1.  **Indentation Error**: A logic block in `build_paths` responsible for processing parameters and responses was accidentally indented inside an `else` block (handling "File Not Found"), making it unreachable for valid operations.
2.  **Implicit Root Failure**: In `account_assessment.251111` (sheet 201), the first data row was `fri` (a header). The generator implicitly assigned this first row as the Root Node. Since headers are expected to be *children* of the Root, `fri` (being the root itself) was skipped during the header collection phase.
3.  **Orphan Node Dropping**: Nodes that didn't have a clear parent link to the implicit root were being dropped during the schema tree reconstruction.

### Solution Implemented

#### 1. Synthetic Root System
Instead of relying on the first row to be the implicit root, implemented a **Synthetic Root Node** (`Response`) at the start of `_build_single_response`.
- **Logic**: Forced all top-level sections (`headers`, `content`, `links`) to attach explicitly to this synthetic root.
- **Benefit**: Ensures that the first row (e.g., `fri`) is treated as a child, making it visible to all processing loops.

#### 2. Header Schema Wrapping
Changed how headers with `Schema Name` references are generated.
- **Old**: `$ref: #/components/headers/MySchema` (Incorrect: Schema Name usually points to a data model)
- **New**: `schema: { $ref: #/components/schemas/MySchema }` (Correct: Wraps the data model in a Header Schema Object)

### Results
- ✅ `201` Response Schema fully populated.
- ✅ `fri` header correctly generated with proper schema reference.
- ✅ `pri` parameter correctly isolated to example sections (not appearing as a Response Header).
- ✅ Codebase structure simplified by removing fragile implicit root logic.
