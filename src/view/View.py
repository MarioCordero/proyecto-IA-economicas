import tkinter as tk
from tkinter import filedialog

class View:
    def __init__(self, controller):
        self.controller = controller
        self.window = tk.Tk()
        self.window.title("Análisis de datos ECC 2024")

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


    def center_window(self, width=400, height=200):
        """Centra la ventana en la pantalla."""
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def run(self):
        """Inicia la interfaz gráfica."""
        self.window.mainloop()