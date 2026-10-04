# Cifrado Atbash

[Volver al índice](../../README.md) · [Ver el código](../../3.atbash.py)

## Teoría

Atbash reemplaza cada letra por la que ocupa la posición opuesta en el alfabeto:
la primera por la última, la segunda por la penúltima, y así sucesivamente.
No solicita una clave, porque la relación queda definida por el alfabeto elegido.

Esta implementación invierte las 27 letras del alfabeto español:

```text
Original: abcdefghijklmnñopqrstuvwxyz
Invertido: zyxwvutsrqpoñnmlkjihgfedcba
```

Las posiciones comienzan en cero. Para un alfabeto de 27 letras:

```text
posición invertida = 26 - posición original
```

| Letra original | Posición original | Posición invertida | Resultado |
| --- | --- | --- | --- |
| a | 0 | 26 | z |
| b | 1 | 25 | y |
| n | 13 | 13 | n |
| ñ | 14 | 12 | m |
| z | 26 | 0 | a |

La n se conserva porque ocupa el centro de este alfabeto. La ñ se transforma en
m, y la m en ñ.

Para descifrar se aplica exactamente la misma operación. Invertir una posición
dos veces devuelve la inicial: `26 - (26 - posición)` es `posición`.
Por ejemplo, `Abc` pasa a `Zyx`, y `Zyx` vuelve a `Abc`.

## Explicación del código

### Variables principales

| Variable | Qué representa |
| --- | --- |
| `ALFABETO` | Las letras cuyo orden se va a invertir. |
| `texto` | Mensaje que se cifra o descifra. |
| `caracter` | Carácter que se está examinando. |
| `letra_minuscula` | Versión en minúscula para buscar en el alfabeto. |
| `posicion_original` | Posición de entrada de la letra. |
| `posicion_invertida` | Posición opuesta dentro del alfabeto. |
| `letra_cifrada` | Letra de reemplazo obtenida. |
| `caracteres_cifrados` | Lista que acumula el resultado. |

### Función principal

`cifrar_atbash(texto)` realiza los siguientes pasos:

1. Recorre el mensaje carácter por carácter.
2. Convierte el carácter a minúscula y comprueba si está en `ALFABETO`.
3. Si está, obtiene su posición y calcula la posición opuesta:

   ```python
   posicion_original = ALFABETO.index(letra_minuscula)
   posicion_invertida = len(ALFABETO) - 1 - posicion_original
   letra_cifrada = ALFABETO[posicion_invertida]
   ```

4. Si la letra original era mayúscula, convierte el reemplazo con `.upper()`.
5. Conserva los caracteres que estén fuera del alfabeto.
6. Une los caracteres mediante `"".join(caracteres_cifrados)`.

Se resta 1 a la longitud del alfabeto porque los índices empiezan en 0: la última
posición es 26, aunque existan 27 letras.

### Menú

`main()` llama a `cifrar_atbash(texto)` tanto para cifrar como para descifrar.
Solo cambia el mensaje que acompaña al resultado. La opción 3 termina el bucle
con `break`, y una opción inválida muestra un aviso.

El bloque `if __name__ == "__main__":` abre el menú cuando se ejecuta el archivo,
pero permite importar la función sin iniciar una sesión interactiva.

## Cómo utilizarlo

Desde la raíz del repositorio:

```bash
python3 3.atbash.py
```

- Opción 1: introduce `Abc`; obtendrás `Zyx`.
- Opción 2: introduce `Zyx`; recuperarás `Abc`.
- Opción 3: termina el programa.

## Caracteres y límites

Conserva mayúsculas y minúsculas. Invierte la ñ como parte del alfabeto, mientras
que las vocales con tilde, la ü, los números, los espacios y los signos quedan
sin cambios.

Cualquier persona que conozca el alfabeto usado puede invertir la transformación.
Atbash es un ejercicio educativo, no un método para proteger datos confidenciales.
