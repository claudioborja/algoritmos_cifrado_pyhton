"""Modelo educativo de rotores con avance de contador, sin clavijero ni muescas."""

ALFABETO = "abcdefghijklmnopqrstuvwxyz"
ROTORES = ("ekmflgdqvzntowyhxuspaibrcj", "ajdksiruxblhwtmcqgznpyfvoe", "bdfhjlcprtxvznyeiwgakmusqo")
REFLECTOR = "yruhqsldpxngokmiebfzcwvjat"


def validar_posiciones(posiciones_iniciales):
    posiciones_iniciales = posiciones_iniciales.lower()
    if len(posiciones_iniciales) != 3 or any(letra not in ALFABETO for letra in posiciones_iniciales):
        raise ValueError("Ingrese 3 letras de a a z como posiciones iniciales, por ejemplo aaa.")
    return [ALFABETO.index(letra) for letra in posiciones_iniciales]


def avanzar_rotores(posiciones_rotores):
    """El rotor derecho avanza primero; al completar una vuelta arrastra al siguiente."""
    for indice_rotor in (2, 1, 0):
        posiciones_rotores[indice_rotor] = (posiciones_rotores[indice_rotor] + 1) % 26
        if posiciones_rotores[indice_rotor] != 0:
            break


def pasar_por_rotor(valor_letra, rotor, posicion_rotor, inverso=False):
    posicion_entrada = (valor_letra + posicion_rotor) % 26
    if inverso:
        posicion_salida = rotor.index(ALFABETO[posicion_entrada])
    else:
        posicion_salida = ALFABETO.index(rotor[posicion_entrada])
    return (posicion_salida - posicion_rotor) % 26


def transformar_enigma(texto, posiciones_iniciales):
    posiciones_rotores = validar_posiciones(posiciones_iniciales)
    caracteres_resultado = []
    for caracter in texto:
        letra_minuscula = caracter.lower()
        if caracter not in ALFABETO and caracter not in ALFABETO.upper():
            caracteres_resultado.append(caracter)
            continue
        avanzar_rotores(posiciones_rotores)
        valor_letra = ALFABETO.index(letra_minuscula)
        for indice_rotor in (2, 1, 0):
            valor_letra = pasar_por_rotor(valor_letra, ROTORES[indice_rotor], posiciones_rotores[indice_rotor])
        valor_letra = ALFABETO.index(REFLECTOR[valor_letra])
        for indice_rotor in (0, 1, 2):
            valor_letra = pasar_por_rotor(valor_letra, ROTORES[indice_rotor], posiciones_rotores[indice_rotor], inverso=True)
        letra_resultado = ALFABETO[valor_letra]
        if caracter.isupper():
            letra_resultado = letra_resultado.upper()
        caracteres_resultado.append(letra_resultado)
    return "".join(caracteres_resultado)


def cifrar_enigma(texto, posiciones_iniciales):
    return transformar_enigma(texto, posiciones_iniciales)


def descifrar_enigma(texto_cifrado, posiciones_iniciales):
    return transformar_enigma(texto_cifrado, posiciones_iniciales)


def main():
    print("Enigma simplificada: reinicie las mismas posiciones para descifrar.")
    while True:
        print("\n1. Cifrar texto\n2. Descifrar texto\n3. Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion in ("1", "2"):
            texto = input("Ingrese el texto: ")
            posiciones_iniciales = input("Ingrese 3 letras para los rotores izquierdo, central y derecho: ").strip()
            try:
                if opcion == "1":
                    print("Texto cifrado:", cifrar_enigma(texto, posiciones_iniciales))
                else:
                    print("Texto descifrado:", descifrar_enigma(texto, posiciones_iniciales))
            except ValueError as error:
                print(error)
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Elija 1, 2 o 3.")


if __name__ == "__main__":
    main()
