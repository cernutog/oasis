# API Designer Technical Specification

**Status**: Draft  
**Date**: 2026-04-11  
**Branch**: `API-Designer`

## 1. Purpose

This document defines the target architecture for the new **API Designer** capability inside OASIS.

The API Designer introduces an internal **API Model** that becomes the primary source of truth for designed APIs. Existing and future OpenAPI outputs remain supported, but they are treated as **projections** of the model rather than the master representation.

The design must be:

- compatible with the current OASIS application structure
- lossless with respect to current OpenAPI outputs and the information already handled in Excel templates
- future-proof for advanced OpenAPI features such as `callbacks`
- release-aware, so that planned changes can be assigned, moved, and published through quarterly releases and hotfixes
- ready for reusable shared components used across multiple APIs
- compatible with a future central server repository
- able to preserve and edit custom `x-*` extensions used by the Playground / API Portal ecosystem

## 2. Strategic Decisions Frozen Up Front

The following decisions are considered foundational for the feature and should not be revisited casually:

1. **Primary source of truth**
   The new `API Model` is the primary editable source for the Designer workflow.

2. **Projection-based outputs**
   `OAS 3.0`, `OAS 3.1`, `SWIFT`, and any future output formats are projections generated from the `API Model`.

3. **Main window integration**
   The Designer is not a side dialog. It becomes the **first and primary tab** of the main window.

4. **Dual-source Generation tab**
   The `Generation` tab must support two explicit and mutually exclusive source modes:
   - `Template Folder`
   - `API Model`

5. **Lossless information coverage**
   The `API Model` must be able to store:
   - all OpenAPI 3.1 standard information
   - all information currently carried by the Excel templates
   - all custom `x-*` extensions already used today
   - additional user-defined metadata at fine granularity

6. **Future-proof nested surfaces**
   The model must be designed so that `callbacks` can be added later without architectural rewrites.

7. **Reusable shared components**
   Components must be definable once and reusable across multiple APIs, with reverse usage tracing and change impact visibility.

8. **Release-aware change planning**
   The model must support explicit releases and explicit business changes, so planned modifications can be assigned to one release, moved to another, and projected into outputs without redefining the API from scratch.

9. **Persistence abstraction**
   The architecture must support both:
   - local file-based persistence
   - future central server persistence

   This means the domain model must not be hard-wired to one storage implementation.

## 3. Product Scope

### 3.1 Target Capabilities

The API Designer must eventually support:

- graphical API modeling
- drag & drop hierarchy editing
- property and component reordering
- inline editing of constraints and metadata
- right-click contextual actions
- reusable shared components across APIs
- reverse usage tracing
- update proposals when shared components evolve
- import of an existing OAS into the `API Model`
- projection from the `API Model` into the already supported OAS outputs

### 3.2 Explicit Non-Goals for the First Iterations

The first implementation phases do not need to deliver all of the following immediately:

- full callback editing UI
- collaborative multi-user editing
- database-backed persistence
- automatic migration from every legacy Excel pattern on day one
- bulk refactoring assistants driven by heuristics

The first release should focus on a solid model, reliable persistence, OAS import, OAS projection, and a usable editing shell.

## 4. Main Window Integration

The current application is centered around the main window in [src/gui.py](C:/Users/giuse/.gemini/antigravity/scratch/OASIS/src/gui.py). The new layout direction is:

- `Designer` as first tab and default landing area for model-centric work
- `Generation` as export/build tab
- `Validation` as generated artifact analysis tab
- `View` as generated artifact viewer tab

### 4.1 Generation Tab Source Modes

The `Generation` tab must expose a clear source selector:

- `Template Folder`
- `API Model`

Rules:

- the source mode must be explicit, not inferred
- only one source mode can be active at a time
- the downstream generation flow must behave deterministically according to the active source
- the UI must make it obvious what will be generated from what

### 4.2 Backward Compatibility

The existing template-driven flow remains valid.

This means OASIS will support two parallel authoring concepts for a transition period:

- legacy/current: Excel template folder as source
- new: API Model as source

## 5. Core Architectural Principles

### 5.1 Separation of Concerns

The feature must be split into distinct layers:

- **Domain model**: the `API Model` and related rules
- **Persistence**: saving/loading model packages
- **Importers**: OAS to model, later template-to-model if needed
- **Projectors**: model to OAS 3.0 / 3.1 / SWIFT / others
- **UI state**: tab state, selection, drag operations, inspector state
- **Validation/impact**: usage tracing, revision tracking, update proposals

