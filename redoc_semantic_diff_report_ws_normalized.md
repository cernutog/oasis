# Redocly HTML Semantic Diff Report

## Inputs
- **A**: `C:\EBA Clearing\APIs\HTML Docs\EBACL_RT1_20260223_Openapi3.1_RT1_API_Participants_4_0_v20260613.html`
- **B**: `C:\EBA Clearing\APIs\HTML Docs\EBACL_RT1_20260306_Openapi3.1_RT1_API_Participants_4_0_v20260613.html`

## Compare options
- **normalize_whitespace**: True
- **ignore_examples**: False
- **ignore_x_sandbox**: False

## API Info
- **A title**: EBACL RT1 REST API - PWS
- **B title**: EBACL RT1 REST API - PWS
- **A version**: 4.0
- **B version**: 4.0

## Paths / Operations
- **Added operations (B only)**: 0
- **Removed operations (A only)**: 0
- **Changed operations**: 46

### Changed operations (details)
#### `POST /apDetails/{senderBic}/{bicAp}`
- **A operationId**: `apDetails`
- **B operationId**: `APDetails`
- `/operationId:` A='apDetails' B='APDetails'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/apDetail[0]/details:` A='len=1' B='len=2'
- `/responses/200/content/application/json/examples/OK/value/apDetail[0]/details[0]/productList:` A='len=1' B='len=2'
- `/responses/200/content/application/json/examples/OK/value/apDetail[0]/details[0]/productList[0]/productId:` A='EOLO' B='INST'
- `/responses/200/content/application/json/examples/OK/value/apDetail[0]/details[0]/tipsUserBic:` A='COURFR2TXXX' B='IPSDID21XXX'
- `/responses/200/content/application/json/examples/OK/value/apDetail[0]/paramHistory/bicAp:` A='COURFR2TXXX' B='IPSDID21XXX'
- `/responses/200/content/application/json/examples/OK/value/apDetail[0]/paramHistory/dpBic:` A='COURFR2T' B='IPSDID21'
- `/responses/200/content/application/json/examples/OK/value/apDetail[0]/paramHistory/endParticipantValidity:` A='2019-06-21' B='2024-08-11'
- `/responses/200/content/application/json/examples/OK/value/apDetail[0]/paramHistory/initParticipantValidity:` A='2024-08-11' B='2019-06-21'
- `/responses/200/content/application/json/examples/OK/value/apDetail[0]/paramHistory/status:` A='ENB' B='CNG'
- `/responses/200/content/application/json/examples/OK/value/apDetail[0]/paramHistory/submittedAOSEolo:` A='A03' B='A02'
- `/responses/200/content/application/json/examples/OK/value/apDetail[0]/paramHistory/submittedAOSinst:` A='A02' B='A01'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Internal Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `PUT /beneficiaryManagement/{senderBic}`
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/beneficiaryAcc:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/beneficiaryName:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/beneficiaryBic:` A='COURFR2TXXX' B='IPSDID21XXX'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/operationType:` A='REM' B='INS'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/participantBic:` A='CIPTBITM' B='IPSDID21'
- `/requestBody/content/application/json/examples/OK/value/criteria/beneficiaryAcc:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/beneficiaryName:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/beneficiaryBic:` A='COURFR2TXXX' B='IPSDID21XXX'
- `/requestBody/content/application/json/examples/OK/value/criteria/operationType:` A='REM' B='INS'
- `/requestBody/content/application/json/examples/OK/value/criteria/participantBic:` A='CIPTBITM' B='IPSDID21'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/dateTime:` A='2024-11-08T14:29:00.012345' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/value/referenceId:` A='ID0452050454' B='ID028472018304'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Internal Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `PUT /changeStatusAP/{senderBic}`
- **A operationId**: `changeStatusAP`
- **B operationId**: `ChangeStatusAP`
- `/operationId:` A='changeStatusAP' B='ChangeStatusAP'
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/effectiveEndValidityDate:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/newStatus:` A='RNL' B='DIS'
- `/requestBody/content/application/json/examples/OK/value/criteria/effectiveEndValidityDate:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/newStatus:` A='RNL' B='DIS'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/dateTime:` A='2024-11-08T14:29:00.012345' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/value/referenceId:` A='ID0452050454' B='ID028472018304'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Generic Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `PUT /commandDelete/{senderBic}/{referenceId}`
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/commandItem/authorizationDate:` A='2024-08-11' B='2019-06-21'
- `/responses/200/content/application/json/examples/OK/value/commandItem/authorizer:` A='ID194839' B='CO0A222'
- `/responses/200/content/application/json/examples/OK/value/commandItem/commandType:` A='RMV' B='INS'
- `/responses/200/content/application/json/examples/OK/value/commandItem/referenceId:` A='ID0452050454' B='ID028472018304'
- `/responses/200/content/application/json/examples/OK/value/commandItem/requestor:` A='ID84739' B='ID20391'
- `/responses/200/content/application/json/examples/OK/value/commandItem/submissionDate:` A='9999-12-31T12:55:45.000001' B='2024-11-08T14:29:00.012345'
- `/responses/200/content/application/json/examples/OK/value/dateTime:` A='2024-11-08T14:29:00.012345' B='2019-06-21T23:20:50.000001'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Generic Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /commandStatusDetails/{senderBic}/{referenceId}`
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/commandItem/authorizer:` A='ID74823' B='CO0A222'
- `/responses/200/content/application/json/examples/OK/value/commandItem/commandType:` A='UPD' B='INS'
- `/responses/200/content/application/json/examples/OK/value/commandItem/requestStatus:` A='EXE' B='ATH'
- `/responses/200/content/application/json/examples/OK/value/commandItem/submissionDate:` A='2019-06-21T23:20:50.000001' B='2024-11-08T14:29:00.012345'
- `/responses/200/content/application/json/examples/OK/value/dateTime:` A='9999-12-31T12:55:45.000001' B='2019-06-21T23:20:50.000001'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Generic Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `PUT /communicationOfUnavailability/{senderBic}`
- **A operationId**: `communicationOfUnavailability`
- **B operationId**: `CommunicationOfUnavailability`
- `/operationId:` A='communicationOfUnavailability' B='CommunicationOfUnavailability'
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/apspsUnavailability:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/eventDescription:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/idOfUnavailableParty:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/endDateTime:` A='2019-05-02T22:22:00.123000-01:10' B='2019-05-02T22:22:00.123-01:10'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/messageId:` A='P08B59450578EA544526A8DB7D060D' B='P08M59270578EA544566A8DB7D970D'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/productsUnavailable:` A='EOLO' B='INST'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/startDateTime:` A='2019-05-02T22:22:00.123000-01:10' B='2019-05-02T22:22:00.123-01:10'
- `/requestBody/content/application/json/examples/OK/value/criteria/apspsUnavailability:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/eventDescription:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/idOfUnavailableParty:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/endDateTime:` A='2019-05-02T22:22:00.123000-01:10' B='2019-05-02T22:22:00.123-01:10'
- `/requestBody/content/application/json/examples/OK/value/criteria/messageId:` A='P08B59450578EA544526A8DB7D060D' B='P08M59270578EA544566A8DB7D970D'
- `/requestBody/content/application/json/examples/OK/value/criteria/productsUnavailable:` A='EOLO' B='INST'
- `/requestBody/content/application/json/examples/OK/value/criteria/startDateTime:` A='2019-05-02T22:22:00.123000-01:10' B='2019-05-02T22:22:00.123-01:10'
- `/requestBody/content/application/json/examples/OK/value/dateTime:` A='2024-11-08T14:29:00.012345' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/dateTime:` A='9999-12-31T12:55:45.000001' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/value/unavailableBic:` A='CIPTBITMXXX' B='IPSDID21XXX'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Generic Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /currentNetPosition/{senderBic}`
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/branchFundsBalancePosition/amount:` A=389.05 B=9.99
- `/responses/200/content/application/json/examples/OK/value/branchFundsBalancePosition/branchFundsBalanceId:` A='COURFR2T00001' B='IPSDID2100001'
- `/responses/200/content/application/json/examples/OK/value/dateTime:` A='2024-11-08T14:29:00.012345' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/value/lspsPosition:` A='len=1' B='len=2'
- `/responses/200/content/application/json/examples/OK/value/lspsPosition[0]/amount:` A=9.99 B=2000.11
- `/responses/200/content/application/json/examples/OK/value/lspsPosition[0]/bic:` A='COURFR2T' B='CIPTBITM'
- `/responses/200/content/application/json/examples/OK/value/lspsPosition[0]/sign:` A='C' B='D'
- `/responses/200/content/application/json/examples/OK/value/lspsPosition[0]/timestamp:` A='2019-06-21T23:20:50.000001' B='9999-12-31T12:55:45.000001'
- `/responses/200/content/application/json/examples/OK/value/ownedBranchFundsBalanceList[0]/ownedBranchFundsBalanceInfo/amount:` A=389.05 B=2000.11
- `/responses/200/content/application/json/examples/OK/value/ownedBranchFundsBalanceList[0]/ownedMemberList:` A='len=1' B='len=2'
- `/responses/200/content/application/json/examples/OK/value/ownedBranchFundsBalanceList[0]/ownedMemberList[0]/amount:` A=2000.11 B=389.05
- `/responses/200/content/application/json/examples/OK/value/ownedBranchFundsBalanceList[0]/ownedMemberList[0]/bic:` A='CIPTBITM' B='IPSDID21'
- `/responses/200/content/application/json/examples/OK/value/ownedBranchFundsBalanceList[0]/ownedMemberList[0]/timestamp:` A='9999-12-31T12:55:45.000001' B='2024-11-08T14:29:00.012345'
- `/responses/200/content/application/json/examples/OK/value/senderPosition/amount:` A=2000.11 B=9.99
- `/responses/200/content/application/json/examples/OK/value/senderPosition/sign:` A='D' B='C'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Generic Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `PUT /defaultPosition/{senderBic}`
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/lspBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/defaultDayValues/day:` A=2 B=1
- `/requestBody/content/application/json/examples/Bad Request/value/defaultDayValues/defaultLACValues:` A='len=1' B='len=2'
- `/requestBody/content/application/json/examples/Bad Request/value/defaultDayValues/defaultLACValues[0]/resetToBasePosition:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/defaultDayValues/defaultLACValues[0]/sendAccountQueryToTips:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/defaultDayValues/defaultLACValues[0]/base:` A=49.2 B=30004958.23
- `/requestBody/content/application/json/examples/Bad Request/value/defaultDayValues/defaultLACValues[0]/lac:` A='2' B='1'
- `/requestBody/content/application/json/examples/Bad Request/value/defaultDayValues/defaultLACValues[0]/upper:` A=30004958.23 B=49.2
- `/requestBody/content/application/json/examples/OK/value/lspBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/dateTime:` A='9999-12-31T12:55:45.000001' B='2019-06-21T23:20:50.000001'
- `/requestBody/content/application/json/examples/OK/value/defaultDayValues/day:` A=2 B=1
- `/requestBody/content/application/json/examples/OK/value/defaultDayValues/defaultLACValues:` A='len=1' B='len=2'
- `/requestBody/content/application/json/examples/OK/value/defaultDayValues/defaultLACValues[0]/resetToBasePosition:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/defaultDayValues/defaultLACValues[0]/sendAccountQueryToTips:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/defaultDayValues/defaultLACValues[0]/base:` A=49.2 B=30004958.23
- `/requestBody/content/application/json/examples/OK/value/defaultDayValues/defaultLACValues[0]/lac:` A='2' B='1'
- `/requestBody/content/application/json/examples/OK/value/defaultDayValues/defaultLACValues[0]/upper:` A=30004958.23 B=49.2
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/effectiveDate:` A='2024-08-11' B='2019-06-21'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Generic Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `PUT /defunding/{senderBic}`
- **A operationId**: `defunding`
- **B operationId**: `releaseLiquidiy`
- `/operationId:` A='defunding' B='releaseLiquidiy'
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/releaseInfo/branchFundsBalanceId:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/releaseInfo/lspBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/releaseInfo/memberBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/releaseInfo/amount:` A=2000.11 B=9.99
- `/requestBody/content/application/json/examples/OK/value/dateTime:` A='2024-11-08T14:29:00.012345' B='2019-06-21T23:20:50.000001'
- `/requestBody/content/application/json/examples/OK/value/releaseInfo/branchFundsBalanceId:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/releaseInfo/lspBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/releaseInfo/memberBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/releaseInfo/amount:` A=2000.11 B=9.99
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/dateTime:` A='9999-12-31T12:55:45.000001' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/value/remainingAmount:` A=389.05 B=9.99
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Generic Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `PUT /exceptionPositionCalendar/{senderBic}`
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/lspBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/businessDate:` A='9999-12-31' B='2019-06-21'
- `/requestBody/content/application/json/examples/Bad Request/value/exceptionLacValues:` A='len=1' B='len=2'
- `/requestBody/content/application/json/examples/Bad Request/value/exceptionLacValues[0]/resetToBasePosition:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/exceptionLacValues[0]/sendAccountQueryToTips:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/exceptionLacValues[0]/base:` A=13402.53 B=30004958.23
- `/requestBody/content/application/json/examples/Bad Request/value/exceptionLacValues[0]/lac:` A='2' B='1'
- `/requestBody/content/application/json/examples/Bad Request/value/exceptionLacValues[0]/lower:` A=49.2 B=13402.53
- `/requestBody/content/application/json/examples/Bad Request/value/exceptionLacValues[0]/upper:` A=30004958.23 B=49.2
- `/requestBody/content/application/json/examples/OK/value/lspBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/businessDate:` A='9999-12-31' B='2019-06-21'
- `/requestBody/content/application/json/examples/OK/value/exceptionLacValues:` A='len=1' B='len=2'
- `/requestBody/content/application/json/examples/OK/value/exceptionLacValues[0]/resetToBasePosition:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/exceptionLacValues[0]/sendAccountQueryToTips:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/exceptionLacValues[0]/base:` A=13402.53 B=30004958.23
- `/requestBody/content/application/json/examples/OK/value/exceptionLacValues[0]/lac:` A='2' B='1'
- `/requestBody/content/application/json/examples/OK/value/exceptionLacValues[0]/lower:` A=49.2 B=13402.53
- `/requestBody/content/application/json/examples/OK/value/exceptionLacValues[0]/upper:` A=30004958.23 B=49.2
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/dateTime:` A='2024-11-08T14:29:00.012345' B='2019-06-21T23:20:50.000001'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Generic Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /fileDetails/{senderBic}`
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/fileReference:` A='DSCI210303000015' B='DSCI210301000015'
- `/requestBody/content/application/json/examples/OK/value/criteria/fileReference:` A='DSCI210303000015' B='DSCI210301000015'
- `/requestBody/content/application/json/examples/OK/value/dateTime:` A='9999-12-31T12:55:45.000001' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/businessDate:` A='2024-08-11' B='2019-06-21'
- `/responses/200/content/application/json/examples/OK/value/fileStatus:` A='TSG' B='TSD'
- `/responses/200/content/application/json/examples/OK/value/fileType:` A='DRR' B='RSF'
- `/responses/200/content/application/json/examples/OK/value/lac:` A='3' B='1'
- `/responses/200/content/application/json/examples/OK/value/listDRRData/investigationData/numReceivedInvestigation:` A=2 B=1
- `/responses/200/content/application/json/examples/OK/value/listDRRData/investigationData/numSentInvestigation:` A=2 B=1
- `/responses/200/content/application/json/examples/OK/value/listDRRData/ipDataDRR/amountHeldIP:` A=2000.11 B=9.99
- `/responses/200/content/application/json/examples/OK/value/listDRRData/ipDataDRR/ipData/amountRjtIP:` A=2000.11 B=389.05
- `/responses/200/content/application/json/examples/OK/value/listDRRData/ipDataDRR/ipData/amountSentIP:` A=9.99 B=2000.11
- `/responses/200/content/application/json/examples/OK/value/listDRRData/ipDataDRR/ipData/amountSettledIP:` A=389.05 B=9.99
- `/responses/200/content/application/json/examples/OK/value/listDRRData/ipDataDRR/ipData/numRjtIP:` A=3 B=1
- `/responses/200/content/application/json/examples/OK/value/listDRRData/ipDataDRR/ipData/numSentIP:` A=3 B=1
- `/responses/200/content/application/json/examples/OK/value/listDRRData/ipDataDRR/ipData/numSettledIP:` A=3 B=1
- `/responses/200/content/application/json/examples/OK/value/listDRRData/ipDataDRR/numHeldIP:` A=2 B=1
- `/responses/200/content/application/json/examples/OK/value/listDRRData/nrrData/numRjtNRR:` A=3 B=1
- `/responses/200/content/application/json/examples/OK/value/listDRRData/nrrData/numSentNRR:` A=3 B=1
- `/responses/200/content/application/json/examples/OK/value/listDRRData/prrDataDRR/numHeldPRR:` A=2 B=1
- `/responses/200/content/application/json/examples/OK/value/listDRRData/prrDataDRR/prrData/amountSentPRR:` A=2000.11 B=389.05
- `/responses/200/content/application/json/examples/OK/value/listDRRData/prrDataDRR/prrData/amountSettledPRR:` A=389.05 B=2000.11
- `/responses/200/content/application/json/examples/OK/value/listDRRData/prrDataDRR/prrData/numRjtPRR:` A=3 B=1
- `/responses/200/content/application/json/examples/OK/value/listDRRData/prrDataDRR/prrData/numSentPRR:` A=3 B=1
- `/responses/200/content/application/json/examples/OK/value/listDRRData/prrDataDRR/prrData/numSettledPRR:` A=3 B=1
- `/responses/200/content/application/json/examples/OK/value/listDRRData/recallData/numRjtRecall:` A=3 B=1
- `/responses/200/content/application/json/examples/OK/value/listDRRData/recallData/numSentRecall:` A=3 B=1
- `/responses/200/content/application/json/examples/OK/value/listDRRData/updatedData/numReceivedReqStatusUpd:` A=2 B=1
- `/responses/200/content/application/json/examples/OK/value/listDRRData/updatedData/numSentReqStatusUpd:` A=2 B=1
- `/responses/200/content/application/json/examples/OK/value/listMSRData/ipData/amountRjtIP:` A=9.99 B=389.05
- `/responses/200/content/application/json/examples/OK/value/listMSRData/ipData/amountSentIP:` A=389.05 B=2000.11
- `/responses/200/content/application/json/examples/OK/value/listMSRData/ipData/amountSettledIP:` A=2000.11 B=9.99
- `/responses/200/content/application/json/examples/OK/value/listMSRData/prrData/amountRjtPRR:` A=9.99 B=389.05
- `/responses/200/content/application/json/examples/OK/value/listMSRData/prrData/amountSentPRR:` A=389.05 B=2000.11
- `/responses/200/content/application/json/examples/OK/value/listMSRData/prrData/amountSettledPRR:` A=2000.11 B=9.99
- `/responses/200/content/application/json/examples/OK/value/listMSRData/recallData/amountRjtRecall:` A=9.99 B=389.05
- `/responses/200/content/application/json/examples/OK/value/listMSRData/recallData/amountSentRecall:` A=389.05 B=2000.11
- `/responses/200/content/application/json/examples/OK/value/netFileName:` A='SWIFT' B='EBICS'
- `/responses/200/content/application/json/examples/OK/value/network:` A='SWA' B='EAS'
- `/responses/200/content/application/json/examples/OK/value/receiverBic:` A='CIPTBITM' B='IPSDID21'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Generic Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `PUT /funding/{senderBic}`
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/fundingInfo/branchFundsBalanceId:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/fundingInfo/lspBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/fundingInfo/memberBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/fundingInfo/branchFundsBalanceId:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/fundingInfo/lspBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/fundingInfo/memberBic:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/dateTime:` A='2024-11-08T14:29:00.012345' B='2019-06-21T23:20:50.000001'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Generic Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `PUT /generateOutboundLto/{senderBic}`
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/beneficiaryAcc:` A='BE68539007547034' B='IT60X0542811101000000123456'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/beneficiaryBicCode:` A='COURFR2TXXX' B='IPSDID21XXX'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/beneficiaryName:` A='Banca Mediolanum' B='BFF Bank'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/participantBic:` A='CIPTBITM' B='IPSDID21'
- `/requestBody/content/application/json/examples/OK/value/criteria/beneficiaryAcc:` A='BE68539007547034' B='IT60X0542811101000000123456'
- `/requestBody/content/application/json/examples/OK/value/criteria/beneficiaryBicCode:` A='COURFR2TXXX' B='IPSDID21XXX'
- `/requestBody/content/application/json/examples/OK/value/criteria/beneficiaryName:` A='Banca Mediolanum' B='BFF Bank'
- `/requestBody/content/application/json/examples/OK/value/criteria/participantBic:` A='CIPTBITM' B='IPSDID21'
- `/requestBody/content/application/json/examples/OK/value/dateTime:` A='2024-11-08T14:29:00.012345' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/dateTime:` A='9999-12-31T12:55:45.000001' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/value/messageId:` A='P08B59450578EA54' B='P08M59270578EA54'
- `/responses/200/content/application/json/examples/OK/value/referenceId:` A='ID0452050454' B='ID028472018304'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Internal Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `PUT /generatePaymentStatusQuery/{senderBic}`
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/csm:` A='TIPS' B='RT1-TIPS'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/date:` A='2019-05-02T22:22:00.123000-01:10' B='2019-05-02T22:22:00.123-01:10'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/participantBic:` A='CIPTBITMXXX' B='IPSDID21XXX'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/transactionId:` A='TXID20231003JMMVPACS8041:TXID20231003JMMVPACS8042' B='TXID20231003JMMVPACS8040'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/transactionType:` A='IPT' B='PRR'
- `/requestBody/content/application/json/examples/OK/value/criteria/csm:` A='TIPS' B='RT1-TIPS'
- `/requestBody/content/application/json/examples/OK/value/criteria/date:` A='2019-05-02T22:22:00.123000-01:10' B='2019-05-02T22:22:00.123-01:10'
- `/requestBody/content/application/json/examples/OK/value/criteria/participantBic:` A='CIPTBITMXXX' B='IPSDID21XXX'
- `/requestBody/content/application/json/examples/OK/value/criteria/transactionId:` A='TXID20231003JMMVPACS8041:TXID20231003JMMVPACS8042' B='TXID20231003JMMVPACS8040'
- `/requestBody/content/application/json/examples/OK/value/criteria/transactionType:` A='IPT' B='PRR'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/dateTime:` A='2024-11-08T14:29:00.012345' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/value/messageId:` A='P08R59805521EA544566A8DB7P998C' B='P08M59270578EA544566A8DB7D970D'
- `/responses/200/content/application/json/examples/OK/value/referenceId:` A='ID4923482830492' B='ID028472018304'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Internal Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /getAccountBalance/{senderBic}`
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/participantBic:` A='COURFR2T' B='IPSDID21'
- `/requestBody/content/application/json/examples/OK/value/criteria/participantBic:` A='COURFR2T' B='IPSDID21'
- `/requestBody/content/application/json/examples/OK/value/dateTime:` A='9999-12-31T12:55:45.000001' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Internal Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /getDefaultPosition/{senderBic}`
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/criteria:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/dateTime:` A='2024-11-08T14:29:00.012345' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/dateTime:` A='9999-12-31T12:55:45.000001' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/value/values/branchFundsBalanceId:` A='CIPBITMM00001' B='IPSDPF2100001'
- `/responses/200/content/application/json/examples/OK/value/values/lspBic:` A='CIPTBITM' B='IPSDID21'
- `/responses/200/content/application/json/examples/OK/value/values/lspBicDefaultDayValues:` A='len=1' B='len=2'
- `/responses/200/content/application/json/examples/OK/value/values/lspBicDefaultDayValues[0]/defaultLACValues:` A='len=1' B='len=2'
- `/responses/200/content/application/json/examples/OK/value/values/lspBicDefaultDayValues[0]/defaultLACValues[0]/base:` A=13402.53 B=30004958.23
- `/responses/200/content/application/json/examples/OK/value/values/lspBicDefaultDayValues[0]/defaultLACValues[0]/lower:` A=30004958.23 B=13402.53
- `/responses/200/content/application/json/examples/OK/value/values/memberBic:` A='COURFR2T' B='CIPTBITM'
- `/responses/200/content/application/json/examples/OK/value/values/memberDefaultDayValues:` A='len=1' B='len=2'
- `/responses/200/content/application/json/examples/OK/value/values/memberDefaultDayValues[0]/defaultLACValues:` A='len=1' B='len=2'
- `/responses/200/content/application/json/examples/OK/value/values/memberDefaultDayValues[0]/defaultLACValues[0]/base:` A=49.2 B=30004958.23
- `/responses/200/content/application/json/examples/OK/value/values/memberDefaultDayValues[0]/defaultLACValues[0]/lac:` A='3' B='2'
- `/responses/200/content/application/json/examples/OK/value/values/memberDefaultDayValues[0]/defaultLACValues[0]/resetToBasePosition:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/values/memberDefaultDayValues[0]/defaultLACValues[0]/sendAccountQueryToTips:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/values/memberDefaultDayValues[0]/defaultLACValues[0]/upper:` A=30004958.23 B=49.2
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Generic Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /getExceptionPositionCalendar/{senderBic}`
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/branchFundsBalanceId:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/lspBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/memberBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/branchFundsBalanceId:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/lspBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/memberBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/dateTime:` A='9999-12-31T12:55:45.000001' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/response/bicExceptionDayValues:` A='len=1' B='len=2'
- `/responses/200/content/application/json/examples/OK/value/response/bicExceptionDayValues[0]/base:` A=49.2 B=30004958.23
- `/responses/200/content/application/json/examples/OK/value/response/bicExceptionDayValues[0]/lac:` A='3' B='1'
- `/responses/200/content/application/json/examples/OK/value/response/bicExceptionDayValues[0]/lower:` A=30004958.23 B=13402.53
- `/responses/200/content/application/json/examples/OK/value/response/bicExceptionDayValues[0]/resetToBasePosition:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/response/bicExceptionDayValues[0]/sendAccountQueryToTips:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/response/bicExceptionDayValues[0]/upper:` A=13402.53 B=49.2
- `/responses/200/content/application/json/examples/OK/value/response/businessDate:` A='2024-08-11' B='2019-06-21'
- `/responses/200/content/application/json/examples/OK/value/response/memberExceptionDayValues:` A='len=1' B='len=2'
- `/responses/200/content/application/json/examples/OK/value/response/memberExceptionDayValues[0]/base:` A=49.2 B=30004958.23
- `/responses/200/content/application/json/examples/OK/value/response/memberExceptionDayValues[0]/lac:` A='1' B='3'
- `/responses/200/content/application/json/examples/OK/value/response/memberExceptionDayValues[0]/lower:` A=30004958.23 B=13402.53
- `/responses/200/content/application/json/examples/OK/value/response/memberExceptionDayValues[0]/upper:` A=13402.53 B=49.2
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Generic Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /getParticipants/{senderBic}`
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/criteria:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/dateTime:` A='9999-12-31T12:55:45.000001' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/responseList:` A='len=1' B='len=2'
- `/responses/200/content/application/json/examples/OK/value/responseList[0]/bic:` A='COURFR2T' B='IPSDID21'
- `/responses/200/content/application/json/examples/OK/value/responseList[0]/lsp:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/responseList[0]/name:` A='Intesa Sanpaolo' B='BFF Bank'
- `/responses/200/content/application/json/examples/OK/value/responseList[0]/network:` A='EBX' B='EAS'
- `/responses/200/content/application/json/examples/OK/value/responseList[0]/newBic:` A='IPSDID21' B='CIPTBITM'
- `/responses/200/content/application/json/examples/OK/value/responseList[0]/newRole:` A='Y' B='N'
- `/responses/200/content/application/json/examples/OK/value/responseList[0]/productList:` A='len=1' B='len=2'
- `/responses/200/content/application/json/examples/OK/value/responseList[0]/productList[0]/productId:` A='EOLO' B='INST'
- `/responses/200/content/application/json/examples/OK/value/responseList[0]/status:` A='CNG' B='ALL'
- `/responses/200/content/application/json/examples/OK/value/responseList[0]/submittedAOSeolo:` A='A03' B='A02'
- `/responses/200/content/application/json/examples/OK/value/responseList[0]/submittedAOSinst:` A='A02' B='A01'
- `/responses/200/content/application/json/examples/OK/value/responseList[0]/technicalBic:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/responseList[0]/tipsAccountOwnerBic:` A='COURFR2TXXX' B='IPSDID21XXX'
- `/responses/200/content/application/json/examples/OK/value/responseList[0]/tipsAdherence:` A='1' B='0'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Internal Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /inquiryUnavailability/{senderBic}`
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/criteria:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/dateTime:` A='2024-11-08T14:29:00.012345' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/value/list:` A='len=1' B='len=2'
- `/responses/200/content/application/json/examples/OK/value/list[0]/apspsUnavailability:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/list[0]/endDateTime:` A='2019-06-21T23:20:50.000001' B='9999-12-31T12:55:45.000001'
- `/responses/200/content/application/json/examples/OK/value/list[0]/generationDateTime:` A='2024-11-08T14:29:00.012345' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/value/list[0]/messageId:` A='P08B59450578EA544526A8DB7D060D' B='P08M59270578EA544566A8DB7D970D'
- `/responses/200/content/application/json/examples/OK/value/list[0]/senderBIC:` A='COURFR2TXXX' B='IPSDID21XXX'
- `/responses/200/content/application/json/examples/OK/value/list[0]/startDateTime:` A='9999-12-31T12:55:45.000001' B='2024-11-08T14:29:00.012345'
- `/responses/200/content/application/json/examples/OK/value/list[0]/status:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/list[0]/unavailableBic:` A='IPSDID21XXX' B='CIPTBITMXXX'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Generic Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `PUT /insertAP/{senderBic}`
- **A operationId**: `insertAP`
- **B operationId**: `InsertAP`
- `/operationId:` A='insertAP' B='InsertAP'
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/bbPositiveCnf:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/bbTimeoutMgm:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/submittedAOSeolo:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/submittedAOSinst:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/bicAp:` A='CIPTBITMXXX' B='IPSDID21XXX'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/initParticipantValidity:` A='9999-12-31' B='2019-06-21'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/name:` A='Banca Mediolanum' B='BFF Bank'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/productList:` A='len=1' B='len=2'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/productList[0]/admissionProfile:` A='CRD' B='CAD'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/tipsUserBic:` A='COURFR2TXXX' B='CIPTBITMXXX'
- `/requestBody/content/application/json/examples/OK/value/criteria/bbPositiveCnf:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/bbTimeoutMgm:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/submittedAOSeolo:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/submittedAOSinst:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/bicAp:` A='CIPTBITMXXX' B='IPSDID21XXX'
- `/requestBody/content/application/json/examples/OK/value/criteria/initParticipantValidity:` A='9999-12-31' B='2019-06-21'
- `/requestBody/content/application/json/examples/OK/value/criteria/name:` A='Banca Mediolanum' B='BFF Bank'
- `/requestBody/content/application/json/examples/OK/value/criteria/productList:` A='len=1' B='len=2'
- `/requestBody/content/application/json/examples/OK/value/criteria/productList[0]/admissionProfile:` A='CRD' B='CAD'
- `/requestBody/content/application/json/examples/OK/value/criteria/tipsUserBic:` A='COURFR2TXXX' B='CIPTBITMXXX'
- `/requestBody/content/application/json/examples/OK/value/dateTime:` A='9999-12-31T12:55:45.000001' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/referenceId:` A='ID4923482830492' B='ID028472018304'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Internal Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /instructionDetails/{senderBic}/{referenceId}`
- **A operationId**: `instructionDetails`
- **B operationId**: `instructionDeteils`
- `/operationId:` A='instructionDetails' B='instructionDeteils'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/instructions/accountToBeDebited:` A='BE68539007547034' B='IT60X0542811101000000123456'
- `/responses/200/content/application/json/examples/OK/value/instructions/amount:` A=389.05 B=9.99
- `/responses/200/content/application/json/examples/OK/value/instructions/bookingDataTime:` A='9999-12-31T12:55:45.000001' B='2024-11-08T14:29:00.012345'
- `/responses/200/content/application/json/examples/OK/value/instructions/date:` A='9999-12-31' B='2019-06-21'
- `/responses/200/content/application/json/examples/OK/value/instructions/instructionType:` A='APFR' B='CPFR'
- `/responses/200/content/application/json/examples/OK/value/instructions/lac:` A='03' B='01'
- `/responses/200/content/application/json/examples/OK/value/instructions/liquidityMessId:` A='P08R59805521EA544566A8DB7P998C' B='P08M59270578EA544566A8DB7D970D'
- `/responses/200/content/application/json/examples/OK/value/instructions/rt1PositionUpdateDataTime:` A='2024-11-08T14:29:00.012345' B='9999-12-31T12:55:45.000001'
- `/responses/200/content/application/json/examples/OK/value/instructions/status:` A='RJT' B='WTG'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Internal Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /interestAmounts/{senderBic}`
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/bic:` A='COURFR2T' B='IPSDID21'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/month:` A=2 B=1
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/year:` A=2023 B=2024
- `/requestBody/content/application/json/examples/OK/value/criteria/bic:` A='COURFR2T' B='IPSDID21'
- `/requestBody/content/application/json/examples/OK/value/criteria/month:` A=2 B=1
- `/requestBody/content/application/json/examples/OK/value/criteria/year:` A=2023 B=2024
- `/requestBody/content/application/json/examples/OK/value/dateTime:` A='2024-11-08T14:29:00.012345' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/dateTime:` A='9999-12-31T12:55:45.000001' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/value/interestList:` A='len=1' B='len=2'
- `/responses/200/content/application/json/examples/OK/value/interestList[0]/dailyInterestAmount:` A=9.99 B=389.05
- `/responses/200/content/application/json/examples/OK/value/interestList[0]/date:` A='9999-12-31' B='2019-06-21'
- `/responses/200/content/application/json/examples/OK/value/interestList[0]/interestRate:` A=389.05 B=9.99
- `/responses/200/content/application/json/examples/OK/value/interestList[0]/snapshotTime:` A='00:00:01' B='16:00:00'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Generic Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `PUT /liquidityTransfer/{senderBic}`
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/liquidityTransferInfo/branchFundsBalanceId:` A='COURFR2T00001' B='IPSDPF2100001'
- `/requestBody/content/application/json/examples/Bad Request/value/liquidityTransferInfo/receiverBic:` A='COURFR2T' B='CIPTBITM'
- `/requestBody/content/application/json/examples/OK/value/dateTime:` A='9999-12-31T12:55:45.000001' B='2019-06-21T23:20:50.000001'
- `/requestBody/content/application/json/examples/OK/value/liquidityTransferInfo/branchFundsBalanceId:` A='COURFR2T00001' B='IPSDPF2100001'
- `/requestBody/content/application/json/examples/OK/value/liquidityTransferInfo/receiverBic:` A='COURFR2T' B='CIPTBITM'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Generic Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /listAAURT1ASTA/{senderBic}`
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/aauRt1Asta:` A='COURFR2TXXX' B='IPSDPF21XXX'
- `/requestBody/content/application/json/examples/OK/value/criteria/aauRt1Asta:` A='COURFR2TXXX' B='IPSDPF21XXX'
- `/requestBody/content/application/json/examples/OK/value/dateTime:` A='2024-11-08T14:29:00.012345' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/aauList/aauRt1AstaEndValidity:` A='2019-06-21' B='2024-08-11'
- `/responses/200/content/application/json/examples/OK/value/aauList/aauRt1AstaInitValidity:` A='9999-12-31' B='2019-06-21'
- `/responses/200/content/application/json/examples/OK/value/aauList/bicCode:` A='CIPTBITM' B='IPSDID21'
- `/responses/200/content/application/json/examples/OK/value/dateTime:` A='9999-12-31T12:55:45.000001' B='2019-06-21T23:20:50.000001'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Internal Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /listAPs/{senderBic}`
- **A operationId**: `listAPs`
- **B operationId**: `ListAPs`
- `/operationId:` A='listAPs' B='ListAPs'
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/criteria:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/dateTime:` A='2024-11-08T14:29:00.012345' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/apList:` A='len=1' B='len=2'
- `/responses/200/content/application/json/examples/OK/value/apList[0]/dpBic:` A='CIPTBITM' B='IPSDID21'
- `/responses/200/content/application/json/examples/OK/value/apList[0]/endParticipantValidity:` A='9999-12-31' B='2024-08-11'
- `/responses/200/content/application/json/examples/OK/value/apList[0]/initParticipantValidity:` A='2024-08-11' B='2019-06-21'
- `/responses/200/content/application/json/examples/OK/value/apList[0]/name:` A='Intesa Sanpaolo' B='BFF Bank'
- `/responses/200/content/application/json/examples/OK/value/apList[0]/newBic:` A='IPSDID21XXX' B='CIPTBITMXXX'
- `/responses/200/content/application/json/examples/OK/value/apList[0]/productList:` A='len=1' B='len=2'
- `/responses/200/content/application/json/examples/OK/value/apList[0]/status:` A='CNG' B='ALL'
- `/responses/200/content/application/json/examples/OK/value/apList[0]/submittedAOSeolo:` A='A01' B='A02'
- `/responses/200/content/application/json/examples/OK/value/apList[0]/submittedAOSinst:` A='A03' B='A01'
- `/responses/200/content/application/json/examples/OK/value/apList[0]/tipsUserBic:` A='CIPTBITMXXX' B='IPSDID21XXX'
- `/responses/200/content/application/json/examples/OK/value/dateTime:` A='9999-12-31T12:55:45.000001' B='2019-06-21T23:20:50.000001'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Generic Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /listAlerts/{senderBic}`
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/offset:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/alertCode:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/alertDateTo:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/alertDescription:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/offset:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/alertCode:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/alertDateTo:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/alertDescription:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/alertDateFrom:` A='2019-06-21T23:20:50.000001' B='2024-11-08T14:29:00.012345'
- `/requestBody/content/application/json/examples/OK/value/dateTime:` A='2024-11-08T14:29:00.012345' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/alertList:` A='len=1' B='len=2'
- `/responses/200/content/application/json/examples/OK/value/alertList[0]/alertDate:` A='2019-06-21T23:20:50.000001' B='2024-11-08T14:29:00.012345'
- `/responses/200/content/application/json/examples/OK/value/alertList[0]/eventType:` A='FATAL' B='ERROR'
- `/responses/200/content/application/json/examples/OK/value/dateTime:` A='9999-12-31T12:55:45.000001' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/value/endOfList:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/numAlerts:` A='int' B='float'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Generic Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /listBeneficiary/{senderBic}`
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/offset:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/offset:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/dateTime:` A='2024-11-08T14:29:00.012345' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/dateTime:` A='9999-12-31T12:55:45.000001' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/value/endOfList:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/listBeneficiary:` A='len=1' B='len=2'
- `/responses/200/content/application/json/examples/OK/value/listBeneficiary[0]/beneficiaryAccount:` A='DE89370400440532013000' B='IT60X0542811101000000123456'
- `/responses/200/content/application/json/examples/OK/value/listBeneficiary[0]/beneficiaryName:` A='Noah Green' B='Richard Byrne'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Internal Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /listCommandStatus/{senderBic}`
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/offset:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/executionDateTimeFrom:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/executionDateTimeTo:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/requestDateTimeFrom:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/requestDateTimeTo:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/userAuthReject:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/userIssuer:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/commandType:` A='UPD' B='INS'
- `/requestBody/content/application/json/examples/OK/value/offset:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/executionDateTimeFrom:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/executionDateTimeTo:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/requestDateTimeFrom:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/requestDateTimeTo:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/userAuthReject:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/userIssuer:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/commandType:` A='UPD' B='INS'
- `/requestBody/content/application/json/examples/OK/value/dateTime:` A='9999-12-31T12:55:45.000001' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/commandList:` A='len=1' B='len=2'
- `/responses/200/content/application/json/examples/OK/value/commandList[0]/authorizationDate:` A='9999-12-31' B='2019-06-21'
- `/responses/200/content/application/json/examples/OK/value/commandList[0]/commandType:` A='RMV' B='INS'
- `/responses/200/content/application/json/examples/OK/value/commandList[0]/referenceId:` A='ID0452050454' B='ID028472018304'
- `/responses/200/content/application/json/examples/OK/value/commandList[0]/requestStatus:` A='WTG' B='ATH'
- `/responses/200/content/application/json/examples/OK/value/commandList[0]/requestor:` A='ID84739' B='ID20391'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Generic Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /listCurrencies/{senderBic}`
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/OK/value/dateTime:` A='9999-12-31T12:55:45.000001' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/listCurrencies:` A='len=1' B='len=2'
- `/responses/200/content/application/json/examples/OK/value/listCurrencies[0]/currencyCode:` A='GBP' B='EUR'
- `/responses/200/content/application/json/examples/OK/value/listCurrencies[0]/currencyName:` A='Great British pound' B='Euro'
- `/responses/200/content/application/json/examples/OK/value/listCurrencies[0]/currencyTimestamp:` A='2024-11-08T14:29:00.012345' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/value/listCurrencies[0]/maxAmountAllowed:` A=1256.0 B=3456.0
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Internal Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /listFiles/{senderBic}`
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/offset:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/dateTo:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/fileReference:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/fileStatus:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/timeTo:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/dateFrom:` A='9999-12-31' B='2019-06-21'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/fileType:` A='DRR' B='RSF'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/timeFrom:` A='int' B='str'
- `/requestBody/content/application/json/examples/OK/value/offset:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/dateTo:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/fileReference:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/fileStatus:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/timeTo:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/dateFrom:` A='9999-12-31' B='2019-06-21'
- `/requestBody/content/application/json/examples/OK/value/criteria/fileType:` A='DRR' B='RSF'
- `/requestBody/content/application/json/examples/OK/value/criteria/timeFrom:` A='int' B='str'
- `/requestBody/content/application/json/examples/OK/value/dateTime:` A='9999-12-31T12:55:45.000001' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/endOfList:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/listFiles:` A='len=1' B='len=2'
- `/responses/200/content/application/json/examples/OK/value/listFiles[0]/fileDetails/fileReference:` A='DSCI210302000015' B='DSCI210301000015'
- `/responses/200/content/application/json/examples/OK/value/listFiles[0]/fileDetails/fileType:` A='PSR' B='RSF'
- `/responses/200/content/application/json/examples/OK/value/listFiles[0]/fileStatus:` A='TSG' B='TSD'
- `/responses/200/content/application/json/examples/OK/value/listFiles[0]/netFileName:` A='SIANET' B='EBICS'
- `/responses/200/content/application/json/examples/OK/value/listFiles[0]/network:` A='EBX' B='EAS'
- `/responses/200/content/application/json/examples/OK/value/numFiles:` A=2 B=1
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Generic Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /listInstructionsFundingDefundingTIPS/{senderBic}`
- **A operationId**: `listInstructionsFundingDefundingTIPS`
- **B operationId**: `listInstructionsFundingDefunding`
- `/operationId:` A='listInstructionsFundingDefundingTIPS' B='listInstructionsFundingDefunding'
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/offset:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/amountRangeFrom:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/amountRangeTo:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/credAccoOwnBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/debAccoOwnBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/lspbranchFundsBalanceMemBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/reference:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/status:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/dateTo:` A='9999-12-31' B='2024-08-11'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/liquidityOperation:` A='PFU' B='REL'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/type:` A='APFR' B='CPFR'
- `/requestBody/content/application/json/examples/OK/value/offset:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/amountRangeFrom:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/amountRangeTo:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/credAccoOwnBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/debAccoOwnBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/lspbranchFundsBalanceMemBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/reference:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/status:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/dateTo:` A='9999-12-31' B='2024-08-11'
- `/requestBody/content/application/json/examples/OK/value/criteria/liquidityOperation:` A='PFU' B='REL'
- `/requestBody/content/application/json/examples/OK/value/criteria/type:` A='APFR' B='CPFR'
- `/requestBody/content/application/json/examples/OK/value/dateTime:` A='2024-11-08T14:29:00.012345' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/dateTime:` A='9999-12-31T12:55:45.000001' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/value/endOfList:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/response/instructions:` A='len=1' B='len=2'
- `/responses/200/content/application/json/examples/OK/value/response/instructions[0]/amount:` A=2000.11 B=9.99
- `/responses/200/content/application/json/examples/OK/value/response/instructions[0]/date:` A='2024-08-11' B='2019-06-21'
- `/responses/200/content/application/json/examples/OK/value/response/instructions[0]/debAccoOwnBic:` A='COURFR2TXXX' B='IPSDID21XXX'
- `/responses/200/content/application/json/examples/OK/value/response/instructions[0]/lac:` A='02' B='01'
- `/responses/200/content/application/json/examples/OK/value/response/instructions[0]/participantToBeCreditedBic:` A='IPSDID21' B='COURFR2T'
- `/responses/200/content/application/json/examples/OK/value/response/instructions[0]/participantToBeDebitedBic:` A='COURFR2T' B='CIPTBITM'
- `/responses/200/content/application/json/examples/OK/value/response/instructions[0]/reference:` A='ID0452050454' B='ID028472018304'
- `/responses/200/content/application/json/examples/OK/value/response/instructions[0]/status:` A='STD' B='WTG'
- `/responses/200/content/application/json/examples/OK/value/response/instructions[0]/time:` A='0,5731597222' B='0.5731597222222222'
- `/responses/200/content/application/json/examples/OK/value/response/instructions[0]/type:` A='CPFN' B='CPFR'
- `/responses/200/content/application/json/examples/OK/value/response/lspbranchFundsBalanceMemBic:` A='CIPTBITM' B='IPSDID21'
- `/responses/200/content/application/json/examples/OK/value/response/numInstructions:` A=2 B=1
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Internal Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /listLACsConfiguration/{senderBic}`
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/defaultValues:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/defaultValues:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/dateTime:` A='2024-11-08T14:29:00.012345' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/value/lacParameters:` A='len=1' B='len=2'
- `/responses/200/content/application/json/examples/OK/value/lacParameters[0]/lac:` A='02' B='01'
- `/responses/200/content/application/json/examples/OK/value/lacParameters[0]/lacAdjustmentTime:` A='00:00:01' B='16:00:00'
- `/responses/200/content/application/json/examples/OK/value/lacParameters[0]/lacSendingCutOffTime:` A='int' B='str'
- `/responses/200/content/application/json/examples/OK/value/otherSystemCutOff/openingTime:` A='00:00:01' B='16:00:00'
- `/responses/200/content/application/json/examples/OK/value/otherSystemCutOff/taw1End:` A='2024-11-10' B='2024-11-12:2024-11-11'
- `/responses/200/content/application/json/examples/OK/value/otherSystemCutOff/taw1Start:` A='2024-11-10' B='2024-11-12:2024-11-11'
- `/responses/200/content/application/json/examples/OK/value/otherSystemCutOff/taw2End:` A='2024-11-10' B='2024-11-12:2024-11-11'
- `/responses/200/content/application/json/examples/OK/value/otherSystemCutOff/taw2Start:` A='2024-11-10' B='2024-11-12:2024-11-11'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Internal Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /listMessage/{senderBic}`
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/offset:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/accOrCmbId:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/accUser:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/businessError:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/creAccOwnBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/debAccOwnBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/intraserviceLtoType:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/ltoTipsStatus:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/messageId:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/messageStatus:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/messageTypeCamt005:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/origMessId:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/origTransactionId:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/paymentStatus:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/processingDtTo:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/processingTmFrom:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/processingTmTo:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/requestedThrough:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/senderReceiverBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/settlDate:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/tipsTimestampDtFrom:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/tipsTimestampDtTo:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/tipsTimestampTmFrom:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/tipsTimestampTmTo:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/messageType:` A='camt.025' B='camt.054'
- `/requestBody/content/application/json/examples/OK/value/offset:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/accOrCmbId:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/accUser:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/businessError:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/creAccOwnBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/debAccOwnBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/intraserviceLtoType:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/ltoTipsStatus:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/messageId:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/messageStatus:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/messageTypeCamt005:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/origMessId:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/origTransactionId:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/paymentStatus:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/processingDtTo:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/processingTmFrom:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/processingTmTo:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/requestedThrough:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/senderReceiverBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/settlDate:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/tipsTimestampDtFrom:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/tipsTimestampDtTo:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/tipsTimestampTmFrom:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/tipsTimestampTmTo:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/messageType:` A='camt.025' B='camt.054'
- `/requestBody/content/application/json/examples/OK/value/dateTime:` A='9999-12-31T12:55:45.000001' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/listMessages:` A='len=1' B='len=2'
- `/responses/200/content/application/json/examples/OK/value/listMessages[0]/debAccOwnBic:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/listMessages[0]/accOrCmbId:` A='IT60X0542811101000000123456' B='DE89370400440532013000'
- `/responses/200/content/application/json/examples/OK/value/listMessages[0]/accountNumber:` A='DE89370400440532013000' B='IT60X0542811101000000123456'
- `/responses/200/content/application/json/examples/OK/value/listMessages[0]/amount:` A=2000.11 B=9.99
- `/responses/200/content/application/json/examples/OK/value/listMessages[0]/businessError:` A='DT01' B='XA01'
- `/responses/200/content/application/json/examples/OK/value/listMessages[0]/ltoTipsStatus:` A='RCON' B='RREJ'
- `/responses/200/content/application/json/examples/OK/value/listMessages[0]/ltoType:` A='DEF' B='FUN'
- `/responses/200/content/application/json/examples/OK/value/listMessages[0]/messageId:` A='P08B59450578EA544526A8DB7D060D' B='P08M59270578EA544566A8DB7D970D'
- `/responses/200/content/application/json/examples/OK/value/listMessages[0]/messageStatus:` A='RJS' B='NTF'
- `/responses/200/content/application/json/examples/OK/value/listMessages[0]/messageType:` A='camt.003' B='camt.054'
- `/responses/200/content/application/json/examples/OK/value/listMessages[0]/messageTypeCamt005:` A='Pacs.004' B='Pacs.008'
- `/responses/200/content/application/json/examples/OK/value/listMessages[0]/origMessId:` A='P08M59270578EA544566A8DB7D970D' B='P08B59450578EA544526A8DB7D060D'
- `/responses/200/content/application/json/examples/OK/value/listMessages[0]/originalTransactionId:` A='CCT000000776156311' B='CCT000000776156310'
- `/responses/200/content/application/json/examples/OK/value/listMessages[0]/paymentStatus:` A='STLD' B='PSTL'
- `/responses/200/content/application/json/examples/OK/value/listMessages[0]/senderReceiverBic:` A='CIPTBITM' B='IPSDID21'
- `/responses/200/content/application/json/examples/OK/value/listMessages[0]/settlDate:` A='2024-08-11' B='2019-06-21'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Internal Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /listParticipantOperation/{senderBic}`
- **A operationId**: `listParticipantOperation`
- **B operationId**: `ListParticipantOperation`
- `/operationId:` A='listParticipantOperation' B='ListParticipantOperation'
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/criteria:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/offset:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/offset:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/dateTime:` A='9999-12-31T12:55:45.000001' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/numRecordFound:` A=2 B=1
- `/responses/200/content/application/json/examples/OK/value/responseList:` A='len=1' B='len=2'
- `/responses/200/content/application/json/examples/OK/value/responseList[0]/authorizer:` A='ID74823' B='CO0A222'
- `/responses/200/content/application/json/examples/OK/value/responseList[0]/confirmer:` A='ID039284' B='ID403821'
- `/responses/200/content/application/json/examples/OK/value/responseList[0]/critical:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/responseList[0]/dateOfExecution:` A='2019-06-21' B='2024-08-11'
- `/responses/200/content/application/json/examples/OK/value/responseList[0]/dateOfRequest:` A='2024-08-11' B='2019-06-21'
- `/responses/200/content/application/json/examples/OK/value/responseList[0]/operationType:` A='REM' B='INS'
- `/responses/200/content/application/json/examples/OK/value/responseList[0]/requestor:` A='ID84739' B='ID20391'
- `/responses/200/content/application/json/examples/OK/value/responseList[0]/status:` A='SUB' B='WTG'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Generic Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /listPayments/{senderBic}`
- **A operationId**: `listPayments`
- **B operationId**: `ListPayments`
- `/operationId:` A='listPayments' B='ListPayments'
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/offset:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/paymentDetails/amountRange:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/paymentDetails/creditorBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/paymentDetails/debtorBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/paymentDetails/endToEndID:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/paymentDetails/instructedBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/paymentDetails/instructingBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/paymentDetails/ipStatus:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/paymentDetails/lac:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/paymentDetails/transactionId:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/paymentDetails/acceptanceDateTimeFrom:` A='2019-05-02T22:22:00.123000-01:10' B='2019-05-02T22:22:00.123-01:10'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/paymentDetails/csm:` A='TIPS' B='RT1-TIPS'
- `/requestBody/content/application/json/examples/OK/value/offset:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/paymentDetails/amountRange:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/paymentDetails/creditorBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/paymentDetails/debtorBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/paymentDetails/endToEndID:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/paymentDetails/instructedBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/paymentDetails/instructingBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/paymentDetails/ipStatus:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/paymentDetails/lac:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/paymentDetails/transactionId:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/paymentDetails/acceptanceDateTimeFrom:` A='2019-05-02T22:22:00.123000-01:10' B='2019-05-02T22:22:00.123-01:10'
- `/requestBody/content/application/json/examples/OK/value/criteria/paymentDetails/csm:` A='TIPS' B='RT1-TIPS'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/dateTime:` A='2024-11-08T14:29:00.012345' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/value/endOfList:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/listPayment[0]/paymentDetails/acceptanceDateTime:` A='2019-05-02T22:22:00.123000-01:10' B='2019-05-02T22:22:00.123-01:10'
- `/responses/200/content/application/json/examples/OK/value/listPayment[0]/paymentDetails/amount:` A=2000.11 B=9.99
- `/responses/200/content/application/json/examples/OK/value/listPayment[0]/paymentDetails/credSettMethod:` A='RT1A' B='LQPS'
- `/responses/200/content/application/json/examples/OK/value/listPayment[0]/paymentDetails/debSettMethod:` A='RT1A' B='LQPS'
- `/responses/200/content/application/json/examples/OK/value/listPayment[0]/paymentDetails/debtorBic:` A='COURFR2TXXX' B='IPSDID21XXX'
- `/responses/200/content/application/json/examples/OK/value/listPayment[0]/paymentDetails/endToEndID:` A='9912L20241107BOIST094347761' B='444596268999'
- `/responses/200/content/application/json/examples/OK/value/listPayment[0]/paymentDetails/instructedBic:` A='IPSDID21' B='CIPTBITM'
- `/responses/200/content/application/json/examples/OK/value/listPayment[0]/paymentDetails/instructingBic:` A='COURFR2T' B='IPSDID21'
- `/responses/200/content/application/json/examples/OK/value/listPayment[0]/paymentDetails/lac:` A='2' B='1'
- `/responses/200/content/application/json/examples/OK/value/listPayment[0]/paymentDetails/productId:` A='EOLO' B='INST'
- `/responses/200/content/application/json/examples/OK/value/listPayment[0]/paymentDetails/reasonCode:` A='AB07' B='AB06'
- `/responses/200/content/application/json/examples/OK/value/listPayment[0]/paymentDetails/transactionId:` A='TXID20231003JMMVPACS8041' B='TXID20231003JMMVPACS8040'
- `/responses/200/content/application/json/examples/OK/value/numPayments:` A=2 B=1
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Generic Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /listThrottlingParameters/{senderBic}`
- `/parameters[0]/schema/$ref:` A='#/components/schemas/SenderBic1' B='#/components/schemas/SenderBic2'
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/dateTime:` A='2024-11-08T14:29:00.012345' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/value/responseList/incThrottDayId:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/responseList/incThrottNightId:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/responseList/outThrottDayId:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/responseList/bic:` A='CIPTBITM' B='IPSDID21'
- `/responses/200/content/application/json/examples/OK/value/responseList/incThrottDay:` A=2 B=1
- `/responses/200/content/application/json/examples/OK/value/responseList/outThrottNightId:` A='ID02' B='ID01'
- `/responses/200/content/application/json/examples/OK/value/timeDetails/startTimeHighVolume:` A='00:00' B='16:00'
- `/responses/200/content/application/json/examples/OK/value/timeDetails/startTimeLowVolume:` A='int' B='str'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Internal Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /listTransactions/{senderBic}`
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/offset:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/amountRange:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/aos:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/instructedBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/instructingBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/lac:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/originalAmount:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/originalEndToEndID:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/originalSettlementDate:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/originalTransactionId:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/processingDate:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/reasonCode:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/timeFrom:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/timeTo:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/transactionStatus:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/csm:` A='TIPS' B='RT1-TIPS'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/productId:` A='EOLO' B='INST'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/transactionDetails/creditorBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/transactionDetails/debtorBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/transactionDetails/transactionId:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/transactionDetails/settlementDate:` A='9999-12-31' B='2019-06-21'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/transactionDetails/transactionType:` A='RCL' B='PRR'
- `/requestBody/content/application/json/examples/OK/value/offset:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/amountRange:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/aos:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/instructedBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/instructingBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/lac:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/originalAmount:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/originalEndToEndID:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/originalSettlementDate:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/originalTransactionId:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/processingDate:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/reasonCode:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/timeFrom:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/timeTo:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/transactionStatus:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/csm:` A='TIPS' B='RT1-TIPS'
- `/requestBody/content/application/json/examples/OK/value/criteria/productId:` A='EOLO' B='INST'
- `/requestBody/content/application/json/examples/OK/value/criteria/transactionDetails/creditorBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/transactionDetails/debtorBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/transactionDetails/transactionId:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/transactionDetails/settlementDate:` A='9999-12-31' B='2019-06-21'
- `/requestBody/content/application/json/examples/OK/value/criteria/transactionDetails/transactionType:` A='RCL' B='PRR'
- `/requestBody/content/application/json/examples/OK/value/dateTime:` A='2024-11-08T14:29:00.012345' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/dateTime:` A='9999-12-31T12:55:45.000001' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/value/listTransactions:` A='len=1' B='len=2'
- `/responses/200/content/application/json/examples/OK/value/listTransactions[0]/amount:` A=2000.11 B=9.99
- `/responses/200/content/application/json/examples/OK/value/listTransactions[0]/credSettMethod:` A='RT1A' B='LQPS'
- `/responses/200/content/application/json/examples/OK/value/listTransactions[0]/debSettMethod:` A='RT1A' B='LQPS'
- `/responses/200/content/application/json/examples/OK/value/listTransactions[0]/originalEndToEndID:` A='SC042411081655' B='SC042411081653'
- `/responses/200/content/application/json/examples/OK/value/listTransactions[0]/reasonCodeToBB:` A='AB07' B='AB06'
- `/responses/200/content/application/json/examples/OK/value/listTransactions[0]/reasonCodeToOB:` A='AB07' B='AB06'
- `/responses/200/content/application/json/examples/OK/value/listTransactions[0]/receptionTime:` A='2019-05-02T22:22:00.123000-01:10' B='2019-05-02T22:22:00.123-01:10'
- `/responses/200/content/application/json/examples/OK/value/listTransactions[0]/transactionDetails/transactionId:` A='T1XMQQEN3XRKRBVXEXRTMTLPH0ZZJWD' B='TP3Q7NW2CFEOSNHLMZYB5DIJEBVGOBD'
- `/responses/200/content/application/json/examples/OK/value/listTransactions[0]/transactionDetails/transactionType:` A='NRR' B='PRR'
- `/responses/200/content/application/json/examples/OK/value/listTransactions[0]/transactionStatus:` A='NTF' B='STD'
- `/responses/200/content/application/json/examples/OK/value/numTransactions:` A=2 B=1
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Internal Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `PUT /manageAAURT1ASTA/{senderBic}`
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/bicCode:` A='COURFR2T' B='IPSDID21'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/eventCode:` A='UPD' B='INS'
- `/requestBody/content/application/json/examples/OK/value/criteria/bicCode:` A='COURFR2T' B='IPSDID21'
- `/requestBody/content/application/json/examples/OK/value/criteria/eventCode:` A='UPD' B='INS'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/referenceId:` A='R400320250620104739586' B='R400320250620104740759'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Generic Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /messageDetails/{senderBic}`
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/messageId:` A='P08R59805521EA544566A8DB7P998C' B='P08M59270578EA544566A8DB7D970D'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/messageType:` A='camt.025' B='camt.054'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/senderReceiverBic:` A='COURFR2T' B='IPSDID21'
- `/requestBody/content/application/json/examples/OK/value/criteria/messageId:` A='P08R59805521EA544566A8DB7P998C' B='P08M59270578EA544566A8DB7D970D'
- `/requestBody/content/application/json/examples/OK/value/criteria/messageType:` A='camt.025' B='camt.054'
- `/requestBody/content/application/json/examples/OK/value/criteria/processingDtTm:` A='2019-06-21T23:20:50.000001' B='2024-11-08T14:29:00.012345'
- `/requestBody/content/application/json/examples/OK/value/criteria/senderReceiverBic:` A='COURFR2T' B='IPSDID21'
- `/requestBody/content/application/json/examples/OK/value/dateTime:` A='2024-11-08T14:29:00.012345' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/dateTime:` A='9999-12-31T12:55:45.000001' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/RT1GrossBalance:` A=1.0 B=123456789012.34
- `/responses/200/content/application/json/examples/OK/value/messageDetails/accCredDebIndic:` A='CRD' B='DEB'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/accToBeCred:` A='DE89370400440532013000' B='IT60X0542811101000000123456'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/accToBeDeb:` A='IT60X0542811101000000123456' B='DE89370400440532013000'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/acceptanceTimestamp:` A='float' B='str'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/accountId:` A='DE89370400440532013000' B='BE68539007547034'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/addInfo:` A='Free Text' B='Addinitional Information'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/amountToBeTraser:` A=123456789012.34 B=1.0
- `/responses/200/content/application/json/examples/OK/value/messageDetails/businessErr:` A='DT01' B='SC01'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/businessErrDes:` A='Invalid Date' B='Internal Error'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/camt004RecDtTmFromTips:` A='2024-11-08T14:29:00.012345' B='9999-12-31T12:55:45.000001'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/camt005ReceFromPartDtTm:` A='9999-12-31T12:55:45.000001' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/camt006RecDtTmFromTips:` A='2019-06-21T23:20:50.000001' B='2024-11-08T14:29:00.012345'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/camt025ReceDtTmFromTIPS:` A='9999-12-31T12:55:45.000001' B='2024-11-08T14:29:00.012345'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/cmbHeadroom:` A=300.0 B=1500.0
- `/responses/200/content/application/json/examples/OK/value/messageDetails/cmbLimitAmt:` A=1500.0 B=10.0
- `/responses/200/content/application/json/examples/OK/value/messageDetails/confReceptTimestamp:` A='float' B='str'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/confToOrigTimestamp:` A='float' B='str'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/creditDebitIndicator:` A='DBIT' B='CRDT'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/creditorAccountId:` A='BE68539007547034' B='DE89370400440532013000'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/creditorBic:` A='CIPBITMMXXX' B='COURFR2TXXX'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/debtorAccountId:` A='DE89370400440532013000' B='IT60X0542811101000000123456'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/debtorBic:` A='COURFR2TXXX' B='CIPBITMMXXX'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/endToEndId:` A='9912L20241107BOIST094347761' B='444596268999'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/fnalPayStatusCode:` A='CAND' B='STLD'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/fnalPayStatusTimestamp:` A='float' B='str'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/forwardingTimestamp:` A='float' B='str'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/ltoTipsStatus:` A='RCON' B='RREJ'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/messageId:` A='P08B59450578EA544526A8DB7D060D' B='P08M59270578EA544566A8DB7D970D'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/messageStatus:` A='NTF' B='STD'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/messageType:` A='camt.003' B='camt.054'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/notStatusTransDtTm:` A='9999-12-31T12:55:45.000001' B='2024-11-08T14:29:00.012345'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/notificationAmount:` A=999999999999.99 B=123456789012.34
- `/responses/200/content/application/json/examples/OK/value/messageDetails/notificationId:` A='210910113010' B='210910113003'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/origInstructingAg:` A='CIPBITMMXXX' B='IPSDPF21XXX'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/origMessId:` A='P08M59270578EA544566A8DB7D970D' B='P08B59450578EA544526A8DB7D060D'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/origTransAmount:` A=123456789012.34 B=1.0
- `/responses/200/content/application/json/examples/OK/value/messageDetails/origTransId:` A='CCT000000776156311' B='CCT000000776156310'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/origTransType:` A='004' B='008'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/reason:` A='DNOR' B='CNOR'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/receiverBic:` A='CIPBITMMXXX' B='IPSDPF21XXX'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/receptionTimestamp:` A='float' B='str'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/requestedThrough:` A='U2A' B='A2A'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/returnAcctTp:` A='CFCN' B='QRER'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/settlDate:` A='9999-12-31' B='2019-06-21'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/tipsAccoId:` A='IT60X0542811101000000123456' B='DE89370400440532013000'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/tipsTimestamp:` A='2024-11-08T14:29:00.012345' B='9999-12-31T12:55:45.000001'
- `/responses/200/content/application/json/examples/OK/value/messageDetails/transmStatusTransDtTm:` A='2019-06-21T23:20:50.000001' B='9999-12-31T12:55:45.000001'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Internal Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /participantDetails/{senderBic}/{bic}`
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/bic:` A='CIPTBITM' B='IPSDID21'
- `/responses/200/content/application/json/examples/OK/value/dateTime:` A='2024-11-08T14:29:00.012345' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/value/endValidityDate:` A='9999-12-31' B='2024-08-11'
- `/responses/200/content/application/json/examples/OK/value/initValidityDate:` A='2024-08-11' B='2019-06-21'
- `/responses/200/content/application/json/examples/OK/value/name:` A='Banca Mediolanum' B='BFF Bank'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory:` A='len=1' B='len=2'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/automaticLiquidityAdjustment:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/bbPositiveCnf:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/bbTimeoutMgm:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/bic:` A='IPSDID21' B='CIPTBITM'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/branchFundsBalanceId:` A='CIPBITMMXXX01' B='IPSDPF21XXX01'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/compression:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/currenciesList:` A='len=1' B='len=2'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/currenciesList[0]/currencyCode:` A='Great British pound' B='Euro'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/currenciesList[0]/currencyDescr:` A='DNOR' B='CNOR'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/dcaCashAcctNm:` A='4353' B='1234'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/drrReq:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/endParameterValidity:` A='9999-12-31' B='2019-06-21'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/fileActiveOutputNet:` A=2 B=1
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/filePrimaryNetId:` A='EBX' B='EAS'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/fileSecondaryNetId:` A='EBX' B='EAS'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/initParameterValidity:` A='2019-06-21' B='9999-12-31'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/intraLACAuthAdjst:` A='0' B='1'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/liquidityManagement:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/maxFileSize:` A=123000000 B=245000000
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/msrReq:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/name:` A='BFF Bank' B='Banca Mediolanum'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/newRole:` A='Y' B='N'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/primaryFileIntRecNetId:` A='EBX' B='EAS'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/productList:` A='len=1' B='len=2'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/productList[0]/admissionProfile:` A='CRD' B='CAD'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/productList[0]/primaryRecNetId:` A='EBX' B='EAS'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/productList[0]/primarySendNetId:` A='EBX' B='EAS'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/productList[0]/productId:` A='EOLO' B='INST'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/productList[0]/secondaryRecNetId:` A='EBX' B='EAS'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/productList[0]/secondarySendNetId:` A='EBX' B='EAS'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/psrReq:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/roleChange:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/rsfReq:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/secondaryFileIntRecNetId:` A='EBX' B='EAS'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/technicalBic:` A='0' B='1'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/tipsNetworkOption:` A='SWI' B='EAS'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/tipsOwnerBic:` A='COURFR2TXXX' B='IPSDPF21XXX'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/tipsUserBic:` A='IPSDPF21XXX' B='CIPBITMMXXX'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/transactionalPrimaryNetId:` A='EBX' B='EAS'
- `/responses/200/content/application/json/examples/OK/value/parametersHistory[0]/transactionalSecondaryNetId:` A='EBX' B='EAS'
- `/responses/200/content/application/json/examples/OK/value/status:` A='DIS' B='CNG'
- `/responses/200/content/application/json/examples/OK/value/technicalBic:` A='1' B='0'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Internal Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /participantOperationDetails/{senderBic}/{referenceId}`
- **A operationId**: `participantOperationDetails`
- **B operationId**: `ParticipantOperationDetails`
- `/operationId:` A='participantOperationDetails' B='ParticipantOperationDetails'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/apOperationDetails/admissionProfile:` A='CRD' B='CAD'
- `/responses/200/content/application/json/examples/OK/value/apOperationDetails/aosListEolo:` A='A01' B='A02'
- `/responses/200/content/application/json/examples/OK/value/apOperationDetails/aosListInst:` A='A03' B='A01'
- `/responses/200/content/application/json/examples/OK/value/apOperationDetails/bbPositiveCnf:` A='0' B='1'
- `/responses/200/content/application/json/examples/OK/value/apOperationDetails/currentPBICCode:` A='CIPBITMMXXX' B='IPSDPF21XXX'
- `/responses/200/content/application/json/examples/OK/value/apOperationDetails/endValidityDate:` A='9999-12-31' B='2019-06-21'
- `/responses/200/content/application/json/examples/OK/value/apOperationDetails/participantBic:` A='IPSDID21' B='CIPTBITM'
- `/responses/200/content/application/json/examples/OK/value/apOperationDetails/participantName:` A='BFF Bank' B='Intesa Sanpaolo'
- `/responses/200/content/application/json/examples/OK/value/apOperationDetails/requesterPBICCode:` A='CIPBITMMXXX' B='IPSDPF21XXX'
- `/responses/200/content/application/json/examples/OK/value/apOperationDetails/tipsUserBic:` A='COURFR2TXXX' B='CIPBITMMXXX'
- `/responses/200/content/application/json/examples/OK/value/dateTime:` A='2024-11-08T14:29:00.012345' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/value/massiveInsertDetails:` A='len=1' B='len=2'
- `/responses/200/content/application/json/examples/OK/value/massiveInsertDetails[0]/bbPositiveCnf:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/massiveInsertDetails[0]/bicCode:` A='IPSDPF21XXX' B='COURFR2TXXX'
- `/responses/200/content/application/json/examples/OK/value/massiveInsertDetails[0]/dpBic:` A='COURFR2TXXX' B='IPSDPF21XXX'
- `/responses/200/content/application/json/examples/OK/value/massiveInsertDetails[0]/endValidity:` A='2019-06-21' B='9999-12-31'
- `/responses/200/content/application/json/examples/OK/value/massiveInsertDetails[0]/initValidity:` A='9999-12-31' B='2024-08-11'
- `/responses/200/content/application/json/examples/OK/value/massiveInsertDetails[0]/name:` A='Intesa Sanpaolo' B='BFF Bank'
- `/responses/200/content/application/json/examples/OK/value/massiveInsertDetails[0]/submittedAOSinst:` A='A02' B='A03'
- `/responses/200/content/application/json/examples/OK/value/massiveInsertDetails[0]/tipsUserBic:` A='CIPBITMMXXX' B='COURFR2TXXX'
- `/responses/200/content/application/json/examples/OK/value/operationDetails/authorizer:` A='ID194839' B='CO0A222'
- `/responses/200/content/application/json/examples/OK/value/operationDetails/confirmer:` A='ID942014' B='ID403821'
- `/responses/200/content/application/json/examples/OK/value/operationDetails/dateOfExecution:` A='9999-12-31' B='2024-08-11'
- `/responses/200/content/application/json/examples/OK/value/operationDetails/dateOfRequest:` A='2024-08-11' B='2019-06-21'
- `/responses/200/content/application/json/examples/OK/value/operationDetails/initParameterValidity:` A='2024-08-11' B='9999-12-31'
- `/responses/200/content/application/json/examples/OK/value/operationDetails/operationType:` A='UPD' B='INS'
- `/responses/200/content/application/json/examples/OK/value/operationDetails/referenceId:` A='ID0452050454' B='ID028472018304'
- `/responses/200/content/application/json/examples/OK/value/operationDetails/requestor:` A='ID84729' B='ID20391'
- `/responses/200/content/application/json/examples/OK/value/operationDetails/status:` A='SUB' B='WTG'
- `/responses/200/content/application/json/examples/OK/value/participantOperationDetails/LSP:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/participantOperationDetails/activeOutNet:` A=2 B=1
- `/responses/200/content/application/json/examples/OK/value/participantOperationDetails/automaticLiquidityAdjus:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/participantOperationDetails/bbPositiveCnf:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/participantOperationDetails/branchFundsBalanceId:` A='COURFR2TXXX01' B='IPSDPF21XXX01'
- `/responses/200/content/application/json/examples/OK/value/participantOperationDetails/compression:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/participantOperationDetails/dpBic:` A='CIPTBITM' B='IPSDID21'
- `/responses/200/content/application/json/examples/OK/value/participantOperationDetails/drrReq:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/participantOperationDetails/endParticipantValidity:` A='2019-06-21' B='9999-12-31'
- `/responses/200/content/application/json/examples/OK/value/participantOperationDetails/filePrimaryNetId:` A='EBX' B='EAS'
- `/responses/200/content/application/json/examples/OK/value/participantOperationDetails/fileSecondaryNetId:` A='EBX' B='EAS'
- `/responses/200/content/application/json/examples/OK/value/participantOperationDetails/liquidityManagement:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/participantOperationDetails/maxFileSize:` A='int' B='float'
- `/responses/200/content/application/json/examples/OK/value/participantOperationDetails/msrReq:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/participantOperationDetails/name:` A='Intesa Sanpaolo' B='BFF Bank'
- `/responses/200/content/application/json/examples/OK/value/participantOperationDetails/primaryFileIntRecNetId:` A='SWI' B='EAS'
- `/responses/200/content/application/json/examples/OK/value/participantOperationDetails/productList:` A='len=1' B='len=2'
- `/responses/200/content/application/json/examples/OK/value/participantOperationDetails/productList[0]/primaryRecNetId:` A='SWI' B='EAS'
- `/responses/200/content/application/json/examples/OK/value/participantOperationDetails/productList[0]/primarySendNetId:` A='SWI' B='EAS'
- `/responses/200/content/application/json/examples/OK/value/participantOperationDetails/productList[0]/productId:` A='EOLO' B='INST'
- `/responses/200/content/application/json/examples/OK/value/participantOperationDetails/productList[0]/secondaryRecNetId:` A='SWF' B='EAS'
- `/responses/200/content/application/json/examples/OK/value/participantOperationDetails/productList[0]/secondarySendNetId:` A='SWF' B='EAS'
- `/responses/200/content/application/json/examples/OK/value/participantOperationDetails/psrReq:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/participantOperationDetails/rsfReq:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/participantOperationDetails/secondaryFileIntRecNetId:` A='SWF' B='EAS'
- `/responses/200/content/application/json/examples/OK/value/participantOperationDetails/submittedAOS:` A='A02' B='A01'
- `/responses/200/content/application/json/examples/OK/value/participantOperationDetails/technicalBic:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/participantOperationDetails/tipsAccoOwnBic:` A='COURFR2TXXX' B='IPSDPF21XXX'
- `/responses/200/content/application/json/examples/OK/value/participantOperationDetails/tipsAdherence:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/participantOperationDetails/tipsNetwOpt:` A='SWI' B='EAS'
- `/responses/200/content/application/json/examples/OK/value/participantOperationDetails/traInterfActiveOutputNet:` A=1 B=2
- `/responses/200/content/application/json/examples/OK/value/participantOperationDetails/transactionalPrimaryNetId:` A='EBX' B='EAS'
- `/responses/200/content/application/json/examples/OK/value/participantOperationDetails/transactionalSecondaryNetId:` A='EBX' B='EAS'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Internal Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /paymentDetails/{senderBic}`
- **A operationId**: `paymentDetails`
- **B operationId**: `PaymentDetails`
- `/operationId:` A='paymentDetails' B='PaymentDetails'
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/acceptanceDateTime:` A='2019-05-02T22:22:00.123000-01:10' B='2019-05-02T22:22:00.123-01:10'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/transactionId:` A='TXID20231003JMMVPACS8042' B='TXID20231003JMMVPACS8040'
- `/requestBody/content/application/json/examples/OK/value/criteria/acceptanceDateTime:` A='2019-05-02T22:22:00.123000-01:10' B='2019-05-02T22:22:00.123-01:10'
- `/requestBody/content/application/json/examples/OK/value/criteria/transactionId:` A='TXID20231003JMMVPACS8042' B='TXID20231003JMMVPACS8040'
- `/requestBody/content/application/json/examples/OK/value/dateTime:` A='9999-12-31T12:55:45.000001' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/acceptanceTime:` A='int' B='str'
- `/responses/200/content/application/json/examples/OK/value/amount:` A=9.99 B=2000.11
- `/responses/200/content/application/json/examples/OK/value/aos:` A='A02' B='A01'
- `/responses/200/content/application/json/examples/OK/value/confirmationTime:` A='int' B='str'
- `/responses/200/content/application/json/examples/OK/value/creditorBic:` A='COURFR2TXXX' B='CIPBITMMXXX'
- `/responses/200/content/application/json/examples/OK/value/instructingBic:` A='COURFR2T' B='IPSDID21'
- `/responses/200/content/application/json/examples/OK/value/interbankSettlementDate:` A='2024-08-11' B='2019-06-21'
- `/responses/200/content/application/json/examples/OK/value/ipStatus:` A='RBB' B='PBB'
- `/responses/200/content/application/json/examples/OK/value/paymentDetails/acceptanceDateTime:` A='2019-05-02T22:22:00.123000-01:10' B='2019-05-02T22:22:00.123-01:10'
- `/responses/200/content/application/json/examples/OK/value/paymentDetails/debtorBic:` A='CIPBITMMXXX' B='IPSDPF21XXX'
- `/responses/200/content/application/json/examples/OK/value/paymentDetails/instructedAmt:` A=389.05 B=9.99
- `/responses/200/content/application/json/examples/OK/value/paymentDetails/originalCurrency:` A='GDP' B='USD'
- `/responses/200/content/application/json/examples/OK/value/paymentDetails/trxDirection:` A='OUT' B='IN'
- `/responses/200/content/application/json/examples/OK/value/reasonCode:` A='AG09' B='AB06'
- `/responses/200/content/application/json/examples/OK/value/sendingTime:` A='int' B='str'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Internal Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `PUT /rejectParticipantOperation/{senderBic}/{referenceId}`
- **A operationId**: `rejectParticipantOperation`
- **B operationId**: `RejectParticipantOperation`
- `/operationId:` A='rejectParticipantOperation' B='RejectParticipantOperation'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/operationItem/referenceId:` A='ID4923482830492' B='ID028472018304'
- `/responses/200/content/application/json/examples/OK/value/operationItem/requestStatus:` A='RJS' B='ATH'
- `/responses/200/content/application/json/examples/OK/value/operationItem/submissionDate:` A='9999-12-31T12:55:45.000001' B='2024-11-08T14:29:00.012345'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Internal Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /transactionDetails/{senderBic}`
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/creditorBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/debtorBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/csm:` A='TIPS' B='RT1-TIPS'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/settlementDate:` A='9999-12-31' B='2019-06-21'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/transactionId:` A='TXID20231003JMMVPACS8041' B='TXID20231003JMMVPACS8040'
- `/requestBody/content/application/json/examples/OK/value/criteria/creditorBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/debtorBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/csm:` A='TIPS' B='RT1-TIPS'
- `/requestBody/content/application/json/examples/OK/value/criteria/settlementDate:` A='9999-12-31' B='2019-06-21'
- `/requestBody/content/application/json/examples/OK/value/criteria/transactionId:` A='TXID20231003JMMVPACS8041' B='TXID20231003JMMVPACS8040'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/aos:` A='A03' B='A01'
- `/responses/200/content/application/json/examples/OK/value/confirmationTimeFromBB:` A='2019-05-02T22:22:00.123000-01:10' B='2019-05-02T22:22:00.123-01:10'
- `/responses/200/content/application/json/examples/OK/value/confirmationTimeToBB:` A='2020-05-02T20:22:00.100000-01:10' B='2020-05-02T20:22:00.100-01:10'
- `/responses/200/content/application/json/examples/OK/value/creditPartyBic:` A='COURFR2TXXX' B='CIPBITMMXXX'
- `/responses/200/content/application/json/examples/OK/value/creditorSettlementMethod:` A='RT1A' B='LQPS'
- `/responses/200/content/application/json/examples/OK/value/dateTime:` A='2024-11-08T14:29:00.012345' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/value/debitPartyBic:` A='CIPBITMMXXX' B='IPSDPF21XXX'
- `/responses/200/content/application/json/examples/OK/value/debtorSettlementMethod:` A='RT1A' B='LQPS'
- `/responses/200/content/application/json/examples/OK/value/instructedBic:` A='IPSDID21' B='CIPTBITM'
- `/responses/200/content/application/json/examples/OK/value/instructingBic:` A='COURFR2T' B='IPSDID21'
- `/responses/200/content/application/json/examples/OK/value/lac:` A='02' B='01'
- `/responses/200/content/application/json/examples/OK/value/originalAmount:` A=9.99 B=389.05
- `/responses/200/content/application/json/examples/OK/value/originalTransactionId:` A='CCT000000776156311' B='CCT000000776156310'
- `/responses/200/content/application/json/examples/OK/value/productId:` A='EOLO' B='INST'
- `/responses/200/content/application/json/examples/OK/value/reasonCode:` A='AB07' B='AB06'
- `/responses/200/content/application/json/examples/OK/value/reasonCodeToBB:` A='AG09' B='AB06'
- `/responses/200/content/application/json/examples/OK/value/reasonCodeToOB:` A='AG09' B='AB06'
- `/responses/200/content/application/json/examples/OK/value/receptionTime:` A='2022-05-02T22:22:00.123000-01:10' B='2019-05-02T22:22:00.123-01:10'
- `/responses/200/content/application/json/examples/OK/value/routingType:` A='ADR' B='DIR'
- `/responses/200/content/application/json/examples/OK/value/sendingTimeToBB:` A='2020-05-02T20:22:00.100000-01:10' B='2022-05-02T22:22:00.123-01:10'
- `/responses/200/content/application/json/examples/OK/value/sendingTimeToOB:` A='2022-05-02T22:22:00.123000-01:10' B='2020-05-02T20:22:00.100-01:10'
- `/responses/200/content/application/json/examples/OK/value/transactionDetails/creditorBic:` A='IPSDPF21XXX' B='CIPBITMMXXX'
- `/responses/200/content/application/json/examples/OK/value/transactionDetails/debtorBic:` A='CIPBITMMXXX' B='IPSDPF21XXX'
- `/responses/200/content/application/json/examples/OK/value/transactionDetails/instructedAmt:` A=389.05 B=9.99
- `/responses/200/content/application/json/examples/OK/value/transactionDetails/originalCurrency:` A='CAD' B='USD'
- `/responses/200/content/application/json/examples/OK/value/transactionDetails/transactionId:` A='TXID20231003JMMVPACS8042' B='TXID20231003JMMVPACS8040'
- `/responses/200/content/application/json/examples/OK/value/transactionDetails/transactionType:` A='RCL' B='PRR'
- `/responses/200/content/application/json/examples/OK/value/transactionStatus:` A='NTF' B='STD'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Internal Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `PUT /updateAP/{senderBic}`
- **A operationId**: `updateAP`
- **B operationId**: `UpdateAP`
- `/operationId:` A='updateAP' B='UpdateAP'
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/bbPositiveCnf:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/bbTimeoutMgm:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/name:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/productList:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/submittedAOSeolo:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/submittedAOSinst:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/tipsUserBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/bicAp:` A='CIPBITMMXXX' B='IPSDPF21XXX'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/effectiveDate:` A='9999-12-31' B='2019-06-21'
- `/requestBody/content/application/json/examples/OK/value/criteria/bbPositiveCnf:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/bbTimeoutMgm:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/name:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/productList:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/submittedAOSeolo:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/submittedAOSinst:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/tipsUserBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/bicAp:` A='CIPBITMMXXX' B='IPSDPF21XXX'
- `/requestBody/content/application/json/examples/OK/value/criteria/effectiveDate:` A='9999-12-31' B='2019-06-21'
- `/requestBody/content/application/json/examples/OK/value/dateTime:` A='2024-11-08T14:29:00.012345' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/dateTime:` A='9999-12-31T12:55:45.000001' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/value/requestStatus:` A='EXE' B='ATH'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Internal Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `PUT /updateParticipant/{senderBic}`
- **A operationId**: `updateParticipant`
- **B operationId**: `participant`
- `/operationId:` A='updateParticipant' B='participant'
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/automaticLiquidityAdjustment:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/bbPositiveCnf:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/bbTimeoutMgm:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/compression:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/drrReq:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/filePrimaryNetId:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/fileSecondaryNetId:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/intraLACAuthAdjst:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/liquidityManagement:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/maxFileSize:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/msrReq:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/name:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/primaryFileIntRecNetId:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/productList:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/psrReq:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/rsfReq:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/secondaryFileIntRecNetId:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/submittedAOSeolo:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/submittedAOSinst:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/technicalBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/tipsAccountOwnerBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/tipsAdherence:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/tipsDcaAccountId:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/tipsNetworkOption:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/tipsUserBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/transactionalPrimaryNetId:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/Bad Request/value/criteria/transactionalSecondaryNetId:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/automaticLiquidityAdjustment:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/bbPositiveCnf:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/bbTimeoutMgm:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/compression:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/drrReq:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/filePrimaryNetId:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/fileSecondaryNetId:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/intraLACAuthAdjst:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/liquidityManagement:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/maxFileSize:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/msrReq:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/name:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/primaryFileIntRecNetId:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/productList:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/psrReq:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/rsfReq:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/secondaryFileIntRecNetId:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/submittedAOSeolo:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/submittedAOSinst:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/technicalBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/tipsAccountOwnerBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/tipsAdherence:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/tipsDcaAccountId:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/tipsNetworkOption:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/tipsUserBic:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/transactionalPrimaryNetId:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/criteria/transactionalSecondaryNetId:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/dateTime:` A='9999-12-31T12:55:45.000001' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/referenceId:` A='ID4923482830492' B='ID028472018304'
- `/responses/200/content/application/json/examples/OK/value/requestStatus:` A='WTG' B='ATH'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/400/content/application/json/examples/Bad Request/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCode:` A='XA01' B='SC01'
- `/responses/400/content/application/json/examples/Bad Request/value/errorCodeDescription:` A='Internal Error' B='Failed Parameter Validation'
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None


