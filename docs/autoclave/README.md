# Vigenère Autoclave — Autokey

[Volver al índice](../../README.md) · [Ver el código](../../20.autoclave.py)

## Teoría

Esta variante de Vigenère comienza con una clave y la extiende con las letras
del propio mensaje original. La clave inicial no se repite indefinidamente.
Se utiliza el alfabeto español de 27 letras.

Con texto `Hola` y clave `sol`, la secuencia que se necesita es `solh`: después
de las tres letras iniciales se utiliza la primera letra del mensaje.

```text
Cifrar:    resultado = (mensaje + clave) % 27
Descifrar: resultado = (cifrado - clave) % 27
```

Los primeros resultados coinciden con Vigenère, pero cambian al terminar la clave
inicial. `Hola` con `sol` produce `Zdvh`.
Para descifrar se extiende la clave con las letras originales que se van
recuperando, nunca con las letras cifradas.

## Variables principales

| Variable | Significado |
| --- | --- |
| `valores_clave` | Lista de índices de la clave inicial y del mensaje original. |
| `posicion_clave` | Siguiente elemento de la lista que debe utilizarse. |
| `valor_entrada` | Índice de la letra original o cifrada. |
| `valor_resultado` | Índice después de sumar o restar. |
| `descifrar` | Indica cuál de las dos operaciones se está realizando. |

## Explicación del código

`transformar_autoclave()` valida la clave y construye una lista con sus valores.
Al cifrar, añade `valor_entrada` a esa lista. Al descifrar, añade el valor recién
recuperado. La lista siempre tiene disponible la siguiente letra de la clave.

`cifrar_autoclave()` utiliza la suma. `descifrar_autoclave()` activa la resta con
`descifrar=True`. Ambos conservan el formato y saltan los caracteres ajenos al
alfabeto sin avanzar la clave.

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
python3 20.autoclave.py
```

- Opción 1: texto `Hola`, clave `sol`; resultado `Zdvh`.
- Opción 2: texto `Zdvh`, misma clave; resultado `Hola`.
- Opción 3: salir.

## Caracteres y límites

Cifra la ñ, conserva mayúsculas y deja tildes, ü, signos y espacios en su lugar.
La clave inicial debe ser no vacía y contener solo letras españolas. La variante
implementada usa el texto original para extender la clave; otras variantes pueden
usar reglas diferentes.

Es un ejercicio educativo; no debe utilizarse para proteger información confidencial.

## Referencia

[Autokey de la ACA](https://www.cryptogram.org/downloads/aca.info/ciphers/Autokey.pdf). La guía describe la variante concreta utilizada en este repositorio.
