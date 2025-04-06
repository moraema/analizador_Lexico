class GeneradorCodigoIntermedio:
    def __init__(self):
        self.codigo = []
        self.contador_temp = 0
        self.contador_etiqueta = 0
        self.tabla_simbolos = {}
    
    def nuevo_temporal(self):
        """Genera un nuevo nombre de variable temporal"""
        temp = f"t{self.contador_temp}"
        self.contador_temp += 1
        return temp
    
    def nueva_etiqueta(self):
        """Genera una nueva etiqueta para saltos"""
        etiqueta = f"L{self.contador_etiqueta}"
        self.contador_etiqueta += 1
        return etiqueta
    
    def generar_codigo(self, ast):
        """Genera código intermedio a partir del AST"""
        if ast["tipo"] == "programa":
            self.codigo.append("# Inicio del programa")
            for instruccion in ast.get("instrucciones", []):
                self.generar_codigo_instruccion(instruccion)
            self.codigo.append("# Fin del programa")
        return self.codigo
    
    def generar_codigo_instruccion(self, nodo):
        """Genera código para una instrucción"""
        tipo_nodo = nodo.get("tipo")
        
        if tipo_nodo == "declaracion_variable":
            nombre = nodo.get("nombre")
            valor_expr = self.generar_codigo_expresion(nodo.get("valor"))
            self.codigo.append(f"{nombre} = {valor_expr}")
            self.tabla_simbolos[nombre] = True
        
        elif tipo_nodo == "asignacion":
            nombre = nodo.get("nombre")
            valor_expr = self.generar_codigo_expresion(nodo.get("valor"))
            self.codigo.append(f"{nombre} = {valor_expr}")
        
        elif tipo_nodo == "if":
            etiqueta_fin = self.nueva_etiqueta()
            self.generar_codigo_condicion(nodo.get("condicion"), None, etiqueta_fin)
            
            # Cuerpo del if
            if isinstance(nodo.get("cuerpo"), list):
                for instruccion in nodo.get("cuerpo"):
                    self.generar_codigo_instruccion(instruccion)
            else:
                self.generar_codigo_instruccion(nodo.get("cuerpo"))
            
            self.codigo.append(f"{etiqueta_fin}:")
        
        elif tipo_nodo == "if_else":
            etiqueta_else = self.nueva_etiqueta()
            etiqueta_fin = self.nueva_etiqueta()
            
            self.generar_codigo_condicion(nodo.get("condicion"), None, etiqueta_else)
            
            # Cuerpo del if
            if isinstance(nodo.get("cuerpo_if"), list):
                for instruccion in nodo.get("cuerpo_if"):
                    self.generar_codigo_instruccion(instruccion)
            else:
                self.generar_codigo_instruccion(nodo.get("cuerpo_if"))
            
            self.codigo.append(f"goto {etiqueta_fin}")
            self.codigo.append(f"{etiqueta_else}:")
            
            # Cuerpo del else
            if isinstance(nodo.get("cuerpo_else"), list):
                for instruccion in nodo.get("cuerpo_else"):
                    self.generar_codigo_instruccion(instruccion)
            else:
                self.generar_codigo_instruccion(nodo.get("cuerpo_else"))
            
            self.codigo.append(f"{etiqueta_fin}:")
        
        elif tipo_nodo == "while":
            etiqueta_inicio = self.nueva_etiqueta()
            etiqueta_fin = self.nueva_etiqueta()
            
            self.codigo.append(f"{etiqueta_inicio}:")
            self.generar_codigo_condicion(nodo.get("condicion"), None, etiqueta_fin)
            
            # Cuerpo del while
            if isinstance(nodo.get("cuerpo"), list):
                for instruccion in nodo.get("cuerpo"):
                    self.generar_codigo_instruccion(instruccion)
            else:
                self.generar_codigo_instruccion(nodo.get("cuerpo"))
            
            self.codigo.append(f"goto {etiqueta_inicio}")
            self.codigo.append(f"{etiqueta_fin}:")
        
        elif tipo_nodo == "for":
            # Inicialización
            self.generar_codigo_instruccion(nodo.get("inicializacion"))
            
            etiqueta_inicio = self.nueva_etiqueta()
            etiqueta_fin = self.nueva_etiqueta()
            
            self.codigo.append(f"{etiqueta_inicio}:")
            self.generar_codigo_condicion(nodo.get("condicion"), None, etiqueta_fin)
            
            # Cuerpo del for
            if isinstance(nodo.get("cuerpo"), list):
                for instruccion in nodo.get("cuerpo"):
                    self.generar_codigo_instruccion(instruccion)
            else:
                self.generar_codigo_instruccion(nodo.get("cuerpo"))
            
            # Incremento
            variable = nodo.get("variable")
            operador = nodo.get("operador")
            
            if operador == "++":
                self.codigo.append(f"{variable} = {variable} + 1")
            elif operador == "--":
                self.codigo.append(f"{variable} = {variable} - 1")
            
            self.codigo.append(f"goto {etiqueta_inicio}")
            self.codigo.append(f"{etiqueta_fin}:")
        
        elif tipo_nodo == "escribir":
            valor_expr = self.generar_codigo_expresion(nodo.get("expresion"))
            self.codigo.append(f"print {valor_expr}")
        
        elif tipo_nodo == "leer":
            variable = nodo.get("variable")
            self.codigo.append(f"read {variable}")
    
    def generar_codigo_expresion(self, expresion):
        """Genera código para una expresión y devuelve el temporal o valor resultante"""
        if not isinstance(expresion, dict):
            return str(expresion)
        
        tipo_expr = expresion.get("tipo")
        
        if tipo_expr == "entero":
            return str(expresion.get("valor"))
        
        elif tipo_expr == "flotante":
            return str(expresion.get("valor"))
        
        elif tipo_expr == "cadena":
            return f'"{expresion.get("valor")}"'
        
        elif tipo_expr == "variable":
            return expresion.get("nombre")
        
        elif tipo_expr == "operacion":
            izquierda = self.generar_codigo_expresion(expresion.get("izquierda"))
            derecha = self.generar_codigo_expresion(expresion.get("derecha"))
            operador = expresion.get("operador")
            
            temp = self.nuevo_temporal()
            self.codigo.append(f"{temp} = {izquierda} {operador} {derecha}")
            return temp
        
        elif tipo_expr == "comparacion":
            izquierda = self.generar_codigo_expresion(expresion.get("izquierda"))
            derecha = self.generar_codigo_expresion(expresion.get("derecha"))
            operador = expresion.get("operador")
            
            temp = self.nuevo_temporal()
            self.codigo.append(f"{temp} = {izquierda} {operador} {derecha}")
            return temp
        
        return "0"  # Valor por defecto
    
    def generar_codigo_condicion(self, condicion, etiqueta_verdadero, etiqueta_falso):
        """Genera código para una condición con saltos"""
        resultado = self.generar_codigo_expresion(condicion)
        
        if etiqueta_verdadero:
            self.codigo.append(f"if {resultado} goto {etiqueta_verdadero}")
        
        if etiqueta_falso:
            self.codigo.append(f"ifFalse {resultado} goto {etiqueta_falso}")