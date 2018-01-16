from smartMirrorManager import *

class Weather(QWidget):
    def __init__(self):
        super(Weather, self).__init__()
        self.initUI()

    def initUI(self):
        font1 = QFont('Helvetica', large_fontsize)
        self.vbox = QVBoxLayout()
        self.temperatureLbl = QLabel()
        self.temperatureLbl.setFont(font1)
        self.temperatureLbl.setText("<font color='white'>Temperature</font>")
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.temperatureLbl)
        self.hbox.setAlignment(Qt.AlignCenter)
        self.setLayout(self.hbox)