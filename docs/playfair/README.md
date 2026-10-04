# Cifrado Playfair

[Volver al índice](../../README.md) · [Ver el código](../../9.playfair.py)

## Teoría

Playfair cifra parejas de letras utilizando una tabla de 5 × 5. Se escribe la
clave sin letras repetidas y se completan las casillas con el resto del alfabeto.
Para que las 26 letras entren en 25 casillas, I y J comparten la letra I.

Con clave `clave`, la tabla es:

```text
C L A V E
B D F G H
I K M N O
P Q R S T
U W X Y Z
```

Antes de cifrar se prepara el texto: se convierte a mayúsculas, se eliminan los
espacios y se reemplaza J por I. Si una pareja contiene dos letras iguales, se
inserta X entre ellas. Si queda una letra al final, se añade X. Cuando la letra
que necesita relleno es X, se utiliza Q para evitar la pareja XX.

Ejemplo: `BALLOON` se prepara como `BA LX LO ON`, es decir, `BALXLOON`.

Para transformar cada pareja se aplican estas reglas:

| Ubicación de las dos letras | Al cifrar | Al descifrar |
| --- | --- | --- |
| Misma fila | Una casilla a la derecha. | Una casilla a la izquierda. |
| Misma columna | Una casilla hacia abajo. | Una casilla hacia arriba. |
| Filas y columnas diferentes | Cada letra toma la columna de la otra, manteniendo su fila. | La misma regla del rectángulo. |

En los bordes se vuelve al extremo contrario usando `% 5`.
Con `Hola` y clave `clave`, las parejas HO y LA producen OT y AV: `OTAV`.

## Explicación del código

| Variable | Significado |
| --- | --- |
| `ALFABETO` | Las 25 letras de la tabla, sin J. |
| `letras_unicas` | Letras de la clave y del alfabeto sin repetir. |
| `tabla` | Lista de cinco filas con cinco letras cada una. |
| `parejas` | Grupos de dos letras del texto preparado. |
| `relleno` | X, o Q cuando la primera letra es X. |
| `posiciones_letras` | Diccionario que relaciona cada letra con su fila y columna. |
| `direccion` | 1 para cifrar; -1 para descifrar. |

`normalizar_texto()` valida las letras, elimina espacios y une I/J. No acepta ñ,
tildes, números ni signos para evitar conversiones ambiguas adicionales.

`crear_tabla()` normaliza la clave y agrega sus letras una sola vez, seguidas de
las letras faltantes. Divide el resultado en filas de cinco casillas.

`preparar_texto()` avanza por el mensaje formando parejas. Avanza solo una letra
cuando inserta relleno para que la segunda letra repetida se procese después.

`transformar_parejas()` busca las posiciones y elige la regla de fila, columna o
rectángulo. En el caso de una fila utiliza, por ejemplo:

```python
letras_resultado.append(tabla[fila_primera][(columna_primera + direccion) % 5])
```

`cifrar_playfair()` prepara el texto y transforma con dirección 1.
`descifrar_playfair()` exige una cantidad par de letras y transforma con dirección
-1. No acepta J en un mensaje cifrado, porque no existe en la tabla.

`main()` muestra el menú y las restricciones. El bloque `if __name__ == "__main__":`
mantiene el menú inactivo cuando se importa el módulo.

## Uso y ejemplo

Desde la raíz del repositorio:

```bash
python3 9.playfair.py
```

- Opción 1: texto `Hola`, clave `clave`; resultado `OTAV`.
- Opción 2: texto `OTAV`, misma clave; resultado preparado `HOLA`.
- Opción 3: salir.

## Normalización y límites

El descifrado recupera el **texto preparado**, no el formato original. No restaura
espacios, minúsculas ni J. Tampoco elimina X o Q automáticamente: podrían ser
letras reales del mensaje. Por ejemplo, un mensaje con letras repetidas conserva
el relleno al descifrar. El programa explica este comportamiento antes del menú.

Este cifrado es educativo y no protege información confidencial.
