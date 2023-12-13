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
- `acept error`: Variables para detectar aceptacion o error.
- `case_action`: Valor del elemento en la tabla de analisis sintactico.
- `production`: Valor de la produccion seleccionada en la regla gramatical.
- `analysis`" Analasis sintactico.

#### Limitaciones
El programa contiene las siguientes limitaciones:
- Tira de tokens leida desde un archivo.
- Formato especifico del archivo tira de tokens id * id + id