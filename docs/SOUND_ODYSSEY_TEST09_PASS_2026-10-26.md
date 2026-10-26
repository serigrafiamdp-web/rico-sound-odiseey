# SOUND ODYSSEY — TEST09 MIDI DATEL / OCTAVAS INDEPENDIENTES

**Fecha de validación en VICE:** 26 de octubre de 2026.
**Resultado reportado por el usuario:** **TEST09 PASS — SOUND funciona desde C1 hasta C6**, incluida la última nota C6, con el cartucho DATEL emulado. El programa mantiene la interfaz de Microsynth operativa y produce sus propios sonidos a través del SID.

## MASTER vigente

- **TEST09 — MASTER MIDI DATEL, PASS funcional en VICE**. SHA-256 del PRG exacto: `5cd58564c68c2ce836f9843a4bc5f794bda07ed44be7909c9bced3196a974647`. Tamaño: **37.970 bytes**.
- **TEST08 — MASTER anterior / recuperación**. SHA-256: `b9a3cfe3dadb90b379674f90ff5cfd35b16d74a82d0dbd8b3c79b562f1de77d0`.
- **SOUND original ISEPIC**. SHA-256: `dfa940539024d63f249b029188bc12e391a9671489f93c96cf1694d2641080a3`.
- Los archivos binarios y fuente del TEST09 están respaldados en el artefacto del chat `SOUND_ODYSSEY_DATEL_MIDI_TEST09_OCTAVAS_INDEPENDIENTES.zip`; **el PRG no se ha cargado como archivo binario en GitHub**. Conservar el ZIP y el PRG de la conversación.
- Precedente técnico: [historia de TEST03–TEST08](SOUND_ODYSSEY_DATEL_MIDI_2026-10-26.md).

## Configuración PASS (VICE)

- Emulación MIDI habilitada, interfaz **DATEL/Siel/JMS**, MIDI IN en `loopMIDI Port`.
- Segundo SID desactivado.
- Se usa el SOUND arrancado desde snapshot ISEPIC, con instrumentos ya cargados, sin intros/menús originales.

## Capacidad implementada en TEST09

| Característica | Estado |
| --- | --- |
| MIDI IN / DATEL | PASS funcional mediante polling; sin IRQ MIDI |
| Sonido | Presets y motor SID originales de SOUND ODYSSEY |
| Rango del editor utilizado | **C1 a C6** (extremos incluidos), **61 semitonos cromáticos programados** |
| Números MIDI recibidos | 12..72 (C1 del editor = número 12 según el mapeo acordado) |
| Índices de frecuencia internos de SOUND | 24..84, dentro de tabla original de 96 entradas |
| Independencia de octava de pantalla | Implementada en selector de frecuencia; usuario confirma acceso a todo el rango |
| Teclado C64 | Ruta original conservada, octava visual independiente |
| Note On / Note Off | Integrados |
| Polifonía | **Monofónico**, una nota MIDI activa |
| Hardware DATEL real | Pendiente de validar; PASS actual es VICE |
| Robustez MIDI bajo carga | Pendiente: parser de polling puede perder bytes |

**Precisión:** el rango extremo a extremo y el sonido están confirmados por la experiencia del usuario, pero **no se ha documentado una prueba individual de los 61 semitonos**, ni una comparación instrumental de afinación, latencia o pérdida de eventos bajo carga. No tratar este PASS como prueba de todos esos aspectos.

## Parche interno respecto de TEST08

- Se conserva la recepción ACIA DATEL **sin habilitar IRQ**: control `$DE04`, estado `$DE06`, datos `$DE07`.
- Se mantiene el hook estable de scan en `$486E` → `JSR $2540`.
- Las rutinas auxiliares nuevas ocupan `$C060–$C0C4` de la imagen restaurada del PRG.
- `$490D` intercepta el cálculo de la nota justo antes de `$4912 TAX / $4913 STX $39D4`.
- La ruta MIDI usa la frecuencia absoluta guardada en `ActivePitch`; la ruta de teclado de C64 conserva su cálculo `posición + $3EEE`.
- Se distinguen `ActiveMidi` y `ActivePitch` para evitar confusión de notas separadas dos octavas.
- Se preservan las tablas originales de 96 frecuencias SID en `$4A26` y `$4A86`, los presets y el motor de sonido.
- Compilación de prueba: `build_sound_midi_test09_absolute.py`; simulador `test_sound_midi09_cpu.py` (incluidos en ZIP de la conversación). El constructor necesita `rebuild_SOUND_DATEL_TEST08_from_original.py` y los demás archivos requeridos que contiene ese ZIP.

## Secuencia histórica

- TEST03: PASS de entrada DATEL con polling y borde.
- TEST04/05/06: FAIL por corrupción al recibir la primera nota cuando habilitábamos IRQ MIDI.
- TEST07: PASS del primer sonido propio de SOUND desde MIDI.
- TEST08: PASS con calibración C1, todavía dependía de octava visual.
- **TEST09: PASS** con rango C1–C6 y selección de frecuencia absoluta para MIDI.

## Próximos trabajos

1. **Congelar TEST09** como punto estable. Si se prueba nueva funcionalidad, siempre derivarla del MASTER.
2. Revisión de comportamiento de `Note Off`, notas consecutivas y notas simultáneas; no prometer polifonía todavía.
3. Test de estrés de polling para evitar pérdida de bytes, sin repetir las IRQ defectuosas.
4. Validación física en DATEL real.
5. Solo después: controles MIDI adicionales (velocity, sustain, pitch bend, etc.) si se solicitan.

La distinción entre el nombre C1 del editor y el número MIDI 12 debe mantenerse en todas las pruebas futuras.
