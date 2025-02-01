import ply.lex as lex

# Definición de los tokens
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


def t_new_line(t):
    r'\n+' 
    t.lexer.lineno += len(t.value)


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
    pila = []  
    esperando_igual = False  
    esperando_val_variable = False  
    esperando_igual_val = False  
    esperando_val_numero = False  
    esperando_fun_nombre = False  
    esperando_llave_fun = False  
    esperando_init = True  
    en_condicion = False  
    
    while True:
        tok = analizador.token()
        if not tok:
            break
        
        tokens_str = f"LexToken({tok.type}, '{tok.value}', {tok.lineno}, {tok.lexpos})"
        if tok.type in palabras_reservadas.values():
            palabras_reservadas_detectadas.append(tokens_str)
        else:
            tokens_generados.append(tokens_str)
        
       
        if tok.type == 'DELIMITADOR':
            if tok.value in '{(':
                pila.append(tok.value)
            elif tok.value in '})':
                if not pila:
                    errores.append(f"Error: Se encontró '{tok.value}' sin un delimitador de apertura en la línea {tok.lineno}")
                else:
                    top = pila.pop()
                    if (top == '(' and tok.value != ')') or (top == '{' and tok.value != '}'):
                        errores.append(f"Error: Delimitador desbalanceado '{top}' en la línea {tok.lineno}")
        
     
        if tok.type == 'INIT' and esperando_init:
            esperando_init = False  
        
      
        if tok.type == 'FUN':
            esperando_fun_nombre = True  
        elif esperando_fun_nombre:
            if tok.type == 'VARIABLE':
                esperando_fun_nombre = False
                esperando_llave_fun = True  
            else:
                errores.append(f"Error: Se esperaba un identificador después de 'fun' en la línea {tok.lineno}")
                esperando_fun_nombre = False
        elif esperando_llave_fun:
            if tok.type == 'DELIMITADOR' and tok.value == '{':
                esperando_llave_fun = False  
            else:
                errores.append(f"Error: Se esperaba {{ después de la declaración de función en la línea {tok.lineno}")
                esperando_llave_fun = False

       
        if tok.type == 'VAL' and not esperando_igual_val:
            esperando_val_variable = True  
        elif esperando_val_variable:
            if tok.type == 'VARIABLE':
                esperando_val_variable = False
                esperando_igual_val = True  
            else:
                errores.append(f"Error: Después de 'val' debe ir una variable en la línea {tok.lineno}")
                esperando_val_variable = False
        elif esperando_igual_val:
            if tok.type == 'ASIGNACION':
                esperando_igual_val = False
                esperando_val_numero = True
            else:
                errores.append(f"Error: Después de la variable debe ir un operador '=' en la línea {tok.lineno}")
                esperando_igual_val = False
        elif esperando_val_numero:
            if tok.type in ['ENTERO', 'FLOTANTE']:
                esperando_val_numero = False  
            else:
                errores.append(f"Error: Después de '=' debe ir un número o valor en la línea {tok.lineno}")
                esperando_val_numero = False

        
        if tok.type == 'IF' or tok.type == 'WHILE' or tok.type == 'FOR': 
            en_condicion = True
        elif en_condicion and tok.type == 'DELIMITADOR' and tok.value == ')':  
            en_condicion = False

 
    if esperando_init:
        errores.append("Error: Se debe definir la función 'init' para iniciar el programa.")
    
    if pila:
        errores.append("Error: Hay delimitadores de apertura sin cerrar: " + "".join(pila))
    
    return tokens_generados, palabras_reservadas_detectadas, errores
