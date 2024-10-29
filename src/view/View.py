from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
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

    def run(self):
        self.show()