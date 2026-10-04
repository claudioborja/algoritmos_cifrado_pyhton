"""ElGamal para enteros: demostración matemática con primos pequeños."""

import secrets

from utilidades_matematicas import obtener_factores_primos, validar_primo


def validar_parametros(primo, generador):
    validar_primo(primo)
    if primo < 5 or type(generador) is not int or not 2 <= generador < primo:
        raise ValueError("Use un primo de al menos 5 y un generador entre 2 y primo - 1.")
    for factor in obtener_factores_primos(primo - 1):
        if pow(generador, (primo - 1) // factor, primo) == 1:
            raise ValueError("El generador debe tener orden primo - 1 en el grupo multiplicativo.")


def generar_claves(primo=467, generador=2):
    validar_parametros(primo, generador)
    exponente_privado = secrets.randbelow(primo - 2) + 1
    valor_publico = pow(generador, exponente_privado, primo)
    clave_privada = (primo, exponente_privado)
    clave_publica = (primo, generador, valor_publico)
    return clave_privada, clave_publica


def cifrar_elgamal(mensaje, clave_publica, exponente_efimero=None):
    if not isinstance(clave_publica, (list, tuple)) or len(clave_publica) != 3:
        raise ValueError("La clave pública debe contener primo, generador y valor público.")
    primo, generador, valor_publico = clave_publica
    validar_parametros(primo, generador)
    if type(valor_publico) is not int or not 2 <= valor_publico < primo:
        raise ValueError("El valor público debe estar entre 2 y primo - 1.")
    if type(mensaje) is not int or not 1 <= mensaje < primo:
        raise ValueError("El mensaje debe ser un entero entre 1 y primo - 1.")
    if exponente_efimero is None:
        exponente_efimero = secrets.randbelow(primo - 2) + 1
    if type(exponente_efimero) is not int or not 1 <= exponente_efimero <= primo - 2:
        raise ValueError("El exponente efímero debe estar entre 1 y primo - 2.")
    primer_componente = pow(generador, exponente_efimero, primo)
    secreto_compartido = pow(valor_publico, exponente_efimero, primo)
    segundo_componente = (mensaje * secreto_compartido) % primo
    return primer_componente, segundo_componente


def descifrar_elgamal(texto_cifrado, clave_privada):
    if not isinstance(clave_privada, (list, tuple)) or len(clave_privada) != 2:
        raise ValueError("La clave privada debe contener primo y exponente privado.")
    primo, exponente_privado = clave_privada
    validar_primo(primo)
    if primo < 5 or type(exponente_privado) is not int or not 1 <= exponente_privado <= primo - 2:
        raise ValueError("El exponente privado debe estar entre 1 y primo - 2, con primo de al menos 5.")
    if not isinstance(texto_cifrado, (list, tuple)) or len(texto_cifrado) != 2:
        raise ValueError("El cifrado debe contener dos enteros.")
    if any(type(valor) is not int or not 1 <= valor < primo for valor in texto_cifrado):
        raise ValueError("Los componentes cifrados deben estar entre 1 y primo - 1.")
    primer_componente, segundo_componente = texto_cifrado
    secreto_compartido = pow(primer_componente, exponente_privado, primo)
    return (segundo_componente * pow(secreto_compartido, -1, primo)) % primo


def main():
    print("Demostración con enteros y primos pequeños; no protege datos reales ni autentica mensajes.")
    while True:
        print("\n1. Generar claves\n2. Cifrar entero\n3. Descifrar entero\n4. Salir")
        opcion = input("Seleccione una opción: ").strip()
        try:
            if opcion == "1":
                primo = int(input("Ingrese un primo (vacío: 467): ") or "467")
                generador = int(input("Ingrese un generador (vacío: 2): ") or "2")
                clave_privada, clave_publica = generar_claves(primo, generador)
                print("Clave pública (primo generador valor):", *clave_publica)
                print("Clave privada (primo exponente):", *clave_privada)
            elif opcion == "2":
                clave_publica = tuple(int(valor) for valor in input("Ingrese primo generador valor público: ").split())
                mensaje = int(input("Ingrese el entero que desea cifrar: "))
                print("Cifrado (dos enteros):", *cifrar_elgamal(mensaje, clave_publica))
            elif opcion == "3":
                clave_privada = tuple(int(valor) for valor in input("Ingrese primo exponente privado: ").split())
                texto_cifrado = tuple(int(valor) for valor in input("Ingrese los dos enteros cifrados: ").split())
                print("Entero descifrado:", descifrar_elgamal(texto_cifrado, clave_privada))
            elif opcion == "4":
                print("¡Hasta luego!")
                break
            else:
                print("Opción no válida. Elija 1, 2, 3 o 4.")
        except ValueError as error:
            print("Entrada inválida:", error)


if __name__ == "__main__":
    main()
