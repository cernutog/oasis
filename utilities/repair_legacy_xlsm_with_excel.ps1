param(
    [Parameter(Mandatory = $true)]
    [string]$LegacyDir,
    [string]$FileName = "*"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $LegacyDir -PathType Container)) {
    throw "Legacy directory not found: $LegacyDir"
}

$files = Get-ChildItem -LiteralPath $LegacyDir -Filter *.xlsm | Where-Object { $_.Name -like $FileName } | Sort-Object Name
if (-not $files) {
    Write-Output "REPAIRED_TOTAL=0"
    Write-Output "FAILED_TOTAL=0"
    exit 0
}

$xlNormalLoad = 0
$xlRepairFile = 1
$repaired = 0
$failed = 0
$excel = $null

function Invoke-ComMethod {
    param(
        [Parameter(Mandatory = $true)] $ComObject,
        [Parameter(Mandatory = $true)] [string]$MethodName,
        [object[]]$Arguments = @()
    )

    return $ComObject.GetType().InvokeMember(
        $MethodName,
        [System.Reflection.BindingFlags]::InvokeMethod,
        $null,
        $ComObject,
        $Arguments
    )
}

try {
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false
    $excel.AskToUpdateLinks = $false
    $excel.EnableEvents = $false
    $excel.AutomationSecurity = 3

    foreach ($file in $files) {
        $workbook = $null
        try {
            $tempRepaired = Join-Path $file.DirectoryName ($file.BaseName + ".excel-repaired" + $file.Extension)
            $preExcelBackup = $file.FullName + ".pre-excel-repair"
            if (Test-Path -LiteralPath $tempRepaired) {
                Remove-Item -LiteralPath $tempRepaired -Force
            }

            $workbook = Invoke-ComMethod -ComObject $excel.Workbooks -MethodName "Open" -Arguments @(
                $file.FullName,
                0,
                $false,
                5,
                "",
                "",
                $true,
                1,
                "",
                $false,
                $false,
                0,
                $false,
                $true,
                $xlRepairFile
            )

            Invoke-ComMethod -ComObject $workbook -MethodName "SaveCopyAs" -Arguments @(
                $tempRepaired
            ) | Out-Null
            Invoke-ComMethod -ComObject $workbook -MethodName "Close" -Arguments @($false) | Out-Null
            $workbook = $null

            if (-not (Test-Path -LiteralPath $preExcelBackup)) {
                Copy-Item -LiteralPath $file.FullName -Destination $preExcelBackup
            }
            Move-Item -LiteralPath $tempRepaired -Destination $file.FullName -Force
            Write-Output ("REPAIRED|{0}" -f $file.Name)
            $repaired += 1
        } catch {
            if ($workbook -ne $null) {
                try { Invoke-ComMethod -ComObject $workbook -MethodName "Close" -Arguments @($false) | Out-Null } catch {}
            }
            Write-Output ("FAILED|{0}|{1}" -f $file.Name, $_.Exception.Message)
            $failed += 1
        }
    }
}
finally {
    if ($excel -ne $null) {
        try { $excel.Quit() | Out-Null } catch {}
    }
}

Write-Output ("REPAIRED_TOTAL={0}" -f $repaired)
Write-Output ("FAILED_TOTAL={0}" -f $failed)

if ($failed -gt 0) {
    exit 1
}
