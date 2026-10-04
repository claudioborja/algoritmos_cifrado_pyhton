"""Pruebas de cifrados intermedios, rotores y uso de la biblioteca criptográfica."""

import contextlib
import importlib.util
import io
import os
from pathlib import Path
import random
import stat
import tempfile
import unittest
from unittest.mock import patch

from utilidades_cifrado import codificar_base64, decodificar_base64

RAIZ = Path(__file__).resolve().parents[1]


def cargar_modulo(nombre_archivo):
    especificacion = importlib.util.spec_from_file_location(nombre_archivo, RAIZ / nombre_archivo)
    modulo = importlib.util.module_from_spec(especificacion)
    salida = io.StringIO()
    with contextlib.redirect_stdout(salida):
        especificacion.loader.exec_module(modulo)
    if salida.getvalue():
        raise AssertionError("Importar el algoritmo no debe ejecutar el menú.")
    return modulo


afin = cargar_modulo("8.afin.py")
playfair = cargar_modulo("9.playfair.py")
hill = cargar_modulo("10.hill.py")
vernam = cargar_modulo("11.vernam.py")
enigma = cargar_modulo("12.enigma_simplificada.py")
aes = cargar_modulo("13.aes_gcm.py")
chacha = cargar_modulo("14.chacha20_poly1305.py")
rsa = cargar_modulo("15.rsa_oaep.py")


def ejecutar_menu(modulo, entradas):
    salida = io.StringIO()
    with patch("builtins.input", side_effect=entradas), contextlib.redirect_stdout(salida):
        modulo.main()
    return salida.getvalue()


