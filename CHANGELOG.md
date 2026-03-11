# Changelog

All notable changes to this project will be documented in this file.

## [2.2] - 2026-03-11
### Major Features
- **Integrated Dual Linter**: Vacuum engine now available alongside Spectral for deep OAS validation with interactive switching.
- **Consolidated UX**: Moved Import/Roundtrip to a standalone tool window; streamlined main interface for Generation.
- **Legacy Converter 2.0**: Full recursive resolution for complex types, robust General Description mapping, and integrated progress logging.
- **Schema Tracer**: New utility for forensic analysis of schema variants across legacy templates.
- **High-Fidelity OAS**: Preserved numeric precision (RawNumericValue Protocol) and improved OAS 3.0 compliance via inline component resolution.

### Refinements
- **Interactive Filters**: Color-coded severity buttons (Error/Warning/Info/Hint) with greyed-out pie slice visualization.
- **Visual Feedback**: Semantic tab coloring for response codes (2xx/4xx/5xx) and improved YAML editor styling.
- **Cleanup Engine**: Automatic pruning of unused global components and empty OAS blocks.

## [2.1.76] - 2026-02-28
- **Fix(LegacyConverter)**: Parallel same-named subtrees in the same sheet (e.g. two `dailyThresholds` blocks under different parents) are now correctly isolated by the BFS descent algorithm. Each `(name, parent)` pair gets its own fingerprint, so schemas like `DailyThresholds1`, `LacAgenda1`, `LacDefaultAgenda1`, and `DefaultDailyThresholds1` are correctly generated.
- **Fix(LegacyConverter)**: `_unique_inline_component_name` now checks already-registered inline component names (not only emitted ones), preventing duplicate schema name registration within the same file.
- **Fix(LegacyConverter)**: `_fp_inline_subtree` always includes description for `$ref`-typed child rows regardless of the `include_descriptions_in_collision` preference, matching old-tool splitting behaviour.
- **Feature(LegacyConverter)**: New preference `tools_legacy_capitalize_schema_names` (default ON) controls whether `operationId` tokens are PascalCased in generated schema wrapper names.

## [1.6.0] - 2026-01-20
- **v1.6.14**: Logic(Roundtrip): Smart detection of Source OAS version (generates only congruent version). Logic(Diff): New "Line Diff Summary" with Add/Remove counts. GUI: Detailed button/log alignment.
- **v1.6.13**: GUI(Reference): Perfected GUI alignment for Import tab to match Generation tab (Single Frame Grid).
- **v1.6.11**: Logic(Import): Roundtrip Check now skips import (compares existing Excel). GUI: Unified alignment/spacing.
- **v1.6.9**: Fix(GUI): Removed obsolete call to `update_import_file_list` causing startup crash.
- **v1.6.7**: GUI Refactor: Single "OAS Source File" input, Detailed Import Logging, Improved Roundtrip Summary formatting.
- **v1.6.5**: Fix(Build): Fixed missing "Templates Master" in executable causing Import/Roundtrip to fail.
- **v1.6.4**: Fix(GUI): Adjusted Import Tab layout to prevent excessive spacing.
- **v1.6.3**: GUI Polish: Layout improvements, Menu updates, Preferences support for Import settings.
- **v1.6.2**: Fix(GUI): Restored missing imports causing runtime crash.
- **v1.6.0**: Added "OAS to Excel" (Import) tab with Roundtrip Check and Differential Logging.
## [1.5.12] - 2026-01-19
- Fix(OAS-Importer): Serialize complex examples as YAML blocks.
- Fix(OAS-Generator): Enable schema examples for OAS 3.0.
## [1.5.11] - 2026-01-18
- Fix: Preserved original property order in schema examples (Gold OAS order instead of alphabetical)
- Fix: Regenerated templates now use correct YAML format for examples

## [v1.4] - 2026-01-06
### Rebranding
- **Project Renamed**: Officially rebranded to **OASIS** (OAS Integration Suite).
- **Repository**: Renamed from `oas-generation-tool` to `oasis`.

### Added
- **Detached Log Window**: New dedicated window for application logs, keeping the main interface clean.
- **Spectral Output**: Cleaned up Validation tab to show only raw Spectral linter output.
- **Docking Constraints**: Added intelligent sizing to Documentation Viewer to respect Windows Taskbar and invisible borders.

### Changed
- **UI Refinements**: Updated issue card styling for better readability.
- **App Logs Theme**: Defaults to "Dark" mode for better contrast.

### Fixed
- **Docking Regression**: Fixed issue where docked window would extend behind the taskbar.

---
*Note: Prior to v1.4, this project was known as 'oas-generation-tool'.*