## Component Schemas
- **Added schemas (B only)**: 8
- **Removed schemas (A only)**: 5
- **Changed schemas**: 331

### Added schemas
- `DateTime2`
- `MemberDefaultDayValues1`
- `Network2`
- `OperationType2`
- `ProductId2`
- `ProductId3`
- `ReturnAcctTp1`
- `SenderBic2`

### Removed schemas
- `Criteria29`
- `DefaultLACValues2`
- `ErrorCode2`
- `ErrorCodeDescription1`
- `MemberDefaultDayValues`

### Changed schemas (details)
#### `AOSList`
- `/examples:` A='len=3' B='len=1'

#### `AccCredDebIndic`
- `/examples:` A='len=2' B='len=1'

#### `Account`
- `/examples:` A='len=3' B='len=1'

#### `ActionType`
- `/examples:` A='len=3' B='len=1'

#### `ActiveOutNet`
- `/examples:` A='len=2' B='len=1'

#### `AddInfo`
- `/examples:` A='len=3' B='len=1'

#### `AdmissionProfile`
- `/examples:` A='len=2' B='len=1'

#### `AdmissionProfile1`
- `/examples:` A='len=2' B='len=1'

#### `AlertCode`
- `/examples:` A='len=3' B='len=1'

#### `AlertDescription`
- `/examples:` A='len=3' B='len=1'

