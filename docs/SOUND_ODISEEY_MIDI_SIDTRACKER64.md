# Sound Odyssey — MIDI, octavas y SIDTracker64

Estado de referencia: **26 de octubre de 2026**.

## Control MIDI en Sound Odyssey

De las pruebas de teclado/emisor MIDI anteriores se acordó usar **C1** como primera nota grave audible de referencia. Fue la primera nota que sonó y correspondió al C grave de Sound Odyssey en el editor.

Convención de trabajo:
- Primera nota práctica: **C1**.
- Extensión de referencia discutida: **C1 a C6**.
- **No forzar C0** por una convención MIDI externa si la interfaz actual ya funciona desde C1.
- Objetivo funcional: las notas entrantes por MIDI deben sonar a su frecuencia real independientemente de la octava visible seleccionada con teclas en la interfaz de Sound Odyssey, hasta cubrir el rango de alturas que efectivamente admite el SID.
- El rango extremo de frecuencias y las traducciones de octava quedan sujetos a validación en una máquina C64/VICE; no se considera cerrado todo el mapeo.

Este es el registro de la decisión de diseño anterior, **no una implementación nueva** en el presente repositorio.

## Interpretación de SIDTracker64 (iPad)

No está acreditada una firma especial de SIDTracker64 en el reproductor de Glenn Rune; SIDPLAY64 interpreta las cabeceras estándar PSID/RSID, direcciones INIT/PLAY, velocidad (CIA/VBI), subtunes, modelo SID y páginas libres de reubicación.

La palabra de velocidad de la cabecera PSID por sí sola **no expresa un número arbitrario de Hz**. Algunas composiciones utilizan cadencias internas no estándar, que requieren medir las invocaciones de PLAY y revisar la rutina INIT.

### Observación de TEST02C/TEST02D

- En TEST02C los temas suenan acelerados a unas 60 llamadas PLAY por segundo.
- En TEST02D, con las llamadas PLAY reducidas a la mitad, los primeros temas se perciben lentos y la última canción (diagnóstico K) queda más próxima a la velocidad correcta.
- No extrapolar 30 Hz a todos los temas: diferenciar tempo interno del tracker, la velocidad PLAY y el reloj de IRQ/precarga.

### Para analizar un SID de SIDTracker64

Registrar: magic PSID/RSID, versión, offset, dirección de carga, INIT, PLAY, cantidad de subtunes, speed bits, flags de reloj/chip, tamaño y rango de memoria ocupado; observar en VICE registro CIA1 $DC04-$DC05, frecuencia real de PLAY y posibles cambios durante INIT. Comparar con el comportamiento en SIDPLAY64 sin introducir delays dentro de Krill.

## Referencias

- [Formato SID en repositorio de SIDPLAY64](https://github.com/serigrafiamdp-web/SIDPLAY64MIX/blob/master/docs/SID_file_format.txt)
- [Interpretación de cabecera y autorreubicación](https://github.com/serigrafiamdp-web/SIDPLAY64MIX/blob/master/src/doheaderstuff.tas)
- [Reproductor SIDPLAY64](https://github.com/serigrafiamdp-web/SIDPLAY64MIX/blob/master/sidplay64.tas)
- [Investigación inicial de timing](https://github.com/serigrafiamdp-web/SIDPLAY64MIX/blob/milestone/test02d-krill-three-sids-audio-pass-26oct2026/docs/SIDTRACKER64_TIMING_INVESTIGATION_2026_10_26.md)

Este documento indica el **estado de conocimiento y las pruebas pendientes**, no garantiza compatibilidad total con cualquier archivo exportado por iPad.