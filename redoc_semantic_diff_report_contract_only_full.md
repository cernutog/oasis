# Redocly HTML Semantic Diff Report

## Inputs
- **A**: `C:\EBA Clearing\APIs\HTML Docs\EBACL_RT1_20260223_Openapi3.1_RT1_API_Participants_4_0_v20260613.html`
- **B**: `C:\EBA Clearing\APIs\HTML Docs\EBACL_RT1_20260306_Openapi3.1_RT1_API_Participants_4_0_v20260613.html`

## Compare options
- **normalize_whitespace**: True
- **ignore_examples**: True
- **ignore_x_sandbox**: True

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
- **Changed referenced schemas (transitive)**: `ApDetail`, `DateTime`, `Details`, `ErrorResponse`, `ProductList4`, `apDetailsResponse`
- `/operationId:` A='apDetails' B='APDetails'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `PUT /beneficiaryManagement/{senderBic}`
- **Changed referenced schemas (transitive)**: `Criteria8`, `Criteria9`, `DateTime`, `ErrorResponse`, `beneficiaryManagementRequest`
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `PUT /changeStatusAP/{senderBic}`
- **A operationId**: `changeStatusAP`
- **B operationId**: `ChangeStatusAP`
- **Changed referenced schemas (transitive)**: `Criteria13`, `Criteria14`, `DateTime`, `ErrorResponse`, `changeStatusAPRequest`
- `/operationId:` A='changeStatusAP' B='ChangeStatusAP'
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `PUT /commandDelete/{senderBic}/{referenceId}`
- **Changed referenced schemas (transitive)**: `DateTime`, `ErrorResponse`
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /commandStatusDetails/{senderBic}/{referenceId}`
- **Changed referenced schemas (transitive)**: `DateTime`, `ErrorResponse`
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `PUT /communicationOfUnavailability/{senderBic}`
- **A operationId**: `communicationOfUnavailability`
- **B operationId**: `CommunicationOfUnavailability`
- **Changed referenced schemas (transitive)**: `Criteria15`, `Criteria16`, `DateTime`, `ErrorResponse`, `communicationOfUnavailabilityRequest`
- `/operationId:` A='communicationOfUnavailability' B='CommunicationOfUnavailability'
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /currentNetPosition/{senderBic}`
- **Changed referenced schemas (transitive)**: `DateTime`, `ErrorResponse`, `currentNetPositionResponse`
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `PUT /defaultPosition/{senderBic}`
- **Changed referenced schemas (transitive)**: `DateTime`, `DefaultDayValues`, `ErrorResponse`, `LacAmount`
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `PUT /defunding/{senderBic}`
- **A operationId**: `defunding`
- **B operationId**: `releaseLiquidiy`
- **Changed referenced schemas (transitive)**: `Amount1`, `DateTime`, `ErrorResponse`
- `/operationId:` A='defunding' B='releaseLiquidiy'
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `PUT /exceptionPositionCalendar/{senderBic}`
- **Changed referenced schemas (transitive)**: `DateTime`, `ErrorResponse`, `LacAmount`, `exceptionPositionCalendarRequest`
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /fileDetails/{senderBic}`
- **Changed referenced schemas (transitive)**: `Criteria25`, `Criteria26`, `DateTime`, `ErrorResponse`, `IpData`, `IpData1`, `IpDataDRR`, `ListDRRData`, `ListMSRData`, `PrrData`, `PrrData1`, `PrrDataDRR`, `RecallData`, `RecallData1`, `fileDetailsRequest`, `fileDetailsResponse`
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `PUT /funding/{senderBic}`
- **Changed referenced schemas (transitive)**: `Amount1`, `DateTime`, `ErrorResponse`
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `PUT /generateOutboundLto/{senderBic}`
- **Changed referenced schemas (transitive)**: `DateTime`, `ErrorResponse`
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `PUT /generatePaymentStatusQuery/{senderBic}`
- **Changed referenced schemas (transitive)**: `DateTime`, `ErrorResponse`
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /getAccountBalance/{senderBic}`
- **Changed referenced schemas (transitive)**: `DateTime`, `ErrorResponse`
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /getDefaultPosition/{senderBic}`
- **Changed referenced schemas (transitive)**: `DateTime`, `DefaultLACValues1`, `ErrorResponse`, `LacAmount`, `LspBicDefaultDayValues`, `Values`
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /getExceptionPositionCalendar/{senderBic}`
- **Changed referenced schemas (transitive)**: `DateTime`, `ErrorResponse`, `LacAmount`, `Response`
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /getParticipants/{senderBic}`
- **Changed referenced schemas (transitive)**: `Criteria10`, `Criteria9`, `DateTime`, `ErrorResponse`, `ResponseList`, `getParticipantsRequest`, `getParticipantsResponse`
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /inquiryUnavailability/{senderBic}`
- **Changed referenced schemas (transitive)**: `Criteria16`, `Criteria17`, `DateTime`, `ErrorResponse`, `inquiryUnavailabilityRequest`
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `PUT /insertAP/{senderBic}`
- **A operationId**: `insertAP`
- **B operationId**: `InsertAP`
- **Changed referenced schemas (transitive)**: `Criteria14`, `Criteria15`, `DateTime`, `ErrorResponse`, `ProductList6`, `insertAPRequest`
- `/operationId:` A='insertAP' B='InsertAP'
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /instructionDetails/{senderBic}/{referenceId}`
- **A operationId**: `instructionDetails`
- **B operationId**: `instructionDeteils`
- **Changed referenced schemas (transitive)**: `DateTime`, `ErrorResponse`
- `/operationId:` A='instructionDetails' B='instructionDeteils'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /interestAmounts/{senderBic}`
- **Changed referenced schemas (transitive)**: `Criteria28`, `DateTime`, `ErrorResponse`, `interestAmountsRequest`, `interestAmountsResponse`
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `PUT /liquidityTransfer/{senderBic}`
- **Changed referenced schemas (transitive)**: `DateTime`, `ErrorResponse`
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /listAAURT1ASTA/{senderBic}`
- **Changed referenced schemas (transitive)**: `Criteria19`, `Criteria20`, `DateTime`, `ErrorResponse`, `listAAURT1ASTARequest`
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /listAPs/{senderBic}`
- **A operationId**: `listAPs`
- **B operationId**: `ListAPs`
- **Changed referenced schemas (transitive)**: `ApList`, `Criteria11`, `Criteria12`, `DateTime`, `ErrorResponse`, `listAPsRequest`
- `/operationId:` A='listAPs' B='ListAPs'
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /listAlerts/{senderBic}`
- **Changed referenced schemas (transitive)**: `Criteria27`, `Criteria28`, `DateTime`, `ErrorResponse`, `listAlertsRequest`, `listAlertsResponse`
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /listBeneficiary/{senderBic}`
- **Changed referenced schemas (transitive)**: `Criteria8`, `DateTime`, `ErrorResponse`, `listBeneficiaryRequest`, `listBeneficiaryResponse`
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /listCommandStatus/{senderBic}`
- **Changed referenced schemas (transitive)**: `Criteria26`, `Criteria27`, `DateTime`, `ErrorResponse`, `listCommandStatusRequest`
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /listCurrencies/{senderBic}`
- **Changed referenced schemas (transitive)**: `DateTime`, `ErrorResponse`, `listCurrenciesResponse`
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /listFiles/{senderBic}`
- **Changed referenced schemas (transitive)**: `Criteria24`, `Criteria25`, `DateTime`, `ErrorResponse`, `listFilesRequest`, `listFilesResponse`
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /listInstructionsFundingDefundingTIPS/{senderBic}`
- **A operationId**: `listInstructionsFundingDefundingTIPS`
- **B operationId**: `listInstructionsFundingDefunding`
- **Changed referenced schemas (transitive)**: `DateTime`, `ErrorResponse`, `Response1`
- `/operationId:` A='listInstructionsFundingDefundingTIPS' B='listInstructionsFundingDefunding'
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /listLACsConfiguration/{senderBic}`
- **Changed referenced schemas (transitive)**: `DateTime`, `ErrorResponse`, `listLACsConfigurationResponse`
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /listMessage/{senderBic}`
- **Changed referenced schemas (transitive)**: `DateTime`, `ErrorResponse`, `listMessageResponse`
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /listParticipantOperation/{senderBic}`
- **A operationId**: `listParticipantOperation`
- **B operationId**: `ListParticipantOperation`
- **Changed referenced schemas (transitive)**: `Criteria17`, `Criteria18`, `DateTime`, `ErrorResponse`, `listParticipantOperationRequest`
- `/operationId:` A='listParticipantOperation' B='ListParticipantOperation'
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /listPayments/{senderBic}`
- **A operationId**: `listPayments`
- **B operationId**: `ListPayments`
- **Changed referenced schemas (transitive)**: `Criteria20`, `Criteria21`, `DateTime`, `ErrorResponse`, `listPaymentsRequest`, `listPaymentsResponse`
- `/operationId:` A='listPayments' B='ListPayments'
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /listThrottlingParameters/{senderBic}`
- **Changed referenced schemas (transitive)**: `DateTime`, `ErrorResponse`, `ThrottNumber`, `listThrottlingParametersRequest`, `listThrottlingParametersResponse`
- `/parameters[0]/schema/$ref:` A='#/components/schemas/SenderBic1' B='#/components/schemas/SenderBic2'
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /listTransactions/{senderBic}`
- **Changed referenced schemas (transitive)**: `Criteria22`, `Criteria23`, `DateTime`, `ErrorResponse`, `listTransactionsRequest`, `listTransactionsResponse`
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `PUT /manageAAURT1ASTA/{senderBic}`
- **Changed referenced schemas (transitive)**: `Criteria18`, `Criteria19`, `DateTime`, `ErrorResponse`, `manageAAURT1ASTARequest`
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /messageDetails/{senderBic}`
- **Changed referenced schemas (transitive)**: `Bic11`, `CmbLimitAmt`, `DateTime`, `ErrorResponse`, `MessageDetails`
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /participantDetails/{senderBic}/{bic}`
- **Changed referenced schemas (transitive)**: `DateTime`, `ErrorResponse`, `ParametersHistory`, `participantDetailsResponse`
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /participantOperationDetails/{senderBic}/{referenceId}`
- **A operationId**: `participantOperationDetails`
- **B operationId**: `ParticipantOperationDetails`
- **Changed referenced schemas (transitive)**: `Bic11`, `DateTime`, `ErrorResponse`, `MaxFileSize2`, `OperationDetails`, `ParticipantOperationDetails`
- `/operationId:` A='participantOperationDetails' B='ParticipantOperationDetails'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /paymentDetails/{senderBic}`
- **A operationId**: `paymentDetails`
- **B operationId**: `PaymentDetails`
- **Changed referenced schemas (transitive)**: `Bic11`, `Criteria21`, `Criteria22`, `DateTime`, `ErrorResponse`, `paymentDetailsRequest`
- `/operationId:` A='paymentDetails' B='PaymentDetails'
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `PUT /rejectParticipantOperation/{senderBic}/{referenceId}`
- **A operationId**: `rejectParticipantOperation`
- **B operationId**: `RejectParticipantOperation`
- **Changed referenced schemas (transitive)**: `DateTime`, `ErrorResponse`
- `/operationId:` A='rejectParticipantOperation' B='RejectParticipantOperation'
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `POST /transactionDetails/{senderBic}`
- **Changed referenced schemas (transitive)**: `Bic11`, `Criteria23`, `Criteria24`, `DateTime`, `ErrorResponse`, `transactionDetailsRequest`
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `PUT /updateAP/{senderBic}`
- **A operationId**: `updateAP`
- **B operationId**: `UpdateAP`
- **Changed referenced schemas (transitive)**: `Criteria12`, `Criteria13`, `DateTime`, `ErrorResponse`, `ProductList5`, `updateAPRequest`
- `/operationId:` A='updateAP' B='UpdateAP'
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None

