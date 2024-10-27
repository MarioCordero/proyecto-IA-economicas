from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMainWindow, QWidget, QSpacerItem, QSizePolicy, QStackedLayout, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRect, Qt
from PyQt5.uic import loadUi  # Importar loadUi desde PyQt5.uic

class View(QMainWindow):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.initUI() # Initialize the User Interface

    def initUI(self):
        loadUi('view/eccProject.ui', self) # Load the GUI on QtDesigner

    def update_label(self, file_path):
        self.label_ruta.setText(f"Archivo seleccionado: {file_path}")
        self.boton_analizar.show()  # Show the "Analizar" button

    def run(self):
        self.show()