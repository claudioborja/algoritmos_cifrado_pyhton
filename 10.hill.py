"""Hill con matrices de 2 × 2 y las 27 letras del alfabeto español."""

from math import gcd

ALFABETO = "abcdefghijklmnñopqrstuvwxyz"


def validar_matriz(matriz_clave):
    if not isinstance(matriz_clave, (list, tuple)) or len(matriz_clave) != 2:
        raise ValueError("La clave debe ser una matriz de 2 × 2 números enteros.")
    for fila in matriz_clave:
        if not isinstance(fila, (list, tuple)) or len(fila) != 2 or any(type(valor) is not int for valor in fila):
            raise ValueError("La clave debe ser una matriz de 2 × 2 números enteros.")
    primera, segunda = matriz_clave
    determinante = primera[0] * segunda[1] - primera[1] * segunda[0]
    if gcd(determinante, len(ALFABETO)) != 1:
        raise ValueError("El determinante debe ser coprimo con 27: no puede ser múltiplo de 3.")
    return determinante


def invertir_matriz(matriz_clave):
    determinante = validar_matriz(matriz_clave)
    inverso_determinante = pow(determinante, -1, len(ALFABETO))
    primera, segunda = matriz_clave
    return [
        [(segunda[1] * inverso_determinante) % 27, (-primera[1] * inverso_determinante) % 27],
        [(-segunda[0] * inverso_determinante) % 27, (primera[0] * inverso_determinante) % 27],
    ]


def transformar_hill(texto, matriz_clave):
    # Solo agrupamos letras del alfabeto; los demás caracteres permanecen en su lugar.
    posiciones_letras = [posicion for posicion, caracter in enumerate(texto) if caracter in ALFABETO or caracter in ALFABETO.upper()]
    if len(posiciones_letras) % 2 != 0:
        raise ValueError("Hill necesita una cantidad par de letras del alfabeto; no añade relleno.")
    caracteres_resultado = list(texto)
    for inicio in range(0, len(posiciones_letras), 2):
        posiciones_pareja = posiciones_letras[inicio:inicio + 2]
        valores_pareja = [ALFABETO.index(texto[posicion].lower()) for posicion in posiciones_pareja]
        for fila, posicion in enumerate(posiciones_pareja):
            valor_resultado = (matriz_clave[fila][0] * valores_pareja[0] + matriz_clave[fila][1] * valores_pareja[1]) % len(ALFABETO)
            letra_resultado = ALFABETO[valor_resultado]
            if texto[posicion].isupper():
                letra_resultado = letra_resultado.upper()
            caracteres_resultado[posicion] = letra_resultado
    return "".join(caracteres_resultado)


def cifrar_hill(texto, matriz_clave):
    validar_matriz(matriz_clave)
    return transformar_hill(texto, matriz_clave)


def descifrar_hill(texto_cifrado, matriz_clave):
    return transformar_hill(texto_cifrado, invertir_matriz(matriz_clave))


def main():
    print("Hill usa parejas de letras; el mensaje debe tener una cantidad par de letras del alfabeto.")
    while True:
        print("\n1. Cifrar texto\n2. Descifrar texto\n3. Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion in ("1", "2"):
            texto = input("Ingrese el texto: ")
            try:
                valores_clave = [int(valor) for valor in input("Ingrese 4 enteros por filas (ejemplo: 1 2 3 5): ").split()]
                if len(valores_clave) != 4:
                    raise ValueError("Debe ingresar exactamente 4 números.")
                matriz_clave = [valores_clave[:2], valores_clave[2:]]
                if opcion == "1":
                    print("Texto cifrado:", cifrar_hill(texto, matriz_clave))
                else:
                    print("Texto descifrado:", descifrar_hill(texto, matriz_clave))
            except ValueError as error:
                print("Entrada inválida:", error)
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Elija 1, 2 o 3.")


if __name__ == "__main__":
    main()
