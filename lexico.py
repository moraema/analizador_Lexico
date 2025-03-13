import ply.lex as lex

# Lista de tokens
tokens = [
    'ENTERO',  
    'FLOTANTE', 
    'VARIABLE',
    'OPERADOR',  
    'ASIGNACION',
    'COMPARACION', 
    'SEPARADOR',  
    'DELIMITADOR_L',  
    'DELIMITADOR_R',  
    'COMILLAS', 
    'LOGICO',
    'DOS_PUNTOS'    
]

# Palabras reservadas
palabras_reservadas = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'escribir': 'ESCRIBIR',
    'leer': 'LEER',
    'val': 'VAL',
    'init': 'INIT',
    'func': 'FUNC'
}

# Agregar palabras reservadas a tokens
tokens += list(palabras_reservadas.values())

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Definición de tokens simples
t_OPERADOR = r'\+|\-|\*|\/'
t_COMPARACION = r'<=|>=|==|!=|<|>'
t_ASIGNACION = r'='
t_SEPARADOR = r';'
t_DELIMITADOR_L = r'\{'
t_DELIMITADOR_R = r'\}'
t_LOGICO = r'&&|\|\||!'
t_DOS_PUNTOS = r'\:'

# Definición de tokens con funciones
def t_FLOTANTE(t):
    r'\d+\.\d+' 
    t.value = float(t.value)
    return t

def t_ENTERO(t):
    r'\d+' 
    t.value = int(t.value)
    return t

def t_VARIABLE(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = palabras_reservadas.get(t.value, 'VARIABLE')  # Prioriza palabras reservadas
    return t

def t_COMILLAS(t):
    r'\"(.*?)\"'
    t.value = t.value[1:-1]  
    return t

def t_COMENTARIOS(t):
    r'/\*.*?\*/|\/\/.*'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}' en la línea {t.lexer.lineno}")
    t.lexer.skip(1)

# Construcción del analizador léxico
analizador = lex.lex()


# Función para realizar el análisis léxico
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