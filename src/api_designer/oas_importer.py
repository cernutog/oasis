"""Import OpenAPI documents into the API Designer model."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, Tuple

import yaml

from .models import ApiModel, DesignWorkspace, OperationModel, PathItemModel, make_id


HTTP_METHODS = {"get", "put", "post", "delete", "options", "head", "patch", "trace"}


class OasImportError(RuntimeError):
    """Raised when an OpenAPI document cannot be imported into the Designer model."""


def import_oas_file_to_workspace(path: str | Path) -> DesignWorkspace:
    source_path = Path(path)
    try:
        with source_path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
    except (OSError, yaml.YAMLError) as exc:
        raise OasImportError(f"Cannot read OAS file {source_path}: {exc}") from exc

    if not isinstance(data, dict):
        raise OasImportError("OpenAPI document must be a YAML mapping at the top level.")

    api = import_oas_dict_to_api_model(data, source_name=source_path.stem)
    workspace_name = f"{api.display_label or api.name} Workspace"
    workspace = DesignWorkspace(
        name=workspace_name,
        description=f"Imported from {source_path}",
        apis=[api],
        settings={
            "projection_defaults": {
                "oas_versions": [api.openapi_version],
                "source": "api_model",
            },
            "import": {
                "source_type": "oas",
                "source_file": str(source_path),
            },
        },
    )
    return workspace


def import_oas_dict_to_api_model(data: Dict[str, Any], source_name: str = "Imported API") -> ApiModel:
    openapi_version = str(data.get("openapi", "3.1.0"))
    info = _mapping(data.get("info"))
    title = str(info.get("title") or source_name or "Imported API")
    version = str(info.get("version") or "0.1.0")

    path_items = [
        _import_path_item(path_key, item)
        for path_key, item in (data.get("paths") or {}).items()
    ]
    webhook_items = [
        _import_path_item(path_key, item)
        for path_key, item in (data.get("webhooks") or {}).items()
    ]

    api = ApiModel(
        id=_make_api_id(title),
        name=title,
        display_label=title,
        version=version,
        openapi_version=openapi_version,
        json_schema_dialect=str(data.get("jsonSchemaDialect", "") or ""),
        info=info,
        servers=_list(data.get("servers")),
        security=_list(data.get("security")),
        tags=_list(data.get("tags")),
        path_items=path_items,
        webhooks=webhook_items,
        local_components=_mapping(data.get("components")),
        external_docs=_mapping(data.get("externalDocs")),
        extensions=_extract_extensions(data),
        extra_fields=_extract_remaining(
            data,
            {
                "openapi",
                "info",
                "jsonSchemaDialect",
                "servers",
                "security",
                "tags",
                "paths",
                "webhooks",
                "components",
                "externalDocs",
            },
        ),
    )
    return api


def _import_path_item(path_key: str, item: Any) -> PathItemModel:
    payload = _mapping(item)
    operations = []
    for method, operation_data in payload.items():
        if method.lower() not in HTTP_METHODS:
            continue
        operations.append(_import_operation(path_key, method, operation_data))

    return PathItemModel(
        id=_make_path_id(path_key),
        path=path_key,
        summary=str(payload.get("summary", "") or ""),
        description=str(payload.get("description", "") or ""),
        ref=str(payload.get("$ref", "") or ""),
        parameters=_list(payload.get("parameters")),
        servers=_list(payload.get("servers")),
        operations=operations,
        extensions=_extract_extensions(payload),
        extra_fields=_extract_remaining(
            payload,
            {"$ref", "summary", "description", "parameters", "servers", *HTTP_METHODS},
        ),
    )


def _import_operation(path_key: str, method: str, operation_data: Any) -> OperationModel:
    payload = _mapping(operation_data)
    callbacks = []
    for callback_key, callback_item in _mapping(payload.get("callbacks")).items():
        callbacks.append(_import_path_item(callback_key, callback_item))

    return OperationModel(
        id=_make_operation_id(method, path_key, payload.get("operationId")),
        method=method.lower(),
        path=path_key,
        operation_id=str(payload.get("operationId", "") or ""),
        summary=str(payload.get("summary", "") or ""),
        description=str(payload.get("description", "") or ""),
        tags=[str(tag) for tag in _list(payload.get("tags"))],
        parameters=_list(payload.get("parameters")),
        request_body=_mapping(payload.get("requestBody")),
        responses=_mapping(payload.get("responses")),
        security=_list(payload.get("security")),
        servers=_list(payload.get("servers")),
        external_docs=_mapping(payload.get("externalDocs")),
        deprecated=payload.get("deprecated"),
        callbacks=callbacks,
        extensions=_extract_extensions(payload),
        extra_fields=_extract_remaining(
            payload,
            {
                "operationId",
                "summary",
                "description",
                "tags",
                "parameters",
                "requestBody",
                "responses",
                "security",
                "servers",
                "externalDocs",
                "deprecated",
                "callbacks",
            },
        ),
    )


def _make_api_id(title: str) -> str:
    return _slug_id("api", title)


def _make_path_id(path: str) -> str:
    return _slug_id("path", path)


def _make_operation_id(method: str, path: str, operation_id: Any) -> str:
    if operation_id:
        return _slug_id("op", str(operation_id))
    return _slug_id("op", f"{method}_{path}")


def _slug_id(prefix: str, value: str) -> str:
    cleaned = "".join(ch.lower() if ch.isalnum() else "_" for ch in value).strip("_")
    cleaned = "_".join(part for part in cleaned.split("_") if part)
    return f"{prefix}_{cleaned[:48]}" if cleaned else make_id(prefix)


def _mapping(value: Any) -> Dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _extract_extensions(data: Dict[str, Any]) -> Dict[str, Any]:
    return {key: value for key, value in data.items() if str(key).startswith("x-")}


def _extract_remaining(data: Dict[str, Any], known_keys: Iterable[str]) -> Dict[str, Any]:
    known = set(known_keys)
    return {
        key: value
        for key, value in data.items()
        if key not in known and not str(key).startswith("x-")
    }
