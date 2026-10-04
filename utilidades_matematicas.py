"""Aritmética para demostraciones con primos pequeños, hasta un millón."""

from math import isqrt

LIMITE_PRIMO = 1_000_000


def validar_primo(numero):
    if type(numero) is not int or not 3 <= numero <= LIMITE_PRIMO:
        raise ValueError("Use un primo entre 3 y 1 000 000; esta demostración no usa claves de producción.")
    if any(numero % divisor == 0 for divisor in range(2, isqrt(numero) + 1)):
        raise ValueError("El número debe ser primo.")


def obtener_factores_primos(numero):
    factores = []
    divisor = 2
    while divisor * divisor <= numero:
        if numero % divisor == 0:
            factores.append(divisor)
            while numero % divisor == 0:
                numero //= divisor
        divisor += 1
    if numero > 1:
        factores.append(numero)
    return factores