The UI must never become the only place where the business rules live.

### 5.2 Stable Identity

Every editable entity must have an internal stable identifier independent from its display name.

This is required for:

- safe rename operations
- drag & drop reparenting
- revision tracking
- usage graph stability
- future undo/redo
- accurate diff and impact analysis

### 5.3 Deterministic Persistence

All persisted model files must be deterministic:

- stable ordering
- no UI-only noise mixed with domain data
- version-control friendly text format
- safe roundtrip without silent data loss

### 5.4 No Loss of Existing Semantics

The model must preserve all semantics already supported by the current toolchain, especially:

- OpenAPI constraints
- schema composition
- examples
- responses and headers
- custom extensions
- ordering when required by output expectations

## 6. Proposed Domain Model

The internal model should be an **OpenAPI 3.1 superset**, not a replacement unrelated to OAS.

### 6.1 Top-Level Objects

- `DesignWorkspace`
  Holds the whole modeling workspace.

- `ApiModel`
  Represents one modeled API.

- `SharedComponentLibrary`
  Holds reusable components shared across multiple APIs.

- `MetadataCatalog`
  Stores custom metadata definitions created by users.

- `ReleaseCatalog`
  Stores release definitions such as quarterly releases and hotfixes.

- `ChangeRegistry`
  Stores business changes assigned to releases.

- `DependencyGraph`
  Reverse index and relationship graph between APIs and reusable components.

- `RevisionStore`
  Tracks revisions of reusable components and, later, possibly of APIs.

### 6.2 DesignWorkspace

Suggested responsibilities:

- list of `ApiModel`
- list of shared libraries
- metadata definitions
- release definitions
- changes
- workspace settings
- projection defaults
- import history references

### 6.3 ApiModel

Suggested shape:

- stable `id`
- name and display label
- version metadata
- `info`
- `servers`
- `tags`
- root `path_items`
- local component registry
- references to shared reusable components
- API-level custom metadata
- API-level custom extensions

### 6.4 Primary HTTP Structure

Suggested responsibilities:

- path items
- operations
- parameters at path level
- API-level extensions and metadata on `ApiModel`

The primary API should be modeled directly as `ApiModel -> path_items -> operations`.
Future `callbacks` should remain owned by their parent operation while reusing the same structural primitives.

### 6.5 OperationModel

Suggested fields:

- stable `id`
- method
- path
- operationId
- summary
- description
- tags
- parameters
- request body
- responses
- security
- callbacks collection
- operation-level extensions
- operation-level custom metadata

### 6.6 Schema and Property Modeling

The model must distinguish between:

- reusable schema components
- inline schema structures
- property nodes
- fragment-like reusable property groups

Suggested objects:

- `SchemaModel`
- `PropertyModel`
- `ArrayItemsModel`
- `CombinatorModel`

Each property node should include:

- stable `id`
- name
- parent reference
- sibling order
- type information
- required/nullable/deprecated flags
- constraints
- examples/defaults
- description/summary if applicable
- standard OAS facets
- custom extensions
- custom metadata values

### 6.7 Reusable Components

Reusable shared elements should not be limited to schemas.

The architecture should support:

- schemas
- parameters
- request bodies
- responses
- headers
- examples
- security schemes
- future callback templates if useful
- optional property fragments / field groups as an OASIS-specific reuse concept

Each reusable component should expose:

- stable `id`
- logical name
- component kind
- owning library
- current revision id
- change history
- compatible/incompatible change marker
- usages

### 6.8 Release Planning Objects

Release planning is a first-class concern of the API Model.

The model must distinguish between:

- the structural state of the API
- the modifications proposed or approved for future publication
- the release to which those modifications belong
- the snapshot actually published for a given release

Suggested objects:

- `ReleaseDefinition`
- `Change`
- `ChangeStep`
- `ChangePhase`
- `ReleaseSnapshot`

#### `ReleaseDefinition`

Represents a planned or published release window.

Suggested fields:

- stable `id`
- release code such as `Q2-2026`, `Q3-2026`, `HF-2026-07`
- year
- release family or cadence
- type: `standard`, `extraordinary`, `hotfix`
- target release date
- effective publication date
- status: `planned`, `in_progress`, `frozen`, `published`, `cancelled`
- optional notes

#### `Change`

