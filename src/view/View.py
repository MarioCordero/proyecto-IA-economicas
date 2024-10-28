from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

class View(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.initUI()  # Initialize the User Interface

    def initUI(self):
        loadUi( 'view/mainWindow.ui' , self )  # Load mainWindow.ui, designed in Qt Designer
        
        self.landingPage = QMainWindow() #Initiate the landingPage first, so the landingPage now gonna be a main window
        loadUi( 'view/landingPage.ui' , self.landingPage ) # Load from the UI file
        self.stackedWidget.addWidget(self.landingPage) # Add landingPage to the stackedWidget
        self.stackedWidget.setCurrentWidget( self.landingPage ) # set the landingPage to the main window on the stackedWidget


        # Load and add the databaseExplorer page
        self.databaseExplorer = QMainWindow()  # Instantiate the databaseExplorer window
        loadUi('view/databaseExplorer.ui', self.databaseExplorer)  # Load its UI layout
        self.stackedWidget.addWidget(self.databaseExplorer)  # Add to the stacked widget

    def update_label(self, file_path):
        self.label_ruta.setText(f"Archivo seleccionado: {file_path}")
        self.boton_analizar.show()  # Show the "Analizar" button

    def run(self):
        self.show()