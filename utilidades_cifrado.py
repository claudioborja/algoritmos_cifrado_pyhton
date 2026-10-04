"""Conversión de bytes a texto Base64 para copiar claves y mensajes cifrados."""

import base64
import binascii


def codificar_base64(datos):
    return base64.b64encode(datos).decode("ascii")


def decodificar_base64(texto):
    try:
        return base64.b64decode(texto, validate=True)
    except (binascii.Error, ValueError) as error:
        raise ValueError("El dato debe ser un texto Base64 válido, sin espacios.") from error