#### `Amount`
- `/examples:` A='len=3' B='len=1'

#### `Amount1`
- `/maximum:` A='only_in_a' B=None
- `/examples:` A='len=3' B='len=1'

#### `Amount2`
- `/examples:` A='len=3' B='len=1'

#### `Amount3`
- `/examples:` A='len=3' B='len=1'

#### `Aos`
- `/examples:` A='len=3' B='len=1'

#### `ApDetail`
- `/properties/details/description:` A=None B='only_in_b'
- `/properties/details/items/description:` A='only_in_a' B=None

#### `ApList`
- `/properties/productList/description:` A=None B='only_in_b'
- `/properties/productList/items/description:` A='only_in_a' B=None

#### `ApspsUnavailability`
- `/examples:` A='len=2' B='len=1'

#### `Authorizer`
- `/examples:` A='len=3' B='len=1'

#### `AutomaticLiquidityAdjus`
- `/examples:` A='len=2' B='len=1'

#### `BbPositiveCnf`
- `/examples:` A='len=2' B='len=1'

#### `BbPositiveCnf1`
- `/examples:` A='len=2' B='len=1'

#### `BbTimeoutMgm`
- `/examples:` A='len=2' B='len=1'

#### `BbTimeoutMgm1`
- `/examples:` A='len=2' B='len=1'

