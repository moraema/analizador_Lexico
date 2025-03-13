import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
from lexico import analisis
from analizador_sintactico import analizar_sintaxis  # Importa la función del analizador sintáctico

def analizar_codigo():

    codigo = entrada_texto.get("1.0", tk.END).strip()
   # codigo_modificado = codigo.replace("[", "\n[")
    # Análisis léxico
    tokens_detectados, palabras_reservadas_detectadas, errores_detectados = analisis(codigo)
    
    # Análisis sintáctico
    try:
        resultado_sintactico, errores_sintacticos = analizar_sintaxis(codigo)
        
        # Limpiar área de texto de análisis sintáctico antes de insertar nuevos datos
        salida_sintactico.delete("1.0", tk.END)

        if errores_sintacticos:
            for error in errores_sintacticos:
                salida_sintactico.insert(tk.END, f"Error: {error}\n")
        else:
            for regla in resultado_sintactico:
                salida_sintactico.insert(tk.END, f"Regla aplicada: {regla}\n")
    except Exception as e:
        salida_sintactico.delete("1.0", tk.END)
        salida_sintactico.insert(tk.END, f"Error: {str(e)}\n")
    
    # Mostrar resultados en la interfaz
    salida_tokens.delete("1.0", tk.END)
    salida_tokens.insert(tk.END, "\n".join(tokens_detectados))
    
    salida_palabras.delete("1.0", tk.END)
    salida_palabras.insert(tk.END, "\n".join(palabras_reservadas_detectadas))
    
    salida_errores.delete("1.0", tk.END)
    salida_errores.insert(tk.END, "\n".join(errores_detectados))

def cargar_archivo():
    """ Permite cargar un archivo de texto en la entrada de código. """
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if archivo:
        with open(archivo, "r") as f:
            entrada_texto.delete("1.0", tk.END)
            entrada_texto.insert(tk.END, f.read())

# Crear interfaz gráfica
root = tk.Tk()
root.title("Analizador Léxico y Sintáctico")
root.geometry("700x600")

frame = tk.Frame(root)
frame.pack(pady=10)

btn_cargar = tk.Button(frame, text="Cargar Archivo", command=cargar_archivo)
btn_cargar.pack(side=tk.LEFT, padx=5)

btn_analizar = tk.Button(frame, text="Analizar", command=analizar_codigo)
btn_analizar.pack(side=tk.LEFT, padx=5)

entrada_texto = scrolledtext.ScrolledText(root, height=10)
entrada_texto.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

# Pestañas
notebook = ttk.Notebook(root)
notebook.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

frame_tokens = tk.Frame(notebook)
frame_palabras = tk.Frame(notebook)
frame_errores = tk.Frame(notebook)
frame_sintactico = tk.Frame(notebook)

notebook.add(frame_tokens, text="Tokens Detectados")
notebook.add(frame_palabras, text="Palabras Reservadas")
notebook.add(frame_sintactico, text="Análisis Sintáctico")

# Áreas de salida
salida_tokens = scrolledtext.ScrolledText(frame_tokens, height=10)
salida_tokens.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

salida_palabras = scrolledtext.ScrolledText(frame_palabras, height=10)
salida_palabras.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

salida_errores = scrolledtext.ScrolledText(frame_errores, height=10)
salida_errores.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)


salida_sintactico = scrolledtext.ScrolledText(frame_sintactico, height=10)
salida_sintactico.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

root.mainloop()
