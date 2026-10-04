# Paillier y sumas sobre cifrados

[Volver al índice](../../README.md) · [Ver el código](../../25.paillier.py)

## Alcance de esta implementación

Es una demostración matemática para enteros no negativos, con primos pequeños
entre 3 y 1 000 000. Permite observar cómo sumar valores sin descifrarlos primero.
No utiliza tamaños de clave de producción ni autentica mensajes. No cifra texto.
Las claves se muestran en pantalla y no se guardan en archivos.

## Teoría

Se escogen dos primos diferentes y se calcula su producto, el módulo público.
Este programa utiliza como generador el módulo más uno:

```text
módulo = primer primo × segundo primo
exponente privado = mcm(primer primo - 1, segundo primo - 1)
generador = módulo + 1
inverso privado = inverso del exponente privado módulo el módulo
```

La elección del generador requiere que exponente privado y módulo sean coprimos.
Al cifrar se utiliza un número aleatorio coprimo con el módulo:

```text
cifrado = generador^mensaje × aleatorio^módulo % módulo²
```

El descifrado aplica una potencia y una división exacta:

```text
potencia = cifrado^exponente privado % módulo²
cociente = (potencia - 1) / módulo
mensaje = cociente × inverso privado % módulo
```

Con primos 17 y 19, la clave pública es 323 y la privada es `(323, 144, 83)`.
Con mensaje 7 y aleatorio 2, se obtiene el cifrado 93338. El menú elige el
aleatorio automáticamente, de modo que los resultados pueden variar.

### Propiedad de suma

Multiplicar dos cifrados módulo módulo² produce un cifrado de la suma de sus
mensajes **módulo la clave pública**. Por ejemplo, con módulo 323:

```text
7 + 9 = 16
320 + 10 = 330 → 330 % 323 = 7
```

El segundo caso no permite recuperar 330 directamente. Hay que elegir un módulo
que cubra el rango esperado si se desea evitar ese retorno al inicio.

## Variables principales

| Variable | Significado |
| --- | --- |
| `modulo` | Producto de los dos primos y clave pública. |
| `modulo_cuadrado` | Módulo con el que se calculan los cifrados. |
| `exponente_privado` | Mínimo común múltiplo utilizado al descifrar. |
| `inverso_privado` | Inverso modular que recupera el mensaje. |
| `aleatorio` | Factor nuevo de ocultación, coprimo con el módulo. |
| `cociente` | Resultado de la función (potencia - 1) / módulo. |
| `producto` | Combinación de los dos cifrados para representar la suma. |

## Explicación del código

`generar_claves()` valida los primos y usa `lcm()` y `gcd()` para calcular el
exponente y comprobar la condición del generador. Usa `pow(..., -1, modulo)` para
el inverso. Devuelve una privada de tres números y una pública de un número.

`cifrar_paillier()` exige un entero entre 0 y módulo - 1. Genera valores con
`secrets.randbelow()` hasta obtener uno coprimo y aplica la fórmula.
El parámetro opcional `aleatorio` existe para reproducir ejemplos en pruebas;
el menú siempre genera ese valor.

`validar_cifrado()` comprueba el rango y que el cifrado sea coprimo con el módulo.
`descifrar_paillier()` valida la relación del inverso, calcula la potencia y
comprueba que la división sea exacta antes de recuperar el entero.

`sumar_cifrados()` valida ambos cifrados y multiplica sus valores. Después
multiplica por un cifrado nuevo de cero para renovar la aleatoriedad sin cambiar
la suma. Ambos mensajes deben haberse cifrado con la misma clave pública;
el formato de entero aislado no incluye un identificador que lo garantice.

Las comprobaciones de primalidad están en
[utilidades_matematicas.py](../../utilidades_matematicas.py).
`main()` ofrece generación, cifrado, descifrado y suma, y maneja entradas inválidas.
El bloque `if __name__ == "__main__":` permite importar sin iniciar el menú.

## Uso y ejemplo

Desde la raíz del repositorio:

```bash
python3 25.paillier.py
```

1. Opción 1: deja vacíos los primos para usar 17 y 19. Obtendrás módulo `323`
   y clave privada `323 144 83`.
2. Opción 2: cifra 7 con módulo 323; conserva el entero cifrado.
3. Opción 2: cifra 9 con el mismo módulo; conserva el segundo cifrado.
4. Opción 4: introduce el módulo y ambos cifrados para obtener una suma cifrada.
5. Opción 3: descifra esa suma con `323 144 83`; recuperarás `16`.
6. Opción 5: salir.

Ejemplo fijo de descifrado: cifrado `93338`, privada `323 144 83`; resultado `7`.

## Límites

Se rechazan negativos, decimales y mensajes iguales o mayores que el módulo.
Las claves públicas introducidas deben proceder del generador del programa:
los controles de rango no prueban que un módulo externo sea producto de dos
primos válidos. Un entero cifrado no aporta autenticación ni identidad del emisor.

## Referencia

La propiedad aditiva y una implementación con generación de claves de mayor
tamaño se encuentran en la [documentación de python-paillier](https://python-paillier.readthedocs.io/en/stable/).
Este programa educativo utiliza solo la biblioteca estándar y muestra sus propias
operaciones matemáticas; no depende de `phe`.
