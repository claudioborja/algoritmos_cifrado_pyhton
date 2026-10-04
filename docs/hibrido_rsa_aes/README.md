# Cifrado híbrido RSA-OAEP + AES-GCM

[Volver al índice](../../README.md) · [Ver el código](../../26.hibrido_rsa_aes.py)

## Teoría

Un cifrado híbrido combina claves públicas y cifrado simétrico. Para cada mensaje
se genera una clave AES de 256 bits. AES-GCM cifra y autentica todo el texto.
RSA-OAEP cifra únicamente esa clave de 32 bytes, usando la pública del receptor.

```text
Texto → AES-GCM con clave nueva → datos cifrados y etiqueta
Clave AES → RSA-OAEP con clave pública → clave cifrada
Ambos resultados + nonce + versión → paquete JSON
```

Al descifrar, la clave privada RSA recupera la clave AES. Luego AES-GCM comprueba
la etiqueta y recupera el texto. El contenido no está limitado a los 190 bytes del
ejemplo RSA directo porque RSA solo procesa la clave AES.

El nonce tiene 12 bytes y se genera automáticamente. La clave AES también cambia
en cada mensaje. La cabecera se utiliza como datos asociados: queda visible, pero
se autentica junto con el contenido. Este formato pertenece a esta demostración;
no es un estándar de intercambio como JWE.

## Formato JSON

| Campo | Contenido |
| --- | --- |
| `version` | Entero 1, versión del formato. |
| `algoritmo` | Identificador fijo `RSA-OAEP-SHA256+AES-256-GCM`. |
| `clave_cifrada` | Clave AES cifrada con RSA y representada en Base64. |
| `nonce` | Los 12 bytes del nonce en Base64. |
| `datos` | Contenido AES-GCM con su etiqueta de 16 bytes, en Base64. |

La clave AES original y la clave privada RSA no aparecen en el paquete.
Base64 representa los bytes y no agrega un cifrado adicional.

## Variables principales

| Variable | Significado |
| --- | --- |
| `clave_simetrica` | Clave AES nueva de 32 bytes. |
| `clave_cifrada` | Resultado de proteger esa clave con RSA-OAEP. |
| `nonce` | Valor público usado por AES-GCM. |
| `cabecera` | Metadatos y clave cifrada que se autentican. |
| `datos_asociados` | JSON de cabecera codificado de forma uniforme. |
| `paquete` | Diccionario con los cinco campos del mensaje. |

## Explicación del código

`obtener_datos_asociados()` serializa versión, algoritmo y clave cifrada con claves
ordenadas y separadores fijos. Esto produce los mismos bytes al cifrar y descifrar,
aunque cambie el orden visual de los campos del paquete.

`cifrar_hibrido()` valida la clave RSA, genera una clave AES y cifra sus bytes con
OAEP y SHA-256. Genera el nonce, prepara la cabecera y llama a `AESGCM.encrypt()`
con el texto UTF-8. Devuelve todos los campos como JSON de una sola línea.

`validar_paquete()` exige un objeto con exactamente los cinco campos esperados,
versión 1, algoritmo compatible y cadenas para los campos Base64.
`descifrar_hibrido()` valida tamaños, recupera la clave AES usando RSA y llama a
`AESGCM.decrypt()`. Un fallo OAEP o de autenticación genera un mensaje de error.
El texto se decodifica solo tras la verificación de la etiqueta.

Las operaciones de claves PEM, contraseñas y OAEP se comparten en
[utilidades_rsa.py](../../utilidades_rsa.py). Son las mismas utilizadas por
[RSA-OAEP directo](../rsa_oaep/README.md). Las conversiones Base64 están en
[utilidades_cifrado.py](../../utilidades_cifrado.py).

`main()` genera archivos PEM en una carpeta nueva o carga los ya existentes.
Protege la privada con contraseña y utiliza `getpass` al solicitarla.
El bloque `if __name__ == "__main__":` permite importar sin abrir el menú.

## Instalación y uso

Desde la raíz del repositorio, con el entorno activado:

```bash
python3 -m pip install -r requirements.txt
python3 26.hibrido_rsa_aes.py
```

1. Opción 1: indica una carpeta nueva, por ejemplo `claves_hibrido`, y una
   contraseña. Se guardan `clave_publica.pem` y `clave_privada.pem`.
2. Opción 2: indica `claves_hibrido/clave_publica.pem` y un mensaje, por ejemplo
   `Hola, ñá 😀`, o un texto de más de 190 bytes. Copia el paquete JSON completo.
3. Opción 3: indica `claves_hibrido/clave_privada.pem`, su contraseña y el JSON.
   Recuperarás exactamente el mensaje.
4. Opción 4: salir.

También puedes utilizar claves generadas por `15.rsa_oaep.py`. Los cifrados de los
dos programas usan formatos diferentes: Base64 en RSA directo y JSON en el híbrido.
Los resultados varían porque se generan claves simétricas y nonces nuevos.

## Caracteres y límites

Admite texto UTF-8, incluidos mensajes vacíos, tildes, ñ, espacios y emoji.
Trabaja en memoria y en una sola línea de entrada; no es una herramienta de
cifrado de archivos ni de contenido ilimitado.

La autenticación de AES-GCM detecta modificaciones, pero no identifica a un
emisor: cualquiera con la clave pública puede crear un paquete válido.
El ejemplo no implementa firmas, certificados ni distribución de claves.
Los PEM privados están excluidos de Git y no deben compartirse.

## Referencias

Las operaciones delegadas a la biblioteca se documentan en
[RSA de cryptography](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/)
y en [AES-GCM de cryptography](https://cryptography.io/en/latest/hazmat/primitives/aead/).
