
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftCOMPARACION_LESSCOMPARACION_GREATERCOMPARACION_LESS_EQCOMPARACION_GREATER_EQleftCOMPARACION_EQCOMPARACION_NEQleftOPERADORASIGNACION COMILLAS COMPARACION_EQ COMPARACION_GREATER COMPARACION_GREATER_EQ COMPARACION_LESS COMPARACION_LESS_EQ COMPARACION_NEQ DECREMENTO DELIMITADOR_L DELIMITADOR_R DOS_PUNTOS ELSE ENTERO ESCRIBIR FLOTANTE FOR FUNC IF INCREMENTO INIT LEER LOGICO OPERADOR SEPARADOR T_PARENTESIS_L T_PARENTESIS_R VAL VARIABLE WHILEprograma : funcionfuncion : FUNC INIT DELIMITADOR_L bloque DELIMITADOR_Rbloque : instruccion bloque\n              | instruccioninstruccion : ESCRIBIR DOS_PUNTOS COMILLAS SEPARADOR\n                   | declaracion_variable\n                   | estructura_if\n                   | estructura_while\n                   | estructura_fordeclaracion_variable : VAL VARIABLE ASIGNACION expresion SEPARADORestructura_if : IF expresion_logica DELIMITADOR_L bloque DELIMITADOR_Restructura_while : WHILE expresion_logica DELIMITADOR_L bloque DELIMITADOR_Restructura_for : FOR T_PARENTESIS_L declaracion_variable VARIABLE operador_comparacion expresion SEPARADOR  VARIABLE  OPERADOR OPERADOR T_PARENTESIS_R DELIMITADOR_L bloque DELIMITADOR_Rcondicion_for : expresion_relacionalincremento_for : VARIABLE INCREMENTO\n                       | VARIABLE DECREMENTOexpresion_logica : expresion_relacional\n                        | expresion_logica LOGICO expresion_relacionaloperador_comparacion : COMPARACION_GREATER\n                            | COMPARACION_LESS\n                            | COMPARACION_LESS_EQ\n                            | COMPARACION_GREATER_EQexpresion_relacional : expresion COMPARACION_LESS expresion\n                            | expresion COMPARACION_GREATER expresion\n                            | expresion COMPARACION_LESS_EQ expresion\n                            | expresion COMPARACION_GREATER_EQ expresion\n                            | expresion COMPARACION_EQ expresion\n                            | expresion COMPARACION_NEQ expresion\n                            | T_PARENTESIS_L expresion_relacional T_PARENTESIS_Rexpresion : ENTERO\n                 | FLOTANTE\n                 | COMILLAS\n                 | VARIABLE'
    
