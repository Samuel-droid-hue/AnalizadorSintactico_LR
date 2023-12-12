import components.AnalizadorSintactico_LR as lr
import components.TablaAnalisis as ta

import utils.grammar as gm

if __name__ == "__main__":
    # lr.to_analyze("tests/grammar.txt", "tests/tokens.txt")
    NT, TE, TA = ta.to_create("tests/pastor_grammar.txt")
    # NT, TE, grammar = gm.get_TAgrammar("tests/grammar.txt")
    # print(NT)
    # print(TE)
    # print(grammar)
    print("NT: ", len(NT))
    print("TE: ", len(TE))
    print("TA: ", len(TA))