from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget
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

        self.backgroundLabel = QLabel(self) # Background label setup
        pixmap = QPixmap("../assets/background.png")

        cropRect = QRect(300, 0, pixmap.width(), int(pixmap.height())) # Define the crop area (e.g., top part of the image) QRect(x, y, width, height)
        croppedPixmap = pixmap.copy(cropRect)

        scaledPixmap = croppedPixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation) # Scale the cropped pixmap to cover the window
        self.backgroundLabel.setPixmap(scaledPixmap)
        self.backgroundLabel.resize(1080, 700)

        self.mainLayout.addWidget(self.backgroundLabel) # Add the background label as the first widget to fill the entire window

        self.overlay = QWidget(self) # Create a white-transparent overlay
        self.overlay.setAttribute(Qt.WA_TransparentForMouseEvents)  # Allow mouse events to pass through the overlay
        self.overlay.setStyleSheet("background-color: rgba(255, 255, 255, 0.5);")  # White color with 50% transparency
        self.overlay.setGeometry(self.backgroundLabel.geometry())  # Set the overlay to the same size as the background

        self.start = QPushButton("Empezar", self) # Create buttons
        self.ayuda = QPushButton("Ayuda", self)
        self.acerca = QPushButton("Acerca de", self)

        # Set buttons styles
        self.start.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; /* Green */
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049; /* Darker green */
            }
        """)

        self.buttonLayout = QVBoxLayout() # Create a layout for the button and center it
        self.buttonLayout.addWidget(self.start, alignment=Qt.AlignCenter)
        
        self.mainLayout.addLayout(self.buttonLayout) # Add the button layout on top of the main layout

        # overlayLayout = QVBoxLayout(self.backgroundLabel) # Overlay layout for buttons and labels
        # overlayLayout.setContentsMargins(0, 0, 10, 10)  # Add a small margin for the buttons if needed
        # overlayLayout.setAlignment(Qt.AlignBottom | Qt.AlignRight)  # Align to bottom-right

        # File path label and "Adjuntar archivo" button
        # self.label_ruta = QLabel("Ningún archivo seleccionado", self)
        # center_layout.addWidget(self.label_ruta, alignment=Qt.AlignCenter)

        # self.boton_adjuntar = QPushButton("Adjuntar archivo", self)
        # self.boton_adjuntar.clicked.connect(self.controller.select_file)
        # center_layout.addWidget(self.boton_adjuntar, alignment=Qt.AlignCenter)

        # # "Analizar" button on the bottom-right
        # self.boton_analizar = QPushButton("Analizar", self)
        # self.boton_analizar.clicked.connect(self.controller.analyze_file)
        # bottom_right_layout.addWidget(self.boton_analizar)
        # self.boton_analizar.hide()  # Hide initially until a file is selected

    def update_label(self, file_path):
        self.label_ruta.setText(f"Archivo seleccionado: {file_path}")
        self.boton_analizar.show()  # Show the "Analizar" button

    def run(self):
        self.show()