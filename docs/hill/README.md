# Cifrado Hill de 2 × 2

[Volver al índice](../../README.md) · [Ver el código](../../10.hill.py)

## Teoría

Hill cifra grupos de letras mediante multiplicación de matrices. Este programa
trabaja con parejas y una matriz clave de 2 × 2, usando las 27 letras españolas.
Cada letra se convierte en su índice: a = 0, n = 13, ñ = 14 y z = 26.

Para una pareja con valores primero y segundo:

```text
Matriz clave: [ a b ]
              [ c d ]

Primer resultado  = (a × primero + b × segundo) % 27
Segundo resultado = (c × primero + d × segundo) % 27
```

Para descifrar se utiliza la matriz inversa módulo 27. Existe si el determinante
`a × d - b × c` es coprimo con 27, es decir, si no es múltiplo de 3.

Con la matriz `[1, 2; 3, 5]`, el determinante es -1 y sí existe inversa:

```text
Clave:   [1 2]       Inversa módulo 27: [22  2]
         [3 5]                          [ 3 26]
```

En la pareja Ho, los valores son 7 y 15. Se obtienen
`(1 × 7 + 2 × 15) % 27 = 10` y `(3 × 7 + 5 × 15) % 27 = 15`, que producen Ko.
La pareja la produce lg. Por tanto, `Hola` se convierte en `Kolg`.

## Explicación del código

| Variable | Significado |
| --- | --- |
| `matriz_clave` | Dos filas de dos enteros cada una. |
| `determinante` | Valor que permite comprobar si la matriz es invertible. |
| `inverso_determinante` | Inverso modular del determinante. |
| `posiciones_letras` | Índices de las letras que participan en las parejas. |
| `valores_pareja` | Los dos índices alfabéticos que se multiplican. |
| `caracteres_resultado` | Copia del texto en la que se reemplazan las letras. |

`validar_matriz()` comprueba el tamaño, el tipo de los valores y el máximo común
divisor del determinante con 27.

`invertir_matriz()` calcula el inverso del determinante con `pow(..., -1, 27)` y
utiliza la fórmula:

```text
Inversa = inverso del determinante × [ d -b ]  módulo 27
                                    [-c  a ]
```

`transformar_hill()` localiza las letras del alfabeto y las agrupa de dos en dos,
saltando los demás caracteres. Multiplica cada pareja y coloca los resultados
en sus posiciones originales, conservando las mayúsculas de cada posición.

`cifrar_hill()` valida la clave y transforma con ella.
`descifrar_hill()` transforma con la matriz inversa.

`main()` solicita cuatro enteros por filas, captura errores y vuelve al menú.
El bloque `if __name__ == "__main__":` permite importar sin ejecutar el menú.

## Uso y ejemplo

Desde la raíz del repositorio:

```bash
python3 10.hill.py
```

- Opción 1: texto `Hola`, clave `1 2 3 5`; resultado `Kolg`.
- Opción 2: texto `Kolg`, misma clave; resultado `Hola`.
- Opción 3: salir.

También `Ho la` produce `Ko lg`: los espacios quedan en su lugar y las parejas
se forman solo con las letras del alfabeto.

## Caracteres y límites

Cifra la ñ y conserva mayúsculas, tildes, ü, signos, números y espacios.
El mensaje debe contener una cantidad **par de letras del alfabeto**. No se añade
relleno: un texto como `Sol` se rechaza y debe completarse de forma explícita.
Contar los caracteres totales no sirve si hay espacios o tildes.

La restricción permite recuperar exactamente el mensaje aceptado, sin adivinar
si una letra final era relleno. Hill es educativo y puede analizarse mediante
relaciones lineales; no protege información confidencial.
