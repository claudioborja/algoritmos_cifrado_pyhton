"""Vigenère utiliza una palabra clave para variar el desplazamiento."""

ALFABETO = "abcdefghijklmnñopqrstuvwxyz"


def validar_clave(clave):
    clave = clave.lower()
    if not clave or any(letra not in ALFABETO for letra in clave):
        raise ValueError("La clave debe contener solo letras de a a z o ñ, sin espacios ni tildes.")
    return clave


def transformar_vigenere(texto, clave, descifrar=False):
    clave = validar_clave(clave)
    caracteres_transformados = []
    posicion_clave = 0
    for caracter in texto:
        letra_minuscula = caracter.lower()
        if caracter in ALFABETO or caracter in ALFABETO.upper():
            letra_clave = clave[posicion_clave % len(clave)]
            desplazamiento = ALFABETO.index(letra_clave)
            if descifrar:
                desplazamiento = -desplazamiento
            posicion_original = ALFABETO.index(letra_minuscula)
            posicion_resultado = (posicion_original + desplazamiento) % len(ALFABETO)
            letra_resultado = ALFABETO[posicion_resultado]
            if caracter.isupper():
                letra_resultado = letra_resultado.upper()
            caracteres_transformados.append(letra_resultado)
            # Solo avanzamos la clave cuando transformamos una letra del alfabeto.
            posicion_clave += 1
        else:
            caracteres_transformados.append(caracter)
    return "".join(caracteres_transformados)


def cifrar_vigenere(texto, clave):
    return transformar_vigenere(texto, clave)


def descifrar_vigenere(texto_cifrado, clave):
    return transformar_vigenere(texto_cifrado, clave, descifrar=True)


def main():
    while True:
        print("\n1. Cifrar texto")
        print("2. Descifrar texto")
        print("3. Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion in ("1", "2"):
            texto = input("Ingrese el texto: ")
            clave = input("Ingrese la palabra clave (sin espacios ni tildes): ").strip()
            try:
                if opcion == "1":
                    print("Texto cifrado:", cifrar_vigenere(texto, clave))
                else:
                    print("Texto descifrado:", descifrar_vigenere(texto, clave))
            except ValueError as error:
                print(error)
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Elija 1, 2 o 3.")


if __name__ == "__main__":
    main()
