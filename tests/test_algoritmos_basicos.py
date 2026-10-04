"""Pruebas de los ejemplos, recuperación del mensaje y validación de entradas."""

import contextlib
import importlib.util
import io
from pathlib import Path
import random
import subprocess
import sys
import unittest

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


vigenere = cargar_modulo("5.vigenere.py")
columnas = cargar_modulo("6.transposicion_columnas.py")
rieles = cargar_modulo("7.rail_fence.py")


class PruebasAlgoritmosBasicos(unittest.TestCase):
    def test_ejemplos_vigenere(self):
        self.assertEqual(vigenere.cifrar_vigenere("Hola", "sol"), "Zdvs")
        self.assertEqual(vigenere.descifrar_vigenere("Zdvs", "sol"), "Hola")
        self.assertEqual(vigenere.cifrar_vigenere("Ho la", "sol"), "Zd vs")
        self.assertEqual(vigenere.cifrar_vigenere("nÑzZ áü!", "b"), "ñOaA áü!")

    def test_ejemplos_columnas(self):
        self.assertEqual(columnas.cifrar_columnas("HOLAAMIGO", "sol"), "LMOOAGHAI")
        self.assertEqual(columnas.descifrar_columnas("LMOOAGHAI", "sol"), "HOLAAMIGO")
        self.assertEqual(columnas.cifrar_columnas("HOLA", "sol"), "LOHA")
        self.assertEqual(columnas.descifrar_columnas("LOHA", "sol"), "HOLA")
        self.assertEqual(columnas.cifrar_columnas("ABCDEFGH", "casa"), "BFDHAECG")
        self.assertEqual(columnas.obtener_orden_columnas("oñn"), [2, 1, 0])

    def test_ejemplos_rieles(self):
        self.assertEqual(rieles.cifrar_rail_fence("HOLAAMIGO", 3), "HAOOAMGLI")
        self.assertEqual(rieles.descifrar_rail_fence("HAOOAMGLI", 3), "HOLAAMIGO")
        # Vector conocido, independiente del ejemplo de la guía.
        self.assertEqual(
            rieles.cifrar_rail_fence("WEAREDISCOVEREDFLEEATONCE", 3),
            "WECRLTEERDSOEEFEAOCAIVDEN",
        )

    def test_recuperar_mensajes(self):
        generador = random.Random(42)
        textos = ["", "a", "  ¡Hola, Ñandú! áéíóú Ü 123 中文 😀  "]
        for longitud in range(50):
            textos.append("".join(generador.choice("abcñXYZ áü!?012😀") for posicion in range(longitud)))
        for texto in textos:
            for clave in ["a", "sol", "casa", "ÑANDU", "abcdefghijklmnñopqrstuvwxyz"]:
                with self.subTest(texto=texto, clave=clave):
                    cifrado = vigenere.cifrar_vigenere(texto, clave)
                    self.assertEqual(vigenere.descifrar_vigenere(cifrado, clave), texto)
                    cifrado = columnas.cifrar_columnas(texto, clave)
                    self.assertEqual(columnas.descifrar_columnas(cifrado, clave), texto)
                    self.assertEqual(sorted(cifrado), sorted(texto))
            for cantidad_rieles in [1, 2, 3, 4, 10, 1000000]:
                with self.subTest(texto=texto, cantidad_rieles=cantidad_rieles):
                    cifrado = rieles.cifrar_rail_fence(texto, cantidad_rieles)
                    self.assertEqual(rieles.descifrar_rail_fence(cifrado, cantidad_rieles), texto)
                    self.assertEqual(sorted(cifrado), sorted(texto))

    def test_claves_invalidas(self):
        for clave in ["", "a b", "á", "123", "sol!", "😀"]:
            for funcion in [vigenere.cifrar_vigenere, vigenere.descifrar_vigenere,
                            columnas.cifrar_columnas, columnas.descifrar_columnas]:
                with self.subTest(clave=clave, funcion=funcion.__name__):
                    with self.assertRaises(ValueError):
                        funcion("Hola", clave)

    def test_rieles_invalidos(self):
        for cantidad in [0, -1, 1.5, "3", True, None]:
            for funcion in [rieles.cifrar_rail_fence, rieles.descifrar_rail_fence]:
                with self.subTest(cantidad=cantidad, funcion=funcion.__name__):
                    with self.assertRaises(ValueError):
                        funcion("Hola", cantidad)

    def test_menus_y_errores(self):
        casos = [
            ("5.vigenere.py", "9\n1\nHola\n123\n1\nHola\nsol\n2\nZdvs\nsol\n3\n", "Zdvs", "Hola"),
            ("6.transposicion_columnas.py", "9\n1\nHOLA\n123\n1\nHOLA\nsol\n2\nLOHA\nsol\n3\n", "LOHA", "HOLA"),
            ("7.rail_fence.py", "9\n1\nHOLAAMIGO\nabc\n1\nHOLAAMIGO\n0\n1\nHOLAAMIGO\n3\n2\nHAOOAMGLI\n3\n3\n", "HAOOAMGLI", "HOLAAMIGO"),
        ]
        for archivo, entrada, cifrado, original in casos:
            with self.subTest(archivo=archivo):
                resultado = subprocess.run(
                    [sys.executable, "-B", str(RAIZ / archivo)],
                    input=entrada, text=True, capture_output=True, timeout=5,
                )
                self.assertEqual(resultado.returncode, 0, resultado.stderr)
                self.assertIn("Opción no válida", resultado.stdout)
                self.assertIn("debe", resultado.stdout)
                self.assertIn(f"Texto cifrado: {cifrado}", resultado.stdout)
                self.assertIn(f"Texto descifrado: {original}", resultado.stdout)


if __name__ == "__main__":
    unittest.main()
