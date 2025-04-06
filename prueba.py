from lark import Lark, Transformer, v_args

# Definición de la gramática en Lark
gramatica = """
    ?start: expr
    ?expr: expr "+" term  -> sum
         | expr "-" term  -> sub
         | term
    ?term: term "*" factor  -> mul
         | term "/" factor  -> div
         | factor
    ?factor: NUMBER         -> number
           | "(" expr ")"
    
    %import common.NUMBER
    %import common.WS
    %ignore WS
"""

# Analizador sintáctico con Lark
parser = Lark(gramatica, parser='lalr')

# Transformer para generar el AST con atributos semánticos y código intermedio
class ASTTransformer(Transformer):
    temp_count = 0
    tac = []
    
    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"
    
    @v_args(inline=True)
    def number(self, n):
        return {"type": "number", "value": float(n), "tac": str(n)}
    
    @v_args(inline=True)
    def sum(self, left, right):
        temp = self.new_temp()
        self.tac.append(f"{temp} = {left['tac']} + {right['tac']}")
        return {"type": "sum", "left": left, "right": right, "value": left["value"] + right["value"], "tac": temp}
    
    @v_args(inline=True)
    def sub(self, left, right):
        temp = self.new_temp()
        self.tac.append(f"{temp} = {left['tac']} - {right['tac']}")
        return {"type": "sub", "left": left, "right": right, "value": left["value"] - right["value"], "tac": temp}
    
    @v_args(inline=True)
    def mul(self, left, right):
        temp = self.new_temp()
        self.tac.append(f"{temp} = {left['tac']} * {right['tac']}")
        return {"type": "mul", "left": left, "right": right, "value": left["value"] * right["value"], "tac": temp}
    
    @v_args(inline=True)
    def div(self, left, right):
        if right["value"] == 0:
            raise ZeroDivisionError("Error: División entre cero")
        temp = self.new_temp()
        self.tac.append(f"{temp} = {left['tac']} / {right['tac']}")
        return {"type": "div", "left": left, "right": right, "value": left["value"] / right["value"], "tac": temp}

# Función para generar el AST, evaluar atributos y obtener código intermedio
def generar_ast_y_tac(expresion):
    transformer = ASTTransformer()
    tree = parser.parse(expresion)
    ast = transformer.transform(tree)
    return ast, transformer.tac

# Ejemplo de uso
expresion = "(3 + 5) * 2 - 4 / 2"
ast, tac = generar_ast_y_tac(expresion)
print("AST:", ast)
print("Código Intermedio (TAC):")
for instr in tac:
    print(instr)
