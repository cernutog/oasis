# Full Parity Audit Report (Generated: 2026-02-04 16:01:41)

**Reference File:** `EBACL_STEP2_20250507_Openapi3.1_CGS-DKK_API_Participants_2_0_v20251006.yaml`
**Generated File:** `generated_oas_3.1.yaml`

## Executive Summary

- Total Reference Schemas: 172
- Total Generated Schemas: 291
- Missing Schemas in Gen (non-native): 10
- Extra Schemas in Gen: 130

## Schema Property Comparison

| Reference Schema | Generated Schema | Match Status | Details |
| :--- | :--- | :--- | :--- |
| AgendaDetails | AgendaDetails | ⚠️ Partial | Extra: ['SettlementBIC']; Types: ['`dailyThresholds`: DailyThresholds1 vs object'] |
| Alerts | Alerts | ❌ Mismatch | Missing: ['eventDescription', 'dateTime', 'eventType'] |
| Amount | Amount | ✅ Exact | Full property set match |
| Amount1 | Amount1 | ✅ Exact | Full property set match |
| BIC11 | BIC11 | ✅ Exact | Full property set match |
| BIC8 | BIC8 | ✅ Exact | Full property set match |
| Bic11Only | Bic11Only | ✅ Exact | Full property set match |
| Boolean1 | - | ❌ Missing | Not found in generated OAS |
| BulkReference | BulkReference | ✅ Exact | Full property set match |
| CGSSettlementBIC | CGSSettlementBIC | ⚠️ Partial | Extra: ['SettlBICName', 'LnrFileRequired', 'LmrFileRequired', 'PreferredS2Service', 'PreferredAgentBIC', 'EodFulDefund', 'ConfiguredS2Dp', 'AutomaticAdjustment', 'MaxRcvgFileSize']; Types: ['`automaticAdjustment`: Boolean1 vs boolean', '`lmrFileRequired`: Boolean1 vs boolean', '`lnrFileRequired`: Boolean1 vs boolean', '`configuredS2Dp`: array vs object', '`eodFulDefund`: Boolean1 vs boolean'] |
| CalendarDetails | CalendarDetails | ⚠️ Partial | Extra: ['SettlementBIC']; Types: ['`dailyThresholds`: DailyThresholds vs object'] |
| CommandReference | CommandReference | ✅ Exact | Full property set match |
| CommandStatus | CommandStatus | ✅ Exact | Full property set match |
| CommandType | CommandType | ✅ Exact | Full property set match |
| Commands | Commands | ❌ Mismatch | Missing: ['commandStatus', 'authRejectDateTime', 'userIssuer', 'commandRef', 'userAuthReject', 'commandType', 'requestDateTime'] |
| ConfiguredS2Dp | ConfiguredS2Dp | ❌ Mismatch | Missing: ['s2DpBIC', 's2Service'] |
| ConfiguredS2Dp1 | ConfiguredS2Dp1 | ❌ Mismatch | Missing: ['s2DpBIC', 's2Service'] |
| CurrentPosition | CurrentPosition | ⚠️ Partial | Extra: ['TimeStamp', 'SettlementBIC'] |
| DailyReport | DailyReport | ❌ Mismatch | Missing: ['eodPosition', 'snapshotTime', 'date', 'interestRate', 'dailyInterestAmount'] |
| DailyThresholds | DailyThresholds | ⚠️ Partial | Extra: ['Day']; Types: ['`lacAgenda`: array vs lacagenda'] |
| DailyThresholds1 | - | ❌ Missing | Not found in generated OAS |
| Date | Date | ✅ Exact | Full property set match |
| DateTime | DateTime | ✅ Exact | Full property set match |
| DateType | DateType | ✅ Exact | Full property set match |
| Day | Day | ✅ Exact | Full property set match |
| DefaultAgenda | DefaultAgenda | ⚠️ Partial | Extra: ['DefaultDailyThresholds']; Types: ['`defaultDailyThresholds`: array vs defaultdailythresholds'] |
| DefaultDailyThresholds | DefaultDailyThresholds | ❌ Mismatch | Missing: ['lacDefaultAgenda', 'day'] |
| DefaultDailyThresholds1 | - | ❌ Missing | Not found in generated OAS |
| DetailsHistory | DetailsHistory | ⚠️ Partial | Extra: ['LnrFileRequired', 'LmrFileRequired', 'Name', 'EodFulDefund', 'ConfiguredS2Dp', 'DlrFileRequired', 'AutomaticAdjustment', 'MaxRcvgFileSize']; Types: ['`configuredS2Dp`: array vs configureds2dp'] |
| DlrData | DlrData | ⚠️ Partial | Extra: ['DateTimeClosingBalance', 'DateTimeOpeningBalance', 'LiquidityInstrCreditPosition', 'LiquidityInstrDebitPosition', 'ProcessedLCRDebitPosition', 'ProcessedLCRCreditPosition']; Types: ['`processedLCRDebitPosition`: Amount1 vs amount', '`liquidityInstrDebitPosition`: Amount1 vs amount', '`positionOpening`: Amount1 vs amount', '`processedLCRCreditPosition`: Amount1 vs amount', '`liquidityInstrCreditPosition`: Amount1 vs amount', '`positionClosing`: Amount1 vs amount'] |
| EndOfList | EndOfList | ✅ Exact | Full property set match |
| ErrorCode | ErrorCode | ✅ Exact | Full property set match |
| ErrorCodeDescription | ErrorCodeDescription | ✅ Exact | Full property set match |
| ErrorResponse | errorResponse | ❌ Mismatch | Missing: ['errorCodeDescription', 'requestId', 'errorCode', 'dateTime']; Extra: ['ErrorCode', 'RequestId'] |
| EventDescription | EventDescription | ✅ Exact | Full property set match |
| EventType | EventType | ✅ Exact | Full property set match |
| ExceptionLacValues | ExceptionLacValues | ❌ Mismatch | Missing: ['lacNumber', 'lowerPosition', 'resetToBasePos', 'upperPosition', 'basePosition'] |
| ExceptionLacValues1 | - | ❌ Missing | Not found in generated OAS |
| FileDetails | FileDetails | ⚠️ Partial | Extra: ['LmrData', 'DlrData', 'BusinessDate', 'CreationDtTm', 'FileType', 'LastStatusUpdate', 'SendingInstitution', 'LacNumber', 'ReceivingInstitution', 'FileStatus', 'ModuleIdentifier', 'CalendarDate', 'FileReference', 'NetworkFileName']; Types: ['`lmrData`: LmrData vs object', '`dlrData`: DlrData vs object', '`lnrData`: LnrData vs object'] |
| FileList | FileList | ❌ Mismatch | Missing: ['lacNumber', 'fileStatus', 'network', 'preferredAgentBIC', 'dateTime', 'networkFileName', 'date', 'fileReference', 'fileType'] |
| FileReference | FileReference | ✅ Exact | Full property set match |
| FileStatus | FileStatus | ✅ Exact | Full property set match |
| FileType | FileType | ✅ Exact | Full property set match |
| FundingDefunding | FundingDefunding | ❌ Mismatch | Missing: ['amount', 'responseInstructionTp', 'creditSttlmBIC', 'debitBIC', 'instructionStatus', 'settlementBIC', 'debitSttlmBIC', 'instructionReference', 'creditBIC', 'date', 'settlementDateTime'] |
| FundingDefundingDetails | FundingDefundingDetails | ⚠️ Partial | Extra: ['SettlementBIC']; Types: ['`amount`: Amount1 vs amount'] |
| InstructionReference | InstructionReference | ✅ Exact | Full property set match |
| InstructionStatus | InstructionStatus | ✅ Exact | Full property set match |
| InstructionTypeRequest | instructionTypeRequest | ✅ Exact | Full property set match |
| InstructionTypeResponse | instructionTypeResponse | ✅ Exact | Full property set match |
| InterestReport | InterestReport | ❌ Mismatch | Missing: ['month', 'settlementBIC', 'monthlyInterestAmount'] |
| InterestReports | InterestReports | ⚠️ Partial | Types: ['`dailyReport`: array vs dailyreport'] |
| LacAgenda | LacAgenda | ❌ Mismatch | Missing: ['lacNumber', 'lowerPosition', 'resetToBasePos', 'upperPosition', 'basePosition'] |
| LacAgenda1 | - | ❌ Missing | Not found in generated OAS |
| LacDefaultAgenda | LacDefaultAgenda | ❌ Mismatch | Missing: ['lacNumber', 'lowerPosition', 'resetToBasePos', 'upperPosition', 'basePosition'] |
| LacDefaultAgenda1 | - | ❌ Missing | Not found in generated OAS |
| LacNumber | LacNumber | ✅ Exact | Full property set match |
| LacParameters | LacParameters | ❌ Mismatch | Missing: ['lacAdjustmentTime', 'nightTimeSettlement', 'lac', 'lacSendingCutOffTime'] |
| LcrDetails | LcrDetails | ⚠️ Partial | Extra: ['BulkType', 'InstdSttlmBIC', 'OriginalBulk', 'LcrReference', 'InstdAgt', 'CgsLacInput', 'Service', 'CgsLcrStatusUpdate', 'LcrStatus', 'Amount', 'DebPartyBIC']; Types: ['`numTransactions`: Number1 vs number', '`amount`: Amount1 vs amount'] |
| LcrStatus | LcrStatus | ✅ Exact | Full property set match |
| Lcrs | Lcrs | ❌ Mismatch | Missing: ['settlementDate', 'lacNumber', 'instdSttlmBIC', 'instdAgt', 'service', 'amount', 'dbrCrdFlag', 'originalInputFileReferenceId', 'lcrStatus', 'instgSttlmBIC', 'instgAgt', 'businessDateTime', 'lcrReference', 'originalBulkReferenceId'] |
| LmrData | LmrData | ⚠️ Partial | Extra: ['ProcessedLCRCreditPosition', 'LiquidityInstrCreditPosition', 'PositionLacClose', 'ProcessedLCRDebitPosition', 'NumTotBulks']; Types: ['`processedLCRDebitPosition`: Amount1 vs amount', '`liquidityInstrDebitPosition`: Amount1 vs amount', '`positionLacOpen`: Amount1 vs amount', '`positionLacClose`: Amount1 vs amount', '`processedLCRCreditPosition`: Amount1 vs amount', '`liquidityInstrCreditPosition`: Amount1 vs amount'] |
| LnrData | LnrData | ⚠️ Partial | Extra: ['PositionNotification', 'PositionDtTm']; Types: ['`positionNotification`: Amount1 vs amount'] |
| MessageType | MessageType | ✅ Exact | Full property set match |
| ModuleIdentifier | ModuleIdentifier | ✅ Exact | Full property set match |
| Network | Network | ✅ Exact | Full property set match |
| NetworkFileName | NetworkFileName | ✅ Exact | Full property set match |
| Number1 | - | ❌ Missing | Not found in generated OAS |
| Offset | Offset | ✅ Exact | Full property set match |
| OperationDetails | OperationDetails | ⚠️ Partial | Extra: ['Critical', 'UserIssuer', 'AuthRejectDateTime', 'EffectiveDate', 'OperationStatus', 'OperationType', 'UserAuthReject', 'CommandRef', 'RequestDateTime', 'SettlementBIC']; Types: ['`commandRef`: OperationReference1 vs operationreference', '`CGSSettlementBIC`: CGSSettlementBIC vs object', '`operationType`: OperationType1 vs operationtype', '`critical`: Boolean1 vs boolean'] |
| OperationReference | OperationReference | ✅ Exact | Full property set match |
| OperationReference1 | OperationReference1 | ✅ Exact | Full property set match |
| OperationStatus | OperationStatus | ✅ Exact | Full property set match |
| OperationType | OperationType | ✅ Exact | Full property set match |
| OperationType1 | OperationType1 | ✅ Exact | Full property set match |
| Operations | Operations | ❌ Mismatch | Missing: ['userIssuer', 'commandRef', 'userAuthReject', 'settlementBIC', 'authRejectExecDateTime', 'operationType', 'critical', 'requestDateTime', 'effectiveDate', 'operationStatus'] |
| OtherModuleCutOff | OtherModuleCutOff | ⚠️ Partial | Extra: ['Taw3Start', 'CorEOD', 'Taw2End', 'Taw1End', 'B2bEOD', 'Taw4End', 'CgsEOD', 'Taw2Start', 'Taw3End', 'Taw1Start', 'Taw4Start', 'OpeningTime', 'SctEOD'] |
| ParModhistory | ParModhistory | ❌ Mismatch | Missing: ['detailsHistory', 'initParameterValidity', 'endParameterValidity'] |
| ParticipantName | ParticipantName | ✅ Exact | Full property set match |
| ParticipantStatus | ParticipantStatus | ✅ Exact | Full property set match |
| PositionHistory | PositionHistory | ❌ Mismatch | Missing: ['timeStamp', 'lacNumber', 'amount', 'businessDate', 'settlementBIC'] |
| RequestId | RequestId | ✅ Exact | Full property set match |
| ResendAllDetails | ResendAllDetails | ⚠️ Partial | Extra: ['FileStatus', 'FileType', 'TimestampLastUpdate'] |
| RetransmitOutFileDetails | RetransmitOutFileDetails | ⚠️ Partial | Extra: ['BusinessDate', 'FileType', 'FileStatus', 'PreferredAgentBIC', 'Lac', 'FileReference', 'SettlementBIC'] |
| RevokeAllLcrDetails | RevokeAllLcrDetails | ⚠️ Partial | Extra: ['SettlementBIC'] |
| RevokeLcrDetails | RevokeLcrDetails | ⚠️ Partial | Extra: ['LcrReference', 'InstgAgt', 'S2Service', 'InstgSttlmBIC'] |
| SearchCriteria | SearchCriteria | ⚠️ Partial | Extra: ['InstructionStatus', 'InstdSttlmBIC', 'AuthRejectDateTimeTo', 'BusinessDate', 'MonthFrom', 'PreferredAgentBIC', 'LacNumber', 'DebitSttlmBIC', 'InstdAgt', 'RequestDateTimeFrom', 'RequestDate', 'FileReference', 'UserAuthReject', 'SettlementDateTo', 'DefaultValues', 'SettlementBIC', 'DateTimeFrom', 'CommandType', 'BusinessDateFrom', 'Status', 'FileType', 'CommandStatus', 'PreferredS2Service', 'UserIssuer', 'CreditSttlmBIC', 'CommandRef', 'AmountFrom', 'SettlementDate', 'NetworkFileName', 'EndValidityDate', 'BusinessDateTo', 'InstructionReference', 'InstructionTp', 'Service', 'LcrStatus', 'OperationType', 'AuthRejectExecDateTime', 'DateTimeTo', 'MonthTo', 'AmountTo', 'SettlementDateFrom', 'Critical', 'FileStatus', 'EventDescription', 'InstgSttlmBIC', 'LcrReference', 'EffectiveDate', 'RequestDateTimeTo', 'OperationStatus', 'DateType', 'Month', 'AuthRejectDateTimeFrom', 'InitialValidityDate', 'InstgAgt'] |
| SearchCriteria1 | SearchCriteria1 | ⚠️ Partial | Types: ['`amountTo`: Amount1 vs amount', '`amountFrom`: Amount1 vs amount'] |
| SearchCriteria10 | SearchCriteria10 | ✅ Exact | Full property set match |
| SearchCriteria11 | SearchCriteria11 | ⚠️ Partial | Types: ['`critical`: Boolean1 vs boolean'] |
| SearchCriteria12 | SearchCriteria12 | ✅ Exact | Full property set match |
| SearchCriteria2 | SearchCriteria2 | ✅ Exact | Full property set match |
| SearchCriteria3 | SearchCriteria3 | ✅ Exact | Full property set match |
| SearchCriteria4 | SearchCriteria4 | ✅ Exact | Full property set match |
| SearchCriteria5 | SearchCriteria5 | ✅ Exact | Full property set match |
| SearchCriteria6 | SearchCriteria6 | ✅ Exact | Full property set match |
| SearchCriteria7 | SearchCriteria7 | ✅ Exact | Full property set match |
| SearchCriteria8 | SearchCriteria8 | ✅ Exact | Full property set match |
| SearchCriteria9 | SearchCriteria9 | ✅ Exact | Full property set match |
| SenderBIC | SenderBIC | ✅ Exact | Full property set match |
| SenderBIC1 | - | ❌ Missing | Not found in generated OAS |
| Service | Service | ✅ Exact | Full property set match |
| SettlementBIC | SettlementBIC | ⚠️ Partial | Extra: ['InitialSettBICValidityDate'] |
| SettlementBICAmend | SettlementBICAmend | ⚠️ Partial | Extra: ['LmrFileRequired', 'DlrFileRequired', 'AutomaticAdjustment', 'MaxRcvgFileSize'] |
| SettlementBICDetails | SettlementBICDetails | ⚠️ Partial | Extra: ['Status', 'EndValidityDate', 'PreferredS2Service', 'PreferredAgentBIC', 'ParModhistory', 'InitialValidityDate', 'SettlementBIC']; Types: ['`parModhistory`: array vs parmodhistory'] |
| SettlementBICParameters | SettlementBICParameters | ⚠️ Partial | Extra: ['SettlBICName', 'LnrFileRequired', 'LmrFileRequired', 'EodFulDefund', 'DlrFileRequired', 'AutomaticAdjustment', 'MaxRcvgFileSize'] |
| SettlementBICs | SettlementBICs | ❌ Mismatch | Missing: ['preferredS2Service', 'status', 'name', 'initialValidityDate', 'settlementBIC', 'preferredAgentBIC', 'endValidityDate'] |
| Sign | Sign | ✅ Exact | Full property set match |
| StandardInteger | StandardInteger | ✅ Exact | Full property set match |
| Time | Time | ✅ Exact | Full property set match |
| TransferType | TransferType | ✅ Exact | Full property set match |
| User | User | ✅ Exact | Full property set match |
| YearMonth | YearMonth | ✅ Exact | Full property set match |
| amendChangeSettlementBICRequest | amendChangeSettlementBICRequest | ❌ Mismatch | Missing: ['dateTime', 'settlementBICAmend', 'settlementBIC']; Extra: ['SettlementBICAmend', 'SettlementBIC'] |
| amendChangeSettlementBICResponse | amendChangeSettlementBICResponse | ❌ Mismatch | Missing: ['dateTime', 'commandRef']; Extra: ['CommandRef'] |
| commandDetailsRequest | commandDetailsRequest | ❌ Mismatch | Missing: ['dateTime', 'commandRef']; Extra: ['DateTime'] |
| commandDetailsResponse | commandDetailsResponse | ❌ Mismatch | Missing: ['revokeAllLcrDetails', 'authRejectDateTime', 'userIssuer', 'fundingDefundingDetails', 'commandRef', 'userAuthReject', 'resendAllDetails', 'commandType', 'retransmitOutFileDetails', 'calendarDetails', 'revokeLcrDetails', 'commandStatus', 'agendaDetails', 'dateTime', 'requestDateTime']; Extra: ['UserIssuer', 'RevokeAllLcrDetails', 'FundingDefundingDetails'] |
| currentPositionRequest | currentPositionRequest | ❌ Mismatch | Missing: ['dateTime', 'settlementBIC'] |
| currentPositionResponse | currentPositionResponse | ❌ Mismatch | Missing: ['dateTime', 'currentPosition'] |
| fileDetailsRequest | fileDetailsRequest | ❌ Mismatch | Missing: ['searchCriteria', 'dateTime']; Extra: ['SearchCriteria'] |
| fileDetailsResponse | fileDetailsResponse | ❌ Mismatch | Missing: ['fileDetails', 'dateTime']; Extra: ['FileDetails'] |
| getDefaultAgendaRequest | getDefaultAgendaRequest | ❌ Mismatch | Missing: ['dateTime', 'settlementBIC']; Extra: ['DateTime'] |
| getDefaultAgendaResponse | getDefaultAgendaResponse | ❌ Mismatch | Missing: ['defaultAgenda', 'dateTime', 'settlementBIC']; Extra: ['SettlementBIC'] |
| interestDailyReportRequest | interestDailyReportRequest | ❌ Mismatch | Missing: ['searchCriteria', 'dateTime']; Extra: ['DateTime'] |
| interestDailyReportResponse | interestDailyReportResponse | ❌ Mismatch | Missing: ['dateTime', 'interestReports', 'settlementBIC'] |
| interestMonthlyReportRequest | interestMonthlyReportRequest | ❌ Mismatch | Missing: ['searchCriteria', 'dateTime'] |
| interestMonthlyReportResponse | interestMonthlyReportResponse | ❌ Mismatch | Missing: ['interestReport', 'dateTime'] |
| lcrDetailsRequest | lcrDetailsRequest | ❌ Mismatch | Missing: ['searchCriteria', 'dateTime'] |
| lcrDetailsResponse | lcrDetailsResponse | ❌ Mismatch | Missing: ['lcrDetails', 'dateTime']; Extra: ['LcrDetails'] |
| lcrListRequest | lcrListRequest | ❌ Mismatch | Missing: ['offset', 'searchCriteria', 'dateTime']; Extra: ['SearchCriteria', 'Offset'] |
| lcrListResponse | lcrListResponse | ❌ Mismatch | Missing: ['offset', 'endOfList', 'dateTime', 'lcrs']; Extra: ['DateTime', 'EndOfList', 'Lcrs', 'Offset'] |
| liquidityManagementRequest | - | ❌ Missing | Not found in generated OAS |
| liquidityManagementResponse | - | ❌ Missing | Not found in generated OAS |
| listAlertsRequest | listAlertsRequest | ❌ Mismatch | Missing: ['offset', 'searchCriteria', 'dateTime']; Extra: ['DateTime', 'SearchCriteria', 'Offset'] |
| listAlertsResponse | listAlertsResponse | ❌ Mismatch | Missing: ['offset', 'endOfList', 'dateTime', 'alerts']; Extra: ['DateTime', 'EndOfList', 'Alerts', 'Offset'] |
| listCalendarRequest | listCalendarRequest | ❌ Mismatch | Missing: ['businessDate', 'dateTime', 'settlementBIC']; Extra: ['DateTime', 'BusinessDate', 'SettlementBIC'] |
| listCalendarResponse | listCalendarResponse | ❌ Mismatch | Missing: ['businessDate', 'dateTime', 'exceptionLacValues']; Extra: ['DateTime', 'ExceptionLacValues', 'BusinessDate'] |
| listCommandsRequest | listCommandsRequest | ❌ Mismatch | Missing: ['offset', 'searchCriteria', 'dateTime']; Extra: ['DateTime', 'SearchCriteria', 'Offset'] |
| listCommandsResponse | listCommandsResponse | ❌ Mismatch | Missing: ['offset', 'commands', 'dateTime', 'endOfList']; Extra: ['DateTime', 'EndOfList', 'Commands', 'Offset'] |
| listFilesRequest | listFilesRequest | ❌ Mismatch | Missing: ['offset', 'searchCriteria', 'dateTime']; Extra: ['DateTime', 'SearchCriteria', 'Offset'] |
| listFilesResponse | listFilesResponse | ❌ Mismatch | Missing: ['offset', 'endOfList', 'fileList', 'dateTime']; Extra: ['DateTime', 'EndOfList', 'FileList', 'Offset'] |
| listFundingDefundingRequest | listFundingDefundingRequest | ❌ Mismatch | Missing: ['offset', 'searchCriteria', 'dateTime']; Extra: ['DateTime', 'SearchCriteria', 'Offset'] |
| listFundingDefundingResponse | listFundingDefundingResponse | ❌ Mismatch | Missing: ['offset', 'endOfList', 'dateTime', 'fundingDefunding']; Extra: ['DateTime', 'EndOfList', 'FundingDefunding', 'Offset'] |
| listLACsConfigurationRequest | listLACsConfigurationRequest | ❌ Mismatch | Missing: ['searchCriteria', 'dateTime']; Extra: ['DateTime', 'SearchCriteria'] |
| listLACsConfigurationResponse | listLACsConfigurationResponse | ❌ Mismatch | Missing: ['lacParameters', 'otherModuleCutOff', 'dateTime']; Extra: ['DateTime', 'LacParameters', 'OtherModuleCutOff'] |
| listOperationRequest | listOperationRequest | ❌ Mismatch | Missing: ['offset', 'searchCriteria', 'dateTime']; Extra: ['DateTime', 'SearchCriteria', 'Offset'] |
| listOperationResponse | listOperationResponse | ❌ Mismatch | Missing: ['offset', 'endOfList', 'dateTime', 'operations']; Extra: ['DateTime', 'EndOfList', 'Operations', 'Offset'] |
| listSettlementBICsRequest | listSettlementBICsRequest | ❌ Mismatch | Missing: ['searchCriteria', 'dateTime']; Extra: ['DateTime', 'SearchCriteria'] |
| listSettlementBICsResponse | listSettlementBICsResponse | ❌ Mismatch | Missing: ['settlementBICs', 'dateTime']; Extra: ['DateTime', 'SettlementBICs'] |
| operationDetailsRequest | operationDetailsRequest | ❌ Mismatch | Missing: ['dateTime', 'commandRef']; Extra: ['DateTime', 'CommandRef'] |
| operationDetailsResponse | operationDetailsResponse | ❌ Mismatch | Missing: ['dateTime', 'operationDetails']; Extra: ['DateTime', 'OperationDetails'] |
| positionLacRequest | positionLacRequest | ❌ Mismatch | Missing: ['lacNumber', 'businessDateFrom', 'settlementBIC', 'businessDateTo', 'dateTime']; Extra: ['BusinessDateFrom', 'DateTime', 'LacNumber', 'SettlementBIC', 'BusinessDateTo'] |
| positionLacResponse | positionLacResponse | ❌ Mismatch | Missing: ['dateTime', 'positionHistory']; Extra: ['DateTime', 'PositionHistory'] |
| rejectParticipantOperationRequest | rejectParticipantOperationRequest | ❌ Mismatch | Missing: ['dateTime', 'commandRef']; Extra: ['DateTime', 'CommandRef'] |
| rejectParticipantOperationResponse | rejectParticipantOperationResponse | ❌ Mismatch | Missing: ['dateTime', 'commandRef']; Extra: ['DateTime', 'CommandRef'] |
| resendAllRequest | resendAllRequest | ❌ Mismatch | Missing: ['dateFrom', 'lacNumber', 'fileStatus', 'dateTo', 'dateTime', 'fileType']; Extra: ['DateFrom', 'FileType', 'DateTo', 'DateTime', 'FileStatus', 'LacNumber'] |
| resendAllResponse | resendAllResponse | ❌ Mismatch | Missing: ['commandStatus', 'dateTime', 'commandRef']; Extra: ['DateTime', 'CommandRef', 'CommandStatus'] |
| retransmitOutFilesRequest | retransmitOutFilesRequest | ❌ Mismatch | Missing: ['networkFileName', 'dateTime']; Extra: ['DateTime', 'NetworkFileName'] |
| retransmitOutFilesResponse | retransmitOutFilesResponse | ❌ Mismatch | Missing: ['commandStatus', 'dateTime', 'commandRef']; Extra: ['DateTime', 'CommandRef', 'CommandStatus'] |
| revokeChangeSettlementBICRequest | revokeChangeSettlementBICRequest | ❌ Mismatch | Missing: ['initParticipantValidity', 'dateTime', 'endParticipantValidity', 'settlementBIC']; Extra: ['DateTime', 'InitParticipantValidity', 'SettlementBIC', 'EndParticipantValidity'] |
| revokeChangeSettlementBICResponse | revokeChangeSettlementBICResponse | ❌ Mismatch | Missing: ['dateTime', 'commandRef']; Extra: ['DateTime', 'CommandRef'] |
| revokeLcrRequest | revokeLcrRequest | ❌ Mismatch | Missing: ['searchCriteria', 'dateTime']; Extra: ['DateTime', 'SearchCriteria'] |
| revokeLcrResponse | revokeLcrResponse | ❌ Mismatch | Missing: ['commandStatus', 'dateTime', 'commandRef']; Extra: ['DateTime', 'CommandRef', 'CommandStatus'] |
| setCalendarRequest | setCalendarRequest | ❌ Mismatch | Missing: ['businessDate', 'dateTime', 'exceptionLacValues', 'settlementBIC']; Extra: ['DateTime', 'ExceptionLacValues', 'BusinessDate', 'SettlementBIC'] |
| setCalendarResponse | setCalendarResponse | ❌ Mismatch | Missing: ['effectiveDate', 'dateTime']; Extra: ['DateTime', 'EffectiveDate'] |
| setDefaultAgendaRequest | setDefaultAgendaRequest | ❌ Mismatch | Missing: ['defaultDailyThresholds', 'dateTime', 'settlementBIC']; Extra: ['DateTime', 'DefaultDailyThresholds', 'SettlementBIC'] |
| setDefaultAgendaResponse | setDefaultAgendaResponse | ❌ Mismatch | Missing: ['effectiveDate', 'dateTime']; Extra: ['DateTime', 'EffectiveDate'] |
| settlementBICDetailsRequest | settlementBICDetailsRequest | ❌ Mismatch | Missing: ['dateTime', 'settlementBIC']; Extra: ['DateTime', 'SettlementBIC'] |
| settlementBICDetailsResponse | settlementBICDetailsResponse | ❌ Mismatch | Missing: ['dateTime', 'settlementBICDetails']; Extra: ['DateTime', 'SettlementBICDetails'] |
| updateSettlementBICRequest | updateSettlementBICRequest | ❌ Mismatch | Missing: ['settlementBICCode', 'effectiveDate', 'settlementBICParameters', 'dateTime']; Extra: ['DateTime', 'SettlementBICCode', 'EffectiveDate', 'SettlementBICParameters'] |
| updateSettlementBICResponse | updateSettlementBICResponse | ❌ Mismatch | Missing: ['dateTime', 'commandRef']; Extra: ['DateTime', 'CommandRef'] |

