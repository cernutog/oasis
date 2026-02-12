# Test Case: R1_basic_structure

## Obiettivo
Verificare la conversione completa da template legacy a template target, incluse strutture annidate e response multiple.

---

## INPUT: Template Legacy

### File: `$index.xlsm`

**General Description**
- info description, info version, info title, servers

**Paths**
- testOperation.260209 | /test/{testId} | post | TestTag | testOperation

---

### File: `testOperation.260209.xlsm`

**Data Type** (foglie - no struttura)
- TestName (string, min=1, max=140, regex, example)
- TestAmount (number, double, min/max, example)
- TestStatus (string, allowed values, example)
- TestCode (string, patternEba, example)
- TestDate (string, date, example)
- TestId (string, max=36, example)
- CorrelationId (string, max=50, example)
- object (object)

**Path**: testId (TestId, M)
**Header**: X-Correlation-Id (CorrelationId, O)

**Body** (struttura annidata con Parent)
- searchCriteria (object, M) → root
  - dateFrom (TestDate, M) → parent=searchCriteria
  - dateTo (TestDate, O) → parent=searchCriteria
- testName (TestName, M) → root, con Validation Rules
- amount (TestAmount, O) → root
- status (TestStatus, M) → root

**200** (Response 200 - OK)
- resultData (object, M) → root
  - result (TestName, M) → parent=resultData
  - processedDate (TestDate, M) → parent=resultData
- status (TestStatus, M) → root

**400** (Response 400 - Bad Request)
- dateTime (TestDate, M)
- errorCode (string, M)
- errorDescription (string, M)

---

## OUTPUT ATTESO

### `$index.xlsx`

**General Description** → valori nelle righe predefinite (servers in riga 7-8)
**Paths** → headers riga 2, dati riga 3
**Tags** → TestTag
**Parameters** → vuoto (inline legacy)
**Headers** → vuoto (inline legacy)
**Responses** → vuoto (inline legacy)

**Schemas** (struttura completa):
- testOperationRequest (object) + figli con Parent
- testOperationResponse (object) + figli con Parent
- ErrorResponse (object) + figli (dateTime, errorCode, errorDescription)
- Data Types: TestName, TestAmount, TestStatus, TestDate, TestId, CorrelationId

---

### `testOperation.260209.xlsx`

**Parameters**: testId (path, inline), X-Correlation-Id (header, inline)
**Body**: solo testOperationRequest (object)
**200**: titolo "Response 200 - Success", solo testOperationResponse (object)
**400**: titolo "Response 400 - Bad Request", solo ErrorResponse (object)
**Fogli 200/400**: creati dal foglio Response del master con stili

---

## Regole chiave testate
- [ ] Wrapper implicito: Body → testOperationRequest, 200 → testOperationResponse, 400 → ErrorResponse
- [ ] Struttura Parent preservata in Schemas
- [ ] Data Types copiati con tutti gli attributi
- [ ] Parameters/Headers inline (non promossi a component)
- [ ] Responses inline (foglio Responses vuoto)
- [ ] Type=schema in Schemas quando riferimento ad altro schema
- [ ] Validation Rules appese alla Description
