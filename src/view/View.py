from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget, QSpacerItem, QSizePolicy, QStackedLayout, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRect, Qt

class View(QWidget):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.initUI() # Initialize the User Interface

    def initUI(self):
        self.setWindowTitle("Análisis de datos ECC 2024")
        self.setFixedSize(1080, 700)  # On this way, u can't resize

        self.mainLayout = QVBoxLayout(self) #Main vertical layout in PyQt
        self.mainLayout.setContentsMargins(0, 0, 0, 0)  # Remove all margins
        self.mainLayout.setSpacing(0)  # Remove any spacing between widgets

        self.backgroundLabel = QLabel(self) # Background label setup (Layer #1)
        pixmap = QPixmap("../assets/background.png")
        cropRect = QRect(300, 0, pixmap.width(), int(pixmap.height())) # Define the crop area (e.g., top part of the image) QRect(x, y, width, height)
        croppedPixmap = pixmap.copy(cropRect)
        scaledPixmap = croppedPixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation) # Scale the cropped pixmap to cover the window
        self.backgroundLabel.setPixmap(scaledPixmap)
        self.backgroundLabel.resize(1080, 700)
        self.mainLayout.addWidget(self.backgroundLabel) # Add the background label as the first widget to fill the entire window

        self.overlay = QWidget(self) # Create a white-transparent overlay (Layer #2)
        self.overlay.setAttribute(Qt.WA_TransparentForMouseEvents)  # Allow mouse events to pass through the overlay
        self.overlay.setStyleSheet("background-color: rgba(255, 255, 255, 0.5);")  # White color with 50% transparency
        self.overlay.setGeometry(self.backgroundLabel.geometry())  # Set the overlay to the same size as the background

        logoLayout = QLabel()
        eCCLogo = QPixmap("../assets/logo_EEC_grande.png")  # Path to your image above the button


        buttonsLayout = QVBoxLayout() # Create buttons layout (Layer #3) 
        start = QPushButton("Empezar", self)
        xCenter = self.width() // 2 - start.width() // 2
        yCenter = self.height() // 2 - start.height() // 2
        start.move(xCenter, yCenter)
        
        buttonsLayout.addWidget(start, alignment=Qt.AlignCenter)

    def update_label(self, file_path):
        self.label_ruta.setText(f"Archivo seleccionado: {file_path}")
        self.boton_analizar.show()  # Show the "Analizar" button

    def run(self):
        self.show()