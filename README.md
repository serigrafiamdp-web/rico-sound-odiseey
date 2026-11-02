# RICOS SOUND ODYSSEY — Port Commodore 64 / SID / TRSE

**Estado actual: TEST68B — PASS funcional en VICE (2 de noviembre de 2026).**

Este repositorio está dedicado a la reconstrucción del sintetizador **3001: A Sound Odyssey** para Commodore 64. El objetivo es obtener un proyecto ASM/TRSE mantenible, conservar la pantalla MICROSYNTH y las funciones del motor SID, eliminar módulos obsoletos y, más adelante, recuperar MIDI IN DATEL y rediseñar algunos controles.

> **IMPORTANTE:** el port todavía es **híbrido**. El programa funciona, pero una parte del código y los datos siguen dependiendo de la captura binaria ISEPIC. No es todavía una compilación independiente realizada completamente por TRSE.

## Última versión comprobada

**TEST68B — LFO + FIRE.** El usuario confirmó que el LFO sigue modulando mientras mantiene pulsado FIRE y maneja el joystick. Partimos de TEST66B PASS, no del TEST67 pendiente. No se desactivaron los sprites de MICROSYNTH.

D64 aprobado: `RICOS_TEST68B_LFO_FIRE_PASS.d64` — SHA-256:
`208c10d03d8b78d622f70e2dd25a762b9e2d4666eb02baede23bc6b5ad54f64d`.

Base de recuperación: TEST66B — SIN DEMO / TUTORIAL — SHA-256 D64:
`260f466e31fa0ec382621481f6f8e4c7b19495b791803e1e1ce10e0fbdc3752f`.

**Nota de distribución:** el ZIP limpio del proyecto, sus D64 y `log.txt` completo se entregaron como artefacto de la sesión. Todavía no se ha sincronizado todo el árbol de fuentes de ese ZIP con este repositorio. No confundir una actualización de documentación con la publicación de un nuevo ejecutable en GitHub.

## Estado de los módulos

| Módulo | Estado comprobado |
|---|---|
| MICROSYNTH, tres voces SID, filtros, ADSR, LOAD / SAVE / PRESETS | Funcionales en pruebas anteriores |
| RETURN / SYNC | PORT59 FIX1 PASS: copia valor ADSR de la voz bajo cursor a las otras dos; conserva origen |
| LFO durante controles FIRE | **TEST68B PASS** |
| Menú antiguo M + RUN/STOP | TEST65B PASS, retirado |
| DEMO / introducción TUTORIAL | TEST66B PASS, regiones retiradas |
| Poda adicional TEST67 | PENDIENTE de validación VICE; no incorporada a TEST68B |
| Sprites de tecla pulsada y nombre de nota | Deben permanecer habilitados en MICROSYNTH |
| SEQUENCER | Todavía no limpiado; aparece con cursor en PRESET + FIRE |
| MIDI IN DATEL | Prototipo histórico TEST09 PASS con polling; aún no reintegrado en el port TRSE actual |

## Rutinas identificadas

| Dirección | Uso identificado |
|---|---|
| `$484A` / `$485D` | Bucle musical y llamada al LFO |
| `$468F` | Actualización de modulación LFO / Envelope Follower |
| `$38A0` | Sondeo del joystick/FIRE |
| `$3A1D` / `$3A27` | Bucle de espera utilizado durante edición |
| `$0B0E` | Zona liberada del menú, reutilizada por servicio LFO TEST68B |
| `$3F03` | Entrada histórica de RETURN y vinculación ADSR |
| `$25C1` | Rutina reubicada de sincronización del parámetro fuente |
| `$39D8`, `$3FFA` | Selección de nibble ADSR y referencia de voz de origen |
| `$3BB7`, `$39D3` | Avance a siguiente voz y estado de voz |
| `$49F6–$4AE5` | Tablas de teclado y frecuencias SID |
| `$D41B`, `$D41C` | Lecturas SID OSC3 y ENV3 |
| `$0A81`, `$37BA` | Arranque histórico del menú y acceso M + RUN/STOP (retirados) |

El parche TEST68B agrega actualización cooperativa del LFO en los bucles de espera y de lectura de FIRE, evitando una segunda IRQ de audio. Ver `sound/lfo_continuous_fire_test68.asm` en el ZIP limpio.

## Cobertura real de fuentes

Hasta PORT63 se contabilizaron **15.041 bytes de instrucciones 6502** y **12.757 bytes de tablas y datos** reconstruidos desde fuentes. **No significa 42,8% de independencia funcional:** todavía se utiliza el residuo binario y el cargador histórico. La eliminación de bloques de menú tampoco reduce automáticamente el tamaño del D64.

## Organización de la distribución limpia

- `README.md`: estado vigente y mapa técnico.
- `log.txt`: **un solo archivo** que reúne los anteriores 95 archivos `.txt` y 7 `.log`, cada uno con ruta de origen y checksum.
- `main.ras`, `RICOSSOUNDODISSEY.trse`: proyecto y bootstrap fuente.
- `sound/`: rutinas ASM y únicamente binarios base necesarios.
- `assets/`: residuales/manifiestos conservados para poder reconstruir.
- `tools/`: ensambladores y constructores; sin D64 ni lanzadores históricos redundantes.
- `D64/`: TEST68B PASS y TEST66B de respaldo.

El ZIP completo anterior se conserva por separado como respaldo; el paquete limpio no contiene lotes viejos de D64 o diagnósticos.

## Siguientes trabajos

1. Regresión de ADSR, PULSE WIDTH, filtros y presets con LFO continuo.
2. Analizar SEQUENCER: cursor en PRESET, pulsar FIRE. Retirar su código exclusivo preservando PRESETS.
3. Completar el port de código real y eliminar dependencia del residuo.
4. Reintegrar MIDI IN DATEL mediante un gestor único del motor de notas, minimizando cortes audibles.
5. Rediseñar la UI y los atajos de teclas solamente después.

## Procedencia e historial

Este README se corrigió porque contenía documentación de **SIDPLAY64, KrillLoad y SIDTracker64**, correspondiente a otra línea de trabajo. El contenido anterior se conservó en la rama `backup/readme-pre-port-2026-11-02`. El historial MIDI específico de SOUND ODYSSEY sigue siendo útil; los tests SIDPLAY64 no forman parte de este port.

Esta publicación no constituye un nuevo PASS de VICE ni un resultado de compilación TRSE autónoma.
