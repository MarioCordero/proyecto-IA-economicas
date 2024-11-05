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
import tensorflow as tf
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential


class Model:
    """
    # Esta clase es el modelo de la app responsable de la lógica de negocio y de interactuar con la base de datos.
    """
    def __init__(self, controller):
        """
        # Este módulo es la constructora del modelo.
        """
        self.controller = controller
        self.client = MongoClient('mongodb://localhost:27017/') # Conexión a la base de datos en el modelo apenas se ejecute el codigo, conectese a la base de datos existente
        self.db = self.client['DB_EEc'] # Crea o se conecta a la base de datos
        self.collection = self.db['proyectos_vigentes'] # Crea o se conecta a la colección
        print("Conexión a la base de datos exitosa!")
        self.nlp = spacy.load("es_core_news_md")  # Carga el modelo de spaCy para español
        self.tokenizer = Tokenizer(num_words=10000)  # Puedes ajustar el número de palabras
        self.max_length = 100  # Longitud máxima para el padding


    def analyzeData(self): # Analyze antecedentes
        """
        # Analiza los antecedentes de los proyectos y entrena la red neuronal.
        """
        # ----------------------------------ENTRENAMIENTO DEL MODELO----------------------------------#
        # Necesitamos entradas (each antcedente), en este caso antecedentesList, que es un 
        # arreglo en el que cada posición del arreglo es un antecedente a un proyecto  
        projects = self.fetchProjects() # Obtener todos los proyectos de la base de datos
        antecedentesList = [project.get("antecedentes", "") for project in projects if project.get("antecedentes")] # Obtener solo los antecedentes de los proyectos mostrados


        # Necesitamos salidas esperadas (each antecedente), en este caso vamos a tener 
        # que usar alguna lista perviamente analizada por nosotros de respuestas a cada
        # antecedente o posición de arreglo

        etiquetas = [
            "Propuesto por institución",
            "Propuesto por profesor",
            "Proyección cultural o artística",
            "Actividades interdisciplinarias",
            "Cambio de enfoque o dirección",
            "Apertura a la comunidad",
            "Vinculación con la historia del arte"
        ]

        # Etiquetas ficticias (0 o 1) para entrenamiento de ejemplo; en un caso real, deberías tener etiquetas reales.
        labels = [0 if i % 2 == 0 else 1 for i in range(len(antecedentesList))]
        
        # Preparar datos y etiquetas
        padded_sequences = self.prepareData(antecedentesList)
        X_train, X_test, y_train, y_test = train_test_split(padded_sequences, labels, test_size=0.2, random_state=42)
        
        # Llamada a buildModel para crear la arquitectura de la red
        model = self.buildModel()
        
        # Entrenamiento del modelo
        model.fit(X_train, y_train, epochs=5, batch_size=32, validation_data=(X_test, y_test))
        
        # Guardar el modelo entrenado
        model.save("trained_model.h5")
        print("Entrenamiento completado y modelo guardado en 'trained_model.h5'")


    def normalizeText(self, text):
        """
        # Normaliza el texto: convierte a minúsculas, elimina puntuación y stopwords.
        """
        # Convertir a minúsculas
        text = text.lower()
        # Eliminar puntuación
        text = re.sub(r'[^\w\s]', '', text)
        # Eliminar palabras irrelevantes
        stopwords = self.nlp.Defaults.stop_words
        tokens = [word for word in text.split() if word not in stopwords]
        return " ".join(tokens)
    

    def savetoFile(self, normalizedText, fileName):        
        """
        # Guardar algun archivo (Variable, Nombre archivo)
        """
        # Abre el archivo en modo escritura
        with open(fileName, 'w', encoding='utf-8') as file:
            # Escribe el texto normalizado en el archivo
            file.write(normalizedText)
    
    def prepareData(self, antecedentes_list):
        """
        # Tokeniza y prepara los datos de texto para el análisis.
        """
        self.tokenizer.fit_on_texts(antecedentes_list) # Tokenizar el texto

        sequences = self.tokenizer.texts_to_sequences(antecedentes_list) 

        padded_sequences = pad_sequences(sequences, maxlen=self.max_length, padding='post')
        
        return padded_sequences
    
    def buildModel(self):
        """
        # Crea un modelo secuencial de Keras con una capa LSTM para analizar texto.
        """
        model = Sequential([
            Embedding(input_dim=10000, output_dim=64, input_length=self.max_length),
            Bidirectional(LSTM(64, return_sequences=True)),
            Bidirectional(LSTM(32)),
            Dense(32, activation='relu'),
            Dense(1, activation='sigmoid')  # Cambiar a 'softmax' si tienes múltiples categorías
        ])
        
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        return model
    
    def analyzeAllAntecedentes(self, antecedentes_list):
        """
        # Analiza todo el texto combinado de la columna "antecedentes".
        """
        combined_text = " ".join(antecedentes_list)
        padded_data = self.prepareData([combined_text])

        # Crear el modelo y entrenar en el texto combinado (si tienes etiquetas para entrenamiento)
        model = self.buildModel()
        # model.fit(padded_data, labels)  # Necesitas etiquetas si estás entrenando supervisadamente

        # Para predicción o embeddings:
        embedding_output = model.predict(padded_data)
        print(f"Embedding de todo el texto combinado: {embedding_output}")


    def analyzeEachAntecedente(self, antecedentes_list):
        """
        # Analiza cada texto individual en la columna "antecedentes".
        """
        padded_data = self.prepareData(antecedentes_list)
        model = self.buildModel()
        
        # Para cada texto individual
        for idx, sequence in enumerate(padded_data):
            prediction = model.predict(sequence.reshape(1, -1))
            print(f"Predicción para el proyecto {idx + 1}: {prediction}")


    def addXLSX(self, filePath):
        """
        # Añade archivos del documento seleccionado.
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
                "antecedentes": BeautifulSoup(str(antecedentes), "html.parser").get_text(separator=" "),
                #"antecedentes": BeautifulSoup(str(antecedentes).lower(), "html.parser").get_text(separator=" "), #(lowercase insert)
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
            self.controller.updateTable()  # Llama a updateTable desde el controlador


    def insertProject(self, project_data):
        """
        # Inserta un proyecto en la colección 'proyectos_vigentes'.
        """
        return self.collection.insert_one(project_data).inserted_id


    def fetchData(self):
        """
        # Obtiene los datos de la base de datos y los devuelve.
        """
        data = list(self.collection.find())
        return data
    
    def fetchProjects(self):
        """
        # Retrieve projects from the database.
        """
        projects = self.collection.find({})
        return [project for project in projects]  # List of dictionaries

    def clearDatabase(self):
        """
        # Elimina todas las entradas de la colección 'proyectos_vigentes' en la base de datos.
        """
        self.db.proyectos_vigentes.drop()
        print("Todas las entradas en 'proyectos_vigentes' han sido eliminadas.")
        self.controller.updateTable()  # Llama a updateTable desde el controlador

    def extractNames(self, text): # UNUSED
        """
        # Func
        """
        capitalizedText = " ".join([word.capitalize() for word in text.split()])
        doc = self.nlp(capitalizedText)
        # self.savetoFile(capitalizedText, "capitalizedText.txt") # Archivo con texto normalizado
        properNouns = [ent.text for ent in doc.ents if ent.label_ == "PERSON"] # Extraer nombres propios
        return properNouns