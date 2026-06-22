"""Initial API Designer domain model.

The model is intentionally independent from tkinter and from the legacy Excel
generation pipeline. OpenAPI artifacts are projections of this model, not the
authoritative representation.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from uuid import uuid4


WORKSPACE_SCHEMA_VERSION = "api-designer.workspace/v1"
API_SCHEMA_VERSION = "api-designer.api/v1"
METADATA_CATALOG_SCHEMA_VERSION = "api-designer.metadata-catalog/v1"


def make_id(prefix: str) -> str:
    """Create a stable internal identifier for a new model entity."""
    return f"{prefix}_{uuid4().hex[:12]}"


def _copy_mapping(value: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    return deepcopy(value) if value else {}


def _copy_list(value: Optional[List[Any]]) -> List[Any]:
    return deepcopy(value) if value else []


def _without_none(data: Dict[str, Any]) -> Dict[str, Any]:
    return {key: value for key, value in data.items() if value is not None}


@dataclass
class MetadataDefinition:
    id: str = field(default_factory=lambda: make_id("meta"))
    name: str = ""
    scope: str = "workspace"
    value_type: str = "string"
    cardinality: str = "single"
    allowed_values: List[Any] = field(default_factory=list)
    default_value: Any = None
    export_policy: str = "internal"
    extensions: Dict[str, Any] = field(default_factory=dict)
    custom_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return _without_none(
            {
                "id": self.id,
                "name": self.name,
                "scope": self.scope,
                "value_type": self.value_type,
                "cardinality": self.cardinality,
                "allowed_values": _copy_list(self.allowed_values),
                "default_value": deepcopy(self.default_value),
                "export_policy": self.export_policy,
                "extensions": _copy_mapping(self.extensions),
                "custom_metadata": _copy_mapping(self.custom_metadata),
            }
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MetadataDefinition":
        return cls(
            id=data.get("id") or make_id("meta"),
            name=data.get("name", ""),
            scope=data.get("scope", "workspace"),
            value_type=data.get("value_type", "string"),
            cardinality=data.get("cardinality", "single"),
            allowed_values=_copy_list(data.get("allowed_values")),
            default_value=deepcopy(data.get("default_value")),
            export_policy=data.get("export_policy", "internal"),
            extensions=_copy_mapping(data.get("extensions")),
            custom_metadata=_copy_mapping(data.get("custom_metadata")),
        )


@dataclass
class ReleaseDefinition:
    id: str = field(default_factory=lambda: make_id("rel"))
    code: str = ""
    year: Optional[int] = None
    family: str = ""
    release_type: str = "standard"
    target_date: str = ""
    publication_date: str = ""
    status: str = "planned"
    notes: str = ""
    extensions: Dict[str, Any] = field(default_factory=dict)
    custom_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return _without_none(
            {
                "id": self.id,
                "code": self.code,
                "year": self.year,
                "family": self.family,
                "release_type": self.release_type,
                "target_date": self.target_date,
                "publication_date": self.publication_date,
                "status": self.status,
                "notes": self.notes,
                "extensions": _copy_mapping(self.extensions),
                "custom_metadata": _copy_mapping(self.custom_metadata),
            }
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ReleaseDefinition":
        return cls(
            id=data.get("id") or make_id("rel"),
            code=data.get("code", ""),
            year=data.get("year"),
            family=data.get("family", ""),
            release_type=data.get("release_type", "standard"),
            target_date=data.get("target_date", ""),
            publication_date=data.get("publication_date", ""),
            status=data.get("status", "planned"),
            notes=data.get("notes", ""),
            extensions=_copy_mapping(data.get("extensions")),
            custom_metadata=_copy_mapping(data.get("custom_metadata")),
        )


@dataclass
class ChangeStep:
    """One ordered technical step inside a business Change."""

    id: str = field(default_factory=lambda: make_id("step"))
    order: int = 0
    kind: str = ""
    target_id: str = ""
    path: str = ""
    before: Any = None
    after: Any = None
    payload: Dict[str, Any] = field(default_factory=dict)
    status: str = "planned"
    extensions: Dict[str, Any] = field(default_factory=dict)
    custom_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return _without_none(
            {
                "id": self.id,
                "order": self.order,
                "kind": self.kind,
                "target_id": self.target_id,
                "path": self.path,
                "before": deepcopy(self.before),
                "after": deepcopy(self.after),
                "payload": _copy_mapping(self.payload),
                "status": self.status,
                "extensions": _copy_mapping(self.extensions),
                "custom_metadata": _copy_mapping(self.custom_metadata),
            }
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChangeStep":
        return cls(
            id=data.get("id") or make_id("step"),
            order=int(data.get("order", 0) or 0),
            kind=data.get("kind", ""),
            target_id=data.get("target_id", ""),
            path=data.get("path", ""),
            before=deepcopy(data.get("before")),
            after=deepcopy(data.get("after")),
            payload=_copy_mapping(data.get("payload")),
            status=data.get("status", "planned"),
            extensions=_copy_mapping(data.get("extensions")),
            custom_metadata=_copy_mapping(data.get("custom_metadata")),
        )


@dataclass
class ChangePhase:
    id: str = field(default_factory=lambda: make_id("phase"))
    name: str = ""
    assigned_release_id: str = ""
    step_ids: List[str] = field(default_factory=list)
    status: str = "planned"
    extensions: Dict[str, Any] = field(default_factory=dict)
    custom_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "assigned_release_id": self.assigned_release_id,
            "step_ids": _copy_list(self.step_ids),
            "status": self.status,
            "extensions": _copy_mapping(self.extensions),
            "custom_metadata": _copy_mapping(self.custom_metadata),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChangePhase":
        return cls(
            id=data.get("id") or make_id("phase"),
            name=data.get("name", ""),
            assigned_release_id=data.get("assigned_release_id", ""),
            step_ids=_copy_list(data.get("step_ids")),
            status=data.get("status", "planned"),
            extensions=_copy_mapping(data.get("extensions")),
            custom_metadata=_copy_mapping(data.get("custom_metadata")),
        )


@dataclass
class Change:
    id: str = field(default_factory=lambda: make_id("chg"))
    kind: str = "CR"
    external_ref: str = ""
    title: str = ""
    description: str = ""
    target_api_id: str = ""
    assigned_release_id: str = ""
    status: str = "planned"
    priority: str = ""
    dependencies: List[str] = field(default_factory=list)
    affected_node_ids: List[str] = field(default_factory=list)
    steps: List[ChangeStep] = field(default_factory=list)
    phases: List[ChangePhase] = field(default_factory=list)
    audit_trail: List[Dict[str, Any]] = field(default_factory=list)
    extensions: Dict[str, Any] = field(default_factory=dict)
    custom_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind,
            "external_ref": self.external_ref,
            "title": self.title,
            "description": self.description,
            "target_api_id": self.target_api_id,
            "assigned_release_id": self.assigned_release_id,
            "status": self.status,
            "priority": self.priority,
            "dependencies": _copy_list(self.dependencies),
            "affected_node_ids": _copy_list(self.affected_node_ids),
            "steps": [step.to_dict() for step in sorted(self.steps, key=lambda item: item.order)],
            "phases": [phase.to_dict() for phase in self.phases],
            "audit_trail": _copy_list(self.audit_trail),
            "extensions": _copy_mapping(self.extensions),
            "custom_metadata": _copy_mapping(self.custom_metadata),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Change":
        return cls(
            id=data.get("id") or make_id("chg"),
            kind=data.get("kind", "CR"),
            external_ref=data.get("external_ref", ""),
            title=data.get("title", ""),
            description=data.get("description", ""),
            target_api_id=data.get("target_api_id", ""),
            assigned_release_id=data.get("assigned_release_id", ""),
            status=data.get("status", "planned"),
            priority=data.get("priority", ""),
            dependencies=_copy_list(data.get("dependencies")),
            affected_node_ids=_copy_list(data.get("affected_node_ids")),
            steps=[ChangeStep.from_dict(item) for item in data.get("steps", [])],
            phases=[ChangePhase.from_dict(item) for item in data.get("phases", [])],
            audit_trail=_copy_list(data.get("audit_trail")),
            extensions=_copy_mapping(data.get("extensions")),
            custom_metadata=_copy_mapping(data.get("custom_metadata")),
        )


@dataclass
class OperationModel:
    id: str = field(default_factory=lambda: make_id("op"))
    method: str = "get"
    path: str = ""
    operation_id: str = ""
    summary: str = ""
    description: str = ""
    tags: List[str] = field(default_factory=list)
    parameters: List[Dict[str, Any]] = field(default_factory=list)
    request_body: Dict[str, Any] = field(default_factory=dict)
    responses: Dict[str, Any] = field(default_factory=dict)
    security: List[Dict[str, Any]] = field(default_factory=list)
    servers: List[Dict[str, Any]] = field(default_factory=list)
    external_docs: Dict[str, Any] = field(default_factory=dict)
    deprecated: Optional[bool] = None
    callbacks: List["PathItemModel"] = field(default_factory=list)
    extensions: Dict[str, Any] = field(default_factory=dict)
    custom_metadata: Dict[str, Any] = field(default_factory=dict)
    extra_fields: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return _without_none(
            {
                "id": self.id,
                "method": self.method.lower(),
                "path": self.path,
                "operation_id": self.operation_id,
                "summary": self.summary,
                "description": self.description,
                "tags": _copy_list(self.tags),
                "parameters": _copy_list(self.parameters),
                "request_body": _copy_mapping(self.request_body),
                "responses": _copy_mapping(self.responses),
                "security": _copy_list(self.security),
                "servers": _copy_list(self.servers),
                "external_docs": _copy_mapping(self.external_docs),
                "deprecated": self.deprecated,
                "callbacks": [callback.to_dict() for callback in self.callbacks],
                "extensions": _copy_mapping(self.extensions),
                "custom_metadata": _copy_mapping(self.custom_metadata),
                "extra_fields": _copy_mapping(self.extra_fields),
            }
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OperationModel":
        return cls(
            id=data.get("id") or make_id("op"),
            method=data.get("method", "get").lower(),
            path=data.get("path", ""),
            operation_id=data.get("operation_id", ""),
            summary=data.get("summary", ""),
            description=data.get("description", ""),
            tags=_copy_list(data.get("tags")),
            parameters=_copy_list(data.get("parameters")),
            request_body=_copy_mapping(data.get("request_body")),
            responses=_copy_mapping(data.get("responses")),
            security=_copy_list(data.get("security")),
            servers=_copy_list(data.get("servers")),
            external_docs=_copy_mapping(data.get("external_docs")),
            deprecated=data.get("deprecated"),
            callbacks=[PathItemModel.from_dict(item) for item in data.get("callbacks", [])],
            extensions=_copy_mapping(data.get("extensions")),
            custom_metadata=_copy_mapping(data.get("custom_metadata")),
            extra_fields=_copy_mapping(data.get("extra_fields")),
        )

    def to_oas_dict(self) -> Dict[str, Any]:
        data = _copy_mapping(self.extra_fields)
        if self.tags:
            data["tags"] = _copy_list(self.tags)
        if self.summary:
            data["summary"] = self.summary
        if self.description:
            data["description"] = self.description
        if self.external_docs:
            data["externalDocs"] = _copy_mapping(self.external_docs)
        if self.operation_id:
            data["operationId"] = self.operation_id
        if self.parameters:
            data["parameters"] = _copy_list(self.parameters)
        if self.request_body:
            data["requestBody"] = _copy_mapping(self.request_body)
        if self.responses:
            data["responses"] = _copy_mapping(self.responses)
        if self.deprecated is not None:
            data["deprecated"] = self.deprecated
        if self.security:
            data["security"] = _copy_list(self.security)
        if self.servers:
            data["servers"] = _copy_list(self.servers)
        if self.callbacks:
            data["callbacks"] = {
                callback.path: callback.to_oas_path_item()
                for callback in self.callbacks
            }
        data.update(_copy_mapping(self.extensions))
        return data


@dataclass
class PathItemModel:
    id: str = field(default_factory=lambda: make_id("path"))
    path: str = ""
    summary: str = ""
    description: str = ""
    ref: str = ""
    parameters: List[Dict[str, Any]] = field(default_factory=list)
    servers: List[Dict[str, Any]] = field(default_factory=list)
    operations: List[OperationModel] = field(default_factory=list)
    extensions: Dict[str, Any] = field(default_factory=dict)
    custom_metadata: Dict[str, Any] = field(default_factory=dict)
    extra_fields: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return _without_none(
            {
                "id": self.id,
                "path": self.path,
                "summary": self.summary,
                "description": self.description,
                "ref": self.ref,
                "parameters": _copy_list(self.parameters),
                "servers": _copy_list(self.servers),
                "operations": [operation.to_dict() for operation in self.operations],
                "extensions": _copy_mapping(self.extensions),
                "custom_metadata": _copy_mapping(self.custom_metadata),
                "extra_fields": _copy_mapping(self.extra_fields),
            }
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PathItemModel":
        return cls(
            id=data.get("id") or make_id("path"),
            path=data.get("path", ""),
            summary=data.get("summary", ""),
            description=data.get("description", ""),
            ref=data.get("ref", ""),
            parameters=_copy_list(data.get("parameters")),
            servers=_copy_list(data.get("servers")),
            operations=[OperationModel.from_dict(item) for item in data.get("operations", [])],
            extensions=_copy_mapping(data.get("extensions")),
            custom_metadata=_copy_mapping(data.get("custom_metadata")),
            extra_fields=_copy_mapping(data.get("extra_fields")),
        )

    def to_oas_path_item(self) -> Dict[str, Any]:
        data = _copy_mapping(self.extra_fields)
        if self.ref:
            data["$ref"] = self.ref
        if self.summary:
            data["summary"] = self.summary
        if self.description:
            data["description"] = self.description
        if self.parameters:
            data["parameters"] = _copy_list(self.parameters)
        if self.servers:
            data["servers"] = _copy_list(self.servers)
        for operation in self.operations:
            data[operation.method.lower()] = operation.to_oas_dict()
        data.update(_copy_mapping(self.extensions))
        return data


@dataclass
class ReusableComponent:
    id: str = field(default_factory=lambda: make_id("cmp"))
    name: str = ""
    component_kind: str = "schema"
    current_revision_id: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    usages: List[Dict[str, Any]] = field(default_factory=list)
    extensions: Dict[str, Any] = field(default_factory=dict)
    custom_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "component_kind": self.component_kind,
            "current_revision_id": self.current_revision_id,
            "payload": _copy_mapping(self.payload),
            "usages": _copy_list(self.usages),
            "extensions": _copy_mapping(self.extensions),
            "custom_metadata": _copy_mapping(self.custom_metadata),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ReusableComponent":
        return cls(
            id=data.get("id") or make_id("cmp"),
            name=data.get("name", ""),
            component_kind=data.get("component_kind", "schema"),
            current_revision_id=data.get("current_revision_id", ""),
            payload=_copy_mapping(data.get("payload")),
            usages=_copy_list(data.get("usages")),
            extensions=_copy_mapping(data.get("extensions")),
            custom_metadata=_copy_mapping(data.get("custom_metadata")),
        )


@dataclass
class SharedComponentLibrary:
    id: str = field(default_factory=lambda: make_id("lib"))
    name: str = ""
    components: List[ReusableComponent] = field(default_factory=list)
    extensions: Dict[str, Any] = field(default_factory=dict)
    custom_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "components": [component.to_dict() for component in self.components],
            "extensions": _copy_mapping(self.extensions),
            "custom_metadata": _copy_mapping(self.custom_metadata),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SharedComponentLibrary":
        return cls(
            id=data.get("id") or make_id("lib"),
            name=data.get("name", ""),
            components=[ReusableComponent.from_dict(item) for item in data.get("components", [])],
            extensions=_copy_mapping(data.get("extensions")),
            custom_metadata=_copy_mapping(data.get("custom_metadata")),
        )


@dataclass
class ApiModel:
    schema_version: str = API_SCHEMA_VERSION
    id: str = field(default_factory=lambda: make_id("api"))
    name: str = "New API"
    display_label: str = "New API"
    version: str = "0.1.0"
    openapi_version: str = "3.1.0"
    json_schema_dialect: str = ""
    info: Dict[str, Any] = field(default_factory=dict)
    servers: List[Dict[str, Any]] = field(default_factory=list)
    security: List[Dict[str, Any]] = field(default_factory=list)
    tags: List[Dict[str, Any]] = field(default_factory=list)
    path_items: List[PathItemModel] = field(default_factory=list)
    webhooks: List[PathItemModel] = field(default_factory=list)
    local_components: Dict[str, Any] = field(default_factory=dict)
    shared_component_refs: List[Dict[str, Any]] = field(default_factory=list)
    external_docs: Dict[str, Any] = field(default_factory=dict)
    extensions: Dict[str, Any] = field(default_factory=dict)
    custom_metadata: Dict[str, Any] = field(default_factory=dict)
    extra_fields: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "id": self.id,
            "name": self.name,
            "display_label": self.display_label,
            "version": self.version,
            "openapi_version": self.openapi_version,
            "json_schema_dialect": self.json_schema_dialect,
            "info": _copy_mapping(self.info),
            "servers": _copy_list(self.servers),
            "security": _copy_list(self.security),
            "tags": _copy_list(self.tags),
            "path_items": [path_item.to_dict() for path_item in self.path_items],
            "webhooks": [path_item.to_dict() for path_item in self.webhooks],
            "local_components": _copy_mapping(self.local_components),
            "shared_component_refs": _copy_list(self.shared_component_refs),
            "external_docs": _copy_mapping(self.external_docs),
            "extensions": _copy_mapping(self.extensions),
            "custom_metadata": _copy_mapping(self.custom_metadata),
            "extra_fields": _copy_mapping(self.extra_fields),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ApiModel":
        if "path_items" in data:
            path_items = [PathItemModel.from_dict(item) for item in data.get("path_items", [])]
        else:
            # Backward-compatible load for the milestone-1 root_surface shape.
            root_surface = data.get("root_surface", {})
            path_items = [
                PathItemModel.from_dict(item) for item in root_surface.get("path_items", [])
            ]
        return cls(
            schema_version=data.get("schema_version", API_SCHEMA_VERSION),
            id=data.get("id") or make_id("api"),
            name=data.get("name", "New API"),
            display_label=data.get("display_label") or data.get("name", "New API"),
            version=data.get("version", "0.1.0"),
            openapi_version=data.get("openapi_version", data.get("openapi", "3.1.0")),
            json_schema_dialect=data.get("json_schema_dialect", ""),
            info=_copy_mapping(data.get("info")),
            servers=_copy_list(data.get("servers")),
            security=_copy_list(data.get("security")),
            tags=_copy_list(data.get("tags")),
            path_items=path_items,
            webhooks=[PathItemModel.from_dict(item) for item in data.get("webhooks", [])],
            local_components=_copy_mapping(data.get("local_components")),
            shared_component_refs=_copy_list(data.get("shared_component_refs")),
            external_docs=_copy_mapping(data.get("external_docs")),
            extensions=_copy_mapping(data.get("extensions")),
            custom_metadata=_copy_mapping(data.get("custom_metadata")),
            extra_fields=_copy_mapping(data.get("extra_fields")),
        )

    def to_oas_dict(self) -> Dict[str, Any]:
        data = _copy_mapping(self.extra_fields)
        data["openapi"] = self.openapi_version or "3.1.0"
        data["info"] = _copy_mapping(self.info)
        if self.json_schema_dialect:
            data["jsonSchemaDialect"] = self.json_schema_dialect
        if self.servers:
            data["servers"] = _copy_list(self.servers)
        if self.security:
            data["security"] = _copy_list(self.security)
        if self.tags:
            data["tags"] = _copy_list(self.tags)
        if self.external_docs:
            data["externalDocs"] = _copy_mapping(self.external_docs)
        data["paths"] = {
            path_item.path: path_item.to_oas_path_item()
            for path_item in self.path_items
        }
        if self.webhooks:
            data["webhooks"] = {
                path_item.path: path_item.to_oas_path_item()
                for path_item in self.webhooks
            }
        if self.local_components:
            data["components"] = _copy_mapping(self.local_components)
        data.update(_copy_mapping(self.extensions))
        return data


@dataclass
class ReleaseSnapshot:
    id: str = field(default_factory=lambda: make_id("snap"))
    release_id: str = ""
    api_id: str = ""
    label: str = ""
    payload_ref: str = ""
    extensions: Dict[str, Any] = field(default_factory=dict)
    custom_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "release_id": self.release_id,
            "api_id": self.api_id,
            "label": self.label,
            "payload_ref": self.payload_ref,
            "extensions": _copy_mapping(self.extensions),
            "custom_metadata": _copy_mapping(self.custom_metadata),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ReleaseSnapshot":
        return cls(
            id=data.get("id") or make_id("snap"),
            release_id=data.get("release_id", ""),
            api_id=data.get("api_id", ""),
            label=data.get("label", ""),
            payload_ref=data.get("payload_ref", ""),
            extensions=_copy_mapping(data.get("extensions")),
            custom_metadata=_copy_mapping(data.get("custom_metadata")),
        )


@dataclass
class DesignWorkspace:
    schema_version: str = WORKSPACE_SCHEMA_VERSION
    id: str = field(default_factory=lambda: make_id("ws"))
    name: str = "Untitled Workspace"
    description: str = ""
    apis: List[ApiModel] = field(default_factory=list)
    shared_libraries: List[SharedComponentLibrary] = field(default_factory=list)
    metadata_catalog: List[MetadataDefinition] = field(default_factory=list)
    release_catalog: List[ReleaseDefinition] = field(default_factory=list)
    changes: List[Change] = field(default_factory=list)
    release_snapshots: List[ReleaseSnapshot] = field(default_factory=list)
    settings: Dict[str, Any] = field(default_factory=dict)
    extensions: Dict[str, Any] = field(default_factory=dict)
    custom_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_manifest_dict(self) -> Dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "apis": [
                {
                    "id": api.id,
                    "name": api.name,
                    "display_label": api.display_label,
                    "file": f"apis/{api.id}.yaml",
                }
                for api in self.apis
            ],
            "libraries": [
                {
                    "id": library.id,
                    "name": library.name,
                    "file": f"libraries/{library.id}.yaml",
                }
                for library in self.shared_libraries
            ],
            "metadata_catalog_file": "metadata/catalog.yaml",
            "release_catalog": [release.to_dict() for release in self.release_catalog],
            "changes": [change.to_dict() for change in self.changes],
            "release_snapshots": [snapshot.to_dict() for snapshot in self.release_snapshots],
            "settings": _copy_mapping(self.settings),
            "extensions": _copy_mapping(self.extensions),
            "custom_metadata": _copy_mapping(self.custom_metadata),
        }

    def to_dict(self) -> Dict[str, Any]:
        data = self.to_manifest_dict()
        data["apis"] = [api.to_dict() for api in self.apis]
        data["libraries"] = [library.to_dict() for library in self.shared_libraries]
        data["metadata_catalog"] = [item.to_dict() for item in self.metadata_catalog]
        data.pop("metadata_catalog_file", None)
        return data

    @classmethod
    def from_manifest_dict(
        cls,
        data: Dict[str, Any],
        apis: Optional[List[ApiModel]] = None,
        shared_libraries: Optional[List[SharedComponentLibrary]] = None,
        metadata_catalog: Optional[List[MetadataDefinition]] = None,
    ) -> "DesignWorkspace":
        return cls(
            schema_version=data.get("schema_version", WORKSPACE_SCHEMA_VERSION),
            id=data.get("id") or make_id("ws"),
            name=data.get("name", "Untitled Workspace"),
            description=data.get("description", ""),
            apis=apis or [],
            shared_libraries=shared_libraries or [],
            metadata_catalog=metadata_catalog or [],
            release_catalog=[ReleaseDefinition.from_dict(item) for item in data.get("release_catalog", [])],
            changes=[Change.from_dict(item) for item in data.get("changes", [])],
            release_snapshots=[ReleaseSnapshot.from_dict(item) for item in data.get("release_snapshots", [])],
            settings=_copy_mapping(data.get("settings")),
            extensions=_copy_mapping(data.get("extensions")),
            custom_metadata=_copy_mapping(data.get("custom_metadata")),
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DesignWorkspace":
        return cls.from_manifest_dict(
            data,
            apis=[ApiModel.from_dict(item) for item in data.get("apis", [])],
            shared_libraries=[
                SharedComponentLibrary.from_dict(item) for item in data.get("libraries", [])
            ],
            metadata_catalog=[
                MetadataDefinition.from_dict(item) for item in data.get("metadata_catalog", [])
            ],
        )

    def validate(self) -> None:
        if not self.id:
            raise ValueError("Workspace id is required.")
        if not self.name:
            raise ValueError("Workspace name is required.")
        api_ids = [api.id for api in self.apis]
        if len(api_ids) != len(set(api_ids)):
            raise ValueError("API ids must be unique inside a workspace.")


def create_empty_workspace(name: str = "Untitled Workspace") -> DesignWorkspace:
    api = ApiModel(name="New API", display_label="New API")
    api.info = {"title": "New API", "version": api.version}
    return DesignWorkspace(
        name=name or "Untitled Workspace",
        apis=[api],
        settings={
            "projection_defaults": {
                "oas_versions": ["3.0", "3.1"],
                "source": "api_model",
            }
        },
    )
