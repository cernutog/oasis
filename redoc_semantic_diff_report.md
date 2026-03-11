# Redocly HTML Semantic Diff Report

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
- `/description:` A='The APDetails request allows the Participant to retrieve the details of an AP.\nThe response contains the details of the specified AP.\nA request addressed to an AP belonging to the sending participant will be responded with the full set of information available.' B='The APDetails request allows the Participant to retrieve the details of an AP.\nThe response contains the details of the specified AP.\nA request addressed to an AP belonging to the sending participant will be responded with the full set of information available.\n'
- `/operationId:` A='apDetails' B='APDetails'
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02) \nIt must be an enabled, suspended, inserted or R-only Participant (ErrorCode PY01)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must be an enabled, suspended, inserted or R-only Participant (ErrorCode PY01)'
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
- **A operationId**: `beneficiaryManagement`
- **B operationId**: `beneficiaryManagement`
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02) \nIt must be an enabled, suspended or R-only Liquidity Provider (ErrorCode PY01)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must be an enabled, suspended or R-only Liquidity Provider (ErrorCode PY01)'
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
- `/description:` A='The ChangeStatusAP request allows the Participant to change the status of an AP that it manages in the SCT Inst, to:\n- r-only (“RON”) if it was a valid AP (enabled) or to\n- Disabled (“DIS”) if it was an r-only AP.\nThe positive response contains the ReferenceId of the take in charge request for change by the system, but the effective modification of the master data has not been executed yet. Application will only take place after final authorization of the Dual Control by EBA CLEARING. The ReferenceId can be subsequently used in the CommandStatusInquiry request to get the status of the submitted command, see ref. 1.1.\nThe negative response contains the Code 204 if no record satisfying the set criteria is found.\nThe request must anyway be submitted within the “Routing Grace Time”, the system parameter that represents the time limit before midnight for the Participants to submit requests for updates, otherwise it is rejected with ErrorCode XA08.\nThe removal (status set as Disabled) can be performed on a non-target day.' B='The ChangeStatusAP request allows the Participant to change the status of an AP that it manages in the SCT Inst, to:\n- r-only (“RON”) if it was a valid AP (enabled) or to\n- Disabled (“DIS”) if it was an r-only AP.\nThe positive response contains the ReferenceId of the take in charge request for change by the system, but the effective modification of the master data has not been executed yet. Application will only take place after final authorization of the Dual Control by EBA CLEARING. The ReferenceId can be subsequently used in the CommandStatusInquiry request to get the status of the submitted command, see ref. 1.1.\nThe negative response contains the Code 204 if no record satisfying the set criteria is found.\nThe request must anyway be submitted within the “Routing Grace Time”, the system parameter that represents the time limit before midnight for the Participants to submit requests for updates, otherwise it is rejected with ErrorCode XA08.\nThe removal (status set as Disabled) can be performed on a non-target day.\n'
- `/operationId:` A='changeStatusAP' B='ChangeStatusAP'
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate  (ErrorCode XA02)\nIt must be an enabled, inserted or R-only Participant (ErrorCode PY01)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate  (ErrorCode XA02)\nIt must be an enabled, inserted or R-only Participant (ErrorCode PY01)'
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
- **A operationId**: `commandDelete`
- **B operationId**: `commandDelete`
- `/description:` A='The Command Delete request allows the Participant to delete a specific command that was submitted to the system and that has not been authorized yet by EBA CLEARING staff.\nThe response contains the confirmation or rejection of the request, Code 204 is returned if no record is found satisfying the selected criteria.' B='The Command Delete request allows the Participant to delete a specific command that was submitted to the system and that has not been authorized yet by EBA CLEARING staff.\nThe response contains the confirmation or rejection of the request, Code 204 is returned if no record is found satisfying the selected criteria.\n'
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02) \nIt must be an enabled, suspended or R-only Participant (ErrorCode PY01)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must be an enabled, suspended or R-only Participant (ErrorCode PY01)'
- `/parameters[1]/description:` A='The univocal ReferenceId that was generated by the system when the request for change was submitted \n\n **Validation Rule(s)** The command corresponding to the ReferenceId must not have been authorized yet (ErrorCode XA07)' B='The univocal ReferenceId that was generated by the system when the request for change was submitted\n\n **Validation Rule(s)** The command corresponding to the ReferenceId must not have been authorized yet (ErrorCode XA07)'
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
- **A operationId**: `commandStatusDetails`
- **B operationId**: `commandStatusDetails`
- `/description:` A='The Command Status Details request allows the Participant to view the details of a specific command that it submitted to the system.\nThe response contains the details of the command submitted by the Participant, or Code 204 if no record is found satisfying the selected criteria' B='The Command Status Details request allows the Participant to view the details of a specific command that it submitted to the system.\nThe response contains the details of the command submitted by the Participant, or Code 204 if no record is found satisfying the selected criteria\n'
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02) \nIt must be an enabled, suspended or R-only Participant (ErrorCode PY01)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must be an enabled, suspended or R-only Participant (ErrorCode PY01)'
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
- `/description:` A='The Communication of unavailability request allows the Participant to communicate his temporary unavailability.\nUsing this API, RT1 user can inform the system about the unavailability or the resumption of availability. It is possible to indicate the time of those events and to send a new message to update a previous one (e.g. to indicate that the expected duration of the unavailability will be shorter / longer). Optionally, RT1 users can indicate whether all the other RT1 users shall be informed. In such a case, all RT1 users can access to the information.' B='The Communication of unavailability request allows the Participant to communicate his temporary unavailability.\nUsing this API, RT1 user can inform the system about the unavailability or the resumption of availability. It is possible to indicate the time of those events and to send a new message to update a previous one (e.g. to indicate that the expected duration of the unavailability will be shorter / longer). Optionally, RT1 users can indicate whether all the other RT1 users shall be informed. In such a case, all RT1 users can access to the information.\n'
- `/operationId:` A='communicationOfUnavailability' B='CommunicationOfUnavailability'
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02) \nIt must be an enabled, r-only or suspended Participant (ErrorCode PY01)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must be an enabled, r-only or suspended Participant (ErrorCode PY01)'
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
- **A operationId**: `currentNetPosition`
- **B operationId**: `currentNetPosition`
- `/description:` A='The Current Position request allows the Participant to inquire about its real time liquidity position in the SCT Inst. \nUpon receiving this Request, the SCT Inst will inquire the real time Position of the inquiring Participant and returns the value of the timestamp of the reading. \nThe result of the inquiry done for a Participant that is not part of a Liquidity Branch Funds Balance will always be a positive value. If the Participant belongs to a Liquidity Branch Funds Balance, it is possible that the Current Position is a negative value.\nThe SCT Inst will always verify if the Participant is part of a Liquidity Branch Funds Balance, if this the case the Response will contain the Position of both the Participant and the Position of all Liquidity Branch Funds Balances the Participant is a member of.\nThe response contains the current Position of the Participant.\nIf the Participant is an LP, the system will return the current Position of each LSP for whose liquidity management it is responsible for.\nIn the case that the Participant is a member of one or more Liquidity Branch Funds Balances, the “BranchFundsBalanceId” and “BranchFundsBalancePosition” elements contain the Branch Funds Balance identification and the current position of the Branch Funds Balance to which the Participant belongs to. If the Participant is the Owner of one or more Liquidity Branch Funds Balances, the section “OwnedBranchFundsBalance” is repeated for each Liquidity Branch Funds Balance that is owns. The “OwnedMember” for each “OwnedBranchFundsBalance” lists the members of the Branch Funds Balance and the Position of each member.' B='The Current Position request allows the Participant to inquire about its real time liquidity position in the SCT Inst.\nUpon receiving this Request, the SCT Inst will inquire the real time Position of the inquiring Participant and returns the value of the timestamp of the reading.\nThe result of the inquiry done for a Participant that is not part of a Liquidity Branch Funds Balance will always be a positive value. If the Participant belongs to a Liquidity Branch Funds Balance, it is possible that the Current Position is a negative value.\nThe SCT Inst will always verify if the Participant is part of a Liquidity Branch Funds Balance, if this the case the Response will contain the Position of both the Participant and the Position of all Liquidity Branch Funds Balances the Participant is a member of.\nThe response contains the current Position of the Participant.\nIf the Participant is an LP, the system will return the current Position of each LSP for whose liquidity management it is responsible for.\nIn the case that the Participant is a member of one or more Liquidity Branch Funds Balances, the “BranchFundsBalanceId” and “BranchFundsBalancePosition” elements contain the Branch Funds Balance identification and the current position of the Branch Funds Balance to which the Participant belongs to. If the Participant is the Owner of one or more Liquidity Branch Funds Balances, the section “OwnedBranchFundsBalance” is repeated for each Liquidity Branch Funds Balance that is owns. The “OwnedMember” for each “OwnedBranchFundsBalance” lists the members of the Branch Funds Balance and the Position of each member.'
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must be an enabled, suspended, r-only or inserted Participant (ErrorCode PY01)\nIf the BIC is valued but different from the SenderBic, the SenderBic must be the Owner of the branchFundsBalanceId (ErrorCode XA06)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must be an enabled, suspended, r-only or inserted Participant (ErrorCode PY01)\nIf the BIC is valued but different from the SenderBic, the SenderBic must be the Owner of the branchFundsBalanceId (ErrorCode XA06)'
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
- **A operationId**: `defaultPosition`
- **B operationId**: `defaultPosition`
- `/description:` A='The Set Default Position request allows the Participant to set its default position for one day specific of the week, from Monday to Sunday, and for one or more specific LACs of that day. The Participant can set the lower, base, upper and reset to base position values for each LAC specified. Only the values of the specified LACs will be modified.\nIf the Participant is an LSP whose liquidity management is delegated the request is rejected with ErrorCode XA14.\nIf the Participant is an LP, it is allowed to send the SetDefaultPosition Request on behalf of the LSPs whose liquidity management is responsible for.\nThe response contains the EffectiveDate that was calculated by the system as the first occurrence for application of the new default values. This date is the next TARGET relative to the processing date of the request.\nIf the pair Day – LAC in the request is the next one with respect to the current one in the system, the new values are applied only if the API Request is received within the “Liquidity Agenda Grace Time” system parameter that represents the minimum time interval remaining to the end of the current LAC, otherwise the request is rejected. \nThe request must anyway be submitted within the “Routing Grace Time”, the system parameter that represents the time limit before midnight for the Participants to submit requests for updates, otherwise it is rejected with ErrorCode XA08.' B='The Set Default Position request allows the Participant to set its default position for one day specific of the week, from Monday to Sunday, and for one or more specific LACs of that day. The Participant can set the lower, base, upper and reset to base position values for each LAC specified. Only the values of the specified LACs will be modified.\nIf the Participant is an LSP whose liquidity management is delegated the request is rejected with ErrorCode XA14.\nIf the Participant is an LP, it is allowed to send the SetDefaultPosition Request on behalf of the LSPs whose liquidity management is responsible for.\nThe response contains the EffectiveDate that was calculated by the system as the first occurrence for application of the new default values. This date is the next TARGET relative to the processing date of the request.\nIf the pair Day – LAC in the request is the next one with respect to the current one in the system, the new values are applied only if the API Request is received within the “Liquidity Agenda Grace Time” system parameter that represents the minimum time interval remaining to the end of the current LAC, otherwise the request is rejected.\nThe request must anyway be submitted within the “Routing Grace Time”, the system parameter that represents the time limit before midnight for the Participants to submit requests for updates, otherwise it is rejected with ErrorCode XA08.'
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02) \nIt must be an enabled, r-only or inserted Participant (ErrorCode PY01)\nThe SenderBic liquidity must be managed by the SenderBic itself (ErrorCode XA14)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must be an enabled, r-only or inserted Participant (ErrorCode PY01)\nThe SenderBic liquidity must be managed by the SenderBic itself (ErrorCode XA14)'
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
- `/description:` A='The ReleaseLiquidity request allows the Participant to defund the desired amount from its Position in the SCT Inst to its DCA account in TIPS; the system shall check that the amount to be defunded is less than or equal to the available position of the Participant in the system and, if not, the request shall be rejected. \nThe Participant is allowed to ask for the defunding of the entire amount corresponding to its position.\nIf the Participant belongs to a Branch Funds Balance and the Liquidity Position of the Branch Funds Balance is lesser than the amount to be defunded, the request shall be rejected.\nIf the Participant is an LSP whose liquidity management is delegated, the request is rejected with ErrorCode XA14.\nIf the Participant is an LP, it is allowed to send the ReleaseLiquidity Request on behalf of the LSPs whose liquidity management is responsible for.\nIf the Participant is the Owner of a Branch Funds Balance, it is allowed to use this request to defund the liquidity of another not-suspended BIC that is a Member of the Branch Funds Balance, from the Position of the MemberBic in the system to the DCA account of the MemberBic in TIPS.\nThe response contains the confirmation or rejection of the request.\nIf the Participant is in Technical Isolation, the request is rejected with ErrorCode XA23\n\nPlease, note that the request can be sent to SCT Inst only if the “FREEZE TIPS Exchange Liquidity” command has not been issued, otherwise the request will be rejected with ErrorCode XA09.' B='The ReleaseLiquidity request allows the Participant to defund the desired amount from its Position in the SCT Inst to its DCA account in TIPS; the system shall check that the amount to be defunded is less than or equal to the available position of the Participant in the system and, if not, the request shall be rejected.\nThe Participant is allowed to ask for the defunding of the entire amount corresponding to its position.\nIf the Participant belongs to a Branch Funds Balance and the Liquidity Position of the Branch Funds Balance is lesser than the amount to be defunded, the request shall be rejected.\nIf the Participant is an LSP whose liquidity management is delegated, the request is rejected with ErrorCode XA14.\nIf the Participant is an LP, it is allowed to send the ReleaseLiquidity Request on behalf of the LSPs whose liquidity management is responsible for.\nIf the Participant is the Owner of a Branch Funds Balance, it is allowed to use this request to defund the liquidity of another not-suspended BIC that is a Member of the Branch Funds Balance, from the Position of the MemberBic in the system to the DCA account of the MemberBic in TIPS.\nThe response contains the confirmation or rejection of the request.\nIf the Participant is in Technical Isolation, the request is rejected with ErrorCode XA23\n\nPlease, note that the request can be sent to SCT Inst only if the “FREEZE TIPS Exchange Liquidity” command has not been issued, otherwise the request will be rejected with ErrorCode XA09.'
- `/operationId:` A='defunding' B='releaseLiquidiy'
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02) \nIt must be an enabled, r-only or inserted Participant (ErrorCode PY01)\nIf the MemberBIC is valued and different from the SenderBic, the SenderBIC must be the Owner of the branchFundsBalanceId (ErrorCode XA06)\nThe SenderBic liquidity must be managed by the SenderBic itself (ErrorCode XA14)\nThe SenderBic must not be isolated (“Technical Isolation” flag equal to “No”) (ErrorCode XA23)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must be an enabled, r-only or inserted Participant (ErrorCode PY01)\nIf the MemberBIC is valued and different from the SenderBic, the SenderBIC must be the Owner of the branchFundsBalanceId (ErrorCode XA06)\nThe SenderBic liquidity must be managed by the SenderBic itself (ErrorCode XA14)\nThe SenderBic must not be isolated (“Technical Isolation” flag equal to “No”) (ErrorCode XA23)'
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
- **A operationId**: `exceptionPositionCalendar`
- **B operationId**: `exceptionPositionCalendar`
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02) \nIt must be an enabled, r-only or inserted Participant (ErrorCode PY01)\nThe SenderBic liquidity must be managed by the SenderBic itself (ErrorCode XA14)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must be an enabled, r-only or inserted Participant (ErrorCode PY01)\nThe SenderBic liquidity must be managed by the SenderBic itself (ErrorCode XA14)'
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
- **A operationId**: `fileDetails`
- **B operationId**: `fileDetails`
- `/description:` A='The FileDetails request allows the Participant to retrieve the details of a file received from the SCT Inst.\nThe response returns the details of the file specified.' B='The FileDetails request allows the Participant to retrieve the details of a file received from the SCT Inst.\nThe response returns the details of the file specified.\n'
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02) \nIt must be an enabled, suspended or R-only Participant (ErrorCode PY01)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must be an enabled, suspended or R-only Participant (ErrorCode PY01)'
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
- **A operationId**: `funding`
- **B operationId**: `funding`
- `/description:` A='The PreFunding request allows the Participant to request for the transfer of a specified amount from their DCA account in TIPS to the RT1 Technical Account in TIPS, thus to their position in the SCT Inst System.\nIf the Participant is an LSP whose liquidity management is delegated, the request is rejected with ErrorCode XA14.\nIf the Participant is an LP, it is allowed to send the PreFunding Request on behalf of the LSPs whose liquidity management is responsible for.\nIf the Participant is the Owner of a Branch Funds Balance, it is allowed to use this functionality to move the liquidity of a not-suspended BIC that is Member of the Branch Funds Balance, from the DCA account of the MemberBic in TIPS to the Position of the MemberBic in the system.\nIf the Participant is in Technical Isolation, the request is rejected with ErrorCode XA23\nAfter receiving the Request for Prefunding by the Participant, the system sends a camt.050 message to TIPS with the instructions to make the funds available, and afterwards, when the system receives the camt.054 message from TIPS, it increases the position of the Participant with the required amount. \nThe requests for pre-funding are sent from the SCT Inst to TIPS and are asynchronous meaning that the application of the funds to the position of the Participant will be subject to a time delay.\nThe positive response is a confirmation that the request has been sent to TIPS for processing.\n\nPlease, note that the request can be sent to SCT Inst only only if the “FREEZE TIPS Exchange Liquidity” command has not been issued, otherwise the request will be rejected with ErrorCode XA09.' B='The PreFunding request allows the Participant to request for the transfer of a specified amount from their DCA account in TIPS to the RT1 Technical Account in TIPS, thus to their position in the SCT Inst System.\nIf the Participant is an LSP whose liquidity management is delegated, the request is rejected with ErrorCode XA14.\nIf the Participant is an LP, it is allowed to send the PreFunding Request on behalf of the LSPs whose liquidity management is responsible for.\nIf the Participant is the Owner of a Branch Funds Balance, it is allowed to use this functionality to move the liquidity of a not-suspended BIC that is Member of the Branch Funds Balance, from the DCA account of the MemberBic in TIPS to the Position of the MemberBic in the system.\nIf the Participant is in Technical Isolation, the request is rejected with ErrorCode XA23\nAfter receiving the Request for Prefunding by the Participant, the system sends a camt.050 message to TIPS with the instructions to make the funds available, and afterwards, when the system receives the camt.054 message from TIPS, it increases the position of the Participant with the required amount.\nThe requests for pre-funding are sent from the SCT Inst to TIPS and are asynchronous meaning that the application of the funds to the position of the Participant will be subject to a time delay.\nThe positive response is a confirmation that the request has been sent to TIPS for processing.\n\nPlease, note that the request can be sent to SCT Inst only only if the “FREEZE TIPS Exchange Liquidity” command has not been issued, otherwise the request will be rejected with ErrorCode XA09.\n'
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02).\nIt must be an enabled, r-only or inserted Participant (ErrorCode PY01)\nIt the MemberBic is valued but different from the SenderBic, the SenderBic must be the Owner of the branchFundsBalanceId (ErrorCode XA06)\nThe SenderBic liquidity must be managed by the SenderBic itself (ErrorCode XA14)\nThe SenderBic must not be isolated (“Technical Isolation” flag equal to “No”) (ErrorCode XA23)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02).\nIt must be an enabled, r-only or inserted Participant (ErrorCode PY01)\nIt the MemberBic is valued but different from the SenderBic, the SenderBic must be the Owner of the branchFundsBalanceId (ErrorCode XA06)\nThe SenderBic liquidity must be managed by the SenderBic itself (ErrorCode XA14)\nThe SenderBic must not be isolated (“Technical Isolation” flag equal to “No”) (ErrorCode XA23)'
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
- **A operationId**: `generateOutboundLto`
- **B operationId**: `generateOutboundLto`
- `/description:` A='This API is available for Liquidity Provider Participants only. This API allows a Liquidity Provider to request the generation of an outbound LTO message for a specific Beneficairy PSP. The relevant camt.050 message is then forwarded to TIPS' B='This API is available for Liquidity Provider Participants only. This API allows a Liquidity Provider to request the generation of an outbound LTO message for a specific Beneficairy PSP. The relevant camt.050 message is then forwarded to TIPS\n'
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02) \nIt must be an enabled, suspended or R-only Liquidity Provider  (ErrorCode PY01)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must be an enabled, suspended or R-only Liquidity Provider  (ErrorCode PY01)'
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
- **A operationId**: `generatePaymentStatusQuery`
- **B operationId**: `generatePaymentStatusQuery`
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02) \nIt must be an enabled, suspended or R-only Participant (ErrorCode PY01)\nThe SenderBic must not be isolated (“Technical Isolation” flag equal to “No”) (ErrorCode XA23)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must be an enabled, suspended or R-only Participant (ErrorCode PY01)\nThe SenderBic must not be isolated (“Technical Isolation” flag equal to “No”) (ErrorCode XA23)'
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
- **A operationId**: `getAccountBalance`
- **B operationId**: `getAccountBalance`
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02) \nIt must be an enabled, suspended or R-only Liquidity Provider (ErrorCode PY01)\nThe SenderBic must not be isolated (“Technical Isolation” flag equal to “No”) (ErrorCode XA23)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must be an enabled, suspended or R-only Liquidity Provider (ErrorCode PY01)\nThe SenderBic must not be isolated (“Technical Isolation” flag equal to “No”) (ErrorCode XA23)'
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
- **A operationId**: `getDefaultPosition`
- **B operationId**: `getDefaultPosition`
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must be an enabled, suspended, r-only or inserted Participant (ErrorCode PY01)\nIf the BIC is valued but different from the SenderBic, the SenderBic must be the Owner of the branchFundsBalanceId (ErrorCode XA06)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must be an enabled, suspended, r-only or inserted Participant (ErrorCode PY01)\nIf the BIC is valued but different from the SenderBic, the SenderBic must be the Owner of the branchFundsBalanceId (ErrorCode XA06)'
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
- **A operationId**: `getExceptionPositionCalendar`
- **B operationId**: `getExceptionPositionCalendar`
- `/description:` A='The GetExceptionCalendar request allows the Participant to retrieve its own set of values (lower, base,upper and reset to base position) that will be applied for each LAC of a specific day in the future (or for the current business date). It is possible to inquire the calendar up to one year from the current day.\nIf the Participant is an LP, it is allowed to send the GetExceptionPositionCalendar Request for those LSPs whose liquidity management is responsible for.\nOnly the Owner of a Liquidity Branch Funds Balance can inquire the values of a Member belonging to its Branch Funds Balance.\nThe returned values are the ones that will be really applied by the system, if an exception was set for the Business Date, it will be returned in place of the default values. If no exception was set for the Business Date, it will be returned the default values. \nThe response contains the values for the request Business Day.' B='The GetExceptionCalendar request allows the Participant to retrieve its own set of values (lower, base,upper and reset to base position) that will be applied for each LAC of a specific day in the future (or for the current business date). It is possible to inquire the calendar up to one year from the current day.\nIf the Participant is an LP, it is allowed to send the GetExceptionPositionCalendar Request for those LSPs whose liquidity management is responsible for.\nOnly the Owner of a Liquidity Branch Funds Balance can inquire the values of a Member belonging to its Branch Funds Balance.\nThe returned values are the ones that will be really applied by the system, if an exception was set for the Business Date, it will be returned in place of the default values. If no exception was set for the Business Date, it will be returned the default values.\nThe response contains the values for the request Business Day.\n'
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02) \nIt must be an enabled, suspended, r-only or inserted Participant (Error Code PY01)\nIf the BIC is valued but different from the SenderBic, the SenderBic must be the Owner of the branchFundsBalanceId (ErrorCode XA06)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must be an enabled, suspended, r-only or inserted Participant (Error Code PY01)\nIf the BIC is valued but different from the SenderBic, the SenderBic must be the Owner of the branchFundsBalanceId (ErrorCode XA06)'
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
- **A operationId**: `getParticipants`
- **B operationId**: `getParticipants`
- `/description:` A='The getParticipants request returns a list of all Participants present in the SCT Inst and is sorted by BIC and InitValidityDate. \nIt is possible to fill one or more fields as filtering criteria: in that case, the API Response returns the full set of rows corresponding to the filter criteria.' B='The getParticipants request returns a list of all Participants present in the SCT Inst and is sorted by BIC and InitValidityDate.\nIt is possible to fill one or more fields as filtering criteria: in that case, the API Response returns the full set of rows corresponding to the filter criteria.\n'
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** Must be equal to the BIC of the Participants certificate (ErrorCode XA02) \nSending Participant must not have status “Disabled” or “Changed” (ErrorCode PY01)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** Must be equal to the BIC of the Participants certificate (ErrorCode XA02)\nSending Participant must not have status “Disabled” or “Changed” (ErrorCode PY01)'
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
- **A operationId**: `inquiryUnavailability`
- **B operationId**: `inquiryUnavailability`
- `/description:` A='The Inquiry unavailability request allows the RT1 user to inquiry the unavailability of the participants, due to what communicated with the function Communication of Unavailability.\nThe Inquiry Unavailability request allows the RT1 user to inquire about the unavailability of:\n•\tRT1 Participants, based on what has been communicated through the Communication of Unavailability function.\n•\tA TIPS Participants, based on the messages sent by TIPS to RT1.\nThe two search options are mutually exclusive, as follows:\n•\tWhen “fromTIPS” is set to “1”, the search result includes all CS admi.004 messages received from TIPS. If present, the element “unavailableBic” is not taken into account.\n•\tWhen “fromTIPS” is set to “0” or is not present, the search result includes any admi.004 message, both CS admi.004 (triggered by an admi.004 received from TIPS) and admi.004 received from RT1 Participants. If “unavailableBic” is present and set to a specific BIC code, it is used as a filter.\n•\tWhen the request is sent without the elements “unavailableBic” and “fromTIPS”, the search result includes all current or future unavailability periods generated by any RT1 Participant, as well as all current or future unavailability periods generated by CS with the TIPS BIC as sender BIC.\n\nIf the unavailability has been communicated for a specific RT1 Participant and for all its APSPs (“BIC Code” = BIC8 and “APSPs Unavailability” checked), the APSP BICs unavailability information shall be available in the “Inquiry Unavailability” functionality even if the unavailability information has been required for a Participant BIC8 in “BIC Code” searching criteria field.' B='The Inquiry unavailability request allows the RT1 user to inquiry the unavailability of the participants, due to what communicated with the function Communication of Unavailability.\nThe Inquiry Unavailability request allows the RT1 user to inquire about the unavailability of:\n•    RT1 Participants, based on what has been communicated through the Communication of Unavailability function.\n•    A TIPS Participants, based on the messages sent by TIPS to RT1.\nThe two search options are mutually exclusive, as follows:\n•    When “fromTIPS” is set to “1”, the search result includes all CS admi.004 messages received from TIPS. If present, the element “unavailableBic” is not taken into account.\n•    When “fromTIPS” is set to “0” or is not present, the search result includes any admi.004 message, both CS admi.004 (triggered by an admi.004 received from TIPS) and admi.004 received from RT1 Participants. If “unavailableBic” is present and set to a specific BIC code, it is used as a filter.\n•    When the request is sent without the elements “unavailableBic” and “fromTIPS”, the search result includes all current or future unavailability periods generated by any RT1 Participant, as well as all current or future unavailability periods generated by CS with the TIPS BIC as sender BIC.\n\nIf the unavailability has been communicated for a specific RT1 Participant and for all its APSPs (“BIC Code” = BIC8 and “APSPs Unavailability” checked), the APSP BICs unavailability information shall be available in the “Inquiry Unavailability” functionality even if the unavailability information has been required for a Participant BIC8 in “BIC Code” searching criteria field.'
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02) \nIt must be an enabled, r-only or suspended Participant (ErrorCode PY01)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must be an enabled, r-only or suspended Participant (ErrorCode PY01)'
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
- `/description:` A='The InsertAP request allows the Participant to add a new AP that it wants to manage in the SCT Inst.\nThe positive response contains the ReferenceId of the take in charge request for change by the system, but the effective modification of the master data has not been executed yet. Application will only take place after final authorization of the Dual Control by EBA CLEARING. The ReferenceId can be subsequently used in the CommandStatusInquiry request to get the status of the submitted command, see ref. 1.1.\nThe request must anyway be submitted within the “Routing Grace Time”, the system parameter that represents the time limit before midnight for the Participants to submit requests for updates, otherwise it is rejected with ErrorCode XA08.' B='The InsertAP request allows the Participant to add a new AP that it wants to manage in the SCT Inst.\nThe positive response contains the ReferenceId of the take in charge request for change by the system, but the effective modification of the master data has not been executed yet. Application will only take place after final authorization of the Dual Control by EBA CLEARING. The ReferenceId can be subsequently used in the CommandStatusInquiry request to get the status of the submitted command, see ref. 1.1.\nThe request must anyway be submitted within the “Routing Grace Time”, the system parameter that represents the time limit before midnight for the Participants to submit requests for updates, otherwise it is rejected with ErrorCode XA08.\n'
- `/operationId:` A='insertAP' B='InsertAP'
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02) \nIt must be an enabled, inserted or R-only Participant (ErrorCode PY01)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must be an enabled, inserted or R-only Participant (ErrorCode PY01)'
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
- **A operationId**: `interestAmounts`
- **B operationId**: `interestAmounts`
- `/description:` A='The GetInterestAmount request returns the Interest Amount calculated by the System for each day of the required month. Retrieved data shall be sorted by date. \nA Liquidity Provider is allowed to perform inquiries on interests calculated for any of its LSP.\nAn Owner of a Liquidity Branch Funds Balance is allowed to perform inquiries on interests calculated for its Branch Funds Balance(s).\nThe Monthly interest information (with Daily Accrual Details) will be available for the selected month only after the Interest Calculation Process has run, otherwise no data will be provided for the month requested, and the following error XA19 will be returned to the API User: “The Interest Calculation has not been calculated for the requested month”.' B='The GetInterestAmount request returns the Interest Amount calculated by the System for each day of the required month. Retrieved data shall be sorted by date.\nA Liquidity Provider is allowed to perform inquiries on interests calculated for any of its LSP.\nAn Owner of a Liquidity Branch Funds Balance is allowed to perform inquiries on interests calculated for its Branch Funds Balance(s).\nThe Monthly interest information (with Daily Accrual Details) will be available for the selected month only after the Interest Calculation Process has run, otherwise no data will be provided for the month requested, and the following error XA19 will be returned to the API User: “The Interest Calculation has not been calculated for the requested month”.\n'
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** Must be equal to the BIC of the Participants certificate (ErrorCode XA02) \nThe “End Validity Date” of the Sender BIC Participant must be greater than the first processing date of the previous month compared to Month/Year (ErrorCode PY01)\nIn case of Branch Funds Balance, the SenderBic must be the Owner (ErrorCode XA18)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** Must be equal to the BIC of the Participants certificate (ErrorCode XA02)\nThe “End Validity Date” of the Sender BIC Participant must be greater than the first processing date of the previous month compared to Month/Year (ErrorCode PY01)\nIn case of Branch Funds Balance, the SenderBic must be the Owner (ErrorCode XA18)'
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
- **A operationId**: `liquidityTransfer`
- **B operationId**: `liquidityTransfer`
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02) \nIt must be an enabled or r-only Participant (Error Code PY01)\nIt must be the Owner of the branchFundsBalanceId (ErrorCode XA06)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must be an enabled or r-only Participant (Error Code PY01)\nIt must be the Owner of the branchFundsBalanceId (ErrorCode XA06)'
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
- **A operationId**: `listAAURT1ASTA`
- **B operationId**: `listAAURT1ASTA`
- `/description:` A='A Participant cal inqury the list of the RT1 TIPS ASTA AAU data for a specific Participant BIC8 and its APSPs configured in TIPS. \nThe listAAURT1ASTA request allows Participant to retrieve and download the list of all “AAU RT1 ASTA in TIPS BIC” configured for itself.' B='A Participant cal inqury the list of the RT1 TIPS ASTA AAU data for a specific Participant BIC8 and its APSPs configured in TIPS.\nThe listAAURT1ASTA request allows Participant to retrieve and download the list of all “AAU RT1 ASTA in TIPS BIC” configured for itself.'
- `/parameters[0]/description:` A='The BIC of EBA CL sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)' B='The BIC of EBA CL sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)'
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
- `/summary:` A='A Participant cal inqury the list of the RT1 TIPS ASTA AAU data for a specific Participant BIC8 and its APSPs configured in TIPS.' B='A Participant cal inqury the list of the RT1 TIPS ASTA AAU data for a specific Participant BIC8 and its APSPs configured in TIPS. '

