# Cifrado Bacon de 26 letras

[Volver al índice](../../README.md) · [Ver el código](../../18.bacon.py)

## Teoría

Cada letra se representa con un grupo de cinco símbolos A/B. En esta variante
se asignan los valores de 0 a 25 a las letras A-Z y se escriben en binario con
cinco bits. Cada 0 se representa con A y cada 1 con B.

| Letra | Valor | Bits | Grupo |
| --- | --- | --- | --- |
| A | 0 | 00000 | AAAAA |
| B | 1 | 00001 | AAAAB |
| C | 2 | 00010 | AAABA |
| Z | 25 | 11001 | BBAAB |

La versión histórica de 24 letras combina I/J y U/V. Este programa utiliza la
variante de **26 letras separadas**, de modo que I, J, U y V conservan su identidad.
No oculta los símbolos dentro de otro texto: muestra directamente los grupos.

## Variables principales

| Variable | Significado |
| --- | --- |
| `bits` | Representación binaria de cinco posiciones. |
| `grupos` | Lista de grupos A/B del mensaje. |
| `simbolos` | Cifrado normalizado sin espacios. |
| `posicion` | Número recuperado a partir de un grupo binario. |

## Explicación del código

`cifrar_bacon()` normaliza las letras y usa `format(posicion, "05b")` para obtener
cinco bits. Reemplaza 0 por A y 1 por B, y separa los grupos con espacios.

`descifrar_bacon()` admite solo A/B y espacios. Exige grupos de cinco símbolos,
invierte los reemplazos y usa `int(bits, 2)` para recuperar el índice. Rechaza
los valores 26 a 31 porque no corresponden a ninguna letra de esta variante.

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
python3 18.bacon.py
```

- Opción 1: texto `ABCZ`; resultado `AAAAA AAAAB AAABA BBAAB`.
- Opción 2: los mismos grupos; resultado `ABCZ`.
- Opción 3: salir. No se solicita clave.

## Caracteres y límites

Devuelve mayúsculas y elimina los espacios del mensaje original. No admite ñ,
tildes, números ni signos. Permite texto vacío. La representación A/B es fija y
no mantiene secreto un mensaje por sí sola.

Es un ejercicio educativo; no debe utilizarse para proteger información confidencial.

## Referencia

[Bacon histórico de la ACA](https://www.cryptogram.org/downloads/aca.info/ciphers/Baconian.pdf). La guía describe la variante concreta utilizada en este repositorio.
