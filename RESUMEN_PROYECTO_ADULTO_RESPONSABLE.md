# Resumen del proyecto — Editor local de Adulto Responsable

## Objetivo

Automatizar localmente la limpieza de los programas grabados de Adulto Responsable:

- Detectar las plecas de inicio, pausa musical y fin de transmisión.
- Conservar los segmentos donde aparece el locutor hablando.
- Reemplazar cada bloque detectado por su animación correspondiente.
- Sustituir el audio de las animaciones por los jingles oficiales.
- Nivelar el audio hablado para que no quede más bajo que los jingles.
- Mantener video y audio sincronizados a 60 FPS.
- Importar cada resultado final a DaVinci Resolve para revisión visual.

## Resultado actual

La versión nivelada se generó como:

`C:\Users\noqui\Documents\Codex\trabajo_AR2\programa_final_nivelado.mp4`

La timeline activa de DaVinci Resolve es:

`Programa Final - AUDIO NIVELADO`

Las timelines de prueba anteriores fueron eliminadas del proyecto.

## Flujo de trabajo

1. Colocar el video fuente en una ruta local configurada.
2. Guardar las referencias visuales en `assets/referencias`.
3. Ejecutar `analizar_vision.py`.
4. Revisar `trabajo_AR2/cortes.json`.
5. Ejecutar `ensamblar_programa.py`.
6. El script conserva los tramos hablados e inserta las animaciones y jingles.
7. El audio hablado se normaliza con objetivo de `-16 LUFS` y techo de `-1.5 dBTP`.
8. Importar el MP4 final a una timeline nueva de DaVinci Resolve.
9. Revisar visualmente la sincronía, los cortes y el volumen.

## Archivos principales

- `analizar_vision.py`: detección visual de plecas mediante las referencias.
- `ensamblar_programa.py`: ensamblado, sustitución de animaciones y nivelación de audio.
- `resolve_client.py`: conexión local con la API/puente de DaVinci Resolve.
- `config.example.json`: plantilla de rutas para otra computadora o cuenta.
- `setup_local.ps1`: preparación de carpetas y dependencias Python.
- `README_INSTALACION.md`: instrucciones de instalación, incluyendo PowerShell.
- `DOCUMENTACION_PIPELINE_LOCAL.md`: documentación técnica completa.
- `PROMPT_EDITOR_LOCAL.md`: prompt reutilizable para otra IA.

## Recursos

- `assets/referencias`: banners de inicio, pausa musical y fin.
- `assets/combinados`: animaciones preparadas a 60 FPS.
- `assets/jingles_originales`: jingles de inicio, pausa y salida.
- `trabajo_AR2`: reportes, transcripción y resultados del programa actual.

## Instalación en otra computadora

Instalar Python, FFmpeg, Git y DaVinci Resolve. Desde PowerShell:

```powershell
winget install --id Python.Python.3.13 --exact --source winget
winget install --id Gyan.FFmpeg.Shared --exact --source winget
winget install --id Git.Git --exact --source winget
python -m pip install numpy Pillow
```

Después, copiar `config.example.json` como `config.json`, ajustar las rutas y ejecutar los dos scripts principales.

## Respaldo

El proyecto tiene un respaldo portable:

`C:\Users\noqui\Documents\Codex\editor_local_template_backup.zip`

También está preparado para el repositorio:

`https://github.com/adultoresponsablefm/editor-video-adulto-responsable`

No deben subirse al repositorio videos finales grandes, WAV, credenciales, claves SSH/GPG ni archivos privados.

## Regla permanente

Cada nueva exportación debe nivelar el audio hablado contra los jingles, eliminar los intentos fallidos anteriores cuando exista una versión válida, y dejar siempre el resultado final visible en una timeline nueva de DaVinci Resolve.
