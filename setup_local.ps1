param([string]$Root = "$PSScriptRoot")
$ErrorActionPreference = 'Stop'
Write-Host "Verificando Python y FFmpeg..."
python --version
ffmpeg -version | Select-Object -First 1
python -m pip install numpy Pillow
New-Item -ItemType Directory -Force -Path "$Root\assets\referencias","$Root\assets\combinados","$Root\assets\jingles_originales","$Root\trabajo_AR2" | Out-Null
Write-Host "Estructura local preparada. Copia config.example.json como config.json y ajusta sus rutas."
