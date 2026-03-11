# OASIS - Project Overview
**Current Version**: `v2.1.98`

## Project Purpose
OASIS (**O**penAPI **S**pecification **I**ntegration **S**uite) generates OpenAPI Specification (OAS) 3.0 and 3.1 YAML files from Excel templates. It provides a robust pipeline for importing, generating, validating, and documenting professional-grade API specifications.

## Recent Major Changes (v2.1.x)
1. **Import Dialog**: Extracted OAS-to-Excel import into standalone `ImportDialog` window (accessible via Tools menu).
2. **Legacy Converter**: Full legacy-to-modern Excel template converter with schema deduplication and recursive resolution.
3. **Dual Linter Support**: Spectral + Vacuum engines with hot-swap, interactive category filters, and CTRL+click solo/exclude.
4. **Preferences Consolidation**: Merged Excel Generation + Tools tabs into "Templates"; tab order: General, OAS Generation, Validation, View, Templates, Logs.
5. **Schema Tracer**: Standalone analysis tool tracing schema variants across legacy endpoint templates.
6. **Style Consistency**: All dialogs share teal `#0A809E` button theme, matching LegacyConverterDialog style.

## Recent Updates (v2.1.71 - v2.1.98)

### 1) Legacy Schema Tracing: Column Fixes
The schema tracing summary table (SCHEMA NAME / USED IN / DIFFERENCES / MERGE) was refined:

- **USED IN column**
  - Now shows the **real Excel sheet name** as context, e.g. `operationId (200)`, `operationId (Body)`, `operationId (400)`.
  - Previously showed generic labels `(Response)` / `(Body)` — now always uses the actual sheet.
  - **Compaction**: usages are aggregated by endpoint on a single line to reduce vertical space:
    - Example: `apDetails (400) (401) (403) (404) (429) (500)`
  - **Width**: the column was widened to avoid excessive line wrapping.

- **Wrapper usage correctness**
  - Wrapper schemas (e.g. `FooRequest` / `FooResponse`) must never show `USED IN: (None)` due to name mismatches.
  - Headless tracer now seeds wrapper usage based on endpoint sheets (`Body`, `200/204/...`) and maps wrapper names to the actual `$index` schema names (handling optional `.YYMMDD` suffix).

- **DIFFERENCES column**
  - **No arrow notation**: each schema now shows only its own attribute values for the differing fields.
    - e.g. `Min Val: 0` (for Amount) and `Min Val: (empty)` (for Amount1) — not `Min Val: 0 -> (empty)`.
  - Extended detection: `description` and `example` fields are now included in group-level diff detection (previously ignored).
  - **Promoted inline schemas**: diffs now also cover `rules` and `mandatory` field changes, not just `dtype`/`items`.
  - **Mixed-type groups** (one schema is a DataType, variant is promoted inline): correctly shows `rules differ: ...`.

- **MERGE column**
  - Uses real sheet names (same as USED IN), e.g. `commandDetails (200)`.
  - Groups by `<Description N>` / `<Example N>` placeholders, listing endpoints indented under each.
  - Only shown when ≥2 distinct values exist (single-value merges are suppressed).

### 2) DefaultDailyThresholds / DefaultDailyThresholds1 — root cause
Both schemas are registered: base as a DataType + inline promoted, variant as inline-only. The diff was missing because:
- `_promoted_diffs` previously compared only `dtype`/`items`, not `rules`.
- Mixed groups (DataType base + inline variant) were skipped by the `fps and not dts` guard.
Both issues fixed in v2.1.72.

### 2) Preferences: Templates Tab (Legacy Tools)
Preferences (Templates tab) include new Legacy Tools toggles:
- Enable Schema Tracing by default
- Include descriptions in collision detection (default OFF)
- Include examples in collision detection (default OFF)

The Templates tab spacing was compacted to avoid bottom buttons being clipped.

### 3) Where the logic lives
- `src/legacy_converter.py` (usage tracking, merge provenance, differences)
- `src/preferences.py` (persistence)
- `src/preferences_dialog.py` (Templates UI)
- `src/legacy_converter_dialog.py` / `src/legacy_schema_tracer_dialog.py` (wiring)

### 4) Quick verification / build commands
- Verify tracing output (Templates Legacy): `.venv\Scripts\python.exe temp.py`
- Build executable (increments build number + PyInstaller): `build_exe.bat`
- Stable release build (no version bump): `build_release.bat`

OASIS/
├── src/
│   ├── main.py                    # Entry point - orchestrates generation
│   ├── gui.py                     # Main UI (Editor, Validation, Tabs) + ImportDialog class
│   ├── generator.py               # High-level OAS orchestrator
│   ├── generator_pkg/             # Schema/Response/YAML builders
│   ├── oas_importer/              # Importer engine (YAML/JSON -> Excel)
│   ├── legacy_converter.py        # Legacy-to-modern template converter
│   ├── legacy_converter_dialog.py # Legacy Converter GUI
│   ├── legacy_schema_tracer_dialog.py # Schema Tracer dialog
│   ├── preferences.py             # Preferences manager
│   ├── preferences_dialog.py      # Preferences UI (6 tabs)
│   ├── linter.py                  # Spectral/Vacuum validation wrapper
│   ├── doc_viewer.py              # Docked documentation viewer
│   └── redoc_gen.py               # Redoc HTML generation
├── bin/                           # External binaries (spectral.exe, vacuum.exe)
├── docs/                          # User Manual & Documentation
├── Templates Master/              # Core Excel templates
├── project history/               # Technical docs & release history
├── tests/                         # Regression tests
└── dist/                          # Compiled executable (OASIS.exe)
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
cd "C:\Users\giuse\.gemini\antigravity\scratch\OASIS"
python run_gui.py
```

Or use the compiled executable: `dist/OASIS.exe`