## Extra Schemas in Generated OAS

The following schemas are in the generated OAS but NOT in the reference. These might be redundant variants or incorrectly hoisted properties.

- AmountFrom
- AmountTo
- AuthRejectDateTime
- AuthRejectDateTimeFrom
- AuthRejectDateTimeTo
- AuthRejectExecDateTime
- AutomaticAdjustment
- AvailableLiquidity
- B2bEOD
- BasePosition
- BulkType
- BusinessDate
- BusinessDateFrom
- BusinessDateTime
- BusinessDateTo
- CalendarDate
- CgsEOD
- CgsLacInput
- CgsLacOutput
- CgsLcrStatusUpdate
- CommandRef
- CorEOD
- CreationDtTm
- CredPartyBIC
- CreditBIC
- CreditSttlmBIC
- Critical
- DailyInterestAmount
- DateFrom
- DateTimeClosingBalance
- DateTimeFrom
- DateTimeOpeningBalance
- DateTimeTo
- DateTo
- DbrCrdFlag
- DebPartyBIC
- DebitBIC
- DebitSttlmBIC
- DefaultValues
- DlrFileRequired
- EffectiveDate
- EndParameterValidity
- EndParticipantValidity
- EndSettBICValidityDate
- EndValidityDate
- EodFulDefund
- EodPosition
- InitParameterValidity
- InitParticipantValidity
- InitialSettBICValidityDate
- InitialValidityDate
- InstdAgt
- InstdSttlmBIC
- InstgAgt
- InstgSttlmBIC
- InstructionTp
- InterestRate
- Lac
- LacAdjustmentTime
- LacInputFromS2
- LacSendingCutOffTime
- LastStatusUpdate
- LcrReference
- LiquidityInstrCreditPosition
- LiquidityInstrDebitPosition
- LmrFileRequired
- LnrFileRequired
- LowerPosition
- MaxRcvgFileSize
- Month
- MonthFrom
- MonthTo
- MonthlyInterestAmount
- NightTimeSettlement
- NumTotBulks
- NumTransactions
- OpeningTime
- OperationStatus1
- OriginalBulk
- OriginalBulkReferenceId
- OriginalFileRef
- OriginalInputFileReferenceId
- PositionClosing
- PositionDtTm
- PositionLacClose
- PositionLacOpen
- PositionNotification
- PositionOpening
- PreferredAgentBIC
- PreferredS2Service
- ProcessedLCRCreditPosition
- ProcessedLCRDebitPosition
- ReceivingInstitution
- RequestDate
- RequestDateTime
- RequestDateTimeFrom
- RequestDateTimeTo
- ResetToBasePos
- ResponseInstructionTp
- S2DpBIC
- S2LcrCreationTimestamp
- S2Service
- SctEOD
- SendingInstitution
- SettlBICName
- SettlementBICCode
- SettlementDate
- SettlementDateFrom
- SettlementDateTime
- SettlementDateTo
- SnapshotTime
- Status
- Taw1End
- Taw1Start
- Taw2End
- Taw2Start
- Taw3End
- Taw3Start
- Taw4End
- Taw4Start
- TimeStamp
- TimestampLastUpdate
- TransferTp
- UpperPosition
- UserAuthReject
- UserIssuer
- errorResponse1
- liquidityManagement1Request
- liquidityManagement1Response
- parameters


**Final Statistics:** 58 Exact Matches, 112 Discrepancies (including missing ref schemas).
