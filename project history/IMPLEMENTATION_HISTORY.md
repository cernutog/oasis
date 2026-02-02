# Implementation History - Custom Extension Formatting

## Development Environment

**IMPORTANT**: This project requires Python 3.13 for compatibility with all dependencies.

**Setup**:
- Use the virtual environment: `.venv` (Python 3.13)
- Activate: `.\.venv\Scripts\python.exe` (direct path recommended)
- Build command: `.\.venv\Scripts\python.exe -m PyInstaller OAS_Gen_Tool.spec`

**Why Python 3.13**:
- `chlorophyll` library requires Python ≤ 3.13
- PyInstaller tkinter DLL resolution works correctly with 3.13
- DO NOT use Python 3.14+ - will cause build failures

---


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

## v1.1.0: Validation Engine & UI Refinements (2025-12-18)

### Problem Statement
The generated OAS files were syntactically correct but potentially contained valid-but-wrong definitions (e.g., missing descriptions, incorrect types) that could only be found by manually running external linters. The UI was also static and lacked feedback.

### Solution Architecture
Integrated **Spectral** (`spectral-cli`) directly into the application flow using a Python wrapper.

1.  **Validation Loop**:
    *   **Pre-Process**: Check/Create `.spectral.yaml` ruleset.
    *   **Execution**: Run `spectral lint -f json` via `subprocess`.
    *   **Parsing**: Capture standard output/error and parse JSON result.
    *   **Visualization**: Convert raw JSON into structured objects for UI consumption.

### Key Implementation Details

#### 1. Semantic Charts (`charts.py`)
Developed a custom `SemanticPieChart` using `tkinter.Canvas` (instead of heavy `matplotlib`).
*   **Dynamic Coloring**: Used HSL color space.
    *   Error (0° Red)
    *   Warning (45° Amber/Yellow)
    *   Info (200° Blue)
*   **Interactivity**: Implemented mouse hover events (`<Enter>`, `<Leave>`, `<Motion>`) to draw tooltips with Rule Code, Description, and Count.

#### 2. Log Management
*   **Dual-Tab System**:
    *   **Analysis Logs**: User-facing application steps.
    *   **Spectral Output**: Raw, pretty-printed JSON for deep debugging.
*   **Smart Toggling**:
    *   Implemented a "Swapping Header" pattern.
    *   **Collapsed**: Button lives in a persistent Footer Frame.
    *   **Expanded**: Button moves to an internal Header Frame at the top of the pane.
    *   **Result**: Eliminates "Ghost Space" issues common with `pack`/`grid` resizing.

#### 3. Filtering Logic (`gui.py`)
User Requirement: "Bad Request" examples often contain intentional schema violations that pollute the error report.
*   **Solution**: Implemented post-validation filtering.
*   **Constraint**: `path contains "examples"` AND `path contains "Bad Request"`.
*   **Optimization**: Cached raw results (`self.last_lint_result`) to allow instant filter toggling without re-running the heavy linter process.

### UI Polish
*   migrated main layout to `grid` geometry manager for better resizing behavior.
*   Added `CTkPanedWindow` for adjustable split between List and Chart.
*   Removed unused Progress Bar (superseded by real-time text logs).

### Release
*   Built standalone executable with `PyInstaller`.
*   Tagged `v1.1` on GitHub.
## v1.2.1: SWIFT Support & Dynamic Systems (2025-12-19)

### Major Features

#### 1. SWIFT OAS Customization
**Requirement**: Generate specialized OAS files for SWIFT compliance alongside standard files.
- **Solution**: Implemented `apply_swift_customization()` method in `OASGenerator`.
- **Logic**:
  - **Servers**: Overrides `servers` list with production/test endpoints.
  - **Security**: Sets specific `oauthBearerToken` scopes.
  - **Components**: Injects mandatory parameters (`ivUserKey`, `ivUserBic`) and headers (`X-Request-ID`).
  - **Polymorphism**: Transforms `400 Bad Request` responses to use `oneOf` polymorphism for error schemas.
  - **Cleanup**: Recursively removes `x-sandbox` extensions.

#### 2. Dynamic Filename Generation
**Requirement**: Output filenames must follow a specific pattern defined in Excel (e.g., `EBACL_FPAD_<date>_...`).
- **Implementation**:
  - Parsing logic added to extract `filename_pattern` and `release` from the "General Description" sheet.
  - `build_filename` helper function replaces placeholders: `<current_date>`, `<oas_version>`, `<customization>`, `<release>`.
  - Fallback mechanism ensures legacy naming if pattern is missing.

