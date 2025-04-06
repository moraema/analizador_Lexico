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

    declaracion_variable: "val" IDENTIFICADOR "=" expresion ";"
    asignacion: IDENTIFICADOR "=" expresion ";"
    
    estructura_if: "if" "(" expresion_logica ")" "{" instruccion* "}"
    estructura_else: "if" "(" expresion_logica ")" "{" instruccion* "}" "else" "{" instruccion* "}"
    estructura_while: "while" "(" expresion_logica ")" "{" instruccion* "}"
    estructura_for: "for" "(" declaracion_variable expresion_logica ";" IDENTIFICADOR operador_incremento ")" "{" instruccion* "}"
    
    print_statement: "escribir" "(" expresion ")" ";"
    input_statement: "leer" "(" IDENTIFICADOR ")" ";"
    
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
        self.tabla_simbolos = {}
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
        if nombre_var not in self.tabla_simbolos:
            self.errores_semanticos.append(f"Error semántico: Variable '{nombre_var}' no declarada")
        else:
            
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
        return {"tipo": "escribir", "expresion": expresion}
    
    def input_statement(self, identificador):
        nombre_var = str(identificador)
        
        if nombre_var not in self.tabla_simbolos:
            self.errores_semanticos.append(f"Error semántico: Variable '{nombre_var}' no declarada en input")
        
        return {"tipo": "leer", "variable": nombre_var}
    
    def operacion(self, izquierda, operador, derecha):
        tipo_izq = self.inferir_tipo(izquierda)
        tipo_der = self.inferir_tipo(derecha)
        
    
        if tipo_izq != tipo_der and tipo_izq != "any" and tipo_der != "any":
            self.errores_semanticos.append(f"Error semántico: Incompatibilidad de tipos en operación aritmética")
        
        return {"tipo": "operacion", "operador": str(operador), "izquierda": izquierda, "derecha": derecha}
    
    def expresion_relacional(self, izquierda, operador, derecha):
        tipo_izq = self.inferir_tipo(izquierda)
        tipo_der = self.inferir_tipo(derecha)
        
        
        if tipo_izq != tipo_der and tipo_izq != "any" and tipo_der != "any":
            self.errores_semanticos.append(f"Error semántico: Incompatibilidad de tipos en comparación")
        
        return {"tipo": "comparacion", "operador": str(operador), "izquierda": izquierda, "derecha": derecha}
    
    def numero(self, valor):
        
        if "." in str(valor):
            return {"tipo": "flotante", "valor": float(valor)}
        else:
            return {"tipo": "entero", "valor": int(valor)}
    
    def variable(self, nombre):
        nombre_var = str(nombre)
       
        if nombre_var not in self.tabla_simbolos:
            self.errores_semanticos.append(f"Error semántico: Variable '{nombre_var}' no declarada")
        
        return {"tipo": "variable", "nombre": nombre_var}
    
    def cadena(self, valor):
        
        valor_str = str(valor)[1:-1]
        return {"tipo": "cadena", "valor": valor_str}
    
    def parentesis(self, expresion):
        return expresion
    
    def inferir_tipo(self, expresion):
       
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
            "tabla_simbolos": transformador.tabla_simbolos,
            "errores": transformador.errores_semanticos
        }
    except UnexpectedToken as e:
        
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


