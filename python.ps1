param([string]$FirstArg)

if ($FirstArg -eq "-c" -or $FirstArg -eq "/-c") {
    Write-Host ""
    Write-Host "==============================================================================" -ForegroundColor Red
    Write-Host "ERRORE CRITICO: L'uso di 'python -c' (inline execution) e' PROIBITO." -ForegroundColor Red
    Write-Host "Protocollo di sicurezza OASIS violato." -ForegroundColor Red
    Write-Host "Per favore, scrivi il codice in un file .py ed esegui quello." -ForegroundColor Red
    Write-Host "==============================================================================" -ForegroundColor Red
    Write-Host ""
    exit 1
}

if (Test-Path ".venv\Scripts\python.exe") {
    & ".venv\Scripts\python.exe" $args
} else {
    & python $args
}
