# Reconstrucción exacta del TEST08

Archivo `rebuild_SOUND_DATEL_TEST08_from_original.py.gz`: código Python fuente comprimido con gzip para preservar exactamente el constructor que pasó pruebas de regresión.

1. Descomprimir con 7-Zip o `gzip -d` para obtener el .py.
2. Colocar cerca la captura ISEPIC exacta `sound(1).PRG`.
3. Ejecutar `python rebuild_SOUND_DATEL_TEST08_from_original.py "sound(1).PRG" TEST08.PRG`.
4. El script comprueba SHA256 del original y del resultado e impide modificar el original accidentalmente.

SHA256 original: `dfa940539024d63f249b029188bc12e391a9671489f93c96cf1694d2641080a3`.
SHA256 TEST08: `b9a3cfe3dadb90b379674f90ff5cfd35b16d74a82d0dbd8b3c79b562f1de77d0`.

En la sesión de creación, este script produjo un PRG de 37.970 bytes idéntico byte por byte al TEST08 validado: **EXACT_REBUILD_PASS**.

El paquete fuente original con instrucciones y ejecutables no está todavía cargado como binario independiente en GitHub; el script sí está preservado. Hay que conservar `sound(1).PRG` para reconstruir.
