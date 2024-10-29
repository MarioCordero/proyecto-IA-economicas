from pymongo import MongoClient

class Model:
    """
    Esta clase es el modelo de la app responsable de la lógica de negocio y de interactuar con la base de datos.
    """
    def __init__(self, controller):
        """
        Este módulo es la constructora del modelo.
        """
        self.controller = controller
        self.file_path = None
        self.client = MongoClient('mongodb://localhost:27017/') # Conexión a la base de datos en el modelo apenas se ejecute el codigo, conectese a la base de datos existente
        self.db = self.client['DB_EEc'] # Crea o se conecta a la base de datos
        self.collection = self.db['proyectos_vigentes'] # Crea o se conecta a la colección
        print("Conexión a la base de datos exitosa!")

    def get_user(self, user_id):
        # Método para obtener un usuario por su ID
        return self.collection.find_one({"_id": user_id})
    
    def insert_project(self, project_data):
        """
        Inserta un proyecto en la colección 'proyectos_vigentes'.
        """
        return self.collection.insert_one(project_data).inserted_id
    
    def insert_user(self, user_data):
        # Método para insertar un usuario
        return self.collection.insert_one(user_data).inserted_id

    def fetchProjects(self):
        """
        Retrieve projects from the database.
        """
        projects = self.collection.find({})
        return [project for project in projects]  # List of dictionaries

    def set_file_path(self, path):
        self.file_path = path

    def get_file_path(self):
        return self.file_path