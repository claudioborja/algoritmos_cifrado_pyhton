"""Vernam con XOR byte a byte y una clave aleatoria de un solo uso."""

import secrets

from utilidades_cifrado import codificar_base64, decodificar_base64


def generar_clave(longitud_bytes):
    if type(longitud_bytes) is not int or longitud_bytes < 0:
        raise ValueError("La longitud debe ser un entero mayor o igual que cero.")
    return secrets.token_bytes(longitud_bytes)


def aplicar_xor(datos, clave):
    if not isinstance(clave, bytes) or len(clave) != len(datos):
        raise ValueError("La clave debe tener exactamente tantos bytes como el mensaje UTF-8.")
    return bytes(byte_dato ^ byte_clave for byte_dato, byte_clave in zip(datos, clave))


def cifrar_vernam(texto, clave):
    datos = texto.encode("utf-8")
    return codificar_base64(aplicar_xor(datos, clave))


def descifrar_vernam(texto_cifrado, clave):
    datos_cifrados = decodificar_base64(texto_cifrado)
    datos_originales = aplicar_xor(datos_cifrados, clave)
    try:
        return datos_originales.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("El resultado no es UTF-8 válido; revise la clave y el mensaje.") from error


def main():
    print("Se genera una clave nueva por mensaje. No la reutilice ni la comparta públicamente.")
    while True:
        print("\n1. Cifrar y generar clave\n2. Descifrar con clave\n3. Salir")
        opcion = input("Seleccione una opción: ").strip()
        try:
            if opcion == "1":
                texto = input("Ingrese el texto: ")
                clave = generar_clave(len(texto.encode("utf-8")))
                print("Texto cifrado (Base64):", cifrar_vernam(texto, clave))
                print("Clave de un solo uso (Base64):", codificar_base64(clave))
            elif opcion == "2":
                texto_cifrado = input("Ingrese el texto cifrado (Base64): ").strip()
                clave = decodificar_base64(input("Ingrese la clave (Base64): ").strip())
                print("Texto descifrado:", descifrar_vernam(texto_cifrado, clave))
            elif opcion == "3":
                print("¡Hasta luego!")
                break
            else:
                print("Opción no válida. Elija 1, 2 o 3.")
        except ValueError as error:
            print(error)


if __name__ == "__main__":
    main()
