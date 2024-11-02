from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QPushButton, QFileDialog, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5 import uic

class View(QMainWindow):

    #
    # Constructor method
    #
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.initUI()  # Initialize the User Interface


    #
    # UI initializer method
    #
    def initUI(self):
        loadUi( 'view/mainWindow.ui' , self )  # Load mainWindow.ui, designed in Qt Designer

        self.centerWindow() # Center the main window on the screen
        
        self.landingPage = QMainWindow() #Initiate the landingPage first, so the landingPage now gonna be a main window
        loadUi( 'view/landingPage.ui' , self.landingPage ) # Load from the UI file
        self.stackedWidget.addWidget(self.landingPage) # Add landingPage to the stackedWidget
        self.stackedWidget.setCurrentWidget( self.landingPage ) # set the landingPage to the main window on the stackedWidget]

        # Load and add the databaseExplorer page
        self.databaseExplorer = QMainWindow()  # Instantiate the databaseExplorer window
        uic.loadUi('view/databaseExplorer.ui', self.databaseExplorer)  # Load its UI layout
        self.stackedWidget.addWidget(self.databaseExplorer)  # Add to the stacked widget

    #
    # Center the main window on the screen
    #
    def centerWindow(self):
        screen = QApplication.primaryScreen().availableGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen.center())
        self.move(window_geometry.topLeft())

    def selectFile(self):
        """
        Abre un diálogo para seleccionar un archivo y pasa la ruta al controlador.
        """
        filePath, _ = QFileDialog.getOpenFileName(None, "Seleccionar archivo", "", "Archivos de Excel (*.xlsx)")
        if filePath:
            return filePath
        
        return -1


    def updateTable(self, projects):
        """
        Limpia y llena el `tableWidget` con los datos del proyecto.
        """
        table = self.databaseExplorer.tableWidget
        table.clear()

        # Define headers
        headers = ["Codigo Inscripcion", "Nombre", "Analisis de Proyecto"]
        table.setRowCount(len(projects))
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)

        for row, project in enumerate(projects):
            # Llena las columnas de datos
            table.setItem(row, 0, QTableWidgetItem(str(project.get("codigo_inscripcion", ""))))
            table.setItem(row, 1, QTableWidgetItem(str(project.get("nombre", ""))))
            
            # Crea y agrega el botón "Ver Análisis"
            analysisButton = QPushButton("Ver Análisis")
            analysisButton.clicked.connect(lambda _, proj=project: self.controller.showProjectDetails(proj))
            table.setCellWidget(row, 2, analysisButton)

    def run(self):
        self.show()