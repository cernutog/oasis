# API Designer - Manuale sintetico

Questo manuale descrive il comportamento attuale del `Designer` nella **Milestone 1**.

L'obiettivo di questa versione non e' offrire tutta l'esperienza finale, ma mettere a disposizione una base stabile per:

- aprire il tab `Designer`
- creare un workspace iniziale
- aprire un workspace esistente
- salvare il modello su file
- navigare la struttura del workspace e del primo `ApiModel`

## 1. Dove si trova

All'avvio di OASIS il `Designer` e' il primo tab della finestra principale.

Puoi raggiungerlo in due modi:

- tab `Designer`
- menu `View > Designer`

## 2. Com'e' fatto il layout

Il `Designer` ha tre aree principali.

### Sinistra: Workspace

Mostra il contenitore di alto livello:

- workspace corrente
- elenco API
- shared libraries
- releases
- changes

In questa milestone le sezioni `Shared Libraries`, `Releases` e `Changes` sono soprattutto strutturali: servono a fissare il perimetro del modello, non a gestire gia' workflow completi.

### Centro: Model

Mostra la struttura del modello dell'API selezionata:

- API
- paths
- operations
- local components
- shared component refs

Questa area e' pensata per diventare il punto centrale di editing del modello. Nella Milestone 1 e' soprattutto una vista di navigazione, ma espone gia' in modo piu' leggibile i `path` e le `operation`.

### Destra: Inspector

Mostra i dettagli dell'elemento selezionato.

L'inspector e' contestuale:

- dichiara se la selezione attiva arriva da `Explorer` o da `Model`
- cambia campi in base al tipo di oggetto cliccato
- mantiene una sola sorgente attiva alla volta, per ridurre ambiguita'

Campi disponibili oggi:

- `Source`
- `Type`
- `ID`
- campi principali che cambiano in base al nodo selezionato
- area `Details` in sola lettura

## 3. Toolbar

In alto sono disponibili quattro azioni:

- `New`
- `Open`
- `Save`
- `Save As`

Accanto compare il percorso del workspace corrente.

Se vedi un asterisco `*`, significa che ci sono modifiche non ancora salvate.

## 4. Flusso consigliato per iniziare

### Creare un nuovo workspace

1. Apri il tab `Designer`.
2. Premi `New`.
3. Inserisci il nome del workspace.
4. OASIS crea un workspace iniziale con una prima API chiamata `New API`.
5. Premi `Save As` per scegliere dove salvarlo.

### Aprire un workspace esistente

1. Premi `Open`.
2. Seleziona il file `workspace.yaml` del workspace.
3. Il Designer carica manifesto, API, metadata catalog e strutture collegate.

### Salvare

- `Save` salva nel workspace gia' associato.
- `Save As` crea o usa una cartella di workspace e poi salva li' il modello.

Se il nome della cartella scelta non coincide con il nome del workspace, OASIS crea una sottocartella con nome normalizzato del workspace.

## 5. Cosa si puo' modificare oggi

### Workspace

Se selezioni il nodo root del workspace puoi modificare:

- `Name`
- `Description`

Poi premi `Apply`.

### API

Se selezioni una API nel pannello `Workspace` o `Model` puoi modificare:

- `Name`
- `Version`
- `Title`

Poi premi `Apply`.

Quando aggiorni l'API, OASIS allinea anche:

- `display_label`
- `info.version`

Se inserisci `Title`, viene aggiornato `info.title`.

### Path

Se selezioni un `path` nel pannello `Model` puoi modificare:

- `Path`
- `Summary`
- `Description`

### Operation

Se selezioni una `operation` nel pannello `Model` puoi modificare:

- `Operation ID`
- `Method`
- `Path`
- `Description`

## 6. Dove vengono salvati i dati

La persistenza e' file-based, testuale e versionabile.

Struttura iniziale del package:

```text
<workspace-folder>/
  workspace.yaml
  apis/
    <api-id>.yaml
  libraries/
  metadata/
    catalog.yaml
  revisions/
```

### Significato dei file

- `workspace.yaml`: manifesto del workspace
- `apis/<api-id>.yaml`: dettaglio di ciascuna API
- `metadata/catalog.yaml`: catalogo metadati del workspace
- `libraries/`: spazio riservato alle shared libraries future
- `revisions/`: spazio riservato alle revisioni future

## 7. Cosa contiene il modello

Il modello introdotto in questa milestone include gia' le fondamenta per:

- `DesignWorkspace`
- `ApiModel`
- `PathItemModel`
- `OperationModel`
- `ReleaseDefinition`
- `Change`
- `ChangeStep`
- `ChangePhase`
- `ReleaseSnapshot`
- custom metadata
- custom extensions `x-*`

Non tutta questa struttura e' gia' esposta in modo editabile nella UI, ma e' presente nel dominio e nella persistenza per evitare scelte da rifare piu' avanti.

## 8. Cosa non fa ancora

In questa milestone il Designer **non** gestisce ancora:

- drag and drop
- editing completo di path e operation
- callback editing
- gestione completa di releases e planning
- chatbot
- repository/server centrale
- import OAS nel modello
- projection `API Model -> OAS`
- modalita' `API Model` nel tab `Generation`

Il tab `Generation` continua quindi a lavorare come prima sul flusso template-driven.

## 9. Limiti pratici da conoscere

- L'inspector e' editabile solo per workspace e API.
- L'inspector e' editabile per workspace, API, path, operation, release, change e library/component di base.
- Le aree `Shared Libraries`, `Releases` e `Changes` sono oggi preparatorie.
- Il centro non e' ancora un editor grafico completo: e' una vista strutturale.
- Se apri un file YAML diverso da `workspace.yaml`, il Designer lo rifiuta.

## 10. Lettura veloce dello stato attuale

Se vuoi capire "a colpo d'occhio" cosa puoi fare oggi, la sintesi e' questa:

- puoi creare un workspace
- puoi salvarlo come package YAML
- puoi riaprirlo
- puoi rinominare workspace e API
- puoi navigare la struttura base del modello

Tutto il resto e' predisposto come fondazione architetturale, ma non ancora esposto come workflow completo.