class Interprete:
    def __init__(self, debug=True):
        
        self.memoria = {}
     
        self.entradas = []
     
        self.salidas = []
       
        self.debug = debug
    
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
            self.memoria = {}  
            self.salidas = []  
            
            ast = resultado_analisis["ast"]
            print(">>> Iniciando ejecución del programa <<<")
            if ast["tipo"] == "programa":
                for instruccion in ast.get("instrucciones", []):
                    self.ejecutar_nodo(instruccion)
            
            print(">>> Ejecución completada <<<")
            print(">>> Estado final de la memoria:", self.memoria)
            print(">>> Salidas generadas:", self.salidas)
            
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
        if isinstance(nodo, dict):
            tipo_nodo = nodo.get("tipo")
            
            if tipo_nodo == "programa":
                for instruccion in nodo.get("instrucciones", []):
                    self.ejecutar_nodo(instruccion)
            
            elif tipo_nodo == "declaracion_variable":
                nombre = nodo.get("nombre")
                valor = self.evaluar_expresion(nodo.get("valor"))
                self.memoria[nombre] = valor
                if self.debug:
                    print(f"DECLARACIÓN: {nombre} = {valor}")
            
            elif tipo_nodo == "asignacion":
                nombre = nodo.get("nombre")
                valor = self.evaluar_expresion(nodo.get("valor"))
                self.memoria[nombre] = valor
                if self.debug:
                    print(f"ASIGNACIÓN: {nombre} = {valor}")
            
            elif tipo_nodo == "if":
                condicion = self.evaluar_expresion(nodo.get("condicion"))
                if self.debug:
                    print(f"EVALUACIÓN IF: condición = {condicion}")
                if condicion:
                    if self.debug:
                        print("EJECUTANDO BLOQUE IF")
                    self.ejecutar_nodo(nodo.get("cuerpo"))
            
            elif tipo_nodo == "if_else":
                condicion = self.evaluar_expresion(nodo.get("condicion"))
                if self.debug:
                    print(f"EVALUACIÓN IF-ELSE: condición = {condicion}")
                if condicion:
                    if self.debug:
                        print("EJECUTANDO BLOQUE IF")
                    self.ejecutar_nodo(nodo.get("cuerpo_if"))
                else:
                    if self.debug:
                        print("EJECUTANDO BLOQUE ELSE")
                    self.ejecutar_nodo(nodo.get("cuerpo_else"))
            
            elif tipo_nodo == "while":
                iteracion = 0
                while True:
                    condicion = self.evaluar_expresion(nodo.get("condicion"))
                    if self.debug:
                        print(f"EVALUACIÓN WHILE (iteración {iteracion}): condición = {condicion}")
                    if not condicion:
                        break
                    if self.debug:
                        print(f"EJECUTANDO CUERPO WHILE (iteración {iteracion})")
                    self.ejecutar_nodo(nodo.get("cuerpo"))
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
                    self.ejecutar_nodo(nodo.get("cuerpo"))
                    
                    variable = nodo.get("variable")
                    operador = nodo.get("operador")
                    valor_anterior = self.memoria.get(variable, 0)
                    
                    if operador == "++":
                        self.memoria[variable] = valor_anterior + 1
                        if self.debug:
                            print(f"INCREMENTO: {variable} = {valor_anterior} + 1 = {self.memoria[variable]}")
                    elif operador == "--":
                        self.memoria[variable] = valor_anterior - 1
                        if self.debug:
                            print(f"DECREMENTO: {variable} = {valor_anterior} - 1 = {self.memoria[variable]}")
                    
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
                    self.memoria[variable] = valor
                    if self.debug:
                        print(f"LEER: {variable} = {valor}")
                else:
                    self.memoria[variable] = 0
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
           elif tipo_expr == "variable":
               nombre = expresion.get("nombre")
               return self.memoria.get(nombre, 0)
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
           
           return 0  # Valor por defecto
   
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
        elif tipo_expr == "variable":
            nombre = expresion.get("nombre")
            return self.memoria.get(nombre, 0)
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
        
        return 0  # Valor por defecto

# Ejemplo de uso
if __name__ == "__main__":
    # Código de ejemplo para probar el compilador e intérprete
    codigo_ejemplo = """
    func init {
        val x = 10;
        val y = 5;
        
        if (x > y) {
            escribir("x es mayor que y");
        } else {
            escribir("x no es mayor que y");
        }
        

    }
    """
    
    # Configurar entradas para el intérprete
    entradas_ejemplo = ["Juan"]
    
    # Crear e inicializar el intérprete
    interprete = Interprete(debug=True)
    interprete.establecer_entradas(entradas_ejemplo)
    
    # Ejecutar el código
    resultado = interprete.ejecutar(codigo_ejemplo)
    
    # Mostrar resultados
    if resultado["exito"]:
        print("\n=== EJECUCIÓN EXITOSA ===")
        print("Salidas:", resultado["salidas"])
        print("Estado final de la memoria:", resultado["memoria"])
    else:
        print("\n=== ERROR ===")
        print(resultado["error"])
        if "errores" in resultado:
            for error in resultado["errores"]:
                print(error)