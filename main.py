import components.AnalizadorSintactico_LR as lr

if __name__ == "__main__":
    lr.to_analyze("tests/grammar.txt", "tests/tokens(1).txt")