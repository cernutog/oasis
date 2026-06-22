# Legacy Example Semantic Rules Config

Questo manuale spiega come usare il file di configurazione delle regole semantiche usate da **Repair and complete examples** nel Legacy Template Converter e nell'Example Tracer.

Il file permette di correggere una classificazione errata, aggiungere una nuova regola per un acronimo o impedire che una regola troppo generica venga applicata a un campo specifico, senza modificare il codice.

## Dove si trova

Il converter crea automaticamente il file qui:

`%APPDATA%\OASIS\legacy_example_semantic_rules.yaml`

Nello stesso percorso si trova anche:

`%APPDATA%\OASIS\legacy_example_seed_values.yaml`

I due file lavorano insieme:

- `legacy_example_semantic_rules.yaml` decide la categoria semantica di un campo, per esempio `bic8`, `filename`, `status`, `service`;
- `legacy_example_seed_values.yaml` contiene gli esempi stabili da usare per ogni categoria.

## Quando modificarlo

Modifica questo file quando:

- un campo viene classificato nella categoria sbagliata;
- un acronimo ricorrente non viene riconosciuto;
- un campo resta `generic`, ma il significato e stabile e dimostrabile;
- una regola generale intercetta un campo che deve restare in un'altra categoria.

Non modificarlo per cambiare i valori degli esempi: in quel caso usa `legacy_example_seed_values.yaml`.

## Struttura

Il file ha tre sezioni principali:

```yaml
overrides:
  exact: {}
  compact_exact: {}

exclusions:
  filename:
    exact:
      - FileStatus
      - FileReference

rules:
  - category: request_id
    compact_contains:
      - requestid
```

## Ordine di priorita

La classificazione segue questo ordine:

1. `overrides`, se presenti;
2. tipo strutturale e vincoli forti, per esempio `boolean`, `integer`, `number`, BIC, IBAN, date, URL;
3. `rules` del file di configurazione;
4. regole built-in residue nel codice, mantenute come fallback;
5. `generic`.

Gli `overrides` sono intenzionalmente molto forti: servono a correggere casi specifici.

## Overrides

Usa `overrides.exact` quando vuoi forzare un nome campo preciso.

```yaml
overrides:
  exact:
    Instruction: instruction_id
    LSP: service
```

Usa `overrides.compact_exact` quando vuoi ignorare maiuscole, spazi, underscore e separatori.

```yaml
overrides:
  compact_exact:
    access_point: channel
    AccessPoint: channel
```

Entrambe le chiavi sopra vengono lette come `accesspoint`.

Puoi anche forzare `generic` se una regola automatica e fuorviante:

```yaml
overrides:
  exact:
    Criteria: generic
```

## Rules

Le regole sono valutate dall'alto verso il basso. La prima che trova un match decide la categoria.

Ogni regola deve avere:

```yaml
- category: nome_categoria
```

Poi puo avere uno o piu matcher.

### Matcher disponibili

| Matcher | Cosa controlla | Esempio |
| --- | --- | --- |
| `exact` | nome campo normalizzato in minuscolo | `FileStatus` |
| `compact_exact` | nome campo senza spazi, underscore e simboli | `filestatus` |
| `contains` | testo completo: nome, descrizione, pattern, regex, format | `description` |
| `compact_contains` | nome compatto | `requestid` |
| `prefix` | prefisso del nome in minuscolo | `total` |
| `suffix` | suffisso del nome in minuscolo | `reference` |
| `compact_prefix` | prefisso del nome compatto | `totnum` |
| `compact_suffix` | suffisso del nome compatto | `sts` |
| `format` | format OAS/legacy | `date-time` |
| `type` | tipo base | `integer` |
| `allowed_values_subset` | tutti gli allowed values stanno nella lista | `Y`, `N` |
| `allowed_values_any` | almeno un allowed value sta nella lista | `SNT`, `RCV` |
| `compact_regex` | regex applicata al nome compatto | `.*time$` |

Esempio:

```yaml
rules:
  - category: service
    compact_exact:
      - lsp

  - category: status
    compact_suffix:
      - sts
    contains:
      - status

  - category: flag
    allowed_values_subset:
      - "0"
      - "1"
      - "Y"
      - "N"
```

Una regola fa match se almeno uno dei matcher corrisponde.

## Exclusions

Usa `exclusions` quando una categoria e corretta in generale, ma deve ignorare alcuni campi.

Esempio: `FileName` deve essere `filename`, ma `FileStatus` e `FileReference` no.

```yaml
exclusions:
  filename:
    exact:
      - FileStatus
      - FileReference
```

Le esclusioni usano gli stessi matcher delle regole.

## Categorie ammesse

Le categorie devono esistere nel file seed values. Sono ammesse sia le categorie predefinite sia le categorie aggiunte dall'utente in:

`%APPDATA%\OASIS\legacy_example_seed_values.yaml`

Le principali categorie predefinite sono:

`bic`, `bic8`, `bic11`, `iban`, `account`, `dca`, `currency`, `country`, `email`, `url`, `uuid`, `date`, `datetime`, `time`, `period`, `amount`, `integer`, `number`, `boolean`, `description`, `reference`, `request_id`, `message_id`, `transaction_id`, `instruction_id`, `operation_id`, `identifier`, `user_id`, `status`, `type`, `network`, `product`, `cycle`, `offset`, `sequence`, `xml`, `aos`, `flag`, `profile`, `role`, `service`, `module`, `channel`, `duration`, `lac`, `sign`, `direction`, `settlement_method`, `csm`, `pointer`, `field_name`, `field_value`, `validation_detail`, `network_address`, `count`, `routing_table`, `operation`, `reason`, `endpoint`, `file_size`, `certificate`, `code`, `error_code`, `name`, `generic`.

