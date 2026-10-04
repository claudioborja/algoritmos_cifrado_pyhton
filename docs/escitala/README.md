# Escítala

[Volver al índice](../../README.md) · [Ver el código](../../16.escitala.py)

## Teoría

La escítala puede representarse mediante una transposición sobre una tabla.
Esta implementación escribe el mensaje por filas y lee por columnas en su orden
original. La clave es la **cantidad de columnas**, no una palabra.

Con `HOLAAMIGO` y 3 columnas:

```text
H O L
A A M
I G O
```

Las columnas son HAI, OAG y LMO, por lo que el resultado es `HAIOAGLMO`.
No se añade relleno. Una última fila incompleta produce columnas de longitudes
diferentes. Esta convención debe utilizarse también al descifrar.

## Variables principales

| Variable | Significado |
| --- | --- |
| `cantidad_columnas` | Ancho de la tabla y clave numérica. |
| `filas_completas` | Filas que contienen todas las columnas. |
| `columnas_con_extra` | Columnas con un carácter más en la última fila. |
| `inicio_columna` | Lugar donde comienza una columna en el cifrado. |
| `caracteres_originales` | Lista donde se reconstruye el mensaje. |

## Explicación del código

`cifrar_escitala()` valida la clave y obtiene cada columna con
`texto[columna::cantidad_columnas]`. Une las columnas de izquierda a derecha.

`descifrar_escitala()` utiliza `divmod()` para calcular la longitud de cada
columna. Reparte el cifrado y devuelve cada carácter a la posición
`fila * cantidad_columnas + columna`.

El número de columnas debe ser un entero positivo. Se recorren como máximo
tantas columnas como caracteres para evitar crear columnas vacías innecesarias.

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
python3 16.escitala.py
```

- Opción 1: texto `HOLAAMIGO`, columnas `3`; resultado `HAIOAGLMO`.
- Opción 2: texto `HAIOAGLMO`, columnas `3`; resultado `HOLAAMIGO`.
- Opción 3: salir.

## Caracteres y límites

Conserva todos los caracteres, incluidas tildes, ñ, espacios y emoji, pero cambia
su posición. Una columna, un texto vacío o más columnas que caracteres dejan
el mensaje igual. Conserva los espacios iniciales y finales al copiar el cifrado.

Es un ejercicio educativo; no debe utilizarse para proteger información confidencial.