Represents the primary business change unit planned for one API and assigned to one target release.

Examples:

- add a new endpoint
- add a property
- deprecate a field
- replace a shared component version

Suggested fields:

- stable `id`
- `kind`, typically `CR` or `Errata`
- `external_ref`, such as `CR5262` or `Errata #44312`
- title
- description
- target API id
- assigned release id
- current status
- priority
- dependencies on other change sets
- affected nodes
- author / timestamps
- audit trail of reassignment between releases

The default user-facing assumption is that a `Change` is handled atomically. In most cases there is no need to expose an additional business-level planning object.

#### `ChangeStep`

Represents one ordered technical step recorded inside a business change.

Examples:

- add node
- remove node
- move node
- rename node
- update constraint
- replace component reference
- update extension
- update metadata value

This object is important because a release-aware system cannot rely only on a free-text description of the change. It is also the natural foundation for undo/redo, replay, and detailed history.

#### `ChangePhase`

Represents an optional advanced split of one business change across multiple releases.

This should not complicate the standard workflow. It exists for rare cases where one complex change, usually a large CR, must be split across phases without losing business identity.

Suggested fields:

- stable `id`
- parent change id
- phase name or label
- assigned release id
- subset of associated change steps
- phase status

#### `ReleaseSnapshot`

Represents the frozen API state published for a release.

This is useful for:

- auditability
- regeneration of official artifacts
- comparison with future releases
- branching of hotfixes from a published baseline

The current Excel `General Description` field `release` should be treated as one projected attribute of the selected `ReleaseDefinition`, not as the complete release model.

## 7. Callback-Ready Design

OpenAPI `callbacks` must be considered now even if editing support is phased later.

### 7.1 Architectural Rule

Callbacks must remain **owned by their parent operation** rather than being lifted to a parallel root structure.

This means a callback should reuse the same building blocks as the main API structure:

- path items
- operations
- parameters
- request bodies
- responses
- schemas
- extensions
- metadata

### 7.2 Benefits

- no later domain-model rewrite
- import/export logic remains compositional
- UI can first support read-only visibility, then editing
- future `webhooks` can follow the same pattern

### 7.3 Minimum Phase-1 Requirement

Even before callback editing is implemented, the persistence model and projection layer must be able to preserve callback structures without loss.

## 8. Custom Extensions and Custom Metadata

### 8.1 Custom `x-*` Extensions

Custom extensions are first-class data.

They are currently critical because they help drive the Playground / API Portal simulator behavior. Therefore:

- extensions must be allowed anywhere OAS allows them
- they must also be allowed on OASIS-specific reusable objects where useful
- they must survive import, editing, save, load, and projection without silent loss

### 8.2 Preservation Requirements

The model must preserve:

- key name
- structured value
- scalar value
- list value
- object value
- multiline textual content

Where current generation relies on special formatting expectations, the model should retain enough rendering hints to reproduce compliant YAML output safely.

### 8.3 User-Defined Metadata

User-defined metadata is conceptually different from OAS extensions.

Suggested distinction:

- **OpenAPI extensions**: exported as `x-*` in projections when intended
- **Designer metadata**: internal modeling data, optionally mapped to output later

Suggested metadata definition fields:

- stable `id`
- name
- scope
- primitive or structured type
- allowed values / validation
- cardinality
- default value
- export policy

Supported scopes should include at least:

- workspace
- API
- operation
- component
- schema
- property
- parameter
- request body
- response
- header
- callback

## 9. Release Planning and Change Management

The Designer must support explicit release management for planned modifications.

This is required because teams may decide that a change originally planned for one release must move to a later release without rebuilding the whole API model manually.

### 9.1 Core Concepts

- the API model defines the design space
- business changes define proposed modifications
- change steps define the technical edit trail
- releases define planning and publication targets
- release snapshots define what was actually published

### 9.2 Supported Release Types

The model should support at least:

- quarterly standard releases such as `Q2 2026`, `Q4 2026`
- quarterly extraordinary releases such as `Q1 2026`, `Q3 2026`
- hotfix releases

The exact naming convention can remain configurable, but the type must be explicit in the model.

### 9.3 Required Capabilities

- assign a change to a release
- move a change from one release to another
- show which changes are included in a release
- show which changes were postponed
- freeze a release snapshot
- generate release-specific OAS artifacts
- support hotfix releases starting from a published release snapshot

### 9.4 Projection Rule

