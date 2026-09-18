# Soluciones y problemas detectados

## Audio ausente en DaVinci

El archivo podía tener una pista AAC válida, pero Resolve reutilizaba un clip anterior con el mismo nombre y no regeneraba su waveform. La solución fue:

1. Verificar siempre el archivo con FFprobe.
2. Exigir `video` y `audio` antes de aceptar una exportación.
3. Importar el resultado con un nombre nuevo cuando Resolve conserve caché del clip anterior.
4. Confirmar en Resolve que existan `V1` y `A1`.

`ensamblar_programa.py` y `importar_final_resolve.py` ahora detienen el flujo si falta una de las pistas.

## Puente de DaVinci inactivo

Después de reiniciar Resolve, el puente local puede no iniciar. El síntoma es `WinError 10061` o `ConnectionRefusedError`. La solución es activar el puente dentro de Resolve antes de ejecutar `importar_final_resolve.py`.

## Detección de rostros equivocados

Contar cualquier rostro no era suficiente: los videos musicales también pueden mostrar personas. Para Chilaquil se agregó una señal más fiable: la pleca inferior propia del programa, calibrada con el primer cuadro del video. La referencia facial queda como apoyo, pero no sustituye la identidad visual del perfil.

## Perfiles separados

Radio CUCEI usa animaciones y jingles. Radio Chilaquil conserva su identidad, no inserta jingles y elimina los bloques sin la pleca/presencia del locutor para retirar canciones y reducir riesgos de copyright.

## Resultado comprobado

La prueba final de Chilaquil se importó con éxito en `Programa Chilaquil - SOLO LOCUTOR AUDIO`, verificada con un clip en video y un clip en audio.
