from lark import Lark, Transformer, v_args
from lark.exceptions import UnexpectedInput, UnexpectedToken, UnexpectedCharacters


grammar = r"""
    ?start: programa

    programa: func+

    func: "func" IDENTIFICADOR "()" "{" instruccion+ "}"

    ?instruccion: declaracion_variable
                | asignacion
                | estructura_if
                | estructura_else
                | estructura_while
                | estructura_for
                | print_statement
                | input_statement
                | llamada_funcion

    declaracion_variable: "val" IDENTIFICADOR ("=" expresion)? ";"
    asignacion: IDENTIFICADOR "=" expresion ";"
    
    estructura_if: "if" "(" condicion ")" "{" instruccion* "}"
    estructura_else: "if" "(" condicion ")" "{" instruccion* "}" "else" "{" instruccion* "}"
    estructura_while: "while" "(" condicion ")" "{" instruccion* "}"
    estructura_for: "for" "(" declaracion_variable condicion ";" IDENTIFICADOR operador_incremento ")" "{" instruccion* "}"
    
    print_statement: "escribir" "(" expresion ")" ";"
    input_statement: "leer" "(" IDENTIFICADOR ")" ";"
    llamada_funcion: IDENTIFICADOR "(" ")" ";"
    
    ?operador_incremento: "++"
                        | "--"

    ?condicion: expresion_logica 
              | valor_booleano
              | IDENTIFICADOR  

    expresion_logica: expresion_relacional (LOGICO expresion_relacional)*

    ?expresion_relacional: expresion COMPARACION expresion
                         | "(" expresion_logica ")"

    ?expresion: termino
              | expresion OPERADOR_ARITMETICO termino -> operacion

    ?termino: NUMERO -> numero
            | IDENTIFICADOR -> variable
            | CADENA -> cadena
            | "(" expresion ")" -> parentesis
            | valor_booleano

    valor_booleano: "true" -> true
                  | "false" -> false

    OPERADOR_ARITMETICO: "+" | "-" | "*" | "/"
    COMPARACION: "==" | "!=" | "<" | ">" | "<=" | ">="
    LOGICO: "&&" | "||"
    
    IDENTIFICADOR: /[a-zA-Z_][a-zA-Z0-9_]*/
    NUMERO: /[0-9]+(\.[0-9]+)?/
    CADENA: /"[^"]*"/
    
    COMENTARIO: /\/\/[^\n]*/
    
    %import common.WS
    %ignore WS
    %ignore COMENTARIO
"""

