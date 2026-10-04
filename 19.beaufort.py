"""Beaufort sobre las 27 letras españolas: resta el mensaje a la clave."""

from utilidades_clasicas import ALFABETO_ESPANOL, validar_clave_espanola


def transformar_beaufort(texto, clave):
    clave = validar_clave_espanola(clave)
    caracteres_resultado = []
    posicion_clave = 0
    for caracter in texto:
        if caracter in ALFABETO_ESPANOL or caracter in ALFABETO_ESPANOL.lower():
            valor_mensaje = ALFABETO_ESPANOL.index(caracter.upper())
            letra_clave = clave[posicion_clave % len(clave)]
            valor_clave = ALFABETO_ESPANOL.index(letra_clave)
            letra_resultado = ALFABETO_ESPANOL[(valor_clave - valor_mensaje) % 27]
            if caracter.islower():
                letra_resultado = letra_resultado.lower()
            caracteres_resultado.append(letra_resultado)
            posicion_clave += 1
        else:
            caracteres_resultado.append(caracter)
    return "".join(caracteres_resultado)


def cifrar_beaufort(texto, clave):
    return transformar_beaufort(texto, clave)


def descifrar_beaufort(texto_cifrado, clave):
    return transformar_beaufort(texto_cifrado, clave)


def main():
    while True:
        print("\n1. Cifrar texto\n2. Descifrar texto\n3. Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion in ("1", "2"):
            texto = input("Ingrese el texto: ")
            try:
                clave = input("Ingrese la palabra clave: ").strip()
                if opcion == "1":
                    print("Texto cifrado:", cifrar_beaufort(texto, clave))
                else:
                    print("Texto descifrado:", descifrar_beaufort(texto, clave))
            except ValueError as error:
                print("Entrada inválida:", error)
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Elija 1, 2 o 3.")


if __name__ == "__main__":
    main()
