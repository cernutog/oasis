---
name: Build OASIS
description: Build OASIS, prepare release manifests, commit, and push.
---

# Build OASIS

This skill defines the standard OASIS release workflow. In this project, a request to
`build` means:

1. build the executable;
2. prepare the versioned GitHub Pages update manifest/release-note JSON files;
3. prepare the SharePoint release folder instructions for the executable;
4. commit the versioned changes;
5. push the current branch.

Do not stop after producing `dist/OASIS.exe` unless the user explicitly asks for a
build-only dry run.

## Mandatory Preflight

Before taking action:

1. Read `project rules/rules.txt`.
2. Check `git status --short --branch`.
3. Confirm the current branch and push target.
4. Exclude unrelated user changes from the build commit unless the user explicitly
   asks to include them.
5. Do not include `docs/presentations` or presentation-build scripts unless the user
   explicitly asks for them.

## Build

1. Stop running OASIS instances so the executable is not locked:

   ```powershell
   taskkill /F /IM "OASIS.exe" /T
   ```

   It is safe to ignore the "process not found" error.

2. Run the standard build script from the repository root:

   ```powershell
   .\build_exe.bat
   ```

3. Read the build output and identify the final version, for example `3.0.12`.

## Version Management

Do not manually edit `BUILD_NUMBER` in `src/version.py` before a standard build.

`build_exe.bat` automatically:

1. reads the current `BUILD_NUMBER`;
2. increments it by one;
3. writes the new value back to `src/version.py`;
4. builds the executable using the new version.

Manual edits before the build can skip version numbers.

## Release Manifest And Pages

For every successful build, prepare the update metadata for GitHub Pages.

The versioned source of truth for release metadata is:

```text
release-metadata/
```

Use this structure:

```text
release-metadata/
  oasis-version.json
  releases/
    index.json
    vX.Y.Z.json
```

Where:

- `oasis-version.json` is the lightweight startup manifest.
- `releases/vX.Y.Z.json` contains the detailed notes for the built release.
- `releases/index.json` indexes all public releases from the update baseline onward.

The startup manifest must point to the newly built version:

```json
{
  "version": "X.Y.Z",
  "download_url": "<SharePoint release executable URL>",
  "announcement_url": "<Teams announcement URL, if available>",
  "release_manifest_url": "https://cernutog.github.io/oasis/releases/vX.Y.Z.json",
  "release_index_url": "https://cernutog.github.io/oasis/releases/index.json",
  "release_notes": "<short release summary>",
  "preferences_override": {}
}
```

The release note file must contain the release-specific "what's new" data:

```json
{
  "version": "X.Y.Z",
  "date": "YYYY-MM-DD",
  "title": "<release title>",
  "release_notes": [
    "<user-facing change>",
    "<user-facing change>"
  ],
  "download_url": "<SharePoint release executable URL>",
  "announcement_url": "<Teams announcement URL, if available>"
}
```

The release index file should remain an index, not a duplicate copy of every note:

```json
{
  "baseline": "X.Y.0",
  "releases": [
    {
      "version": "X.Y.Z",
      "manifest_url": "https://cernutog.github.io/oasis/releases/vX.Y.Z.json"
    }
  ]
}
```

Keep entries sorted newest first unless an existing file clearly uses a different
stable order.

`dist/` is build output and may be used only as local staging. Do not treat `dist/`
as the canonical location for release notes or manifests because it is ignored by
Git.

## SharePoint Release Layout

The executable must be published under a versioned SharePoint folder:

```text
Announcements/
  vX.Y.Z/
    OASIS.exe
```

Optionally maintain:

```text
Announcements/
  latest/
    OASIS.exe
```

The versioned folder is the stable release location. `latest` is only a convenience
shortcut and must not be the only download target in the manifest.

If publishing to SharePoint cannot be automated in the current environment, report
the exact local executable path and the expected SharePoint target folder/URL.

## Verification

Before committing:

1. Confirm `dist/OASIS.exe` exists and has the expected version.
2. Validate that the JSON files are syntactically valid.
3. Verify that `oasis-version.json` points to the built version.
4. Verify that the release index contains the built version.
5. Run relevant automated tests when the build includes code changes.
6. If tests or publication steps cannot be run, report the exact gap.

## Commit And Push

After a successful build and manifest preparation:

1. Stage only the intended files.
2. Commit with this format:

   ```powershell
   git commit -m "Build vX.Y.Z: <short release summary>"
   ```

3. Push the current branch:

   ```powershell
   git push origin <current-branch>
   ```

4. Verify the branch is not left ahead of upstream.

If push cannot be completed, report the local commit hash, branch, and reason.
