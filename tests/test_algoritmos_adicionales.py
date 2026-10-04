"""Vectores publicados, límites, normalización y menús de los once algoritmos nuevos."""

import json
from math import gcd
from pathlib import Path
import random
import tempfile
import unittest
from unittest.mock import patch

from test_algoritmos_intermedios_avanzados import cargar_modulo, ejecutar_menu
from utilidades_cifrado import codificar_base64, decodificar_base64
from utilidades_clasicas import ALFABETO_ESPANOL, ALFABETO_LATINO, ALFABETO_POLIBIO, normalizar_texto

escitala = cargar_modulo("16.escitala.py")
polibio = cargar_modulo("17.polibio.py")
bacon = cargar_modulo("18.bacon.py")
beaufort = cargar_modulo("19.beaufort.py")
autoclave = cargar_modulo("20.autoclave.py")
bifid = cargar_modulo("21.bifid.py")
trifid = cargar_modulo("22.trifid.py")
adfgvx = cargar_modulo("23.adfgvx.py")
elgamal = cargar_modulo("24.elgamal.py")
paillier = cargar_modulo("25.paillier.py")
hibrido = cargar_modulo("26.hibrido_rsa_aes.py")


class PruebasClasicosAdicionales(unittest.TestCase):
    def test_escitala_ejemplo_y_recuperacion(self):
        self.assertEqual(escitala.cifrar_escitala("HOLAAMIGO", 3), "HAIOAGLMO")
        for texto in ["", "a", "HOLA", "  Ñ áéíóú 中文 😀  "]:
            for columnas in [1, 2, 3, 5, 1000000]:
                cifrado = escitala.cifrar_escitala(texto, columnas)
                self.assertEqual(escitala.descifrar_escitala(cifrado, columnas), texto)
                self.assertEqual(sorted(cifrado), sorted(texto))
        for columnas in [0, -1, 1.5, True]:
            with self.assertRaises(ValueError):
                escitala.cifrar_escitala("Hola", columnas)

    def test_polibio_coordenadas_y_normalizacion(self):
        self.assertEqual(polibio.cifrar_polibio("Hola", "clave"), "25 35 12 13")
        self.assertEqual(polibio.cifrar_polibio("ABC", "a"), "11 12 13")
        self.assertEqual(polibio.descifrar_polibio("25131235", "clave"), "HALO")
        for texto in ["", "J I", "abcdefghijklmnopqrstuvwxyz", "Hola mundo"]:
            cifrado = polibio.cifrar_polibio(texto, "claves repetidas")
            self.assertEqual(polibio.descifrar_polibio(cifrado, "claves repetidas"), normalizar_texto(texto, ALFABETO_POLIBIO, True))
        for cifrado in ["1", "00", "66", "١١", "AB"]:
            with self.assertRaises(ValueError):
                polibio.descifrar_polibio(cifrado, "clave")

    def test_bacon_variante_26_letras(self):
        self.assertEqual(bacon.cifrar_bacon("ABCZ"), "AAAAA AAAAB AAABA BBAAB")
        self.assertEqual(bacon.descifrar_bacon(bacon.cifrar_bacon(ALFABETO_LATINO)), ALFABETO_LATINO)
        self.assertEqual(bacon.descifrar_bacon(bacon.cifrar_bacon("I J U V")), "IJUV")
        self.assertEqual(bacon.descifrar_bacon(""), "")
        for cifrado in ["A", "BBBBB", "BBAAAAB", "AAAAC"]:
            with self.assertRaises(ValueError):
                bacon.descifrar_bacon(cifrado)

    def test_beaufort_y_autoclave(self):
        self.assertEqual(beaufort.cifrar_beaufort("Hola", "sol"), "Maas")
        self.assertEqual(autoclave.cifrar_autoclave("Hola", "sol"), "Zdvh")
        texto = "  Hola Ñandú, áéíóú Ü 😀 K!  " * 20
        for clave in ["a", "Ñ", "sol", "CLAVEMASLARGA"]:
            for modulo, cifrar, descifrar in [
                (beaufort, beaufort.cifrar_beaufort, beaufort.descifrar_beaufort),
                (autoclave, autoclave.cifrar_autoclave, autoclave.descifrar_autoclave),
            ]:
                self.assertEqual(descifrar(cifrar(texto, clave), clave), texto)
                self.assertEqual(cifrar("", clave), "")
                for invalida in ["", "a b", "á", "123", "K"]:
                    with self.assertRaises(ValueError):
                        cifrar(texto, invalida)

    def test_bifid_vector_publicado(self):
        # American Cryptogram Association, Bifid.pdf: tabla completa por filas.
        clave = "EXTRAKLMPOHWZQDGVUSIFCBYN"
        esperado = "MWEINGIMGEOYYRLVEYWY"
        self.assertEqual(bifid.cifrar_bifid("Odd periods are popular", clave, 7), esperado)
        self.assertEqual(bifid.descifrar_bifid(esperado, clave, 7), "ODDPERIODSAREPOPULAR")
        self.assertEqual(bifid.cifrar_bifid("ABC", "a", 3), "AAH")

    def test_trifid_vector_publicado(self):
        # ACA Trifid.pdf usa # como símbolo 27; aquí ocupa esa casilla la Ñ.
        clave = "EXTRAODINYBCFGHJKLMPQSUVWZÑ"
        texto = "trifids are fractionated ciphers"
        esperado = "EYMXVUCRYY" + "YYEAYVYOVV" + "XITDPATHE"
        self.assertEqual(trifid.cifrar_trifid(texto, clave, 10), esperado)
        self.assertEqual(trifid.descifrar_trifid(esperado, clave, 10), texto.replace(" ", "").upper())
        self.assertEqual(trifid.cifrar_trifid("ABC", "a", 3), "AAF")

    def test_fraccionamiento_bloques_incompletos(self):
        generador = random.Random(31)
        for longitud in range(30):
            texto = "".join(generador.choice(ALFABETO_LATINO + "  ") for posicion in range(longitud))
            for periodo in [1, 2, 3, 5, 11, 100]:
                cifrado = bifid.cifrar_bifid(texto, "clave", periodo)
                self.assertEqual(bifid.descifrar_bifid(cifrado, "clave", periodo), normalizar_texto(texto, ALFABETO_POLIBIO, True))
                texto_espanol = texto + "ñ"
                cifrado = trifid.cifrar_trifid(texto_espanol, "niño", periodo)
                self.assertEqual(trifid.descifrar_trifid(cifrado, "niño", periodo), normalizar_texto(texto_espanol, ALFABETO_ESPANOL))
        for funcion in [bifid.cifrar_bifid, trifid.cifrar_trifid]:
            for periodo in [0, -1, 1.5, True]:
                with self.assertRaises(ValueError):
                    funcion("ABC", "clave", periodo)

    def test_adfgvx_vector_publicado_y_columnas_repetidas(self):
        # Vector del portal CrypTool: tabla completa y clave de columnas MYKEY.
        clave_tabla = "JE5CL1D347A2XNS0UPMFKZ89I6QVWBTGYORH"
        esperado = "DV DX AX AD FG VX XX GV XG DA AA VX XA DX AA".replace(" ", "")
        self.assertEqual(adfgvx.cifrar_adfgvx("GEHEIMNACHRICHT", clave_tabla, "MYKEY"), esperado)
        self.assertEqual(adfgvx.cifrar_adfgvx("ABC", adfgvx.ALFABETO, "ba"), "ADFAAA")
        for texto in ["", "a", "Hola 123", adfgvx.ALFABETO]:
            for clave_columnas in ["a", "casa", "ñon", "palabralarga"]:
                cifrado = adfgvx.cifrar_adfgvx(texto, "clave123", clave_columnas)
                self.assertEqual(adfgvx.descifrar_adfgvx(cifrado, "clave123", clave_columnas), normalizar_texto(texto, adfgvx.ALFABETO))
        for texto in ["A", "AB", "123"]:
            with self.assertRaises(ValueError):
                adfgvx.descifrar_adfgvx(texto, "clave", "sol")

    def test_caracteres_no_permitidos(self):
        funciones = [lambda texto: polibio.cifrar_polibio(texto, "clave"), bacon.cifrar_bacon,
                     lambda texto: bifid.cifrar_bifid(texto, "clave", 5),
                     lambda texto: adfgvx.cifrar_adfgvx(texto, "clave", "sol")]
        for funcion in funciones:
            for texto in ["ñ", "á", "!", "K", "ß"]:
                with self.assertRaises(ValueError):
                    funcion(texto)
        for texto in ["á", "!", "1", "K"]:
            with self.assertRaises(ValueError):
                trifid.cifrar_trifid(texto, "clave", 5)

    def test_menus_clasicos(self):
        casos = [
            (escitala, ["9", "1", "Hola", "0", "1", "HOLAAMIGO", "3", "2", "HAIOAGLMO", "3", "3"], "HOLAAMIGO"),
            (polibio, ["9", "1", "ñ", "clave", "1", "Hola", "clave", "2", "25 35 12 13", "clave", "3"], "HOLA"),
            (bacon, ["9", "1", "ñ", "1", "ABCZ", "2", "AAAAA AAAAB AAABA BBAAB", "3"], "ABCZ"),
            (beaufort, ["9", "1", "Hola", "123", "1", "Hola", "sol", "2", "Maas", "sol", "3"], "Hola"),
            (autoclave, ["9", "1", "Hola", "123", "1", "Hola", "sol", "2", "Zdvh", "sol", "3"], "Hola"),
            (bifid, ["9", "1", "ABC", "a", "0", "1", "ABC", "a", "3", "2", "AAH", "a", "3", "3"], "ABC"),
            (trifid, ["9", "1", "ABC", "a", "0", "1", "ABC", "a", "3", "2", "AAF", "a", "3", "3"], "ABC"),
            (adfgvx, ["9", "1", "ñ", "clave", "sol", "1", "ABC", adfgvx.ALFABETO, "ba", "2", "ADFAAA", adfgvx.ALFABETO, "ba", "3"], "ABC"),
        ]
        for modulo, entradas, original in casos:
            with self.subTest(modulo=modulo.__name__):
                salida = ejecutar_menu(modulo, entradas)
                self.assertIn("Opción no válida", salida)
                self.assertIn("Entrada inválida", salida)
                self.assertIn(f"Texto descifrado: {original}", salida)