class PruebasIntermedios(unittest.TestCase):
    def test_afin_ejemplo_y_recuperacion(self):
        self.assertEqual(afin.cifrar_afin("Hola", 5, 8), "Pcji")
        texto = "  Hola Ñandú, áéíóú Ü 123 😀 K!  "
        for multiplicador in [-28, -5, 1, 2, 4, 5, 7, 8, 10, 11, 13, 14, 16, 17, 19, 20, 22, 23, 25, 26, 28]:
            for desplazamiento in [-100, 0, 8, 100]:
                with self.subTest(multiplicador=multiplicador, desplazamiento=desplazamiento):
                    cifrado = afin.cifrar_afin(texto, multiplicador, desplazamiento)
                    self.assertEqual(afin.descifrar_afin(cifrado, multiplicador, desplazamiento), texto)

    def test_afin_claves_invalidas(self):
        for multiplicador, desplazamiento in [(0, 1), (3, 1), (-9, 1), (27, 1), (1.5, 1), (1, "2"), (True, 1)]:
            for funcion in [afin.cifrar_afin, afin.descifrar_afin]:
                with self.assertRaises(ValueError):
                    funcion("Hola", multiplicador, desplazamiento)

    def test_playfair_vector_y_reglas(self):
        self.assertEqual(playfair.cifrar_playfair("Hola", "clave"), "OTAV")
        self.assertEqual(
            playfair.cifrar_playfair("Hide the gold in the tree stump", "playfair example"),
            "BMODZBXDNABEKUDMUIXMMOUVIF",
        )
        self.assertEqual(playfair.preparar_texto("BALLOON"), "BALXLOON")
        self.assertEqual(playfair.preparar_texto("XX"), "XQXQ")
        self.assertEqual(playfair.preparar_texto("J"), "IX")
        tabla = playfair.crear_tabla("clave")
        self.assertEqual(len({letra for fila in tabla for letra in fila}), 25)
        for texto in ["", "Hola", "BALLOON", "XX", "J I", "XQ", "aaaa", "Mi mensaje"]:
            cifrado = playfair.cifrar_playfair(texto, "clave")
            self.assertEqual(playfair.descifrar_playfair(cifrado, "clave"), playfair.preparar_texto(texto))

    def test_playfair_entradas_invalidas(self):
        for texto in ["ñ", "á", "123", "hola!", "ß"]:
            with self.assertRaises(ValueError):
                playfair.cifrar_playfair(texto, "clave")
        for texto_cifrado in ["A", "JJ", "ññ"]:
            with self.assertRaises(ValueError):
                playfair.descifrar_playfair(texto_cifrado, "clave")
        with self.assertRaises(ValueError):
            playfair.cifrar_playfair("Hola", " ")

    def test_hill_inversa_y_recuperacion(self):
        clave = [[1, 2], [3, 5]]
        self.assertEqual(hill.invertir_matriz(clave), [[22, 2], [3, 26]])
        self.assertEqual(hill.cifrar_hill("Hola", clave), "Kolg")
        self.assertEqual(hill.cifrar_hill("Ho la", clave), "Ko lg")
        for matriz in [clave, [[2, 3], [1, 2]], [[-1, 0], [0, 1]], [[100, 2], [3, 5]]]:
            inversa = hill.invertir_matriz(matriz)
            for fila in range(2):
                for columna in range(2):
                    producto = sum(matriz[fila][indice] * inversa[indice][columna] for indice in range(2)) % 27
                    self.assertEqual(producto, int(fila == columna))
            for texto in ["", "Hola", "ñZá!", "  Ho la áéíóú Ü 123 😀 K!  "]:
                cifrado = hill.cifrar_hill(texto, matriz)
                self.assertEqual(hill.descifrar_hill(cifrado, matriz), texto)

    def test_hill_entradas_invalidas(self):
        for matriz in [None, [], [[1, 2]], [[1, 2], [2, 4]], [[3, 3], [2, 5]], [[1, 2], [3, "5"]]]:
            with self.assertRaises(ValueError):
                hill.cifrar_hill("Hola", matriz)
        for funcion in [hill.cifrar_hill, hill.descifrar_hill]:
            with self.assertRaises(ValueError):
                funcion("Sol", [[1, 2], [3, 5]])

    def test_vernam_vector_unicode_y_longitud(self):
        self.assertEqual(vernam.cifrar_vernam("Hola", bytes([1, 2, 3, 4])), "SW1vZQ==")
        for texto in ["", "Hola", "  Ñ áéíóú 😀 中文  "]:
            clave = vernam.generar_clave(len(texto.encode("utf-8")))
            cifrado = vernam.cifrar_vernam(texto, clave)
            self.assertEqual(vernam.descifrar_vernam(cifrado, clave), texto)
        for clave in [b"", b"12345", "1234"]:
            with self.assertRaises(ValueError):
                vernam.cifrar_vernam("Hola", clave)
        with self.assertRaises(ValueError):
            vernam.descifrar_vernam("%%%", b"1234")
        with self.assertRaises(ValueError):
            vernam.generar_clave(-1)
        # XOR no autentica: una alteración puede cambiar el mensaje sin producir error.
        self.assertEqual(vernam.descifrar_vernam(codificar_base64(b"B"), b"\0"), "B")

    def test_menus_intermedios(self):
        casos = [
            (afin, ["9", "1", "Hola", "3", "8", "1", "Hola", "5", "8", "2", "Pcji", "5", "8", "3"], "Pcji", "Hola"),
            (playfair, ["9", "1", "ñ", "clave", "1", "Hola", "clave", "2", "OTAV", "clave", "3"], "OTAV", "HOLA"),
            (hill, ["9", "1", "Hola", "1 2", "1", "Hola", "1 2 3 5", "2", "Kolg", "1 2 3 5", "3"], "Kolg", "Hola"),
        ]
        for modulo, entradas, cifrado, original in casos:
            salida = ejecutar_menu(modulo, entradas)
            self.assertIn("Opción no válida", salida)
            self.assertIn(f"Texto cifrado: {cifrado}", salida)
            self.assertIn(original, salida)
        salida = ejecutar_menu(vernam, ["9", "2", "%%%", "AQ==", "1", "Hola", "2", "SW1vZQ==", "AQIDBA==", "3"])
        self.assertIn("Texto descifrado: Hola", salida)
        self.assertIn("Base64 válido", salida)