Release-aware projection should be based on:

- a baseline API state
- plus all changes included in the selected release scope

This avoids encoding release planning only in free-text notes or filenames.

### 9.5 Change Movement Between Releases

When a team decides to postpone or accelerate planned modifications, the system should preserve:

- the identity of the change
- the original target release
- the new assigned release
- the history of the reassignment
- any dependency conflicts created by the move

### 9.6 Relationship With Shared Components

Release planning must work together with reusable component updates.

Examples:

- a component revision may be scheduled for `Q2 2026`
- one consuming API may adopt it in `Q2 2026`
- another API may postpone adoption to `Q3 2026`

Therefore component adoption itself may be represented by release-bound business changes, backed internally by change steps.

## 10. Dependency Graph and Change Impact

The Designer must maintain a reverse usage index for reusable shared components.

This extends the same need already visible in the dependency tracing logic under [src/oas_diff/dependency_tracer.py](C:/Users/giuse/.gemini/antigravity/scratch/OASIS/src/oas_diff/dependency_tracer.py).

### 10.1 Core Capabilities

- show which APIs use a given reusable component
- show where in the API the usage occurs
- show which revision is currently adopted
- detect when a library component changed after adoption
- mark APIs as potentially impacted
- support preview of proposed updates

### 10.2 Suggested Relationship Objects

- `UsageEdge`
  Connects an API node to a reusable component revision.

- `ImpactRecord`
  Represents the effect of a component change on a consumer API.

- `UpdateProposal`
  Represents a candidate update from one adopted revision to another.

### 10.3 Impact Strategy

The graph should support both:

- direct usage
- transitive usage through nested schemas/components

This is important because a component change can impact an API indirectly through another shared component.

## 11. Persistence Strategy

The persistence strategy should be **hybrid by architecture**:

- local authoring should work with versionable text files
- future central repository support should use a database-backed implementation

The domain model must be independent from the concrete storage backend.

### 11.1 Persistence Goals

- git-friendly
- human-inspectable
- deterministic
- easy backup
- safe merge behavior
- ready for server-side indexing and querying

### 11.2 Recommended Initial Local Packaging

Suggested package structure:

```text
API Models/
  <workspace-name>/
    workspace.yaml
    apis/
      <api-id>.yaml
    libraries/
      <library-id>.yaml
    metadata/
      catalog.yaml
    revisions/
      <component-id>/
        <revision-id>.yaml
```

This is only a starting structure, but the key idea should remain:

- workspace-level manifest
- one logical entity per file where possible
- text-based storage
- deterministic ordering rules

### 11.3 Future Central Repository

For a future central server, the recommended direction is:

- relational database for authoritative storage
- PostgreSQL as the preferred initial choice
- document snapshots stored as structured payloads
- indexed relational links for usages, revisions, releases, and change sets

Reasons:

- reverse usage tracing is query-heavy
- revision and adoption tracking are relational by nature
- release planning and change reassignment need auditability
- concurrent editing and locking are better handled with transactional semantics

Suggested central storage approach:

- normalized tables for core identifiers and relationships
- `JSONB` payload columns for full canonical snapshots where useful
- audit tables for reassignment, publication, and revision history

### 11.4 Persistence Abstraction

The application should define a repository abstraction from the beginning.

Suggested implementations:

- `FileSystemRepository`
- `ServerRepository`

This avoids coupling the Designer domain model to only one storage mode.

### 11.5 UI State Exclusion

UI-only state must not pollute domain persistence.

Examples of UI-only state:

- splitter positions
- expanded/collapsed tree nodes
- last selected node
- temporary drag targets

These may be stored separately in preferences, but not mixed into the domain package.

## 12. Import and Projection Flows

### 12.1 OAS to API Model

This is a first-class requirement because it is the easiest migration path for existing APIs.

The importer must:

- read existing OAS 3.x files
- preserve standard content
- preserve custom extensions
- preserve callbacks if present, even if editing is delayed
- create stable internal identities
- populate a complete `ApiModel`

### 12.2 API Model to OAS

The projection layer must generate the currently supported OAS outputs from the model:

- OAS 3.1
- OAS 3.0
- SWIFT variant if applicable

The projector should reuse as much as possible from the current generation knowledge, but without forcing the Designer domain model to mirror legacy generator internals.

### 12.3 Release-Aware Projection

The projection layer must be able to generate artifacts for a selected release context.

Examples:

