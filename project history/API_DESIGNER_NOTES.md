# API Designer Working Notes

**Status**: Working notes  
**Date**: 2026-04-11  
**Branch**: `API-Designer`

## Purpose

This document captures product, domain, and workflow notes gathered while shaping the API Designer feature.

It is intentionally less formal than [API_DESIGNER_SPEC.md](C:/Users/giuse/.gemini/antigravity/scratch/OASIS/project%20history/API_DESIGNER_SPEC.md). Its role is to preserve business vocabulary, planning concepts, and operational examples before the final data contract is defined.

## Frozen Product Direction

- `API Model` is the primary source of truth for Designer-driven APIs.
- OpenAPI outputs are projections of the model.
- The `Designer` should become the first tab of the main window.
- The `Generation` tab should support two explicit source modes:
  - `Template Folder`
  - `API Model`
- Existing OAS files must be importable into the `API Model`.
- The model must remain lossless for current Excel-carried information and current custom extensions.

## Business Vocabulary

### Change

In the business context, a modification usually originates from one identifiable item:

- `CR`
- `Errata`

Examples:

- `CR5262`
- `Errata #44312`

These should be modeled through one abstract business object:

- `Change`

Recommended fields:

- internal stable `id`
- `kind`
- `external_ref`
- `title`
- `description`
- `target_release_id`
- `status`
- `priority` or `severity`
- `api_scope`
- timestamps and audit info

Important note:

- `Errata` also has its own identifier and must be treated like the other change kinds
- future item kinds should be possible without changing the whole model

### Release

The business works with quarterly releases and hotfixes.

Observed release patterns:

- `Q2` and `Q4` are usually standard releases
- `Q1` and `Q3` are usually extraordinary releases
- hotfixes may exist outside the normal cadence

The model must not reduce release handling to a plain string field.

The current Excel `General Description -> release` value should be seen as a projected attribute of the release selected for generation.

## Planning Model Notes

### Change as the Primary Planning Unit

The default planning unit for designers should be the `Change`.

This keeps the workflow simple because, in most real cases:

- a CR is treated atomically
- an errata is treated atomically

Therefore the UI should not force designers to manage an additional explicit business-planning concept beyond `Change` in the normal flow.

### ChangeStep as Internal Technical Unit

Even if the designer works mainly with `Change`, the system still needs an internal unit of technical modification.

Suggested internal concept:

- `ChangeStep`

Examples:

- add endpoint
- remove endpoint
- rename node
- add property
- update property type
- update constraint
- move property in hierarchy
- replace component reference
- change custom extension
- change metadata value

`ChangeStep` is needed for:

- undo/redo
- history/audit
- release-specific projection
- change split in advanced scenarios
- diff between baseline and target release
- creation of release snapshots

### Optional Split for Complex Changes

Most changes should stay simple and atomic from the designer point of view.

However, some complex CRs may need to be split across multiple releases.

Recommended direction:

- do not expose split as the default workflow
- support it as an advanced capability
- represent split through optional phases or partitions of one `Change`
- each phase contains a subset of `ChangeStep`

This gives a practical balance:

- normal case remains simple
- complex case remains possible

## Q4 2026 Example Workflow

Example scenario:

- one new endpoint must be added
- one property of another endpoint must be modified
- both changes are initially planned for `Q4 2026`

Suggested flow:

1. Create or select the release definition for `Q4 2026`.
2. Create one or more `Change` records that represent the business drivers.
3. In the `Designer`, attach modifications to the relevant change.
4. Record each technical edit as a `ChangeStep`.
5. View the release projection as:
   - baseline
   - plus changes included in `Q4 2026`
6. Generate OAS artifacts from:
   - source mode `API Model`
   - release context `Q4 2026`
7. Validate the projected artifacts.
8. Freeze the release and create a release snapshot when ready.

If the work must slip:

- the `Change` is reassigned to a later release
- or, in complex cases, only part of its change steps are moved into a later phase/release

## Shared Components and Release Adoption

Reusable components and release planning are connected.

Examples:

- a shared component revision may be available before all APIs adopt it
- one API may adopt it in `Q4 2026`
- another API may adopt it in a later release

This means component adoption should be representable as a planned modification associated with a change and a release.

## Custom Extensions

Custom `x-*` extensions are critical because they are used to drive simulator behavior in the Playground / API Portal context.

Notes:

- they must be first-class data
- they must survive OAS import and projection
- they must be editable in the Designer
- they may appear at many levels, including operation, schema, property, and future callback surfaces

## Callback Note

Callbacks are not required immediately in the UI, but the model must remain callback-ready.

The safest direction remains:

- keep callbacks owned by the parent operation
- reuse the same building blocks used by the main API path/operation structure

This avoids future structural rewrites.

## Local and Central Persistence

Recommended persistence direction:

- local authoring: versionable file package
- future central repository: database-backed implementation

Reason:

- central querying for usages, revisions, releases, and audit history is relational in nature
- release reassignment and traceability are better served by database semantics

## UX Notes

- designers should primarily think in terms of APIs, changes, and releases
- advanced constructs should not clutter the default editing flow
- single click should expose editable attributes
- right click should expose contextual actions
- the `Model` tree should own structural hierarchy and navigation
- the `Inspector` should edit only the direct attributes of the selected node
- nested OAS structures such as `content`, media types, `schema`, `properties`, `items`, `responses`, `headers`, `links`, `examples` and similar should be navigated as dedicated tree nodes instead of being recursively expanded inside the inspector
- drag & drop will need `ChangeStep` recording from the start
- OAS-only technical sections should be hidden when not applicable, rather than shown empty by default
- Example: `Server Variables` should only be shown when the selected server URL actually contains placeholders such as `{environment}` or `{version}`
- schema editing should use an explicit definition mode selector: `Simple`, `Reference`, `All Of`, `Any Of`, `One Of`
- schema composition modes should be treated as an alternative way of defining a schema, not as low-level details buried under a generic schema form

## Open Questions

- how visible should `ChangeStep` history be in the UI
- whether split phases should be named explicitly by users or auto-generated
- how release dashboards should summarize included and postponed changes
- how much of the release/change workflow should be available in the first UI iteration

## Recommended Next Step

The next data-modeling document should explicitly define:

- `Change`
- `ChangeStep`
- `ReleaseDefinition`
- `ReleaseSnapshot`
- optional `ChangePhase`
- the relationship between changes, change steps, reusable components, and projections
