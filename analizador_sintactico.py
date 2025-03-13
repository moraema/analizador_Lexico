import ply.yacc as yacc
from lexico import tokens  # Asegúrate de que el lexer se llame lexer.py

# Reglas de la gramática
def p_programa(p):
    '''programa : funcion'''
    p[0] = ('programa', p[1])

def p_funcion(p):
    '''funcion : FUNC INIT DELIMITADOR_L bloque DELIMITADOR_R'''
    p[0] = ('funcion_init', p[4])

def p_bloque(p):
    '''bloque : instruccion'''
    p[0] = ('bloque', p[1])

def p_instruccion(p):
    '''instruccion : ESCRIBIR DOS_PUNTOS COMILLAS SEPARADOR'''
    p[0] = ('escribir', p[3])  # Ahora se toma el valor de la cadena entre comillas (p[3])

def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}', línea {p.lineno}")
    else:
        print("Error de sintaxis en el final de la entrada")

# Construcción del parser
parser = yacc.yacc()

def analizar_sintaxis(codigo):
    return parser.parse(codigo)

# Ejemplo de prueba
codigo_prueba = 'func init { escribir:"Hola"; }' 
resultado = analizar_sintaxis(codigo_prueba)
print(resultado)
