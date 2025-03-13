import ply.yacc as yacc
from lexico import tokens  # Asegúrate de que los tokens estén correctamente importados

# Reglas de la gramática
precedence = (# Los operadores aritméticos
    ('left', 'COMPARACION_LESS', 'COMPARACION_GREATER', 'COMPARACION_LESS_EQ', 'COMPARACION_GREATER_EQ'),  # Comparaciones
    ('left', 'COMPARACION_EQ', 'COMPARACION_NEQ'),  # Comparaciones de igualdad
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
    else:  # Si solo hay una instrucción
        p[0] = ('bloque', [p[1]])

def p_instruccion(p):
    '''instruccion : ESCRIBIR DOS_PUNTOS COMILLAS SEPARADOR
                   | declaracion_variable
                   | estructura_if
                   | estructura_while
                   | estructura_for''' 
    if len(p) == 5:  # Es una instrucción escribir
        p[0] = ('escribir', p[3])
    else:  # Es otra instrucción
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


def p_condicion_for(p):
    '''condicion_for : expresion_relacional'''
    p[0] = ('condicion', p[1])

def p_incremento_for(p):
    '''incremento_for : VARIABLE INCREMENTO
                       | VARIABLE DECREMENTO'''
    p[0] = ('incremento', p[1], p[2])
    
def p_expresion_logica(p):
    '''expresion_logica : expresion_relacional
                        | expresion_logica LOGICO expresion_relacional'''
    if len(p) == 2:  # Solo expresión relacional
        p[0] = p[1]
    else:  # Operador lógico
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

def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}' (token {p.type}), línea {p.lineno}")
    else:
        print("Error de sintaxis en el final de la entrada")

# Construcción del parser
parser = yacc.yacc()

def analizar_sintaxis(codigo):
    return parser.parse(codigo)

# Ejemplo de prueba
codigo_prueba = """
func init {
    val x = 10;
    escribir:"Hola";
    
    if( x < 20 ) {
        escribir:"Numero valido";
    }
    
    val y = 30;

    if(y == 30) {
        escribir:"Y es 30";
    }
    
    while(y > 30) {
        escribir:"Y es 30";
    }

   for (val i = 0; i >= 1; i++) {
   escribir:"Y es 30";
  }

}
"""

resultado = analizar_sintaxis(codigo_prueba)
print(resultado) 