# Instalación del editor local

## Descargas seguras

Instala primero estas herramientas desde sus sitios oficiales:

- [Python para Windows](https://www.python.org/downloads/windows/)
- [FFmpeg — página oficial de descargas](https://ffmpeg.org/download.html)
- [DaVinci Resolve Free — Blackmagic Design](https://www.blackmagicdesign.com/products/davinciresolve)
- [Git para Windows](https://git-scm.com/download/win)
- [Gpg4win, opcional para firmar commits](https://gpg4win.org/)

### Instalación desde PowerShell

Abre PowerShell como administrador y verifica que `winget` esté disponible:

```powershell
winget --version
```

Después puedes instalar las herramientas automatizables:

```powershell
winget install --id Python.Python.3.13 --exact --source winget
winget install --id Gyan.FFmpeg.Shared --exact --source winget
winget install --id Git.Git --exact --source winget
winget install --id GnuPG.Gpg4win --exact --source winget
```

Si algún identificador cambia o `winget` no encuentra el paquete, usa los enlaces oficiales de arriba. No descargues instaladores desde páginas no verificadas.

DaVinci Resolve se descarga manualmente desde Blackmagic Design porque el sitio puede solicitar datos, aceptación de licencia y selección de edición Free/Studio. Después de instalarlo, comprueba:

```powershell
Get-Command python, ffmpeg, ffprobe, git -ErrorAction SilentlyContinue
```

### Preparar Python y el proyecto

```powershell
python -m pip install --upgrade pip
python -m pip install numpy Pillow
Set-ExecutionPolicy -Scope Process Bypass
.\setup_local.ps1
```

FFmpeg es un proyecto de código abierto. Su página oficial enlaza a builds para Windows; usa únicamente los enlaces recomendados desde `ffmpeg.org`. GitHub puede contener builds o forks, pero no todos son oficiales.

## Instalación del proyecto

1. Descarga o clona este repositorio.
2. Abre PowerShell en la carpeta del proyecto.
3. Ejecuta:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\setup_local.ps1
```

4. Copia `config.example.json` como `config.json` y ajusta las rutas de tu computadora.
5. Copia el video fuente a la ruta indicada en `config.json`.
6. Coloca las referencias, animaciones y jingles en `assets`.
7. Ejecuta `python analizar_vision.py` y después `python ensamblar_programa.py`.

## GitHub Releases

El repositorio puede distribuir una versión `.zip` o un `.exe` desde la sección **Releases**. El instalador no debe incluir DaVinci Resolve ni FFmpeg sin verificar sus licencias y distribución; debe comprobar si están instalados y dirigir al usuario a sus sitios oficiales.

## Funcionamiento offline

El análisis y el ensamblado se ejecutan localmente. Internet solo es necesario para descargar dependencias, actualizar la plantilla o publicar respaldos en GitHub.
