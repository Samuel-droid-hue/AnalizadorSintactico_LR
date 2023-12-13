import utils.grammar as gm
import components.TablaAnalisis as ta

# Get data structure to token strip
def get_tokens(path):
    with open(path, "r") as file:
        content = file.readlines()

    # ONLY CONSIDER A SINGLE LINE OF FILE!
    tokens = []
    tokens = content[0].strip().split()

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
    
    return TA[i][j]

# ------------- ANALYZER ------------- #
def to_analyze(grammar_path, tokens_path):
    # Variables
    augmentedGrammar = gm.get_ASgrammar(grammar_path)
    stack = []
    input = []
    action = []
    error = False
    production = 0

    # Get the table and more values
    NT, TE, TA = ta.to_create(grammar_path)
    TE.append('$')
    input = get_tokens(tokens_path)
    input.append('$')
    
    # Algorithm
    stack.append(0)

    # Prints to show input
    print("Pila\t\tEntrada\t\tAccion")

    for iteration in range(14):
        case_action = get_action(TA, NT, TE, stack[-1], input[0])
        if case_action[0] == 'd':
            print(stack, "\t\t", input, "\t\t", case_action)
            stack.append(input[0])
            stack.append(int(case_action[-1]))
            input.pop(0)
        else:
            print(stack, "\t\t", input, "\t\t", case_action, " ", augmentedGrammar[int(case_action[-1])])
            # print(augmentedGrammar[int(case_action[-1])][-1].count(' ')+1)
            for j in range(0, 2*(augmentedGrammar[int(case_action[-1])][-1].count(' ')+1)):
                stack.pop()
            # Append not termial of the ruler select before <-
            j = stack[-1]
            stack.append(augmentedGrammar[int(case_action[-1])][0])
            ir_a = get_action(TA, NT, TE, j, augmentedGrammar[int(case_action[-1])][0])
            stack.append(ir_a)