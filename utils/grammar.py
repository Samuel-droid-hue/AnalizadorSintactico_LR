# Get data structure to augmented grammar to AnalizadorSintactico LR
def get_ASgrammar(path):
    with open(path, "r") as file:
        content = file.readlines()
    
    grammar = []
    content = content[2:]

    for line in content:
        grammar.append(line.strip().split(" -> "))

    return grammar

def get_TAgrammar(path):
    with open(path, "r") as file:
        content = file.readlines()

    NT = content[0].split()
    TE = content[1].split()

    grammar = []
    content = content[3:]

    for line in content:
        grammar.append(line.strip().replace(" -> ", " "))

    return NT, TE, grammar