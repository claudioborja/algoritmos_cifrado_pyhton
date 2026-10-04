"""Rail Fence distribuye el texto en un zigzag y lo lee por filas."""


def validar_cantidad_rieles(cantidad_rieles):
    if not isinstance(cantidad_rieles, int) or isinstance(cantidad_rieles, bool) or cantidad_rieles < 1:
        raise ValueError("La cantidad de rieles debe ser un número entero mayor o igual que 1.")


def obtener_recorrido(longitud_texto, cantidad_rieles):
    """Devuelve el riel correspondiente a cada posición del texto."""
    recorrido = []
    riel_actual = 0
    direccion = 1
    for posicion in range(longitud_texto):
        recorrido.append(riel_actual)
        if cantidad_rieles > 1:
            if riel_actual == 0:
                direccion = 1
            elif riel_actual == cantidad_rieles - 1:
                direccion = -1
            riel_actual += direccion
    return recorrido


def cifrar_rail_fence(texto, cantidad_rieles):
    validar_cantidad_rieles(cantidad_rieles)
    # Estos casos no cambian el texto y evitan crear filas innecesarias.
    if cantidad_rieles == 1 or cantidad_rieles >= len(texto):
        return texto
    recorrido = obtener_recorrido(len(texto), cantidad_rieles)
    rieles = [[] for riel in range(cantidad_rieles)]
    for caracter, riel in zip(texto, recorrido):
        rieles[riel].append(caracter)
    return "".join("".join(caracteres_riel) for caracteres_riel in rieles)


def descifrar_rail_fence(texto_cifrado, cantidad_rieles):
    validar_cantidad_rieles(cantidad_rieles)
    if cantidad_rieles == 1 or cantidad_rieles >= len(texto_cifrado):
        return texto_cifrado
    recorrido = obtener_recorrido(len(texto_cifrado), cantidad_rieles)
    cantidades_por_riel = [0] * cantidad_rieles
    for riel in recorrido:
        cantidades_por_riel[riel] += 1
    rieles = []
    inicio_riel = 0
    for cantidad_caracteres in cantidades_por_riel:
        fin_riel = inicio_riel + cantidad_caracteres
        rieles.append(texto_cifrado[inicio_riel:fin_riel])
        inicio_riel = fin_riel
    posiciones_por_riel = [0] * cantidad_rieles
    caracteres_originales = []
    for riel in recorrido:
        posicion_en_riel = posiciones_por_riel[riel]
        caracteres_originales.append(rieles[riel][posicion_en_riel])
        posiciones_por_riel[riel] += 1
    return "".join(caracteres_originales)


def main():
    while True:
        print("\n1. Cifrar texto")
        print("2. Descifrar texto")
        print("3. Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion in ("1", "2"):
            texto = input("Ingrese el texto: ")
            try:
                cantidad_rieles = int(input("Ingrese la cantidad de rieles (mínimo 1): "))
                if opcion == "1":
                    print("Texto cifrado:", cifrar_rail_fence(texto, cantidad_rieles))
                else:
                    print("Texto descifrado:", descifrar_rail_fence(texto, cantidad_rieles))
            except ValueError:
                print("La cantidad de rieles debe ser un número entero mayor o igual que 1.")
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Elija 1, 2 o 3.")


if __name__ == "__main__":
    main()
