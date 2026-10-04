# Cifrado Beaufort

[Volver al índice](../../README.md) · [Ver el código](../../19.beaufort.py)

## Teoría

Beaufort usa una palabra clave repetida, como Vigenère, pero resta el valor del
mensaje al valor de la clave. Este programa utiliza las 27 letras españolas.

```text
posición cifrada = (posición de la clave - posición del mensaje) % 27
```

La misma operación descifra porque `clave - (clave - mensaje)` recupera el
mensaje, módulo 27. Con texto `Hola` y clave `sol`, la clave se repite como `sols`:

| Letra | Valor mensaje | Valor clave | Resultado módulo 27 |
| --- | --- | --- | --- |
| H | 7 | 19 | 12 → M |
| o | 15 | 15 | 0 → a |
| l | 11 | 11 | 0 → a |
| a | 0 | 19 | 19 → s |

El resultado es `Maas`.

## Variables principales

| Variable | Significado |
| --- | --- |
| `posicion_clave` | Número de letras transformadas. |
| `letra_clave` | Letra correspondiente de la clave repetida. |
| `valor_mensaje`, `valor_clave` | Índices en el alfabeto español. |
| `caracteres_resultado` | Lista del mensaje transformado. |

## Explicación del código

`transformar_beaufort()` valida la clave, recorre el mensaje y aplica la resta.
Usa `% len(clave)` para repetirla. Conserva la mayúscula o minúscula de cada
posición y avanza la clave solo cuando transforma una letra del alfabeto.

`cifrar_beaufort()` y `descifrar_beaufort()` llaman a la misma transformación;
no se necesita una fórmula de descifrado diferente.

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
python3 19.beaufort.py
```

- Opción 1: texto `Hola`, clave `sol`; resultado `Maas`.
- Opción 2: texto `Maas`, misma clave; resultado `Hola`.
- Opción 3: salir.

## Caracteres y límites

Cifra la ñ y conserva el formato. Tildes, ü, signos, números, espacios y símbolos
fuera del alfabeto permanecen en su lugar y no consumen clave. La clave debe
contener letras españolas, sin espacios ni tildes.

Es un ejercicio educativo; no debe utilizarse para proteger información confidencial.

## Referencia

[Definición Beaufort de la ACA](https://www.cryptogram.org/downloads/aca.info/ciphers/Beaufort.pdf). La guía describe la variante concreta utilizada en este repositorio.
