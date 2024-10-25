import sys
from PyQt5.QtWidgets import QApplication
from controller.Controller import Controller

def main():
    # Inicializa QApplication antes de cualquier QWidget
    app = QApplication(sys.argv)

    # Crear la controladora y correr el programa
    controller = Controller()
    controller.run()

    # Ejecuta el evento de la aplicación
    sys.exit(app.exec_())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller()
    controller.run()
    sys.exit(app.exec_())