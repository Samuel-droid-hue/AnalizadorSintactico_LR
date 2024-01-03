import networkx as nx# Librería para grafos
import matplotlib.pyplot as plt# Librería para grafos


def crearGRa(f):# Función para crear un gráfico de un autómata finito
    # Crear un gráfico dirigido
    G = nx.DiGraph()

    # Añadir nodos y aristas al gráfico
    for estado in f:
        G.add_node(estado.nombreestado)
        if estado.next1 is not None:
            G.add_edge(estado.nombreestado, estado.next1.nombreestado,label=estado.nombrenext1)
        if estado.next2 is not None:
            G.add_edge(estado.nombreestado, estado.next2.nombreestado,label=estado.nombrenext2)

    # Crear una lista de colores para los nodos
    node_colors = ['red' if estado.nombreestado == 0 else 'blue' for estado in f]

    # Dibujar el gráfico
    pos = nx.drawing.nx_agraph.graphviz_layout(G, prog='dot')  # Usar graphviz_layout para obtener un layout de árbol
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color='gray')
    #nx.draw(G, pos, with_labels=True, edge_color='gray')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'label'))
    plt.show()


# Función de clave personalizada para ordenar por atributo1
def clave_de_orden(obj):
    return obj.nombreestado


    
def infix_to_postfix(expression):# Función para convertir una expresión regular de infija a posfija
    def precedence(operator):
        if operator in {'|'}:
            return 1
        if operator in {'.'}:
            return 2
        elif operator in {'*', '?', '+'}:
            return 3
        return 0  # Consideramos que los paréntesis tienen la menor precedencia

    def is_higher_precedence(op1, op2):
        return precedence(op1) > precedence(op2)

    output = []
    stack = []

    for token in expression:
        if token.isalnum():
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # Deshacemos el paréntesis izquierdo
        else:
            while stack and stack[-1] != '(' and is_higher_precedence(stack[-1], token):
                output.append(stack.pop())
            stack.append(token)

    while stack:
        output.append(stack.pop())

    return output

class Estado:# Clase para representar un estado de un autómata finito
    def __init__(self):
        self.nombreestado=0
        self.nombrenext1=""
        self.nombrenext2=""
        self.next1 = None
        self.next2 = None
        self.opera = '/'  
    def __init__(self,n):
        self.nombreestado=n
        self.nombrenext1=""
        self.nombrenext2=""
        self.next1 = None
        self.next2 = None
        self.opera = '/' 
class afn:# Clase para tener apuntado el inicio y final de un autómata 
    def __init__(self):
        self.EstIni=Estado(None)
        self.EstFin=Estado(None)
def buscarOper(postfix_expression):# Función para buscar el operador con mayor precedencia
    i=0
    operator=['|','.','*','?','+']
    while len(postfix_expression)>1 and postfix_expression[i] not in operator:
            i=i+1
    
    return postfix_expression[i],i
def reordenar(lista):#funcio que aunque no reordena si le cambia el nombre a los estados a un numero +1
    k=0
    while k<len(lista):
        lista[k].nombreestado=lista[k].nombreestado+1
        k=k+1

    
def concatenacion(Tafn,i,expresion,lista):#funcion para concatenar (.)
    Afn=afn()
    if expresion[i-2]!='q@|':
        
        if Tafn==[] or expresion[i-1]!='q@|':
            A=Estado(0)
            B=Estado(1)
            C=Estado(2)
            A.nombrenext1=expresion[i-2]
            A.next1=B
            B.nombrenext1=expresion[i-1]
            B.next1=C
            Afn.EstIni=A
            Afn.EstFin=C
            aux=[]
            lista=aux
            lista.append(A)
            lista.append(B)
            lista.append(C)
            Tafn.append(Afn)
            return lista
            
            
            
        else:
            Afn=Tafn[len(Tafn)-1]
            A=Estado(0)
            A.nombrenext1=expresion[i-2]
            A.next1=Afn.EstIni
            Afn.EstIni=A
            reordenar(lista)
            lista.append(A)
            lista.sort(key=clave_de_orden)
            
    else:
        if expresion[i-2]=='q@|' and expresion[i-1]!='q@|':
            Afn=Tafn[len(Tafn)-1]
            A=Estado(len(lista))
            Afn.EstFin.nombrenext1=expresion[i-1]
            Afn.EstFin.next1=A
            Afn.EstFin=A
            lista.append(A)
        else:
            Afn=afn
            i=0
            Tafn[len(Tafn)-2].EstFin.next1=Tafn[len(Tafn)-1].EstIni.next1
            Tafn[len(Tafn)-2].EstFin.next2=Tafn[len(Tafn)-1].EstIni.next2
            #Tafn[len(Tafn)-2].EstFin.nombreestado=Tafn[len(Tafn)-1].EstIni.nombreestado
            Tafn[len(Tafn)-2].EstFin.nombrenext1=Tafn[len(Tafn)-1].EstIni.nombrenext1
            Tafn[len(Tafn)-2].EstFin.nombrenext2=Tafn[len(Tafn)-1].EstIni.nombrenext2
            #while lista[i]!=Tafn[len(Tafn)-1].EstIni:
            #    i=i+1
            #lista.pop(i)
            Tafn[len(Tafn)-2].EstFin=Tafn[len(Tafn)-1].EstFin
            Tafn[len(Tafn)-1]=Afn()
            Tafn.pop(len(Tafn)-1)
            
            
            
    return None