#### `BbTimeoutMngm`
- `/examples:` A='len=2' B='len=1'

#### `BeneficiaryAccount`
- `/examples:` A='len=3' B='len=1'

#### `BeneficiaryBankPosPaymConf`
- `/examples:` A='len=2' B='len=1'

#### `BeneficiaryBankTimeoutManag`
- `/examples:` A='len=2' B='len=1'

#### `BeneficiaryName`
- `/examples:` A='len=3' B='len=1'

#### `Bic11`
- `/pattern:` A=None B='only_in_b'
- `/examples:` A='len=3' B='len=1'
- `/examples[0]:` A='IPSDID21XXX' B='IPSDPF21XXX'
- `/minLength:` A=11 B=8

#### `Bic111`
- `/examples:` A='len=3' B='len=1'

#### `Bic11Only`
- `/examples:` A='len=3' B='len=1'

#### `Bic11Only1`
- `/examples:` A='len=3' B='len=1'

#### `Bic8`
- `/examples:` A='len=3' B='len=1'

#### `Bic81`
- `/examples:` A='len=3' B='len=1'

#### `BicAp`
- `/examples:` A='len=3' B='len=1'

#### `BranchFundsBalanceId`
- `/examples:` A='len=3' B='len=1'

#### `BranchFundsBalanceId1`
- `/examples:` A='len=3' B='len=1'