# Crear el parser de Lark
parser = Lark(grammar, parser='lalr', debug=True)
@v_args(inline=True)
class ASTBuilder(Transformer):
    def __init__(self):
        super().__init__()
        self.tabla_simbolos_global = {}  
        self.tabla_funciones = {}       
        self.llamadas_funciones = []     
        self.errores_semanticos = []
        self.ambito_actual = None        
        self.tabla_simbolos_local = {}   
    
    def programa(self, *funciones):
    
        for func in funciones:
            nombre_func = func.get("nombre")
            self.tabla_funciones[nombre_func] = func
        
        # Verificar que haya una función init
        if "init" not in self.tabla_funciones:
            self.errores_semanticos.append("Error semántico: Debe existir una función 'init'")
        
     
        for llamada in self.llamadas_funciones:
            if llamada not in self.tabla_funciones:
                self.errores_semanticos.append(f"Error semántico: Función '{llamada}' no declarada")
        
        return {"tipo": "programa", "funciones": list(funciones)}
    
    def func(self, nombre, *instrucciones):
        nombre_func = str(nombre)
        self.ambito_actual = nombre_func
        self.tabla_simbolos_local = {}  
        
      
        instrucciones_procesadas = []
        for inst in instrucciones:
            instrucciones_procesadas.append(inst)
        
        
        return {"tipo": "funcion", "nombre": nombre_func, "instrucciones": instrucciones_procesadas}
    
    def llamada_funcion(self, nombre):
        nombre_func = str(nombre)
       
        self.llamadas_funciones.append(nombre_func)
        
        return {"tipo": "llamada_funcion", "nombre": nombre_func}
    
    def declaracion_variable(self, identificador, *args):
        nombre_var = str(identificador)
        
        # Verificar si la variable ya está declarada en el ámbito actual
        if self.ambito_actual: 
            if nombre_var in self.tabla_simbolos_local:
                self.errores_semanticos.append(f"Error semántico: Variable '{nombre_var}' ya declarada en la función")
            else:
                
                if args:
                    expresion = args[0]
                    tipo_expr = self.inferir_tipo(expresion)
                    valor_inicial = self.evaluar_valor_inicial(expresion)
                    self.tabla_simbolos_local[nombre_var] = {"tipo": tipo_expr, "valor": valor_inicial}
                    return {"tipo": "declaracion_variable", "nombre": nombre_var, "valor": expresion}
                else:
                    # Si no hay argumentos, es una declaración sin inicialización
                    self.tabla_simbolos_local[nombre_var] = {"tipo": "any", "valor": "No inicializado"}
                    return {"tipo": "declaracion_variable", "nombre": nombre_var, "valor": None}
        else:  
            if nombre_var in self.tabla_simbolos_global:
                self.errores_semanticos.append(f"Error semántico: Variable '{nombre_var}' ya declarada")
            else:
                if args:
                    expresion = args[0]
                    tipo_expr = self.inferir_tipo(expresion)
                    valor_inicial = self.evaluar_valor_inicial(expresion)
                    self.tabla_simbolos_global[nombre_var] = {"tipo": tipo_expr, "valor": valor_inicial}
                    return {"tipo": "declaracion_variable", "nombre": nombre_var, "valor": expresion}
                else:
                    self.tabla_simbolos_global[nombre_var] = {"tipo": "any", "valor": "No inicializado"}
                    return {"tipo": "declaracion_variable", "nombre": nombre_var, "valor": None}
            
    def evaluar_valor_inicial(self, expresion):
        """Intenta evaluar el valor inicial de una expresión constante"""
        if isinstance(expresion, dict):
            if expresion["tipo"] == "entero":
                return expresion["valor"]
            elif expresion["tipo"] == "flotante":
                return expresion["valor"]
            elif expresion["tipo"] == "cadena":
                return f'"{expresion["valor"]}"'
            elif expresion["tipo"] == "booleano":
                return "true" if expresion["valor"] else "false"
        return "Expresión compleja"
    
    def asignacion(self, identificador, expresion):
        nombre_var = str(identificador)
        
        
        if self.ambito_actual and nombre_var in self.tabla_simbolos_local:
            tipo_var = self.tabla_simbolos_local[nombre_var]["tipo"]
            tipo_expr = self.inferir_tipo(expresion)
            if not self.tipos_compatibles(tipo_var, tipo_expr):
                self.errores_semanticos.append(f"Error semántico: Incompatibilidad de tipos en asignación a '{nombre_var}'")
        elif nombre_var in self.tabla_simbolos_global:
            tipo_var = self.tabla_simbolos_global[nombre_var]["tipo"]
            tipo_expr = self.inferir_tipo(expresion)
            if not self.tipos_compatibles(tipo_var, tipo_expr):
                self.errores_semanticos.append(f"Error semántico: Incompatibilidad de tipos en asignación a '{nombre_var}'")
        else:
            self.errores_semanticos.append(f"Error semántico: Variable '{nombre_var}' no declarada")
        
        return {"tipo": "asignacion", "nombre": nombre_var, "valor": expresion}
    
    def estructura_if(self, condicion, *instrucciones):
      
        instrucciones_lista = list(instrucciones)
        return {"tipo": "if", "condicion": condicion, "cuerpo": instrucciones_lista}
    
    def estructura_else(self, condicion, cuerpo_if, cuerpo_else):
        return {"tipo": "if_else", "condicion": condicion, "cuerpo_if": cuerpo_if, "cuerpo_else": cuerpo_else}
    
    def estructura_while(self, condicion, *instrucciones):
       
        instrucciones_lista = list(instrucciones)
        return {"tipo": "while", "condicion": condicion, "cuerpo": instrucciones_lista}
    
    def estructura_for(self, inicializacion, condicion, variable, operador, *instrucciones):
        nombre_var = str(variable)
        instrucciones_lista = list(instrucciones)
        
        
        if not (nombre_var in self.tabla_simbolos_local or nombre_var in self.tabla_simbolos_global):
            self.errores_semanticos.append(f"Error semántico: Variable '{nombre_var}' no declarada en bucle for")
        
        return {
            "tipo": "for", 
            "inicializacion": inicializacion, 
            "condicion": condicion, 
            "variable": nombre_var,
            "operador": operador,
            "cuerpo": instrucciones_lista
        }
    
    def print_statement(self, expresion):
        return {"tipo": "escribir", "expresion": expresion}
    
    def input_statement(self, identificador):
        nombre_var = str(identificador)
        
       
        if not (nombre_var in self.tabla_simbolos_local or nombre_var in self.tabla_simbolos_global):
            self.errores_semanticos.append(f"Error semántico: Variable '{nombre_var}' no declarada en input")
        
        return {"tipo": "leer", "variable": nombre_var}
    
    def operacion(self, izquierda, operador, derecha):
        tipo_izq = self.inferir_tipo(izquierda)
        tipo_der = self.inferir_tipo(derecha)
        
        if not self.tipos_compatibles(tipo_izq, tipo_der):
            self.errores_semanticos.append(f"Error semántico: Incompatibilidad de tipos en operación aritmética")
        
        return {"tipo": "operacion", "operador": str(operador), "izquierda": izquierda, "derecha": derecha}
    
    def expresion_relacional(self, izquierda, operador, derecha):
        tipo_izq = self.inferir_tipo(izquierda)
        tipo_der = self.inferir_tipo(derecha)
        
      
        if not self.tipos_compatibles(tipo_izq, tipo_der):
            self.errores_semanticos.append(f"Error semántico: Incompatibilidad de tipos en comparación")
        
        return {"tipo": "comparacion", "operador": str(operador), "izquierda": izquierda, "derecha": derecha}
    
    def booleano(self, valor):
        valor_bool = str(valor).lower() == "true"
        return {"tipo": "booleano", "valor": valor_bool}
    
    def true(self):
        return {"tipo": "booleano", "valor": True}
    
    def false(self):
        return {"tipo": "booleano", "valor": False}
    
    def numero(self, valor):
        if "." in str(valor):
            return {"tipo": "flotante", "valor": float(valor)}
        else:
            return {"tipo": "entero", "valor": int(valor)}
    
    def variable(self, nombre):
        nombre_var = str(nombre)
        
     
        if self.ambito_actual and nombre_var in self.tabla_simbolos_local:
            return {"tipo": "variable", "nombre": nombre_var}
        elif nombre_var in self.tabla_simbolos_global:
            return {"tipo": "variable", "nombre": nombre_var}
        else:
            self.errores_semanticos.append(f"Error semántico: Variable '{nombre_var}' no declarada")
            return {"tipo": "variable", "nombre": nombre_var}
    
    def cadena(self, valor):
        valor_str = str(valor)[1:-1]
        return {"tipo": "cadena", "valor": valor_str}
    
    def parentesis(self, expresion):
        return expresion
    
    def tipos_compatibles(self, tipo1, tipo2):
      
        if tipo1 == tipo2:
            return True
        if (tipo1 == "entero" and tipo2 == "flotante") or (tipo1 == "flotante" and tipo2 == "entero"):
            return True
        if tipo1 == "any" or tipo2 == "any":
            return True
        return False
    
    def inferir_tipo(self, expresion):
        if isinstance(expresion, dict):
            if expresion["tipo"] == "entero":
                return "entero"
            elif expresion["tipo"] == "flotante":
                return "flotante"
            elif expresion["tipo"] == "cadena":
                return "cadena"
            elif expresion["tipo"] == "booleano":
                return "booleano"
            elif expresion["tipo"] == "variable":
                nombre_var = expresion["nombre"]
              
                if self.ambito_actual and nombre_var in self.tabla_simbolos_local:
                    return self.tabla_simbolos_local[nombre_var]["tipo"]
                elif nombre_var in self.tabla_simbolos_global:
                    return self.tabla_simbolos_global[nombre_var]["tipo"]
                return "any"
            elif expresion["tipo"] == "operacion":
                tipo_izq = self.inferir_tipo(expresion["izquierda"])
                tipo_der = self.inferir_tipo(expresion["derecha"])
                
               
                if tipo_izq == tipo_der:
                    return tipo_izq
                
                elif "flotante" in [tipo_izq, tipo_der]:
                    return "flotante"
              
                elif "any" in [tipo_izq, tipo_der]:
                    return "any"
               
                else:
                    return "any"
        
        return "any" 


