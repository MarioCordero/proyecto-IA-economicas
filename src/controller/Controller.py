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


    def analyzeFile(self):
        """
        Analiza el archivo seleccionado.
        """
        filePath = self.view.selectFile()
        if  filePath == -1:
            print("No se ha seleccionado ningún archivo para analizar.")
        else:
            print(f"Analizando y añadiendo proyectos del archivo: {filePath}")
            self.model.addXLSX(filePath)
            self.model.analyzeData()

    #
    # Controller logic
    #
    def run(self):
        """
        Inicia la vista.
        """
        self.view.run()
        projects = self.model.fetchData() # Get the data
        self.view.updateTable(projects)
        self.view.landingPage.pushButton.clicked.connect(lambda: self.view.stackedWidget.setCurrentWidget(self.view.databaseExplorer)) # Connect "Empezar" button to show the databaseExplorer page
        # projects = self.model.fetchData() # Get the data
        # self.view.updateTable(projects)
        self.view.databaseExplorer.addAndAnalyzeButton.clicked.connect(self.analyzeFile) # The analize button