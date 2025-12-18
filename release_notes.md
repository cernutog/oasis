# OAS Generation Tool - Release Notes

## v1.1.0 - The Validation Update 🛡️

This release introduces a powerful new **Validation Engine** powered by `spectral-cli`.

### 🌟 New Features
*   **Validation Tab**: A dedicated interface to verify your generated OAS specifications.
    *   **Analytic List**: Complete breakdown of Errors, Warnings, and Info.
    *   **Interactive Chart**: Dynamic Pie Chart with semantic colors (HSL gradients) and tooltips explaining the rules.
    *   **Bad Request Filter**: One-click filter to ignore intentional errors in "Bad Request" examples.
    *   **Dual Log View**:
        *   **App Logs**: Standard application output.
        *   **Spectral Output**: Raw JSON output for deep debugging.
*   **UI Experience Improvements**:
    *   **Resizable Layout**: New split-pane design with draggable dividers.
    *   **Smart Log Toggle**: "Logs" button moves intelligently (Footer when closed, Header when open).
    *   **Visual Polish**: Clean, professional aesthetics with custom icons and consistent spacing.

### 🔧 Fixes & Refinements
*   Fixed chart visibility issues on window resize.
*   Optimized layout for varying window sizes.
*   Corrected handling of spectral process timeouts.

---

# OAS Generation Tool - v1.0.0

First official release of the OAS Generation Tool.

## 🌟 New Features
*   **Modern GUI**: Completely new graphical interface built with `CustomTkinter`.
    *   Dark Mode / System Theme support.
    *   Real-time log window.
    *   Responsive design.
    *   Native File Dialog for folder selection.
*   **Smart Icon**: New, high-legibility application icon ("Concept 19 - Split Grid").
*   **Standalone Executable**: Single `.exe` file with no external dependencies required.

## 🔧 Core Improvements
*   **Automated Excel Fixing**: Heuristics to detect and fix common logical errors in Excel templates.
*   **OAS 3.0 & 3.1**: Simultaneous generation of both OpenAPI specification versions.
*   **Robust Parsing**: Improved handling of merged cells, missing headers, and incomplete data rows.
*   **Validation**: Integrated checking of required fields (Description, Summary, Tags).

## 📦 Installation
Simply download `OAS_Generation.exe` and run it. No installation required.
