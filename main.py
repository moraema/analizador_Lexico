import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
from lexico import analisis

def analizar_codigo():
    global errores
    errores = []
    codigo = entrada_texto.get("1.0", tk.END)
   
    tokens_detectados, palabras_reservadas_detectadas, errores_detectados = analisis(codigo)

    salida_tokens.delete("1.0", tk.END)
    salida_tokens.insert(tk.END, "\n".join(tokens_detectados))
    
    salida_palabras.delete("1.0", tk.END)
    salida_palabras.insert(tk.END, "\n".join(palabras_reservadas_detectadas))
    
    salida_errores.delete("1.0", tk.END)
    salida_errores.insert(tk.END, "\n".join(errores_detectados))

def cargar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if archivo:
        with open(archivo, "r") as f:
            entrada_texto.delete("1.0", tk.END)
            entrada_texto.insert(tk.END, f.read())

# Crear interfaz gráfica
root = tk.Tk()
root.title("Analizador Léxico")
root.geometry("700x600")

frame = tk.Frame(root)
frame.pack(pady=10)

btn_cargar = tk.Button(frame, text="Cargar Archivo", command=cargar_archivo)
btn_cargar.pack(side=tk.LEFT, padx=5)

btn_analizar = tk.Button(frame, text="Analizar", command=analizar_codigo)
btn_analizar.pack(side=tk.LEFT, padx=5)

entrada_texto = scrolledtext.ScrolledText(root, height=10)
entrada_texto.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

notebook = ttk.Notebook(root)
notebook.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

frame_tokens = tk.Frame(notebook)
frame_palabras = tk.Frame(notebook)
frame_errores = tk.Frame(notebook)

notebook.add(frame_tokens, text="Tokens Detectados")
notebook.add(frame_palabras, text="Palabras Reservadas")
notebook.add(frame_errores, text="Errores")

salida_tokens = scrolledtext.ScrolledText(frame_tokens, height=10)
salida_tokens.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

salida_palabras = scrolledtext.ScrolledText(frame_palabras, height=10)
salida_palabras.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

salida_errores = scrolledtext.ScrolledText(frame_errores, height=10)
salida_errores.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

root.mainloop()