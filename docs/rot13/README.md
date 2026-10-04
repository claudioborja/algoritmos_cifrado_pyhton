# Cifrado ROT13

[Volver al índice](../../README.md) · [Ver el código](../../4.%20ROT13.py)

## Teoría

ROT13 es un cifrado César con un desplazamiento fijo de 13 posiciones sobre las
26 letras de a a z. No solicita clave porque el desplazamiento siempre es 13.

```text
Original: abcdefghijklmnopqrstuvwxyz
ROT13:    nopqrstuvwxyzabcdefghijklm
```

Las posiciones empiezan en cero y la transformación se calcula así:

```text
posición cifrada = (posición original + 13) % 26
```

El operador `%` obtiene el resto de la división y mantiene la posición entre 0 y
25. Así, después de z se vuelve a a.

| Letra original | Posición original | Cálculo | Resultado |
| --- | --- | --- | --- |
| a | 0 | (0 + 13) % 26 = 13 | n |
| n | 13 | (13 + 13) % 26 = 0 | a |
| z | 25 | (25 + 13) % 26 = 12 | m |

Aplicar ROT13 dos veces suma 26 posiciones, una vuelta completa al alfabeto.
Por eso la misma operación cifra y descifra: `Hola` pasa a `Ubyn`, y `Ubyn`
vuelve a `Hola`.

La ñ queda fuera del alfabeto y se conserva. Usar 27 letras impediría recuperar
el texto al aplicar dos veces el desplazamiento de 13, porque 26 posiciones ya
no representarían una vuelta completa.

## Explicación del código

### Variables principales

| Variable | Qué representa |
| --- | --- |
| `ALFABETO` | Las 26 letras de a a z. |
| `DESPLAZAMIENTO` | Constante con el valor 13. |
| `texto` | Mensaje que se transforma. |
| `caracter` | Carácter que se está procesando. |
| `letra_minuscula` | Letra normalizada para buscar en el alfabeto. |
| `posicion_original` | Posición antes de aplicar ROT13. |
| `posicion_cifrada` | Posición después de avanzar 13 lugares. |
| `letra_cifrada` | Letra que sustituye a la original. |
| `caracteres_cifrados` | Lista de los caracteres de salida. |

### Cifrado y descifrado

`cifrar_rot13(texto)` recorre cada carácter. Si su versión en minúscula pertenece
al alfabeto, obtiene su índice y calcula:

```python
posicion_cifrada = (posicion_original + DESPLAZAMIENTO) % len(ALFABETO)
```

Busca la letra de esa posición y restaura la mayúscula si el carácter original
era mayúsculo. Si no pertenece al alfabeto, lo agrega sin modificarlo.
Al final devuelve `"".join(caracteres_cifrados)`.

`descifrar_rot13(texto_cifrado)` reutiliza la misma función:

```python
return cifrar_rot13(texto_cifrado)
```

Esto funciona porque las letras se agrupan en parejas de reemplazo, como a y n,
b y o, o c y p.

### Menú

`main()` solicita el texto y llama a la función de cifrado o descifrado según la
opción seleccionada. La opción 3 sale y las opciones inválidas muestran un aviso.
No necesita pedir desplazamiento ni validar una clave.

El bloque `if __name__ == "__main__":` permite ejecutar el menú al abrir el
programa y mantenerlo inactivo cuando se importan sus funciones.

## Cómo utilizarlo

Desde la raíz del repositorio:

```bash
python3 "4. ROT13.py"
```

- Opción 1: introduce `Hola ñá`; obtendrás `Ubyn ñá`.
- Opción 2: introduce `Ubyn ñá`; recuperarás `Hola ñá`.
- Opción 3: termina el programa.

## Caracteres y límites

Respeta mayúsculas y minúsculas. La ñ, las vocales con tilde, la ü, los espacios,
los números y los signos permanecen sin cambios.

ROT13 permite ocultar un texto a simple vista, pero cualquiera puede recuperar
el mensaje aplicando la misma operación. No protege información confidencial.