def union(Tafn,i,expresion,lista):#funcion para la union (|)
    Afn=afn()
    if expresion[i-2]!='q@|':
        
        if Tafn==[] or expresion[i-1]!='q@|':
            A=Estado(0)
            B=Estado(1)
            C=Estado(3)
            D=Estado(2)
            E=Estado(4)
            F=Estado(5)
            A.nombrenext1='ϵ'
            A.next1=B
            A.nombrenext2='ϵ'
            A.next2=C
            B.nombrenext1=expresion[i-2]
            B.next1=D
            C.nombrenext1=expresion[i-1]
            C.next1=E           
            D.nombrenext1='ϵ'
            D.next1=F
            E.nombrenext1='ϵ'
            E.next1=F
            
            
            Afn.EstIni=A
            Afn.EstFin=F
            aux=[]
            lista=aux
            lista.append(A)
            lista.append(B)
            lista.append(C)
            lista.append(D)
            lista.append(E)
            lista.append(F)
            Tafn.append(Afn)
            return lista
            
            
            
        else:
            Afn=Tafn[len(Tafn)-1]
            A=Estado(0)
            B=Estado(len(lista)+1)
            C=Estado(len(lista)+2)
            D=Estado(len(lista)+3) 
            A.nombrenext1='ϵ'
            A.next1=B
            A.nombrenext2='ϵ'
            A.next2=Afn.EstIni
            B.nombrenext1=expresion[i-2]
            B.next1=C
            C.nombrenext1='ϵ'
            C.next1=D
            Afn.EstFin.nombrenext1='ϵ'
            Afn.EstFin.next1=D
            Afn.EstIni=A
            Afn.EstFin=D
            reordenar(lista)                                                                                                 
            lista.append(A)
            lista.append(B)
            lista.append(C)
            lista.append(D)
            
    else:
        if expresion[i-2]=='q@|' and expresion[i-1]!='q@|':
            Afn=Tafn[len(Tafn)-1]
            A=Estado(0)
            B=Estado(len(lista)+1)
            C=Estado(len(lista)+2)
            D=Estado(len(lista)+3) 
            A.nombrenext1='ϵ'
            A.next1=B
            A.nombrenext2='ϵ'
            A.next2=Afn.EstIni
            B.nombrenext1=expresion[i-1]
            B.next1=C
            C.nombrenext1='ϵ'
            C.next1=D
            Afn.EstFin.nombrenext1='ϵ'
            Afn.EstFin.next1=D
            Afn.EstIni=A
            Afn.EstFin=D                                                                                                 
            lista.append(A)
            lista.append(B)
            lista.append(C)
            lista.append(D)
        else:
            Afn=afn
            A=Estado(0)
            B=Estado(len(lista)+1)
            reordenar(lista)
            A.nombrenext1='ϵ'
            A.next1=Tafn[len(Tafn)-2].EstIni
            A.nombrenext2='ϵ'
            A.next2=Tafn[len(Tafn)-1].EstIni
            Tafn[len(Tafn)-2].EstFin.next1=B
            Tafn[len(Tafn)-1].EstFin.next1=B
            Tafn[len(Tafn)-2].EstFin.nombrenext1='ϵ'
            Tafn[len(Tafn)-1].EstFin.nombrenext1='ϵ'
            Tafn[len(Tafn)-2].EstIni=A
            
            Tafn[len(Tafn)-2].EstFin=B
            Tafn[len(Tafn)-1]=Afn()
            Tafn.pop(len(Tafn)-1)
            lista.append(A)
            lista.append(B)
            lista.sort(key=clave_de_orden)
            
            #Tafn[len(Tafn)-2].EstFin.next1=Tafn[len(Tafn)-1].EstIni
    
    
        
    return None