class PruebasAsimetricosMatematicos(unittest.TestCase):
    def test_elgamal_vector_y_recuperacion(self):
        self.assertEqual(elgamal.cifrar_elgamal(10, (23, 5, 8), 3), (10, 14))
        self.assertEqual(elgamal.descifrar_elgamal((10, 14), (23, 6)), 10)
        for primo, generador in [(23, 5), (467, 2)]:
            privada, publica = elgamal.generar_claves(primo, generador)
            for mensaje in [1, 7, primo - 1]:
                self.assertEqual(elgamal.descifrar_elgamal(elgamal.cifrar_elgamal(mensaje, publica), privada), mensaje)
        salida = ejecutar_menu(elgamal, ["9", "1", "", "", "2", "23 5 8", "0", "2", "23 5 8", "10", "3", "23 6", "10 14", "4"])
        self.assertIn("Entero descifrado: 10", salida)
        self.assertIn("Entrada inválida", salida)

    def test_elgamal_parametros_invalidos(self):
        for primo, generador in [(4, 2), (23, 1), (23, 4), (1000001, 2), (True, 2)]:
            with self.assertRaises(ValueError):
                elgamal.generar_claves(primo, generador)
        for mensaje in [0, -1, 23, "10"]:
            with self.assertRaises(ValueError):
                elgamal.cifrar_elgamal(mensaje, (23, 5, 8))
        for cifrado in [(0, 10), (10,), (10, 23)]:
            with self.assertRaises(ValueError):
                elgamal.descifrar_elgamal(cifrado, (23, 6))

    def test_paillier_vector_sumas_y_modulo(self):
        privada, publica = paillier.generar_claves()
        self.assertEqual(privada, (323, 144, 83))
        self.assertEqual(paillier.cifrar_paillier(7, publica, 2), 93338)
        self.assertEqual(paillier.descifrar_paillier(93338, privada), 7)
        for mensaje in [0, 1, 7, 322]:
            self.assertEqual(paillier.descifrar_paillier(paillier.cifrar_paillier(mensaje, publica), privada), mensaje)
        for primero, segundo in [(7, 9), (320, 10), (0, 0)]:
            cifrado_primero = paillier.cifrar_paillier(primero, publica)
            cifrado_segundo = paillier.cifrar_paillier(segundo, publica)
            suma = paillier.sumar_cifrados(cifrado_primero, cifrado_segundo, publica)
            self.assertEqual(paillier.descifrar_paillier(suma, privada), (primero + segundo) % publica)
            self.assertEqual(gcd(suma, publica), 1)
        salida = ejecutar_menu(paillier, ["9", "1", "", "", "2", "323", "-1", "2", "323", "7", "3", "323 144 83", "93338", "4", "323", "93338", "93338", "5"])
        self.assertIn("Entero descifrado: 7", salida)
        self.assertIn("Suma cifrada", salida)

    def test_paillier_claves_y_entradas_invalidas(self):
        for primero, segundo in [(17, 17), (15, 19), (3, 7), (1000001, 19)]:
            with self.assertRaises(ValueError):
                paillier.generar_claves(primero, segundo)
        for mensaje in [-1, 323, 1.5, True]:
            with self.assertRaises(ValueError):
                paillier.cifrar_paillier(mensaje, 323)
        for aleatorio in [0, 17, 19, 323]:
            with self.assertRaises(ValueError):
                paillier.cifrar_paillier(7, 323, aleatorio)
        for cifrado in [0, 17, 323 ** 2]:
            with self.assertRaises(ValueError):
                paillier.descifrar_paillier(cifrado, (323, 144, 83))
        with self.assertRaises(ValueError):
            paillier.descifrar_paillier(93338, (323, 144, 84))