#### `PUT /updateParticipant/{senderBic}`
- **A operationId**: `updateParticipant`
- **B operationId**: `participant`
- **Changed referenced schemas (transitive)**: `Criteria10`, `Criteria11`, `DateTime`, `ErrorResponse`, `updateParticipantRequest`
- `/operationId:` A='updateParticipant' B='participant'
- `/requestBody/required:` A='only_in_a' B=None
- `/responses/204/content:` A='only_in_a' B=None
- `/responses/401/content:` A='only_in_a' B=None
- `/responses/403/content:` A='only_in_a' B=None
- `/responses/404/content:` A='only_in_a' B=None
- `/responses/429/content:` A='only_in_a' B=None
- `/responses/500/content:` A='only_in_a' B=None


## Component Schemas
- **Added schemas (B only)**: 8
- **Removed schemas (A only)**: 5
- **Changed schemas**: 95

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
#### `Amount1`
- `/maximum:` A='only_in_a' B=None

#### `ApDetail`
- `/properties/details/description:` A=None B='only_in_b'
- `/properties/details/items/description:` A='only_in_a' B=None

#### `ApList`
- `/properties/productList/description:` A=None B='only_in_b'
- `/properties/productList/items/description:` A='only_in_a' B=None

#### `Bic11`
- `/pattern:` A=None B='only_in_b'
- `/minLength:` A=11 B=8

