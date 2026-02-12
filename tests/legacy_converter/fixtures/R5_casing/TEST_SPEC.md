# Test Case: R5_casing

## Obiettivo
Verificare che il converter normalizzi correttamente i nomi dei Data Type in PascalCase, preservando i riferimenti.

## INPUT: Template Legacy
`testCasing.250101.xlsm`
- **Data Type**:
  - `username` (Type=string, Max=50)
  - `EMAIL_ADDRESS` (Type=string, Pattern=...)
- **Body**:
  - `userName` (Data Type=username)
  - `userEmail` (Data Type=EMAIL_ADDRESS)

## OUTPUT ATTESO
`$index.xlsx` (Foglio Schemas)
- `Username`: (Normalizzato da username)
- `EmailAddress`: (Normalizzato da EMAIL_ADDRESS)
- Wrapper `testCasingRequest`:
  - `userName`: Schema Name=Username
  - `userEmail`: Schema Name=EmailAddress