class PruebasHibrido(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.privada, cls.publica = hibrido.generar_claves()

    def test_texto_extenso_unicode_y_aleatoriedad(self):
        for texto in ["", "Hola ñá 😀", "  Hola ñá 😀 中文  " * 3000]:
            paquete = hibrido.cifrar_hibrido(texto, self.publica)
            self.assertEqual(hibrido.descifrar_hibrido(paquete, self.privada), texto)
            campos = json.loads(paquete)
            self.assertEqual(set(campos), {"version", "algoritmo", "clave_cifrada", "nonce", "datos"})
            reordenado = json.dumps(dict(reversed(list(campos.items()))), indent=2)
            self.assertEqual(hibrido.descifrar_hibrido(reordenado, self.privada), texto)
        primero = json.loads(hibrido.cifrar_hibrido("Hola", self.publica))
        segundo = json.loads(hibrido.cifrar_hibrido("Hola", self.publica))
        self.assertNotEqual(primero["clave_cifrada"], segundo["clave_cifrada"])
        self.assertNotEqual(primero["nonce"], segundo["nonce"])

    def test_modificaciones_clave_y_formato(self):
        original = json.loads(hibrido.cifrar_hibrido("Hola", self.publica))
        for campo in ["clave_cifrada", "nonce", "datos"]:
            paquete = dict(original)
            modificado = bytearray(decodificar_base64(paquete[campo]))
            modificado[0] ^= 1
            paquete[campo] = codificar_base64(bytes(modificado))
            with self.assertRaises(ValueError):
                hibrido.descifrar_hibrido(json.dumps(paquete), self.privada)
        otra_privada, otra_publica = hibrido.generar_claves()
        with self.assertRaises(ValueError):
            hibrido.descifrar_hibrido(json.dumps(original), otra_privada)
        invalidos = ["no es JSON", "[]", "{}", json.dumps({**original, "version": True}),
                     json.dumps({**original, "version": 2}), json.dumps({**original, "algoritmo": "otro"}),
                     json.dumps({**original, "extra": "dato"}), json.dumps({**original, "nonce": "%%%"}),
                     json.dumps({**original, "datos": ""}), json.dumps({**original, "clave_cifrada": 123})]
        for invalido in invalidos:
            with self.assertRaises(ValueError):
                hibrido.descifrar_hibrido(invalido, self.privada)

    def test_menu_y_reutilizacion_de_claves_pem(self):
        with tempfile.TemporaryDirectory() as temporal:
            carpeta = Path(temporal) / "claves"
            ruta_privada, ruta_publica = hibrido.guardar_claves(carpeta, b"contrasena")
            publica = hibrido.cargar_clave_publica(ruta_publica)
            paquete = hibrido.cifrar_hibrido("Hola ñá 😀", publica)
            with patch("getpass.getpass", return_value="contrasena"):
                salida = ejecutar_menu(hibrido, ["9", "3", str(ruta_privada), "{}",
                                               "2", str(ruta_publica), "Hola", "3", str(ruta_privada), paquete, "4"])
                nueva_carpeta = Path(temporal) / "nuevas"
                ejecutar_menu(hibrido, ["1", str(nueva_carpeta), "4"])
            self.assertIn("Texto descifrado: Hola ñá 😀", salida)
            self.assertIn("No se pudo completar", salida)
            self.assertTrue((nueva_carpeta / "clave_privada.pem").exists())


if __name__ == "__main__":
    unittest.main()