#### 3. 3D Visualizations
**Requirement**: "Make the chart look nicer."
- **Implementation**:
  - Upgraded `SemanticPieChart` to a "2.5D" Elliptical Renderer.
  - **Depth**: Draws stacked arcs shifted on the Y-axis to simulate 3D volume.
  - **Cosmetics**: Added black outlines and optimized depth sizing (25px).
  - **Hit Testing**: Updated mouse hover checks to use Elliptical Math (`(dx/rx)^2 + (dy/ry)^2 <= 1`) to correctly detect slices in the distorted projection.

### Stability & Compliance (v1.2.1 Hotfixes)

#### 1. OAS Info Object Injection
**Issue**: The custom `release` and `filename_pattern` fields were leaking into the generated YAML's `info` object, causing validation errors ("Object includes not allowed fields").
**Fix**: Implemented a sanitization step in `src/main.py`. A `clean_info` copy is created (popping internal keys) before passing it to the generator.

#### 2. Icon Persistence
**Issue**: Application icon missing in Window Title and Filesystem for the frozen executable.
**Fix**: 
- **Runtime**: Updated `gui.py` to resolving icon path via `sys._MEIPASS` (PyInstaller temp dir).
- **Build**: Added `--icon='icon.ico'` and `--add-data 'icon.ico;.'` to PyInstaller command to ensure both metadata and physical file presence.

#### 3. Spectral on Windows
**Issue**: Linter failing with "Invalid ruleset provided".
**Fix**: Forced inclusion of `os.path.normpath` for ruleset paths to handle Windows backslashes correctly.

## Release v1.2.2: UI, Ordering, and Traceability

### Problem Statement
User feedback identified several issues in the v1.2.x series:
1. **AES**: The "pie chart" vector validation icon was confusing. User requested a simple Unicode checkmark.
2. **Schema Ordering**: The `example` property in YAML schemas was not consistently placed at the end of the object, despite previous attempts.
3. **SWIFT Parameters**: `ivUserKey` and `ivUserBic` were not correctly ordered at the top of the parameter list.
4. **Traceability**: SWIFT OAS files lacked a clear reference to the source non-SWIFT OAS file they were derived from.
5. **Shared State**: Generating multiple SWIFT versions (3.0, 3.1) in one session caused description notes to accumulate inappropriately.

### Solutions Implemented

#### 1. Recursive Schema Re-ordering (Robustness)
**Approach**: Instead of relying on insertion order or shallow sorts, implemented a **recursive** post-processing step (`_recursive_schema_fix`).
- Traversing the entire generated OAS dictionary immediately before YAML dumping.
- For every dictionary found, if it contains `example` or `examples`, it creates a new `OrderedDict`.
- All keys *except* examples are added first.
- Example keys are added *last*.
- The original dictionary is destructively updated (`clear()` + `update()`) to ensure no reference breakage.
**Result**: Verified by test script (`tests/verify_example_order.py`); `example` is rigorously at the end.

#### 2. Clean State for Generator (Fixing Pollution)
**Problem**: `OASGenerator.build_info` was assigning the input `info` dictionary by reference.
**Fix**: Updated `build_info` to use `copy.deepcopy(info_data)`.
**Result**: SWIFT customizations (allocating "Based on..." notes) now affect only the local copy, preventing bleed-over between 3.0 and 3.1 generations.

#### 3. SWIFT Source Traceability
**Feature**: Modified `apply_swift_customization` to accept `source_filename`.
- Appends `\n\nBased on {filename}` to `info.description`.
- `main.py` updated to capture standard filenames during generation and pass them to the SWIFT generator.

#### 4. UI Simplification
**Change**: Replaced complex `tkinter` canvas drawing logic in `Src/charts.py` with a simple text label rendering a green Unicode Checkmark (✔).

### Conclusion
v1.2.2 consolidates these fixes into a stable release, verified by both automated scripts and manual inspection of generated artifacts.

## Release v1.3: Docked Documentation Viewer (2025-12-25)

### Major Features

#### 1. Integrated Documentation Viewer
**Requirement**: View Redoc-style API documentation directly from the application without external browser.
- **Implementation**:
  - New `doc_viewer.py` module using `pywebview` for embedded browser rendering
  - Multiprocessing architecture for stable window management
  - Shared memory IPC (`multiprocessing.Value`) for dock state synchronization

