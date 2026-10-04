# Cifrado de sustitución simple

[Volver al índice](../../README.md) · [Ver el código](../../2.%20sustitucion_simple.py)

## Teoría

La sustitución simple asigna una letra de reemplazo a cada letra del alfabeto.
La misma letra siempre tiene el mismo reemplazo mientras se use la misma clave.
La clave es una reorganización de las 27 letras del alfabeto español.

Cada posición del alfabeto original se relaciona con la misma posición de la clave:

```text
Alfabeto: abcdefghijklmnñopqrstuvwxyz
Clave:    qwertyuiopasdfghjklñzxcvbnm
```

Por ejemplo, a se reemplaza por q, b por w y c por e. La clave puede establecer
reemplazos que no siguen un desplazamiento fijo, a diferencia del cifrado César.

| Letra original | Posición | Letra de la clave |
| --- | --- | --- |
| A | 0 | Q |
| b | 1 | w |
| c | 2 | e |

Con esta clave, `Abc` se convierte en `Qwe`.

Para descifrar se invierte la relación: se busca cada letra cifrada en la clave y
se toma la letra de esa posición en el alfabeto original. Así, Q vuelve a A.

La clave debe contener todas las letras exactamente una vez. Si dos letras
originales tuvieran el mismo reemplazo, no sería posible distinguirlas al
descifrar. Por eso se rechazan las claves con letras repetidas, faltantes o ajenas
al alfabeto.

## Explicación del código

### Variables principales

| Variable | Qué representa |
| --- | --- |
| `ALFABETO` | Las 27 letras en su orden original. |
| `clave` | Las mismas letras reorganizadas para definir los reemplazos. |
| `alfabeto_original` | Letras entre las que se busca el carácter de entrada. |
| `alfabeto_reemplazo` | Letras de las que se toma el carácter de salida. |
| `letra_minuscula` | Letra normalizada para realizar la búsqueda. |
| `posicion` | Índice compartido por la letra original y su reemplazo. |
| `letra_reemplazo` | Letra que se escribe en el resultado. |
| `caracteres_sustituidos` | Lista de los caracteres procesados. |

### Validación de la clave

`validar_clave(clave)` convierte la clave a minúsculas y comprueba:

```python
if len(clave) != len(ALFABETO) or set(clave) != set(ALFABETO):
    raise ValueError("La clave debe contener las 27 letras del alfabeto español una sola vez.")
```

`len()` verifica que haya 27 caracteres. `set()` compara las letras presentes
sin considerar su orden. Juntas, ambas comprobaciones garantizan que estén todas
las letras y no haya repeticiones. La función devuelve la clave en minúsculas.

### Sustitución y descifrado

`sustituir_letras(texto, alfabeto_original, alfabeto_reemplazo)` recorre el texto,
busca cada letra en el primer alfabeto y toma su reemplazo del segundo:

```python
posicion = alfabeto_original.index(letra_minuscula)
letra_reemplazo = alfabeto_reemplazo[posicion]
```

Después restaura la mayúscula si corresponde. Los caracteres fuera del alfabeto
se conservan. Finalmente, `"".join(caracteres_sustituidos)` forma el resultado.

`cifrar_sustitucion(texto, clave)` valida la clave y llama a:

```python
sustituir_letras(texto, ALFABETO, clave)
```

`descifrar_sustitucion(texto_cifrado, clave)` valida la misma clave e intercambia
los alfabetos para invertir los reemplazos:

```python
sustituir_letras(texto_cifrado, clave, ALFABETO)
```

`main()` solicita texto y clave. Si la clave es inválida, captura `ValueError`,
muestra el mensaje y vuelve al menú. El bloque `if __name__ == "__main__":`
permite importar las funciones sin abrir el menú.

## Cómo utilizarlo

Desde la raíz del repositorio:

```bash
python3 "2. sustitucion_simple.py"
```

1. Elige la opción 1 e introduce `Abc`.
2. Introduce la clave `qwertyuiopasdfghjklñzxcvbnm`; obtendrás `Qwe`.
3. Elige la opción 2 e introduce `Qwe` y la misma clave; recuperarás `Abc`.
4. Usa la opción 3 para salir.

Guarda la clave que utilizaste: el programa no la almacena ni la deduce del
mensaje cifrado. Una clave como `abc` o una que repita letras será rechazada.

## Caracteres y límites

Conserva mayúsculas y minúsculas, y sustituye la ñ. Las vocales con tilde, la ü,
los espacios, los números y los signos se mantienen sin cambios.

Aunque tiene muchas claves posibles, mantiene las repeticiones y frecuencias de
las letras, lo que permite analizar patrones para intentar recuperar el mensaje.
Su finalidad es educativa; no protege información confidencial.
