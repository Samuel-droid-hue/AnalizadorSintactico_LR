import components.AnalizadorSintactico_LR as lr

if __name__ == "__main__":
    analysis, program, tokens = lr.to_analyze("tests/grammar.txt", "tests/tokens(1).txt")
    
    print("Programa: ", program)
    print("Tokens: ", tokens)
    print('')

    print("Pila\t\tEntrada\t\tAccion")
    for i in range(len(analysis)):
        for j in range(len(analysis[i])):
            print(analysis[i][j], end='\t|\t')
        print('')