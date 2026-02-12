# Test Case: R4_array

## Obiettivo
Verificare la gestione degli array che utilizzano la colonna `Items Data Type`.

## INPUT: Template Legacy
`listItems.250101.xlsm`
- **Data Type**:
  - `ItemList` (Type=array, Items Data Type=Item, Min=1, Max=100)
  - `Item` (Type=object)
  - `ItemName` (Type=string, Max=50)

## OUTPUT ATTESO
`$index.xlsx` (Foglio Schemas)
- `ItemList`: Type=array, Items Data Type=Item, Min=1, Max=100
- `Item`: Type=object
- `ItemName`: Type=string, Max=50
