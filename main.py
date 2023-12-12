import components.AnalizadorSintactico_LR as lr
import utils.grammar as gm

if __name__ == "__main__":
    lr.to_analyze("tests/grammar.txt", "tests/tokens.txt")