def analizar_programa(codigo):
    try:
        # Parseo inicial
        arbol = parser.parse(codigo)
        
        transformador = ASTBuilder()
        ast = transformador.transform(arbol)
        
        return {
            "exito": len(transformador.errores_semanticos) == 0,
            "ast": ast,
            "tabla_simbolos": {
                "global": transformador.tabla_simbolos_global,
                "local": transformador.tabla_simbolos_local
            },
            "tabla_funciones": transformador.tabla_funciones,
            "errores": transformador.errores_semanticos
        }
    except UnexpectedToken as e:
        return {
            "exito": False,
            "error_tipo": "sintáctico",
            "mensaje": f"Error sintáctico en línea {e.line}, columna {e.column}: {e.token}"
        }
    except UnexpectedCharacters as e:
        return {
            "exito": False,
            "error_tipo": "léxico",
            "mensaje": f"Error léxico en línea {e.line}, columna {e.column}: caracter inesperado '{e.char}'"
        }
    except Exception as e:
        return {
            "exito": False,
            "error_tipo": "desconocido",
            "mensaje": f"Error desconocido: {str(e)}"
        }

# Función para imprimir el AST de forma legible
def imprimir_ast(ast, nivel=0):
    if isinstance(ast, dict):
        indent = "  " * nivel
        print(f"{indent}{ast.get('tipo', 'nodo')}")
        for clave, valor in ast.items():
            if clave != "tipo":
                print(f"{indent}  {clave}:")
                imprimir_ast(valor, nivel + 2)
    elif isinstance(ast, list):
        for elemento in ast:
            imprimir_ast(elemento, nivel)
    else:
        indent = "  " * nivel
        print(f"{indent}{ast}")


