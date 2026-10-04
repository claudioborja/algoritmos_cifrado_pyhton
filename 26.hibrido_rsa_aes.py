"""Cifrado híbrido: RSA-OAEP protege una clave nueva de AES-GCM por mensaje."""

import getpass
import json
import secrets

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from utilidades_cifrado import codificar_base64, decodificar_base64
from utilidades_rsa import cargar_clave_privada, cargar_clave_publica, crear_relleno_oaep, generar_claves, guardar_claves

NOMBRE_ALGORITMO = "RSA-OAEP-SHA256+AES-256-GCM"


def obtener_datos_asociados(paquete):
    cabecera = {"version": paquete["version"], "algoritmo": paquete["algoritmo"], "clave_cifrada": paquete["clave_cifrada"]}
    return json.dumps(cabecera, sort_keys=True, separators=(",", ":")).encode("utf-8")


def cifrar_hibrido(texto, clave_publica):
    if not isinstance(clave_publica, rsa.RSAPublicKey) or clave_publica.key_size < 2048:
        raise ValueError("Se necesita una clave pública RSA de al menos 2048 bits.")
    clave_simetrica = AESGCM.generate_key(bit_length=256)
    clave_cifrada = clave_publica.encrypt(clave_simetrica, crear_relleno_oaep())
    nonce = secrets.token_bytes(12)
    paquete = {"version": 1, "algoritmo": NOMBRE_ALGORITMO, "clave_cifrada": codificar_base64(clave_cifrada)}
    datos_asociados = obtener_datos_asociados(paquete)
    datos_cifrados = AESGCM(clave_simetrica).encrypt(nonce, texto.encode("utf-8"), datos_asociados)
    paquete["nonce"] = codificar_base64(nonce)
    paquete["datos"] = codificar_base64(datos_cifrados)
    return json.dumps(paquete, sort_keys=True, separators=(",", ":"))


def validar_paquete(texto_cifrado):
    try:
        paquete = json.loads(texto_cifrado)
    except (ValueError, TypeError) as error:
        raise ValueError("El paquete debe ser un objeto JSON válido.") from error
    campos = {"version", "algoritmo", "clave_cifrada", "nonce", "datos"}
    if not isinstance(paquete, dict) or set(paquete) != campos:
        raise ValueError("El paquete debe contener version, algoritmo, clave_cifrada, nonce y datos.")
    if type(paquete["version"]) is not int or paquete["version"] != 1 or paquete["algoritmo"] != NOMBRE_ALGORITMO:
        raise ValueError("La versión o el algoritmo del paquete no son compatibles.")
    if any(not isinstance(paquete[campo], str) for campo in ("clave_cifrada", "nonce", "datos")):
        raise ValueError("Los campos cifrados deben ser cadenas Base64.")
    return paquete


def descifrar_hibrido(texto_cifrado, clave_privada):
    if not isinstance(clave_privada, rsa.RSAPrivateKey) or clave_privada.key_size < 2048:
        raise ValueError("Se necesita una clave privada RSA de al menos 2048 bits.")
    paquete = validar_paquete(texto_cifrado)
    clave_cifrada = decodificar_base64(paquete["clave_cifrada"])
    nonce = decodificar_base64(paquete["nonce"])
    datos_cifrados = decodificar_base64(paquete["datos"])
    if len(nonce) != 12 or len(datos_cifrados) < 16:
        raise ValueError("El nonce debe tener 12 bytes y los datos deben incluir la etiqueta de autenticación.")
    try:
        clave_simetrica = clave_privada.decrypt(clave_cifrada, crear_relleno_oaep())
        if len(clave_simetrica) != 32:
            raise ValueError("La clave simétrica recuperada no tiene 32 bytes.")
        datos_originales = AESGCM(clave_simetrica).decrypt(nonce, datos_cifrados, obtener_datos_asociados(paquete))
        return datos_originales.decode("utf-8")
    except (ValueError, InvalidTag) as error:
        raise ValueError("No se pudo descifrar o autenticar: revise la clave privada y la integridad del paquete.") from error


def main():
    while True:
        print("\n1. Generar y guardar claves RSA\n2. Cifrar texto\n3. Descifrar texto\n4. Salir")
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
                texto = input("Ingrese el texto: ")
                print("Paquete cifrado (JSON):", cifrar_hibrido(texto, clave_publica))
            elif opcion == "3":
                ruta = input("Ingrese la ruta de la clave privada PEM: ").strip()
                contrasena = getpass.getpass("Contraseña de la clave privada: ").encode("utf-8")
                clave_privada = cargar_clave_privada(ruta, contrasena)
                texto_cifrado = input("Ingrese el paquete cifrado (JSON): ")
                print("Texto descifrado:", descifrar_hibrido(texto_cifrado, clave_privada))
            elif opcion == "4":
                print("¡Hasta luego!")
                break
            else:
                print("Opción no válida. Elija 1, 2, 3 o 4.")
        except (ValueError, OSError) as error:
            print("No se pudo completar la operación:", error)


if __name__ == "__main__":
    main()
