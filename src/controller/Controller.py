import os
import openpyxl
from PyQt5.QtWidgets import QFileDialog
from view.View import View
from model.Model import Model

class Controller:
    """
    Constructor del Controller
    """
    def __init__(self):
        """
        Inicializa la vista y el modelo.
        """
        self.view = View(self)  # Construye la vista y pasa la controladora por parámetro
        self.model = Model(self)  # Construye el modelo y pasa la controladora por parámetro
        self.file_path = None  # Inicializa la ruta del archivo vacía
        print("Controladora construida!")

    def select_file(self):
        """
        Muestra el cuadro de diálogo para seleccionar un archivo y actualiza la vista.
        """
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self.view, "Seleccionar archivo", "", "Archivos Excel (*.xlsx *.xls);;Todos los archivos (*)", options=options)

        if file_path and os.path.isfile(file_path):
            self.file_path = file_path  # Guarda la ruta del archivo seleccionado
            self.view.update_label(file_path)  # Actualiza la vista
        else:
            print("No se seleccionó ningún archivo o el archivo no existe.")

    def analyze_file(self):
        """
        Analiza el archivo seleccionado.
        """
        if self.file_path:
            print(f"Analizando el archivo: {self.file_path}")
            self.analyze_data(self.file_path)
        else:
            print("No se ha seleccionado ningún archivo para analizar.")

    def analyze_data(self, file_path):
        """
        Procesa y analiza el archivo seleccionado.
        """
        print(f"Procesando y analizando los datos del archivo {file_path}...")

        # Abrir el archivo XLSX
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active  # Usamos la primera hoja

        # Iterar sobre las filas y extraer los datos
        for row in sheet.iter_rows(min_row=2, values_only=True):  # min_row=2 para saltar la cabecera
            if all(cell is None for cell in row):
                continue

            # Extraer los valores de la fila y organizarlos
            codigo_inscripcion, nombre, fecha_inicio, fecha_fin, area_academica, comunidades_indigenas, antecedentes, poblacion, \
            beneficios_ucr, beneficios_poblacion, evaluacion_proyecto, tematicas = row

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

            # Inserta el proyecto en la base de datos a través del modelo
            inserted_id = self.model.insert_project(proyecto_data)

            # Imprimir los datos extraídos
            print("\nProyecto encontrado!")
            print(f"Código de inscripción: {codigo_inscripcion}")
            print(f"ID insertado en MongoDB: {inserted_id}")
            print("-" * 40)

    def run(self):
        """
        Inicia la vista.
        """
        self.view.run()