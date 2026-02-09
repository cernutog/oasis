"""
Fix expected/$index.xlsx with correct structure
- General Description: fill existing server rows (7-8)
- Paths: headers row 2, data row 3+
- Tags: clear existing data, add TestTag
- Schemas: Type=schema when referencing another schema
"""
import openpyxl
from openpyxl.cell.cell import MergedCell
import shutil
from pathlib import Path

TODAY = "260209"
MASTER = Path("Templates Master")
EXPECTED_DIR = Path("tests/legacy_converter/fixtures/R1_basic_structure/expected")

def set_cell(ws, row, col, value):
    cell = ws.cell(row, col)
    if not isinstance(cell, MergedCell):
        cell.value = value

def clear_cells(ws, start_row, end_row=None):
    if end_row is None:
        end_row = ws.max_row
    for row in range(start_row, end_row + 1):
        for col in range(1, ws.max_column + 1):
            cell = ws.cell(row, col)
            if not isinstance(cell, MergedCell):
                cell.value = None

# Start fresh from Templates Master
print("Copying fresh Templates Master...")
shutil.copy(MASTER / "$index.xlsx", EXPECTED_DIR / "$index.xlsx")

wb = openpyxl.load_workbook(EXPECTED_DIR / "$index.xlsx")

# === General Description ===
print("Fixing General Description...")
ws_gd = wb["General Description"]
# Row 2: info description
set_cell(ws_gd, 2, 2, "This is a test API for legacy converter validation.")
# Row 3: info version
set_cell(ws_gd, 3, 2, "1.0.0")
# Row 4: info title
set_cell(ws_gd, 4, 2, "Test API")
# Rows 5-6: contact (leave empty for this test)
# Row 7: servers url (column B) and servers description (column D)
set_cell(ws_gd, 7, 2, "/int/test")
set_cell(ws_gd, 7, 4, "Integration Test")
# Row 8: second server
set_cell(ws_gd, 8, 2, "/test")
set_cell(ws_gd, 8, 4, "Production")

# === Paths ===
print("Fixing Paths...")
ws_paths = wb["Paths"]
# Row 2 is headers (already there), data starts row 3
set_cell(ws_paths, 3, 1, f"testOperation.{TODAY}.xlsx")
set_cell(ws_paths, 3, 2, "/test/{testId}")
set_cell(ws_paths, 3, 3, "testOperation")
set_cell(ws_paths, 3, 4, "post")
set_cell(ws_paths, 3, 5, "A test operation for validation")
set_cell(ws_paths, 3, 6, "TestTag")
set_cell(ws_paths, 3, 7, "Test operation summary")
set_cell(ws_paths, 3, 8, "testOperation")
set_cell(ws_paths, 3, 9, "x-custom-field: custom-value\nx-another: value2")

# === Tags ===
print("Fixing Tags...")
ws_tags = wb["Tags"]
# Clear all existing data (row 2+)
clear_cells(ws_tags, 2)
# Add TestTag
set_cell(ws_tags, 2, 1, "TestTag")
set_cell(ws_tags, 2, 2, "TestTag")

# === Parameters ===
print("Fixing Parameters...")
ws_params = wb["Parameters"]
set_cell(ws_params, 2, 1, "testId")
set_cell(ws_params, 2, 2, "The unique test identifier")
set_cell(ws_params, 2, 3, "path")
set_cell(ws_params, 2, 4, "string")
set_cell(ws_params, 2, 8, "M")
set_cell(ws_params, 2, 10, "36")

# === Headers ===
print("Fixing Headers...")
ws_headers = wb["Headers"]
set_cell(ws_headers, 2, 1, "X-Correlation-Id")
set_cell(ws_headers, 2, 2, "Request correlation identifier")
set_cell(ws_headers, 2, 3, "string")
set_cell(ws_headers, 2, 7, "O")
set_cell(ws_headers, 2, 9, "50")

# === Schemas ===
print("Fixing Schemas...")
ws_schemas = wb["Schemas"]
# Clear any existing data
clear_cells(ws_schemas, 2)

row = 2
# Request wrapper - Type=object (it IS an object)
set_cell(ws_schemas, row, 1, "testOperationRequest")
set_cell(ws_schemas, row, 4, "object")
row += 1

# searchCriteria - child of request, Type=object (inline object)
set_cell(ws_schemas, row, 1, "searchCriteria")
set_cell(ws_schemas, row, 2, "testOperationRequest")
set_cell(ws_schemas, row, 3, "Search criteria container")
set_cell(ws_schemas, row, 4, "object")  # Type=object because it's an inline object
set_cell(ws_schemas, row, 8, "M")
row += 1

# dateFrom - child of searchCriteria, Type=schema, Schema Name=TestDate
set_cell(ws_schemas, row, 1, "dateFrom")
set_cell(ws_schemas, row, 2, "searchCriteria")
set_cell(ws_schemas, row, 3, "Start date")
set_cell(ws_schemas, row, 4, "schema")  # Type=schema because it references TestDate
set_cell(ws_schemas, row, 6, "TestDate")  # Schema Name
set_cell(ws_schemas, row, 8, "M")
row += 1

# dateTo
set_cell(ws_schemas, row, 1, "dateTo")
set_cell(ws_schemas, row, 2, "searchCriteria")
set_cell(ws_schemas, row, 3, "End date")
set_cell(ws_schemas, row, 4, "schema")
set_cell(ws_schemas, row, 6, "TestDate")
set_cell(ws_schemas, row, 8, "O")
row += 1

