import utils.grammar as gm

# Get data structure to token strip
def get_tokens(path):
    with open(path, "r") as file:
        content = file.readlines()

    # ONLY CONSIDER A SINGLE LINE OF FILE!
    tokens = []
    tokens = content[0].strip().split()

    return tokens

# ------------- ANALYZER ------------- #
def to_analyze(grammar_path, tokens_path):
    # Variables
    augmentedGrammar = gm.get_grammar(grammar_path)
    tokenStrip = get_tokens(tokens_path)
    tokenStrip.append('$')
    stack = [0]
    input = []

    print(augmentedGrammar)
    print(tokenStrip)
    print(stack)