#### `BranchFundsBalanceId2`
- `/examples:` A='len=3' B='len=1'

#### `BusinessError`
- `/examples:` A='len=3' B='len=1'

#### `CmbLimitAmt`
- `/maximum:` A='only_in_a' B=None
- `/examples:` A='len=3' B='len=1'

#### `CommandType`
- `/examples:` A='len=3' B='len=1'

#### `CommandType1`
- `/examples:` A='len=3' B='len=1'

#### `Compression`
- `/examples:` A='len=2' B='len=1'

#### `Compression1`
- `/examples:` A='len=2' B='len=1'

#### `Confirmer`
- `/examples:` A='len=3' B='len=1'

#### `CredSettMethod`
- `/examples:` A='len=3' B='len=1'

#### `CredSettMethod1`
- `/examples:` A='len=3' B='len=1'

#### `CreditDebitIndicator`
- `/examples:` A='len=2' B='len=1'

#### `CreditorSettlementMethod`
- `/examples:` A='len=3' B='len=1'

#### `Criteria10`
- `/required:` A=None B='only_in_b'
- `/properties/aos:` A='only_in_a' B=None
- `/properties/bic:` A='only_in_a' B=None
- `/properties/lsp:` A='only_in_a' B=None
- `/properties/network:` A='only_in_a' B=None
- `/properties/productId:` A='only_in_a' B=None
- `/properties/status:` A='only_in_a' B=None
- `/properties/automaticLiquidityAdjustment:` A=None B='only_in_b'
- `/properties/bbPositiveCnf:` A=None B='only_in_b'
- `/properties/bbTimeoutMgm:` A=None B='only_in_b'
- `/properties/compression:` A=None B='only_in_b'
- `/properties/drrReq:` A=None B='only_in_b'
- `/properties/effectiveDate:` A=None B='only_in_b'
- `/properties/filePrimaryNetId:` A=None B='only_in_b'
- `/properties/fileSecondaryNetId:` A=None B='only_in_b'
- `/properties/intraLACAuthAdjst:` A=None B='only_in_b'
- `/properties/liquidityManagement:` A=None B='only_in_b'
- `/properties/maxFileSize:` A=None B='only_in_b'
- `/properties/msrReq:` A=None B='only_in_b'
- `/properties/name:` A=None B='only_in_b'
- `/properties/primaryFileIntRecNetId:` A=None B='only_in_b'
- `/properties/productList:` A=None B='only_in_b'
- `/properties/psrReq:` A=None B='only_in_b'
- `/properties/rsfReq:` A=None B='only_in_b'
- `/properties/secondaryFileIntRecNetId:` A=None B='only_in_b'
- `/properties/submittedAOSeolo:` A=None B='only_in_b'
- `/properties/submittedAOSinst:` A=None B='only_in_b'
- `/properties/tipsDcaAccountId:` A=None B='only_in_b'
- `/properties/tipsNetworkOption:` A=None B='only_in_b'
- `/properties/tipsUserBic:` A=None B='only_in_b'
- `/properties/transactionalPrimaryNetId:` A=None B='only_in_b'
- `/properties/transactionalSecondaryNetId:` A=None B='only_in_b'
- `/properties/technicalBic/description:` A='It indicates if the BIC is a technical one (1) or not (0)' B='It indicates if the BIC is a technical one (1) or not (0) **Validation Rule(s)** It can contain 0 or 1 (schema validation)'
- `/properties/tipsAccountOwnerBic/$ref:` A='#/components/schemas/Bic11Only' B='#/components/schemas/Bic11Only1'
- `/properties/tipsAccountOwnerBic/description:` A='TIPS DCA Account Owner for Instra-Service Liquidity Transfer (li-quidity funding/defunding)' B='The BIC(11) by which the Direct participant will be known to the ESM for settlement purpose'
- `/properties/tipsAdherence/description:` A='It indicates if the Participant joined to TIPS (1) or not (0) (Mandatory if the section is present) **Validation Rule(s)** Allowed values: - 0 = Participant not joined to TIPS - 1 = Participant joined to TIPS' B='It indicates if the Participant is allowed to settle transactions in TIPS through its TIPS DAC account. **Validation Rule(s)** It can assume the values: - “1” = YES - “0” = NO (schema validation)'