class PruebasEnigma(unittest.TestCase):
    def test_permutaciones_reflector_y_avance(self):
        for rotor in enigma.ROTORES:
            self.assertEqual(sorted(rotor), sorted(enigma.ALFABETO))
        for posicion, letra in enumerate(enigma.REFLECTOR):
            self.assertEqual(enigma.REFLECTOR[enigma.ALFABETO.index(letra)], enigma.ALFABETO[posicion])
        for entrada, esperado in [([0, 0, 25], [0, 1, 0]), ([0, 25, 25], [1, 0, 0]), ([25, 25, 25], [0, 0, 0])]:
            enigma.avanzar_rotores(entrada)
            self.assertEqual(entrada, esperado)

    def test_recuperacion_reinicio_y_validacion(self):
        self.assertEqual(enigma.cifrar_enigma("Hola", "aaa"), "Iibg")
        generador = random.Random(17)
        texto = "  Ñ áéíóú Ü 😀 K " + "".join(generador.choice(enigma.ALFABETO + " ABC") for posicion in range(1500))
        for posiciones in ["aaa", "azx", "ZZZ"]:
            cifrado = enigma.cifrar_enigma(texto, posiciones)
            self.assertEqual(enigma.descifrar_enigma(cifrado, posiciones), texto)
            self.assertEqual(enigma.cifrar_enigma(texto, posiciones), cifrado)
        for posiciones in ["", "aaaa", "ñaa", "a1a"]:
            with self.assertRaises(ValueError):
                enigma.cifrar_enigma("Hola", posiciones)
        salida = ejecutar_menu(enigma, ["9", "1", "Hola", "a1a", "1", "Hola", "aaa", "2", "Iibg", "aaa", "3"])
        self.assertIn("Texto descifrado: Hola", salida)
        self.assertIn("Ingrese 3 letras", salida)


class PruebasCifradoAutenticado(unittest.TestCase):
    ALGORITMOS = [(aes, aes.cifrar_aes_gcm, aes.descifrar_aes_gcm),
                  (chacha, chacha.cifrar_chacha20, chacha.descifrar_chacha20)]

    def test_unicode_vacio_y_nonce_nuevo(self):
        for modulo, cifrar, descifrar in self.ALGORITMOS:
            clave = modulo.generar_clave()
            self.assertEqual(len(clave), 32)
            for texto in ["", "Hola", "  Ñ áéíóú Ü 😀 中文  "]:
                primero, segundo = cifrar(texto, clave), cifrar(texto, clave)
                self.assertEqual(descifrar(primero, clave), texto)
                self.assertEqual(descifrar(segundo, clave), texto)
                self.assertNotEqual(decodificar_base64(primero)[:12], decodificar_base64(segundo)[:12])
                self.assertEqual(len(decodificar_base64(primero)), 28 + len(texto.encode("utf-8")))

    def test_modificaciones_clave_y_paquetes_invalidos(self):
        for modulo, cifrar, descifrar in self.ALGORITMOS:
            clave = b"\0" * 32
            cifrado = cifrar("Hola", clave)
            paquete = decodificar_base64(cifrado)
            for posicion in [0, 12, len(paquete) - 1]:
                modificado = bytearray(paquete)
                modificado[posicion] ^= 1
                with self.assertRaisesRegex(ValueError, "autenticar"):
                    descifrar(codificar_base64(bytes(modificado)), clave)
            with self.assertRaisesRegex(ValueError, "autenticar"):
                descifrar(cifrado, b"\1" * 32)
            for invalido in ["%%%", "ñ", codificar_base64(b"123"), ""]:
                with self.assertRaises(ValueError):
                    descifrar(invalido, clave)
            for clave_invalida in [b"", b"a" * 16, "a" * 32]:
                with self.assertRaises(ValueError):
                    cifrar("Hola", clave_invalida)

    def test_menus_modernos(self):
        for modulo, cifrar, descifrar in self.ALGORITMOS:
            clave = modulo.generar_clave()
            paquete = cifrar("Hola ñá 😀", clave)
            salida = ejecutar_menu(modulo, ["9", "1", "Hola", "%%%", "1", "Hola", "", "2", paquete, codificar_base64(clave), "3"])
            self.assertIn("Texto descifrado: Hola ñá 😀", salida)
            self.assertIn("Paquete cifrado (Base64)", salida)
            self.assertIn("Base64 válido", salida)


