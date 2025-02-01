import tkinter as tk
from tkinter import filedialog, scrolledtext
import ply.lex as lex

# Definir tokens y palabras reservadas
tokens = [
    'ENTERO', 'FLOTANTE', 'VARIABLE', 'OPERADOR', 'ASIGNACION',
    'COMPARACION', 'SEPARADOR', 'DELIMITADOR', 'COMILLAS', 'DOS_PUNTOS', 'PUNTO'
] + list({
    'if': 'IF', 'else': 'ELSE', 'while': 'WHILE', 'for': 'FOR',
    'func': 'FUN', 'escribir': 'ESCRIBIR', 'leer': 'LEER', 'val': 'VAL'
}.values())

palabras_reservadas = {
    'if': 'IF', 'else': 'ELSE', 'while': 'WHILE', 'for': 'FOR',
    'func': 'FUN', 'escribir': 'ESCRIBIR', 'leer': 'LEER', 'val': 'VAL'
}

def t_VARIABLE(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = palabras_reservadas.get(t.value, 'VARIABLE')  # Verifica si es palabra reservada
    return t

def t_ENTERO(t):
    r'\d+'
    return t

def t_FLOTANTE(t):
    r'\d+\.\d+'
    return t

def t_OPERADOR(t):
    r'[+\-*/]'
    return t

def t_ASIGNACION(t):
    r'='  
    return t

def t_COMPARACION(t):
    r'==|!=|<=|>=|<|>'
    return t

def t_SEPARADOR(t):
    r';'
    return t

def t_DELIMITADOR(t):
    r'[{}()]'
    return t

def t_COMILLAS(t):
    r'"|\''
    return t

def t_DOS_PUNTOS(t):
    r':'
    return t

def t_PUNTO(t):
    r'\.'
    return t

def t_ignore_WHITESPACE(t):
    r'\s+'
    pass

def t_error(t):
    errores.append(f"Error léxico: '{t.value[0]}' en la posición {t.lexpos}")
    t.lexer.skip(1)

lexer = lex.lex()
errores = []

def analizar_codigo():
    global errores
    errores = []
    codigo = entrada_texto.get("1.0", tk.END)
    lexer.input(codigo)
    tokens_detectados = []
    palabras_detectadas = []
    
    for tok in lexer:
        tokens_detectados.append(f"{tok.type}: {tok.value}")
        if tok.type in palabras_reservadas.values():
            palabras_detectadas.append(tok.value)
    
    salida_tokens.delete("1.0", tk.END)
    salida_tokens.insert(tk.END, "\n".join(tokens_detectados))
    
    salida_palabras.delete("1.0", tk.END)
    salida_palabras.insert(tk.END, "\n".join(palabras_detectadas))
    
    salida_errores.delete("1.0", tk.END)
    salida_errores.insert(tk.END, "\n".join(errores))

def cargar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if archivo:
        with open(archivo, "r") as f:
            entrada_texto.delete("1.0", tk.END)
            entrada_texto.insert(tk.END, f.read())

# Crear interfaz gráfica
root = tk.Tk()
root.title("Analizador Léxico")
root.geometry("700x600")

frame = tk.Frame(root)
frame.pack(pady=10)

btn_cargar = tk.Button(frame, text="Cargar Archivo", command=cargar_archivo)
btn_cargar.pack(side=tk.LEFT, padx=5)

btn_analizar = tk.Button(frame, text="Analizar", command=analizar_codigo)
btn_analizar.pack(side=tk.LEFT, padx=5)

entrada_texto = scrolledtext.ScrolledText(root, height=10)
entrada_texto.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

label_tokens = tk.Label(root, text="Tokens Detectados")
label_tokens.pack()
salida_tokens = scrolledtext.ScrolledText(root, height=5)
salida_tokens.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

label_palabras = tk.Label(root, text="Palabras Reservadas")
label_palabras.pack()
salida_palabras = scrolledtext.ScrolledText(root, height=3)
salida_palabras.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

label_errores = tk.Label(root, text="Errores")
label_errores.pack()
salida_errores = scrolledtext.ScrolledText(root, height=3)
salida_errores.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

root.mainloop()