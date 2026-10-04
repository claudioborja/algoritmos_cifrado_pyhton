"""Funciones compartidas de RSA-OAEP y almacenamiento de claves PEM."""

import os
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from utilidades_cifrado import codificar_base64, decodificar_base64


def generar_claves():
    clave_privada = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return clave_privada, clave_privada.public_key()


def crear_relleno_oaep():
    return padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)


def cifrar_rsa(texto, clave_publica):
    if not isinstance(clave_publica, rsa.RSAPublicKey) or clave_publica.key_size < 2048:
        raise ValueError("Se necesita una clave pública RSA de al menos 2048 bits.")
    datos = texto.encode("utf-8")
    longitud_maxima = (clave_publica.key_size + 7) // 8 - 2 * hashes.SHA256().digest_size - 2
    if len(datos) > longitud_maxima:
        raise ValueError(f"RSA-OAEP admite como máximo {longitud_maxima} bytes UTF-8 con esta clave.")
    return codificar_base64(clave_publica.encrypt(datos, crear_relleno_oaep()))


def descifrar_rsa(texto_cifrado, clave_privada):
    if not isinstance(clave_privada, rsa.RSAPrivateKey) or clave_privada.key_size < 2048:
        raise ValueError("Se necesita una clave privada RSA de al menos 2048 bits.")
    datos_cifrados = decodificar_base64(texto_cifrado)
    try:
        datos_originales = clave_privada.decrypt(datos_cifrados, crear_relleno_oaep())
        return datos_originales.decode("utf-8")
    except ValueError as error:
        raise ValueError("No se pudo descifrar: revise la clave privada y el mensaje cifrado.") from error


def guardar_claves(carpeta, contrasena):
    if not isinstance(contrasena, bytes) or not contrasena:
        raise ValueError("La clave privada requiere una contraseña no vacía.")
    carpeta = Path(carpeta)
    if carpeta.exists():
        raise ValueError("La carpeta ya existe. Elija otra para evitar sobrescribir claves.")
    clave_privada, clave_publica = generar_claves()
    datos_privados = clave_privada.private_bytes(
        serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
        serialization.BestAvailableEncryption(contrasena),
    )
    datos_publicos = clave_publica.public_bytes(
        serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    carpeta.mkdir(mode=0o700, parents=True, exist_ok=False)
    ruta_privada = carpeta / "clave_privada.pem"
    ruta_publica = carpeta / "clave_publica.pem"
    descriptor = os.open(ruta_privada, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "wb") as archivo:
        archivo.write(datos_privados)
    ruta_publica.write_bytes(datos_publicos)
    return ruta_privada, ruta_publica


def cargar_clave_publica(ruta):
    clave_publica = serialization.load_pem_public_key(Path(ruta).read_bytes())
    if not isinstance(clave_publica, rsa.RSAPublicKey):
        raise ValueError("El archivo no contiene una clave pública RSA.")
    return clave_publica


def cargar_clave_privada(ruta, contrasena):
    try:
        clave_privada = serialization.load_pem_private_key(Path(ruta).read_bytes(), password=contrasena)
    except (ValueError, TypeError) as error:
        raise ValueError("La contraseña es incorrecta o el archivo de clave privada no es válido.") from error
    if not isinstance(clave_privada, rsa.RSAPrivateKey):
        raise ValueError("El archivo no contiene una clave privada RSA.")
    return clave_privada