_lr_action_items = {'FUNC':([0,],[3,]),'$end':([1,2,17,],[0,-1,-2,]),'INIT':([3,],[4,]),'DELIMITADOR_L':([4,21,22,25,26,27,28,29,47,48,49,50,51,52,53,54,70,],[5,33,-17,-30,-31,-32,-33,42,-18,-23,-24,-25,-26,-27,-28,-29,71,]),'ESCRIBIR':([5,7,9,10,11,12,33,42,44,57,58,59,71,73,],[8,8,-6,-7,-8,-9,8,8,-5,-10,-11,-12,8,-13,]),'VAL':([5,7,9,10,11,12,30,33,42,44,57,58,59,71,73,],[13,13,-6,-7,-8,-9,13,13,13,-5,-10,-11,-12,13,-13,]),'IF':([5,7,9,10,11,12,33,42,44,57,58,59,71,73,],[14,14,-6,-7,-8,-9,14,14,-5,-10,-11,-12,14,-13,]),'WHILE':([5,7,9,10,11,12,33,42,44,57,58,59,71,73,],[15,15,-6,-7,-8,-9,15,15,-5,-10,-11,-12,15,-13,]),'FOR':([5,7,9,10,11,12,33,42,44,57,58,59,71,73,],[16,16,-6,-7,-8,-9,16,16,-5,-10,-11,-12,16,-13,]),'DELIMITADOR_R':([6,7,9,10,11,12,18,44,46,55,57,58,59,72,73,],[17,-4,-6,-7,-8,-9,-3,-5,58,59,-10,-11,-12,73,-13,]),'DOS_PUNTOS':([8,],[19,]),'VARIABLE':([13,14,15,24,32,34,35,36,37,38,39,40,43,57,60,61,62,63,64,66,],[20,28,28,28,28,28,28,28,28,28,28,28,56,-10,28,-19,-20,-21,-22,67,]),'T_PARENTESIS_L':([14,15,16,24,34,],[24,24,30,24,24,]),'ENTERO':([14,15,24,32,34,35,36,37,38,39,40,60,61,62,63,64,],[25,25,25,25,25,25,25,25,25,25,25,25,-19,-20,-21,-22,]),'FLOTANTE':([14,15,24,32,34,35,36,37,38,39,40,60,61,62,63,64,],[26,26,26,26,26,26,26,26,26,26,26,26,-19,-20,-21,-22,]),'COMILLAS':([14,15,19,24,32,34,35,36,37,38,39,40,60,61,62,63,64,],[27,27,31,27,27,27,27,27,27,27,27,27,27,-19,-20,-21,-22,]),'ASIGNACION':([20,],[32,]),'LOGICO':([21,22,25,26,27,28,29,47,48,49,50,51,52,53,54,],[34,-17,-30,-31,-32,-33,34,-18,-23,-24,-25,-26,-27,-28,-29,]),'COMPARACION_LESS':([23,25,26,27,28,56,],[35,-30,-31,-32,-33,62,]),'COMPARACION_GREATER':([23,25,26,27,28,56,],[36,-30,-31,-32,-33,61,]),'COMPARACION_LESS_EQ':([23,25,26,27,28,56,],[37,-30,-31,-32,-33,63,]),'COMPARACION_GREATER_EQ':([23,25,26,27,28,56,],[38,-30,-31,-32,-33,64,]),'COMPARACION_EQ':([23,25,26,27,28,],[39,-30,-31,-32,-33,]),'COMPARACION_NEQ':([23,25,26,27,28,],[40,-30,-31,-32,-33,]),'SEPARADOR':([25,26,27,28,31,45,65,],[-30,-31,-32,-33,44,57,66,]),'T_PARENTESIS_R':([25,26,27,28,41,48,49,50,51,52,53,54,69,],[-30,-31,-32,-33,54,-23,-24,-25,-26,-27,-28,-29,70,]),'OPERADOR':([67,68,],[68,69,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'programa':([0,],[1,]),'funcion':([0,],[2,]),'bloque':([5,7,33,42,71,],[6,18,46,55,72,]),'instruccion':([5,7,33,42,71,],[7,7,7,7,7,]),'declaracion_variable':([5,7,30,33,42,71,],[9,9,43,9,9,9,]),'estructura_if':([5,7,33,42,71,],[10,10,10,10,10,]),'estructura_while':([5,7,33,42,71,],[11,11,11,11,11,]),'estructura_for':([5,7,33,42,71,],[12,12,12,12,12,]),'expresion_logica':([14,15,],[21,29,]),'expresion_relacional':([14,15,24,34,],[22,22,41,47,]),'expresion':([14,15,24,32,34,35,36,37,38,39,40,60,],[23,23,23,45,23,48,49,50,51,52,53,65,]),'operador_comparacion':([56,],[60,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> programa","S'",1,None,None,None),
  ('programa -> funcion','programa',1,'p_programa','analizador_sintactico.py',12),
  ('funcion -> FUNC INIT DELIMITADOR_L bloque DELIMITADOR_R','funcion',5,'p_funcion','analizador_sintactico.py',16),
  ('bloque -> instruccion bloque','bloque',2,'p_bloque','analizador_sintactico.py',20),
  ('bloque -> instruccion','bloque',1,'p_bloque','analizador_sintactico.py',21),
  ('instruccion -> ESCRIBIR DOS_PUNTOS COMILLAS SEPARADOR','instruccion',4,'p_instruccion','analizador_sintactico.py',28),
  ('instruccion -> declaracion_variable','instruccion',1,'p_instruccion','analizador_sintactico.py',29),
  ('instruccion -> estructura_if','instruccion',1,'p_instruccion','analizador_sintactico.py',30),
  ('instruccion -> estructura_while','instruccion',1,'p_instruccion','analizador_sintactico.py',31),
  ('instruccion -> estructura_for','instruccion',1,'p_instruccion','analizador_sintactico.py',32),
  ('declaracion_variable -> VAL VARIABLE ASIGNACION expresion SEPARADOR','declaracion_variable',5,'p_declaracion_variable','analizador_sintactico.py',39),
  ('estructura_if -> IF expresion_logica DELIMITADOR_L bloque DELIMITADOR_R','estructura_if',5,'p_estructura_if','analizador_sintactico.py',43),
  ('estructura_while -> WHILE expresion_logica DELIMITADOR_L bloque DELIMITADOR_R','estructura_while',5,'p_estructura_while','analizador_sintactico.py',47),
  ('estructura_for -> FOR T_PARENTESIS_L declaracion_variable VARIABLE operador_comparacion expresion SEPARADOR VARIABLE OPERADOR OPERADOR T_PARENTESIS_R DELIMITADOR_L bloque DELIMITADOR_R','estructura_for',14,'p_estructura_for','analizador_sintactico.py',51),
  ('condicion_for -> expresion_relacional','condicion_for',1,'p_condicion_for','analizador_sintactico.py',56),
  ('incremento_for -> VARIABLE INCREMENTO','incremento_for',2,'p_incremento_for','analizador_sintactico.py',60),
  ('incremento_for -> VARIABLE DECREMENTO','incremento_for',2,'p_incremento_for','analizador_sintactico.py',61),
  ('expresion_logica -> expresion_relacional','expresion_logica',1,'p_expresion_logica','analizador_sintactico.py',65),
  ('expresion_logica -> expresion_logica LOGICO expresion_relacional','expresion_logica',3,'p_expresion_logica','analizador_sintactico.py',66),
  ('operador_comparacion -> COMPARACION_GREATER','operador_comparacion',1,'p_operador_comparacion','analizador_sintactico.py',73),
  ('operador_comparacion -> COMPARACION_LESS','operador_comparacion',1,'p_operador_comparacion','analizador_sintactico.py',74),
  ('operador_comparacion -> COMPARACION_LESS_EQ','operador_comparacion',1,'p_operador_comparacion','analizador_sintactico.py',75),
  ('operador_comparacion -> COMPARACION_GREATER_EQ','operador_comparacion',1,'p_operador_comparacion','analizador_sintactico.py',76),
  ('expresion_relacional -> expresion COMPARACION_LESS expresion','expresion_relacional',3,'p_expresion_relacional','analizador_sintactico.py',81),
  ('expresion_relacional -> expresion COMPARACION_GREATER expresion','expresion_relacional',3,'p_expresion_relacional','analizador_sintactico.py',82),
  ('expresion_relacional -> expresion COMPARACION_LESS_EQ expresion','expresion_relacional',3,'p_expresion_relacional','analizador_sintactico.py',83),
  ('expresion_relacional -> expresion COMPARACION_GREATER_EQ expresion','expresion_relacional',3,'p_expresion_relacional','analizador_sintactico.py',84),
  ('expresion_relacional -> expresion COMPARACION_EQ expresion','expresion_relacional',3,'p_expresion_relacional','analizador_sintactico.py',85),
  ('expresion_relacional -> expresion COMPARACION_NEQ expresion','expresion_relacional',3,'p_expresion_relacional','analizador_sintactico.py',86),
  ('expresion_relacional -> T_PARENTESIS_L expresion_relacional T_PARENTESIS_R','expresion_relacional',3,'p_expresion_relacional','analizador_sintactico.py',87),
  ('expresion -> ENTERO','expresion',1,'p_expresion','analizador_sintactico.py',94),
  ('expresion -> FLOTANTE','expresion',1,'p_expresion','analizador_sintactico.py',95),
  ('expresion -> COMILLAS','expresion',1,'p_expresion','analizador_sintactico.py',96),
  ('expresion -> VARIABLE','expresion',1,'p_expresion','analizador_sintactico.py',97),
]
