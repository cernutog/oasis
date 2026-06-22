# Legacy Example Semantic Classification

Questo documento descrive la classificazione semantica usata dal Legacy Template Converter per la funzione **Repair and complete examples**.

Per l'uso operativo del file di configurazione, vedi `docs/legacy_example_semantic_rules_config.md`.

La classificazione serve a scegliere esempi verosimili quando i template legacy hanno esempi mancanti, incompleti o non coerenti con i vincoli. La logica non modifica la generazione OAS direttamente: agisce sui nuovi template convertiti, una volta consolidati gli schemi.

## Obiettivo

Per ogni campo foglia di uno schema, il converter tenta di:

1. conservare gli esempi gia validi;
2. correggere gli esempi esistenti che non rispettano type, pattern, allowed values o limiti;
3. completare gli esempi mancanti fino a tre valori, quando possibile;
4. usare esempi coerenti con la semantica del campo;
5. lasciare il campo su `generic` quando la semantica non e abbastanza affidabile.

La classificazione e deterministica: dato lo stesso template, la stessa configurazione seed e le stesse regole semantiche, produce sempre la stessa categoria.

## Input Usati

La categoria e derivata da questi metadati del `DataType`:

| Sorgente | Uso |
| --- | --- |
| `name` | Segnale principale per categorie note, acronimi, suffissi e abbreviazioni legacy. |
| `description` | Segnale aggiuntivo quando presente. Molti template legacy non la valorizzano. |
| `pattern_eba` / `regex` | Usati per riconoscere vincoli noti, come BIC8/BIC11, date/time e pattern numerici. |
| `format` | Usato per `email`, `url`/`uri`, `uuid`, `date`, `date-time`. |
| `allowed_values` | Ha priorita sugli esempi semanticamente generati. Se e binario, aiuta a classificare come `flag`. |
| `example` | Non decide direttamente la categoria, ma aiuta a verificare o riparare i valori. |
| frequenza e contesto dei template | Usati durante l'analisi manuale per decidere nuove regole, non a runtime. |

## Ordine Decisionale

La logica e implementata in `LegacyConverter._classify_example_category`.

L'ordine e importante:

1. override espliciti dal file `legacy_example_semantic_rules.yaml`;
2. tipo strutturale (`boolean`, `integer`, `number`);
3. allowed values binari (`0/1`, `Y/N`, `true/false`) come `flag`;
4. identificatori bancari forti (`iban`, `bic`, `dca`, `account`);
5. formati standard (`email`, `url`, `uuid`, `date`, `datetime`, `time`);
6. regole configurabili dal file `legacy_example_semantic_rules.yaml`;
7. categorie tecniche o di dominio da nome compatto;
8. categorie legacy ricorrenti emerse dalla scansione dei template;
9. `generic` come fallback.

Gli `allowed_values` restano comunque il primo bacino di esempi: se sono presenti, vengono usati prima dei seed semantici.

## Categorie

