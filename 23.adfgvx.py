"""ADFGVX: cuadrado de 6 × 6 y transposición por columnas."""

from utilidades_clasicas import ALFABETO_ESPANOL, crear_alfabeto_clave, normalizar_texto, validar_clave_espanola

ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
SIMBOLOS = "ADFGVX"


def obtener_orden_columnas(clave_columnas):
    return sorted(range(len(clave_columnas)), key=lambda columna: ALFABETO_ESPANOL.index(clave_columnas[columna]))


def transponer_columnas(texto, clave_columnas, descifrar=False):
    cantidad_columnas = len(clave_columnas)
    orden_columnas = obtener_orden_columnas(clave_columnas)
    if not descifrar:
        return "".join(texto[columna::cantidad_columnas] for columna in orden_columnas)
    filas_completas, columnas_con_extra = divmod(len(texto), cantidad_columnas)
    caracteres_originales = [""] * len(texto)
    inicio_columna = 0
    for columna in orden_columnas:
        longitud_columna = filas_completas + int(columna < columnas_con_extra)
        texto_columna = texto[inicio_columna:inicio_columna + longitud_columna]
        for fila, caracter in enumerate(texto_columna):
            caracteres_originales[fila * cantidad_columnas + columna] = caracter
        inicio_columna += longitud_columna
    return "".join(caracteres_originales)


def cifrar_adfgvx(texto, clave_tabla, clave_columnas):
    alfabeto_clave = crear_alfabeto_clave(clave_tabla, ALFABETO)
    clave_columnas = validar_clave_espanola(clave_columnas)
    texto = normalizar_texto(texto, ALFABETO)
    coordenadas = []
    for letra in texto:
        fila, columna = divmod(alfabeto_clave.index(letra), 6)
        coordenadas.append(SIMBOLOS[fila] + SIMBOLOS[columna])
    return transponer_columnas("".join(coordenadas), clave_columnas)


def descifrar_adfgvx(texto_cifrado, clave_tabla, clave_columnas):
    alfabeto_clave = crear_alfabeto_clave(clave_tabla, ALFABETO)
    clave_columnas = validar_clave_espanola(clave_columnas)
    texto_cifrado = normalizar_texto(texto_cifrado, SIMBOLOS)
    if len(texto_cifrado) % 2:
        raise ValueError("El texto cifrado debe contener una cantidad par de símbolos ADFGVX.")
    coordenadas = transponer_columnas(texto_cifrado, clave_columnas, descifrar=True)
    letras = []
    for posicion in range(0, len(coordenadas), 2):
        fila = SIMBOLOS.index(coordenadas[posicion])
        columna = SIMBOLOS.index(coordenadas[posicion + 1])
        letras.append(alfabeto_clave[fila * 6 + columna])
    return "".join(letras)


def main():
    print("Este cifrado elimina espacios y devuelve mayúsculas; no admite ñ ni tildes en el mensaje.")
    while True:
        print("\n1. Cifrar texto\n2. Descifrar texto\n3. Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion in ("1", "2"):
            texto = input("Ingrese el texto: ")
            try:
                clave_tabla = input("Ingrese la clave de la tabla (letras o números): ")
                clave_columnas = input("Ingrese la clave de columnas (letras españolas): ").strip()
                if opcion == "1":
                    print("Texto cifrado:", cifrar_adfgvx(texto, clave_tabla, clave_columnas))
                else:
                    print("Texto descifrado:", descifrar_adfgvx(texto, clave_tabla, clave_columnas))
            except ValueError as error:
                print("Entrada inválida:", error)
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Elija 1, 2 o 3.")


if __name__ == "__main__":
    main()
