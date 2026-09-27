# Sestaví studijní materiál daného okruhu pomocí LuaLaTeX + latexmk.
# Aux/tmp soubory -> tmp/, výsledné PDF -> out/, src/ zůstává čistý.
#
# Použití:
#   .\build.ps1 <cesta-k-okruhu>        # např. .\build.ps1 03_specializace_ui_su/S3_strojove_uceni
#   .\build.ps1 <cesta> clean           # smaže tmp/ a out/
#   .\build.ps1 all                     # sestaví všechny okruhy, které mají src/main.tex

param(
    [Parameter(Position=0)][string]$Target = "",
    [Parameter(Position=1)][string]$Action = ""
)

$Root = $PSScriptRoot
# Append na existující TEXINPUTS (kdyby měl uživatel vlastní), oddělovač ';' na Windows.
$env:TEXINPUTS = "$Root\common_latex\;$env:TEXINPUTS"

function Build-One {
    param([string]$Dir)
    if (-not (Test-Path "$Dir\src\main.tex")) {
        Write-Host "  preskakuji $Dir (chybí src/main.tex)"
        return
    }
    Write-Host ">> sestavuji: $Dir"
    Push-Location $Dir
    try {
        latexmk -lualatex -interaction=nonstopmode -file-line-error -outdir=out -auxdir=tmp src/main.tex
        if ($LASTEXITCODE -ne 0) { throw "latexmk selhal (exit $LASTEXITCODE)" }
        Write-Host "   hotovo: $Dir\out\main.pdf"
    } finally {
        Pop-Location
    }
}

function Clean-One {
    param([string]$Dir)
    Push-Location $Dir
    try {
        # Nativní příkazy v PS nehází výjimky, jen nastaví $LASTEXITCODE — selhání ignorujeme.
        latexmk -outdir=out -auxdir=tmp -C src/main.tex 2>$null
    } finally {
        Pop-Location
    }
    if (Test-Path "$Dir\tmp") { Remove-Item "$Dir\tmp\*" -Recurse -Force -ErrorAction SilentlyContinue }
    Write-Host "   vyčištěno: $Dir"
}

if ($Target -eq "all") {
    Get-ChildItem -Path $Root -Recurse -Filter "main.tex" | Where-Object { $_.DirectoryName -match "\\src$" } | ForEach-Object {
        $okruhDir = Split-Path (Split-Path $_.FullName -Parent) -Parent
        Build-One $okruhDir
    }
    exit 0
}

if (-not $Target) {
    Write-Error "Použití: .\build.ps1 <cesta-k-okruhu> [clean] | .\build.ps1 all"
    exit 1
}

$FullTarget = if ([System.IO.Path]::IsPathRooted($Target)) { $Target } else { Join-Path $Root $Target }

if ($Action -eq "clean") {
    Clean-One $FullTarget
} else {
    Build-One $FullTarget
}
