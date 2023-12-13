from components.ColeccionCanonica import coleccion_canonica
from components.PrimerosSiguientes import PrimerosYsiguientes
from utils.grammar import get_TAgrammar

#Programa que contiene la función para obtener la tabla de análisis sintáctico, así como sus funciones auxiliares

def obtenerIndex(simbolo, array):
    for i in range(len(array)):
        if array[i] == simbolo:
            return i
    return -1

def puntoAlFinal(cad):
    final = len(cad) - 1
    return cad[final] == "."

def modificar_cadena(cadOrig):
    indice_punto = cadOrig.find('.')
    if indice_punto > 0 and cadOrig[indice_punto - 1] == ' ':
        cad_modificada = cadOrig[:indice_punto - 1]
        return cad_modificada
    return cadOrig

def imprimirTabla(tas, te, nt):
    print("    ", end=' ')
    if "@" in te:
        for ter in te[:-1]:
            print(ter + "    ", end=' ')
    else:
        for ter in te:
            print(ter + "    ", end=' ')
    print("$ ", end=' ')
    print(str(nt))
    i = 0
    for estado in tas:
        print(str(i) + " " + str(estado))
        i += 1

def tablaDeAnalisisSintactico(Gramatica, coleccionEstados, ir_aTerminales, ir_aNoTerminales, siguientes, terminales, noTerminales):
    TAS = []

    if "@" in terminales:
        lenTerminales = len(terminales) - 1 #variable que guarda la longitud - 1 del arreglo de los simbolos terminales
    else:
        lenTerminales = len(terminales) #variable que guarda la longitud del arreglo de los simbolos terminales

    lenNoTerminales = len(noTerminales) #variable que guarda la longitud del arreglo de los simbolos no terminales
    lenGramatica = len(Gramatica)

    #Creando la tabla de transiciones
    for i in range(len(coleccionEstados)):
        TAS.append([])
        for j in range(lenTerminales + 1 + lenNoTerminales):
            TAS[i].append("  ")

    #Recorremos los ir_a con terminales y se agregan a la tabla de transiciones
    for transiciones in ir_aTerminales:
        simbolo = transiciones[1]   #guarda el símbolo con el que se ejecuta la transicion
        if simbolo == "$":  #Pregunta si es el símbolo de aceptación y lo coloca en la última columna de Acción
            TAS[transiciones[0]][lenTerminales] = "AC"
        else:   #Si no, coloca en [estado][index del simboloTerminal] el número de estado al que va la transicion
            TAS[transiciones[0]][obtenerIndex(transiciones[1], terminales)] = "d" + str(transiciones[2])

    #Recorremos los ir_a con no terminales y se agregan a la tabla de transiciones
    for transiciones in ir_aNoTerminales:
        simbolo = transiciones[1]   #guarda el símbolo con el que se ejecuta la transicion
        #coloca en [estado][lenTerminales + 1 posicion ($) + index del simboloNoTerminal] el número de estado al que va la transicion
        TAS[transiciones[0]][lenTerminales + 1 + obtenerIndex(transiciones[1], noTerminales)] = str(transiciones[2])

    #Recorremos los estados de la colección canónica
    noDeEstado = 0
    for estado in coleccionEstados:
        for elemento in estado:
            if puntoAlFinal(elemento):
                nuevaCadena = modificar_cadena(elemento)    #elimina el punto y el espacio del final del elemento y lo guarda en una nueva cadena
                if len(nuevaCadena) == 1:
                    nuevaCadena = nuevaCadena + " @"
                noTerminal = nuevaCadena[0]     #resguarda el no terminal del que se usarán los siguientes
                for numRegla in range(lenGramatica):    #busca la producción en la gramática
                    if nuevaCadena == Gramatica[numRegla]:  #cuando encuentra la producción en la gramática, comienza a ingresar los remplazar(r)
                        siguientesNoTerminal = siguientes[obtenerIndex(noTerminal, noTerminales)]   #obtiene los siguientes del no terminal
                        for simbolo in siguientesNoTerminal:
                            if simbolo == "$":  #Pregunta si es el símbolo de aceptación y coloca el r en la última columna de Acción
                                TAS[noDeEstado][lenTerminales] = "r" + str(numRegla + 1)
                            else:   #Si no, coloca en [estado][index del simboloTerminal] el número de estado al que va la transicion
                                TAS[noDeEstado][obtenerIndex(simbolo, terminales)] = "r" + str(numRegla + 1)
        noDeEstado += 1
    return TAS



