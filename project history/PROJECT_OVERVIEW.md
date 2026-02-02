# OASIS - Project Overview
**Current Version**: `v2.0.36` (Stable)

## Project Purpose
OASIS (**O**penAPI **S**pecification **I**ntegration **S**uite) generates OpenAPI Specification (OAS) 3.0 and 3.1 YAML files from Excel templates. It provides a robust pipeline for importing, generating, validating, and documenting professional-grade API specifications.

## Recent Major Changes (v2.0.x)
1. **Multiple Examples**: Support for multiple examples per property via CSV-style smart quoting.
2. **Precision Roundtrip**: Fixed array item description displacement and inheritance issues.
3. **Clean Metadata**: Removed hard-coded strings in servers and enabled dynamic description parsing.
4. **Natural Ordering**: Restored Excel-defined property order for schema data (preserving metadata prioritization only for docs).
5. **OAS Importer**: Full bidirectional engine to transform existing OAS back into Excel templates.
6. **Hybrid Documentation**: Bundled local User Manual with online GitHub Pages fallback.

```
OASIS/
├── src/
│   ├── main.py          # Entry point - orchestrates generation process
│   ├── gui.py           # Main UI logic (Integrated Editor & Logs)
│   ├── generator.py     # High-level OAS orchestrator
│   ├── generator_pkg/   # Specialized generation modules (Schema/Response builders)
│   └── oas_importer/    # Importer engine (YAML/JSON -> Excel)
├── docs/                # User Manual & Documentation (online/offline)
├── Templates Master/    # Core Excel templates
├── project history/     # Technical documentation & release history
└── dist/                # Compiled executable (OASIS.exe)

```

## Key Components

### 1. Parser (`src/parser.py`)
- Reads Excel files using pandas
- Extracts: operations, schemas, global metadata, tags
- Handles column name variations (e.g., "Custom Extensions" or "Unnamed: 8")
- **Critical**: Preserves raw text from "Custom Extensions" column

### 2. Generator (`src/generator.py`)
- Builds OAS document structure
- Handles custom extensions with **raw YAML insertion**
- Orders operation object keys correctly
- Manages schema references and combinators (oneOf, allOf, anyOf)

### 3. Schema Builder (`src/schema_builder.py`)
- Constructs JSON Schema objects from Excel definitions
- Handles complex types, arrays, enums
- Processes schema combinators

## Excel Structure

### $index.xlsm Sheets:
- **Global**: API metadata (title, version, servers, etc.)
- **Paths**: List of all operations with references to detail files
- **Tags**: API tag definitions
- **Components**: Reusable components (not currently used)

### Operation Files (e.g., `account_assessment.251111.xlsm`):
- **Request**: Request body schema definition
- **Parameters**: Path/query/header parameters
- **Responses**: Response definitions with schemas and examples

## Critical Implementation Details

### Custom Extension Formatting (RECENTLY FIXED)
**Problem**: Custom extensions (e.g., `x-sandbox-rule-type`, `x-sandbox-response-body`) need to preserve literal block YAML style (`|`) from Excel source.

**Solution**: Raw YAML insertion approach
1. Store raw Excel text without parsing: `op_obj["__RAW_EXTENSIONS__"] = extensions_yaml.rstrip()`
2. Post-process final YAML output to replace `__RAW_EXTENSIONS__` marker with raw text
3. Excel text has absolute indentation (6 spaces) - insert as-is without modification

**Key Files**:
- `generator.py:99-103` - Store raw text
- `generator.py:688-751` - Post-processing insertion
- `parser.py:157` - Read extensions from Excel

### Extension Ordering
Custom extensions appear BEFORE `responses` in operation objects:
```yaml
operationId: example
parameters: []
x-sandbox-rule-type: SCRIPT_JS
x-sandbox-rule-content: |
  ...
responses:
  '200':
```

Implemented via `generator.py:140-150` - includes `__RAW_EXTENSIONS__` in extension list before responses.

## Common Patterns

### Reading Excel with Column Fallbacks
```python
row.get("Custom Extensions") or row.get("Unnamed: 8")
```

### Preserving Order
Use `OrderedDict` throughout to maintain key order from Excel source.

### Schema References
Format: `$ref: '#/components/schemas/SchemaName'`

## Known Issues & Solutions

### Issue: Extension Formatting
- **Symptom**: Multiline strings appear as quoted strings instead of literal blocks
- **Solution**: Raw YAML insertion (see above)

### Issue: Indentation
- **Symptom**: Double indentation on nested content
- **Solution**: Use `.rstrip()` not `.strip()` to preserve leading spaces from Excel

### Issue: Order
- **Symptom**: Extensions sorted alphabetically
- **Solution**: Removed `sorted()`, preserve Excel order

## Running the Tool

```bash
cd "C:\Users\giuse\.gemini\antigravity\scratch\OAS_Generation_Tool"
python src/main.py
```

Output files:
- `API Templates/generated/generated_oas_3.0.yaml`
- `API Templates/generated/generated_oas_3.1.yaml`

## Recent Major Changes

1. **Raw YAML Insertion for Custom Extensions** - Preserves literal block style
2. **Extension Ordering** - Ensures extensions appear before responses
3. **Indentation Fix** - Changed `.strip()` to `.rstrip()` to preserve leading spaces
