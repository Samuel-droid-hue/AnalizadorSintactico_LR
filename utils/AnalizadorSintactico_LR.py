def open_file(path):
    with open(path, "r") as file:
        content = file.readlines()
    
    grammar = []
    for line in content:
        grammar.append(line.strip())
    
    for rule in grammar:
        print(rule)