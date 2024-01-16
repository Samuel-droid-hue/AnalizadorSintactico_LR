import re
import math

class TrieNode:
    def __init__(self, value=None):
        self.value = value
        self.children = {}

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert_rule(self, rule):
        node = self.root
        for symbol in rule:
            if symbol not in node.children:
                node.children[symbol] = TrieNode(symbol)
            node = node.children[symbol]

#Simbolos terminales y no terminales
def replace_word(text, old_word, new_word):
    pattern = re.compile(r'\b' + re.escape(old_word) + r'\b')
    return pattern.sub(new_word, text)

def siguiente(A):
        sig = []
        if A == SimboloInicial: #Si A es el simbolo inicial, agrega "$" a los siguientes de A
            sig.append("$")
        
        for regla in Reglas:    #analiza las reglas en busca del simbolo A
            B = regla[0]    #B tiene el simbolo no terminal que inicia la regla. en "F -> TE", F seria el simbolo B
            Beta=[]  #arreglo que va a contener los simbolos de Beta
            for i in range(len(regla)):    #indice que recorre la regla
                if i == 0:  #condicion que impide que se analice el simbolo que inicia la regla
                    continue
                if regla[i] == A:   #se ejecuta si detecta el simbolo A en la regla
                    j = i + 1   #indice que recorre los simbolos que estan después de A, es decir, los simbolos que tendrá Beta
                    if j < len(regla) and regla[j]:    #se ejecuta si existen simbolos que agregar a Beta (B -> alfa A beta)
                        while j < len(regla) and regla[j]:
                            Beta.append(regla[j])
                            j += 1
                        if Beta:
                            primerosBeta=obtenerPrimeros(Beta)
                            for k in primerosBeta:
                                if k != "@":
                                    sig.append(k)
                            if "@" in primerosBeta and B != A:  #se ejecuta si en los primeros de beta hay @, y B no es el simbolo A
                                sig = agregarSiguientesB(B, sig)
                    elif B != A:    #se ejecuta si la transicion es del tipo B -> alfa A y B no es el simbolo A
                        sig = agregarSiguientesB(B, sig)
        return sig  #retorna una arreglo con los siguientes de A

def obtenerPrimeros(arregloBeta):
    primerosB = []
    for cadena in arregloBeta:
        if cadena in TE:
            primerosB.append(cadena)
            return primerosB
        primerosAux = Primeros[NT.index(cadena)]
        for cadena2 in primerosAux:
            primerosB.append(cadena2)
    return primerosB

def agregarSiguientesB(B, sigArreglo):
    siguientesB = siguiente(B)  #obtiene los siguientes de B
    conjuntoSig = set(siguientesB)
    siguientesPrincipal = set(sigArreglo)
    siguientesPrincipal.update(conjuntoSig)
    siguienteActualizado = list(siguientesPrincipal)
    return siguienteActualizado

def reducirS(TE,Reglas,cadena):
    i=0
    k=0
    ind=0
    letra=97
    for s in TE:
        if len(str(TE[i]))!=1:
            cadena.append(TE[i])
            cadena.append(chr(letra))
            letra=letra+1
            ind=0
            for r in range (len(Reglas)):
                Reglas[r]=Reglas[r].replace(cadena[k*2],cadena[k*2+1])
                ind=ind+1
            k=k+1       
        i=i+1

def print_tree(node, depth=0):
    if node.value is not None:
        print("  " * depth+ node.value)
    for child in node.children.values():
        print_tree(child, depth + 1)

def buscarP(node,K=None,PrimeroD=None,value="",depth=0):
    for child in node.children.values():
        if(child.value!=node.value and 'A' <= str(node.value) <= 'Z' and depth!=2):
            buscarP(child,K,PrimeroD,value,depth+1)
            if(node.value!=None ):
                K.append(str(node.value)+"="+str(child.value))
                PrimeroD[node.value]=value+" "+child.value
                value=child.value

def PrimerosYsiguientes(TEaux,NTaux,Reglasaux):           
    # Crear un árbol Trie basado en las reglas dadas
    trie = Trie()
    global TE
    global NT 
    global Reglas
    TE=TEaux
    NT=NTaux
    Reglas=Reglasaux
    cadena=[]
    Siguientes=[]   #arreglo que contendra los siguientes de los simbolos no terminales
    global SimboloInicial
    SimboloInicial=NT[0]    #se guarda el simbolo inicial de la gramatica
    reducirS(TE,Reglas,cadena)
    for rule in Reglas:
        trie.insert_rule(rule)
    K=[]
    S=[]
    PrimeroD={}
    value=""
    contador=0
    buscarP(trie.root,K,PrimeroD,value)
    for r in range(len(K)):
        if  'A' <= K[r][2] <= 'Z':
            contador=contador+1
    PrimeroDAx={} 
    for i in K:
        PrimeroDAx[i[0]]=""
    for f in K:
        PrimeroD[f[0]]= PrimeroDAx[f[0]]+" "+f[2]
        PrimeroDAx[f[0]]=  PrimeroD[f[0]] 
    PrimeroD=PrimeroDAx       
    contador2=0
    k=0
    k1=contador
    while k <k1:
        contador2=0
        for r in range(len(K)):
            if  'A' <= K[r][2] <= 'Z':
                contador2=contador2+1    
            if  'A' <= K[r][2] <= 'Z' and contador2==contador:
                PrimeroD[K[r][0]]=PrimeroD[K[r][2]]
                contador=contador-1
        k=k+1   
    cadena2="" 
    for k in NT:
        for i in range(math.floor(len(cadena)/2)):
            cadena2=PrimeroD[k]
            cadena2=replace_word(cadena2,cadena[i*2+1], cadena[i*2])
            PrimeroD[k]=cadena2
    global Primeros
    Primeros=[]
    value=""
    for i in NT:
        value=PrimeroD[i]
        Primeros.append(value.split())
    NTAux=NT
    TEaux=TE
    auxPrimeros=Primeros
    for i in range(math.floor(len(cadena)/2)):
        for k in range(len(TE)):
            TE[k]=TE[k].replace(cadena[i*2],cadena[i*2+1])

    for i in range(math.floor(len(cadena)/2)):
        for k in range(len(Primeros)):
            for j in range(len(Primeros[k])):
                Primeros[k][j]=replace_word(Primeros[k][j],cadena[i*2+1], cadena[i*2])
    Siguientes=[]   #arreglo que contendra los siguientes de los simbolos no terminales
    SimboloInicial=NT[0]    #se guarda el simbolo inicial de la gramatica

    for SimboloNoTerminal in NT:
        Siguientes.append(siguiente(SimboloNoTerminal))
    for i in range(math.floor(len(cadena)/2)):
        for k in range(len(TE)):
            #TE[k]=TE[k].replace(cadena[i*2+1],cadena[i*2])
            TE[k]=replace_word(TE[k],cadena[i*2+1], cadena[i*2])
    for i in range(math.floor(len(cadena)/2)):
        for k in range(len(Siguientes)):
            for j in range(len(Siguientes[k])):
                Siguientes[k][j]=replace_word(Siguientes[k][j],cadena[i*2+1], cadena[i*2])
    return {'S':Siguientes,'P':Primeros}