#### 2. Docked Side-by-Side Mode
**Requirement**: Documentation viewer should dock alongside the main window for seamless editing.
- **Implementation**:
  - Windows API integration (`SystemParametersInfoW` with `SPI_GETWORKAREA`) for accurate screen dimensions
  - Invisible border compensation (7px) for Windows 11 compatibility
  - 30px bottom margin for visible rounded corners above taskbar
  - Non-blocking positioning using `self.after()` to prevent UI freezes

#### 3. Bidirectional Sync
**Features**:
  - **Locate in Docs**: Right-click YAML operations → navigate to corresponding section in documentation
  - **Sync from Docs**: Click documentation sections → jump to corresponding YAML code in editor

#### 4. Preferences System
- New `preferences.py` and `preferences_dialog.py` modules
- Customizable settings: font size, color schemes, dock behavior
- Multiple editor themes: OAS Dark, One Dark, Nord, GitHub Dark, VS Dark

### Bugfixes

#### 1. Viewer Reopen Fix
**Problem**: Closed documentation viewers could not be reopened - clicking "View Documentation" did nothing.
**Root Cause**: `process.is_alive()` returned True even after window was closed.
**Solution**: Modified `focus()` to detect closed windows via `pygetwindow.getWindowsWithTitle()`. If window not found, marks viewer as closed and allows creating a new one.

#### 2. Terminology Consistency
- Renamed "Bind/Unbind" to "Dock/Undock" throughout the UI for clarity

### Repository Cleanup
- Removed generated HTML files from git tracking
- Added `*.html` to `.gitignore`
- Deleted merged feature branch `feat-view-redocly`

### Files Added
- `src/doc_viewer.py` - Docked viewer implementation
- `src/preferences.py` - Preferences manager
- `src/preferences_dialog.py` - Preferences UI dialog
- `src/redoc_gen.py` - Redoc HTML generation
- `src/resources/redoc.standalone.js` - Bundled Redoc library
- `src/colorschemes/*.toml` - Editor color scheme definitions

### Next Steps (v1.4)
- Make generated HTML files temporary and clean up on viewer/app close
- Remove `_redoc` suffix from generated filenames


## v1.4: Refactoring, Logs & Rebranding (2026-01-06)

### 1. Generator Refactoring
**Goal**: Improve code maintainability and testability by splitting the monolithic `generator.py`.
**Implementation**:
- Extracted `GenerationContext` to `src/generator_pkg/context.py` (Registry for Headers, Links, Tags).
- Extracted `SchemaBuilder` logic to `src/generator_pkg/schema_builder.py`.
- Extracted `ResponseBuilder` logic to `src/generator_pkg/response_builder.py`.
- Created `src/generator_pkg/row_helpers.py` for Excel row processing.
- `generator.py` now acts as the high-level orchestrator.

### 2. Enhanced Logging
**Goal**: Clean up the UI and separate implementation logs from validation results.
**Implementation**:
- **Detached Window**: Created `LogWindow` (`CTkToplevel`) to show global application logs.
- **Validation Tab**: Removed nested tabs. Now shows only "Spectral Output".
- **Theme**: "Application Logs" window defaults to "Dark" theme for better readability.

### 3. Docking & Regression Fixes
**Issue**: Docked Documentation Viewer was extending behind the Windows Taskbar.
**Fix**:
- Implemented `src/doc_viewer.py::_get_monitor_work_area` using `ctypes` and `SystemParametersInfoW`.
- **Logic**: Doc window height = `WorkArea.bottom - Window.y` + 8px (Shadow Allowance).
- **Parity**: Main Window also constrained to Workspace Area.

### 4. Rebranding (OASIS)
**Goal**: Official product launch as OAS Integration Suite.
**Changes**:
- Renamed project to **OASIS**.
- Repository renamed to `oasis`.
- Created `setup_oasis.bat` for automated environment repair after folder rename.
- Added `CHANGELOG.md` to track official releases.

## v1.5: Selection Fixes, Docking & Source Mapping (2026-01-07)

### 1. YAML Editor Selection Fix
**Problem**: After double-clicking a word, Shift+Left/Right would incorrectly expand/contract the selection from the wrong end.
**Root Cause**: Tkinter's internal word-selection mode was overriding manual anchor settings.
**Solution**:
- Implemented custom `_on_shift_left` and `_on_shift_right` handlers in `gui.py`.
- Handlers manually adjust selection bounds and return `"break"` to bypass Tkinter's default behavior.
- Logic: Cursor at end → Shift+Left contracts from right; Cursor at start → Shift+Left expands to left.
- Added `_on_yaml_double_click` that always sets cursor to END after selection.

