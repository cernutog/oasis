---
description: Commit and push approved OASIS changes
---

// turbo-all

In OASIS, "commit" means commit + push, unless the user explicitly asks to keep the
commit local.

1. **Preflight**
   - Read `project rules/rules.txt`.
   - Check `git status --short --branch`.
   - Stage only approved/intended files.
   - Do not include unrelated user changes.

2. **Stage Intended Files**

   ```powershell
   git add -- <intended files>
   ```

3. **Commit**

   ```powershell
   git commit -m "<clear commit message>"
   ```

4. **Push Current Branch**

   ```powershell
   git push origin <current-branch>
   ```

5. **Verify**
   Confirm the branch is not left ahead of upstream. If push fails, report the local
   commit hash, branch, and reason.
