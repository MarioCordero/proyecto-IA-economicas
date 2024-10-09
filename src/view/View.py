import tkinter as tk
from tkinter import filedialog

class View:

    #    """
    #    Constructor del View
    #    """
    def __init__(self, controller):
        self.controller = controller
        self.window = tk.Tk()
        self.window.title("Análisis de datos ECC 2024")

        self.center_window(400, 200) # Centrar la ventana con 400px x 200px

        self.label_ruta = tk.Label(self.window, text="Ningún archivo seleccionado")
        self.label_ruta.pack(pady=10)

        self.boton_adjuntar = tk.Button(self.window, text="Adjuntar archivo", command=self.controller.select_file)
        self.boton_adjuntar.pack(pady=10)

        self.boton_analizar = tk.Button(self.window, text="Analizar", command=self.controller.analyze_file)
        self.boton_analizar.pack(pady=10)

        self.boton_analizar.pack_forget() # Ocultar hasta que se seleccione un archivo


    #    """
    #    Centra la ventana en la pantalla
    #    """
    def center_window(self, width=400, height=200):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    #    """
    #    Actualiza la etiqueta con la ruta del archivo seleccionado y muestra el botón 'Analizar'
    #    """
    def update_label(self, file_path):
        self.label_ruta.config(text=f"Archivo seleccionado: {file_path}")
        self.boton_analizar.pack(pady=10)  # Mostrar el botón 'Analizar'


    #    """
    #    Inicia la interfaz gráfica
    #    """
    def run(self):
        self.window.mainloop()