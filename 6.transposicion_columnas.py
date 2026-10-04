"""Transposición por columnas sin relleno: cambia el orden de los caracteres."""

ALFABETO = "abcdefghijklmnñopqrstuvwxyz"


def validar_clave(clave):
    clave = clave.lower()
    if not clave or any(letra not in ALFABETO for letra in clave):
        raise ValueError("La clave debe contener solo letras de a a z o ñ, sin espacios ni tildes.")
    return clave


def obtener_orden_columnas(clave):
    """Ordena según el alfabeto español; los empates se leen de izquierda a derecha."""
    return sorted(range(len(clave)), key=lambda columna: ALFABETO.index(clave[columna]))


def cifrar_columnas(texto, clave):
    clave = validar_clave(clave)
    cantidad_columnas = len(clave)
    orden_columnas = obtener_orden_columnas(clave)
    columnas_cifradas = []
    for columna in orden_columnas:
        # Tomamos el carácter de esta columna en cada fila de la tabla.
        texto_columna = texto[columna::cantidad_columnas]
        columnas_cifradas.append(texto_columna)
    return "".join(columnas_cifradas)


def descifrar_columnas(texto_cifrado, clave):
    clave = validar_clave(clave)
    cantidad_columnas = len(clave)
    filas_completas, columnas_con_extra = divmod(len(texto_cifrado), cantidad_columnas)
    orden_columnas = obtener_orden_columnas(clave)
    caracteres_originales = [""] * len(texto_cifrado)
    inicio_columna = 0
    for columna in orden_columnas:
        longitud_columna = filas_completas
        if columna < columnas_con_extra:
            longitud_columna += 1
        fin_columna = inicio_columna + longitud_columna
        texto_columna = texto_cifrado[inicio_columna:fin_columna]
        for fila, caracter in enumerate(texto_columna):
            posicion_original = fila * cantidad_columnas + columna
            caracteres_originales[posicion_original] = caracter
        inicio_columna = fin_columna
    return "".join(caracteres_originales)


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
                    print("Texto cifrado:", cifrar_columnas(texto, clave))
                else:
                    print("Texto descifrado:", descifrar_columnas(texto, clave))
            except ValueError as error:
                print(error)
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Elija 1, 2 o 3.")


if __name__ == "__main__":
    main()
