"""Bacon de 26 letras: cada letra se representa con cinco símbolos A/B."""

from utilidades_clasicas import ALFABETO_LATINO, normalizar_texto


def cifrar_bacon(texto):
    texto = normalizar_texto(texto, ALFABETO_LATINO)
    grupos = []
    for letra in texto:
        bits = format(ALFABETO_LATINO.index(letra), "05b")
        grupos.append(bits.replace("0", "A").replace("1", "B"))
    return " ".join(grupos)


def descifrar_bacon(texto_cifrado):
    simbolos = normalizar_texto(texto_cifrado, "AB")
    if len(simbolos) % 5:
        raise ValueError("El mensaje cifrado debe contener grupos de cinco símbolos A/B.")
    letras = []
    for inicio in range(0, len(simbolos), 5):
        bits = simbolos[inicio:inicio + 5].replace("A", "0").replace("B", "1")
        posicion = int(bits, 2)
        if posicion >= len(ALFABETO_LATINO):
            raise ValueError("El grupo A/B no corresponde a ninguna de las 26 letras.")
        letras.append(ALFABETO_LATINO[posicion])
    return "".join(letras)


def main():
    print("Este cifrado elimina espacios y devuelve mayúsculas; no admite ñ ni tildes en el mensaje.")
    while True:
        print("\n1. Cifrar texto\n2. Descifrar texto\n3. Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion in ("1", "2"):
            texto = input("Ingrese el texto: ")
            try:
                if opcion == "1":
                    print("Texto cifrado:", cifrar_bacon(texto))
                else:
                    print("Texto descifrado:", descifrar_bacon(texto))
            except ValueError as error:
                print("Entrada inválida:", error)
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Elija 1, 2 o 3.")


if __name__ == "__main__":
    main()
