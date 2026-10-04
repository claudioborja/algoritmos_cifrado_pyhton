# Cifrado afín

[Volver al índice](../../README.md) · [Ver el código](../../8.afin.py)

## Teoría

El cifrado afín transforma la posición de cada letra mediante una multiplicación
y una suma. Utiliza dos números como clave: el multiplicador y el desplazamiento.
En este programa se trabaja con las 27 letras del alfabeto español, con a = 0,
n = 13, ñ = 14 y z = 26.

```text
posición cifrada = (multiplicador × posición original + desplazamiento) % 27
posición original = inverso × (posición cifrada - desplazamiento) % 27
```

`%` calcula el resto de una división. El inverso modular es un número que,
multiplicado por el multiplicador, da resto 1 al dividir entre 27.
Existe solo si ambos números son coprimos: su máximo común divisor debe ser 1.
Como 27 es una potencia de 3, el multiplicador no puede ser múltiplo de 3.

Con multiplicador 5 y desplazamiento 8, `Hola` pasa a `Pcji`:

| Letra | Posición | Cálculo módulo 27 | Resultado |
| --- | --- | --- | --- |
| H | 7 | (5 × 7 + 8) % 27 = 16 | P |
| o | 15 | (5 × 15 + 8) % 27 = 2 | c |
| l | 11 | (5 × 11 + 8) % 27 = 9 | j |
| a | 0 | (5 × 0 + 8) % 27 = 8 | i |

El inverso de 5 es 11 porque `5 × 11 % 27 = 1`. Para recuperar H desde P se
calcula `11 × (16 - 8) % 27 = 7`.

## Explicación del código

| Variable | Significado |
| --- | --- |
| `ALFABETO` | Las 27 letras disponibles. |
| `multiplicador` | Factor que multiplica la posición original. |
| `desplazamiento` | Cantidad que se suma después de multiplicar. |
| `inverso_multiplicador` | Factor que permite invertir la transformación. |
| `posicion_resultado` | Índice de la letra de salida. |
| `caracteres_transformados` | Lista donde se construye el mensaje. |

`validar_claves()` comprueba que las claves sean enteros y que
`gcd(multiplicador, 27)` sea 1. `gcd()` calcula el máximo común divisor.

`transformar_afin()` recorre cada carácter, busca las letras en el alfabeto y
aplica la fórmula. Restaura las mayúsculas y conserva los caracteres restantes.

`cifrar_afin()` valida las claves y llama a la transformación.
`descifrar_afin()` calcula el inverso con:

```python
inverso_multiplicador = pow(multiplicador, -1, len(ALFABETO))
```

Después reutiliza la transformación con el inverso como multiplicador y
`-inverso_multiplicador * desplazamiento` como suma. Esto equivale a restar el
desplazamiento antes de multiplicar por el inverso.

`main()` solicita las dos claves, muestra errores y permite volver al menú.
La protección `if __name__ == "__main__":` permite importar sin abrir el menú.

## Uso y ejemplo

Desde la raíz del repositorio:

```bash
python3 8.afin.py
```

- Opción 1: mensaje `Hola`, multiplicador `5`, desplazamiento `8`; produce `Pcji`.
- Opción 2: mensaje `Pcji` y las mismas claves; recupera `Hola`.
- Opción 3: salir.

Se admiten claves negativas y mayores que 27 siempre que el multiplicador sea
válido. Un multiplicador como 3 se rechaza porque no tiene inverso módulo 27.

## Caracteres y límites

La ñ se cifra. Se conservan mayúsculas, tildes, ü, signos, números y espacios.
Las letras repetidas mantienen el mismo reemplazo, por lo que este cifrado
educativo puede analizarse por frecuencias y no protege información confidencial.
