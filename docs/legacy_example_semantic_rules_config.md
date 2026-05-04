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

Le categorie devono esistere anche nel file seed values. Le principali sono:

`bic`, `bic8`, `bic11`, `iban`, `account`, `dca`, `currency`, `country`, `email`, `url`, `uuid`, `date`, `datetime`, `time`, `period`, `amount`, `integer`, `number`, `boolean`, `description`, `reference`, `request_id`, `message_id`, `transaction_id`, `instruction_id`, `operation_id`, `identifier`, `user_id`, `status`, `type`, `network`, `product`, `cycle`, `offset`, `sequence`, `xml`, `aos`, `flag`, `profile`, `role`, `service`, `module`, `channel`, `duration`, `lac`, `sign`, `direction`, `settlement_method`, `csm`, `pointer`, `field_name`, `field_value`, `validation_detail`, `network_address`, `count`, `routing_table`, `operation`, `reason`, `endpoint`, `file_size`, `certificate`, `code`, `error_code`, `name`, `generic`.

Se usi una categoria non riconosciuta, il converter la ignora e scrive un warning nel log.

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
