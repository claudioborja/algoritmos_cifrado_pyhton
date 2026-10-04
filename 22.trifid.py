"""Trifid con las 27 letras españolas en un cubo de 3 × 3 × 3."""

from utilidades_clasicas import ALFABETO_ESPANOL, crear_alfabeto_clave, normalizar_texto, validar_entero_positivo


def obtener_coordenadas(posicion):
    plano, resto = divmod(posicion, 9)
    fila, columna = divmod(resto, 3)
    return plano, fila, columna


def transformar_trifid(texto, clave, periodo, descifrar=False):
    validar_entero_positivo(periodo, "El período")
    alfabeto_clave = crear_alfabeto_clave(clave, ALFABETO_ESPANOL)
    texto = normalizar_texto(texto, ALFABETO_ESPANOL)
    letras_resultado = []
    for inicio in range(0, len(texto), periodo):
        bloque = texto[inicio:inicio + periodo]
        coordenadas = [obtener_coordenadas(alfabeto_clave.index(letra)) for letra in bloque]
        longitud_bloque = len(bloque)
        if descifrar:
            numeros = [numero for terna in coordenadas for numero in terna]
            planos = numeros[:longitud_bloque]
            filas = numeros[longitud_bloque:2 * longitud_bloque]
            columnas = numeros[2 * longitud_bloque:]
            for plano, fila, columna in zip(planos, filas, columnas):
                letras_resultado.append(alfabeto_clave[plano * 9 + fila * 3 + columna])
        else:
            planos = [plano for plano, fila, columna in coordenadas]
            filas = [fila for plano, fila, columna in coordenadas]
            columnas = [columna for plano, fila, columna in coordenadas]
            numeros = planos + filas + columnas
            for posicion in range(0, len(numeros), 3):
                plano, fila, columna = numeros[posicion:posicion + 3]
                letras_resultado.append(alfabeto_clave[plano * 9 + fila * 3 + columna])
    return "".join(letras_resultado)


def cifrar_trifid(texto, clave, periodo):
    return transformar_trifid(texto, clave, periodo)


def descifrar_trifid(texto_cifrado, clave, periodo):
    return transformar_trifid(texto_cifrado, clave, periodo, descifrar=True)


def main():
    print("Trifid español: elimina espacios y devuelve mayúsculas; admite ñ, pero no tildes.")
    while True:
        print("\n1. Cifrar texto\n2. Descifrar texto\n3. Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion in ("1", "2"):
            texto = input("Ingrese el texto: ")
            try:
                clave = input("Ingrese la palabra clave: ").strip()
                periodo = int(input("Ingrese el período (entero positivo): "))
                if opcion == "1":
                    print("Texto cifrado:", cifrar_trifid(texto, clave, periodo))
                else:
                    print("Texto descifrado:", descifrar_trifid(texto, clave, periodo))
            except ValueError as error:
                print("Entrada inválida:", error)
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Elija 1, 2 o 3.")


if __name__ == "__main__":
    main()
