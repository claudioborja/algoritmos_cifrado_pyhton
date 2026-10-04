"""Paillier para enteros y sumas cifradas, con primos pequeños educativos."""

from math import gcd, lcm
import secrets

from utilidades_matematicas import validar_primo


def validar_modulo(modulo):
    if type(modulo) is not int or not 9 <= modulo <= 1_000_000 ** 2:
        raise ValueError("Use el módulo de una clave generada por esta demostración (entre 9 y un billón).")


def generar_claves(primo_primero=17, primo_segundo=19):
    validar_primo(primo_primero)
    validar_primo(primo_segundo)
    if primo_primero == primo_segundo:
        raise ValueError("Los dos primos deben ser diferentes.")
    modulo = primo_primero * primo_segundo
    exponente_privado = lcm(primo_primero - 1, primo_segundo - 1)
    if gcd(exponente_privado, modulo) != 1:
        raise ValueError("Estos primos no permiten usar el generador módulo + 1; elija otros.")
    inverso_privado = pow(exponente_privado, -1, modulo)
    return (modulo, exponente_privado, inverso_privado), modulo


def cifrar_paillier(mensaje, clave_publica, aleatorio=None):
    modulo = clave_publica
    validar_modulo(modulo)
    if type(mensaje) is not int or not 0 <= mensaje < modulo:
        raise ValueError("El mensaje debe ser un entero entre 0 y módulo - 1.")
    if aleatorio is None:
        aleatorio = secrets.randbelow(modulo - 1) + 1
        while gcd(aleatorio, modulo) != 1:
            aleatorio = secrets.randbelow(modulo - 1) + 1
    if type(aleatorio) is not int or not 1 <= aleatorio < modulo or gcd(aleatorio, modulo) != 1:
        raise ValueError("El aleatorio debe estar entre 1 y módulo - 1 y ser coprimo con el módulo.")
    modulo_cuadrado = modulo * modulo
    generador = modulo + 1
    return (pow(generador, mensaje, modulo_cuadrado) * pow(aleatorio, modulo, modulo_cuadrado)) % modulo_cuadrado


def validar_cifrado(texto_cifrado, modulo):
    validar_modulo(modulo)
    if type(texto_cifrado) is not int or not 1 <= texto_cifrado < modulo * modulo or gcd(texto_cifrado, modulo) != 1:
        raise ValueError("El cifrado debe estar entre 1 y módulo² - 1 y ser coprimo con el módulo.")


def descifrar_paillier(texto_cifrado, clave_privada):
    if not isinstance(clave_privada, (tuple, list)) or len(clave_privada) != 3:
        raise ValueError("La clave privada debe contener módulo, exponente e inverso.")
    modulo, exponente_privado, inverso_privado = clave_privada
    validar_cifrado(texto_cifrado, modulo)
    if type(exponente_privado) is not int or not 1 <= exponente_privado < modulo:
        raise ValueError("El exponente privado debe estar entre 1 y módulo - 1.")
    if type(inverso_privado) is not int or not 1 <= inverso_privado < modulo or (exponente_privado * inverso_privado) % modulo != 1:
        raise ValueError("El inverso privado no corresponde al exponente y al módulo.")
    valor_potencia = pow(texto_cifrado, exponente_privado, modulo * modulo)
    if (valor_potencia - 1) % modulo != 0:
        raise ValueError("El cifrado no es compatible con esta clave privada.")
    cociente = (valor_potencia - 1) // modulo
    return (cociente * inverso_privado) % modulo


def sumar_cifrados(cifrado_primero, cifrado_segundo, clave_publica):
    validar_cifrado(cifrado_primero, clave_publica)
    validar_cifrado(cifrado_segundo, clave_publica)
    # Multiplicar cifrados equivale a sumar mensajes, módulo la clave pública.
    producto = (cifrado_primero * cifrado_segundo) % (clave_publica * clave_publica)
    # Cifrar cero con aleatoriedad nueva renueva la aleatoriedad del resultado.
    return (producto * cifrar_paillier(0, clave_publica)) % (clave_publica * clave_publica)


def main():
    print("Demostración con primos pequeños y enteros; las sumas se recuperan módulo la clave pública.")
    while True:
        print("\n1. Generar claves\n2. Cifrar entero\n3. Descifrar entero\n4. Sumar cifrados\n5. Salir")
        opcion = input("Seleccione una opción: ").strip()
        try:
            if opcion == "1":
                primo_primero = int(input("Ingrese el primer primo (vacío: 17): ") or "17")
                primo_segundo = int(input("Ingrese el segundo primo (vacío: 19): ") or "19")
                clave_privada, clave_publica = generar_claves(primo_primero, primo_segundo)
                print("Clave pública (módulo):", clave_publica)
                print("Clave privada (módulo exponente inverso):", *clave_privada)
            elif opcion == "2":
                clave_publica = int(input("Ingrese la clave pública (módulo): "))
                mensaje = int(input("Ingrese el entero que desea cifrar: "))
                print("Entero cifrado:", cifrar_paillier(mensaje, clave_publica))
            elif opcion == "3":
                clave_privada = tuple(int(valor) for valor in input("Ingrese módulo exponente inverso: ").split())
                texto_cifrado = int(input("Ingrese el entero cifrado: "))
                print("Entero descifrado:", descifrar_paillier(texto_cifrado, clave_privada))
            elif opcion == "4":
                clave_publica = int(input("Ingrese la clave pública (módulo): "))
                cifrado_primero = int(input("Ingrese el primer cifrado: "))
                cifrado_segundo = int(input("Ingrese el segundo cifrado: "))
                print("Suma cifrada:", sumar_cifrados(cifrado_primero, cifrado_segundo, clave_publica))
            elif opcion == "5":
                print("¡Hasta luego!")
                break
            else:
                print("Opción no válida. Elija 1, 2, 3, 4 o 5.")
        except ValueError as error:
            print("Entrada inválida:", error)


if __name__ == "__main__":
    main()
