import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class mainUI(QMainWindow):

    def __init__(self):

        # Initialize parent window object
        super(mainUI, self).__init__()

        # Initialize application window's UI
        self.initUI()


    def initUI(self):
        # Create full screen application window
        self.showFullScreen()
        self.setWindowTitle("magicMirror")

        # Make background dark
        self.setAutoFillBackground(True)
        darkPalette = self.palette()
        darkPalette.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(darkPalette)



def main():
    # Create application
    app = QApplication([])

    # Create application window
    window = mainUI()

    # Ensure a clean exit
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()



