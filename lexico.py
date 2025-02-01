import ply.lex as lex

tokens_principales = [
    'ENTERO',
    'FLOTANTE', 
    'VARIABLE',
    'OPERADOR', 
    'ASIGNACION', 
    'COMPARACION', 
    'SEPARADOR',
    'DELIMITADOR', 
    'COMILLAS', 
    'DOS_PUNTOS', 
    'PUNTO',
    'LOGICO'
]

palabras_reservadas = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'escribir': 'ESCRIBIR',
    'leer': 'LEER',
    'val': 'VAL'
}

tokens = list(palabras_reservadas.values()) + tokens_principales

# Ignorar los espacios
t_ignore = ' \t,'

# Definición de las expresiones regulares 
t_OPERADOR = r'\+|\-|\*|\/'
t_ASIGNACION = r'='
t_COMPARACION = r'>|<|>=|<=|==|!='
t_SEPARADOR = r';'
t_DELIMITADOR = r'\(|\)|\{|\}'  
t_DOS_PUNTOS = r'\:'
t_PUNTO = r'\.'
t_LOGICO = r'&&|\|\||!'


# Números decimales
def t_FLOTANTE(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Números enteros
def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Variables
def t_VARIABLE(t):
    r'[a-zA-Z_][a-zA-Z_]*'
    t.type = palabras_reservadas.get(t.value, 'VARIABLE')
    return t

def t_COMILLAS(t):
    r'\"(.*?)\"'
    t.value = t.value[1:-1]
    return t

def t_COMENTARIOS(t):
    r'/\*.*?\*/'
    pass

# Manejar nuevas líneas
def t_new_line(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejar errores
def t_error(t):
    errores.append(f"Caracter ilegal '{t.value[0]}' en la línea {t.lexer.lineno}")
    t.lexer.skip(1)

def analisis(input_code):
    global errores
    errores = []

    analizador = lex.lex()
    analizador.input(input_code)

    tokens_generados = []
    palabras_reservadas_detectadas = []



    while True:
        tok = analizador.token()
        if not tok:
            break
        tokens_str = f"LexToken({tok.type}, '{tok.value}', {tok.lineno}, {tok.lexpos})"

        if tok.type in palabras_reservadas.values():
            palabras_reservadas_detectadas.append(tokens_str)
        else:
            tokens_generados.append(tokens_str)

    return tokens_generados, palabras_reservadas_detectadas, errores