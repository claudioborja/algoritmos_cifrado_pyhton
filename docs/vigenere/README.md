# Cifrado Vigenère

[Volver al índice](../../README.md) · [Ver el código](../../5.vigenere.py)

## Teoría

Vigenère utiliza una palabra clave para cambiar el desplazamiento de cada letra.
La clave se repite hasta cubrir todas las letras que se van a cifrar. Una a en la
clave desplaza 0 posiciones, una b desplaza 1, y así sucesivamente.

Esta implementación usa las 27 letras del alfabeto español:

```text
abcdefghijklmnñopqrstuvwxyz
```

Las posiciones empiezan en cero. La ñ ocupa la posición 14 y la z la 26.
La fórmula para cada letra es:

```text
posición cifrada = (posición original + posición de la letra clave) % 27
posición descifrada = (posición cifrada - posición de la letra clave) % 27
```

El operador `%` calcula el resto y permite volver al inicio del alfabeto.
Con el texto `Hola` y la clave `sol` se utiliza `sols`:

| Letra original | Posición | Letra clave | Desplazamiento | Letra cifrada |
| --- | --- | --- | --- | --- |
| H | 7 | s | 19 | Z |
| o | 15 | o | 15 | d |
| l | 11 | l | 11 | v |
| a | 0 | s | 19 | s |

El resultado es `Zdvs`. Al descifrar se restan los mismos desplazamientos.
Una letra repetida en el mensaje puede tener reemplazos diferentes dependiendo
de la letra de la clave que le corresponda.

## Explicación del código

### Variables principales

| Variable | Qué representa |
| --- | --- |
| `ALFABETO` | Las 27 letras con las que se calcula el desplazamiento. |
| `clave` | Palabra que determina los desplazamientos. |
| `posicion_clave` | Cantidad de letras transformadas hasta el momento. |
| `letra_clave` | Letra de la clave usada para el carácter actual. |
| `desplazamiento` | Posición de la letra clave, con signo negativo al descifrar. |
| `posicion_original` | Posición de la letra del mensaje. |
| `posicion_resultado` | Posición después de aplicar el desplazamiento. |
| `caracteres_transformados` | Lista que acumula el resultado. |

### Funciones

`validar_clave(clave)` convierte la clave a minúsculas. Rechaza claves vacías,
espacios, números, tildes y cualquier carácter fuera del alfabeto. Se permite
repetir letras y utilizar la ñ.

`transformar_vigenere(texto, clave, descifrar=False)` recorre el mensaje:

1. Comprueba si el carácter pertenece al alfabeto.
2. Obtiene la letra de la clave mediante:

   ```python
   letra_clave = clave[posicion_clave % len(clave)]
   ```

   El resto permite reiniciar la clave al llegar a su final.
3. Busca el desplazamiento con `ALFABETO.index(letra_clave)`.
4. Si se está descifrando, cambia el desplazamiento a negativo.
5. Calcula la nueva posición, busca la letra y restaura la mayúscula original.
6. Incrementa `posicion_clave` solo si transformó una letra del alfabeto.
7. Conserva los demás caracteres y une la lista al final.

`cifrar_vigenere(texto, clave)` llama a la transformación normal.
`descifrar_vigenere(texto_cifrado, clave)` usa `descifrar=True` para restar.

`main()` controla el menú y captura `ValueError` si la clave es inválida.
El bloque `if __name__ == "__main__":` evita abrir el menú al importar el archivo.

## Cómo utilizarlo

Desde la raíz del repositorio:

```bash
python3 5.vigenere.py
```

- Opción 1: texto `Hola`, clave `sol`; resultado `Zdvs`.
- Opción 2: texto `Zdvs`, clave `sol`; resultado `Hola`.
- Opción 3: salir.

También `Ho la` se convierte en `Zd vs`: el espacio no consume una letra de la
clave. Debes usar la misma clave y la misma regla de avance al descifrar.

## Caracteres y límites

Conserva las mayúsculas. La ñ se cifra; las vocales con tilde, la ü, los espacios,
los números y los signos quedan en su posición y no avanzan la clave.

La repetición de la clave introduce patrones que pueden analizarse. Vigenère es
un ejercicio educativo y no debe proteger información confidencial.