class PruebasRSA(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.clave_privada, cls.clave_publica = rsa.generar_claves()

    def test_recuperacion_y_limite_utf8(self):
        for texto in ["", "  Hola ñá 😀  ", "a" * 190, "ñ" * 95]:
            cifrado = rsa.cifrar_rsa(texto, self.clave_publica)
            self.assertEqual(rsa.descifrar_rsa(cifrado, self.clave_privada), texto)
        for texto in ["a" * 191, "ñ" * 96]:
            with self.assertRaisesRegex(ValueError, "190 bytes"):
                rsa.cifrar_rsa(texto, self.clave_publica)
        self.assertNotEqual(rsa.cifrar_rsa("Hola", self.clave_publica), rsa.cifrar_rsa("Hola", self.clave_publica))

    def test_clave_incorrecta_y_modificaciones(self):
        cifrado = rsa.cifrar_rsa("Hola", self.clave_publica)
        otra_privada, otra_publica = rsa.generar_claves()
        with self.assertRaises(ValueError):
            rsa.descifrar_rsa(cifrado, otra_privada)
        paquete = bytearray(decodificar_base64(cifrado))
        paquete[-1] ^= 1
        for invalido in [codificar_base64(bytes(paquete)), "%%%", codificar_base64(b"123")]:
            with self.assertRaises(ValueError):
                rsa.descifrar_rsa(invalido, self.clave_privada)
        with self.assertRaises(ValueError):
            rsa.cifrar_rsa("Hola", self.clave_privada)

    def test_guardar_cargar_contrasena_y_no_sobrescribir(self):
        with tempfile.TemporaryDirectory() as temporal:
            carpeta = Path(temporal) / "claves"
            privada, publica = rsa.guardar_claves(carpeta, b"contrasena de prueba")
            datos_originales = privada.read_bytes()
            self.assertIn(b"BEGIN ENCRYPTED PRIVATE KEY", datos_originales)
            clave_publica = rsa.cargar_clave_publica(publica)
            clave_privada = rsa.cargar_clave_privada(privada, b"contrasena de prueba")
            cifrado = rsa.cifrar_rsa("Hola ñá", clave_publica)
            self.assertEqual(rsa.descifrar_rsa(cifrado, clave_privada), "Hola ñá")
            with self.assertRaises(ValueError):
                rsa.cargar_clave_privada(privada, b"otra contrasena")
            with self.assertRaises(ValueError):
                rsa.guardar_claves(carpeta, b"otra contrasena")
            self.assertEqual(privada.read_bytes(), datos_originales)
            with self.assertRaises(ValueError):
                rsa.guardar_claves(Path(temporal) / "sin_contrasena", b"")
            if os.name == "posix":
                self.assertEqual(stat.S_IMODE(privada.stat().st_mode), 0o600)
                self.assertEqual(stat.S_IMODE(carpeta.stat().st_mode), 0o700)
            with patch("getpass.getpass", return_value="contrasena de prueba"):
                salida = ejecutar_menu(rsa, ["9", "2", str(Path(temporal) / "no_existe.pem"),
                                            "2", str(publica), "Hola ñá", "3", str(privada), cifrado, "4"])
            self.assertIn("Texto descifrado: Hola ñá", salida)
            self.assertIn("No se pudo completar", salida)
            carpeta_menu = Path(temporal) / "desde_menu"
            with patch("getpass.getpass", return_value="contrasena de prueba"):
                ejecutar_menu(rsa, ["1", str(carpeta_menu), "4"])
            self.assertTrue((carpeta_menu / "clave_privada.pem").exists())


if __name__ == "__main__":
    unittest.main()
