import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
from lexico import analisis
from analizador_sintactico import analizar_sintaxis
from analizador import analizar_programa  

def formatear_ast(ast, nivel=0):
    """Convierte el AST a un formato de texto legible"""
    resultado = ""
    if isinstance(ast, dict):
        indent = "  " * nivel
        resultado += f"{indent}{ast.get('tipo', 'nodo')}\n"
        for clave, valor in ast.items():
            if clave != "tipo":
                resultado += f"{indent}  {clave}:\n"
                resultado += formatear_ast(valor, nivel + 2)
    elif isinstance(ast, list):
        for elemento in ast:
            resultado += formatear_ast(elemento, nivel)
    else:
        indent = "  " * nivel
        resultado += f"{indent}{ast}\n"
    return resultado

def analizar_codigo():
    codigo = entrada_texto.get("1.0", tk.END).strip()
    
    # Limpiar todas las salidas primero
    salida_tokens.delete("1.0", tk.END)
    salida_palabras.delete("1.0", tk.END)
    salida_errores.delete("1.0", tk.END)
    salida_sintactico.delete("1.0", tk.END)
    salida_semantico.delete("1.0", tk.END)
    
    # Análisis léxico
    tokens_detectados, palabras_reservadas_detectadas, errores_detectados = analisis(codigo)
    
    # Mostrar resultados léxicos
    salida_tokens.insert(tk.END, "\n".join(tokens_detectados))
    salida_palabras.insert(tk.END, "\n".join(palabras_reservadas_detectadas))
    salida_errores.insert(tk.END, "\n".join(errores_detectados))
    
    # Análisis sintáctico
    try:
        resultado_sintactico, errores_sintacticos = analizar_sintaxis(codigo)
        
        if errores_sintacticos:
            for error in errores_sintacticos:
                salida_sintactico.insert(tk.END, f"Error: {error}\n")
        else:
            for regla in resultado_sintactico:
                salida_sintactico.insert(tk.END, f"Regla aplicada: {regla}\n")
    except Exception as e:
        salida_sintactico.insert(tk.END, f"Error: {str(e)}\n")
    
    # Análisis semántico
    try:
        resultado_semantico = analizar_programa(codigo)
        
        if not resultado_semantico["exito"]:
            salida_semantico.insert(tk.END, "=== ERRORES SEMÁNTICOS ===\n")
            if "errores" in resultado_semantico and resultado_semantico["errores"]:
                for error in resultado_semantico["errores"]:
                    salida_semantico.insert(tk.END, f"• {error}\n")
            else:
                mensaje_error = resultado_semantico.get('mensaje', 'Error desconocido')
                error_tipo = resultado_semantico.get('error_tipo', 'desconocido')
                salida_semantico.insert(tk.END, f"Error {error_tipo}: {mensaje_error}\n")
        else:
            salida_semantico.insert(tk.END, "=== ANÁLISIS SEMÁNTICO CORRECTO ===\n")
            
            salida_semantico.insert(tk.END, "\n=== TABLA DE SÍMBOLOS ===\n")
            for variable, info in resultado_semantico["tabla_simbolos"].items():
                tipo_var = info.get("tipo", "desconocido")
                salida_semantico.insert(tk.END, f"• Variable: {variable}, Tipo: {tipo_var}\n")
            
            salida_semantico.insert(tk.END, "\n=== ÁRBOL DE SINTAXIS ABSTRACTA (AST) ===\n")
            # Formatear el AST para una mejor visualización
            ast_formateado = formatear_ast(resultado_semantico["ast"])
            salida_semantico.insert(tk.END, ast_formateado)
    except Exception as e:
        salida_semantico.insert(tk.END, f"Error en análisis semántico: {str(e)}\n")
        import traceback
        salida_semantico.insert(tk.END, f"\nDetalles de la excepción:\n{traceback.format_exc()}")

def cargar_archivo():
    """ Permite cargar un archivo de texto en la entrada de código. """
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if archivo:
        with open(archivo, "r") as f:
            entrada_texto.delete("1.0", tk.END)
            entrada_texto.insert(tk.END, f.read())

