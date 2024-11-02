import os
import openpyxl
import re
import spacy
from pymongo import MongoClient
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QPushButton
from bs4 import BeautifulSoup
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline


class Model:
    """
    Esta clase es el modelo de la app responsable de la lógica de negocio y de interactuar con la base de datos.
    """
    def __init__(self, controller):
        """
        Este módulo es la constructora del modelo.
        """
        self.controller = controller
        self.client = MongoClient('mongodb://localhost:27017/') # Conexión a la base de datos en el modelo apenas se ejecute el codigo, conectese a la base de datos existente
        self.db = self.client['DB_EEc'] # Crea o se conecta a la base de datos
        self.collection = self.db['proyectos_vigentes'] # Crea o se conecta a la colección
        print("Conexión a la base de datos exitosa!")
        self.nlp = spacy.load("es_core_news_sm")  # Carga el modelo de spaCy para español


    def analyzeData(self):
        """
        Analiza los antecedentes de los proyectos y categoriza la información relevante.
        """
        projects = self.fetchProjects() # Recuperar todos los proyectos vigentes
        antecedentesList = [project.get("antecedentes", "") for project in projects if project.get("antecedentes")]

        # training_data = self.db['datos_entrenamiento']  # Colección que contiene datos para el entrenamiento
        # training_records = training_data.find({}, {"antecedentes": 1, "categoria": 1})  # Extrae antecedentes y categorías
        # training_antecedentes = []
        # training_categories = []

        # for record in training_records:
        #     training_antecedentes.append(record.get("antecedentes", ""))
        #     training_categories.append(record.get("categoria", ""))

        # Normalizar el texto
        combinedAntecedentes = " ".join(antecedentesList)
        normalizedText = self.normalizeText(combinedAntecedentes)
        self.savetoFile(normalizedText, "normalizedText.txt") # Archivo con texto normalizado
        print(f"Nombres propios extraídos {self.extractNames(normalizedText)}")

        # # Fase 1: Entrenamiento del modelo de clasificación
        # X = training_antecedentes  # Textos
        # y = training_categories  # Etiquetas

        # # Dividir los datos
        # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # # Crear y entrenar el modelo
        # self.model = make_pipeline(CountVectorizer(), MultinomialNB())
        # self.model.fit(X_train, y_train)

        # # Evaluar el modelo
        # print("Precisión del modelo:", self.model.score(X_test, y_test))

        # # Fase 2: Análisis detallado por proyecto
        # for project in projects:
        #     projectAntecedents = project.get("antecedentes", "")
        #     normalizedProjectText = self.normalizeText(projectAntecedents)

        #     # Predecir categorías utilizando el modelo entrenado
        #     category_pred = self.model.predict([normalizedProjectText])[0]

        #     # Actualizar cada proyecto en la base de datos con la nueva categoría
        #     self.collection.update_one(
        #         {"_id": project["_id"]},
        #         {
        #             "$set": {
        #                 "categoria_predicha": category_pred
        #             }
        #         }
        #     )
        #     print(f"\nProyecto actualizado: ID {project['_id']}, Categoría predicha: {category_pred}")


    def normalizeText(self, text):
        """
        Normaliza el texto: convierte a minúsculas, elimina puntuación y stopwords.
        """
        # Convertir a minúsculas
        text = text.lower()
        # Eliminar puntuación
        text = re.sub(r'[^\w\s]', '', text)
        # Eliminar palabras irrelevantes
        stopwords = set(spacy.lang.es.stop_words.STOP_WORDS)  # Obtener stopwords de spaCy
        tokens = [word for word in text.split() if word not in stopwords]
        return " ".join(tokens)
    

    def savetoFile(self, normalizedText, fileName):        
        # Abre el archivo en modo escritura
        with open(fileName, 'w', encoding='utf-8') as file:
            # Escribe el texto normalizado en el archivo
            file.write(normalizedText)

    
    def extractNames(self, text):

        capitalizedText = " ".join([word.capitalize() for word in text.split()])
        nlp = spacy.load("es_core_news_sm")  # Asegúrate de tener el modelo en español
        doc = nlp(capitalizedText)
        self.savetoFile(capitalizedText, "capitalizedText.txt") # Archivo con texto normalizado
        properNouns = [ent.text for ent in doc.ents if ent.label_ == "PERSON"] # Extraer nombres propios
        return properNouns


    def extractCategories(self, text):
        """
        Extrae las categorías relevantes de los antecedentes procesados.
        """
        doc = self.nlp(text)
        proposal_type = None
        proposer = None
        
        for ent in doc.ents:
            if ent.label_ == "ORG":  # Si es una organización
                if "universidad" in ent.text or "docente" in ent.text or "estudiante" in ent.text:
                    proposal_type = "Propuesto por Universidad"
                    proposer = ent.text
                    break  # Salir si se encuentra una universidad
                else:
                    proposal_type = "Propuesto por Institución Externa"
                    proposer = ent.text
                    break  # Salir si se encuentra una organización externa
        
        return proposal_type, proposer

    def extractCategoriesGeneral(self, text):
        """
        Extrae las categorías relevantes de los antecedentes procesados.
        """
        doc = self.nlp(text)
        proposal_type = None
        proposer = None
        
        for ent in doc.ents:
            if ent.label_ == "ORG":  # Si es una organización
                if "universidad" in ent.text or "docente" in ent.text or "estudiante" in ent.text:
                    proposal_type = "Propuesto por Universidad"
                    proposer = ent.text
                    break  # Salir si se encuentra una universidad
                else:
                    proposal_type = "Propuesto por Institución Externa"
                    proposer = ent.text
                    break  # Salir si se encuentra una organización externa
        
        return proposal_type, proposer


    def addXLSX(self, filePath):
        """
        Procesa y analiza el archivo seleccionado.
        """

        workbook = openpyxl.load_workbook(filePath) # Abrir el archivo XLSX
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
                "antecedentes": BeautifulSoup(str(antecedentes).lower(), "html.parser").get_text(separator=" "), #(lowercase insert)
                #"antecedentes": antecedentes, # (normal insert)
                "poblacion": poblacion,
                "beneficios_ucr": beneficios_ucr,
                "beneficios_poblacion": beneficios_poblacion,
                "evaluacion_proyecto": evaluacion_proyecto,
                "tematicas": tematicas
            }

            # Inserta el proyecto en la base de datos a través del modelo
            inserted_id = self.insertProject(proyecto_data)

            # Imprimir los datos extraídos
            print("\nProyecto encontrado!")
            print(f"Código de inscripción: {codigo_inscripcion}")
            print(f"ID insertado en MongoDB: {inserted_id}")
            print("-" * 40)

        # Actualizar tabla

        
    
    def insertProject(self, project_data):
        """
        Inserta un proyecto en la colección 'proyectos_vigentes'.
        """
        return self.collection.insert_one(project_data).inserted_id


    def fetchData(self):
        """
        Obtiene los datos de la base de datos y los devuelve.
        """
        data = list(self.collection.find())
        return data
    

    def fetchProjects(self):
        """
        Retrieve projects from the database.
        """
        projects = self.collection.find({})
        return [project for project in projects]  # List of dictionaries