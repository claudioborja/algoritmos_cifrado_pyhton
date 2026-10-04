"""Cifrado afín con el alfabeto español de 27 letras."""

from math import gcd

ALFABETO = "abcdefghijklmnñopqrstuvwxyz"


def validar_claves(multiplicador, desplazamiento):
    if type(multiplicador) is not int or type(desplazamiento) is not int:
        raise ValueError("Las dos claves deben ser números enteros.")
    if gcd(multiplicador, len(ALFABETO)) != 1:
        raise ValueError("El multiplicador debe ser coprimo con 27: no puede ser múltiplo de 3.")


def transformar_afin(texto, multiplicador, desplazamiento):
    caracteres_transformados = []
    for caracter in texto:
        letra_minuscula = caracter.lower()
        if caracter in ALFABETO or caracter in ALFABETO.upper():
            posicion_original = ALFABETO.index(letra_minuscula)
            posicion_resultado = (multiplicador * posicion_original + desplazamiento) % len(ALFABETO)
            letra_resultado = ALFABETO[posicion_resultado]
            if caracter.isupper():
                letra_resultado = letra_resultado.upper()
            caracteres_transformados.append(letra_resultado)
        else:
            caracteres_transformados.append(caracter)
    return "".join(caracteres_transformados)


def cifrar_afin(texto, multiplicador, desplazamiento):
    validar_claves(multiplicador, desplazamiento)
    return transformar_afin(texto, multiplicador, desplazamiento)


def descifrar_afin(texto_cifrado, multiplicador, desplazamiento):
    validar_claves(multiplicador, desplazamiento)
    inverso_multiplicador = pow(multiplicador, -1, len(ALFABETO))
    return transformar_afin(texto_cifrado, inverso_multiplicador, -inverso_multiplicador * desplazamiento)


def main():
    while True:
        print("\n1. Cifrar texto\n2. Descifrar texto\n3. Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion in ("1", "2"):
            texto = input("Ingrese el texto: ")
            try:
                multiplicador = int(input("Ingrese el multiplicador (no múltiplo de 3): "))
                desplazamiento = int(input("Ingrese el desplazamiento: "))
                if opcion == "1":
                    print("Texto cifrado:", cifrar_afin(texto, multiplicador, desplazamiento))
                else:
                    print("Texto descifrado:", descifrar_afin(texto, multiplicador, desplazamiento))
            except ValueError as error:
                print("Entrada inválida:", error)
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Elija 1, 2 o 3.")


if __name__ == "__main__":
    main()
