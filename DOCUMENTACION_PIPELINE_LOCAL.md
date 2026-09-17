# Editor local de Adulto Responsable

## Objetivo

Detectar las plecas de inicio, pausas musicales y fin de transmisión; conservar los segmentos hablados; reemplazar cada pleca por su animación y jingle; normalizar el audio hablado al nivel de los jingles; y revisar el resultado en DaVinci Resolve.

## 1. Programas y dependencias

- Windows 10/11.
- DaVinci Resolve Free 21.x.
- Python 3.11 o posterior.
- FFmpeg y FFprobe disponibles en `PATH`.
- Paquetes Python: `numpy`, `Pillow`.
- Opcional: puente local de Resolve (`resolve_client.py`) para importar medios y seleccionar timelines.
- Cuenta de GitHub solo si se desea publicar el respaldo; el procesamiento no depende de Internet.

Instalación rápida:

```powershell
py -m pip install numpy Pillow
ffmpeg -version
python --version
```

## 2. Carpetas

```text
Codex/
  analizar_vision.py
  ensamblar_programa.py
  resolve_client.py
  config.example.json
  assets/
    referencias/
    combinados/
    animaciones_originales/
    jingles_originales/
  trabajo_AR2/
    cortes.json
    programa_final_nivelado.mp4
```

`assets` contiene recursos reutilizables. `trabajo_AR2` contiene datos y resultados de una grabación concreta. El video fuente puede permanecer en OneDrive; no se modifica.

## 3. Flujo de ejecución

1. Copiar las tres referencias a `assets/referencias`.
2. Ajustar rutas en `config.json`.
3. Ejecutar `python analizar_vision.py`.
4. Revisar `trabajo_AR2/cortes.json`.
5. Ejecutar `python ensamblar_programa.py`.
6. El ensamblador conserva los tramos hablados, inserta las animaciones, sustituye su audio por los jingles y aplica `loudnorm=I=-16:TP=-1.5:LRA=11` solamente al audio hablado.
7. Importar `programa_final_nivelado.mp4` a una timeline nueva de Resolve para revisión.

## 4. Nueva computadora o cuenta

Copiar la carpeta `Codex`, instalar las dependencias, editar `config.json`, colocar los medios en las rutas configuradas y verificar que `ffmpeg`, `ffprobe`, Python y Resolve funcionen. No se deben copiar tokens, contraseñas ni configuraciones privadas.

## 5. Respaldo

Versionar scripts, documentación, configuración de ejemplo y assets pequeños. No versionar videos grandes, WAV, cachés ni credenciales. Usar Git LFS o almacenamiento externo para medios pesados.

```powershell
git init
git add .
git commit -m "Plantilla inicial del editor local"
git remote add origin https://github.com/USUARIO/REPOSITORIO.git
git push -u origin main
```

El procesamiento sigue siendo local aunque el repositorio esté en GitHub.
