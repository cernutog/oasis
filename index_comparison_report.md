# Index Comparison Report
**Reference**: `API Templates\$index.xlsm`
**Generated**: `Imported Templates\$index.xlsx`

## Sheet: General Description
- [ ] **Content Differences**:
  - **Row 9** (Excel Line 9):
    - **Unnamed: 1**: Reference=`v20251212` vs Generated=``
  - **Row 10** (Excel Line 10):
    - **Unnamed: 1**: Reference=`EBACL_FPAD_<current_date>_OpenApi<oas_version>_<cu...` vs Generated=``
## Sheet: Headers
- [x] Content Identical
## Sheet: Parameters
- [x] Content Identical
## Sheet: Paths
- [ ] **Shape Mismatch**: Ref (13, 10) vs Gen (13, 9)
- [ ] **Column Mismatch**:
  - Ref: ['Unnamed: 0', 'Paths', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9']
  - Gen: ['Unnamed: 0', 'Paths', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8']
- [ ] **Content Differences**:
  - **Row 3** (Excel Line 3):
    - **Unnamed: 0**: Reference=`accounts_assessments.251111` vs Generated=`create-account-assessment.xlsx`
    - **Unnamed: 2**: Reference=`Account Assessment` vs Generated=`Perform Account Assessment`
  - **Row 4** (Excel Line 4):
    - **Unnamed: 0**: Reference=`accounts_asessments_vop.251111` vs Generated=`create-account-assessment-vop.xlsx`
    - **Unnamed: 2**: Reference=`Account Assessment VOP` vs Generated=`Perform Verification Of Payee (VOP) with Account A...`
    - **Unnamed: 4**: Reference=`Performs a simultaneous Account Assessment and Ver...` vs Generated=`Performs a simultaneous Account Assessment and Ver...`
  - **Row 5** (Excel Line 5):
    - **Unnamed: 0**: Reference=`accounts_asessments_vop_bulk.251111` vs Generated=`create-account-assessment-vop-bulk.xlsx`
    - **Unnamed: 2**: Reference=`Account Assessment VOP Bulk` vs Generated=`Request a Bulk Verification Of Payee (VOP) with Ac...`
  - **Row 6** (Excel Line 6):
    - **Unnamed: 0**: Reference=`accounts_asessments_vop_bulk_{bulkId}.251111` vs Generated=`get-account-assessment-vop-bulk.xlsx`
    - **Unnamed: 2**: Reference=`Account Assessment VOP Bulk BulkId` vs Generated=`Retrieve a Bulk Verification Of Payee (VOP) with A...`
  - **Row 7** (Excel Line 7):
    - **Unnamed: 0**: Reference=`vop_v1_payee_verifications.251111` vs Generated=`postVerificationOfPayeeRequests.xlsx`
    - **Unnamed: 2**: Reference=`Vop Payee-verifications` vs Generated=`Perform Verification Of Payee (VOP)`
    - **Unnamed: 4**: Reference=`Performs a Verification of Payee (VOP) only reques...` vs Generated=`Performs a Verification of Payee (VOP) only reques...`
  - **Row 8** (Excel Line 8):
    - **Unnamed: 0**: Reference=`v1_transactions_assessments.251111` vs Generated=`create-transaction-assessment.xlsx`
    - **Unnamed: 2**: Reference=`Transacyion Assessments` vs Generated=`Create Transaction Assessment`
    - **Unnamed: 4**: Reference=`This operation creates a pre-validation risk asses...` vs Generated=`This operation creates a pre-validation risk asses...`
  - **Row 9** (Excel Line 9):
    - **Unnamed: 0**: Reference=`v1_transactions_investigations.251111` vs Generated=`get-transaction-investigation-by-transaction-key.x...`
    - **Unnamed: 2**: Reference=`Transaction Investigation` vs Generated=`Retrieve Transaction Investigation by Transaction ...`
    - **Unnamed: 4**: Reference=`This operation retrieves a risk assessment for a s...` vs Generated=`This operation retrieves a risk assessment for a s...`
  - **Row 10** (Excel Line 10):
    - **Unnamed: 0**: Reference=`v1_transactions_investigations_{fuid}.251111` vs Generated=`get-transaction-investigation-by-fuid.xlsx`
    - **Unnamed: 2**: Reference=`Transaction Investigation fuid` vs Generated=`Retrieve Transaction Investigation By FUID`
    - **Unnamed: 4**: Reference=`This operation retrieves a risk assessment for a s...` vs Generated=`This operation retrieves a risk assessment for a s...`
  - **Row 11** (Excel Line 11):
    - **Unnamed: 0**: Reference=`v1_transactions_investigations_reports.251111` vs Generated=`create-transaction-investigation-report.xlsx`
    - **Unnamed: 2**: Reference=`Transaction Investigation Reports` vs Generated=`Request Transaction Investigation Report`
  - **Row 12** (Excel Line 12):
    - **Unnamed: 0**: Reference=`v1_transactions_investigations_reports_{reportId}....` vs Generated=`get-transaction-investigation-report.xlsx`
    - **Unnamed: 2**: Reference=`Transaction Investigation Reports reportId` vs Generated=`Retrieve Transaction Investigation Report`
  - **Row 13** (Excel Line 13):
    - **Unnamed: 0**: Reference=`v1_risk-info_feedbacks.251111` vs Generated=`create-feedback-by-fuid.xlsx`
    - **Unnamed: 2**: Reference=`Risk-Info Feedbacks` vs Generated=`Provide Feedback`
  - **Row 14** (Excel Line 14):
    - **Unnamed: 0**: Reference=`v1_eds_local-file.251111` vs Generated=`get-eds-local-file.xlsx`
    - **Unnamed: 2**: Reference=`EDS Local-File` vs Generated=`Retrieve the EDS local file in the format specifie...`
## Sheet: Responses
- [ ] **Shape Mismatch**: Ref (83, 15) vs Gen (43, 15)
- [ ] **Content Differences**:
  - **Row 2** (Excel Line 2):
    - **Description**: Reference=`Structure describing FPAD error response for HTTP ...` vs Generated=`Response`
  - **Row 3** (Excel Line 3):
    - **Description**: Reference=`` vs Generated=`FPAD (API) Response Identifier - A Universal Uniqu...`
    - **Type**: Reference=`header` vs Generated=`string`
    - **Schema Name
(for Type or Items Data Type = 'schema'||'header')**: Reference=`FpadResponseIdentifier` vs Generated=``
    - **Format**: Reference=`` vs Generated=`uuid`
  - **Row 4** (Excel Line 4):
    - **Section**: Reference=`` vs Generated=`content`
    - **Name**: Reference=`x-sandbox-request-name` vs Generated=`text/plain`
    - **Example**: Reference=`OK` vs Generated=``
  - **Row 5** (Excel Line 5):
    - **Section**: Reference=`` vs Generated=`examples`
    - **Name**: Reference=`x-sandbox-request-headers` vs Generated=`Unauthorized`
  - **Row 6** (Excel Line 6):
    - **Section**: Reference=`` vs Generated=`examples`
    - **Name**: Reference=`senderBic` vs Generated=`value`
    - **Parent**: Reference=`x-sandbox-request-headers` vs Generated=`Unauthorized`
    - **Type**: Reference=`string` vs Generated=`str`
    - **Example**: Reference=`FPADITMM` vs Generated=`Unauthorized`
  - **Row 7** (Excel Line 7):
    - **Name**: Reference=`pri` vs Generated=`ErrorResponse_403`
    - **Parent**: Reference=`x-sandbox-request-headers` vs Generated=``
    - **Description**: Reference=`` vs Generated=`Response`
    - **Type**: Reference=`string` vs Generated=``
    - **Example**: Reference=`a206e009-ef37-4040-924d-db758b29b401` vs Generated=``
  - **Row 8** (Excel Line 8):
    - **Section**: Reference=`content` vs Generated=`headers`
    - **Name**: Reference=`text/plain` vs Generated=`fri`
    - **Parent**: Reference=`ErrorResponse_401` vs Generated=`ErrorResponse_403`
    - **Description**: Reference=`Error message` vs Generated=`FPAD (API) Response Identifier - A Universal Uniqu...`
    - **Format**: Reference=`` vs Generated=`uuid`
  - **Row 9** (Excel Line 9):
    - **Section**: Reference=`examples` vs Generated=`content`
    - **Name**: Reference=`Unauthorized` vs Generated=`text/plain`
    - **Parent**: Reference=`text/plain` vs Generated=`ErrorResponse_403`
    - **Type**: Reference=`` vs Generated=`string`
  - **Row 10** (Excel Line 10):
    - **Section**: Reference=`` vs Generated=`examples`
    - **Name**: Reference=`value` vs Generated=`Forbidden`
    - **Parent**: Reference=`Unauthorized` vs Generated=`ErrorResponse_403`
    - **Type**: Reference=`string` vs Generated=``
    - **Example**: Reference=`Unauthorized` vs Generated=``
  - **Row 11** (Excel Line 11):
    - **Section**: Reference=`` vs Generated=`examples`
    - **Name**: Reference=`ErrorResponse_403` vs Generated=`x-sandbox-request-name`
    - **Parent**: Reference=`` vs Generated=`Forbidden`
    - **Description**: Reference=`Structure describing FPAD error response for HTTP ...` vs Generated=``
    - **Type**: Reference=`` vs Generated=`str`
    - **Example**: Reference=`` vs Generated=`OK`
  - **Row 12** (Excel Line 12):
    - **Section**: Reference=`headers` vs Generated=`examples`
    - **Name**: Reference=`fri` vs Generated=`x-sandbox-request-headers`
    - **Parent**: Reference=`ErrorResponse_403` vs Generated=`Forbidden`
    - **Type**: Reference=`header` vs Generated=`object`
    - **Schema Name
(for Type or Items Data Type = 'schema'||'header')**: Reference=`FpadResponseIdentifier` vs Generated=``
  - **Row 13** (Excel Line 13):
    - **Section**: Reference=`` vs Generated=`examples`
    - **Name**: Reference=`x-sandbox-request-name` vs Generated=`senderBic`
    - **Parent**: Reference=`ErrorResponse_403` vs Generated=`x-sandbox-request-headers`
    - **Type**: Reference=`string` vs Generated=`str`
    - **Example**: Reference=`OK` vs Generated=`FPADITMM`
  - **Row 14** (Excel Line 14):
    - **Section**: Reference=`content` vs Generated=`examples`
    - **Name**: Reference=`text/plain` vs Generated=`pri`
    - **Parent**: Reference=`ErrorResponse_403` vs Generated=`x-sandbox-request-headers`
    - **Description**: Reference=`Error message` vs Generated=``
    - **Type**: Reference=`string` vs Generated=`str`
    - **Example**: Reference=`` vs Generated=`a206e009-ef37-4040-924d-db758b29b401`
  - **Row 15** (Excel Line 15):
    - **Name**: Reference=`Forbidden` vs Generated=`value`
    - **Parent**: Reference=`text/plain` vs Generated=`Forbidden`
    - **Type**: Reference=`` vs Generated=`str`
    - **Example**: Reference=`` vs Generated=`Forbidden`
  - **Row 16** (Excel Line 16):
    - **Section**: Reference=`examples` vs Generated=``
    - **Name**: Reference=`x-sandbox-request-name` vs Generated=`ErrorResponse_404`
    - **Parent**: Reference=`Forbidden` vs Generated=``
    - **Description**: Reference=`` vs Generated=`Response`
    - **Type**: Reference=`string` vs Generated=``
    - **Example**: Reference=`OK` vs Generated=``
  - **Row 17** (Excel Line 17):
    - **Section**: Reference=`examples` vs Generated=`headers`
    - **Name**: Reference=`x-sandbox-request-headers` vs Generated=`fri`
    - **Parent**: Reference=`Forbidden` vs Generated=`ErrorResponse_404`
    - **Description**: Reference=`` vs Generated=`FPAD (API) Response Identifier - A Universal Uniqu...`
    - **Type**: Reference=`` vs Generated=`string`
    - **Format**: Reference=`` vs Generated=`uuid`
  - **Row 18** (Excel Line 18):
    - **Section**: Reference=`examples` vs Generated=`content`
    - **Name**: Reference=`senderBic` vs Generated=`text/plain`
    - **Parent**: Reference=`x-sandbox-request-headers` vs Generated=`ErrorResponse_404`
    - **Example**: Reference=`FPADITMM` vs Generated=``
  - **Row 19** (Excel Line 19):
    - **Name**: Reference=`pri` vs Generated=`Not Found`
    - **Parent**: Reference=`x-sandbox-request-headers` vs Generated=`ErrorResponse_404`
    - **Type**: Reference=`string` vs Generated=``
    - **Example**: Reference=`a206e009-ef37-4040-924d-db758b29b401` vs Generated=``
  - **Row 20** (Excel Line 20):
    - **Parent**: Reference=`Forbidden` vs Generated=`Not Found`
    - **Type**: Reference=`string` vs Generated=`str`
    - **Example**: Reference=`Forbidden` vs Generated=`Not Found`
  - **Row 21** (Excel Line 21):
    - **Section**: Reference=`content` vs Generated=``
    - **Name**: Reference=`application/json` vs Generated=`ErrorResponse_409`
    - **Parent**: Reference=`ErrorResponse_403` vs Generated=``
    - **Description**: Reference=`` vs Generated=`Response`
    - **Type**: Reference=`schema` vs Generated=``
    - **Schema Name
(for Type or Items Data Type = 'schema'||'header')**: Reference=`ErrorResponse` vs Generated=``
  - **Row 22** (Excel Line 22):
    - **Section**: Reference=`examples` vs Generated=`headers`
    - **Name**: Reference=`Forbidden (application managed)` vs Generated=`fri`
    - **Parent**: Reference=`application/json` vs Generated=`ErrorResponse_409`
    - **Description**: Reference=`` vs Generated=`FPAD (API) Response Identifier - A Universal Uniqu...`
    - **Type**: Reference=`` vs Generated=`string`
    - **Format**: Reference=`` vs Generated=`uuid`
  - **Row 23** (Excel Line 23):
    - **Section**: Reference=`examples` vs Generated=`content`
    - **Name**: Reference=`x-sandbox-request-name` vs Generated=`application/json`
    - **Parent**: Reference=`Forbidden (application managed)` vs Generated=`ErrorResponse_409`
    - **Type**: Reference=`string` vs Generated=`object`
    - **Schema Name
(for Type or Items Data Type = 'schema'||'header')**: Reference=`` vs Generated=`ErrorResponse`
    - **Example**: Reference=`OK` vs Generated=``
  - **Row 24** (Excel Line 24):
    - **Name**: Reference=`x-sandbox-request-headers` vs Generated=`Conflict`
    - **Parent**: Reference=`Forbidden (application managed)` vs Generated=`ErrorResponse_409`
  - **Row 25** (Excel Line 25):
    - **Name**: Reference=`senderBic` vs Generated=`x-sandbox-request-name`
    - **Parent**: Reference=`x-sandbox-request-headers` vs Generated=`Conflict`
    - **Type**: Reference=`string` vs Generated=`str`
    - **Example**: Reference=`FPADITMM` vs Generated=`OK`
  - **Row 26** (Excel Line 26):
    - **Name**: Reference=`pri` vs Generated=`x-sandbox-request-headers`
    - **Parent**: Reference=`x-sandbox-request-headers` vs Generated=`Conflict`
    - **Type**: Reference=`string` vs Generated=`object`
    - **Example**: Reference=`a206e009-ef37-4040-924d-db758b29b401` vs Generated=``
  - **Row 27** (Excel Line 27):
    - **Name**: Reference=`value` vs Generated=`senderBic`
    - **Parent**: Reference=`Forbidden (application managed)` vs Generated=`x-sandbox-request-headers`
    - **Type**: Reference=`` vs Generated=`str`
    - **Example**: Reference=`` vs Generated=`FPADITMM`
  - **Row 28** (Excel Line 28):
    - **Name**: Reference=`errors` vs Generated=`pri`
    - **Parent**: Reference=`value` vs Generated=`x-sandbox-request-headers`
    - **Type**: Reference=`array` vs Generated=`str`
    - **Items Data Type 
(Array only)**: Reference=`ErrorResponse` vs Generated=``
    - **Example**: Reference=`` vs Generated=`a206e009-ef37-4040-924d-db758b29b401`
  - **Row 29** (Excel Line 29):
    - **Name**: Reference=`dateTime` vs Generated=`value`
    - **Parent**: Reference=`errors` vs Generated=`Conflict`
    - **Type**: Reference=`string` vs Generated=`object`
    - **Example**: Reference=`2023-07-20T14:15:22Z` vs Generated=``
  - **Row 30** (Excel Line 30):
    - **Name**: Reference=`code` vs Generated=`errors`
    - **Parent**: Reference=`errors` vs Generated=`value`
    - **Type**: Reference=`string` vs Generated=`array`
    - **Items Data Type 
(Array only)**: Reference=`` vs Generated=`dict`
    - **Example**: Reference=`E403` vs Generated=``
  - **Row 31** (Excel Line 31):
    - **Section**: Reference=`examples` vs Generated=``
    - **Name**: Reference=`description` vs Generated=`ErrorResponse_429`
    - **Parent**: Reference=`errors` vs Generated=``
    - **Description**: Reference=`` vs Generated=`Response`
    - **Type**: Reference=`string` vs Generated=``
    - **Example**: Reference=`The provided sender BIC is not authorized to perfo...` vs Generated=``
  - **Row 32** (Excel Line 32):
    - **Section**: Reference=`` vs Generated=`headers`
    - **Name**: Reference=`ErrorResponse_404` vs Generated=`fri`
    - **Parent**: Reference=`` vs Generated=`ErrorResponse_429`
    - **Description**: Reference=`Structure describing FPAD error response for HTTP ...` vs Generated=`FPAD (API) Response Identifier - A Universal Uniqu...`
    - **Type**: Reference=`` vs Generated=`string`
    - **Format**: Reference=`` vs Generated=`uuid`
  - **Row 33** (Excel Line 33):
    - **Section**: Reference=`headers` vs Generated=`content`
    - **Name**: Reference=`fri` vs Generated=`text/plain`
    - **Parent**: Reference=`ErrorResponse_404` vs Generated=`ErrorResponse_429`
    - **Type**: Reference=`header` vs Generated=`string`
    - **Schema Name
(for Type or Items Data Type = 'schema'||'header')**: Reference=`FpadResponseIdentifier` vs Generated=``
  - **Row 34** (Excel Line 34):
    - **Section**: Reference=`` vs Generated=`examples`
    - **Name**: Reference=`x-sandbox-request-name` vs Generated=`Too many requests`
    - **Parent**: Reference=`ErrorResponse_404` vs Generated=`ErrorResponse_429`
    - **Type**: Reference=`string` vs Generated=``
    - **Example**: Reference=`OK` vs Generated=``
  - **Row 35** (Excel Line 35):
    - **Section**: Reference=`` vs Generated=`examples`
    - **Name**: Reference=`x-sandbox-request-headers` vs Generated=`value`
    - **Parent**: Reference=`ErrorResponse_404` vs Generated=`Too many requests`
    - **Type**: Reference=`` vs Generated=`str`
    - **Example**: Reference=`` vs Generated=`Too many requests`
  - **Row 36** (Excel Line 36):
    - **Name**: Reference=`senderBic` vs Generated=`ErrorResponse_500`
    - **Parent**: Reference=`x-sandbox-request-headers` vs Generated=``
    - **Description**: Reference=`` vs Generated=`Response`
    - **Type**: Reference=`string` vs Generated=``
    - **Example**: Reference=`FPADITMM` vs Generated=``
  - **Row 37** (Excel Line 37):
    - **Section**: Reference=`` vs Generated=`headers`
    - **Name**: Reference=`pri` vs Generated=`fri`
    - **Parent**: Reference=`x-sandbox-request-headers` vs Generated=`ErrorResponse_500`
    - **Description**: Reference=`` vs Generated=`FPAD (API) Response Identifier - A Universal Uniqu...`
    - **Format**: Reference=`` vs Generated=`uuid`
    - **Example**: Reference=`a206e009-ef37-4040-924d-db758b29b401` vs Generated=``
  - **Row 38** (Excel Line 38):
    - **Parent**: Reference=`ErrorResponse_404` vs Generated=`ErrorResponse_500`
    - **Description**: Reference=`Error message` vs Generated=``
  - **Row 39** (Excel Line 39):
    - **Name**: Reference=`Not Found` vs Generated=`Generic Error`
    - **Parent**: Reference=`text/plain` vs Generated=`ErrorResponse_500`
  - **Row 40** (Excel Line 40):
    - **Name**: Reference=`value` vs Generated=`x-sandbox-request-name`
    - **Parent**: Reference=`Not Found` vs Generated=`Generic Error`
    - **Type**: Reference=`string` vs Generated=`str`
    - **Example**: Reference=`Not Found` vs Generated=`OK`
  - **Row 41** (Excel Line 41):
    - **Section**: Reference=`` vs Generated=`examples`
    - **Name**: Reference=`ErrorResponse_409` vs Generated=`x-sandbox-request-headers`
    - **Parent**: Reference=`` vs Generated=`Generic Error`
    - **Description**: Reference=`Structure describing FPAD error response for HTTP ...` vs Generated=``
    - **Type**: Reference=`` vs Generated=`object`
  - **Row 42** (Excel Line 42):
    - **Section**: Reference=`headers` vs Generated=`examples`
    - **Name**: Reference=`fri` vs Generated=`senderBic`
    - **Parent**: Reference=`ErrorResponse_409` vs Generated=`x-sandbox-request-headers`
    - **Type**: Reference=`header` vs Generated=`str`
    - **Schema Name
(for Type or Items Data Type = 'schema'||'header')**: Reference=`FpadResponseIdentifier` vs Generated=``
    - **Example**: Reference=`` vs Generated=`FPADITMM`
  - **Row 43** (Excel Line 43):
    - **Section**: Reference=`` vs Generated=`examples`
    - **Name**: Reference=`x-sandbox-request-name` vs Generated=`pri`
    - **Parent**: Reference=`ErrorResponse_409` vs Generated=`x-sandbox-request-headers`
    - **Type**: Reference=`string` vs Generated=`str`
    - **Example**: Reference=`OK` vs Generated=`a206e009-ef37-4040-924d-db758b29b401`
  - **Row 44** (Excel Line 44):
    - **Section**: Reference=`content` vs Generated=`examples`
    - **Name**: Reference=`application/json` vs Generated=`value`
    - **Parent**: Reference=`ErrorResponse_409` vs Generated=`Generic Error`
    - **Type**: Reference=`schema` vs Generated=`str`
    - **Schema Name
(for Type or Items Data Type = 'schema'||'header')**: Reference=`ErrorResponse` vs Generated=``
    - **Example**: Reference=`` vs Generated=`Internal Server Error`
  - **Row 45** (Excel Line 45):
    - **Section**: Reference=`examples` vs Generated=``
    - **Name**: Reference=`Conflict` vs Generated=``
    - **Parent**: Reference=`application/json` vs Generated=``
  - **Row 46** (Excel Line 46):
    - **Section**: Reference=`examples` vs Generated=``
    - **Name**: Reference=`x-sandbox-request-name` vs Generated=``
    - **Parent**: Reference=`Conflict` vs Generated=``
    - **Type**: Reference=`string` vs Generated=``
    - **Example**: Reference=`OK` vs Generated=``
  - **Row 47** (Excel Line 47):
    - **Section**: Reference=`examples` vs Generated=``
    - **Name**: Reference=`x-sandbox-request-headers` vs Generated=``
    - **Parent**: Reference=`Conflict` vs Generated=``
  - **Row 48** (Excel Line 48):
    - **Section**: Reference=`examples` vs Generated=``
    - **Name**: Reference=`senderBic` vs Generated=``
    - **Parent**: Reference=`x-sandbox-request-headers` vs Generated=``
    - **Type**: Reference=`string` vs Generated=``
    - **Example**: Reference=`FPADITMM` vs Generated=``
  - **Row 49** (Excel Line 49):
    - **Section**: Reference=`examples` vs Generated=``
    - **Name**: Reference=`pri` vs Generated=``
    - **Parent**: Reference=`x-sandbox-request-headers` vs Generated=``
    - **Type**: Reference=`string` vs Generated=``
    - **Example**: Reference=`a206e009-ef37-4040-924d-db758b29b401` vs Generated=``
  - **Row 50** (Excel Line 50):
    - **Section**: Reference=`examples` vs Generated=``
    - **Name**: Reference=`value` vs Generated=``
    - **Parent**: Reference=`Conflict` vs Generated=``
  - **Row 51** (Excel Line 51):
    - **Section**: Reference=`examples` vs Generated=``
    - **Name**: Reference=`errors` vs Generated=``
    - **Parent**: Reference=`value` vs Generated=``
    - **Type**: Reference=`array` vs Generated=``
    - **Items Data Type 
(Array only)**: Reference=`ErrorResponse` vs Generated=``
  - **Row 52** (Excel Line 52):
    - **Section**: Reference=`examples` vs Generated=``
    - **Name**: Reference=`dateTime` vs Generated=``
    - **Parent**: Reference=`errors` vs Generated=``
    - **Type**: Reference=`string` vs Generated=``
    - **Example**: Reference=`2023-07-20T14:15:22Z` vs Generated=``
  - **Row 53** (Excel Line 53):
    - **Section**: Reference=`examples` vs Generated=``
    - **Name**: Reference=`code` vs Generated=``
    - **Parent**: Reference=`errors` vs Generated=``
    - **Type**: Reference=`string` vs Generated=``
    - **Example**: Reference=`E409` vs Generated=``
  - **Row 54** (Excel Line 54):
    - **Section**: Reference=`examples` vs Generated=``
    - **Name**: Reference=`description` vs Generated=``
    - **Parent**: Reference=`errors` vs Generated=``
    - **Type**: Reference=`string` vs Generated=``
    - **Example**: Reference=`The same PRI has already been sent.` vs Generated=``
  - **Row 55** (Excel Line 55):
    - **Name**: Reference=`ErrorResponse_429` vs Generated=``
    - **Description**: Reference=`Structure describing FPAD error response for HTTP ...` vs Generated=``
  - **Row 56** (Excel Line 56):
    - **Section**: Reference=`headers` vs Generated=``
    - **Name**: Reference=`fri` vs Generated=``
    - **Parent**: Reference=`ErrorResponse_429` vs Generated=``
    - **Type**: Reference=`header` vs Generated=``
    - **Schema Name
(for Type or Items Data Type = 'schema'||'header')**: Reference=`FpadResponseIdentifier` vs Generated=``
  - **Row 57** (Excel Line 57):
    - **Name**: Reference=`x-sandbox-request-name` vs Generated=``
    - **Parent**: Reference=`ErrorResponse_429` vs Generated=``
    - **Type**: Reference=`string` vs Generated=``
    - **Example**: Reference=`OK` vs Generated=``
  - **Row 58** (Excel Line 58):
    - **Name**: Reference=`x-sandbox-request-headers` vs Generated=``
    - **Parent**: Reference=`ErrorResponse_429` vs Generated=``
  - **Row 59** (Excel Line 59):
    - **Name**: Reference=`senderBic` vs Generated=``
    - **Parent**: Reference=`x-sandbox-request-headers` vs Generated=``
    - **Type**: Reference=`string` vs Generated=``
    - **Example**: Reference=`FPADITMM` vs Generated=``
  - **Row 60** (Excel Line 60):
    - **Name**: Reference=`pri` vs Generated=``
    - **Parent**: Reference=`x-sandbox-request-headers` vs Generated=``
    - **Type**: Reference=`string` vs Generated=``
    - **Example**: Reference=`a206e009-ef37-4040-924d-db758b29b401` vs Generated=``
  - **Row 61** (Excel Line 61):
    - **Section**: Reference=`content` vs Generated=``
    - **Name**: Reference=`text/plain` vs Generated=``
    - **Parent**: Reference=`ErrorResponse_429` vs Generated=``
    - **Description**: Reference=`Error message` vs Generated=``
    - **Type**: Reference=`string` vs Generated=``
  - **Row 62** (Excel Line 62):
    - **Section**: Reference=`examples` vs Generated=``
    - **Name**: Reference=`Too many requests` vs Generated=``
    - **Parent**: Reference=`text/plain` vs Generated=``
  - **Row 63** (Excel Line 63):
    - **Section**: Reference=`examples` vs Generated=``
    - **Name**: Reference=`value` vs Generated=``
    - **Parent**: Reference=`Too many requests` vs Generated=``
    - **Type**: Reference=`string` vs Generated=``
    - **Example**: Reference=`Too many requests` vs Generated=``
  - **Row 64** (Excel Line 64):
    - **Name**: Reference=`ErrorResponse_500` vs Generated=``
    - **Description**: Reference=`Structure describing FPAD error response for HTTP ...` vs Generated=``
  - **Row 65** (Excel Line 65):
    - **Section**: Reference=`headers` vs Generated=``
    - **Name**: Reference=`fri` vs Generated=``
    - **Parent**: Reference=`ErrorResponse_500` vs Generated=``
    - **Type**: Reference=`header` vs Generated=``
    - **Schema Name
(for Type or Items Data Type = 'schema'||'header')**: Reference=`FpadResponseIdentifier` vs Generated=``
  - **Row 66** (Excel Line 66):
    - **Name**: Reference=`x-sandbox-request-name` vs Generated=``
    - **Parent**: Reference=`ErrorResponse_500` vs Generated=``
    - **Type**: Reference=`string` vs Generated=``
    - **Example**: Reference=`OK` vs Generated=``
  - **Row 67** (Excel Line 67):
    - **Section**: Reference=`content` vs Generated=``
    - **Name**: Reference=`text/plain` vs Generated=``
    - **Parent**: Reference=`ErrorResponse_500` vs Generated=``
    - **Description**: Reference=`Error message` vs Generated=``
    - **Type**: Reference=`string` vs Generated=``
  - **Row 68** (Excel Line 68):
    - **Section**: Reference=`examples` vs Generated=``
    - **Name**: Reference=`Generic Error` vs Generated=``
    - **Parent**: Reference=`text/plain` vs Generated=``
  - **Row 69** (Excel Line 69):
    - **Section**: Reference=`examples` vs Generated=``
    - **Name**: Reference=`x-sandbox-request-name` vs Generated=``
    - **Parent**: Reference=`Generic Error` vs Generated=``
    - **Type**: Reference=`string` vs Generated=``
    - **Example**: Reference=`OK` vs Generated=``
  - **Row 70** (Excel Line 70):
    - **Section**: Reference=`examples` vs Generated=``
    - **Name**: Reference=`x-sandbox-request-headers` vs Generated=``
    - **Parent**: Reference=`Generic Error` vs Generated=``
  - **Row 71** (Excel Line 71):
    - **Section**: Reference=`examples` vs Generated=``
    - **Name**: Reference=`senderBic` vs Generated=``
    - **Parent**: Reference=`x-sandbox-request-headers` vs Generated=``
    - **Type**: Reference=`string` vs Generated=``
    - **Example**: Reference=`FPADITMM` vs Generated=``
  - **Row 72** (Excel Line 72):
    - **Section**: Reference=`examples` vs Generated=``
    - **Name**: Reference=`pri` vs Generated=``
    - **Parent**: Reference=`x-sandbox-request-headers` vs Generated=``
    - **Type**: Reference=`string` vs Generated=``
    - **Example**: Reference=`a206e009-ef37-4040-924d-db758b29b401` vs Generated=``
  - **Row 73** (Excel Line 73):
    - **Section**: Reference=`examples` vs Generated=``
    - **Name**: Reference=`value` vs Generated=``
    - **Parent**: Reference=`Generic Error` vs Generated=``
    - **Type**: Reference=`string` vs Generated=``
    - **Example**: Reference=`Internal Server Error` vs Generated=``
  - **Row 74** (Excel Line 74):
    - **Section**: Reference=`content` vs Generated=``
    - **Name**: Reference=`application/json` vs Generated=``
    - **Parent**: Reference=`ErrorResponse_500` vs Generated=``
    - **Type**: Reference=`schema` vs Generated=``
    - **Schema Name
(for Type or Items Data Type = 'schema'||'header')**: Reference=`ErrorResponse` vs Generated=``
  - **Row 75** (Excel Line 75):
    - **Section**: Reference=`examples` vs Generated=``
    - **Name**: Reference=`Generic Error (application managed)` vs Generated=``
    - **Parent**: Reference=`application/json` vs Generated=``
  - **Row 76** (Excel Line 76):
    - **Section**: Reference=`examples` vs Generated=``
    - **Name**: Reference=`x-sandbox-request-name` vs Generated=``
    - **Parent**: Reference=`Generic Error (application managed)` vs Generated=``
    - **Type**: Reference=`string` vs Generated=``
    - **Example**: Reference=`OK` vs Generated=``
  - **Row 77** (Excel Line 77):
    - **Section**: Reference=`examples` vs Generated=``
    - **Name**: Reference=`x-sandbox-request-headers` vs Generated=``
    - **Parent**: Reference=`Generic Error (application managed)` vs Generated=``
  - **Row 78** (Excel Line 78):
    - **Section**: Reference=`examples` vs Generated=``
    - **Name**: Reference=`senderBic` vs Generated=``
    - **Parent**: Reference=`x-sandbox-request-headers` vs Generated=``
    - **Type**: Reference=`string` vs Generated=``
    - **Example**: Reference=`FPADITMM` vs Generated=``
  - **Row 79** (Excel Line 79):
    - **Section**: Reference=`examples` vs Generated=``
    - **Name**: Reference=`pri` vs Generated=``
    - **Parent**: Reference=`x-sandbox-request-headers` vs Generated=``
    - **Type**: Reference=`string` vs Generated=``
    - **Example**: Reference=`a206e009-ef37-4040-924d-db758b29b401` vs Generated=``
  - **Row 80** (Excel Line 80):
    - **Section**: Reference=`examples` vs Generated=``
    - **Name**: Reference=`value` vs Generated=``
    - **Parent**: Reference=`Generic Error (application managed)` vs Generated=``
  - **Row 81** (Excel Line 81):
    - **Section**: Reference=`examples` vs Generated=``
    - **Name**: Reference=`errors` vs Generated=``
    - **Parent**: Reference=`value` vs Generated=``
    - **Type**: Reference=`array` vs Generated=``
    - **Items Data Type 
(Array only)**: Reference=`ErrorResponse` vs Generated=``
  - **Row 82** (Excel Line 82):
    - **Section**: Reference=`examples` vs Generated=``
    - **Name**: Reference=`dateTime` vs Generated=``
    - **Parent**: Reference=`errors` vs Generated=``
    - **Type**: Reference=`string` vs Generated=``
    - **Example**: Reference=`2023-07-20T14:15:22Z` vs Generated=``
  - **Row 83** (Excel Line 83):
    - **Section**: Reference=`examples` vs Generated=``
    - **Name**: Reference=`code` vs Generated=``
    - **Parent**: Reference=`errors` vs Generated=``
    - **Type**: Reference=`string` vs Generated=``
    - **Example**: Reference=`E500` vs Generated=``
  - **Row 84** (Excel Line 84):
    - **Section**: Reference=`examples` vs Generated=``
    - **Name**: Reference=`description` vs Generated=``
    - **Parent**: Reference=`errors` vs Generated=``
    - **Type**: Reference=`string` vs Generated=``
    - **Example**: Reference=`Application error.` vs Generated=``
## Sheet: Schemas
- [ ] **Shape Mismatch**: Ref (178, 14) vs Gen (179, 14)
- [ ] **Content Differences**:
  - **Row 7** (Excel Line 7):
    - **Format**: Reference=`double` vs Generated=``
    - **Max  
Value/Length/Item**: Reference=`999999999999.99` vs Generated=``
    - **Example**: Reference=`1048.27` vs Generated=``
  - **Row 12** (Excel Line 12):
    - **Description**: Reference=`BIC of the Agent managing the Debtor's Account pre...` vs Generated=``
  - **Row 13** (Excel Line 13):
    - **Description**: Reference=`IBAN of the debtor` vs Generated=``
  - **Row 15** (Excel Line 15):
    - **Description**: Reference=`BIC of the Agent managing the Creditor's Account p...` vs Generated=``
  - **Row 16** (Excel Line 16):
    - **Description**: Reference=`IBAN identifies the Creditor's Account present in ...` vs Generated=``
  - **Row 17** (Excel Line 17):
    - **Description**: Reference=`Amount of the potential transaction that has to be...` vs Generated=``
  - **Row 18** (Excel Line 18):
    - **Description**: Reference=`Currency of the Amount of the potential transactio...` vs Generated=``
  - **Row 19** (Excel Line 19):
    - **Description**: Reference=`Reference date and time of the potential transacti...` vs Generated=``
  - **Row 22** (Excel Line 22):
    - **Regex**: Reference=`[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}([A-Z0-9]{3,3}...` vs Generated=``
    - **Example**: Reference=`FPADITMMXXX` vs Generated=``
  - **Row 23** (Excel Line 23):
    - **Min  
Value/Length/Item**: Reference=`8.0` vs Generated=``
    - **Max  
Value/Length/Item**: Reference=`8.0` vs Generated=``
    - **Regex**: Reference=`[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}` vs Generated=``
    - **Example**: Reference=`FPADITMM` vs Generated=``
  - **Row 24** (Excel Line 24):
    - **Regex**: Reference=`^[A-Z0-9]{4,4}[A-Z]{2,2}[A-Z0-9]{2,2}([A-Z0-9]{3,3...` vs Generated=``
    - **Example**: Reference=`ABCDBEBBFIM` vs Generated=``
  - **Row 25** (Excel Line 25):
    - **Regex**: Reference=`[A-Z]{3}` vs Generated=``
    - **Example**: Reference=`EUR` vs Generated=``
  - **Row 26** (Excel Line 26):
    - **Format**: Reference=`date-time` vs Generated=``
    - **Example**: Reference=`2019-08-24T14:15:22Z` vs Generated=``
  - **Row 29** (Excel Line 29):
    - **Parent**: Reference=`errors` vs Generated=`items`
  - **Row 30** (Excel Line 30):
    - **Parent**: Reference=`errors` vs Generated=`items`
  - **Row 31** (Excel Line 31):
    - **Parent**: Reference=`errors` vs Generated=`items`
  - **Row 32** (Excel Line 32):
    - **Format**: Reference=`uuid` vs Generated=``
    - **Example**: Reference=`4ac04478-d70d-4d25-8bde-f2ad0001093d` vs Generated=``
  - **Row 34** (Excel Line 34):
    - **Description**: Reference=`Unique and unambiguous identification of an organi...` vs Generated=``
  - **Row 35** (Excel Line 35):
    - **Description**: Reference=`An entry provided by an external ISO code list.` vs Generated=``
  - **Row 36** (Excel Line 36):
    - **Description**: Reference=`A scheme name defined in a proprietary way.` vs Generated=``
  - **Row 37** (Excel Line 37):
    - **Description**: Reference=`Issuer of the identification.` vs Generated=``
  - **Row 38** (Excel Line 38):
    - **Example**: Reference=`{'rel': 'next', 'href': '/transactions/investigati...` vs Generated=``
  - **Row 41** (Excel Line 41):
    - **Regex**: Reference=`[A-Z]{2,2}[0-9]{2,2}[a-zA-Z0-9]{1,30}` vs Generated=``
    - **Example**: Reference=`IT78K0300203280111271851199` vs Generated=``
  - **Row 42** (Excel Line 42):
    - **Regex**: Reference=`^[A-Z]{2,2}[0-9]{2,2}[a-zA-Z0-9]{1,30}$` vs Generated=``
  - **Row 43** (Excel Line 43):
    - **Example**: Reference=`{'instructingAgentBic': 'FPADITMM', 'instructedAge...` vs Generated=``
  - **Row 44** (Excel Line 44):
    - **Description**: Reference=`BIC of the instructing Agent for the transaction.` vs Generated=``
  - **Row 45** (Excel Line 45):
    - **Description**: Reference=`BIC of the instructed Agent for the transaction.` vs Generated=``
  - **Row 49** (Excel Line 49):
    - **Description**: Reference=`BIC of the Agent managing the Debtor's Account pre...` vs Generated=``
  - **Row 50** (Excel Line 50):
    - **Description**: Reference=`IBAN of the debtor.` vs Generated=``
  - **Row 52** (Excel Line 52):
    - **Description**: Reference=`BIC of the Agent managing the Creditor's Account p...` vs Generated=``
  - **Row 53** (Excel Line 53):
    - **Description**: Reference=`IBAN identifies the Creditor's Account present in ...` vs Generated=``
  - **Row 54** (Excel Line 54):
    - **Description**: Reference=`Amount of the transaction.` vs Generated=``
  - **Row 55** (Excel Line 55):
    - **Description**: Reference=`Currency of the Amount of the transaction.` vs Generated=``
  - **Row 56** (Excel Line 56):
    - **Description**: Reference=`Reference date and time of the transaction._x000D_...` vs Generated=``
  - **Row 59** (Excel Line 59):
    - **Regex**: Reference=`^[A-Z0-9]{18}[0-9]{2}$` vs Generated=``
    - **Example**: Reference=`549300DTUYXVMJXZNY75` vs Generated=``
  - **Row 60** (Excel Line 60):
    - **Allowed value**: Reference=`FORMAT_ERROR,CLIENT_INVALID,CLIENT_INCONSISTENT,TI...` vs Generated=``
  - **Row 61** (Excel Line 61):
    - **Min  
Value/Length/Item**: Reference=`0.0` vs Generated=``
    - **Max  
Value/Length/Item**: Reference=`35.0` vs Generated=``
  - **Row 62** (Excel Line 62):
    - **Min  
Value/Length/Item**: Reference=`0.0` vs Generated=``
    - **Max  
Value/Length/Item**: Reference=`70.0` vs Generated=``
  - **Row 63** (Excel Line 63):
    - **Min  
Value/Length/Item**: Reference=`0.0` vs Generated=``
    - **Max  
Value/Length/Item**: Reference=`140.0` vs Generated=``
  - **Row 64** (Excel Line 64):
    - **Min  
Value/Length/Item**: Reference=`0.0` vs Generated=``
    - **Max  
Value/Length/Item**: Reference=`256.0` vs Generated=``
  - **Row 65** (Excel Line 65):
    - **Min  
Value/Length/Item**: Reference=`0.0` vs Generated=``
    - **Max  
Value/Length/Item**: Reference=`500.0` vs Generated=``
  - **Row 66** (Excel Line 66):
    - **Example**: Reference=`{'messageType': 'WARNING', 'messageCode': 'W001', ...` vs Generated=``
  - **Row 67** (Excel Line 67):
    - **Allowed value**: Reference=`INFO,WARNING,ERROR` vs Generated=`INFO, WARNING, ERROR`
  - **Row 73** (Excel Line 73):
    - **Max  
Value/Length/Item**: Reference=`20.0` vs Generated=``
  - **Row 74** (Excel Line 74):
    - **Max  
Value/Length/Item**: Reference=`15.0` vs Generated=``
  - **Row 75** (Excel Line 75):
    - **Max  
Value/Length/Item**: Reference=`10.0` vs Generated=``
  - **Row 76** (Excel Line 76):
    - **Max  
Value/Length/Item**: Reference=`120.0` vs Generated=``
  - **Row 77** (Excel Line 77):
    - **Allowed value**: Reference=`MTCH,CMTC,NMTC,NOAP` vs Generated=``
  - **Row 78** (Excel Line 78):
    - **Allowed value**: Reference=`BANK,CBID,CHID,CINC,COID,CUST,DUNS,EMPL,GS1G,SREN,...` vs Generated=``
    - **Example**: Reference=`BOID` vs Generated=``
  - **Row 83** (Excel Line 83):
    - **Items Data Type 
(Array only)**: Reference=`HateoasBlock` vs Generated=`schema`
    - **Schema Name
(if Type = schema)**: Reference=`` vs Generated=`HateoasBlock`
  - **Row 84** (Excel Line 84):
    - **Allowed value**: Reference=`MTCH,NMTC,NOAP` vs Generated=``
  - **Row 89** (Excel Line 89):
    - **Description**: Reference=`Legal Entity Identifier.` vs Generated=``
  - **Row 91** (Excel Line 91):
    - **Items Data Type 
(Array only)**: Reference=`GenericOrganisationIdentification` vs Generated=`schema`
    - **Schema Name
(if Type = schema)**: Reference=`` vs Generated=`GenericOrganisationIdentification`
  - **Row 97** (Excel Line 97):
    - **Items Data Type 
(Array only)**: Reference=`object` vs Generated=``
  - **Row 98** (Excel Line 98):
    - **Name**: Reference=`modelName` vs Generated=`RiskInfoArray`
    - **Description**: Reference=`` vs Generated=`The RiskInfoArray is an array where each item repr...`
    - **Type**: Reference=`schema` vs Generated=`array`
    - **Items Data Type 
(Array only)**: Reference=`` vs Generated=`object`
    - **Schema Name
(if Type = schema)**: Reference=`ModelName` vs Generated=``
  - **Row 99** (Excel Line 99):
    - **Name**: Reference=`modelVersion` vs Generated=`modelName`
    - **Parent**: Reference=`RiskInfoArray` vs Generated=`items`
    - **Schema Name
(if Type = schema)**: Reference=`ModelVersion` vs Generated=`ModelName`
    - **Mandatory**: Reference=`` vs Generated=`M`
  - **Row 100** (Excel Line 100):
    - **Name**: Reference=`modelOutcome` vs Generated=`modelVersion`
    - **Parent**: Reference=`RiskInfoArray` vs Generated=`items`
    - **Schema Name
(if Type = schema)**: Reference=`ModelOutcome` vs Generated=`ModelVersion`
  - **Row 101** (Excel Line 101):
    - **Name**: Reference=`modelNarratives` vs Generated=`modelOutcome`
    - **Parent**: Reference=`RiskInfoArray` vs Generated=`items`
    - **Schema Name
(if Type = schema)**: Reference=`ModelNarratives` vs Generated=`ModelOutcome`
  - **Row 102** (Excel Line 102):
    - **Name**: Reference=`ServiceType` vs Generated=`modelNarratives`
    - **Parent**: Reference=`` vs Generated=`items`
    - **Description**: Reference=`EBA CLEARING Service type (SCT, SCTInst).` vs Generated=``
    - **Type**: Reference=`string` vs Generated=`schema`
    - **Schema Name
(if Type = schema)**: Reference=`` vs Generated=`ModelNarratives`
    - **Allowed value**: Reference=`SCT,SCTInst` vs Generated=``
  - **Row 103** (Excel Line 103):
    - **Name**: Reference=`ShortErrorResponse` vs Generated=`ServiceType`
    - **Description**: Reference=`Compact version of ErrorResponse structure, used i...` vs Generated=`EBA CLEARING Service type (SCT, SCTInst).`
    - **Type**: Reference=`object` vs Generated=`string`
  - **Row 104** (Excel Line 104):
    - **Name**: Reference=`xid` vs Generated=`ShortErrorResponse`
    - **Parent**: Reference=`ShortErrorResponse` vs Generated=``
    - **Description**: Reference=`The same *xid* sent in the bulk request, for match...` vs Generated=`Compact version of ErrorResponse structure, used i...`
    - **Type**: Reference=`string` vs Generated=`object`
    - **Format**: Reference=`uuid` vs Generated=``
  - **Row 105** (Excel Line 105):
    - **Name**: Reference=`err` vs Generated=`xid`
    - **Description**: Reference=`` vs Generated=`The same *xid* sent in the bulk request, for match...`
    - **Type**: Reference=`array` vs Generated=`string`
    - **Items Data Type 
(Array only)**: Reference=`object` vs Generated=``
    - **Format**: Reference=`` vs Generated=`uuid`
    - **Min  
Value/Length/Item**: Reference=`1.0` vs Generated=``
  - **Row 106** (Excel Line 106):
    - **Name**: Reference=`dt` vs Generated=`err`
    - **Parent**: Reference=`err` vs Generated=`ShortErrorResponse`
    - **Type**: Reference=`schema` vs Generated=`array`
    - **Items Data Type 
(Array only)**: Reference=`` vs Generated=`object`
    - **Schema Name
(if Type = schema)**: Reference=`DateTime` vs Generated=``
    - **Mandatory**: Reference=`M` vs Generated=``
    - **Min  
Value/Length/Item**: Reference=`` vs Generated=`1.0`
  - **Row 107** (Excel Line 107):
    - **Name**: Reference=`code` vs Generated=`dt`
    - **Parent**: Reference=`err` vs Generated=`items`
    - **Description**: Reference=`A four character string representing the FPAD erro...` vs Generated=``
    - **Type**: Reference=`string` vs Generated=`schema`
    - **Schema Name
(if Type = schema)**: Reference=`` vs Generated=`DateTime`
    - **Min  
Value/Length/Item**: Reference=`4.0` vs Generated=``
    - **Max  
Value/Length/Item**: Reference=`4.0` vs Generated=``
  - **Row 108** (Excel Line 108):
    - **Name**: Reference=`desc` vs Generated=`code`
    - **Parent**: Reference=`err` vs Generated=`items`
    - **Description**: Reference=`A string containing the error description.` vs Generated=`A four character string representing the FPAD erro...`
    - **Min  
Value/Length/Item**: Reference=`` vs Generated=`4.0`
    - **Max  
Value/Length/Item**: Reference=`` vs Generated=`4.0`
  - **Row 109** (Excel Line 109):
    - **Name**: Reference=`ShortMessage` vs Generated=`desc`
    - **Parent**: Reference=`` vs Generated=`items`
    - **Description**: Reference=`Basic structure for reporting messages. Typically ...` vs Generated=`A string containing the error description.`
    - **Type**: Reference=`object` vs Generated=`string`
    - **Mandatory**: Reference=`` vs Generated=`M`
  - **Row 110** (Excel Line 110):
    - **Name**: Reference=`type` vs Generated=`ShortMessage`
    - **Parent**: Reference=`ShortMessage` vs Generated=``
    - **Description**: Reference=`Message type.` vs Generated=`Basic structure for reporting messages. Typically ...`
    - **Type**: Reference=`string` vs Generated=`object`
    - **Mandatory**: Reference=`M` vs Generated=``
    - **Allowed value**: Reference=`INFO,WARNING,ERROR` vs Generated=``
  - **Row 111** (Excel Line 111):
    - **Name**: Reference=`code` vs Generated=`type`
    - **Description**: Reference=`Message code.` vs Generated=`Message type.`
    - **Allowed value**: Reference=`` vs Generated=`INFO, WARNING, ERROR`
  - **Row 112** (Excel Line 112):
    - **Name**: Reference=`text` vs Generated=`code`
    - **Description**: Reference=`Full textual description of the message.` vs Generated=`Message code.`
  - **Row 113** (Excel Line 113):
    - **Name**: Reference=`TransactionInvestigationReportFilter` vs Generated=`text`
    - **Parent**: Reference=`` vs Generated=`ShortMessage`
    - **Description**: Reference=`Data structure user as extraction filter for repor...` vs Generated=`Full textual description of the message.`
    - **Type**: Reference=`object` vs Generated=`string`
    - **Mandatory**: Reference=`` vs Generated=`M`
  - **Row 114** (Excel Line 114):
    - **Name**: Reference=`instructingAgentBic` vs Generated=`TransactionInvestigationReportFilter`
    - **Parent**: Reference=`TransactionInvestigationReportFilter` vs Generated=``
    - **Description**: Reference=`BIC of the instructing agent.` vs Generated=`Data structure user as extraction filter for repor...`
    - **Type**: Reference=`schema` vs Generated=`object`
    - **Schema Name
(if Type = schema)**: Reference=`Bic8` vs Generated=``
  - **Row 115** (Excel Line 115):
    - **Name**: Reference=`instructedAgentBic` vs Generated=`instructingAgentBic`
    - **Description**: Reference=`BIC of the instructed agent.` vs Generated=``
  - **Row 116** (Excel Line 116):
    - **Name**: Reference=`serviceType` vs Generated=`instructedAgentBic`
    - **Description**: Reference=`Service Type of considered transactions.` vs Generated=``
    - **Schema Name
(if Type = schema)**: Reference=`ServiceType` vs Generated=`Bic8`
  - **Row 117** (Excel Line 117):
    - **Name**: Reference=`transactionId` vs Generated=`serviceType`
    - **Description**: Reference=`Unique identifier of the transaction.` vs Generated=``
    - **Type**: Reference=`string` vs Generated=`schema`
    - **Schema Name
(if Type = schema)**: Reference=`` vs Generated=`ServiceType`
    - **Max  
Value/Length/Item**: Reference=`35.0` vs Generated=``
  - **Row 118** (Excel Line 118):
    - **Name**: Reference=`debtorName` vs Generated=`transactionId`
    - **Description**: Reference=`Name associated with the Debtor's Account present ...` vs Generated=`Unique identifier of the transaction.`
    - **Max  
Value/Length/Item**: Reference=`` vs Generated=`35.0`
  - **Row 119** (Excel Line 119):
    - **Name**: Reference=`debtorBic` vs Generated=`debtorName`
    - **Description**: Reference=`BIC of the Agent managing the Debtor's Account pre...` vs Generated=`Name associated with the Debtor's Account present ...`
    - **Type**: Reference=`schema` vs Generated=`string`
    - **Schema Name
(if Type = schema)**: Reference=`Bic` vs Generated=``
  - **Row 120** (Excel Line 120):
    - **Name**: Reference=`debtorIban` vs Generated=`debtorBic`
    - **Description**: Reference=`IBAN of the debtor` vs Generated=``
    - **Schema Name
(if Type = schema)**: Reference=`Iban` vs Generated=`Bic`
  - **Row 121** (Excel Line 121):
    - **Name**: Reference=`creditorName` vs Generated=`debtorIban`
    - **Description**: Reference=`Name associated with the Creditor's Account presen...` vs Generated=``
    - **Type**: Reference=`string` vs Generated=`schema`
    - **Schema Name
(if Type = schema)**: Reference=`` vs Generated=`Iban`
  - **Row 122** (Excel Line 122):
    - **Name**: Reference=`creditorBic` vs Generated=`creditorName`
    - **Description**: Reference=`BIC of the Agent managing the Creditor's Account p...` vs Generated=`Name associated with the Creditor's Account presen...`
    - **Type**: Reference=`schema` vs Generated=`string`
    - **Schema Name
(if Type = schema)**: Reference=`Bic` vs Generated=``
  - **Row 123** (Excel Line 123):
    - **Name**: Reference=`creditorIban` vs Generated=`creditorBic`
    - **Description**: Reference=`IBAN identifies the Creditor's Account present in ...` vs Generated=``
    - **Schema Name
(if Type = schema)**: Reference=`Iban` vs Generated=`Bic`
  - **Row 124** (Excel Line 124):
    - **Name**: Reference=`minAmount` vs Generated=`creditorIban`
    - **Description**: Reference=`Minumum amount of the transaction.` vs Generated=``
    - **Schema Name
(if Type = schema)**: Reference=`Amount` vs Generated=`Iban`
  - **Row 125** (Excel Line 125):
    - **Name**: Reference=`maxAmount` vs Generated=`minAmount`
    - **Description**: Reference=`Maximum amount of the transaction.` vs Generated=``
  - **Row 126** (Excel Line 126):
    - **Name**: Reference=`currency` vs Generated=`maxAmount`
    - **Description**: Reference=`Currency of the Amount of the transaction.` vs Generated=``
    - **Schema Name
(if Type = schema)**: Reference=`Currency` vs Generated=`Amount`
  - **Row 127** (Excel Line 127):
    - **Name**: Reference=`minReferenceDateTime` vs Generated=`currency`
    - **Description**: Reference=`Minimum reference date and time._x000D_
Reference ...` vs Generated=``
    - **Schema Name
(if Type = schema)**: Reference=`DateTime` vs Generated=`Currency`
  - **Row 128** (Excel Line 128):
    - **Name**: Reference=`maxReferenceDateTime` vs Generated=`minReferenceDateTime`
    - **Description**: Reference=`Maximum reference date and time. It cannot exceed ...` vs Generated=``
  - **Row 129** (Excel Line 129):
    - **Name**: Reference=`minGeneralRiskIndicator` vs Generated=`maxReferenceDateTime`
    - **Description**: Reference=`Minimum value admitted as General Risk Indicator (...` vs Generated=``
    - **Type**: Reference=`number` vs Generated=`schema`
    - **Schema Name
(if Type = schema)**: Reference=`` vs Generated=`DateTime`
  - **Row 130** (Excel Line 130):
    - **Name**: Reference=`maxGeneralRiskIndicator` vs Generated=`minGeneralRiskIndicator`
    - **Description**: Reference=`Maximum value admitted as General Risk Indicator (...` vs Generated=`Minimum value admitted as General Risk Indicator (...`
  - **Row 131** (Excel Line 131):
    - **Name**: Reference=`TransactionKey` vs Generated=`maxGeneralRiskIndicator`
    - **Parent**: Reference=`` vs Generated=`TransactionInvestigationReportFilter`
    - **Description**: Reference=`Basic structure with all key elements identifìying...` vs Generated=`Maximum value admitted as General Risk Indicator (...`
    - **Type**: Reference=`object` vs Generated=`number`
    - **Example**: Reference=`{'serviceType': 'SCT', 'debtorBic': 'FPADITMMXXX',...` vs Generated=``
  - **Row 132** (Excel Line 132):
    - **Name**: Reference=`serviceType` vs Generated=`TransactionKey`
    - **Parent**: Reference=`TransactionKey` vs Generated=``
    - **Description**: Reference=`EBA CLEARING Service type associated with the tran...` vs Generated=`Basic structure with all key elements identifìying...`
    - **Type**: Reference=`schema` vs Generated=`object`
    - **Schema Name
(if Type = schema)**: Reference=`ServiceType` vs Generated=``
    - **Mandatory**: Reference=`M` vs Generated=``
  - **Row 133** (Excel Line 133):
    - **Name**: Reference=`debtorBic` vs Generated=`serviceType`
    - **Description**: Reference=`BIC of the Agent managing the Debtor's Account.` vs Generated=``
    - **Schema Name
(if Type = schema)**: Reference=`Bic` vs Generated=`ServiceType`
  - **Row 134** (Excel Line 134):
    - **Name**: Reference=`transactionId` vs Generated=`debtorBic`
    - **Description**: Reference=`Identifier of the transaction, unique for the Debt...` vs Generated=``
    - **Type**: Reference=`string` vs Generated=`schema`
    - **Schema Name
(if Type = schema)**: Reference=`` vs Generated=`Bic`
    - **Max  
Value/Length/Item**: Reference=`35.0` vs Generated=``
  - **Row 135** (Excel Line 135):
    - **Name**: Reference=`referenceDateTime` vs Generated=`transactionId`
    - **Description**: Reference=`This attribute refers to:

- Settlement date for S...` vs Generated=`Identifier of the transaction, unique for the Debt...`
    - **Type**: Reference=`schema` vs Generated=`string`
    - **Schema Name
(if Type = schema)**: Reference=`DateTime` vs Generated=``
    - **Max  
Value/Length/Item**: Reference=`` vs Generated=`35.0`
  - **Row 136** (Excel Line 136):
    - **Name**: Reference=`VerificationOfPayeeResponse` vs Generated=`referenceDateTime`
    - **Parent**: Reference=`` vs Generated=`TransactionKey`
    - **Description**: Reference=`Separation of the two kinds of responses in differ...` vs Generated=``
    - **Type**: Reference=`object` vs Generated=`schema`
    - **Schema Name
(if Type = schema)**: Reference=`` vs Generated=`DateTime`
    - **Mandatory**: Reference=`` vs Generated=`M`
  - **Row 137** (Excel Line 137):
    - **Name**: Reference=`partyNameMatch` vs Generated=`VerificationOfPayeeResponse`
    - **Parent**: Reference=`VerificationOfPayeeResponse` vs Generated=``
    - **Description**: Reference=`` vs Generated=`Separation of the two kinds of responses in differ...`
    - **Type**: Reference=`schema` vs Generated=`object`
    - **Schema Name
(if Type = schema)**: Reference=`NameMatchType` vs Generated=``
  - **Row 138** (Excel Line 138):
    - **Name**: Reference=`partyIdMatch` vs Generated=`partyNameMatch`
    - **Schema Name
(if Type = schema)**: Reference=`PartyIdMatchType` vs Generated=`NameMatchType`
  - **Row 139** (Excel Line 139):
    - **Name**: Reference=`matchedName` vs Generated=`partyIdMatch`
    - **Schema Name
(if Type = schema)**: Reference=`Max140Text` vs Generated=`PartyIdMatchType`
  - **Row 140** (Excel Line 140):
    - **Name**: Reference=`VerificationOfPayeeError` vs Generated=`matchedName`
    - **Parent**: Reference=`` vs Generated=`VerificationOfPayeeResponse`
    - **Type**: Reference=`object` vs Generated=`schema`
    - **Schema Name
(if Type = schema)**: Reference=`` vs Generated=`Max140Text`
  - **Row 141** (Excel Line 141):
    - **Name**: Reference=`type` vs Generated=`VerificationOfPayeeError`
    - **Parent**: Reference=`VerificationOfPayeeError` vs Generated=``
    - **Type**: Reference=`schema` vs Generated=`object`
    - **Schema Name
(if Type = schema)**: Reference=`Max70Text` vs Generated=``
    - **Mandatory**: Reference=`M` vs Generated=``
  - **Row 142** (Excel Line 142):
    - **Name**: Reference=`code` vs Generated=`type`
    - **Description**: Reference=`An entry provided by an external ISO code list.` vs Generated=``
    - **Schema Name
(if Type = schema)**: Reference=`MessageCode` vs Generated=`Max70Text`
  - **Row 143** (Excel Line 143):
    - **Name**: Reference=`title` vs Generated=`code`
    - **Schema Name
(if Type = schema)**: Reference=`Max70Text` vs Generated=`MessageCode`
    - **Mandatory**: Reference=`` vs Generated=`M`
  - **Row 144** (Excel Line 144):
    - **Name**: Reference=`status` vs Generated=`title`
    - **Type**: Reference=`integer` vs Generated=`schema`
    - **Schema Name
(if Type = schema)**: Reference=`` vs Generated=`Max70Text`
    - **Allowed value**: Reference=`400,401,500` vs Generated=``
  - **Row 145** (Excel Line 145):
    - **Name**: Reference=`detail` vs Generated=`status`
    - **Type**: Reference=`schema` vs Generated=`integer`
    - **Schema Name
(if Type = schema)**: Reference=`Max500Text` vs Generated=``
    - **Allowed value**: Reference=`` vs Generated=`400, 401, 500`
  - **Row 146** (Excel Line 146):
    - **Name**: Reference=`instance` vs Generated=`detail`
    - **Schema Name
(if Type = schema)**: Reference=`Max256Text` vs Generated=`Max500Text`
  - **Row 147** (Excel Line 147):
    - **Name**: Reference=`VerificationOfPayeeRequest` vs Generated=`instance`
    - **Parent**: Reference=`` vs Generated=`VerificationOfPayeeError`
    - **Type**: Reference=`object` vs Generated=`schema`
    - **Schema Name
(if Type = schema)**: Reference=`` vs Generated=`Max256Text`
  - **Row 148** (Excel Line 148):
    - **Name**: Reference=`party` vs Generated=`VerificationOfPayeeRequest`
    - **Parent**: Reference=`VerificationOfPayeeRequest` vs Generated=``
    - **Type**: Reference=`schema` vs Generated=`object`
    - **Schema Name
(if Type = schema)**: Reference=`PartyType` vs Generated=``
    - **Mandatory**: Reference=`M` vs Generated=``
  - **Row 149** (Excel Line 149):
    - **Name**: Reference=`partyAccount` vs Generated=`party`
    - **Schema Name
(if Type = schema)**: Reference=`AccountType` vs Generated=`PartyType`
  - **Row 150** (Excel Line 150):
    - **Name**: Reference=`partyAgent` vs Generated=`partyAccount`
    - **Schema Name
(if Type = schema)**: Reference=`AgentType` vs Generated=`AccountType`
  - **Row 151** (Excel Line 151):
    - **Name**: Reference=`unstructuredRemittanceInformation` vs Generated=`partyAgent`
    - **Description**: Reference=`Additional information about AT-C001 sent by the R...` vs Generated=``
    - **Type**: Reference=`array` vs Generated=`schema`
    - **Items Data Type 
(Array only)**: Reference=`Max140Text` vs Generated=``
    - **Schema Name
(if Type = schema)**: Reference=`` vs Generated=`AgentType`
    - **Mandatory**: Reference=`` vs Generated=`M`
  - **Row 152** (Excel Line 152):
    - **Name**: Reference=`requestingAgent` vs Generated=`unstructuredRemittanceInformation`
    - **Description**: Reference=`` vs Generated=`Additional information about AT-C001 sent by the R...`
    - **Type**: Reference=`schema` vs Generated=`array`
    - **Items Data Type 
(Array only)**: Reference=`` vs Generated=`schema`
    - **Schema Name
(if Type = schema)**: Reference=`AgentType` vs Generated=`Max140Text`
    - **Mandatory**: Reference=`M` vs Generated=``
  - **Row 153** (Excel Line 153):
    - **Name**: Reference=`VopBulkIdentification` vs Generated=`requestingAgent`
    - **Parent**: Reference=`` vs Generated=`VerificationOfPayeeRequest`
    - **Description**: Reference=`This object contains all info about the *identific...` vs Generated=``
    - **Type**: Reference=`object` vs Generated=`schema`
    - **Schema Name
(if Type = schema)**: Reference=`` vs Generated=`AgentType`
    - **Mandatory**: Reference=`` vs Generated=`M`
  - **Row 154** (Excel Line 154):
    - **Name**: Reference=`lei` vs Generated=`VopBulkIdentification`
    - **Parent**: Reference=`VopBulkIdentification` vs Generated=``
    - **Description**: Reference=`Legal Entity Identifier of the party` vs Generated=`This object contains all info about the *identific...`
    - **Type**: Reference=`schema` vs Generated=`object`
    - **Schema Name
(if Type = schema)**: Reference=`LEIType` vs Generated=``
  - **Row 155** (Excel Line 155):
    - **Name**: Reference=`bic` vs Generated=`lei`
    - **Description**: Reference=`BIC of the party` vs Generated=``
    - **Schema Name
(if Type = schema)**: Reference=`BICType` vs Generated=`LEIType`
  - **Row 156** (Excel Line 156):
    - **Name**: Reference=`id` vs Generated=`bic`
    - **Description**: Reference=`Identification: unique and unambiguous identificat...` vs Generated=``
    - **Schema Name
(if Type = schema)**: Reference=`Max256Text` vs Generated=`BICType`
  - **Row 157** (Excel Line 157):
    - **Name**: Reference=`snc` vs Generated=`id`
    - **Description**: Reference=`Scheme Name Code: an entry provided by an external...` vs Generated=``
    - **Schema Name
(if Type = schema)**: Reference=`OrganisationIdentificationCode` vs Generated=`Max256Text`
  - **Row 158** (Excel Line 158):
    - **Name**: Reference=`snp` vs Generated=`snc`
    - **Description**: Reference=`Scheme Name Proprietary: a scheme name defined in ...` vs Generated=``
    - **Schema Name
(if Type = schema)**: Reference=`Max35Text` vs Generated=`OrganisationIdentificationCode`
  - **Row 159** (Excel Line 159):
    - **Name**: Reference=`iss` vs Generated=`snp`
    - **Description**: Reference=`Issuer of the identification.` vs Generated=``
  - **Row 160** (Excel Line 160):
    - **Name**: Reference=`VopBulkRequest` vs Generated=`iss`
    - **Parent**: Reference=`` vs Generated=`VopBulkIdentification`
    - **Description**: Reference=`This object contains all fields to make request fo...` vs Generated=``
    - **Type**: Reference=`object` vs Generated=`schema`
    - **Schema Name
(if Type = schema)**: Reference=`` vs Generated=`Max35Text`
  - **Row 161** (Excel Line 161):
    - **Name**: Reference=`xid` vs Generated=`VopBulkRequest`
    - **Parent**: Reference=`VopBulkRequest` vs Generated=``
    - **Description**: Reference=`X-Request-ID used as Requesting PSP’s reference nu...` vs Generated=`This object contains all fields to make request fo...`
    - **Type**: Reference=`string` vs Generated=`object`
    - **Format**: Reference=`uuid` vs Generated=``
    - **Mandatory**: Reference=`M` vs Generated=``
  - **Row 162** (Excel Line 162):
    - **Name**: Reference=`rBic` vs Generated=`xid`
    - **Description**: Reference=`BIC of the requesting agent` vs Generated=`X-Request-ID used as Requesting PSP’s reference nu...`
    - **Type**: Reference=`schema` vs Generated=`string`
    - **Schema Name
(if Type = schema)**: Reference=`BICType` vs Generated=``
    - **Format**: Reference=`` vs Generated=`uuid`
  - **Row 163** (Excel Line 163):
    - **Name**: Reference=`pBic` vs Generated=`rBic`
    - **Description**: Reference=`BIC of the party agent` vs Generated=``
  - **Row 164** (Excel Line 164):
    - **Name**: Reference=`iban` vs Generated=`pBic`
    - **Description**: Reference=`IBAN of the party account` vs Generated=``
    - **Schema Name
(if Type = schema)**: Reference=`IBANType` vs Generated=`BICType`
  - **Row 165** (Excel Line 165):
    - **Name**: Reference=`name` vs Generated=`iban`
    - **Description**: Reference=`Party name` vs Generated=``
    - **Schema Name
(if Type = schema)**: Reference=`Max140Text` vs Generated=`IBANType`
    - **Mandatory**: Reference=`` vs Generated=`M`
  - **Row 166** (Excel Line 166):
    - **Name**: Reference=`id` vs Generated=`name`
    - **Description**: Reference=`Party identification (may be used as an alternativ...` vs Generated=``
    - **Type**: Reference=`array` vs Generated=`schema`
    - **Items Data Type 
(Array only)**: Reference=`VopBulkIdentification` vs Generated=``
    - **Schema Name
(if Type = schema)**: Reference=`` vs Generated=`Max140Text`
  - **Row 167** (Excel Line 167):
    - **Name**: Reference=`VopBulkResponse` vs Generated=`id`
    - **Parent**: Reference=`` vs Generated=`VopBulkRequest`
    - **Description**: Reference=`This object contains the reponse of a get bulk vop` vs Generated=`Party identification (may be used as an alternativ...`
    - **Type**: Reference=`object` vs Generated=`array`
    - **Items Data Type 
(Array only)**: Reference=`` vs Generated=`schema`
    - **Schema Name
(if Type = schema)**: Reference=`` vs Generated=`VopBulkIdentification`
  - **Row 168** (Excel Line 168):
    - **Name**: Reference=`xid` vs Generated=`VopBulkResponse`
    - **Parent**: Reference=`VopBulkResponse` vs Generated=``
    - **Description**: Reference=`X-Request-ID used as Requesting PSP’s reference nu...` vs Generated=`This object contains the reponse of a get bulk vop`
    - **Type**: Reference=`string` vs Generated=`object`
    - **Format**: Reference=`uuid` vs Generated=``
    - **Mandatory**: Reference=`M` vs Generated=``
  - **Row 169** (Excel Line 169):
    - **Name**: Reference=`fuid` vs Generated=`xid`
    - **Description**: Reference=`FPAD Unique Identifier (a UUID specified by RFC412...` vs Generated=`X-Request-ID used as Requesting PSP’s reference nu...`
    - **Format**: Reference=`` vs Generated=`uuid`
  - **Row 170** (Excel Line 170):
    - **Name**: Reference=`fName` vs Generated=`fuid`
    - **Description**: Reference=`FPAD Payee Name.` vs Generated=`FPAD Unique Identifier (a UUID specified by RFC412...`
    - **Mandatory**: Reference=`` vs Generated=`M`
  - **Row 171** (Excel Line 171):
    - **Name**: Reference=`ria` vs Generated=`fName`
    - **Description**: Reference=`` vs Generated=`FPAD Payee Name.`
    - **Type**: Reference=`array` vs Generated=`string`
    - **Items Data Type 
(Array only)**: Reference=`Ria` vs Generated=``
  - **Row 172** (Excel Line 172):
    - **Name**: Reference=`vPnm` vs Generated=`ria`
    - **Description**: Reference=`VOP Party Name Match.` vs Generated=``
    - **Type**: Reference=`schema` vs Generated=`array`
    - **Items Data Type 
(Array only)**: Reference=`` vs Generated=`schema`
    - **Schema Name
(if Type = schema)**: Reference=`NameMatchType` vs Generated=`Ria`
  - **Row 173** (Excel Line 173):
    - **Name**: Reference=`vPim` vs Generated=`vPnm`
    - **Description**: Reference=`VOP Party Id Match.` vs Generated=``
    - **Schema Name
(if Type = schema)**: Reference=`PartyIdMatchType` vs Generated=`NameMatchType`
  - **Row 174** (Excel Line 174):
    - **Name**: Reference=`vName` vs Generated=`vPim`
    - **Description**: Reference=`VOP matched name.` vs Generated=``
    - **Schema Name
(if Type = schema)**: Reference=`Max140Text` vs Generated=`PartyIdMatchType`
  - **Row 175** (Excel Line 175):
    - **Name**: Reference=`msgs` vs Generated=`vName`
    - **Description**: Reference=`Messages array.` vs Generated=``
    - **Type**: Reference=`array` vs Generated=`schema`
    - **Items Data Type 
(Array only)**: Reference=`ShortMessage` vs Generated=``
    - **Schema Name
(if Type = schema)**: Reference=`` vs Generated=`Max140Text`
  - **Row 176** (Excel Line 176):
    - **Name**: Reference=`vrts` vs Generated=`msgs`
    - **Description**: Reference=`VOP Response Time Stamp: Time stamp of provided by...` vs Generated=`Messages array.`
    - **Type**: Reference=`string` vs Generated=`array`
    - **Items Data Type 
(Array only)**: Reference=`` vs Generated=`schema`
    - **Schema Name
(if Type = schema)**: Reference=`` vs Generated=`ShortMessage`
    - **Format**: Reference=`date-time` vs Generated=``
    - **Example**: Reference=`2024-08-12 15:19:22.678000+00:00` vs Generated=``
  - **Row 177** (Excel Line 177):
    - **Name**: Reference=`VopBulkResponseCounter` vs Generated=`vrts`
    - **Parent**: Reference=`` vs Generated=`VopBulkResponse`
    - **Description**: Reference=`Counter for bulk responses having the same matchin...` vs Generated=`VOP Response Time Stamp: Time stamp of provided by...`
    - **Type**: Reference=`object` vs Generated=`string`
    - **Format**: Reference=`` vs Generated=`date-time`
  - **Row 178** (Excel Line 178):
    - **Name**: Reference=`matchingResult` vs Generated=`VopBulkResponseCounter`
    - **Parent**: Reference=`VopBulkResponseCounter` vs Generated=``
    - **Description**: Reference=`Matching value for successful responses, "ERROR" f...` vs Generated=`Counter for bulk responses having the same matchin...`
    - **Type**: Reference=`string` vs Generated=`object`
    - **Allowed value**: Reference=`MTCH,CMTC,NMTC,NOAP,ERROR` vs Generated=``
  - **Row 179** (Excel Line 179):
    - **Name**: Reference=`counter` vs Generated=`matchingResult`
    - **Description**: Reference=`Number of responses having the matching value spec...` vs Generated=`Matching value for successful responses, "ERROR" f...`
    - **Type**: Reference=`integer` vs Generated=`string`
    - **Allowed value**: Reference=`` vs Generated=`MTCH, CMTC, NMTC, NOAP, ERROR`
  - **Row 180** (Excel Line 180):
    - **Name**: Reference=`` vs Generated=`counter`
    - **Parent**: Reference=`` vs Generated=`VopBulkResponseCounter`
    - **Description**: Reference=`` vs Generated=`Number of responses having the matching value spec...`
    - **Type**: Reference=`` vs Generated=`integer`
## Sheet: Tags
- [x] Content Identical