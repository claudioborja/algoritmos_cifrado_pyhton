# RSA-OAEP con SHA-256

[Volver al índice](../../README.md) · [Ver el código](../../15.rsa_oaep.py)

## Teoría

RSA utiliza dos claves relacionadas matemáticamente: una pública para cifrar y
una privada para descifrar. La clave pública puede compartirse; la privada y su
contraseña deben mantenerse en secreto.

En términos matemáticos, RSA utiliza un módulo `n` construido a partir de dos
primos grandes, un exponente público `e` y un exponente privado `d`. La operación
básica de cifrado es una potencia modular y la de descifrado utiliza `d`.
Este programa no aplica esa operación directamente al texto: usa **OAEP**, una
codificación aleatoria del mensaje que se realiza antes de la operación RSA.

OAEP emplea funciones hash y máscaras para preparar el mensaje. Aquí se usa
SHA-256 tanto para OAEP como para MGF1, su función de generación de máscaras.
El mismo mensaje puede producir cifrados diferentes con la misma clave pública.

### Límite de longitud

RSA-OAEP admite mensajes pequeños. La longitud máxima en bytes se calcula como:

```text
máximo = bytes del módulo RSA - 2 × bytes del hash - 2
Con RSA de 2048 bits y SHA-256: 256 - 2 × 32 - 2 = 190 bytes
```

Se cuentan bytes UTF-8, no letras. Una ñ necesita dos bytes. Los mensajes que
superan ese límite se rechazan explícitamente. Este programa no divide el mensaje
en bloques RSA: para datos extensos se utiliza normalmente un esquema híbrido,
donde RSA protege una clave simétrica y esa clave cifra el contenido.

## Explicación del código

Las funciones RSA se definen en [utilidades_rsa.py](../../utilidades_rsa.py),
compartidas con el cifrado híbrido. El archivo `15.rsa_oaep.py` las importa y
contiene el menú. Sus nombres y parámetros se mantienen disponibles al importarlo.

| Variable | Significado |
| --- | --- |
| `clave_privada` | Objeto RSA que permite descifrar. |
| `clave_publica` | Objeto RSA que permite cifrar. |
| `datos` | Mensaje codificado en UTF-8. |
| `longitud_maxima` | Cantidad de bytes que OAEP admite con esa clave. |
| `contrasena` | Bytes usados para proteger el archivo privado. |
| `datos_privados`, `datos_publicos` | Claves serializadas en formato PEM. |
| `ruta_privada`, `ruta_publica` | Archivos donde se guardan las claves. |

`generar_claves()` crea una clave privada de 2048 bits y exponente público 65537.
Obtiene la pública mediante `clave_privada.public_key()`.

`crear_relleno_oaep()` configura la misma codificación para cifrado y descifrado:

```python
padding.OAEP(
    mgf=padding.MGF1(algorithm=hashes.SHA256()),
    algorithm=hashes.SHA256(),
    label=None,
)
```

`cifrar_rsa()` comprueba que la clave sea RSA de al menos 2048 bits, valida la
longitud, llama a `encrypt()` y representa los bytes en Base64.
`descifrar_rsa()` convierte desde Base64, llama a `decrypt()` y recupera UTF-8.
Un mensaje alterado o una clave incorrecta provocan un error.

`guardar_claves()` exige una contraseña y una carpeta nueva. Guarda la privada
en PKCS8 PEM cifrado mediante `BestAvailableEncryption()` y la pública en PEM.
En sistemas Unix crea la carpeta con permisos 700 y el archivo privado con 600.
No sobrescribe una carpeta existente. El repositorio ignora archivos `*.pem`.

`cargar_clave_publica()` y `cargar_clave_privada()` leen archivos PEM y comprueban
que contengan claves RSA. La privada se abre con la contraseña correspondiente.

`main()` usa `getpass.getpass()` para que la contraseña no se muestre mientras se
escribe en una terminal. Captura errores de claves, contraseñas y archivos.
El bloque `if __name__ == "__main__":` permite importar sin abrir el menú.
Las conversiones Base64 proceden de
[utilidades_cifrado.py](../../utilidades_cifrado.py).

## Instalación y uso

Desde la raíz del repositorio, con Python 3.10 o posterior:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 15.rsa_oaep.py
```

Si ya tienes el entorno y la biblioteca instalados, ejecuta únicamente el programa.

1. Opción 1: indica una carpeta nueva, por ejemplo `claves_rsa`, y una contraseña.
   Se crean `clave_privada.pem` y `clave_publica.pem` dentro de ella.
2. Opción 2: indica `claves_rsa/clave_publica.pem` y el texto `Hola, ñá 😀`.
   Copia el mensaje cifrado Base64.
3. Opción 3: indica `claves_rsa/clave_privada.pem`, su contraseña y el mensaje
   cifrado. Recuperarás `Hola, ñá 😀`.
4. Opción 4: salir.

Solo comparte la clave pública y el mensaje cifrado. El programa no recupera una
contraseña olvidada ni una clave privada perdida.

## Caracteres y límites

Acepta texto UTF-8, incluidos tildes, ñ, espacios y emoji, respetando el límite
de bytes. También admite el mensaje vacío.

RSA-OAEP proporciona cifrado, pero no acredita quién envió el mensaje: cualquier
persona con la clave pública puede cifrar. Las firmas digitales son una operación
diferente. Esta demostración no implementa certificados ni distribución de claves.

## Referencias

Las APIs de generación, cifrado y serialización se explican en la
[documentación oficial de RSA de cryptography](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/).

El formato OAEP y el límite de longitud se definen en
[RFC 8017, sección 7.1](https://www.rfc-editor.org/rfc/rfc8017.html#section-7.1).
