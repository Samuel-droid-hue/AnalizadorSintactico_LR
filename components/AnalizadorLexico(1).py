from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

import string
import re
from collections import OrderedDict

class Application:
    def __init__(self, title):
        # Variables de la aplicacion
        self.file = ""

        # Variable especificas de la aplicacion
        self.total = []
        self.conjunto_sin_duplicados = []
        self.tira_tokens = []
        self.errores = []
        
        self.analyzed = False

        # Variable de las ventanas en ejecucion
        self.sub_tokens = None
        self.sub_symbols = None
        self.sub_errors = None

        # Creacion de la ventana
        self.root = Tk()
        self.root.geometry("600x450+470+200")
        self.root.title(title)
        self.root.config(bg="#E7E7B0")
        self.root.resizable(False, False)

        # Contenedor para los botones
        self.frame = Frame(self.root, background="#FFFFDD", relief=SUNKEN, padx=20, pady=20)
        self.frame.pack(padx=20, pady=20)

        boton_open = Button(self.frame, text="Abrir Archivo", background="#C0EFD2", command=self.open_file)
        boton_open.grid(row=0, column=0, padx=10, pady=10)

        # Crear aqui mas botones
        # Posicionar los botones solo por filas y columnas!

        # Creacion del boton obtener resultado
        boton_get = Button(self.frame, text="Analizar", background="#C0EFD2", command=self.get_result)
        boton_get.grid(row=0, column=1, padx=10, pady=10)

        boton_tokens = Button(self.frame, text="Tira Tokens", background="#C0EFD2", command=self.show_tokens)
        boton_tokens.grid(row=0, column=2, padx=10, pady=10)

        boton_symbols = Button(self.frame, text="Tabla Simbolos", background="#C0EFD2", command=self.show_symbols)
        boton_symbols.grid(row=0, column=3, padx=10, pady=10)

        boton_errors = Button(self.frame, text="Tabla Errores", background="#C0EFD2", command=self.show_errors)
        boton_errors.grid(row=0, column=4, padx=10, pady=10)

        # Estilo para la tabla
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25, fieldbackground="#D3D3D3")
        style.map('Treeview', background=[('selected', '#E9D6AF')])
        style.map('Treeview', foreground=[('selected', 'black')])
    
    def open_file(self):
        file = filedialog.askopenfilename(filetype=[("Archivos de texto", "*.txt")])
        
        if file:
            self.file = file
            messagebox.showinfo("Analizador Lexico", "Archivo seleccionado correctamente!")
        else:
            messagebox.showerror("Analizador Lexico", "No se selecciono ningun archivo!")

    # Funcion MODIFICABLE
    # Insertar aqui su logica de BACKEND!
    def get_result(self):
        if self.file:
        
            analizador= AnalizadorLexico()
            caracteres_separadores = analizador.caracteres
            letra= string.ascii_letters + string.digits + '.' + "'" + "_" +'['+']'+'!'
            self.errores = analizador.encontrar_error(self.file,caracteres_separadores,letra)
            self.tira_tokens,self.total,palabras_id= analizador.tokenizar(self.file)

            self.conjunto_sin_duplicados = OrderedDict()

            # Iteración sobre la lista palabras_id_unicas para crear un conjunto sin duplicados:

            for elemento in palabras_id:
                self.conjunto_sin_duplicados[elemento] = None  # Usamos el objeto None como marcador
                
            self.analyzed = True
            messagebox.showinfo("Analizador Lexico", "El archivo se analizo con exito!")
        else:
            self.analyzed = False
            messagebox.showerror("Analizador Lexico", "No ha seleccionado un archivo!")
        

    def show_tokens(self):
        if self.analyzed:
            if self.sub_tokens is None or not self.sub_tokens.winfo_exists():
                sub = Toplevel(self.root)
                sub.title("Tira De Tokens")
                sub.geometry("+100+50")

                table = ttk.Treeview(sub, columns=("# Linea", "Lexema", "Token"), show="headings")
                
                # Configuracion de las cabeceras
                table.heading("# Linea", text="# Linea")
                table.heading("Lexema", text="Lexema")
                table.heading("Token", text="Token")

                # Configuracion de las columnas
                table.column("# Linea", width=100, anchor="center")
                table.column("Lexema", width=100, anchor="center")
                table.column("Token", width=100, anchor="center")
                
                for elemento in self.total:
                    partes= elemento.split(',')
                    if len(partes) >= 3:
                        linea = partes[0].strip()
                        lexema = partes[1].strip()
                        token = partes[2].strip()

                        # Insertar los valores en la tabla
                        table.insert("", END, values=(linea, lexema, token))

                table.pack()
                self.sub_tokens = sub
            else:
                self.sub_tokens.lift()
        else:
            messagebox.showerror("Analizador Lexico", "No ha analizado el archivo!")
    
    def show_symbols(self):
        if self.analyzed:
            if self.sub_symbols is None or not self.sub_symbols.winfo_exists():
                sub = Toplevel(self.root)
                sub.title("Tira De Simbolos")
                sub.geometry("+100+400")

                table = ttk.Treeview(sub, columns=("ID", "Valor", "Funcion"), show="headings")

                # Configuracion de las cabeceras
                table.heading("ID", text="ID")
                table.heading("Valor", text="Valor")
                table.heading("Funcion", text="Funcion")

                # Configuracion de las columnas
                table.column("ID", width=100, anchor="center")
                table.column("Valor", width=100, anchor="center")
                table.column("Funcion", width=100, anchor="center")

                for elemento in self.conjunto_sin_duplicados:
                    table.insert("", END, values=elemento)

                table.pack()
                self.sub_symbols = sub  
            else:
                self.sub_symbols.lift()
        else:
            messagebox.showerror("Analizador Lexico", "No ha analizado el archivo!")
    
    def show_errors(self):
        if self.analyzed:
            if self.sub_errors is None or not self.sub_errors.winfo_exists():
                sub = Toplevel(self.root)
                sub.title("Tira De Errores")
                sub.geometry("+1150+50")

                table = ttk.Treeview(sub, columns=("# Linea", "Valor", "Funcion"), show="headings")

                # Configuracion de las cabeceras
                table.heading("# Linea", text="# Linea")
                table.heading("Valor", text="Valor")
                table.heading("Funcion", text="Funcion")

                # Configuracion de las columnas
                table.column("# Linea", width=100, anchor="center")
                table.column("Valor", width=100, anchor="center")
                table.column("Funcion", width=100, anchor="center")

                for elemento in self.errores:
                    table.insert("", END, values=elemento)

                table.pack()
                self.sub_errors = sub
            else:
                self.sub_errors.lift() 
        else:
            messagebox.showerror("Analizador Lexico", "No ha analizado el archivo!")

