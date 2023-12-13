# Analizador Sintactico LR
Implementación del algoritmo Analizador Sintáctico LR para gramáticas de clases

## Estructura del proyecto
A continuacion se describe la estructura de los directorios:
- `tests`: Archivos txt de prueba para el analizador.
- `utils`: Archivos py de herramientas generales para compiladores.
- `components`: Archivos py de componentes para el analizador.

### Variables
El programa utiliza las siguientes variables:
- `stack`: Lista para almacenar el contenido de la columna PILA
- `input`: Lista para almacenar el contenido de la columna ENTRADA
- `action`: ACCION

#### Limitaciones
El programa contiene las siguientes limitaciones:
- No considera estados de mas de 1 digito.
- No considera aceptacion o error.
- Tira de tokens leida desde un archivo.