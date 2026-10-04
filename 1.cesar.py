"""Cifrado César con las 27 letras del alfabeto español."""

ALFABETO = "abcdefghijklmnñopqrstuvwxyz"


def cifrar_cesar(texto, desplazamiento):
    """Desplaza las letras y conserva mayúsculas, tildes y signos."""
    caracteres_cifrados = []
    for caracter in texto:
        letra_minuscula = caracter.lower()
        if caracter in ALFABETO or caracter in ALFABETO.upper():
            posicion_original = ALFABETO.index(letra_minuscula)
            posicion_cifrada = (posicion_original + desplazamiento) % len(ALFABETO)
            letra_cifrada = ALFABETO[posicion_cifrada]
            if caracter.isupper():
                letra_cifrada = letra_cifrada.upper()
            caracteres_cifrados.append(letra_cifrada)
        else:
            caracteres_cifrados.append(caracter)
    return "".join(caracteres_cifrados)


def descifrar_cesar(texto_cifrado, desplazamiento):
    """Recupera el texto usando el mismo desplazamiento del cifrado."""
    return cifrar_cesar(texto_cifrado, -desplazamiento)


def mostrar_posibles_descifrados(texto_cifrado):
    """Muestra los 27 resultados cuando se desconoce el desplazamiento."""
    for desplazamiento in range(len(ALFABETO)):
        texto_descifrado = descifrar_cesar(texto_cifrado, desplazamiento)
        print(f"Desplazamiento {desplazamiento}: {texto_descifrado}")


def main():
    while True:
        print("\n1. Cifrar")
        print("2. Descifrar con desplazamiento conocido")
        print("3. Salir")
        print("4. Probar todos los desplazamientos")
        opcion = input("Elija una opción: ").strip()

        if opcion in ("1", "2"):
            texto = input("Ingrese el texto: ")
            try:
                desplazamiento = int(input("Ingrese el desplazamiento (número entero): "))
            except ValueError:
                print("El desplazamiento debe ser un número entero.")
                continue
            if opcion == "1":
                print("Texto cifrado:", cifrar_cesar(texto, desplazamiento))
            else:
                print("Texto descifrado:", descifrar_cesar(texto, desplazamiento))
        elif opcion == "4":
            texto_cifrado = input("Ingrese el texto cifrado: ")
            mostrar_posibles_descifrados(texto_cifrado)
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Elija 1, 2, 3 o 4.")


if __name__ == "__main__":
    main()
