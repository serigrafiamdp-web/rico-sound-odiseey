# Protocolo de trabajo y control de versiones

Para cada cambio del motor SID o del controlador MIDI:

1. Partir de una referencia PASS conocida y anotar el commit SHA.
2. Hacer **una modificación funcional controlada** por TEST.
3. Generar una compilación autocontenida, con D64 listo para VICE cuando sea una prueba de C64.
4. Registrar compilación por separado de ejecución: **BUILD PASS no implica VICE PASS**.
5. Si VICE falla, registrar pantalla, letra de diagnóstico, borde, comportamiento del drive, audio y etapa de carga.
6. Después de confirmación del usuario, marcar **PASS funcional** o FAIL con el alcance exacto, conservando el archivo reproducible.
7. Nunca sobrescribir el MASTER o la rama de referencia. Usar ramas TEST y conservar el código fuente más los manifiestos.
8. No atribuir compatibilidad general con SD2IEC/PSID/NTSC hasta validarla explícitamente.
9. Documentar la procedencia y licencias del código de Glenn Rune, Krill y proyectos externos.

Ramas de recuperación: [TEST02C PASS](https://github.com/serigrafiamdp-web/SIDPLAY64MIX/tree/milestone/test02c-krill-abc-pass-26oct2026) y [TEST02D PASS funcional](https://github.com/serigrafiamdp-web/SIDPLAY64MIX/tree/milestone/test02d-krill-three-sids-audio-pass-26oct2026).

Mantener el estado del proyecto explícito: **PASS de prototipo independiente, TEST03 integración pendiente**.