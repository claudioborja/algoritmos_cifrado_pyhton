"""Vigenère Autoclave: extiende la clave inicial con las letras del mensaje."""

from utilidades_clasicas import ALFABETO_ESPANOL, validar_clave_espanola


def transformar_autoclave(texto, clave, descifrar=False):
    clave = validar_clave_espanola(clave)
    valores_clave = [ALFABETO_ESPANOL.index(letra) for letra in clave]
    posicion_clave = 0
    caracteres_resultado = []
    for caracter in texto:
        if caracter in ALFABETO_ESPANOL or caracter in ALFABETO_ESPANOL.lower():
            valor_entrada = ALFABETO_ESPANOL.index(caracter.upper())
            valor_clave = valores_clave[posicion_clave]
            if descifrar:
                valor_resultado = (valor_entrada - valor_clave) % 27
                valores_clave.append(valor_resultado)
            else:
                valor_resultado = (valor_entrada + valor_clave) % 27
                valores_clave.append(valor_entrada)
            letra_resultado = ALFABETO_ESPANOL[valor_resultado]
            if caracter.islower():
                letra_resultado = letra_resultado.lower()
            caracteres_resultado.append(letra_resultado)
            posicion_clave += 1
        else:
            caracteres_resultado.append(caracter)
    return "".join(caracteres_resultado)


def cifrar_autoclave(texto, clave):
    return transformar_autoclave(texto, clave)


def descifrar_autoclave(texto_cifrado, clave):
    return transformar_autoclave(texto_cifrado, clave, descifrar=True)


def main():
    while True:
        print("\n1. Cifrar texto\n2. Descifrar texto\n3. Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion in ("1", "2"):
            texto = input("Ingrese el texto: ")
            try:
                clave = input("Ingrese la palabra clave: ").strip()
                if opcion == "1":
                    print("Texto cifrado:", cifrar_autoclave(texto, clave))
                else:
                    print("Texto descifrado:", descifrar_autoclave(texto, clave))
            except ValueError as error:
                print("Entrada inválida:", error)
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Elija 1, 2 o 3.")


if __name__ == "__main__":
    main()
