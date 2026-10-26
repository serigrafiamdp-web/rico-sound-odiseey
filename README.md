# RICO SOUND ODISEEY

**Proyecto Commodore 64 / SID / MIDI.**

Este repositorio reúne la documentación, las pruebas reproducibles y el desarrollo futuro de **RICO SOUND ODISEEY**.

## Estado inicial — 26 de octubre de 2026

Este repositorio se creó vacío. Se inicializó con documentación de referencia y copias de código de pruebas **sin modificar** los repositorios fuente ni confundir una compilación exitosa con una validación en VICE.

### Áreas de trabajo

- **Sound Odyssey / MIDI**: mapeo de notas y octavas para el chip SID. Referencia operativa: `C1` es la primera nota grave audible validada en Sound Odyssey. La escala C1–C6 y el alcance real del SID requieren verificación de pruebas MIDI adicionales.
- **Reproducción SID / precarga**: experiencia probada en VICE con KrillLoad y transiciones A → B → C en el prototipo experimental derivado de SIDPLAY64.
- **Compatibilidad SIDTracker64 (iPad)**: investigar cadencias reales de reproducción de los SID exportados, cabeceras PSID, timer CIA/VBI y CALL PLAY. No atribuir una velocidad única a todos los SID.

## Documentos

- [Registro de pruebas de precarga](docs/SID_PRELOAD_TESTS_2026-10-26.md) — TEST02C y TEST02D, resultados observados, límites y riesgos.
- [Estado de MIDI, Sound Odyssey y SIDTracker64](docs/SOUND_ODISEEY_MIDI_SIDTRACKER64.md) — convenciones verificadas y problemas pendientes.
- [Protocolo de pruebas](docs/TEST_PROTOCOL.md) — cómo registrar nuevos TEST / PASS / FAIL sin alterar un MASTER.

## Código experimentado

Las rutinas de las pruebas de Krill están en el proyecto donde se desarrollaron y compilaron:

- [SIDPLAY64MIX (fuente original de los TEST)](https://github.com/serigrafiamdp-web/SIDPLAY64MIX)
- [TEST02C — punto de recuperación PASS](https://github.com/serigrafiamdp-web/SIDPLAY64MIX/tree/milestone/test02c-krill-abc-pass-26oct2026)
- [TEST02D — punto de recuperación PASS funcional](https://github.com/serigrafiamdp-web/SIDPLAY64MIX/tree/milestone/test02d-krill-three-sids-audio-pass-26oct2026)
- [Documentación original de Glenn Rune y código del reproductor](https://github.com/serigrafiamdp-web/SIDPLAY64MIX/blob/master/sidplay64-readme.txt)
- [SCUMM-PET-C64 — precedente de reproducción mientras Krill carga](https://github.com/serigrafiamdp-web/SCUMM-PET-C64)

**Importante:** la precarga demostrada en el *harness* no está todavía integrada en la interfaz, playlist y sistema autorreubicable de SIDPLAY64. No hay confirmación de compatibilidad con SD2IEC real ni de velocidad musical final. No promover a MASTER sin nueva prueba.

## Siguiente objetivo

Desarrollar un TEST03 que conecte la precarga al timer y a la selección de archivos del SIDPLAY64 original: mientras suena A, cargar B; al cumplirse el timer, activar B desde RAM; durante B, precargar C. Mantener controles y playlist originales.

Los nuevos cambios se hacen en ramas de prueba; el código validado se conserva en referencias MASTER/PASS inmutables o ramas etiquetadas claramente.

## Créditos

- **SIDPLAY64** — Glenn Rune Gallefoss.
- **Krill's Loader** — Gunnar Ruthenberg.
- **SIDTracker64** — aplicación de composición SID para iPad (referencia de compatibilidad).

El código fuente de terceros conserva sus respectivas licencias y créditos. Esta documentación no implica que las pruebas estén listas para publicación como reproductor final.
