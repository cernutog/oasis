"""Initial API Designer tab shell."""

from __future__ import annotations

import os
import json
import tkinter as tk
from copy import deepcopy
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Any, Callable, Dict, Optional, Tuple

import customtkinter as ctk
import yaml

from .models import (
    ApiModel,
    Change,
    ChangeStep,
    DesignWorkspace,
    OperationModel,
    PathItemModel,
    ReleaseDefinition,
    SharedComponentLibrary,
    create_empty_workspace,
)
from .oas_importer import OasImportError, import_oas_dict_to_api_model, import_oas_file_to_workspace
from .persistence import DesignerPersistenceError, FileSystemDesignerRepository


PETROL = "#0A809E"
PETROL_HOVER = "#076075"
HTTP_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS", "TRACE"]
PARAMETER_LOCATIONS = ["query", "header", "path", "cookie"]
OPENAPI_VERSIONS = ["3.0.0", "3.0.1", "3.1.0"]
SCHEMA_TYPES = ["", "string", "number", "integer", "boolean", "array", "object"]
SCHEMA_MODE_OPTIONS = ["Simple", "Reference", "All Of", "Any Of", "One Of"]
STRING_FORMAT_OPTIONS = ["", "date", "date-time", "time", "duration", "email", "idn-email", "hostname", "idn-hostname", "ipv4", "ipv6", "uri", "uri-reference", "uuid", "byte", "binary", "password"]
PARAMETER_STYLE_OPTIONS = ["", "form", "simple", "matrix", "label", "spaceDelimited", "pipeDelimited", "deepObject"]

SECTION_TEMPLATES: Dict[str, Any] = {
    "info": {
        "title": "",
        "summary": "",
        "description": "",
        "termsOfService": "",
        "version": "",
        "contact": {"name": "", "url": "", "email": ""},
        "license": {"name": "", "identifier": "", "url": ""},
    },
    "contact": {"name": "", "url": "", "email": ""},
    "license": {"name": "", "identifier": "", "url": ""},
    "external_docs": {"description": "", "url": ""},
    "server": {"url": "", "description": "", "variables": {}},
    "server_variable": {"enum": [], "default": "", "description": ""},
    "tag": {"name": "", "description": "", "externalDocs": {}},
    "operation_details": {
        "summary": "",
        "description": "",
        "tags": [],
        "security": [],
        "servers": [],
        "externalDocs": {},
        "deprecated": False,
    },
    "path_details": {
        "summary": "",
        "description": "",
        "servers": [],
        "parameters": [],
    },
    "parameter": {
        "name": "",
        "in": "query",
        "description": "",
        "required": False,
        "deprecated": False,
        "allowEmptyValue": False,
        "style": "",
        "explode": False,
        "allowReserved": False,
        "schema": {"type": "string"},
        "example": "",
        "examples": {},
        "content": {},
    },
    "request_body": {"description": "", "required": False, "content": {}},
    "response": {"description": "", "headers": {}, "content": {}, "links": {}},
    "path_item": {"summary": "", "description": "", "parameters": [], "servers": []},
    "media_type": {"schema": {}, "example": "", "examples": {}, "encoding": {}},
    "header": {
        "description": "",
        "required": False,
        "deprecated": False,
        "style": "",
        "explode": False,
        "schema": {},
        "example": "",
        "examples": {},
        "content": {},
    },
    "encoding": {"contentType": "", "headers": {}, "style": "", "explode": False, "allowReserved": False},
    "example": {"summary": "", "description": "", "value": "", "externalValue": ""},
    "link": {"operationRef": "", "operationId": "", "parameters": {}, "requestBody": "", "description": "", "server": {}},
    "schema": {
        "__schema_mode__": "Simple",
        "title": "",
        "type": "",
        "format": "",
        "minLength": "",
        "maxLength": "",
        "pattern": "",
        "minItems": "",
        "maxItems": "",
        "description": "",
        "default": "",
        "enum": [],
        "properties": {},
        "items": {},
        "required": [],
        "allOf": [],
        "anyOf": [],
        "oneOf": [],
    },
}
MAP_SECTION_KEYS = {
    "callbacks",
    "components",
    "content",
    "encoding",
    "examples",
    "headers",
    "links",
    "paths",
    "patternProperties",
    "properties",
    "responses",
    "schemas",
    "securitySchemes",
    "variables",
    "webhooks",
}


