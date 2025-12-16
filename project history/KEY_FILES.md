# Key Files Reference

## Core Source Files

### `src/main.py`
**Purpose**: Entry point for OAS generation

**Key Functions**:
- `generate_oas(templates_dir)` - Main orchestration function
- Reads $index.xlsm
- Parses operation files
- Generates both OAS 3.0 and 3.1 outputs

**Important Lines**:
- Line 50: Parse paths index
- Line 109-116: Write generated YAML to files

---

### `src/generator.py`  
**Purpose**: Core OAS document generation logic

**Key Classes**:
- `OASGenerator` - Main generator class

**Critical Methods**:
- `__init__(version, global_meta, tags_list, operations_meta, operations_details)` - Initialize
- `generate()` - Build complete OAS structure
- `get_yaml()` - Output YAML with correct section order
- `_insert_raw_extensions(yaml_text, oas_dict)` - Post-process to insert raw custom extensions

**Important Sections**:
- Lines 99-103: Store raw extensions without parsing
- Lines 140-150: Order operation keys (extensions before responses)
- Lines 688-751: Raw YAML insertion post-processing
- Lines 720-733: `_reorder_dict` - Returns OrderedDict to preserve key order

**Custom Extension Implementation**:
```python
# Store raw text (line 102)
op_obj["__RAW_EXTENSIONS__"] = extensions_yaml.rstrip()

# Post-process to insert (lines 710-720)
for raw_line in raw_text.split('\n'):
    new_output.append(raw_line)  # Insert as-is
```

---

### `src/parser.py`
**Purpose**: Parse Excel files to extract API definitions

**Key Functions**:
- `parse_global_metadata(df_global)` - Extract API info, servers, security
- `parse_paths_index(df_paths)` - Read operations list from $index
- `parse_operation_file(filepath)` - Parse individual operation Excel files
- `parse_tags(df_tags)` - Extract tag definitions

**Important Lines**:
- Line 157: Read custom extensions - `"extensions": row.get("Custom Extensions") or row.get("Unnamed: 8")`
- Lines 50-70: Column helper functions for flexible column naming

---

### `src/schema_builder.py`
**Purpose**: Build JSON Schema objects from Excel definitions

**Key Functions**:
- `build_schema_from_df(df, schema_name)` - Construct schema from dataframe
- `_handle_combinators(row, prop_dict)` - Process oneOf/allOf/anyOf
- `_detect_array_combinators(description)` - Detect array with combinators pattern

## Excel Template Files

### `API Templates/$index.xlsm`
**Main index file**

**Sheets**:
- **Global**: API metadata (title, version, description, servers, security schemes)
- **Paths**: Operations list with columns:
  - Path (A): URL path
  - File Reference (B): Link to operation detail file  
  - Method (C): HTTP method
  - Summary (F): Operation summary
  - Custom Extensions (I/Unnamed: 8): Raw YAML with x-sandbox-* extensions
- **Tags**: Tag definitions
- **Components**: Reusable components (schemas, responses, etc.)

### Operation Detail Files (e.g., `account_assessment.251111.xlsm`)
**Individual operation definitions**

**Sheets**:
- **Request**: Request body schema
- **Parameters**: Path/query/header/cookie parameters
- **Responses**: Response definitions with schemas and examples
- **200**, **400**, etc.: Individual response status code details

## Generated Output

### `API Templates/generated/generated_oas_3.0.yaml`
OpenAPI 3.0 specification

### `API Templates/generated/generated_oas_3.1.yaml`
OpenAPI 3.1 specification (with examples in separate examples field)

## Configuration

No external configuration files - all settings embedded in source code:
- Column mappings in `parser.py`
- Section ordering in `generator.py:get_yaml()`
- Default values in various builders
