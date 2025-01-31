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
    'PUNTO'
]

palabras_reservadas = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'func': 'FUN',
    'escribir': 'ESCRIBIR',
    'leer': 'LEER',
    'val': 'VAL'
}

