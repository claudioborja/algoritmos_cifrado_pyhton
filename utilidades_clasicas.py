"""Preparación explícita de alfabetos para los cifrados clásicos adicionales."""

ALFABETO_LATINO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALFABETO_ESPANOL = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
ALFABETO_POLIBIO = "ABCDEFGHIKLMNOPQRSTUVWXYZ"


def normalizar_texto(texto, alfabeto, unir_ij=False):
    """Quita espacios y convierte a mayúsculas; rechaza símbolos fuera del alfabeto."""
    letras = []
    letras_permitidas = alfabeto + ("J" if unir_ij else "")
    for caracter in texto:
        if caracter.isspace():
            continue
        if caracter not in letras_permitidas and caracter not in letras_permitidas.lower():
            raise ValueError("El texto contiene caracteres que no pertenecen al alfabeto de este cifrado.")
        letra = caracter.upper()
        if unir_ij and letra == "J":
            letra = "I"
        letras.append(letra)
    return "".join(letras)


def crear_alfabeto_clave(clave, alfabeto, unir_ij=False):
    clave = normalizar_texto(clave, alfabeto, unir_ij)
    if not clave:
        raise ValueError("La clave debe contener al menos una letra o símbolo del alfabeto.")
    letras_unicas = []
    for letra in clave + alfabeto:
        if letra not in letras_unicas:
            letras_unicas.append(letra)
    return "".join(letras_unicas)


def validar_clave_espanola(clave):
    if not clave or any(letra not in ALFABETO_ESPANOL + ALFABETO_ESPANOL.lower() for letra in clave):
        raise ValueError("La clave debe contener letras españolas, sin espacios ni tildes.")
    return clave.upper()


def validar_entero_positivo(numero, nombre):
    if type(numero) is not int or numero < 1:
        raise ValueError(f"{nombre} debe ser un número entero mayor o igual que 1.")