#### `Criteria11`
- `/required:` A='only_in_a' B=None
- `/properties/automaticLiquidityAdjustment:` A='only_in_a' B=None
- `/properties/bbPositiveCnf:` A='only_in_a' B=None
- `/properties/bbTimeoutMgm:` A='only_in_a' B=None
- `/properties/compression:` A='only_in_a' B=None
- `/properties/drrReq:` A='only_in_a' B=None
- `/properties/effectiveDate:` A='only_in_a' B=None
- `/properties/filePrimaryNetId:` A='only_in_a' B=None
- `/properties/fileSecondaryNetId:` A='only_in_a' B=None
- `/properties/intraLACAuthAdjst:` A='only_in_a' B=None
- `/properties/liquidityManagement:` A='only_in_a' B=None
- `/properties/maxFileSize:` A='only_in_a' B=None
- `/properties/msrReq:` A='only_in_a' B=None
- `/properties/name:` A='only_in_a' B=None
- `/properties/primaryFileIntRecNetId:` A='only_in_a' B=None
- `/properties/productList:` A='only_in_a' B=None
- `/properties/psrReq:` A='only_in_a' B=None
- `/properties/rsfReq:` A='only_in_a' B=None
- `/properties/secondaryFileIntRecNetId:` A='only_in_a' B=None
- `/properties/submittedAOSeolo:` A='only_in_a' B=None
- `/properties/submittedAOSinst:` A='only_in_a' B=None
- `/properties/technicalBic:` A='only_in_a' B=None
- `/properties/tipsAccountOwnerBic:` A='only_in_a' B=None
- `/properties/tipsAdherence:` A='only_in_a' B=None
- `/properties/tipsDcaAccountId:` A='only_in_a' B=None
- `/properties/tipsNetworkOption:` A='only_in_a' B=None
- `/properties/tipsUserBic:` A='only_in_a' B=None
- `/properties/transactionalPrimaryNetId:` A='only_in_a' B=None
- `/properties/transactionalSecondaryNetId:` A='only_in_a' B=None
- `/properties/aos:` A=None B='only_in_b'
- `/properties/bicAp:` A=None B='only_in_b'
- `/properties/dpBic:` A=None B='only_in_b'
- `/properties/productId:` A=None B='only_in_b'
- `/properties/status:` A=None B='only_in_b'

