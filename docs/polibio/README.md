# Cuadrado de Polibio

[Volver al índice](../../README.md) · [Ver el código](../../17.polibio.py)

## Teoría

Polibio representa cada letra con sus coordenadas en una tabla de 5 × 5.
Se construye la tabla escribiendo las letras de la clave sin repetir y luego
las restantes del alfabeto. I y J comparten la casilla I.

Con clave `clave`:

```text
    1 2 3 4 5
1   C L A V E
2   B D F G H
3   I K M N O
4   P Q R S T
5   U W X Y Z
```

El primer dígito indica la fila y el segundo la columna. H está en fila 2,
columna 5, y se convierte en 25. `Hola` produce `25 35 12 13`.
Para recuperar una letra se busca su casilla.

## Variables principales

| Variable | Significado |
| --- | --- |
| `alfabeto_clave` | Las 25 letras de la tabla en orden por filas. |
| `fila`, `columna` | Coordenadas de cada letra; internamente empiezan en cero. |
| `coordenadas` | Parejas de dígitos que se muestran separadas por espacios. |
| `digitos` | Cifrado sin espacios, que se procesa de dos en dos. |

## Explicación del código

`cifrar_polibio()` prepara la tabla y normaliza el mensaje. Calcula la posición
con `.index()` y sus coordenadas con `divmod(posicion, 5)`. Suma 1 a cada
coordenada para mostrar dígitos entre 1 y 5.

`descifrar_polibio()` elimina los espacios del cifrado, exige una cantidad par
de dígitos entre 1 y 5 y obtiene cada letra mediante `fila * 5 + columna`.
Se pueden introducir coordenadas con o sin separadores.

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
python3 17.polibio.py
```

- Opción 1: texto `Hola`, clave `clave`; resultado `25 35 12 13`.
- Opción 2: coordenadas `25 35 12 13`, misma clave; resultado `HOLA`.
- Opción 3: salir.

## Caracteres y límites

Elimina espacios, devuelve mayúsculas y transforma J en I. No recupera el formato
original. No admite ñ, tildes, números ni signos en el mensaje original.
El cifrado vacío representa el texto vacío. Una coordenada como 06 se rechaza.

Es un ejercicio educativo; no debe utilizarse para proteger información confidencial.