#### `POST /listAPs/{senderBic}`
- **A operationId**: `listAPs`
- **B operationId**: `ListAPs`
- `/description:` A='The ListAPs request allows the Participant to retrieve the list of all APs in the SCT Inst sorted by BIC, DPBIC, and Status.\nIt is possible to fill one or more fields as filtering criteria: in this case the response returns the full set of rows matching the criteria.' B='The ListAPs request allows the Participant to retrieve the list of all APs in the SCT Inst sorted by BIC, DPBIC, and Status.\nIt is possible to fill one or more fields as filtering criteria: in this case the response returns the full set of rows matching the criteria.\n'
- `/operationId:` A='listAPs' B='ListAPs'
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02) \nIt must be an enabled, suspended, inserted or R-only Participant (ErrorCode PY01)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must be an enabled, suspended, inserted or R-only Participant (ErrorCode PY01)'
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
- **A operationId**: `listAlerts`
- **B operationId**: `listAlerts`
- `/description:` A='The ListAlerts Request allows the Participant to get all the alerts that were generated by the SCT Inst for the Participant. The Participant can use filtering criteria to restrict the number of alerts listed.\nIf the Participant is an LP, in the full set of the returned Alerts there are also the ones regarding the liquidity change of the positions of the LSPs on whose behalf such LP is configured to perform liquidity management functions. \nThe response contains the list of all Alerts that match the criteria and is sorted by AlertDate. The response contains a maximum of 1000 Alerts' B='The ListAlerts Request allows the Participant to get all the alerts that were generated by the SCT Inst for the Participant. The Participant can use filtering criteria to restrict the number of alerts listed.\nIf the Participant is an LP, in the full set of the returned Alerts there are also the ones regarding the liquidity change of the positions of the LSPs on whose behalf such LP is configured to perform liquidity management functions.\nThe response contains the list of all Alerts that match the criteria and is sorted by AlertDate. The response contains a maximum of 1000 Alerts\n'
- `/parameters[0]/description:` A='sender Bic \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02) \nIt must be an enabled, suspended or R-only Participant (ErrorCode PY01)' B='sender Bic\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must be an enabled, suspended or R-only Participant (ErrorCode PY01)'
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
- **A operationId**: `listBeneficiary`
- **B operationId**: `listBeneficiary`
- `/parameters[0]/description:` A='Bic \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02) \nIt must be an enabled, suspended or R-only Liquidity Provider (ErrorCode PY01)' B='Bic\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must be an enabled, suspended or R-only Liquidity Provider (ErrorCode PY01)'
- `/requestBody/required:` A='only_in_a' B=None
- `/requestBody/content/application/json/examples/Bad Request/value/offset:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/offset:` A=None B='only_in_b'
- `/requestBody/content/application/json/examples/OK/value/dateTime:` A='2024-11-08T14:29:00.012345' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-headers:` A='only_in_a' B=None
- `/responses/200/content/application/json/examples/OK/x-sandbox-request-path-params:` A=None B='only_in_b'
- `/responses/200/content/application/json/examples/OK/value/dateTime:` A='9999-12-31T12:55:45.000001' B='2019-06-21T23:20:50.000001'
- `/responses/200/content/application/json/examples/OK/value/endOfList:` A='1' B='0'
- `/responses/200/content/application/json/examples/OK/value/listBeneficiary:` A='len=1' B='len=2'
- `/responses/200/content/application/json/examples/OK/value/listBeneficiary[0]/beneficiaryAccount:` A='\xa0DE89370400440532013000' B='IT60X0542811101000000123456'
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
- **A operationId**: `listCommandStatus`
- **B operationId**: `listCommandStatus`
- `/description:` A='The ListCommandsStatus request allows the Participant to retrieve a list of all commands issued by its staff via GUI or via API that fall under Dual Control. It is possible to filter the result to a particular command type or requestor.\nThe SCT Inst uses the RequestDateTime as the starting point of the response data which is sorted by SubmissionDate, RequestStatus and CommandType. The Response is limited by a maximum of 1000 commands.' B='The ListCommandsStatus request allows the Participant to retrieve a list of all commands issued by its staff via GUI or via API that fall under Dual Control. It is possible to filter the result to a particular command type or requestor.\nThe SCT Inst uses the RequestDateTime as the starting point of the response data which is sorted by SubmissionDate, RequestStatus and CommandType. The Response is limited by a maximum of 1000 commands.\n'
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02) \nIt must be an enabled, suspended or R-only Participant (ErrorCode PY01)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must be an enabled, suspended or R-only Participant (ErrorCode PY01)'
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
- **A operationId**: `listCurrencies`
- **B operationId**: `listCurrencies`
- `/parameters[0]/description:` A='The BIC of EBA CL sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)' B='The BIC of EBA CL sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)'
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
- **A operationId**: `listFiles`
- **B operationId**: `listFiles`
- `/description:` A='The List Files request allows the Participant to retrieve a list of files sent by the SCT Inst to the Participant. The Participant has the option to use filtering criteria to reduce the number of files in the response.\nThe response will return a list of all files that match the criteria of the request and is sorted by DateFrom, TimeFrom, FileType, FilreRef and FileStatus. The resulting list shall contain a maximum of 1000 files, or Code 204 if no record satisfying the set criteria is found.\nThe system shall use the AcceptanceDateTimeFrom timestamp as the start point of the search. The Participant has the option to specify the DateTimeFrom up to the level of seconds to fine-tune the timeframe of the search. Milliseconds and nanoseconds are not supported by the API.' B='The List Files request allows the Participant to retrieve a list of files sent by the SCT Inst to the Participant. The Participant has the option to use filtering criteria to reduce the number of files in the response.\nThe response will return a list of all files that match the criteria of the request and is sorted by DateFrom, TimeFrom, FileType, FilreRef and FileStatus. The resulting list shall contain a maximum of 1000 files, or Code 204 if no record satisfying the set criteria is found.\nThe system shall use the AcceptanceDateTimeFrom timestamp as the start point of the search. The Participant has the option to specify the DateTimeFrom up to the level of seconds to fine-tune the timeframe of the search. Milliseconds and nanoseconds are not supported by the API.\n'
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02) \nIt must be an enabled, suspended or R-only Participant (ErrorCode PY01)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must be an enabled, suspended or R-only Participant (ErrorCode PY01)'
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
- `/description:` A='The ListInstructionsFundingDefunding request returns a list of all instructions present in the SCT Inst for a specific BIC and is sorted by Date. \nIt is possible to fill one or more fields as filtering criteria: in that case, the API Response returns the full set of rows corresponding to the filter criteria. \nIf the Participant is an LP, it is allowed to inquire the instructions of the LSPs whose liquidity management is responsible for.\nIf the Participant is the Owner of a Branch Funds Balance, it is allowed to inquire the instructions of another BIC that is a Member of the Branch Funds Balance that it owns.\nThe configuration of LSP and Branch Funds Balances taken into account for checks by the system is the one present at the moment in which the API Request is received: no restriction is applied to old stored instructions for which a different configuration was active.\nIf all the checks pass, but the system does not find any instruction related to the filtering criteria of the Request, the reason Code 204 – No Record Found is returned.\nThe resulting list shall contain a maximum of 1000 rows satisfying the criteria, in the case that the result has more than 1000 matching instructions, the response will contain an offset. By resubmitting the same request with a different offset value the Participant can retrieve all matching instructions' B='The ListInstructionsFundingDefunding request returns a list of all instructions present in the SCT Inst for a specific BIC and is sorted by Date.\nIt is possible to fill one or more fields as filtering criteria: in that case, the API Response returns the full set of rows corresponding to the filter criteria.\nIf the Participant is an LP, it is allowed to inquire the instructions of the LSPs whose liquidity management is responsible for.\nIf the Participant is the Owner of a Branch Funds Balance, it is allowed to inquire the instructions of another BIC that is a Member of the Branch Funds Balance that it owns.\nThe configuration of LSP and Branch Funds Balances taken into account for checks by the system is the one present at the moment in which the API Request is received: no restriction is applied to old stored instructions for which a different configuration was active.\nIf all the checks pass, but the system does not find any instruction related to the filtering criteria of the Request, the reason Code 204 – No Record Found is returned.\nThe resulting list shall contain a maximum of 1000 rows satisfying the criteria, in the case that the result has more than 1000 matching instructions, the response will contain an offset. By resubmitting the same request with a different offset value the Participant can retrieve all matching instructions'
- `/operationId:` A='listInstructionsFundingDefundingTIPS' B='listInstructionsFundingDefunding'
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** Must be equal to the BIC of the Participants certificate (ErrorCode XA02) \nIt must be an enabled, suspended or r-only Participant (Error Code PY01)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** Must be equal to the BIC of the Participants certificate (ErrorCode XA02)\nIt must be an enabled, suspended or r-only Participant (Error Code PY01)'
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
- **A operationId**: `listLACsConfiguration`
- **B operationId**: `listLACsConfiguration`
- `/parameters[0]/description:` A='The BIC of EBA CL sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)' B='The BIC of EBA CL sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)'
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
- **A operationId**: `listMessage`
- **B operationId**: `listMessage`
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02) \nIt must be an enabled, suspended or R-only Participant (ErrorCode PY01)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must be an enabled, suspended or R-only Participant (ErrorCode PY01)'
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
- _(truncated 1 more op diffs)_

#### `POST /listParticipantOperation/{senderBic}`
- **A operationId**: `listParticipantOperation`
- **B operationId**: `ListParticipantOperation`
- `/description:` A='The List Participant Operation request allows the Participant to retrieve the list of a specific operations based on a search filter.\nThe response returns the requested details or Code 204 if no record satisfying the criteria is found.' B='The List Participant Operation request allows the Participant to retrieve the list of a specific operations based on a search filter.\nThe response returns the requested details or Code 204 if no record satisfying the criteria is found.\n'
- `/operationId:` A='listParticipantOperation' B='ListParticipantOperation'
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02) \nIt must not be a disabled or changed Participant (ErrorCode PY01)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must not be a disabled or changed Participant (ErrorCode PY01)'
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
- `/description:` A='The system shall use the AcceptanceDateTimeFrom timestamp as the start point of the search and the same UTC format as the AT-T056 contained in the instant payment pacs.008. The Participant has the option to specify the AcceptanceDateTimeFrom up to the level of milliseconds to fine-tune the timeframe of the search.' B='The system shall use the AcceptanceDateTimeFrom timestamp as the start point of the search and the same UTC format as the AT-T056 contained in the instant payment pacs.008. The Participant has the option to specify the AcceptanceDateTimeFrom up to the level of milliseconds to fine-tune the timeframe of the search. '
- `/operationId:` A='listPayments' B='ListPayments'
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02) \nIt must be an enabled, suspended or R-only Participant (ErrorCode PY01)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must be an enabled, suspended or R-only Participant (ErrorCode PY01)'
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
- **A operationId**: `listThrottlingParameters`
- **B operationId**: `listThrottlingParameters`
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** Must be equal to the BIC of the Participants certificate (ErrorCode XA02) \nSending Participant must not have status “Disabled” or “Changed” (ErrorCode PY01)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** Must be equal to the BIC of the Participants certificate (ErrorCode XA02)\nSending Participant must not have status “Disabled” or “Changed” (ErrorCode PY01)'
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
- **A operationId**: `listTransactions`
- **B operationId**: `listTransactions`
- `/description:` A='The ListTransactions request allows the Participant to retrieve a list of R-messages (pacs.004, pacs.002, pacs.028, camt.056, camt.027 and camt.029) send to or received from the SCT Inst. The Participant has the option to use filtering criteria to reduce the number of transactions in the response. In the case that the result has more than 1000 matching transactions, the response will contain an offset. By resubmitting the same request with a different offset value the Participant can retrieve all matching transactions.\nThe response will return a list of all R-messages, matching the criteria of the request that is sorted by TransactionId, ProcessingDate, ReceptionTime, InstructingBic, InstructedBic and TransactionStatus. The resulting list shall contain a maximum of 1000 R-messages.\nThe transactions rejected due to acceptance-date-time (AT-T056) already expired when received by RT1 System are not displayed (In case the pacs.008 cannot be delivered to the BB, because it is not reacheable (AB07) or when the pacs.008 arrive in the CS already overdue (and it is consequently not delivered to the BB and rejected to the OB for timeout - AB06), the transaction will not be visible in the PWS and API by the Beneficiary Bank but will be notified in the RSF file. In case the transaction is delivered to the BB and then goes in timeout (TM01 for BB and AB06 for OB), it is then visible via PWS and API to both OB and BB.)' B='The ListTransactions request allows the Participant to retrieve a list of R-messages (pacs.004, pacs.002, pacs.028, camt.056, camt.027 and camt.029) send to or received from the SCT Inst. The Participant has the option to use filtering criteria to reduce the number of transactions in the response. In the case that the result has more than 1000 matching transactions, the response will contain an offset. By resubmitting the same request with a different offset value the Participant can retrieve all matching transactions.\nThe response will return a list of all R-messages, matching the criteria of the request that is sorted by TransactionId, ProcessingDate, ReceptionTime, InstructingBic, InstructedBic and TransactionStatus. The resulting list shall contain a maximum of 1000 R-messages.\nThe transactions rejected due to acceptance-date-time (AT-T056) already expired when received by RT1 System are not displayed (In case the pacs.008 cannot be delivered to the BB, because it is not reacheable (AB07) or when the pacs.008 arrive in the CS already overdue (and it is consequently not delivered to the BB and rejected to the OB for timeout - AB06), the transaction will not be visible in the PWS and API by the Beneficiary Bank but will be notified in the RSF file. In case the transaction is delivered to the BB and then goes in timeout (TM01 for BB and AB06 for OB), it is then visible via PWS and API to both OB and BB.)\n'
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02) \nIt must be an enabled, suspended or R-only Participant (ErrorCode PY01)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must be an enabled, suspended or R-only Participant (ErrorCode PY01)'
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
- **A operationId**: `manageAAURT1ASTA`
- **B operationId**: `manageAAURT1ASTA`
- `/parameters[0]/description:` A='The BIC of EBA CL sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)' B='The BIC of EBA CL sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)'
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
- **A operationId**: `messageDetails`
- **B operationId**: `messageDetails`
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02) \nIt must be an enabled, suspended or R-only Participant (ErrorCode PY01)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must be an enabled, suspended or R-only Participant (ErrorCode PY01)'
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
- **A operationId**: `participantDetails`
- **B operationId**: `participantDetails`
- `/description:` A='The participantDetails request allows a Participant to retrieve the details of a specified Participant in the SCT Inst.\nIf the inquiring Participant asks for their own details they are allowed to download the complete set of parameters, otherwise they can see only a subset of the whole set. \nThe response contains a list of the parameter modifications associated to the BIC, containing the old configurations, the current one, and the new planned one if it has been already authorized.' B='The participantDetails request allows a Participant to retrieve the details of a specified Participant in the SCT Inst.\nIf the inquiring Participant asks for their own details they are allowed to download the complete set of parameters, otherwise they can see only a subset of the whole set.\nThe response contains a list of the parameter modifications associated to the BIC, containing the old configurations, the current one, and the new planned one if it has been already authorized.\n'
- `/parameters[0]/description:` A='sender Bic \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02) \nIt must not be a disabled or changed Participant (ErrorCode PY01)' B='sender Bic\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must not be a disabled or changed Participant (ErrorCode PY01)'
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
- `/description:` A='The Participant Operation Details request allows the Participant to retrieve the details of specific provisioning operations based on a search filter.\nThe response returns the requested details or Code 204 if no record satisfying the criteria is found.' B='The Participant Operation Details request allows the Participant to retrieve the details of specific provisioning operations based on a search filter.\nThe response returns the requested details or Code 204 if no record satisfying the criteria is found.\n'
- `/operationId:` A='participantOperationDetails' B='ParticipantOperationDetails'
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02) \nIt must not be a disabled or changed Participant (ErrorCode PY01)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must not be a disabled or changed Participant (ErrorCode PY01)'
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
- `/description:` A='The PaymentDetails request allows the Participant to retrieve the details of a specific Payment Transaction that it sent to or received from the SCT Inst.\nThe response returns the requested details.' B='The PaymentDetails request allows the Participant to retrieve the details of a specific Payment Transaction that it sent to or received from the SCT Inst.\nThe response returns the requested details.\n'
- `/operationId:` A='paymentDetails' B='PaymentDetails'
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02) \nIt must be an enabled, suspended or R-only Participant (ErrorCode PY01)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must be an enabled, suspended or R-only Participant (ErrorCode PY01)'
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
- `/description:` A='The Reject Participant Operation allows the Participant to reject a specific change operation submitted and not yet authorized. (See 10.11)\nThe response contains the confirmation or rejection of the request, Code 204 is returned if no record is found satisfying the selected criteria.' B='The Reject Participant Operation allows the Participant to reject a specific change operation submitted and not yet authorized. (See 10.11)\nThe response contains the confirmation or rejection of the request, Code 204 is returned if no record is found satisfying the selected criteria.\n'
- `/operationId:` A='rejectParticipantOperation' B='RejectParticipantOperation'
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02) \nIt must be an enabled, suspended or R-only Participant (ErrorCode PY01)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must be an enabled, suspended or R-only Participant (ErrorCode PY01)'
- `/parameters[1]/description:` A='The ReferenceId generated by the CS when the request to update was sent \n\n **Validation Rule(s)** The change operation corresponding to the ReferenceId must not have been authorized yet (ErrorCode XA07' B='The ReferenceId generated by the CS when the request to update was sent\n\n **Validation Rule(s)** The change operation corresponding to the ReferenceId must not have been authorized yet (ErrorCode XA07'
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
- **A operationId**: `transactionDetails`
- **B operationId**: `transactionDetails`
- `/description:` A='The TransactionDetails request allows the Participant the retrieve the details of a specific R-message, Payment Status Report or Investigation sent to or received by the SCT Inst.\nThe response contains the R-message, Payment Status Report or Investigation details.' B='The TransactionDetails request allows the Participant the retrieve the details of a specific R-message, Payment Status Report or Investigation sent to or received by the SCT Inst.\nThe response contains the R-message, Payment Status Report or Investigation details.\n'
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)'
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
- `/description:` A='The UpdateAP request allows the Participant to update the configuration of a specific AP that the Participant manages in the SCT Inst.\nThe positive response contains the ReferenceId of the take in charge request for change by the system, but the effective modification of the master data has not been executed yet. Application will only take place after final authorization of the Dual Control by EBA CLEARING. The ReferenceId can be subsequently used in the CommandStatusInquiry request to get the status of the submitted command, see ref. 1.1. \nThe negative response contains the Code 204 if no record satisfying the set criteria is found.\nThe request must anyway be submitted within the “Routing Grace Time”, the system parameter that represents the time limit before midnight for the Participants to submit requests for updates, otherwise it is rejected with ErrorCode XA08\nIn case the provisioning operation is inserted without changings (with the exception of the Effective Date), the command is rejected with error code XA31.' B='The UpdateAP request allows the Participant to update the configuration of a specific AP that the Participant manages in the SCT Inst.\nThe positive response contains the ReferenceId of the take in charge request for change by the system, but the effective modification of the master data has not been executed yet. Application will only take place after final authorization of the Dual Control by EBA CLEARING. The ReferenceId can be subsequently used in the CommandStatusInquiry request to get the status of the submitted command, see ref. 1.1.\nThe negative response contains the Code 204 if no record satisfying the set criteria is found.\nThe request must anyway be submitted within the “Routing Grace Time”, the system parameter that represents the time limit before midnight for the Participants to submit requests for updates, otherwise it is rejected with ErrorCode XA08\nIn case the provisioning operation is inserted without changings (with the exception of the Effective Date), the command is rejected with error code XA31.'
- `/operationId:` A='updateAP' B='UpdateAP'
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02) \nIt must be an enabled, inserted or R-only Participant (ErrorCode PY01)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must be an enabled, inserted or R-only Participant (ErrorCode PY01)'
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
- `/description:` A='The UpdateParticipant request allows a Participant to update its configuration in the SCT Inst.\nThe Participant can fill only the new values of the configuration elements that have to be changed; elements that are not present in the request are not involved in the change and the system will keep the existing values for them.\nIf the Participant is an LSP, it is allowed to submit a request for change of its Liquidity Management.\nIf the Participant is an LP, it is not allowed to change its own Liquidity Management parameter.\nThe positive response contains the ReferenceId of the take in charge request for change by the system, but the effective modification of the master data has not been executed yet. Application will only take place after final authorization of the Dual Control by EBA CLEARING. The ReferenceId can be subsequently used in the CommandStatusInquiry request to get the status of the submitted command, see ref. 1.1.\nThe request must anyway be submitted within the “Routing Grace Time”, the system parameter that represents the time limit before midnight for the Participants to submit requests for updates, otherwise it is rejected with ErrorCode XA08.\nThe parameters provided in this API are classified as Critical or non-critical, see ref. 10.20\nDepending on the nature of the parameter, Critical or Not Critical, checks performed on the effective date change: \nFor Critical parameter:\n• if the command is issued on between Monday W1, and Tuesday the first effective date will be the Tuesday of the W3 week\n• if the command is issued between Tuesday Wednesday and Sunday W1 the first effective date will be the Tuesday of the W4 \nFor Not Critical parameter:\n• the effective date must be grater than the current business date, , with respect to the End Validity Date configured for the Participant.\nIn case the provisioning operation is inserted without changings (with the exception of the Effective Date), the command is rejected with error code XA31.' B='The UpdateParticipant request allows a Participant to update its configuration in the SCT Inst.\nThe Participant can fill only the new values of the configuration elements that have to be changed; elements that are not present in the request are not involved in the change and the system will keep the existing values for them.\nIf the Participant is an LSP, it is allowed to submit a request for change of its Liquidity Management.\nIf the Participant is an LP, it is not allowed to change its own Liquidity Management parameter.\nThe positive response contains the ReferenceId of the take in charge request for change by the system, but the effective modification of the master data has not been executed yet. Application will only take place after final authorization of the Dual Control by EBA CLEARING. The ReferenceId can be subsequently used in the CommandStatusInquiry request to get the status of the submitted command, see ref. 1.1.\nThe request must anyway be submitted within the “Routing Grace Time”, the system parameter that represents the time limit before midnight for the Participants to submit requests for updates, otherwise it is rejected with ErrorCode XA08.\nThe parameters provided in this API are classified as Critical or non-critical, see ref. 10.20\nDepending on the nature of the parameter, Critical or Not Critical, checks performed on the effective date change:\nFor Critical parameter:\n• if the command is issued on between Monday W1, and Tuesday the first effective date will be the Tuesday of the W3 week\n• if the command is issued between Tuesday Wednesday and Sunday W1 the first effective date will be the Tuesday of the W4\nFor Not Critical parameter:\n• the effective date must be grater than the current business date, , with respect to the End Validity Date configured for the Participant.\nIn case the provisioning operation is inserted without changings (with the exception of the Effective Date), the command is rejected with error code XA31.\n\n'
- `/operationId:` A='updateParticipant' B='participant'
- `/parameters[0]/description:` A='The BIC of the Participant sending the API Request \n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02) \nIt must be an enabled, suspended or R-only Participant (ErrorCode PY01)' B='The BIC of the Participant sending the API Request\n\n **Validation Rule(s)** It must be equal to the BIC identified through its certificate (ErrorCode XA02)\nIt must be an enabled, suspended or R-only Participant (ErrorCode PY01)'
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
- **Changed schemas**: 347

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

#### `BicExceptionDayValues`
- `/properties/sendAccountQueryToTips/description:` A='Whether the “Send Account Query to TIPS” flag for the relevant LAC is checked/unchecked. \nThe field is present only when set to: 1=YES' B='Whether the “Send Account Query to TIPS” flag for the relevant LAC is checked/unchecked.\nThe field is present only when set to: 1=YES'

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

#### `CommandItem1`
- `/properties/authorizer/description:` A='The authorizer of the event.\nIf the deletion is rejected because the command has been already authorized = the authorizer that already authorized the command.\nIf the deletion is accepted = the authorizer of the deletion request. \nIf the deletion is rejected for any other reason (but the command has not been already authorized), this field is empty.' B='The authorizer of the event.\nIf the deletion is rejected because the command has been already authorized = the authorizer that already authorized the command.\nIf the deletion is accepted = the authorizer of the deletion request.\nIf the deletion is rejected for any other reason (but the command has not been already authorized), this field is empty.'
- `/properties/requestStatus/description:` A='The status of the submitted request, it can contain only \n- “ATH” = Authorised if the deletion was accepted and the command was deleted\n- “RJT” Rejected by the system if the deletion failed and the command was not deleted' B='The status of the submitted request, it can contain only\n- “ATH” = Authorised if the deletion was accepted and the command was deleted\n- “RJT” Rejected by the system if the deletion failed and the command was not deleted'

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
- `/properties/technicalBic/description:` A='It indicates if the BIC is a technical one (1) or not (0)' B='It indicates if the BIC is a technical one (1) or not (0)\n\n **Validation Rule(s)** It can contain 0 or 1 (schema validation)'
- `/properties/tipsAccountOwnerBic/$ref:` A='#/components/schemas/Bic11Only' B='#/components/schemas/Bic11Only1'
- `/properties/tipsAccountOwnerBic/description:` A='TIPS DCA Account Owner for Instra-Service Liquidity Transfer (li-quidity funding/defunding)' B='The BIC(11) by which the Direct participant will be known to the ESM for settlement purpose'
- `/properties/tipsAdherence/description:` A='It indicates if the Participant joined to TIPS (1) or not (0) (Mandatory if the section is present)\n\n **Validation Rule(s)** Allowed values:\n- 0 = Participant not joined to TIPS\n- 1 = Participant joined to TIPS' B='It indicates if the Participant is allowed to settle transactions in TIPS through its TIPS DAC account.\n\n **Validation Rule(s)** It can assume the values:\n- “1” = YES\n- “0” = NO\n(schema validation)'

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
- `/properties/effectiveDate/description:` A='It indicates the future starting date for the planned changes\n\n **Validation Rule(s)** A date >= P Initial Validity Date between tomorrow and the EndValidityDate of the Participant (ErrorCode DT01)' B='It indicates the future starting date for the planned changes\n\n **Validation Rule(s)** For Critical parameter:\n• if on Monday W1 the first effective date will be Tuesday W3\n• if between Tuesday and Sunday W1 the first effective date will be Tuesday of the W4\n(ErrorCode DT01)\n• it must be greater than Current Date + 2 calendar days\n(ErrorCode DT01)'
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
- `/properties/bicAp/description:` A='The BIC of the AP' B='The BIC of the new AP\n\n **Validation Rule(s)** If already present in the system it must have ‘disabled’ status with respect to the InitValidityDate(ErrorCode PY01)'
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
- `/properties/unavailableBic/description:` A='BIC of the Participant or APSP that is going to be unavailable.\n\n **Validation Rule(s)** It must be equal to the BIC of the sender. If different, it must be one APSP of the SenderBic. (ErrorCode XA06).\nField used for duplicate checking (error code AM05)' B='BIC of the Participant or APSP that could be unavailable.\n\n **Validation Rule(s)** It must be one of the following:\n- Blank: the response shall provide all the BIC present in the admi.004 directory.\n- A direct Participant BIC that is enabled, suspended or r-only in the CS repository on the current calendar date (ErrorCode PY01).\n- An APSP BIC that is enabled, suspended or r-only in the CS repository on the current calendar date (ErrorCode PY01).\nThe list shall be ordered in alphabetic order.'

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

#### `Criteria2`
- `/properties/lspbranchFundsBalanceMemBic/description:` A='The BIC for which the API request is sent. If present, the system will return the stored instructions related to this BIC\n\n **Validation Rule(s)** One of the following must be true:\n- The BIC is an LSP of the SenderBic and the SenderBic manages the liquidity of the BIC \n- The BIC must belong to a branchFundsBalance and the SenderBic is the Owner of that branchFundsBalance\n \nIf none of the above conditions applies, the ErrorCode XA07 is returned.' B='The BIC for which the API request is sent. If present, the system will return the stored instructions related to this BIC\n\n **Validation Rule(s)** One of the following must be true:\n- The BIC is an LSP of the SenderBic and the SenderBic manages the liquidity of the BIC\n- The BIC must belong to a branchFundsBalance and the SenderBic is the Owner of that branchFundsBalance\n\nIf none of the above conditions applies, the ErrorCode XA07 is returned.'
- `/properties/type/description:` A='It indicates the type of instruction that is requested\n\n **Validation Rule(s)** It must be one of the configured values in the system. The possible values are:\n• Checkpoint Funding Request (CPFR)\n• Adjustment Funding Request (APFR)\n• LAC Funding notification (CPFN)\n• Checkpoint Liquidity Release Request (CLRR)\n• Adjustment Liquidity Release (ALRR) \n• Reversal (RVLT) \n• Emergency Liquidity Request Release (ELRR)\n• Emergency Funding (EPFN)\n (ErrorCode XA03)' B='It indicates the type of instruction that is requested\n\n **Validation Rule(s)** It must be one of the configured values in the system. The possible values are:\n• Checkpoint Funding Request (CPFR)\n• Adjustment Funding Request (APFR)\n• LAC Funding notification (CPFN)\n• Checkpoint Liquidity Release Request (CLRR)\n• Adjustment Liquidity Release (ALRR)\n• Reversal (RVLT)\n• Emergency Liquidity Request Release (ELRR)\n• Emergency Funding (EPFN)\n (ErrorCode XA03)'

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
- `/properties/fileType/description:` A='The file type\n\n **Validation Rule(s)** It must be one of the configured values in the system. The possible values:\nPSR”\n“DRR”\n“RSF”\n“MSR”\n“BCA”\n“BCS”\n"RTF-TIPS"\n"RTF-INST"\n"RTF-OLO"\n"RTF-IXB"\n (ErrorCode XA03)' B='The file type of the file\n\n **Validation Rule(s)** The file corresponding to the file reference must exist in the system, ref.10.7 (ErrorCode XA03)'
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

#### `Criteria3`
- `/properties/messageType/description:` A='Identification of the message sent by Participant\n\n **Validation Rule(s)** Possible values are:\n• Outbound LTO (camt.050)\n• Funding/Defunding LTO (camt.050)\n• Credit/Debit Notification (camt.054)\n• Receipt (camt.025)\n• Get Account (camt.003)\n• Return Account (camt.004)\n• Payment Status Query (camt.005) \n• Payment Status Query Response (camt.006)\n(schema error)' B='Identification of the message sent by Participant\n\n **Validation Rule(s)** Possible values are:\n• Outbound LTO (camt.050)\n• Funding/Defunding LTO (camt.050)\n• Credit/Debit Notification (camt.054)\n• Receipt (camt.025)\n• Get Account (camt.003)\n• Return Account (camt.004)\n• Payment Status Query (camt.005)\n• Payment Status Query Response (camt.006)\n(schema error)'
- `/properties/requestedThrough/description:` A='Indicates the interface through which the message (or the original message, in case of camt.025, camt.004 or camt.006) has been requested or sent.\n\n **Validation Rule(s)** Allowed values:\n• U2A: GUI-API interface;\n• A2A: Message interface;\n(schema validation) \nNot required if message type is equal to camt.054, ErrorCode XA07 is returned.\n"Resend Receipt" and "Resend Notification" are allowed only when the messages was previously trasmitted to the Participant via interface Message Interface' B='Indicates the interface through which the message (or the original message, in case of camt.025, camt.004 or camt.006) has been requested or sent.\n\n **Validation Rule(s)** Allowed values:\n• U2A: GUI-API interface;\n• A2A: Message interface;\n(schema validation)\nNot required if message type is equal to camt.054, ErrorCode XA07 is returned.\n"Resend Receipt" and "Resend Notification" are allowed only when the messages was previously trasmitted to the Participant via interface Message Interface'
- `/properties/senderReceiverBic/description:` A='Sender BIC of the message\n\n **Validation Rule(s)** One of the following must be true:\n- The BIC is an LSP of the SenderBic and the SenderBic manages the liquidity of the BIC \n- The BIC must belong to a Branch Funds Balance and the SenderBic is the Owner of that Branch Funds Balance\n \nIf none of the above conditions applies, the ErrorCode XA07 is returned.' B='Sender BIC of the message\n\n **Validation Rule(s)** One of the following must be true:\n- The BIC is an LSP of the SenderBic and the SenderBic manages the liquidity of the BIC\n- The BIC must belong to a Branch Funds Balance and the SenderBic is the Owner of that Branch Funds Balance\n\nIf none of the above conditions applies, the ErrorCode XA07 is returned.'

#### `Criteria4`
- `/properties/messageType/description:` A='Identification of the message sent by Participant\n\n **Validation Rule(s)** Possible values are:\n• Outbound LTO (camt.050)\n• Funding/Defunding LTO (camt.050)\n• Receipt (camt.025)\n• Get Account (camt.003)\n• Return Account (camt.004)\n• Payment Status Query (camt.005) \n• Payment Status Query Response (camt.006)\n(schema validation)' B='Identification of the message sent by Participant\n\n **Validation Rule(s)** Possible values are:\n• Outbound LTO (camt.050)\n• Funding/Defunding LTO (camt.050)\n• Receipt (camt.025)\n• Get Account (camt.003)\n• Return Account (camt.004)\n• Payment Status Query (camt.005)\n• Payment Status Query Response (camt.006)\n(schema validation)'

#### `Criteria8`
- `/properties/beneficiaryAcc:` A=None B='only_in_b'
- `/properties/beneficiaryBic:` A=None B='only_in_b'
- `/properties/beneficiaryName:` A=None B='only_in_b'
- `/properties/operationType:` A=None B='only_in_b'
- `/properties/participantBic/description:` A='The Participant Bic' B='The Participant Bic\n\n **Validation Rule(s)** Must be equal to the BIC of the senderBic (ErrorCodeXA02)'
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

- _(truncated 267 more changed schemas)_