"""ChaCha20-Poly1305: cifrado autenticado mediante la biblioteca cryptography."""

import secrets

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

from utilidades_cifrado import codificar_base64, decodificar_base64

LONGITUD_NONCE = 12
DATOS_ASOCIADOS = b"algoritmos_cifrado_python:ChaCha20-Poly1305:v1"


def generar_clave():
    return ChaCha20Poly1305.generate_key()


def validar_clave(clave):
    if not isinstance(clave, bytes) or len(clave) != 32:
        raise ValueError("La clave debe contener 32 bytes (256 bits), representados en Base64 en el menú.")


def cifrar_chacha20(texto, clave):
    validar_clave(clave)
    nonce = secrets.token_bytes(LONGITUD_NONCE)
    cifrador = ChaCha20Poly1305(clave)
    datos_cifrados = cifrador.encrypt(nonce, texto.encode("utf-8"), DATOS_ASOCIADOS)
    # La biblioteca agrega la etiqueta de autenticación al final de datos_cifrados.
    return codificar_base64(nonce + datos_cifrados)


def descifrar_chacha20(texto_cifrado, clave):
    validar_clave(clave)
    paquete = decodificar_base64(texto_cifrado)
    if len(paquete) < LONGITUD_NONCE + 16:
        raise ValueError("El paquete debe incluir el nonce y la etiqueta de autenticación de 16 bytes.")
    nonce = paquete[:LONGITUD_NONCE]
    datos_cifrados = paquete[LONGITUD_NONCE:]
    cifrador = ChaCha20Poly1305(clave)
    try:
        datos_originales = cifrador.decrypt(nonce, datos_cifrados, DATOS_ASOCIADOS)
        return datos_originales.decode("utf-8")
    except InvalidTag as error:
        raise ValueError("No se pudo autenticar: la clave es incorrecta o el paquete fue modificado.") from error
    except UnicodeDecodeError as error:
        raise ValueError("El contenido descifrado no es un mensaje UTF-8 válido.") from error


def main():
    while True:
        print("\n1. Cifrar texto\n2. Descifrar texto\n3. Salir")
        opcion = input("Seleccione una opción: ").strip()
        try:
            if opcion == "1":
                texto = input("Ingrese el texto: ")
                clave_base64 = input("Ingrese la clave Base64 o deje vacío para generar una: ").strip()
                clave = decodificar_base64(clave_base64) if clave_base64 else generar_clave()
                texto_cifrado = cifrar_chacha20(texto, clave)
                print("Paquete cifrado (Base64):", texto_cifrado)
                print("Clave secreta (Base64):", codificar_base64(clave))
                print("Guarde la clave separada del paquete cifrado.")
            elif opcion == "2":
                texto_cifrado = input("Ingrese el paquete cifrado (Base64): ").strip()
                clave = decodificar_base64(input("Ingrese la clave (Base64): ").strip())
                print("Texto descifrado:", descifrar_chacha20(texto_cifrado, clave))
            elif opcion == "3":
                print("¡Hasta luego!")
                break
            else:
                print("Opción no válida. Elija 1, 2 o 3.")
        except ValueError as error:
            print(error)


if __name__ == "__main__":
    main()
