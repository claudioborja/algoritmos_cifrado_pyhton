# Cifrado ADFGVX

[Volver al índice](../../README.md) · [Ver el código](../../23.adfgvx.py)

## Teoría

ADFGVX combina sustitución por coordenadas y transposición. Utiliza una tabla
6 × 6 con las letras A-Z y los dígitos 0-9. Las filas y columnas se identifican
con los símbolos A, D, F, G, V y X.

Se necesitan dos claves: una para construir la tabla y otra para ordenar las
columnas de la transposición. La clave de la tabla se escribe sin repetir y se
completa con los símbolos restantes.

Con clave de tabla `ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`, A produce AA,
B produce AD y C produce AF. Por tanto, `ABC` produce inicialmente `AAADAF`.
Con clave de columnas `ba`:

```text
b a
A A
A D
A F
```

Se lee primero la columna a, ADF, y después la b, AAA. El resultado es `ADFAAA`.
El descifrado invierte primero la transposición y luego las coordenadas.

## Variables principales

| Variable | Significado |
| --- | --- |
| `SIMBOLOS` | ADFGVX: etiquetas de filas y columnas. |
| `alfabeto_clave` | Letras y números de la tabla. |
| `clave_columnas` | Palabra que define el orden de lectura de columnas. |
| `orden_columnas` | Índices ordenados por las letras de esa palabra. |
| `columnas_con_extra` | Columnas originales con un carácter adicional. |
| `coordenadas` | Mensaje intermedio antes o después de la transposición. |

## Explicación del código

`obtener_orden_columnas()` ordena índices por el alfabeto español. Los empates
se mantienen de izquierda a derecha.

`transponer_columnas()` lee columnas al cifrar. Al descifrar calcula sus longitudes
con `divmod()` y vuelve a colocar los caracteres en su posición por filas.

`cifrar_adfgvx()` convierte las posiciones en parejas ADFGVX y transpone.
`descifrar_adfgvx()` acepta solo esos seis símbolos, exige una cantidad par,
deshace las columnas y recupera cada casilla de la tabla.
No añade relleno aunque la última fila esté incompleta.

La validación y preparación de alfabetos se encuentran en
[utilidades_clasicas.py](../../utilidades_clasicas.py). Las funciones compartidas
comprueban caracteres, convierten a mayúsculas cuando corresponde y eliminan
repeticiones de las claves para construir tablas.

`main()` solicita el mensaje y los parámetros, muestra errores de entrada y vuelve
al menú. El bloque `if __name__ == "__main__":` permite importar las funciones
sin abrir una sesión interactiva.

## Uso y ejemplo

Desde la raíz del repositorio:

```bash
python3 23.adfgvx.py
```

- Opción 1: texto `ABC`, clave de tabla `ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`,
  clave de columnas `ba`; resultado `ADFAAA`.
- Opción 2: texto `ADFAAA` y las mismas dos claves; resultado `ABC`.
- Opción 3: salir.

## Caracteres y límites

El mensaje admite A-Z y 0-9, elimina espacios y devuelve mayúsculas. No admite
ñ, tildes ni signos. I y J son diferentes. La clave de columnas admite ñ, pero
no espacios ni tildes. La clave de tabla admite letras latinas y números.

Es un ejercicio educativo; no debe utilizarse para proteger información confidencial.

## Referencia

[Explicación ADFGVX de CrypTool](https://legacy.cryptool.org/en/cto/adfg-v-x). La guía describe la variante concreta utilizada en este repositorio.
