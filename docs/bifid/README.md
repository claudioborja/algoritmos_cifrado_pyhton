# Cifrado Bifid

[Volver al índice](../../README.md) · [Ver el código](../../21.bifid.py)

## Teoría

Bifid combina un cuadrado de Polibio de 5 × 5 con mezcla de coordenadas.
La clave determina el alfabeto de la tabla y el **período** indica cuántas letras
se procesan juntas. La tabla se llena por filas con la clave sin repetir, seguida
de las letras restantes, uniendo I/J.

Para cada bloque se escriben todas sus filas y después todas sus columnas.
Se toman los números resultantes de dos en dos para obtener letras nuevas.

Con clave `a`, la tabla comienza ABCDE en la primera fila. Para `ABC`, período 3,
las coordenadas internas son (0,0), (0,1), (0,2):

```text
Filas:     0 0 0
Columnas:  0 1 2
Secuencia: 0 0 0 0 1 2
Parejas:   (0,0) (0,0) (1,2) → A A H
```

El resultado es `AAH`. Para descifrar se deshacen las parejas y se divide la
secuencia en dos partes iguales: filas originales y columnas originales.

## Variables principales

| Variable | Significado |
| --- | --- |
| `periodo` | Cantidad máxima de letras de cada bloque. |
| `alfabeto_clave` | Letras de la tabla en orden por filas. |
| `coordenadas` | Parejas de fila y columna de un bloque. |
| `longitud_bloque` | Longitud real del bloque, que puede ser menor que el período. |
| `numeros` | Secuencia de coordenadas que se mezcla o separa. |

## Explicación del código

`transformar_bifid()` exige un período entero positivo y crea la tabla.
Recorre el texto por bloques. Al cifrar concatena `filas + columnas` y reconstruye
letras de cada pareja. Al descifrar aplana las parejas del cifrado y separa la
lista según `longitud_bloque`, no según el período configurado.

`cifrar_bifid()` y `descifrar_bifid()` seleccionan el sentido de esa operación.
El último bloque se procesa sin añadir relleno. Con período 1, cada letra queda
igual después de normalizar.

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
python3 21.bifid.py
```

- Opción 1: texto `ABC`, clave `a`, período `3`; resultado `AAH`.
- Opción 2: texto `AAH`, misma clave y período; resultado `ABC`.
- Opción 3: salir.

## Caracteres y límites

Elimina espacios, devuelve mayúsculas y une I/J. No admite ñ, tildes, signos ni
números. No recupera el formato original. La tabla se llena por filas; una tabla
construida en espiral produciría resultados diferentes.

Es un ejercicio educativo; no debe utilizarse para proteger información confidencial.

## Referencia

[Regla de fraccionamiento Bifid de la ACA](https://www.cryptogram.org/downloads/aca.info/ciphers/Bifid.pdf). La guía describe la variante concreta utilizada en este repositorio.
