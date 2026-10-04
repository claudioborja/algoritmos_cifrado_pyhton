"""Playfair con una tabla de 5 × 5: I y J comparten casilla."""

ALFABETO = "ABCDEFGHIKLMNOPQRSTUVWXYZ"


def normalizar_texto(texto):
    """Elimina espacios, convierte a mayúsculas y reemplaza J por I."""
    letras = []
    for caracter in texto:
        if caracter.isspace():
            continue
        if caracter.lower() not in "abcdefghijklmnopqrstuvwxyz":
            raise ValueError("Playfair admite solo letras de a a z y espacios, sin ñ ni tildes.")
        letras.append(caracter.upper().replace("J", "I"))
    return "".join(letras)


def crear_tabla(clave):
    clave = normalizar_texto(clave)
    if not clave:
        raise ValueError("La clave debe contener al menos una letra.")
    letras_unicas = []
    for letra in clave + ALFABETO:
        if letra not in letras_unicas:
            letras_unicas.append(letra)
    return [letras_unicas[inicio:inicio + 5] for inicio in range(0, 25, 5)]


def preparar_texto(texto):
    texto = normalizar_texto(texto)
    parejas = []
    posicion = 0
    while posicion < len(texto):
        primera_letra = texto[posicion]
        # Q evita formar XX cuando la primera letra ya es X.
        relleno = "Q" if primera_letra == "X" else "X"
        if posicion + 1 == len(texto) or texto[posicion + 1] == primera_letra:
            parejas.append(primera_letra + relleno)
            posicion += 1
        else:
            parejas.append(texto[posicion:posicion + 2])
            posicion += 2
    return "".join(parejas)


def transformar_parejas(texto, tabla, direccion):
    posiciones_letras = {}
    for fila in range(5):
        for columna in range(5):
            posiciones_letras[tabla[fila][columna]] = (fila, columna)
    letras_resultado = []
    for posicion in range(0, len(texto), 2):
        fila_primera, columna_primera = posiciones_letras[texto[posicion]]
        fila_segunda, columna_segunda = posiciones_letras[texto[posicion + 1]]
        if fila_primera == fila_segunda:
            letras_resultado.append(tabla[fila_primera][(columna_primera + direccion) % 5])
            letras_resultado.append(tabla[fila_segunda][(columna_segunda + direccion) % 5])
        elif columna_primera == columna_segunda:
            letras_resultado.append(tabla[(fila_primera + direccion) % 5][columna_primera])
            letras_resultado.append(tabla[(fila_segunda + direccion) % 5][columna_segunda])
        else:
            letras_resultado.append(tabla[fila_primera][columna_segunda])
            letras_resultado.append(tabla[fila_segunda][columna_primera])
    return "".join(letras_resultado)


def cifrar_playfair(texto, clave):
    tabla = crear_tabla(clave)
    return transformar_parejas(preparar_texto(texto), tabla, 1)


def descifrar_playfair(texto_cifrado, clave):
    tabla = crear_tabla(clave)
    if "j" in texto_cifrado.lower():
        raise ValueError("El texto cifrado no puede contener J; la tabla utiliza I.")
    texto_cifrado = normalizar_texto(texto_cifrado)
    if len(texto_cifrado) % 2 != 0:
        raise ValueError("El texto cifrado debe contener una cantidad par de letras.")
    return transformar_parejas(texto_cifrado, tabla, -1)


def main():
    print("Playfair elimina espacios, une I/J y devuelve mayúsculas con relleno X o Q.")
    while True:
        print("\n1. Cifrar texto\n2. Descifrar texto\n3. Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion in ("1", "2"):
            texto = input("Ingrese el texto (sin ñ ni tildes): ")
            clave = input("Ingrese la palabra clave: ")
            try:
                if opcion == "1":
                    print("Texto cifrado:", cifrar_playfair(texto, clave))
                else:
                    print("Texto descifrado preparado:", descifrar_playfair(texto, clave))
            except ValueError as error:
                print(error)
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Elija 1, 2 o 3.")


if __name__ == "__main__":
    main()