| Categoria | Segnali principali | Esempi campo reali |
| --- | --- | --- |
| `bic8` | nome `BIC8`, pattern BIC da 8 caratteri | `BIC8`, `Bic8` |
| `bic11` | nome `BIC11`, `BIC11Only`, pattern BIC da 11 caratteri | `BIC11`, `Bic11Only` |
| `bic` | nome o pattern BIC senza lunghezza certa | `SenderBIC`, `TechnicalBic` |
| `iban` | `iban` nel nome o testo | `IBAN` |
| `account` | `account` nel nome, esclusi DCA specifici | `Account`, `BeneficiaryAccount` |
| `dca` | `dca`, `DedicatedCashAccount` | `DCAnumber`, `DedicatedCashAccount` |
| `currency` | `currency`, `ccy` | `Currency`, `SubmittedCurrencies` quando riconoscibile |
| `country` | `country`, `countrycode` | `CountryCode` |
| `email` | `format=email` o nome email | `Email` |
| `url` | `url`, `uri`, `format=url/uri` | `CallbackUrl` |
| `endpoint` | suffisso `Endpoint`, `ApiEndpoint` | `PryApiEndpoint`, `ScyApiEndpoint` |
| `uuid` | `uuid`, `format=uuid`, `UETR` | `UETR`, `Uetr` |
| `date` | `format=date`, `YYYY-MM-DD`, suffisso `Dt`/`Date` | `BusinessDate`, `EffectiveDate` |
| `datetime` | `format=date-time`, `YYYY-MM-DDTHH`, suffisso `DtTm` | `DateTime`, `AccptncDtTm` |
| `time` | `format=time`, nome time | `TimeFrom`, `TimeTo`, `StartTimeHighVolume` |
| `period` | `period`, `quarter`, `year`, `month`, `day` | `Year`, `Month`, `Day` |
| `amount` | type number con parole amount/balance/fee/total, o nome amount | `Amount`, `LacAmount`, `OrigTransAmount` |
| `integer` | type integer | `StandardInteger` |
| `number` | type number senza semantica piu specifica | `MaxRvqFileSize` se numerico |
| `count` | prefissi `Num`, `TotNum`, suffisso `Count` | `TotNumOfMsgRcv`, `NumC029RcvAccr` |
| `boolean` | type boolean | `GenericBoolean` |
| `flag` | allowed binari o nomi indicator/flag/req/rqst | `LSP`, `FlowIndicator`, `EndOfList` |
| `status` | `status`, `state`, suffisso `Sts`, `MsgSts` | `FileStatus`, `CommandStatus`, `XmlMsgSts` |
| `type` | `type` o suffisso `Tp` | `FileType`, `MessageType`, `BulkType2` |
| `direction` | `SentReceived`, `TrxDirection`, `direction` | `SentReceived`, `TrxDirection` |
| `reference` | `reference`, suffisso `Ref`, abbreviazione `Rfrnc` | `FileReference`, `CmndRfrnc` |
| `request_id` | `RequestId` | `RequestId` |
| `message_id` | `MessageId`, `MsgId` | `MessageId` |
| `transaction_id` | `TransactionId`, `EndToEndId`, `TxId` | `TransactionId`, `EndToEndId` |
| `instruction_id` | `InstructionId` | `InstructionId` |
| `operation_id` | `OperationId` | `OperationId` |
| `identifier` | suffisso `Id`, `Identifier` | `ModuleIdentifier`, `PoolId` |
| `user_id` | `UserId`, `User`, user issuer/supervisor | `UserId`, `UserIssr`, `UserSprvr` |
| `code` | `code` non gia classificato come error code | `ReasonCode` quando non piu specifico |
| `error_code` | `ErrorCode`, `error code` | `ErrorCode`, `BusinessError` quando riconoscibile |
| `reason` | `reason`, abbreviazione `Rsn` | `XmlStsRsn`, `R2pRsnCd` |
| `description` | `description` | `ErrorCodeDescription`, `EventDescription` |
| `validation_detail` | `ErrorDetails` | `ErrorDetails` |
| `field_name` | `Field`, `FieldName` | `Field` |
| `field_value` | `Value`, `FieldValue` | `Value` |
| `name` | `name` o suffisso `Name` | `ParticipantName`, `BeneficiaryName` |
| `filename` | `filename`, `file name` | `NetworkFileName` |
| `file_size` | `FileSize` | `MaxFileSize` |
| `xml` | `OriginalXml`, suffisso `Xml`, suffisso `Data` | `OriginalXml`, `ReportData` |
| `network` | `network`, `NetwOpt`, `OutputNet` | `Network`, `ActiveOutputNetwork` |
| `network_address` | suffisso `NetAd` | `SecRcvgNetAd`, `SecSndgNetAd` |
| `channel` | `channel`, `RequestedThrough` | `RequestedThrough` |
| `product` | `product` | `ProductId`, `DebitProduct` |
| `service` | `service` | `Service` |
| `module` | `module` | `ModuleIdentifier` se non gia ID |
| `cycle` | `cycle` | `Cycle`, `CyclesArray` |
| `offset` | nome `Offset` | `Offset` |
| `sequence` | `sequence` | `Sequence` |
| `aos` | `aos`, nome `AO` | `AOSList`, `AOSParam`, `AO` |
| `profile` | `profile` | `AdmissionProfile` |
| `role` | `role`, `Requestor`, `Authorizer`, `Confirmer` | `Requestor`, `Authorizer` |
| `lac` | `lac` | `Lac`, `LacNumber` |
| `sign` | nome `Sign` | `Sign` |
| `settlement_method` | `SettMethod`, `SettlementMethod` | `CredSettMethod`, `DebSettMethod` |
| `csm` | nome `Csm` | `Csm` |
| `pointer` | nome `Pointer` | `Pointer` |
| `routing_table` | `RoutingTable` | `RoutingTable` |
| `operation` | `Operation`, `FreezeUnfreeze` | `FreezeUnfreeze`, `DPRBOperation` |
| `duration` | `duration` | `DurationOfUnavailability` |
| `certificate` | `AuthenticationCA` | `ParticipantAuthenticationCA` |
| `generic` | nessun segnale affidabile | `Instruction`, `Criteria`, `String8` |

