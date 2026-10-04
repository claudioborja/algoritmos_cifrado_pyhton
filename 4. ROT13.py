"""ROT13 desplaza 13 posiciones las 26 letras de a a z, sin incluir la ñ."""

ALFABETO = "abcdefghijklmnopqrstuvwxyz"
DESPLAZAMIENTO = 13


def cifrar_rot13(texto):
    """Conserva mayúsculas y deja la ñ, las tildes y los signos sin cambios."""
    caracteres_cifrados = []
    for caracter in texto:
        letra_minuscula = caracter.lower()
        if caracter in ALFABETO or caracter in ALFABETO.upper():
            posicion_original = ALFABETO.index(letra_minuscula)
            posicion_cifrada = (posicion_original + DESPLAZAMIENTO) % len(ALFABETO)
            letra_cifrada = ALFABETO[posicion_cifrada]
            if caracter.isupper():
                letra_cifrada = letra_cifrada.upper()
            caracteres_cifrados.append(letra_cifrada)
        else:
            caracteres_cifrados.append(caracter)
    return "".join(caracteres_cifrados)


def descifrar_rot13(texto_cifrado):
    """Aplicar ROT13 dos veces recupera el texto original."""
    return cifrar_rot13(texto_cifrado)


def main():
    while True:
        print("\n1. Cifrar texto")
        print("2. Descifrar texto")
        print("3. Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion in ("1", "2"):
            texto = input("Ingrese el texto: ")
            if opcion == "1":
                print("Texto cifrado:", cifrar_rot13(texto))
            else:
                print("Texto descifrado:", descifrar_rot13(texto))
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Elija 1, 2 o 3.")


if __name__ == "__main__":
    main()
