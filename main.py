import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
from lexico import analisis
from analizador_sintactico import analizar_sintaxis
from analizador_semantico import analizar_programa
import matplotlib.pyplot as plt
import networkx as nx
import uuid

def formatear_ast(ast, nivel=0):
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


def ast_to_graph(ast, graph=None, parent=None):
    if graph is None:
        graph = nx.DiGraph()

    node_id = str(uuid.uuid4())
    label = ast.get("tipo", "nodo") if isinstance(ast, dict) else str(ast)
    graph.add_node(node_id, label=label)

    if parent:
        graph.add_edge(parent, node_id)

    if isinstance(ast, dict):
        for key, value in ast.items():
            if key != "tipo":
                ast_to_graph(value, graph, node_id)
    elif isinstance(ast, list):
        for item in ast:
            ast_to_graph(item, graph, node_id)

    return graph

def draw_ast(ast):
    graph = ast_to_graph(ast)
    pos = hierarchy_pos(graph, vert_gap=0.5) 


    labels = nx.get_node_attributes(graph, 'label')

    plt.figure(figsize=(18, 12))
    nx.draw(graph, pos, with_labels=True, labels=labels, node_size=3000, node_color="#a6cee3", font_size=9, font_family="monospace", font_weight="bold", arrows=False)
    plt.title("Árbol de Sintaxis Abstracta (AST)", fontsize=14)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    plt.savefig("ast.png")
    plt.close()


def mostrar_tabla_simbolos(resultado_semantico):
    # Crear una nueva ventana para la tabla
    ventana_tabla = tk.Toplevel(root)
    ventana_tabla.title("Tabla de Símbolos Completa")
    ventana_tabla.geometry("1000x600")
    
    # Crear un Frame para la tabla
    frame_tabla = ttk.Frame(ventana_tabla)
    frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    

    tabla = ttk.Treeview(frame_tabla)
    tabla["columns"] = ("ambito", "tipo", "valor", "funcion")
    tabla.column("#0", width=150, minwidth=120)
    tabla.column("ambito", width=100, minwidth=80)
    tabla.column("tipo", width=100, minwidth=80)
    tabla.column("valor", width=200, minwidth=120)
    tabla.column("funcion", width=150, minwidth=100)
    
    tabla.heading("#0", text="Variable", anchor=tk.W)
    tabla.heading("ambito", text="Ámbito", anchor=tk.W)
    tabla.heading("tipo", text="Tipo", anchor=tk.W)
    tabla.heading("valor", text="Valor", anchor=tk.W)
    tabla.heading("funcion", text="Función", anchor=tk.W)
    
    # Añadir scrollbars
    vsb = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
    hsb = ttk.Scrollbar(frame_tabla, orient="horizontal", command=tabla.xview)
    tabla.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    
    # Posicionamiento del grid
    tabla.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')
    
    frame_tabla.grid_columnconfigure(0, weight=1)
    frame_tabla.grid_rowconfigure(0, weight=1)
    

    def agregar_variables(variables, ambito, funcion="", linea=0):
        if variables:
            for var, info in variables.items():
                tipo = info.get("tipo", "desconocido")
                valor = str(info.get("valor", "No inicializado"))
                tabla.insert("", tk.END, text=var, 
                            values=(ambito, tipo, valor, funcion, linea))


    if "ast" in resultado_semantico and "funciones" in resultado_semantico["ast"]:
        for funcion in resultado_semantico["ast"]["funciones"]:
            nombre_func = funcion.get("nombre", "")
            
           
            tabla.insert("", tk.END, text=nombre_func, 
                        values=("Función", "function", "-", "-", "-"))
            
           
            variables_locales = {}
            for inst in funcion.get("instrucciones", []):
                if isinstance(inst, dict) and inst.get("tipo") == "declaracion_variable":
                    nombre_var = inst.get("nombre", "")
                    tipo = "any"  
                    valor = "No inicializado"
                    
                   
                    if inst.get("valor") is not None:
                        if isinstance(inst["valor"], dict):
                            tipo = inst["valor"].get("tipo", "any")
                            valor = inst["valor"].get("valor", "No inicializado")
                    
                    variables_locales[nombre_var] = {"tipo": tipo, "valor": valor}
            
            # Añadir las variables encontradas
            if variables_locales:
                agregar_variables(variables_locales, "Local", nombre_func)
    
    # Añadir botones adicionales
    frame_botones = ttk.Frame(ventana_tabla)
    frame_botones.pack(pady=10)
    
    btn_cerrar = ttk.Button(frame_botones, text="Cerrar", command=ventana_tabla.destroy)
    btn_cerrar.pack(side=tk.LEFT, padx=5)


def hierarchy_pos(G, root=None, width=1.0, vert_gap=0.2, vert_loc=0, xcenter=0.5):
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        root = list(G.nodes)[0]

    def _hierarchy_pos(G, root, left, right, vert_loc, xcenter, pos=None, parent=None):
        if pos is None:
            pos = {}
        pos[root] = (xcenter, vert_loc)
        neighbors = list(G.successors(root))
        if neighbors:
            dx = (right - left) / len(neighbors)
            next_x = left + dx / 2
            for neighbor in neighbors:
                pos = _hierarchy_pos(G, neighbor, next_x - dx / 2, next_x + dx / 2, vert_loc - vert_gap, next_x, pos, root)
                next_x += dx
        return pos

    return _hierarchy_pos(G, root, 0, width, vert_loc, xcenter)


