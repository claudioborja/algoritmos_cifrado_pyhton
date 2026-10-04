# Algoritmos de cifrado en Python

Cuatro programas de consola para aprender cómo funcionan los cifrados clásicos.
Las funciones, variables y mensajes están en español.

Estos algoritmos son educativos y no deben usarse para proteger contraseñas ni
información confidencial.

## Índice de algoritmos

Cada guía explica la teoría, las variables, las funciones y el uso del programa.

| Algoritmo | Guía individual | Código |
| --- | --- | --- |
| César | [Teoría y explicación](docs/cesar/README.md) | [1.cesar.py](1.cesar.py) |
| Sustitución simple | [Teoría y explicación](docs/sustitucion_simple/README.md) | [2. sustitucion_simple.py](2.%20sustitucion_simple.py) |
| Atbash | [Teoría y explicación](docs/atbash/README.md) | [3.atbash.py](3.atbash.py) |
| ROT13 | [Teoría y explicación](docs/rot13/README.md) | [4. ROT13.py](4.%20ROT13.py) |

## Requisitos y ejecución

Necesitas Python 3. No se requieren paquetes externos.

Ejecuta el programa que quieras usar desde esta carpeta:

```bash
python3 1.cesar.py
python3 "2. sustitucion_simple.py"
python3 3.atbash.py
python3 "4. ROT13.py"
```

Cada programa muestra un menú para cifrar, descifrar o salir. También puedes
importar sus funciones sin que se abra el menú.

## Algoritmos

- **César:** desplaza las 27 letras del alfabeto español, incluida la ñ.
  Acepta desplazamientos enteros positivos, negativos o mayores que 27.
  Para descifrar, utiliza el mismo desplazamiento; si lo desconoces, la opción 4
  muestra todos los posibles resultados. Por ejemplo, `Hola` con desplazamiento
  3 se convierte en `Krñd`.
- **Sustitución simple:** reemplaza cada letra por otra según una clave.
  La clave debe contener las 27 letras del alfabeto español exactamente una vez,
  en el orden de reemplazo de `abcdefghijklmnñopqrstuvwxyz`.
  Una clave de ejemplo es `qwertyuiopasdfghjklñzxcvbnm`:
  la a se reemplaza por q, la b por w y la c por e.
  Para descifrar debes usar la misma clave. No es un desplazamiento César.
- **Atbash:** invierte las 27 letras del alfabeto español; a pasa a z y b pasa
  a y. Aplicar la función dos veces recupera el mensaje original.
- **ROT13:** desplaza 13 posiciones las 26 letras de a a z.
  Mantiene la ñ sin cambios para respetar el ROT13 estándar.
  Aplicarlo dos veces recupera el mensaje original.

Todos conservan mayúsculas y minúsculas. Las vocales con tilde, la ü, los
espacios, los números, los signos y las letras fuera del alfabeto definido
se mantienen sin cambios para evitar perder información.

Las entradas de desplazamiento o clave inválidas muestran un mensaje y permiten
volver a intentarlo desde el menú.
