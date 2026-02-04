# Full Parity Audit Report (Generated: 2026-02-04 12:09:02)

**Reference File:** `EBACL_STEP2_20250507_Openapi3.1_CGS-DKK_API_Participants_2_0_v20251006.yaml`
**Generated File:** `generated_oas_3.1.yaml`

## Executive Summary

- Total Reference Schemas: 172
- Total Generated Schemas: 291
- Missing Schemas in Gen (non-native): 10

## Schema Property Comparison

| Reference Schema | Generated Schema | Match Status | Details |
| :--- | :--- | :--- | :--- |
| AgendaDetails | AgendaDetails | ⚠️ Partial | Extra: ['SettlementBIC']; Types: ['`dailyThresholds`: #/components/schemas/DailyThresholds1 vs object', '`settlementBIC`: #/components/schemas/Bic11Only vs bic11only'] |
| Alerts | Alerts | ❌ Mismatch | Missing: ['eventType', 'dateTime', 'eventDescription'] |
| Amount | Amount | ✅ Exact | Full property set match |
| Amount1 | Amount1 | ✅ Exact | Full property set match |
| BIC11 | BIC11 | ✅ Exact | Full property set match |
| BIC8 | BIC8 | ✅ Exact | Full property set match |
| Bic11Only | Bic11Only | ✅ Exact | Full property set match |
| Boolean1 | - | ❌ Missing | Not found in generated OAS |
| BulkReference | BulkReference | ✅ Exact | Full property set match |
| CGSSettlementBIC | CGSSettlementBIC | ⚠️ Partial | Extra: ['ConfiguredS2Dp', 'SettlBICName', 'PreferredAgentBIC', 'AutomaticAdjustment', 'EodFulDefund', 'LmrFileRequired', 'MaxRcvgFileSize', 'PreferredS2Service', 'LnrFileRequired']; Types: ['`preferredS2Service`: #/components/schemas/Service vs service', '`preferredAgentBIC`: #/components/schemas/BIC8 vs bic8', '`eodFulDefund`: #/components/schemas/Boolean1 vs boolean', '`automaticAdjustment`: #/components/schemas/Boolean1 vs boolean', '`maxRcvgFileSize`: #/components/schemas/StandardInteger vs standardinteger', '`configuredS2Dp`: array vs object', '`settlBICName`: #/components/schemas/ParticipantName vs participantname', '`lmrFileRequired`: #/components/schemas/Boolean1 vs boolean', '`lnrFileRequired`: #/components/schemas/Boolean1 vs boolean'] |
| CalendarDetails | CalendarDetails | ⚠️ Partial | Extra: ['SettlementBIC']; Types: ['`dailyThresholds`: #/components/schemas/DailyThresholds vs object', '`settlementBIC`: #/components/schemas/Bic11Only vs bic11only'] |
| CommandReference | CommandReference | ✅ Exact | Full property set match |
| CommandStatus | CommandStatus | ✅ Exact | Full property set match |
| CommandType | CommandType | ✅ Exact | Full property set match |
| Commands | Commands | ❌ Mismatch | Missing: ['requestDateTime', 'commandRef', 'authRejectDateTime', 'commandType', 'commandStatus', 'userIssuer', 'userAuthReject'] |
| ConfiguredS2Dp | ConfiguredS2Dp | ❌ Mismatch | Missing: ['s2Service', 's2DpBIC'] |
| ConfiguredS2Dp1 | ConfiguredS2Dp1 | ❌ Mismatch | Missing: ['s2Service', 's2DpBIC'] |
| CurrentPosition | CurrentPosition | ⚠️ Partial | Extra: ['SettlementBIC', 'TimeStamp']; Types: ['`timeStamp`: #/components/schemas/DateTime vs datetime', '`settlementBIC`: #/components/schemas/Bic11Only vs bic11only', '`amount`: #/components/schemas/Amount vs amount'] |
| DailyReport | DailyReport | ❌ Mismatch | Missing: ['snapshotTime', 'dailyInterestAmount', 'eodPosition', 'date', 'interestRate'] |
| DailyThresholds | DailyThresholds | ⚠️ Partial | Extra: ['Day']; Types: ['`day`: #/components/schemas/Day vs day', '`lacAgenda`: array vs lacagenda'] |
| DailyThresholds1 | - | ❌ Missing | Not found in generated OAS |
| Date | Date | ✅ Exact | Full property set match |
| DateTime | DateTime | ✅ Exact | Full property set match |
| DateType | DateType | ✅ Exact | Full property set match |
| Day | Day | ✅ Exact | Full property set match |
| DefaultAgenda | DefaultAgenda | ⚠️ Partial | Extra: ['DefaultDailyThresholds']; Types: ['`defaultDailyThresholds`: array vs defaultdailythresholds'] |
| DefaultDailyThresholds | DefaultDailyThresholds | ❌ Mismatch | Missing: ['day', 'lacDefaultAgenda'] |
| DefaultDailyThresholds1 | - | ❌ Missing | Not found in generated OAS |
| DetailsHistory | DetailsHistory | ⚠️ Partial | Extra: ['Name', 'ConfiguredS2Dp', 'AutomaticAdjustment', 'LmrFileRequired', 'EodFulDefund', 'MaxRcvgFileSize', 'DlrFileRequired', 'LnrFileRequired']; Types: ['`eodFulDefund`: #/components/schemas/Boolean vs boolean', '`automaticAdjustment`: #/components/schemas/Boolean vs boolean', '`maxRcvgFileSize`: #/components/schemas/Number vs number', '`configuredS2Dp`: array vs configureds2dp', '`dlrFileRequired`: #/components/schemas/Boolean vs boolean', '`name`: #/components/schemas/ParticipantName vs participantname', '`lmrFileRequired`: #/components/schemas/Boolean vs boolean', '`lnrFileRequired`: #/components/schemas/Boolean vs boolean'] |
| DlrData | DlrData | ⚠️ Partial | Extra: ['LiquidityInstrCreditPosition', 'DateTimeClosingBalance', 'ProcessedLCRCreditPosition', 'ProcessedLCRDebitPosition', 'DateTimeOpeningBalance', 'LiquidityInstrDebitPosition']; Types: ['`numTotBulks`: #/components/schemas/Number vs number', '`liquidityInstrDebitPosition`: #/components/schemas/Amount1 vs amount', '`dateTimeOpeningBalance`: #/components/schemas/DateTime vs datetime', '`processedLCRCreditPosition`: #/components/schemas/Amount1 vs amount', '`dateTimeClosingBalance`: #/components/schemas/DateTime vs datetime', '`liquidityInstrCreditPosition`: #/components/schemas/Amount1 vs amount', '`positionOpening`: #/components/schemas/Amount1 vs amount', '`processedLCRDebitPosition`: #/components/schemas/Amount1 vs amount', '`positionClosing`: #/components/schemas/Amount1 vs amount'] |
| EndOfList | EndOfList | ✅ Exact | Full property set match |
| ErrorCode | ErrorCode | ✅ Exact | Full property set match |
| ErrorCodeDescription | ErrorCodeDescription | ✅ Exact | Full property set match |
| ErrorResponse | errorResponse | ❌ Mismatch | Missing: ['requestId', 'errorCodeDescription', 'errorCode', 'dateTime']; Extra: ['RequestId', 'ErrorCode'] |
| EventDescription | EventDescription | ✅ Exact | Full property set match |
| EventType | EventType | ✅ Exact | Full property set match |
| ExceptionLacValues | ExceptionLacValues | ❌ Mismatch | Missing: ['resetToBasePos', 'lacNumber', 'basePosition', 'upperPosition', 'lowerPosition'] |
| ExceptionLacValues1 | - | ❌ Missing | Not found in generated OAS |
| FileDetails | FileDetails | ⚠️ Partial | Extra: ['BusinessDate', 'LastStatusUpdate', 'NetworkFileName', 'FileType', 'CreationDtTm', 'FileReference', 'CalendarDate', 'ModuleIdentifier', 'ReceivingInstitution', 'FileStatus', 'SendingInstitution', 'LmrData', 'LacNumber', 'DlrData']; Types: ['`lmrData`: #/components/schemas/LmrData vs object', '`dlrData`: #/components/schemas/DlrData vs object', '`creationDtTm`: #/components/schemas/DateTime vs datetime', '`businessDate`: #/components/schemas/Date vs date', '`lastStatusUpdate`: #/components/schemas/DateTime vs datetime', '`fileType`: #/components/schemas/FileType vs filetype', '`lacNumber`: #/components/schemas/LacNumber vs lacnumber', '`sendingInstitution`: #/components/schemas/BIC8 vs bic8', '`networkFileName`: #/components/schemas/NetworkFileName vs networkfilename', '`fileStatus`: #/components/schemas/FileStatus vs filestatus', '`lnrData`: #/components/schemas/LnrData vs object', '`calendarDate`: #/components/schemas/Date vs date', '`fileReference`: #/components/schemas/FileReference vs filereference', '`receivingInstitution`: #/components/schemas/BIC8 vs bic8', '`moduleIdentifier`: #/components/schemas/ModuleIdentifier vs moduleidentifier'] |
| FileList | FileList | ❌ Mismatch | Missing: ['preferredAgentBIC', 'lacNumber', 'fileType', 'fileReference', 'fileStatus', 'networkFileName', 'date', 'network', 'dateTime'] |
| FileReference | FileReference | ✅ Exact | Full property set match |
| FileStatus | FileStatus | ✅ Exact | Full property set match |
| FileType | FileType | ✅ Exact | Full property set match |
| FundingDefunding | FundingDefunding | ❌ Mismatch | Missing: ['settlementDateTime', 'instructionReference', 'amount', 'creditBIC', 'debitSttlmBIC', 'creditSttlmBIC', 'debitBIC', 'settlementBIC', 'responseInstructionTp', 'instructionStatus', 'date'] |
| FundingDefundingDetails | FundingDefundingDetails | ⚠️ Partial | Extra: ['SettlementBIC']; Types: ['`settlementBIC`: #/components/schemas/Bic11Only vs bic11only', '`amount`: #/components/schemas/Amount1 vs amount'] |
| InstructionReference | InstructionReference | ✅ Exact | Full property set match |
| InstructionStatus | InstructionStatus | ✅ Exact | Full property set match |
| InstructionTypeRequest | instructionTypeRequest | ✅ Exact | Full property set match |
| InstructionTypeResponse | instructionTypeResponse | ✅ Exact | Full property set match |
| InterestReport | InterestReport | ❌ Mismatch | Missing: ['monthlyInterestAmount', 'settlementBIC', 'month'] |
| InterestReports | InterestReports | ⚠️ Partial | Types: ['`dailyReport`: array vs dailyreport'] |
| LacAgenda | LacAgenda | ❌ Mismatch | Missing: ['resetToBasePos', 'lacNumber', 'basePosition', 'upperPosition', 'lowerPosition'] |
| LacAgenda1 | - | ❌ Missing | Not found in generated OAS |
| LacDefaultAgenda | LacDefaultAgenda | ❌ Mismatch | Missing: ['resetToBasePos', 'lacNumber', 'basePosition', 'upperPosition', 'lowerPosition'] |
| LacDefaultAgenda1 | - | ❌ Missing | Not found in generated OAS |
| LacNumber | LacNumber | ✅ Exact | Full property set match |
| LacParameters | LacParameters | ❌ Mismatch | Missing: ['lacSendingCutOffTime', 'lacAdjustmentTime', 'nightTimeSettlement', 'lac'] |
| LcrDetails | LcrDetails | ⚠️ Partial | Extra: ['DebPartyBIC', 'LcrStatus', 'BulkType', 'InstdAgt', 'CgsLacInput', 'InstdSttlmBIC', 'Service', 'OriginalBulk', 'LcrReference', 'CgsLcrStatusUpdate', 'Amount']; Types: ['`cgsLcrStatusUpdate`: #/components/schemas/DateTime vs datetime', '`lcrReference`: #/components/schemas/OperationReference vs operationreference', '`cgsLacInput`: #/components/schemas/LacNumber vs lacnumber', '`credPartyBIC`: #/components/schemas/BIC8 vs bic8', '`instdSttlmBIC`: #/components/schemas/Bic11Only vs bic11only', '`amount`: #/components/schemas/Amount1 vs amount', '`dbrCrdFlag`: #/components/schemas/Sign vs sign', '`bulkType`: #/components/schemas/MessageType vs messagetype', '`service`: #/components/schemas/Service vs service', '`lcrStatus`: #/components/schemas/LcrStatus vs lcrstatus', '`instgSttlmBIC`: #/components/schemas/Bic11Only vs bic11only', '`originalBulk`: #/components/schemas/BulkReference vs bulkreference', '`lacInputFromS2`: #/components/schemas/LacNumber vs lacnumber', '`cgsLacOutput`: #/components/schemas/LacNumber vs lacnumber', '`businessDate`: #/components/schemas/Date vs date', '`instgAgt`: #/components/schemas/BIC8 vs bic8', '`s2LcrCreationTimestamp`: #/components/schemas/DateTime vs datetime', '`instdAgt`: #/components/schemas/BIC8 vs bic8', '`originalFileRef`: #/components/schemas/FileReference vs filereference', '`numTransactions`: #/components/schemas/Number1 vs number', '`debPartyBIC`: #/components/schemas/BIC8 vs bic8'] |
| LcrStatus | LcrStatus | ✅ Exact | Full property set match |
| Lcrs | Lcrs | ❌ Mismatch | Missing: ['originalBulkReferenceId', 'amount', 'dbrCrdFlag', 'instgAgt', 'lacNumber', 'originalInputFileReferenceId', 'lcrReference', 'lcrStatus', 'instdAgt', 'service', 'instdSttlmBIC', 'instgSttlmBIC', 'businessDateTime', 'settlementDate'] |
| LmrData | LmrData | ⚠️ Partial | Extra: ['LiquidityInstrCreditPosition', 'NumTotBulks', 'ProcessedLCRCreditPosition', 'ProcessedLCRDebitPosition', 'PositionLacClose']; Types: ['`numTotBulks`: #/components/schemas/Number vs number', '`liquidityInstrDebitPosition`: #/components/schemas/Amount1 vs amount', '`positionLacOpen`: #/components/schemas/Amount1 vs amount', '`processedLCRCreditPosition`: #/components/schemas/Amount1 vs amount', '`liquidityInstrCreditPosition`: #/components/schemas/Amount1 vs amount', '`processedLCRDebitPosition`: #/components/schemas/Amount1 vs amount', '`positionLacClose`: #/components/schemas/Amount1 vs amount'] |
| LnrData | LnrData | ⚠️ Partial | Extra: ['PositionNotification', 'PositionDtTm']; Types: ['`positionDtTm`: #/components/schemas/DateTime vs datetime', '`positionNotification`: #/components/schemas/Amount1 vs amount'] |
| MessageType | MessageType | ✅ Exact | Full property set match |
| ModuleIdentifier | ModuleIdentifier | ✅ Exact | Full property set match |
| Network | Network | ✅ Exact | Full property set match |
| NetworkFileName | NetworkFileName | ✅ Exact | Full property set match |
| Number1 | - | ❌ Missing | Not found in generated OAS |
| Offset | Offset | ✅ Exact | Full property set match |
| OperationDetails | OperationDetails | ⚠️ Partial | Extra: ['SettlementBIC', 'EffectiveDate', 'OperationStatus', 'OperationType', 'AuthRejectDateTime', 'UserAuthReject', 'UserIssuer', 'CommandRef', 'RequestDateTime', 'Critical']; Types: ['`authRejectDateTime`: #/components/schemas/DateTime vs datetime', '`operationType`: #/components/schemas/OperationType1 vs operationtype', '`effectiveDate`: #/components/schemas/Date vs date', '`operationStatus`: #/components/schemas/OperationStatus vs operationstatus', '`userAuthReject`: #/components/schemas/User vs user', '`requestDateTime`: #/components/schemas/DateTime vs datetime', '`commandRef`: #/components/schemas/OperationReference1 vs operationreference', '`settlementBIC`: #/components/schemas/BIC11 vs bic11', '`critical`: #/components/schemas/Boolean1 vs boolean', '`CGSSettlementBIC`: #/components/schemas/CGSSettlementBIC vs object', '`userIssuer`: #/components/schemas/User vs user'] |
| OperationReference | OperationReference | ✅ Exact | Full property set match |
| OperationReference1 | OperationReference1 | ✅ Exact | Full property set match |
| OperationStatus | OperationStatus | ✅ Exact | Full property set match |
| OperationType | OperationType | ✅ Exact | Full property set match |
| OperationType1 | OperationType1 | ✅ Exact | Full property set match |
| Operations | Operations | ❌ Mismatch | Missing: ['operationType', 'authRejectExecDateTime', 'effectiveDate', 'operationStatus', 'userAuthReject', 'requestDateTime', 'commandRef', 'settlementBIC', 'critical', 'userIssuer'] |
| OtherModuleCutOff | OtherModuleCutOff | ⚠️ Partial | Extra: ['Taw2End', 'Taw3End', 'Taw3Start', 'Taw2Start', 'OpeningTime', 'CgsEOD', 'Taw4End', 'CorEOD', 'Taw1End', 'SctEOD', 'B2bEOD', 'Taw1Start', 'Taw4Start']; Types: ['`taw4Start`: #/components/schemas/Time vs time', '`taw1Start`: #/components/schemas/Time vs time', '`taw2End`: #/components/schemas/Time vs time', '`taw2Start`: #/components/schemas/Time vs time', '`openingTime`: #/components/schemas/Time vs time', '`corEOD`: #/components/schemas/Time vs time', '`taw1End`: #/components/schemas/Time vs time', '`cgsEOD`: #/components/schemas/Time vs time', '`taw4End`: #/components/schemas/Time vs time', '`taw3Start`: #/components/schemas/Time vs time', '`taw3End`: #/components/schemas/Time vs time', '`sctEOD`: #/components/schemas/Time vs time', '`b2bEOD`: #/components/schemas/Time vs time'] |
| ParModhistory | ParModhistory | ❌ Mismatch | Missing: ['endParameterValidity', 'detailsHistory', 'initParameterValidity'] |
| ParticipantName | ParticipantName | ✅ Exact | Full property set match |
| ParticipantStatus | ParticipantStatus | ✅ Exact | Full property set match |
| PositionHistory | PositionHistory | ❌ Mismatch | Missing: ['amount', 'settlementBIC', 'businessDate', 'lacNumber', 'timeStamp'] |
| RequestId | RequestId | ✅ Exact | Full property set match |
| ResendAllDetails | ResendAllDetails | ⚠️ Partial | Extra: ['TimestampLastUpdate', 'FileStatus', 'FileType']; Types: ['`fileType`: #/components/schemas/FileType vs filetype', '`fileStatus`: #/components/schemas/FileStatus vs filestatus', '`timestampLastUpdate`: #/components/schemas/DateTime vs datetime'] |
| RetransmitOutFileDetails | RetransmitOutFileDetails | ⚠️ Partial | Extra: ['SettlementBIC', 'BusinessDate', 'PreferredAgentBIC', 'FileType', 'FileReference', 'FileStatus', 'Lac']; Types: ['`businessDate`: #/components/schemas/Date vs date', '`preferredAgentBIC`: #/components/schemas/BIC8 vs bic8', '`fileType`: #/components/schemas/FileType vs filetype', '`fileStatus`: #/components/schemas/FileStatus vs filestatus', '`settlementBIC`: #/components/schemas/Bic11Only vs bic11only', '`fileReference`: #/components/schemas/FileReference vs filereference', '`lac`: #/components/schemas/LacNumber vs lacnumber'] |
| RevokeAllLcrDetails | RevokeAllLcrDetails | ⚠️ Partial | Extra: ['SettlementBIC']; Types: ['`settlementBIC`: #/components/schemas/Bic11Only vs bic11only', '`businessDate`: #/components/schemas/Date vs date'] |
| RevokeLcrDetails | RevokeLcrDetails | ⚠️ Partial | Extra: ['InstgSttlmBIC', 'LcrReference', 'S2Service', 'InstgAgt']; Types: ['`businessDate`: #/components/schemas/Date vs date', '`instgAgt`: #/components/schemas/BIC8 vs bic8', '`lcrReference`: #/components/schemas/OperationReference vs operationreference', '`lcrStatus`: #/components/schemas/LcrStatus vs lcrstatus', '`instdAgt`: #/components/schemas/BIC8 vs bic8', '`instdSttlmBIC`: #/components/schemas/Bic11Only vs bic11only', '`instgSttlmBIC`: #/components/schemas/Bic11Only vs bic11only', '`s2Service`: #/components/schemas/Service vs service'] |
| SearchCriteria | SearchCriteria | ⚠️ Partial | Extra: ['AmountFrom', 'MonthTo', 'FileType', 'InstructionTp', 'LcrReference', 'InstgAgt', 'LacNumber', 'SettlementDateTo', 'Critical', 'AuthRejectDateTimeTo', 'InstgSttlmBIC', 'SettlementBIC', 'BusinessDate', 'DebitSttlmBIC', 'PreferredAgentBIC', 'CommandType', 'LcrStatus', 'RequestDateTimeTo', 'OperationStatus', 'EffectiveDate', 'AuthRejectExecDateTime', 'InstdSttlmBIC', 'AmountTo', 'EndValidityDate', 'PreferredS2Service', 'EventDescription', 'MonthFrom', 'RequestDateTimeFrom', 'CreditSttlmBIC', 'UserAuthReject', 'RequestDate', 'DateTimeTo', 'NetworkFileName', 'InstdAgt', 'CommandStatus', 'SettlementDateFrom', 'UserIssuer', 'InstructionReference', 'Month', 'SettlementDate', 'DateType', 'DateTimeFrom', 'DefaultValues', 'AuthRejectDateTimeFrom', 'InstructionStatus', 'OperationType', 'FileReference', 'BusinessDateFrom', 'FileStatus', 'Service', 'CommandRef', 'InitialValidityDate', 'BusinessDateTo', 'Status']; Types: ['`preferredS2Service`: #/components/schemas/Service vs service', '`initialValidityDate`: #/components/schemas/Date vs date', '`preferredAgentBIC`: #/components/schemas/BIC8 vs bic8', '`status`: #/components/schemas/ParticipantStatus vs participantstatus', '`settlementBIC`: #/components/schemas/Bic11Only vs bic11only', '`endValidityDate`: #/components/schemas/Date vs date'] |
| SearchCriteria1 | SearchCriteria1 | ⚠️ Partial | Types: ['`instructionReference`: #/components/schemas/InstructionReference vs instructionreference', '`businessDateTo`: #/components/schemas/Date vs date', '`debitSttlmBIC`: #/components/schemas/BIC11 vs bic11', '`creditSttlmBIC`: #/components/schemas/BIC11 vs bic11', '`businessDateFrom`: #/components/schemas/Date vs date', '`instructionTp`: #/components/schemas/InstructionTypeRequest vs instructiontyperequest', '`settlementBIC`: #/components/schemas/Bic11Only vs bic11only', '`amountTo`: #/components/schemas/Amount1 vs amount', '`instructionStatus`: #/components/schemas/InstructionStatus vs instructionstatus', '`amountFrom`: #/components/schemas/Amount1 vs amount'] |
| SearchCriteria10 | SearchCriteria10 | ⚠️ Partial | Types: ['`authRejectDateTimeFrom`: #/components/schemas/DateTime vs datetime', '`commandType`: #/components/schemas/CommandType vs commandtype', '`authRejectDateTimeTo`: #/components/schemas/DateTime vs datetime', '`requestDateTimeFrom`: #/components/schemas/DateTime vs datetime', '`commandStatus`: #/components/schemas/CommandStatus vs commandstatus', '`requestDateTimeTo`: #/components/schemas/DateTime vs datetime', '`userAuthReject`: #/components/schemas/User vs user', '`userIssuer`: #/components/schemas/User vs user'] |
| SearchCriteria11 | SearchCriteria11 | ⚠️ Partial | Types: ['`authRejectExecDateTime`: #/components/schemas/DateTime vs datetime', '`operationType`: #/components/schemas/OperationType vs operationtype', '`requestDate`: #/components/schemas/Date vs date', '`effectiveDate`: #/components/schemas/Date vs date', '`operationStatus`: #/components/schemas/OperationStatus vs operationstatus', '`userAuthReject`: #/components/schemas/User vs user', '`commandRef`: #/components/schemas/CommandReference vs commandreference', '`critical`: #/components/schemas/Boolean1 vs boolean', '`settlementBIC`: #/components/schemas/Bic11Only vs bic11only', '`userIssuer`: #/components/schemas/User vs user'] |
| SearchCriteria12 | SearchCriteria12 | ⚠️ Partial | Types: ['`defaultValues`: #/components/schemas/Boolean vs boolean'] |
| SearchCriteria2 | SearchCriteria2 | ⚠️ Partial | Types: ['`settlementBIC`: #/components/schemas/Bic11Only vs bic11only', '`monthTo`: #/components/schemas/YearMonth vs yearmonth', '`monthFrom`: #/components/schemas/YearMonth vs yearmonth'] |
| SearchCriteria3 | SearchCriteria3 | ⚠️ Partial | Types: ['`settlementBIC`: #/components/schemas/Bic11Only vs bic11only', '`month`: #/components/schemas/YearMonth vs yearmonth'] |
| SearchCriteria4 | SearchCriteria4 | ⚠️ Partial | Types: ['`instgAgt`: #/components/schemas/BIC8 vs bic8', '`lacNumber`: #/components/schemas/LacNumber vs lacnumber', '`lcrReference`: #/components/schemas/OperationReference vs operationreference', '`lcrStatus`: #/components/schemas/LcrStatus vs lcrstatus', '`instdAgt`: #/components/schemas/BIC8 vs bic8', '`service`: #/components/schemas/Service vs service', '`settlementBIC`: #/components/schemas/Bic11Only vs bic11only', '`settlementDateTo`: #/components/schemas/Date vs date', '`instdSttlmBIC`: #/components/schemas/Bic11Only vs bic11only', '`settlementDateFrom`: #/components/schemas/Date vs date', '`instgSttlmBIC`: #/components/schemas/Bic11Only vs bic11only', '`dateTimeTo`: #/components/schemas/DateTime vs datetime', '`dateTimeFrom`: #/components/schemas/DateTime vs datetime'] |
| SearchCriteria5 | SearchCriteria5 | ⚠️ Partial | Types: ['`settlementBIC`: #/components/schemas/Bic11Only vs bic11only', '`lcrReference`: #/components/schemas/OperationReference vs operationreference', '`settlementDate`: #/components/schemas/Date vs date'] |
| SearchCriteria6 | SearchCriteria6 | ⚠️ Partial | Types: ['`settlementBIC`: #/components/schemas/Bic11Only vs bic11only', '`lcrReference`: #/components/schemas/OperationReference vs operationreference', '`businessDate`: #/components/schemas/Date vs date'] |
| SearchCriteria7 | SearchCriteria7 | ⚠️ Partial | Types: ['`dateType`: #/components/schemas/DateType vs datetype', '`preferredAgentBIC`: #/components/schemas/BIC8 vs bic8', '`fileStatus`: #/components/schemas/FileStatus vs filestatus', '`lacNumber`: #/components/schemas/LacNumber vs lacnumber', '`fileType`: #/components/schemas/FileType vs filetype', '`fileReference`: #/components/schemas/FileReference vs filereference', '`dateTimeTo`: #/components/schemas/DateTime vs datetime', '`dateTimeFrom`: #/components/schemas/DateTime vs datetime'] |
| SearchCriteria8 | SearchCriteria8 | ⚠️ Partial | Types: ['`fileType`: #/components/schemas/FileType vs filetype', '`networkFileName`: #/components/schemas/NetworkFileName vs networkfilename', '`businessDate`: #/components/schemas/Date vs date'] |
| SearchCriteria9 | SearchCriteria9 | ⚠️ Partial | Types: ['`settlementBIC`: #/components/schemas/Bic11Only vs bic11only', '`dateTimeTo`: #/components/schemas/DateTime vs datetime', '`dateTimeFrom`: #/components/schemas/DateTime vs datetime', '`eventDescription`: #/components/schemas/EventDescription vs eventdescription'] |
| SenderBIC | SenderBIC | ✅ Exact | Full property set match |
| SenderBIC1 | - | ❌ Missing | Not found in generated OAS |
| Service | Service | ✅ Exact | Full property set match |
| SettlementBIC | SettlementBIC | ⚠️ Partial | Extra: ['InitialSettBICValidityDate']; Types: ['`settlementBICCode`: #/components/schemas/Bic11Only vs bic11only', '`initialSettBICValidityDate`: #/components/schemas/Date vs date', '`endSettBICValidityDate`: #/components/schemas/Date vs date'] |
| SettlementBICAmend | SettlementBICAmend | ⚠️ Partial | Extra: ['AutomaticAdjustment', 'DlrFileRequired', 'MaxRcvgFileSize', 'LmrFileRequired']; Types: ['`eodFulDefund`: #/components/schemas/Boolean vs boolean', '`automaticAdjustment`: #/components/schemas/Boolean vs boolean', '`maxRcvgFileSize`: #/components/schemas/Number vs number', '`dlrFileRequired`: #/components/schemas/Boolean vs boolean', '`settlBICName`: #/components/schemas/ParticipantName vs participantname', '`lmrFileRequired`: #/components/schemas/Boolean vs boolean', '`lnrFileRequired`: #/components/schemas/Boolean vs boolean'] |
| SettlementBICDetails | SettlementBICDetails | ⚠️ Partial | Extra: ['SettlementBIC', 'PreferredAgentBIC', 'EndValidityDate', 'InitialValidityDate', 'ParModhistory', 'PreferredS2Service', 'Status']; Types: ['`preferredS2Service`: #/components/schemas/Service vs service', '`initialValidityDate`: #/components/schemas/Date vs date', '`preferredAgentBIC`: #/components/schemas/BIC8 vs bic8', '`status`: #/components/schemas/ParticipantStatus vs participantstatus', '`settlementBIC`: #/components/schemas/Bic11Only vs bic11only', '`endValidityDate`: #/components/schemas/Date vs date', '`parModhistory`: array vs parmodhistory'] |
| SettlementBICParameters | SettlementBICParameters | ⚠️ Partial | Extra: ['SettlBICName', 'EodFulDefund', 'AutomaticAdjustment', 'LmrFileRequired', 'MaxRcvgFileSize', 'DlrFileRequired', 'LnrFileRequired']; Types: ['`eodFulDefund`: #/components/schemas/Boolean vs boolean', '`automaticAdjustment`: #/components/schemas/Boolean vs boolean', '`maxRcvgFileSize`: #/components/schemas/StandardInteger vs standardinteger', '`dlrFileRequired`: #/components/schemas/Boolean vs boolean', '`settlBICName`: #/components/schemas/ParticipantName vs participantname', '`lmrFileRequired`: #/components/schemas/Boolean vs boolean', '`lnrFileRequired`: #/components/schemas/Boolean vs boolean'] |
| SettlementBICs | SettlementBICs | ❌ Mismatch | Missing: ['preferredS2Service', 'settlementBIC', 'initialValidityDate', 'name', 'endValidityDate', 'preferredAgentBIC', 'status'] |
| Sign | Sign | ✅ Exact | Full property set match |
| StandardInteger | StandardInteger | ✅ Exact | Full property set match |
| Time | Time | ✅ Exact | Full property set match |
| TransferType | TransferType | ✅ Exact | Full property set match |
| User | User | ✅ Exact | Full property set match |
| YearMonth | YearMonth | ✅ Exact | Full property set match |
| amendChangeSettlementBICRequest | amendChangeSettlementBICRequest | ❌ Mismatch | Missing: ['settlementBICAmend', 'settlementBIC', 'dateTime']; Extra: ['SettlementBIC', 'SettlementBICAmend'] |
| amendChangeSettlementBICResponse | amendChangeSettlementBICResponse | ❌ Mismatch | Missing: ['commandRef', 'dateTime']; Extra: ['CommandRef'] |
| commandDetailsRequest | commandDetailsRequest | ❌ Mismatch | Missing: ['commandRef', 'dateTime']; Extra: ['DateTime'] |
| commandDetailsResponse | commandDetailsResponse | ❌ Mismatch | Missing: ['userIssuer', 'authRejectDateTime', 'revokeLcrDetails', 'commandType', 'calendarDetails', 'commandStatus', 'fundingDefundingDetails', 'revokeAllLcrDetails', 'retransmitOutFileDetails', 'userAuthReject', 'requestDateTime', 'commandRef', 'resendAllDetails', 'dateTime', 'agendaDetails']; Extra: ['UserIssuer', 'FundingDefundingDetails', 'RevokeAllLcrDetails'] |
| currentPositionRequest | currentPositionRequest | ❌ Mismatch | Missing: ['settlementBIC', 'dateTime'] |
| currentPositionResponse | currentPositionResponse | ❌ Mismatch | Missing: ['dateTime', 'currentPosition'] |
| fileDetailsRequest | fileDetailsRequest | ❌ Mismatch | Missing: ['searchCriteria', 'dateTime']; Extra: ['SearchCriteria'] |
| fileDetailsResponse | fileDetailsResponse | ❌ Mismatch | Missing: ['fileDetails', 'dateTime']; Extra: ['FileDetails'] |
| getDefaultAgendaRequest | getDefaultAgendaRequest | ❌ Mismatch | Missing: ['settlementBIC', 'dateTime']; Extra: ['DateTime'] |
| getDefaultAgendaResponse | getDefaultAgendaResponse | ❌ Mismatch | Missing: ['defaultAgenda', 'settlementBIC', 'dateTime']; Extra: ['SettlementBIC'] |
| interestDailyReportRequest | interestDailyReportRequest | ❌ Mismatch | Missing: ['searchCriteria', 'dateTime']; Extra: ['DateTime'] |
| interestDailyReportResponse | interestDailyReportResponse | ❌ Mismatch | Missing: ['settlementBIC', 'dateTime', 'interestReports'] |
| interestMonthlyReportRequest | interestMonthlyReportRequest | ❌ Mismatch | Missing: ['searchCriteria', 'dateTime'] |
| interestMonthlyReportResponse | interestMonthlyReportResponse | ❌ Mismatch | Missing: ['dateTime', 'interestReport'] |
| lcrDetailsRequest | lcrDetailsRequest | ❌ Mismatch | Missing: ['searchCriteria', 'dateTime'] |
| lcrDetailsResponse | lcrDetailsResponse | ❌ Mismatch | Missing: ['dateTime', 'lcrDetails']; Extra: ['LcrDetails'] |
| lcrListRequest | lcrListRequest | ❌ Mismatch | Missing: ['searchCriteria', 'dateTime', 'offset']; Extra: ['Offset', 'SearchCriteria'] |
| lcrListResponse | lcrListResponse | ❌ Mismatch | Missing: ['lcrs', 'dateTime', 'offset', 'endOfList']; Extra: ['Offset', 'Lcrs', 'EndOfList', 'DateTime'] |
| liquidityManagementRequest | - | ❌ Missing | Not found in generated OAS |
| liquidityManagementResponse | - | ❌ Missing | Not found in generated OAS |
| listAlertsRequest | listAlertsRequest | ❌ Mismatch | Missing: ['searchCriteria', 'dateTime', 'offset']; Extra: ['DateTime', 'Offset', 'SearchCriteria'] |
| listAlertsResponse | listAlertsResponse | ❌ Mismatch | Missing: ['endOfList', 'dateTime', 'offset', 'alerts']; Extra: ['Offset', 'EndOfList', 'Alerts', 'DateTime'] |
| listCalendarRequest | listCalendarRequest | ❌ Mismatch | Missing: ['settlementBIC', 'dateTime', 'businessDate']; Extra: ['SettlementBIC', 'BusinessDate', 'DateTime'] |
| listCalendarResponse | listCalendarResponse | ❌ Mismatch | Missing: ['exceptionLacValues', 'dateTime', 'businessDate']; Extra: ['BusinessDate', 'ExceptionLacValues', 'DateTime'] |
| listCommandsRequest | listCommandsRequest | ❌ Mismatch | Missing: ['searchCriteria', 'dateTime', 'offset']; Extra: ['DateTime', 'Offset', 'SearchCriteria'] |
| listCommandsResponse | listCommandsResponse | ❌ Mismatch | Missing: ['commands', 'endOfList', 'dateTime', 'offset']; Extra: ['Commands', 'Offset', 'EndOfList', 'DateTime'] |
| listFilesRequest | listFilesRequest | ❌ Mismatch | Missing: ['searchCriteria', 'dateTime', 'offset']; Extra: ['DateTime', 'Offset', 'SearchCriteria'] |
| listFilesResponse | listFilesResponse | ❌ Mismatch | Missing: ['endOfList', 'dateTime', 'fileList', 'offset']; Extra: ['DateTime', 'FileList', 'EndOfList', 'Offset'] |
| listFundingDefundingRequest | listFundingDefundingRequest | ❌ Mismatch | Missing: ['searchCriteria', 'dateTime', 'offset']; Extra: ['DateTime', 'Offset', 'SearchCriteria'] |
| listFundingDefundingResponse | listFundingDefundingResponse | ❌ Mismatch | Missing: ['fundingDefunding', 'endOfList', 'dateTime', 'offset']; Extra: ['Offset', 'FundingDefunding', 'EndOfList', 'DateTime'] |
| listLACsConfigurationRequest | listLACsConfigurationRequest | ❌ Mismatch | Missing: ['searchCriteria', 'dateTime']; Extra: ['DateTime', 'SearchCriteria'] |
| listLACsConfigurationResponse | listLACsConfigurationResponse | ❌ Mismatch | Missing: ['otherModuleCutOff', 'dateTime', 'lacParameters']; Extra: ['OtherModuleCutOff', 'DateTime', 'LacParameters'] |
| listOperationRequest | listOperationRequest | ❌ Mismatch | Missing: ['searchCriteria', 'dateTime', 'offset']; Extra: ['DateTime', 'Offset', 'SearchCriteria'] |
| listOperationResponse | listOperationResponse | ❌ Mismatch | Missing: ['endOfList', 'dateTime', 'operations', 'offset']; Extra: ['Offset', 'EndOfList', 'Operations', 'DateTime'] |
| listSettlementBICsRequest | listSettlementBICsRequest | ❌ Mismatch | Missing: ['searchCriteria', 'dateTime']; Extra: ['DateTime', 'SearchCriteria'] |
| listSettlementBICsResponse | listSettlementBICsResponse | ❌ Mismatch | Missing: ['dateTime', 'settlementBICs']; Extra: ['SettlementBICs', 'DateTime'] |
| operationDetailsRequest | operationDetailsRequest | ❌ Mismatch | Missing: ['commandRef', 'dateTime']; Extra: ['CommandRef', 'DateTime'] |
| operationDetailsResponse | operationDetailsResponse | ❌ Mismatch | Missing: ['dateTime', 'operationDetails']; Extra: ['DateTime', 'OperationDetails'] |
| positionLacRequest | positionLacRequest | ❌ Mismatch | Missing: ['businessDateTo', 'lacNumber', 'businessDateFrom', 'settlementBIC', 'dateTime']; Extra: ['SettlementBIC', 'DateTime', 'BusinessDateFrom', 'BusinessDateTo', 'LacNumber'] |
| positionLacResponse | positionLacResponse | ❌ Mismatch | Missing: ['positionHistory', 'dateTime']; Extra: ['PositionHistory', 'DateTime'] |
| rejectParticipantOperationRequest | rejectParticipantOperationRequest | ❌ Mismatch | Missing: ['commandRef', 'dateTime']; Extra: ['CommandRef', 'DateTime'] |
| rejectParticipantOperationResponse | rejectParticipantOperationResponse | ❌ Mismatch | Missing: ['commandRef', 'dateTime']; Extra: ['CommandRef', 'DateTime'] |
| resendAllRequest | resendAllRequest | ❌ Mismatch | Missing: ['dateFrom', 'fileType', 'lacNumber', 'fileStatus', 'dateTo', 'dateTime']; Extra: ['FileType', 'DateTime', 'FileStatus', 'DateFrom', 'LacNumber', 'DateTo'] |
| resendAllResponse | resendAllResponse | ❌ Mismatch | Missing: ['commandRef', 'commandStatus', 'dateTime']; Extra: ['CommandRef', 'CommandStatus', 'DateTime'] |
| retransmitOutFilesRequest | retransmitOutFilesRequest | ❌ Mismatch | Missing: ['networkFileName', 'dateTime']; Extra: ['NetworkFileName', 'DateTime'] |
| retransmitOutFilesResponse | retransmitOutFilesResponse | ❌ Mismatch | Missing: ['commandRef', 'commandStatus', 'dateTime']; Extra: ['CommandRef', 'CommandStatus', 'DateTime'] |
| revokeChangeSettlementBICRequest | revokeChangeSettlementBICRequest | ❌ Mismatch | Missing: ['dateTime', 'settlementBIC', 'endParticipantValidity', 'initParticipantValidity']; Extra: ['SettlementBIC', 'EndParticipantValidity', 'InitParticipantValidity', 'DateTime'] |
| revokeChangeSettlementBICResponse | revokeChangeSettlementBICResponse | ❌ Mismatch | Missing: ['commandRef', 'dateTime']; Extra: ['CommandRef', 'DateTime'] |
| revokeLcrRequest | revokeLcrRequest | ❌ Mismatch | Missing: ['searchCriteria', 'dateTime']; Extra: ['DateTime', 'SearchCriteria'] |
| revokeLcrResponse | revokeLcrResponse | ❌ Mismatch | Missing: ['commandRef', 'commandStatus', 'dateTime']; Extra: ['CommandRef', 'CommandStatus', 'DateTime'] |
| setCalendarRequest | setCalendarRequest | ❌ Mismatch | Missing: ['settlementBIC', 'dateTime', 'businessDate', 'exceptionLacValues']; Extra: ['SettlementBIC', 'BusinessDate', 'ExceptionLacValues', 'DateTime'] |
| setCalendarResponse | setCalendarResponse | ❌ Mismatch | Missing: ['dateTime', 'effectiveDate']; Extra: ['EffectiveDate', 'DateTime'] |
| setDefaultAgendaRequest | setDefaultAgendaRequest | ❌ Mismatch | Missing: ['defaultDailyThresholds', 'settlementBIC', 'dateTime']; Extra: ['SettlementBIC', 'DateTime', 'DefaultDailyThresholds'] |
| setDefaultAgendaResponse | setDefaultAgendaResponse | ❌ Mismatch | Missing: ['dateTime', 'effectiveDate']; Extra: ['EffectiveDate', 'DateTime'] |
| settlementBICDetailsRequest | settlementBICDetailsRequest | ❌ Mismatch | Missing: ['settlementBIC', 'dateTime']; Extra: ['SettlementBIC', 'DateTime'] |
| settlementBICDetailsResponse | settlementBICDetailsResponse | ❌ Mismatch | Missing: ['dateTime', 'settlementBICDetails']; Extra: ['DateTime', 'SettlementBICDetails'] |
| updateSettlementBICRequest | updateSettlementBICRequest | ❌ Mismatch | Missing: ['settlementBICCode', 'dateTime', 'effectiveDate', 'settlementBICParameters']; Extra: ['SettlementBICCode', 'DateTime', 'EffectiveDate', 'SettlementBICParameters'] |
| updateSettlementBICResponse | updateSettlementBICResponse | ❌ Mismatch | Missing: ['commandRef', 'dateTime']; Extra: ['CommandRef', 'DateTime'] |


**Final Statistics:** 48 Exact Matches, 122 Discrepancies.