#### `CmbLimitAmt`
- `/maximum:` A='only_in_a' B=None

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

#### `DateTime`
- `/description:` A=None B='only_in_b'
- `/pattern:` A=None B='only_in_b'

#### `DefaultDayValues`
- `/properties/defaultLACValues/description:` A=None B='only_in_b'
- `/properties/defaultLACValues/items/description:` A='only_in_a' B=None

#### `DefaultLACValues1`
- `/properties/base/description:` A='The base value amount set in the system for either the SenderBic or the MemberBic, the Day and LAC (Mandatory if this section is present)' B='The base value amount set in the system for the LSPBic, the Day and LAC (Mandatory if this section is present)'
- `/properties/lac/description:` A='The base value amount set in the system for either the SenderBic or the MemberBic, the Day and LAC (Mandatory if this section is present)' B='The LAC in the system (Mandatory if this section is present)'
- `/properties/lower/description:` A='The minimum value amount set in the system for either the SenderBic or the MemberBic, the Day and LAC (Mandatory if this section is present)' B='The minimum value amount set in the system for the LSPBic, the Day and LAC (Mandatory if this section is present)'
- `/properties/upper/description:` A='The maximum value amount set in the system for either the SenderBic or the MemberBic, the Day and LAC (Mandatory if this section is present)' B='The maximum value amount set in the system for the LSPBic, the Day and LAC (Mandatory if this section is present)'

