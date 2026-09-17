param(
  [string]$Video = ""
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Trabajo = Join-Path $Root "trabajo_AR2"
$Config = Join-Path $Root "config.json"

if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw "Python no está instalado o no está en PATH." }
if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) { throw "FFmpeg no está instalado o no está en PATH." }
if (-not (Test-Path $Config)) {
  Copy-Item (Join-Path $Root "config.example.json") $Config
  Write-Host "Se creó config.json. Ajusta las rutas y vuelve a ejecutar este script." -ForegroundColor Yellow
  exit 0
}

if ($Video -ne "") { $env:EDITOR_VIDEO = $Video }
New-Item -ItemType Directory -Force -Path $Trabajo | Out-Null
Write-Host "Analizando plecas..." -ForegroundColor Cyan
python (Join-Path $Root "analizar_vision.py")
Write-Host "Ensamblando animaciones, jingles y audio nivelado..." -ForegroundColor Cyan
python (Join-Path $Root "ensamblar_programa.py")
Write-Host "Listo. Importa trabajo_AR2\programa_final_nivelado.mp4 en DaVinci Resolve." -ForegroundColor Green
