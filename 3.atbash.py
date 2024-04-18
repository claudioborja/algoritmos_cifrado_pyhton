def atbash_cipher(text):
    result = ""
    for char in text:
        if char.isalpha():
            if char.isupper():
                result += chr(90 - (ord(char) - 65))
            else:
                result += chr(122 - (ord(char) - 97))
        else:
            result += char
    return result

def main():
    while True:
        print("1. Cifrar mensaje")
        print("2. Descifrar mensaje")
        print("3. Salir")
        choice = input("Seleccione una opción: ")

        if choice == "1":
            message = input("Ingrese el mensaje a cifrar: ")
            encrypted_message = atbash_cipher(message)
            print("Mensaje cifrado:", encrypted_message)
        elif choice == "2":
            message = input("Ingrese el mensaje a descifrar: ")
            decrypted_message = atbash_cipher(message)
            print("Mensaje descifrado:", decrypted_message)
        elif choice == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, seleccione 1, 2 o 3.")

if __name__ == "__main__":
    main()