#### `Details`
- `/properties/productList/description:` A=None B='only_in_b'
- `/properties/productList/items/description:` A='only_in_a' B=None

#### `ErrorResponse`
- `/properties/errorCode/$ref:` A='#/components/schemas/ErrorCode1' B='#/components/schemas/ErrorCode'
- `/properties/errorCodeDescription/$ref:` A='#/components/schemas/ErrorCodeDescription1' B='#/components/schemas/ErrorCodeDescription'

#### `IpData`
- `/properties/amountSentIP/description:` A='It is the sum of the following fields: AmountRjtIP AmountSettledIP.' B='It is the sum of the following fields: AmountRjtIP AmountHeldIP AmountSettledIP.'
- `/properties/amountSettledIP/description:` A='The sum of the values of the IP transactions included in the NumSettledIP' B='The sum of the values of the IP transactions included in the NumSettledIP field'
- `/properties/numRjtIP/description:` A='The number of IP that were received from the SenderBic and rejected by SCT Inst or BB' B='The number of IP received from the SenderBic that were rejected by SCT Inst or BB'
- `/properties/numSentIP/description:` A='It is the sum of the following fields: NumRjtIP, NumSettledIP.' B='It is the sum of the following fields: NumRjtIP, NumHeldIP , NumSettledIP.'
- `/properties/numSettledIP/description:` A='The number of IP that were received from the SenderBic and positively processed.' B='The number of IPs that were received from the SenderBic and positively processed.'

#### `IpData1`
- `/properties/amountSentIP/description:` A='It is the sum of the following fields: AmountRjtIP AmountHeldIP AmountSettledIP.' B='It is the sum of the following fields: AmountRjtIP AmountSettledIP.'
- `/properties/amountSettledIP/description:` A='The sum of the values of the IP transactions included in the NumSettledIP field' B='The sum of the values of the IP transactions included in the NumSettledIP'
- `/properties/numRjtIP/description:` A='The number of IP received from the SenderBic that were rejected by SCT Inst or BB' B='The number of IP that were received from the SenderBic and rejected by SCT Inst or BB'
- `/properties/numSentIP/description:` A='It is the sum of the following fields: NumRjtIP, NumHeldIP , NumSettledIP.' B='It is the sum of the following fields: NumRjtIP, NumSettledIP.'
- `/properties/numSettledIP/description:` A='The number of IPs that were received from the SenderBic and positively processed.' B='The number of IP that were received from the SenderBic and positively processed.'

#### `IpDataDRR`
- `/properties/ipData/$ref:` A='#/components/schemas/IpData1' B='#/components/schemas/IpData'

