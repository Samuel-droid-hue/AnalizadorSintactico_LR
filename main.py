import components.AnalizadorSintactico_LR as lr
import components.TablaAnalisis as ta

if __name__ == "__main__":
    analysis, program, tokens = lr.to_analyze("tests/grammar(2).txt", "tests/tokens(2).txt")
    
    print("Programa: ", program)
    print("Tokens: ", tokens)
    print('')

    print("Pila\t\tEntrada\t\tAccion")
    for i in range(len(analysis)):
        for j in range(len(analysis[i])):
            print(analysis[i][j], end='\t|\t')
        print('')

    #NT, TE, table = ta.to_create("tests/grammar(2).txt")
    #print(ta.imprimirTabla(table, TE, NT))