import tkinter as tk
from tkinter import filedialog

def seleccionar_archivo(ventana, callback):
    ruta_archivo = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=(("Archivos Excel", "*.xlsx *.xls"), ("Todos los archivos", "*.*"))
    )
    if ruta_archivo:
        label_ruta.config(text=f"Archivo seleccionado: {ruta_archivo}")
        callback(ruta_archivo)  # Llama al callback con la ruta del archivo
        ventana.destroy()  # Cierra la ventana
    return ruta_archivo

def initializeUI(callback):
    """
    Inicializa la interfaz de usuario y pasa la ruta del archivo seleccionado
    a la función `callback`. La ventana se cierra después de seleccionar.
    """
    ventana = tk.Tk()
    ventana.title("Seleccionar archivo")

    # Crear un botón para abrir el cuadro de diálogo
    boton_adjuntar = tk.Button(ventana, text="Adjuntar archivo", command=lambda: seleccionar_archivo(ventana, callback))
    boton_adjuntar.pack(pady=10)

    # Crear una etiqueta para mostrar la ruta del archivo seleccionado
    global label_ruta
    label_ruta = tk.Label(ventana, text="Ningún archivo seleccionado")
    label_ruta.pack(pady=10)

    ventana.mainloop()