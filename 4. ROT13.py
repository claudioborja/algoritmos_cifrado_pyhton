def cifrar_rot13(texto):
    resultado = ''
    for char in texto:
        if char.isalpha():
            offset = 13 if char.islower() else -13
            resultado += chr((ord(char) - ord('a' if char.islower() else 'A') + offset) % 26 + ord('a' if char.islower() else 'A'))
        else:
            resultado += char
    return resultado

def descifrar_rot13(texto):
    return cifrar_rot13(texto)

def main():
    while True:
        print("1. Cifrar texto")
        print("2. Descifrar texto")
        print("3. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            texto = input("Introduce el texto a cifrar: ")
            texto_cifrado = cifrar_rot13(texto)
            print("Texto cifrado:", texto_cifrado)
        elif opcion == '2':
            texto = input("Introduce el texto a descifrar: ")
            texto_descifrado = descifrar_rot13(texto)
            print("Texto descifrado:", texto_descifrado)
        elif opcion == '3':
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Por favor, selecciona una opción válida.")

if __name__ == "__main__":
    main()
