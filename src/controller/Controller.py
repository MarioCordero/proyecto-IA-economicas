import os
import tkinter as tk
import openpyxl
from tkinter import filedialog
from view.View import View
from model.Model import Model

class Controller:
    """
    Constructor de cointroller
    """

    def __init__(self):
        """
        Constructora de la clase (self) es una referencia de la clase a si misma para empezar a construirse
        """
        self.view = View(self) # Construir en la controladora la vista y enviarle la controladora por parámetro
        self.model = Model(self) # Construir en la controladora el modelo y enviarle la controladora por parámetro
        self.file_path = None # Inicializar la ruta del archivo vacía
        print("Controladora construida!")


    def select_file(self):
        """
        Muestra el cuadro de diálogo para seleccionar un archivo, actualiza la vista con la ruta seleccionada.
        """ 
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=(("Archivos Excel", "*.xlsx *.xls"), ("Todos los archivos", "*.*"))
        )
        
        if file_path and os.path.isfile(file_path):
            self.file_path = file_path  # Guardar la ruta del archivo seleccionado
            self.view.update_label(file_path)  # Actualizar la vista
        else:
            print("No se seleccionó ningún archivo o el archivo no existe.")


    def analyze_file(self):
        """
        Analiza el archivo seleccionado. Esta función se ejecuta cuando el usuario hace clic en el botón 'Analizar'.
        """
        if self.file_path:
            print(f"Analizando el archivo: {self.file_path}")
            self.analyze_data(self.file_path)
        else:
            print("No se ha seleccionado ningún archivo para analizar.")


    def analyze_data(self, file_path):
        """
        Lógica para procesar y analizar el archivo seleccionado.
        Extrae toda la información del XLSX y la inserta en la base de datos.
        """
        print(f"Procesando y analizando los datos del archivo {file_path}...")
        
        # Abrir el archivo XLSX
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active  # Usamos la primera hoja

        # Iterar sobre las filas y extraer los datos
        for row in sheet.iter_rows(min_row=2, values_only=True):  # min_row=2 para saltar la cabecera
            # Ignorar filas completamente vacías
            if all(cell is None for cell in row):
                continue
            
            # Asignar cada celda de la fila a una variable
            codigo_inscripcion, nombre, fecha_inicio, fecha_fin, area_academica, comunidades_indigenas, antecedentes, poblacion, \
            beneficios_ucr, beneficios_poblacion, evaluacion_proyecto, tematicas = row
            
            # Crear un diccionario con los datos para insertar en la base de datos
            proyecto_data = {
                "codigo_inscripcion": codigo_inscripcion,
                "nombre": nombre,
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin,
                "area_academica": area_academica,
                "comunidades_indigenas": comunidades_indigenas,
                "antecedentes": antecedentes,
                "poblacion": poblacion,
                "beneficios_ucr": beneficios_ucr,
                "beneficios_poblacion": beneficios_poblacion,
                "evaluacion_proyecto": evaluacion_proyecto,
                "tematicas": tematicas
            }
            
            # Insertar el proyecto en la base de datos a través del modelo
            inserted_id = self.model.insert_project(proyecto_data)
            
            # Imprimir los datos extraídos
            print("\nProyecto encontrado!")
            print(f"Código de inscripción: {codigo_inscripcion}")
            print(f"ID insertado en MongoDB: {inserted_id}")
            print("-" * 40)
            # Borrar en mongosh "db.proyectos_vigentes.deleteMany({})"


    def run(self):
        """
        Inicia la vista (la interfaz gráfica).
        """
        self.view.run()