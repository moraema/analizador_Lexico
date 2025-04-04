from lark import Lark, Transformer, v_args
from lark.exceptions import UnexpectedInput, UnexpectedToken, UnexpectedCharacters

# Definición de la gramática en Lark
grammar = r"""
    ?start: programa

    programa: "func" "init" "{" instruccion+ "}"

    ?instruccion: declaracion_variable
                | asignacion
                | estructura_if
                | estructura_else
                | estructura_while
                | estructura_for
                | print_statement
                | input_statement

    declaracion_variable: "var" IDENTIFICADOR "=" expresion ";"
    asignacion: IDENTIFICADOR "=" expresion ";"
    
    estructura_if: "if" "(" expresion_logica ")" "{" instruccion* "}"
    estructura_else: "if" "(" expresion_logica ")" "{" instruccion* "}" "else" "{" instruccion* "}"
    estructura_while: "while" "(" expresion_logica ")" "{" instruccion* "}"
    estructura_for: "for" "(" declaracion_variable expresion_logica ";" IDENTIFICADOR operador_incremento ")" "{" instruccion* "}"
    
    print_statement: "print" "(" expresion ")" ";"
    input_statement: "input" "(" IDENTIFICADOR ")" ";"
    
    ?operador_incremento: "++"
                        | "--"

    expresion_logica: expresion_relacional (LOGICO expresion_relacional)*

    expresion_relacional: expresion COMPARACION expresion
                        | "(" expresion_logica ")"

    ?expresion: expresion_aritmetica
    
    ?expresion_aritmetica: expresion_aritmetica OPERADOR_ARITMETICO termino -> operacion
                        | termino
    
    ?termino: NUMERO -> numero
            | IDENTIFICADOR -> variable
            | CADENA -> cadena
            | "(" expresion ")" -> parentesis

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

# Transformador para construir el AST
@v_args(inline=True)
class ASTBuilder(Transformer):
    def __init__(self):
        super().__init__()
        # Tabla de símbolos para almacenar variables y sus tipos
        self.tabla_simbolos = {}
        # Lista para almacenar errores semánticos
        self.errores_semanticos = []
    
    def programa(self, *instrucciones):
        return {"tipo": "programa", "instrucciones": list(instrucciones)}
    
    def declaracion_variable(self, identificador, expresion):
        nombre_var = str(identificador)
        # Verificar si la variable ya está declarada
        if nombre_var in self.tabla_simbolos:
            self.errores_semanticos.append(f"Error semántico: Variable '{nombre_var}' ya declarada")
        else:
            # Determinar el tipo de la expresión
            tipo_expr = self.inferir_tipo(expresion)
            self.tabla_simbolos[nombre_var] = {"tipo": tipo_expr}
        
        return {"tipo": "declaracion_variable", "nombre": nombre_var, "valor": expresion}
    
    def asignacion(self, identificador, expresion):
        nombre_var = str(identificador)
        # Verificar si la variable existe
        if nombre_var not in self.tabla_simbolos:
            self.errores_semanticos.append(f"Error semántico: Variable '{nombre_var}' no declarada")
        else:
            # Verificar compatibilidad de tipos
            tipo_var = self.tabla_simbolos[nombre_var]["tipo"]
            tipo_expr = self.inferir_tipo(expresion)
            if tipo_var != tipo_expr and tipo_var != "any" and tipo_expr != "any":
                self.errores_semanticos.append(f"Error semántico: Incompatibilidad de tipos en asignación a '{nombre_var}'")
        
        return {"tipo": "asignacion", "nombre": nombre_var, "valor": expresion}
    
    def estructura_if(self, condicion, cuerpo):
        return {"tipo": "if", "condicion": condicion, "cuerpo": cuerpo}
    
    def estructura_else(self, condicion, cuerpo_if, cuerpo_else):
        return {"tipo": "if_else", "condicion": condicion, "cuerpo_if": cuerpo_if, "cuerpo_else": cuerpo_else}
    
    def estructura_while(self, condicion, cuerpo):
        return {"tipo": "while", "condicion": condicion, "cuerpo": cuerpo}
    
    def estructura_for(self, inicializacion, condicion, variable, operador, cuerpo):
        # Verificar que la variable del incremento existe
        nombre_var = str(variable)
        if nombre_var not in self.tabla_simbolos:
            self.errores_semanticos.append(f"Error semántico: Variable '{nombre_var}' no declarada en bucle for")
        
        return {
            "tipo": "for", 
            "inicializacion": inicializacion, 
            "condicion": condicion, 
            "variable": nombre_var,
            "operador": operador,
            "cuerpo": cuerpo
        }
    
    def print_statement(self, expresion):
        return {"tipo": "print", "expresion": expresion}
    
    def input_statement(self, identificador):
        nombre_var = str(identificador)
        # Verificar si la variable existe
        if nombre_var not in self.tabla_simbolos:
            self.errores_semanticos.append(f"Error semántico: Variable '{nombre_var}' no declarada en input")
        
        return {"tipo": "input", "variable": nombre_var}
    
    def operacion(self, izquierda, operador, derecha):
        tipo_izq = self.inferir_tipo(izquierda)
        tipo_der = self.inferir_tipo(derecha)
        
        # Verificar compatibilidad de tipos para operaciones aritméticas
        if tipo_izq != tipo_der and tipo_izq != "any" and tipo_der != "any":
            self.errores_semanticos.append(f"Error semántico: Incompatibilidad de tipos en operación aritmética")
        
        return {"tipo": "operacion", "operador": str(operador), "izquierda": izquierda, "derecha": derecha}
    
    def expresion_relacional(self, izquierda, operador, derecha):
        tipo_izq = self.inferir_tipo(izquierda)
        tipo_der = self.inferir_tipo(derecha)
        
        # Verificar compatibilidad de tipos para comparaciones
        if tipo_izq != tipo_der and tipo_izq != "any" and tipo_der != "any":
            self.errores_semanticos.append(f"Error semántico: Incompatibilidad de tipos en comparación")
        
        return {"tipo": "comparacion", "operador": str(operador), "izquierda": izquierda, "derecha": derecha}
    
    def numero(self, valor):
        # Determinar si es entero o flotante
        if "." in str(valor):
            return {"tipo": "flotante", "valor": float(valor)}
        else:
            return {"tipo": "entero", "valor": int(valor)}
    
    def variable(self, nombre):
        nombre_var = str(nombre)
        # Verificar si la variable existe
        if nombre_var not in self.tabla_simbolos:
            self.errores_semanticos.append(f"Error semántico: Variable '{nombre_var}' no declarada")
        
        return {"tipo": "variable", "nombre": nombre_var}
    
    def cadena(self, valor):
        # Eliminar las comillas del string
        valor_str = str(valor)[1:-1]
        return {"tipo": "cadena", "valor": valor_str}
    
    def parentesis(self, expresion):
        return expresion
    
    def inferir_tipo(self, expresion):
        # Inferir el tipo de una expresión para chequeo de tipos
        if isinstance(expresion, dict):
            if expresion["tipo"] == "entero":
                return "entero"
            elif expresion["tipo"] == "flotante":
                return "flotante"
            elif expresion["tipo"] == "cadena":
                return "cadena"
            elif expresion["tipo"] == "variable":
                nombre_var = expresion["nombre"]
                if nombre_var in self.tabla_simbolos:
                    return self.tabla_simbolos[nombre_var]["tipo"]
                return "any"  # Si no existe, asumimos tipo any para evitar cascada de errores
            elif expresion["tipo"] == "operacion":
                # Para operaciones, inferimos el tipo basado en los operandos
                tipo_izq = self.inferir_tipo(expresion["izquierda"])
                tipo_der = self.inferir_tipo(expresion["derecha"])
                
                # Si ambos son del mismo tipo, el resultado es de ese tipo
                if tipo_izq == tipo_der:
                    return tipo_izq
                # Si alguno es flotante, el resultado es flotante
                elif "flotante" in [tipo_izq, tipo_der]:
                    return "flotante"
                # Si alguno es any, asumimos any
                elif "any" in [tipo_izq, tipo_der]:
                    return "any"
                # En otros casos (como con cadenas), podría haber problemas
                else:
                    return "any"
        
        return "any"  # Tipo por defecto

# Función para analizar un programa
def analizar_programa(codigo):
    try:
        # Parseo inicial
        arbol = parser.parse(codigo)
        
        # Construcción del AST y análisis semántico
        transformador = ASTBuilder()
        ast = transformador.transform(arbol)
        
        return {
            "exito": len(transformador.errores_semanticos) == 0,
            "ast": ast,
            "tabla_simbolos": transformador.tabla_simbolos,
            "errores": transformador.errores_semanticos
        }
    except UnexpectedToken as e:
        # Mensaje especial para cuando falta func init
        if e.token == "func":
            return {
                "exito": False,
                "error_tipo": "sintáctico",
                "mensaje": "El programa debe comenzar con 'func init {}'"
            }
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

# Clase Intérprete para ejecutar el AST
class Interprete:
    def __init__(self):
        # Memoria para almacenar valores de variables
        self.memoria = {}
        # Para simular la entrada del usuario
        self.entradas = []
        # Para capturar las salidas del programa
        self.salidas = []
    
    def establecer_entradas(self, entradas):
        """Establece una lista de valores de entrada para simular input()"""
        self.entradas = entradas
    
    def ejecutar(self, codigo):
        """Ejecuta un programa y devuelve el resultado de la ejecución"""
        # Analizar el programa primero
        resultado_analisis = analizar_programa(codigo)
        
        if not resultado_analisis["exito"]:
            return {
                "exito": False,
                "error": resultado_analisis.get("mensaje", "Error semántico"),
                "errores": resultado_analisis.get("errores", [])
            }
        
        # Si el análisis fue exitoso, ejecutamos el programa
        try:
            self.memoria = {}  # Reiniciar memoria
            self.salidas = []  # Reiniciar salidas
            
            ast = resultado_analisis["ast"]
            # Ejecutar solo las instrucciones dentro de func init
            if ast["tipo"] == "programa":
                for instruccion in ast.get("instrucciones", []):
                    self.ejecutar_nodo(instruccion)
            
            return {
                "exito": True,
                "memoria": self.memoria,
                "salidas": self.salidas
            }
        except Exception as e:
            return {
                "exito": False,
                "error": f"Error en ejecución: {str(e)}"
            }
    
    def ejecutar_nodo(self, nodo):
        """Ejecuta un nodo del AST"""
        if isinstance(nodo, dict):
            tipo_nodo = nodo.get("tipo")
            
            if tipo_nodo == "programa":
                for instruccion in nodo.get("instrucciones", []):
                    self.ejecutar_nodo(instruccion)
            
            elif tipo_nodo == "declaracion_variable":
                nombre = nodo.get("nombre")
                valor = self.evaluar_expresion(nodo.get("valor"))
                self.memoria[nombre] = valor
            
            elif tipo_nodo == "asignacion":
                nombre = nodo.get("nombre")
                valor = self.evaluar_expresion(nodo.get("valor"))
                self.memoria[nombre] = valor
            
            elif tipo_nodo == "if":
                condicion = self.evaluar_expresion(nodo.get("condicion"))
                if condicion:
                    self.ejecutar_nodo(nodo.get("cuerpo"))
            
            elif tipo_nodo == "if_else":
                condicion = self.evaluar_expresion(nodo.get("condicion"))
                if condicion:
                    self.ejecutar_nodo(nodo.get("cuerpo_if"))
                else:
                    self.ejecutar_nodo(nodo.get("cuerpo_else"))
            
            elif tipo_nodo == "while":
                while self.evaluar_expresion(nodo.get("condicion")):
                    self.ejecutar_nodo(nodo.get("cuerpo"))
            
            elif tipo_nodo == "for":
                # Ejecutar inicialización
                self.ejecutar_nodo(nodo.get("inicializacion"))
                
                # Ejecutar el bucle
                while self.evaluar_expresion(nodo.get("condicion")):
                    self.ejecutar_nodo(nodo.get("cuerpo"))
                    
                    # Actualizar la variable de incremento
                    variable = nodo.get("variable")
                    operador = nodo.get("operador")
                    
                    if operador == "++":
                        self.memoria[variable] = self.memoria.get(variable, 0) + 1
                    elif operador == "--":
                        self.memoria[variable] = self.memoria.get(variable, 0) - 1
            
            elif tipo_nodo == "print":
                valor = self.evaluar_expresion(nodo.get("expresion"))
                self.salidas.append(str(valor))
            
            elif tipo_nodo == "input":
                variable = nodo.get("variable")
                if self.entradas:
                    self.memoria[variable] = self.entradas.pop(0)
                else:
                    # Si no hay entradas simuladas, usamos un valor por defecto
                    self.memoria[variable] = 0
    
    def evaluar_expresion(self, expresion):
        """Evalúa una expresión y devuelve su valor"""
        if not isinstance(expresion, dict):
            return expresion
        
        tipo_expr = expresion.get("tipo")
        
        if tipo_expr == "entero":
            return expresion.get("valor")
        
        elif tipo_expr == "flotante":
            return expresion.get("valor")
        
        elif tipo_expr == "cadena":
            return expresion.get("valor")
        
        elif tipo_expr == "variable":
            nombre = expresion.get("nombre")
            return self.memoria.get(nombre, 0)  # 0 por defecto si no existe
        
        elif tipo_expr == "operacion":
            izquierda = self.evaluar_expresion(expresion.get("izquierda"))
            derecha = self.evaluar_expresion(expresion.get("derecha"))
            operador = expresion.get("operador")
            
            if operador == "+":
                return izquierda + derecha
            elif operador == "-":
                return izquierda - derecha
            elif operador == "*":
                return izquierda * derecha
            elif operador == "/":
                return izquierda / derecha if derecha != 0 else 0  # Evitar división por cero
        
        elif tipo_expr == "comparacion":
            izquierda = self.evaluar_expresion(expresion.get("izquierda"))
            derecha = self.evaluar_expresion(expresion.get("derecha"))
            operador = expresion.get("operador")
            
            if operador == "==":
                return izquierda == derecha
            elif operador == "!=":
                return izquierda != derecha
            elif operador == "<":
                return izquierda < derecha
            elif operador == ">":
                return izquierda > derecha
            elif operador == "<=":
                return izquierda <= derecha
            elif operador == ">=":
                return izquierda >= derecha
        
        return 0  # Valor por defecto