def Ckleene(TAfn,i,expresion,lista):#funcion para la cerradura de kleene (*)
    Afn1=afn()
    
    if expresion[i-1]=='q@|':
        A=Estado(0)
        B=Estado(-1)
        reordenar(lista)
        Afn=TAfn[len(TAfn)-1]
        A.next1=Afn.EstIni
        A.nombrenext1='ϵ'
        Afn.EstFin.next2=Afn.EstIni
        Afn.EstFin.nombrenext2='ϵ'
        Afn.EstFin.nombrenext1='ϵ'
        Afn.EstFin.next1=B
        B.nombreestado=Afn.EstFin.nombreestado+1
        A.next2=B
        A.nombrenext2='ϵ'
        Afn.EstIni=A
        Afn.EstFin=B
        lista.append(A)
        lista.append(B)
    else:
        
        A=Estado(0)
        B=Estado(1)
        C=Estado(2)
        D=Estado(3)
        A.next1=B
        A.nombrenext1='ϵ'
        A.next2=D
        A.nombrenext2='ϵ'
        B.next1=C
        B.nombrenext1=expresion[i-1]
        C.next1=D
        C.nombrenext1='ϵ'
        C.next2=B
        C.nombrenext2='ϵ'
        Afn1.EstIni=A
        Afn1.EstFin=D
        aux=[]
        lista=aux
        lista.append(A)
        lista.append(B)
        lista.append(C)
        lista.append(D)
        TAfn.append(Afn1)
        return lista

def Copcional(TAfn,i,expresion,lista):#funcion para la cerradura de opcional (?)
    Afn1=afn()
    
    if expresion[i-1]=='q@|':
        A=Estado(0)
        B=Estado(-1)
        reordenar(lista)
        Afn=TAfn[len(TAfn)-1]
        A.next1=Afn.EstIni
        A.nombrenext1='ϵ'
        #Afn.EstFin.next2=Afn.EstIni
        #Afn.EstFin.nombrenext2='ϵ'
        Afn.EstFin.nombrenext1='ϵ'
        Afn.EstFin.next1=B
        B.nombreestado=Afn.EstFin.nombreestado+1
        A.next2=B
        A.nombrenext2='ϵ'
        Afn.EstIni=A
        Afn.EstFin=B
        lista.append(A)
        lista.append(B)
    else:
        
        A=Estado(0)
        B=Estado(1)
        C=Estado(2)
        D=Estado(3)
        A.next1=B
        A.nombrenext1='ϵ'
        A.next2=D
        A.nombrenext2='ϵ'
        B.next1=C
        B.nombrenext1=expresion[i-1]
        C.next1=D
        C.nombrenext1='ϵ'
        #C.next2=B
        #C.nombrenext2='ϵ'
        Afn1.EstIni=A
        Afn1.EstFin=D
        aux=[]
        lista=aux
        lista.append(A)
        lista.append(B)
        lista.append(C)
        lista.append(D)
        TAfn.append(Afn1)
        return lista

def Cpositiva(TAfn,i,expresion,lista):#funcion para la cerradura de positiva (+)
    Afn1=afn()
    
    if expresion[i-1]=='q@|':
        A=Estado(0)
        B=Estado(-1)
        reordenar(lista)
        Afn=TAfn[len(TAfn)-1]
        A.next1=Afn.EstIni
        A.nombrenext1='ϵ'
        Afn.EstFin.next2=Afn.EstIni
        Afn.EstFin.nombrenext2='ϵ'
        Afn.EstFin.nombrenext1='ϵ'
        Afn.EstFin.next1=B
        B.nombreestado=Afn.EstFin.nombreestado+1
        #A.next2=B
        #A.nombrenext2='ϵ'
        Afn.EstIni=A
        Afn.EstFin=B
        lista.append(A)
        lista.append(B)
        lista.sort(key=clave_de_orden)
    else:
        
        A=Estado(0)
        B=Estado(1)
        C=Estado(2)
        D=Estado(3)
        A.next1=B
        A.nombrenext1='ϵ'
        #A.next2=D
        #A.nombrenext2='ϵ'
        B.next1=C
        B.nombrenext1=expresion[i-1]
        C.next1=D
        C.nombrenext1='ϵ'
        C.next2=B
        C.nombrenext2='ϵ'
        Afn1.EstIni=A
        Afn1.EstFin=D
        aux=[]
        lista=aux
        lista.append(A)
        lista.append(B)
        lista.append(C)
        lista.append(D)
        TAfn.append(Afn1)
        return lista

