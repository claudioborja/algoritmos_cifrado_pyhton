# Vernam y libreta de un solo uso

[Volver al índice](../../README.md) · [Ver el código](../../11.vernam.py)

## Teoría

Esta implementación de Vernam combina cada byte del mensaje con un byte de clave
mediante XOR. En Python, XOR se escribe `^`: dos bits iguales dan 0 y dos bits
diferentes dan 1.

```text
byte cifrado = byte original XOR byte de clave
byte original = byte cifrado XOR byte de clave
```

Aplicar la misma clave dos veces deshace la operación porque cada bit de la
clave se cancela. Por ejemplo, el byte de H es 72; con un byte de clave 1 se
obtiene 73, y `73 ^ 1` vuelve a dar 72.

La variante de libreta de un solo uso requiere una clave aleatoria, secreta,
independiente del mensaje, de igual longitud y utilizada una única vez. El
programa obtiene bytes del generador criptográfico del sistema con `secrets`;
esto es una demostración práctica y no una prueba de aleatoriedad perfecta.

Reutilizar una clave revela relaciones entre los mensajes. XOR tampoco detecta
modificaciones: una clave incorrecta puede producir otro texto aparentemente
válido. No debe asumirse autenticidad aunque el resultado pueda leerse.

## Explicación del código

| Variable | Significado |
| --- | --- |
| `longitud_bytes` | Cantidad de bytes de la clave. |
| `datos` | Mensaje convertido a UTF-8. |
| `clave` | Bytes secretos, tantos como bytes del mensaje. |
| `byte_dato`, `byte_clave` | Pareja de bytes que se combina con XOR. |
| `datos_originales` | Bytes recuperados antes de decodificar UTF-8. |

`generar_clave()` usa `secrets.token_bytes(longitud_bytes)`.
`aplicar_xor()` valida la longitud exacta de la clave y combina los bytes:

```python
return bytes(byte_dato ^ byte_clave for byte_dato, byte_clave in zip(datos, clave))
```

`cifrar_vernam()` convierte el texto a UTF-8, aplica XOR y representa el resultado
en Base64 para poder copiarlo como texto.
`descifrar_vernam()` decodifica Base64, aplica XOR y convierte los bytes a UTF-8.
Si esa conversión falla, muestra un error; no garantiza detectar una clave incorrecta.

Las funciones `codificar_base64()` y `decodificar_base64()` proceden de
[utilidades_cifrado.py](../../utilidades_cifrado.py). Base64 es una representación
transportable de bytes y **no es un cifrado adicional**.

`main()` genera una clave nueva en cada cifrado y muestra el mensaje cifrado y
la clave por separado. El programa no guarda claves ni impide que una persona
las reutilice fuera de ese flujo. El bloque `if __name__ == "__main__":` permite
importar sin abrir el menú.

## Uso y ejemplo

Desde la raíz del repositorio:

```bash
python3 11.vernam.py
```

- Opción 1: introduce el mensaje; copia el resultado y guarda su clave aparte.
- Opción 2: introduce el resultado Base64 y la clave correspondiente.
- Opción 3: salir.

Ejemplo reproducible solo para entender la operación: con el texto `Hola` y los
bytes de clave `[1, 2, 3, 4]`, el resultado es `SW1vZQ==` y la clave Base64 es
`AQIDBA==`. Esta clave fija no debe utilizarse para proteger mensajes.

## Caracteres y límites

Admite tildes, ñ, signos, espacios y emoji. La longitud se calcula en **bytes
UTF-8**, no en letras: ñ ocupa dos bytes y muchos emoji ocupan cuatro.
Un texto vacío admite una clave vacía; un mensaje no vacío requiere una clave
de la longitud exacta. La distribución y conservación de claves son responsabilidad
de quien use la demostración.

## Referencia

La operación de libreta de un solo uso y sus condiciones se presentan en el
[Handbook of Applied Cryptography, capítulo 7](https://cacr.uwaterloo.ca/hac/about/chap7.pdf).