## Esempi Seed

I seed predefiniti sono definiti in `DEFAULT_LEGACY_EXAMPLE_SEED_VALUES`.

Quando il converter viene eseguito con `Repair and complete examples`, i seed vengono copiati o aggiornati nel file configurabile:

`%APPDATA%\OASIS\legacy_example_seed_values.yaml`

Quel file consente di cambiare i valori senza modificare il codice. Se il file esiste gia, il converter conserva le personalizzazioni e aggiunge solo le categorie mancanti. I vecchi default generati automaticamente vengono aggiornati quando riconosciuti esattamente.

## Regole Configurabili

Le regole di classificazione vengono copiate automaticamente nel file:

`%APPDATA%\OASIS\legacy_example_semantic_rules.yaml`

Questo file consente di aggiungere override, nuove regole e esclusioni senza modificare il codice. Il manuale operativo e in `docs/legacy_example_semantic_rules_config.md`.

## Vincoli e Priorita

La categoria semantica propone candidati, ma non e una validazione alternativa. La validazione resta sempre basata sui constraint Excel.

La generazione degli esempi segue questa priorita:

1. `allowed_values`, se presenti;
2. esempi esistenti e validi;
3. candidati della categoria semantica;
4. generazione da regex semplice, se possibile;
5. seed `generic`, se compatibili;
6. best-effort fallback tracciato, oppure `IMPOSSIBLE` / `TOO COMPLEX`.

Ogni candidato viene validato contro:

- allowed values;
- pattern EBA / regex;
- type;
- min/max numerici;
- min/max length stringa.

Gli esempi gia presenti nel template Excel vengono conservati se rispettano i constraint e non matchano un placeholder semantico configurato per la categoria. Non vengono scartati solo perche non corrispondono ai seed della categoria semantica.

I placeholder semantici sono configurati in `legacy_example_semantic_rules.yaml`, sezione `placeholder_patterns`. Servono per casi in cui un valore e formalmente valido per la regex ma non e un esempio verosimile, per esempio `AAAAAAAA` per una categoria BIC. Gli `allowed_values` espliciti restano prevalenti e non vengono scartati da questo filtro.

Quando l'esempio Excel manca o non e valido, la categoria semantica viene usata prima della generazione da regex. Questo evita esempi formalmente validi ma poco realistici, per esempio un orario `99:99` prodotto da una regex troppo ampia. La regex resta comunque il filtro finale: se un campo ammette solo `HH:MM`, i candidati `HH:MM:SS` vengono esclusi.

Le categorie ammesse sono quelle presenti nei seed caricati da `%APPDATA%\OASIS\legacy_example_seed_values.yaml`. Aggiungere una nuova categoria in quel file e poi referenziarla in `legacy_example_semantic_rules.yaml` non richiede modifiche al codice.

## Casi Generic Voluti

Alcuni campi restano `generic` per scelta. Questo evita di inventare semantiche non dimostrate dai template.

Esempi osservati:

| Campo | Motivo |
| --- | --- |
| `Instruction` | Troppo generico: puo essere payload, categoria, testo o riferimento a seconda del contesto. |
| `Criteria` | Troppo generico e spesso privo di pattern/esempi. |
| `String8` | Nome tecnico, semantica assente. |
| `IdOfUnavailableParty` | Il nome suggerisce un identificativo, ma gli esempi sono free text. |
| `TAW*` | Segnali temporali non abbastanza stabili per una categoria dedicata. |

## Risultato della Scansione

La classificazione e stata tarata sui template legacy sotto:

`C:\EBA Clearing\APIs\Templates`

Ultima scansione eseguita:

| Misura | Valore |
| --- | ---: |
| Workbook legacy analizzati | 364 |
| Righe `Data Type` lette | 13.335 |
| Campi foglia analizzati | 12.488 |
| Campi foglia rimasti `generic` | 45 |

Il residuo `generic` e intenzionale: contiene campi senza segnale semantico affidabile o con contesto troppo ambiguo.

## Manutenzione

Quando emergono nuovi template:

1. rieseguire la scansione sui campi classificati come `generic`;
2. promuovere una nuova categoria solo se il segnale e stabile su piu template o chiaramente deducibile dai vincoli;
3. aggiungere seed deterministici nel file configurabile;
4. aggiungere un test di regressione per almeno un campo reale;
5. evitare categorie basate solo su intuizioni linguistiche deboli.

In caso di dubbio, preferire `generic` a una classificazione fuorviante.