#### `LacAmount`
- `/maximum:` A='only_in_a' B=None

#### `ListDRRData`
- `/properties/recallData/$ref:` A='#/components/schemas/RecallData1' B='#/components/schemas/RecallData'

#### `ListMSRData`
- `/properties/ipData/$ref:` A='#/components/schemas/IpData' B='#/components/schemas/IpData1'
- `/properties/prrData/$ref:` A='#/components/schemas/PrrData' B='#/components/schemas/PrrData1'
- `/properties/recallData/$ref:` A='#/components/schemas/RecallData' B='#/components/schemas/RecallData1'

#### `LspBicDefaultDayValues`
- `/properties/defaultLACValues/description:` A=None B='only_in_b'
- `/properties/defaultLACValues/items/description:` A='only_in_a' B=None
- `/properties/defaultLACValues/items/$ref:` A='#/components/schemas/DefaultLACValues2' B='#/components/schemas/DefaultLACValues1'

#### `MaxFileSize2`
- `/maximum:` A='float' B='int'

#### `MessageDetails`
- `/properties/returnAcctTp/$ref:` A='#/components/schemas/ReturnAcctTp' B='#/components/schemas/ReturnAcctTp1'

#### `OperationDetails`
- `/properties/operationType/$ref:` A='#/components/schemas/OperationType1' B='#/components/schemas/OperationType2'

#### `ParametersHistory`
- `/properties/currenciesList/description:` A=None B='only_in_b'
- `/properties/currenciesList/items/description:` A='only_in_a' B=None
- `/properties/productList/description:` A=None B='only_in_b'
- `/properties/productList/items/description:` A='only_in_a' B=None

#### `ParticipantOperationDetails`
- `/properties/productList/description:` A=None B='only_in_b'
- `/properties/productList/items/description:` A='only_in_a' B=None

#### `ProductList4`
- `/properties/productId/$ref:` A='#/components/schemas/ProductId' B='#/components/schemas/ProductId2'

#### `ProductList5`
- `/properties/productId/$ref:` A='#/components/schemas/ProductId1' B='#/components/schemas/ProductId3'

#### `ProductList6`
- `/properties/productId/$ref:` A='#/components/schemas/ProductId1' B='#/components/schemas/ProductId3'

#### `PrrData`
- `/properties/amountRjtPRR/description:` A='The sum of the values of the returns transactions included in the NumRjtPRR' B='The sum of the values of the PRR transactions included in the NumRjtPRR'
- `/properties/amountSentPRR/description:` A='It is the sum of the following fields: AmountRjtPRR AmountSettledPRR.' B='It is the sum of the following fields: AmountRjtPRR AmountHeldPRR AmountSettledPRR'
- `/properties/amountSettledPRR/description:` A='The sum of the values of the returns transactions included in the NumSettledPRR field' B='The sum of the values of the PRR transactions included in the NumSettledPRR field'
- `/properties/numRjtPRR/description:` A='The number of PRR that were received from the SenderBic and rejected by SCT Inst' B='The number of PRR that were received from the SenderBic and rejected by SCT Inst.'
- `/properties/numSentPRR/description:` A='It is the sum of the following fields: NumRjtPRR, NumSettledPRR.' B='It is the sum of the following fields: NumRjtPRR, NumHeldPRR , NumSettledPRR.'

#### `PrrData1`
- `/properties/amountRjtPRR/description:` A='The sum of the values of the PRR transactions included in the NumRjtPRR' B='The sum of the values of the returns transactions included in the NumRjtPRR'
- `/properties/amountSentPRR/description:` A='It is the sum of the following fields: AmountRjtPRR AmountHeldPRR AmountSettledPRR' B='It is the sum of the following fields: AmountRjtPRR AmountSettledPRR.'
- `/properties/amountSettledPRR/description:` A='The sum of the values of the PRR transactions included in the NumSettledPRR field' B='The sum of the values of the returns transactions included in the NumSettledPRR field'
- `/properties/numRjtPRR/description:` A='The number of PRR that were received from the SenderBic and rejected by SCT Inst.' B='The number of PRR that were received from the SenderBic and rejected by SCT Inst'
- `/properties/numSentPRR/description:` A='It is the sum of the following fields: NumRjtPRR, NumHeldPRR , NumSettledPRR.' B='It is the sum of the following fields: NumRjtPRR, NumSettledPRR.'

