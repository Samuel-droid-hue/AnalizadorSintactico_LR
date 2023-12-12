# Get data structure to augmented grammar
def get_grammar(path):
    with open(path, "r") as file:
        content = file.readlines()
    
    grammar = []
    for line in content:
        grammar.append(line.strip().split(" -> "))

    return grammar