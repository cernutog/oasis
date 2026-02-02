# Source Mapping Analysis

## Current Situation
- `_record_source` in `generator.py` is defined but never called
- `source_map` remains empty
- GUI tries to resolve source files but finds nothing

## Path Examples from Screenshot
1. `info-contact` → Path: `info`
   - Should map to: `$index.xlsx` → "General Description" sheet
   
2. `operation-tags` → Path: `paths > /vop/v1/payee-information > post`
   - Should map to: `$index.xlsx` → "Paths" sheet (NOT the operation template)

## Required Mapping Logic

### Global Sections (in $index.xlsx)
- `info` → "General Description"
- `info.contact` → "General Description"
- `info.license` → "General Description"
- `tags` → "Tags"
- `paths` → "Paths"
- `paths.{path}.{method}` → "Paths" (for operation-level properties like tags)
- `paths.{path}.{method}.tags` → "Paths"
- `components.schemas` → "Schemas"
- `components.parameters` → "Parameters"
- `components.responses` → "Responses"
- `components.securitySchemes` → "Security Schemes"

### Operation-Specific Sections (in operation template files)
- `paths.{path}.{method}.parameters` → Operation template file
- `paths.{path}.{method}.requestBody` → Operation template file
- `paths.{path}.{method}.responses` → Operation template file
- `paths.{path}.{method}.responses.{code}` → Operation template file

## Implementation Strategy
1. Populate `source_map` during OAS generation
2. For each section, determine if it belongs to $index or operation template
3. Record the correct file and sheet name
