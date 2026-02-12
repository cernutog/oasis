# Test Case: R8_collision

## Obiettivo
Verificare la gestione delle collisioni quando due endpoint definiscono lo stesso Data Type con vincoli diversi.

## INPUT: Template Legacy
`firstOperation.250101.xlsm`
- **Data Type**: `Amount` (Type=number, Max=1000)

`secondOperation.250101.xlsm`
- **Data Type**: `Amount` (Type=number, Max=5000)

## OUTPUT ATTESO
`$index.xlsx` (Foglio Schemas)
- `Amount`: Type=number, Max=1000
- `Amount1`: Type=number, Max=5000 (O altro suffisso univoco)
- Wrapper `firstOperationRequest`: Schema Name=Amount
- Wrapper `secondOperationRequest`: Schema Name=Amount1
