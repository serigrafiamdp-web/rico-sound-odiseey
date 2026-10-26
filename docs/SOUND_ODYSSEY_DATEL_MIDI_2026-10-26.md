# SOUND ODYSSEY — MIDI IN DATEL (26-10-2026)

## MASTER actual

**TEST08 — PASS funcional informado por el usuario en VICE (26/10/2026).** SOUND ODYSSEY / Microsynth reproduce sus propios instrumentos al tocar notas MIDI externas. El programa permanece estable. La referencia auditiva adoptada es **C1 del editor MIDI como primer Do grave audible**. La equivalencia interna programada en TEST08 es **número MIDI 12 → primera posición del teclado musical**; la nomenclatura C1 depende del editor y no es parte del estándar MIDI.

No confundir este PASS con soporte MIDI completo: TEST08 es **monofónico**, escucha 18 semitonos consecutivos (números MIDI 12–29), conserva la selección de octava de Microsynth y usa polling. La independencia de octava, todas las notas del SID, buffer MIDI, polifonía y hardware físico todavía no están implementados/validados.

## Base y objetivo

- Programa: **3001: A Sound Odyssey**, sintetizador **Microsynth**.
- Binario base: **sound(1).PRG**, capturado con cartucho **ISEPIC** con instrumentos ya cargados; evita intros y menús anteriores.
- Entrada: cartucho **DATEL/Siel/JMS** MIDI IN, emulada en VICE con **loopMIDI Port**. **Segundo SID desactivado** en VICE (su activación produjo problemas con Cynthcart en esta configuración).
- Salida: sonido de los **presets y motor SID originales de SOUND**; el MIDI externo no es un sintetizador adicional.
- Teclado Commodore **Q2W3ER5T6Y7U8I9O0P** se conserva y continúa funcionando.

## Cronología de pruebas

| Prueba | Técnica | Resultado en VICE | Observación |
|---|---|---|---|
| TEST00 | Análisis PRG y Cynthcart | Análisis | Autorreubicación y rutinas MIDI documentadas |
| TEST01 DATEL independiente | Receptor ACIA, Note On/Off | **PASS** | Confirmó lectura de datos externos; aún sin SOUND |
| TEST02 | Primer parche sobre PRG empaquetado | **FAIL** | No detectaba; hook no era el código definitivo reubicado |
| TEST03 | SOUND + polling DATEL + borde | **PASS** | Colores al recibir MIDI, SOUND sobrevivía |
| TEST04 | DATEL IRQ + teclado virtual | **FAIL** | Corrupción de pantalla al tocar |
| TEST05 | IRQ sin teclado virtual | **FAIL** | Corrupción con primera nota; descarta que la única causa sea el teclado virtual |
| TEST06 | IRQ mínima + contador | **FAIL** | Corrupción con primera nota; causa exacta no demostrada |
| TEST07 | Polling en escaneo musical | **PASS** | Sonido MIDI real de SOUND, sin cuelgues; base MIDI 60 |
| TEST08 | Igual que TEST07, base MIDI 12 | **PASS funcional** | Usuario confirmó sonido/estabilidad y fijó C1 como primer Do grave audible |

**Regla de recuperación:** no seguir trabajando sobre TEST04–TEST06; retomar **TEST08** para funciones y **TEST03** para recepción diagnóstica. Mantener original, TEST03, TEST07 y TEST08 por separado. Un PASS en VICE no implica prueba en cartucho físico.

## Implementación actual

Registros ACIA 6850 para DATEL:

- `$DE04`: control/reset; TEST08 establece `$03` y luego `$16` para recepción **sin IRQ de MIDI**.
- `$DE06`: registro de estado; bit 0 indica byte disponible.
- `$DE07`: dato de recepción MIDI.

Rutas identificadas en la imagen ya desempaquetada del snapshot:

- `$486E`: sustitución localizada de `JSR $007B` por `JSR $2540`.
- `$007B`: lector original `STY $DC00 / AND $DC01 / RTS`, preservado.
- `$2540–$25F9` aprox.: rutina TEST08 de polling, parser sencillo de mensajes de nota y simulación de una posición musical.
- `$49F6` y `$4A0E`: tablas de 24 entradas del escaneo musical original.
- `$3EEE`: selección de octava del teclado original (observados offsets 24/36/48).
- `$4A26` y `$4A86`: dos tablas de 96 bytes para frecuencias SID (96 índices = 8 octavas almacenadas).
- `$490D–$4913`: cálculo original `TXA / CLC / ADC $3EEE / TAX / STX $39D4` que aplica la octava seleccionada.

El receptor TEST08 **no** cambia los vectores IRQ/NMI (`$0314/$0315`, `$FFFE/$FFFF`) ni modifica directamente SID o presets. Procesa `$9n` velocidad distinta de cero como Note On, `$8n` y Note On velocidad cero como Note Off; usa running status básico. Borde verde/azul = diagnóstico de ON/OFF. Puede perder bytes por falta de buffer de hardware/sondeo poco frecuente: **no dar por garantizada la fiabilidad MIDI bajo carga**.

## Calibración

- La conversión instalada es `indice_tecla = numero_midi - 12`, permitiendo índices 0..17.
- El usuario identificó **C1 en su editor** como el primer Do grave que coincide con SOUND.
- **No cambiar otra vez a C0** sin comprobar qué número MIDI envía el editor. Los nombres de octava MIDI cambian entre programas.

## ISEPIC: captura original útil para ingeniería inversa

La captura `3001 CODE.zip` contiene bloques de RAM `PGM.0` a `PGM.3`, `PGM.C` para Color RAM y `PGM.X` para estado adicional. Al concatenar el contenido de los cuatro bloques (sin las cabeceras PRG de 2 B), se obtiene un mapa de **65.536 bytes**. La comparación con la RAM recuperada del PRG mostró **64.528 bytes iguales (98,46%)**. La snapshot es **una imagen de memoria, no un ejecutable por sí sola**.

ISEPIC en modo cartucho usa la región `$DE00–$DE07`, que puede entrar en conflicto con DATEL; el PRG independiente ya restaurado no requiere mantener el ISEPIC conectado.

## Siguiente etapa — NO implementada

Conservar TEST08 y lograr notas MIDI **absolutas**, independientes de la octava visual de SOUND:

1. Identificar la ruta completa de índice musical hasta selección de frecuencias y gate SID.
2. Separar nota física relativa (`indice + $3EEE`) de nota MIDI absoluta.
3. Explorar tablas existentes de 96 notas sin modificar preset, filtros ni envolventes.
4. Mantener teclado C64 con sus octavas, y MIDI con número de nota independiente.
5. Mejorar confiabilidad del polling o encontrar sistema de recepción seguro sin repetir el fallo IRQ.
6. Probar primero en VICE; después DATEL físico.

## Referencias

- Código de Cynthcart (ejemplo de receptor MIDI): https://github.com/PaulSlocum/cynthcart
- Archivos ISEPIC y proyecto: `3001 CODE.zip`, `sound(1).PRG`.
- Repositorio: https://github.com/serigrafiamdp-web/rico-sound-odiseey
