"""Escítala: transposición por una tabla de columnas fijas, sin relleno."""

from utilidades_clasicas import validar_entero_positivo


def cifrar_escitala(texto, cantidad_columnas):
    validar_entero_positivo(cantidad_columnas, "La cantidad de columnas")
    # Las columnas vacías no aportan caracteres al resultado.
    columnas = [texto[columna::cantidad_columnas] for columna in range(min(cantidad_columnas, len(texto)))]
    return "".join(columnas)


def descifrar_escitala(texto_cifrado, cantidad_columnas):
    validar_entero_positivo(cantidad_columnas, "La cantidad de columnas")
    filas_completas, columnas_con_extra = divmod(len(texto_cifrado), cantidad_columnas)
    caracteres_originales = [""] * len(texto_cifrado)
    inicio_columna = 0
    for columna in range(min(cantidad_columnas, len(texto_cifrado))):
        longitud_columna = filas_completas + int(columna < columnas_con_extra)
        texto_columna = texto_cifrado[inicio_columna:inicio_columna + longitud_columna]
        for fila, caracter in enumerate(texto_columna):
            caracteres_originales[fila * cantidad_columnas + columna] = caracter
        inicio_columna += longitud_columna
    return "".join(caracteres_originales)


def main():
    while True:
        print("\n1. Cifrar texto\n2. Descifrar texto\n3. Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion in ("1", "2"):
            texto = input("Ingrese el texto: ")
            try:
                cantidad_columnas = int(input("Ingrese la cantidad de columnas: "))
                if opcion == "1":
                    print("Texto cifrado:", cifrar_escitala(texto, cantidad_columnas))
                else:
                    print("Texto descifrado:", descifrar_escitala(texto, cantidad_columnas))
            except ValueError as error:
                print("Entrada inválida:", error)
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Elija 1, 2 o 3.")


if __name__ == "__main__":
    main()
