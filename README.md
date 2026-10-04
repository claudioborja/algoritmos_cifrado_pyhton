# Algoritmos de cifrado en Python

Veintiséis programas de consola para aprender cifrados clásicos y utilizar algoritmos
modernos. Las funciones propias, variables, comentarios y mensajes están en español.

Los cifrados clásicos y las simulaciones son ejercicios educativos. Los ejemplos AES-GCM, ChaCha20-Poly1305, RSA-OAEP e híbrido
utilizan `cryptography`; sus menús muestran cómo trabajar con claves y mensajes,
pero no implementan un sistema completo de seguridad para una aplicación real.

## Índice de algoritmos

Cada guía explica la teoría, las variables, las funciones y el uso del programa.
La dificultad corresponde a los conceptos que se estudian en estos ejemplos.

| Algoritmo | Nivel | Guía individual | Código |
| --- | --- | --- | --- |
| César | Básico | [Teoría y explicación](docs/cesar/README.md) | [1.cesar.py](1.cesar.py) |
| Sustitución simple | Básico | [Teoría y explicación](docs/sustitucion_simple/README.md) | [2. sustitucion_simple.py](2.%20sustitucion_simple.py) |
| Atbash | Básico | [Teoría y explicación](docs/atbash/README.md) | [3.atbash.py](3.atbash.py) |
| ROT13 | Básico | [Teoría y explicación](docs/rot13/README.md) | [4. ROT13.py](4.%20ROT13.py) |
| Vigenère | Básico | [Teoría y explicación](docs/vigenere/README.md) | [5.vigenere.py](5.vigenere.py) |
| Transposición por columnas | Básico | [Teoría y explicación](docs/transposicion_columnas/README.md) | [6.transposicion_columnas.py](6.transposicion_columnas.py) |
| Rail Fence (zigzag) | Básico | [Teoría y explicación](docs/rail_fence/README.md) | [7.rail_fence.py](7.rail_fence.py) |
| Afín | Intermedio | [Teoría y explicación](docs/afin/README.md) | [8.afin.py](8.afin.py) |
| Playfair | Intermedio | [Teoría y explicación](docs/playfair/README.md) | [9.playfair.py](9.playfair.py) |
| Hill de 2 × 2 | Intermedio | [Teoría y explicación](docs/hill/README.md) | [10.hill.py](10.hill.py) |
| Vernam y libreta de un solo uso | Intermedio | [Teoría y explicación](docs/vernam/README.md) | [11.vernam.py](11.vernam.py) |
| Enigma simplificada | Avanzado | [Teoría y explicación](docs/enigma_simplificada/README.md) | [12.enigma_simplificada.py](12.enigma_simplificada.py) |
| AES-GCM | Avanzado | [Teoría y explicación](docs/aes_gcm/README.md) | [13.aes_gcm.py](13.aes_gcm.py) |
| ChaCha20-Poly1305 | Avanzado | [Teoría y explicación](docs/chacha20_poly1305/README.md) | [14.chacha20_poly1305.py](14.chacha20_poly1305.py) |
| RSA-OAEP | Avanzado | [Teoría y explicación](docs/rsa_oaep/README.md) | [15.rsa_oaep.py](15.rsa_oaep.py) |
| Escítala | Básico | [Teoría y explicación](docs/escitala/README.md) | [16.escitala.py](16.escitala.py) |
| Cuadrado de Polibio | Básico | [Teoría y explicación](docs/polibio/README.md) | [17.polibio.py](17.polibio.py) |
| Bacon (26 letras) | Básico | [Teoría y explicación](docs/bacon/README.md) | [18.bacon.py](18.bacon.py) |
| Beaufort | Intermedio | [Teoría y explicación](docs/beaufort/README.md) | [19.beaufort.py](19.beaufort.py) |
| Autoclave — Autokey | Intermedio | [Teoría y explicación](docs/autoclave/README.md) | [20.autoclave.py](20.autoclave.py) |
| Bifid | Intermedio | [Teoría y explicación](docs/bifid/README.md) | [21.bifid.py](21.bifid.py) |
| Trifid español | Intermedio | [Teoría y explicación](docs/trifid/README.md) | [22.trifid.py](22.trifid.py) |
| ADFGVX | Intermedio | [Teoría y explicación](docs/adfgvx/README.md) | [23.adfgvx.py](23.adfgvx.py) |
| ElGamal para enteros | Avanzado | [Teoría y explicación](docs/elgamal/README.md) | [24.elgamal.py](24.elgamal.py) |
| Paillier para enteros | Avanzado | [Teoría y explicación](docs/paillier/README.md) | [25.paillier.py](25.paillier.py) |
| Híbrido RSA-OAEP + AES-GCM | Avanzado | [Teoría y explicación](docs/hibrido_rsa_aes/README.md) | [26.hibrido_rsa_aes.py](26.hibrido_rsa_aes.py) |

