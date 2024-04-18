def cifrar(texto, desplazamiento):
    # Función para cifrar un texto utilizando el cifrado César
    texto_cifrado = ""
    for caracter in texto:
        if caracter.isalpha():
            # Calcula la nueva letra cifrada utilizando el desplazamiento proporcionado
            nueva_letra = chr(((ord(caracter) - ord('a') + desplazamiento) % 26) + ord('a'))
            texto_cifrado += nueva_letra
        else:
            texto_cifrado += caracter  # Si el caracter no es una letra, se agrega sin cifrar al texto cifrado
    return texto_cifrado

def descifrar(texto_cifrado):
    # Función para descifrar un texto cifrado utilizando fuerza bruta
    resultados = []  
    for desplazamiento in range(26):  # Itera sobre todos los posibles desplazamientos (0 al 25)
        texto_descifrado = ""  
        for caracter in texto_cifrado:  
            if caracter.isalpha():  
                nueva_letra = chr(((ord(caracter) - ord('a') - desplazamiento) % 26) + ord('a'))
                texto_descifrado += nueva_letra  # Agrega el nuevo caracter descifrado al texto descifrado
            else:
                texto_descifrado += caracter  
        resultados.append(texto_descifrado)  
    return resultados  

def main():
    while True:
        print("1. Cifrar texto")
        print("2. Descifrar texto")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")  

        if opcion == '1':  
            texto = input("Ingrese el texto a cifrar: ").lower()
            desplazamiento = int(input("Ingrese el valor de desplazamiento (0-25): "))
            texto_cifrado = cifrar(texto, desplazamiento) 
            print("Texto cifrado:", texto_cifrado)  

        elif opcion == '2': 
            texto_cifrado = input("Ingrese el texto cifrado: ").lower() 
            resultados_descifrado = descifrar(texto_cifrado)  
            print("Posibles textos descifrados:")  
            for idx, resultado in enumerate(resultados_descifrado):  
                print(f"Desplazamiento {idx}: {resultado}")  

        elif opcion == '3':  
            print("Saliendo...")  
            break  

        else:  
            print("Opción no válida. Por favor, seleccione una opción válida.") 

if __name__ == "__main__":
    main()  