### 2. Documentation Docking - Maximized Window Fix
**Problem**: When main window was maximized, clicking "View Documentation" failed to dock properly (no resize).
**Solution**:
- Added check `if self.state() == "zoomed"` before creating `DockedDocViewer`.
- Restores window to `"normal"` state with `update_idletasks()` before applying docking layout.

### 3. Source Mapping for Excel Links
**Feature**: Validation issues now include contextual links to source Excel templates.
**Implementation**:
- `main.py`: Creates `.oasis_excel_maps/` directory alongside OAS output.
- `generator.py`: Tracks source file for each generated component via `build_components(source_file=...)`.
- New method `get_source_map_json()` exports mapping data.
- Orphan map cleanup added to generation flow.

### 4. Repository Cleanup
- Removed 10 generated HTML files from git tracking (~23K lines).
- Removed 17 debug/test scripts from tracking.
- Fixed `.gitignore` (added `*.html`, `test_*.py`, `reproduce_*.py`, `scripts/debug/`).
- GitHub now correctly identifies Python as the primary language.
- Deleted local test folders and obsolete files (~100MB freed).

### Files Modified
- `src/gui.py` - Selection handlers, docking fix
- `src/main.py` - Source mapping, map cleanup
- `src/generator.py` - Source tracking
- `src/version.py` - Bumped to 1.5
- `.gitignore` - Updated exclusions

### Build v1.8.100 (2026-01-19)
- **Spectral Error Analysis**: Root cause identified as `ShortErrorResponse` ambiguity.
- **Generator Improvements**:
    - Enhanced example coercion with `$ref` resolution.
    - Added support for examples in response headers.
    - Improved mapping of Excel "Description" to OAS "title" for containers.
- **Key Modules**: `src/generator_pkg/schema_builder.py`, `src/generator_pkg/row_helpers.py`, `src/generator_pkg/response_builder.py`.

### Build v1.8.101 (2026-01-27)
- **Metadata Fix**: `type: object` fields now consistently use `description` instead of `title`.
- **Key Modules**: `src/generator_pkg/schema_builder.py`.

### Build v1.8.102 (2026-01-27)
- **Precision Overhaul (String Preservation Protocol)**:
    - Implemented `RawNumericValue(str)` to preserve exact numeric formatting (e.g., `4800.00`).
    - Unified precision logic across Importer and Generator using string-based preservation.
    - Prevented all automatic numeric casts (`float`/`int`) to ensure source fidelity.
- **Key Modules**: `src/generator_pkg/yaml_output.py`, `src/oas_importer/schema_flattener.py`, `src/generator_pkg/row_helpers.py`.

### Build v1.8.103 (2026-01-27)
- **Hotfix**: Restored missing imports in `oas_converter.py` that caused a `NameError` on startup.
- **Improved Stability**: Verified startup behavior and precision logic.

### Build v1.8.107 (2026-01-27)
- **Fix**: Dynamic YAML Tagging. Resolved `!!float` tag leakage by updating `yaml_output.py` to dynamically assign tags based on content (decimal presence).
- **Verification**: Added `verify_tag_roundtrip.py` for autonomous regression testing.

### Build v1.8.108 (2026-01-27)
- **Fix**: "Triple Quote" Artifacts. Updated `src/oas_importer/schema_flattener.py` to remove forced quote wrapping for string fields. Importer now faithfully preserves source string format (e.g., `'1.0'` -> `'1.0'`), relying on the Generator for correct type handling.
- **Verification**: Verified with `verify_fix_live.py` (simulating full app flow).

### Build v1.8.109 (2026-01-27)
- **Emergency Fix**: Active Quote Stripping. Implemented robust sanitization in `schema_flattener.py` to detect and strip redundant quotes (e.g., `"'1.0'"`) from input values.
- **Verification**: Verified with `verify_strip.py` and `verify_fix_live.py`.

### Build v1.8.117 (2026-01-28)
- **Fix**: Universal Custom Extension Support in Importer. Updated `OASParser` and `SchemaFlattener` to recognize, capture, and export all vendor-specific extensions (keys starting with `x-`) at response, parameter, and schema property levels.
- **Safety**: Strict Build & Commit Workflow. Modified `build_exe.bat` to include mandatory Git reminders and created `.agent/workflows/build.md` to formalize the release cycle.
- **Verification**: Verified extension capture with `verify_extensions.py` and confirmed workflow safety prompts during build.

