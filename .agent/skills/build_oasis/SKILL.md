---
name: Build OASIS
description: Kills running OASIS instances and rebuilds the executable.
---

# Build OASIS

This skill builds the OASIS project into a standalone executable using `PyInstaller`.

## Prerequisites
- Windows OS
- Repository cloned locally

## Instructions

1.  **Kill Running Tasks**
    Stop any running instances of `OASIS.exe` and `python.exe` (related to the project) to ensure the build files aren't locked.
    ```powershell
    taskkill /F /IM "OASIS.exe" /T
    ```
    *(Note: It is safe to ignore error "The process ... not found" if it's not running).*

2.  **Run Build Script**
    Execute the `build_exe.bat` script located in the project root.
    ```powershell
    .\build_exe.bat
    ```

## ⚠️ CRITICAL: Version Management

**DO NOT manually edit `BUILD_NUMBER` in `src/version.py` before running the build.**

The `build_exe.bat` script **automatically increments** the build number:
1. Reads current `BUILD_NUMBER` from `src/version.py`
2. Increments it by 1
3. Writes the new value back to `src/version.py`
4. Builds with the new version

**If you manually edit version.py first**, the build number will increment **twice**:
- Manual edit: 30 → 31
- Script auto-increment: 31 → 32
- Result: Version 31 is skipped entirely

**Correct workflow**: Just run `build_exe.bat` directly. The script handles versioning automatically.

3.  **Verify Output**
    Check that the build completed successfully (Look for "Build SUCCESSFUL" message).
    The output executable will be at `dist/OASIS.exe`.

4.  **Commit and Tag Changes**
    After a successful build, commit the changes to source control.
    -   **Message**: Should start with `Build v1.5.XX` followed by a descriptive summary of changes.
    -   **Files**: Ensure `src/version.py` is included (it contains the incremented build number).
    ```powershell
    git add .
    git commit -m "Build v1.5.XX: <Description of changes>"
    ```
