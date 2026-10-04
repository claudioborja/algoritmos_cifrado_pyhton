# Rail Fence: cifrado en zigzag

[Volver al índice](../../README.md) · [Ver el código](../../7.rail_fence.py)

## Teoría

Rail Fence es una transposición: cambia el orden de los caracteres sin
sustituirlos. Escribe el mensaje en zigzag entre varias filas llamadas **rieles**.
La clave es la cantidad de rieles.

El recorrido comienza en el riel superior, baja hasta el último y vuelve a subir.
Al cifrar, se lee cada riel de izquierda a derecha, empezando por el superior.
Esta implementación comienza siempre arriba y bajando, sin desplazamiento inicial.

Con el texto `HOLAAMIGO` y 3 rieles:

```text
Posición: 0 1 2 3 4 5 6 7 8
Riel 0:   H       A       O
Riel 1:     O   A   M   G
Riel 2:       L       I
```

| Riel | Posiciones del texto | Contenido |
| --- | --- | --- |
| 0 | 0, 4, 8 | HAO |
| 1 | 1, 3, 5, 7 | OAMG |
| 2 | 2, 6 | LI |

Al unir los rieles se obtiene `HAOOAMGLI`.

Para descifrar se reconstruye el mismo recorrido. Se cuentan las posiciones de
cada riel, se divide el texto cifrado en segmentos de esas longitudes y se leen
los caracteres siguiendo de nuevo el zigzag.

Con 3 rieles, el recorrido de este ejemplo es:

```text
0, 1, 2, 1, 0, 1, 2, 1, 0
```

Los segmentos del texto cifrado son `HAO`, `OAMG` y `LI`. Tomar un carácter del
riel indicado en cada paso recupera `HOLAAMIGO`.

## Explicación del código

### Variables principales

| Variable | Qué representa |
| --- | --- |
| `cantidad_rieles` | Número de filas que se utilizan como clave. |
| `recorrido` | Lista del riel al que pertenece cada posición del mensaje. |
| `riel_actual` | Riel donde se coloca el siguiente carácter. |
| `direccion` | Valor 1 para bajar o -1 para subir. |
| `rieles` | Contenido de cada fila. |
| `cantidades_por_riel` | Cantidad de caracteres que se debe asignar a cada riel. |
| `inicio_riel`, `fin_riel` | Límites de un segmento dentro del texto cifrado. |
| `posiciones_por_riel` | Siguiente índice que se leerá de cada riel al descifrar. |
| `caracteres_originales` | Lista que acumula el mensaje recuperado. |

### Funciones

`validar_cantidad_rieles(cantidad_rieles)` exige un entero mayor o igual que 1.
Rechaza cero, negativos y valores de otros tipos.

`obtener_recorrido(longitud_texto, cantidad_rieles)` guarda el riel de cada
posición. En el riel superior establece `direccion = 1`; en el inferior establece
`direccion = -1`. Después actualiza `riel_actual` con esa dirección.

`cifrar_rail_fence(texto, cantidad_rieles)` crea una lista por riel y distribuye
los caracteres con:

```python
for caracter, riel in zip(texto, recorrido):
    rieles[riel].append(caracter)
```

`zip()` asocia cada carácter con su riel. Finalmente, se unen los caracteres de
cada riel y se concatenan todos los rieles.

`descifrar_rail_fence(texto_cifrado, cantidad_rieles)`:

1. Calcula el mismo recorrido que se utilizó para cifrar.
2. Cuenta cuántos caracteres corresponden a cada riel.
3. Divide el texto cifrado en segmentos con esas longitudes.
4. Recorre el zigzag tomando el siguiente carácter de cada riel:

   ```python
   posicion_en_riel = posiciones_por_riel[riel]
   caracteres_originales.append(rieles[riel][posicion_en_riel])
   posiciones_por_riel[riel] += 1
   ```

5. Une los caracteres para devolver el mensaje original.

Ambas funciones devuelven directamente el texto si hay un solo riel o si hay
tantos rieles como caracteres, o más. En esos casos el orden no cambia, y se
evita crear filas innecesarias. El texto vacío también se admite con una clave válida.

`main()` convierte la entrada con `int()` y muestra un mensaje si no es un entero
positivo. El bloque `if __name__ == "__main__":` permite importar las funciones
sin ejecutar el menú.

## Cómo utilizarlo

Desde la raíz del repositorio:

```bash
python3 7.rail_fence.py
```

- Opción 1: texto `HOLAAMIGO`, cantidad de rieles `3`; resultado `HAOOAMGLI`.
- Opción 2: texto `HAOOAMGLI`, cantidad de rieles `3`; resultado `HOLAAMIGO`.
- Opción 3: salir.

Para que el ejemplo se recupere correctamente, utiliza los mismos 3 rieles al
descifrar. Entradas como `abc`, `0` o `-2` muestran un error y vuelven al menú.

## Caracteres y límites

Se reordenan también espacios, tildes, ñ, signos y números, conservando todos
los caracteres y sus mayúsculas. No se añade relleno. Los espacios que queden al
inicio o al final del mensaje cifrado deben conservarse al copiarlo.

La cantidad de rieles puede probarse para intentar recuperar un mensaje.
Rail Fence es educativo y no debe usarse para proteger información confidencial.