### Build v1.8.121 (2026-01-28)
- **Fix**: Polymorphic Schema Title/Description Duplication. 
    - **Importer**: Updated `SchemaFlattener` to correctly map Titles to Descriptions for container branches.
    - **Generator**: 
        - Restored Titles for top-level containers and branch roots.
        - Prevented Title promotion for nested properties.
        - Implemented deduplication for identical Title/Description pairs.
    - **Ordering**: Enforced `title` priority (appearing before `type`/`oneOf`) in `_recursive_schema_fix`.
- **Key Modules**: `src/generator.py`, `src/oas_importer/schema_flattener.py`, `src/generator_pkg/schema_builder.py`.

### Build v1.8.122 (2026-01-28)
- **Fix**: Selective `oneOf` Exclusivity & Inheritance Protection.
    - **Tracking**: Implemented pre-scanning pass to identify components used in `oneOf` vs `allOf`.
    - **Selective Closure**: 
        - Applied `additionalProperties: false` only to components used in `oneOf` but NOT in `allOf`, preventing inheritance breakage.
        - For OAS 3.1, applied closure as a direct sibling to `$ref` in `oneOf` branches.
    - **Strictness**: Added `minProperties: 1` to optional-only object branches in `oneOf` to prevent ambiguous empty object matches.
    - **Compatibility**: Guaranteed identical behavior across OAS 3.0 and 3.1.
- **Key Modules**: `src/generator.py`, `src/generator_pkg/schema_builder.py`.

### Build v1.8.123 (2026-01-28)
- **Fix**: Schema Description Preservation (Global). 
    - Attempted to remove all title promotion for combinators. (Superseded by v1.8.124).
- **Key Modules**: `src/generator.py`, `src/generator_pkg/schema_builder.py`.

### Build v1.8.124 (2026-01-28)
- **Refinement**: Schema Title/Description Logic (Root vs Branch).
    - **Root Containers**: Restricted `description` preservation to the main root of combinators (`allOf`, `oneOf`, `anyOf`).
    - **Branch Roots**: Restored `title` promotion for indexed branch roots (e.g., `Branch[0]`) to maintain documentation readability.
    - **Deduplication**: Ensured that if a description is promoted to a title for a branch, the redundant description field is removed.
- **Key Modules**: `src/generator.py`.

### Build v1.8.125 (2026-01-28)
- **Fix**: Inline Header Resolution (OAS 3.0).
    - Implemented inline expansion for response headers in OAS 3.0 when a `description` override is detected.
    - Added `x-comment` to explain the expansion.
- **Key Modules**: `src/generator_pkg/response_builder.py`.

### Build v1.8.126 (2026-01-28)
- **Fix**: Automatic Abandoned Component Cleanup (OAS 3.0).
    - Implemented a reference-counting mechanism to identify and remove global components (`headers`, `schemas`) that become unused after being inlined.
    - Prevents `oas3-unused-component` warnings while maintaining valid doc-level references.
- **Key Modules**: `src/generator.py`, `src/generator_pkg/response_builder.py`.

### Build v1.8.127 (2026-01-28)
- **Refinement**: Consistent `x-comment` wording.
    - Updated the prefix to `"Reference from..."` for inlined headers in OAS 3.0, matching the style used for parameters.
- **Key Modules**: `src/generator_pkg/response_builder.py`.

### Build v1.8.128 (2026-01-28)
- **Feature**: User Manual & Navigation refinement.
    - Updated `user_manual.html`: Fixed "View" menu description and endpoint file extensions (.xlsx).
- **Key Modules**: `src/docs/user_manual.html`.

### Build v1.8.130 (2026-01-29)
- **Feature**: Workspace Cleanup.
    - Removed redundant scripts, temporary output folders, and helper assets to streamline the repository.
    - Updated `.gitignore` with comprehensive release-ready exclusions.
    - Archived essential regression tests in `tests/`.

### Build v1.8.131 (2026-01-29)
- **Refinement**: Entry point restoration.
    - Restored `run_gui.py` (accidentally removed during cleanup) to fix the build process.
- **Key Modules**: `run_gui.py`.

## v2.0: Stable Release & Doc Migration (2026-01-29)

### 1. OAS Importer Engine
**Feature**: Full bidirectional support.
- Implemented `oas_importer` package to transform OAS 3.0/3.1 files back into Excel Templates.
- High-fidelity conversion preserving schemas, parameters, and custom extensions.

