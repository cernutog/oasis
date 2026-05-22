---
description: Build, release metadata, commit, and push OASIS
---

// turbo-all

In OASIS, "build" means build + release metadata + commit + push, unless the user
explicitly asks for a build-only dry run.

1. **Preflight**
   - Read `project rules/rules.txt`.
   - Check `git status --short --branch`.
   - Identify the current branch and push target.
   - Exclude unrelated user changes, `docs/presentations`, and presentation-build
     scripts unless explicitly requested.

2. **Run Build Script**
   Execute the standard build script. It auto-increments the build number.

   ```powershell
   .\build_exe.bat
   ```

3. **Verify Build Output**
   Confirm the build succeeded, `dist/OASIS.exe` exists, and note the final version
   from the terminal output.

4. **Prepare Release Metadata For GitHub Pages**
   Use `release-metadata/` as the versioned source of truth. `dist/` is only
   build output or local staging.

   Prepare or update:

   ```text
   release-metadata/oasis-version.json
   release-metadata/releases/vX.Y.Z.json
   release-metadata/releases/index.json
   ```

   Ensure the startup manifest points to the built version and to the versioned
   SharePoint release folder.

5. **Prepare SharePoint Publication Target**
   Use a versioned folder:

   ```text
   Announcements/vX.Y.Z/OASIS.exe
   ```

   If upload cannot be automated, report the exact local executable path and target
   folder/URL to the user.

6. **Run Verification**
   - Validate JSON syntax.
   - Verify the manifest points to the built version.
   - Verify the release index contains the built version.
   - Run relevant automated tests for any code changes.

7. **Commit And Push**
   Stage only intended files, commit, then push the current branch.

   ```powershell
   git add -- <intended files>
   git commit -m "Build vX.Y.Z: <short release summary>"
   git push origin <current-branch>
   ```

> [!IMPORTANT]
> Never skip the commit and push after a requested build. If push fails, report the
> local commit hash, branch, and reason.
