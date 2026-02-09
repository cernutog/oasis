# Test Case: R1_basic_structure

## Obiettivo
Verificare la copia completa di tutti i campi, incluse strutture annidate con Parent.

---

## INPUT: Template Legacy

### File: `$index.xlsm`

**General Description**
- info description: This is a test API for legacy converter validation.
- info version: 1.0.0
- info title: Test API
- servers url: /int/test, servers description: Integration Test
- servers url: /test, servers description: Production

**Paths**
- Excel file: testOperation.260209
- Path: /test/{testId}
- Name: testOperation
- Method: post
- Description: A test operation for validation
- Tag: TestTag
- Summary: Test operation summary
- OperationId: testOperation
- Custom Extensions: x-custom-field: custom-value\nx-another: value2

---

### File: `testOperation.260209.xlsm`

**Data Type**
- TestName (string, min=1, max=140, regex=^[A-Za-z]+$, example=ExampleTestName)
- TestAmount (number, format=double, min=0.01, max=999999.99, example=1234.56)
- TestStatus (string, allowed=ACTIVE;INACTIVE;PENDING, example=ACTIVE)
- TestCode (string, patternEba=4!c2!a2!c, example=TESTIT2XXXX)
- TestDate (string, format=date, example=2026-02-09)
- TestId (string, max=36, example=abc-123-def)
- CorrelationId (string, max=50, example=corr-12345)

**Path**
- testId (Type=TestId, M, Description: The unique test identifier, Validation: Must be a valid UUID)

**Header**
- X-Correlation-Id (Type=CorrelationId, O, Description: Request correlation identifier)

**Body** (struttura annidata con Parent)
- searchCriteria (object, M, Description: Search criteria container)
  - dateFrom (Parent=searchCriteria, Type=TestDate, M, Description: Start date)
  - dateTo (Parent=searchCriteria, Type=TestDate, O, Description: End date)
- testName (Type=TestName, M, Description: The test name, Validation: Must not be empty)
- amount (Type=TestAmount, O, Description: The amount)
- status (Type=TestStatus, M, Description: The status)

**200**
- resultData (object, M, Description: Result container)
  - result (Parent=resultData, Type=TestName, M, Description: The processed result)
  - processedDate (Parent=resultData, Type=TestDate, M, Description: Date of processing)
- status (Type=TestStatus, M, Description: Response status)

---

## OUTPUT ATTESO

### `$index.xlsx`

**General Description** -> copia fedele

**Paths** -> Excel file con .xlsx, resto copiato

**Tags**
- TestTag

**Parameters**
- testId (path, string, M, max=36)

**Headers**
- X-Correlation-Id (string, O, max=50)

**Schemas** (con gerarchia Parent)
- testOperationRequest (object)
  - searchCriteria (Parent=testOperationRequest, object, M)
    - dateFrom (Parent=searchCriteria, Schema Name=TestDate, M)
    - dateTo (Parent=searchCriteria, Schema Name=TestDate, O)
  - testName (Parent=testOperationRequest, Schema Name=TestName, M)
  - amount (Parent=testOperationRequest, Schema Name=TestAmount, O)
  - status (Parent=testOperationRequest, Schema Name=TestStatus, M)
- testOperationResponse (object)
  - resultData (Parent=testOperationResponse, object, M)
    - result (Parent=resultData, Schema Name=TestName, M)
    - processedDate (Parent=resultData, Schema Name=TestDate, M)
  - status (Parent=testOperationResponse, Schema Name=TestStatus, M)
- TestName, TestAmount, TestStatus, TestDate (Data Types)

**Responses**
- 200 (Success)

---

### `testOperation.260209.xlsx`

**Body** (con wrapper testOperationRequest e gerarchia Parent)
**Response** (Section 200 con wrapper testOperationResponse e gerarchia Parent)

---

## Criteri di successo
- [ ] Strutture annidate con Parent correttamente convertite
- [ ] Wrapper Request/Response creati
- [ ] Data Types copiati con tutti gli attributi
- [ ] Parameters/Headers estratti
- [ ] Tags estratto da Paths.Tag
- [ ] Custom Extensions preservate
- [ ] Validation Rules integrate in Description