def guardar_archivo():
    """ Permite guardar el código actual en un archivo de texto. """
    archivo = filedialog.asksaveasfilename(filetypes=[("Archivos de texto", "*.txt")])
    if archivo:
        if not archivo.endswith(".txt"):
            archivo += ".txt"
        with open(archivo, "w") as f:
            f.write(entrada_texto.get("1.0", tk.END))

def limpiar_entrada():
    """ Limpia el área de entrada de código. """
    entrada_texto.delete("1.0", tk.END)

def limpiar_todo():
    """ Limpia todas las áreas de texto. """
    entrada_texto.delete("1.0", tk.END)
    salida_tokens.delete("1.0", tk.END)
    salida_palabras.delete("1.0", tk.END)
    salida_errores.delete("1.0", tk.END)
    salida_sintactico.delete("1.0", tk.END)
    salida_semantico.delete("1.0", tk.END)

# Configuración de la ventana principal
root = tk.Tk()
root.title("Analizador Léxico, Sintáctico y Semántico")
root.geometry("900x800")

# Frame para botones
frame_botones = tk.Frame(root)
frame_botones.pack(pady=10)

# Botones
btn_cargar = tk.Button(frame_botones, text="Cargar Archivo", command=cargar_archivo)
btn_cargar.pack(side=tk.LEFT, padx=5)

btn_guardar = tk.Button(frame_botones, text="Guardar Archivo", command=guardar_archivo)
btn_guardar.pack(side=tk.LEFT, padx=5)

btn_limpiar = tk.Button(frame_botones, text="Limpiar Entrada", command=limpiar_entrada)
btn_limpiar.pack(side=tk.LEFT, padx=5)

btn_limpiar_todo = tk.Button(frame_botones, text="Limpiar Todo", command=limpiar_todo)
btn_limpiar_todo.pack(side=tk.LEFT, padx=5)

btn_analizar = tk.Button(frame_botones, text="Analizar", command=analizar_codigo, bg="#4CAF50", fg="white")
btn_analizar.pack(side=tk.LEFT, padx=5)

# Frame para código y resultados
frame_principal = tk.Frame(root)
frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# Etiqueta para el área de entrada
lbl_entrada = tk.Label(frame_principal, text="Código fuente:")
lbl_entrada.pack(anchor=tk.W)

# Área de entrada de código
entrada_texto = scrolledtext.ScrolledText(frame_principal, height=15, wrap=tk.WORD, font=("Courier", 10))
entrada_texto.pack(pady=5, fill=tk.BOTH, expand=True)

# Etiqueta para el área de resultados
lbl_resultados = tk.Label(frame_principal, text="Resultados del análisis:")
lbl_resultados.pack(anchor=tk.W)

# Notebook para las pestañas de resultados
notebook = ttk.Notebook(frame_principal)
notebook.pack(pady=5, fill=tk.BOTH, expand=True)

# Frames para cada pestaña
frame_tokens = tk.Frame(notebook)
frame_palabras = tk.Frame(notebook)
frame_errores = tk.Frame(notebook)
frame_sintactico = tk.Frame(notebook)
frame_semantico = tk.Frame(notebook)

# Añadir pestañas al notebook
notebook.add(frame_tokens, text="Tokens")
notebook.add(frame_palabras, text="Palabras Reservadas")
notebook.add(frame_errores, text="Errores Léxicos")
notebook.add(frame_sintactico, text="Análisis Sintáctico")
notebook.add(frame_semantico, text="Análisis Semántico")

# Áreas de salida para cada pestaña
salida_tokens = scrolledtext.ScrolledText(frame_tokens, height=10, wrap=tk.WORD)
salida_tokens.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

salida_palabras = scrolledtext.ScrolledText(frame_palabras, height=10, wrap=tk.WORD)
salida_palabras.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

salida_errores = scrolledtext.ScrolledText(frame_errores, height=10, wrap=tk.WORD)
salida_errores.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

salida_sintactico = scrolledtext.ScrolledText(frame_sintactico, height=10, wrap=tk.WORD)
salida_sintactico.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

salida_semantico = scrolledtext.ScrolledText(frame_semantico, height=10, wrap=tk.WORD, font=("Courier", 10))
salida_semantico.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

# Barra de estado
barra_estado = tk.Label(root, text="Listo", bd=1, relief=tk.SUNKEN, anchor=tk.W)
barra_estado.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()