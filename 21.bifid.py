"""Bifid combina coordenadas de un cuadrado de Polibio y transposición."""

from utilidades_clasicas import ALFABETO_POLIBIO, crear_alfabeto_clave, normalizar_texto, validar_entero_positivo


def transformar_bifid(texto, clave, periodo, descifrar=False):
    validar_entero_positivo(periodo, "El período")
    alfabeto_clave = crear_alfabeto_clave(clave, ALFABETO_POLIBIO, unir_ij=True)
    if descifrar and "j" in texto.lower():
        raise ValueError("El texto cifrado no contiene J; utiliza I.")
    texto = normalizar_texto(texto, ALFABETO_POLIBIO, unir_ij=True)
    letras_resultado = []
    for inicio in range(0, len(texto), periodo):
        bloque = texto[inicio:inicio + periodo]
        coordenadas = [divmod(alfabeto_clave.index(letra), 5) for letra in bloque]
        longitud_bloque = len(bloque)
        if descifrar:
            numeros = [numero for pareja in coordenadas for numero in pareja]
            filas = numeros[:longitud_bloque]
            columnas = numeros[longitud_bloque:]
            for fila, columna in zip(filas, columnas):
                letras_resultado.append(alfabeto_clave[fila * 5 + columna])
        else:
            filas = [fila for fila, columna in coordenadas]
            columnas = [columna for fila, columna in coordenadas]
            numeros = filas + columnas
            for posicion in range(0, len(numeros), 2):
                fila, columna = numeros[posicion:posicion + 2]
                letras_resultado.append(alfabeto_clave[fila * 5 + columna])
    return "".join(letras_resultado)


def cifrar_bifid(texto, clave, periodo):
    return transformar_bifid(texto, clave, periodo)


def descifrar_bifid(texto_cifrado, clave, periodo):
    return transformar_bifid(texto_cifrado, clave, periodo, descifrar=True)


def main():
    print("Este cifrado elimina espacios, devuelve mayúsculas y une I/J; no admite ñ ni tildes.")
    while True:
        print("\n1. Cifrar texto\n2. Descifrar texto\n3. Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion in ("1", "2"):
            texto = input("Ingrese el texto: ")
            try:
                clave = input("Ingrese la palabra clave: ").strip()
                periodo = int(input("Ingrese el período (entero positivo): "))
                if opcion == "1":
                    print("Texto cifrado:", cifrar_bifid(texto, clave, periodo))
                else:
                    print("Texto descifrado:", descifrar_bifid(texto, clave, periodo))
            except ValueError as error:
                print("Entrada inválida:", error)
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Elija 1, 2 o 3.")


if __name__ == "__main__":
    main()
