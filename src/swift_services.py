from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

from openpyxl import load_workbook


SWIFT_SERVICES_PREFERENCE_KEY = "swift_services"
SWIFT_SERVER_URL_KEY = "swift servers url"
SWIFT_SERVER_DESCRIPTION_KEY = "swift servers description"
MAX_TEMPLATE_SWIFT_SERVERS = 2


def normalize_swift_services(value: Any) -> dict[str, dict[str, list[dict[str, str]]]]:
    """Normalize the configurable SWIFT service catalog."""
    if not isinstance(value, dict):
        return {}

    services: dict[str, dict[str, list[dict[str, str]]]] = {}
    for raw_name, raw_service in value.items():
        name = str(raw_name or "").strip()
        if not name or not isinstance(raw_service, dict):
            continue

        servers = []
        raw_servers = raw_service.get("servers", [])
        if isinstance(raw_servers, list):
            for raw_server in raw_servers:
                if not isinstance(raw_server, dict):
                    continue
                servers.append(
                    {
                        "url": str(raw_server.get("url", "") or "").strip(),
                        "description": str(raw_server.get("description", "") or "").strip(),
                    }
                )
        services[name] = {"servers": servers}

    return services


def get_swift_service_servers(
    services: Any,
    service_name: str,
    log_callback: Callable[[str], None] | None = None,
) -> list[dict[str, str]]:
    catalog = normalize_swift_services(services)
    service = catalog.get(str(service_name or "").strip())
    if not service:
        return []

    servers = deepcopy(service.get("servers", []))
    if len(servers) > MAX_TEMPLATE_SWIFT_SERVERS and log_callback:
        log_callback(
            f"WARNING: SWIFT service '{service_name}' has {len(servers)} configured servers; "
            f"only the first {MAX_TEMPLATE_SWIFT_SERVERS} were written to the template."
        )
    return servers[:MAX_TEMPLATE_SWIFT_SERVERS]


def has_swift_server_rows(index_path: str | Path) -> bool:
    workbook = load_workbook(index_path, read_only=True, data_only=True)
    try:
        if "General Description" not in workbook.sheetnames:
            return False
        ws = workbook["General Description"]
        for row in ws.iter_rows(min_col=1, max_col=1):
            value = row[0].value
            if str(value or "").strip().lower() == SWIFT_SERVER_URL_KEY:
                return True
        return False
    finally:
        workbook.close()


def read_swift_servers_from_general_description(df_info) -> list[dict[str, str]]:
    servers: list[dict[str, str]] = []
    if df_info is None:
        return servers

    for _, row in df_info.iterrows():
        key = str(row.iloc[0]).strip().lower()
        if key != SWIFT_SERVER_URL_KEY:
            continue

        url = row.iloc[1] if len(row) > 1 else ""
        if url is None or str(url).strip().lower() == "nan" or not str(url).strip():
            continue

        server = {"url": str(url).strip()}
        if len(row) > 3:
            desc = row.iloc[3]
            if desc is not None and str(desc).strip().lower() != "nan" and str(desc).strip():
                server["description"] = str(desc).strip()
        servers.append(server)

    return servers


def ensure_swift_server_rows_in_workbook(workbook, servers: list[dict[str, str]] | None = None) -> None:
    if "General Description" not in workbook.sheetnames:
        return

    ws = workbook["General Description"]
    swift_rows = [
        row_idx
        for row_idx in range(1, ws.max_row + 1)
        if str(ws.cell(row=row_idx, column=1).value or "").strip().lower() == SWIFT_SERVER_URL_KEY
    ]

    if not swift_rows:
        insert_at = _find_swift_insert_row(ws)
        ws.insert_rows(insert_at, MAX_TEMPLATE_SWIFT_SERVERS)
        for offset in range(MAX_TEMPLATE_SWIFT_SERVERS):
            row_idx = insert_at + offset
            _label_swift_row(ws, row_idx)
            swift_rows.append(row_idx)
    elif len(swift_rows) < MAX_TEMPLATE_SWIFT_SERVERS:
        insert_at = swift_rows[-1] + 1
        ws.insert_rows(insert_at, MAX_TEMPLATE_SWIFT_SERVERS - len(swift_rows))
        swift_rows = swift_rows + [
            insert_at + offset
            for offset in range(MAX_TEMPLATE_SWIFT_SERVERS - len(swift_rows))
        ]
        for row_idx in swift_rows:
            _label_swift_row(ws, row_idx)
    else:
        swift_rows = swift_rows[:MAX_TEMPLATE_SWIFT_SERVERS]
        for row_idx in swift_rows:
            _label_swift_row(ws, row_idx)

    values = list(servers or [])[:MAX_TEMPLATE_SWIFT_SERVERS]
    for idx, row_idx in enumerate(swift_rows):
        server = values[idx] if idx < len(values) else {}
        ws.cell(row=row_idx, column=2).value = server.get("url", "")
        ws.cell(row=row_idx, column=4).value = server.get("description", "")


def update_index_swift_servers(index_path: str | Path, servers: list[dict[str, str]]) -> None:
    workbook = load_workbook(index_path)
    try:
        ensure_swift_server_rows_in_workbook(workbook, servers)
        workbook.save(index_path)
    finally:
        workbook.close()


def _find_swift_insert_row(ws) -> int:
    for row_idx in range(1, ws.max_row + 1):
        key = str(ws.cell(row=row_idx, column=1).value or "").strip().lower()
        if key == "release":
            return row_idx
    return min(ws.max_row + 1, 9)


def _label_swift_row(ws, row_idx: int) -> None:
    ws.cell(row=row_idx, column=1).value = SWIFT_SERVER_URL_KEY
    ws.cell(row=row_idx, column=3).value = SWIFT_SERVER_DESCRIPTION_KEY