#Gramatica = [
#    "E' E $",   #0
#    "E E + T",  #1
#    "E T",      #2
#    "T T * F",  #3
#    "T F",      #4
#    "F ( E )",  #5
#    "F id"      #6
#]
#
#terminales = ["+", "*", "(", ")", "id"]
#noTerminales = ["E", "T", "F"]
#
#ir_aTerminales = [
#    [0, "(", 4],
#    [0, "id", 5],
#    [1, "$", -1],
#    [1, "+", 6],
#    [2, "*", 7],
#    [4, "(", 4],
#    [4, "id", 5],
#    [6, "(", 4],
#    [6, "id", 5],
#    [7, "(", 4],
#    [7, "id", 5],
#    [8, ")", 11],
#    [8, "+", 6],
#    [9, "*", 7]
#]
#
#ir_aNoTerminales = [
#    [0, "E", 1],
#    [0, "T", 2],
#    [0, "F", 3],
#    [4, "E", 8],
#    [4, "T", 2],
#    [4, "F", 3],
#    [6, "T", 9],
#    [6, "F", 3],
#    [7, "F", 10]
#]
#coleccionEstados = [
#    ["E' . E $", "E . E + T", "E . T", "T . T * F", "T . F", "F . ( E )", "F . id"],
#    ["E' E . $", "E E . + T"],
#    ["E T .", "T T . * F"],
#    ["T F ."],
#    ["F ( . E )", "E . E + T", "E . T", "T . T * F", "T . F", "F . ( E )", "F . id"],
#    ["F id ."],
#    ["E E + . T", "T . T * F", "T . F", "F . ( E )", "F . id"],
#    ["T T * . F", "F . ( E )", "F . id"],
#    ["F ( E . )", "E E . + T"],
#    ["E E + T .", "T T . * F"],
#    ["T T * F ."],
#    ["F ( E ) ."]
#]
#
#siguientes = [
#    ["$", "+", ")"],
#    ["$", "+", ")", "*"],
#    ["$", "+", ")", "*"]
#]
#
#TAS = []
#
##Script
#if "@" in terminales:
#    lenTerminales = len(terminales) - 1 #variable que guarda la longitud - 1 del arreglo de los simbolos terminales
#else:
#    lenTerminales = len(terminales) #variable que guarda la longitud del arreglo de los simbolos terminales
#
#lenNoTerminales = len(noTerminales) #variable que guarda la longitud del arreglo de los simbolos no terminales
#lenGramatica = len(Gramatica)
#
##Creando la tabla de transiciones
#for i in range(len(coleccionEstados)):
#    TAS.append([])
#    for j in range(lenTerminales + 1 + lenNoTerminales):
#        TAS[i].append("  ")
#
##Recorremos los ir_a con terminales y se agregan a la tabla de transiciones
#for transiciones in ir_aTerminales:
#    simbolo = transiciones[1]   #guarda el símbolo con el que se ejecuta la transicion
#    if simbolo == "$":  #Pregunta si es el símbolo de aceptación y lo coloca en la última columna de Acción
#        TAS[transiciones[0]][lenTerminales] = "AC"
#    else:   #Si no, coloca en [estado][index del simboloTerminal] el número de estado al que va la transicion
#        TAS[transiciones[0]][obtenerIndex(transiciones[1], terminales)] = "d" + str(transiciones[2])
#
##Recorremos los ir_a con no terminales y se agregan a la tabla de transiciones
#for transiciones in ir_aNoTerminales:
#    simbolo = transiciones[1]   #guarda el símbolo con el que se ejecuta la transicion
#    #coloca en [estado][lenTerminales + 1 posicion ($) + index del simboloNoTerminal] el número de estado al que va la transicion
#    TAS[transiciones[0]][lenTerminales + 1 + obtenerIndex(transiciones[1], noTerminales)] = str(transiciones[2])
#
##Recorremos los estados de la colección canónica
#noDeEstado = 0
#for estado in coleccionEstados:
#    for elemento in estado:
#        if puntoAlFinal(elemento):
#            nuevaCadena = modificar_cadena(elemento)    #elimina el punto y el espacio del final del elemento y lo guarda en una nueva cadena
#            noTerminal = nuevaCadena[0]     #resguarda el no terminal del que se usarán los siguientes
#            for numRegla in range(lenGramatica):    #busca la producción en la gramática
#                if numRegla == 0:   #ignora la producción 0, ya que es parte de la gramática aumentada
#                    continue
#                if nuevaCadena == Gramatica[numRegla]:  #cuando encuentra la producción en la gramática, comienza a ingresar los remplazar(r)
#                    siguientesNoTerminal = siguientes[obtenerIndex(noTerminal, noTerminales)]
#                    for simbolo in siguientesNoTerminal:
#                        if simbolo == "$":  #Pregunta si es el símbolo de aceptación y coloca el r en la última columna de Acción
#                            TAS[noDeEstado][lenTerminales] = "r" + str(numRegla)
#                        else:   #Si no, coloca en [estado][index del simboloTerminal] el número de estado al que va la transicion
#                            TAS[noDeEstado][obtenerIndex(simbolo, terminales)] = "r" + str(numRegla)
#    noDeEstado += 1
#
#imprimirTabla(TAS, terminales, noTerminales)