#### `Criteria12`
- `/required:` A=None B='only_in_b'
- `/properties/aos:` A='only_in_a' B=None
- `/properties/dpBic:` A='only_in_a' B=None
- `/properties/productId:` A='only_in_a' B=None
- `/properties/status:` A='only_in_a' B=None
- `/properties/bbPositiveCnf:` A=None B='only_in_b'
- `/properties/bbTimeoutMgm:` A=None B='only_in_b'
- `/properties/effectiveDate:` A=None B='only_in_b'
- `/properties/name:` A=None B='only_in_b'
- `/properties/productList:` A=None B='only_in_b'
- `/properties/submittedAOSeolo:` A=None B='only_in_b'
- `/properties/submittedAOSinst:` A=None B='only_in_b'
- `/properties/tipsUserBic:` A=None B='only_in_b'
- `/properties/bicAp/$ref:` A='#/components/schemas/Bic11Only' B='#/components/schemas/Bic11Only1'
- `/properties/bicAp/description:` A='The BIC of the searched AP' B='The BIC of the inquired AP'

#### `Criteria13`
- `/properties/bbPositiveCnf:` A='only_in_a' B=None
- `/properties/bbTimeoutMgm:` A='only_in_a' B=None
- `/properties/name:` A='only_in_a' B=None
- `/properties/productList:` A='only_in_a' B=None
- `/properties/submittedAOSeolo:` A='only_in_a' B=None
- `/properties/submittedAOSinst:` A='only_in_a' B=None
- `/properties/tipsUserBic:` A='only_in_a' B=None
- `/properties/effectiveEndValidityDate:` A=None B='only_in_b'
- `/properties/newStatus:` A=None B='only_in_b'
- `/properties/bicAp/$ref:` A='#/components/schemas/Bic11Only1' B='#/components/schemas/Bic11Only'
- `/properties/bicAp/description:` A='The BIC of the inquired AP' B='The BIC of the AP'
- `/properties/effectiveDate/description:` A='It indicates the future starting date for the planned changes **Validation Rule(s)** A date >= P Initial Validity Date between tomorrow and the EndValidityDate of the Participant (ErrorCode DT01)' B='It indicates the future starting date for the planned changes **Validation Rule(s)** For Critical parameter: • if on Monday W1 the first effective date will be Tuesday W3 • if between Tuesday and Sunday W1 the first effective date will be Tuesday of the W4 (ErrorCode DT01) • it must be greater than Current Date + 2 calendar days (ErrorCode DT01)'
- `/required:` A='len=2' B='len=3'

#### `Criteria14`
- `/properties/effectiveDate:` A='only_in_a' B=None
- `/properties/effectiveEndValidityDate:` A='only_in_a' B=None
- `/properties/newStatus:` A='only_in_a' B=None
- `/properties/bbPositiveCnf:` A=None B='only_in_b'
- `/properties/bbTimeoutMgm:` A=None B='only_in_b'
- `/properties/endParticipantValidity:` A=None B='only_in_b'
- `/properties/initParticipantValidity:` A=None B='only_in_b'
- `/properties/name:` A=None B='only_in_b'
- `/properties/productList:` A=None B='only_in_b'
- `/properties/submittedAOSeolo:` A=None B='only_in_b'
- `/properties/submittedAOSinst:` A=None B='only_in_b'
- `/properties/tipsUserBic:` A=None B='only_in_b'
- `/properties/bicAp/description:` A='The BIC of the AP' B='The BIC of the new AP **Validation Rule(s)** If already present in the system it must have ‘disabled’ status with respect to the InitValidityDate(ErrorCode PY01)'
- `/required:` A='len=3' B='len=6'
- `/required[1]:` A='effectiveDate' B='endParticipantValidity'
- `/required[2]:` A='newStatus' B='initParticipantValidity'

#### `Criteria15`
- `/properties/bbPositiveCnf:` A='only_in_a' B=None
- `/properties/bbTimeoutMgm:` A='only_in_a' B=None
- `/properties/bicAp:` A='only_in_a' B=None
- `/properties/endParticipantValidity:` A='only_in_a' B=None
- `/properties/initParticipantValidity:` A='only_in_a' B=None
- `/properties/name:` A='only_in_a' B=None
- `/properties/productList:` A='only_in_a' B=None
- `/properties/submittedAOSeolo:` A='only_in_a' B=None
- `/properties/submittedAOSinst:` A='only_in_a' B=None
- `/properties/tipsUserBic:` A='only_in_a' B=None
- `/properties/apspsUnavailability:` A=None B='only_in_b'
- `/properties/endDateTime:` A=None B='only_in_b'
- `/properties/eventCode:` A=None B='only_in_b'
- `/properties/eventDescription:` A=None B='only_in_b'
- `/properties/idOfUnavailableParty:` A=None B='only_in_b'
- `/properties/messageId:` A=None B='only_in_b'
- `/properties/productsUnavailable:` A=None B='only_in_b'
- `/properties/startDateTime:` A=None B='only_in_b'
- `/properties/unavailableBic:` A=None B='only_in_b'
- `/required[0]:` A='bicAp' B='endDateTime'
- `/required[1]:` A='endParticipantValidity' B='eventCode'
- `/required[2]:` A='initParticipantValidity' B='messageId'
- `/required[3]:` A='name' B='productsUnavailable'
- `/required[4]:` A='productList' B='startDateTime'
- `/required[5]:` A='tipsUserBic' B='unavailableBic'

