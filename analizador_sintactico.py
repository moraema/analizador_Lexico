import ply.yacc as yacc
from lexico import tokens  

precedence = (
    ('left', 'COMPARACION_LESS', 'COMPARACION_GREATER', 'COMPARACION_LESS_EQ', 'COMPARACION_GREATER_EQ'),  # Comparaciones
    ('left', 'COMPARACION_EQ', 'COMPARACION_NEQ'), 
     ('left', 'OPERADOR'),  
)

def p_programa(p):
    '''programa : funcion'''
    p[0] = ('programa', p[1])

def p_funcion(p):
    '''funcion : FUNC INIT DELIMITADOR_L bloque DELIMITADOR_R'''
    p[0] = ('funcion_init', p[4])

def p_bloque(p):
    '''bloque : instruccion bloque
              | instruccion'''
    if len(p) == 3:  # Si hay dos elementos, p[2] es un bloque adicional
        p[0] = ('bloque', [p[1]] + p[2][1])
    else:  # solo hay una instrucción
        p[0] = ('bloque', [p[1]])

def p_instruccion(p):
    '''instruccion : ESCRIBIR DOS_PUNTOS COMILLAS SEPARADOR
                   | LEER VARIABLE SEPARADOR
                   | declaracion_variable
                   | estructura_if
                   | estructura_while
                   | estructura_for''' 
    if len(p) == 5:  # una instrucción escribir
        p[0] = ('escribir', p[3])
    elif len(p) == 3 and p[1] == 'leer':  
        p[0] = ('leer', p[2])  #  variable que se lee
    else:  
        p[0] = p[1]

def p_declaracion_variable(p):
    '''declaracion_variable : VAL VARIABLE ASIGNACION expresion SEPARADOR'''
    p[0] = ('declaracion_variable', p[2], p[4])

def p_estructura_if(p):
    '''estructura_if : IF expresion_logica DELIMITADOR_L bloque DELIMITADOR_R'''
    p[0] = ('if', p[2], p[4])

def p_estructura_while(p):
    '''estructura_while : WHILE expresion_logica DELIMITADOR_L bloque DELIMITADOR_R'''
    p[0] = ('while', p[2], p[4])

def p_estructura_for(p):
    '''estructura_for : FOR T_PARENTESIS_L declaracion_variable VARIABLE operador_comparacion expresion SEPARADOR  VARIABLE  OPERADOR OPERADOR T_PARENTESIS_R DELIMITADOR_L bloque DELIMITADOR_R'''
    p[0] = ('for', p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11], p[12], p[13])



def p_expresion_logica(p):
    '''expresion_logica : expresion_relacional
                        | expresion_logica LOGICO expresion_relacional'''
    if len(p) == 2: 
        p[0] = p[1]
    else:  
        p[0] = ('operacion_logica', p[2], p[1], p[3])

def p_operador_comparacion(p):
    '''operador_comparacion : COMPARACION_GREATER
                            | COMPARACION_LESS
                            | COMPARACION_LESS_EQ
                            | COMPARACION_GREATER_EQ'''
    p[0] = ('operador_comparacion', p[1])


def p_expresion_relacional(p):
    '''expresion_relacional : expresion COMPARACION_LESS expresion
                            | expresion COMPARACION_GREATER expresion
                            | expresion COMPARACION_LESS_EQ expresion
                            | expresion COMPARACION_GREATER_EQ expresion
                            | expresion COMPARACION_EQ expresion
                            | expresion COMPARACION_NEQ expresion
                            | T_PARENTESIS_L expresion_relacional T_PARENTESIS_R'''
    if len(p) == 4:
        p[0] = ('comparacion', p[1], p[2], p[3])
    elif len(p) == 3:
        p[0] = ('expresion_parentesis', p[2])

def p_expresion_aritmetica(p):
    '''expresion : expresion OPERADOR expresion'''
    p[0] = ('operacion_aritmetica', p[2], p[1], p[3])

def p_expresion(p):
    '''expresion : ENTERO
                 | FLOTANTE
                 | COMILLAS
                 | VARIABLE'''
    if p.slice[1].type == 'ENTERO':
        p[0] = ('expresion_entero', p[1])
    elif p.slice[1].type == 'FLOTANTE':
        p[0] = ('expresion_flotante', p[1])
    elif p.slice[1].type == 'COMILLAS':
        p[0] = ('expresion_cadena', p[1])
    else:  # VARIABLE
        p[0] = ('expresion_variable', p[1])


errores_sintacticos = [] 
def p_error(p):
    global errores_sintacticos
    if p:
        mensaje = f"Error de sintaxis en '{p.value}' (token {p.type}), línea {p.lineno}"
    else:
        mensaje = "Error de sintaxis en el final de la entrada"
    
    errores_sintacticos.append(mensaje)

# Construcción del parser
parser = yacc.yacc(debug=True)

def analizar_sintaxis(codigo):
    global errores_sintacticos
    errores_sintacticos.clear()  
    resultado = parser.parse(codigo)
    return resultado, errores_sintacticos

'''
def mostrar_tablas():
    print("Tabla de análisis predictivo:")
    # Usar trace para ver las transiciones paso a paso del parser
    parser.parse('func init { val x = 5; leer y; escribir : "Hello, world!"; }')

'''