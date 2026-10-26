# Binarios de referencia y verificación

Este repositorio de GitHub conserva **código fuente y documentación**. Los D64 PASS fueron generados y compartidos en la conversación de prueba del **26/10/2026**. Por ahora **los D64 binarios no están subidos a este repositorio**; no confundir una referencia con un archivo alojado.

## Archivos probados por el usuario en VICE

| Archivo | Tamaño | SHA-256 | Estado |
| --- | ---: | --- | --- |
| `SIDPLAY64MIX_TEST02C_FILENAME_FIX.d64` | 174848 | `2b26415bca866f17191673e2b554ab9419ba616cf261464fe6377aca015b94fe` | PASS funcional: precarga y cambio A/B/C; velocidad acelerada |
| `SIDPLAY64MIX_TEST02D_50PCT_KRILL.d64` | 174848 | `c59179529512ea83e55170aedfb003c2b1f564c25691e5ec89775fd12a810178` | PASS funcional: precarga/cambios, velocidad 50% experimental |

Los hashes se calcularon sobre los D64 reales ya generados, no sobre los ZIP.

## Fuentes archivadas

En `experiments/sid-preload/` se conservaron copias byte a byte del **contenido textual** de estos archivos (sus Git blob SHA resultaron idénticos a las referencias):

- `test02c_krill_irq_harness.tas`, Git blob `d98e489cf7312df9c00158d5f82545e5bf5ae822`
- `test02d_half_playrate.tas`, Git blob `7f588db8d51cfa780de0c2b05a38f7ac2e9b03ae`
- `build_test02_d64.py`, Git blob `6d25a589986a0829f4ca26b6f0f40c2b5d5ea88c`
- `preload_assets.py`, Git blob `6ebb79799db4a27bd66e389615efb74f78b74706`

Importante: no basta con esos cuatro archivos para reconstruir totalmente el D64. Se requiere **Krill's Loader v184**, los SID de prueba originales y la cadena de compilación; consultar [SIDPLAY64MIX](https://github.com/serigrafiamdp-web/SIDPLAY64MIX).

Estos binarios son *harness* experimentales, **no el SIDPLAY64 original integrado**.
