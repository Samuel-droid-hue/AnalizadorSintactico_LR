import re

terminals = []
not_terminals = []
gramatical_rules = []

def coleccion_canonica(TE, NT, rules):
    global terminals, not_terminals

    terminals = NT

    not_terminals = TE

    # Parse to data structure rules
    create_rules(rules)
    
    # -- Step 1
    states = []
    final = []

    # Output
    output_states = []
    output_ir_a_NT = []
    output_ir_a_TE = []

    i0 = move_dot_together([gramatical_rules[0]])
    states.append(full_lock(i0))
    final.append(status_format(states[0]))
    output_states.append(output_format(states[0]))

    # Variable to state current and new
    icurrent = 0
    inew = 0

    for s in states:
        while s:
            w, matches = search_after_point(s)

            if isinstance(matches, list):
                matches = move_dot_together(matches)
                cerradura = full_lock(matches)
                if search_matches(final, status_format(cerradura)) is False and cerradura and w != '.':
                    final.append(status_format(cerradura))
                    states.append(cerradura)
                    # output_states.append(status_format(cerradura))
                    output_states.append(output_format(cerradura))
                    inew += 1
                    if w in terminals:
                        output_ir_a_TE.append([icurrent, w, inew])
                    elif w in not_terminals:
                        output_ir_a_NT.append([icurrent, w, inew])
                    # print(f"Ir_a (I{icurrent}, {w}) = Cerradura: ({status_format(matches)} )")
                    # print(f"I{inew} = : {status_format(cerradura)}\n")
                elif search_matches(final, status_format(cerradura))is True:
                    # print(f"Ir_a (I{icurrent}, {w}) = Cerradura: ({status_format(matches)} )")
                    # print(f"I{final.index(status_format(cerradura))} = : {status_format(cerradura)}\n")
                    if w in terminals:
                        output_ir_a_TE.append([icurrent, w, final.index(status_format(cerradura))])
                    elif w in not_terminals:
                        output_ir_a_NT.append([icurrent, w, final.index(status_format(cerradura))])

            else:
                #final.append(matches)
                if matches == "Aceptacion":
                    #print(f"Ir_a (I{icurrent}, {w}) = {matches}\n")
                    output_ir_a_TE.append([icurrent, w, -1])
                    
        icurrent += 1

    gramatical_rules.clear()
    
    return output_ir_a_NT, output_ir_a_TE, output_states

def create_rules(rules):
    aux_s = []
    aux_list = []
    symbol = ""
    
    # First rule type $
    gramatical_rules.append([rules[0][0]+"'", [rules[0][0], "$"]])

    for i in rules:
        aux_s = i.split(" ")
        symbol = aux_s.pop(0)
        for j in aux_s:
            aux_list.append(j)
        gramatical_rules.append([symbol, aux_list])
        aux_list = []

# ---------------------- FORMAT ---------------------------
# Format to an only grammar element
def element_format(element):
    symbol = element[0]
    list_production = element[1]
    production = ""

    for i in list_production:
        production += i

    return f"[ {symbol} -> {production} ]"

# Format to all one state
def status_format(state):
    if isinstance(state, list):
        format = ""

        for element in state:
            format += element_format(element) + " "
    
        return "{ " + format + "}"
    else:
        return state

# Output format
def ouput_item_format(item):
    element = ""
    element += item[0]

    sublist = item[-1]
    for i in sublist:
        element += " " + i

    return element

def output_format(state):
    format = []
    
    for element in state:
        format.append(ouput_item_format(element))
    
    return format
# ---------------------------------------------------------

# ------------------------ POINT --------------------------
# Only changes position point
def move_dot(derivation):
    if '.' not in derivation:
        derivation.insert(0, '.')
    elif derivation.index('.') == len(derivation) - 1:
        derivation = None
    else:
        position = derivation.index('.')
        derivation.remove('.')
        position += 1
        derivation.insert(position, '.')
        
    return derivation

# Changes position point into a set
# Recive a list of lists of items
def move_dot_together(element):
    for i in range(len(element)):
        element[i][-1] = move_dot(element[i][-1])
        if element[i][-1] == None:
            element.pop(i)
    
    return element
# ---------------------------------------------------------

