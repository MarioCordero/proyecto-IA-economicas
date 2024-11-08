import os
import openpyxl
import re
import spacy
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from pymongo import MongoClient
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QPushButton
from bs4 import BeautifulSoup
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
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

    def analyzeData(self):  # Realizar la predicción de etiquetas en analyzeData
        """
        # Analiza los antecedentes de los proyectos usando la red neuronal
        """
        # ----------------------------------PREPARACIÓN DE DATOS----------------------------------#

        model = load_model("trainedModel.h5") # Cargar el modelo entrenado

        # with open("bancoEtiquetas.txt", "r", encoding="utf-8") as file: # Leer el archivo de etiquetas
        #     bancoEtiquetas = [line.strip() for line in file.readlines()] # Una lista de etiquetas disponibles

        projects = self.fetchProjects() # Obtener todos los proyectos de la base de datos
        antecedentesList = [project.get("antecedentes", "") for project in projects if project.get("antecedentes")] # Obtener solo los antecedentes de los proyectos mostrados
        
        # ----------------------------------ANALISIS DE DATOS----------------------------------#
        # Realizar predicción para cada proyecto en antecedentesList
        texto_proyecto = ["Ejemplo de texto de proyecto para analizar"]
        secuencia_proyecto = self.tokenizer.texts_to_sequences(texto_proyecto)
        texto_proyecto_pad = pad_sequences(secuencia_proyecto, maxlen=100, padding='post', truncating='post')
        predicciones = model.predict(texto_proyecto_pad)
        print("Realizando predicción de etiquetas...")
        
        # Generar etiquetas propuestas en función de la predicción
        etiquetas_propuestas = []
        for i, prediccion in enumerate(predicciones[0]):
            if prediccion > 0.5:  # Umbral para considerar una etiqueta como aplicable
                etiquetas_propuestas.append(etiquetas_disponibles[i])
        print("Etiquetas propuestas:", etiquetas_propuestas)


    def trainModel(self): # Analyze antecedentes
        """
        # Entrena y guarda la red neuronal
        """
        # ----------------------------------PREPARACIÓN DE DATOS----------------------------------#

        # Necesitamos entradas (each antcedente), en este caso antecedentesList, que es un 
        # arreglo en el que cada posición del arreglo es un antecedente a un proyecto  
        projects = self.fetchProjects() # Obtener todos los proyectos de la base de datos
        antecedentesList = [project.get("antecedentes", "") for project in projects if project.get("antecedentes")] # Obtener solo los antecedentes de los proyectos mostrados


        # Necesitamos salidas esperadas (each antecedente), en este caso vamos a tener 
        # que usar alguna lista perviamente analizada por nosotros de respuestas a cada
        # antecedente o posición de arreglo, esas son etiquetas que usaremos para entrenar
        # el modelo, o sea, de los proyectos vistos vamos a entrenar a este modelo. 
        # Definir etiquetas esperadas para cada proyecto en `antecedentesList`
        etiquetasEsperadas = [
            ["Historia del Arte"], ["Cultura Popular"], ["Ministerio de Cultura y Juventud"], ["Educación"], ["Escuela de Artes Plásticas"], ["Universidad de Costa Rica"], ["Instituto de Investigaciones en Arte (IIARTE)"], ["Actividades de Difusión y Extensión Cultural"], ["Teatro Nacional de Costa Rica"],                                                                                                                                                         # Proyecto #1  
            ["Propuesto por institución"], ["Propuesto por profesor"], ["Proyección cultural o artística"], ["Difusión de valores nacionales"], ["Fomento de la colaboración interdisciplinaria"], ["Producción artística anual"], ["Escuelas de la Facultad de Bellas Artes"], ["Obra de Carlos Salazar Herrera"], ["Destinada al público universitario y general"], ["Teatro de Bellas Artes"],                                                                           # Proyecto #2
            ["Propuesto por institución"], ["Proyección cultural o artística"], ["Patrimonio cultural"], ["Patrimonio natural"], ["Extensión cultural"], ["Conciencia y conservación de herencia cultural"], ["Actividades dirigidas a diversos públicos"], ["Uso de plataformas digitales"], ["Convenio de préstamo cultural"], ["Museo Regional"], ["Educación a la comunidad"],                                                                                          # Proyecto #3
            ["Proyección cultural o artística"], ["Extensión cultural"], ["Educación comunitaria"], ["Fomento de apreciación musical"], ["Desarrollo de destrezas musicales"], ["Herencia musical regional"], ["Conciertos comunitarios"], ["Fortalecimiento de lazos culturales"], ["Capacitación de integrantes"], ["Presentaciones en escuelas y colegios"], ["Colaboración interinstitucional"],                                                                        # Proyecto #4
            ["Divulgación cultural"], ["Exposición de expresiones visuales"], ["Promoción de artistas emergentes y consolidados"], ["Espacio alternativo para prácticas culturales"], ["Sensibilización artística"], ["Proyección de quehacer artístico"], ["Participación ciudadana"], ["Descentralización del arte capitalino"], ["Difusión en medios y redes"], ["Alianzas estratégicas"], ["Crecimiento cultural regional"], ["Participación de la Acción Social UCR"]  # Proyecto #5
        ]

        with open( "model/bancoEtiquetas.txt" , "r") as file: # Abrir banco de etiquetas
            etiquetasDisponibles = [line.strip() for line in file if line.strip()]  # Lee y limpia cada línea

        # Convertir etiquetas esperadas a formato binario
        numClasses = len(etiquetasDisponibles) # Número total de categorías que hay en base al banco de palabras
        matrizEtiquetasBinarias = np.zeros((len(etiquetasEsperadas), numClasses)) # Cada fila representa un proyecto, cada columna representa una etiqueta única de etiquetasDisponibles

        for i, etiquetas in enumerate(etiquetasEsperadas): # En la matriz binaria marcar las etiquetas que están en esos proyectos
            for etiqueta in etiquetas:
                if etiqueta in etiquetasDisponibles:
                    matrizEtiquetasBinarias[i][etiquetasDisponibles.index(etiqueta)] = 1

        # Tokenización y cosas necesarias para que la red neuronal pueda hacer las asociaciones correctas
        tokenizer = Tokenizer(num_words=10000)  # Número máximo de palabras
        tokenizer.fit_on_texts(antecedentesList)  # Ajusta el tokenizador con tus datos de texto
        sequences = tokenizer.texts_to_sequences(antecedentesList) # Convertir el texto a secuencias
        maxLength = 100  # Define la longitud máxima de las secuencias
        inputData = pad_sequences(sequences, maxlen=maxLength)


        # CHATGPT
        #
        #
        # tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>") # Tokenización y secuenciación del texto, 10 000 palabras de vocabulario, OOV Out Of Vocabulary, todas las palabras que no estén en las 10 000 más comunes
        # tokenizer.fit_on_texts(antecedentesList) # texts_to_sequences convierte cada texto (en este caso, cada elemento en antecedentesList) en una secuencia de números. Cada número en la secuencia representa una palabra en el texto original
        # textoEntrada = tokenizer.texts_to_sequences(antecedentesList) # onvierte cada texto (en este caso, cada elemento en antecedentesList) en una secuencia de números. Cada número en la secuencia representa una palabra en el texto original, representación numérica para las redes neuronales
        # textoEntrada = pad_sequences(textoEntrada, maxlen=100, padding='post', truncating='post') #  Las secuencias de texto (anteriores) pueden tener longitudes variables; algunos textos son más largos y otros más cortos. pad_sequences ajusta todas las secuencias a una longitud fija (maxlen=100 en este caso) para que sean del mismo tamaño
        # # Convertir etiquetas esperadas a un formato binario
        # etiquetasEsperadas = []
        # for etiqueta in etiquetas:
        #     etiqueta_binaria = [1 if tag in etiqueta else 0 for tag in [
        #         "Propuesto por institución", "Propuesto por profesor", "Proyección cultural o artística",
        #         "Actividades interdisciplinarias", "Cambio de enfoque o dirección",
        #         "Apertura a la comunidad", "Vinculación con la historia del arte"
        #     ]]
        #     etiquetasEsperadas.append(etiqueta_binaria)
        # etiquetasEsperadas = np.array(etiquetasEsperadas)
        #
        #
        # CHATGPT

        # ----------------------------------CREACIÓN DEL MODELO-----------------------------------#

        model = Sequential([
            Embedding( input_dim = 10000 , output_dim = 64 , input_length = maxLength ), # Convierte cada palabra (representada como un número entero) en un vector de características de tamaño output_dim. Este vector es una representación densa que permite al modelo entender relaciones y similitudes entre palabras.
            Bidirectional( LSTM( 64 , return_sequences = True ) ), # Procesa las secuencias de palabras en ambas direcciones, es decir, de inicio a fin y de fin a inicio, para capturar patrones en ambas direcciones. 
            Bidirectional( LSTM( 32 ) ), # Esta segunda capa LSTM bidireccional permite que el modelo refine su interpretación de los patrones en el texto al reducir la secuencia procesada por la primera capa.
            Dense( 32 , activation = 'relu' ), # Esta capa completamente conectada permite al modelo interpretar y capturar patrones más complejos en los datos.
            Dense( numClasses , activation = 'sigmoid' ) # Genera la salida final del modelo, que consiste en la probabilidad de que cada etiqueta esté presente en la entrada.
        ])

        model.compile( # Compilar el modelo
            optimizer   = tf.keras.optimizers.Adam(0.1),
            loss        = 'binary_crossentropy'
        )

        # ---------------------------------- ENTRENAMIENTO DEL MODELO  ---------------------------------- #
        print("Tamaño de inputData:", len(inputData))
        print("Tamaño de matrizEtiquetasBinarias:", len(matrizEtiquetasBinarias))
        historial = model.fit(inputData, matrizEtiquetasBinarias, epochs=1000, verbose=False)  
        print("Entrenamiento completado!")

        # Guardar el modelo entrenado
        model.save("trainedModel.h5")
        print("Modelo guardado en 'trainedModel.h5'!")

        # Graficar la pérdida de entrenamiento
        plt.xlabel("Época")
        plt.ylabel("Pérdida")
        # plt.plot(historial.history["loss"])


        # ---------------------------------- PROPUESTA DE ETIQUETAS NUEVAS ---------------------------------- #
        # CHATGPT
        #
        #
        # texto_proyecto = ["Ejemplo de texto de proyecto para analizar"]  # Ejemplo de entrada # Realizar predicciones en nuevos textos
        # secuencia_proyecto = tokenizer.texts_to_sequences(texto_proyecto)
        # texto_proyecto_pad = pad_sequences(secuencia_proyecto, maxlen=100, padding='post', truncating='post')
        # predicciones = model.predict(texto_proyecto_pad)

        # # Generar etiquetas propuestas en función de la predicción
        # etiquetas_disponibles = [
        #     "Propuesto por institución", "Propuesto por profesor", "Proyección cultural o artística",
        #     "Actividades interdisciplinarias", "Cambio de enfoque o dirección",
        #     "Apertura a la comunidad", "Vinculación con la historia del arte"
        # ]
        # etiquetas_propuestas = []
        # for i, prediccion in enumerate(predicciones[0]):
        #     if prediccion > 0.5:  # Umbral para considerar una etiqueta como aplicable
        #         etiquetas_propuestas.append(etiquetas_disponibles[i])
        # print("Etiquetas propuestas:", etiquetas_propuestas)  # Imprimir etiquetas propuestas para revisión
        #
        #
        # CHATGPT


    def loadWordBank(ruta):
        """
        # Carga banco de palabras que son posibles respuestas a los proyectos
        """
        with open(ruta, 'r') as archivo:
            palabras = [linea.strip() for linea in archivo if linea.strip()]
        return palabras
    

    def savetoFile(self, normalizedText, fileName):        
        """
        # Guardar algun archivo (Variable, Nombre archivo)
        """
        # Abre el archivo en modo escritura
        with open(fileName, 'w', encoding='utf-8') as file:
            # Escribe el texto normalizado en el archivo
            file.write(normalizedText)


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

    def normalizeText(self, text): # UNUSED
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