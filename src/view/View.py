import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class View(QWidget):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.initUI() # Initialize the User Interface

    def initUI(self):
        self.setWindowTitle("Análisis de datos ECC 2024")
        self.setGeometry(100, 100, 1080, 700)  # Set the initial size and position of the window

        self.background_label = QLabel(self) # Set the background image
        pixmap = QPixmap("../assets/background.png")
        self.background_label.setPixmap(pixmap)
        self.background_label.setScaledContents(True)
        self.background_label.setGeometry(0, 0, 1080, 700)  # Adjust to cover the entire window

        # Create layout
        self.layout = QVBoxLayout(self)

        # Create label to display selected file path
        self.label_ruta = QLabel("Ningún archivo seleccionado", self)
        self.layout.addWidget(self.label_ruta, alignment=Qt.AlignCenter)

        # Create "Adjuntar archivo" button
        self.boton_adjuntar = QPushButton("Adjuntar archivo", self)
        self.boton_adjuntar.clicked.connect(self.controller.select_file)
        self.layout.addWidget(self.boton_adjuntar, alignment=Qt.AlignCenter)

        # Create "Analizar" button
        self.boton_analizar = QPushButton("Analizar", self)
        self.boton_analizar.clicked.connect(self.controller.analyze_file)
        self.layout.addWidget(self.boton_analizar, alignment=Qt.AlignCenter)
        self.boton_analizar.hide()  # Initially hide the button until a file is selected

        self.setLayout(self.layout)

    def update_label(self, file_path):
        self.label_ruta.setText(f"Archivo seleccionado: {file_path}")
        self.boton_analizar.show()  # Show the "Analizar" button

    def run(self):
        self.show()

class Controller:
    def __init__(self):
        self.view = View(self)
        self.file_path = None
        print("Controladora construida!")

    def select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self.view, "Seleccionar archivo", "", "Archivos Excel (*.xlsx *.xls);;Todos los archivos (*)", options=options)
        if file_path:
            self.file_path = file_path  # Save the selected file path
            self.view.update_label(file_path)  # Update the view
        else:
            print("No se seleccionó ningún archivo o el archivo no existe.")

    def analyze_file(self):
        if self.file_path:
            print(f"Analizando el archivo: {self.file_path}")
            self.analyze_data(self.file_path)
        else:
            print("No se ha seleccionado ningún archivo para analizar.")

    def analyze_data(self, file_path):
        print(f"Procesando y analizando los datos del archivo {file_path}...")
        # Aquí iría la lógica de IA o procesamiento de datos

    def run(self):
        self.view.run()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = Controller()
    controller.run()
    sys.exit(app.exec_())
