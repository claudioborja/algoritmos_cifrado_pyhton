"""Sustitución simple: cada letra tiene un reemplazo definido por la clave."""

ALFABETO = "abcdefghijklmnñopqrstuvwxyz"


def validar_clave(clave):
    """La clave debe contener las 27 letras, sin omisiones ni repeticiones."""
    clave = clave.lower()
    if len(clave) != len(ALFABETO) or set(clave) != set(ALFABETO):
        raise ValueError("La clave debe contener las 27 letras del alfabeto español una sola vez.")
    return clave


def sustituir_letras(texto, alfabeto_original, alfabeto_reemplazo):
    caracteres_sustituidos = []
    for caracter in texto:
        letra_minuscula = caracter.lower()
        if caracter in alfabeto_original or caracter in alfabeto_original.upper():
            posicion = alfabeto_original.index(letra_minuscula)
            letra_reemplazo = alfabeto_reemplazo[posicion]
            if caracter.isupper():
                letra_reemplazo = letra_reemplazo.upper()
            caracteres_sustituidos.append(letra_reemplazo)
        else:
            caracteres_sustituidos.append(caracter)
    return "".join(caracteres_sustituidos)


def cifrar_sustitucion(texto, clave):
    """Reemplaza cada letra del alfabeto por la letra correspondiente de la clave."""
    clave = validar_clave(clave)
    return sustituir_letras(texto, ALFABETO, clave)


def descifrar_sustitucion(texto_cifrado, clave):
    """Invierte los reemplazos usando la misma clave del cifrado."""
    clave = validar_clave(clave)
    return sustituir_letras(texto_cifrado, clave, ALFABETO)


def main():
    while True:
        print("\n1. Cifrar texto")
        print("2. Descifrar texto")
        print("3. Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion in ("1", "2"):
            texto = input("Ingrese el texto: ")
            print("Alfabeto original:", ALFABETO)
            print("Ejemplo de clave:  qwertyuiopasdfghjklñzxcvbnm")
            clave = input("Ingrese las 27 letras en el orden de reemplazo: ").strip()
            try:
                if opcion == "1":
                    resultado = cifrar_sustitucion(texto, clave)
                    print("Texto cifrado:", resultado)
                else:
                    resultado = descifrar_sustitucion(texto, clave)
                    print("Texto descifrado:", resultado)
            except ValueError as error:
                print(error)
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Elija 1, 2 o 3.")


if __name__ == "__main__":
    main()