#### `PrrDataDRR`
- `/properties/prrData/$ref:` A='#/components/schemas/PrrData1' B='#/components/schemas/PrrData'

#### `RecallData`
- `/properties/numSentRecall/description:` A='The number of Recall instructions received from the SenderBic by the system' B='The number of Recall instructions received from the SenderBic by the system. This counter includes also the rejected by SCT Inst.'

#### `RecallData1`
- `/properties/numSentRecall/description:` A='The number of Recall instructions received from the SenderBic by the system. This counter includes also the rejected by SCT Inst.' B='The number of Recall instructions received from the SenderBic by the system'

#### `Response`
- `/properties/bicExceptionDayValues/description:` A=None B='only_in_b'
- `/properties/bicExceptionDayValues/items/description:` A='only_in_a' B=None
- `/properties/memberExceptionDayValues/description:` A=None B='only_in_b'
- `/properties/memberExceptionDayValues/items/description:` A='only_in_a' B=None

#### `Response1`
- `/properties/instructions/description:` A=None B='only_in_b'
- `/properties/instructions/items/description:` A='only_in_a' B=None

#### `ResponseList`
- `/properties/productList/description:` A=None B='only_in_b'
- `/properties/productList/items/description:` A='only_in_a' B=None

#### `ThrottNumber`
- `/maximum:` A='float' B='int'

#### `Values`
- `/properties/lspBicDefaultDayValues/description:` A=None B='only_in_b'
- `/properties/lspBicDefaultDayValues/items/description:` A='only_in_a' B=None
- `/properties/memberDefaultDayValues/description:` A=None B='only_in_b'
- `/properties/memberDefaultDayValues/items/description:` A='only_in_a' B=None
- `/properties/memberDefaultDayValues/items/$ref:` A='#/components/schemas/MemberDefaultDayValues' B='#/components/schemas/MemberDefaultDayValues1'

#### `apDetailsResponse`
- `/properties/apDetail/description:` A=None B='only_in_b'
- `/properties/apDetail/items/description:` A='only_in_a' B=None

#### `beneficiaryManagementRequest`
- `/properties/criteria/$ref:` A='#/components/schemas/Criteria9' B='#/components/schemas/Criteria8'

#### `changeStatusAPRequest`
- `/properties/criteria/$ref:` A='#/components/schemas/Criteria14' B='#/components/schemas/Criteria13'

#### `communicationOfUnavailabilityRequest`
- `/properties/criteria/$ref:` A='#/components/schemas/Criteria16' B='#/components/schemas/Criteria15'

#### `currentNetPositionResponse`
- `/properties/lspsPosition/description:` A=None B='only_in_b'
- `/properties/lspsPosition/items/description:` A='only_in_a' B=None
- `/properties/ownedBranchFundsBalanceList/description:` A=None B='only_in_b'
- `/properties/ownedBranchFundsBalanceList/items/description:` A='only_in_a' B=None

#### `exceptionPositionCalendarRequest`
- `/properties/exceptionLacValues/description:` A=None B='only_in_b'
- `/properties/exceptionLacValues/items/description:` A='only_in_a' B=None

#### `fileDetailsRequest`
- `/properties/criteria/$ref:` A='#/components/schemas/Criteria26' B='#/components/schemas/Criteria25'

#### `fileDetailsResponse`
- `/properties/network/$ref:` A='#/components/schemas/Network1' B='#/components/schemas/Network2'

#### `getParticipantsRequest`
- `/properties/criteria/$ref:` A='#/components/schemas/Criteria10' B='#/components/schemas/Criteria9'

#### `getParticipantsResponse`
- `/properties/responseList/description:` A=None B='only_in_b'
- `/properties/responseList/items/description:` A='only_in_a' B=None

#### `inquiryUnavailabilityRequest`
- `/properties/criteria/$ref:` A='#/components/schemas/Criteria17' B='#/components/schemas/Criteria16'

#### `insertAPRequest`
- `/properties/criteria/$ref:` A='#/components/schemas/Criteria15' B='#/components/schemas/Criteria14'

#### `interestAmountsRequest`
- `/properties/criteria/$ref:` A='#/components/schemas/Criteria29' B='#/components/schemas/Criteria28'

#### `interestAmountsResponse`
- `/properties/interestList/description:` A=None B='only_in_b'
- `/properties/interestList/items/description:` A='only_in_a' B=None