#### `Criteria16`
- `/required:` A='only_in_a' B=None
- `/properties/apspsUnavailability:` A='only_in_a' B=None
- `/properties/endDateTime:` A='only_in_a' B=None
- `/properties/eventCode:` A='only_in_a' B=None
- `/properties/eventDescription:` A='only_in_a' B=None
- `/properties/idOfUnavailableParty:` A='only_in_a' B=None
- `/properties/messageId:` A='only_in_a' B=None
- `/properties/productsUnavailable:` A='only_in_a' B=None
- `/properties/startDateTime:` A='only_in_a' B=None
- `/properties/fromTIPS:` A=None B='only_in_b'
- `/properties/unavailableBic/description:` A='BIC of the Participant or APSP that is going to be unavailable. **Validation Rule(s)** It must be equal to the BIC of the sender. If different, it must be one APSP of the SenderBic. (ErrorCode XA06). Field used for duplicate checking (error code AM05)' B='BIC of the Participant or APSP that could be unavailable. **Validation Rule(s)** It must be one of the following: - Blank: the response shall provide all the BIC present in the admi.004 directory. - A direct Participant BIC that is enabled, suspended or r-only in the CS repository on the current calendar date (ErrorCode PY01). - An APSP BIC that is enabled, suspended or r-only in the CS repository on the current calendar date (ErrorCode PY01). The list shall be ordered in alphabetic order.'

#### `Criteria17`
- `/properties/fromTIPS:` A='only_in_a' B=None
- `/properties/unavailableBic:` A='only_in_a' B=None
- `/properties/authorizer:` A=None B='only_in_b'
- `/properties/confirmer:` A=None B='only_in_b'
- `/properties/critical:` A=None B='only_in_b'
- `/properties/dateOfConfirmFrom:` A=None B='only_in_b'
- `/properties/dateOfConfirmTo:` A=None B='only_in_b'
- `/properties/dateOfExecutionFrom:` A=None B='only_in_b'
- `/properties/dateOfExecutionTo:` A=None B='only_in_b'
- `/properties/dateOfRequestFrom:` A=None B='only_in_b'
- `/properties/dateOfRequestTo:` A=None B='only_in_b'
- `/properties/operationType:` A=None B='only_in_b'
- `/properties/referenceId:` A=None B='only_in_b'
- `/properties/requestor:` A=None B='only_in_b'
- `/properties/status:` A=None B='only_in_b'

#### `Criteria18`
- `/required:` A=None B='only_in_b'
- `/properties/authorizer:` A='only_in_a' B=None
- `/properties/confirmer:` A='only_in_a' B=None
- `/properties/critical:` A='only_in_a' B=None
- `/properties/dateOfConfirmFrom:` A='only_in_a' B=None
- `/properties/dateOfConfirmTo:` A='only_in_a' B=None
- `/properties/dateOfExecutionFrom:` A='only_in_a' B=None
- `/properties/dateOfExecutionTo:` A='only_in_a' B=None
- `/properties/dateOfRequestFrom:` A='only_in_a' B=None
- `/properties/dateOfRequestTo:` A='only_in_a' B=None
- `/properties/operationType:` A='only_in_a' B=None
- `/properties/referenceId:` A='only_in_a' B=None
- `/properties/requestor:` A='only_in_a' B=None
- `/properties/status:` A='only_in_a' B=None
- `/properties/aauRt1Asta:` A=None B='only_in_b'
- `/properties/aauRt1AstaEndValidity:` A=None B='only_in_b'
- `/properties/aauRt1AstaInitValidity:` A=None B='only_in_b'
- `/properties/bicCode:` A=None B='only_in_b'
- `/properties/eventCode:` A=None B='only_in_b'

#### `Criteria19`
- `/properties/aauRt1AstaEndValidity:` A='only_in_a' B=None
- `/properties/aauRt1AstaInitValidity:` A='only_in_a' B=None
- `/properties/eventCode:` A='only_in_a' B=None
- `/properties/aauRt1Asta/$ref:` A='#/components/schemas/Bic11Only' B='#/components/schemas/Bic11Only1'
- `/required:` A='len=5' B='len=2'
- `/required[1]:` A='aauRt1AstaEndValidity' B='bicCode'

#### `Criteria20`
- `/properties/aauRt1Asta:` A='only_in_a' B=None
- `/properties/bicCode:` A='only_in_a' B=None
- `/properties/paymentDetails:` A=None B='only_in_b'
- `/required:` A='len=2' B='len=1'
- `/required[0]:` A='aauRt1Asta' B='paymentDetails'

#### `Criteria21`
- `/properties/paymentDetails:` A='only_in_a' B=None
- `/properties/acceptanceDateTime:` A=None B='only_in_b'
- `/properties/csm:` A=None B='only_in_b'
- `/properties/debtorBic:` A=None B='only_in_b'
- `/properties/transactionId:` A=None B='only_in_b'
- `/required:` A='len=1' B='len=4'
- `/required[0]:` A='paymentDetails' B='acceptanceDateTime'

#### `Criteria22`
- `/properties/acceptanceDateTime:` A='only_in_a' B=None
- `/properties/debtorBic:` A='only_in_a' B=None
- `/properties/transactionId:` A='only_in_a' B=None
- `/properties/amountRange:` A=None B='only_in_b'
- `/properties/aos:` A=None B='only_in_b'
- `/properties/instructedBic:` A=None B='only_in_b'
- `/properties/instructingBic:` A=None B='only_in_b'
- `/properties/lac:` A=None B='only_in_b'
- `/properties/originalAmount:` A=None B='only_in_b'
- `/properties/originalEndToEndID:` A=None B='only_in_b'
- `/properties/originalSettlementDate:` A=None B='only_in_b'
- `/properties/originalTransactionId:` A=None B='only_in_b'
- `/properties/processingDate:` A=None B='only_in_b'
- `/properties/productId:` A=None B='only_in_b'
- `/properties/reasonCode:` A=None B='only_in_b'
- `/properties/timeFrom:` A=None B='only_in_b'
- `/properties/timeTo:` A=None B='only_in_b'
- `/properties/transactionDetails:` A=None B='only_in_b'
- `/properties/transactionStatus:` A=None B='only_in_b'
- `/required:` A='len=4' B='len=3'
- `/required[0]:` A='acceptanceDateTime' B='csm'
- `/required[1]:` A='csm' B='productId'
- `/required[2]:` A='debtorBic' B='transactionDetails'

#### `Criteria23`
- `/properties/amountRange:` A='only_in_a' B=None
- `/properties/aos:` A='only_in_a' B=None
- `/properties/instructedBic:` A='only_in_a' B=None
- `/properties/instructingBic:` A='only_in_a' B=None
- `/properties/lac:` A='only_in_a' B=None
- `/properties/originalAmount:` A='only_in_a' B=None
- `/properties/originalEndToEndID:` A='only_in_a' B=None
- `/properties/originalSettlementDate:` A='only_in_a' B=None
- `/properties/originalTransactionId:` A='only_in_a' B=None
- `/properties/processingDate:` A='only_in_a' B=None
- `/properties/productId:` A='only_in_a' B=None
- `/properties/reasonCode:` A='only_in_a' B=None
- `/properties/timeFrom:` A='only_in_a' B=None
- `/properties/timeTo:` A='only_in_a' B=None
- `/properties/transactionDetails:` A='only_in_a' B=None
- `/properties/transactionStatus:` A='only_in_a' B=None
- `/properties/creditorBic:` A=None B='only_in_b'
- `/properties/debtorBic:` A=None B='only_in_b'
- `/properties/settlementDate:` A=None B='only_in_b'
- `/properties/transactionId:` A=None B='only_in_b'
- `/properties/transactionType:` A=None B='only_in_b'
- `/required:` A='len=3' B='len=4'
- `/required[1]:` A='productId' B='settlementDate'
- `/required[2]:` A='transactionDetails' B='transactionId'

#### `Criteria24`
- `/properties/creditorBic:` A='only_in_a' B=None
- `/properties/csm:` A='only_in_a' B=None
- `/properties/debtorBic:` A='only_in_a' B=None
- `/properties/settlementDate:` A='only_in_a' B=None
- `/properties/transactionId:` A='only_in_a' B=None
- `/properties/transactionType:` A='only_in_a' B=None
- `/properties/dateFrom:` A=None B='only_in_b'
- `/properties/dateTo:` A=None B='only_in_b'
- `/properties/fileReference:` A=None B='only_in_b'
- `/properties/fileStatus:` A=None B='only_in_b'
- `/properties/fileType:` A=None B='only_in_b'
- `/properties/timeFrom:` A=None B='only_in_b'
- `/properties/timeTo:` A=None B='only_in_b'
- `/required:` A='len=4' B='len=3'
- `/required[0]:` A='csm' B='dateFrom'
- `/required[1]:` A='settlementDate' B='fileType'
- `/required[2]:` A='transactionId' B='timeFrom'

#### `Criteria25`
- `/properties/dateFrom:` A='only_in_a' B=None
- `/properties/dateTo:` A='only_in_a' B=None
- `/properties/fileStatus:` A='only_in_a' B=None
- `/properties/timeFrom:` A='only_in_a' B=None
- `/properties/timeTo:` A='only_in_a' B=None
- `/properties/fileDate:` A=None B='only_in_b'
- `/properties/fileType/description:` A='The file type **Validation Rule(s)** It must be one of the configured values in the system. The possible values: PSR” “DRR” “RSF” “MSR” “BCA” “BCS” "RTF-TIPS" "RTF-INST" "RTF-OLO" "RTF-IXB" (ErrorCode XA03)' B='The file type of the file **Validation Rule(s)** The file corresponding to the file reference must exist in the system, ref.10.7 (ErrorCode XA03)'
- `/required[0]:` A='dateFrom' B='fileDate'
- `/required[1]:` A='fileType' B='fileReference'
- `/required[2]:` A='timeFrom' B='fileType'

#### `Criteria26`
- `/properties/fileDate:` A='only_in_a' B=None
- `/properties/fileReference:` A='only_in_a' B=None
- `/properties/fileType:` A='only_in_a' B=None
- `/properties/commandType:` A=None B='only_in_b'
- `/properties/executionDateTimeFrom:` A=None B='only_in_b'
- `/properties/executionDateTimeTo:` A=None B='only_in_b'
- `/properties/requestDateTimeFrom:` A=None B='only_in_b'
- `/properties/requestDateTimeTo:` A=None B='only_in_b'
- `/properties/userAuthReject:` A=None B='only_in_b'
- `/properties/userIssuer:` A=None B='only_in_b'
- `/required:` A='len=3' B='len=1'
- `/required[0]:` A='fileDate' B='commandType'

#### `Criteria27`
- `/properties/commandType:` A='only_in_a' B=None
- `/properties/executionDateTimeFrom:` A='only_in_a' B=None
- `/properties/executionDateTimeTo:` A='only_in_a' B=None
- `/properties/requestDateTimeFrom:` A='only_in_a' B=None
- `/properties/requestDateTimeTo:` A='only_in_a' B=None
- `/properties/userAuthReject:` A='only_in_a' B=None
- `/properties/userIssuer:` A='only_in_a' B=None
- `/properties/alertCode:` A=None B='only_in_b'
- `/properties/alertDateFrom:` A=None B='only_in_b'
- `/properties/alertDateTo:` A=None B='only_in_b'
- `/properties/alertDescription:` A=None B='only_in_b'
- `/required[0]:` A='commandType' B='alertDateFrom'

#### `Criteria28`
- `/properties/alertCode:` A='only_in_a' B=None
- `/properties/alertDateFrom:` A='only_in_a' B=None
- `/properties/alertDateTo:` A='only_in_a' B=None
- `/properties/alertDescription:` A='only_in_a' B=None
- `/properties/bic:` A=None B='only_in_b'
- `/properties/month:` A=None B='only_in_b'
- `/properties/year:` A=None B='only_in_b'
- `/required:` A='len=1' B='len=3'
- `/required[0]:` A='alertDateFrom' B='bic'

#### `Criteria8`
- `/properties/beneficiaryAcc:` A=None B='only_in_b'
- `/properties/beneficiaryBic:` A=None B='only_in_b'
- `/properties/beneficiaryName:` A=None B='only_in_b'
- `/properties/operationType:` A=None B='only_in_b'
- `/properties/participantBic/description:` A='The Participant Bic' B='The Participant Bic **Validation Rule(s)** Must be equal to the BIC of the senderBic (ErrorCodeXA02)'
- `/required:` A='len=1' B='len=3'
- `/required[0]:` A='participantBic' B='beneficiaryBic'

#### `Criteria9`
- `/required:` A='only_in_a' B=None
- `/properties/beneficiaryAcc:` A='only_in_a' B=None
- `/properties/beneficiaryBic:` A='only_in_a' B=None
- `/properties/beneficiaryName:` A='only_in_a' B=None
- `/properties/operationType:` A='only_in_a' B=None
- `/properties/participantBic:` A='only_in_a' B=None
- `/properties/aos:` A=None B='only_in_b'
- `/properties/bic:` A=None B='only_in_b'
- `/properties/lsp:` A=None B='only_in_b'
- `/properties/network:` A=None B='only_in_b'
- `/properties/productId:` A=None B='only_in_b'
- `/properties/status:` A=None B='only_in_b'
- `/properties/technicalBic:` A=None B='only_in_b'
- `/properties/tipsAccountOwnerBic:` A=None B='only_in_b'
- `/properties/tipsAdherence:` A=None B='only_in_b'

#### `Critical`
- `/examples:` A='len=2' B='len=1'

#### `Csm`
- `/examples:` A='len=2' B='len=1'

#### `Csm1`
- `/examples:` A='len=2' B='len=1'

#### `CurrencyCode`
- `/examples:` A='len=3' B='len=1'

#### `CurrencyCode1`
- `/examples:` A='len=3' B='len=1'

#### `CurrencyDescr`
- `/examples:` A='len=3' B='len=1'

#### `CurrencyName`
- `/examples:` A='len=3' B='len=1'

#### `CurrencyTimestamp`
- `/examples:` A='len=3' B='len=1'

#### `CurrentPBICCode`
- `/examples:` A='len=3' B='len=1'

- _(truncated 251 more changed schemas)_