# --------------------------------------------------------------------------------------------------
def gramaticaSinEspacios(gramatica):    #funcion que crea una nueva gramática o Reglas, con los espacios eliminados
    nuevaGramatica = []
    for regla in gramatica:
        nuevaGramatica.append(regla.replace(" ", ""))
    return nuevaGramatica

def to_create(path):
    #Gramática 1
    #NT = ["E", "T", "F"]
    #TE = ["+", "*", "(", ")", "id"]
    #Reglas = [
    #    "E E + T",
    #    "E T",
    #    "T T * F",
    #    "T F",
    #    "F ( E )",
    #    "F id"
    #]

    #Gramática 2
    # NT = ["D", "L", "T"]
    # TE = ["id", ";", ",", "float", "int"]
    # Reglas = [
    #     "D T id L ;",
    #     "L , id L",
    #     "L @",
    #     "T float",
    #     "T int"
    # ]

    NT, TE, Reglas = get_TAgrammar(path)
    #Script
    Reglas2 = gramaticaSinEspacios(Reglas)  #crea la gramatica sin espacios, para usarla en PrimerosYsiguientes()
    PYS = PrimerosYsiguientes(TE, NT, Reglas2)  #obtiene primeros y siguientes, en un diccionario
    siguientes = PYS['S']       #guarda solo la lista de siguientes, para usarla en tablaDeAnalisisSintactico()
    ir_a_NT, ir_a_TE, states = coleccion_canonica(NT, TE, Reglas)   #obtiene los ir_a de terminales y no terminales y la lista de estados
    tablaAS = tablaDeAnalisisSintactico(Reglas, states, ir_a_TE, ir_a_NT, siguientes, TE, NT)   #obtiene la tabla de análisis sintáctico
    
    # print("-------------REGLAS2----------")
    # for m in Reglas2:
    #     print(m)
    # print("\n")
    # print("-------------REGLAS----------")
    # for n in Reglas:
    #     print(n)
    # print("\n")
    # print("-------------SIGUIENTES----------")
    # for l in siguientes:
    #     print(l)
    # print("\n")
    # print("-------------IR_A_NT----------")
    # for i in ir_a_NT:
    #     print(i)
    # print("\n")
    # print("-------------IR_A_TE----------")
    # for j in ir_a_TE:
    #     print(j)
    # print("\n")
    # print("------------ESTATES-----------")
    # for k in states:
    #     print(k)
    # print("\n")
    # print("------------TAS-----------")
    # imprimirTabla(tablaAS, TE, NT)

    return NT, TE, tablaAS