### 2. Documentation Hybrid Strategy
**Feature**: Offline-first documentation with online mirror.
- Moved documentation to root `/docs` for GitHub Pages compatibility.
- Implemented "Local Priority" in `gui.py`: checks for bundled `user_manual.html` before falling back to `https://cernutog.github.io/oasis/`.
- Created `index.html` redirect for easy online navigation.

### 3. Repository Performance Optimization
**Action**: Squash Rebase.
- Consolidated hundreds of historical commits (and large deleted binary assets) into a single baseline commit.
- Drastically reduced repository size and fixed Git push timeout issues.

### 4. Stability & Precision Fixes
- Unified numeric precision handling across the suite.
- Optimized polymorphic schema generation (`oneOf` exclusivity).
- Standardized release-ready `.gitignore`.

### Release
- **Tag**: `v2.0`
- **GitHub Release**: Attached finalized `OASIS.exe` with bundled docs and release notes.

### Build v2.0.1 (2026-01-29)
- **Feature**: Attribute Diff (RoundTrip Check).
    - Implemented a recursive deep-comparison engine in `OASComparator` to identify missing or added attributes.
    - Added "Attribute Diff" checkbox to the Import tab.
    - Specialized logic for matching parameters by `name`/`in` and security by requirement keys.
- **Fix**: Browse Button Initialization.
    - Implemented `_get_initial_dir` helper to ensure all directory dialogs open in the most relevant folder (preferring the current field content or its parent).
- **Key Modules**: `src/oas_importer/oas_comparator.py`, `src/gui.py`.

### Build v2.0.2 (2026-01-29)
- **Feature**: Refined Attribute Diff (Noise Reduction).
    - Implemented `_has_semantic_content` logic to filter out structural noise.
    - Added "Noise Container" check to skip empty `headers`, `parameters`, `responses`, etc.
    - Categorized diff output into **Info, Paths, Components, Security** groups for better visibility.
    - Standardized path formatting (single slashes).
- **Fix**: Empty Tag Generation (.nan).
    - Added `nan` and empty string safety checks in `ExcelParser.parse_tags` and `build_paths`.
    - Prevented propagation of invalid tag values into the final OAS document.
- **Key Modules**: `src/oas_importer/oas_comparator.py`, `src/generator.py`, `src/excel_parser.py`, `src/gui.py`.

### Build v2.0.3 (2026-01-29)
- **Feature**: OAS Cleanup (Pruning Empty Blocks).
    - Modified `OASGenerator.build_paths` to omit empty `tags` and `parameters` at the operation level.
    - Modified `OASGenerator.get_yaml` to prune empty global `components` sub-blocks (`parameters`, `headers`, `schemas`, `responses`, `securitySchemes`).
    - Entire `components` section is omitted if it becomes empty after pruning.
- **Key Modules**: `src/generator.py`.
## v2.1: Attribute Diff & Precision Overhaul (2026-02-02)

### 1. Attribute Diff Engine
**Goal**: Identify semantic differences between source and generated OAS to ensure 100% roundtrip fidelity.
**Implementation**:
- Recursive deep-comparison in `OASComparator`.
- Categorized reporting (Info, Paths, Components, Security).
- Integrated into the GUI (Import tab) with color-coded highlighting.

### 2. Multiple Examples Support
**Goal**: Allow multiple example values per schema property from Excel.
**Implementation**:
- **Importer**: Joins examples in Excel cells using `, `.
- **Generator**: Parses comma-separated values using `csv` smart-quoting to handle values containing commas.
- Refined `schema_builder.py` and `schema_flattener.py`.

### 3. High-Fidelity Schema Rules
**Goal**: Prevent "Added Attribute" warnings caused by generator heuristics.
**Implementation**:
- **Array Integrity**: Fixed displacement of descriptions from `items` to parent. Supported OAS 3.0 `$ref` description via `allOf` workaround.
- **Natural Ordering**: Restricted `name`/`title` prioritization to metadata only; data properties now follow Excel order.
- **Servers**: Removed hard-coded "Server base path" and enabled parsing from Column D of the index file.
- **Numeric Fidelity**: Universal use of `RawNumericValue` to preserve string formatting (e.g., `4800.00`).

### 4. Hybrid Documentation
**Goal**: Clean up repository while maintaining accessible docs.
**Implementation**:
- Migrated user guide to root `/docs` for GitHub Pages.
- Implemented hybrid loading in `gui.py` (Local mirror vs. Online fallback).

### Release
- **Tag**: `v2.1`
- **GitHub Release**: Consolidated 40+ incremental builds into a single stable release with attached `OASIS.exe`.
