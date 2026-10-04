# Enigma simplificada

[Volver al índice](../../README.md) · [Ver el código](../../12.enigma_simplificada.py)

## Teoría del modelo

Una máquina de rotores cambia la sustitución de las letras a medida que se escribe
el mensaje. Cada rotor contiene un alfabeto reorganizado; su posición modifica
la relación entre la entrada y la salida.

Este modelo educativo utiliza tres rotores fijos y un reflector. Las posiciones
iniciales se indican con tres letras, de izquierda a derecha. `aaa` significa que
los tres comienzan en la posición cero.

Antes de transformar cada letra, avanza el rotor derecho. Al completar una vuelta,
arrastra al central; cuando este completa otra vuelta, arrastra al izquierdo.
Es un contador de base 26. No simula las muescas, el doble paso, los anillos ni
el clavijero de la máquina histórica.

El recorrido de una letra es:

```text
Entrada → rotor derecho → rotor central → rotor izquierdo
        → reflector
        → inverso del izquierdo → inverso del central → inverso del derecho
        → salida
```

El reflector intercambia letras por parejas. Gracias a ese intercambio y al
recorrido inverso de vuelta, repetir la transformación con las mismas posiciones
iniciales recupera el mensaje.

## Explicación del código

| Variable | Significado |
| --- | --- |
| `ALFABETO` | Las 26 letras de a a z. |
| `ROTORES` | Tres permutaciones fijas del alfabeto. |
| `REFLECTOR` | Relación de parejas que devuelve la señal hacia los rotores. |
| `posiciones_rotores` | Posiciones actuales del izquierdo, central y derecho. |
| `valor_letra` | Índice numérico que viaja por los rotores. |
| `posicion_entrada` | Índice tras considerar la posición del rotor. |
| `posicion_salida` | Índice obtenido de la sustitución del rotor. |

`validar_posiciones()` exige tres letras de a a z y las convierte en índices.
`avanzar_rotores()` incrementa primero la posición derecha y propaga el avance
solo cuando el rotor vuelve a cero.

`pasar_por_rotor()` suma la posición del rotor a la entrada, aplica su permutación
y resta la posición a la salida. Todo se calcula módulo 26. Para el regreso,
busca la posición de la letra en el rotor en lugar de leerla directamente.

`transformar_enigma()` crea posiciones nuevas para cada llamada. Avanza los
rotores solo cuando procesa una letra del alfabeto; luego recorre los tres
rotores, el reflector y los rotores en sentido inverso. Restaura la mayúscula.

`cifrar_enigma()` y `descifrar_enigma()` llaman a esa misma función. Por eso el
estado se reinicia al descifrar y no continúa donde terminó el cifrado.

`main()` solicita las posiciones y controla el menú. El bloque
`if __name__ == "__main__":` permite importar las funciones sin iniciar el menú.

## Uso y ejemplo

Desde la raíz del repositorio:

```bash
python3 12.enigma_simplificada.py
```

- Opción 1: mensaje `Hola`, posiciones `aaa`; resultado `Iibg`.
- Opción 2: mensaje `Iibg`, posiciones `aaa`; resultado `Hola`.
- Opción 3: salir.

Las posiciones deben reiniciarse al mismo valor para cada mensaje independiente.
Este ejemplo pertenece al modelo implementado y no debe usarse como vector de
una máquina Enigma histórica.

## Caracteres y límites

Se conservan mayúsculas. La ñ, las tildes, la ü, los números, los espacios y los
signos quedan en su lugar y no avanzan los rotores.

Es una simulación educativa de sustituciones variables, no una implementación
histórica completa ni un sistema moderno para proteger información confidencial.
