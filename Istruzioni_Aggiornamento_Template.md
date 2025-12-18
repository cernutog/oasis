# Template Update Instructions

## Executive Summary
This document outlines the necessary updates to the "Original" Excel templates to align them with the current production-ready versions (`API Templates`).
Given the high volume of structural changes (~7400 cell updates), **we strongly recommend replacing the files entirely** rather than applying individual patches.

## Detailed Change Log

### 1. Global Updates (All Files)
- **Error Response Standardization**:
    - Changed Content-Type for error responses (400, 401, 403, 500) from `text/plain` to `application/json`.
    - Updated Schema references to point to `ErrorResponse` instead of generic strings.
    - Standardized Response Names (e.g., `ErrorResponse_401` -> `ErrorResponse_403` where appropriate).
- **Validation Improvements**:
    - "Mandatory" (`M`) flags have been populated for many Header and Path parameters where they were previously missing or blank.
    - Date format examples specific to OAS 3.0/3.1 compatibility have been updated (e.g., `2024-08-12T...` timestamp formats).

### 2. Critical Fixes by File

#### `$index.xlsm`
- **Schema Missing Fields**:
    - **`ShortErrorResponse`**: Added `dt`, `code`, and `desc` properties to the `err` object definition. (Fixes missing validation in generated specifications).
- **Service Type Alignment**:
    - Updated `VopBulkIdentification` to align with the latest schema definitions.

#### `vop_v1_payee_verifications.251111.xlsm`
- **Header Definitions**:
    - corrected `X-Request-ID` and `X-Response-Timestamp` definitions to be explicit headers rather than generic strings.
- **Example Data**:
    - Updated JSON examples for `Bad Request` and `OK` responses to match the new schema structure.

#### Transaction & Assessment Files
- **Status Codes**:
    - Explicit names added for `429` (Too many requests) and `409` (Conflict).
    - `fri` / `pri` headers standardized across response definitions.

## Recommendation
To ensure 1:1 compliance and avoid regression, please archive the "Original" templates and adopt the files currently in `API Templates` as the new Golden Source.
