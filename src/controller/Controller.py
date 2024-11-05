from view.View import View
from model.Model import Model

class Controller:

    #
    # Constructor del Controller
    #
    def __init__(self):
        """
        Inicializa la vista y el modelo.
        """
        self.view = View(self)  # Construye la vista y pasa la controladora por parámetro
        self.model = Model(self)  # Construye el modelo y pasa la controladora por parámetro
        print("Controladora construida!")

    def updateTable(self):
        """
        Actualiza la tabla en la vista con los datos obtenidos del modelo.
        """
        projects = self.model.fetchData()  # Obtiene los datos de la base de datos
        self.view.updateTable(projects)  # Actualiza la tabla en la vista


    def addData(self):
        """
        Analiza el archivo seleccionado.
        """
        filePath = self.view.selectFile()
        if  filePath == -1:
            print("No se ha seleccionado ningún archivo para analizar.")
        else:
            print(f"Analizando y añadiendo proyectos del archivo: {filePath}")
            self.model.addXLSX(filePath)

    def analyzeProyects(self):
        """
        Analiza el archivo seleccionado.
        """
        self.model.analyzeData()

    #
    # Controller logic
    #
    def run(self):
        """
        # Inicia la vista.
        """
        self.view.run()
        self.updateTable()  # Actualiza la tabla al iniciar
        self.view.landingPage.pushButton.clicked.connect(
            lambda: self.view.stackedWidget.setCurrentWidget(self.view.databaseExplorer) # Connect "Empezar" button to show the databaseExplorer page
        )
        self.view.databaseExplorer.addDataButton.clicked.connect(
            self.addData # The add data button
        )
        self.view.databaseExplorer.analyzeProyectsButton.clicked.connect(
            self.analyzeProyects # The analize button
        )
        self.view.databaseExplorer.clearDatabaseButton.clicked.connect(
            self.model.clearDatabase  # Botón para borrar todas las entradas de la base de datos
        )