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
def action(TA, NT, TE, s, a):
    # Get i index
    i = s
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
    tokenStrip = get_tokens(tokens_path)
    tokenStrip.append('$')
    stack = [0]
    input = []

    # Get the table and more
    NT, TE, TA = ta.to_create("tests/pastor_grammar.txt")
    TE.append('$')

    print(action(TA, NT, TE, 0, 'float'))