Se usi una categoria che non esiste nei seed, il converter la ignora e scrive un warning nel log.

## Nuove Categorie

Per creare una nuova categoria semantica, aggiungila prima nel file seed values:

```yaml
clearing_system:
  - STEP2
  - RT1
  - TIPS
```

Poi usa la categoria nel file delle regole:

```yaml
rules:
  - category: clearing_system
    compact_exact:
      - clrgsys
```

La categoria diventa valida perche esiste nei seed caricati. Non serve modificare il codice.

I valori nei seed sono candidati: il converter li usa solo se rispettano i constraint Excel del campo, come type, allowed values, regex, Pattern EBA e min/max.

## Priorita nella Generazione degli Esempi

Le regole semantiche classificano il campo, ma non validano i valori. La validazione resta sempre basata sui constraint Excel.

La generazione segue questa priorita:

1. `allowed_values`, se presenti;
2. esempi Excel esistenti e validi;
3. candidati della categoria semantica;
4. candidati generati da regex/pattern semplice;
5. seed `generic`, se compatibili;
6. best-effort tracciato, oppure `IMPOSSIBLE` / `TOO COMPLEX`.

Per esempio, un campo `TimeIndicator` con regex `[0-9]{2,2}:[0-9]{2,2}` usa prima i candidati della categoria `time`, come `10:15`, `12:00`, `23:59`. La regex resta il filtro finale e impedisce di usare candidati con formato diverso.

## Placeholder semantici

Alcuni esempi presenti nei template legacy possono rispettare formalmente i constraint Excel ma essere comunque placeholder non significativi per una categoria semantica nota. Per esempio `AAAAAAAA` rispetta una regex BIC8 generica, ma non e un BIC verosimile.

Questi casi vanno configurati in `placeholder_patterns`. I pattern sono espressioni regolari Python applicate al valore intero dell'esempio gia letto da Excel. Se un esempio matcha uno di questi pattern, viene trattato come non valido e riparato.

```yaml
placeholder_patterns:
  categories:
    bic:
      - '^([A-Z0-9])\1+$'
    bic8:
      - '^([A-Z0-9])\1+$'
    bic11:
      - '^([A-Z0-9])\1+$'
```

Il filtro e applicato solo dopo i constraint Excel. Gli `allowed_values` espliciti restano la fonte piu forte: se il template dichiara allowed values, il converter non li scarta come placeholder semantici.

Un esempio Excel valido e non-placeholder viene conservato. Per esempio `TimeIndicator = 16:00` con regex `[0-9]{2,2}:[0-9]{2,2}` resta il primo esempio, anche se la categoria `time` dispone di seed diversi.

## Azioni dell'Example Tracer

La colonna `ACTION` indica il tipo di intervento effettuato:

- `KEPT`: gli esempi Excel erano validi e sono rimasti invariati.
- `COMPLETED`: il campo non aveva esempi, oppure aveva esempi validi ma incompleti e il converter ne ha aggiunti altri.
- `REPAIRED`: almeno un esempio Excel era presente ma non rispettava i constraint, quindi e stato corretto, sostituito o rimosso.
- `BEST EFFORT`: e stato possibile produrre solo un esempio di fallback.
- `IMPOSSIBLE`: i constraint sono internamente incompatibili.
- `TOO COMPLEX`: i constraint sono troppo complessi per la generazione automatica.

La colonna `REASON` deve spiegare la causa reale dell'intervento. Per esempio:

- `completed missing examples from allowed values`
- `completed missing examples from semantic category: time`
- `completed missing examples from regex alternatives`
- `repaired invalid example: regex mismatch`
- `repaired invalid example: semantic placeholder`
- `repaired invalid example: minLength not met`
- `repaired invalid example: maxLength exceeded`
- `repaired invalid example: type mismatch`

## Esempi pratici

### Classificare un acronimo come service

```yaml
overrides:
  exact:
    LSP: service
```

### Riconoscere tutti i campi che finiscono con NetAd

```yaml
rules:
  - category: network_address
    compact_suffix:
      - netad
```

### Impedire che un campo sia trattato come filename

```yaml
exclusions:
  filename:
    exact:
      - FileReference
```

### Forzare un campo ambiguo a generic

```yaml
overrides:
  exact:
    Instruction: generic
```

## Buone pratiche

- Preferisci `overrides.exact` per correzioni puntuali.
- Usa `rules` solo per pattern stabili su piu template.
- Non creare categorie troppo specifiche se il nome del campo non prova quella semantica.
- Dopo una modifica, esegui l'Example Tracer con tracing attivo e controlla la colonna `REASON`.
- Se cambi categoria, verifica anche i valori in `legacy_example_seed_values.yaml`.

## Troubleshooting

Se la modifica non ha effetto:

1. controlla che il file sia in `%APPDATA%\OASIS`;
2. verifica che la categoria esista;
3. controlla l'indentazione YAML;
4. cerca warning nel log del converter;
5. ricorda che BIC, IBAN, date, numeri e booleani hanno regole strutturali forti.

Se il converter non riesce a leggere il file, continua con le regole default e scrive un warning nel log.
