# OAS Generation Tool - Project Overview

## Project Purpose
This tool generates OpenAPI Specification (OAS) 3.0 and 3.1 YAML files from Excel templates (.xlsm files). It reads API definitions from structured Excel sheets and produces compliant OpenAPI specifications.

## Directory Structure

```
OAS_Generation_Tool/
├── src/
│   ├── main.py          # Entry point - orchestrates generation process
│   ├── generator.py     # Core OAS generation logic
│   ├── parser.py        # Excel file parsing
│   └── schema_builder.py # JSON Schema construction
├── API Templates/
│   ├── $index.xlsm      # Main index file listing all operations
│   ├── *.xlsm           # Individual operation definition files
│   └── generated/       # Output directory for generated YAML files
└── project history/     # This documentation folder

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
