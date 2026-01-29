---
description: Build and Commit OASIS
---

// turbo-all

1.  **Update Implementation History**
    Ensure `IMPLEMENTATION_HISTORY.md` has a new entry for the upcoming version. If the current version is `1.8.116`, the new one will be `1.8.117`.

2.  **Run Build Script**
    Execute the build script to auto-increment the version and generate the executable.
    ```powershell
    .\build_exe.bat
    ```

3.  **Verify Build Output**
    Confirm the build succeeded and note the final version number from the terminal output.

4.  **Commit Immediately**
    Add all changes (including the updated `version.py` and `IMPLEMENTATION_HISTORY.md`) and commit.
    ```powershell
    git add .
    git commit -m "Build v1.8.XXX: <Description of changes>"
    ```

> [!IMPORTANT]
> **NEVER skip the commit step.** This is the only way to ensure stability and allow for reliable reverts.
