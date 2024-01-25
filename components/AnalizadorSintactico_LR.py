import utils.grammar as gm
import components.TablaAnalisis as ta
import components.AnalizadorLexico1 as al

class Token:
    def __init__(self, token, lexema):
        self.token = token
        self.lexema = lexema

    def __str__(self):
        return f"{self.token}.\"{self.lexema}\""

# Get data to input stack
def get_input(tokens):
    # Convert tokens to data structure
    data = []
    for token in tokens:
        row = token.split(',')
        for r in range(len(row)):
            row[r] = row[r].strip()
        data.append(row)
    
    # Get input stack
    input = []
    for d in data:
        if d[1] != d[2]:
            input.append(Token(d[2], d[1]))
        else:
            input.append(d[1])

    return input

# Get data structure to token strip
def get_tokens(path):
    with open(path, "r") as file:
        content = file.readlines()

    # ONLY CONSIDER A SINGLE LINE OF FILE!
    tokens = []
    tokens = content[1].strip().split()

    return tokens

# Get one positiion on the table
# ------------------------------
# WARNING!: TOO MUCH PARAMAETERS
# ------------------------------
# s: State number
# a: Symbol
def get_action(TA, NT, TE, s, a):
    # Get i index
    i = int(s)
    # Get j index
    if a in TE:
        j = TE.index(a)
    else:
        j = len(TE) + NT.index(a)
        # j -= 1

    return TA[i][j]

def find_error(row, TE):
    indexs = []
    symbols = []
    n = len(TE)

    # Search into table row for not nulls values
    for i in range(0, n):
        if row[i] != '  ':
            indexs.append(i)

    for j in indexs:
        symbols.append(TE[j])
    
    return symbols

# Get format to rows
def get_rowda(stack, input, action):
    column1 = ' '.join(map(str, stack))
    column2 = ' '.join(str(e) for e in input)

    return [column1,  column2, action]

def get_rowr(stack, input, action, production, semantic):
    column1 = ' '.join(map(str, stack))
    column2 = ' '.join(str(e) for e in input)
    column3 = '->'.join(production)
    column3 = action + ' ' + column3 + ' ' + semantic

    return [column1, column2, column3]

def get_rowe(stack, input, symbols):
    column1 = ' '.join(map(str, stack))
    column2 = ' '.join(str(e) for e in input)
    column3 = 'Error se esperaba ' + ' o '.join(symbols)

    return [column1, column2, column3]



# ------------- ANALYZER ------------- #
def to_analyze(grammar_path, tokens_path, actions_path):
    # Variables
    augmentedGrammar = gm.get_ASgrammar(grammar_path)
    stack = []
    input = []
    accept = False
    error = False
    production = []
    analysis = []

    tokens, total = al.Application.to_analizar(al.Application,tokens_path)
    # print(tokens)
    # Get the table and more values
    NT, TE, TA = ta.to_create(grammar_path)
    TE.append('$')
    #tokens = al.to_analyze(tokens_path)
    input = get_input(total)
    # input = tokens.split()
    input.append('$')

    # Get semantic actions
    semantic = gm.get_semantic(actions_path)

    #################################
    ta.imprimirTabla(TA, TE, NT)

    #################################
    
    # Algorithm
    stack.append(0)

    while not (accept or error):
        print(analysis)
        # Get the atributte of the object is is required
        case_action = get_action(TA, NT, TE, stack[-1], input[0].token if isinstance(input[0], Token) else input[0])
        if case_action[0] in {'d', 'r'}:
            # Calculates index of dn or rn
            index = case_action[1:]
            index = int(index)
            if case_action[0] == 'd':
                # Modify the input to get the token and lexema on the row
                analysis.append(get_rowda(stack, input, case_action))
                stack.append(input[0])
                stack.append(index)
                input.pop(0)
            elif case_action[0] == 'r':
                production = augmentedGrammar[index]
                # Modify the input to get the token and lexema on the row
                semantic_action = semantic[index]
                # Delete the first and last character of the string
                analysis.append(get_rowr(stack, input, case_action, production, semantic_action))
                if production[-1] != '@':
                    # Save not terminal symbols to translate
                    back = []
                    for j in range(0, 2*(production[-1].count(' ')+1)):
                        top = stack.pop()
                        if isinstance(top, Token):
                            back.append(top)
                j = stack[-1]
                t = translate(production[0], semantic_action, back)
                stack.append(t)
                ir_a = get_action(TA, NT, TE, j, t.token)
                
                stack.append(ir_a)
        else:
            if case_action == 'AC':
                # print(stack, "\t\t", input, "\t\t", case_action)
                analysis.append(get_rowda(stack, input, case_action))
                accept = True
            else:
                symbols = find_error(TA[stack[-1]], TE)
                # print(stack, "\t\t", input, "\t\tError se esperaba: ", symbols)
                analysis.append(get_rowe(stack, input, symbols))
                al.Application.errores.append((1, symbols))
                error = True
    
    # Get data to interface
    program = gm.get_content(tokens_path)

    return analysis, program, tokens

def translate(production, semantic, stack):
    semantic = semantic[1:-1]
    semantic = semantic.split(" := ")
    semantic = semantic[1]
    
    # Looking for id and NOT terminal symbols on production
    while stack:
        i = stack.pop()
        semantic = semantic.replace('{'+i.token+'.value}', str(i.lexema))

    element = Token(production, semantic)

    return element