#### `listAAURT1ASTARequest`
- `/properties/criteria/$ref:` A='#/components/schemas/Criteria20' B='#/components/schemas/Criteria19'

#### `listAPsRequest`
- `/properties/criteria/$ref:` A='#/components/schemas/Criteria12' B='#/components/schemas/Criteria11'

#### `listAlertsRequest`
- `/properties/criteria/$ref:` A='#/components/schemas/Criteria28' B='#/components/schemas/Criteria27'

#### `listAlertsResponse`
- `/properties/alertList/description:` A=None B='only_in_b'
- `/properties/alertList/items/description:` A='only_in_a' B=None

#### `listBeneficiaryRequest`
- `/properties/criteria/$ref:` A='#/components/schemas/Criteria8' B='#/components/schemas/Criteria7'
- `/properties/offset/description:` A='The offset points to a set of records' B='The offset points to a set of records **Validation Rule(s)** It must correspond to the value provided in the previous listBeneficiary - Positive Response'

#### `listBeneficiaryResponse`
- `/properties/listBeneficiary/description:` A=None B='only_in_b'
- `/properties/listBeneficiary/items/description:` A='only_in_a' B=None

#### `listCommandStatusRequest`
- `/properties/criteria/$ref:` A='#/components/schemas/Criteria27' B='#/components/schemas/Criteria26'

#### `listCurrenciesResponse`
- `/properties/listCurrencies/description:` A=None B='only_in_b'
- `/properties/listCurrencies/items/description:` A='only_in_a' B=None

#### `listFilesRequest`
- `/properties/criteria/$ref:` A='#/components/schemas/Criteria25' B='#/components/schemas/Criteria24'

#### `listFilesResponse`
- `/properties/listFiles/description:` A=None B='only_in_b'
- `/properties/listFiles/items/description:` A='only_in_a' B=None

#### `listLACsConfigurationResponse`
- `/properties/lacParameters/description:` A=None B='only_in_b'
- `/properties/lacParameters/items/description:` A='only_in_a' B=None

#### `listMessageResponse`
- `/properties/listMessages/description:` A=None B='only_in_b'
- `/properties/listMessages/items/description:` A='only_in_a' B=None

#### `listParticipantOperationRequest`
- `/properties/criteria/$ref:` A='#/components/schemas/Criteria18' B='#/components/schemas/Criteria17'

#### `listPaymentsRequest`
- `/properties/criteria/$ref:` A='#/components/schemas/Criteria21' B='#/components/schemas/Criteria20'

#### `listPaymentsResponse`
- `/properties/listPayment/description:` A=None B='only_in_b'
- `/properties/listPayment/items/description:` A='only_in_a' B=None

#### `listThrottlingParametersRequest`
- `/properties/dateTime/$ref:` A='#/components/schemas/DateTime' B='#/components/schemas/DateTime2'

#### `listThrottlingParametersResponse`
- `/properties/dateTime/$ref:` A='#/components/schemas/DateTime' B='#/components/schemas/DateTime2'

#### `listTransactionsRequest`
- `/properties/criteria/$ref:` A='#/components/schemas/Criteria23' B='#/components/schemas/Criteria22'

#### `listTransactionsResponse`
- `/properties/listTransactions/description:` A=None B='only_in_b'
- `/properties/listTransactions/items/description:` A='only_in_a' B=None

#### `manageAAURT1ASTARequest`
- `/properties/criteria/$ref:` A='#/components/schemas/Criteria19' B='#/components/schemas/Criteria18'

#### `participantDetailsResponse`
- `/properties/parametersHistory/description:` A=None B='only_in_b'
- `/properties/parametersHistory/items/description:` A='only_in_a' B=None

#### `paymentDetailsRequest`
- `/properties/criteria/$ref:` A='#/components/schemas/Criteria22' B='#/components/schemas/Criteria21'

#### `transactionDetailsRequest`
- `/properties/criteria/$ref:` A='#/components/schemas/Criteria24' B='#/components/schemas/Criteria23'

#### `updateAPRequest`
- `/properties/criteria/$ref:` A='#/components/schemas/Criteria13' B='#/components/schemas/Criteria12'

#### `updateParticipantRequest`
- `/properties/criteria/$ref:` A='#/components/schemas/Criteria11' B='#/components/schemas/Criteria10'