tabla_simbolos_btn = None
ultimo_resultado_semantico = None

# === Análisis principal ===
def analizar_codigo():
    global tabla_simbolos_btn, ultimo_resultado_semantico
    
    codigo = entrada_texto.get("1.0", tk.END).strip()

    salida_tokens.delete("1.0", tk.END)
    salida_palabras.delete("1.0", tk.END)
    salida_errores.delete("1.0", tk.END)
    salida_sintactico.delete("1.0", tk.END)
    salida_semantico.delete("1.0", tk.END)
    
   
    if tabla_simbolos_btn is not None:
        tabla_simbolos_btn.pack_forget()

    tokens_detectados, palabras_reservadas_detectadas, errores_detectados = analisis(codigo)

    salida_tokens.insert(tk.END, "\n".join(tokens_detectados))
    salida_palabras.insert(tk.END, "\n".join(palabras_reservadas_detectadas))
    salida_errores.insert(tk.END, "\n".join(errores_detectados))

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

    try:
        resultado_semantico = analizar_programa(codigo)
        ultimo_resultado_semantico = resultado_semantico 

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

           
            if tabla_simbolos_btn is None:
                tabla_simbolos_btn = ttk.Button(frame_semantico, text="Ver Tabla de Símbolos", 
                                               command=lambda: mostrar_tabla_simbolos(resultado_semantico))
            else:
                tabla_simbolos_btn.config(command=lambda: mostrar_tabla_simbolos(resultado_semantico))
            
            tabla_simbolos_btn.pack(pady=5)

            salida_semantico.insert(tk.END, "\n=== ÁRBOL DE SINTAXIS ===\n")
            ast_formateado = formatear_ast(resultado_semantico["ast"])
            salida_semantico.insert(tk.END, ast_formateado)
    except Exception as e:
        salida_semantico.insert(tk.END, f"Error en análisis semántico: {str(e)}\n")
        import traceback
        salida_semantico.insert(tk.END, f"\nDetalles:\n{traceback.format_exc()}")

def cargar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if archivo:
        with open(archivo, "r") as f:
            entrada_texto.delete("1.0", tk.END)
            entrada_texto.insert(tk.END, f.read())

def limpiar_entrada():
    entrada_texto.delete("1.0", tk.END)

def limpiar_todo():
    global tabla_simbolos_btn
    
    entrada_texto.delete("1.0", tk.END)
    salida_tokens.delete("1.0", tk.END)
    salida_palabras.delete("1.0", tk.END)
    salida_errores.delete("1.0", tk.END)
    salida_sintactico.delete("1.0", tk.END)
    salida_semantico.delete("1.0", tk.END)
    
    # Ocultar el botón si existe
    if tabla_simbolos_btn is not None:
        tabla_simbolos_btn.pack_forget()

# ==== Interfaz Tkinter ====
root = tk.Tk()
root.title("Analizador Léxico, Sintáctico y Semántico")
root.geometry("900x800")

frame_botones = tk.Frame(root)
frame_botones.pack(pady=10)

btn_cargar = tk.Button(frame_botones, text="Cargar Archivo", command=cargar_archivo)
btn_cargar.pack(side=tk.LEFT, padx=5)

btn_limpiar = tk.Button(frame_botones, text="Limpiar Entrada", command=limpiar_entrada)
btn_limpiar.pack(side=tk.LEFT, padx=5)

btn_limpiar_todo = tk.Button(frame_botones, text="Limpiar Todo", command=limpiar_todo)
btn_limpiar_todo.pack(side=tk.LEFT, padx=5)

btn_analizar = tk.Button(frame_botones, text="Analizar", command=analizar_codigo, bg="#4CAF50", fg="white")
btn_analizar.pack(side=tk.LEFT, padx=5)

frame_principal = tk.Frame(root)
frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

lbl_entrada = tk.Label(frame_principal, text="Código fuente:")
lbl_entrada.pack(anchor=tk.W)

entrada_texto = scrolledtext.ScrolledText(frame_principal, height=15, wrap=tk.WORD, font=("Courier", 10))
entrada_texto.pack(pady=5, fill=tk.BOTH, expand=True)

lbl_resultados = tk.Label(frame_principal, text="Resultados del análisis:")
lbl_resultados.pack(anchor=tk.W)

notebook = ttk.Notebook(frame_principal)
notebook.pack(pady=5, fill=tk.BOTH, expand=True)

frame_tokens = tk.Frame(notebook)
frame_palabras = tk.Frame(notebook)
frame_errores = tk.Frame(notebook)
frame_sintactico = tk.Frame(notebook)
frame_semantico = tk.Frame(notebook)

notebook.add(frame_tokens, text="Tokens")
notebook.add(frame_palabras, text="Palabras Reservadas")
notebook.add(frame_errores, text="Errores Léxicos")
notebook.add(frame_sintactico, text="Análisis Sintáctico")
notebook.add(frame_semantico, text="Análisis Semántico")

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

barra_estado = tk.Label(root, text="Listo", bd=1, relief=tk.SUNKEN, anchor=tk.W)
barra_estado.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()