class AnalizadorLexico:
    def __init__(self):
        self.reservadas = {
            'printf', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
            'double', 'else', 'enum', 'main', 'float', 'for', 'goto', 'if','bool',
            'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof', 'static',
            'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while',
            'auto','extern','scanf','pow','malloc','free','strlen','strcpy','fopen','fclose'
        }
        self.caracteres = {
            '\n': 'salto de línea', '\t': 'tabulación', '(': 'paréntesis abierto', '{': 'llave abierta',
            ',': 'coma', '<': 'menor que', '>': 'mayor que', '=': 'igual', '+': 'más', '-': 'menos',
            '*': 'asterisco', ';': 'punto y coma', ' ': 'espacio', '}': 'llave cerrada',')': 'paréntesis cerrado',
            '"': 'comillas dobles', '/': 'barra', '&': 'y', '%': 'porcentaje', '|':'barra',':':'doblep'
            
        }
    def caracter_separador(self,caracter):
        return caracter in self.caracteres

    lin_num = 1

    def tokenizar(self, codigo):
        reglas = [
            ('RESERVADO', '|'.join(re.escape(word) for word in self.reservadas)),
            ('PARENTA', r'\('),        # (
            ('PARENTC', r'\)'),        # )
            ('LLAVEA', r'\{'),          # {
            ('LLAVEC', r'\}'),          # }
            ('COMA', r','),            # ,
            ('PCOMA', r';'),           # ;
            ('EQ', r'=='),              # ==
            ('NE', r'!='),              # !=
            ('LE', r'<='),              # <=
            ('GE', r'>='),              # >=
            ('OR', r'\|\|'),            # ||
            ('AND', r'&&'),             # &&
            ('AMPER', r'&'),             # &
            ('PORCENT', r'%'),             # %
            ('TWOP', r':'),             # :
            ('COMEN_START', r'/\*'),  # Inicio de comentario /* 
            ('COMEN_END', r'\*/'),    # Fin de comentario */
            ('COMENT',  r'\/\/.*'),             # &&
            ('literalCad', r'"([^"\\]*(\\.[^"\\]*)*)"'),
            ('literalCar', r"'([^'\\]*(\\.[^'\\]*)*)'"),
            ('ARRAY',r'[a-zA-Z1-9_]\w*\[\d+\]'),        #arreglos
            ('ARRAYAP',r'\*[a-zA-Z1-9]*.\[[1-9]*\]'),        #apuntadores arreglos
            ('APUNT',r'\*[a-zA-Z_]\w*'),        #apuntadores
            ('CORCHETEA', r'\['),           # [
            ('CORCHETEC', r'\]'),           # ]
            ('IGUAL', r'\='),            # =
            ('MAYOR', r'<'),               # <
            ('MENOR', r'>'),               # >
            ('iNCRE', r'\+\+'),            # ++
            ('DECRE', r'--'),            # -
            ('SUMA', r'\+'),            # +
            ('RESTA', r'-'),            # -
            ('MULT', r'\*'),            # *
            ('DIV', r'\/'),             # / 
            ('id', r'[a-zA-Z]\w*'),     # IDENTIFICADORES
            ('nfloat', r'\d(\d)*\.\d(\d)*'),   # FLOAT
            ('nint', r'\d(\d)*'),          # INT
            ('NEWLINE', r'\n'),         # NUEVA LINEA
            ('SKIP', r'[ \t]+'),        # SPACIO Y TABS
            ('MISMATCH', r'.'),         # OTRO CARACTER
        ]
        tokens_unidos = '|'.join('(?P<%s>%s)' % x for x in reglas)

        # Listas de salida del programa
        simbolos=[]
        token = []
        lexema = []
        fila = []
        total = []
        tira_token = ""
        in_comentario = False 
        with open(codigo, 'r') as file:
            codigo = file.read()
        # Analiza el código para encontrar los lexemas y sus respectivos Tokens
        for m in re.finditer(tokens_unidos, codigo):
            token_tipo = m.lastgroup
            token_lexema = m.group(token_tipo)

            
            if token_tipo == 'NEWLINE':
                self.lin_num += 1
            elif token_tipo == 'COMEN_START':
                in_comentario = True
                continue  # Salta al siguiente token sin imprimir nada
            elif token_tipo == 'COMEN_END':
                in_comentario = False
                continue  # Salta al siguiente token sin imprimir nada
            elif in_comentario:
                continue
            elif token_tipo == 'COMENT':
                continue
            elif token_tipo == 'SKIP':
                continue
            elif token_tipo == 'MISMATCH':
                raise RuntimeError('%r unexpected on line %d' % (token_lexema, self.lin_num))
            else:

                    token.append(token_tipo)
                    lexema.append(token_lexema)
                    fila.append(self.lin_num)
                    
                    # Imprimir información sobre un Token
                    if token_tipo != 'id'and token_tipo != 'literalCad' and token_tipo != 'literalCar' and token_tipo != 'nint'and token_tipo != 'nfloat':
                        if token_tipo == 'ARRAY' or token_tipo == 'ARRAYAP' or token_tipo == 'APUNT':
                            total += ["{2}  , {1}  , {0} ".format("id", token_lexema, self.lin_num)]
                            tira_token += "id "
                        else:
                            total += ["{2} , {1}  , {1} ".format(token_tipo, token_lexema, self.lin_num)]
                            tira_token += token_lexema +" "
                    else:
                        total += ["{2} , {1}  , {0} ".format(token_tipo, token_lexema, self.lin_num)]
                        tira_token += token_tipo + " "
                    if token_tipo == 'id' or token_tipo == 'ARRAY' or token_tipo == 'ARRAYAP' or token_tipo == 'APUNT':
                        simbolos.append((token_lexema,(0),(0)))
        return tira_token, total, simbolos 

    def encontrar_error(self, archivo_path, caracteres_separadores, letra):
        lineas_validas = []
        errores = []
        num_linea = 1  # Número de línea inicial
        with open(archivo_path, 'r') as archivo:
            for numero_linea, linea in enumerate(archivo, start=1):
                nueva_linea = ''.join(char if char in caracteres_separadores or char in letra else (errores.append((num_linea, char,char)), ' ')[1] for char in linea)
                lineas_validas.append(nueva_linea)
                num_linea += 1
        # Sobrescribe el archivo con las líneas válidas
        with open(archivo_path, 'w') as archivo:
            archivo.writelines(lineas_validas)

        return errores

if __name__ == "__main__":
    app = Application("Analizador Lexico")
    app.root.mainloop()