## Requisitos e instalación

Utiliza Python 3.10 o posterior. Los programas 1 a 12 y 16 a 25 solo necesitan
la biblioteca estándar. AES-GCM, ChaCha20-Poly1305, RSA-OAEP y el híbrido RSA + AES
requieren `cryptography`.

ElGamal y Paillier son demostraciones matemáticas para enteros con primos pequeños;
no utilizan parámetros de producción ni cifran texto. Sus guías explican el alcance.

Para instalar la dependencia en un entorno virtual desde esta carpeta:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

En Windows, activa el entorno con `.venv\Scripts\activate` en lugar de `source`.
Si tu instalación de Python no incluye `pip` o `venv`, instala esos componentes
para tu sistema antes de seguir estos pasos.

## Ejecución

Ejecuta el programa que quieras usar desde esta carpeta:

```bash
python3 1.cesar.py
python3 "2. sustitucion_simple.py"
python3 3.atbash.py
python3 "4. ROT13.py"
python3 5.vigenere.py
python3 6.transposicion_columnas.py
python3 7.rail_fence.py
python3 8.afin.py
python3 9.playfair.py
python3 10.hill.py
python3 11.vernam.py
python3 12.enigma_simplificada.py
python3 13.aes_gcm.py
python3 14.chacha20_poly1305.py
python3 15.rsa_oaep.py
python3 16.escitala.py
python3 17.polibio.py
python3 18.bacon.py
python3 19.beaufort.py
python3 20.autoclave.py
python3 21.bifid.py
python3 22.trifid.py
python3 23.adfgvx.py
python3 24.elgamal.py
python3 25.paillier.py
python3 26.hibrido_rsa_aes.py
```

Cada programa muestra un menú. También puedes importar sus funciones sin abrirlo.
Las entradas de clave, desplazamiento, matriz o cantidad de rieles inválidas
muestran un mensaje y permiten volver a intentarlo.

## Qué hace cada algoritmo

- **César:** desplaza las 27 letras españolas. Permite descifrar con la clave o
  probar todos los desplazamientos. `Hola`, desplazamiento 3 → `Krñd`.
- **Sustitución simple:** reemplaza letras según una clave con las 27 letras
  exactamente una vez. `Abc`, clave `qwertyuiopasdfghjklñzxcvbnm` → `Qwe`.
- **Atbash:** invierte el alfabeto español. `Abc` → `Zyx`.
- **ROT13:** desplaza 13 posiciones las 26 letras de a a z y conserva la ñ.
  `Hola` → `Ubyn`.
- **Vigenère:** repite una palabra clave para variar los desplazamientos.
  `Hola`, clave `sol` → `Zdvs`.
- **Transposición por columnas:** reordena el mensaje según una palabra clave,
  sin relleno. `HOLAAMIGO`, clave `sol` → `LMOOAGHAI`.
- **Rail Fence:** distribuye el mensaje en zigzag y lee sus rieles.
  `HOLAAMIGO`, 3 rieles → `HAOOAMGLI`.
- **Afín:** multiplica y desplaza posiciones módulo 27. El multiplicador debe
  ser coprimo con 27. `Hola`, claves 5 y 8 → `Pcji`.
- **Playfair:** cifra parejas con una tabla de 5 × 5. Une I/J y añade relleno.
  `Hola`, clave `clave` → `OTAV`; al descifrar devuelve `HOLA`.
- **Hill:** multiplica parejas por una matriz invertible módulo 27.
  `Hola`, matriz `[1, 2; 3, 5]` → `Kolg`.
- **Vernam:** aplica XOR con una clave aleatoria de tantos bytes como el mensaje.
  El menú genera una clave de un solo uso y devuelve Base64.
- **Enigma simplificada:** aplica tres rotores, un reflector y avance de contador.
  `Hola`, posiciones `aaa` → `Iibg`. No simula todos los mecanismos históricos.
- **AES-GCM:** cifra y autentica texto UTF-8 con una clave de 256 bits y un nonce
  generado en cada operación. Devuelve un paquete Base64.
- **ChaCha20-Poly1305:** ofrece cifrado de flujo y autenticación con una clave
  de 256 bits y un nonce nuevo por operación. Devuelve un paquete Base64.
- **RSA-OAEP:** cifra con una clave pública y descifra con la privada. Genera
  claves de 2048 bits y protege el archivo privado con contraseña. Con SHA-256
  admite mensajes de hasta 190 bytes UTF-8 para ese tamaño de clave.

- **Escítala:** transpone por columnas en su orden original con una clave
  numérica. `HOLAAMIGO`, 3 columnas → `HAIOAGLMO`.
- **Polibio:** representa letras con coordenadas de una tabla de 5 × 5.
  `Hola`, clave `clave` → `25 35 12 13`.
