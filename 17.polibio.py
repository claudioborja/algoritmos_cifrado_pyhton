"""Cuadrado de Polibio de 5 × 5, con I/J en la misma casilla."""

from utilidades_clasicas import ALFABETO_POLIBIO, crear_alfabeto_clave, normalizar_texto


def cifrar_polibio(texto, clave):
    alfabeto_clave = crear_alfabeto_clave(clave, ALFABETO_POLIBIO, unir_ij=True)
    texto = normalizar_texto(texto, ALFABETO_POLIBIO, unir_ij=True)
    coordenadas = []
    for letra in texto:
        fila, columna = divmod(alfabeto_clave.index(letra), 5)
        coordenadas.append(f"{fila + 1}{columna + 1}")
    return " ".join(coordenadas)


def descifrar_polibio(texto_cifrado, clave):
    alfabeto_clave = crear_alfabeto_clave(clave, ALFABETO_POLIBIO, unir_ij=True)
    digitos = "".join(caracter for caracter in texto_cifrado if not caracter.isspace())
    if len(digitos) % 2 or any(digito not in "12345" for digito in digitos):
        raise ValueError("Ingrese parejas de coordenadas entre 11 y 55; cada dígito debe estar entre 1 y 5.")
    letras = []
    for posicion in range(0, len(digitos), 2):
        fila = int(digitos[posicion]) - 1
        columna = int(digitos[posicion + 1]) - 1
        letras.append(alfabeto_clave[fila * 5 + columna])
    return "".join(letras)


def main():
    print("Este cifrado elimina espacios, devuelve mayúsculas y une I/J; no admite ñ ni tildes.")
    while True:
        print("\n1. Cifrar texto\n2. Descifrar texto\n3. Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion in ("1", "2"):
            texto = input("Ingrese el texto: ")
            try:
                clave = input("Ingrese la palabra clave: ").strip()
                if opcion == "1":
                    print("Texto cifrado:", cifrar_polibio(texto, clave))
                else:
                    print("Texto descifrado:", descifrar_polibio(texto, clave))
            except ValueError as error:
                print("Entrada inválida:", error)
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Elija 1, 2 o 3.")


if __name__ == "__main__":
    main()