# testName - Type=schema, Schema Name=TestName
set_cell(ws_schemas, row, 1, "testName")
set_cell(ws_schemas, row, 2, "testOperationRequest")
set_cell(ws_schemas, row, 3, "The test name")
set_cell(ws_schemas, row, 4, "schema")
set_cell(ws_schemas, row, 6, "TestName")
set_cell(ws_schemas, row, 8, "M")
row += 1

# amount
set_cell(ws_schemas, row, 1, "amount")
set_cell(ws_schemas, row, 2, "testOperationRequest")
set_cell(ws_schemas, row, 3, "The amount")
set_cell(ws_schemas, row, 4, "schema")
set_cell(ws_schemas, row, 6, "TestAmount")
set_cell(ws_schemas, row, 8, "O")
row += 1

# status
set_cell(ws_schemas, row, 1, "status")
set_cell(ws_schemas, row, 2, "testOperationRequest")
set_cell(ws_schemas, row, 3, "The status")
set_cell(ws_schemas, row, 4, "schema")
set_cell(ws_schemas, row, 6, "TestStatus")
set_cell(ws_schemas, row, 8, "M")
row += 1

# Response wrapper
set_cell(ws_schemas, row, 1, "testOperationResponse")
set_cell(ws_schemas, row, 4, "object")
row += 1

# resultData
set_cell(ws_schemas, row, 1, "resultData")
set_cell(ws_schemas, row, 2, "testOperationResponse")
set_cell(ws_schemas, row, 3, "Result container")
set_cell(ws_schemas, row, 4, "object")
set_cell(ws_schemas, row, 8, "M")
row += 1

# result
set_cell(ws_schemas, row, 1, "result")
set_cell(ws_schemas, row, 2, "resultData")
set_cell(ws_schemas, row, 3, "The processed result")
set_cell(ws_schemas, row, 4, "schema")
set_cell(ws_schemas, row, 6, "TestName")
set_cell(ws_schemas, row, 8, "M")
row += 1

# processedDate
set_cell(ws_schemas, row, 1, "processedDate")
set_cell(ws_schemas, row, 2, "resultData")
set_cell(ws_schemas, row, 3, "Date of processing")
set_cell(ws_schemas, row, 4, "schema")
set_cell(ws_schemas, row, 6, "TestDate")
set_cell(ws_schemas, row, 8, "M")
row += 1

# status (response)
set_cell(ws_schemas, row, 1, "status")
set_cell(ws_schemas, row, 2, "testOperationResponse")
set_cell(ws_schemas, row, 3, "Response status")
set_cell(ws_schemas, row, 4, "schema")
set_cell(ws_schemas, row, 6, "TestStatus")
set_cell(ws_schemas, row, 8, "M")
row += 1

# Data Types - these ARE the definitions, so Type is the actual type, no Schema Name
set_cell(ws_schemas, row, 1, "TestName")
set_cell(ws_schemas, row, 3, "A test name field")
set_cell(ws_schemas, row, 4, "string")  # Type=string (actual type)
set_cell(ws_schemas, row, 9, "1")
set_cell(ws_schemas, row, 10, "140")
set_cell(ws_schemas, row, 12, "^[A-Za-z]+$")
set_cell(ws_schemas, row, 14, "ExampleTestName")
row += 1

set_cell(ws_schemas, row, 1, "TestAmount")
set_cell(ws_schemas, row, 3, "A monetary amount")
set_cell(ws_schemas, row, 4, "number")
set_cell(ws_schemas, row, 7, "double")
set_cell(ws_schemas, row, 9, "0.01")
set_cell(ws_schemas, row, 10, "999999.99")
set_cell(ws_schemas, row, 14, "1234.56")
row += 1

set_cell(ws_schemas, row, 1, "TestStatus")
set_cell(ws_schemas, row, 3, "Status indicator")
set_cell(ws_schemas, row, 4, "string")
set_cell(ws_schemas, row, 13, "ACTIVE; INACTIVE; PENDING")
set_cell(ws_schemas, row, 14, "ACTIVE")
row += 1

set_cell(ws_schemas, row, 1, "TestDate")
set_cell(ws_schemas, row, 3, "A date field")
set_cell(ws_schemas, row, 4, "string")
set_cell(ws_schemas, row, 7, "date")
set_cell(ws_schemas, row, 14, "2026-02-09")
row += 1

set_cell(ws_schemas, row, 1, "TestId")
set_cell(ws_schemas, row, 3, "Unique identifier")
set_cell(ws_schemas, row, 4, "string")
set_cell(ws_schemas, row, 10, "36")
set_cell(ws_schemas, row, 14, "abc-123-def")
row += 1

set_cell(ws_schemas, row, 1, "CorrelationId")
set_cell(ws_schemas, row, 3, "Request correlation identifier")
set_cell(ws_schemas, row, 4, "string")
set_cell(ws_schemas, row, 10, "50")
set_cell(ws_schemas, row, 14, "corr-12345")
row += 1

# object type for nested containers
set_cell(ws_schemas, row, 1, "object")
set_cell(ws_schemas, row, 3, "Generic object container")
set_cell(ws_schemas, row, 4, "object")

# === Responses ===
print("Fixing Responses...")
ws_resp = wb["Responses"]
set_cell(ws_resp, 2, 1, "200")
set_cell(ws_resp, 2, 4, "Success")

wb.save(EXPECTED_DIR / "$index.xlsx")
print(f"\nSaved: {EXPECTED_DIR / '$index.xlsx'}")
