"""File-based persistence for the API Designer model package."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import yaml

from .models import (
    METADATA_CATALOG_SCHEMA_VERSION,
    ApiModel,
    DesignWorkspace,
    MetadataDefinition,
    SharedComponentLibrary,
)


class DesignerPersistenceError(RuntimeError):
    """Raised when a Designer workspace package cannot be loaded or saved."""


class DesignerDumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


class FileSystemDesignerRepository:
    """Repository implementation backed by a versionable folder package."""

    def __init__(self, root_path: str | Path):
        self.root_path = Path(root_path)

    @property
    def workspace_file(self) -> Path:
        return self.root_path / "workspace.yaml"

    def save_workspace(self, workspace: DesignWorkspace) -> None:
        try:
            workspace.validate()
            self._ensure_package_dirs()
            self._write_yaml(self.workspace_file, workspace.to_manifest_dict())
            for api in sorted(workspace.apis, key=lambda item: item.id):
                self._write_yaml(self.root_path / "apis" / f"{api.id}.yaml", api.to_dict())
            for library in sorted(workspace.shared_libraries, key=lambda item: item.id):
                self._write_yaml(
                    self.root_path / "libraries" / f"{library.id}.yaml",
                    library.to_dict(),
                )
            self._write_metadata_catalog(workspace.metadata_catalog)
        except OSError as exc:
            raise DesignerPersistenceError(f"Cannot save workspace: {exc}") from exc

    def load_workspace(self) -> DesignWorkspace:
        if not self.workspace_file.exists():
            raise DesignerPersistenceError(f"workspace.yaml not found in {self.root_path}")

        manifest = self._read_yaml(self.workspace_file)
        apis = self._load_apis(manifest)
        libraries = self._load_libraries(manifest)
        metadata_catalog = self._load_metadata_catalog(manifest)
        return DesignWorkspace.from_manifest_dict(
            manifest,
            apis=apis,
            shared_libraries=libraries,
            metadata_catalog=metadata_catalog,
        )

    def _ensure_package_dirs(self) -> None:
        self.root_path.mkdir(parents=True, exist_ok=True)
        (self.root_path / "apis").mkdir(exist_ok=True)
        (self.root_path / "libraries").mkdir(exist_ok=True)
        (self.root_path / "metadata").mkdir(exist_ok=True)
        (self.root_path / "revisions").mkdir(exist_ok=True)

    def _write_metadata_catalog(self, definitions: List[MetadataDefinition]) -> None:
        data = {
            "schema_version": METADATA_CATALOG_SCHEMA_VERSION,
            "definitions": [definition.to_dict() for definition in definitions],
        }
        self._write_yaml(self.root_path / "metadata" / "catalog.yaml", data)

    def _load_apis(self, manifest: Dict[str, Any]) -> List[ApiModel]:
        apis = []
        for entry in manifest.get("apis", []):
            rel_file = entry.get("file") or f"apis/{entry.get('id')}.yaml"
            path = self._resolve_package_file(rel_file)
            if not path.exists():
                raise DesignerPersistenceError(f"API model file not found: {rel_file}")
            apis.append(ApiModel.from_dict(self._read_yaml(path)))
        return apis

    def _load_libraries(self, manifest: Dict[str, Any]) -> List[SharedComponentLibrary]:
        libraries = []
        for entry in manifest.get("libraries", []):
            rel_file = entry.get("file") or f"libraries/{entry.get('id')}.yaml"
            path = self._resolve_package_file(rel_file)
            if path.exists():
                libraries.append(SharedComponentLibrary.from_dict(self._read_yaml(path)))
        return libraries

    def _load_metadata_catalog(self, manifest: Dict[str, Any]) -> List[MetadataDefinition]:
        rel_file = manifest.get("metadata_catalog_file", "metadata/catalog.yaml")
        path = self._resolve_package_file(rel_file)
        if not path.exists():
            return []
        data = self._read_yaml(path)
        return [MetadataDefinition.from_dict(item) for item in data.get("definitions", [])]

    def _resolve_package_file(self, relative_path: str) -> Path:
        candidate = (self.root_path / relative_path).resolve()
        root = self.root_path.resolve()
        if root not in candidate.parents and candidate != root:
            raise DesignerPersistenceError(f"Path escapes workspace package: {relative_path}")
        return candidate

    def _read_yaml(self, path: Path) -> Dict[str, Any]:
        try:
            with path.open("r", encoding="utf-8") as handle:
                data = yaml.safe_load(handle) or {}
            if not isinstance(data, dict):
                raise DesignerPersistenceError(f"YAML document must be a mapping: {path}")
            return data
        except yaml.YAMLError as exc:
            raise DesignerPersistenceError(f"Invalid YAML in {path}: {exc}") from exc
        except OSError as exc:
            raise DesignerPersistenceError(f"Cannot read {path}: {exc}") from exc

    def _write_yaml(self, path: Path, data: Dict[str, Any]) -> None:
        text = yaml.dump(
            data,
            Dumper=DesignerDumper,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
            width=100,
        )
        if not text.endswith("\n"):
            text += "\n"
        if path.exists() and path.read_text(encoding="utf-8") == text:
            return
        path.write_text(text, encoding="utf-8")
