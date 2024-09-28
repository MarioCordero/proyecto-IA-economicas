import os
import tkinter as tk
from tkinter import filedialog
from view.fileView import FileView

class FileController:
    # """
    #    Inicializa la controladora creando la vista y configurando los manejadores de eventos.
    #    """
    def __init__(self):
        # Crear la vista y pasar esta instancia como su controlador
        self.view = FileView(self)
        self.file_path = None

    #    """
    #    Muestra el cuadro de diálogo para seleccionar un archivo, actualiza la vista con la ruta seleccionada.
    #    """
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=(("Archivos Excel", "*.xlsx *.xls"), ("Todos los archivos", "*.*"))
        )
        
        if file_path and os.path.isfile(file_path):
            self.file_path = file_path  # Guardar la ruta del archivo seleccionado
            self.view.update_label(file_path)  # Actualizar la vista
        else:
            print("No se seleccionó ningún archivo o el archivo no existe.")

    #    """
    #    Analiza el archivo seleccionado. Esta función se ejecuta cuando el usuario hace clic en el botón 'Analizar'.
    #    """
    def analyze_file(self):
        if self.file_path:
            print(f"Analizando el archivo: {self.file_path}")
            self.analyze_data(self.file_path)
        else:
            print("No se ha seleccionado ningún archivo para analizar.")

    #    """
    #    Lógica para procesar y analizar el archivo seleccionado.
    #    """
    def analyze_data(self, file_path):
        print(f"Procesando y analizando los datos del archivo {file_path}...")
        # Aquí iría la lógica de IA o procesamiento de datos

    #    """
    #    Inicia la vista (la interfaz gráfica).
    #    """
    def run(self):
        self.view.run()