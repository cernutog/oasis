OASIS project instructions

Before every response, action, code edit, build, commit, or explanation in this repository, read and apply the rules in:

- project rules/rules.txt

Mandatory preflight:

1. Identify whether the next output is analysis, proposal, code edit, build, commit, explanation, or verification.
2. Do not modify code or behavior unless the user has explicitly authorized implementation after the strategy is clear.
3. Treat Excel templates and existing project configuration/preferences as the source of truth.
4. Do not introduce hard-coded data, ad-hoc heuristics, silent fallbacks, or source-data fixes in code.
5. Prefer fixing the upstream data structure or algorithm over applying a posterior correction.
6. If source data is missing, inconsistent, or ambiguous, report it clearly instead of inventing values.
7. When behavior changes, explain impact and verification evidence.
8. Before claiming completion, run the relevant checks or state exactly what could not be verified.

If any planned output fails this preflight, stop and ask the user or explain the blocker before proceeding.
