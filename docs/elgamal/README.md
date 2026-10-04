# ElGamal para enteros

[Volver al índice](../../README.md) · [Ver el código](../../24.elgamal.py)

## Alcance de esta implementación

Esta es una demostración matemática con enteros y primos pequeños, entre 5 y
1 000 000. No cifra texto, no autentica mensajes y no utiliza parámetros de
seguridad adecuados para datos reales. Las claves se muestran en pantalla y no
se almacenan en archivos. El objetivo es poder seguir las operaciones a mano.

## Teoría

Se elige un primo y un generador del grupo multiplicativo módulo ese primo.
La clave privada es un exponente secreto. La pública incluye el primo, el
generador y el resultado de elevar el generador al exponente privado.

```text
Valor público = generador^exponente privado % primo
```

Para cifrar se elige un exponente efímero nuevo:

```text
Primer componente = generador^exponente efímero % primo
Secreto compartido = valor público^exponente efímero % primo
Segundo componente = mensaje × secreto compartido % primo
```

El descifrado calcula el mismo secreto a partir del primer componente y el
exponente privado, y multiplica el segundo componente por su inverso modular.

```text
Secreto = primer componente^exponente privado % primo
Mensaje = segundo componente × inverso del secreto % primo
```

Con primo 23, generador 5 y exponente privado 6, el valor público es 8.
Para mensaje 10 y exponente efímero 3, los componentes son 10 y 14.
El secreto compartido es 6, su inverso módulo 23 es 4 y `14 × 4 % 23 = 10`.

## Variables principales

| Variable | Significado |
| --- | --- |
| `primo` | Módulo de las operaciones. |
| `generador` | Elemento de orden primo - 1. |
| `exponente_privado` | Número secreto del receptor. |
| `valor_publico` | Potencia pública derivada de la clave privada. |
| `exponente_efimero` | Número nuevo que se elige para un cifrado. |
| `primer_componente`, `segundo_componente` | Pareja que representa el mensaje cifrado. |
| `secreto_compartido` | Factor con el que se oculta y recupera el mensaje. |

## Explicación del código

`validar_parametros()` comprueba la primalidad y verifica que el generador tenga
orden primo - 1. Para cada factor primo de ese orden, exige que
`generador^((primo - 1) / factor) % primo` sea diferente de 1.

`generar_claves()` usa `secrets.randbelow()` para elegir el exponente privado y
calcula el valor público con `pow(base, exponente, modulo)`. Devuelve la privada
como `(primo, exponente)` y la pública como `(primo, generador, valor_publico)`.

`cifrar_elgamal()` exige un mensaje entre 1 y primo - 1 y genera un exponente
nuevo por defecto. Calcula la pareja con las fórmulas anteriores.
Su parámetro opcional `exponente_efimero` permite reproducir ejemplos en pruebas;
el menú no pide ese valor y lo genera automáticamente.

`descifrar_elgamal()` valida las longitudes y rangos de las claves y componentes.
Calcula el inverso con `pow(secreto_compartido, -1, primo)`.
Las comprobaciones de primos y factores están en
[utilidades_matematicas.py](../../utilidades_matematicas.py).

`main()` permite generar, cifrar y descifrar introduciendo los números separados
por espacios. Captura `ValueError` para volver al menú. El bloque
`if __name__ == "__main__":` impide iniciar el menú al importar.

## Uso y ejemplo

Desde la raíz del repositorio:

```bash
python3 24.elgamal.py
```

- Opción 1: deja vacíos primo y generador para usar 467 y 2. Guarda las dos claves
  mostradas; los exponentes variarán en cada generación.
- Opción 2: introduce la clave pública y un entero válido. Obtendrás dos enteros.
- Opción 3: introduce la clave privada y esos dos componentes para recuperarlo.
- Opción 4: salir.

Ejemplo fijo de descifrado: clave privada `23 6`, cifrado `10 14`; resultado `10`.
La clave pública correspondiente es `23 5 8`. El cifrado con ella puede producir
otra pareja por la elección aleatoria del exponente efímero.

## Límites

El mensaje 0 se rechaza para trabajar dentro del grupo multiplicativo.
Cambiar una clave o un componente puede producir otro entero sin avisar:
ElGamal básico no ofrece autenticación. No reutilices exponentes efímeros para
ocultar mensajes. Los primos pequeños y las operaciones Python de esta
demostración no constituyen una implementación para uso real.

## Referencia

Las operaciones de ElGamal se presentan en
[Handbook of Applied Cryptography, capítulo 8, sección 8.4](https://cacr.uwaterloo.ca/hac/about/chap8.pdf).
