# ChaCha20-Poly1305

[Volver al índice](../../README.md) · [Ver el código](../../14.chacha20_poly1305.py)

## Teoría

ChaCha20 genera un flujo de bytes a partir de una clave de 256 bits, un nonce
y un contador. Sus rondas combinan sumas, XOR y rotaciones de bits. El flujo se
combina con el mensaje mediante XOR. Poly1305 calcula una etiqueta de
autenticación que permite detectar cambios en los datos.

Es un cifrado simétrico: se usa la misma clave secreta para cifrar y descifrar.
También es un cifrado autenticado: una clave incorrecta o un paquete alterado
provocan un error de autenticación antes de devolver el mensaje.

Cada cifrado utiliza un **nonce** nuevo de 12 bytes. Es un dato público que
acompaña al mensaje y no debe repetirse con la misma clave. Aquí se genera con
`secrets.token_bytes(12)`. La aleatoriedad hace improbable una repetición, pero
no constituye un registro de nonces ni una garantía para cantidades ilimitadas
de mensajes.

Los datos asociados se autentican, pero no se cifran. En esta demostración son
una etiqueta fija del programa y la versión del formato. El descifrado debe
utilizar esa misma etiqueta.

## Formato del resultado

El programa devuelve una cadena Base64 con estos bytes:

```text
nonce de 12 bytes | mensaje cifrado | etiqueta de autenticación de 16 bytes
```

La biblioteca agrega la etiqueta al mensaje cifrado. La clave no se incluye en
el paquete; se muestra por separado y debe conservarse en secreto. Base64 solo
permite representar los bytes como texto, no agrega protección.

## Explicación del código

| Variable | Significado |
| --- | --- |
| `clave` | Los 32 bytes secretos utilizados para cifrar y descifrar. |
| `LONGITUD_NONCE` | Constante con el valor 12. |
| `DATOS_ASOCIADOS` | Etiqueta fija autenticada del programa. |
| `nonce` | Valor público nuevo para cada cifrado. |
| `cifrador` | Objeto de la biblioteca que realiza la operación criptográfica. |
| `datos_cifrados` | Mensaje cifrado con su etiqueta de autenticación. |
| `paquete` | Bytes obtenidos al decodificar el resultado Base64. |

`generar_clave()` obtiene bytes criptográficos mediante:

```python
return ChaCha20Poly1305.generate_key()
```

`validar_clave()` exige exactamente 32 bytes. Una palabra o contraseña no se
acepta directamente como clave.

`cifrar_chacha20()` valida la clave, genera el nonce, convierte el texto a UTF-8
y llama a `encrypt()`. Después concatena el nonce y el resultado antes de
codificarlos en Base64.

`descifrar_chacha20()` valida la clave y el paquete, separa los primeros 12 bytes
como nonce y llama a `decrypt()`. Captura `InvalidTag` para explicar que la clave
es incorrecta o el paquete fue modificado. Convierte a UTF-8 solo tras autenticar.

Las conversiones se definen en
[utilidades_cifrado.py](../../utilidades_cifrado.py).
`main()` solicita el mensaje y permite generar una clave al dejar el campo vacío.
La opción de descifrado requiere la clave original. El bloque
`if __name__ == "__main__":` impide abrir el menú durante la importación.

Las rondas y operaciones internas se delegan a `cryptography`; este archivo
explica cómo utilizar la biblioteca sin reimplementarlas manualmente.

## Instalación y uso

Desde la raíz del repositorio, con Python 3.10 o posterior:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 14.chacha20_poly1305.py
```

Si ya tienes el entorno y la biblioteca instalados, ejecuta únicamente el programa.

1. Elige la opción 1 e introduce `Hola, ñá 😀`.
2. Deja la clave vacía para generar una nueva.
3. Copia el paquete Base64 y conserva la clave aparte.
4. Elige la opción 2 e introduce ambos valores; recuperarás `Hola, ñá 😀`.
5. Usa la opción 3 para salir.

El resultado cambia en cada ejecución porque el nonce es nuevo, incluso si
utilizas la misma clave y el mismo mensaje.

## Caracteres y límites

Admite cualquier texto UTF-8, incluidos espacios, tildes, ñ, emoji y mensajes
vacíos. Recupera exactamente el mensaje aceptado.

La etiqueta comprueba integridad con la clave compartida; no es una firma digital
ni identifica a una persona. Este menú educativo muestra las claves en pantalla
y no implementa almacenamiento seguro, distribución de claves ni un protocolo
completo para una aplicación real.

## Referencias

La interfaz, los tamaños y la verificación de etiquetas se describen en la
[documentación oficial de cifrado autenticado de cryptography](https://cryptography.io/en/latest/hazmat/primitives/aead/).

[Especificación ChaCha20-Poly1305, RFC 8439](https://www.rfc-editor.org/rfc/rfc8439.html) explica el algoritmo subyacente.