- current working draft
- planned `Q2 2026`
- postponed `Q3 2026`
- published hotfix baseline

Release-aware generation should use the release definition plus the applicable change sets rather than relying only on a manually typed release string.
Release-aware generation should use the release definition plus the applicable changes rather than relying only on a manually typed release string.

### 12.4 Excel Relation

The existing template-driven generation remains supported as a separate source mode.

The new model must nevertheless be able to represent all semantics currently carried by Excel templates, including:

- component definitions
- constraints
- examples
- headers
- request/response structures
- custom extensions

If later desired, a dedicated `Template -> API Model` importer can be added without changing the model itself.

## 13. UI Concept for the Designer Tab

The API Designer tab should eventually use a three-panel editing experience:

- left: workspace explorer
- center: hierarchical modeling canvas/editor
- right: inspector for attributes, constraints, metadata, and extensions

Optional lower pane or sub-tab:

- usages
- validation
- revision history
- import/export messages

### 13.1 Interaction Rules

- **single click**
  Select node and show its attributes immediately in the inspector.

- **right click**
  Open contextual actions for the selected node.

- **drag & drop**
  Support sibling reorder and hierarchy move when valid.

- **double click**
  Optional shortcut for rename or focused edit, not mandatory in the first version.

### 13.2 Important UX Safeguards

- undo/redo support should be part of the architecture, even if delivered later
- drag operations need visible drop indicators and invalid-target feedback
- destructive actions must be explicit
- component replacement and extraction flows need previews

### 13.3 Technical Direction

The current app uses `customtkinter`. The Designer should keep the visual language coherent with the application, but the hierarchy editor should not be constrained by simplistic stock tree widgets if they limit interaction quality.

## 14. Validation and Quality Gates

The Designer workflow should validate at two levels:

1. **Model-level validation**
   Structural integrity, required identities, reuse graph consistency, metadata validity, callback containment rules, ordering consistency.

2. **Projection-level validation**
   Validate exported OAS with the existing linter pipeline, especially Spectral.

The current project rule that Spectral checks are mandatory remains valid for generated OAS artifacts.

## 15. Suggested Incremental Rollout

### Phase 1 - Model Foundation

- define the `API Model`
- define persistence format
- define custom metadata model
- define release/change objects
- make the model callback-ready

### Phase 2 - OAS Import

- implement `OAS -> API Model`
- preserve extensions and callbacks
- create stable identities

### Phase 3 - OAS Projection

- implement `API Model -> OAS 3.1`
- implement `API Model -> OAS 3.0`
- support release-aware projection
- integrate with existing validation flow

### Phase 4 - Main Window Integration

- add `Designer` as the first tab
- update startup/default tab behavior
- add `API Model` source mode to `Generation`

### Phase 5 - Basic Editing Shell

- workspace explorer
- selection model
- inspector
- basic node editing without full drag & drop

### Phase 6 - Advanced Graphical Editing

- drag & drop
- reorder
- hierarchy changes
- context menus
- inline editing refinement

### Phase 7 - Shared Components and Impact Analysis

- libraries
- usage tracking
- revision tracking
- update proposals

### Phase 8 - Release Planning Workflows

- release dashboard
- change assignment and reassignment
- release freeze / snapshot creation
- hotfix branching from published baselines

### Phase 9 - Advanced OpenAPI Features

- callback editing UI
- webhook support if needed
- richer reuse patterns

## 16. Immediate Design Constraints for Implementation

Any implementation started from this specification should respect these practical constraints:

- do not hardcode business data outside the source model
- keep deterministic output behavior
- do not make the UI the only source of domain truth
- preserve custom extension fidelity
- avoid architectural choices that would block callback support later
- do not encode release planning only in filenames or free-text fields
- keep the persistence package text-based and versionable

## 17. Recommended Next Deliverable

The next implementation-oriented document should be a **data contract specification** containing:

- the exact persisted schema for `workspace.yaml`
- the exact persisted schema for `ApiModel`
- the exact representation for reusable components
- the exact representation for metadata definitions and values
- the exact representation for `ReleaseDefinition`, `Change`, `ChangeStep`, optional `ChangePhase`, and `ReleaseSnapshot`
- the exact representation for callbacks and nested surfaces
- the repository abstraction for local file persistence and future server persistence
- import mapping rules from OAS objects into the internal model

That follow-up document will turn this architectural specification into an executable implementation plan.