class ModelTreeWidget(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#FFFFFF", highlightthickness=0, bd=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.canvas = tk.Canvas(self, bg="#FFFFFF", highlightthickness=0, bd=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self._bindings: Dict[str, list[Callable[..., None]]] = {}
        self._nodes: Dict[str, Dict[str, Any]] = {}
        self._roots: list[str] = []
        self._selection: str = ""
        self._focus: str = ""
        self._counter = 0
        self._tag_styles: Dict[str, Dict[str, Any]] = {}
        self._row_height = 20
        self._indent = 18
        self._left_pad = 8
        self._indicator_size = 10
        self._label_gap = 8
        self._visible_nodes: list[str] = []
        self._row_map: Dict[str, int] = {}
        self._guide_labels: Dict[int, str] = {}
        self._indicator_hits: Dict[str, tuple[int, int, int, int]] = {}
        self._virtual_height = 0
        self._current_guide_label: Optional[str] = None
        self._batch_depth = 0
        self._pending_redraw = False

        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.bind("<Button-1>", self._on_left_click)
        self.canvas.bind("<Double-1>", self._on_double_click)
        self.canvas.bind("<Button-3>", self._on_right_click)
        self.canvas.bind("<Motion>", self._on_motion)
        self.canvas.bind("<Leave>", self._on_leave)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)

    def bind(self, sequence=None, func=None, add=None):
        self._bindings.setdefault(sequence, []).append(func)
        return func

    def tag_configure(self, tagname, **kw):
        self._tag_styles[tagname] = kw

    def delete(self, *node_ids):
        if not node_ids:
            return
        if set(node_ids) == set(self._roots):
            self._nodes.clear()
            self._roots.clear()
            self._visible_nodes = []
            self._row_map = {}
            self._guide_labels = {}
            self._indicator_hits = {}
            self._selection = ""
            self._focus = ""
            self._current_guide_label = None
            self._virtual_height = 0
            self._request_redraw()
            return
        for node_id in node_ids:
            self._delete_node(node_id)
        self._request_redraw()

    def _delete_node(self, node_id: str) -> None:
        node = self._nodes.get(node_id)
        if not node:
            return
        parent = node["parent"]
        siblings = None
        if parent:
            parent_node = self._nodes.get(parent)
            siblings = parent_node["children"] if parent_node else None
        else:
            siblings = self._roots
        for child in list(node["children"]):
            self._delete_node(child)
        if siblings is not None and node_id in siblings:
            siblings.remove(node_id)
        if self._selection == node_id:
            self._selection = ""
        if self._focus == node_id:
            self._focus = ""
        self._nodes.pop(node_id, None)

    def get_children(self, node_id: str = ""):
        if not node_id:
            return tuple(self._roots)
        node = self._nodes.get(node_id)
        return tuple(node["children"]) if node else ()

    def insert(self, parent, index, text="", open=True, tags=()):
        self._counter += 1
        node_id = f"model-node-{self._counter}"
        self._nodes[node_id] = {
            "id": node_id,
            "parent": parent or "",
            "children": [],
            "text": text,
            "open": bool(open),
            "tags": tuple(tags),
        }
        siblings = self._roots if not parent else self._nodes[parent]["children"]
        siblings.append(node_id)
        self._request_redraw()
        return node_id

    def item(self, node_id: str, option: Optional[str] = None, **kwargs):
        node = self._nodes[node_id]
        old_open = node["open"]
        if kwargs:
            if "text" in kwargs:
                node["text"] = kwargs["text"]
            if "open" in kwargs:
                node["open"] = bool(kwargs["open"])
            if "tags" in kwargs:
                node["tags"] = tuple(kwargs["tags"])
            self._request_redraw()
            if "open" in kwargs and old_open != node["open"] and self._batch_depth == 0:
                self._emit("<<TreeviewOpen>>" if node["open"] else "<<TreeviewClose>>", None)
            return None
        if option is None:
            return dict(node)
        return node.get(option)

    def selection(self):
        return (self._selection,) if self._selection else ()

    def selection_set(self, node_id: str):
        self._selection = node_id
        self._focus = node_id
        self._request_redraw()

    def selection_remove(self, node_ids):
        ids = set(node_ids if isinstance(node_ids, (list, tuple)) else [node_ids])
        if self._selection in ids:
            self._selection = ""
        self._request_redraw()

    def focus(self, node_id: Optional[str] = None):
        if node_id is None:
            return self._focus
        self._focus = node_id

    def see(self, node_id: str):
        if node_id not in self._row_map:
            return
        row_index = self._row_map[node_id]
        top = row_index * self._row_height
        bottom = top + self._row_height
        height = max(self.canvas.winfo_height(), 1)
        total = max(self._virtual_height, 1)
        start = self.canvas.canvasy(0)
        end = start + height
        if top < start:
            self.canvas.yview_moveto(max(0.0, top / total))
        elif bottom > end:
            self.canvas.yview_moveto(max(0.0, (bottom - height) / total))

    def bbox(self, node_id: str):
        if node_id not in self._row_map:
            return ()
        row_index = self._row_map[node_id]
        return (0, row_index * self._row_height, max(self.canvas.winfo_width(), 1), self._row_height)

    def identify_row(self, y: int):
        canvas_y = self.canvas.canvasy(y)
        row_index = int(canvas_y // self._row_height)
        if 0 <= row_index < len(self._visible_nodes):
            return self._visible_nodes[row_index]
        return ""

    def yview(self, *args):
        self.canvas.yview(*args)

    def begin_update(self):
        self._batch_depth += 1

    def end_update(self):
        if self._batch_depth > 0:
            self._batch_depth -= 1
        if self._batch_depth == 0 and self._pending_redraw:
            self.redraw()

    def _request_redraw(self):
        if self._batch_depth > 0:
            self._pending_redraw = True
            return
        self.redraw()

    def redraw(self):
        if self._batch_depth > 0:
            self._pending_redraw = True
            return
        self._pending_redraw = False
        yview = self.canvas.yview()
        self.canvas.delete("all")
        self._visible_nodes = []
        self._row_map = {}
        self._guide_labels = {}
        self._indicator_hits = {}
        self._build_visible_nodes()
        self._virtual_height = len(self._visible_nodes) * self._row_height + 4
        self.canvas.configure(scrollregion=(0, 0, max(self.canvas.winfo_width(), 1), self._virtual_height))
        if yview:
            canvas_height = max(self.canvas.winfo_height(), 1)
            visible_fraction = min(1.0, canvas_height / max(self._virtual_height, 1))
            max_first = max(0.0, 1.0 - visible_fraction)
            first = min(yview[0], max_first)
            self.canvas.yview_moveto(first)
        self._draw_guides()
        self._draw_rows()

    def _build_visible_nodes(self):
        def visit(node_id: str):
            node = self._nodes.get(node_id)
            if not node:
                return
            self._row_map[node_id] = len(self._visible_nodes)
            self._visible_nodes.append(node_id)
            if node["open"]:
                for child in node["children"]:
                    visit(child)

        for root in self._roots:
            visit(root)

    def _draw_guides(self):
        for segment in self._build_guide_segments():
            item_id = self.canvas.create_line(
                segment["x1"],
                segment["y1"],
                segment["x2"],
                segment["y2"],
                fill=segment["fill"],
                width=1,
            )
            self._guide_labels[item_id] = segment["label"]

    def _build_guide_segments(self) -> list[dict[str, Any]]:
        segments: list[dict[str, Any]] = []
        for node_id, node in list(self._nodes.items()):
            if not node["children"] or not node["open"]:
                continue
            visible_children = [child for child in node["children"] if child in self._row_map]
            if not visible_children:
                continue
            first_child = visible_children[0]
            last_descendant = self._last_visible_descendant(node_id)
            x = self._guide_x(self._depth(node_id))
            segments.append(
                {
                    "kind": "vertical",
                    "node_id": node_id,
                    "label": node["text"],
                    "x1": x,
                    "y1": self._row_center(first_child),
                    "x2": x,
                    "y2": self._row_center(last_descendant),
                    "fill": "#CBD4DA",
                }
            )

        for node_id in self._visible_nodes:
            node = self._nodes.get(node_id)
            if not node:
                continue
            parent = node["parent"]
            if not parent:
                continue
            parent_node = self._nodes.get(parent)
            if not parent_node:
                continue
            y = self._row_center(node_id)
            segments.append(
                {
                    "kind": "branch",
                    "node_id": node_id,
                    "label": parent_node["text"],
                    "x1": self._guide_x(self._depth(parent)),
                    "y1": y,
                    "x2": self._label_x(node_id) - 6,
                    "y2": y,
                    "fill": "#D7DEE3",
                }
            )
        return segments

    def _guide_label_at_point(self, canvas_x: float, canvas_y: float, tolerance: int = 3) -> Optional[str]:
        for segment in reversed(self._build_guide_segments()):
            x1 = float(segment["x1"])
            y1 = float(segment["y1"])
            x2 = float(segment["x2"])
            y2 = float(segment["y2"])
            if x1 == x2:
                if abs(canvas_x - x1) <= tolerance and min(y1, y2) <= canvas_y <= max(y1, y2):
                    return str(segment["label"])
                continue
            if y1 == y2:
                if abs(canvas_y - y1) <= tolerance and min(x1, x2) <= canvas_x <= max(x1, x2):
                    return str(segment["label"])
        return None

    def _draw_rows(self):
        width = max(self.canvas.winfo_width(), 200)
        for node_id in self._visible_nodes:
            row_index = self._row_map[node_id]
            y = row_index * self._row_height
            if node_id == self._selection:
                self.canvas.create_rectangle(0, y, width, y + self._row_height, fill="#127AB5", outline="")
            node = self._nodes[node_id]
            depth = self._depth(node_id)
            label_x = self._label_x(node_id)
            if node["children"]:
                box_x = self._left_pad + depth * self._indent
                box_y = y + (self._row_height - self._indicator_size) / 2
                box = self.canvas.create_rectangle(
                    box_x,
                    box_y,
                    box_x + self._indicator_size,
                    box_y + self._indicator_size,
                    outline="#7E8B94",
                    fill="#FFFFFF",
                    width=1,
                )
                symbol = "-" if node["open"] else "+"
                self.canvas.create_text(
                    box_x + self._indicator_size / 2,
                    y + self._row_height / 2,
                    text=symbol,
                    fill="#4A5963",
                    font=("Segoe UI", 8),
                )
                self._indicator_hits[node_id] = (
                    int(box_x),
                    int(box_y),
                    int(box_x + self._indicator_size),
                    int(box_y + self._indicator_size),
                )
            text_color = self._text_color(node)
            if node_id == self._selection:
                text_color = "#FFFFFF"
            self.canvas.create_text(
                label_x,
                y + self._row_height / 2,
                text=node["text"],
                anchor="w",
                fill=text_color,
                font=("Segoe UI", 10),
            )

    def _text_color(self, node: Dict[str, Any]) -> str:
        for tag in node.get("tags", ()):
            style = self._tag_styles.get(tag)
            if style and style.get("foreground"):
                return str(style["foreground"])
        return "#111111"

    def _depth(self, node_id: str) -> int:
        depth = 0
        node = self._nodes.get(node_id)
        if not node:
            return depth
        current = node["parent"]
        while current:
            depth += 1
            current_node = self._nodes.get(current)
            if not current_node:
                break
            current = current_node["parent"]
        return depth

    def _guide_x(self, depth: int) -> int:
        return self._left_pad + depth * self._indent + self._indicator_size / 2

    def _label_x(self, node_id: str) -> int:
        return self._left_pad + self._depth(node_id) * self._indent + self._indicator_size + self._label_gap

    def _row_center(self, node_id: str) -> float:
        return self._row_map.get(node_id, 0) * self._row_height + self._row_height / 2

    def _last_visible_descendant(self, node_id: str) -> str:
        node = self._nodes.get(node_id)
        if not node:
            return node_id
        visible_children = [child for child in node["children"] if child in self._row_map]
        if not node["open"] or not visible_children:
            return node_id
        return self._last_visible_descendant(visible_children[-1])

    def _emit(self, sequence: str, event) -> None:
        for callback in self._bindings.get(sequence, []):
            callback(event)

    def _toggle_node(self, node_id: str) -> None:
        node = self._nodes.get(node_id)
        if not node or not node["children"]:
            return
        node["open"] = not node["open"]
        self._request_redraw()
        self._emit("<<TreeviewOpen>>" if node["open"] else "<<TreeviewClose>>", None)

    def _on_canvas_configure(self, event) -> None:
        self.redraw()
        self._emit("<Configure>", event)

    def _on_left_click(self, event) -> None:
        node_id = self.identify_row(event.y)
        if not node_id or node_id not in self._nodes:
            return
        hit = self._indicator_hits.get(node_id)
        canvas_x = int(self.canvas.canvasx(event.x))
        canvas_y = int(self.canvas.canvasy(event.y))
        if hit and hit[0] <= canvas_x <= hit[2] and hit[1] <= canvas_y <= hit[3]:
            self._toggle_node(node_id)
            return
        self._selection = node_id
        self._focus = node_id
        self.redraw()
        self._emit("<<TreeviewSelect>>", None)

    def _on_double_click(self, event) -> None:
        node_id = self.identify_row(event.y)
        if node_id and node_id in self._nodes and self._nodes[node_id]["children"]:
            self._toggle_node(node_id)

    def _on_right_click(self, event) -> None:
        node_id = self.identify_row(event.y)
        if node_id and node_id in self._nodes:
            self._selection = node_id
            self._focus = node_id
            self.redraw()
        self._emit("<Button-3>", event)

    def _on_motion(self, event) -> None:
        if self._batch_depth > 0 or not self._nodes:
            self._current_guide_label = None
            self._emit("<Leave>", None)
            return
        canvas_x = float(self.canvas.canvasx(event.x))
        canvas_y = float(self.canvas.canvasy(event.y))
        self._current_guide_label = self._guide_label_at_point(canvas_x, canvas_y)
        if self._current_guide_label is None:
            self._emit("<Leave>", None)
            return
        self._emit("<Motion>", event)

    def _on_leave(self, event) -> None:
        self._current_guide_label = None
        self._emit("<Leave>", event)

    def _on_mousewheel(self, event) -> None:
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

class ApiDesignerTab:
    """Three-area shell for the API Designer milestone."""

    def __init__(self, master, prefs_manager, status_callback=None):
        self.master = master
        self.prefs_manager = prefs_manager
        self.status_callback = status_callback
        self.workspace: DesignWorkspace = create_empty_workspace("Untitled Workspace")
        self.workspace_path: Optional[Path] = None
        self.selected_ref: Optional[Tuple[str, Any]] = None
        self.selected_source: str = "explorer"
        self._workspace_node_index: Dict[str, Tuple[str, Any]] = {}
        self._model_node_index: Dict[str, Tuple[str, Any]] = {}
        self._model_visual_index: Dict[str, Dict[str, Any]] = {}
        self._section_expansion_state: Dict[tuple[Any, ...], bool] = {}
        self._model_tooltip_window = None
        self._model_tooltip_label = None
        self._dirty = False

        self._build_ui()
        self._load_last_workspace_or_default()

    def _build_ui(self) -> None:
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)

        self.toolbar = ctk.CTkFrame(self.master, fg_color="transparent")
        self.toolbar.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.toolbar.grid_columnconfigure(5, weight=1)

        self.btn_new = ctk.CTkButton(
            self.toolbar, text="New", width=80, command=self.new_workspace
        )
        self.btn_new.grid(row=0, column=0, padx=(0, 8))

        self.btn_open = ctk.CTkButton(
            self.toolbar, text="Open", width=80, command=self.open_workspace
        )
        self.btn_open.grid(row=0, column=1, padx=(0, 8))

        self.btn_import_oas = ctk.CTkButton(
            self.toolbar, text="Import OAS", width=110, command=self.import_oas
        )
        self.btn_import_oas.grid(row=0, column=2, padx=(0, 8))

        self.btn_save = ctk.CTkButton(
            self.toolbar, text="Save", width=80, command=self.save_workspace
        )
        self.btn_save.grid(row=0, column=3, padx=(0, 8))

        self.btn_save_as = ctk.CTkButton(
            self.toolbar, text="Save As", width=90, command=self.save_workspace_as
        )
        self.btn_save_as.grid(row=0, column=4, padx=(0, 12))

        self.lbl_path = ctk.CTkLabel(
            self.toolbar, text="Workspace:", font=ctk.CTkFont(weight="bold")
        )
        self.lbl_path.grid(row=0, column=5, padx=(0, 8), sticky="w")

        self.var_path = tk.StringVar(value="Not saved")
        self.entry_path = ctk.CTkEntry(self.toolbar, textvariable=self.var_path)
        self.entry_path.grid(row=0, column=6, sticky="ew")
        self.entry_path.configure(state="disabled")

        self.status_label = ctk.CTkLabel(self.toolbar, text="", width=140, anchor="e")
        self.status_label.grid(row=0, column=7, padx=(10, 0), sticky="e")

        self.main_pane = tk.PanedWindow(
            self.master,
            orient=tk.HORIZONTAL,
            sashwidth=6,
            sashrelief=tk.RAISED,
            opaqueresize=False,
            bg="#D5DEE2",
            bd=0,
        )
        self.main_pane.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        self.workspace_frame = self._make_panel(self.main_pane, "Explorer")
        self.model_frame = self._make_panel(self.main_pane, "Model")
        self.inspector_frame = self._make_panel(self.main_pane, "Inspector")

        self.main_pane.add(self.workspace_frame, minsize=220, width=280)
        self.main_pane.add(self.model_frame, minsize=360, width=520)
        self.main_pane.add(self.inspector_frame, minsize=260, width=320)

        self.workspace_tree = self._make_tree(self.workspace_frame)
        self.workspace_tree.bind("<<TreeviewSelect>>", self._on_workspace_select)

        self.model_tree = self._make_tree(self.model_frame, with_guides=True)
        self.model_tree.bind("<<TreeviewSelect>>", self._on_model_select)
        self.model_tree.bind("<Button-3>", self._on_model_context_menu)
        self.model_tree.bind("<<TreeviewOpen>>", lambda _e: self._schedule_model_guides_redraw())
        self.model_tree.bind("<<TreeviewClose>>", lambda _e: self._schedule_model_guides_redraw())
        self.model_tree.bind("<Configure>", lambda _e: self._schedule_model_guides_redraw())
        self.model_tree.bind("<Motion>", self._on_model_guides_motion)
        self.model_tree.bind("<Leave>", self._hide_model_tooltip)
        self.model_tree.tag_configure("shared_component", foreground=PETROL)
        self.model_context_menu = tk.Menu(self.model_tree, tearoff=0)

        model_header = getattr(self.model_frame, "_header", None)
        if model_header is not None:
            ctk.CTkButton(
                model_header,
                text="Expand All",
                width=86,
                height=26,
                corner_radius=5,
                command=self._expand_all_model_nodes,
            ).pack(side="right", padx=(6, 0))
            ctk.CTkButton(
                model_header,
                text="Collapse All",
                width=92,
                height=26,
                corner_radius=5,
                command=self._collapse_all_model_nodes,
            ).pack(side="right")

        self._build_inspector()

    def _make_panel(self, parent, title: str):
        panel = ctk.CTkFrame(parent, corner_radius=6)
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(1, weight=1)
        header = ctk.CTkFrame(panel, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 4))
        ctk.CTkLabel(
            header,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=PETROL,
        ).pack(side="left")
        panel._header = header
        return panel

    def _make_tree(self, parent, with_guides: bool = False):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        if with_guides:
            tree = ModelTreeWidget(frame)
            tree.grid(row=0, column=0, sticky="nsew")
            return tree

        tree = ttk.Treeview(frame, show="tree", selectmode="browse")
        yscroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=yscroll.set)
        tree.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        return tree

    def _build_inspector(self) -> None:
        form = ctk.CTkScrollableFrame(self.inspector_frame, fg_color="transparent")
        form.grid(row=1, column=0, sticky="nsew", padx=12, pady=(4, 12))
        form.grid_columnconfigure(1, weight=1)
        form.grid_rowconfigure(1, weight=1)

        self.var_context = tk.StringVar(value="Explorer > Workspace")
        self.var_inspector_mode = tk.StringVar(value="View")
        self.var_primary = tk.StringVar(value="")
        self.var_secondary = tk.StringVar(value="")
        self.var_tertiary = tk.StringVar(value="")
        self.var_primary_label = tk.StringVar(value="Name")
        self.var_secondary_label = tk.StringVar(value="Version")
        self.var_tertiary_label = tk.StringVar(value="Path")
        self.var_description_label = tk.StringVar(value="Description")

        ctk.CTkLabel(
            form,
            textvariable=self.var_context,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=PETROL,
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))
        self.inspector_mode_switch = ctk.CTkSegmentedButton(
            form,
            values=["View", "Edit"],
            variable=self.var_inspector_mode,
            command=self._on_inspector_mode_change,
        )
        self.inspector_mode_switch.grid(row=0, column=1, sticky="e", pady=(0, 8))

        self.lbl_primary = ctk.CTkLabel(form, textvariable=self.var_primary_label)
        self.lbl_primary.grid(row=1, column=0, sticky="w", pady=(10, 4))
        self.entry_primary = ctk.CTkEntry(form, textvariable=self.var_primary)
        self.entry_primary.grid(row=1, column=1, sticky="ew", pady=(10, 4))
        self.combo_primary = ctk.CTkComboBox(form, variable=self.var_primary, values=[])
        self.combo_primary.grid(row=1, column=1, sticky="ew", pady=(10, 4))
        self.combo_primary.grid_remove()

        self.lbl_secondary = ctk.CTkLabel(form, textvariable=self.var_secondary_label)
        self.lbl_secondary.grid(row=2, column=0, sticky="w", pady=4)
        self.entry_secondary = ctk.CTkEntry(form, textvariable=self.var_secondary)
        self.entry_secondary.grid(row=2, column=1, sticky="ew", pady=4)
        self.combo_secondary = ctk.CTkComboBox(form, variable=self.var_secondary, values=[])
        self.combo_secondary.grid(row=2, column=1, sticky="ew", pady=4)
        self.combo_secondary.grid_remove()

        self.lbl_tertiary = ctk.CTkLabel(form, textvariable=self.var_tertiary_label)
        self.lbl_tertiary.grid(row=3, column=0, sticky="w", pady=4)
        self.entry_tertiary = ctk.CTkEntry(form, textvariable=self.var_tertiary)
        self.entry_tertiary.grid(row=3, column=1, sticky="ew", pady=4)
        self.combo_tertiary = ctk.CTkComboBox(form, variable=self.var_tertiary, values=[])
        self.combo_tertiary.grid(row=3, column=1, sticky="ew", pady=4)
        self.combo_tertiary.grid_remove()

        self.lbl_description = ctk.CTkLabel(form, textvariable=self.var_description_label)
        self.lbl_description.grid(row=4, column=0, sticky="nw", pady=4)
        self.entry_description = ctk.CTkTextbox(form, height=90, wrap="word")
        self.entry_description.grid(row=4, column=1, sticky="nsew", pady=4)

        self.btn_apply = ctk.CTkButton(
            form,
            text="Apply",
            width=90,
            command=self.apply_inspector_changes,
            fg_color=PETROL,
            hover_color=PETROL_HOVER,
        )
        self.btn_apply.grid(row=5, column=1, sticky="e", pady=(8, 10))

        self.dynamic_editor = ctk.CTkFrame(form, fg_color="transparent")
        self.dynamic_editor.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(8, 8))
        self.dynamic_editor.grid_columnconfigure(1, weight=1)
        self.dynamic_editor.grid_remove()
        self._dynamic_bindings: list[dict[str, Any]] = []
        self._dynamic_meta: Optional[Dict[str, Any]] = None
        self._dynamic_working_copy: Any = None

    def _load_last_workspace_or_default(self) -> None:
        last = self.prefs_manager.get("last_api_model_workspace", "")
        if last and Path(last).exists():
            try:
                self._load_workspace_from_path(Path(last))
                return
            except DesignerPersistenceError as exc:
                self._set_status(f"Open failed: {exc}")
        last_oas = self.prefs_manager.get("last_designer_oas_import_file", "")
        if last_oas and Path(last_oas).exists():
            try:
                self.workspace = import_oas_file_to_workspace(last_oas)
                self.workspace_path = None
                self._dirty = True
                self._refresh_all()
                return
            except OasImportError as exc:
                self._set_status(f"Import failed: {exc}")
        self._refresh_all()

    def new_workspace(self) -> None:
        if not self._confirm_discard_dirty():
            return
        name = self._prompt_workspace_name("New Workspace")
        if not name:
            return
        self.workspace = create_empty_workspace(name)
        self.workspace_path = None
        self._dirty = True
        self._refresh_all()
        self._set_status("New workspace")

    def open_workspace(self) -> None:
        if not self._confirm_discard_dirty():
            return
        initial = self._initial_dir()
        filename = filedialog.askopenfilename(
            parent=self.master.winfo_toplevel(),
            initialdir=initial,
            title="Open API Model Workspace",
            filetypes=[("Workspace manifest", "workspace.yaml"), ("YAML files", "*.yaml *.yml")],
        )
        if not filename:
            return
        path = Path(filename)
        if path.name.lower() != "workspace.yaml":
            messagebox.showerror(
                "Open Workspace",
                "Select the workspace.yaml file inside an API Model workspace.",
                parent=self.master.winfo_toplevel(),
            )
            return
        try:
            self._load_workspace_from_path(path.parent)
            self._set_status("Workspace opened")
        except DesignerPersistenceError as exc:
            messagebox.showerror("Open Workspace", str(exc), parent=self.master.winfo_toplevel())

    def save_workspace(self) -> None:
        if self.workspace_path is None:
            self.save_workspace_as()
            return
        try:
            FileSystemDesignerRepository(self.workspace_path).save_workspace(self.workspace)
            self._dirty = False
            self._remember_workspace_path()
            self._refresh_path()
            self._set_status("Saved")
        except DesignerPersistenceError as exc:
            messagebox.showerror("Save Workspace", str(exc), parent=self.master.winfo_toplevel())

    def save_workspace_as(self) -> None:
        initial = self._initial_dir()
        directory = filedialog.askdirectory(
            parent=self.master.winfo_toplevel(),
            initialdir=initial,
            title="Save API Model Workspace",
        )
        if not directory:
            return
        target = Path(directory)
        if target.name.lower() != self._safe_folder_name(self.workspace.name).lower():
            target = target / self._safe_folder_name(self.workspace.name)
        self.workspace_path = target
        self.save_workspace()

    def import_oas(self) -> None:
        if not self._confirm_discard_dirty():
            return
        initial = self._initial_oas_dir()
        filename = filedialog.askopenfilename(
            parent=self.master.winfo_toplevel(),
            initialdir=initial,
            title="Import OpenAPI document",
            filetypes=[
                ("OpenAPI / YAML", "*.yaml *.yml *.json"),
                ("YAML files", "*.yaml *.yml"),
                ("JSON files", "*.json"),
            ],
        )
        if not filename:
            return
        self._remember_oas_dir(Path(filename).parent)
        self._remember_oas_file(Path(filename))
        try:
            self.workspace = import_oas_file_to_workspace(filename)
        except OasImportError as exc:
            messagebox.showerror("Import OAS", str(exc), parent=self.master.winfo_toplevel())
            return
        self.workspace_path = None
        self._dirty = True
        self._refresh_all()
        self._set_status("OAS imported")

    def apply_inspector_changes(self) -> None:
        if not self.selected_ref:
            return
        kind, obj = self.selected_ref
        if kind == "section" and isinstance(obj, dict):
            if not self._apply_dynamic_section():
                return
            self._dirty = True
            self._refresh_all(preserve_selection=True)
            self._set_status("Changed")
            return
        primary = self.var_primary.get().strip()
        secondary = self.var_secondary.get().strip()
        tertiary = self.var_tertiary.get().strip()
        description = self._get_description_text()

        if kind == "workspace":
            self.workspace.name = primary or "Untitled Workspace"
            self.workspace.description = description
        elif kind == "value_field" and isinstance(obj, dict):
            if not self._apply_value_field_change(obj):
                return
        elif kind == "api" and isinstance(obj, ApiModel):
            obj.name = primary or "New API"
            obj.display_label = obj.name
            obj.info["title"] = secondary or obj.display_label
            obj.openapi_version = tertiary or obj.openapi_version
            obj.info["description"] = description
        elif kind == "path" and obj is not None:
            obj.path = primary or obj.path
            obj.summary = secondary
            obj.description = description
        elif kind == "operation" and obj is not None:
            obj.operation_id = primary or obj.operation_id
            obj.method = secondary.lower() or obj.method
            obj.path = tertiary or obj.path
            obj.description = description
        elif kind == "parameter" and isinstance(obj, dict):
            ref_info = self._resolve_reference_info(obj)
            if ref_info:
                target_payload = deepcopy(ref_info["payload"])
                target_payload["name"] = primary or target_payload.get("name", ref_info["component_name"])
                target_payload["in"] = secondary or target_payload.get("in", "")
                target_payload["required"] = tertiary.lower() in {"true", "1", "yes", "y"}
                target_payload["description"] = description
                if not self._commit_reference_edit(obj, ref_info, target_payload):
                    return
                self._dirty = True
                self._refresh_all(preserve_selection=True)
                self._set_status("Changed")
                return
            obj["name"] = primary or obj.get("name", "")
            obj["in"] = secondary or obj.get("in", "")
            obj["required"] = tertiary.lower() in {"true", "1", "yes", "y"}
            obj["description"] = description
        elif kind == "request_body" and isinstance(obj, dict):
            ref_info = self._resolve_reference_info(obj)
            if ref_info:
                target_payload = deepcopy(ref_info["payload"])
                target_payload["description"] = description
                if not self._commit_reference_edit(obj, ref_info, target_payload):
                    return
                self._dirty = True
                self._refresh_all(preserve_selection=True)
                self._set_status("Changed")
                return
            if primary:
                obj["$ref"] = primary
            elif "$ref" in obj:
                obj.pop("$ref", None)
            obj["required"] = secondary.lower() in {"true", "1", "yes", "y"}
            obj["description"] = description
        elif kind == "response" and isinstance(obj, dict):
            ref_info = self._resolve_reference_info(obj)
            if ref_info:
                target_payload = deepcopy(ref_info["payload"])
                target_payload["description"] = secondary
                self._rename_response(obj, primary)
                if not self._commit_reference_edit(obj, ref_info, target_payload):
                    return
                self._dirty = True
                self._refresh_all(preserve_selection=True)
                self._set_status("Changed")
                return
            self._rename_response(obj, primary)
            obj["description"] = secondary
        elif kind == "change" and obj is not None:
            obj.title = primary or obj.title
            obj.external_ref = secondary
            obj.status = tertiary or obj.status
            obj.description = description
        elif kind == "release" and obj is not None:
            obj.code = primary or obj.code
            obj.release_type = secondary or obj.release_type
            obj.status = tertiary or obj.status
            obj.notes = description
        elif kind == "library" and obj is not None:
            obj.name = primary or obj.name
        elif kind == "component" and obj is not None:
            obj.name = primary or obj.name
        elif kind == "callback" and isinstance(obj, PathItemModel):
            obj.path = primary or obj.path
            obj.summary = secondary
            obj.description = description
        elif kind in {"object_field", "list_field", "resolved_ref"}:
            return
        else:
            return

        self._dirty = True
        self._refresh_all(preserve_selection=True)
        self._set_status("Changed")

    def _apply_dynamic_section(self) -> bool:
        if self._dynamic_meta is None:
            return False
        ref_groups: Dict[str, Dict[str, Any]] = {}
        for binding in self._dynamic_bindings:
            if binding.get("binding_type") != "scalar":
                continue
            new_value = self._binding_value(binding)
            ref_context = binding.get("ref_context")
            if ref_context:
                ref_key = ref_context["ref_info"]["ref"]
                if ref_key not in ref_groups:
                    ref_groups[ref_key] = {
                        "ref_context": ref_context,
                        "payload": deepcopy(ref_context["ref_info"]["payload"]),
                    }
                self._set_nested_value(
                    ref_groups[ref_key]["payload"],
                    list(binding.get("ref_path", ())),
                    new_value,
                )
            else:
                self._set_nested_value(
                    self._dynamic_working_copy,
                    list(binding["path"]),
                    new_value,
                )
        if not self._apply_map_key_renames():
            return False
        self._normalize_schema_modes_in_payload(self._dynamic_working_copy)
        for group in ref_groups.values():
            self._normalize_schema_modes_in_payload(group["payload"])
            if not self._commit_reference_edit(
                group["ref_context"]["ref_holder"],
                group["ref_context"]["ref_info"],
                group["payload"],
            ):
                return False
        meta = self._dynamic_meta
        ref_context = meta.get("ref_context")
        if ref_context and ref_groups:
            return True
        if ref_context and not ref_groups:
            return self._commit_reference_edit(
                ref_context["ref_holder"],
                ref_context["ref_info"],
                self._prune_empty_values(self._dynamic_working_copy),
            )
        cleaned = self._prune_empty_values(self._dynamic_working_copy)
        if meta.get("virtual") and meta.get("parent_mode") == "object" and isinstance(meta.get("parent_payload"), dict):
            meta["parent_payload"][meta.get("parent_key")] = cleaned
            meta["virtual"] = False
            return True
        commit = meta.get("commit")
        if callable(commit):
            commit(cleaned)
            return True
        payload = meta.get("payload")
        if isinstance(payload, dict) and isinstance(cleaned, dict):
            payload.clear()
            payload.update(cleaned)
            return True
        if isinstance(payload, list) and isinstance(cleaned, list):
            payload[:] = cleaned
            return True
        return False

    def _load_workspace_from_path(self, path: Path) -> None:
        workspace = FileSystemDesignerRepository(path).load_workspace()
        workspace.validate()
        self.workspace = workspace
        self.workspace_path = path
        self._dirty = False
        self._remember_workspace_path()
        self._refresh_all()

    def _refresh_all(self, preserve_selection: bool = False) -> None:
        selected = self.selected_ref if preserve_selection else None
        if not preserve_selection:
            self.selected_ref = None
            self.selected_source = "explorer"
        self._refresh_path()
        self._refresh_workspace_tree()
        self._refresh_model_tree()
        self._schedule_model_guides_redraw()
        if selected:
            self._restore_selection(selected)
        else:
            self._select_default_designer_focus()

    def _refresh_path(self) -> None:
        if self.workspace_path:
            marker = " *" if self._dirty else ""
            self.var_path.set(f"{self.workspace_path}{marker}")
        else:
            self.var_path.set("Not saved *" if self._dirty else "Not saved")

    def _refresh_workspace_tree(self) -> None:
        self.workspace_tree.delete(*self.workspace_tree.get_children())
        self._workspace_node_index.clear()

        root = self.workspace_tree.insert("", "end", text=self.workspace.name, open=True)
        self._workspace_node_index[root] = ("workspace", self.workspace)

        api_group = self.workspace_tree.insert(root, "end", text=f"APIs ({len(self.workspace.apis)})", open=True)
        self._workspace_node_index[api_group] = ("api_group", None)
        for api in self.workspace.apis:
            node = self.workspace_tree.insert(api_group, "end", text=api.display_label or api.name)
            self._workspace_node_index[node] = ("api", api)

        library_group = self.workspace_tree.insert(
            root, "end", text=f"Shared Libraries ({len(self.workspace.shared_libraries)})"
        )
        self._workspace_node_index[library_group] = ("library_group", None)
        for library in self.workspace.shared_libraries:
            library_node = self.workspace_tree.insert(library_group, "end", text=library.name, open=True)
            self._workspace_node_index[library_node] = ("library", library)
            for component in library.components:
                component_node = self.workspace_tree.insert(
                    library_node,
                    "end",
                    text=f"{component.component_kind}: {component.name}",
                )
                self._workspace_node_index[component_node] = ("component", component)

        release_group = self.workspace_tree.insert(
            root, "end", text=f"Releases ({len(self.workspace.release_catalog)})"
        )
        self._workspace_node_index[release_group] = ("release_group", None)
        for release in self.workspace.release_catalog:
            release_node = self.workspace_tree.insert(release_group, "end", text=release.code)
            self._workspace_node_index[release_node] = ("release", release)

        change_group = self.workspace_tree.insert(root, "end", text=f"Changes ({len(self.workspace.changes)})")
        self._workspace_node_index[change_group] = ("change_group", None)
        for change in self.workspace.changes:
            label = change.title or change.external_ref or change.id
            change_node = self.workspace_tree.insert(change_group, "end", text=label, open=True)
            self._workspace_node_index[change_node] = ("change", change)
            for step in sorted(change.steps, key=lambda item: item.order):
                step_label = f"{step.order}. {step.kind}"
                step_node = self.workspace_tree.insert(change_node, "end", text=step_label)
                self._workspace_node_index[step_node] = ("change_step", step)

    def _refresh_model_tree(self) -> None:
        if getattr(self, "_model_guides_redraw_job", None):
            try:
                self.master.after_cancel(self._model_guides_redraw_job)
            except Exception:
                pass
            self._model_guides_redraw_job = None
        if hasattr(self.model_tree, "begin_update"):
            self.model_tree.begin_update()
        try:
            self.model_tree.delete(*self.model_tree.get_children())
            self._model_node_index.clear()
            self._model_visual_index.clear()

            if not self.workspace.apis:
                self._insert_model_node("", "No APIs", ("empty", None), open=False)
                return

            api = self._selected_api() or self.workspace.apis[0]
            api_node = self._insert_model_node("", api.display_label or api.name, ("api", api), open=True)
            self._insert_recursive_section(
                api_node,
                "Info",
                self._make_section_meta("Info", api.info, template="info"),
            )
            self._insert_recursive_section(
                api_node,
                "Servers",
                self._make_section_meta("Servers", api.servers, mode="list", item_template="server"),
            )
            self._insert_recursive_section(
                api_node,
                "Tags",
                self._make_section_meta("Tags", api.tags, mode="list", item_template="tag"),
            )
            self._insert_recursive_section(
                api_node,
                "Security",
                self._make_section_meta("Security", api.security, mode="list", item_template="security_requirement"),
            )
            self._insert_recursive_section(
                api_node,
                "External Docs",
                self._make_section_meta("External Docs", api.external_docs, template="external_docs"),
            )

            paths_node = self._insert_model_node(
                api_node, f"Paths ({len(api.path_items)})", ("path_group", api.path_items), open=True
            )
            for path_item in api.path_items:
                parent_node = paths_node
                if self._path_has_shared_data(path_item):
                    path_node = self._insert_model_node(paths_node, path_item.path, ("path", path_item), open=True)
                    self._insert_recursive_section(
                        path_node,
                        "Parameters",
                        self._make_section_meta(
                            "Parameters",
                            path_item.parameters,
                            mode="list",
                            item_template="parameter",
                        ),
                    )
                    parent_node = path_node
                for operation in path_item.operations:
                    operation_path = operation.path or path_item.path
                    label = f"{operation.method.upper()} {operation_path}"
                    op_node = self._insert_model_node(parent_node, label, ("operation", operation), open=True)
                    self._insert_recursive_section(
                        op_node,
                        "Operation",
                        self._make_section_meta(
                            "Operation",
                            self._build_operation_details_payload(operation),
                            template="operation_details",
                            commit=lambda payload, op=operation: self._commit_operation_details(op, payload),
                        ),
                    )
                    self._insert_recursive_section(
                        op_node,
                        "Parameters",
                        self._make_section_meta(
                            "Parameters",
                            operation.parameters,
                            mode="list",
                            item_template="parameter",
                        ),
                    )
                    request_body_ref = self._resolve_reference_info(operation.request_body)
                    self._insert_recursive_section(
                        op_node,
                        self._request_body_label(operation.request_body),
                        self._make_section_meta(
                            "Request Body",
                            deepcopy(request_body_ref["payload"]) if request_body_ref else operation.request_body,
                            template="request_body",
                            ref_context=self._ref_context_for(operation.request_body) if operation.request_body else None,
                            default_factory=lambda: {},
                            commit=(
                                None
                                if operation.request_body or request_body_ref
                                else lambda payload, op=operation: self._commit_request_body(op, payload)
                            ),
                        ),
                    )
                    self._insert_recursive_section(
                        op_node,
                        "Responses",
                        self._make_section_meta(
                            "Responses",
                            operation.responses,
                            mode="map",
                            item_template="response",
                        ),
                    )
                    self._insert_recursive_section(
                        op_node,
                        "Callbacks",
                        self._make_section_meta(
                            "Callbacks",
                            self._build_callbacks_payload(operation),
                            mode="map",
                            item_template="path_item",
                            commit=lambda payload, op=operation: self._commit_callbacks(op, payload),
                        ),
                    )

            if api.webhooks:
                webhooks_node = self._insert_model_node(
                    api_node, f"Webhooks ({len(api.webhooks)})", ("webhook_group", api.webhooks), open=True
                )
                for webhook in api.webhooks:
                    webhook_node = self._insert_model_node(
                        webhooks_node,
                        webhook.path or webhook.id,
                        ("path", webhook),
                        open=True,
                    )
                    self._insert_recursive_section(
                        webhook_node,
                        "Parameters",
                        self._make_section_meta(
                            "Parameters",
                            webhook.parameters,
                            mode="list",
                            item_template="parameter",
                        ),
                    )
                    for operation in webhook.operations:
                        operation_path = operation.path or webhook.path
                        label = f"{operation.method.upper()} {operation_path}"
                        op_node = self._insert_model_node(webhook_node, label, ("operation", operation), open=True)
                        self._insert_recursive_section(
                            op_node,
                            "Operation",
                            self._make_section_meta(
                                "Operation",
                                self._build_operation_details_payload(operation),
                                template="operation_details",
                                commit=lambda payload, op=operation: self._commit_operation_details(op, payload),
                            ),
                        )
                        self._insert_recursive_section(
                            op_node,
                            "Parameters",
                            self._make_section_meta(
                                "Parameters",
                                operation.parameters,
                                mode="list",
                                item_template="parameter",
                            ),
                        )
                        request_body_ref = self._resolve_reference_info(operation.request_body)
                        self._insert_recursive_section(
                            op_node,
                            self._request_body_label(operation.request_body),
                            self._make_section_meta(
                                "Request Body",
                                deepcopy(request_body_ref["payload"]) if request_body_ref else operation.request_body,
                                template="request_body",
                                ref_context=self._ref_context_for(operation.request_body)
                                if operation.request_body
                                else None,
                                default_factory=lambda: {},
                                commit=(
                                    None
                                    if operation.request_body or request_body_ref
                                    else lambda payload, op=operation: self._commit_request_body(op, payload)
                                ),
                            ),
                        )
                        self._insert_recursive_section(
                            op_node,
                            "Responses",
                            self._make_section_meta(
                                "Responses",
                                operation.responses,
                                mode="map",
                                item_template="response",
                            ),
                        )
                        self._insert_recursive_section(
                            op_node,
                            "Callbacks",
                            self._make_section_meta(
                                "Callbacks",
                                self._build_callbacks_payload(operation),
                                mode="map",
                                item_template="path_item",
                                commit=lambda payload, op=operation: self._commit_callbacks(op, payload),
                            ),
                        )

            local_component_total = sum(
                len(component_map)
                for component_map in api.local_components.values()
                if isinstance(component_map, dict)
            )
            total_components = local_component_total + len(api.shared_component_refs)
            components_node = self._insert_model_node(
                api_node, f"Components ({total_components})", ("components", api), open=True
            )

            kind_nodes: Dict[str, str] = {}
            kind_counts: Dict[str, int] = {}

            for component_kind, component_map in sorted(api.local_components.items()):
                if not isinstance(component_map, dict):
                    continue
                normalized_kind = self._normalize_component_kind(component_kind)
                kind_counts[normalized_kind] = len(component_map)
                kind_node = self._insert_model_node(
                    components_node,
                    f"{normalized_kind} ({len(component_map)})",
                    ("component_kind", {"kind": normalized_kind, "count": len(component_map)}),
                    open=False,
                )
                kind_nodes[normalized_kind] = kind_node
                for name, payload in sorted(component_map.items()):
                    self._insert_model_node(
                        kind_node,
                        name,
                        (
                            "section",
                            self._make_section_meta(
                                name,
                                payload,
                                template=self._template_for_component_kind(normalized_kind),
                            ),
                        ),
                    )

            for ref in api.shared_component_refs:
                component_kind = self._normalize_component_kind(ref.get("component_kind", "component"))
                if component_kind not in kind_nodes:
                    kind_counts[component_kind] = 0
                    kind_node = self._insert_model_node(
                        components_node,
                        f"{component_kind} (0)",
                        ("component_kind", {"kind": component_kind, "count": 0}),
                        open=False,
                    )
                    kind_nodes[component_kind] = kind_node

                kind_counts[component_kind] += 1
                kind_node = kind_nodes[component_kind]
                self.model_tree.item(kind_node, text=f"{component_kind} ({kind_counts[component_kind]})")

                component_id = ref.get("component_id", "")
                library_id = ref.get("library_id", "")
                text = f"[shared] {component_id}"
                if library_id:
                    text = f"{text} ({library_id})"
                ref_node = self._insert_model_node(
                    kind_node,
                    text,
                    ("shared_ref", ref),
                    tags=("shared_component",),
                )
                shared_payload = self._resolve_shared_component_payload(ref)
                if shared_payload is not None:
                    self._model_node_index[ref_node] = (
                        "section",
                        self._make_section_meta(
                            text,
                            shared_payload,
                            template=self._template_for_component_kind(component_kind),
                            commit=lambda payload, shared=ref: self._commit_shared_component_payload(shared, payload),
                        ),
                    )
        finally:
            if hasattr(self.model_tree, "end_update"):
                self.model_tree.end_update()

    def _normalize_component_kind(self, raw_kind: str) -> str:
        kind = (raw_kind or "component").strip()
        if not kind:
            return "component"
        normalized = kind.lower().replace("_", "")
        aliases = {
            "schema": "schemas",
            "schemas": "schemas",
            "header": "headers",
            "headers": "headers",
            "response": "responses",
            "responses": "responses",
            "parameter": "parameters",
            "parameters": "parameters",
            "requestbody": "requestBodies",
            "requestbodies": "requestBodies",
            "securityscheme": "securitySchemes",
            "securityschemes": "securitySchemes",
            "example": "examples",
            "examples": "examples",
            "link": "links",
            "links": "links",
            "callback": "callbacks",
            "callbacks": "callbacks",
        }
        return aliases.get(normalized, kind)

    def _make_section_meta(
        self,
        label: str,
        payload: Any,
        *,
        mode: str = "object",
        template: Optional[str] = None,
        item_template: Optional[str] = None,
        ref_context: Optional[Dict[str, Any]] = None,
        commit: Optional[Callable[[Any], None]] = None,
        default_factory: Optional[Callable[[], Any]] = None,
        direct_only: bool = False,
        node_path: tuple[Any, ...] = (),
        parent_payload: Any = None,
        parent_mode: Optional[str] = None,
        parent_key: Any = None,
        virtual: bool = False,
    ) -> Dict[str, Any]:
        return {
            "label": label,
            "payload": payload,
            "mode": mode,
            "template": template,
            "item_template": item_template,
            "ref_context": ref_context,
            "commit": commit,
            "default_factory": default_factory,
            "direct_only": direct_only,
            "node_path": node_path,
            "parent_payload": parent_payload,
            "parent_mode": parent_mode,
            "parent_key": parent_key,
            "virtual": virtual,
        }

    def _insert_recursive_section(
        self,
        parent_node: str,
        label: str,
        meta: Dict[str, Any],
    ) -> None:
        if "node_path" not in meta or not meta.get("node_path"):
            meta = {**meta, "node_path": (label,), "direct_only": True}
        payload = meta.get("payload")
        node_text = label
        if isinstance(payload, list):
            node_text = f"{label} ({len(payload)})"
        elif meta.get("mode") == "map" and isinstance(payload, dict):
            node_text = f"{label} ({len(payload)})"
        node = self._insert_model_node(parent_node, node_text, ("section", meta), open=True)
        self._insert_section_children(node, meta)

    def _insert_model_node(
        self,
        parent_node: str,
        raw_text: str,
        ref: Tuple[str, Any],
        *,
        open: bool = True,
        tags: tuple[str, ...] = (),
    ) -> str:
        parent_meta = self._model_visual_index.get(parent_node)
        depth = 0 if parent_meta is None else parent_meta["depth"] + 1
        ancestors = [] if parent_meta is None else parent_meta["ancestors"] + [parent_meta["raw_text"]]
        node = self.model_tree.insert(
            parent_node,
            "end",
            text=self._tree_display_text(raw_text, depth),
            open=open,
            tags=tags,
        )
        self._model_node_index[node] = ref
        self._model_visual_index[node] = {
            "raw_text": raw_text,
            "depth": depth,
            "ancestors": ancestors,
        }
        return node

    def _insert_section_children(self, parent_node: str, meta: Dict[str, Any]) -> None:
        payload = meta.get("payload")
        mode = meta.get("mode", "object")
        if mode == "object" and isinstance(payload, dict):
            for child_label, child_meta in self._tree_children_for_object(meta):
                self._insert_recursive_section(parent_node, child_label, child_meta)
            return
        if mode == "list" and isinstance(payload, list):
            item_template = meta.get("item_template")
            for index, child in enumerate(payload):
                child_meta = self._tree_meta_for_collection_item(
                    meta,
                    index,
                    child,
                    item_template=item_template,
                    path_segment=index,
                )
                if child_meta is None:
                    continue
                label = self._collection_item_title(index, child, item_template)
                self._insert_recursive_section(parent_node, label, child_meta)
            return
        if mode == "map" and isinstance(payload, dict):
            item_template = meta.get("item_template")
            for map_key, child in payload.items():
                child_meta = self._tree_meta_for_collection_item(
                    meta,
                    map_key,
                    child,
                    item_template=item_template,
                    path_segment=map_key,
                )
                if child_meta is None:
                    continue
                label = str(map_key)
                self._insert_recursive_section(parent_node, label, child_meta)

    def _tree_children_for_object(self, meta: Dict[str, Any]) -> list[tuple[str, Dict[str, Any]]]:
        payload = meta.get("payload")
        if not isinstance(payload, dict):
            return []
        template = meta.get("template")
        children: list[tuple[str, Dict[str, Any]]] = []
        seen: set[str] = set()
        for key, child in self._iter_object_fields(payload, template):
            child_mode, child_template, child_item_template = self._child_meta_for_key(key, child)
            if not self._tree_child_should_exist(key, child, template, child_mode, payload):
                continue
            seen.add(key)
            child_payload = child
            child_ref_context = None
            if child_mode == "object" and isinstance(child, dict):
                ref_info = self._resolve_reference_info(child)
                if ref_info:
                    child_payload = child
                    child_ref_context = {"ref_holder": child, "ref_info": ref_info}
            children.append(
                (
                    self._display_label(key),
                    self._make_section_meta(
                        self._display_label(key),
                        child_payload,
                        mode=child_mode,
                        template=child_template,
                        item_template=child_item_template,
                        ref_context=child_ref_context,
                        direct_only=True,
                        node_path=tuple(meta.get("node_path", ())) + (key,),
                        parent_payload=payload,
                        parent_mode="object",
                        parent_key=key,
                        virtual=False,
                    ),
                )
            )
        for key in self._always_visible_tree_children(template, payload):
            if key in seen:
                continue
            child_mode, child_template, child_item_template = self._child_meta_for_key(key, payload.get(key))
            default_payload = self._default_structural_value(key, child_mode, child_template)
            children.append(
                (
                    self._display_label(key),
                    self._make_section_meta(
                        self._display_label(key),
                        default_payload,
                        mode=child_mode,
                        template=child_template,
                        item_template=child_item_template,
                        direct_only=True,
                        node_path=tuple(meta.get("node_path", ())) + (key,),
                        parent_payload=payload,
                        parent_mode="object",
                        parent_key=key,
                        virtual=True,
                    ),
                )
            )
        return children

    def _tree_meta_for_collection_item(
        self,
        parent_meta: Dict[str, Any],
        key: Any,
        child: Any,
        *,
        item_template: Optional[str],
        path_segment: Any,
    ) -> Optional[Dict[str, Any]]:
        parent_path = tuple(parent_meta.get("node_path", ()))
        if isinstance(child, dict):
            mode = "object"
            template = item_template
            if item_template == "schema":
                template = "schema"
            return self._make_section_meta(
                str(key),
                child,
                mode=mode,
                template=template,
                direct_only=True,
                node_path=parent_path + (path_segment,),
                parent_payload=parent_meta.get("payload"),
                parent_mode=parent_meta.get("mode"),
                parent_key=key,
                virtual=False,
            )
        if isinstance(child, list):
            return self._make_section_meta(
                str(key),
                child,
                mode="list",
                item_template=item_template,
                direct_only=True,
                node_path=parent_path + (path_segment,),
                parent_payload=parent_meta.get("payload"),
                parent_mode=parent_meta.get("mode"),
                parent_key=key,
                virtual=False,
            )
        return None

    def _list_item_label(self, index: int, child: Any) -> str:
        if isinstance(child, dict):
            if "$ref" in child:
                ref = str(child.get("$ref", ""))
                return ref.split("/")[-1] if ref else f"[{index}]"
            for key in ("name", "title", "operationId", "url"):
                if key in child:
                    return str(child[key])
        return f"Item {index + 1}"

    def _collection_item_title(self, index: int, child: Any, item_template: Optional[str]) -> str:
        template_titles = {
            "server": "Server",
            "tag": "Tag",
            "parameter": "Parameter",
            "security_requirement": "Security Requirement",
            "schema": "Schema",
            "response": "Response",
            "header": "Header",
            "link": "Link",
            "example": "Example",
            "server_variable": "Variable",
        }
        base = template_titles.get(item_template)
        detail = self._list_item_label(index, child)
        if base and detail and detail != f"Item {index + 1}":
            return f"{base}: {detail}"
        if base:
            return f"{base} {index + 1}"
        return detail

    def _display_label(self, raw: str) -> str:
        if not raw:
            return ""
        label = raw.replace("_", " ")
        pieces: list[str] = []
        current = ""
        for char in label:
            if current and char.isupper() and not current[-1].isupper():
                pieces.append(current)
                current = char
            else:
                current += char
        if current:
            pieces.append(current)
        words = " ".join(pieces).split()
        return " ".join(word if word.isupper() else word.capitalize() for word in words)

    def _tree_display_text(self, raw_text: str, depth: int) -> str:
        return raw_text

    def _tree_guide_parent_label(self, ancestors: list[str], guide_index: int) -> Optional[str]:
        if guide_index < 0 or guide_index >= len(ancestors):
            return None
        return ancestors[guide_index]

    def _schedule_model_guides_redraw(self) -> None:
        tree = getattr(self, "model_tree", None)
        if tree is None or not hasattr(tree, "redraw"):
            return
        if getattr(self, "_model_guides_redraw_job", None):
            try:
                self.master.after_cancel(self._model_guides_redraw_job)
            except Exception:
                pass
        self._model_guides_redraw_job = self.master.after(16, self._redraw_model_guides)

    def _redraw_model_guides(self) -> None:
        self._model_guides_redraw_job = None
        tree = getattr(self, "model_tree", None)
        if tree is None or not hasattr(tree, "redraw"):
            return
        tree.redraw()

    def _visible_model_nodes(self) -> list[str]:
        if hasattr(self.model_tree, "_visible_nodes"):
            return list(self.model_tree._visible_nodes)
        result: list[str] = []

        def walk(parent: str) -> None:
            for child in self.model_tree.get_children(parent):
                if self.model_tree.bbox(child):
                    result.append(child)
                if self.model_tree.item(child, "open"):
                    walk(child)

        walk("")
        return result

    def _last_visible_descendant(self, node_id: str) -> str:
        if hasattr(self.model_tree, "_last_visible_descendant"):
            return self.model_tree._last_visible_descendant(node_id)
        children = self.model_tree.get_children(node_id)
        if not children or not self.model_tree.item(node_id, "open"):
            return node_id
        last_child = children[-1]
        return self._last_visible_descendant(last_child)

    def _inspector_indent(self, path: tuple[Any, ...]) -> int:
        depth = self._schema_visual_depth(path)
        if depth <= 0:
            return 0
        return min(depth * 18, 72)

    def _schema_visual_depth(self, path: tuple[Any, ...]) -> int:
        depth = 0
        for segment in path:
            if segment in {"schema", "properties", "items", "allOf", "anyOf", "oneOf"}:
                depth += 1
        return max(0, depth - 1)

    def _on_workspace_select(self, _event=None) -> None:
        selection = self.workspace_tree.selection()
        if not selection:
            return
        ref = self._workspace_node_index.get(selection[0])
        if not ref:
            return
        self._clear_tree_selection(self.model_tree)
        self.selected_ref = ref
        self.selected_source = "explorer"
        self._render_inspector(*ref)
        if ref[0] == "api":
            self._refresh_model_tree()

    def _on_model_select(self, _event=None) -> None:
        selection = self.model_tree.selection()
        if not selection:
            return
        ref = self._model_node_index.get(selection[0])
        if not ref:
            return
        self._clear_tree_selection(self.workspace_tree)
        self.selected_ref = ref
        self.selected_source = "model"
        self._render_inspector(*ref)

    def _on_model_context_menu(self, event) -> None:
        node_id = self.model_tree.identify_row(event.y)
        if not node_id:
            return
        self._apply_tree_selection(self.model_tree, node_id)
        ref = self._model_node_index.get(node_id)
        if not ref:
            return
        self._clear_tree_selection(self.workspace_tree)
        self.selected_ref = ref
        self.selected_source = "model"
        self._render_inspector(*ref)
        actions = self._context_actions_for_ref(ref)
        if not actions:
            return
        self.model_context_menu.delete(0, "end")
        for label, command in actions:
            self.model_context_menu.add_command(label=label, command=command)
        try:
            self.model_context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.model_context_menu.grab_release()

    def _on_model_guides_motion(self, event) -> None:
        label = getattr(self.model_tree, "_current_guide_label", None)
        if not label:
            self._hide_model_tooltip()
            return
        self._show_model_tooltip(event.x_root + 14, event.y_root + 12, f"Parent: {label}")

    def _show_model_tooltip(self, x_root: int, y_root: int, text: str) -> None:
        if self._model_tooltip_window is None:
            self._model_tooltip_window = tk.Toplevel(self.model_tree)
            self._model_tooltip_window.wm_overrideredirect(True)
            self._model_tooltip_window.attributes("-topmost", True)
            self._model_tooltip_label = tk.Label(
                self._model_tooltip_window,
                text=text,
                background="#FFFBEA",
                foreground="#27323A",
                relief="solid",
                borderwidth=1,
                padx=6,
                pady=3,
            )
            self._model_tooltip_label.pack()
        else:
            self._model_tooltip_label.configure(text=text)
        self._model_tooltip_window.geometry(f"+{x_root}+{y_root}")
        self._model_tooltip_window.deiconify()

    def _hide_model_tooltip(self, _event=None) -> None:
        if self._model_tooltip_window is not None:
            self._model_tooltip_window.withdraw()

    def _context_actions_for_ref(self, ref: Tuple[str, Any]) -> list[tuple[str, Callable[[], None]]]:
        kind, obj = ref
        node_id = self.model_tree.focus()
        actions: list[tuple[str, Callable[[], None]]] = []
        actions.extend(
            [
                ("Expand All", self._expand_all_model_nodes),
                ("Collapse All", self._collapse_all_model_nodes),
            ]
        )
        if node_id:
            actions.extend(
                [
                    ("Expand Siblings At This Level", lambda n=node_id: self._expand_model_siblings_at_level(n)),
                    ("Collapse Siblings At This Level", lambda n=node_id: self._collapse_model_siblings_at_level(n)),
                ]
            )
        if node_id and self.model_tree.get_children(node_id):
            actions.extend(
                [
                    ("Expand All Below", lambda n=node_id: self._expand_model_subtree_and_redraw(n)),
                    ("Collapse All Below", lambda n=node_id: self._collapse_model_subtree_and_redraw(n)),
                ]
            )
        if kind != "section" or not isinstance(obj, dict):
            return actions
        mode = obj.get("mode")
        if mode in {"list", "map"}:
            actions.append(("Add", lambda meta=obj: self._context_add_section_item(meta)))
        if obj.get("parent_mode") in {"list", "map"}:
            actions.append(("Delete", lambda meta=obj: self._context_delete_section_node(meta)))
        return actions

    def _with_model_tree_batch_update(self, callback: Callable[[], None], *, redraw_guides: bool = True) -> None:
        if hasattr(self.model_tree, "begin_update"):
            self.model_tree.begin_update()
        try:
            callback()
        finally:
            if hasattr(self.model_tree, "end_update"):
                self.model_tree.end_update()
        if redraw_guides:
            self._schedule_model_guides_redraw()

    def _model_parent_node(self, node_id: str) -> str:
        nodes = getattr(self.model_tree, "_nodes", {})
        if not isinstance(nodes, dict):
            return ""
        node = nodes.get(node_id)
        if not isinstance(node, dict):
            return ""
        parent = node.get("parent")
        return str(parent) if parent else ""

    def _model_node_chain(self, node_id: str) -> list[str]:
        chain: list[str] = []
        current = node_id
        seen: set[str] = set()
        while current and current not in seen:
            chain.append(current)
            seen.add(current)
            current = self._model_parent_node(current)
        chain.reverse()
        return chain

    def _model_level_selector(self, node_id: str) -> tuple[Any, ...]:
        kind, obj = self._model_node_index.get(node_id, ("", None))
        if kind == "section" and isinstance(obj, dict):
            return (
                "section",
                tuple(obj.get("node_path", ())),
                obj.get("mode"),
                obj.get("template"),
                obj.get("item_template"),
            )
        if kind == "component_kind" and isinstance(obj, dict):
            return ("component_kind", obj.get("kind"))
        return (kind,)

    def _model_matching_children(self, parent_node: str, selector: tuple[Any, ...]) -> list[str]:
        matches: list[str] = []
        for child in self.model_tree.get_children(parent_node):
            if self._model_level_selector(child) == selector:
                matches.append(child)
        return matches

    def _set_model_siblings_at_level(self, node_id: str, *, expand: bool) -> None:
        chain = self._model_node_chain(node_id)
        if not chain:
            return
        selectors = [self._model_level_selector(current) for current in chain]

        def apply() -> None:
            frontier = [""]
            for index, selector in enumerate(selectors):
                next_frontier: list[str] = []
                is_target_level = index == len(selectors) - 1
                for parent in frontier:
                    matches = self._model_matching_children(parent, selector)
                    if expand:
                        for match in matches:
                            self.model_tree.item(match, open=True)
                    elif is_target_level:
                        for match in matches:
                            self.model_tree.item(match, open=False)
                    next_frontier.extend(matches)
                frontier = next_frontier

        self._with_model_tree_batch_update(apply)

    def _expand_model_siblings_at_level(self, node_id: str) -> None:
        self._set_model_siblings_at_level(node_id, expand=True)

    def _collapse_model_siblings_at_level(self, node_id: str) -> None:
        self._set_model_siblings_at_level(node_id, expand=False)

    def _expand_all_model_nodes(self) -> None:
        self._with_model_tree_batch_update(
            lambda: [self._expand_model_subtree(node) for node in self.model_tree.get_children("")]
        )

    def _collapse_all_model_nodes(self) -> None:
        self._with_model_tree_batch_update(
            lambda: [self._collapse_model_subtree(node) for node in self.model_tree.get_children("")]
        )

    def _expand_model_subtree(self, node_id: str) -> None:
        stack = [node_id]
        while stack:
            current = stack.pop()
            self.model_tree.item(current, open=True)
            children = list(self.model_tree.get_children(current))
            stack.extend(reversed(children))

    def _collapse_model_subtree(self, node_id: str) -> None:
        stack = [node_id]
        while stack:
            current = stack.pop()
            self.model_tree.item(current, open=False)
            children = list(self.model_tree.get_children(current))
            stack.extend(reversed(children))

    def _expand_model_subtree_and_redraw(self, node_id: str) -> None:
        self._with_model_tree_batch_update(lambda: self._expand_model_subtree(node_id))

    def _collapse_model_subtree_and_redraw(self, node_id: str) -> None:
        self._with_model_tree_batch_update(lambda: self._collapse_model_subtree(node_id))

    def _context_add_section_item(self, meta: Dict[str, Any]) -> None:
        target = meta.get("payload")
        mode = meta.get("mode")
        if meta.get("virtual") and meta.get("parent_mode") == "object" and isinstance(meta.get("parent_payload"), dict):
            meta["parent_payload"][meta.get("parent_key")] = target
            meta["virtual"] = False
        if mode == "list" and isinstance(target, list):
            target.append(self._new_collection_item(tuple(meta.get("node_path", ())), target, meta.get("item_template")))
        elif mode == "map" and isinstance(target, dict):
            new_key = self._prompt_map_key(self._map_key_label(tuple(meta.get("node_path", ()))))
            if not new_key:
                return
            if new_key in target:
                messagebox.showerror(
                    "Duplicate Entry",
                    f"An item named '{new_key}' already exists.",
                    parent=self.master.winfo_toplevel(),
                )
                return
            target[new_key] = self._new_map_item(tuple(meta.get("node_path", ())), meta.get("item_template"))
        else:
            return
        self._dirty = True
        self._refresh_all(preserve_selection=True)
        self._set_status("Changed")

    def _context_delete_section_node(self, meta: Dict[str, Any]) -> None:
        parent_payload = meta.get("parent_payload")
        parent_mode = meta.get("parent_mode")
        parent_key = meta.get("parent_key")
        if parent_mode == "list" and isinstance(parent_payload, list) and isinstance(parent_key, int):
            if 0 <= parent_key < len(parent_payload):
                parent_payload.pop(parent_key)
            else:
                return
        elif parent_mode in {"map", "object"} and isinstance(parent_payload, dict) and parent_key in parent_payload:
            if parent_mode == "object":
                parent_payload[parent_key] = self._default_structural_value(
                    str(parent_key),
                    meta.get("mode", "object"),
                    meta.get("template"),
                )
            else:
                parent_payload.pop(parent_key, None)
        else:
            return
        self._dirty = True
        self._refresh_all()
        self._set_status("Changed")

    def _render_inspector(self, kind: str, obj: Any) -> None:
        source_label = "Explorer" if self.selected_source == "explorer" else "Model"
        if kind == "section" and isinstance(obj, dict):
            self.var_context.set(f"{source_label} > {obj.get('label', 'Section')}")
            self._render_dynamic_section(obj)
            return
        self.var_context.set(f"{source_label} > {kind.replace('_', ' ').title()}")
        self._clear_dynamic_editor()
        config = self._inspector_config(kind, obj)
        self.var_primary_label.set(config["primary_label"])
        self.var_secondary_label.set(config["secondary_label"])
        self.var_tertiary_label.set(config["tertiary_label"])
        self.var_description_label.set(config["description_label"])
        self.var_primary.set(config["primary_value"])
        self.var_secondary.set(config["secondary_value"])
        self.var_tertiary.set(config["tertiary_value"])

        description = config["description_value"]
        self._set_description_text(description)
        self._configure_field_slot(
            "primary",
            config["primary_editor"],
            config["primary_state"],
            config["primary_options"],
        )
        self._configure_field_slot(
            "secondary",
            config["secondary_editor"],
            config["secondary_state"],
            config["secondary_options"],
        )
        self._configure_field_slot(
            "tertiary",
            config["tertiary_editor"],
            config["tertiary_state"],
            config["tertiary_options"],
        )
        self.entry_description.configure(state=config["description_state"])
        self.btn_apply.configure(state=config["apply_state"])
        self._set_field_visibility(self.lbl_primary, self.entry_primary, config["show_primary"])
        self._set_field_visibility(self.lbl_secondary, self.entry_secondary, config["show_secondary"])
        self._set_field_visibility(self.lbl_tertiary, self.entry_tertiary, config["show_tertiary"])
        self._set_field_visibility(
            self.lbl_description,
            self.entry_description,
            config["show_description"],
        )

    def _on_inspector_mode_change(self, _value: str) -> None:
        if not self.selected_ref:
            return
        kind, obj = self.selected_ref
        self._render_inspector(kind, obj)

    def _render_dynamic_section(self, meta: Dict[str, Any]) -> None:
        self._dynamic_meta = meta
        payload = deepcopy(meta.get("payload"))
        if payload is None and meta.get("default_factory"):
            payload = meta["default_factory"]()
        self._dynamic_working_copy = self._prepare_section_payload(
            payload,
            meta.get("template"),
            meta.get("mode", "object"),
        )
        self._clear_dynamic_editor()
        for widget in (
            self.lbl_primary,
            self.entry_primary,
            self.combo_primary,
            self.lbl_secondary,
            self.entry_secondary,
            self.combo_secondary,
            self.lbl_tertiary,
            self.entry_tertiary,
            self.combo_tertiary,
            self.lbl_description,
            self.entry_description,
        ):
            widget.grid_remove()
        self.dynamic_editor.grid()
        self.btn_apply.configure(state="normal" if self._is_edit_mode() else "disabled")
        mode = meta.get("mode", "object")
        if meta.get("direct_only"):
            if mode == "list":
                self._render_atomic_list(
                    self.dynamic_editor,
                    self._dynamic_working_copy if isinstance(self._dynamic_working_copy, list) else [],
                    (),
                    item_template=meta.get("item_template"),
                )
            elif mode == "map":
                self._render_atomic_map(
                    self.dynamic_editor,
                    self._dynamic_working_copy if isinstance(self._dynamic_working_copy, dict) else {},
                    (),
                    item_template=meta.get("item_template"),
                )
            else:
                self._render_atomic_object(
                    self.dynamic_editor,
                    self._dynamic_working_copy if isinstance(self._dynamic_working_copy, dict) else {},
                    (),
                    template=meta.get("template"),
                    ref_context=meta.get("ref_context"),
                )
        elif mode == "list":
            self._render_dynamic_list(
                self.dynamic_editor,
                self._dynamic_working_copy if isinstance(self._dynamic_working_copy, list) else [],
                (),
                item_template=meta.get("item_template"),
                ref_context=meta.get("ref_context"),
                show_add_button=True,
            )
        elif mode == "map":
            self._render_dynamic_map(
                self.dynamic_editor,
                self._dynamic_working_copy if isinstance(self._dynamic_working_copy, dict) else {},
                (),
                item_template=meta.get("item_template"),
                ref_context=meta.get("ref_context"),
                show_add_button=True,
            )
        else:
            self._render_dynamic_object(
                self.dynamic_editor,
                self._dynamic_working_copy if isinstance(self._dynamic_working_copy, dict) else {},
                (),
                template=meta.get("template"),
                ref_context=meta.get("ref_context"),
            )

    def _prepare_section_payload(self, payload: Any, template: Optional[str], mode: str) -> Any:
        prepared = deepcopy(payload)
        if mode == "object":
            if self._is_edit_mode():
                return self._merge_template(prepared if isinstance(prepared, dict) else {}, template)
            return prepared if isinstance(prepared, dict) else {}
        if mode == "list":
            return prepared if isinstance(prepared, list) else []
        if mode == "map":
            return prepared if isinstance(prepared, dict) else {}
        return prepared

    def _merge_template(self, payload: dict[str, Any], template: Optional[str]) -> dict[str, Any]:
        result = deepcopy(SECTION_TEMPLATES.get(template, {}))
        for key, value in payload.items():
            result[key] = deepcopy(value)
        return result

    def _clear_dynamic_editor(self) -> None:
        self.dynamic_editor.grid_remove()
        for child in self.dynamic_editor.winfo_children():
            child.destroy()
        self._dynamic_bindings.clear()

    def _is_edit_mode(self) -> bool:
        return self.var_inspector_mode.get() == "Edit"

    def _should_render_value(self, value: Any) -> bool:
        if self._is_edit_mode():
            return True
        if isinstance(value, bool):
            return value
        if isinstance(value, (list, dict)):
            return len(value) > 0
        return value not in ("", None)

    def _inspector_config(self, kind: str, obj: Any) -> Dict[str, str]:
        config = {
            "primary_label": "Name",
            "secondary_label": "Version",
            "tertiary_label": "Path",
            "description_label": "Description",
            "primary_value": "",
            "secondary_value": "",
            "tertiary_value": "",
            "description_value": "",
            "primary_state": "disabled",
            "secondary_state": "disabled",
            "tertiary_state": "disabled",
            "description_state": "disabled",
            "apply_state": "disabled",
            "primary_editor": "entry",
            "secondary_editor": "entry",
            "tertiary_editor": "entry",
            "primary_options": [],
            "secondary_options": [],
            "tertiary_options": [],
            "show_primary": True,
            "show_secondary": True,
            "show_tertiary": True,
            "show_description": True,
        }
        if kind == "workspace":
            config.update(
                {
                    "primary_label": "Workspace Name",
                    "primary_value": self.workspace.name,
                    "description_value": self.workspace.description,
                    "primary_state": "normal",
                    "description_state": "normal",
                    "apply_state": "normal",
                    "show_secondary": False,
                    "show_tertiary": False,
                }
            )
        elif kind == "value_field" and isinstance(obj, dict):
            value = obj.get("value")
            value_type = type(value).__name__
            config.update(
                {
                    "primary_label": "Attribute",
                    "secondary_label": "Value",
                    "tertiary_label": "Type",
                    "primary_value": obj.get("label", ""),
                    "secondary_value": self._format_scalar_value(value),
                    "tertiary_value": value_type,
                    "primary_state": "disabled",
                    "tertiary_state": "disabled",
                    "description_state": "disabled",
                    "apply_state": "normal",
                    "show_description": False,
                }
            )
            options = self._value_field_options(obj)
            if options:
                config["secondary_editor"] = "combo"
                config["secondary_state"] = "readonly"
                config["secondary_options"] = options
            else:
                config["secondary_state"] = "normal"
            if isinstance(value, str) and ("\n" in value or len(value) > 80):
                config.update(
                    {
                        "secondary_state": "disabled",
                        "description_label": obj.get("label", ""),
                        "description_value": value,
                        "description_state": "normal",
                        "show_description": True,
                    }
                )
            return config
        elif kind in {"object_field", "list_field", "resolved_ref"} and isinstance(obj, dict):
            config.update(
                {
                    "primary_label": "Section",
                    "primary_value": obj.get("label", ""),
                    "primary_state": "disabled",
                    "show_secondary": False,
                    "show_tertiary": False,
                    "show_description": False,
                    "apply_state": "disabled",
                }
            )
            return config
        elif kind == "api" and isinstance(obj, ApiModel):
            config.update(
                {
                    "primary_label": "API Name",
                    "secondary_label": "Title",
                    "tertiary_label": "OpenAPI",
                    "primary_value": obj.name,
                    "secondary_value": obj.info.get("title", obj.display_label or obj.name),
                    "tertiary_value": obj.openapi_version,
                    "description_label": "Description",
                    "description_value": obj.info.get("description", ""),
                    "primary_state": "normal",
                    "secondary_state": "normal",
                    "tertiary_state": "readonly",
                    "tertiary_editor": "combo",
                    "tertiary_options": ["3.0.0", "3.0.1", "3.1.0"],
                    "description_state": "normal",
                    "apply_state": "normal",
                }
            )
        elif kind == "path" and obj is not None:
            config.update(
                {
                    "primary_label": "Path",
                    "secondary_label": "Summary",
                    "primary_value": getattr(obj, "path", ""),
                    "secondary_value": getattr(obj, "summary", ""),
                    "description_label": "Description",
                    "description_value": getattr(obj, "description", ""),
                    "primary_state": "normal",
                    "secondary_state": "normal",
                    "description_state": "normal",
                    "apply_state": "normal",
                    "show_tertiary": False,
                }
            )
        elif kind == "operation" and obj is not None:
            config.update(
                {
                    "primary_label": "Operation ID",
                    "secondary_label": "Method",
                    "tertiary_label": "Path",
                    "primary_value": getattr(obj, "operation_id", ""),
                    "secondary_value": getattr(obj, "method", "").upper(),
                    "tertiary_value": getattr(obj, "path", ""),
                    "description_label": "Description",
                    "description_value": getattr(obj, "description", ""),
                    "primary_state": "normal",
                    "secondary_state": "readonly",
                    "secondary_editor": "combo",
                    "secondary_options": ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS", "TRACE"],
                    "tertiary_state": "normal",
                    "description_state": "normal",
                    "apply_state": "normal",
                }
            )
        elif kind == "callback" and obj is not None:
            config.update(
                {
                    "primary_label": "Callback Path",
                    "secondary_label": "Summary",
                    "primary_value": getattr(obj, "path", ""),
                    "secondary_value": getattr(obj, "summary", ""),
                    "description_label": "Description",
                    "description_value": getattr(obj, "description", ""),
                    "primary_state": "normal",
                    "secondary_state": "normal",
                    "description_state": "normal",
                    "apply_state": "normal",
                    "show_tertiary": False,
                }
            )
        elif kind == "parameter" and isinstance(obj, dict):
            ref_info = self._resolve_reference_info(obj)
            if ref_info:
                target = ref_info["payload"]
                config.update(
                    {
                        "primary_label": "Component",
                        "secondary_label": "In",
                        "tertiary_label": "Required",
                        "primary_value": ref_info["component_name"],
                        "secondary_value": str(target.get("in", "")),
                        "tertiary_value": "true" if target.get("required") else "false",
                        "description_label": "Description",
                        "description_value": str(target.get("description", "")),
                        "primary_state": "disabled",
                        "secondary_state": "readonly",
                        "secondary_editor": "combo",
                        "secondary_options": ["query", "header", "path", "cookie"],
                        "tertiary_state": "readonly",
                        "tertiary_editor": "combo",
                        "tertiary_options": ["true", "false"],
                        "description_state": "normal",
                        "apply_state": "normal",
                    }
                )
                return config
            config.update(
                {
                    "primary_label": "Name",
                    "secondary_label": "In",
                    "tertiary_label": "Required",
                    "primary_value": str(obj.get("name", "")),
                    "secondary_value": str(obj.get("in", "")),
                    "tertiary_value": "true" if obj.get("required") else "false",
                    "description_label": "Description",
                    "description_value": str(obj.get("description", "")),
                    "primary_state": "normal",
                    "secondary_state": "readonly",
                    "secondary_editor": "combo",
                    "secondary_options": ["query", "header", "path", "cookie"],
                    "tertiary_state": "readonly",
                    "tertiary_editor": "combo",
                    "tertiary_options": ["true", "false"],
                    "description_state": "normal",
                    "apply_state": "normal",
                }
            )
        elif kind == "request_body" and isinstance(obj, dict):
            ref_info = self._resolve_reference_info(obj)
            if ref_info:
                config.update(
                    {
                        "primary_label": "Component",
                        "secondary_label": "Reference",
                        "primary_value": ref_info["component_name"],
                        "secondary_value": ref_info["ref"],
                        "description_label": "Description",
                        "description_value": str(ref_info["payload"].get("description", "")),
                        "primary_state": "disabled",
                        "secondary_state": "disabled",
                        "description_state": "normal",
                        "apply_state": "normal",
                        "show_tertiary": False,
                    }
                )
                return config
            config.update(
                {
                    "primary_label": "$ref",
                    "secondary_label": "Required",
                    "tertiary_label": "Content Types",
                    "primary_value": str(obj.get("$ref", "")),
                    "secondary_value": "true" if obj.get("required") else "false",
                    "tertiary_value": ", ".join(sorted((obj.get("content") or {}).keys())),
                    "description_label": "Description",
                    "description_value": str(obj.get("description", "")),
                    "primary_state": "normal",
                    "secondary_state": "readonly",
                    "secondary_editor": "combo",
                    "secondary_options": ["true", "false"],
                    "tertiary_state": "disabled",
                    "description_state": "normal",
                    "apply_state": "normal",
                }
            )
        elif kind == "response" and isinstance(obj, dict):
            ref_info = self._resolve_reference_info(obj)
            if ref_info:
                config.update(
                    {
                        "primary_label": "Status Code",
                        "secondary_label": "Component",
                        "tertiary_label": "Reference",
                        "primary_value": self._response_code_for(obj),
                        "secondary_value": ref_info["component_name"],
                        "tertiary_value": ref_info["ref"],
                        "description_label": "Description",
                        "description_value": str(ref_info["payload"].get("description", "")),
                        "primary_state": "normal",
                        "secondary_state": "disabled",
                        "tertiary_state": "disabled",
                        "description_state": "normal",
                        "apply_state": "normal",
                    }
                )
                return config
            config.update(
                {
                    "primary_label": "Status Code",
                    "secondary_label": "Description",
                    "tertiary_label": "Content Types",
                    "primary_value": self._response_code_for(obj),
                    "secondary_value": str(obj.get("description", "")),
                    "tertiary_value": ", ".join(sorted((obj.get("content") or {}).keys())),
                    "description_label": "Description",
                    "description_value": str(obj.get("description", "")),
                    "primary_state": "normal",
                    "secondary_state": "normal",
                    "tertiary_state": "disabled",
                    "show_description": False,
                    "description_state": "normal",
                    "apply_state": "normal",
                }
            )
        elif kind == "release" and obj is not None:
            config.update(
                {
                    "primary_label": "Release Code",
                    "secondary_label": "Type",
                    "tertiary_label": "Status",
                    "primary_value": getattr(obj, "code", ""),
                    "secondary_value": getattr(obj, "release_type", ""),
                    "tertiary_value": getattr(obj, "status", ""),
                    "description_label": "Notes",
                    "description_value": getattr(obj, "notes", ""),
                    "primary_state": "normal",
                    "secondary_state": "normal",
                    "tertiary_state": "normal",
                    "description_state": "normal",
                    "apply_state": "normal",
                }
            )
        elif kind == "change" and obj is not None:
            config.update(
                {
                    "primary_label": "Title",
                    "secondary_label": "External Ref",
                    "tertiary_label": "Status",
                    "primary_value": getattr(obj, "title", ""),
                    "secondary_value": getattr(obj, "external_ref", ""),
                    "tertiary_value": getattr(obj, "status", ""),
                    "description_value": getattr(obj, "description", ""),
                    "primary_state": "normal",
                    "secondary_state": "normal",
                    "tertiary_state": "normal",
                    "description_state": "normal",
                    "apply_state": "normal",
                }
            )
        elif kind == "library" and obj is not None:
            config.update(
                {
                    "primary_label": "Library Name",
                    "primary_value": getattr(obj, "name", ""),
                    "description_label": "Description",
                    "description_value": "",
                    "primary_state": "normal",
                    "apply_state": "normal",
                    "description_state": "disabled",
                    "show_secondary": False,
                    "show_tertiary": False,
                    "show_description": False,
                }
            )
        elif kind == "component" and obj is not None:
            config.update(
                {
                    "primary_label": "Component Name",
                    "secondary_label": "Kind",
                    "primary_value": getattr(obj, "name", ""),
                    "secondary_value": getattr(obj, "component_kind", ""),
                    "description_label": "Description",
                    "description_value": "",
                    "primary_state": "normal",
                    "secondary_state": "normal",
                    "description_state": "disabled",
                    "apply_state": "normal",
                    "show_tertiary": False,
                    "show_description": False,
                }
            )
        elif kind == "change_step" and obj is not None:
            config.update(
                {
                    "primary_label": "Step Kind",
                    "secondary_label": "Target ID",
                    "tertiary_label": "Order",
                    "primary_value": getattr(obj, "kind", ""),
                    "secondary_value": getattr(obj, "target_id", ""),
                    "tertiary_value": str(getattr(obj, "order", "")),
                    "description_label": "Change Step Payload",
                    "description_value": self._payload_editor_text(kind, obj),
                    "show_description": True,
                    "description_state": "normal",
                    "apply_state": "normal",
                }
            )
        elif kind == "local_component" and obj is not None:
            config.update(
                {
                    "primary_label": "Component Name",
                    "secondary_label": "Kind",
                    "primary_value": obj.get("name", ""),
                    "secondary_value": obj.get("kind", ""),
                    "description_state": "disabled",
                    "apply_state": "normal",
                    "show_tertiary": False,
                    "show_description": False,
                }
            )
        elif kind == "shared_ref" and obj is not None:
            config.update(
                {
                    "primary_label": "Component ID",
                    "secondary_label": "Kind",
                    "tertiary_label": "Revision",
                    "primary_value": obj.get("component_id", ""),
                    "secondary_value": obj.get("component_kind", ""),
                    "tertiary_value": obj.get("adopted_revision_id", ""),
                    "description_state": "disabled",
                    "apply_state": "normal",
                    "show_description": False,
                }
            )
        elif kind in {"parameter_group", "response_group", "request_body_group", "callback_group", "webhook_group"}:
            config.update(
                {
                    "show_primary": False,
                    "show_secondary": False,
                    "show_tertiary": False,
                    "show_description": False,
                }
            )
        elif kind.endswith("_group") or kind in {"components", "shared_refs", "empty", "component_kind"}:
            config.update(
                {
                    "show_primary": False,
                    "show_secondary": False,
                    "show_tertiary": False,
                    "show_description": False,
                }
            )
        return config

    def _configure_editor(self, widget, state: str) -> None:
        widget.configure(state="normal")
        if state == "disabled":
            widget.configure(state="disabled")

    def _configure_field_slot(
        self,
        slot: str,
        editor_type: str,
        state: str,
        options: list[str],
    ) -> None:
        entry = getattr(self, f"entry_{slot}")
        combo = getattr(self, f"combo_{slot}")
        if editor_type == "combo":
            combo.configure(values=options or [""])
            combo.grid()
            entry.grid_remove()
            combo.configure(state=state)
        else:
            entry.grid()
            combo.grid_remove()
            self._configure_editor(entry, state)

    def _set_field_visibility(self, label_widget, value_widget, visible: bool) -> None:
        combo_widget = None
        if value_widget is self.entry_primary:
            combo_widget = self.combo_primary
        elif value_widget is self.entry_secondary:
            combo_widget = self.combo_secondary
        elif value_widget is self.entry_tertiary:
            combo_widget = self.combo_tertiary

        if visible:
            label_widget.grid()
            if value_widget.winfo_ismapped():
                value_widget.grid()
            elif combo_widget is not None and combo_widget.winfo_ismapped():
                combo_widget.grid()
        else:
            label_widget.grid_remove()
            value_widget.grid_remove()
            if combo_widget is not None:
                combo_widget.grid_remove()

    def _render_atomic_object(
        self,
        parent,
        value: dict[str, Any],
        path: tuple[Any, ...],
        *,
        template: Optional[str],
        ref_context: Optional[Dict[str, Any]] = None,
    ) -> None:
        if template == "schema":
            self._render_atomic_schema_object(parent, value, path, ref_context)
            return
        row = 0
        for key, child in self._iter_object_fields(value, template):
            child_mode, _, _ = self._child_meta_for_key(key, child)
            if child_mode != "scalar":
                continue
            if not self._should_render_value(child):
                continue
            self._render_dynamic_scalar(
                parent,
                row,
                key,
                child,
                path + (key,),
                ref_context=ref_context,
                ref_path=path + (key,),
                template_context=template,
            )
            row += 1

    def _render_atomic_schema_object(
        self,
        parent,
        value: dict[str, Any],
        path: tuple[Any, ...],
        ref_context: Optional[Dict[str, Any]],
    ) -> None:
        row = 0
        schema_mode = self._schema_mode(value)
        value["__schema_mode__"] = self._schema_mode_label(schema_mode)
        if self._is_edit_mode() or schema_mode != "simple":
            self._render_dynamic_scalar(parent, row, "schema_mode", value["__schema_mode__"], path + ("__schema_mode__",), ref_context=ref_context, ref_path=path + ("__schema_mode__",), template_context="schema")
            row += 1
        if schema_mode == "reference":
            self._render_dynamic_scalar(parent, row, "$ref", value.get("$ref", ""), path + ("$ref",), ref_context=ref_context, ref_path=path + ("$ref",), template_context="schema")
            return
        base_keys = ["title", "type", "description", "default"]
        schema_type = str(value.get("type", "") or "")
        if schema_type == "string":
            base_keys = ["title", "type", "format", "minLength", "maxLength", "pattern", "description", "default"]
        elif schema_type == "array":
            base_keys = ["title", "type", "minItems", "maxItems", "description", "default"]
        for key in base_keys:
            current_value = value.get(key, "")
            if not self._should_render_value(current_value):
                continue
            self._render_dynamic_scalar(parent, row, key, current_value, path + (key,), ref_context=ref_context, ref_path=path + (key,), template_context="schema")
            row += 1

    def _render_atomic_list(
        self,
        parent,
        value: list[Any],
        path: tuple[Any, ...],
        *,
        item_template: Optional[str],
    ) -> None:
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 4))
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            header,
            text=f"{len(value)} item" if len(value) == 1 else f"{len(value)} items",
            text_color="#5C6670",
        ).grid(row=0, column=0, sticky="w")
        for index, child in enumerate(value):
            row = index + 1
            ctk.CTkLabel(
                parent,
                text=self._collection_item_title(index, child, item_template),
                font=ctk.CTkFont(weight="bold"),
            ).grid(row=row, column=0, sticky="w", pady=2)
            if not isinstance(child, (dict, list)):
                self._render_dynamic_scalar(parent, row, "value", child, path + (index,), ref_path=path + (index,), template_context=item_template)

    def _render_atomic_map(
        self,
        parent,
        value: dict[str, Any],
        path: tuple[Any, ...],
        *,
        item_template: Optional[str],
    ) -> None:
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 4))
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            header,
            text=f"{len(value)} item" if len(value) == 1 else f"{len(value)} items",
            text_color="#5C6670",
        ).grid(row=0, column=0, sticky="w")
        row = 1
        for map_key, child in value.items():
            ctk.CTkLabel(
                parent,
                text=self._map_item_title(path, map_key),
                font=ctk.CTkFont(weight="bold"),
            ).grid(row=row, column=0, columnspan=2, sticky="w", pady=2)
            row += 1
            if not isinstance(child, (dict, list)):
                self._render_dynamic_scalar(parent, row, "value", child, path + (map_key,), ref_path=path + (map_key,), template_context=item_template)
                row += 1

    def _render_dynamic_object(
        self,
        parent,
        value: dict[str, Any],
        path: tuple[Any, ...],
        *,
        template: Optional[str],
        ref_context: Optional[Dict[str, Any]] = None,
    ) -> None:
        if template == "parameter":
            self._render_parameter_object(parent, value, path, ref_context)
            return
        if template == "media_type":
            self._render_media_type_object(parent, value, path, ref_context)
            return
        if template == "schema":
            self._render_schema_object(parent, value, path, ref_context)
            return
        row = 0
        for key, child in self._iter_object_fields(value, template):
            if not self._should_render_value(child):
                continue
            child_mode, child_template, child_item_template = self._child_meta_for_key(key, child)
            if isinstance(child, dict):
                ref_info = self._resolve_reference_info(child)
                if ref_info:
                    box, expanded = self._dynamic_section_box(
                        parent,
                        row,
                        f"{key}: {ref_info['component_name']}",
                        path + (key,),
                        default_expanded=True,
                        render_children=lambda target, child_key=key, payload=deepcopy(ref_info["payload"]), tmpl=child_template, ref=child, ref_meta=ref_info: self._render_dynamic_object(
                            target,
                            self._merge_template(payload, tmpl),
                            path + (child_key,),
                            template=tmpl,
                            ref_context={"ref_holder": ref, "ref_info": ref_meta},
                        ),
                    )
                elif child_mode == "map":
                    box, expanded = self._dynamic_section_box(
                        parent,
                        row,
                        key,
                        path + (key,),
                        default_expanded=self._section_default_expanded(key, child),
                        render_children=lambda target, payload=child, child_key=key, item_tmpl=child_item_template: self._render_dynamic_map(
                            target,
                            payload,
                            path + (child_key,),
                            item_template=item_tmpl,
                            ref_context=ref_context,
                            show_add_button=True,
                        ),
                    )
                else:
                    box, expanded = self._dynamic_section_box(
                        parent,
                        row,
                        key,
                        path + (key,),
                        default_expanded=self._section_default_expanded(key, child),
                        render_children=lambda target, payload=child, child_key=key, tmpl=child_template: self._render_dynamic_object(
                            target,
                            self._merge_template(payload, tmpl),
                            path + (child_key,),
                            template=tmpl,
                            ref_context=ref_context,
                        ),
                    )
            elif isinstance(child, list):
                box, expanded = self._dynamic_section_box(
                    parent,
                    row,
                    key,
                    path + (key,),
                    default_expanded=self._section_default_expanded(key, child),
                    render_children=lambda target, payload=child, child_key=key, item_tmpl=child_item_template: self._render_dynamic_list(
                        target,
                        payload,
                        path + (child_key,),
                        item_template=item_tmpl,
                        ref_context=ref_context,
                        show_add_button=True,
                    ),
                )
            else:
                self._render_dynamic_scalar(
                    parent,
                    row,
                    key,
                    child,
                    path + (key,),
                    ref_context=ref_context,
                    ref_path=path + (key,),
                    template_context=template,
                )
            row += 1

    def _render_parameter_object(
        self,
        parent,
        value: dict[str, Any],
        path: tuple[Any, ...],
        ref_context: Optional[Dict[str, Any]],
    ) -> None:
        row = 0
        for key in ("name", "in", "description", "required"):
            current_value = value.get(key, "" if key != "required" else False)
            if not self._should_render_value(current_value):
                continue
            self._render_dynamic_scalar(
                parent,
                row,
                key,
                current_value,
                path + (key,),
                ref_context=ref_context,
                ref_path=path + (key,),
                template_context="parameter",
            )
            row += 1
        schema_payload = value.get("schema") if isinstance(value.get("schema"), dict) else {}
        if self._should_render_value(schema_payload):
            box, _expanded = self._dynamic_section_box(
                parent,
                row,
                "Schema",
                path + ("schema",),
                default_expanded=False,
                render_children=lambda target, payload=schema_payload: self._render_schema_object(
                    target,
                    self._merge_template(payload, "schema") if self._is_edit_mode() else payload,
                    path + ("schema",),
                    ref_context,
                ),
            )
            row += 1
        if value.get("example", "") not in ("", None):
            self._render_dynamic_scalar(
                parent,
                row,
                "example",
                value.get("example", ""),
                path + ("example",),
                ref_context=ref_context,
                ref_path=path + ("example",),
                template_context="parameter",
            )
            row += 1
        advanced_payload = {key: value.get(key) for key in ("deprecated", "allowEmptyValue", "style", "explode", "allowReserved")}
        if self._should_render_value(advanced_payload):
            box, _expanded = self._dynamic_section_box(
                parent,
                row,
                "Advanced",
                path + ("advanced",),
                default_expanded=False,
                render_children=lambda target, payload=advanced_payload: self._render_parameter_advanced(
                    target,
                    payload,
                    path,
                    ref_context,
                ),
            )

    def _render_parameter_advanced(
        self,
        parent,
        value: dict[str, Any],
        path: tuple[Any, ...],
        ref_context: Optional[Dict[str, Any]],
    ) -> None:
        row = 0
        for key in ("deprecated", "allowEmptyValue", "style", "explode", "allowReserved"):
            current_value = value.get(key, False if key != "style" else "")
            if not self._should_render_value(current_value):
                continue
            self._render_dynamic_scalar(
                parent,
                row,
                key,
                current_value,
                path + (key,),
                ref_context=ref_context,
                ref_path=path + (key,),
                template_context="parameter",
            )
            row += 1

    def _render_media_type_object(
        self,
        parent,
        value: dict[str, Any],
        path: tuple[Any, ...],
        ref_context: Optional[Dict[str, Any]],
    ) -> None:
        row = 0
        schema_payload = value.get("schema") if isinstance(value.get("schema"), dict) else {}
        if self._should_render_value(schema_payload):
            self._dynamic_section_box(
                parent,
                row,
                "Schema",
                path + ("schema",),
                default_expanded=True,
                render_children=lambda target, payload=schema_payload: self._render_schema_object(
                    target,
                    self._merge_template(payload, "schema") if self._is_edit_mode() else payload,
                    path + ("schema",),
                    ref_context,
                ),
            )
            row += 1
        example_value = value.get("example", "")
        if self._should_render_value(example_value):
            self._render_dynamic_scalar(
                parent,
                row,
                "example",
                example_value,
                path + ("example",),
                ref_context=ref_context,
                ref_path=path + ("example",),
                template_context="media_type",
            )
            row += 1
        for key in ("examples", "encoding"):
            child = value.get(key, {} if key == "encoding" else {})
            if not self._should_render_value(child):
                continue
            child_mode, child_template, child_item_template = self._child_meta_for_key(key, child)
            if child_mode == "map":
                self._dynamic_section_box(
                    parent,
                    row,
                    key,
                    path + (key,),
                    default_expanded=False,
                    render_children=lambda target, payload=child, child_key=key, item_tmpl=child_item_template: self._render_dynamic_map(
                        target,
                        payload,
                        path + (child_key,),
                        item_template=item_tmpl,
                        ref_context=ref_context,
                        show_add_button=True,
                    ),
                )
            else:
                self._dynamic_section_box(
                    parent,
                    row,
                    key,
                    path + (key,),
                    default_expanded=False,
                    render_children=lambda target, payload=child, child_key=key, tmpl=child_template: self._render_dynamic_object(
                        target,
                        self._merge_template(payload, tmpl) if self._is_edit_mode() else payload,
                        path + (child_key,),
                        template=tmpl,
                        ref_context=ref_context,
                    ),
                )
            row += 1

    def _render_schema_object(
        self,
        parent,
        value: dict[str, Any],
        path: tuple[Any, ...],
        ref_context: Optional[Dict[str, Any]],
    ) -> None:
        row = 0
        schema_mode = self._schema_mode(value)
        value["__schema_mode__"] = self._schema_mode_label(schema_mode)
        if self._is_edit_mode() or schema_mode != "simple":
            self._render_dynamic_scalar(
                parent,
                row,
                "schema_mode",
                value["__schema_mode__"],
                path + ("__schema_mode__",),
                ref_context=ref_context,
                ref_path=path + ("__schema_mode__",),
                template_context="schema",
            )
            row += 1

        if schema_mode == "reference":
            self._render_dynamic_scalar(
                parent,
                row,
                "$ref",
                value.get("$ref", ""),
                path + ("$ref",),
                ref_context=ref_context,
                ref_path=path + ("$ref",),
                template_context="schema",
            )
            row += 1
            resolved_ref = self._resolve_reference_info(value)
            if resolved_ref:
                self._dynamic_section_box(
                    parent,
                    row,
                    "Referenced Schema",
                    path + ("$ref", "resolved"),
                    default_expanded=False,
                    render_children=lambda target, payload=deepcopy(resolved_ref["payload"]), context=resolved_ref: self._render_schema_object(
                        target,
                        self._merge_template(payload, "schema"),
                        path + ("$ref", "resolved"),
                        {"ref_holder": value, "ref_info": context},
                    ),
                )
            return

        for key in ("title", "type"):
            current_value = value.get(key, "")
            if not self._should_render_value(current_value):
                continue
            self._render_dynamic_scalar(
                parent,
                row,
                key,
                current_value,
                path + (key,),
                ref_context=ref_context,
                ref_path=path + (key,),
                template_context="schema",
            )
            row += 1
        schema_type = str(value.get("type", "") or "")
        if schema_mode == "simple" and schema_type == "string":
            for key in ("format", "minLength", "maxLength", "pattern"):
                current_value = value.get(key, "")
                if not self._should_render_value(current_value):
                    continue
                self._render_dynamic_scalar(
                    parent,
                    row,
                    key,
                    current_value,
                    path + (key,),
                    ref_context=ref_context,
                    ref_path=path + (key,),
                    template_context="schema",
                )
                row += 1
        if schema_mode == "simple" and schema_type == "array":
            for key in ("minItems", "maxItems"):
                current_value = value.get(key, "")
                if not self._should_render_value(current_value):
                    continue
                self._render_dynamic_scalar(
                    parent,
                    row,
                    key,
                    current_value,
                    path + (key,),
                    ref_context=ref_context,
                    ref_path=path + (key,),
                    template_context="schema",
                )
                row += 1
        for key in ("description", "default"):
            current_value = value.get(key, "")
            if not self._should_render_value(current_value):
                continue
            self._render_dynamic_scalar(
                parent,
                row,
                key,
                current_value,
                path + (key,),
                ref_context=ref_context,
                ref_path=path + (key,),
                template_context="schema",
            )
            row += 1
        enum_value = value.get("enum")
        show_enum = (
            schema_mode == "simple"
            and isinstance(enum_value, list)
            and (
                len(enum_value) > 0
                or schema_type in {"string", "number", "integer", "boolean"}
            )
        )
        if show_enum:
            self._dynamic_section_box(
                parent,
                row,
                "Enum",
                path + ("enum",),
                default_expanded=False,
                render_children=lambda target, payload=value.get("enum", []): self._render_dynamic_list(
                    target,
                    payload,
                    path + ("enum",),
                    item_template=None,
                    ref_context=ref_context,
                    show_add_button=True,
                ),
            )
            row += 1
        if schema_mode == "simple":
            self._render_schema_composition(parent, value, path, ref_context, row)
            return
        composition_key = self._schema_mode_composition_key(schema_mode)
        if composition_key:
            self._dynamic_section_box(
                parent,
                row,
                composition_key,
                path + (composition_key,),
                default_expanded=True,
                render_children=lambda target, payload=value.get(composition_key, []), child_key=composition_key: self._render_dynamic_list(
                    target,
                    payload,
                    path + (child_key,),
                    item_template="schema",
                    ref_context=ref_context,
                    show_add_button=True,
                ),
            )

    def _render_schema_composition(
        self,
        parent,
        value: dict[str, Any],
        path: tuple[Any, ...],
        ref_context: Optional[Dict[str, Any]],
        start_row: int = 0,
    ) -> None:
        row = start_row
        schema_type = str(value.get("type", "") or "")
        visible_keys: list[str] = []
        if schema_type == "object":
            visible_keys.extend(["properties", "required"])
        if schema_type == "array":
            visible_keys.append("items")
        for key in visible_keys:
            child = value.get(key, {} if key in {"properties", "items"} else [])
            if not self._should_render_value(child):
                continue
            if isinstance(child, dict):
                self._dynamic_section_box(
                    parent,
                    row,
                    key,
                    path + (key,),
                    default_expanded=False,
                    render_children=lambda target, payload=child, child_key=key: self._render_dynamic_map(
                        target,
                        payload,
                        path + (child_key,),
                        item_template="schema" if child_key == "properties" else None,
                        ref_context=ref_context,
                        show_add_button=True,
                    ),
                )
            else:
                self._dynamic_section_box(
                    parent,
                    row,
                    key,
                    path + (key,),
                    default_expanded=False,
                    render_children=lambda target, payload=child, child_key=key: self._render_dynamic_list(
                        target,
                        payload,
                        path + (child_key,),
                        item_template="schema" if child_key in {"allOf", "anyOf", "oneOf"} else None,
                        ref_context=ref_context,
                        show_add_button=True,
                    ),
                )
            row += 1

    def _dynamic_section_box(
        self,
        parent,
        row: int,
        label: str,
        path: tuple[Any, ...],
        default_expanded: bool = True,
        render_children: Optional[Callable[[Any], None]] = None,
    ) -> tuple[Any, bool]:
        wrapper = ctk.CTkFrame(parent, fg_color="transparent")
        wrapper.grid(
            row=row,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(4, 2),
            padx=(self._inspector_indent(path), 0),
        )
        wrapper.grid_columnconfigure(1, weight=1)
        expanded = self._ensure_section_expansion_state(path, default_expanded)
        toggle = ctk.CTkButton(
            wrapper,
            text=self._section_toggle_symbol(expanded),
            width=20,
            height=20,
            corner_radius=3,
            fg_color="transparent",
            border_width=1,
            border_color="#7F8A93",
            hover_color=("gray88", "gray24"),
            text_color=PETROL,
        )
        toggle.grid(row=0, column=0, sticky="w", pady=(0, 2), padx=(0, 6))
        title = ctk.CTkLabel(
            wrapper,
            text=self._display_label(label),
            font=ctk.CTkFont(weight="bold"),
            text_color=PETROL,
        )
        title.grid(row=0, column=1, sticky="w", pady=(0, 2))
        body = ctk.CTkFrame(wrapper, fg_color="transparent")
        if expanded:
            body.grid(row=1, column=0, columnspan=2, sticky="ew")
            if render_children is not None:
                render_children(body)
        body.grid_columnconfigure(1, weight=1)
        def toggle_section(_event=None):
            current = self._section_expansion_state.get(path, default_expanded)
            next_value = not current
            self._section_expansion_state[path] = next_value
            toggle.configure(text=self._section_toggle_symbol(next_value))
            if next_value:
                body.grid(row=1, column=0, columnspan=2, sticky="ew")
                if render_children is not None and not body.winfo_children():
                    render_children(body)
            else:
                body.grid_remove()
        toggle.configure(command=toggle_section)
        title.bind("<Button-1>", toggle_section)
        return body, expanded

    def _render_dynamic_list(
        self,
        parent,
        value: list[Any],
        path: tuple[Any, ...],
        *,
        item_template: Optional[str],
        ref_context: Optional[Dict[str, Any]] = None,
        show_add_button: bool = False,
    ) -> None:
        start_row = 0
        if show_add_button:
            header = ctk.CTkFrame(parent, fg_color="transparent")
            header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 4))
            header.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(
                header,
                text=f"{len(value)} item" if len(value) == 1 else f"{len(value)} items",
                text_color="#5C6670",
            ).grid(row=0, column=0, sticky="w")
            if self._is_edit_mode():
                ctk.CTkButton(
                    header,
                    text="+ Add",
                    width=68,
                    height=26,
                    corner_radius=5,
                    command=lambda p=path, template=item_template: self._dynamic_add_item(p, "list", template),
                ).grid(row=0, column=1, sticky="e")
            start_row = 1
        for index, child in enumerate(value):
            card = ctk.CTkFrame(parent, corner_radius=5, fg_color=("gray92", "gray20"))
            card.grid(
                row=start_row + index,
                column=0,
                columnspan=2,
                sticky="ew",
                pady=2,
                padx=(self._inspector_indent(path), 0),
            )
            card.grid_columnconfigure(0, weight=1)
            head = ctk.CTkFrame(card, fg_color="transparent")
            head.grid(row=0, column=0, sticky="ew", padx=8, pady=(6, 2))
            head.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(
                head,
                text=self._collection_item_title(index, child, item_template),
                font=ctk.CTkFont(weight="bold"),
            ).grid(row=0, column=0, sticky="w")
            ctk.CTkButton(
                head,
                text="🗑",
                width=28,
                height=28,
                corner_radius=6,
                fg_color="transparent",
                text_color=PETROL,
                hover_color=("gray84", "gray28"),
                command=lambda p=path, i=index: self._dynamic_remove_item(p, i),
                state="normal" if self._is_edit_mode() else "disabled",
            ).grid(row=0, column=1, sticky="e")
            body = ctk.CTkFrame(card, fg_color="transparent")
            body.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 6))
            body.grid_columnconfigure(1, weight=1)
            if isinstance(child, dict):
                ref_info = self._resolve_reference_info(child)
                if ref_info:
                    self._render_dynamic_object(
                        body,
                        self._merge_template(deepcopy(ref_info["payload"]), item_template) if self._is_edit_mode() else deepcopy(ref_info["payload"]),
                        path + (index,),
                        template=item_template,
                        ref_context={"ref_holder": child, "ref_info": ref_info},
                    )
                else:
                    self._render_dynamic_object(
                        body,
                        self._merge_template(child, item_template) if self._is_edit_mode() else child,
                        path + (index,),
                        template=item_template,
                        ref_context=ref_context,
                    )
            elif isinstance(child, list):
                self._render_dynamic_list(
                    body,
                    child,
                    path + (index,),
                    item_template=item_template,
                    ref_context=ref_context,
                    show_add_button=True,
                )
            else:
                self._render_dynamic_scalar(
                    body,
                    0,
                    "value",
                    child,
                    path + (index,),
                    ref_context=ref_context,
                    ref_path=path + (index,),
                )

    def _render_dynamic_map(
        self,
        parent,
        value: dict[str, Any],
        path: tuple[Any, ...],
        *,
        item_template: Optional[str],
        ref_context: Optional[Dict[str, Any]] = None,
        show_add_button: bool = False,
    ) -> None:
        start_row = 0
        if show_add_button:
            header = ctk.CTkFrame(parent, fg_color="transparent")
            header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 4))
            header.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(
                header,
                text=f"{len(value)} item" if len(value) == 1 else f"{len(value)} items",
                text_color="#5C6670",
            ).grid(row=0, column=0, sticky="w")
            if self._is_edit_mode():
                ctk.CTkButton(
                    header,
                    text="+ Add",
                    width=68,
                    height=26,
                    corner_radius=5,
                    command=lambda p=path, template=item_template: self._dynamic_add_item(p, "map", template),
                ).grid(row=0, column=1, sticky="e")
            start_row = 1
        for row_index, (map_key, child) in enumerate(value.items()):
            card = ctk.CTkFrame(parent, corner_radius=5, fg_color=("gray92", "gray20"))
            card.grid(
                row=start_row + row_index,
                column=0,
                columnspan=2,
                sticky="ew",
                pady=2,
                padx=(self._inspector_indent(path), 0),
            )
            card.grid_columnconfigure(1, weight=1)
            title = ctk.CTkFrame(card, fg_color="transparent")
            title.grid(row=0, column=0, columnspan=3, sticky="ew", padx=8, pady=(6, 2))
            title.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(
                title,
                text=self._map_item_title(path, map_key),
                font=ctk.CTkFont(weight="bold"),
            ).grid(row=0, column=0, sticky="w")
            ctk.CTkButton(
                title,
                text="🗑",
                width=28,
                height=28,
                corner_radius=6,
                fg_color="transparent",
                text_color=PETROL,
                hover_color=("gray84", "gray28"),
                command=lambda p=path, k=map_key: self._dynamic_remove_map_item(p, k),
                state="normal" if self._is_edit_mode() else "disabled",
            ).grid(row=0, column=1, sticky="e")
            body = ctk.CTkFrame(card, fg_color="transparent")
            body.grid(row=1, column=0, columnspan=3, sticky="ew", padx=8, pady=(0, 6))
            body.grid_columnconfigure(1, weight=1)
            key_var = tk.StringVar(value=str(map_key))
            child_parent = body
            if self._is_edit_mode():
                ctk.CTkLabel(body, text=self._map_key_editor_label(path)).grid(row=0, column=0, sticky="w", padx=(0, 8))
                key_entry = ctk.CTkEntry(body, textvariable=key_var)
                key_entry.grid(row=0, column=1, sticky="ew")
                self._dynamic_bindings.append(
                    {
                        "binding_type": "map_key",
                        "path": path,
                        "original_key": map_key,
                        "var": key_var,
                    }
                )
                child_parent = ctk.CTkFrame(body, fg_color="transparent")
                child_parent.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(6, 0))
                child_parent.grid_columnconfigure(1, weight=1)
            if isinstance(child, dict):
                ref_info = self._resolve_reference_info(child)
                if ref_info:
                    self._render_dynamic_object(
                        child_parent,
                        self._merge_template(deepcopy(ref_info["payload"]), item_template) if self._is_edit_mode() else deepcopy(ref_info["payload"]),
                        path + (map_key,),
                        template=item_template,
                        ref_context={"ref_holder": child, "ref_info": ref_info},
                    )
                else:
                    self._render_dynamic_object(
                        child_parent,
                        self._merge_template(child, item_template) if self._is_edit_mode() else child,
                        path + (map_key,),
                        template=item_template,
                        ref_context=ref_context,
                    )
            elif isinstance(child, list):
                self._render_dynamic_list(
                    child_parent,
                    child,
                    path + (map_key,),
                    item_template=item_template,
                    ref_context=ref_context,
                    show_add_button=True,
                )
            else:
                self._render_dynamic_scalar(
                    child_parent,
                    0,
                    "value",
                    child,
                    path + (map_key,),
                    ref_context=ref_context,
                    ref_path=path + (map_key,),
                )

    def _render_dynamic_scalar(
        self,
        parent,
        row: int,
        label: str,
        value: Any,
        path: tuple[Any, ...],
        ref_context: Optional[Dict[str, Any]] = None,
        ref_path: tuple[Any, ...] = (),
        template_context: Optional[str] = None,
    ) -> None:
        ctk.CTkLabel(parent, text=self._display_label(label)).grid(
            row=row,
            column=0,
            sticky="w",
            padx=(0, 8),
            pady=2,
        )
        options = self._value_field_options(
            {
                "label": label,
                "value": value,
                "path": path,
                "template_context": template_context,
            }
        )
        if isinstance(value, bool):
            variable = tk.BooleanVar(value=value)
            widget = ctk.CTkCheckBox(parent, text="", variable=variable, onvalue=True, offvalue=False)
            if not self._is_edit_mode():
                widget.configure(state="disabled")
        elif options:
            variable = tk.StringVar(value=self._format_scalar_value(value))
            widget_state = "readonly" if self._is_edit_mode() else "disabled"
            widget = ctk.CTkComboBox(parent, variable=variable, values=options, state=widget_state, height=28)
        else:
            variable = tk.StringVar(value=self._format_scalar_value(value))
            widget = ctk.CTkEntry(parent, textvariable=variable, height=28)
            if not self._is_edit_mode():
                widget.configure(state="disabled")
        widget.grid(row=row, column=1, sticky="ew", pady=2)
        self._dynamic_bindings.append(
            {
                "binding_type": "scalar",
                "path": path,
                "ref_path": ref_path,
                "var": variable,
                "original": value,
                "ref_context": ref_context,
            }
        )

    def _binding_value(self, binding: Dict[str, Any]) -> Any:
        original = binding["original"]
        raw_value = binding["var"].get()
        if isinstance(original, bool):
            return bool(raw_value)
        if isinstance(raw_value, str):
            return self._parse_scalar_value(original, raw_value.strip())
        return raw_value

    def _dynamic_add_item(self, path: tuple[Any, ...], mode: str, template: Optional[str]) -> None:
        target = self._get_nested(self._dynamic_working_copy, path)
        if mode == "list":
            if not isinstance(target, list):
                return
            target.append(self._new_collection_item(path, target, template))
        elif mode == "map":
            if not isinstance(target, dict):
                return
            new_key = self._prompt_map_key(self._map_key_label(path))
            if not new_key:
                return
            if new_key in target:
                messagebox.showerror(
                    "Duplicate Entry",
                    f"An item named '{new_key}' already exists.",
                    parent=self.master.winfo_toplevel(),
                )
                return
            target[new_key] = self._new_map_item(path, template)
        self._rerender_dynamic_editor()

    def _dynamic_remove_item(self, path: tuple[Any, ...], index: int) -> None:
        target = self._get_nested(self._dynamic_working_copy, path)
        if not isinstance(target, list) or index >= len(target):
            return
        target.pop(index)
        self._rerender_dynamic_editor()

    def _dynamic_remove_map_item(self, path: tuple[Any, ...], map_key: str) -> None:
        target = self._get_nested(self._dynamic_working_copy, path)
        if not isinstance(target, dict) or map_key not in target:
            return
        target.pop(map_key)
        self._rerender_dynamic_editor()

    def _rerender_dynamic_editor(self) -> None:
        if not self._dynamic_meta:
            return
        self._render_dynamic_section(self._dynamic_meta)

    def _get_nested(self, value: Any, path: tuple[Any, ...]) -> Any:
        target = value
        for segment in path:
            target = target[segment]
        return target

    def _new_collection_item(self, path: tuple[Any, ...], target: list[Any], template: Optional[str]) -> Any:
        if template:
            return deepcopy(SECTION_TEMPLATES.get(template, {}))
        if target:
            sample = target[0]
            if isinstance(sample, dict):
                return {key: "" if not isinstance(val, bool) else False for key, val in sample.items()}
            if isinstance(sample, list):
                return []
            return ""
        return ""

    def _new_map_item(self, path: tuple[Any, ...], template: Optional[str]) -> Any:
        if template:
            return deepcopy(SECTION_TEMPLATES.get(template, {}))
        label = str(path[-1]) if path else ""
        if label == "responses":
            return deepcopy(SECTION_TEMPLATES["response"])
        if label == "content":
            return deepcopy(SECTION_TEMPLATES["media_type"])
        if label == "headers":
            return deepcopy(SECTION_TEMPLATES["header"])
        if label == "links":
            return deepcopy(SECTION_TEMPLATES["link"])
        if label == "examples":
            return deepcopy(SECTION_TEMPLATES["example"])
        if label == "variables":
            return deepcopy(SECTION_TEMPLATES["server_variable"])
        if label in {"properties", "schemas"}:
            return deepcopy(SECTION_TEMPLATES["schema"])
        return {}

    def _section_default_expanded(self, key: str, value: Any) -> bool:
        if key in {"schema", "properties", "items", "content", "headers", "links", "examples", "encoding", "allOf", "anyOf", "oneOf", "enum"}:
            return False
        if key in {"externalDocs", "variables"} and self._is_empty_section_value(value):
            return False
        return True

    def _ensure_section_expansion_state(self, path: tuple[Any, ...], default_expanded: bool) -> bool:
        if path not in self._section_expansion_state:
            self._section_expansion_state[path] = default_expanded
        return self._section_expansion_state[path]

    def _section_toggle_symbol(self, expanded: bool) -> str:
        return "-" if expanded else "+"

    def _is_empty_section_value(self, value: Any) -> bool:
        if isinstance(value, dict):
            return not any(child not in ("", None, [], {}) for child in value.values())
        if isinstance(value, list):
            return len(value) == 0
        return value in ("", None)

    def _iter_object_fields(self, value: dict[str, Any], template: Optional[str]) -> list[tuple[str, Any]]:
        ordered_keys: list[str] = []
        template_payload = SECTION_TEMPLATES.get(template, {})
        if isinstance(template_payload, dict):
            ordered_keys.extend(template_payload.keys())
        for key in value.keys():
            if key not in ordered_keys:
                ordered_keys.append(key)
        return [(key, value.get(key)) for key in ordered_keys]

    def _child_meta_for_key(self, key: str, value: Any) -> tuple[str, Optional[str], Optional[str]]:
        if key == "contact":
            return "object", "contact", None
        if key == "license":
            return "object", "license", None
        if key == "externalDocs":
            return "object", "external_docs", None
        if key == "servers":
            return "list", None, "server"
        if key == "tags":
            return "list", None, "tag"
        if key == "security":
            return "list", None, "security_requirement"
        if key == "parameters":
            return "list", None, "parameter"
        if key == "requestBody":
            return "object", "request_body", None
        if key == "responses":
            return "map", None, "response"
        if key == "content":
            return "map", None, "media_type"
        if key == "headers":
            return "map", None, "header"
        if key == "links":
            return "map", None, "link"
        if key == "examples":
            return "map", None, "example"
        if key == "variables":
            return "map", None, "server_variable"
        if key == "encoding":
            return "map", None, "encoding"
        if key == "properties":
            return "map", None, "schema"
        if key == "callbacks":
            return "map", None, "path_item"
        if key == "schema":
            return "object", "schema", None
        if key in {"allOf", "anyOf", "oneOf"}:
            return "list", None, "schema"
        if isinstance(value, list):
            return "list", None, None
        if isinstance(value, dict):
            if key in MAP_SECTION_KEYS:
                return "map", None, None
            return "object", None, None
        return "scalar", None, None

    def _always_visible_tree_children(self, template: Optional[str], payload: dict[str, Any]) -> list[str]:
        if "$ref" in payload:
            return []
        if template == "request_body":
            return ["content"]
        if template == "media_type":
            return ["schema"]
        if template == "parameter":
            return ["schema"]
        if template == "response":
            return ["content", "headers", "links"]
        if template == "info":
            return ["contact", "license"]
        if template == "server":
            url = str(payload.get("url", "") or "")
            return ["variables"] if "{" in url and "}" in url else []
        if template == "schema":
            schema_mode = self._schema_mode(payload)
            if schema_mode == "reference":
                return []
            if schema_mode != "simple":
                composition_key = self._schema_mode_composition_key(schema_mode)
                return [composition_key] if composition_key else []
            schema_type = str(payload.get("type", "") or "")
            if schema_type == "object":
                return ["properties"]
            if schema_type == "array":
                return ["items"]
        return []

    def _tree_child_should_exist(
        self,
        key: str,
        child: Any,
        template: Optional[str],
        child_mode: str,
        payload: dict[str, Any],
    ) -> bool:
        if key in self._always_visible_tree_children(template, payload):
            return True
        if isinstance(child, dict):
            return len(child) > 0 and child_mode in {"object", "map"}
        if isinstance(child, list):
            return len(child) > 0
        return False

    def _default_structural_value(
        self,
        key: str,
        child_mode: str,
        child_template: Optional[str],
    ) -> Any:
        if key == "schema":
            return deepcopy(SECTION_TEMPLATES["schema"])
        if child_template:
            template_payload = deepcopy(SECTION_TEMPLATES.get(child_template, {}))
            if template_payload not in (None, {}):
                return template_payload
        if child_mode == "list":
            return []
        return {}

    def _apply_map_key_renames(self) -> bool:
        rename_bindings = [binding for binding in self._dynamic_bindings if binding.get("binding_type") == "map_key"]
        rename_bindings.sort(key=lambda item: len(item.get("path", ())), reverse=True)
        for binding in rename_bindings:
            target = self._get_nested(self._dynamic_working_copy, binding["path"])
            if not isinstance(target, dict):
                continue
            old_key = binding["original_key"]
            new_key = binding["var"].get().strip()
            if not new_key or new_key == old_key:
                continue
            if new_key in target:
                messagebox.showerror(
                    "Duplicate Entry",
                    f"An item named '{new_key}' already exists.",
                    parent=self.master.winfo_toplevel(),
                )
                return False
            self._rename_map_key(target, old_key, new_key)
        return True

    def _rename_map_key(self, target: dict[str, Any], old_key: str, new_key: str) -> None:
        rebuilt: dict[str, Any] = {}
        for key, value in target.items():
            rebuilt[new_key if key == old_key else key] = value
        target.clear()
        target.update(rebuilt)

    def _prune_empty_values(self, value: Any) -> Any:
        if isinstance(value, dict):
            cleaned: dict[str, Any] = {}
            for key, child in value.items():
                pruned = self._prune_empty_values(child)
                if pruned in ("", None, [], {}):
                    continue
                cleaned[key] = pruned
            return cleaned
        if isinstance(value, list):
            cleaned_list = [self._prune_empty_values(item) for item in value]
            return [item for item in cleaned_list if item not in ("", None, [], {})]
        return value

    def _map_key_label(self, path: tuple[Any, ...]) -> str:
        label = str(path[-1]) if path else "Name"
        if label == "responses":
            return "Status Code"
        if label == "content":
            return "Media Type"
        if label == "headers":
            return "Header"
        if label == "properties":
            return "Property"
        if label == "variables":
            return "Variable"
        if label == "callbacks":
            return "Callback"
        return "Name"

    def _map_key_editor_label(self, path: tuple[Any, ...]) -> str:
        label = str(path[-1]) if path else "Name"
        if label == "content":
            return "Media Type"
        if label == "properties":
            return "Property Name"
        return self._map_key_label(path)

    def _map_item_title(self, path: tuple[Any, ...], map_key: str) -> str:
        item_label = self._map_key_label(path)
        return f"{item_label}: {map_key}"

    def _prompt_map_key(self, label: str) -> Optional[str]:
        dialog = ctk.CTkInputDialog(text=f"{label}:", title=f"Add {label}")
        value = dialog.get_input()
        if value is None:
            return None
        value = value.strip()
        return value or None

    def _template_for_component_kind(self, kind: str) -> Optional[str]:
        mapping = {
            "schemas": "schema",
            "parameters": "parameter",
            "responses": "response",
            "requestBodies": "request_body",
            "headers": "header",
            "examples": "example",
            "links": "link",
            "callbacks": "path_item",
        }
        return mapping.get(kind)

    def _build_operation_details_payload(self, operation: OperationModel) -> Dict[str, Any]:
        payload = {
            "summary": operation.summary,
            "description": operation.description,
            "tags": deepcopy(operation.tags),
            "security": deepcopy(operation.security),
            "servers": deepcopy(operation.servers),
            "externalDocs": deepcopy(operation.external_docs),
        }
        if operation.deprecated is not None:
            payload["deprecated"] = operation.deprecated
        payload.update(deepcopy(operation.extensions))
        payload.update(deepcopy(operation.extra_fields))
        return payload

    def _commit_operation_details(self, operation: OperationModel, payload: Dict[str, Any]) -> None:
        known_keys = {"summary", "description", "tags", "security", "servers", "externalDocs", "deprecated"}
        operation.summary = str(payload.get("summary", ""))
        operation.description = str(payload.get("description", ""))
        operation.tags = deepcopy(payload.get("tags", []))
        operation.security = deepcopy(payload.get("security", []))
        operation.servers = deepcopy(payload.get("servers", []))
        operation.external_docs = deepcopy(payload.get("externalDocs", {}))
        operation.deprecated = payload.get("deprecated") if "deprecated" in payload else None
        operation.extensions = {key: deepcopy(value) for key, value in payload.items() if key.startswith("x-")}
        operation.extra_fields = {
            key: deepcopy(value)
            for key, value in payload.items()
            if key not in known_keys and not key.startswith("x-")
        }

    def _commit_request_body(self, operation: OperationModel, payload: Dict[str, Any]) -> None:
        operation.request_body = deepcopy(payload)

    def _build_callbacks_payload(self, operation: OperationModel) -> Dict[str, Any]:
        return {callback.path: callback.to_oas_path_item() for callback in operation.callbacks}

    def _commit_callbacks(self, operation: OperationModel, payload: Dict[str, Any]) -> None:
        callbacks: list[PathItemModel] = []
        for callback_path, callback_payload in payload.items():
            imported = self._import_path_payload(callback_path, callback_payload)
            callbacks.append(PathItemModel.from_dict({"path": callback_path, **imported}))
        operation.callbacks = callbacks

    def _commit_shared_component_payload(self, shared_ref: dict, payload: Dict[str, Any]) -> None:
        library_id = shared_ref.get("library_id")
        component_id = shared_ref.get("component_id")
        for library in self.workspace.shared_libraries:
            if library.id != library_id:
                continue
            for component in library.components:
                if component.id == component_id:
                    component.payload = deepcopy(payload)
                    return

    def _details_for(self, kind: str, obj: Any) -> str:
        payload = self._payload_for(kind, obj)
        if payload is not None:
            return yaml.safe_dump(payload, sort_keys=False, allow_unicode=True).strip()
        if kind == "workspace":
            return (
                f"APIs: {len(self.workspace.apis)}\n"
                f"Shared libraries: {len(self.workspace.shared_libraries)}\n"
                f"Metadata definitions: {len(self.workspace.metadata_catalog)}\n"
                f"Releases: {len(self.workspace.release_catalog)}\n"
                f"Changes: {len(self.workspace.changes)}"
            )
        if kind == "api" and isinstance(obj, ApiModel):
            local_component_total = sum(
                len(component_map)
                for component_map in obj.local_components.values()
                if isinstance(component_map, dict)
            )
            return (
                f"Servers: {len(obj.servers)}\n"
                f"Tags: {len(obj.tags)}\n"
                f"Paths: {len(obj.path_items)}\n"
                f"Operations: {sum(len(path_item.operations) for path_item in obj.path_items)}\n"
                f"Components: {local_component_total + len(obj.shared_component_refs)}\n"
                f"Shared component refs: {len(obj.shared_component_refs)}"
            )
        if kind == "components" and isinstance(obj, ApiModel):
            local_component_total = sum(
                len(component_map)
                for component_map in obj.local_components.values()
                if isinstance(component_map, dict)
            )
            return (
                f"Local components: {local_component_total}\n"
                f"Shared component refs: {len(obj.shared_component_refs)}\n"
                f"Shared items are highlighted in the tree."
            )
        if kind == "component_kind" and isinstance(obj, dict):
            return f"Kind: {obj.get('kind', '')}\nItems: {obj.get('count', 0)}"
        if kind == "path" and obj is not None:
            return (
                f"Operations: {len(getattr(obj, 'operations', []))}\n"
                f"Parameters: {len(getattr(obj, 'parameters', []))}\n"
                f"Extensions: {len(getattr(obj, 'extensions', {}))}\n"
                f"Custom metadata: {len(getattr(obj, 'custom_metadata', {}))}"
            )
        if kind == "operation" and obj is not None:
            details = {
                "path": getattr(obj, "path", ""),
                "method": getattr(obj, "method", "").upper(),
                "summary": getattr(obj, "summary", ""),
                "tags": getattr(obj, "tags", []),
                "parameters": getattr(obj, "parameters", []),
                "request_body": getattr(obj, "request_body", {}),
                "responses": getattr(obj, "responses", {}),
                "security": getattr(obj, "security", []),
                "callbacks": [callback.to_dict() for callback in getattr(obj, "callbacks", [])],
                "extensions": getattr(obj, "extensions", {}),
                "custom_metadata": getattr(obj, "custom_metadata", {}),
            }
            return json.dumps(details, indent=2, ensure_ascii=True)
        if kind == "release" and obj is not None:
            return json.dumps(obj.to_dict(), indent=2, ensure_ascii=True)
        if kind == "change" and obj is not None:
            return json.dumps(obj.to_dict(), indent=2, ensure_ascii=True)
        if kind == "change_step" and obj is not None:
            return json.dumps(obj.to_dict(), indent=2, ensure_ascii=True)
        if kind == "library" and obj is not None:
            return f"Components: {len(getattr(obj, 'components', []))}"
        if kind == "component" and obj is not None:
            return json.dumps(obj.to_dict(), indent=2, ensure_ascii=True)
        if kind == "local_component" and obj is not None:
            return json.dumps(obj.get("payload", {}), indent=2, ensure_ascii=True)
        if kind == "shared_ref" and obj is not None:
            return json.dumps(obj, indent=2, ensure_ascii=True)
        if kind == "callback" and obj is not None:
            return json.dumps(obj.to_dict(), indent=2, ensure_ascii=True)
        if kind == "operation_group":
            return "Select an operation to edit its identifier, method, path, and description."
        if kind == "path_group":
            return "Select a path to inspect its summary, description, parameters, and operations."
        if kind.endswith("_group"):
            return "Items: 0" if obj is None else f"Items: {len(obj)}" if hasattr(obj, "__len__") else ""
        return ""

    def _select_workspace(self) -> None:
        roots = self.workspace_tree.get_children()
        if roots:
            self.workspace_tree.selection_set(roots[0])
            self.workspace_tree.focus(roots[0])
        self._clear_tree_selection(self.model_tree)
        self.selected_ref = ("workspace", self.workspace)
        self.selected_source = "explorer"
        self._render_inspector("workspace", self.workspace)

    def _select_default_designer_focus(self) -> None:
        model_roots = self.model_tree.get_children()
        if model_roots:
            self._apply_tree_selection(self.model_tree, model_roots[0])
            self._clear_tree_selection(self.workspace_tree)
            ref = self._model_node_index.get(model_roots[0])
            if ref:
                self.selected_ref = ref
                self.selected_source = "model"
                self._render_inspector(*ref)
                return
        self._select_workspace()

    def _restore_selection(self, ref: Tuple[str, Any]) -> None:
        workspace_node = self._find_node_for_ref(self._workspace_node_index, ref)
        if workspace_node:
            self._apply_tree_selection(self.workspace_tree, workspace_node)
            self._clear_tree_selection(self.model_tree)
            self.selected_source = "explorer"
            self.selected_ref = ref
            self._render_inspector(*ref)
            return

        model_node = self._find_node_for_ref(self._model_node_index, ref)
        if model_node:
            self._apply_tree_selection(self.model_tree, model_node)
            self._clear_tree_selection(self.workspace_tree)
            self.selected_source = "model"
            self.selected_ref = ref
            self._render_inspector(*ref)
            return

        self._select_workspace()

    def _apply_tree_selection(self, tree, node_id: str) -> None:
        tree.selection_set(node_id)
        tree.focus(node_id)
        tree.see(node_id)

    def _clear_tree_selection(self, tree) -> None:
        current = tree.selection()
        if current:
            tree.selection_remove(current)
        tree.focus("")

    def _find_node_for_ref(
        self,
        index: Dict[str, Tuple[str, Any]],
        ref: Tuple[str, Any],
    ) -> Optional[str]:
        wanted_kind, wanted_obj = ref
        for node_id, node_ref in index.items():
            if node_ref[0] != wanted_kind:
                continue
            if node_ref[1] is wanted_obj:
                return node_id
            if (
                isinstance(node_ref[1], dict)
                and isinstance(wanted_obj, dict)
                and node_ref[1].get("node_path") == wanted_obj.get("node_path")
            ):
                return node_id
            if getattr(node_ref[1], "id", None) and getattr(wanted_obj, "id", None):
                if getattr(node_ref[1], "id", None) == getattr(wanted_obj, "id", None):
                    return node_id
        return None

    def _selected_api(self) -> Optional[ApiModel]:
        if not self.selected_ref:
            return None
        return self._api_for_ref(self.selected_ref)

    def _api_for_ref(self, ref: Tuple[str, Any]) -> Optional[ApiModel]:
        kind, obj = ref
        if kind == "api" and isinstance(obj, ApiModel):
            return obj if obj in self.workspace.apis else None
        if kind == "components" and isinstance(obj, ApiModel):
            return obj if obj in self.workspace.apis else None
        if kind == "section" and isinstance(obj, dict):
            if self.workspace.apis:
                return self.workspace.apis[0]
        if kind in {"value_field", "object_field", "list_field", "resolved_ref"} and isinstance(obj, dict):
            if self.workspace.apis:
                return self.workspace.apis[0]
        if kind == "path" and isinstance(obj, PathItemModel):
            for api in self.workspace.apis:
                if obj in api.path_items or obj in api.webhooks:
                    return api
        if kind == "operation" and isinstance(obj, OperationModel):
            for api in self.workspace.apis:
                for path_item in api.path_items:
                    if obj in path_item.operations:
                        return api
        if kind == "callback" and isinstance(obj, PathItemModel):
            for api in self.workspace.apis:
                for path_item in api.path_items:
                    for operation in path_item.operations:
                        if obj in operation.callbacks:
                            return api
        if kind in {
            "local_component",
            "shared_ref",
            "shared_refs",
            "path_group",
            "operation_group",
            "webhook_group",
        }:
            for api in self.workspace.apis:
                if obj is api.path_items or obj is api.local_components or obj is api.shared_component_refs:
                    return api
                if kind == "local_component" and isinstance(obj, dict):
                    payload = obj.get("payload")
                    for component_map in api.local_components.values():
                        if isinstance(component_map, dict) and payload in component_map.values():
                            return api
        return None

    def _set_description_text(self, text: str) -> None:
        self.entry_description.configure(state="normal")
        self.entry_description.delete("1.0", "end")
        if text:
            self.entry_description.insert("1.0", text)

    def _get_description_text(self) -> str:
        return self.entry_description.get("1.0", "end").strip()

    def _set_status(self, text: str) -> None:
        self.status_label.configure(text=text)
        if self.status_callback:
            self.status_callback(f"[Designer] {text}")

    def _remember_workspace_path(self) -> None:
        if not self.workspace_path:
            return
        self.prefs_manager.set("last_api_model_workspace", str(self.workspace_path))
        self.prefs_manager.save()

    def _initial_dir(self) -> Optional[str]:
        last = self.prefs_manager.get("last_api_model_workspace", "")
        if last and Path(last).exists():
            return str(Path(last))
        last_oas_file = self.prefs_manager.get("last_designer_oas_import_file", "")
        if last_oas_file and Path(last_oas_file).exists():
            return str(Path(last_oas_file).parent)
        oas_folder = self.prefs_manager.get("last_oas_folder", "")
        if oas_folder and os.path.exists(oas_folder):
            return oas_folder
        return os.getcwd()

    def _initial_oas_dir(self) -> Optional[str]:
        designer_oas_folder = self.prefs_manager.get("last_designer_oas_import_folder", "")
        if designer_oas_folder and os.path.exists(designer_oas_folder):
            return designer_oas_folder
        oas_folder = self.prefs_manager.get("last_oas_folder", "")
        if oas_folder and os.path.exists(oas_folder):
            return oas_folder
        return self._initial_dir()

    def _confirm_discard_dirty(self) -> bool:
        if not self._dirty:
            return True
        return messagebox.askyesno(
            "Unsaved Workspace",
            "Discard unsaved API Model changes?",
            parent=self.master.winfo_toplevel(),
        )

    def _prompt_workspace_name(self, default: str) -> Optional[str]:
        dialog = ctk.CTkInputDialog(text="Workspace name:", title="New API Model Workspace")
        value = dialog.get_input()
        if value is None:
            return None
        value = value.strip()
        return value or default

    def _safe_folder_name(self, name: str) -> str:
        cleaned = "".join(ch if ch.isalnum() or ch in ("-", "_", " ") else "_" for ch in name)
        cleaned = cleaned.strip().replace(" ", "_")
        return cleaned or "API_Model_Workspace"

    def _remember_oas_dir(self, directory: Path) -> None:
        self.prefs_manager.set("last_designer_oas_import_folder", str(directory))
        self.prefs_manager.save()

    def _remember_oas_file(self, path: Path) -> None:
        self.prefs_manager.set("last_designer_oas_import_file", str(path))
        self.prefs_manager.save()

    def _path_has_shared_data(self, path_item: PathItemModel) -> bool:
        return any(
            [
                path_item.summary,
                path_item.description,
                path_item.ref,
                path_item.parameters,
                path_item.servers,
                path_item.extensions,
                path_item.extra_fields,
            ]
        )

    def _payload_editor_text(self, kind: str, obj: Any) -> str:
        payload = self._payload_for(kind, obj)
        return self._dump_yaml(payload)

    def _payload_for(self, kind: str, obj: Any) -> Dict[str, Any]:
        if kind == "api" and isinstance(obj, ApiModel):
            payload = obj.to_oas_dict()
            payload.pop("openapi", None)
            info = dict(payload.get("info") or {})
            info.pop("title", None)
            info.pop("version", None)
            payload["info"] = info
            return payload
        if kind in {"path", "callback"} and isinstance(obj, PathItemModel):
            payload = obj.to_oas_path_item()
            for key in ("summary", "description"):
                payload.pop(key, None)
            return payload
        if kind == "operation" and isinstance(obj, OperationModel):
            payload = obj.to_oas_dict()
            payload.pop("operationId", None)
            return payload
        if kind == "parameter" and isinstance(obj, dict):
            return {k: v for k, v in obj.items() if k not in {"name", "in", "required"}}
        if kind == "request_body" and isinstance(obj, dict):
            return {k: v for k, v in obj.items() if k not in {"$ref", "required"}}
        if kind == "response" and isinstance(obj, dict):
            return {k: v for k, v in obj.items() if k != "description"}
        if kind == "release" and obj is not None and hasattr(obj, "to_dict"):
            return obj.to_dict()
        if kind == "change" and obj is not None and hasattr(obj, "to_dict"):
            return obj.to_dict()
        if kind == "change_step" and obj is not None and hasattr(obj, "to_dict"):
            return obj.to_dict()
        if kind == "library" and obj is not None and hasattr(obj, "to_dict"):
            return obj.to_dict()
        if kind == "component" and obj is not None and hasattr(obj, "to_dict"):
            return obj.to_dict()
        if kind == "local_component" and isinstance(obj, dict):
            return obj.get("payload", {})
        if kind == "shared_ref" and isinstance(obj, dict):
            return obj
        return {}

    def _parse_payload_text(self, text: str) -> Dict[str, Any]:
        if not text:
            return {}
        try:
            data = yaml.safe_load(text)
        except yaml.YAMLError as exc:
            messagebox.showerror(
                "Invalid Payload",
                f"Payload is not valid YAML/JSON:\n{exc}",
                parent=self.master.winfo_toplevel(),
            )
            raise
        if data is None:
            return {}
        if not isinstance(data, dict):
            messagebox.showerror(
                "Invalid Payload",
                "Payload must be a mapping/object.",
                parent=self.master.winfo_toplevel(),
            )
            raise ValueError("Payload must be a mapping.")
        return data

    def _dump_yaml(self, data: Any) -> str:
        if not data:
            return ""
        return yaml.safe_dump(data, sort_keys=False, allow_unicode=True).strip()

    def _apply_payload_to_object(self, kind: str, obj: Any, payload: Dict[str, Any]) -> None:
        if kind == "workspace":
            self.workspace.settings = payload.get("settings", self.workspace.settings)
            self.workspace.extensions = payload.get("extensions", self.workspace.extensions)
            self.workspace.custom_metadata = payload.get(
                "custom_metadata", self.workspace.custom_metadata
            )
            return
        if kind == "api" and isinstance(obj, ApiModel):
            info_payload = dict(payload.get("info") or {})
            info_payload["title"] = obj.info.get("title", obj.display_label or obj.name)
            info_payload["version"] = obj.info.get("version", obj.version)
            rebuilt_payload = {"openapi": obj.openapi_version, **payload, "info": info_payload}
            rebuilt = import_oas_dict_to_api_model(
                rebuilt_payload, source_name=obj.name or obj.display_label
            )
            obj.__dict__.update(rebuilt.__dict__)
            return
        if kind in {"path", "callback"} and isinstance(obj, PathItemModel):
            full_payload = {
                "summary": obj.summary,
                "description": obj.description,
                **payload,
            }
            rebuilt = PathItemModel.from_dict({"path": obj.path, **self._import_path_payload(obj.path, full_payload)})
            obj.__dict__.update(rebuilt.__dict__)
            return
        if kind == "operation" and isinstance(obj, OperationModel):
            full_payload = {"operationId": obj.operation_id, **payload}
            rebuilt = self._operation_from_payload(obj.path, obj.method, full_payload)
            obj.__dict__.update(rebuilt.__dict__)
            return
        if kind == "parameter" and isinstance(obj, dict):
            preserved = {
                "name": obj.get("name", ""),
                "in": obj.get("in", ""),
                "required": obj.get("required", False),
            }
            obj.clear()
            obj.update(preserved)
            obj.update(payload)
            return
        if kind == "request_body" and isinstance(obj, dict):
            ref_value = obj.get("$ref")
            required_value = obj.get("required")
            obj.clear()
            if ref_value:
                obj["$ref"] = ref_value
            obj["required"] = required_value
            obj.update(payload)
            return
        if kind == "response" and isinstance(obj, dict):
            description = obj.get("description", "")
            obj.clear()
            obj["description"] = description
            obj.update(payload)
            return
        if kind == "local_component" and isinstance(obj, dict):
            obj["payload"] = payload
            api = self._selected_api()
            if api:
                component_map = api.local_components.setdefault(obj.get("kind", ""), {})
                if isinstance(component_map, dict):
                    component_map[obj.get("name", "")] = payload
            return
        if kind == "shared_ref" and isinstance(obj, dict):
            obj.clear()
            obj.update(payload)
            return
        if obj is not None and hasattr(obj, "to_dict") and hasattr(type(obj), "from_dict"):
            rebuilt = type(obj).from_dict(payload)
            obj.__dict__.update(rebuilt.__dict__)

    def _import_path_payload(self, path_key: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        from .oas_importer import _import_path_item

        return _import_path_item(path_key, payload).to_dict()

    def _operation_from_payload(
        self, path_key: str, method: str, payload: Dict[str, Any]
    ) -> OperationModel:
        from .oas_importer import _import_operation

        return _import_operation(path_key, method, payload)

    def _apply_value_field_change(self, meta: Dict[str, Any]) -> bool:
        current_value = meta.get("value")
        new_raw = self.entry_description.get("1.0", "end").strip() if self.entry_description.winfo_ismapped() and self.entry_description.cget("state") == "normal" else self.var_secondary.get().strip()
        new_value = self._parse_scalar_value(current_value, new_raw)

        ref_context = meta.get("ref_context")
        if ref_context:
            ref_info = ref_context["ref_info"]
            target_payload = deepcopy(ref_info["payload"])
            relative_path = list(meta.get("node_path", ()))[-self._relative_ref_path_length(meta):]
            self._set_nested_value(target_payload, relative_path, new_value)
            return self._commit_reference_edit(ref_context["ref_holder"], ref_info, target_payload)

        container = meta.get("container")
        key = meta.get("key")
        if isinstance(container, dict):
            container[key] = new_value
            return True
        if isinstance(container, list) and isinstance(key, int):
            container[key] = new_value
            return True
        return False

    def _relative_ref_path_length(self, meta: Dict[str, Any]) -> int:
        node_path = list(meta.get("node_path", ()))
        if "resolved" in node_path:
            idx = node_path.index("resolved")
            return len(node_path) - idx - 1
        if "ref" in node_path:
            idx = node_path.index("ref")
            return len(node_path) - idx - 2
        return 1

    def _set_nested_value(self, payload: Any, path_segments: list[Any], new_value: Any) -> None:
        target = payload
        for segment in path_segments[:-1]:
            target = target[segment]
        target[path_segments[-1]] = new_value

    def _parse_scalar_value(self, current_value: Any, raw: str) -> Any:
        if isinstance(current_value, bool):
            return raw.lower() == "true"
        if isinstance(current_value, int) and not isinstance(current_value, bool):
            return int(raw) if raw else 0
        if isinstance(current_value, float):
            return float(raw) if raw else 0.0
        if current_value is None:
            lowered = raw.lower()
            if lowered in {"true", "false"}:
                return lowered == "true"
            return raw
        return raw

    def _format_scalar_value(self, value: Any) -> str:
        if value is None:
            return ""
        if isinstance(value, bool):
            return "true" if value else "false"
        return str(value)

    def _value_field_options(self, meta: Dict[str, Any]) -> list[str]:
        value = meta.get("value")
        label = str(meta.get("label", ""))
        normalized_label = label.lower()
        if isinstance(value, bool):
            return ["true", "false"]
        if normalized_label == "$ref":
            options = self._component_ref_options(meta)
            if options:
                return options
        if normalized_label == "schema_mode":
            return SCHEMA_MODE_OPTIONS
        if normalized_label == "openapi":
            return OPENAPI_VERSIONS
        if normalized_label == "in":
            return PARAMETER_LOCATIONS
        if normalized_label == "method":
            return HTTP_METHODS
        if normalized_label == "type":
            return SCHEMA_TYPES
        if normalized_label == "style":
            return PARAMETER_STYLE_OPTIONS
        if normalized_label == "format":
            return STRING_FORMAT_OPTIONS
        return []

    def _component_ref_options(self, meta: Dict[str, Any]) -> list[str]:
        section = self._component_section_for_ref_meta(meta)
        if not section:
            return []
        api = self._selected_api()
        if not api:
            return []
        component_map = api.local_components.get(section)
        if not isinstance(component_map, dict):
            return []
        refs = [f"#/components/{section}/{name}" for name in sorted(component_map.keys())]
        current = str(meta.get("value", "") or "")
        if current and current not in refs:
            refs.insert(0, current)
        if "" not in refs:
            refs.insert(0, "")
        return refs

    def _component_section_for_ref_meta(self, meta: Dict[str, Any]) -> Optional[str]:
        path = tuple(meta.get("path") or ())
        template_context = str(meta.get("template_context") or "")
        if not path or path[-1] != "$ref":
            return None
        path_labels = [segment for segment in path[:-1] if isinstance(segment, str)]
        if any(label in {"schema", "properties", "items", "allOf", "anyOf", "oneOf"} for label in path_labels):
            return "schemas"
        if template_context == "schema":
            return "schemas"
        direct_template_sections = {
            "parameter": "parameters",
            "request_body": "requestBodies",
            "response": "responses",
            "header": "headers",
            "example": "examples",
            "link": "links",
        }
        if len(path) == 1:
            return direct_template_sections.get(template_context)
        if "headers" in path_labels:
            return "headers"
        if "responses" in path_labels:
            return "responses"
        if "examples" in path_labels:
            return "examples"
        if "links" in path_labels:
            return "links"
        return None

    def _schema_mode(self, schema: dict[str, Any]) -> str:
        raw_mode = str(schema.get("__schema_mode__", "") or "").strip()
        raw_mode_key = self._schema_mode_key(raw_mode) if raw_mode else ""
        if raw_mode_key and raw_mode_key != "simple":
            return raw_mode_key
        if schema.get("$ref"):
            return "reference"
        for key in ("allOf", "anyOf", "oneOf"):
            if isinstance(schema.get(key), list) and schema.get(key):
                return key
        if raw_mode_key:
            return raw_mode_key
        return "simple"

    def _schema_mode_key(self, raw_mode: str) -> str:
        normalized = raw_mode.strip().lower().replace(" ", "")
        if normalized == "reference":
            return "reference"
        if normalized == "allof":
            return "allOf"
        if normalized == "anyof":
            return "anyOf"
        if normalized == "oneof":
            return "oneOf"
        return "simple"

    def _schema_mode_label(self, schema_mode: str) -> str:
        return {
            "reference": "Reference",
            "allOf": "All Of",
            "anyOf": "Any Of",
            "oneOf": "One Of",
        }.get(schema_mode, "Simple")

    def _schema_mode_composition_key(self, schema_mode: str) -> Optional[str]:
        if schema_mode in {"allOf", "anyOf", "oneOf"}:
            return schema_mode
        return None

    def _normalize_schema_modes_in_payload(self, value: Any) -> None:
        if isinstance(value, dict):
            for child in value.values():
                self._normalize_schema_modes_in_payload(child)
            if "__schema_mode__" in value:
                self._normalize_single_schema_dict(value)
        elif isinstance(value, list):
            for child in value:
                self._normalize_schema_modes_in_payload(child)

    def _normalize_single_schema_dict(self, schema: dict[str, Any]) -> None:
        mode = self._schema_mode_key(str(schema.pop("__schema_mode__", "") or "simple"))
        simple_shape_keys = {
            "type",
            "format",
            "minLength",
            "maxLength",
            "pattern",
            "minItems",
            "maxItems",
            "enum",
            "properties",
            "items",
            "required",
            "default",
        }
        composition_keys = {"allOf", "anyOf", "oneOf"}
        if mode == "reference":
            for key in simple_shape_keys | composition_keys:
                schema.pop(key, None)
            return
        schema.pop("$ref", None)
        if mode == "simple":
            for key in composition_keys:
                schema.pop(key, None)
            schema_type = str(schema.get("type", "") or "")
            if schema_type != "string":
                schema.pop("format", None)
                schema.pop("minLength", None)
                schema.pop("maxLength", None)
                schema.pop("pattern", None)
            if schema_type != "array":
                schema.pop("minItems", None)
                schema.pop("maxItems", None)
            if schema_type != "object":
                schema.pop("properties", None)
                schema.pop("required", None)
            if schema_type != "array":
                schema.pop("items", None)
            return
        for key in simple_shape_keys:
            schema.pop(key, None)
        for key in composition_keys:
            if key != mode:
                schema.pop(key, None)
        schema.setdefault(mode, [])

    def _resolve_reference_info(self, obj: Any) -> Optional[Dict[str, Any]]:
        if not isinstance(obj, dict):
            return None
        ref = str(obj.get("$ref", "") or "")
        if not ref.startswith("#/components/"):
            return None
        parts = ref.split("/")
        if len(parts) != 4:
            return None
        _, _, section, component_name = parts
        api = self._selected_api()
        if not api:
            return None
        component_map = api.local_components.get(section)
        if not isinstance(component_map, dict):
            return None
        payload = component_map.get(component_name)
        if not isinstance(payload, dict):
            return None
        return {
            "ref": ref,
            "section": section,
            "component_name": component_name,
            "payload": payload,
            "component_map": component_map,
        }

    def _ref_context_for(self, obj: Any) -> Optional[Dict[str, Any]]:
        ref_info = self._resolve_reference_info(obj)
        if not ref_info:
            return None
        return {"ref_holder": obj, "ref_info": ref_info}

    def _resolve_shared_component_payload(self, ref: dict) -> Optional[Dict[str, Any]]:
        library_id = ref.get("library_id")
        component_id = ref.get("component_id")
        for library in self.workspace.shared_libraries:
            if library.id != library_id:
                continue
            for component in library.components:
                if component.id == component_id:
                    return component.payload
        return None

    def _commit_reference_edit(
        self,
        ref_holder: dict,
        ref_info: Dict[str, Any],
        target_payload: Dict[str, Any],
    ) -> bool:
        api = self._selected_api()
        if not api:
            return False
        ref = ref_info["ref"]
        usage_count = self._count_ref_usages(api, ref)
        apply_globally = True
        if usage_count > 1:
            decision = messagebox.askyesnocancel(
                "Referenced Component",
                "This component is referenced in multiple places.\n\n"
                "Yes: keep the change global\n"
                "No: split into a specific copy for this usage",
                parent=self.master.winfo_toplevel(),
            )
            if decision is None:
                return False
            apply_globally = decision

        if apply_globally:
            ref_info["component_map"][ref_info["component_name"]] = target_payload
            return True

        suggested_name = f"{ref_info['component_name']}_copy"
        new_name = self._prompt_component_name(suggested_name)
        if not new_name:
            return False
        ref_info["component_map"][new_name] = target_payload
        ref_holder["$ref"] = f"#/components/{ref_info['section']}/{new_name}"
        return True

    def _count_ref_usages(self, api: ApiModel, ref: str) -> int:
        count = 0
        for value in self._iter_values(api.to_oas_dict()):
            if isinstance(value, dict) and value.get("$ref") == ref:
                count += 1
        return count

    def _iter_values(self, value: Any):
        yield value
        if isinstance(value, dict):
            for child in value.values():
                yield from self._iter_values(child)
        elif isinstance(value, list):
            for child in value:
                yield from self._iter_values(child)

    def _prompt_component_name(self, default: str) -> Optional[str]:
        dialog = ctk.CTkInputDialog(
            text="New component name:",
            title="Split Referenced Component",
        )
        value = dialog.get_input()
        if value is None:
            return None
        value = value.strip() or default
        return value

    def _parameter_label(self, parameter: dict) -> str:
        ref_info = self._resolve_reference_info(parameter)
        if ref_info:
            return ref_info["component_name"]
        return f"{parameter.get('name', 'parameter')} ({parameter.get('in', '')})"

    def _request_body_label(self, request_body: dict) -> str:
        ref_info = self._resolve_reference_info(request_body)
        if ref_info:
            return f"Request Body: {ref_info['component_name']}"
        return "Request Body"

    def _response_label(self, status_code: Any, response_payload: dict) -> str:
        ref_info = self._resolve_reference_info(response_payload)
        if ref_info:
            return f"{status_code} -> {ref_info['component_name']}"
        return str(status_code)

    def _response_code_for(self, response_payload: dict) -> str:
        for api in self.workspace.apis:
            for path_item in api.path_items + api.webhooks:
                for operation in path_item.operations:
                    for status_code, candidate in operation.responses.items():
                        if candidate is response_payload:
                            return str(status_code)
        return ""

    def _rename_response(self, response_payload: dict, new_code: str) -> None:
        new_code = (new_code or "").strip()
        if not new_code:
            return
        for api in self.workspace.apis:
            for path_item in api.path_items + api.webhooks:
                for operation in path_item.operations:
                    for status_code, candidate in list(operation.responses.items()):
                        if candidate is response_payload and status_code != new_code:
                            operation.responses.pop(status_code)
                            operation.responses[new_code] = response_payload
                            return

    def _kind_uses_payload_editor(self, kind: str) -> bool:
        return kind in {
            "api",
            "path",
            "operation",
            "callback",
            "parameter",
            "request_body",
            "response",
            "release",
            "change",
            "change_step",
            "library",
            "component",
            "local_component",
            "shared_ref",
        }