class Interprete:
    def __init__(self, debug=True):
        self.memoria_global = {}
        self.memoria_local = {}
        self.entradas = []
        self.salidas = []
        self.debug = debug
        self.tabla_funciones = {}
        self.ambito_actual = None
    
    def establecer_entradas(self, entradas):
        self.entradas = entradas
    
    def ejecutar(self, codigo):
        resultado_analisis = analizar_programa(codigo)
        
        if not resultado_analisis["exito"]:
            return {
                "exito": False,
                "error": resultado_analisis.get("mensaje", "Error semántico"),
                "errores": resultado_analisis.get("errores", [])
            }
        
        try:
            self.memoria_global = {}  
            self.memoria_local = {}
            self.salidas = []
            self.tabla_funciones = resultado_analisis["tabla_funciones"]
            
            ast = resultado_analisis["ast"]
            print(">>> Iniciando ejecución del programa <<<")
            
            # Primero, registrar todas las funciones en la tabla de funciones
            if ast["tipo"] == "programa":
                funciones = ast.get("funciones", [])
                
                # Registramos todas las funciones primero
                for funcion in funciones:
                    nombre_func = funcion.get("nombre")
                    self.tabla_funciones[nombre_func] = funcion
                    if self.debug:
                        print(f"Registrando función: {nombre_func}")
                
                # Luego buscamos y ejecutamos init
                if "init" in self.tabla_funciones:
                    self.ejecutar_funcion("init")
                else:
                    print("Error: No se encontró la función 'init'")
                    return {
                        "exito": False,
                        "error": "No se encontró la función 'init'"
                    }
            
            print(">>> Ejecución completada <<<")
            print(">>> Estado final de la memoria global:", self.memoria_global)
            print(">>> Salidas generadas:", self.salidas)
            
            return {
                "exito": True,
                "memoria_global": self.memoria_global,
                "memoria_local": self.memoria_local,
                "salidas": self.salidas
            }
        except Exception as e:
            return {
                "exito": False,
                "error": f"Error en ejecución: {str(e)}"
            }
    
    def ejecutar_funcion(self, nombre_funcion):
        if self.debug:
            print(f"EJECUTANDO FUNCIÓN: {nombre_funcion}")
        
        if nombre_funcion not in self.tabla_funciones:
            print(f"Error: Función '{nombre_funcion}' no encontrada")
            return
        
        # Guardar el ámbito anterior
        ambito_anterior = self.ambito_actual
        memoria_local_anterior = self.memoria_local
        
        # Establecer nuevo ámbito
        self.ambito_actual = nombre_funcion
        self.memoria_local = {}
        
        funcion = self.tabla_funciones[nombre_funcion]
        instrucciones = funcion.get("instrucciones", [])
        
        for instruccion in instrucciones:
            self.ejecutar_nodo(instruccion)
        
        # Restaurar el ámbito anterior
        self.ambito_actual = ambito_anterior
        self.memoria_local = memoria_local_anterior
    
    def obtener_variable(self, nombre):
        """Busca una variable primero en el ámbito local, luego en el global"""
        if self.ambito_actual and nombre in self.memoria_local:
            return self.memoria_local[nombre]
        elif nombre in self.memoria_global:
            return self.memoria_global[nombre]
        else:
            if self.debug:
                print(f"Advertencia: Variable '{nombre}' no encontrada, se asume 0")
            return 0
    
    def asignar_variable(self, nombre, valor):
        """Asigna una variable en el ámbito correcto"""
        if self.ambito_actual:
            # Si estamos en una función y la variable existe localmente
            if nombre in self.memoria_local:
                self.memoria_local[nombre] = valor
            # Si existe globalmente, la asignamos allí (a menos que sea shadowing)
            elif nombre in self.memoria_global:
                self.memoria_global[nombre] = valor
            else:
                # Por defecto, creamos la variable en el ámbito local
                self.memoria_local[nombre] = valor
        else:
            # Ámbito global
            self.memoria_global[nombre] = valor
    
    def ejecutar_nodo(self, nodo):
        if isinstance(nodo, dict):
            tipo_nodo = nodo.get("tipo")
            
            if tipo_nodo == "programa":
                for funcion in nodo.get("funciones", []):
                    if funcion.get("nombre") == "init":
                        self.ejecutar_nodo(funcion)
            
            elif tipo_nodo == "funcion":
                if nodo.get("nombre") == "init":
                    for instruccion in nodo.get("instrucciones", []):
                        self.ejecutar_nodo(instruccion)
            
            elif tipo_nodo == "llamada_funcion":
                nombre_func = nodo.get("nombre")
                self.ejecutar_funcion(nombre_func)
            
            elif tipo_nodo == "declaracion_variable":
                nombre = nodo.get("nombre")
                valor = self.evaluar_expresion(nodo.get("valor")) if nodo.get("valor") is not None else 0
                self.asignar_variable(nombre, valor)
                if self.debug:
                    print(f"DECLARACIÓN: {nombre} = {valor}")
            
            elif tipo_nodo == "asignacion":
                nombre = nodo.get("nombre")
                valor = self.evaluar_expresion(nodo.get("valor"))
                self.asignar_variable(nombre, valor)
                if self.debug:
                    print(f"ASIGNACIÓN: {nombre} = {valor}")
            
            elif tipo_nodo == "if":
                condicion = self.evaluar_expresion(nodo.get("condicion"))
                if self.debug:
                    print(f"EVALUACIÓN IF: condición = {condicion}")
                if condicion:
                    if self.debug:
                        print("EJECUTANDO BLOQUE IF")
                    for instruccion in nodo.get("cuerpo", []):
                        self.ejecutar_nodo(instruccion)
            
            elif tipo_nodo == "if_else":
                condicion = self.evaluar_expresion(nodo.get("condicion"))
                if self.debug:
                    print(f"EVALUACIÓN IF-ELSE: condición = {condicion}")
                if condicion:
                    if self.debug:
                        print("EJECUTANDO BLOQUE IF")
                    for instruccion in nodo.get("cuerpo_if", []):
                        self.ejecutar_nodo(instruccion)
                else:
                    if self.debug:
                        print("EJECUTANDO BLOQUE ELSE")
                    for instruccion in nodo.get("cuerpo_else", []):
                        self.ejecutar_nodo(instruccion)
            
            elif tipo_nodo == "while":
                # Modificado para manejar correctamente el cuerpo del while
                iteracion = 0
                while True:
                    condicion = self.evaluar_expresion(nodo.get("condicion"))
                    if self.debug:
                        print(f"EVALUACIÓN WHILE (iteración {iteracion}): condición = {condicion}")
                    if not condicion:
                        break
                    
                    if self.debug:
                        print(f"EJECUTANDO CUERPO WHILE (iteración {iteracion})")
                    
                    # Ejecutar cada instrucción en el cuerpo del while
                    cuerpo = nodo.get("cuerpo", [])
                    for instruccion in cuerpo:
                        self.ejecutar_nodo(instruccion)
                    
                    iteracion += 1
            
            elif tipo_nodo == "for":
                if self.debug:
                    print("INICIALIZACIÓN FOR")
                self.ejecutar_nodo(nodo.get("inicializacion"))
                
                iteracion = 0
                while True:
                    condicion = self.evaluar_expresion(nodo.get("condicion"))
                    if self.debug:
                        print(f"EVALUACIÓN FOR (iteración {iteracion}): condición = {condicion}")
                    if not condicion:
                        break
                    
                    if self.debug:
                        print(f"EJECUTANDO CUERPO FOR (iteración {iteracion})")
                    
                    # Ejecutar cada instrucción en el cuerpo del for
                    cuerpo = nodo.get("cuerpo", [])
                    for instruccion in cuerpo:
                        self.ejecutar_nodo(instruccion)
                    
                    variable = nodo.get("variable")
                    operador = nodo.get("operador")
                    valor_anterior = self.obtener_variable(variable)
                    
                    if operador == "++":
                        nuevo_valor = valor_anterior + 1
                        self.asignar_variable(variable, nuevo_valor)
                        if self.debug:
                            print(f"INCREMENTO: {variable} = {valor_anterior} + 1 = {nuevo_valor}")
                    elif operador == "--":
                        nuevo_valor = valor_anterior - 1
                        self.asignar_variable(variable, nuevo_valor)
                        if self.debug:
                            print(f"DECREMENTO: {variable} = {valor_anterior} - 1 = {nuevo_valor}")
                    
                    iteracion += 1
            
            elif tipo_nodo == "escribir":
                valor = self.evaluar_expresion(nodo.get("expresion"))
                self.salidas.append(str(valor))
                if self.debug:
                    print(f"ESCRIBIR: {valor}")
                else:
                    print(f">>> {valor}")
            
            elif tipo_nodo == "leer":
                variable = nodo.get("variable")
                if self.entradas:
                    valor = self.entradas.pop(0)
                    self.asignar_variable(variable, valor)
                    if self.debug:
                        print(f"LEER: {variable} = {valor}")
                else:
                    self.asignar_variable(variable, 0)
                    if self.debug:
                        print(f"LEER (sin entrada disponible): {variable} = 0")
        
        elif isinstance(nodo, list):
            for elemento in nodo:
                self.ejecutar_nodo(elemento)

    
    def evaluar_expresion(self, expresion):
        """Evalúa una expresión y devuelve su valor"""
        if not isinstance(expresion, dict):
            return expresion
        
        tipo_expr = expresion.get("tipo")
        
        if tipo_expr == "entero":
            return int(expresion.get("valor"))
        elif tipo_expr == "flotante":
            return float(expresion.get("valor"))
        elif tipo_expr == "cadena":
            return str(expresion.get("valor"))
        elif tipo_expr == "booleano":
            return bool(expresion.get("valor"))
        elif tipo_expr == "variable":
            nombre = expresion.get("nombre")
            return self.obtener_variable(nombre)
        elif tipo_expr == "operacion":
            izq = self.evaluar_expresion(expresion.get("izquierda"))
            der = self.evaluar_expresion(expresion.get("derecha"))
            operador = expresion.get("operador")
            
            if operador == "+":
                return izq + der
            elif operador == "-":
                return izq - der
            elif operador == "*":
                return izq * der
            elif operador == "/":
                return izq / der if der != 0 else 0
        elif tipo_expr == "comparacion":
            izq = self.evaluar_expresion(expresion.get("izquierda"))
            der = self.evaluar_expresion(expresion.get("derecha"))
            operador = expresion.get("operador")
            
            if operador == "==":
                return izq == der
            elif operador == "!=":
                return izq != der
            elif operador == "<":
                return izq < der
            elif operador == ">":
                return izq > der
            elif operador == "<=":
                return izq <= der
            elif operador == ">=":
                return izq >= der
        
        return 0