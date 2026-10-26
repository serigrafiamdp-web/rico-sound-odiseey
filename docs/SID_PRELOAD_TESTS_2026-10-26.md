# KrillLoad / SIDPLAY64MIX — Registro de pruebas

Fecha: **26/10/2026**. Entorno: **Commodore 64 / VICE, unidad 1541 emulada**. Los resultados de reproducción provienen de las observaciones de la persona que ejecutó las pruebas en VICE; la compilación y los archivos D64 se verificaron en GitHub Actions.

## Tabla de resultados

| Test | Resultado | Verificado | Pendiente |
| --- | --- | --- | --- |
| TEST01 | Preparación de recursos | Banco fijo $1000 ejecutable y $5000 precarga; archivos A/B/C generados y comprobados | No reproduce por sí solo |
| TEST02 | FAIL de arranque | Cargador no avanzaba; diagnóstico posterior | Corregido en TEST02C |
| TEST02B | FAIL de arranque | Diagnóstico marcó fallo de KERNAL al leer INSTA; causa: codificación incorrecta del nombre | Corregido |
| **TEST02C** | **PASS funcional en VICE** | Carga los tres SID y cambia entre ellos; se oye música durante precarga | Velocidad excesiva, integración original pendiente |
| **TEST02D** | **PASS funcional en VICE** | Continúan carga y cambios con PLAY alternando IRQ (50%) | Primeras canciones más lentas de lo deseado; la tercera se oye más próxima a la velocidad correcta |

## Arquitectura experimental demostrada

```text
A activo ($1000, INIT=$1000, PLAY=$1003)
    |
    +--> Krill carga B en $5000 mientras A reproduce
    |
    +--> umbral experimental: copiar B $5000->$1000, INIT B
                         |
                         +--> Krill carga C en $5000 mientras B reproduce
                         |
                         +--> copiar C $5000->$1000, INIT C
```

Los dos primeros bancos y la copia de 8 KB fueron elegidos para un **conjunto concreto de canciones**; no constituyen un sistema universal de PSID.

### Detalles relevantes

- Krill v184 compilado para instalador $6000, cargador residente $9000, ZP $C0.
- Durante IRQ musical, se preservan 22 bytes de Zero Page del cargador y se intercambian con los de la canción.
- En el prototipo se trabaja con KERNAL antes de instalar el cargador. La prueba inicial apunta a **1541 emulada**, no a SD2IEC real.
- TEST02D mantiene la interrupción CIA a ~60 Hz ($4025 PAL), pero ejecuta PLAY en una de cada dos interrupciones: ~30 llamadas PLAY/s. El umbral de 600 IRQ (~10 s) **no cambia**.
- En el último cambio de TEST02D aparece la letra K del diagnóstico. El usuario indicó que **ese último SID** se aproxima más a su velocidad correcta, mientras que los primeros se oyen lentos. No hay todavía medida instrumental por canción.
- El indicador de pantalla, audio y transiciones no equivale a certificar ausencia total de clicks o ciclos perdidos. Falta una prueba instrumentada.

## Evidencia y fuentes de recuperación

- [Código TEST02C PASS](https://github.com/serigrafiamdp-web/SIDPLAY64MIX/tree/milestone/test02c-krill-abc-pass-26oct2026)
- [Código TEST02D PASS funcional](https://github.com/serigrafiamdp-web/SIDPLAY64MIX/tree/milestone/test02d-krill-three-sids-audio-pass-26oct2026)
- [Bitácora de observación auditiva del usuario](https://github.com/serigrafiamdp-web/SIDPLAY64MIX/blob/test/test01-preload-staging/tests/TEST02D_USER_VICE_PASS_2026_10_26.md)
- [Harness TEST02C local](../experiments/sid-preload/test02c_krill_irq_harness.tas) — copia del fuente probado
- [Harness TEST02D local](../experiments/sid-preload/test02d_half_playrate.tas) — variante 50% probada
- [Constructor de D64](../experiments/sid-preload/build_test02_d64.py)
- [Preparación de PSID](../experiments/sid-preload/preload_assets.py)

## Próximo hito: TEST03

**Objetivo:** adaptar precarga e intercambio a SIDPLAY64 original sin romper interfaz ni playlist.

1. Mantener el timer original (checkdigits) y su selección M/N/R.
2. Determinar el sucesor ANTES del vencimiento del timer y cargarlo en buffer seguro.
3. Al vencer: si NEXT_READY coincide con el tema elegido, hacer el handoff sin esperar disco; si no, fallback controlado al loader original.
4. En el nuevo tema volver a precargar el siguiente durante PLAY.
5. Preservar IRQ CIA/raster, Zero Page y autorreubicación por cabecera PSID. Probar 1541 y SD2IEC por separado.
6. Determinar velocidad por música; **no** convertir el divisor experimental global al 50% en configuración definitiva.

**No se ha validado todavía TEST03.**

## Dependencias y créditos

SIDPLAY64: Glenn Rune Gallefoss · Krill's Loader: Gunnar Ruthenberg · SCUMM-PET-C64: referencia anterior de convivencia IRQ/carga. No mezclar licencias de software de terceros ni publicar código fuente ajeno sin revisar condiciones.