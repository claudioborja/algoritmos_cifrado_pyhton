# Cifrado Trifid con alfabeto español

[Volver al índice](../../README.md) · [Ver el código](../../22.trifid.py)

## Teoría

Trifid utiliza tres coordenadas por letra: plano, fila y columna de un cubo
3 × 3 × 3. Esta variante utiliza las **27 letras españolas**, incluida la ñ,
en lugar de 26 letras y un símbolo adicional.

La clave sin repeticiones, seguida de las letras faltantes, determina el orden
de las 27 casillas. Cada plano contiene 9 letras, repartidas en tres filas.
Para cada bloque se unen todos los planos, todas las filas y todas las columnas.
La secuencia se vuelve a agrupar en ternas para obtener el texto cifrado.

Con clave `a`, `ABC` y período 3:

```text
Coordenadas: (0,0,0) (0,0,1) (0,0,2)
Planos:      0 0 0
Filas:       0 0 0
Columnas:    0 1 2
Secuencia:   0 0 0 0 0 0 0 1 2
Ternas:      (0,0,0) (0,0,0) (0,1,2) → A A F
```

El resultado es `AAF`. El descifrado separa la secuencia en tres partes iguales
y vuelve a combinar las coordenadas originales.

## Variables principales

| Variable | Significado |
| --- | --- |
| `periodo` | Cantidad máxima de letras por bloque. |
| `plano`, `fila`, `columna` | Coordenadas internas entre 0 y 2. |
| `resto` | Posición dentro de un plano de nueve casillas. |
| `longitud_bloque` | Longitud real del grupo que se transforma. |
| `numeros` | Lista de coordenadas para mezclar o separar. |

## Explicación del código

`obtener_coordenadas()` divide primero la posición entre 9 y luego el resto
entre 3 usando `divmod()`.

`transformar_trifid()` construye el alfabeto clave y procesa bloques. Al cifrar
concatena `planos + filas + columnas`. Al descifrar separa una lista de ternas
aplanadas en tres segmentos de `longitud_bloque`.
Reconstruye cada letra con `plano * 9 + fila * 3 + columna`.

`cifrar_trifid()` y `descifrar_trifid()` eligen el sentido. El último bloque puede
ser más corto y no utiliza relleno. Con período 1 se obtiene el texto normalizado.

La validación y preparación de alfabetos se encuentran en
[utilidades_clasicas.py](../../utilidades_clasicas.py). Las funciones compartidas
comprueban caracteres, convierten a mayúsculas cuando corresponde y eliminan
repeticiones de las claves para construir tablas.

`main()` solicita el mensaje y los parámetros, muestra errores de entrada y vuelve
al menú. El bloque `if __name__ == "__main__":` permite importar las funciones
sin abrir una sesión interactiva.

## Uso y ejemplo

Desde la raíz del repositorio:

```bash
python3 22.trifid.py
```

- Opción 1: texto `ABC`, clave `a`, período `3`; resultado `AAF`.
- Opción 2: texto `AAF`, misma clave y período; resultado `ABC`.
- Opción 3: salir.

## Caracteres y límites

Admite ñ, elimina espacios y devuelve mayúsculas. Rechaza tildes, signos y números.
Una implementación con un símbolo como # en lugar de ñ no será compatible con
esta variante. Para descifrar se necesitan el mismo alfabeto, clave y período.

Es un ejercicio educativo; no debe utilizarse para proteger información confidencial.

## Referencia

[Regla Trifid de la ACA](https://www.cryptogram.org/downloads/aca.info/ciphers/Trifid.pdf). La guía describe la variante concreta utilizada en este repositorio.
