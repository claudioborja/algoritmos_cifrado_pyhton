"""RSA-OAEP con SHA-256 para mensajes cortos y claves PEM."""

import getpass

from utilidades_rsa import (
    cargar_clave_privada,
    cargar_clave_publica,
    cifrar_rsa,
    crear_relleno_oaep,
    descifrar_rsa,
    generar_claves,
    guardar_claves,
)


def main():
    while True:
        print("\n1. Generar y guardar claves\n2. Cifrar texto\n3. Descifrar texto\n4. Salir")
        opcion = input("Seleccione una opción: ").strip()
        try:
            if opcion == "1":
                carpeta = input("Ingrese una carpeta nueva para las claves: ").strip()
                if not carpeta:
                    raise ValueError("Debe indicar una carpeta nueva.")
                contrasena = getpass.getpass("Contraseña para proteger la clave privada: ").encode("utf-8")
                ruta_privada, ruta_publica = guardar_claves(carpeta, contrasena)
                print("Clave pública:", ruta_publica)
                print("Clave privada protegida:", ruta_privada)
            elif opcion == "2":
                ruta = input("Ingrese la ruta de la clave pública PEM: ").strip()
                clave_publica = cargar_clave_publica(ruta)
                texto = input("Ingrese el mensaje corto: ")
                print("Texto cifrado (Base64):", cifrar_rsa(texto, clave_publica))
            elif opcion == "3":
                ruta = input("Ingrese la ruta de la clave privada PEM: ").strip()
                contrasena = getpass.getpass("Contraseña de la clave privada: ").encode("utf-8")
                clave_privada = cargar_clave_privada(ruta, contrasena)
                texto_cifrado = input("Ingrese el texto cifrado (Base64): ").strip()
                print("Texto descifrado:", descifrar_rsa(texto_cifrado, clave_privada))
            elif opcion == "4":
                print("¡Hasta luego!")
                break
            else:
                print("Opción no válida. Elija 1, 2, 3 o 4.")
        except (ValueError, OSError) as error:
            print("No se pudo completar la operación:", error)


if __name__ == "__main__":
    main()
