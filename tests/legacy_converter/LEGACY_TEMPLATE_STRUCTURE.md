# Legacy Template Structure Reference

> **Note:** La colonna **Constraint** nei fogli Path/Header/Body/Response è generata da macro e va ignorata.
> La fonte di verità per i vincoli è il foglio **Data Type**.

## $index.xlsm
**Sheets:** ['General Description', 'Paths']

### Sheet: General Description
**Headers (row 1):** 1: General Description
  Row 2: C1=info description, C2=STEP2 System CGS Module - API Specifications Annex
  Row 3: C1=info version, C2=2.1
  Row 4: C1=info title, C2=EBACL STEP2 CGS REST API

### Sheet: Paths
**Headers (row 1):** 2: Paths
  Row 2: C1=Excel file, C2=Path, C3=Name, C4=Method, C5=Description, C6=Tag, C7=Summary, C8=OperationId, C9=Custom Extensions, C10=Track Changes
  Row 3: C1=listSettlementBICs.211207, C2=/listSettlementBICs/{senderBIC}, C3=listSettlementBICs, C4=post, C5=The listSettlement request allows the STEP2-DKK Pr, C6=Preferred Agent, C7=It allows the Participant to inquire the Settlemen, C8=listSettlementBICs, C9=x-sandbox-rule-type: SCRIPT_JS
x-sandbox-rule-cont
  Row 4: C1=settlementBICDetails.230511, C2=/settlementBICDetails/{senderBIC}, C3=settlementBICDetails, C4=post, C5=The settlementBICDetails allows the STEP2-DKK Pref, C6=Preferred Agent, C7=It allows the Participant to inquire the details o, C8=settlementBICDetails, C9=x-sandbox-rule-type: SCRIPT_JS
x-sandbox-rule-cont

---
## Endpoint File (example: listAlerts.211207.xlsm)

## amendChangeSettlementBIC.230511.xlsm
**Sheets:** ['Data Type', 'Path', 'Header', 'Body', '200', '204', '400', '401', '403', '404', '429', '500']

### Sheet: Data Type
**Headers (row 1):** 2: Data Type
  Row 2: C1=Name, C2=Description, C3=Type, C4=Format, C5=Items Data Type 
(Array only), C6=Min  
Value/Length/Item, C7=Max  
Value/Length/Item, C8=PatternEba, C9=Regex, C10=Allowed value, C11=Example, C12=Track Changes
  Row 3: C1=Amount, C2=Standard Amount, C3=number, C4=double, C7=999999999999.99, C11=1000; 100000; 99999.01
  Row 4: C1=array, C3=array, C5=object

### Sheet: Path
**Headers (row 1):** 2: Request Path
  Row 2: C1=Type, C2=Element, C3=Mandatory, C4=Constraint, C5=Description , C6=Validation Rules, C7=Track Changes
  Row 3: C1=senderBIC, C2=senderBIC, C3=M, C4=Type: string
Pattern: 4!c2!a2!c, C5=The BIC sending the request, C6=It must be equal to the BIC of the DP certificate 

### Sheet: Header
**Headers (row 1):** 2: Request Header
  Row 2: C1=Type, C2=Element, C3=Mandatory, C4=Constraint, C5=Description , C6=Validation Rules, C7=Track Changes

### Sheet: Body
**Headers (row 1):** 3: Request Body
  Row 2: C1=Type, C2=Parent, C3=Element, C4=Parents, C5=Mandatory, C6=Constraint, C7=Description , C8=Validation Rules, C9=Track Changes
  Row 3: C1=DateTime, C3=dateTime, C5=M, C6=Type: string
Pattern: YYYY-MM-DDTHH:MM:SS[.M{1,6}], C7=The date and time of the API Request creation
  Row 4: C1=object, C3=settlementBIC, C5=M, C6=Type: object

### Sheet: 200
**Headers (row 1):** 3: Response 200 - OK
  Row 2: C1=Type, C2=Parent, C3=Element, C4=Parents, C5=Mandatory, C6=Constraint, C7=Description , C8=Track Changes
  Row 3: C1=DateTime, C3=dateTime, C5=M, C6=Type: string
Pattern: YYYY-MM-DDTHH:MM:SS[.M{1,6}], C7=The date and time of the API Response creation
  Row 4: C1=CommandReference, C3=commandRef, C5=M, C6=Type: string
Max Length: 22, C7=The command reference

### Sheet: 204
**Headers (row 1):** 3: Response 204 - No Content
  Row 2: C1=Type, C2=Parent, C3=Element, C4=Parents, C5=Mandatory, C6=Constraint, C7=Description , C8=Track Changes

### Sheet: 400
**Headers (row 1):** 3: Response 400 - Bad Request
  Row 2: C1=Type, C2=Parent, C3=Element, C4=Parents, C5=Mandatory, C6=Constraint, C7=Description , C8=Track Changes
  Row 3: C1=DateTime, C3=dateTime, C5=M, C6=Type: string
Pattern: YYYY-MM-DDTHH:MM:SS[.M{1,6}], C7=The date and time of the API Response creation
  Row 4: C1=ErrorCode, C3=errorCode, C5=M, C6=Type: string, C7=The relevant error code

### Sheet: 401
**Headers (row 1):** 3: Response 401 - Unauthorized
  Row 2: C1=Type, C2=Parent, C3=Element, C4=Parents, C5=Mandatory, C6=Constraint, C7=Description , C8=Track Changes

### Sheet: 403
**Headers (row 1):** 3: Response 403 - Forbidden
  Row 2: C1=Type, C2=Parent, C3=Element, C4=Parents, C5=Mandatory, C6=Constraint, C7=Description , C8=Track Changes

### Sheet: 404
**Headers (row 1):** 3: Response 404 - Not Found
  Row 2: C1=Type, C2=Parent, C3=Element, C4=Parents, C5=Mandatory, C6=Constraint, C7=Description , C8=Track Changes

### Sheet: 429
**Headers (row 1):** 3: Response 429 - Too many requests
  Row 2: C1=Type, C2=Parent, C3=Element, C4=Parents, C5=Mandatory, C6=Constraint, C7=Description , C8=Track Changes

### Sheet: 500
**Headers (row 1):** 3: Response 500 - Internal Server Error
  Row 2: C1=Type, C2=Parent, C3=Element, C4=Parents, C5=Mandatory, C6=Constraint, C7=Description , C8=Track Changes