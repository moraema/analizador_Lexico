import ply.lex as lex
import ply.yacc as yacc


tokens = [
    'INCREMENTO', 'DECREMENTO', 'ENTERO', 'FLOTANTE', 'VARIABLE', 'ASIGNACION', 'SEPARADOR', 'DELIMITADOR_L',
    'DELIMITADOR_R', 'COMILLAS', 'LOGICO', 'DOS_PUNTOS', 'T_PARENTESIS_L', 'T_PARENTESIS_R',
    'COMPARACION_LESS', 'COMPARACION_GREATER', 'COMPARACION_LESS_EQ', 'COMPARACION_GREATER_EQ',
    'COMPARACION_EQ', 'COMPARACION_NEQ', 'OPERADOR'
]


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


tokens += list(palabras_reservadas.values())


t_ignore = ' \t'


t_INCREMENTO = r'\+\+'
t_DECREMENTO = r'--'


t_COMPARACION_GREATER = r'>'
t_COMPARACION_LESS = r'<'
t_COMPARACION_LESS_EQ = r'<='
t_COMPARACION_GREATER_EQ = r'>='
t_COMPARACION_EQ = r'=='
t_COMPARACION_NEQ = r'!='



t_ASIGNACION = r'='
t_SEPARADOR = r';'
t_DELIMITADOR_L = r'\{'
t_DELIMITADOR_R = r'\}'
t_LOGICO = r'&&|\|\||!'
t_DOS_PUNTOS = r'\:'
t_T_PARENTESIS_L = r'\('
t_T_PARENTESIS_R = r'\)'
t_OPERADOR = r'\+|\-|\*|\/'
t_LEER = r'leer'


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
    t.type = palabras_reservadas.get(t.value, 'VARIABLE')  
    return t

def t_COMILLAS(t):
    r'\"(.*?)\"'
    t.value = t.value[1:-1] 
    return t

def t_COMENTARIOS(t):
    r'(/\*([^*]|\*[^/])*\*/)|(//[^\n]*)'
    pass 

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}' en la línea {t.lexer.lineno}")
    t.lexer.skip(1)


analizador = lex.lex()


def analisis(input_code):
    errores = []
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