# Transposición por columnas

[Volver al índice](../../README.md) · [Ver el código](../../6.transposicion_columnas.py)

## Teoría

Una transposición cambia el orden de los caracteres sin reemplazarlos.
En este algoritmo se escribe el mensaje por filas en una tabla. La cantidad de
columnas es la longitud de una palabra clave. Luego se leen las columnas de
arriba abajo siguiendo el orden alfabético de las letras de la clave.

Con el mensaje `HOLAAMIGO` y la clave `sol`:

```text
Clave:    s o l
          H O L
          A A M
          I G O
```

El orden alfabético de la clave es l, o, s, por lo que se leen las columnas 2, 1
y 0, usando índices que comienzan en cero:

| Columna | Letra clave | Contenido | Orden de lectura |
| --- | --- | --- | --- |
| 0 | s | HAI | 3 |
| 1 | o | OAG | 2 |
| 2 | l | LMO | 1 |

El texto cifrado es `LMOOAGHAI`.

La clave puede repetir letras. En ese caso, las columnas con la misma letra se
leen de izquierda a derecha. Para la clave `casa`, el orden es 1, 3, 0, 2.
Se utiliza el orden del alfabeto español, con la ñ entre n y o.

### Filas incompletas y descifrado

No se añaden caracteres de relleno. Si la última fila está incompleta, las
primeras columnas de la tabla original tienen un carácter más.

Por ejemplo, `HOLA` con clave `sol` forma:

```text
s o l
H O L
A
```

Se leen `L`, `O` y `HA`; el resultado es `LOHA`.

Para descifrar se calculan las longitudes de las columnas, se separa el texto
cifrado en ese orden y se reconstruye la tabla. Finalmente, se lee por filas.
Las columnas adicionales se determinan por su posición original, no por el orden
en que se leyeron para cifrar.

## Explicación del código

### Variables principales

| Variable | Qué representa |
| --- | --- |
| `clave` | Palabra que define la cantidad y el orden de las columnas. |
| `cantidad_columnas` | Longitud de la clave. |
| `orden_columnas` | Índices de las columnas ordenadas por su letra clave. |
| `filas_completas` | Cantidad de filas que contienen todas las columnas. |
| `columnas_con_extra` | Cantidad de columnas con un carácter en la última fila. |
| `longitud_columna` | Número de caracteres que contiene una columna. |
| `inicio_columna`, `fin_columna` | Límites de una columna en el texto cifrado. |
| `posicion_original` | Posición donde se debe colocar un carácter recuperado. |

### Funciones

`validar_clave(clave)` exige una palabra no vacía formada por letras del alfabeto
español, sin espacios ni tildes. Normaliza la clave a minúsculas.

`obtener_orden_columnas(clave)` usa `sorted()` sobre los índices y ordena según
la posición de cada letra en `ALFABETO`. La ordenación estable mantiene de
izquierda a derecha los índices cuyas letras sean iguales.

`cifrar_columnas(texto, clave)` obtiene cada columna con:

```python
texto_columna = texto[columna::cantidad_columnas]
```

Este corte empieza en el índice de la columna y avanza de fila en fila. Después
concatena las columnas en el orden definido por la clave.

`descifrar_columnas(texto_cifrado, clave)` calcula:

```python
filas_completas, columnas_con_extra = divmod(len(texto_cifrado), cantidad_columnas)
```

`divmod()` devuelve el cociente y el resto de la división. Con 4 caracteres y
3 columnas, hay 1 fila completa y 1 columna con un carácter extra.
Para cada columna, separa su contenido del texto cifrado y coloca cada carácter
mediante:

```python
posicion_original = fila * cantidad_columnas + columna
```

La lista reconstruida se une para recuperar el mensaje.

`main()` solicita texto y clave, controla las opciones y muestra los errores de
validación. El bloque `if __name__ == "__main__":` impide que el menú se abra al
importar las funciones.

## Cómo utilizarlo

Desde la raíz del repositorio:

```bash
python3 6.transposicion_columnas.py
```

- Opción 1: texto `HOLAAMIGO`, clave `sol`; resultado `LMOOAGHAI`.
- Opción 2: texto `LMOOAGHAI`, misma clave `sol`; resultado `HOLAAMIGO`.
- Opción 3: salir.

Una clave de una sola letra deja el texto igual. Las claves más largas que el
mensaje también se admiten: algunas columnas quedan vacías.

## Caracteres y límites

Se reordenan todos los caracteres, incluidos los espacios, las tildes, la ñ, los
signos y los números. Ninguno se elimina ni se agrega. Al descifrar se recuperan
exactamente sus posiciones originales, incluidas las mayúsculas.

Los espacios también pueden quedar al inicio o al final del texto cifrado:
consérvalos al copiarlo. El programa no elimina espacios del mensaje.

Las frecuencias de los caracteres permanecen iguales y permiten estudiar
patrones. Este algoritmo es educativo y no protege datos confidenciales.
