"""Atbash invierte el alfabeto español: a ↔ z, b ↔ y, etc."""

ALFABETO = "abcdefghijklmnñopqrstuvwxyz"


def cifrar_atbash(texto):
    """La misma función sirve para cifrar y descifrar."""
    caracteres_cifrados = []
    for caracter in texto:
        letra_minuscula = caracter.lower()
        if letra_minuscula in ALFABETO:
            posicion_original = ALFABETO.index(letra_minuscula)
            posicion_invertida = len(ALFABETO) - 1 - posicion_original
            letra_cifrada = ALFABETO[posicion_invertida]
            if caracter.isupper():
                letra_cifrada = letra_cifrada.upper()
            caracteres_cifrados.append(letra_cifrada)
        else:
            caracteres_cifrados.append(caracter)
    return "".join(caracteres_cifrados)


def main():
    while True:
        print("\n1. Cifrar mensaje")
        print("2. Descifrar mensaje")
        print("3. Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion in ("1", "2"):
            texto = input("Ingrese el mensaje: ")
            resultado = cifrar_atbash(texto)
            if opcion == "1":
                print("Mensaje cifrado:", resultado)
            else:
                print("Mensaje descifrado:", resultado)
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Elija 1, 2 o 3.")


if __name__ == "__main__":
    main()
