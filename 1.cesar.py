def cifrador_cesar(texto, desplazamiento):
    texto_cifrado = ""
    for caracter in texto:
        if caracter.isalpha():  # Verificar si es una letra
            if caracter.islower():
                nuevo_caracter = chr((ord(caracter) - 97 + desplazamiento) % 27 + 97)
            else:
                nuevo_caracter = chr((ord(caracter) - 65 + desplazamiento) % 27 + 65)
        else:  # Mantener los caracteres especiales sin cambios
            nuevo_caracter = caracter
        texto_cifrado += nuevo_caracter
    return texto_cifrado

def descifrador_cesar(texto_cifrado):
    for desplazamiento in range(27):
        texto_descifrado = ""
        for caracter in texto_cifrado:
            if caracter.isalpha():  # Verificar si es una letra
                if caracter.islower():
                    nuevo_caracter = chr((ord(caracter) - 97 - desplazamiento) % 27 + 97)
                else:
                    nuevo_caracter = chr((ord(caracter) - 65 - desplazamiento) % 27 + 65)
            else:  # Mantener los caracteres especiales sin cambios
                nuevo_caracter = caracter
            texto_descifrado += nuevo_caracter
        print(f"Desplazamiento {desplazamiento}: {texto_descifrado}")

# Ciclo principal para mostrar un menú y ejecutar las funciones según la opción seleccionada
while True:
    print("1. Cifrar")
    print("2. Descifrar")
    print("3. Salir")
    opcion = input("Elija una opción: ")

    if opcion == '1':  
        texto_original = input("Ingrese el texto a cifrar: ")  
        desplazamiento = int(input("Ingrese el valor de desplazamiento: "))  
        texto_cifrado = cifrador_cesar(texto_original, desplazamiento)  
        print("Texto cifrado:", texto_cifrado)  
    elif opcion == '2':  
        texto_cifrado = input("Ingrese el texto cifrado: ")  
        descifrador_cesar(texto_cifrado)  
    elif opcion == '3':  
        print("¡Hasta luego!")  
        break  
    else:  
        print("Opción no válida. Por favor, elija una opción válida.")  
