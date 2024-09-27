import tkinter as tk
from tkinter import filedialog

class FileView:
    def __init__(self, controller):
        self.controller = controller
        self.window = tk.Tk()
        self.window.title("Seleccionar archivo")

        # Definir ancho y alto específicos
        self.window.geometry("400x200")

        self.label_ruta = tk.Label(self.window, text="Ningún archivo seleccionado")
        self.label_ruta.pack(pady=10)

        self.boton_adjuntar = tk.Button(self.window, text="Adjuntar archivo", command=self.controller.select_file)
        self.boton_adjuntar.pack(pady=10)

        self.boton_analizar = tk.Button(self.window, text="Analizar", command=self.controller.analyze_file)
        self.boton_analizar.pack(pady=10)
        self.boton_analizar.pack_forget()  # Ocultar hasta que se seleccione un archivo

    def update_label(self, file_path):
        """Actualiza la etiqueta con la ruta del archivo seleccionado y muestra el botón 'Analizar'."""
        self.label_ruta.config(text=f"Archivo seleccionado: {file_path}")
        self.boton_analizar.pack(pady=10)  # Mostrar el botón 'Analizar'

    def run(self):
        """Inicia la interfaz gráfica."""
        self.window.mainloop()