# Cifrado César

[Volver al índice](../../README.md) · [Ver el código](../../1.cesar.py)

## Teoría

El cifrado César reemplaza cada letra por otra situada un número fijo de
posiciones más adelante en el alfabeto. Ese número es el **desplazamiento** y
actúa como clave. Al llegar al final del alfabeto, se vuelve al principio.

Esta implementación utiliza las 27 letras del alfabeto español:

```text
abcdefghijklmnñopqrstuvwxyz
```

Las posiciones comienzan en cero: a ocupa la posición 0, n la 13, ñ la 14 y z la
26. Si `posicion_original` es la posición de una letra, se calcula:

```text
posición cifrada = (posición original + desplazamiento) % 27
posición descifrada = (posición cifrada - desplazamiento) % 27
```

El operador `%` obtiene el resto de la división. Permite volver al inicio del
alfabeto y también manejar desplazamientos negativos. Por ejemplo, con un
desplazamiento de 1, z pasa a a porque `(26 + 1) % 27` es 0.

Con desplazamiento 3:

| Letra original | Posición original | Posición cifrada | Letra cifrada |
| --- | --- | --- | --- |
| H | 7 | 10 | K |
| o | 15 | 18 | r |
| l | 11 | 14 | ñ |
| a | 0 | 3 | d |

Por eso `Hola` se convierte en `Krñd`. La ñ hace que algunos resultados difieran
respecto de un César que use únicamente las 26 letras de a a z.

## Explicación del código

### Variables principales

| Variable | Qué representa |
| --- | --- |
| `ALFABETO` | Letras disponibles en el orden que se usa para desplazar. |
| `texto` | Mensaje que se va a transformar. |
| `desplazamiento` | Número entero de posiciones que se avanza. |
| `caracter` | Carácter que se está procesando. |
| `letra_minuscula` | Versión en minúscula para buscar en el alfabeto. |
| `posicion_original` | Índice de la letra antes del desplazamiento. |
| `posicion_cifrada` | Índice calculado después del desplazamiento. |
| `letra_cifrada` | Letra obtenida en esa nueva posición. |
| `caracteres_cifrados` | Lista que acumula los caracteres del resultado. |

### Funciones y recorrido

`cifrar_cesar(texto, desplazamiento)` recorre el texto carácter por carácter:

1. Convierte el carácter a minúscula para buscarlo en `ALFABETO`.
2. Si pertenece al alfabeto, obtiene su posición con `.index()`.
3. Calcula la nueva posición:

   ```python
   posicion_cifrada = (posicion_original + desplazamiento) % len(ALFABETO)
   ```

4. Busca la letra de reemplazo y la convierte a mayúscula si el original lo era.
5. Si el carácter está fuera del alfabeto, lo conserva sin cambios.
6. Une la lista con `"".join(caracteres_cifrados)` y devuelve el resultado.

`descifrar_cesar(texto_cifrado, desplazamiento)` reutiliza el cifrado con el
desplazamiento negativo. De este modo, retrocede las mismas posiciones.

`mostrar_posibles_descifrados(texto_cifrado)` prueba los desplazamientos de 0 a
26 y muestra los 27 candidatos. No determina automáticamente cuál es el mensaje
correcto: quien usa el programa debe identificarlo.

`main()` controla el menú. Convierte el desplazamiento mediante `int()` y
captura `ValueError` cuando la entrada no es un entero. El bloque
`if __name__ == "__main__":` abre el menú únicamente al ejecutar el archivo.

## Cómo utilizarlo

Desde la raíz del repositorio:

```bash
python3 1.cesar.py
```

- Opción 1: escribe `Hola` y el desplazamiento `3`; obtendrás `Krñd`.
- Opción 2: escribe `Krñd` y el mismo desplazamiento `3`; recuperarás `Hola`.
- Opción 3: termina el programa.
- Opción 4: muestra todos los posibles descifrados de un mensaje.

Los desplazamientos pueden ser negativos o mayores que 27. Los valores 3 y 30
producen el mismo resultado porque `30 % 27` es 3.

## Caracteres y límites

Conserva las mayúsculas y las minúsculas. Cifra la ñ, pero deja las vocales con
tilde, la ü, los espacios, los números y los signos sin cambios.

Solo hay 27 desplazamientos distintos, por lo que probarlos todos resulta
sencillo. Este cifrado sirve para aprender, no para proteger datos confidenciales.