def thonsonf(infix_expression):#funcion principal que recibe la expresion regular y devuelve el automata
    l=0
    Tafn=[]
    TafnAux={}
    listEs=[]
    operatorEcep=['*','?','+']
    #infix_expression1= lad(infix_expression)
    postfix_expression = infix_to_postfix(infix_expression)
    #print("expresion infija: "+infix_expression)
    #print("expresion infija: ",infix_expression)
    #print("expresion posfija: ",postfix_expression)
    while len(postfix_expression)>1:
        
        i=buscarOper(postfix_expression)
        switch_dict = {
        '|':union,
        '.':concatenacion,
        '*':Ckleene,
        '?':Copcional,
        '+':Cpositiva
        }
        
        # Obtener la función correspondiente al valor del caso
        selected_case = switch_dict.get(i[0], None)
        m=selected_case(Tafn,i[1],postfix_expression,listEs)
        if m!=None:
            l=l+1
            TafnAux[l]=m
            listEs=m
        # Ejecutar la función seleccionada
        #print(m)
        if postfix_expression[i[1]] not in operatorEcep:
            postfix_expression.pop(i[1]-2)
            postfix_expression.pop(i[1]-2)
            postfix_expression[i[1]-2]='q@|'
        else:   
            postfix_expression.pop(i[1]-1)
            postfix_expression[i[1]-1]='q@|'
        # Organizar la lista utilizando sort() con la función de clave
        i=buscarOper(postfix_expression)
        if i[0]=='q@|' and i[1]==0:
            listEs.sort(key=clave_de_orden)
            for i in range(len(listEs)):
                listEs[i].nombreestado=i
            #crearGRa(listEs) 
            "<---------------------------- esta funcion es para graficar el automata"
            return listEs
        listEs.sort(key=clave_de_orden)
        #print(postfix_expression)
        if postfix_expression[i[1]-1]=='q@|' and postfix_expression[i[1]-2]=='q@|' and i[0] not in operatorEcep:
            k=0
            listaaux=TafnAux[len(TafnAux)-1]
            suma=TafnAux[len(TafnAux)-1][len(TafnAux[len(TafnAux)-1])-1].nombreestado
            while k<len(TafnAux[len(TafnAux)]):
                TafnAux[len(TafnAux)][k].nombreestado= suma+TafnAux[len(TafnAux)][k].nombreestado+1
                if k!=0 or i[0]=='|':
                    listaaux.append(TafnAux[len(TafnAux)][k])
                k=k+1
            aux=[]
            TafnAux[len(TafnAux)]=aux
            TafnAux.pop(len(TafnAux))
            listEs=TafnAux[len(TafnAux)]
            l=l-1
        else:    
            listEs.sort(key=clave_de_orden)
            if ((postfix_expression.count('q@|')<2 and postfix_expression[i[1]-1]=='q@|') or  postfix_expression[i[1]-2]!='q@|') or (postfix_expression[i[1]-2]=='q@|' and  postfix_expression[i[1]-1]!='q@|') or (i[0] in operatorEcep):
                TafnAux[l]=listEs
            else:
                l=l+1
                aux=[]
                listEs=aux
                TafnAux[l]=listEs  
def creartabla(alfabeto,expresion):
    tabla=[]
    
    Af=thonsonf(expresion)
    for i in Af:
        g={}
        for a in alfabeto:
            g[a]=""
        if i.nombrenext1!='':
            g[i.nombrenext1]=str(g[i.nombrenext1])+' '+str(i.next1.nombreestado)
        if i.nombrenext2!='':   
            g[i.nombrenext2]=str(g[i.nombrenext2])+' '+str(i.next2.nombreestado)
        tabla.append(g)
    return tabla                   
"""1. lo siguiente es para probar el codigo usando el alfabeto correcto para cada expresion regular 
2. uso q@| para representar el vacio que esa parte de la expresion regular ya a sido procesada y que ya tiene un automata finito, se puede ver como un subautomata
3.la entrada de la expresion regular debe ser una lista de caracteres, no una cadena de caracteres
4. el simbolo de la concatenacion es el punto (.) por lo que si se requere usar el punto como simbolo de la expresion regular se debe usar p en su lugar o cualquier otro simbolo que no este en el alfabeto de los operadores
5.al alfabeto de los operadores es (* + ? | .) y el simbolo de vacio es ϵ
6.la funcion principal es crear tabla que recibe el alfabeto y la expresion regular y devuelve la tabla de transiciones usando un diccionario por cada estado
7. la funcion thonsonf recibe la expresion regular y devuelve el automata finito


"""    

#expression = ['(','(','a','|','b','.','c',')','*','.','d','*',')','|','e','|','(','f','.','g',')']
#expression = ['(','a','|','b',')','*','.','a','.','b','.','b']
#expression=['(','i','.','f',')','|','(','letra','.','(','letra','|','digito',')','*',')']
expression=['(','i','.','f',')','|','(','f','.','o','.','r',')','|','(','letra','.','(','letra','|','digito',')','*',')','|','(','digito','+','.','(','p','.','digito','+',')','?',')']
"en la expresion anterior use p para representar el punto y no confundirlo con el operador de concatenacion"


#alfabeto=['i','f','letra','digito']
#alfabeto=list(alfabeto)
alfabeto=['i','f','o','r','letra','digito','p','ϵ']

"el alfabeto debe contener el simbolo vacio, es obligatorio usar el simbolo ϵ para representar el vacio"
tabla=creartabla(alfabeto,expression)
#print(tabla)
#tabla=[]
#i=0