- **Bacon:** representa las 26 letras con grupos de cinco símbolos A/B.
  `ABCZ` → `AAAAA AAAAB AAABA BBAAB`.
- **Beaufort:** resta posiciones del mensaje a una clave repetida módulo 27.
  `Hola`, clave `sol` → `Maas`.
- **Autoclave:** extiende la clave inicial con letras del propio mensaje original.
  `Hola`, clave `sol` → `Zdvh`.
- **Bifid:** mezcla filas y columnas de Polibio por bloques de un período dado.
  `ABC`, clave `a`, período 3 → `AAH`.
- **Trifid:** mezcla coordenadas de un cubo de 3 × 3 × 3. Utiliza las 27 letras
  españolas. `ABC`, clave `a`, período 3 → `AAF`.
- **ADFGVX:** combina una tabla de letras y números con transposición. Requiere
  una clave de tabla y otra de columnas.
- **ElGamal:** demuestra cifrado de enteros mediante exponentes, un primo y un
  generador. Utiliza primos pequeños para seguir las operaciones.
- **Paillier:** demuestra cifrado de enteros y sumas sobre cifrados. La suma
  recuperada se calcula módulo la clave pública.
- **Híbrido RSA + AES:** genera una clave AES-GCM por mensaje y la protege con
  RSA-OAEP. Devuelve un paquete JSON y permite textos mayores que el límite del
  ejemplo RSA directo.

## Tratamiento de caracteres

| Programas | Tratamiento |
| --- | --- |
| César, sustitución, Atbash, Vigenère, afín, Beaufort y Autoclave | Cifran la ñ; conservan mayúsculas y dejan tildes, ü, espacios y signos en su lugar. |
| ROT13 y Enigma simplificada | Transforman a-z y A-Z; los demás caracteres quedan en su lugar. |
| Transposición por columnas, Rail Fence y Escítala | Reordenan todos los caracteres y recuperan exactamente el texto. Conserva los espacios al copiar el cifrado. |
| Hill | Conserva el formato; requiere una cantidad par de letras del alfabeto español y no añade relleno. |
| Playfair | Solo admite a-z y espacios; elimina espacios, devuelve mayúsculas, une I/J y conserva el relleno al descifrar. No admite ñ ni tildes. |
| Vernam, AES-GCM, ChaCha20-Poly1305, RSA-OAEP e híbrido RSA + AES | Trabajan con bytes UTF-8 y recuperan tildes, ñ, espacios y emoji. RSA tiene un límite de longitud. |
| Polibio y Bifid | Admiten letras latinas; eliminan espacios, devuelven mayúsculas y unen I/J. |
| Bacon | Variante de 26 letras latinas, sin unir I/J ni U/V; elimina espacios y devuelve mayúsculas. |
| Trifid | Variante con las 27 letras españolas; elimina espacios y devuelve mayúsculas. |
| ADFGVX | Admite A-Z y 0-9; elimina espacios y devuelve mayúsculas. |
| ElGamal y Paillier | Operan sobre enteros en un rango definido por la clave pública, sin formato de texto. |

## Claves y formatos modernos

Vernam muestra su clave en Base64 y exige la misma longitud en bytes que el
mensaje. No debe reutilizarse. No proporciona autenticación.

AES-GCM y ChaCha20-Poly1305 muestran una clave Base64 de 32 bytes por separado del
paquete. El paquete incluye nonce, contenido cifrado y etiqueta de autenticación.
El descifrado rechaza una clave incorrecta o un paquete modificado. Base64 solo
representa bytes como texto.

RSA guarda claves PEM en una carpeta nueva. La privada está cifrada con una
contraseña y no debe compartirse. Los archivos PEM están excluidos de Git mediante
[.gitignore](.gitignore). El cifrado RSA no es una firma digital.

El híbrido utiliza los mismos archivos PEM de RSA, pero produce JSON con la
clave AES cifrada, el nonce, el contenido autenticado y la versión del formato.

ElGamal muestra dos componentes enteros por mensaje. Paillier muestra un entero
por cifrado y permite sumar dos cifrados de la misma clave. Ninguno de estos dos
modelos matemáticos ofrece autenticación.

Las guías modernas enlazan la documentación oficial de
[cryptography](https://cryptography.io/en/latest/hazmat/primitives/aead/) y las
especificaciones correspondientes.

## Pruebas

Con la dependencia instalada, ejecuta:

```bash
python3 -B -m unittest discover -s tests -v
```

Las 40 pruebas verifican ejemplos y vectores publicados, recuperación de mensajes,
reglas de normalización, claves y matrices inválidas, menús, detección de
modificaciones en los cifrados modernos, sumas de Paillier y almacenamiento
protegido de claves RSA. Las claves de prueba se generan en memoria o en carpetas
temporales, sin guardar claves privadas en el repositorio.
