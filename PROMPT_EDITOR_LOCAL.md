# Prompt para otra IA

Trabaja como ingeniero de automatización audiovisual local y offline. Debes operar sobre un programa de radio grabado a 1280x720 y 60 FPS. El objetivo es conservar únicamente los segmentos donde aparece el locutor hablando, reemplazar cada bloque de pleca por su animación correspondiente y sustituir el audio de esas animaciones por los jingles disponibles.

Usa Python, FFmpeg/FFprobe y DaVinci Resolve Free. No subas videos a servicios externos. Lee las referencias de `assets/referencias`: inicio, pausa musical y fin de transmisión. Lee las animaciones de `assets/combinados` y los jingles de `assets/jingles_originales`.

Primero analiza el video y genera `trabajo_AR2/cortes.json`. Después ensambla una nueva versión: conserva los tramos hablados, inserta una animación por cada bloque detectado, recorta cada inserción a su duración real y usa el jingle correspondiente. Normaliza únicamente el audio original hablado a `-16 LUFS`, techo `-1.5 dBTP`; no cambies el nivel de los jingles.

Antes de reemplazar un resultado, conserva solo la versión final y elimina los intentos generados anteriores, sin tocar el original ni `assets`. Importa cada resultado final a una timeline nueva de DaVinci Resolve y deja esa timeline activa para revisión visual. Documenta cualquier error, no inventes rutas y verifica duración, FPS, pistas de audio y sincronía antes de declarar terminado el trabajo.
