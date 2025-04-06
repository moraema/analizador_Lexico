import ply.yacc as yacc
from lexico import tokens


precedence = (
    ('left', 'LOGICO'),
    ('left', 'COMPARACION_EQ', 'COMPARACION_NEQ', 'COMPARACION_LESS', 'COMPARACION_GREATER', 'COMPARACION_LESS_EQ', 'COMPARACION_GREATER_EQ'),
    ('left', 'OPERADOR'),
)

def p_programa(p):
    '''programa : FUNC INIT DELIMITADOR_L instrucciones DELIMITADOR_R'''
    p[0] = ('programa', p[4])

def p_instrucciones(p):
    '''instrucciones : instruccion instrucciones
                     | instruccion'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]

def p_instruccion(p):
    '''instruccion : declaracion_variable
                   | asignacion
                   | estructura_if
                   | estructura_else
                   | estructura_while
                   | estructura_for
                   | print_statement
                   | input_statement
                   | SEPARADOR'''
    if len(p) == 2:
        p[0] = p[1]

def p_declaracion_variable(p):
    '''declaracion_variable : VAL VARIABLE ASIGNACION expresion SEPARADOR'''
    p[0] = ('declaracion_variable', p[2], p[4])

def p_asignacion(p):
    '''asignacion : VARIABLE ASIGNACION expresion SEPARADOR'''
    p[0] = ('asignacion', p[1], p[3])

def p_estructura_if(p):
    '''estructura_if : IF T_PARENTESIS_L expresion_logica T_PARENTESIS_R DELIMITADOR_L instrucciones DELIMITADOR_R'''
    p[0] = ('if', p[3], p[6])

def p_estructura_else(p):
    '''estructura_else : estructura_if ELSE DELIMITADOR_L instrucciones DELIMITADOR_R'''
    p[0] = ('if_else', p[1][1], p[1][2], p[4])

def p_estructura_while(p):
    '''estructura_while : WHILE T_PARENTESIS_L expresion_logica T_PARENTESIS_R DELIMITADOR_L instrucciones DELIMITADOR_R'''
    p[0] = ('while', p[3], p[6])

def p_estructura_for(p):
    '''estructura_for : FOR T_PARENTESIS_L declaracion_variable expresion_logica SEPARADOR VARIABLE OPERADOR OPERADOR T_PARENTESIS_R DELIMITADOR_L instrucciones DELIMITADOR_R'''
    p[0] = ('for', p[3], p[4], p[6], p[9])

def p_print_statement(p):
    '''print_statement : ESCRIBIR T_PARENTESIS_L expresion T_PARENTESIS_R SEPARADOR'''
    p[0] = ('escribir', p[3])

def p_input_statement(p):
    '''input_statement : LEER T_PARENTESIS_L VARIABLE T_PARENTESIS_R SEPARADOR'''
    p[0] = ('leer', p[3])

def p_expresion_logica(p):
    '''expresion_logica : expresion_relacional
                        | expresion_logica LOGICO expresion_relacional'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('operacion_logica', p[2], p[1], p[3])

def p_expresion_relacional(p):
    '''expresion_relacional : expresion COMPARACION_EQ expresion
                           | expresion COMPARACION_NEQ expresion
                           | expresion COMPARACION_LESS expresion
                           | expresion COMPARACION_GREATER expresion
                           | expresion COMPARACION_LESS_EQ expresion
                           | expresion COMPARACION_GREATER_EQ expresion
                           | T_PARENTESIS_L expresion_logica T_PARENTESIS_R'''
    if len(p) == 4 and isinstance(p[2], str):
        p[0] = ('comparacion', p[1], p[2], p[3])
    else:
        p[0] = ('expresion_parentesis', p[2])

def p_expresion(p):
    '''expresion : termino
                 | expresion OPERADOR termino'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('operacion_aritmetica', p[2], p[1], p[3])

def p_termino(p):
    '''termino : ENTERO
               | FLOTANTE
               | VARIABLE
               | COMILLAS
               | T_PARENTESIS_L expresion T_PARENTESIS_R'''
    if len(p) == 2:
        if isinstance(p[1], int):
            p[0] = ('numero', p[1])
        elif isinstance(p[1], float):
            p[0] = ('flotante', p[1])
        elif p.slice[1].type == 'VARIABLE':
            p[0] = ('variable', p[1])
        else:
            p[0] = ('cadena', p[1])
    else:
        p[0] = ('parentesis', p[2])

errores_sintacticos = []
def p_error(p):
    global errores_sintacticos
    if p:
        mensaje = f"Error de sintaxis en '{p.value}' (token {p.type}), línea {p.lineno}"
    else:
        mensaje = "Error de sintaxis en el final de la entrada"
    errores_sintacticos.append(mensaje)

parser = yacc.yacc(debug=True)

def analizar_sintaxis(codigo):
    global errores_sintacticos
    errores_sintacticos = []
    resultado = parser.parse(codigo)
    return resultado, errores_sintacticos