# ---------------------- SEARCH ---------------------------
# Search into productions by not terminal symbol
def search_productions(not_terminal):
    # Importante : Debera borra la siguiente linea yo solo la coloque para tratar las variables como globales en este caso equivalencia al atributo del objeto
    global gramatical_rules

    result = []

    for i in range(len(gramatical_rules)):
        if gramatical_rules[i][0] == not_terminal:
            result.append(gramatical_rules[i])
    
    return result

# To determinate if there are same states
def search_matches(list, element):
    if element in list:
        return True
    else:
        return False

# Recieve a state
def search_after_point(state):
    result = []
    element = after_point(state[0])
    result.append(state.pop(0))
    if element == "$":
        return element, "Aceptacion"
    else:
        
        while state and after_point(state[0]) == element:
            result.append(state.pop(0))

        return element, result

# Seach element after the point
def after_point(production):
        index = production[-1].index('.')
        if index < len(production[-1]) - 1:
            return production[-1][index+1]
        else:
            return production[-1][index]
# ---------------------------------------------------------

# ---------------------- LOCK -----------------------------
# Calculate lock of an only element
def element_lock(element):
    # Importante : Debera borra la siguiente linea yo solo la coloque para tratar las variables como globales en este caso equivalencia al atributo del objeto
    global not_terminals

    # p : point's position
    # c : current symbol to search a
    # n : next symbol to search e

    result = [element]
    queue = []
    n = ""

    p = result[0][-1].index('.')
    if p < len(result[0][-1])-1:
        n = result[0][-1][p+1]
        if n in not_terminals:
            queue = move_dot_together(search_productions(n))

    # Saber el estado actual
    c = n
    # Mientras la pila de operaciones no este vacia
    while queue:
        p = queue[0][-1].index('.')
        # Si el punto no esta al final
        if p < len(queue[0][-1]):
            n = queue[0][-1][p+1]
            # Si el elemento siguiente es no terminal y es igual que actual
            # Solo apila no calcules
            if n in not_terminals and n == c:
                # Busca si el resultado existe o no 
                if search_matches(result, queue[0]) is False:
                    result.append(queue.pop(0))
            # Si el elemento siguiente es un terminal
            elif n in terminals:
                if search_matches(result, queue[0]) is False:
                    result.append(queue.pop(0))
            # Si el elemento siguiente es diferente del actual y es no terminal
            # Calcula de nuevo y apila
            elif n != c and n in not_terminals:
                if search_matches(result, queue[0]) is False:
                    result.append(queue.pop(0))
                ###########################################################
                # HERE IS THE ERROR!!!!
                queue_aux = move_dot_together(search_productions(n))
                for item in queue_aux:
                    queue.append(item)
                # queue.append(move_dot_together(search_productions(n)))
                # queue = move_dot_together(search_productions(n))
                ###########################################################
        
            # Caso para el epsilon donde solamente se calcula el L -> .
            elif n == '@':
                aux = queue.pop(0)
                aux[-1] = ['.']
                if search_matches(result, aux) is False:
                    result.append(aux)

        # Actualiza el simbolo actual
        c = n

    return result

def full_lock(list):
    global gramatical_rules

    new_state = []
    back = None

    for element in list:
        back = restore_grammar()
        new_state += element_lock(element)
        gramatical_rules = back

    return new_state
# ---------------------------------------------------------

# ------------------- AUXILIARY ---------------------------
def restore_grammar():
    gram_original=[]
    gram_original2=[]
    # Recorre gramatical rules
    # RECUERDA AGREGAR GRAMATICAL RULES SELF
    for r in range(len(gramatical_rules)):
        gram_original2=[]
        # 2 por que son dos elementos
        for k in range(2):
            # RECUERDA AGREGAR GRAMATICAL RULES SELF
            for i in range(len(gramatical_rules[r][k])):
                if k!=0:
                    # RECUERDA AGREGAR GRAMATICAL RULES SELF
                    gram_original2.append(gramatical_rules[r][k][i]) 
                else:
                    if i!=1 and k!=1:
                        # RECUERDA AGREGAR GRAMATICAL RULES SELF
                        gram_original2.append(gramatical_rules[r][k])
        gram_original.append(gram_original2) 
    
    original=[]
    for i in range(len(gram_original)):
        aux=""
        aux2=[]
        original_aux=[]
        for k in range(len(gram_original[i])):
            if k==0:
                aux=gram_original[i][k]
            else:
                aux2.append(gram_original[i][k])
        original_aux.append(aux)
        original_aux.append(aux2)
        original.append(original_aux)

    return original
# -----------------------------------------------------------