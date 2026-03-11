# Schema Audit Report

### Missing in Excel:
- AgendaDetails
- Alerts
- Boolean
- Boolean1
- CGSSettlementBIC
- CalendarDetails
- Commands
- ConfiguredS2Dp
- ConfiguredS2Dp1
- CurrentPosition
- DailyReport
- DailyThresholds
- DailyThresholds1
- DefaultAgenda
- DefaultDailyThresholds
- DefaultDailyThresholds1
- DetailsHistory
- DlrData
- ExceptionLacValues
- ExceptionLacValues1
- FileDetails
- FileList
- FundingDefunding
- FundingDefundingDetails
- InterestReport
- InterestReports
- LacAgenda
- LacAgenda1
- LacDefaultAgenda
- LacDefaultAgenda1
- LacParameters
- LcrDetails
- Lcrs
- LmrData
- LnrData
- Number
- Number1
- OperationDetails
- OtherModuleCutOff
- ParModhistory
- PositionHistory
- ResendAllDetails
- RetransmitOutFileDetails
- RevokeAllLcrDetails
- RevokeLcrDetails
- SearchCriteria
- SearchCriteria1
- SearchCriteria10
- SearchCriteria11
- SearchCriteria12
- SearchCriteria2
- SearchCriteria3
- SearchCriteria4
- SearchCriteria5
- SearchCriteria6
- SearchCriteria7
- SearchCriteria8
- SearchCriteria9
- SenderBIC
- SenderBIC1
- SettlementBIC
- SettlementBICAmend
- SettlementBICDetails
- SettlementBICParameters
- SettlementBICs

### Extra in Excel (Missing in YAML):
- ErrorCode1
- OperationStatus1
- alerts
- commands
- configuredS2Dp
- dailyReport
- defaultDailyThresholds
- exceptionLacValues
- fileList
- fundingDefunding
- interestReport
- lacAgenda
- lacDefaultAgenda
- lcrs
- parModhistory
- positionHistory
- senderBIC
- senderBIC1
- settlementBICs

### Property Discrepancies:
#### Amount
  - Maximum mismatch: YAML=1000000000000000, Excel=1000000000000000.1
#### Amount1
  - Maximum mismatch: YAML=1000000000000000, Excel=1000000000000000.1
#### Bic11Only
  - Maximum mismatch: YAML=None, Excel=11.0
  - Minimum mismatch: YAML=None, Excel=11.0
#### CommandReference
  - Maximum mismatch: YAML=None, Excel=22.0
#### ErrorCodeDescription
  - Maximum mismatch: YAML=None, Excel=255.0
#### EventDescription
  - Maximum mismatch: YAML=None, Excel=1000.0
#### InstructionReference
  - Maximum mismatch: YAML=None, Excel=16.0
#### OperationReference
  - Maximum mismatch: YAML=None, Excel=16.0
#### OperationReference1
  - Maximum mismatch: YAML=None, Excel=22.0
#### Operations
  - Type mismatch: YAML=object, Excel=array
#### RequestId
  - Maximum mismatch: YAML=None, Excel=36.0
#### User
  - Maximum mismatch: YAML=None, Excel=8.0