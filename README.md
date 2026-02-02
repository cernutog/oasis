# 🏝️ OASIS - OAS Integration Suite

> **Transform Excel Templates into robust OpenAPI 3.0 & 3.1 Specifications.**

OASIS (**O**penAPI **S**pecification **I**ntegration **S**uite) is a professional tool designed to streamline the creation, validation, and documentation of OpenAPI specifications from Excel templates.

[**📖 Leggi la Guida Utente Online**](https://cernutog.github.io/oasis/) | [**🚀 Scarica l'ultima Release Stabile (v2.0)**](https://github.com/cernutog/oasis/releases/latest)

---

**OASIS** takes structured Excel files (`.xlsm`) as input and automatically generates valid, standards-compliant OpenAPI Specifications (OAS) in YAML format.

But it doesn't stop at generation. With its **v1.1 Validation Update**, it now includes a built-in **Spectral** engine to analyze, score, and visualize the quality of your API definitions.

![OASIS](https://via.placeholder.com/800x400?text=OASIS+Screenshot+Placeholder)

---

## ✨ Key Features

### 🚀 Generation Engine
*   **Dual Output**: Generates both **OAS 3.0** (Salesforce compatibility) and **OAS 3.1** (Modern standard) simultaneously.
*   **Smart Heuristics**: Automatically detects and fixes common data entry errors in Excel (e.g., merged cells, missing methods, typo correction).
*   **Template Support**: Optimized for the "Account Assessment" Excel structure.

### 🛡️ Integrated Validation (New in v1.1)
*   **Spectral Powered**: Uses `spectral-cli` under the hood for industry-standard linting.
*   **Visual Analytics**:
    *   **Interactive Pie Chart**: Visual breakdown of errors, warnings, and info with semantic coloring.
    *   **Dashboard**: Sortable list of issues with direct links to the rule definitions.
*   **Dual Logs**: Switch between user-friendly application logs and raw Spectral JSON output.
*   **Smart Filters**: One-click filter to ignore intentional errors in "Bad Request" examples.

### 🎨 Modern UI/UX
*   **Standalone App**: Single `.exe` file. No Python installation required for end-users.
*   **Responsive Design**: Resizable split-panes and adaptive layouts.
*   **Dark/Light Mode**: Respects system theme preferences.

---

## 📦 Installation

### Option 1: Standalone Executable (Recommended)
1.  Go to the [**Releases**](https://github.com/cernutog/oasis/releases) page.
2.  Download the latest `OASIS.exe`.
3.  Run it. No installation or dependencies needed.

### Option 2: Running from Source
If you are a developer and want to modify the tool:

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/cernutog/oasis.git
    cd oasis
    ```

2.  **Install Dependencies**:
    Requires Python 3.10+.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the App**:
    ```bash
    python src/main.py
    ```

---

## 📖 Usage

1.  **Launch the Application**.
2.  **Select File**: Click the dropdown or use the "Browse" folder icon to select your Excel template (`.xlsm`).
3.  **Generate**: Click the **"Generation"** tab and hit the **Generate** button.
4.  **Validate**: Switch to the **"Validation"** tab.
    *   Select one of the generated YAML files.
    *   Explore the chart and issue list to find and fix discrepancies.
5.  **Documentation**: Use the **Help > User Guide** menu to open the latest documentation (Online or Local fallback).

---

## 🛠️ Built With
*   **Python**: Core logic.
*   **CustomTkinter**: Modern GUI framework.
*   **Pandas / OpenPyXL**: Excel processing.
*   **Spectral**: API Linting engine.
*   **PyInstaller**: For compiling the standalone executable.

---

## 📄 License
[MIT](LICENSE)
